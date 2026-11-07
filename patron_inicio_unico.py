# Al inicio del __main__ de cada daemon (sentinel, dispatcher, widget, dictado):
from wril_proc_guard import guardia, asentar, purgar
import os, sys

NOMBRE = "WRIL_SENTINEL"
g = guardia(NOMBRE)
if g == "NOTIFY":
    print(f"[✓ {NOMBRE}__EXECUTION_STATE-NOTIFY] ya en curso; no se duplica.")
    sys.exit(0)
if g == "PURGE_Y_OK":
    purgar(NOMBRE)
    print(f"[⚠ {NOMBRE}] entrada stale saneada; se relanza.")

# ... arranque real del proceso ...

# Solo tras inicio exitoso:
globals()[f"{NOMBRE}__EXECUTION_STATE"] = True
asentar(NOMBRE, os.getpid())