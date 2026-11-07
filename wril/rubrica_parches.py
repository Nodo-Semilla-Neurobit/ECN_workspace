#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ecosistema Neurobit - WRIL
Módulo: rubrica_parches.py (idempotencia informada + HERENCIA de parche)
Función: v0.2 encadena el linaje de cada parche: hash_prev + padre, y sella
         en el header la marca ##NB::HERENCIA:: que identifica la herencia
         de la modificación. Auditoría precisa y regeneración desde la descripción.
MFN_LOCATION: wril/  |  MFN_LEVEL: 2
VERSION: v0.3
"""
import json, hashlib, re, sys
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

RUBRICA = Path('data/runtime/parches_rubricados.jsonl')
CADENA_HERENCIA = "##NB::HERENCIA::"

def h(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def ultima_rubrica(nombre):
    if not RUBRICA.exists(): return None
    prev = None
    for linea in RUBRICA.read_text(encoding='utf-8').splitlines():
        r = json.loads(linea)
        if r.get('parche') == nombre: prev = r
    return prev

def veredicto(nombre, objetivos):
    prev = ultima_rubrica(nombre)
    if prev is None: return None
    iguales = all(h(o) == prev['hash'].get(str(o)) for o in objetivos)
    return (prev, iguales)

def rubricar(nombre, objetivos, hash_prev=None):
    RUBRICA.parent.mkdir(parents=True, exist_ok=True)
    padre = ultima_rubrica(nombre)
    entrada = {'t': datetime.now().isoformat(), 'parche': nombre,
               'padre': padre['t'] if padre else None,
               'hash_prev': hash_prev or (padre['hash'] if padre else None),
               'hash': {str(o): h(o) for o in objetivos}}
    with open(RUBRICA, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entrada, ensure_ascii=False) + '\n')
    return entrada

def sellar_herencia(ruta, parche, hash_prev):
    """Marca en el header la herencia de la modificación."""
    p = Path(ruta)
    from wril_backup import resguardar
    resguardar(p)  # LEY 2: nunca mutar sin resguardo
    texto = p.read_text(encoding='utf-8')
    marca = f"{CADENA_HERENCIA}{parche} <- {hash_prev[:8]}"
    if CADENA_HERENCIA in texto:
        texto = re.sub(re.escape(CADENA_HERENCIA) + r"[^\n]*", marca, texto, count=1)
    else:
        texto = re.sub(r"(VERSION:[^\n]*)", rf"\1\n{marca}", texto, count=1)
    p.write_text(texto, encoding='utf-8')