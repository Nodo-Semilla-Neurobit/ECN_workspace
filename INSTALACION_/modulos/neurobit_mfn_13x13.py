#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: neurobit_mfn_13x13.py
Función: Formalización matemática de la Matriz Fractal Neurobitrónica
         radial polar de orden 13. Anexo de la Tesis v1.0.
         M = Z13 x Z13; p(i,j) = (rho=i+1, phi=2*pi*j/13); origen = Dispatcher.
VERSION: v0.1
"""

import math

ORDEN = 13

DOMINIOS = {
    0:"kernel_hid", 1:"desktop_gtk", 2:"desktop_cinnamon", 3:"browser_eva",
    4:"headless_xlib", 5:"http_sala", 6:"dictado_evdev", 7:"ledger",
    8:"memoria_eva", 9:"auditoria_sha", 10:"versiones", 11:"tesis", 12:"reserva"
}
ANILLOS = {
    0:"ram_volatil", 1:"staging_tmp", 2:"buzon_salida", 3:"ledger_log",
    4:"backups", 5:"memoria_jsonl", 6:"auditoria", 7:"readme_manifiesto",
    8:"yaml_declaracion", 9:"bitacora_conversacional", 10:"dossier_joseph",
    11:"anexo_historico", 12:"semilla_fractal"
}

def phi(j):
    return 2 * math.pi * (j % ORDEN) / ORDEN

def ubicar(anillo_i, sector_j):
    """Vector radial polar de una celda + proyección cartesiana."""
    r = (anillo_i % ORDEN) + 1
    a = phi(sector_j)
    return {"rho": r, "phi": round(a, 5),
            "x": round(r * math.cos(a), 3), "y": round(r * math.sin(a), 3),
            "dominio": DOMINIOS[sector_j % ORDEN],
            "persistencia": ANILLOS[anillo_i % ORDEN]}

def origen():
    """La Oficina de Correos: punto de emisión, rho = 0."""
    return {"rho": 0, "phi": None, "x": 0.0, "y": 0.0, "dominio": "dispatcher"}

def clasificar_carta(accion, clase):
    """Teorema de clasificación: sello -> coordenadas (rho, phi)."""
    sector = list(DOMINIOS.values()).index(accion) if accion in DOMINIOS.values() else 7
    anillo = list(ANILLOS.values()).index(clase) if clase in ANILLOS.values() else 3
    return ubicar(anillo, sector)

if __name__ == "__main__":
    print("[✓ MFN] Matriz 13x13 activa. Origen:", origen())
    print("    Ejemplo carta ledger/ledger_log:", clasificar_carta("ledger", "ledger_log"))
