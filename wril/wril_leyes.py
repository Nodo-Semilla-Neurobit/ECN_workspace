#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL
Módulo: wril_leyes.py (Las Leyes de la Estación — invariantes operativos)
Función: Ancla canónica de raíz, exclusión de backups del pliegue, y
         guarda de convergencia. Estas leyes NO viajaron en la semilla v1;
         por eso el nodo nuevo actuó por defecto y rompió los invariantes.
MFN_LOCATION: wril/
MFN_LEVEL: 0
VERSION: v1.0
"""
import re
from pathlib import Path

# LEY 1 — RAÍZ ÚNICA E INMUTABLE.
# El ancla es algo que el pliegue NUNCA mueve ni replica: el deploy maestro
# o el marcador .ecn_raiz escrito UNA vez a mano del NODO_SEMILLA.
def raiz_canonica() -> Path:
    p = Path(__file__).resolve().parent
    for c in (p, *p.parents):
        if (c / ".ecn_raiz").exists() or \
           (c / "deploy_neurobit_estacion_v3.2.sh").exists():
            return c
    return p

RAIZ = raiz_canonica()

# LEY 2 — LA PRESERVACIÓN JAMÁS SE PLIEGA.
# Un backup con sello de tiempo es memoria quieta, no artefacto móvil.
RE_BACKUP = re.compile(r"_20\d{6}(_\d{6})+")
def es_backup(nombre: str) -> bool:
    return bool(RE_BACKUP.search(nombre)) or "backups_wril" in str(nombre)

# LEY 3 — CONVERGENCIA. El pliegue debe REDUCIR la tensión.
# Si después de plegar la tensión sube, el pliegue diverge: abortar y reportar.
def guarda_convergencia(antes: int, despues: int) -> bool:
    return despues <= antes
