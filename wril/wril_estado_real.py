#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL (Capa de Resolución, Integridad y Circulación)
Módulo: wril_estado_real.py
Función: Verdad de estado para el salón. Reporta ALIVE/DEAD real de los
         componentes soberanos vía pidfile + os.kill(pid,0), con fallback
         pgrep. Escribe estado_real.json que el dashboard consume.
         El salón jamás simula estado: lo consulta.
MFN_LOCATION: wril/  |  MFN_LEVEL: 2
VERSION: v0.1
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent if (AQUI.name == "wril" and (AQUI.parent / "pids").exists()) else AQUI

COMPONENTES = [
    ("WS_SENTINEL",    "sentinel.pid",   "wril_sentinel"),
    ("DISPATCHER",     "dispatcher.pid", "neurobit_dispatcher"),
    ("VISOR_SOBERANO", "widget.pid",     "neurobit_gnome_widget"),
    ("DICTAFONO",      "dictado.pid",    "neurobit_dictado_evdev"),
]

def esta_vivo(pid):
    try:
        os.kill(pid, 0)
        return True
    except Exception:
        return False

def estado_real():
    reporte = {"t": datetime.now().isoformat(), "componentes": []}
    for nombre, pidfile, patron in COMPONENTES:
        pid = None
        pf = RAIZ / "pids" / pidfile
        if pf.exists():
            try:
                pid = int(pf.read_text().strip())
            except Exception:
                pid = None
        vivo = pid is not None and esta_vivo(pid)
        if not vivo:
            try:
                out = subprocess.run(["pgrep", "-f", patron],
                                     capture_output=True, text=True)
                vivo = out.returncode == 0
                pid = int(out.stdout.split()[0]) if vivo else None
            except Exception:
                pass
        reporte["componentes"].append(
            {"nombre": nombre, "pid": pid,
             "estado": "ALIVE" if vivo else "DEAD"})
    return reporte

if __name__ == "__main__":
    rep = estado_real()
    (RAIZ / "estado_real.json").write_text(json.dumps(rep, indent=1), encoding="utf-8")
    for c in rep["componentes"]:
        print(f"[✓ ESTADO] {c['nombre']}: {c['estado']} (pid {c['pid']})")
