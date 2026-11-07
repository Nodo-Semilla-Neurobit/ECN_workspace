#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - WRIL
Módulo: patch_post_campo.py
Función: Sutura las heridas A y D del Informe de Campo:
  A) Extirpa el '1' parásito de neurobit_clipboard_core.py (SyntaxError).
  B) Envuelve el main de wril_sentinel.py en try/except (HALT limpio).
         Backup previo vía wril_backup (ética: nunca mutar sin resguardo).
MFN_LOCATION: wril/
MFN_LEVEL: 2
VERSION: v1.0
"""
import re
from pathlib import Path
from wril_backup import resguardar

RAIZ = Path(__file__).resolve().parent

def patch_core():
    f = RAIZ / "neurobit_clipboard_core.py"
    if not f.exists():
        print("[X PATCH A] No existe neurobit_clipboard_core.py"); return
    t = f.read_text(encoding="utf-8")
    nuevo = re.sub(r"ejecutar_commit_verificado\(\)1$",
                   "ejecutar_commit_verificado()", t, flags=re.M)
    if nuevo != t:
        resguardar(f)
        f.write_text(nuevo, encoding="utf-8")
        print("[✓ PATCH A] '1' parásito extirpado del core.")
    else:
        print("[· PATCH A] Core ya limpio.")

def patch_sentinel():
    f = RAIZ / "wril_sentinel.py"
    if not f.exists():
        print("[X PATCH B] No existe wril_sentinel.py"); return
    t = f.read_text(encoding="utf-8")
    if "except KeyboardInterrupt" in t:
        print("[· PATCH B] Sentinel ya maneja KeyboardInterrupt."); return
    viejo = 'if __name__ == "__main__":\n    correr()'
    nuevo = ('if __name__ == "__main__":\n'
             '    try:\n'
             '        correr()\n'
             '    except KeyboardInterrupt:\n'
             '        print("[✓ SENTINEL] HALT limpio. Reposo.")')
    if viejo in t:
        resguardar(f)
        f.write_text(t.replace(viejo, nuevo), encoding="utf-8")
        print("[✓ PATCH B] Sentinel con HALT limpio.")
    else:
        print("[· PATCH B] Main no coincidente; revisar manual.")

if __name__ == "__main__":
    patch_core()
    patch_sentinel()
