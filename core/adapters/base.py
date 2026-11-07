#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MFN_LOCATION: core/adapters/
# MFN_LEVEL: 1
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: core/adapters/base.py
Función: Interfaz formal BaseAdapter + validación de contratos
         (mini JSON-Schema sin dependencias externas). Design by Contract.
VERSION: v1.0
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

from abc import ABC, abstractmethod
from typing import Dict, Any


class ValidationError(Exception):
    """Incumplimiento de contrato de entrada o salida."""


def check_schema(payload: Any, schema: Dict[str, Any], path: str = "$") -> None:
    """Validación mínima: type, required, properties, enum."""
    if not schema:
        return
    tipo = schema.get("type")
    if tipo == "object":
        if not isinstance(payload, dict):
            raise ValidationError(f"{path}: se esperaba object")
        for req in schema.get("required", []):
            if req not in payload:
                raise ValidationError(f"{path}: falta campo requerido '{req}'")
        for clave, sub in schema.get("properties", {}).items():
            if clave in payload:
                check_schema(payload[clave], sub, f"{path}.{clave}")
    elif tipo == "string":
        if not isinstance(payload, str):
            raise ValidationError(f"{path}: se esperaba string")
        if "enum" in schema and payload not in schema["enum"]:
            raise ValidationError(f"{path}: valor fuera de enum {schema['enum']}")
    elif tipo == "number":
        if isinstance(payload, bool) or not isinstance(payload, (int, float)):
            raise ValidationError(f"{path}: se esperaba number")
    elif tipo == "integer":
        if isinstance(payload, bool) or not isinstance(payload, int):
            raise ValidationError(f"{path}: se esperaba integer")
    elif tipo == "boolean":
        if not isinstance(payload, bool):
            raise ValidationError(f"{path}: se esperaba boolean")
    elif tipo == "array":
        if not isinstance(payload, list):
            raise ValidationError(f"{path}: se esperaba array")


class BaseAdapter(ABC):
    """Interfaz base para todos los adaptadores de la ECN."""

    @abstractmethod
    def get_module_id(self) -> str: ...

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]: ...

    def validate_input(self, payload: Dict[str, Any], endpoint_path: str) -> None:
        check_schema(payload, self._schema_de(endpoint_path, "input_schema"))

    def validate_output(self, result: Dict[str, Any], endpoint_path: str) -> None:
        check_schema(result, self._schema_de(endpoint_path, "output_schema"))

    def _schema_de(self, endpoint_path: str, clave: str):
        for ep in self.get_metadata().get("endpoints", []):
            if ep.get("path") == endpoint_path:
                return ep.get(clave)
        return None
