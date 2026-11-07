#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: neurobit_salon_vivo.py (Salón Vivo)
Función: Hace que el Cartógrafo MFN vea latir a sus propios radios.
         Event-driven: inotify sobre pids/; con --latido, reloj visual (2 s).
         Estado 169 bits: c = algún radio vivo; am = 4 radios; resto = pulso.
         POST al Cartógrafo (5002); si duerme, sella carta (soberanía).
         0.0% CPU en reposo: select con timeout, sin busy-polling.
MFN_LOCATION: tools/
MFN_LEVEL: 3
VERSION: v1.0
"""
import os, sys, json, select, argparse, ctypes, ctypes.util
from pathlib import Path
from datetime import datetime

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent if AQUI.name in ("tools", "wril") else AQUI
for p in (RAIZ, RAIZ / "wril", RAIZ / "tools"):
    if p.exists() and str(p) not in sys.path:
        sys.path.insert(0, str(p))

from neurobit_pulso_radial import dot_map, TOTAL_BITS
try:
    from wril_estado_real import estado_real as leer_estado
except Exception:
    leer_estado = None

CARTOGRAFO = "http://127.0.0.1:5002/api/sprite/create"
PIDS = RAIZ / "pids"
ORDEN_RADIOS = ["WS_SENTINEL", "DISPATCHER", "VISOR_SOBERANO", "DICTAFONO"]
_libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
IN_CREATE, IN_CLOSE_WRITE, IN_DELETE, IN_MOVED_TO = 0x100, 0x8, 0x200, 0x80

def estado_vivo():
    rep = leer_estado() if leer_estado else {"componentes": []}
    vivos = {c["nombre"]: c["estado"] == "ALIVE"
             for c in rep.get("componentes", [])}
    return rep, vivos

def pintar(t, vivos):
    estado = dot_map(t)
    estado[0] = 1 if any(vivos.values()) else 0        # c: observatorio
    for i, nombre in enumerate(ORDEN_RADIOS):          # am: los 4 radios
        estado[1 + i] = 1 if vivos.get(nombre) else 0
    return estado

def enviar(estado, t, vivos):
    try:
        import urllib.request
        req = urllib.request.Request(
            CARTOGRAFO, data=json.dumps({"estado": estado}).encode("utf-8"),
            headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=1.5)
        return True
    except Exception:                                   # Cartógrafo dormido
        buz = RAIZ / "buzon_salida"; buz.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        txt = ", ".join(f"{n}:{'VIVO' if v else 'CAIDO'}"
                        for n, v in vivos.items())
        (buz / f"carta_salon_{ts}.txt").write_text(
            f"|=•'salon'•=|»|['t{t}'.]\n{txt}\n[.'t{t}']|«|=•'salon'•=|",
            encoding="utf-8")
        return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--latido", action="store_true", help="reloj visual (2 s)")
    ap.add_argument("--intervalo", type=float, default=2.0)
    args = ap.parse_args()
    PIDS.mkdir(parents=True, exist_ok=True)
    fd = _libc.inotify_init()
    _libc.inotify_add_watch(fd, str(PIDS).encode(),
                            IN_CREATE | IN_CLOSE_WRITE | IN_DELETE | IN_MOVED_TO)
    t, ultimo = 0, None
    while True:
        if args.latido:
            t += 1
        rep, vivos = estado_vivo()
        (RAIZ / "estado_real.json").write_text(json.dumps(rep, indent=1),
                                               encoding="utf-8")
        estado = pintar(t, vivos)
        if estado != ultimo:
            ultimo = estado if enviar(estado, t, vivos) else ultimo
        if args.latido:
            if select.select([fd], [], [], args.intervalo)[0]:
                os.read(fd, 4096)
        else:
            os.read(fd, 4096)                          # bloqueante: 0% CPU

if __name__ == "__main__":
    main()
