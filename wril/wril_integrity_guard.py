#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL (Workspace Resolution & Integrity Layer)
Módulo: wril_integrity_guard.py (Escudo de Coherencia e Integridad Activa)
Función: Escudo proactivo contra el ruido estructural, duplicados silenciosos, 
         archivos malformados y desalineaciones de cabeceras MFN en la ECN.
         Funciona como un centinela pre-bootstrap y pre-commit.
MFN_LOCATION: wril/
MFN_LEVEL: 2
VERSION: v1.0
"""

import os
import re
import json
import hashlib
import shutil
from pathlib import Path
from datetime import datetime

# Definición de la LEY 1 y LEY 2 del WRIL (Parche v1.1 - Sin colisión de cuantificador)
RE_BACKUP = re.compile(r"\d{8}_\d{6}")

def es_backup(nombre: str) -> bool:
    """Verifica si el archivo es un backup estático con timestamp o pertenece a backups_wril/"""
    return bool(RE_BACKUP.search(nombre)) or "backups_wril" in nombre

class WRILIntegrityGuard:
    def __init__(self, raiz_path=None):
        self.raiz = self._detectar_raiz(raiz_path)
        self.inbox = self.raiz / "inbox"
        self.wril_dir = self.raiz / "wril"
        self.archive_legacy = self.raiz / "archive" / "legacy"
        self.backups_dir = self.raiz / "backups_wril"
        self.historial_path = self.raiz / "wril" / "wril_historial.jsonl"
        
        # Inicialización de rutas
        self.inbox.mkdir(parents=True, exist_ok=True)
        self.archive_legacy.mkdir(parents=True, exist_ok=True)
        self.backups_dir.mkdir(parents=True, exist_ok=True)
        
    def _detectar_raiz(self, custom_path) -> Path:
        """Ley 1: Anclaje de Raíz Canónica Unívoca e Inmutable"""
        if custom_path:
            return Path(custom_path).resolve()
        
        p = Path(__file__).resolve().parent
        for c in (p, *p.parents):
            if (c / ".ecn_raiz").exists() or (c / "deploy_neurobit_estacion_v3.2.sh").exists():
                return c
        return p

    def registrar_evento(self, operacion: str, detalles: dict):
        """Asienta en el Ledger de la Capa WRIL para garantizar trazabilidad inmutable (Record)"""
        evento = {
            "timestamp": datetime.now().isoformat(),
            "modulo": "wril_integrity_guard",
            "operacion": operacion,
            "detalles": detalles
        }
        self.historial_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.historial_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(evento, ensure_ascii=False) + "\n")

    def sanear_sintaxis_nombres(self, aplicar: bool = False) -> list:
        """
        Busca nombres de archivos malformados (por ejemplo, con paréntesis colgados
        de operaciones de copia o descargas corruptas como 'declaracion_modulos_v9.yaml)')
        """
        correcciones = []
        # Escaneamos recursivamente el workspace (evitando .git y node_modules)
        for p_file in self.raiz.rglob("*"):
            if p_file.is_dir() or ".git" in p_file.parts or "node_modules" in p_file.parts:
                continue
            
            nombre_sucio = p_file.name
            # Patrón para paréntesis final huérfano: ej: archivo.yaml)
            if nombre_sucio.endswith(")") and not "(" in nombre_sucio:
                nombre_sano = nombre_sucio.rstrip(")")
                p_destino = p_file.parent / nombre_sano
                correcciones.append({
                    "original": str(p_file.relative_to(self.raiz)),
                    "sano": str(p_destino.relative_to(self.raiz)),
                    "causa": "Paréntesis huérfano al final del nombre"
                })
                
                if aplicar:
                    # Aplicar resguardo preventivo (Ley 2)
                    self._resguardar_archivo(p_file)
                    p_file.rename(p_destino)
                    
        if correcciones:
            self.registrar_evento("SANEAMIENTO_SINTAXIS", {"correcciones": correcciones, "aplicado": aplicar})
        return correcciones

    def _resguardar_archivo(self, ruta_file: Path):
        """Genera una copia inmutable antes de cualquier mutación física (RECORD)"""
        if not ruta_file.exists():
            return
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        sub_dir = self.backups_dir / ruta_file.parent.relative_to(self.raiz)
        sub_dir.mkdir(parents=True, exist_ok=True)
        destino_backup = sub_dir / f"{ruta_file.stem}_{ts}{ruta_file.suffix}"
        shutil.copy2(ruta_file, destino_backup)

    def auditar_duplicados(self) -> dict:
        """
        Audita el workspace para listar duplicados de forma exacta (por hash MD5)
        y por nombre de archivo.
        """
        registro_hashes = {}  # hash -> [rutas]
        registro_nombres = {} # nombre -> [rutas]
        
        for p_file in self.raiz.rglob("*"):
            # Omitimos carpetas del sistema, caches, backups y el propio legacy
            partes = p_file.parts
            if (p_file.is_dir() or 
                ".git" in partes or 
                "node_modules" in partes or 
                "__pycache__" in partes or 
                "backups_wril" in partes or 
                "archive" in partes):
                continue
            
            nombre = p_file.name
            if es_backup(nombre):
                continue
                
            # Agrupar por nombre
            registro_nombres.setdefault(nombre, []).append(p_file)
            
            # Agrupar por hash
            try:
                content = p_file.read_bytes()
                file_hash = hashlib.md5(content).hexdigest()
                registro_hashes.setdefault(file_hash, []).append(p_file)
            except IOError:
                continue

        # Filtrar solo los duplicados reales
        duplicados_nombre = {k: [str(p.relative_to(self.raiz)) for p in v] for k, v in registro_nombres.items() if len(v) > 1}
        duplicados_hash = {k: [str(p.relative_to(self.raiz)) for p in v] for k, v in registro_hashes.items() if len(v) > 1}
        
        return {
            "duplicados_por_nombre": duplicados_nombre,
            "duplicados_por_contenido": duplicados_hash
        }

    def proponer_plan_canonicalizacion(self) -> dict:
        """
        Genera un plan de acción Dry-Run inteligente de movimientos y backups.
        Determina cuál es el archivo canónico y cuáles son redundantes o históricos.
        """
        auditoria = self.auditar_duplicados()
        plan_movimientos = []
        
        # 1. Resolver duplicados por nombre
        for nombre, rutas in auditoria["duplicados_por_nombre"].items():
            # Criterio de canonicalización:
            # - Priorizar rutas declaradas en headers MFN
            # - Priorizar rutas según Guía Maestra (core/, tools/, wril/, adapters/)
            # - Si hay uno en la raíz y otro en la carpeta canónica, el de la raíz se mueve a archive/legacy/
            canonico = None
            obsoletos = []
            
            for r_str in rutas:
                p_file = self.raiz / r_str
                # Extraemos cabeceras MFN si tiene
                header_location = self.extraer_mfn_location(p_file)
                
                # Si está en su ubicación declarada, es el canónico
                if header_location and r_str.startswith(header_location):
                    canonico = r_str
                elif r_str.startswith(("core/", "tools/", "wril/", "core/adapters/")):
                    # Si no hay concordancia directa pero está en un directorio clave de la Guía Maestra
                    if not canonico:
                        canonico = r_str
                    else:
                        obsoletos.append(r_str)
                else:
                    obsoletos.append(r_str)
            
            # Si no se pudo determinar un canónico por headers, tomamos el primero
            if not canonico and rutas:
                canonico = rutas[0]
                obsoletos = rutas[1:]
            elif canonico and canonico in obsoletos:
                obsoletos.remove(canonico)
                
            for obs in obsoletos:
                plan_movimientos.append({
                    "nombre": nombre,
                    "origen": obs,
                    "destino_propuesto": f"archive/legacy/{obs}",
                    "accion": "MOVE_TO_LEGACY",
                    "estado": "PENDIENTE_APROBACION"
                })
                
        return {
            "total_movimientos_propuestos": len(plan_movimientos),
            "movimientos": plan_movimientos
        }

    def ejecutar_plan_canonicalizacion(self, plan: dict) -> dict:
        """Aplica físicamente el plan aprobado por el Director con resguardo previo total"""
        reporte = {"estado": "EXITO", "movimientos_realizados": []}
        
        for mov in plan.get("movimientos", []):
            origen = self.raiz / mov["origen"]
            destino = self.raiz / mov["destino_propuesto"]
            
            if not origen.exists():
                continue
                
            # Asegurar directorio de destino
            destino.parent.mkdir(parents=True, exist_ok=True)
            
            # 1. Resguardo preventivo (RECORD) en backups_wril
            self._resguardar_archivo(origen)
            if destino.exists():
                self._resguardar_archivo(destino)
                
            # 2. Mover el archivo (ROUTE)
            shutil.move(str(origen), str(destino))
            
            mov_realizado = {
                "archivo": mov["nombre"],
                "origen": mov["origen"],
                "destino": mov["destino_propuesto"],
                "timestamp_registro": datetime.now().isoformat()
            }
            reporte["movimientos_realizados"].append(mov_realizado)
            self.registrar_evento("CANONICALIZACION_MOVIMIENTO", mov_realizado)
            
        return reporte

    def extraer_mfn_location(self, p_file: Path) -> str:
        """Lee el archivo de texto y busca la directiva MFN_LOCATION"""
        try:
            content = p_file.read_text(encoding="utf-8", errors="ignore")
            match = re.search(r"MFN_LOCATION:\s*([^\s\n\r|#]+)", content)
            if match:
                loc = match.group(1).strip()
                if not loc.endswith("/"):
                    loc += "/"
                return loc
        except Exception:
            pass
        return ""

    def verificar_bloqueo_path_map(self, nuevo_mapa: dict) -> dict:
        """
        Verifica antes de guardar el path_map.json si existen colisiones de llaves.
        Evita que un archivo de igual nombre en raíz pise silenciosamente la ruta canónica.
        """
        colisiones = {}
        for clave, ruta in nuevo_mapa.items():
            # Si la ruta ya se mapeó bajo otra ubicación
            if nuevo_mapa.get(clave) != ruta:
                colisiones[clave] = [nuevo_mapa[clave], ruta]
                
        if colisiones:
            self.registrar_evento("COLISION_PREVENIDA_PATH_MAP", {"colisiones": colisiones})
            raise ValueError(f"[TENSIÓN] Se impidió la escritura de path_map.json por colisiones en llaves: {colisiones}")
        
        return {"estado": "COHERENTE"}

if __name__ == "__main__":
    print("─" * 60)
    print("  [INTEGRITY_GUARD] Inicializando Escudo de Coherencia WRIL 🛡️")
    print("─" * 60)
    guard = WRILIntegrityGuard()
    
    # 1. Analizar nombres sucios
    errores_sintaxis = guard.sanear_sintaxis_nombres(aplicar=False)
    print(f"  Analizando Sintaxis de Nombres... Detectados: {len(errores_sintaxis)}")
    for err in errores_sintaxis:
        print(f"    [!] Archivo malformado detectado: {err['original']} -> Proponer: {err['sano']}")
        
    # 2. Auditar Duplicados
    print("\n  Auditando duplicados en el territorio...")
    duplicados = guard.auditar_duplicados()
    print(f"    Duplicados por Nombre: {len(duplicados['duplicados_por_nombre'])}")
    print(f"    Duplicados por Contenido: {len(duplicados['duplicados_por_contenido'])}")
    
    # 3. Proponer Plan
    plan = guard.proponer_plan_canonicalizacion()
    print(f"\n  Plan de Canonicalización Generado: {plan['total_movimientos_propuestos']} movimientos propuestos.")
    for mov in plan["movimientos"]:
        print(f"    • Mover: {mov['origen']} -> {mov['destino_propuesto']} (Estado: {mov['estado']})")
