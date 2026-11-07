#!/usr/bin/env bash
# Exporta la raíz canónica del proyecto como ECN_ROOT.
# Sirve para desacoplar el runtime del nombre literal del directorio físico.

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd -P)"
export ECN_ROOT="$PROJECT_ROOT"
echo "$ECN_ROOT"
