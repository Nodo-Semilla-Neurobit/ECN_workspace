#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MFN_LOCATION: tools/salon/
# MFN_LEVEL: 2
# VERSION: v1.0
"""
ECN · SIMÓN DEL SALÓN v3 · clasificador y secretario de memoria
Reemplaza el rol de postman sin borrarlo: lee envelopes/contenedores,
detecta ACTION_WORD, ORIGEN/DESTINO/TAGS, extrae preguntas abiertas y
decisiones, asienta en data/salon/historial.jsonl (append-only, encadenado)
y emite un informe-resumen para el sello del Director.

VIA_LATERAL_CONSIDERADA: clasificador determinista por patrones, como Simón
  lo hacía con los tags (ejemplo)/(ciencia ficción): el envelope declara su
  plano y el clasificador solo lo lee y lo asienta.
DESCARTE de la vía convencional (clasificador semántico/LLM): exigiría API
  paga o tokens locales para una tarea que el envelope ya resuelve por
  declaración; el veredicto debe ser auditable y reproducible, no probable.

Uso:
  python3 salon_clasificador_simon_v1.py --msg archivo.txt
  cat archivo.txt | python3 salon_clasificador_simon_v1.py --stdin
  python3 salon_clasificador_simon_v1.py --informe
"""
import json, re, sys, hashlib
from pathlib import Path
from datetime import datetime, timezone

def raiz_canonica():
    p = Path(__file__).resolve().parent
    for c in (p, *p.parents):
        if (c / ".ecn_raiz").exists() or (c / "deploy_neurobit_estacion_v3.2.sh").exists():
            return c
    return p

RAIZ  = raiz_canonica()
SALON = RAIZ / "data" / "salon"
SALON.mkdir(parents=True, exist_ok=True)
HIST  = SALON / "historial.jsonl"

CONT_RE  = re.compile(r"\|=•'(?P<action>\w+)'•=\|»")
FIELD_RE = re.compile(r"^(MESSAGE_ID|ORIGEN|DESTINO|TAGS|PERSPECTIVA|CONTEXT|TIMESTAMP|VERSION)\s*:\s*(.+)$", re.M)
PREG_RE  = re.compile(r"¿[^?\n]{5,200}\?")
DEC_RE   = re.compile(r"(sell[áa]s|veredicto|un[áa]nime|LEY\s+DEL|LEY\s+\w+)", re.I)

def sha16(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]

def analizar(texto: str) -> dict:
    fields = {k: v.strip() for k, v in FIELD_RE.findall(texto)}
    return {
        "t": datetime.now(timezone.utc).isoformat(),
        "message_id": fields.get("MESSAGE_ID", ""),
        "origen": fields.get("ORIGEN", "?"),
        "destino": fields.get("DESTINO", "?"),
        "perspectiva": fields.get("PERSPECTIVA", ""),
        "tags": fields.get("TAGS", ""),
        "action_words": sorted(set(CONT_RE.findall(texto))),
        "preguntas_abiertas": PREG_RE.findall(texto)[:8],
        "decisiones": [l.strip()[:160] for l in texto.splitlines() if DEC_RE.search(l)][:6],
        "hash": sha16(texto),
        "canal": "SALON",
    }

def asentar(reg: dict) -> dict:
    prev = ""
    if HIST.exists():
        lines = HIST.read_text(encoding="utf-8", errors="ignore").splitlines()
        if lines:
            try: prev = json.loads(lines[-1]).get("hash", "")
            except Exception: prev = ""
    reg["prev"] = prev
    with open(HIST, "a", encoding="utf-8") as f:
        f.write(json.dumps(reg, ensure_ascii=False) + "\n")
    return reg

def informe():
    regs = []
    if HIST.exists():
        for l in HIST.read_text(encoding="utf-8", errors="ignore").splitlines():
            try: regs.append(json.loads(l))
            except Exception: pass
    por_origen, por_action, preguntas, decisiones = {}, {}, [], []
    for r in regs:
        o = r.get("origen", "?")
        por_origen[o] = por_origen.get(o, 0) + 1
        for a in r.get("action_words", []):
            por_action[a] = por_action.get(a, 0) + 1
        preguntas  += [(o, p) for p in r.get("preguntas_abiertas", [])]
        decisiones += [(o, d) for d in r.get("decisiones", [])]
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out = SALON / f"informe_simon_{ts}.md"
    L = ["# INFORME SIMÓN · SALÓN v3", f"t: {ts} · registros: {len(regs)}", "", "## Por origen"]
    L += [f"- {k}: {v}" for k, v in sorted(por_origen.items(), key=lambda x: -x[1])]
    L += ["", "## Por ACTION_WORD"]
    L += [f"- {k}: {v}" for k, v in sorted(por_action.items(), key=lambda x: -x[1])]
    L += ["", "## Preguntas abiertas (requieren sello del Director)"]
    L += [f"- [{o}] {p}" for o, p in preguntas[-12:]] or ["- (ninguna)"]
    L += ["", "## Decisiones / leyes detectadas"]
    L += [f"- [{o}] {d}" for o, d in decisiones[-12:]] or ["- (ninguna)"]
    out.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print(f"\n[✓ SIMÓN] informe en {out}")

def main():
    args = sys.argv[1:]
    if "--informe" in args:
        informe(); return
    if "--stdin" in args:
        texto = sys.stdin.read()
    elif "--msg" in args:
        i = args.index("--msg")
        texto = Path(args[i + 1]).read_text(encoding="utf-8", errors="ignore")
    else:
        print(__doc__); return
    reg = asentar(analizar(texto))
    print(f"[✓ SIMÓN] asentado: {reg['message_id'] or reg['hash']} · origen {reg['origen']} "
          f"· actions {reg['action_words']} · preguntas {len(reg['preguntas_abiertas'])}")

if __name__ == "__main__":
    main()
