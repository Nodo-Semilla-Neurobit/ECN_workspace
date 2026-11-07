#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: neurobit_pipboy.py (Brújula Radial de Orientación / Pip-Boy)
Función: Traduce presencias físicas a coordenadas MFN Radial Polar,
         anuncia la propia y calcula el camino de contracción radial
         hasta el centro de control c:G7. No usa el árbol como guía:
         lo usa solo como fuente de presencias a reconocer.
MFN_LOCATION: tools/
MFN_LEVEL: 3
VERSION: 0.1
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import re, sys
from pathlib import Path
from datetime import datetime

ANILLOS = ["c", "am", "na", "vi", "añ", "az", "m"]      # centro -> perímetro
BITS    = {"c":1, "am":1, "na":2, "vi":3, "añ":4, "az":5, "m":6}
OFFSET  = {"c":0, "am":1, "na":9, "vi":25, "añ":49, "az":81, "m":121}
RUMBO   = ["N","NE","E","SE","S","SW","W","NW"]          # porcion_global 0..7
RE_COORD = re.compile(r"(am|na|vi|añ|az|m):S(\d):P(\d):B(\d)")

def porcion_global(s, p): return (s-1)*2 + (p-1)
def indice_absoluto(a, s, p, b): return OFFSET[a] + porcion_global(s,p)*BITS[a] + (b-1)
def rumbo_de(s, p): return RUMBO[porcion_global(s,p) % 8]

def contraer(c):
    """Un hop hacia el centro: conserva S/P, clamp-ea B al ancho del anillo interno."""
    a, s, p, b = c
    i = ANILLOS.index(a)
    if i == 0: return None
    interno = ANILLOS[i-1]
    return ("c",0,0,0) if interno == "c" else (interno, s, p, min(b, BITS[interno]))

def camino_al_centro(c):
    ruta = [c]
    while c[0] != "c":
        c = contraer(c); ruta.append(c)
    return ruta

def fmt(c):
    return "c:G7" if c[0]=="c" else f"{c[0]}:S{c[1]}:P{c[2]}:B{c[3]}"

def leer_presencias(map_file):
    t = Path(map_file).read_text(encoding="utf-8")
    return [ (m.group(1),int(m.group(2)),int(m.group(3)),int(m.group(4)))
             for m in RE_COORD.finditer(t) ]

if __name__ == "__main__":
    estoy = ("az",3,2,2)
    if "--estoy" in sys.argv:
        m = RE_COORD.search(sys.argv[sys.argv.index("--estoy")+1])
        estoy = (m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)))
    print(f"[PIP-BOY] RUMBO {rumbo_de(estoy[1],estoy[2])} · ANILLO {estoy[0]} "
          f"· ÍNDICE {indice_absoluto(*estoy)}/169 · PRESENCIAS RECONOCIDAS: "
          f"{len(leer_presencias(sys.argv[sys.argv.index('--map')+1])) if '--map' in sys.argv else '-'}")
    for n, c in enumerate(camino_al_centro(estoy), 1):
        tag = "  <- ESTÁS AQUÍ" if n==1 else ("  <- CENTRO DE CONTROL" if c[0]=="c" else "")
        print(f"  {n}. {fmt(c)}{tag}")
