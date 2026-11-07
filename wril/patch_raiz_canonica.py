#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL
Módulo: patch_raiz_canonica.py
Función: Reescribe las líneas RAIZ auto-referenciales de los módulos wril
         para que usen wril_self_root.detectar_raiz(). Idempotente.
         Corrige el bug de anidación wril/wril/ y la deriva del mapa duplicado.
MFN_LOCATION: wril/  |  MFN_LEVEL: 2
VERSION: v1.0
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import re
from pathlib import Path
from wril_backup import resguardar
from wril_self_root import detectar_raiz

RAIZ = detectar_raiz()
DIR_WRIL = RAIZ / "wril"
RE_VIEJA = re.compile(
    r"^RAIZ = Path\(__file__\)\.resolve\(\)\.(?:parent|parents\[1\]).*$", re.M)
NUEVA = ("from wril_self_root import detectar_raiz as _raiz_canonica"
         "  # WRIL::RAIZ_CANONICA\nRAIZ = _raiz_canonica()")
SALTAR = {"wril_self_root.py", "wril_estado_real.py", "patch_raiz_canonica.py"}

def patchear():
    for f in sorted(DIR_WRIL.glob("wril_*.py")):
        if f.name in SALTAR:
            continue
        t = f.read_text(encoding="utf-8")
        if "WRIL::RAIZ_CANONICA" in t:
            print(f"[· RAIZ] {f.name}: ya canónica.")
            continue
        nuevo, n = RE_VIEJA.subn(NUEVA, t, count=1)
        if n:
            resguardar(f)
            f.write_text(nuevo, encoding="utf-8")
            print(f"[✓ RAIZ] {f.name}: RAIZ canónica inyectada.")
        else:
            print(f"[· RAIZ] {f.name}: sin línea RAIZ; sin cambios.")

if __name__ == "__main__":
    patchear()
