#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL
Módulo: wril_root_alias.py
Función: resolver la raíz de trabajo de forma independiente del nombre literal del
         directorio físico. El sistema usa un alias canónico (ECN_ROOT) que apunta
         al directorio real y evita acoplarse a rutas con caracteres especiales.
MFN_LOCATION: wril/  |  MFN_LEVEL: 2
VERSION: v0.1
"""

from __future__ import annotations

import os
from pathlib import Path

CANONICAL_ALIAS = "ECN_ROOT"
ROOT_MARKERS = ("wril", "core", "README_ECN_Workspace_Canonico_v3.md")


def find_ecn_root(start: Path | str | None = None) -> Path:
    """Descubre la raíz real del proyecto sin depender del nombre literal."""
    if start is None:
        base = Path(__file__).resolve().parents[1]
    else:
        base = Path(start).resolve()

    candidates = [base, *base.parents]
    for candidate in candidates:
        if all((candidate / marker).exists() for marker in ("wril", "core")) and (
            candidate / "README_ECN_Workspace_Canonico_v3.md"
        ).exists():
            return candidate.resolve()

    return base.resolve()


def export_ecn_root(start: Path | str | None = None, alias_name: str = CANONICAL_ALIAS) -> Path:
    """Registra la raíz canónica como alias de entorno para el proceso actual."""
    root = find_ecn_root(start)
    os.environ[alias_name] = str(root)
    return root


def resolve_ecn_root(start: Path | str | None = None, alias_name: str = CANONICAL_ALIAS) -> Path:
    """Devuelve la raíz real del proyecto y normaliza el alias canónico."""
    env_value = os.environ.get(alias_name)
    if env_value:
        env_path = Path(env_value).expanduser().resolve(strict=False)
        if env_path.exists():
            return env_path

    return export_ecn_root(start, alias_name=alias_name)
