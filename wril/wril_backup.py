#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL (Capa de Resolución, Integridad y Circulación)
Módulo: wril_backup.py
Función: Única fuente de resguardo previo a toda mutación del workspace.
         Sentinel y PatchResolver lo consumen: cero redundancias.
MFN_LOCATION: wril/  |  MFN_LEVEL: 2
VERSION: v0.1
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import shutil
from pathlib import Path
from datetime import datetime

def resguardar(ruta: Path, directorio_backups: Path = None) -> Path:
    """Copia inmutable previa a sobrescritura/movimiento. Retorna el backup."""
    ruta = Path(ruta)
    if not ruta.exists():
        return None
    if directorio_backups is None:
        directorio_backups = ruta.parent / "backups_wril"
    directorio_backups.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    destino = directorio_backups / f"{ruta.stem}_{ts}{ruta.suffix}"
    n = 1
    while destino.exists():                      # colisión del mismo segundo
        destino = directorio_backups / f"{ruta.stem}_{ts}_{n}{ruta.suffix}"
        n += 1
    shutil.copy2(ruta, destino)
    return destino
