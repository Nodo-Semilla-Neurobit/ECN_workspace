#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MFN_LOCATION: ./
# MFN_LEVEL: 1
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: neurobit_clipboard_core.py (v2.0 soberana)
Función: Rutas sagradas + commit transaccional WAL verificado por bytes.
         Sin polling: expone funciones puras; los radios (HID, GTK,
         adapter) invocan captura y commit como eventos.
VERSION: v2.0
"""
import os
import re
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

VARIABLE_SEPARADOR = "=" * 60
STRING_CONTADOR = "Numero de captura:"
STRING_TIMESTAMP = "Timestamp:"

RUTA_DEL_SCRIPT = Path(__file__).resolve().parent
CARPETA_DEL_PROCESO = RUTA_DEL_SCRIPT / "clipboard_captured_folder"
ARCHIVO_TEMPORAL = CARPETA_DEL_PROCESO / "archivo_temporal.tmp"
ARCHIVO_LOG_DEFINITIVO = CARPETA_DEL_PROCESO / "tesis_neurobit_ledger.log"
DIRECTORIO_BACKUPS = CARPETA_DEL_PROCESO / "backups"
CARPETA_DEL_PROCESO.mkdir(parents=True, exist_ok=True)

def ejecutar_paste_nativo() -> str:
    """Detecta la sesión (Wayland/X11) y vuelca la caché de texto."""
    sesion = os.environ.get("XDG_SESSION_TYPE", "x11").lower()
    try:
        if sesion == "wayland":
            return subprocess.check_output(
                ["wl-paste", "--type", "text/plain"],
                stderr=subprocess.DEVNULL).decode("utf-8")
        return subprocess.check_output(
            ["xclip", "-selection", "clipboard", "-o"],
            stderr=subprocess.DEVNULL).decode("utf-8")
    except Exception:
        return ""

def capturar_evento_hid() -> bool:
    contenido = ejecutar_paste_nativo()
    if not contenido.strip():
        return False
    ARCHIVO_TEMPORAL.write_text(contenido, encoding="utf-8")
    return True

def _resguardo_preventivo():
    """Backup indexado del Ledger antes de toda mutación (ética WRIL)."""
    if not ARCHIVO_LOG_DEFINITIVO.exists():
        return
    DIRECTORIO_BACKUPS.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = DIRECTORIO_BACKUPS / f"tesis_neurobit_ledger_{ts}.log"
    n = 1
    while destino.exists():
        destino = DIRECTORIO_BACKUPS / f"tesis_neurobit_ledger_{ts}_{n}.log"
        n += 1
    shutil.copy2(ARCHIVO_LOG_DEFINITIVO, destino)

def obtener_siguiente_indice() -> int:
    """Parser inverso stateless: últimos 4KB del Ledger."""
    if not ARCHIVO_LOG_DEFINITIVO.exists() or \
       ARCHIVO_LOG_DEFINITIVO.stat().st_size == 0:
        return 1
    patron = re.compile(rf"{re.escape(STRING_CONTADOR)}\s*(\d+)", re.IGNORECASE)
    with open(ARCHIVO_LOG_DEFINITIVO, "rb") as f:
        f.seek(max(0, ARCHIVO_LOG_DEFINITIVO.stat().st_size - 4096))
        bloque = f.read(4096).decode("utf-8", errors="ignore")
    nums = patron.findall(bloque)
    return int(nums[-1]) + 1 if nums else 1

def ejecutar_commit_verificado() -> bool:
    """Volcado WAL: purga el temporal SOLO si el Ledger creció en bytes."""
    if not ARCHIVO_TEMPORAL.exists() or ARCHIVO_TEMPORAL.stat().st_size == 0:
        return False
    _resguardo_preventivo()
    previo = ARCHIVO_LOG_DEFINITIVO.stat().st_size \
        if ARCHIVO_LOG_DEFINITIVO.exists() else 0
    indice = obtener_siguiente_indice()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    datos = ARCHIVO_TEMPORAL.read_text(encoding="utf-8")
    with open(ARCHIVO_LOG_DEFINITIVO, "a", encoding="utf-8") as f:
        f.write(f"\n{VARIABLE_SEPARADOR}\n")
        f.write(f"{STRING_CONTADOR} {indice}\n")
        f.write(f"{STRING_TIMESTAMP} {ts}\n")
        f.write(f"{VARIABLE_SEPARADOR}\n")
        f.write(datos)
        f.write("\n")
    actual = ARCHIVO_LOG_DEFINITIVO.stat().st_size
    if actual > previo:
        ARCHIVO_TEMPORAL.write_text("", encoding="utf-8")
        return True
    raise IOError("Fallo en la confirmación del Commit: "
                  "el Ledger no incrementó su tamaño.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--capture":
        capturar_evento_hid()
    elif len(sys.argv) > 1 and sys.argv[1] == "--commit":
        ejecutar_commit_verificado()
