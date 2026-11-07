import sys; sys.path.insert(0, 'wril')
from rubrica_parches import h, veredicto, rubricar, sellar_herencia

OBJETIVOS = ['wril/wril_mfn_registry.py']
v = veredicto('metricas_v02', OBJETIVOS)
if v:
    prev, iguales = v
    if iguales:
        print('[· YA APLICADO] desde', prev['t'], '(--force para re-provocar)'); sys.exit(0)
    print('[⚠ MUTADO DESPUÉS] re-evaluar anclas.')

hash_prev = {o: h(o) for o in OBJETIVOS}   # herencia: estado previo
# ... cuerpo del parche (muta OBJETIVOS) ...
rubricar('metricas_v02', OBJETIVOS, hash_prev)          # linaje
for o in OBJETIVOS: sellar_herencia(o, 'metricas_v02', hash_prev[o])  # marca en header
