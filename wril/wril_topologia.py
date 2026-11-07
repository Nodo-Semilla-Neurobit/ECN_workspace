#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL (Capa de Resolución, Integridad y Circulación)
Módulo: wril_topologia.py (El Pliegue Topológico)
Función: Lleva la tensión DECLARACIÓN ≠ REALIDAD a cero: muda cada artefacto
         a su MFN_LOCATION declarada con backup previo, parches controlados
         para los .py (rebase RAIZ + shim SELF_PATH), registro histórico y
         reindexación final. Dry-run por defecto; --apply materializa.
MFN_LOCATION: wril/  |  MFN_LEVEL: 2
VERSION: v0.1
"""
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from wril_mfn_registry import auditar_declaraciones
from wril_backup import resguardar
from wril_path_map import generar_mapa

from wril_self_root import detectar_raiz as _raiz_canonica  # WRIL::RAIZ_CANONICA
RAIZ = _raiz_canonica()
HISTORIAL = RAIZ / "wril_historial.jsonl"

SHIM = ("import sys as _ws\n"
        "from pathlib import Path as _wp\n"
        "_ws.path.insert(0, str(_wp(__file__).resolve().parent))"
        "  # WRIL::SELF_PATH::v1\n")

LINEA_RAIZ_VIEJA = "RAIZ = Path(__file__).resolve().parent"
LINEA_RAIZ_NUEVA = ("RAIZ = Path(__file__).resolve().parents[1]"
                    "  # WRIL::RAIZ_PLEGADA")

def parchear_py(ruta: Path):
    """Dos parches controlados e idempotentes sobre el .py plegado."""
    texto = ruta.read_text(encoding="utf-8")
    mutado = False
    if "WRIL::RAIZ_PLEGADA" not in texto and LINEA_RAIZ_VIEJA in texto:
        texto = texto.replace(LINEA_RAIZ_VIEJA, LINEA_RAIZ_NUEVA, 1)
        mutado = True
    if "WRIL::SELF_PATH" not in texto:
        i = texto.find('"""')
        if i != -1:
            j = texto.find('"""', i + 3)
            if j != -1:
                texto = texto[:j + 3] + "\n" + SHIM + texto[j + 3:]
                mutado = True
    if mutado:
        ruta.write_text(texto, encoding="utf-8")

def registrar(entrada: dict):
    with open(HISTORIAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(entrada, ensure_ascii=False) + "\n")

def plegar(dry_run: bool = True):
    reporte = auditar_declaraciones(RAIZ)
    movimientos = []
    for inc in reporte["inconsistentes"]:
        origen = RAIZ / inc["archivo"]
        destino = RAIZ / inc["declara"] / origen.name
        if not origen.exists() or origen == destino:
            continue
        movimientos.append((origen, destino))
        if dry_run:
            continue
        destino.parent.mkdir(parents=True, exist_ok=True)
        if destino.exists():
            resguardar(destino)          # backup antes de sobrescribir
        resguardar(origen)               # preserva el estado previo al pliegue
        shutil.move(str(origen), str(destino))
        if destino.suffix == ".py":
            parchear_py(destino)
        registrar({"t": datetime.now().isoformat(), "archivo": origen.name,
                   "destino": str(destino.relative_to(RAIZ)),
                   "estado": "PLIEGUE_OK"})
    if not dry_run:
        generar_mapa(RAIZ, RAIZ / "path_map.json")   # el índice refleja el pliegue
    return movimientos

if __name__ == "__main__":
    aplicar = "--apply" in sys.argv
    movs = plegar(dry_run=not aplicar)
    print(f"[✓ TOPOLOGIA] {'APLICADO' if aplicar else 'DRY-RUN'}: "
          f"{len(movs)} artefactos por plegar.")
    for o, d in movs[:15]:
        print(f"    {o.name} -> {d.relative_to(RAIZ)}")
    if aplicar:
        residual = auditar_declaraciones(RAIZ)
        print(f"[✓ TOPOLOGIA] Tensión residual: "
              f"{len(residual['inconsistentes'])} inconsistencias.")
    elif movs:
        print("    (ejecutá con --apply para materializar el pliegue)")
