#!/bin/bash
# ==============================================================================
# ECN Command Resolver — Interceptación dinámica de comandos WRIL
# MFN_LOCATION: wril/ | MFN_LEVEL: 1 | VERSION: v1.0
# ==============================================================================
# Propósito: permite invocar módulos ECN por nombre (ej: `wril_sentinel.py`)
# sin rutas absolutas, consultando path_map.json dinámicamente.
#
# Instalación (una sola vez):
#   echo 'source /ruta/a/ecn_command_resolver.sh' >> ~/.bashrc
#
# Principio: el shell intercepta; WRIL resuelve; el territorio manda.
# ==============================================================================

# 1. Detectar raíz canónica una sola vez al sourcear (no en cada comando)
if [ -z "$ECN_ROOT" ]; then
    # Ascenso recursivo hasta encontrar marcadores atómicos
    _ecn_detect_root() {
        local current="$PWD"
        while [ "$current" != "/" ]; do
            if [ -d "$current/pids" ] && [ -d "$current/buzon_salida" ]; then
                echo "$current"
                return 0
            fi
            current="$(dirname "$current")"
        done
        return 1
    }
    
    ECN_ROOT="$(_ecn_detect_root)"
    if [ -z "$ECN_ROOT" ]; then
        echo "[ECN] Advertencia: no se detectó raíz canónica. command_not_found_handle desactivado." >&2
        return 0
    fi
    export ECN_ROOT
fi

# 2. Handler que encadena (no reemplaza) otros handlers existentes
_ecn_original_handler=""
if declare -f command_not_found_handle >/dev/null 2>&1; then
    # Guardar el handler previo para encadenar si ECN no resuelve
    _ecn_original_handler="$(declare -f command_not_found_handle | sed '1d')"
fi

command_not_found_handle() {
    local cmd="$1"
    shift
    local args=("$@")
    
    # Solo interceptar comandos que parezcan módulos ECN (.py, .sh)
    if [[ "$cmd" != *.py && "$cmd" != *.sh ]]; then
        # Encadenar al handler original si existe
        if [ -n "$_ecn_original_handler" ]; then
            eval "$_ecn_original_handler"
            command_not_found_handle "$cmd" "${args[@]}"
            return $?
        fi
        echo "bash: $cmd: orden no encontrada" >&2
        return 127
    fi
    
    # Estrategia 1: consultar path_map.json vía wril_path_resolver.py
    local resolver="$ECN_ROOT/wril/wril_path_resolver.py"
    local real_path=""
    
    if [ -f "$resolver" ]; then
        real_path="$(python3 "$resolver" --resolve "$cmd" 2>/dev/null)"
    fi
    
    # Estrategia 2 (fallback): parseo directo de path_map.json
    if [ -z "$real_path" ] || [ ! -f "$real_path" ]; then
        local path_map="$ECN_ROOT/wril/path_map.json"
        if [ -f "$path_map" ]; then
            real_path="$(python3 -c "
import json, sys
try:
    with open('$path_map') as f:
        data = json.load(f)
    # Buscar por nombre base (ej: 'wril_sentinel.py' sin ruta)
    for key, path in data.items():
        if key.endswith('$cmd') or path.endswith('$cmd'):
            print(path)
            sys.exit(0)
except Exception:
    pass
" 2>/dev/null)"
        fi
    fi
    
    # Si el territorio guio con éxito, ejecutar el módulo
    if [ -n "$real_path" ] && [ -f "$real_path" ]; then
        if [[ "$cmd" == *.py ]]; then
            exec python3 "$real_path" "${args[@]}"
        elif [[ "$cmd" == *.sh ]]; then
            exec bash "$real_path" "${args[@]}"
        else
            exec "$real_path" "${args[@]}"
        fi
    fi
    
    # Si ECN no resolvió, encadenar al handler original
    if [ -n "$_ecn_original_handler" ]; then
        eval "$_ecn_original_handler"
        command_not_found_handle "$cmd" "${args[@]}"
        return $?
    fi
    
    echo "bash: $cmd: orden no encontrada (ECN PathResolver: módulo fuera de mapa)" >&2
    return 127
}

# 3. Registro en log para auditoría (opcional, desactivado por defecto)
# echo "[$(date '+%Y-%m-%d %H:%M:%S')] ECN Command Resolver activado en $ECN_ROOT" >> "$ECN_ROOT/data/runtime/ecn_command_resolver.log"

echo "[ECN] Command Resolver activado. Raíz: $ECN_ROOT"