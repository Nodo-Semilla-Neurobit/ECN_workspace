cd "/home/gus/workspace_reconstruido"
while IFS= read -r f; do
  case "$f" in ''|\#*) continue;; esac
  if [ -f "$f" ]; then
    case "$f" in
      *.py)
        if python3 -m py_compile "$f" 2>/dev/null; then
          # extrae declaración MFN si existe
          d=$(grep -m1 "MFN_LOCATION:" "$f" 2>/dev/null | sed 's/.*MFN_LOCATION: .' )
          echo "[✓ SINTAXIS] $f | MFN: ${d:-AUSENTE}"
        else
          echo "[X SINTAXIS] $f"
        fi;;
      *) echo "[· PRESENTE] $f";;
    esac
  else
    echo "[X FALTA] $f"
  fi
done < lista_compendio_base.txt