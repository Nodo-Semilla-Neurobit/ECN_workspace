#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: tools/indice_compendio.py
Función: Indexador y comparador de compendios MODULE_CODES.
  --indice : tabla NRO/archivo/carpeta/rango de líneas + anomalías.
  --diff   : artefactos agregados, faltantes y mudados entre dos compendios.
Principio: SOLO LECTURA de las fuentes; nunca muta originales.
MFN_LOCATION: tools/
MFN_LEVEL: 3
VERSION: v0.2
"""
import re, sys, json
from pathlib import Path

RE_HDR   = re.compile(r"N_Archivos_Actuales:\s*\((\d+)\)")
RE_FECHA = re.compile(r"Analisis_Date:\s*\('([^']*)'\)")
RE_REG   = re.compile(
    r"ARCHIVO NRO\. : \((\d+)\)\s*"
    r"Archivo: \('([^']*)'\);\s*"
    r"Carpeta de ubicación: \('([^']*)'\);\s*"
    r"función: \('([^']*)'\)"
)
MARCA_LISTA = "-LISTA DE ARCHIVOS"

def parsear(texto):
    return [{"nro": int(m.group(1)), "archivo": m.group(2),
             "carpeta": m.group(3), "funcion": m.group(4), "off": m.start()}
            for m in RE_REG.finditer(texto)]

def linea_de(offsets, off):
    lo, hi = 0, len(offsets) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if offsets[mid] <= off: lo = mid
        else: hi = mid - 1
    return lo + 1

def indexar(ruta):
    texto = Path(ruta).read_text(encoding="utf-8", errors="ignore")
    offsets = [0] + [i + 1 for i, ch in enumerate(texto) if ch == "\n"]
    hdr, fecha = RE_HDR.search(texto), RE_FECHA.search(texto)
    declarado = int(hdr.group(1)) if hdr else None
    regs = parsear(texto)
    marca = texto.find(MARCA_LISTA)
    for i, r in enumerate(regs):
        fin = regs[i + 1]["off"] if i + 1 < len(regs) else \
              (marca if marca > r["off"] else len(texto))
        r["linea_inicio"] = linea_de(offsets, r["off"])
        r["linea_fin"]    = linea_de(offsets, fin) - 1
        r["cantidad_lineas"] = r["linea_fin"] - r["linea_inicio"] + 1
    anom, nros = [], [r["nro"] for r in regs]
    if declarado is not None and len(regs) != declarado:
        anom.append(f"declara {declarado} registros; parseados {len(regs)}")
    dup = sorted({n for n in nros if nros.count(n) > 1})
    if dup: anom.append(f"NRO duplicados: {dup}")
    huecos = sorted(set(range(1, max(nros) + 1)) - set(nros)) if nros else []
    if huecos: anom.append(f"NRO faltantes: {huecos}")
    return {"fuente": str(ruta),
            "analisis_date": fecha.group(1) if fecha else None,
            "declarados": declarado, "parseados": len(regs),
            "anomalias": anom}, regs

def cmd_indice(ruta, como_json):
    meta, regs = indexar(ruta)
    if como_json:
        print(json.dumps({"meta": meta, "registros": regs},
                         ensure_ascii=False, indent=1))
        return
    print(f"# INDICE DE COMPENDIO - {meta['fuente']}")
    print(f"Analisis_Date: {meta['analisis_date']} | "
          f"declarados: {meta['declarados']} | parseados: {meta['parseados']}")
    for a in meta["anomalias"]:
        print(f"[!] ANOMALIA: {a}")
    print("\n| NRO | archivo | carpeta | lineas | rango |")
    print("|-|-|-|-|-|")
    for r in regs:
        print(f"| {r['nro']} | {r['archivo']} | {r['carpeta']} "
              f"| {r['cantidad_lineas']} | {r['linea_inicio']}-{r['linea_fin']} |")

def cmd_diff(viejo, nuevo):
    mv, rv = indexar(viejo)
    mn, rn = indexar(nuevo)
    kv = {(r["archivo"], r["carpeta"]) for r in rv}
    kn = {(r["archivo"], r["carpeta"]) for r in rn}
    nom_n = {}
    for r in rn: nom_n.setdefault(r["archivo"], []).append(r["carpeta"])
    agregados = sorted(kn - kv)
    faltantes = sorted(kv - kn)
    mudados = [(a, c, sorted(set(nom_n[a]))) for a, c in faltantes if a in nom_n]
    print("# DIFF DE COMPENDIOS")
    print(f"VIEJO: {mv['fuente']} ({mv['analisis_date']}, {mv['parseados']} regs)")
    print(f"NUEVO: {mn['fuente']} ({mn['analisis_date']}, {mn['parseados']} regs)\n")
    print(f"## AGREGADOS ({len(agregados)})")
    for a, c in agregados: print(f"- {c}/{a}")
    print(f"\n## FALTANTES ({len(faltantes)})")
    for a, c in faltantes: print(f"- {c}/{a}")
    print(f"\n## MUDADOS ({len(mudados)})")
    for arch, origen, dest in mudados:
        print(f"- {arch}: {origen} -> {', '.join(dest)}")

def main():
    a = sys.argv[1:]
    if len(a) >= 2 and a[0] == "--indice":
        cmd_indice(a[1], "--json" in a)
    elif len(a) >= 3 and a[0] == "--diff":
        cmd_diff(a[1], a[2])
    else:
        print("Uso:\n  python3 indice_compendio.py --indice COMPENDIO.txt [--json]"
              "\n  python3 indice_compendio.py --diff VIEJO.txt NUEVO.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()