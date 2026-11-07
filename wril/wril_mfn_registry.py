#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL
Módulo: wril_mfn_registry.py
Función: Interpreta la identidad declarada (MFN_LOCATION/LEVEL/COORD).
         Detecta DECLARACIÓN ≠ REALIDAD como señal de integridad.
         NO fusionar con path_map: preguntas distintas, módulos distintos.
MFN_LOCATION: wril/  |  MFN_LEVEL: 2
VERSION: v0.1
##NB::HERENCIA::metricas_v02 <- 2ebebde0
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import re
from pathlib import Path

from wril_self_root import detectar_raiz as _raiz_canonica  # WRIL::RAIZ_CANONICA
RAIZ = _raiz_canonica()
EXT = ('.py', '.sh', '.js', '.md', '.yaml', '.c')
RE_MEMORIA = re.compile(r"(-D|-R_\d+|_20\d{6}(_\d{6})+)$")
DIRS_QUIETOS = {'inbox', 'backups_wril', 'archive',
                'compendio_workspaces', '.venv',
                'node_modules', '.git',
                'INSTALACION_', 'MD'}
RE_MFN = re.compile(
    r"MFN_LOCATION:\s*(\S+).*?MFN_LEVEL:\s*(\d+)"
    r"(?:.*?MFN_COORD:\s*\((\d+),\s*(\d+)\))?", re.DOTALL)

def escanear_identidades(root: Path = RAIZ) -> dict:
    indice = {}
    for f in root.rglob("*"):
        if not f.is_file() or f.suffix not in EXT:
            continue
        if RE_MEMORIA.search(f.stem):
            continue
        if set(f.relative_to(root).parts[:-1]) & DIRS_QUIETOS:
            continue
        m = RE_MFN.search(f.read_text(encoding="utf-8", errors="ignore")[:500])
        if m:
            indice[str(f.relative_to(root))] = {
                "location": m.group(1), "level": int(m.group(2)),
                "coord": (int(m.group(3)), int(m.group(4))) if m.group(3) else None}
    return indice

def auditar_declaraciones(root: Path = RAIZ) -> dict:
    """La tensión DECLARACIÓN ≠ REALIDAD, como señal de integridad."""
    reporte = {"coherentes": [], "inconsistentes": []}
    for rel, meta in escanear_identidades(root).items():
        realidad = Path(rel).parent.as_posix()
        realidad = "" if realidad == "." else realidad.rstrip("/")
        declarada = str(meta["location"]).strip()
        declarada = "" if declarada in ("./", ".") else declarada.rstrip("/")
        if realidad == declarada:
            reporte["coherentes"].append(rel)
        else:
            reporte["inconsistentes"].append(
                {"archivo": rel, "declara": declarada, "realidad": realidad})
    return reporte

if __name__ == "__main__":
    r = auditar_declaraciones()
    print(f"[✓ REGISTRY] Coherentes: {len(r['coherentes'])} | "
          f"Pendientes de pliegue topológico: {len(r['inconsistentes'])}")
    for inc in r["inconsistentes"][:10]:
        print(f"    {inc['archivo']}: declara {inc['declara']} / vive en {inc['realidad'] or './'}")

