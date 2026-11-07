#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL
Módulo: wril_bootstrap.py (Ritual de sincronización previa al despertar)
Función: Proceso inicial de toda tarea: 1) regenera path_map;
         2) PatchResolver dry-run sobre los .sh (referencias obsoletas);
         3) dependency scanner. Rescate canonizado de bootstrap.py.
MFN_LOCATION: wril/  |  MFN_LEVEL: 2
VERSION: v0.1
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

from pathlib import Path
from wril_path_map import generar_mapa
from wril_patch_resolver import PatchResolver
from wril_dependency_scanner import generar as generar_deps
from wril_root_alias import resolve_ecn_root

RAIZ = resolve_ecn_root()  # WRIL::RAIZ_CANONICA

def ritual():
    print("[0.1 WRIL] Regenerando path_map.json...")
    mapa = generar_mapa(RAIZ, RAIZ / "path_map.json")
    print(f"[✓ WRIL] Índice construido: {len(mapa)} artefactos.")
    print("[0.2 WRIL] PatchResolver (dry-run) sobre scripts .sh ...")
    pr = PatchResolver(RAIZ)
    for script in sorted(RAIZ.glob("*.sh")):
        rep = pr.reconcile(script, dry_run=True)
        if rep["cambios"]:
            print(f"    [⚠ REFERENCIA] {script.name}: {len(rep['cambios'])} obsoletas (sin mutar)")
        else:
            print(f"    [✓ REFERENCIA] {script.name}: coherente.")
    print("[0.3 WRIL] Dependency scanner...")
    generar_deps()
    print("[✓ WRIL] Bootstrap completo: topología y estado coinciden.")

if __name__ == "__main__":
    ritual()
