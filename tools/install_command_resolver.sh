#!/usr/bin/env bash
# ==============================================================================
# ECN · Instalador del Command Resolver (Re-anclaje Dinámico)
# MFN_LOCATION: tools/ | MFN_LEVEL: 1 | VERSION: v1.0
# ==============================================================================
# Función: Asegura que ~/.bashrc apunte a la ubicación ACTUAL del resolver.
# Uso: bash tools/install_command_resolver.sh
# Principio: El territorio manda; la declaración se actualiza a la realidad.
# ==============================================================================

set -euo pipefail

# 1. Detectar territorio actual (sin asumir cwd)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
ECN_ROOT="$(dirname "$SCRIPT_DIR")"  # tools/ está un nivel bajo la raíz
RESOLVER_PATH="$ECN_ROOT/wril/ecn_command_resolver.sh"

if [ ! -f "$RESOLVER_PATH" ]; then
    echo "[X ERROR] No se encuentra ecn_command_resolver.sh en:" >&2
    echo "          $RESOLVER_PATH" >&2
    exit 1
fi

BASHRC="$HOME/.bashrc"
MARKER="# ECN_COMMAND_RESOLVER"
SOURCE_LINE="source \"$RESOLVER_PATH\""

# 2. Backup de seguridad (Invariante 2: Preservación Pre-Mutación)
BACKUP="$BASHRC.bak.$(date +%Y%m%d_%H%M%S)"
cp "$BASHRC" "$BACKUP"
echo "[✓ BACKUP] ~/.bashrc respaldado en: $BACKUP"

# 3. Lógica de reconciliación (Declaración vs Realidad)
if grep -q "$MARKER" "$BASHRC"; then
    # La línea existe (puede tener ruta vieja). Reemplazarla.
    sed -i "s|^.*$MARKER.*|$SOURCE_LINE  $MARKER|" "$BASHRC"
    echo "[✓ UPDATE] Ruta actualizada en ~/.bashrc"
    echo "           Nueva ruta: $RESOLVER_PATH"
else
    # La línea no existe. Agregarla al final.
    {
        echo ""
        echo "$SOURCE_LINE  $MARKER"
    } >> "$BASHRC"
    echo "[✓ INSTALL] Source agregado a ~/.bashrc"
fi

# 4. Activación inmediata en la sesión actual
source "$RESOLVER_PATH"

echo ""
echo "============================================================"
echo "✅ ECN COMMAND RESOLVER INSTALADO"
echo "   Raíz detectada: $ECN_ROOT"
echo "   Prueba: escribe 'wril_sentinel.py' (sin ruta) y debería ejecutar."
echo "============================================================"