#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MFN_LOCATION: tools/
# MFN_LEVEL: 3
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: tools/ingest_compendium.py
Función: Ingestor unificado de compendios. Divide por separadores
         'ARCHIVO NRO.', extrae el header MFN_LOCATION si existe, y
         deposita cada artefacto en inbox/ para que el WS-Sentinel lo
         rutee a su casa declarada. Append-only sobre salida; NUNCA
         toca el original.
VERSION: v1.0
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]  # WRIL::RAIZ_PLEGADAs[1]
INBOX = RAIZ / "inbox"

RE_BLOQUE = re.compile(
    r"ARCHIVO NRO\.?\s*:\s*\(?(\d+)\)?\s*\nArchivo:\s*\('?(.+?)'?\);",
    re.IGNORECASE)
RE_MFN = re.compile(r"MFN_LOCATION:\s*(\S+)")

def dividir_compendio(texto):
    bloques, matches = [], list(RE_BLOQUE.finditer(texto))
    for i, m in enumerate(matches):
        fin = matches[i + 1].start() if i + 1 < len(matches) else len(texto)
        bloques.append((m.group(2).strip(), texto[m.start():fin]))
    return bloques

def ingerir(compendio: Path, seco: bool = True):
    INBOX.mkdir(parents=True, exist_ok=True)
    texto = compendio.read_text(encoding="utf-8", errors="ignore")
    reporte = []
    for nombre, bloque in dividir_compendio(texto):
        seguro = re.sub(r"[^A-Za-z0-9_.-]", "_", nombre)
        mfn = RE_MFN.search(bloque[:500])
        reporte.append({"archivo": seguro,
                        "declara": mfn.group(1) if mfn else "sin_declaracion"})
        if not seco:
            (INBOX / seguro).write_text(bloque, encoding="utf-8")
    return reporte

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 ingest_compendium.py <compendio.txt> [--apply]")
        sys.exit(1)
    seco = "--apply" not in sys.argv
    rep = ingerir(Path(sys.argv[1]), seco=seco)
    for r in rep:
        print(f"[INGEST] {r['archivo']} -> declara: {r['declara']}")
    print(f"[INGEST] {'DRY-RUN' if seco else 'APLICADO'}: {len(rep)} artefactos hacia inbox/")
