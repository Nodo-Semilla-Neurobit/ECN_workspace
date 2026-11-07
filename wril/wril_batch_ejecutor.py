#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL
Módulo: wril_batch_executor.py (Brazo Operativo)
Función: Ejecuta secuencias declaradas sobre targets resueltos por el
         PathResolver. Periferia operacional del núcleo de resolución:
         RESOLVER -> TARGETS -> OPERATIONS -> REPORT (carta sellada).
MFN_LOCATION: wril/  |  MFN_LEVEL: 2
VERSION: v0.1
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import subprocess
import json
from pathlib import Path
from datetime import datetime
from wril_path_resolver import PathResolver

from wril_self_root import detectar_raiz as _raiz_canonica  # WRIL::RAIZ_CANONICA
RAIZ = _raiz_canonica()

def ejecutar_secuencia(operaciones: list, resolver=None) -> list:
    """op = {"tipo": "shell"|"python", "target": nombre, "args": [...]}"""
    resolver = resolver or PathResolver(RAIZ)
    reporte = []
    for op in operaciones:
        entrada = {"op": op.get("target", op.get("args", ["?"])[0]),
                   "t": datetime.now().isoformat(), "ok": False}
        try:
            if op["tipo"] == "shell":
                r = subprocess.run(op["args"], capture_output=True, text=True, timeout=60)
            else:
                ruta = resolver.resolve(op["target"])    # RESOLVER -> TARGET
                r = subprocess.run(["python3", str(ruta)] + op.get("args", []),
                                   capture_output=True, text=True, timeout=120)
            entrada["ok"] = r.returncode == 0
            entrada["salida"] = r.stdout[-400:]
        except Exception as e:
            entrada["error"] = str(e)
        reporte.append(entrada)
    return reporte

def asentar_reporte(reporte: list):
    """El reporte viaja como carta: la Oficina lo enruta a memoria."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    buz = RAIZ / "buzon_salida"
    buz.mkdir(parents=True, exist_ok=True)
    (buz / f"carta_wril_batch_{ts}.txt").write_text(
        "|=•'wril'•=|»|['batch_reporte'.]\n"
        + json.dumps(reporte, ensure_ascii=False, indent=1)
        + "\n[.'batch_reporte']|«|=•'wril'•=|", encoding="utf-8")

if __name__ == "__main__":
    rep = ejecutar_secuencia([
        {"tipo": "python", "target": "wril_path_map.py"},
        {"tipo": "python", "target": "wril_dependency_scanner.py"},
        {"tipo": "python", "target": "wril_mfn_registry.py"},
    ])
    asentar_reporte(rep)
    print("[✓ BATCH] Secuencia ejecutada; reporte asentado en buzón.
