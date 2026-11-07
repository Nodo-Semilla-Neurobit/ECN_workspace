#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ecosistema Neurobit - compilar_compendio_base.py
Función: emite compendio_base.txt en formato canónico ARCHIVO NRO.
         desde lista_compendio_base.txt. SOLO LECTURA de las fuentes.
MFN_LOCATION: tools/  |  MFN_LEVEL: 3
VERSION: v0.1
"""
from pathlib import Path
from datetime import datetime

LISTA  = Path('lista_compendio_base.txt')
SALIDA = Path('compendio_base.txt')

rutas = [l.strip() for l in LISTA.read_text(encoding='utf-8').splitlines()
         if l.strip() and not l.strip().startswith('#')]

bloques = []
for n, r in enumerate(rutas, 1):
    p = Path(r)
    if not p.exists():
        print(f'[X FALTA] {r}'); continue
    cuerpo = p.read_text(encoding='utf-8', errors='ignore')
    bloques.append(
        "____________________________________________________________\n"
        f"ARCHIVO NRO. : ({n})\n"
        f"Archivo: ('{p.name}');\n"
        f"Carpeta de ubicación: ('~/{p.parent}');\n"
        "función: ('ver módulo');\n"
        "Variables del entorno: (ninguna)\n"
        "-------------------------------------------------Inicio:\n\n"
        f"{cuerpo}\n\n"
        "FINAL---------------------------------------------------------------\n")

cab = ("Compendio de Archivos del proyecto: 'ECN_BASE';\n"
       f"Analisis_Date: ('{datetime.now():%Y-%m-%d %H:%M:%S}')\n"
       f"N_Archivos_Actuales: ({len(bloques)})\n"
       "----------------------------------------------------"
       "------------------------\n")
SALIDA.write_text(cab + "\n".join(bloques), encoding='utf-8')
print(f'[✓ COMPENDIO] {SALIDA} con {len(bloques)} artefactos.')