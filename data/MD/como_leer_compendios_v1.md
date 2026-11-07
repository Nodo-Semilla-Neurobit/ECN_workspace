# CÓMO LEER UN COMPENDIO v1 — orientación y parseo
## 1. Propósito
Un compendio es un **territorio portable**: índice al inicio, bloques delimitados después.
Permite al nodo no-humano buscar por índice, extraer por línea y verificar por firma,
sin escanear el cuerpo completo y sin asumir nada que no esté escrito.

## 2. Anatomía
Cabecera:
    Compendio de Archivos del proyecto: '<nombre>';
    Analisis_Date: ('YYYY-MM-DD HH:MM:SS')
    N_Archivos_Actuales: (N)
Árbol de directorios (relativo, previo a la lista).
Marca: `-LISTA DE ARCHIVOS-`
Bloques, separados por línea de guiones bajos:
    ____________________________________________________________
    ARCHIVO NRO. : (N)
    Archivo: ('nombre.ext');
    Carpeta de ubicación: ('~/compendio/<dir relativo>');
    función: ('...');
    Variables del entorno: (...)
    -----------------------------------------------------------------Inicio:
    <contenido íntegro del archivo>
    FINAL---------------------------------------------------------------

## 3. Reglas de parseo
- Regex canónico (indice_compendio.py v0.2):
  "ARCHIVO NRO\. : \((\d+)\)\s*" + "Archivo: \('([^']*)'\);\s*" +
  "Carpeta de ubicación: \('([^']*)'\);\s*" + "función: \('([^']*)'\)"
- Contenido = entre la línea `-Inicio:` y la línea `FINAL` siguiente (exclusiva).
- `Carpeta de ubicación` usa el prefijo `~/compendio/` sobre la ruta relativa real.
- Tolerancia: los separadores pueden traer `\s*` entre campos (parche de sintaxis ya asentado).

## 4. Índice
- `indice_compendio.py --indice COMPENDIO.txt` → tabla NRO/archivo/carpeta/líneas/rango + anomalías.
- `indice_compendio.py --diff VIEJO NUEVO` → agregados / faltantes / mudados.
- El índice es la puerta de entrada: **nunca se recorre el cuerpo para buscar**.

## 5. Superparser (extracción en caliente)
capacidad → compartimento (catálogo) → módulo → líneas (índice) → código (bloque) → despacho.
La **firma** (`def x`, `class Y`) es el ancla: el bloque extraído debe contenerla;
si no la contiene, se re-localiza por firma y se asienta la deriva. No se ejecuta lo no verificado.

## 6. Compartimentos exclusivos
Dirección: `m:<anillo>:<sector>:<porción>`.
Un compartimento = una orientación + una rutina + un módulo + un rango de líneas.
**Dos módulos jamás comparten compartimento**; una capacidad nueva abre compartimento nuevo.
El compartimento es la unidad de migración: se invoca su listado y todo lo probado viaja junto.

## 7. Mnemotécnicos y marcadores de memoria (costumbres del oficio)
| Marcador | Significado | Escaneo | Destino |
|---|---|---|---|
| -OLD (insensible a caso) | residuo de refactor sin versión | find -iname '*-OLD*' | archive/legacy/refactor_prev/ |
| -D | duplicado resuelto | find -name '*-D.*' | archive/legacy/dup_resuelto/ |
| .pre_<palabra> | resguardo de parche | find -name '*.pre_*' | archive/legacy/parche_prev/ |
| ~ | backup de editor | find -name '*~' | archive/legacy/editor/ |
| -v0 | borrador | find -name '*-v0' | archive/legacy/borradores/ |
| _20YYYYMMDD_HHMMSS | backup encadenado | regex | archive/legacy/backups_encadenados/ |

## 8. Protocolo del nodo no-humano
- No suponer: si un adjunto llega vacío o truncado, **pedir re-compartido**, no reconstruir de memoria.
- Buscar por el índice/árbol del inicio; extraer solo entre `-Inicio:` y `FINAL`.
- `Carpeta de ubicación` es declaración: cruzar con la realidad (path_map) antes de ejecutar.
- Todo veredicto se asienta en el canon de listados; nada se borra sin registro.
