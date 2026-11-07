#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: tools/neurobit_ram_neuronibble.py
Función: RAM viva de neuronibbles. Cada POS# guarda (AB,CD); cada celda es
         dato E instrucción. Resuelve el grafo de herencia (STA/NOT) y, si
         dos herencias colisionan en un slot, expone las compuertas CVR
         (OR/XOR/NAND/NOR) para que el NODO negocie cuál sella.
         La memoria no almacena representaciones: deriva estados.
MFN_LOCATION: tools/
MFN_LEVEL: 3
VERSION: v0.1
"""
def NOT(x): return "".join("1" if c == "0" else "0" for c in x)

def GATE(a, b, op):
    ai, bi = int(a, 2), int(b, 2)
    r = {"OR": ai | bi, "XOR": ai ^ bi, "AND": ai & bi,
         "NAND": ~(ai & bi) & 0xF, "NOR": ~(ai | bi) & 0xF}[op]
    return format(r, "04b")

# Semillas literales declaradas por el NODO_SEMILLA
SEMILLA = {1: ("0000", "0000"), 2: ("0000", "0001"), 3: ("0000", "0010")}

def resolver(gate_negociada="XOR"):
    ram = {p: {"AB": ab, "CD": cd} for p, (ab, cd) in SEMILLA.items()}
    # POS#04: CD := NOT POS#01.CD  (ALFA -> OMEGA)
    ram[4] = {"AB": "0000", "CD": NOT(ram[1]["CD"])}
    # POS#05: AB := POS#02.CD ; CD := CVR( NOT POS#03.CD , NOT POS#04.CD )
    w1, w2 = NOT(ram[3]["CD"]), NOT(ram[4]["CD"])
    ram[5] = {"AB": ram[2]["CD"], "CD": GATE(w1, w2, gate_negociada)}
    return ram

if __name__ == "__main__":
    for g in ("OR", "XOR", "NAND", "NOR"):
        print(f"-- CVR negociada: {g} --")
        for p in sorted(resolver(g)):
            r = resolver(g)[p]
            print(f"  POS#{p:02d} | {r['AB']} {r['CD']}")
