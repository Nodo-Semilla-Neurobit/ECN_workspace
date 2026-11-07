#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MFN_LOCATION: core/adapters/
# MFN_LEVEL: 1
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: core/adapters/adapter_centinela_legacy.py
Función: Puente entre el Centinela WebSocket legacy (Message Builder) y la
         Oficina de Correos soberana. Traduce el protocolo Centinela
         (MESSAGE_ID, EMISOR, ASUNTO, CONTEXT, TIMESTAMP) al formato de
         cartas selladas del buzón de salida. Sin lógica de negocio.
VERSION: v1.0
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import json
from datetime import datetime
from pathlib import Path
from core.adapters.base import BaseAdapter

RAIZ = Path(__file__).resolve().parents[1]  # WRIL::RAIZ_PLEGADAs[2]
BUZON = RAIZ / "buzon_salida"

class CentinelaLegacyAdapter(BaseAdapter):
    def __init__(self):
        self.module_id = "nb.centinela_legacy"
        self.metadata = {
            "module_id": self.module_id,
            "version": "1.0.0",
            "endpoints": [
                {"path": "/centinela_ingest", "methods": ["POST"],
                 "handler": "centinela_ingest",
                 "description": "Recibe mensaje del Centinela legacy y lo sella como carta",
                 "input_schema": {"type": "object",
                                  "properties": {"fields": {"type": "object"},
                                                 "body": {"type": "string"},
                                                 "full_text": {"type": "string"}},
                                  "required": ["fields"]},
                 "output_schema": {"type": "object",
                                   "properties": {"estado": {"type": "string"},
                                                  "archivo": {"type": "string"}},
                                   "required": ["estado"]}},
            ],
        }

    def get_module_id(self): return self.module_id
    def get_metadata(self): return self.metadata

    def validate_input(self, payload, path):
        if path == "/centinela_ingest":
            if not isinstance(payload, dict) or "fields" not in payload:
                from core.adapters.base import ValidationError
                raise ValidationError(f"{path}: falta 'fields'")

    def validate_output(self, result, path): pass

    def centinela_ingest(self, payload=None):
        BUZON.mkdir(parents=True, exist_ok=True)
        fields = (payload or {}).get("fields", {})
        body = (payload or {}).get("body", "")
        message_id = fields.get("message_id", "unknown")
        emisor = fields.get("emisor", "centinela_legacy")
        asunto = fields.get("asunto", "sin_asunto")
        context = fields.get("context", "PROTOCOLO_MENSAJES")
        perspectiva = fields.get("perspectiva", "SINGULAR_HUMANA")
        fase = fields.get("fase", "sin_fase")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        carta = BUZON / f"carta_centinela_{ts}.txt"
        contenido = (
            f"|=•'centinela'•=|»|['{message_id}'.]\n"
            f"EMISOR: {emisor}\n"
            f"ASUNTO: {asunto}\n"
            f"CONTEXT: {context}\n"
            f"PERSPECTIVA: {perspectiva}\n"
            f"FASE: {fase}\n"
            f"TIMESTAMP: {fields.get('timestamp', datetime.now().isoformat())}\n"
            f"---\n{body}\n"
            f"[.'{message_id}']|«|=•'centinela'•=|"
        )
        carta.write_text(contenido, encoding="utf-8")
        return {"estado": "CARTA_DEPOSITADA", "archivo": carta.name}
