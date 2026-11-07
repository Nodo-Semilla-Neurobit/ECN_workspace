#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL (Capa de Resolución, Integridad y Circulación)
Módulo: wril_adapter_ecn.py (Puente del Ensamble Primario)
Función: Traduce sobre legacy ECN (MESSAGE_ID/ORIGEN/CONTENT) a carta
         sellada del protocolo fractal, y viceversa. Permite que el Hub
         Dinámico (puerto 5000) y la Oficina de Correos soberana compartan
         buzón y Arca sin fusionarse jamás.
MFN_LOCATION: wril/  |  MFN_LEVEL: 2
VERSION: v0.1
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import json
import re
import uuid
from pathlib import Path
from datetime import datetime

from wril_self_root import detectar_raiz as _raiz_canonica  # WRIL::RAIZ_CANONICA
RAIZ = _raiz_canonica()
BUZON = RAIZ / "buzon_salida"

RE_SELLO = re.compile(r"\|=•'([^']+)'•=\|»(?:\|\['([^'.]+)'\.\])?")
RE_CIERRE = re.compile(r"\[\.?'?[^'\]]*'?\]\|«\|=•'[^']+'•=\|\s*$")

def sobre_a_carta(sobre: dict) -> str:
    """Sobre legacy -> carta sellada (la Oficina la enruta)."""
    accion = str(sobre.get("source", "memoria")).lower()
    clase = sobre.get("tipo", "ecn")
    contenido = sobre.get("CONTENT", sobre.get("content", ""))
    return f"|=•'{accion}'•=|»|['{clase}'.]\n{contenido}\n[.'{clase}']|«|=•'{accion}'•=|"

def carta_a_sobre(texto: str) -> dict:
    """Carta sellada -> sobre legacy (el Arca la recibe)."""
    m = RE_SELLO.search(texto)
    if m:
        accion = m.group(1) or "general"
        clase = m.group(2) or "sin_clase"
        cuerpo = RE_CIERRE.sub("", texto[m.end():])
    else:
        accion, clase, cuerpo = "general", "sin_clase", texto
    return {
        "MESSAGE_ID": f"WRIL_{uuid.uuid4().hex[:8]}",
        "TIMESTAMP": datetime.now().isoformat(),
        "ORIGEN": "WRIL_ADAPTER",
        "ACTION": accion, "CLASS": clase,
        "CONTENT": cuerpo.strip(),
    }

def depositar_desde_legacy(sobre: dict) -> Path:
    """Injerto: el Hub legacy deposita en el buzón de la Oficina."""
    BUZON.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    carta = BUZON / f"carta_ecn_{ts}.txt"
    carta.write_text(sobre_a_carta(sobre), encoding="utf-8")
    return carta

def asentar_en_arca(sobre: dict, arca: Path = None) -> None:
    """Postman 'ecn': append-only sobre el Arca legacy (data/memoria_eva.jsonl)."""
    arca = arca or (RAIZ / "data" / "memoria_eva.jsonl")
    arca.parent.mkdir(parents=True, exist_ok=True)
    with open(arca, "a", encoding="utf-8") as f:
        f.write(json.dumps(sobre, ensure_ascii=False) + "\n")
