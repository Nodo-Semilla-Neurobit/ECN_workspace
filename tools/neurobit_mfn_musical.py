#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: neurobit_mfn_musical.py
Función: Anexo musical de la Tesis v1.0. Segunda proyección semántica
         sobre el toro Z13xZ13: espacio de alturas temperado.
         Sector j mod 12 = semitono; anillo i = octava; sector 12 = costura
         enarmónica (retorno de la tónica con salto de anillo).
         Origen (rho=0) = diapasón La 440: la Oficina de Correos afina.
VERSION: v0.1
"""

NOTAS = ["La","La#","Si","Do","Do#","Re","Re#","Mi","Fa","Fa#","Sol","Sol#"]

def semitono(sector_j):
    return sector_j % 12

def es_costura(sector_j):
    return sector_j % 13 == 12

def frecuencia(anillo_i, sector_j, f0=440.0):
    """f = f0 * 2^(s/12) * 2^i : el angulo es la altura, el radio la octava."""
    if es_costura(sector_j):
        return f0 * (2 ** (anillo_i + 1))
    return f0 * (2 ** (semitono(sector_j) / 12.0)) * (2 ** anillo_i)

def nombre_celda(anillo_i, sector_j):
    if es_costura(sector_j):
        return f"La{anillo_i+1} [costura enarmonica]"
    return f"{NOTAS[semitono(sector_j)]}{anillo_i}"

if __name__ == "__main__":
    print("[✓ ANEXO MUSICAL] La matriz suena. Origen = La 440 (diapason).")
    for j in range(13):
        print(f"    sector {j:2d} -> {nombre_celda(0, j):28s} {frecuencia(0, j):7.2f} Hz")
