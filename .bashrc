# ==========================================================================
# ECOSISTEMA NEUROBÍTRONICO - CLAUSURA INMUNOLÓGICA LOCAL v3.2
# Paradigma: Inmunidad de Estado, Abstracción por Alias y Carga Viva
# ==========================================================================

# 1. Fijación del Pivote Ontológico (Contexto Raíz Dinámico)
# El sistema determina dónde despertó sin hardcodear rutas rígidas en disco.
export ECN_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd 2>/dev/null || echo "$HOME/.neurobit")"
export INSTANCES_JOURNAL="$ECN_ROOT/.ecn_journal"
export ALIAS_INDEX="$ECN_ROOT/.ecn_alias_index"
export MODULES_DIR="$ECN_ROOT/modules_pool"

# 2. Intercepción Sintáctica de Comandos Inexistentes
# Modificamos el entorno para que, ante una "falla de inexistencia" (Comando no encontrado),
# el shell no aborte con un error crítico, sino que dispare el motor de autorreparación.
command_not_found_handle() {
    local comando_invocado="$1"
    shift
    local argumentos_invocados="$@"

    # Consulta al Archivo Dinámico Índice (.ecn_alias_index)
    if [ -f "$ALIAS_INDEX" ]; then
        local registro_linea=$(grep "^${comando_invocado}:" "$ALIAS_INDEX")
        
        if [ -n "$registro_linea" ]; then
            local plantilla_ruta=$(echo "$registro_linea" | cut -d':' -f2)
            
            # Clonación Automática: Reconstruye el puente semántico en caliente
            if [ -f "$plantilla_ruta" ]; then
                echo "[RESILIENCIA] Interceptando comando falible: ${comando_invocado}. Reparando puente..."
                
                # Inyección dinámica de la plantilla universal sin cajas negras
                alias $comando_invocado="bash $plantilla_ruta"
                
                # Ejecución de la acción en milisegundos una vez asegurada su existencia
                bash "$plantilla_ruta" $argumentos_invocados
                return $?
            fi
        fi
    fi

    # Fallback Silencioso al comportamiento tradicional si el comando no es del Logos
    echo "bash: ${comando_invocado}: comando no encontrado"
    return 127
}

# 3. Desactivación de la Persistencia Sudo (Protección de la Voluntad)
# El sistema se purga a sí mismo. Rechaza la inyección de binarios maliciosos 
# alienantes mediante un mecanismo trap que limpia los alias al lanzar el apagado.
trap 'unalias -a 2>/dev/null; echo "[JOURNAL] Purgando trazas de memoria viva. Vacío Latente Alfa."' INT TERM EXIT

