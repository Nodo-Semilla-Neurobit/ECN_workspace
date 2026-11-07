#!/bin/bash
# NB::VERIFY_HEADERS::v0.1
# Inspección de primeras líneas sin mutación.
# Criterio: shebang, encoding, header MFN, NB::, sys.path en primeras 10 líneas.

cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1
RAIZ="$(pwd)"
INFORME="$RAIZ/data/runtime/informe_headers_$(date +%Y%m%d_%H%M%S).txt"
mkdir -p "$RAIZ/data/runtime"

echo "=== VERIFICACIÓN DE PRIMERAS LÍNEAS — $(date) ===" | tee "$INFORME"
echo "RAÍZ: $RAIZ" | tee -a "$INFORME"

# --- 1. Python: shebang + encoding + MFN_LOCATION ---
echo "" | tee -a "$INFORME"
echo "─── PYTHON ───" | tee -a "$INFORME"
find "$RAIZ" -name "*.py" -not -path "*/.venv/*" -not -path "*/__pycache__/*" \
  -not -path "*/node_modules/*" -not -name "*.pre_*" -not -name "*-old.py" | sort | \
while IFS= read -r f; do
  rel="${f#$RAIZ/}"
  head10="$(head -10 "$f" 2>/dev/null)"
  has_shebang="$(head -1 "$f" | grep -c '^#!.*python3')"
  has_mfn="$(echo "$head10" | grep -c 'MFN_LOCATION:')"
  has_encoding="$(echo "$head10" | grep -c 'coding[:=].*utf-8')"
  caso=""
  [ "$has_shebang" -eq 0 ] && caso="${caso}[SIN_SHEBANG]"
  [ "$has_encoding" -eq 0 ] && caso="${caso}[SIN_ENCODING]"
  [ "$has_mfn" -eq 0 ] && caso="${caso}[SIN_MFN_HEADER]"
  # Verificar si MFN_LOCATION declarado coincide con carpeta real
  if [ "$has_mfn" -gt 0 ]; then
    declarado="$(echo "$head10" | grep -m1 'MFN_LOCATION:' | sed 's/.*MFN_LOCATION:[[:space:]]*//' | tr -d '| ')"
    carpeta_real="$(dirname "$rel")/"
    [ "$declarado" != "$carpeta_real" ] && caso="${caso}[TENSION:declara=$declarado/real=$carpeta_real]"
  fi
  [ -n "$caso" ] && echo "[⚠] $rel $caso" | tee -a "$INFORME"
done

# --- 2. Shell: shebang + header NB:: ---
echo "" | tee -a "$INFORME"
echo "─── SHELL ───" | tee -a "$INFORME"
find "$RAIZ" -name "*.sh" -not -path "*/.venv/*" -not -name "*.pre_*" | sort | \
while IFS= read -r f; do
  rel="${f#$RAIZ/}"
  head3="$(head -3 "$f" 2>/dev/null)"
  has_shebang="$(head -1 "$f" | grep -c '^#!/bin/\(ba\)sh')"
  has_nb="$(echo "$head3" | grep -c 'NB::')"
  has_hardcode="$(echo "$head3" | grep -c 'cd "/home/')"
  caso=""
  [ "$has_shebang" -eq 0 ] && caso="${caso}[SIN_SHEBANG]"
  [ "$has_nb" -eq 0 ] && caso="${caso}[SIN_NB_HEADER]"
  [ "$has_hardcode" -gt 0 ] && caso="${caso}[RUTA_HARDCODEADA]"
  [ -n "$caso" ] && echo "[⚠] $rel $caso" | tee -a "$INFORME"
done

# --- 3. Referencias fantasma en scripts ---
echo "" | tee -a "$INFORME"
echo "─── REFERENCIAS FANTASMA ───" | tee -a "$INFORME"
grep -rE 'python3[[:space:]]+[a-zA-Z_./]+\.py|bash[[:space:]]+[a-zA-Z_./]+\.sh' \
  --include="*.sh" "$RAIZ" 2>/dev/null | \
while IFS=: read -r script _ cmd; do
  ref="$(echo "$cmd" | grep -oE '[a-zA-Z_./-]+\.(py|sh)' | head -1)"
  [ -n "$ref" ] && [ ! -f "$RAIZ/$ref" ] && [ ! -f "$(dirname "$script")/$ref" ] && \
    echo "[⚠ FANTASMA] ${script#$RAIZ/} → $ref" | tee -a "$INFORME"
done

echo "" | tee -a "$INFORME"
echo "=== FIN. Informe asentado en: $INFORME ===" | tee -a "$INFORME"