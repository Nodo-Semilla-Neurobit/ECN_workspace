#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: wril_adapter_c64.py (Conector VIC-II / C64)
Función: Lee la salida virtual del puerto de comunicaciones del emulador C64
         (PTY o archivo), interpreta charset 8x8 (8 bytes/glifo) como 64 bits
         y los pliega al espacio MFN 169 centrando el glifo en 13x13.
         Emite al Cartógrafo (5002); si duerme, sella carta.
MFN_LOCATION: wril/
MFN_LEVEL: 2
VERSION: v0.1
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import json, time, argparse, urllib.request
from pathlib import Path
from wril_self_root import detectar_raiz as _raiz_canonica  # WRIL::RAIZ_CANONICA
RAIZ = _raiz_canonica()
if RAIZ.name=="wril": RAIZ = RAIZ.parent
CARTOGRAFO = "http://127.0.0.1:5002/api/sprite/create"

def glifo_a_169(ocho: bytes) -> list:
    """8 bytes (8x8) -> malla 13x13 centrada (3..10,3..10) -> 169 bits."""
    estado=[0]*169
    for fila in range(8):
        byte = ocho[fila] if fila < len(ocho) else 0
        for col in range(8):
            estado[(fila+3)*13 + (col+3)] = (byte >> (7-col)) & 1
    return estado

def leer_glifos(fuente: Path, tam=8):
    data = fuente.read_bytes()
    for i in range(0, len(data)-tam+1, tam):
        yield data[i:i+tam]

def emitir(estado):
    try:
        req=urllib.request.Request(CARTOGRAFO, data=json.dumps({"estado":estado}).encode(),
                                   headers={"Content-Type":"application/json"})
        urllib.request.urlopen(req, timeout=1.5); return True
    except Exception: return False

def sellar(estado, idx):
    buz=RAIZ/"buzon_salida"; buz.mkdir(parents=True, exist_ok=True)
    ts=time.strftime("%Y%m%d_%H%M%S")
    (buz/f"carta_c64_{ts}.txt").write_text(
        f"|=•'c64'•=|»|['vic2'.]\nglifo: {idx}\nactivos: {sum(estado)}\n[.'vic2']|«|=•'c64'•=|",
        encoding="utf-8")

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("fuente"); ap.add_argument("--continuo", action="store_true")
    a=ap.parse_args(); fuente=Path(a.fuente); idx=0
    while True:
        for g in leer_glifos(fuente):
            st=glifo_a_169(g)
            if not emitir(st): sellar(st, idx)
            idx+=1
        if not a.continuo: break
        time.sleep(0.5)

if __name__=="__main__":
    main()
