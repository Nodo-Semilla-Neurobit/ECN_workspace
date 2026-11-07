#!/bin/bash
##NB::DEPLOY_MAESTRO_ESTACION::v1.0##
# Ecosistema Neurobit - Estación Central Neurobitrónica
# Script: deploy_neurobit_estacion.sh
# Función: Despliegue maestro en un solo gesto: compila los módulos C,
#          verifica soberanía de permisos, purga huérfanos y levanta
#          dispatcher + widget + dictáfono. Apagado atómico por trap.

cd "$(dirname "$0")" || exit 1
RAIZ="$(pwd)"
PID_DIR="$RAIZ/pids"
mkdir -p "$PID_DIR" buzon_salida clipboard_captured_folder/backups

echo "============================================================"
echo "🏛️  NEUROBIT_DEV_TEAM™ - DESPLIEGUE MAESTRO DE LA ESTACIÓN v1.0"
echo "============================================================"

# 1. COMPILACIÓN SOBERANA DE LOS MÓDULOS C (solo si falta o mutó)
if [ -f "neurobit_x11_selector.c" ]; then
    if [ ! -x "neurobit_x11_selector" ] || [ "neurobit_x11_selector.c" -nt "neurobit_x11_selector" ]; then
        echo "[⚙ COMPILAR] neurobit_x11_selector.c -> binario"
        gcc -O2 -o neurobit_x11_selector neurobit_x11_selector.c -lX11 \
            && echo "[✓ C] Lector Xlib cristalizado." \
            || echo "[X C] Falló la compilación (¿falta libx11-dev?)"
    else
        echo "[✓ C] neurobit_x11_selector ya cristalizado."
    fi
fi

# 2. VERIFICACIÓN DE SOBERANÍA DE PERMISOS (grupo input)
if id -nG | grep -qw "input"; then
    echo "[✓ UDEV] El NODO_SEMILLA pertenece al grupo 'input'."
else
    echo "[ UDEV] Sin grupo 'input': ejecutá deploy_neurobit_perms.sh y re-iniciá sesión."
fi

# 3. PURGA DE HUÉRFANOS (Control de Oficio)
for pidfile in "$PID_DIR"/*.pid; do
    [ -e "$pidfile" ] || continue
    PID_VIEJO=$(cat "$pidfile")
    if kill -0 "$PID_VIEJO" 2>/dev/null; then
        echo "[🔌 PURGA] Terminando instancia previa PID $PID_VIEJO"
        kill -15 "$PID_VIEJO" 2>/dev/null
    fi
    rm -f "$pidfile"
done
pkill -f "neurobit_gnome_widget.py" 2>/dev/null
pkill -f "neurobit_dispatcher.py" 2>/dev/null
pkill -f "neurobit_dictado_evdev.py" 2>/dev/null
sleep 0.5

# 4. LEVANTAMIENTO SECUENCIAL DE LA MATRIZ
echo "[1/3] Abriendo la Oficina de Correos (dispatcher)..."
python3 neurobit_dispatcher.py & echo $! > "$PID_DIR/dispatcher.pid"
echo "[2/3] Levantando el Visor Soberano (widget GTK)..."
python3 neurobit_gnome_widget.py & echo $! > "$PID_DIR/widget.pid"
echo "[3/3] Armando el Dictáfono Soberano (evdev, en reposo)..."
python3 neurobit_dictado_evdev.py & echo $! > "$PID_DIR/dictado.pid"

# 5. APAGADO ATÓMICO (trap): pliegue del vector al origen
apagar_estacion() {
    echo ""
    echo "[🔌 HALT] Liberando la Estación Central..."
    for pidfile in "$PID_DIR"/*.pid; do
        [ -e "$pidfile" ] || continue
        kill -15 "$(cat "$pidfile")" 2>/dev/null
        rm -f "$pidfile"
    done
    echo "[✓ HALT] Matriz plegada al origen. Sin huérfanos."
    exit 0
}
trap apagar_estacion INT TERM

echo "============================================================"
echo "✅ ESTACIÓN OPERATIVA. Radios activos: kernel, gtk, dictado."
echo "   Ctrl+C en esta terminal pliega la matriz (apagado atómico)."
echo "============================================================"
wait
