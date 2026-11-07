#!/usr/bin/env bash
# ============================================================
# ECN · INICIALIZADOR DE LA JAULA VIRTUAL (.venv)
# Función: Crea el entorno aislado local y aprovisiona las
#          dependencias dynamic declaradas por el escáner.
# MFN_LOCATION: core/  |  MFN_LEVEL: 1
# VERSION: v1.0
# ============================================================
set -u
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAIZ="$(cd "$AQUI/.." && pwd)"
cd "$RAIZ" || exit 1

REQ_FILE="$RAIZ/requirements_dynamic.txt"
SYS_FILE="$RAIZ/system_deps_check.txt"

echo "============================================================"
echo "🛡️  ECN · AISLAMIENTO TERRITORIAL — CREACIÓN DE .VENV"
echo "============================================================"

# 1. Verificar si existen los manifiestos del escáner
if [ ! -f "$REQ_FILE" ]; then
    echo "[⚠] Requerimientos dinámicos ausentes. Invocando al escáner..."
    python3 wril/wril_dependency_scanner.py
fi

# 2. Intentar fundar la jaula virtual
echo "[1/3] Creando cordón sanitario virtual (.venv)..."
python3 -m venv .venv
if [ $? -ne 0 ]; then
    echo "[X ERROR] No se pudo crear el entorno virtual."
    echo "    Asegúrate de tener instalado python3-venv en el sistema."
    exit 1
fi

# 3. Activar y aprovisionar el entorno en frío
echo "[2/3] Activando jaula y actualizando instalador interno (pip)..."
source .venv/bin/activate
pip install --upgrade pip

echo "[3/3] Instalando dependencias dinámicas detectadas en el territorio..."
# Para evitar fallos si el archivo de requerimientos está vacío o solo con comentarios
if [ -f "$REQ_FILE" ] && [ -n "$(grep -v '^#' "$REQ_FILE")" ]; then
    pip install -r "$REQ_FILE"
else
    echo "[✓] No se detectaron librerías de terceros complejas. Instalando Flask base..."
    pip install flask flask-cors
fi

echo "============================================================"
echo "✅ JAULA VIRTUAL CONFIGURADA COHERENTE"
echo "   Entorno aislado y listo para el Hub dinámico."
echo "============================================================"
