cd "/home/gus/workspace_reconstruido"
# 1) sintaxis
python3 -m py_compile wril/rubrica_parches.py && echo '[✓ SINTAXIS] ok'
# 2) autoprueba: asienta y consulta una rúbrica (crea data/runtime/)
python3 wril/rubrica_parches.py

