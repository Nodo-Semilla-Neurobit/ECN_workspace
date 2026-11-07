#!/bin/bash
##NB::SELF_ROOT::v2.0##
# "Where am I?" — estampa una vez, lee siempre.
# Autoridad: existencia de where_am_I.inf o marcadores (pids/ + buzon_salida/).
# Contenido del .inf = memoria persistida; divergencia = señal auto-sanada.

DIR_ACTUAL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAIZ=""; d="$DIR_ACTUAL"
while [ "$d" != "/" ]; do
  if [ -f "$d/where_am_I.inf" ] || { [ -d "$d/pids" ] && [ -d "$d/buzon_salida" ]; }; then
    RAIZ="$d"; break
  fi
  d="$(dirname "$d")"
done
if [ -z "$RAIZ" ]; then
  echo "[X WRIL] Raíz no hallada desde $DIR_ACTUAL"
  return 1 2>/dev/null || exit 1
fi

FISICA="$(cd "$RAIZ" && pwd -P)"
INF="$RAIZ/where_am_I.inf"

sellar() {  # escritura atómica: tmp + mv
  local tmp="$INF.tmp.$$"
  { echo "RAIZ_LOGICA=$RAIZ"; echo "RAIZ_FISICA=$FISICA"
    echo "SELLADO=$(date -u +%Y-%m-%dT%H:%M:%SZ)"; [ -n "$1" ] && echo "MUDANZA_DEDE=$1"; } > "$tmp"
  mv "$tmp" "$INF"
}

if [ ! -f "$INF" ]; then
  sellar ""; echo "[✓ RAIZ] where_am_I.inf sellado: $RAIZ"
else
  REGISTRADA="$(grep -m1 '^RAIZ_LOGICA=' "$INF" | cut -d= -f2-)"
  if [ "$REGISTRADA" != "$RAIZ" ]; then
    sellar "$REGISTRADA"
    echo "[⚠ WRIL] Mudanza detectada: .inf decía $REGISTRADA; ahora $RAIZ (auto-sanado con asiento)"
  fi
fi

# Symlink mentiroso: señal, no error.
[ "$RAIZ" != "$FISICA" ] && echo "[⚠ WRIL] Raíz lógica ≠ raíz física: $RAIZ -> $FISICA"

# La voz declarada se hereda a todo hijo (lectura barata, cada invocación).
export APP_HOME="$RAIZ"