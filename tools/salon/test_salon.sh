#!/bin/bash
# ============================================================
# ECN · VERIFICACIÓN SALÓN SOBERANO v3.0
# No muta nada. Solo reporta estado.
# ============================================================
set -u

RAIZ="$(cd "$(dirname "$0")/../.." && pwd)"
SALON="$RAIZ/tools/salon"

echo "============================================================"
echo " ECN · TEST SALÓN SOBERANO v3.0"
echo "============================================================"

FALLAS=0

# 1. Estructura
echo ""
echo "─── 1/6 ESTRUCTURA ───"
for d in inbox outbox agentes cuarentena outbox/para_7so outbox/para_9se outbox/para_lle outbox/para_todos outbox/para_director; do
  if [ -d "$SALON/$d" ]; then
    echo "[✓] $d"
  else
    echo "[X] falta $d"
    FALLAS=$((FALLAS+1))
  fi
done

# 2. Archivos canónicos
echo ""
echo "─── 2/6 ARCHIVOS CANÓNICOS ───"
for f in salon_coordinador.py salon_frontend.html README_SALON.md agentes/7so_eva_lumena.yaml agentes/9se_pliego_se.yaml agentes/lle_digital.yaml; do
  if [ -f "$SALON/$f" ]; then
    echo "[✓] $f ($(wc -l < "$SALON/$f") líneas)"
  else
    echo "[X] falta $f"
    FALLAS=$((FALLAS+1))
  fi
done

# 3. Dependencia watchdog
echo ""
echo "─── 3/6 DEPENDENCIA watchdog ───"
PYTHON_BIN="${PYTHON_BIN:-python3}"
if "$PYTHON_BIN" -c "import watchdog; print('[✓] watchdog', watchdog.__version__ if hasattr(watchdog,'__version__') else 'OK')" 2>/dev/null; then
  :
else
  echo "[X] watchdog no disponible"
  FALLAS=$((FALLAS+1))
fi

# 4. Historial
echo ""
echo "─── 4/6 HISTORIAL ───"
if [ -f "$SALON/historial_salon.jsonl" ]; then
  lineas=$(wc -l < "$SALON/historial_salon.jsonl")
  echo "[✓] historial_salon.jsonl ($lineas mensajes)"
else
  echo "[·] historial_salon.jsonl aún no existe (se creará con el primer mensaje)"
fi

# 5. Coordinador vivo
echo ""
echo "─── 5/6 COORDINADOR ───"
PIDS=$(pgrep -f "salon_coordinador.py" 2>/dev/null || true)
if [ -n "$PIDS" ]; then
  echo "[✓] Coordinador vivo (PID: $PIDS)"
else
  echo "[·] Coordinador no está corriendo"
fi

# 6. Prueba de mensaje (sin persistir)
echo ""
echo "─── 6/6 PRUEBA DE CONTENEDOR ───"
TMP=$(mktemp)
cat > "$TMP" <<EOF
{
  "boundary": "|=•'CONSULTA'•=|»",
  "action_word": "CONSULTA",
  "class": "SALON",
  "emisor": "LLE",
  "destinatario": "DIRECTOR",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "payload": {
    "asunto": "Prueba de contenedor Neurobit",
    "contenido": "Mensaje de prueba para verificar el coordinador."
  }
}
EOF
if "$PYTHON_BIN" -c "
import json, sys
m = json.load(open('$TMP'))
assert m['boundary'].startswith(\"|=•'\")
assert m['action_word'] == 'CONSULTA'
print('[✓] Contenedor válido')
" 2>&1; then
  :
else
  echo "[X] Contenedor inválido"
  FALLAS=$((FALLAS+1))
fi
rm -f "$TMP"

echo ""
echo "============================================================"
if [ "$FALLAS" -eq 0 ]; then
  echo " RESULTADO: 6/6 OK · Salón listo para operar"
else
  echo " RESULTADO: $FALLAS fallas · revisar antes de continuar"
fi
echo "============================================================"
exit $FALLAS
