#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: neurobit_dispatcher.py (La Oficina de Correos)
Función: Duerme hasta que inotify anuncia una carta en el buzón de salida;
         la clasifica por su sello protocolar (ACTION_WORD/CLASS) y la
         entrega al postman radial correspondiente. Cero sondeo.
VERSION: v0.1
"""

import os
import re
import json
import ctypes
import ctypes.util
from pathlib import Path
from datetime import datetime

_libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
IN_CLOSE_WRITE = 0x00000008
IN_MOVED_TO    = 0x00000080

RAIZ = Path(__file__).resolve().parent
BUZON = RAIZ / "buzon_salida"
BUZON.mkdir(parents=True, exist_ok=True)

RE_SELLO = re.compile(r"\|=•'([^']+)'•=\|»(?:\|\['([^'.]+)'\.\])?")

POSTMANS = {}
def registrar_postman(dominio):
    def deco(fn):
        POSTMANS[dominio] = fn
        return fn
    return deco

@registrar_postman('ledger')
def postman_ledger(texto, clase):
    from neurobit_clipboard_core import ARCHIVO_TEMPORAL, ejecutar_commit_verificado
    ARCHIVO_TEMPORAL.write_text(texto, encoding="utf-8")
    ejecutar_commit_verificado()

@registrar_postman('memoria')
def postman_memoria(texto, clase):
    registro = {"t": datetime.now().isoformat(), "class": clase, "logos": texto}
    with open(RAIZ / "memoria_eva.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(registro, ensure_ascii=False) + "\n")

@registrar_postman('general')
def postman_general(texto, clase):
    postman_memoria(texto, clase)

def clasificar_y_entregar(carta: Path):
    texto = carta.read_text(encoding="utf-8", errors="ignore")
    m = RE_SELLO.search(texto)
    accion = m.group(1) if m else "general"
    clase = (m.group(2) or "sin_clase") if m else "sin_clase"
    POSTMANS.get(accion, postman_general)(texto, clase)
    carta.unlink()                  # carta entregada: el buzón queda vacío

def correr():
    fd = _libc.inotify_init()
    _libc.inotify_add_watch(fd, str(BUZON).encode(), IN_CLOSE_WRITE | IN_MOVED_TO)
    print("[✓ CORREOS] Oficina abierta. El Kernel avisará por cada carta.")
    while True:
        os.read(fd, 4096)           # reposo absoluto hasta el push del VFS
        for carta in sorted(BUZON.iterdir()):
            clasificar_y_entregar(carta)

if __name__ == "__main__":
    correr()
