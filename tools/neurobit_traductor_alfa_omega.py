#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: tools/neurobit_traductor_alfa_omega.py
Función: Traductor ALFA<->OMEGA. Convierte glifos 8x8 ([ ],[0],[1],[█])
         a lineas de 8 bits, a pares de neuronibbles SINCERO (sin cero:
         valor+1 en hex, etiquetas 1..9,A..G), y viceversa.
         Un glifo 8x8 = 8 bytes = 16 simbolos SINCERO.
MFN_LOCATION: tools/
MFN_LEVEL: 3
VERSION: v0.1
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

TABLA = "123456789ABCDEFG"          # SINCERO: valor+1 en hex; el cero no se nombra

def linea_a_bits(linea):
    out = []
    for tok in linea.replace("[", " ").split():
        t = tok.strip("[]")
        out.append("1" if t in ("1", "█") else "0")
    return "".join(out)

def bits_a_simbolos(bits):
    return [TABLA[int(bits[i:i+4], 2)] for i in (0, 4)]

def glifo_a_sincero(glifo_8x8):
    return [bits_a_simbolos(linea_a_bits(l)) for l in glifo_8x8 if l.strip()]

def simbolo_a_bits(s):
    v = TABLA.index(s)
    return format(v, "04b")

def sincero_a_linea(par):
    return simbolo_a_bits(par[0]) + simbolo_a_bits(par[1])

ALFA, OMEGA = "00000000", "11011011"   # 0x00 latente / 0xDB manifiesto c/ mortero

if __name__ == "__main__":
    for nombre, linea in (("ALFA", ALFA), ("OMEGA", OMEGA)):
        print(f"{nombre}: {linea} -> 0x{int(linea,2):02X} -> SINCERO {bits_a_simbolos(linea)}")
