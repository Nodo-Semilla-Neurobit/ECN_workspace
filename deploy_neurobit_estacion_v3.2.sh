#!/bin/bash
##NB::DEPLOY_MAESTRO_ESTACION::v3.3##
# Script: deploy_neurobit_estacion_v3.2.sh (maestro vigente)
# Función: Gesto único definitivo: topología, ancla, bootstrap, entorno,
#          compilación C, permisos, purga+baseline, levantamiento, verdad.
# Uso: bash deploy_neurobit_estacion_v3.2.sh [--plegar]
cd "$(dirname "$0")" || exit 1
RAIZ="$(pwd)"; PID_DIR="$RAIZ/pids"; PLEGAR="${1:-}"
mkdir -p "$PID_DIR" buzon_salida inbox clipboard_captured_folder/backups

mod_path() { if [ -f "wril/$1.py" ]; then echo "wril/$1.py"; else echo "$1.py"; fi; }
launch()   { python3 "$(mod_path "$1")" & echo $! > "$PID_DIR/$2"; }   # D2

echo "============================================================"
echo "🏛️  NEUROBIT_DEV_TEAM™ - DESPLIEGUE DEFINITIVO v3.2 (gestos 0-6)"
echo "============================================================"

echo "[0/6] Auditoría topológica (DECLARACIÓN vs REALIDAD)..."
if [ "$PLEGAR" = "--plegar" ]; then
    python3 "$(mod_path wril_topologia)" --apply || echo "[⚠ TOPO] Pliegue con advertencias."
else
    python3 "$(mod_path wril_topologia)" || echo "[⚠ TOPO] Auditoría con advertencias."
    echo "[· TOPO] Para materializar: bash $0 --plegar"
fi

# 0.5 RE-ANCLAJE del resolver (D6; idempotente, silencioso)
if [ -f tools/install_command_resolver.sh ]; then
    bash tools/install_command_resolver.sh --silencioso >/dev/null 2>&1 \
        && echo "[✓ ANCLA] ~/.bashrc reconciliado con el territorio actual."
fi

echo "[1/6] Bootstrap WRIL: mapa, reconciliación, dependencias..."
python3 "$(mod_path wril_bootstrap)" || echo "[⚠ WRIL] Advertencias; continúo con reservas."

echo "[2/6] Verificando entorno declarado..."
if [ -f system_deps_check.txt ]; then
    while IFS= read -r dep || [ -n "$dep" ]; do          # D3
        case "$dep" in
            "#"*|"") continue ;;
            *gcc*)        command -v gcc >/dev/null && echo "[✓ DEP] gcc" || echo "[⚠ DEP] gcc ausente (build-essential)" ;;
            *libx11*)     [ -f /usr/include/X11/Xlib.h ] && echo "[✓ DEP] Xlib.h" || echo "[⚠ DEP] libx11-dev ausente" ;;
            *python3-gi*) python3 -c "import gi" 2>/dev/null && echo "[✓ DEP] gi" || echo "[⚠ DEP] python3-gi ausente (visor)" ;;
            *flask*)      python3 -c "import flask" 2>/dev/null && echo "[✓ DEP] flask" || echo "[· DEP] flask ausente (Sala opcional)" ;;
            *uinput*)     [ -e /dev/uinput ] && echo "[✓ DEP] uinput" || echo "[⚠ DEP] modprobe uinput" ;;
        esac
    done < system_deps_check.txt
fi

echo "[3/6] Compilación soberana de módulos C..."
if [ -f neurobit_x11_selector.c ] && { [ ! -x neurobit_x11_selector ] || [ neurobit_x11_selector.c -nt neurobit_x11_selector ]; }; then
    gcc -O2 -o neurobit_x11_selector neurobit_x11_selector.c -lX11 \
        && echo "[✓ C] Lector Xlib cristalizado." || echo "[X C] ¿Falta libx11-dev?"
else echo "[· C] Binario vigente; no recompilo."; fi

echo "[4/6] Soberanía de permisos HID..."
id -nG | grep -qw "input" && echo "[✓ UDEV] grupo input presente." \
    || echo "[⚠ UDEV] ejecutá deploy_neurobit_perms.sh y re-iniciá sesión."

echo "[5/6] Purga de huérfanos + baseline snapshot..."
for pidfile in "$PID_DIR"/*.pid; do
    [ -e "$pidfile" ] || continue
    kill -15 "$(cat "$pidfile")" 2>/dev/null; rm -f "$pidfile"
done
pkill -f "neurobit_gnome_widget.py" 2>/dev/null
pkill -f "neurobit_dispatcher.py"   2>/dev/null
pkill -f "neurobit_dictado_evdev.py" 2>/dev/null
pkill -f "wril_sentinel.py"         2>/dev/null
sleep 0.5
ps -eo pid,args | grep -E "neurobit_|wril_" | grep -v grep | grep -v "deploy_neurobit" \
    | awk '{print $1}' | sort > "$PID_DIR/baseline_snapshot"
echo "[✓ BASELINE] Snapshot: $(wc -l < "$PID_DIR/baseline_snapshot") procesos preexistentes."

# HALT definido ANTES de levantar (D4): ninguna ventana sin red
apagar_estacion() {
    echo ""; echo "[🔌 HALT] Plegando la matriz al origen..."
    for pidfile in "$PID_DIR"/*.pid; do
        [ -e "$pidfile" ] || continue
        kill -15 "$(cat "$pidfile")" 2>/dev/null; rm -f "$pidfile"
    done
    ACTUALES=$(ps -eo pid,args | grep -E "neurobit_|wril_" | grep -v grep | grep -v "deploy_neurobit" | awk '{print $1}')
    NUEVOS=""
    for p in $ACTUALES; do
        grep -qx "$p" "$PID_DIR/baseline_snapshot" 2>/dev/null || NUEVOS="$NUEVOS $p"
    done
    if [ -n "$NUEVOS" ]; then
        echo "[📝 HALT-LOG] Nacidos post-baseline:$NUEVOS" > "$PID_DIR/halt_log.txt"
        for p in $NUEVOS; do kill -15 "$p" 2>/dev/null; done
        sleep 1
        for p in $NUEVOS; do kill -9 "$p" 2>/dev/null; done
    fi
    echo "[✓ HALT] Sin huérfanos. WRIL y Estación en reposo (0.0% CPU)."; exit 0
}
trap apagar_estacion INT TERM

echo "[6/6] Levantamiento secuencial (la frontera antes que el núcleo)..."
echo "      [6.1] Guardián de Frontera (WS-Sentinel)...";  launch wril_sentinel        sentinel.pid
echo "      [6.2] Oficina de Correos (dispatcher)...";     launch neurobit_dispatcher dispatcher.pid
echo "      [6.3] Visor Soberano (widget GTK)...";         launch neurobit_gnome_widget widget.pid
echo "      [6.4] Dictáfono Soberano (evdev, reposo)...";  launch neurobit_dictado_evdev dictado.pid

sleep 1
python3 "$(mod_path wril_estado_real)" || echo "[⚠ ESTADO] No se pudo escribir estado_real.json"

echo "============================================================"
echo "✅ ESTACIÓN v3.2 OPERATIVA: WRIL + kernel + gtk + dictado."
echo "   Ctrl+C pliega todo al origen (pidfiles + baseline + log)."
echo "============================================================"
wait
echo "[⚠ WAIT] Un radio terminó antes del HALT; revisá estado_real.json."   # D5
