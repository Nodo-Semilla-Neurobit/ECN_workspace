#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - PSI (Procedimiento Serial de Ingesta)
Módulo: extensions/psi/psi_nucleo.py
Función: Núcleo de orquestación serial. Despierta por inotify sobre
         psi_tareas.lst; ejecuta FIFO; asienta OK y encola el siguiente.
         Contrato CPS-1: invocación por append; log interno por módulo;
         depósito de resultado codificado atado a la cadena.
MFN_LOCATION: extensions/psi/ | MFN_LEVEL: 3
VERSION: v0.1
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))              # WRIL::SELF_PATH::v1
_ws.path.insert(0, str(_wp(__file__).resolve().parents[2] / "wril")) # WRIL::HERMANOS::v1
import os, sys, time, hashlib, subprocess, atexit, ctypes
from pathlib import Path
from wril_self_root import detectar_raiz
from wril_proc_guard import iniciar, liberar

RAIZ   = detectar_raiz()
LISTA  = RAIZ / "data" / "runtime" / "psi_tareas.lst"
TMP    = RAIZ / "data" / "runtime" / "psi_tmp"
CADENA_PSI = ["ps0_clasificador", "ps1_gemelo", "ps2_metadatos", "ps3_frases"]
NOMBRE = "PSI_NUCLEO"
IN_CLOSE_WRITE, IN_MOVED_TO = 0x00000008, 0x00000080

def _sha(r: Path) -> str:
    return hashlib.sha256(r.read_bytes()).hexdigest()[:16] if r.exists() else "-"

def asentar(modulo, estado, destino="-", nota=""):
    LISTA.parent.mkdir(parents=True, exist_ok=True)
    with open(LISTA, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}|"
                f"{modulo}|{estado}|-|{destino}|{nota}\n")

def pendientes():
    if not LISTA.exists():
        return []
    return [l.split("|") for l in LISTA.read_text(encoding="utf-8").splitlines()
            if len(l.split("|")) >= 6 and l.split("|")[2] == "ENCOLADO"]

def ruta_modulo(nombre):
    d = RAIZ / "extensions" / "psi" / nombre / f"{nombre}.py"
    return d if d.exists() else None

def ejecutar(tarea):
    modulo, nota = tarea[1], tarea[5]
    kv = dict(x.split("=", 1) for x in nota.split(";") if "=" in x)
    cadena = kv.get("cadena", "SIN_CADENA")
    rmod = ruta_modulo(modulo)
    if not rmod:
        asentar(modulo, "FALLO", nota=f"cadena={cadena};modulo_no_resuelto")
        return
    out_dir = TMP / cadena
    out_dir.mkdir(parents=True, exist_ok=True)
    asentar(modulo, "EJECUTANDO", nota=f"cadena={cadena}")
    r = subprocess.run([sys.executable, str(rmod), str(cadena), str(out_dir)],
                       capture_output=True, text=True)
    res = out_dir / f"{modulo}_resultado.json"
    if r.returncode == 0 and res.exists():
        h = _sha(res)
        asentar(modulo, "OK", destino=str(res.relative_to(RAIZ)),
                nota=f"cadena={cadena};hash={h}")
        if modulo in CADENA_PSI and CADENA_PSI.index(modulo) < len(CADENA_PSI) - 1:
            asentar(CADENA_PSI[CADENA_PSI.index(modulo) + 1], "ENCOLADO",
                    nota=f"cadena={cadena};prev={h}")  # el append dispara al siguiente
    else:
        asentar(modulo, "FALLO", nota=f"cadena={cadena};rc={r.returncode}")

def esperar_push():
    libc = ctypes.CDLL("libc.so.6", use_errno=True)
    fd = libc.inotify_init()
    libc.inotify_add_watch(fd, str(LISTA.parent).encode(),
                           IN_CLOSE_WRITE | IN_MOVED_TO)
    while True:
        os.read(fd, 4096)          # bloqueo kernel: 0.0% CPU en espera
        for t in pendientes():
            ejecutar(t)

def main():
    if iniciar(NOMBRE) == "NOTIFY":
        sys.exit(0)
    atexit.register(liberar, NOMBRE, os.getpid())
    for t in pendientes():
        ejecutar(t)
    esperar_push()

if __name__ == "__main__":
    main()
