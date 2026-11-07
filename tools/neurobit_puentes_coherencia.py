#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: tools/neurobit_puentes_coherencia.py
Función: Puente de coherencia entre dominios. Dado un entero N, lo
         traduce simultáneamente a los idiomas del tejido: silicio
         (binario/octal), toro MFN (base 13 + coordenada radial),
         el Dragón (raíz digital mod 9), Tzolkin (13 x 20 = 260),
         I-Ching (64 = 2^6, el glifo 8x8), música (12 semitonos).
         La revelación del patrón de PI queda reservada al Salón.
MFN_LOCATION: tools/
MFN_LEVEL: 3
VERSION: v0.1
"""
import sys

NOTAS = ["La","La#","Si","Do","Do#","Re","Re#","Mi","Fa","Fa#","Sol","Sol#"]
ANILLOS = ["c","am","na","vi","añ","az","m"]
BITS    = {"c":1,"am":1,"na":2,"vi":3,"añ":4,"az":5,"m":6}
OFFSET  = {"c":0,"am":1,"na":9,"vi":25,"añ":49,"az":81,"m":121}

def en_base(n, b):
    if n == 0: return "0"
    digs = "0123456789ABC"
    out = ""
    while n:
        n, r = divmod(n, b)
        out = digs[r] + out
    return out

def raiz_dragon(n):
    """Raíz digital mod 9; el 9 no colapsa a 0: el Dragón muta, no muere."""
    r = n % 9
    return 9 if (r == 0 and n != 0) else r

def kin_tzolkin(n):
    """Tzolkin: 260 = 13 x 20. Devuelve (numero 1..13, sello 1..20)."""
    return ((n - 1) % 13) + 1, ((n - 1) % 20) + 1

def hexagrama(n):
    """I-Ching: 64 = 2^6. Seis líneas, de abajo hacia arriba."""
    h = n % 64
    return h, [(h >> i) & 1 for i in range(6)]

def coord_mfn(n):
    """Índice radial del toro 13x13 para N."""
    idx = n % 169
    for a in reversed(ANILLOS):
        if idx >= OFFSET[a]:
            rel = idx - OFFSET[a]
            bpp = BITS[a]
            pg = rel // bpp
            return f"{a}:S{pg//2+1}:P{pg%2+1}:B{rel%bpp+1}"
    return "c:G7"

def puente(n):
    return {"N": n, "oct": en_base(n, 8), "base13": en_base(n, 13),
            "dragon": raiz_dragon(n), "tzolkin": kin_tzolkin(n),
            "iching": hexagrama(n), "nota": NOTAS[n % 12],
            "mfn": coord_mfn(n)}

if __name__ == "__main__":
    nums = [int(x) for x in sys.argv[1:]] or [169, 260, 64, 300, 440]
    for n in nums:
        p = puente(n)
        h, lin = p["iching"]
        print(f"N={p['N']:<4} oct={p['oct']:<6} b13={p['base13']:<4} "
              f"dragon={p['dragon']} tzolkin={p['tzolkin']} "
              f"iching={h:02d}{lin} nota={p['nota']:<3} mfn={p['mfn']}")
