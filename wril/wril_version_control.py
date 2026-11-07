#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Scrum Master Engine
Módulo: neurobit_version_control.py
Función: Resguardo secuencial no destructivo, verificación de diferencias e incrementos.
"""

import os
import re
from pathlib import Path
from datetime import datetime

# Configuraciones globales normalizadas (Estilo estandarizado de Neurobit)
CADENA_VERSION = "VERSION:"
CADENA_SEPARADOR = "-" * 76

def gestionar_resguardo_y_version(ruta_archivo: Path, directorio_backups: Path) -> bool:
    """
    Verifica la existencia del archivo. Si existe, analiza su encabezado para extraer
    la versión, realiza un backup indexado incremental (v1, v2...) y prepara el archivo 
    actualizado incrementando su versión en +0.1 de forma no destructiva.
    """
    # 1. Asegurar la existencia de los directorios sagrados de resguardo
    directorio_backups.mkdir(parents=True, exist_ok=True)
    
    if not ruta_archivo.exists():
        # Caso base: El archivo es nuevo, se inicializa la estructura con v0.1
        print(f"🐣 Archivo nuevo detectado. Inicializando firmas en {ruta_archivo.name}")
        inicializar_archivo_nuevo(ruta_archivo)
        return True

    # 2. Análisis del Historial (Parser de la versión actual en el encabezado)
    contenido_actual = ruta_archivo.read_text(encoding="utf-8")
    version_actual = 0.1
    
    # Expresión regular que busca 'VERSION:\s*v(\d+\.\d+)'
    match_version = re.search(rf"{re.escape(CADENA_VERSION)}\s*v?(\d+\.\d+)", contenido_actual, re.IGNORECASE)
    if match_version:
        version_actual = float(match_version.group(1))

    # 3. Determinar el índice del próximo backup físico en disco (Evitar colisiones)
    # Emula de forma nativa tu comando secuencial 'ls | grep | sort -V | tail -1'
    proximo_indice_backup = 1
    patron_backup = re.compile(rf"^{re.escape(ruta_archivo.stem)}_v(\d+){re.escape(ruta_archivo.suffix)}$")
    
    for item in directorio_backups.iterdir():
        if item.is_file():
            match_idx = patron_backup.match(item.name)
            if match_idx:
                idx_detectado = int(match_idx.group(1))
                if idx_detectado >= proximo_indice_backup:
                    proximo_indice_backup = idx_detectado + 1

    # 4. Clonación inmutable del archivo anterior (Resguardo Preventivo)
    nombre_backup = f"{ruta_archivo.stem}_v{proximo_indice_backup}{ruta_archivo.suffix}"
    ruta_backup_final = directorio_backups / nombre_backup
    ruta_backup_final.write_text(contenido_actual, encoding="utf-8")
    print(f"🛡️ Backup secuencial cristalizado en: {ruta_backup_final} ({ruta_backup_final.stat().st_size} bytes)")

    # 5. Cálculo del incremento lógico de la versión para el nuevo encabezado
    nueva_version = round(version_actual + 0.1, 1)
    
    # Reemplazar la versión vieja por la nueva en el payload de memoria
    contenido_actualizado = re.sub(
        rf"({re.escape(CADENA_VERSION)}\s*v?)(\d+\.\d+)",
        f"\\1{nueva_version}",
        contenido_actual,
        count=1,
        flags=re.IGNORECASE
    )
    
    # 6. Escritura del nuevo estado en el archivo de trabajo
    tamanio_previo = ruta_archivo.stat().st_size
    ruta_archivo.write_text(contenido_actualizado, encoding="utf-8")
    tamanio_actual = ruta_archivo.stat().st_size
    
    print(f"⚡ Archivo de trabajo actualizado a la versión v{nueva_version}")
    print(f"📊 Control de bytes - Antes: {tamanio_previo} | Ahora: {tamanio_actual}")
    return True

def inicializar_archivo_nuevo(ruta_archivo: Path):
    """Genera un encabezado protocolar base para los nuevos archivos del ecosistema."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(f"{CADENA_SEPARADOR}\n")
        f.write(f"Ecosistema Neurobit - Estación Central\n")
        f.write(f"Archivo: {ruta_archivo.name}\n")
        f.write(f"{CADENA_VERSION} v0.1\n")
        f.write(f"Creado el: {timestamp}\n")
        f.write(f"{CADENA_SEPARADOR}\n\n")

