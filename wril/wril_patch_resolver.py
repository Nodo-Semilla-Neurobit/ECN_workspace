#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL
Módulo: wril_patch_resolver.py
Función: Motor de reconciliación referencia-logica vs estado-fisico.
         Pipeline: locate -> detect -> resolve -> generate -> backup ->
         apply -> verify. SOSPathFixer = primera implementacion.
MFN_LOCATION: wril/  |  MFN_LEVEL: 2
VERSION: v0.1
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import re
from pathlib import Path
from wril_backup import resguardar
from wril_path_resolver import PathResolver

PATRONES_OBSOLETOS = [
    r'~/WORKSPACE_NEUROBIT_V0\.\d([^"\'\s]*)',
    r'/home/[^/]+/WORKSPACE_NEUROBIT_V0\.\d([^"\'\s]*)',
    r'\$HOME/WORKSPACE_NEUROBIT_V0\.\d([^"\'\s]*)',
    r'~/NEUROBIT-Widget([^"\'\s]*)',
]

class PatchResolver:
    def __init__(self, raiz: Path):
        self.raiz = raiz
        self.resolver = PathResolver(raiz)

    def locate_target(self, script: Path) -> Path:
        return self.resolver.resolve(Path(script).name)

    def detect_stale_reference(self, contenido: str):
        for patron in PATRONES_OBSOLETOS:
            for m in re.finditer(patron, contenido):
                yield m.group(0), m.group(1)

    def resolve_target(self, relativa: str):
        try:
            return self.resolver.resolve(Path(relativa).name)
        except FileNotFoundError:
            return None

    def generate_patch(self, contenido: str):
        return [(v, str(self.resolve_target(r)))
                for v, r in self.detect_stale_reference(contenido)
                if self.resolve_target(r)]

    def backup(self, script: Path):
        return resguardar(script)

    def apply(self, script: Path, cambios):
        texto = script.read_text(encoding="utf-8")
        for vieja, nueva in cambios:
            texto = texto.replace(vieja, nueva, 1)
        script.write_text(texto, encoding="utf-8")

    def verify(self, script: Path) -> bool:
        texto = script.read_text(encoding="utf-8")
        return not any(True for _ in self.detect_stale_reference(texto))

    def reconcile(self, script: Path, dry_run: bool = True) -> dict:
        script = self.locate_target(script)
        cambios = self.generate_patch(script.read_text(encoding="utf-8"))
        reporte = {"archivo": str(script), "cambios": cambios, "aplicado": False}
        if cambios and not dry_run:
            self.backup(script)                 # siempre antes de mutar
            self.apply(script, cambios)
            reporte["aplicado"] = self.verify(script)
        return reporte
