#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: neurobit_dictado_evdev.py (Keylogger Soberano / Dictáfono de Tesis)
Función: Captura la escritura propia vía evdev SOLO bajo activación consciente
         (F8 abre/cierra sesión). Traduce keycodes (layout es básico + acentos
         por tecla muerta) y deposita la carta sellada en buzón_salida.
         Cero dependencias externas, cero exfiltración, 0.0% CPU en reposo.
VERSION: v0.1
"""

import struct
import glob
from pathlib import Path
from datetime import datetime

RAIZ = Path(__file__).resolve().parent
BUZON = RAIZ / "buzon_salida"
BUZON.mkdir(parents=True, exist_ok=True)

FMT_EVENTO = "@llHHi"                      # struct input_event (64 bits)
TAM_EVENTO = struct.calcsize(FMT_EVENTO)   # 24 bytes

KEY_F8 = 66
KEY_SHIFT_L, KEY_SHIFT_R = 42, 54
KEY_ENTER, KEY_SPACE, KEY_MUERTA = 28, 57, 40

# Layout español básico (keycode -> minúscula)
ES = {
    30:'a',48:'b',46:'c',32:'d',18:'e',33:'f',34:'g',35:'h',23:'i',36:'j',
    37:'k',38:'l',50:'m',49:'n',24:'o',25:'p',16:'q',19:'r',31:'s',20:'t',
    22:'u',47:'v',17:'w',45:'x',21:'y',44:'z',
    2:'1',3:'2',4:'3',5:'4',6:'5',7:'6',8:'7',9:'8',10:'9',11:'0',
    39:'ñ', 51:',', 52:'.', 53:'-', 12:'\'', 13:'¡',
}
MAYUS = {k: v.upper() for k, v in ES.items() if v.isalpha()}
COMBINAS = {'a':'á','e':'é','i':'í','o':'ó','u':'ú'}   # tecla muerta + vocal

class DictadoSoberano:
    def __init__(self):
        self.activo = False
        self.shift = False
        self.muerta = False
        self.buffer = []

    def tecla(self, code, valor):
        if code in (KEY_SHIFT_L, KEY_SHIFT_R):
            self.shift = valor in (1, 2)
            return
        if code == KEY_F8 and valor == 1:
            self.activo = not self.activo
            if self.activo:
                print("[✓ DICTADO] Sesión abierta: escribí; el Logos queda.")
            else:
                self.depositar()
            return
        if not self.activo or valor != 1:
            return
        if code == KEY_MUERTA:
            self.muerta = True
            return
        if code == KEY_ENTER:
            self.buffer.append('\n'); return
        if code == KEY_SPACE:
            self.buffer.append(' '); return
        base = ES.get(code)
        if base is None:
            return
        ch = MAYUS.get(code, base) if self.shift else base
        if self.muerta:
            ch = COMBINAS.get(base, base)
            self.muerta = False
        self.buffer.append(ch)

    def depositar(self):
        texto = "".join(self.buffer).strip()
        self.buffer = []
        if not texto:
            return
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        sello = "|=•'dictado'•=|»|['evdev'.]\n"
        cierre = "\n[.'evdev']|«|=•'dictado'•=|"
        (BUZON / f"carta_dictado_{ts}.txt").write_text(
            sello + texto + cierre, encoding="utf-8")
        print(f"[✓ CARTA] Dictado asentado en buzón ({len(texto)} bytes).")

def main():
    teclados = sorted(glob.glob("/dev/input/by-id/*-event-kbd"))
    if not teclados:
        print("[X ERROR] Sin teclado visible en /dev/input/by-id/.")
        return 1
    d = DictadoSoberano()
    print(f"[✓ DICTADO] Soberano en reposo sobre {teclados[0]}. F8 abre/cierra.")
    with open(teclados[0], "rb") as fd:
        while True:
            raw = fd.read(TAM_EVENTO)
            if len(raw) < TAM_EVENTO:
                break
            _, _, tipo, code, valor = struct.unpack(FMT_EVENTO, raw)
            if tipo == 1:                      # EV_KEY
                d.tecla(code, valor)

if __name__ == "__main__":
    main()
