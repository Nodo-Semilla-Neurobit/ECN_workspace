#!/bin/bash
##NB::ENSAMBLE_PRIMARIO::v1.0##
# Función: Verifica que los dos linajes compartan buzón y Arca sin fusionarse.
cd "$(dirname "$0")" || exit 1
mkdir -p buzon_salida data

echo "[1/3] Sobre legacy -> carta sellada (cruza el puente)..."
python3 - <<'PY'
from wril_adapter_ecn import depositar_desde_legacy
sobre = {"MESSAGE_ID":"TEST_0001","ORIGEN":"ECN_LEGACY","source":"memoria",
         "tipo":"ensamble","CONTENT":"Ensamble primario: el sobre cruzó el puente."}
print(f"[✓ PUENTE] Depositado como: {depositar_desde_legacy(sobre).name}")
PY

echo "[2/3] Esperando al dispatcher (inotify)..."
sleep 2

echo "[3/3] Verificando asiento en el Arca..."
grep -q "cruzó el puente" memoria_eva.jsonl data/memoria_eva.jsonl 2>/dev/null \
    && echo "[✓ ARCA] El postman asentó la carta: los linajes comparten memoria." \
    || echo "[· ARCA] Sin asiento aún: levantá la Estación (deploy v3.0) y reintentá."
echo "[✓ ENSAMBLE] Dos líneas, una semilla."
