#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL
Módulo: wril_integridad_json.py (Conductor de integridad de índices)
Función: Escaneo estructural y territorial de .json/.jsonl:
  - path_map.json: llaves/commas/cierre, patrón "clave": "valor",
    referencias fantasma (valor sin existencia real) y cotejo inverso
    (territorio sin consolidar en el mapa).
  - *.jsonl: parseo por línea; líneas no-parseables se reportan
    (NUNCA se reescriben: cuarentena vía saneo, la memoria no se edita).
  - estado_real.json: parseo + frescura + cada VIVO/MUERTO contra /proc.
  --reparar: backup previo (LEY 2) y regeneración vía los módulos canónicos
  (generar_mapa / wril_estado_real). El mapa refleja lo registrado;
  el territorio manda.
MFN_LOCATION: wril/  |  MFN_LEVEL: 2
VERSION: v0.1
"""
import json, os, sys
from pathlib import Path
from datetime import datetime

from wril_self_root import detectar_raiz as _raiz_canonica  # WRIL::RAIZ_CANONICA
RAIZ = _raiz_canonica()

def _vive(pid):
    try:
        os.kill(int(pid), 0); return True
    except Exception:
        return False

def verificar_path_map(ruta: Path):
    prob = []
    t = ruta.read_text(encoding="utf-8")
    if not t.strip().startswith("{") or not t.strip().endswith("}"):
        prob.append("estructura: no abre/cierra con llaves")
    lines = [l for l in t.splitlines() if l.strip() and l.strip() not in ("{", "}")]
    for i, l in enumerate(lines):
        s = l.strip(); ultimo = (i == len(lines) - 1)
        if ultimo and s.endswith(","):
            prob.append(f"linea {i+1}: coma final en ultimo registro")
        if not ultimo and not s.endswith(","):
            prob.append(f"linea {i+1}: falta coma al cierre")
        if not (s.startswith('"') and '": "' in s):
            prob.append(f"linea {i+1}: patron de registro no reconocido")
    try:
        data = json.loads(t)
    except Exception as e:
        prob.append(f"parse JSON: {e.__class__.__name__}"); data = {}
    fantasmas = [k for k, v in data.items() if not Path(v).exists()]
    if fantasmas:
        prob.append(f"referencias fantasma: {len(fantasmas)} (ej: {fantasmas[:3]})")
    EXT = ('.py', '.sh', '.js', '.md', '.yaml', '.json', '.c')
    RUIDO = {'.git', '__pycache__', '.venv', 'node_modules', 'backups_wril',
             'buzon_salida', 'pids', 'archive'}
    reales = set()
    for root, dirs, files in os.walk(RAIZ):
        dirs[:] = [d for d in dirs if d not in RUIDO]
        for f in files:
            if f.endswith(EXT):
                reales.add(f)
    claves = set(data.keys()) | {Path(k).name for k in data.keys()}
    sin_consol = sorted(reales - claves)
    if sin_consol:
        prob.append(f"sin consolidar en mapa: {len(sin_consol)} (ej: {sin_consol[:5]})")
    return prob

def verificar_jsonl(ruta: Path):
    prob = []
    for i, l in enumerate(ruta.read_text(encoding="utf-8").splitlines(), 1):
        s = l.strip()
        if not s:
            continue
        try:
            json.loads(s)
        except Exception as e:
            prob.append(f"linea {i}: {e.__class__.__name__}")
    return prob

def verificar_estado_real(ruta: Path):
    try:
        data = json.loads(ruta.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"parse JSON: {e.__class__.__name__}"]
    prob = []
    try:
        edad_h = (datetime.now() - datetime.fromisoformat(data.get("t", ""))).total_seconds() / 3600
        if edad_h > 24:
            prob.append(f"stale: {edad_h:.0f} h sin reescribir")
    except Exception:
        prob.append("timestamp ilegible")
    for c in data.get("componentes", []):
        pid, est = c.get("pid"), c.get("estado")
        if est == "VIVO" and (pid is None or not _vive(pid)):
            prob.append(f"{c.get('nombre')}: declarado VIVO pero pid {pid} no vive")
        if est == "MUERTO" and pid is not None and _vive(pid):
            prob.append(f"{c.get('nombre')}: declarado MUERTO pero pid {pid} vive")
    return prob

OBJETIVOS = {
    "path_map.json": (RAIZ / "path_map.json", verificar_path_map),
    "estado_real.json": (RAIZ / "estado_real.json", verificar_estado_real),
    "wril_historial.jsonl": (RAIZ / "wril_historial.jsonl", verificar_jsonl),
}

def main():
    reparar = "--reparar" in sys.argv
    total = 0
    for nombre, (ruta, fn) in OBJETIVOS.items():
        if not ruta.exists():
            print(f"[⚠ {nombre}] ausente"); total += 1; continue
        prob = fn(ruta)
        if prob:
            total += len(prob)
            print(f"[⚠ {nombre}] {len(prob)} problemas:")
            for p in prob[:8]:
                print(f"    - {p}")
        else:
            print(f"[✓ {nombre}] integridad coherente")
    if reparar and total:
        from wril_backup import resguardar
        from wril_path_map import generar_mapa
        b1 = resguardar(RAIZ / "path_map.json")
        generar_mapa(RAIZ, RAIZ / "path_map.json")
        print(f"[✓ REPARAR] path_map regenerado (backup: {b1})")
        import subprocess
        subprocess.run([sys.executable, str(RAIZ / "wril" / "wril_estado_real.py")])
        print("[✓ REPARAR] estado_real reescrito desde la realidad (consulta, no simula)")
        print("[· REPARAR] jsonl NO se reescribe: memoria se cuarentena, no se edita")
    sys.exit(0 if total == 0 else 1)

if __name__ == "__main__":
    main()