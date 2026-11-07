#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: tools/visor_informes.py (Visor de Informes v0.1)
Función: compila en un solo reporte la verdad del territorio: kernel (ps/ss),
índices declarados, buzones y cartas varadas, colas de logs, colisiones de
nombre y freezer. Acepta directorios externos como argumentos para listar
sus archivos (logs, imágenes, versiones otras) SIN tocarlos.
SOLO LECTURA: no muta nada.
MFN_LOCATION: tools/  |  MFN_LEVEL: 3
VERSION: v0.1
"""
import sys, json, subprocess, hashlib
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))  # WRIL::SELF_PATH::v1
RAIZ = Path(__file__).resolve().parents[1]
PATRONES = ("neurobit_", "wril_", "port_lighthouse", "backend_instalador", "despertador_hub")
PUERTOS = (5000, 5001, 5002, 5003, 5005, 5010, 8080)
BUZONES = ("buzon_salida", "core/buzon_salida", "INSTALACION_/modulos/buzon_salida")
LOGS = ("logs/hub_dinamico.log", "logs/dispatcher_cartero.log", "logs/faro_puente.log",
        "INSTALACION_/logs/instalador_ludico.log", "sesiones/wal_consola.log")
COLISIONES = (("README_ECN_Workspace_Canonico_v3.md", "data/MD/README_ECN_Workspace_Canonico_v3.md"),
              ("corre_rubrica.sh", "wril/corre_rubrica.sh"),
              ("uso_en_parche.py", "wril/uso_en_parche.py"))
def vivo(pid): return Path(f"/proc/{pid}").exists()
def sha8(p):
    p = Path(p)
    return hashlib.sha256(p.read_bytes()).hexdigest()[:8] if p.exists() else "ausente"
def sec(t): print(f"\n=== {t} ===")
sec("1 RAÍZ Y ANCLA")
print("RAIZ_VISOR:", RAIZ)
inf = RAIZ / "where_am_I.inf"
if inf.exists():
    txt = inf.read_text(encoding="utf-8", errors="ignore")
    for l in txt.splitlines(): print("  .inf:", l)
    log = [l.split("=",1)[1] for l in txt.splitlines() if l.startswith("RAIZ_LOGICA=")]
    print("  ¿coincide?:", "SÍ" if log and log[0]==str(RAIZ) else "NO (mudanza sin re-sellar)")
else: print("  .inf: AUSENTE")
sec("2 KERNEL (ps / ss)")
out = subprocess.run(["ps","-eo","pid=,etimes=,args="],capture_output=True,text=True).stdout
for l in out.splitlines():
    if any(p in l for p in PATRONES) and "visor_informes" not in l: print("  VIVO:", l.strip())
ss = subprocess.run(["ss","-tln"],capture_output=True,text=True).stdout
for l in ss.splitlines():
    if any(f":{p} " in l for p in PUERTOS): print("  MUELLE:", l.strip())
sec("3 ÍNDICES DECLARADOS")
pdir = RAIZ/"pids"
if pdir.exists():
    for pf in sorted(pdir.glob("*.pid")):
        pid = pf.read_text().strip()
        print(f"  {pf.name}: pid={pid} vive={vivo(pid)}")
else: print("  pids/: AUSENTE")
iden = RAIZ/"data/runtime/api_port.identity"
print("  api_port.identity:", (iden.read_text(encoding='utf-8').strip() if iden.exists() else "AUSENTE"))
tmp = RAIZ/"data/runtime/procesos_iniciados.tmp"
print("  procesos_iniciados.tmp:", ((tmp.read_text(encoding='utf-8').strip() or "VACÍO") if tmp.exists() else "AUSENTE"))
er = RAIZ/"estado_real.json"
if er.exists():
    d = json.loads(er.read_text(encoding="utf-8"))
    print("  estado_real.json t:", d.get("t"), "|", ", ".join(f"{c['nombre']}:{c['estado']}" for c in d.get("componentes",[])))
else: print("  estado_real.json: AUSENTE")
sec("4 BUZONES Y CARTAS")
for b in BUZONES:
    d = RAIZ/b
    if d.exists():
        cartas = sorted(p.name for p in d.glob("carta_*"))
        print(f"  {b}: {len(cartas)} carta(s)", cartas if cartas else "")
    else: print(f"  {b}: AUSENTE")
sec("5 COLAS DE LOGS (últimas 4 líneas)")
for lg in LOGS:
    p = RAIZ/lg
    print(f"  --- {lg}")
    if p.exists():
        for l in p.read_text(encoding="utf-8", errors="ignore").splitlines()[-4:]: print("   ", l)
    else: print("    AUSENTE")
sec("6 COLISIONES DE NOMBRE (tamaño + sha256:8)")
for a,b in COLISIONES:
    pa, pb = RAIZ/a, RAIZ/b
    sa = pa.stat().st_size if pa.exists() else -1
    sb = pb.stat().st_size if pb.exists() else -1
    print(f"  {a}: {sa}B {sha8(pa)} | {b}: {sb}B {sha8(pb)} | {'IDÉNTICOS' if sha8(pa)==sha8(pb) else 'DIFIEREN'}")
sec("7 FREEZER (conteos)")
for d in ("archive/legacy", "backups_wril", "inbox"):
    p = RAIZ/d
    n = sum(1 for x in p.rglob("*") if x.is_file()) if p.exists() else 0
    print(f"  {d}: {n} archivo(s)")
sec("8 DIRECTORIOS EXTERNOS (solo listado, sin tocar)")
for ext in sys.argv[1:]:
    p = Path(ext).expanduser()
    print(f"  --- {p} ({'existe' if p.exists() else 'AUSENTE'})")
    if p.exists():
        for f in sorted(p.rglob("*"))[:40]:
            if f.is_file(): print(f"    {f.stat().st_size:>9} B  {f}")
print("\n[✓ VISOR] reporte compilado. SOLO LECTURA: nada fue mutado.")
