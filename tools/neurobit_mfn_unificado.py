#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: neurobit_mfn_unificado.py
Función: Tesis v2.0 — Unificación de las tres proyecciones de la MFN:
         (A) Cartógrafo radial polar (169 bits, 7 anillos x 8 porciones),
         (B) Toro algebraico Z13xZ13 (rho, phi),
         (C) Anexo musical (semitono, octava).
         La grilla cartesiana 13x13 es la carta de transicion.
MFN_LOCATION: tools/
MFN_LEVEL: 3
VERSION: v2.0
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import math

MATRIX_SIZE = 13
CENTER = 6
TOTAL_BITS = 169
ANILLOS = ["c", "am", "na", "vi", "añ", "az", "m"]
BITS_POR_PORCION = {"c": 1, "am": 1, "na": 2, "vi": 3, "añ": 4, "az": 5, "m": 6}
TOTAL_POR_ANILLO = {a: (1 if a == "c" else 8 * BITS_POR_PORCION[a]) for a in ANILLOS}
OFFSET = {}
_acc = 0
for _a in ANILLOS:
    OFFSET[_a] = _acc
    _acc += TOTAL_POR_ANILLO[_a]
NOTAS = ["La", "La#", "Si", "Do", "Do#", "Re", "Re#", "Mi", "Fa", "Fa#", "Sol", "Sol#"]

# --- Carta A: Cartografo radial (celda <- indice) ---
def _celda_de_radial(anillo, sector, porcion, bit):
    if anillo == "c":
        return (CENTER, CENTER)
    r = ANILLOS.index(anillo)
    gp = (sector - 1) * 2 + (porcion - 1)
    s = bit - 1
    return {0: (CENTER-r, CENTER+s), 1: (CENTER-r+s, CENTER+r),
            2: (CENTER+s, CENTER+r), 3: (CENTER+r, CENTER+r-s),
            4: (CENTER+r, CENTER-s), 5: (CENTER+r-s, CENTER-r),
            6: (CENTER-s, CENTER-r), 7: (CENTER-r, CENTER-r+s)}[gp]

_CELDA_A_INDICE = {}
_INDICE_A_CELDA = {}
_idx = 0
for _a in ANILLOS:
    if _a == "c":
        _CELDA_A_INDICE[(CENTER, CENTER)] = 0
        _INDICE_A_CELDA[0] = (CENTER, CENTER)
        continue
    r = ANILLOS.index(_a)
    for sec in range(1, 5):
        for por in range(1, 3):
            for b in range(1, r + 1):
                celda = _celda_de_radial(_a, sec, por, b)
                _CELDA_A_INDICE[celda] = _idx
                _INDICE_A_CELDA[_idx] = celda
                _idx += 1

def indice_a_radial(idx):
    row, col = _INDICE_A_CELDA[idx]
    r = max(abs(row-CENTER), abs(col-CENTER))
    anillo = ANILLOS[r]
    for sec in range(1, 5):
        for por in range(1, 3):
            for b in range(1, (r or 1) + 1):
                if _celda_de_radial(anillo, sec, por, b) == (row, col):
                    return {"anillo": anillo, "sector": sec, "porcion": por,
                            "bit": b, "coord": f"{anillo}:S{sec}:P{por}:B{b}"}
    return {"anillo": "c", "sector": 1, "porcion": 1, "bit": 1, "coord": "c:G7"}

# --- Carta B: toro algebraico Z13xZ13 ---
def indice_a_toro(idx):
    i, j = _INDICE_A_CELDA[idx]
    return {"i": i, "j": j, "rho": i + 1, "phi": round(2*math.pi*j/13, 5)}

# --- Carta C: anexo musical ---
def indice_a_musica(idx):
    t = indice_a_toro(idx)
    i, j = t["i"], t["j"]
    if j % 13 == 12:
        return f"{NOTAS[0]}{i+1} [costura enarmonica]"
    return f"{NOTAS[j % 12]}{i}"

def puente(idx):
    """Las tres lecturas de la misma celda."""
    return {"lineal": idx, "radial": indice_a_radial(idx),
            "toro": indice_a_toro(idx), "musica": indice_a_musica(idx)}

if __name__ == "__main__":
    assert sum(TOTAL_POR_ANILLO.values()) == TOTAL_BITS == 169
    assert len(_CELDA_A_INDICE) == 169 and len(_INDICE_A_CELDA) == 169
    for muestra in (0, 1, 49, 81, 121, 168):
        p = puente(muestra)
        print(f"[{p['lineal']:3d}] {p['radial']['coord']:14s} "
              f"rho={p['toro']['rho']:2d} phi={p['toro']['phi']:.3f} -> {p['musica']}")
    print("[✓ UNIFICADO] Tres cartas, una variedad de 169 celdas.")
