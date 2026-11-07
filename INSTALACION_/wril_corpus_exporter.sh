#!/bin/bash
##NB::CORPUS_EXPORTER::v1.0##
# Función: Concatena los archivos de una lista en un solo .txt con
#          separadores MFN, para que un nodo externo (Qwen/Copilot)
#          los inspeccione sin perder trazabilidad de origen.
# Uso:     bash wril_corpus_exporter.sh lista_archivos.txt [salida.txt]
# Principio: append-only sobre la salida; NUNCA toca los originales.
LISTA="${1:-lista_archivos.txt}"
SALIDA="${2:-corpus_export_$(date +%Y%m%d_%H%M%S).txt}"
: > "$SALIDA"
while IFS= read -r f; do
  [ -f "$f" ] || { echo "[⚠] No existe: $f"; continue; }
  { echo "================================================";
    echo "ARCHIVO: $f";
    echo "MFN_LOCATION: INSTALACION_ "$f")";
    echo "------------------------------------------------";
    cat "$f";
    echo "";
  } >> "$SALIDA"
done < "$LISTA"
echo "[✓ CORPUS] Exportado: $SALIDA ($(wc -c < "$SALIDA") bytes)"
