#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MFN_LOCATION: wril/
# MFN_LEVEL: 2
"""
Ecosistema Neurobit - WRIL
Módulo: wril_sanea_memoria.py (Saneo Automatizado de la Fritura)
Función: Implementa la política ética de 'Archivar, no borrar'. Confrina
         residuos de refactor, colisiones resueltas y duplicados en archive/legacy/.
VERSION: v1.0 (Saneo sin Amnesia)
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime
from wril_self_root import detectar_raiz

RAIZ = detectar_raiz()
HISTORIAL_PATH = RAIZ / "wril" / "wril_historial.jsonl"
ARCHIVE_LEGACY = RAIZ / "archive" / "legacy"

# Patrones de exclusión y confinamiento de fritura declarados en la arquitectura
PATRONES_FRITURA = [
    (re.compile(r".*-OLD.*", re.I),        "refactor_prev"),
    (re.compile(r".*-D\..*", re.I),       "dup_resuelto"),
    (re.compile(r".*\.pre_.*", re.I),     "parche_prev"),
    (re.compile(r".*-v0.*", re.I),        "borradores")
]

class WRILSaneaMemoria:
    def __init__(self, raiz_path=RAIZ):
        self.raiz = raiz_path
        ARCHIVE_LEGACY.mkdir(parents=True, exist_ok=True)

    def registrar_saneo(self, operacion: str, detalles: dict):
        evento = {
            "timestamp": datetime.now().isoformat(),
            "modulo": "wril_sanea_memoria",
            "operacion": operacion,
            "detalles": detalles
        }
        with open(HISTORIAL_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(evento, ensure_ascii=False) + "\n")

    def ejecutar_saneo(self, aplicar: bool = False) -> list:
        confinamientos = []
        
        for p_file in self.raiz.rglob("*"):
            partes = p_file.parts
            if (p_file.is_dir() or ".git" in partes or "node_modules" in partes or 
                "__pycache__" in partes or "backups_wril" in partes or "archive" in partes):
                continue
                
            nombre = p_file.name
            for regex, sub_carpeta in PATRONES_FRITURA:
                if regex.search(nombre):
                    target_dir = ARCHIVE_LEGACY / sub_carpeta
                    target_file = target_dir / nombre
                    
                    confinamientos.append({
                        "archivo_sucio": str(p_file.relative_to(self.raiz)),
                        "destino_confinamiento": f"archive/legacy/{sub_carpeta}/{nombre}",
                        "causa": sub_carpeta
                    })
                    
                    if aplicar:
                        target_dir.mkdir(parents=True, exist_ok=True)
                        # Movimiento físico atómico en el VFS
                        shutil.move(str(p_file), str(target_file))
                    break  # Rompe el bucle de patrones al emparejar el primero

        if confinamientos and aplicar:
            self.registrar_saneo("FRITURA_CONFINADA", {"confinamientos": confinamientos})
            # Forzar actualización del Cartógrafo Físico tras limpiar la casa
            from wril_path_map import generar_mapa
            generar_mapa(self.raiz, self.raiz / "path_map.json")
            
        return confinamientos

if __name__ == "__main__":
    saneador = WRILSaneaMemoria()
    detectados = saneador.ejecutar_saneo(aplicar=False)
    print("=== MONITOR DE MEMORIA QUIETA (SANEO) ===")
    print(f"[·] Residuos de fritura latentes detectados: {len(detectados)}")
    for d in detectados[:5]:
        print(f"    - {d['archivo_sucio']} -> {d['destino_confinamiento']}")

