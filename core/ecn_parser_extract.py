#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobitrónica - Estación Central Neurobitrónica (ECN) v3.2
Módulo: core/ecn_parser_extract.py
Función: Extraer el Logos de un artefacto desde el compendio inmutable basándose
         en los límites estrictos del Protocolo de Contenedores Semánticos Fractales.
MFN_LOCATION: core/
VERSION: v1.1
"""
import sys
import re
from pathlib import Path

def extraer_logos_desde_compendio(content_target: str):
    p = Path(__file__).resolve().parent
    raiz = p
    for candidato in (p, *p.parents):
        if (candidato / "ecn_codes_compendium.bak").exists():
            raiz = candidato
            break
            
    compendio_path = raiz / "ecn_codes_compendium.bak"
    temp_dir = raiz / "_TEMP"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    if not compendio_path.exists():
        print(f"[X ERROR] Archivo compendio ausente: {compendio_path.name}. Imposible resolver extracción.")
        sys.exit(1)
        
    try:
        content_bak = compendio_path.read_text(encoding="utf-8", errors="ignore")
        
        # STRING_PARSE estructurado según la gramática normativa del protocolo de contenedores fractales:
        # |=•'[FORMAT]_CODE'•=|»{ [SOURCE_CODE] }«|=•'[FORMAT]_CODE'•=|
        # Compilamos una Regex multilínea no codiciosa que busque el contenedor específico del filename
        pattern = re.compile(
            r"\|=\•'([^']+)_CODE'\•=\|»\{\s*([\s\S]*?)\s*\}«\|=\•'\1_CODE'\•=\|", 
            re.MULTILINE
        )
        
        matches = pattern.findall(content_bak)
        source_code_encontrado = None
        
        # Escaneamos los bloques extraídos buscando la correspondencia interna por firma o metadato
        for fmt, code in matches:
            # Si el contenedor contiene la declaración de la ruta física buscada o su cabecera MFN
            if content_target in code or f"Módulo: core/{content_target}" in code or f"Archivo: '{content_target}'" in code:
                source_code_encontrado = code
                break
                
        # Fallback de parseo lineal si el contenedor es directo e inequívoco
        if not source_code_encontrado:
            # Buscar coincidencia exacta por bloques planos en caso de formatos simplificados
            if content_target in content_bak:
                # Intento de extracción por límites crudos si el contenedor viene empaquetado directamente
                segmentos = content_bak.split(f"Archivo: '{content_target}'")
                if len(segmentos) > 1:
                    bloque_post = segmentos[1].split("FINAL")
                    if len(bloque_post) > 0:
                        sub_bloque = bloque_post[0]
                        if "-Inicio:" in sub_bloque:
                            source_code_encontrado = sub_bloque.split("-Inicio:")[1].strip()

        if source_code_encontrado:
            # Formato de salida mandatorio: /_TEMP/[CONTENT]_extract.tmp
            archivo_extract = temp_dir / f"{content_target}_extract.tmp"
            archivo_extract.write_text(source_code_encontrado, encoding="utf-8")
            print(f"[✓ EXTRACCIÓN] Búfer temporal sembrado con éxito en: _TEMP/{content_target}_extract.tmp")
        else:
            print(f"[X ALERTA] No se encontró la firma semántica de '{content_target}' dentro del compendio histórico.")
            
    except Exception as e:
        print(f"[X CRITICAL] Falla en el motor de parseo lingüístico: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[X ERROR] Se requiere especificar el [CONTENT] string de búsqueda.")
        sys.exit(1)
        
    content_target = sys.argv[1].strip()
    extraer_logos_desde_compendio(content_target)

