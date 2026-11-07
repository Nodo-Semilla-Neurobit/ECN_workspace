#!/usr/bin/env bash
# ============================================================
# ECN · DESPERTADOR DEL HUB DINÁMICO v1.1
# Instancia m4.5 del instalador lúdico.
# Cliente del SOSPortLighthouse (Faro de Puertos Soberano).
#
# Principio: el territorio verifica; el instalador lee.
# El Faro asigna el puerto real en rango CORE (5000-5009).
# Si el Faro no está disponible, fallback a 5000.
# ============================================================
set -u
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$AQUI" || exit 1

PID_DIR="$AQUI/pids";       mkdir -p "$PID_DIR"
LOG_DIR="$AQUI/logs";       mkdir -p "$LOG_DIR"
WAL_FILE="$AQUI/sesiones/wal_consola.log"
PORT_FILE="$PID_DIR/hub_dinamico.port"
RUNTIME_DIR="$AQUI/data/runtime"

# ---------- 1. Leer puerto real del Faro ----------
PUERTO=""
if [ -f "$AQUI/core/port_lighthouse.py" ]; then
  PUERTO=5000
import sys, os
sys.path.insert(0, '$AQUI')
try:
    from core.port_lighthouse import SOSPortLighthouse
    f = SOSPortLighthouse('$AQUI')
    print(f.request_port('neurobit_api', 'CORE', default_port=5000))
except Exception as e:
    print('')
" 2>/dev/null)
fi

# Fallback si el Faro falló o no existe
if [ -z "$PUERTO" ]; then
  PUERTO=5000
  echo "[⚠ FARO] No disponible; usando fallback 5000"
fi

echo "[✓ HUB] Puerto asignado: $PUERTO"
echo "$PUERTO" > "$PORT_FILE"

# ---------- 2. Verificar si ya vive ----------
if ss -tln 2>/dev/null | grep -q ":$PUERTO "; then
  # Probar salud real
  RESP=$(curl -s --max-time 3 "http://127.0.0.1:$PUERTO/health" 2>/dev/null)
  if echo "$RESP" | grep -q "status"; then
    echo "[✓ HUB] Ya vive en puerto $PUERTO y responde /health"
    echo "[# SISTEMA] HUB_DINAMICO: VIVO puerto=$PUERTO (preexistente)" >> "$WAL_FILE"
    exit 0
  else
    echo "[⚠ HUB] Puerto $PUERTO ocupado pero no responde /health"
    echo "    verificar: ss -tlnp | grep $PUERTO"
    exit 1
  fi
fi

# ---------- 3. Localizar neurobit_api.py ----------
API_FILE=""
for candidato in \
  "$AQUI/neurobit_api.py" \
  "$AQUI/core/neurobit_api.py" \
  "$AQUI/INSTALACION_/modulos/neurobit_api.py"; do
  if [ -f "$candidato" ]; then
    API_FILE="$candidato"
    break
  fi
done

if [ -z "$API_FILE" ]; then
  echo "[X ERROR] neurobit_api.py no encontrado en territorio"
  echo "    buscado en: $AQUI/{neurobit_api.py,core/,INSTALACION_/modulos/}"
  exit 1
fi

echo "[✓ HUB] API encontrada: $API_FILE"

# ---------- 4. Detectar python del venv ----------
if [ -f "$AQUI/.venv/bin/python3" ]; then
  PYTHON="$AQUI/.venv/bin/python3"
mkdir -p "$AQUI/data/runtime"; echo "$PYTHON" > "$AQUI/data/runtime/python_bin.identity"
mkdir -p "$AQUI/data/runtime"; echo "$PYTHON" > "$AQUI/data/runtime/python_bin.identity"
mkdir -p "$AQUI/data/runtime"; echo "$PYTHON" > "$AQUI/data/runtime/python_bin.identity"
  echo "[✓ HUB] Usando venv: $PYTHON"
else
  PYTHON="python3"
  echo "[⚠ HUB] Sin venv; usando python3 del sistema"
fi

# ---------- 5. Inyectar variable de puerto para neurobit_api.py ----------
export ECN_HUB_PORT="$PUERTO"

# ---------- 6. Levantar en background ----------
LOG_FILE="$LOG_DIR/hub_dinamico.log"
nohup "$PYTHON" "$API_FILE" > "$LOG_FILE" 2>&1 &
HUB_PID=$!
echo "$HUB_PID" > "$PID_DIR/hub_dinamico.pid"

echo "[✓ HUB] Arrancado PID $HUB_PID · log: $LOG_FILE"

# ---------- 7. Verificar /health con timeout ----------
MAX_INTENTOS=12
for i in $(seq 1 $MAX_INTENTOS); do
  sleep 0.5
  if ! kill -0 "$HUB_PID" 2>/dev/null; then
    echo "[X ERROR] El proceso murió antes de responder"
    echo "    últimas 20 líneas del log:"
    tail -20 "$LOG_FILE" | sed 's/^/    /'
    exit 1
  fi
  RESP=$(curl -s --max-time 2 "http://127.0.0.1:$PUERTO/health" 2>/dev/null)
  if echo "$RESP" | grep -q "status"; then
    echo "[✓ HUB] /health respondió en intento $i"
    echo "[# SISTEMA] HUB_DINAMICO: VIVO puerto=$PUERTO pid=$HUB_PID" >> "$WAL_FILE"
    echo ""
    echo "============================================================"
    echo " HUB DINÁMICO VIVO"
    echo "   puerto:  $PUERTO"
    echo "   pid:     $HUB_PID"
    echo "   log:     $LOG_FILE"
    echo "   prueba:  curl -s http://127.0.0.1:$PUERTO/health"
    echo "============================================================"
    echo ""
    echo "Próximo paso del camino del aspirante:"
    echo "   curl -s http://127.0.0.1:$PUERTO/health"
    exit 0
  fi
done

echo "[X ERROR] El Hub no respondió /health en $MAX_INTENTOS intentos"
echo "    últimas 20 líneas del log:"
tail -20 "$LOG_FILE" | sed 's/^/    /'
echo "    puerto asignado: $PUERTO"
echo "    verificar: ss -tlnp | grep $PUERTO"
exit 1
