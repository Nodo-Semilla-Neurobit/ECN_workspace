#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MFN_LOCATION: core/
# MFN_LEVEL: 1
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: core/module_connector.py
Función: Registry de adaptadores. Carga dinámica desde core/adapters/,
         instanciando toda subclase de BaseAdapter declarada en cada archivo.
VERSION: v1.0
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import importlib.util
import inspect
from pathlib import Path
from typing import Dict, Optional


class ModuleConnector:
    def __init__(self, adapters_dir=None):
        root = Path(__file__).resolve().parent.parent
        self.adapters_dir = Path(adapters_dir) if adapters_dir else root / "core" / "adapters"
        self._registry: Dict[str, object] = {}
        self.reload_adapters()

    def reload_adapters(self) -> None:
        self._registry = {}
        if not self.adapters_dir.exists():
            return
        from core.adapters.base import BaseAdapter
        for archivo in sorted(self.adapters_dir.glob("adapter_*.py")):
            try:
                spec = importlib.util.spec_from_file_location(
                    f"nb_adapter_{archivo.stem}", archivo)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                for _, cls in inspect.getmembers(mod, inspect.isclass):
                    if issubclass(cls, BaseAdapter) and cls.__module__ == mod.__name__:
                        instancia = cls()
                        self._registry[instancia.get_module_id()] = instancia
            except Exception as e:
                print(f"[connector] error cargando {archivo.name}: {e}")

    def get_adapters(self) -> Dict[str, object]:
        return dict(self._registry)

    def get_adapter(self, module_id: str) -> Optional[object]:
        return self._registry.get(module_id)
