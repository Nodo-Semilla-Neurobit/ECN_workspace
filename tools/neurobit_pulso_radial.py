#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: neurobit_pulso_radial.py
Función: Reloj binario radial headless. Resuelve los 7 anillos
         (c, am, na, vi, añ, az, m) por instancia t, sin memoria histórica:
         E(k,t) = floor(t / 2^k) mod 2. Acarreo ripple-carry: el anillo k+1
         muta solo cuando el anillo k alcanza su Omega.
         Emite el dot-map de 169 bits al Cartógrafo (/api/sprite/create) o,
         si la Sala duerme, lo sella como carta 'pulso' en buzón_salida.
MFN_LOCATION: tools/
MFN_LEVEL: 3
VERSION: v1.0
"""
import argparse
import json
import threading
import time
from pathlib import Path
from datetime import datetime

ANILLOS = ["c", "am", "na", "vi", "añ", "az", "m"]
BITS_POR_PORCION = {"c": 1, "am": 1, "na": 2, "vi": 3, "añ": 4, "az": 5, "m": 6}
PORCIONES = 8
OFFSET = {"c": 0, "am": 1, "na": 9, "vi": 25, "añ": 49, "az": 81, "m": 121}
TOTAL_BITS = 169

def estado_anillo(k: int, t: int) -> int:
    """E(k,t) = floor(t / 2^k) mod 2. Resolución determinista por instancia."""
    return (t >> k) & 1

def omega_anillo(k: int, t: int) -> bool:
    """El anillo k alcanza Omega cuando su semiciclo termina:
    t mod 2^k == 2^k - 1. El pulso (k=0) alcanza Omega en cada paso."""
    if k == 0:
        return True
    mascara = (1 << k) - 1
    return (t & mascara) == mascara

def dot_map(t: int) -> list:
    """Array radial de 169 bits para la instancia t (centro -> perímetro)."""
    estado = [0] * TOTAL_BITS
    for k, a in enumerate(ANILLOS):
        bit = estado_anillo(k, t)
        n = BITS_POR_PORCION[a] * PORCIONES
        for i in range(OFFSET[a], OFFSET[a] + n):
            estado[i] = bit
    return estado

def coordenada(idx: int) -> str:
    """Índice lineal (0..168) -> notación anillo:S[sector]:P[porción]:B[bit]."""
    for k in range(len(ANILLOS) - 1, -1, -1):
        a = ANILLOS[k]
        if idx >= OFFSET[a]:
            rel = idx - OFFSET[a]
            bpp = BITS_POR_PORCION[a]
            pg = rel // bpp                      # porción global 0..7
            bit = rel % bpp + 1
            return f"{a}:S{pg // 2 + 1}:P{pg % 2 + 1}:B{bit}"
    return "c:G7"

def render_ascii(t: int) -> str:
    lineas = [f"instancia t={t}  (binario {t:07b})"]
    for k in range(len(ANILLOS) - 1, -1, -1):
        a = ANILLOS[k]
        bit = estado_anillo(k, t)
        masa = ("█" if bit else "·") * PORCIONES
        lineas.append(f"  {a:>2} [{masa}] {bit}")
    return "\n".join(lineas)

class PuenteCartografo:
    """Envía el estado al Cartógrafo sin bloquear; si falla, sella carta."""
    def __init__(self, url="http://127.0.0.1:5000/api/sprite/create",
                 buzon: Path = None):
        self.url = url
        self.buzon = buzon or Path(__file__).resolve().parent / "buzon_salida"

    def transmitir(self, t: int, estado: list):
        threading.Thread(target=self._post, args=(t, estado), daemon=True).start()

    def _post(self, t, estado):
        try:
            import urllib.request
            req = urllib.request.Request(
                self.url, data=json.dumps({"estado": estado}).encode("utf-8"),
                headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=1.5)
        except Exception:
            self._sellar(t, estado)

    def _sellar(self, t, estado):
        self.buzon.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        activos = [i for i, b in enumerate(estado) if b]
        coords = [coordenada(i) for i in activos[:12]]
        carta = (f"|=•'pulso'•=|»|['t{t}'.]\n"
                 f"instancia: {t}\nactivos: {len(activos)}\n"
                 + "\n".join(coords) +
                 f"\n[.'t{t}']|«|=•'pulso'•=|")
        (self.buzon / f"carta_pulse_{ts}.txt").write_text(carta, encoding="utf-8")

def main():
    ap = argparse.ArgumentParser(description="Reloj binario radial MFN")
    ap.add_argument("--t", type=int, default=None, help="instancia a resolver")
    ap.add_argument("--auto", action="store_true", help="latido continuo")
    ap.add_argument("--delay", type=float, default=1.0)
    ap.add_argument("--url", default="http://127.0.0.1:5000/api/sprite/create")
    args = ap.parse_args()
    puente = PuenteCartografo(url=args.url)
    if args.t is not None:
        print(render_ascii(args.t))
        puente.transmitir(args.t, dot_map(args.t))
        return
    t = 0
    while True:
        print(render_ascii(t))
        puente.transmitir(t, dot_map(t))
        t += 1
        if not args.auto:
            break
        time.sleep(args.delay)

if __name__ == "__main__":
    main()
