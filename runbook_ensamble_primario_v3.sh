#!/bin/bash
##NB::RUNBOOK_ENSAMBLE_PRIMARIO::v3.0##
cd "$(dirname "$0")" || exit 1
run_mod() { local n="$1"; shift
if [ -f "wril/$n.py" ]; then python3 "wril/$n.py" "$@"
else python3 "$n.py" "$@"; fi; }
echo "─── 0/7 RAÍZ CANÓNICA ───";      run_mod patch_raiz_canonica
echo "─── 1/7 BOOTSTRAP WRIL ───";        run_mod wril_bootstrap
echo "─── 2/7 TOPOLOGÍA (dry-run) ───";   run_mod wril_topologia
read -r -p "¿Aplicar pliegue? [s/N] " ok
[ "$ok" = "s" ] && run_mod wril_topologia --apply
echo "─── 3/7 DESPERTAR (deploy v3.2) ───"; bash deploy_neurobit_estacion_v3.2.sh & DPID=$!
sleep 2
echo "─── 4/7 TEST OFICINA DE CORREOS ───"; bash test_integracion_matriz.sh
echo "─── 5/7 ESTADO REAL ───";           run_mod wril_estado_real
echo "─── 6/7 HALT ───"; kill -INT "$DPID" 2>/dev/null
echo "[✓ RUNBOOK v3] Ciclo completo. Esperá 4/4 ALIVE."
