#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - PSI
Módulo: extensions/psi/ps1_gemelo/ps1_gemelo.py
Función: Detecta párrafos idénticos entre archivos del lote y frases firma
         (patrones de entrenamiento corporativo); asienta observaciones en
         observaciones_gemelos.lst y deposita resultado atado a la cadena.
MFN_LOCATION: extensions/psi/ps1_gemelo/ | MFN_LEVEL: 3
VERSION: v0.1
"""
import sys, json, hashlib, re, unicodedata, time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
EXT_LEIBLES = {".txt", ".md", ".log", ".jsonl"}
UMBRAL_MIN = 40   # descarta frases triviales

def norm(t: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", t)).strip().lower()

def parrafos(texto: str):
    for b in re.split(r"\n\s*\n", texto):
        b = b.strip()
        if len(b) >= UMBRAL_MIN:
            yield b

def main(cadena: str, out_dir: Path):
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    lote_root = RAIZ / "extensions" / "psi" / "psi_ingesta"
    lotes = [d for d in lote_root.iterdir() if d.is_dir()] if lote_root.exists() else []
    firmas_path = Path(__file__).parent / "frases_firma.lst"
    firmas = []
    if firmas_path.exists():
        firmas = [norm(l) for l in firmas_path.read_text(encoding="utf-8").splitlines()
                 if l.strip() and not l.startswith("#")]

    indice, observ = {}, []
    for ld in lotes:
        for arch in sorted(ld.rglob("*")):
            if not arch.is_file() or arch.suffix not in EXT_LEIBLES:
                continue
            if "quarentine" in arch.parts or "HISTORY" in arch.parts:
                continue
            texto = arch.read_text(encoding="utf-8", errors="replace")
            for n, par in enumerate(parrafos(texto), 1):
                h = hashlib.sha256(norm(par).encode()).hexdigest()[:16]
                e = indice.setdefault(h, {"preview": par[:80], "ocurrencias": []})
                e["ocurrencias"].append({"archivo": str(arch.relative_to(RAIZ)),
                                         "parrafo": n})
                for f in firmas:
                    if f and f in norm(par):
                        observ.append({"tipo": "FIRMA", "hash": h,
                                       "frase": f[:60],
                                       "ref": f"{arch.relative_to(RAIZ)}#{n}"})
    gemelos = {h: v for h, v in indice.items() if len(v["ocurrencias"]) > 1}

    out_dir.mkdir(parents=True, exist_ok=True)
    res = out_dir / "ps1_gemelo_resultado.json"
    res.write_text(json.dumps({"cadena": cadena, "gemelos": gemelos,
                               "observaciones": observ},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    lst = out_dir / "observaciones_gemelos.lst"
    with open(lst, "a", encoding="utf-8") as fo:
        for h, v in gemelos.items():
            o = v["ocurrencias"]
            refs = ";".join(f"{x['archivo']}#{x['parrafo']}" for x in o[1:])
            fo.write(f"{ts}|ps1_gemelo|GEMELO|{h}|"
                     f"{o[0]['archivo']}#{o[0]['parrafo']}|{refs}\n")
        for ob in observ:
            fo.write(f"{ts}|ps1_gemelo|{ob['tipo']}|{ob['hash']}|"
                     f"{ob['ref']}|{ob['frase']}\n")
    logdir = Path(__file__).parent / "logs"
    logdir.mkdir(parents=True, exist_ok=True)
    with open(logdir / "ejecucion.log", "a", encoding="utf-8") as fl:
        fl.write(f"{ts}|OK|gemelos={len(gemelos)}|firmas={len(observ)}|"
                 f"cadena={cadena}\n")
    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv[1], Path(sys.argv[2]))
