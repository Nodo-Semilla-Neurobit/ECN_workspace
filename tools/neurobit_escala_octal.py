#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: tools/neurobit_escala_octal.py
Función: La escalera octal del paquete MFN. Verifica la cadena de
         potencias de 2 descubierta por el NODO_SEMILLA y la desciende
         hasta el observador. El octal expone el esqueleto 2^k que el
         decimal esconde. Juego matemático asentado como módulo.
MFN_LOCATION: tools/
MFN_LEVEL: 3
VERSION: v0.1
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

NUMPAD = [[7, 8, 9], [4, 5, 6], [3, 2, 1]]   # brújula física: 8 rumbos + 5 observador
CUERPO = 169 - 9                              # 160 bits viajan; la brújula se comparte

PELDANOS = [
    (160, "cuerpo del paquete (169 - 9 del numpad raiz)"),
    (136, "cuerpo por estado del numpad (2^160 / 8^8)"),
    (68,  "raiz cuadrada (mitad del exponente)"),
    (34,  "raiz cuadrada otra vez"),
    (26,  "div 2^8 (un byte) -> 4 x 8^8"),
    (13,  "raiz: el exponente es el ORDEN del toro Z13"),
    (12,  "div 2: la OCTAVA temperada (12 semitonos)"),
    (6,   "raiz: 2^6 = 64 = glifo 8x8 del C64"),
    (3,   "raiz: 2^3 = 8 = porcion / digito octal / rumbo"),
    (0,   "div 8: 2^0 = 1 = observador c:G7"),
]

def verificar():
    assert 8 ** 8 == 16777216 == (1 << 24)
    assert (1 << 160) // (8 ** 8) == (1 << 136)
    assert (1 << 136) == 87112285931760246646623899502532662132736
    assert (1 << 68) == 295147905179352825856
    assert (1 << 34) == 17179869184
    assert (1 << 26) == 67108864
    assert CUERPO == 160
    return True

if __name__ == "__main__":
    verificar()
    print("[✓ ESCALA] La cuenta del NODO es correcta. Desciendo:")
    for exp, nota in PELDANOS:
        val = 1 << exp
        print(f"  2^{exp:<3} = {oct(val)[2:]:>46}  | {nota}")
    print(f"[✓ BRUJULA] numpad compartido (no viaja): {NUMPAD[0]} / {NUMPAD[1]} / {NUMPAD[2]}")
