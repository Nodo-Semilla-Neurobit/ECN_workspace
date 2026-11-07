#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL (Capa de Resolución, Integridad y Circulación)
Módulo: wril_dynamic_tester.py (Module Linker / Dynamic Tester)
Función: Verifica que cada módulo se comporte como declara.
         Pipeline: PATH RESOLUTION -> MODULE DISCOVERY -> PROCESS CONTROL
         -> ENDPOINT TEST. Importación dinámica (rescate canonizado de _loader).
MFN_LOCATION: wril/  |  MFN_LEVEL: 2
VERSION: v0.1
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import importlib.util
import inspect
import subprocess
import time
import json
import urllib.request
from pathlib import Path
from wril_path_resolver import PathResolver

from wril_self_root import detectar_raiz as _raiz_canonica  # WRIL::RAIZ_CANONICA
RAIZ = _raiz_canonica()
CANDIDATOS = ["main", "correr", "run", "generar", "escanear", "auditar",
              "restaurar", "clasificar_y_entregar", "ubicar", "ritual"]

def cargar_modulo(ruta: Path):
    """Descubrimiento sin tocar sys.path: spec + exec aislado."""
    spec = importlib.util.spec_from_file_location("wril_test_" + ruta.stem, str(ruta))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def descubrir_callable(mod):
    for nombre in CANDIDATOS:
        fn = getattr(mod, nombre, None)
        if callable(fn):
            return nombre, fn
    for nombre, obj in inspect.getmembers(mod, inspect.isfunction):
        if obj.__module__ == mod.__name__:
            return nombre, obj
    return None, None

def probar_modulo(nombre_archivo: str) -> dict:
    resolver = PathResolver(RAIZ)
    mapa = resolver.path_map                      # consulta directa, sin cartas de fallo
    ruta = mapa.get(nombre_archivo) or next(
        (v for k, v in mapa.items() if Path(k).name == nombre_archivo), None)
    if not ruta:
        return {"modulo": nombre_archivo, "estado": "IRRESOLUBLE"}
    try:
        mod = cargar_modulo(Path(ruta))           # MODULE DISCOVERY
    except Exception as e:
        return {"modulo": nombre_archivo, "estado": f"IMPORT_ERROR: {e}"}
    nombre_fn, fn = descubrir_callable(mod)
    return {"modulo": nombre_archivo, "callable": nombre_fn,
            "estado": "DESCUBIERTO" if fn else "SIN_CALLABLE"}

def probar_endpoint_sala(url="http://127.0.0.1:5000/ingesta_neurobit",
                         levantar_si_duerme=False, timeout=2) -> dict:
    """PROCESS CONTROL + ENDPOINT TEST sobre la Sala."""
    def _ping():
        try:
            req = urllib.request.Request(url, data=json.dumps(
                {"payload": "PING WRIL", "origen": "wril_dynamic_tester",
                 "class_filter": "ping"}).encode(),
                headers={"Content-Type": "application/json"})
            urllib.request.urlopen(req, timeout=timeout)
            return True
        except Exception:
            return False
    if _ping():
        return {"endpoint": url, "estado": "VIVO"}
    if levantar_si_duerme:
        mapa = PathResolver(RAIZ).path_map
        sala = mapa.get("sala_app.py")
        if not sala:
            return {"endpoint": url, "estado": "SALA_IRRESOLUBLE"}
        proc = subprocess.Popen(["python3", sala], stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
        time.sleep(2)
        vivo = _ping()
        proc.terminate()
        return {"endpoint": url,
                "estado": "LEVANTADO_Y_TESTEADO" if vivo else "LEVANTADO_SIN_RESPUESTA"}
    return {"endpoint": url, "estado": "DORMIDA"}

if __name__ == "__main__":
    for m in ["neurobit_dispatcher.py", "neurobit_mfn_13x13.py",
              "wril_path_map.py", "wril_backup.py", "wril_sentinel.py"]:
        print("[✓ TESTER]", probar_modulo(m))
