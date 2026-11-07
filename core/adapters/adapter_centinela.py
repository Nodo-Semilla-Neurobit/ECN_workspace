#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MFN_LOCATION: core/adapters/
# MFN_LEVEL: 1
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: core/adapters/adapter_centinela.py
Función: Puente entre el Hub Dinámico y centinela_monitor.py existente.
VERSION: v1.0
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import json
import subprocess
import sys
from pathlib import Path
from core.adapters.base import BaseAdapter

ROOT = Path(__file__).resolve().parents[2]
STATE_FILE = ROOT / "data" / ".centinela_state"


class CentinelaAdapter(BaseAdapter):
    def get_module_id(self) -> str:
        return "nb.sos_centinela"

    def get_metadata(self) -> dict:
        return {
            "module_id": self.get_module_id(),
            "version": "1.0.0",
            "endpoints": [
                {"path": "/centinela_status", "methods": ["GET"],
                 "handler": "centinela_status",
                 "description": "Estado del monitor de clipboard",
                 "output_schema": {"type": "object",
                                   "properties": {"status": {"type": "string"}},
                                   "required": ["status"]}},
                {"path": "/start_centinela", "methods": ["POST"],
                 "handler": "start_centinela",
                 "description": "Arranca centinela_monitor.py en background",
                 "output_schema": {"type": "object",
                                   "properties": {"status": {"type": "string"}},
                                   "required": ["status"]}},
            ],
        }

    def _script(self):
        for candidato in (ROOT / "modules" / "centinela_monitor.py",
                          ROOT / "core" / "centinela_monitor.py"):
            if candidato.exists():
                return candidato
        return None

    def centinela_status(self) -> dict:
        estado = {"status": "unknown", "source": "state_file"}
        try:
            if STATE_FILE.exists():
                estado.update(json.loads(STATE_FILE.read_text(encoding="utf-8")))
        except Exception:
            pass
        script = self._script()
        estado["script"] = str(script) if script else None
        return estado

    def start_centinela(self, payload=None) -> dict:
        script = self._script()
        if script is None:
            return {"status": "error", "detail": "centinela_monitor.py no hallado"}
        subprocess.Popen([sys.executable, str(script), "--start"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         cwd=str(ROOT))
        return {"status": "started", "script": str(script)}
