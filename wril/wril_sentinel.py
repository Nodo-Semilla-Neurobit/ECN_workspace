#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL (Capa de Resolución, Integridad y Circulación)
Módulo: wril_sentinel.py (Boundary Controller / WS-Sentinel v1.0)
Función: Vigila inbox/ mediante inotify; lee MFN_LOCATION del artefacto,
         valida destino, resguarda antes de sobrescribir (wril_backup),
         MOVE y registra en el historial. Sin declaración: carta de
         orfandad y retención en inbox (no se rutea lo que no se declara).
         Tras cada MOVE regenera path_map: el índice refleja el estado.
MFN_LOCATION: wril/  |  MFN_LEVEL: 2
VERSION: v1.0
"""
import os
import re
import json
import shutil
import struct
import ctypes
import ctypes.util
from pathlib import Path
from datetime import datetime
from wril_backup import resguardar
from wril_path_map import generar_mapa

_libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
IN_CLOSE_WRITE = 0x00000008
IN_MOVED_TO    = 0x00000080

from wril_self_root import detectar_raiz as _raiz_canonica  # WRIL::RAIZ_CANONICA
RAIZ = _raiz_canonica()
INBOX = RAIZ / "inbox"
INBOX.mkdir(parents=True, exist_ok=True)
HISTORIAL = RAIZ / "wril_historial.jsonl"
MAP_FILE = RAIZ / "path_map.json"
BUZON = RAIZ / "buzon_salida"
CREAR_DESTINOS = True      # destino declarado ausente: crear o retener

RE_LOC = re.compile(r"MFN_LOCATION:\s*(\S+)")

def leer_declaracion(ruta: Path):
    try:
        cabeza = ruta.read_text(encoding="utf-8", errors="ignore")[:500]
    except Exception:
        return None
    m = RE_LOC.search(cabeza)
    return m.group(1).strip() if m else None

def registrar(entrada: dict):
    with open(HISTORIAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(entrada, ensure_ascii=False) + "\n")

def carta_orfandad(nombre: str):
    BUZON.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    (BUZON / f"carta_wril_{ts}.txt").write_text(
        "|=•'wril'•=|»|['sin_declaracion'.]\n"
        f"WS-Sentinel: '{nombre}' carece de MFN_LOCATION. "
        "Queda retenido en inbox/ hasta que declare su identidad.\n"
        "[.'sin_declaracion']|«|=•'wril'•=|", encoding="utf-8")

def enrutar(nombre: str):
    origen = INBOX / nombre
    if not origen.is_file():
        return
    destino_rel = leer_declaracion(origen)
    if not destino_rel:
        carta_orfandad(nombre)
        return
    dir_destino = RAIZ / destino_rel
    if not dir_destino.exists():
        if CREAR_DESTINOS:
            dir_destino.mkdir(parents=True, exist_ok=True)
        else:
            registrar({"t": datetime.now().isoformat(), "archivo": nombre,
                       "estado": "DESTINO_AUSENTE"})
            return
    destino = dir_destino / nombre
    backup = resguardar(destino) if destino.exists() else None
    shutil.move(str(origen), str(destino))
    generar_mapa(RAIZ, MAP_FILE)          # el índice refleja la nueva topología
    registrar({"t": datetime.now().isoformat(), "archivo": nombre,
               "destino": str(destino),
               "backup": str(backup) if backup else None, "estado": "ROUTE_OK"})
    print(f"[✓ SENTINEL] {nombre} -> {destino_rel}")

def _leer_eventos(fd):
    datos = os.read(fd, 4096)
    offset, nombres = 0, []
    while offset < len(datos):
        wd, mask, cookie, length = struct.unpack_from("iIII", datos, offset)
        offset += struct.calcsize("iIII")
        nombres.append(datos[offset:offset+length].rstrip(b"\x00").decode())
        offset += length
    return nombres

def correr():
    fd = _libc.inotify_init()
    _libc.inotify_add_watch(fd, str(INBOX).encode(), IN_CLOSE_WRITE | IN_MOVED_TO)
    print("[✓ SENTINEL] Guardián de frontera en reposo sobre inbox/.")
    while True:
        for nombre in _leer_eventos(fd):
            if nombre:
                enrutar(nombre)

if __name__ == "__main__":
    from wril_proc_guard import iniciar, liberar
    import atexit as _atx, os as _os
    NOMBRE = "WRIL_SENTINEL"
    _v = iniciar(NOMBRE)
    if _v == "NOTIFY":
        print(f"[✓ {NOMBRE}__EXECUTION_STATE-NOTIFY] ya en curso; no se duplica.")
        raise SystemExit(0)
    if _v == "PURGE_Y_OK":
        print(f"[⚠ {NOMBRE}] entrada stale saneada; se relanza.")
    _atx.register(lambda: liberar(NOMBRE, _os.getpid()))
    import signal as _sig
    def _halt_gracioso(signum, frame):
        liberar(NOMBRE, _os.getpid())
        raise SystemExit(0)
    _sig.signal(_sig.SIGTERM, _halt_gracioso)
    _sig.signal(_sig.SIGINT, _halt_gracioso)
    try:
        correr()
    except KeyboardInterrupt:
        print("[✓ SENTINEL] HALT limpio. Reposo.")

