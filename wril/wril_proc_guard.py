#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL
Módulo: wril_proc_guard.py
Función: Guardia de inicio único. Cruza la lista declarada
         (data/runtime/procesos_iniciados.tmp) con la vida real (/proc).
         Veredictos: OK | NOTIFY | PURGE_Y_OK. Atomicidad bajo flock.
         La .tmp es índice vivo (reescribible bajo lock);
         la memoria append-only es wril_historial.jsonl.
MFN_LOCATION: wril/  |  MFN_LEVEL: 2
VERSION: v0.2
"""
import fcntl, os, time
from pathlib import Path

from wril_self_root import detectar_raiz as _raiz_canonica  # WRIL::RAIZ_CANONICA
RAIZ = _raiz_canonica()
LISTA = RAIZ / "data" / "runtime" / "procesos_iniciados.tmp"
LOCK  = RAIZ / "data" / "runtime" / "procesos_iniciados.lock"

def _partes(linea): return linea.split("|")
def _vive(pid):    return Path(f"/proc/{pid}").exists()

def leer_lista():
    if not LISTA.exists(): return []
    return [l for l in LISTA.read_text(encoding="utf-8").splitlines() if l.strip()]

class _cerrado:
    def __enter__(self):
        LOCK.parent.mkdir(parents=True, exist_ok=True)
        self.fd = os.open(str(LOCK), os.O_CREAT | os.O_RDWR, 0o644)
        fcntl.flock(self.fd, fcntl.LOCK_EX)
        return self
    def __exit__(self, *exc):
        fcntl.flock(self.fd, fcntl.LOCK_UN); os.close(self.fd)
        return False

def _estado(nombre):
    vivos = stale = 0
    for l in leer_lista():
        p = _partes(l)
        if len(p) >= 3 and p[1] == nombre:
            if _vive(p[2]): vivos += 1
            else: stale += 1
    return vivos, stale

def iniciar(nombre):
    """Guardia + saneado + asiento, atómico bajo flock.
    Devuelve NOTIFY (no tocar) | OK | PURGE_Y_OK (asentado tras sanear)."""
    with _cerrado():
        vivos, stale = _estado(nombre)
        if vivos:
            return "NOTIFY"
        keep = [l for l in leer_lista()
                if not (len(_partes(l)) >= 3 and _partes(l)[1] == nombre
                        and not _vive(_partes(l)[2]))]
        keep = [l for l in keep if not (len(_partes(l)) >= 3
                  and _partes(l)[1] == nombre and _partes(l)[2] == str(os.getpid()))]
        # Defensa per-pid: eliminar línea previa si existe con mismo nombre+pid
        keep = [l for l in keep if not (len(_partes(l)) >= 3
                  and _partes(l)[1] == nombre and _partes(l)[2] == str(os.getpid()))]
        # Defensa per-pid: eliminar línea previa si existe con mismo nombre+pid
        keep = [l for l in keep if not (len(_partes(l)) >= 3
                  and _partes(l)[1] == nombre and _partes(l)[2] == str(os.getpid()))]
        keep.append(f"{time.strftime('%Y-%m-%dT%H:%M:%S')}|{nombre}|{os.getpid()}"
                    f"|{nombre}__EXECUTION_STATE=true")
        LISTA.parent.mkdir(parents=True, exist_ok=True)
        LISTA.write_text("\n".join(keep) + "\n", encoding="utf-8")
        return "PURGE_Y_OK" if stale else "OK"

def liberar(nombre, pid=None):
    """Apagado gracioso: retira la línea propia bajo flock."""
    with _cerrado():
        keep = [l for l in leer_lista()
                if not (len(_partes(l)) >= 3 and _partes(l)[1] == nombre
                        and (pid is None or _partes(l)[2] == str(pid)))]
        LISTA.write_text("\n".join(keep) + ("\n" if keep else ""), encoding="utf-8")