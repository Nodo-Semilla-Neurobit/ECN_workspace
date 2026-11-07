#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ecosistema Neurobit - WRIL
Módulo: wril_firma_funcional.py (CAPA 4 de identidad)
Función: extrae la firma funcional de cada artefacto (def/class en .py,
         funciones en .sh, function/const en .js, encabezados en .md).
         Si el nombre falla, la firma descubre al módulo y actualiza el mapa.
         Los .md con diagrama y operación son identidad legible para el Aula.
MFN_LOCATION: wril/  |  MFN_LEVEL: 2
VERSION: v0.1
"""
import ast, re, json
from pathlib import Path
from wril_self_root import detectar_raiz

RAIZ = detectar_raiz()
RE_SH  = re.compile(r'^\s*(?:function\s+([\w-]+)|([\w-]+)\s*\(\)\s*\{)', re.M)
RE_JS  = re.compile(r'(?:function\s+([\w$]+)|(?:const|let|var)\s+([\w$]+)\s*=)', re.M)
RE_MD  = re.compile(r'^#{1,3}\s+(.+)$', re.M)

def firma_python(ruta):
    try:
        arbol = ast.parse(ruta.read_text(encoding='utf-8', errors='ignore'))
    except SyntaxError:
        return []
    return sorted({n.name for n in ast.walk(arbol)
                   if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))})

def firma_texto(ruta, patron, grupo=0):
    texto = ruta.read_text(encoding='utf-8', errors='ignore')
    return sorted({m.group(g) or m.group(g + 1) for m in patron.finditer(texto)
                   if (m.group(g) or m.group(g + 1))}) if grupo == 0 else \
           sorted({m.group(1) for m in patron.finditer(texto)})

def firma_de(ruta):
    ext = ruta.suffix.lower()
    if ext == '.py':  return firma_python(ruta)
    if ext == '.sh':  return firma_texto(ruta, RE_SH)
    if ext == '.js':  return firma_texto(ruta, RE_JS)
    if ext == '.md':  return firma_texto(ruta, RE_MD, grupo=1)
    return []

def registrar_firmas(salida=None):
    salida = salida or (RAIZ / 'data' / 'runtime' / 'firmas_funcionales.json')
    firmas = {}
    for f in RAIZ.rglob('*'):
        if f.is_file() and f.suffix in ('.py', '.sh', '.js', '.md'):
            firma = firma_de(f)
            if firma:
                firmas[str(f.relative_to(RAIZ))] = firma
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(json.dumps(firmas, ensure_ascii=False, indent=1), encoding='utf-8')
    return firmas

def buscar_por_firma(nombre_funcion, firmas=None):
    """Descubre qué artefacto contiene la función pedida (CAPA 4)."""
    firmas = firmas or json.loads((RAIZ / 'data' / 'runtime' /
                     'firmas_funcionales.json').read_text(encoding='utf-8'))
    return [ruta for ruta, firma in firmas.items() if nombre_funcion in firma]

if __name__ == '__main__':
    n = registrar_firmas()
    print(f'[✓ FIRMA] {len(n)} artefactos con Logos operativo indexado.')
