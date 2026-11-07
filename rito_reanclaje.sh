#!/bin/bash
##NB::REANCLAJE::v1.0##
# Una pantalla para cualquier nodo/sesión. Lee territorio; no muta
# (salvo saneo sancionado de índices muertos si el reposo se confirma).
set -u
cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1
[ -f self_root.sh ] && source self_root.sh >/dev/null 2>&1
cd "${APP_HOME:-.}" || exit 1
echo "─── RAÍZ (sello) ───";      cat where_am_I.inf 2>/dev/null || echo "[⚠] sin where_am_I.inf"
echo "─── REPOSO ───";           .venv/bin/python3 wril/wril_reposo.py 2>/dev/null | tail -2 || echo "[⚠] reposo no verificable"
echo "─── TENSIÓN ───";          .venv/bin/python3 wril/wril_mfn_registry.py 2>/dev/null | grep "Coherentes" || echo "[⚠] registry no disponible"
echo "─── CANON (líneas) ───"
for L in artefactos_funcionando.tmp parches_aplicados.tmp modulos_no_activados.lst; do
  printf "  %-30s %s\n" "$L" "$(wc -l < "data/runtime/$L" 2>/dev/null || echo 0)"
done
echo "─── CONTRATO (leer antes de mutar) ───"
for d in ACTA_ESTADO_ACTUAL_20260908.md Mecanica_Operativa_ECN.md \
         data/MD/como_leer_compendios_v1.md data/MD/flujo_arranque_v1.md; do
  [ -f "$d" ] && echo "  [✓] $d" || echo "  [⚠ FALTA] $d"
done
echo "─── ÚLTIMA MEMORIA ───";   tail -3 wril/wril_historial.jsonl 2>/dev/null | cut -c1-110 || echo "[⚠] sin historial"