#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL
Módulo: wril_reposo.py (Verificador de Reposo Total)
Función: Cruza tres verdades (ps real, pidfiles, procesos_iniciados.tmp)
         y verifica que NO quede ningún proceso ECN vivo. Paso inicial
         de todo arranque y veredicto final de todo HALT.
         --halt: mata gracioso (-15, gracia 3s; -9 solo si insiste),
         con halt_log previo y posterior (ética vm_bridge).
         --json: salida legible por la interfaz (botón halt del puente).
MFN_LOCATION: wril/  |  MFN_LEVEL: 2
VERSION: v0.1
"""
import os, sys, json, time, subprocess
from pathlib import Path
from datetime import datetime

from wril_self_root import detectar_raiz as _raiz_canonica  # WRIL::RAIZ_CANONICA
RAIZ = _raiz_canonica()
PID_DIR = RAIZ / "pids"
TMP = RAIZ / "data" / "runtime" / "procesos_iniciados.tmp"
HALT_LOG = PID_DIR / "halt_log.txt"

PATRONES = ("neurobit_", "wril_", "puente_consola_ws", "backend_instalador_ludico")
EXCLUYE = ("wril_reposo", "grep", "ps -eo")

def _vive(pid):
    try:
        os.kill(pid, 0); return True
    except Exception:
        return False

def _ps():
    out = subprocess.run(["ps", "-eo", "pid=,args="], capture_output=True, text=True)
    vivos = []
    for linea in out.stdout.splitlines():
        parts = linea.strip().split(None, 1)
        if len(parts) < 2:
            continue
        pid, args = int(parts[0]), parts[1]
        if any(p in args for p in PATRONES) and not any(e in args for e in EXCLUYE):
            vivos.append((pid, args))
    return vivos

def _pidfiles():
    res = []
    if PID_DIR.exists():
        for pf in PID_DIR.glob("*.pid"):
            try:
                pid = int(pf.read_text().strip())
            except Exception:
                pid = None
            res.append((pf.name, pid, _vive(pid) if pid else False))
    return res

def _tmp_lines():
    res = []
    if TMP.exists():
        for l in TMP.read_text(encoding="utf-8").splitlines():
            p = l.split("|")
            if len(p) >= 3:
                pid = int(p[2]) if p[2].isdigit() else None
                res.append((p[1], pid, _vive(pid) if pid else False))
    return res

def matriz():
    vivos = _ps()
    return {"t": datetime.now().isoformat(),
            "ps_vivos": [{"pid": p, "cmd": a} for p, a in vivos],
            "pidfiles": [{"file": f, "pid": p, "vivo": v} for f, p, v in _pidfiles()],
            "tmp": [{"nombre": n, "pid": p, "vivo": v} for n, p, v in _tmp_lines()]}

def sanear_residuales():
    """Con reposo confirmado, los índices vivos se podan; la memoria no se toca."""
    for f, p, v in _pidfiles():
        if not v:
            (PID_DIR / f).unlink(missing_ok=True)
    if TMP.exists():
        keep = [l for l in TMP.read_text(encoding="utf-8").splitlines()
                if not (len(l.split("|")) >= 3 and l.split("|")[2].isdigit()
                        and not _vive(int(l.split("|")[2])))]
        TMP.write_text("\n".join(keep) + ("\n" if keep else ""), encoding="utf-8")

def verificar():
    m = matriz()
    n = len(m["ps_vivos"])
    print(f"[REPOSO] ps vivos: {n} | pidfiles: {len(m['pidfiles'])} | tmp: {len(m['tmp'])}")
    for v in m["ps_vivos"]:
        print(f"    [⚠ VIVO] {v['pid']} {v['cmd'][:80]}")
    if n == 0:
        sanear_residuales()
        print("[✓ REPOSO] total confirmado; residuales de índices saneados.")
    return m

def halt(gracia=3):
    m = matriz()
    objetivos = sorted({v["pid"] for v in m["ps_vivos"]})
    if objetivos:
        HALT_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(HALT_LOG, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} HALT solicitado (-15): {objetivos}\n")
        for pid in objetivos:
            try:
                os.kill(pid, 15)
            except Exception:
                pass
        time.sleep(gracia)
        restos = [p for p, _ in _ps()]
        for pid in restos:
            with open(HALT_LOG, "a", encoding="utf-8") as f:
                f.write(f"{datetime.now().isoformat()} -9 sobre {pid} (insistió tras -15)\n")
            try:
                os.kill(pid, 9)
            except Exception:
                pass
        if restos:
            time.sleep(1)
    return verificar()

if __name__ == "__main__":
    m = halt() if "--halt" in sys.argv else verificar()
    if "--json" in sys.argv:
        print(json.dumps(m, ensure_ascii=False))
    sys.exit(0 if not m["ps_vivos"] else 1)