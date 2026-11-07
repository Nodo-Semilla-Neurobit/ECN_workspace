#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MFN_LOCATION: core/adapters/
# MFN_LEVEL: 1
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: core/adapters/adapter_mfn_cartografo.py
Función: Radio visual de la MFN. Puente HTTP localhost entre el Hub Dinámico
         (5000) y el backend del MFN Sprite Cartógrafo (5002).
         Sin lógica de negocio: solo traduce y reenvía.
VERSION: v1.0
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import requests
from core.adapters.base import BaseAdapter, ValidationError

CARTOGRAFO = "http://127.0.0.1:5002"
TIMEOUT = 2

class CartografoAdapter(BaseAdapter):
    def __init__(self):
        self.module_id = "nb.mfn_cartografo"
        self.metadata = {
            "module_id": self.module_id,
            "version": "1.0.0",
            "endpoints": [
                {"path": "/mfn/state", "methods": ["POST"], "handler": "set_state",
                 "description": "Crea/actualiza el estado radial de 169 bits",
                 "input_schema": {"type": "object",
                                  "properties": {"estado": {}},
                                  "required": ["estado"]},
                 "output_schema": {"type": "object",
                                   "properties": {"sprite_id": {"type": "string"},
                                                  "estado": {"type": "array"}},
                                   "required": ["sprite_id"]}},
                {"path": "/mfn/transmission", "methods": ["POST"],
                 "handler": "transmission",
                 "description": "Empaqueta el estado para transmisión a 300 baudios",
                 "input_schema": {"type": "object", "properties": {"estado": {}}},
                 "output_schema": {"type": "object"}},
                {"path": "/mfn/health", "methods": ["GET"], "handler": "health",
                 "description": "Salud del backend del Cartógrafo",
                 "input_schema": {}, "output_schema": {"type": "object"}},
            ],
        }

    def get_module_id(self): return self.module_id
    def get_metadata(self): return self.metadata

    def validate_input(self, payload, path):
        if path == "/mfn/state" and not isinstance(payload, dict):
            raise ValidationError("/mfn/state: se espera object")

    def validate_output(self, result, path): pass

    def _proxy(self, ruta, payload=None):
        try:
            r = (requests.post(CARTOGRAFO + ruta, json=payload, timeout=TIMEOUT)
                 if payload is not None else
                 requests.get(CARTOGRAFO + ruta, timeout=TIMEOUT))
            try: return r.json()
            except ValueError: return {"status": r.status_code}
        except requests.RequestException as e:
            return {"error": "cartografo_offline", "detail": str(e)}

    def set_state(self, payload=None):
        return self._proxy("/api/sprite/create", payload or {})

    def transmission(self, payload=None):
        return self._proxy("/api/sprite/transmission", payload or {})

    def health(self):
        # Un 404 igual significa "conectado"; solo la excepción es offline.
        try:
            requests.get(CARTOGRAFO + "/", timeout=TIMEOUT)
            return {"cartografo": "ONLINE", "puerto": 5002}
        except requests.RequestException as e:
            return {"cartografo": "OFFLINE", "detail": str(e)}
