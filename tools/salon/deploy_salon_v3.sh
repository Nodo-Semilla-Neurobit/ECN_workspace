#!/bin/bash
# ============================================================
# ECN · DESPLIEGUE SALÓN SOBERANO v3.0
# Ubicación canónica: tools/salon/deploy_salon_v3.sh
# Idempotente: no duplica, no rompe, verifica antes de actuar.
# Principio: el territorio primero; el mapa después.
# ============================================================
set -u

RAIZ="$(cd "$(dirname "$0")/../.." && pwd)"
SALON="$RAIZ/tools/salon"
BACKUP="$RAIZ/backups_wril"

echo "============================================================"
echo " ECN · DESPLIEGUE SALÓN SOBERANO v3.0"
echo "============================================================"
echo "[·] RAÍZ: $RAIZ"
echo "[·] SALÓN: $SALON"
echo ""

# ---------- 1/6 Verificar ancla de raíz ----------
if [ ! -f "$RAIZ/.ecn_raiz" ] && [ ! -f "$RAIZ/deploy_neurobit_estacion_v3.2.sh" ]; then
  echo "[X] No se detecta raíz canónica ECN"
  echo "    Ejecutá este script desde tools/salon/ de la ECN."
  exit 1
fi
echo "[✓] Raíz canónica detectada"

# ---------- 2/6 Crear estructura (idempotente) ----------
mkdir -p "$SALON"/{inbox,outbox,agentes,cuarentena}
for sub in para_7so para_9se para_lle para_todos para_director; do
  mkdir -p "$SALON/outbox/$sub"
done
echo "[✓] Estructura de directorios verificada"

# ---------- 3/6 Verificar archivos canónicos ----------
ARCHIVOS_REQUERIDOS=(
  "salon_coordinador.py"
  "salon_frontend.html"
  "agentes/7so_eva_lumena.yaml"
  "agentes/9se_pliego_se.yaml"
  "agentes/lle_digital.yaml"
  "README_SALON.md"
)
for f in "${ARCHIVOS_REQUERIDOS[@]}"; do
  if [ ! -f "$SALON/$f" ]; then
    echo "[X] Falta archivo canónico: $SALON/$f"
    echo "    Copialo desde el entregable del par local."
    exit 1
  fi
done
echo "[✓] Todos los archivos canónicos presentes"

# ---------- 4/6 Instalar dependencia watchdog (si falta) ----------
PYTHON_BIN="${PYTHON_BIN:-python3}"
if ! "$PYTHON_BIN" -c "import watchdog" 2>/dev/null; then
  echo "[·] watchdog no instalado; instalando en venv si existe..."
  if [ -f "$RAIZ/.venv/bin/pip" ]; then
    "$RAIZ/.venv/bin/pip" install watchdog -q && echo "[✓] watchdog instalado en venv"
  else
    "$PYTHON_BIN" -m pip install watchdog -q && echo "[✓] watchdog instalado en sistema"
  fi
else
  echo "[✓] watchdog ya disponible"
fi

# ---------- 5/6 Backup preventivo ----------
mkdir -p "$BACKUP"
if [ -f "$RAIZ/wril_historial.jsonl" ]; then
  ts=$(date +%Y%m%d_%H%M%S)
  cp -n "$RAIZ/wril_historial.jsonl" "$BACKUP/wril_historial.pre_salon_v3_$ts.jsonl" 2>/dev/null
  echo "[✓] Backup de wril_historial en $BACKUP"
fi

# ---------- 6/6 Registro en path_map.json ----------
if [ -f "$RAIZ/wril_path_map.py" ]; then
  "$PYTHON_BIN" "$RAIZ/wril_path_map.py" 2>/dev/null && \
    echo "[✓] path_map.json regenerado con tools/salon/"
else
  echo "[·] wril_path_map.py no encontrado; omito regeneración"
fi

echo ""
echo "============================================================"
echo " DESPLIEGUE COMPLETADO"
echo "============================================================"
echo " Siguiente paso:"
echo "   bash $SALON/test_salon.sh"
echo ""
echo " Para iniciar el coordinador:"
echo "   nohup $PYTHON_BIN $SALON/salon_coordinador.py > $SALON/coordinador.log 2>&1 &"
echo ""
echo " Para abrir el frontend:"
echo "   xdg-open $SALON/salon_frontend.html"
echo "============================================================"
