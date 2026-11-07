#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL
Módulo: wril_path_resolver.py
Función: CONSULTA el índice (direccionamiento lógico). Si falla, regenera
         hasta [n] intentos; agotados, reporta por end-point y por carta.
MFN_LOCATION: wril/  |  MFN_LEVEL: 2
VERSION: v0.2 (depuracion [n]_intentos canonizada)
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import json
from pathlib import Path
from datetime import datetime
from wril_path_map import generar_mapa
from wril_root_alias import resolve_ecn_root

RAIZ = resolve_ecn_root()  # WRIL::RAIZ_CANONICA
BUZON = RAIZ / "buzon_salida"
MAX_INTENTOS = 3

class PathResolver:
    def __init__(self, raiz: Path = RAIZ, max_intentos: int = MAX_INTENTOS):
        self.raiz = raiz
        self.map_file = raiz / "path_map.json"
        self.max_intentos = max_intentos
        self.path_map = self._load()

    def _load(self):
        if self.map_file.exists():
            return json.loads(self.map_file.read_text(encoding="utf-8"))
        return {}

    def resolve(self, filename: str) -> Path:
        intentos = 0
        while intentos <= self.max_intentos:
            if filename in self.path_map:
                return Path(self.path_map[filename])
            for clave, valor in self.path_map.items():
                if Path(clave).name == filename:
                    return Path(valor)
            intentos += 1
            self.path_map = generar_mapa(self.raiz, self.map_file)
        self._reportar_fallo(filename, intentos)
        raise FileNotFoundError(f"WRIL: '{filename}' irresoluble tras {intentos} regeneraciones.")

    def _reportar_fallo(self, filename, intentos):
        cuerpo = (f"REPORTE WRIL: PathResolver agotó {intentos} regeneraciones sin "
                  f"localizar '{filename}'. Revisar topología o declaración MFN.")
        try:  # 1) end-point HTTP local, si la Sala está despierta
            import urllib.request
            req = urllib.request.Request(
                "http://127.0.0.1:5000/ingesta_neurobit",
                data=json.dumps({"payload": cuerpo, "origen": "wril_path_resolver",
                                 "class_filter": "reporte"}).encode(),
                headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=2)
        except Exception:
            pass
        # 2) carta sellada al buzón: la Oficina enruta el reporte a memoria
        BUZON.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        (BUZON / f"carta_wril_{ts}.txt").write_text(
            "|=•'wril'•=|»|['reporte'.]\n" + cuerpo + "\n[.'reporte']|«|=•'wril'•=|",
            encoding="utf-8")
