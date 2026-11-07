#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL
Módulo: wril_path_map.py
Función: CONSTRUYE el índice nombre -> ubicación. No interpreta, no muta.
MFN_LOCATION: wril/  |  MFN_LEVEL: 2
VERSION: v0.2
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import json, os
from pathlib import Path

from wril_root_alias import resolve_ecn_root

RUIDO = {'.git','__pycache__','.venv','node_modules','backups_wril','buzon_salida','pids'}
EXT = ('.py','.js','.yaml','.json','.md','.sh','.c')
RAIZ = resolve_ecn_root()


def generar_mapa(root_dir: Path | str | None = None, output_file: Path | str | None = None) -> dict:
    root_dir = Path(root_dir).resolve() if root_dir is not None else RAIZ.resolve()
    output_file = Path(output_file) if output_file is not None else root_dir / "path_map.json"
    path_map = {}
    colisiones = []
    
    for root, dirs, files in os.walk(root_dir):
        root_path = Path(root)
        dirs[:] = [d for d in dirs if d not in RUIDO]
        for f in files:
            if f.endswith(EXT):
                try:
                    clave = str((root_path / f).relative_to(root_dir))
                except ValueError:
                    clave = str(root_path / f)
                
                if f in path_map:
                    colisiones.append(f"COLISION: '{f}' en '{path_map[f]}' y '{clave}'")
                
                path_map[clave] = str(root_path / f)
    
    if colisiones:
        from datetime import datetime
        with open(root_dir / "wril_historial.jsonl", "a", encoding="utf-8") as h:
            registro = json.dumps({"t": datetime.now().isoformat(), "tipo": "COLISION_NOMBRES", "detalle": colisiones}, ensure_ascii=False)
            h.write(registro + "\n")
        print(f"[⚠ PATH_MAP] Se detectaron {len(colisiones)} colisiones. Revisar wril_historial.jsonl")

    output_file.write_text(json.dumps(path_map, indent=2, ensure_ascii=False), encoding="utf-8")
    return path_map

if __name__ == "__main__":
    mapa = generar_mapa()
    print(f"[✓ MAPA GENERADO] Índice construido con {len(mapa)} elementos.")


