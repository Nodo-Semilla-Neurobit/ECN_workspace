#!/usr/bin/env bash
# ============================================================
# ECN · levantar/detener el PUENTE DE CONSOLA WS
# Idempotente: jamás duplica (tensión "address already in use").
# Sin dependencias: el servidor es node puro (RFC6455 a mano).
# Uso:
#   bash levantar_puente.sh          # levantar
#   bash levantar_puente.sh stop     # detener
# ============================================================
set -u
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_DIR="$AQUI/../pids"; mkdir -p "$PID_DIR"
PID_FILE="$PID_DIR/puente_ws.pid"
LOG_FILE="$PID_DIR/puente_ws.log"
PORT="${ECN_WS_PORT:-8080}"

detener(){
  if [ -f "$PID_FILE" ]; then
    PID="$(cat "$PID_FILE")"
    if kill -0 "$PID" 2>/dev/null; then
      kill "$PID" 2>/dev/null && echo "[✓ PUENTE] detenido (pid $PID)"
    else
      echo "[⚠ PUENTE] pid $PID ya muerto"
    fi
    rm -f "$PID_FILE"
  else
    echo "[⚠ PUENTE] sin pid file; nada que detener"
  fi
}

case "${1:-start}" in
  stop) detener; exit 0 ;;
esac

# 1. idempotencia: si ya vive, no se duplica
if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "[✓ PUENTE] ya vive (pid $(cat "$PID_FILE")) en ws://127.0.0.1:$PORT"
  exit 0
fi

# 2. verdad de territorio: ¿el puerto está ocupado por otro?
if command -v ss >/dev/null 2>&1 && ss -tln 2>/dev/null | grep -q ":$PORT "; then
  echo "[⚠ PUENTE] el puerto $PORT ya está ocupado por otro proceso."
  echo "    verificar: ss -tlnp | grep $PORT"
  exit 1
fi

# 3. dependencia única: node
if ! command -v node >/dev/null 2>&1; then
  echo "[X ERROR] node no encontrado. El puente requiere node (sin paquetes npm)."
  exit 1
fi

# 4. levantar en background absoluto
nohup node "$AQUI/puente_consola_ws.js" > "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"
sleep 1

if kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "[✓ PUENTE] vivo en ws://127.0.0.1:$PORT (pid $(cat "$PID_FILE"))"
  echo "    log:      $LOG_FILE"
  echo "    abrir:     public/index.html"
else
  echo "[X ERROR] el puente no arrancó; leer $LOG_FILE"
  rm -f "$PID_FILE"
  exit 1
fi
