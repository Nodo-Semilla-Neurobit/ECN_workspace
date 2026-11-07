#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: tools/neurobit_pesos_binarios.py
Función: La respiración de la matriz. Tabla de pesos binarios C(n,k),
         factor de herencia (n-k)/(k+1), ecuador de paridad y huella
         conceptual por neuronibbles (peso, no glifo).
MFN_LOCATION: tools/
MFN_LEVEL: 3
VERSION: v0.1
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

from math import comb

def factor_herencia(n, k):
    """El paso k+1 hereda del paso k multiplicando por (n-k)/(k+1)."""
    return (n - k, k + 1)

def tabla_pesos(n, hasta=8):
    print(f"--- tabla de pesos (n={n}) ---")
    for k in range(hasta + 1):
        her = "semilla" if k == 0 else \
              f"hereda x{factor_herencia(n, k-1)[0]}/{factor_herencia(n, k-1)[1]}"
        print(f"  peso {k:2d} | C={comb(n, k):>20,} | {her}")

def ecuador(n):
    """Par -> ecuador exacto; impar -> sin ecuador (piso, techo)."""
    return (n//2, n//2) if n % 2 == 0 else (n//2, n//2 + 1)

def huella_neuronibble(estado_int):
    """Lee 64 bits como 16 neuronibbles; devuelve 16 pesos (0..4)."""
    return [bin((estado_int >> (4*i)) & 0xF).count("1") for i in range(16)]

if __name__ == "__main__":
    tabla_pesos(64)
    e = ecuador(64)
    print(f"ecuador 8x8: peso {e[0]} = {comb(64, e[0]):,} estados "
          f"(~9,93% de 2^64; auto-dual bajo NOT; pausa del aliento)")
    p, q = ecuador(169)
    print(f"13x13 (169 impar): sin ecuador; {p} vs {q} -> c:G7 desempata")
