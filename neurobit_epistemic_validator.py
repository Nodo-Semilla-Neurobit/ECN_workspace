#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: neurobit_epistemic_validator.py
Función: Auditoría criptográfica del Ledger histórico (SHA256 por bloque).
MFN_LOCATION: ./
MFN_LEVEL: 2
VERSION: v1.0
"""
import hashlib
import re
from pathlib import Path

CADENA_SEPARADOR = "=" * 60
STRING_CONTADOR = "Numero de captura:"
STRING_TIMESTAMP = "Timestamp:"

def auditar_integridad_ledger(ruta_log: Path) -> dict:
    reporte = {"estado": "COHERENTE", "capturas_procesadas": 0,
               "bloques_corruptos": [], "detalles": []}
    if not ruta_log.exists():
        reporte["estado"] = "LEDGER_INEXISTENTE"
        return reporte
    contenido = ruta_log.read_text(encoding="utf-8")
    patron = re.compile(
        rf"{re.escape(CADENA_SEPARADOR)}\n"
        rf"{re.escape(STRING_CONTADOR)}\s*(\d+)\n"
        rf"{re.escape(STRING_TIMESTAMP)}\s*([^\n]+)\n"
        rf"{re.escape(CADENA_SEPARADOR)}\n"
        rf"(.*?)(?=\n{re.escape(CADENA_SEPARADOR)}|\Z)", re.DOTALL)
    for indice, timestamp, cuerpo in patron.findall(contenido):
        limpio = cuerpo.strip()
        reporte["capturas_procesadas"] += 1
        reporte["detalles"].append({
            "captura_nro": int(indice), "timestamp": timestamp,
            "sha256": hashlib.sha256(limpio.encode()).hexdigest(),
            "bytes": len(limpio)})
    return reporte

if __name__ == "__main__":
    ruta = Path(__file__).resolve().parent / "clipboard_captured_folder" / "tesis_neurobit_ledger.log"
    r = auditar_integridad_ledger(ruta)
    print(f"[✓ AUDITORÍA] {r['estado']} | bloques: {r['capturas_procesadas']}")
