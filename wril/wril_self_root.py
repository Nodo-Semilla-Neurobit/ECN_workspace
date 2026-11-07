#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL
Módulo: wril_self_root.py (Capa 0 de direccionamiento)
Función: "Where am I?" canónico. Detecta la raíz del workspace por
         marcadores (buzon_salida/, pids/, deploy_neurobit_estacion*.sh)
         ascendiendo desde este archivo. Inmune al pliegue: funciona
         desde raíz, wril/ o wril/wril/.
MFN_LOCATION: wril/  |  MFN_LEVEL: 2
VERSION: v2.1
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

from pathlib import Path

SELLO = "where_am_I.inf"
MARCADORES_FUERTES = ("buzon_salida", "pids")
MARCADORES_DEBILES = ("wril", "core", "README_ECN_Workspace_Canonico_v3.md")

def detectar_raiz() -> Path:
    p = Path(__file__).resolve().parent
    for candidato in (p, *p.parents):          # 1) sello persistido
        if (candidato / SELLO).exists():
            return candidato
    for candidato in (p, *p.parents):          # 2) conjunción fuerte
        if all((candidato / m).exists() for m in MARCADORES_FUERTES):
            return candidato
    for candidato in (p, *p.parents):          # 3) conjunción débil (alias)
        if all((candidato / m).exists() for m in MARCADORES_DEBILES):
            return candidato
    return p

RAIZ = detectar_raiz()

if __name__ == "__main__":
    print(f"[✓ RAIZ] {RAIZ}")
