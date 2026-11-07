# Delta sobre wril_leyes.py — añade LEY 4 (self-path) y es_backup compartido.
import sys
from pathlib import Path

def asegurar_syspath():
    """LEY 4: el módulo wril se ve a sí mismo antes de importar hermanos."""
    d = str(Path(__file__).resolve().parent)
    if d not in sys.path:
        sys.path.insert(0, d)

# En wril_topologia.py, al inicio:
#   from wril_leyes import RAIZ, es_backup, guarda_convergencia, asegurar_syspath
#   asegurar_syspath()
# Y dentro del bucle de plegar(), antes de mover:
#   if es_backup(origen.name): continue        # LEY 2
# Y al final:
#   if not guarda_convergencia(t_antes, t_despues):
#       print("[X CONVERGENCIA] Tensión subió; pliegue abortado.")  # LEY 3
