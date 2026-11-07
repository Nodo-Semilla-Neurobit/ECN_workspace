#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ecosistema Neurobit - Superparser (semilla v0.1)
Función: resolución capacidad→compartimento→módulo→línea sobre el compendio
         maestro. NO muta: extrae por línea/firma y despacha el resultado.
         WRIL resuelve territorio; esto entiende la solicitud. No se fusionan.
MFN_LOCATION: core/  |  MFN_LEVEL: 3
VERSION: v0.1
"""
from pathlib import Path

def extraer_por_linea(compendio, li, lf):
    """La operación atómica: línea x … extraer x líneas."""
    lineas = Path(compendio).read_text(encoding='utf-8', errors='ignore').splitlines()
    return "\n".join(lineas[li-1:lf])

def consultar_catalogo(catalogo, capacidad):
    """Devuelve el compartimento cuya firma/orientación responde a la capacidad."""
    for c in catalogo:
        if capacidad in c.get('orientacion','') or capacidad in c.get('firma',[]):
            return c
    return None

def resolver(solicitud, catalogo, compendio):
    c = consultar_catalogo(catalogo, solicitud)
    if not c: return None
    return {'compartimento': c['compartimento'], 'modulo': c['modulo'],
            'linea': (c['linea_inicio'], c['linea_fin']),
            'codigo': extraer_por_linea(compendio, c['linea_inicio'], c['linea_fin'])}