#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL
Módulo: wril_dependency_scanner.py
Función: Determina QUÉ NECESITA el workspace: genera
         requirements_dynamic.txt (Python de terceros) y
         system_deps_check.txt (libs/binarios de sistema).
MFN_LOCATION: wril/  |  MFN_LEVEL: 2
VERSION: v0.1
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import re
import sys
from pathlib import Path

from wril_self_root import detectar_raiz as _raiz_canonica  # WRIL::RAIZ_CANONICA
RAIZ = _raiz_canonica()
try:
    STDLIB = set(sys.stdlib_module_names)          # py3.10+
except AttributeError:
    STDLIB = {"os","re","json","sys","struct","shutil","ctypes","glob","math",
              "hashlib","subprocess","threading","signal","time","datetime",
              "pathlib","typing","importlib","inspect","queue","socket","urllib"}

RE_IMPORT = re.compile(r"^\s*(?:import|from)\s+([a-zA-Z_][a-zA-Z0-9_]*)", re.M)

MAPEO_SISTEMA = [
    (r"#include\s*<X11/",            "libx11-dev (Xlib)"),
    (r"^\s*(import|from) gi\b",      "python3-gi + gir1.2-gtk-3.0"),
    (r"^\s*(import|from) evdev\b",   "python3-evdev + modprobe uinput"),
    (r"^\s*(import|from) flask\b",   "python3-flask"),
    (r"^\s*(import|from) yaml\b",    "python3-yaml"),
    (r"^\s*(import|from) psutil\b",  "python3-psutil"),
    (r"^\s*(import|from) requests\b","python3-requests"),
    (r"\bgcc\b",                     "build-essential (gcc)"),
]

def locales():
    return {p.name for p in RAIZ.rglob("*.py")} | {p.stem for p in RAIZ.rglob("*.py")}

def escanear():
    terceros, sistema = set(), set()
    for f in RAIZ.rglob("*"):
        if not f.is_file() or f.suffix not in ('.py', '.c', '.sh'):
            continue
        texto = f.read_text(encoding="utf-8", errors="ignore")
        if f.suffix == ".py":
            for mod in RE_IMPORT.findall(texto):
                if mod not in STDLIB and mod not in locales():
                    terceros.add(mod)
        for patron, dep in MAPEO_SISTEMA:
            if re.search(patron, texto, re.M):
                sistema.add(dep)
    return sorted(terceros), sorted(sistema)

def generar():
    terceros, sistema = escanear()
    (RAIZ / "requirements_dynamic.txt").write_text(
        "# Generado por wril_dependency_scanner (cruce vs stdlib + locales)\n"
        + "".join(f"{t}\n" for t in terceros), encoding="utf-8")
    (RAIZ / "system_deps_check.txt").write_text(
        "# Verificación de entorno previa al deploy\n"
        + "".join(f"{s}\n" for s in sistema), encoding="utf-8")
    print(f"[✓ SCANNER] Terceros: {len(terceros)} | Sistema: {len(sistema)}")

if __name__ == "__main__":
    generar()
