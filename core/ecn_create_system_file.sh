#!/usr/bin/env bash
# =====================================================================
# Ecosistema Neurobitrónica - Módulo: core/ecn_create_system_file.sh
# Función: Extraer de /_TEMP, mover, limpiar extensión y renombrar al ECN_ROOT.
# MFN_LOCATION: core/
# VERSION: v1.1
# =====================================================================
set -eu

# 1. Absorber el ancla del territorio calculada previamente por ecn_root_detect.sh
if [ -f "ecn_root.cfg" ]; then
    # Leer el archivo de configuración limpiando retornos de carro
    ECN_ROOT=$(grep "ECN_ROOT=" ecn_root.cfg | cut -d'=' -f2 | tr -d '\r')
else
    # Fallback fisiológico de emergencia si el archivo .cfg fue borrado
    ECN_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi

if [ -z "${1:-}" ]; then
    echo "[X ERROR] Sintaxis inválida. Uso: ./ecn_create_system_file.sh [basic_module_filename]"
    exit 1
fi

BASIC_MODULE_FILENAME="$1"
TEMP_FILE="${ECN_ROOT}/_TEMP/${BASIC_MODULE_FILENAME}_extract.tmp"
DESTINO_FINAL="${ECN_ROOT}/core/${BASIC_MODULE_FILENAME}"

# Si el módulo pertenece a la raíz o a otra capa según el censo, ajustar
if [[ "$BASIC_MODULE_FILENAME" == *.sh ]] || [[ "$BASIC_MODULE_FILENAME" == *.cfg ]]; then
    DESTINO_FINAL="${ECN_ROOT}/${BASIC_MODULE_FILENAME}"
fi

echo "[✓ MOVIMIENTO] Procesando buffer temporal para: ${BASIC_MODULE_FILENAME}"

if [ -f "$TEMP_FILE" ]; then
    # Remover la cadena '_extract.tmp' y reubicar de forma atómica en el territorio real
    cp "$TEMP_FILE" "$DESTINO_FINAL"
    chmod +x "$DESTINO_FINAL" # Garantizar la capacidad operativa del script
    
    # Limpieza higiénica del espacio de intercambio volátil
    rm -f "$TEMP_FILE"
    echo "[✓ CRISTALIZACIÓN] El artefacto ha mutado exitosamente a su estado definitivo en: ${DESTINO_FINAL}"
else
    echo "[X ERROR] No se localizó el buffer vivo en ${TEMP_FILE}. Revisa la traza del parser."
    exit 1
fi

