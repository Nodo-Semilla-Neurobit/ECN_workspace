#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MFN_LOCATION: core/adapters/
# MFN_LEVEL: 1
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: core/adapters/adapter_correos.py
Función: Puente entre el Hub Dinámico (legacy) y la Oficina de Correos
         soberana. Expone /ingesta_neurobit y /correos/status; deposita
         cartas selladas en buzón_salida sin tocar el núcleo.
VERSION: v1.0
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import json
from datetime import datetime
from pathlib import Path

from core.adapters.base import BaseAdapter, ValidationError

RAIZ = Path(__file__).resolve().parents[1]  # WRIL::RAIZ_PLEGADAs[2]
BUZON = RAIZ / "buzon_salida"

class CorreosAdapter(BaseAdapter):
    def __init__(self):
        self.module_id = "nb.core_correos"
        self.metadata = {
            "module_id": self.module_id,
            "version": "1.0.0",
            "endpoints": [
                {"path": "/ingesta_neurobit", "methods": ["POST"],
                 "handler": "ingesta_neurobit",
                 "description": "Deposita una carta sellada en el buzón de salida",
                 "input_schema": {"type": "object",
                     "properties": {"payload": {"type": "string"},
                                    "origen": {"type": "string"},
                                    "class_filter": {"type": "string"}},
                     "required": ["payload"]},
                 "output_schema": {"type": "object",
                     "properties": {"estado": {"type": "string"},
                                    "archivo": {"type": "string"}},
                     "required": ["estado"]}},
                {"path": "/correos/status", "methods": ["GET"],
                 "handler": "correos_status",
                 "description": "Cartas pendientes y estado real de los radios",
                 "input_schema": {}, "output_schema": {"type": "object"}},
            ],
        }

    def get_module_id(self): return self.module_id
    def get_metadata(self): return self.metadata

    def validate_input(self, payload, path):
        if path == "/ingesta_neurobit":
            if not isinstance(payload, dict) or not str(payload.get("payload", "")).strip():
                raise ValidationError(f"{path}: falta 'payload' no vacío")

    def validate_output(self, result, path): pass

    def ingesta_neurobit(self, payload=None):
        BUZON.mkdir(parents=True, exist_ok=True)
        clase = (payload or {}).get("class_filter", "dom_copy")
        origen = (payload or {}).get("origen", "extension")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        carta = BUZON / f"carta_{origen}_{ts}.txt"
        carta.write_text(
            f"|=•'captura'•=|»|['{clase}'.]\n{payload['payload']}\n[.'{clase}']|«|=•'captura'•=|",
            encoding="utf-8")
        return {"estado": "CARTA_DEPOSITADA", "archivo": carta.name}

    def correos_status(self):
        pendientes = sorted(p.name for p in BUZON.glob("carta_*")) if BUZON.exists() else []
        estado_real = {}
        er = RAIZ / "estado_real.json"
        if er.exists():
            try: estado_real = json.loads(er.read_text(encoding="utf-8"))
            except Exception: estado_real = {}
        return {"pendientes": pendientes, "estado_real": estado_real}

