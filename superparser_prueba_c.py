#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prueba (c): capacidad→compartimento→módulo→línea→código→despacho.
No muta el maestro; solo escribe una carta sellada en inbox/prueba_c/."""
import re, sys, pathlib
CAP  = sys.argv[1]
COMP = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "compendio_base.txt")
CAT = [
  {"compartimento": "m:S2:P1", "orientacion": "resolver ruta",
   "modulo": "wril_path_resolver.py", "firma": ["def resolve", "def _reportar_fallo"]},
  {"compartimento": "m:S4:P2", "orientacion": "unificar proyecciones MFN",
   "modulo": "neurobit_mfn_unificado.py", "firma": ["def ubicar", "def indice"]},
  {"compartimento": "na:S1:P1", "orientacion": "vigilar inbox / enrutar",
   "modulo": "wril_sentinel.py", "firma": ["def enrutar", "def carta_orfandad"]},
]
c = next((x for x in CAT if CAP in x["orientacion"]), None)
if not c:
    print("[X SUPERPARSER] capacidad sin compartimento: " + CAP); sys.exit(1)
txt = COMP.read_text(encoding="utf-8", errors="ignore").splitlines()
pat = re.compile(r"^Archivo:\s*\('?" + re.escape(c["modulo"]) + r"'?\);")
li = next((i for i, l in enumerate(txt) if pat.search(l)), None)
if li is None:
    print("[X SUPERPARSER] módulo no indexado: " + c["modulo"]); sys.exit(1)
lf = next((j for j in range(li + 1, len(txt)) if txt[j].startswith("FINAL")), len(txt))
bloque = "\n".join(txt[li:lf])
ok = all(f in bloque for f in c["firma"])
print(f"[✓ SUPERPARSER] {c['compartimento']} -> {c['modulo']} -> lineas {li+1}..{lf}")
print(f"[✓ FIRMA] {c['firma']} -> {'PRESENTE' if ok else 'AUSENTE (deriva)'}")
out = pathlib.Path("inbox/prueba_c"); out.mkdir(parents=True, exist_ok=True)
carta = out / (CAP.replace(" ", "_") + ".txt")
carta.write_text("|=•'superparser'•=|»|['" + c["compartimento"] + "'.]\n"
                 + f"modulo: {c['modulo']}\nlineas: {li+1}-{lf}\nfirma_ok: {ok}\n"
                 + bloque[:800] + "\n[.'" + c["compartimento"] + "']|«|=•'superparser'•=|",
                 encoding="utf-8")
print("[✓ DESPACHO] carta sellada en " + str(carta))