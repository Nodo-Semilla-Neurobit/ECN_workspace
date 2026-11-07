#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobitrónica - Estación Central Neurobitrónica (ECN) v3.2
Módulo: core/ecn_artifact_check.py
Función: Detectar la existencia de artefactos declarados en ecn_basic_modules.cfg.
         Gatillar el extractor en caso de Tensión Estructural (Ausencia = False).
MFN_LOCATION: core/
VERSION: v1.1
"""
import sys
import os
import subprocess
from pathlib import Path

def detectar_raiz_ecn() -> Path:
    # Intenta localizar el ancla canónica basada en tu ecn_root.cfg o where_am_I.inf
    p = Path(__file__).resolve().parent
    for candidato in (p, *p.parents):
        if (candidato / "ecn_root.cfg").exists() or (candidato / "where_am_I.inf").exists():
            return candidato
    return p

def auditar_existencia_artefacto(filename_modulo: str) -> bool:
    raiz = detectar_raiz_ecn()
    # Buscar el artefacto en el territorio basándose en las rutas relativas o el directorio de ejecución
    ruta_física = raiz / filename_modulo
    
    if ruta_física.exists() and ruta_física.is_file():
        # Devuelve TRUE para que install.sh prosiga con el flujo secuencial ordinario
        print(f"[✓ PRESENCIA] Artefacto detectado en el territorio: {filename_modulo}")
        return True
    else:
        # Devuelve FALSE ante la ausencia física del Logos en la ruta declarada
        print(f"[🚨 TENSIÓN] Artefacto ausente: {filename_modulo}. Invocando ecn_parser_extract.py...")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[X ERROR] Sintaxis inválida. Se requiere: python3 ecn_artifact_check.py [basic_module_filename]")
        sys.exit(1)
        
    basic_module_filename = sys.argv[1].strip()
    
    # Ejecutar censo de presencia física
    if auditar_existencia_artefacto(basic_module_filename):
        # Retorno 0 a nivel de proceso de shell (TRUE para install.sh)
        sys.exit(0)
    else:
        # El artefacto no existe. Se delega la invocación forzosa al extractor asíncrono
        raiz_sistema = detectar_raiz_ecn()
        script_extractor = raiz_sistema / "core" / "ecn_parser_extract.py"
        
        if not script_extractor.exists():
            # Si el extractor no está en core/, probar en la raíz actual de ejecución
            script_extractor = raiz_sistema / "ecn_parser_extract.py"
            
        try:
            # Comando canónico: python3 ecn_parser_extract.py [basic_module_filename]
            resultado = subprocess.run(
                ["python3", str(script_extractor), basic_module_filename],
                cwd=str(raiz_sistema),
                capture_output=True,
                text=True
            )
            # Imprimir traza del extractor en la consola del instalador
            if resultado.stdout: print(resultado.stdout.strip())
            if resultado.stderr: print(resultado.stderr.strip())
        except Exception as e:
            print(f"[X CRITICAL] Error al invocar el extractor secundario: {e}")
            
        # Retorno 1 a nivel de shell (FALSE para install.sh, gatillando la bifurcación remedial)
        sys.exit(1)

