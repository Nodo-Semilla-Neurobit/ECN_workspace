# Informe: Duplicados y Colisiones del path_map.json

Fecha: 2026-08-25T06:18:53 -03:00 (registro de wril_historial)

Resumen ejecutivo
- Entradas en path_map.json: 149
- Colisiones registradas en wril_historial.jsonl (último registro): 9
- Nombres de archivo duplicados detectados: 14 grupos
- Claves sin separador (raíz) tras normalización: 16 (estas permanecen en la raíz como entradas explícitas)

Archivo historial (última entrada en wril_historial.jsonl):

```
{"t": "2026-08-25T06:18:53.965319", "tipo": "COLISION_NOMBRES", "detalle": [
  "COLISION: 'README_ECN_Workspace_Canonico_v3.md' en '/home/gus/workspace_reconstruido/README_ECN_Workspace_Canonico_v3.md' y 'data/MD/README_ECN_Workspace_Canonico_v3.md'",
  "COLISION: 'informe_01_clasificacion.md' en '/home/gus/workspace_reconstruido/informe_01_clasificacion.md' y 'data/MD/informe_01_clasificacion.md'",
  "COLISION: 'clasificacion_ecn_v3.md' en '/home/gus/workspace_reconstruido/clasificacion_ecn_v3.md' y 'data/MD/clasificacion_ecn_v3.md'",
  "COLISION: 'boot_payload_v2.md' en '/home/gus/workspace_reconstruido/boot_payload_v2.md' y 'data/MD/boot_payload_v2.md'",
  "COLISION: 'informe_00_estado_inicial.md' en '/home/gus/workspace_reconstruido/informe_00_estado_inicial.md' y 'data/MD/informe_00_estado_inicial.md'",
  "COLISION: 'README_v2.md' en '/home/gus/workspace_reconstruido/README_v2.md' y 'data/MD/README_v2.md'",
  "COLISION: 'README.md' en '/home/gus/workspace_reconstruido/README.md' y 'data/MD/README.md'",
  "COLISION: 'path_map.json' en '/home/gus/workspace_reconstruido/path_map.json' y 'wril/path_map.json'",
  "COLISION: 'README.md' en '/home/gus/workspace_reconstruido/README.md' y 'MFN_Sprite_Cartografo/README.md'"
]}
```

---

Duplicados detectados (extracto):

1) README.md (3 ocurrencias)
   - ./README.md
   - data/MD/README.md
   - MFN_Sprite_Cartografo/README.md

2) README_ECN_Workspace_Canonico_v3.md (2)
   - ./README_ECN_Workspace_Canonico_v3.md
   - data/MD/README_ECN_Workspace_Canonico_v3.md

3) README_v2.md (2)
   - ./README_v2.md
   - data/MD/README_v2.md

4) boot_payload_v2.md (2)
   - ./boot_payload_v2.md
   - data/MD/boot_payload_v2.md

5) clasificacion_ecn_v3.md (2)
   - ./clasificacion_ecn_v3.md
   - data/MD/clasificacion_ecn_v3.md

6) informe_00_estado_inicial.md (2)
   - ./informe_00_estado_inicial.md
   - data/MD/informe_00_estado_inicial.md

7) informe_01_clasificacion.md (2)
   - ./informe_01_clasificacion.md
   - data/MD/informe_01_clasificacion.md

8) patch_post_campo.py (2)
   - INSTALACION_/Parches/patch_post_campo.py
   - wril/patch_post_campo.py

9) patch_raiz_canonica.py (2)
   - INSTALACION_/Parches/patch_raiz_canonica.py
   - wril/patch_raiz_canonica.py

10) path_map.json (2)
    - ./path_map.json
    - wril/path_map.json

11) wril_adapter_c64.py (2)
    - wril/wril_adapter_c64.py
    - tools/wril_adapter_c64.py

12) wril_canonizacion.md (2)
    - data/MD/wril_canonizacion.md
    - wril/wril_canonizacion.md

13) wril_corpus_exporter.sh (2)
    - INSTALACION_/wril_corpus_exporter.sh
    - wril/wril_corpus_exporter.sh

14) wril_patch_resolver.py (2)
    - INSTALACION_/Parches/wril_patch_resolver.py
    - wril/wril_patch_resolver.py

---

Sugerencias y notas para revisión manual
- Para documentación (.md): definir política clara: ¿`data/MD/` es el canon para documentación histórica y secundaria, y la raíz contiene apenas la documentación principal (README.md, guía de arranque)? O al revés. Propongo por defecto: mantener `./README.md` como punto de entrada y mover las copias en `data/MD/` a `archive/legacy/docs/` si no contienen información adicional.

- Para scripts y utilidades WRIL (wril_*, wril_patch_resolver.py, wril_corpus_exporter.sh): normalmente deben residir en `wril/`. Propuesta: mover las copias residuales en `INSTALACION_/` o `tools/` a `archive/legacy/wril_copies/` o consolidarlas en `wril/` si son activas.

- Para `path_map.json`: conservar la copia canónica en la raíz (`./path_map.json`) y mantener `wril/path_map.json` como archivo histórico (o eliminar la copia redundante después de verificar que no hay procesos que lo consuman directamente desde wril/).

- Antes de mover o borrar: crear backups atómicos en `archive/legacy/YYYYMMDD_HHMMSS/` y producir un plan dry-run con `mv -n` o `git mv` (si quieres versionarlo).

---

Siguientes pasos propuestos (elige uno):
- Generar plan dry-run con comandos `mv`/`cp` y backups para cada duplicado (recomendado si quieres aplicar un criterio uniforme).
- Revisar caso por caso: exportar este informe como archivo (hecho) y marcar los que quieres conservar/archivar; luego ejecuto los movimientos.

Reporte guardado en: `wril/path_map_duplicates_report.md`
