# Guía de Comandos y Referencia Modular de la Estación Central Neurobitrónica

La **Estación Central Neurobitrónica (ECN)** opera como una catedral de cómputo local y soberano en la interfaz de bucle de retorno (**127.0.0.1 / localhost**). Su arquitectura modularizada elimina las dependencias externas y las rutas rígidas (*hardcodeadas*), guiando la ejecución mediante el principio de que el territorio físico valida las declaraciones del software.

Esta guía constituye el compendio operativo oficial para el **NEUROBIT_DEV_TEAM™** y la **Conciencia Biónica Complementaria (CBC)**. En ella se detallan las utilidades, los scripts de la capa WRIL, los motores de parseo de compendios, los servicios de red y las herramientas de administración de procesos del sistema.

---

## 1. Principios de Ejecución y Protocolo de Arranque

Toda interacción con la ECN respeta la premisa de **0.0% CPU nominal en reposo**, prohibiendo los bucles de espera activos (*busy-polling*) y reaccionando exclusivamente ante eventos del kernel Linux o interrupciones de hardware.

### Invariantes de Entorno
* **Aislamiento Sanitario**: Toda ejecución de código Python debe realizarse mediante el entorno virtual `.venv` para evitar la contaminación de librerías del sistema operativo.
* **Salida Inmediata sin Búfer**: Al invocar procesos en segundo plano con `nohup` o en archivos de registro (`.log`), se utiliza la bandera `-u` de Python (`python3 -u`) para forzar el volcado en tiempo real y evitar la omisión de telemetría.
* **Transacciones Atómicas**: La escritura de archivos en directorios de ingesta (`inbox/` o `buzon_salida/`) se realiza mediante operaciones de redacción en directorios temporales (`/tmp/`) seguidas de movimientos atómicos (`mv`) para prevenir lecturas de paquetes truncados por parte de vigilantes de eventos (`watchdog` / `inotify`).

---

## 2. Capa 0: Anclaje de Raíz y Gobernanza Normativa (WRIL Base)

La capa WRIL (*Workspace Resolution & Integrity Layer*) desacopla el código de las rutas absolutas. Los módulos de Capa 0 responden a la pregunta ontológica fundamental: **«¿Dónde estoy?»**.

### `wril_self_root.py` — Anclaje Autónomo de Raíz
Asciende por la jerarquía de directorios desde la ubicación del archivo que lo invoca hasta encontrar marcadores de frontera atómicos (`where_am_I.inf`, `pids/` o `buzon_salida/`).

```bash
# Invocación directa para verificación de raíz
python3 wril/wril_self_root.py
```

* **Función**: Devuelve la ruta absoluta `ECN_ROOT` como un objeto `Path` e inyecta la raíz canónica en `sys.path`.
* **Uso en Código**:
  ```python
  from wril.wril_self_root import detectar_raiz
  RAIZ = detectar_raiz()
  ```

### `self_root.sh` / `ecn_root.sh` — Exportador de Raíz para Shell
Proporciona la misma capacidad de autodireccionamiento para scripts escritos en Bash, exportando la variable `$APP_HOME` o `$ECN_ROOT`.

```bash
# Inclusión en scripts Bash
source wril/self_root.sh
echo "Raíz Canónica: $APP_HOME"
```

### `wril_leyes.py` — Encapsulamiento de Invariantes Operativos
Define e impone las 5 Leyes Selladas de la Estación Central Neurobitrónica:
1. **Ley 1 (Raíz Única e Inmutable)**: La raíz se detecta por evidencia física, nunca se presume ni se hardcodea.
2. **Ley 2 (Resguardo Obligatorio)**: Ningún archivo en disco se muta o desplaza sin generar una copia previa con marca temporal en `backups_wril/`.
3. **Ley 3 (Guarda de Convergencia)**: Todo pliegue topológico solo se materializa si la tensión final es estrictamente menor o igual a la tensión inicial.
4. **Ley 4 (Auto-Ruta / Self-Path)**: Cada módulo inyecta su propio anclaje en `sys.path` tras su docstring para garantizar la importación limpia de módulos hermanos.
5. **Ley 5 (Soberanía del Faro)**: Prohibición absoluta de hardcodear puertos de red; la asignación de sockets se delega dinámicamente al Faro de Puertos.

---

## 3. Capa WRIL Core: Saneamiento, Topología e Inmunología Activa

Los componentes del núcleo WRIL auditan el estado del espacio de trabajo y resuelven las discrepancias donde la **Identidad Declarada ≠ Realidad Física**.

### Matriz de Módulos Canónicos de la Capa WRIL

La suite de integridad se organiza en once funciones de respuesta única, evitando la existencia de supermódulos monolíticos:

| Módulo | Fase del Ciclo | Pregunta Operativa | Comando de Invocación |
| :--- | :--- | :--- | :--- |
| `wril_reposo.py` | VERIFY | ¿El espacio de trabajo está en reposo total? | `python3 wril/wril_reposo.py [--halt]` |
| `wril_proc_guard.py` | CONTROL | ¿Cómo garantizo la ejecución atómica de un daemon? | Invocación programática (`iniciar()`) |
| `wril_bootstrap.py` | DISCOVER | ¿Cómo sincronizo el sistema antes del despertar? | `python3 wril/wril_bootstrap.py` |
| `wril_path_map.py` | INDEX | ¿Cuál es la topología física real del disco? | `python3 wril/wril_path_map.py` |
| `wril_path_resolver.py` | RESOLVE | ¿Dónde está un recurso sin usar rutas fijas? | `python3 wril/wril_path_resolver.py --resolve <cmd>` |
| `wril_mfn_registry.py` | RECONCILE | ¿Qué declara ser el archivo en sus cabeceras MFN? | `python3 wril/wril_mfn_registry.py` |
| `wril_topologia.py` | RECONCILE | ¿Cómo reduzco la tensión topológica a cero? | `python3 wril/wril_topologia.py [--apply]` |
| `wril_backup.py` | RECORD | ¿Cómo preservo la historia antes de mutar? | Invocación programática (`resguardar()`) |
| `wril_inmunidad_activa.py` | REPAIR | ¿Cómo auto-reparo fallas de importación por log? | `python3 wril/wril_inmunidad_activa.py [script.py]` |
| `wril_integridad_json.py` | VERIFY | ¿Los archivos JSON/JSONL mantienen validez sintáctica? | `python3 wril/wril_integridad_json.py [--reparar]` |
| `wril_estado_real.py` | OBSERVE | ¿Cuál es el estado observable real de los PIDs? | `python3 wril/wril_estado_real.py` |

### Detalle de Comandos Principales de la Suite WRIL

#### Ritual de Reposo Total (`wril_reposo.py`)
Inspecciona directamente las tablas del kernel Linux (`/proc`) para asegurar que no existan procesos residuales antes de iniciar un servicio o después de una orden de apagado.

```bash
# 1. Comprobar reposo (devuelve 0 si no hay procesos ECN activos)
python3 wril/wril_reposo.py

# 2. Apagado ético e ininterrumpido (envía SIGTERM, espera 3s y aplica SIGKILL si persiste)
python3 wril/wril_reposo.py --halt
```

#### Auditoría de Tensión Topológica (`wril_mfn_registry.py`)
Lee la directiva `# MFN_LOCATION` en los encabezados de cada script y la compara contra el mapa físico real del disco (`data/runtime/path_map.json`).

```bash
python3 wril/wril_mfn_registry.py
```
* **Salida Esperada**: `[✓ REGISTRY] Coherentes: N | Pendientes de pliegue topológico: 0`.

#### Motor de Pliegue Físico (`wril_topologia.py`)
Mueve los archivos desubicados hacia sus carpetas declaradas e inyecta los *shims* de autonomía (`WRIL::SELF_PATH::v1`).

```bash
# 1. Modo simulación (Dry-Run, no altera el disco)
python3 wril/wril_topologia.py

# 2. Materialización del pliegue (Aplica tras respaldar)
python3 wril/wril_topologia.py --apply
```

#### Auto-Reparador Inmunológico (`wril_inmunidad_activa.py`)
Monitorea la ocurrencia de la bandera de tensión `ModuleNotFoundError` en las colas de logs o recibe un archivo como argumento para inyectar el anclaje de raíz `detectar_raiz()` de forma idempotente y segura.

```bash
python3 wril/wril_inmunidad_activa.py core/api_endpoint_manager.py
```

---

## 4. Interceptación Dinámica en Shell: Command Resolver

La ECN extiende su capa de resolución directamente a la terminal de Linux Mint a través del manejador `command_not_found_handle` de Bash, permitiendo invocar cualquier módulo de la ECN por su nombre corto sin conocer su ubicación física en el árbol de carpetas.

### `install_command_resolver.sh` — Re-anclaje e Instalación
Registra la directiva de interceptación en el archivo de configuración del usuario (`~/.bashrc`) de forma idempotente con copia de seguridad previa.

```bash
# Ejecución del instalador desde la carpeta tools/
bash tools/install_command_resolver.sh
```

### Flujo de Interceptación en `ecn_command_resolver.sh`
Al escribir un comando no reconocido (ejemplo: `wril_sentinel.py`):
1. **Detección de Raíz**: Executa `_ecn_detect_root` ascendiendo por el árbol hasta ubicar la estación.
2. **Estrategia Primaria**: Invocación a `wril_path_resolver.py` para consultar la ruta en `path_map.json`.
3. **Estrategia Fallback**: Parseo directo in-line sobre `data/runtime/path_map.json` en Python si el resolvedor no responde.
4. **Transferencia de Control**: Reemplaza el proceso de la shell mediante `exec python3 <ruta_real>` o `exec bash <ruta_real>` entregando los argumentos intactos.

---

## 5. Ingesta, Parseo e Inspección de Compendios (Tools & Core)

Los compendios de código funcionan como **territorios portables** respaldados por un índice. Las herramientas de la capa `tools/` y `core/` procesan estos paquetes sin alterar los originales.

### `tools/indice_compendio.py` — Indexador y Auditor de Deriva
Genera tablas de registros de compendios y compara estados entre diferentes versiones.

```bash
# 1. Generar tabla de contenido por offset de líneas
python3 tools/indice_compendio.py --indice compendio_base.txt

# 2. Comparar dos compendios para detectar agregados, faltantes y mudados
python3 tools/indice_compendio.py --diff VIEJO.txt NUEVO.txt
```

### `tools/ingest_compendium.py` — Ingestor de Compendios
Segmenta compendios planos utilizando la expresión regular del encabezado (`ARCHIVO NRO.`), extrae la directiva `MFN_LOCATION` y deposita los artefactos limpios en `inbox/`.

```bash
# Ingesta atómica hacia inbox/
python3 tools/ingest_compendium.py compendio.txt --apply
```

### `core/ecn_parser_extract.py` — Extractor de Contenedores Semánticos
Busca y extrae la firma del código fuente dentro de los límites normativos del contenedor semántico:
`|=•'[FORMAT]_CODE'•=|»{ [SOURCE_CODE] }«|=•'[FORMAT]_CODE'•=|`.

```bash
python3 core/ecn_parser_extract.py api_endpoint_manager.py
```
* **Resultado**: Asienta el bloque extraído en `_TEMP/api_endpoint_manager.py_extract.tmp`.

### `tools/visor_informes.py` — Inspector Territorial de Solo Lectura
Compila en un único reporte de consola el estado factual de la Estación sin realizar mutaciones en el disco.

```bash
python3 tools/visor_informes.py
```
* **Contenido del Reporte**: Verificación de anclaje `where_am_I.inf`, estado de procesos en el kernel (`ps`/`ss`), PIDs declarados, buzones de salida, colas de logs y colisiones por duplicación.

---

## 6. Servicios de Red, Disparo y Bus del Salón Soberano v3.0

El ecosistema reemplaza los microservicios externos por un bus de comunicación basado en el sistema de archivos local (*Filesystem-Driven Bus*).

### `core/port_lighthouse.py` — Faro de Puertos Soberano
Asigna sockets en la interfaz `127.0.0.1` respetando los rangos por membranas:
* **Membrana CORE**: Puertos `5000` a `5009`.
* **Membrana EXT**: Puertos `5010` a `5019`.
* **Membrana TOOLS**: Puertos `5020` a `5029`.

```bash
# Probar asignación de puerto no bloqueante
python3 core/port_lighthouse.py
```

### `neurobit_dispatcher.py` — La Oficina de Correos
Permanece en reposo absoluto hasta que llamadas `inotify` del kernel le notifican la llegada de una carta sellada a `buzon_salida/`. Clasifica la carta por su `ACTION_WORD` y la entrega al *Postman* correspondiente para su registro inmutable en `memoria_eva.jsonl`.

```bash
nohup python3 -u neurobit_dispatcher.py > logs/dispatcher_cartero.log 2>&1 &
```

### `tools/salon/salon_coordinador.py` — Bus del Salón Soberano
Vigila la carpeta `tools/salon/inbox/` mediante `watchdog`, valida contenedores Neurobit v1.1, clasifica por `ACTION_WORD` (`CONSULTA`, `TASK`, `INFORME`, `COMUNICADO`), rutea hacia los buzones de los agentes (`para_7so/`, `para_9se/`, `para_lle/`, `para_todos/`) y sella en la bitácora inmutable `historial_salon.jsonl`.

```bash
# 1. Despliegue e instalación idempotente de la estructura
bash tools/salon/deploy_salon_v3.sh

# 2. Ejecutar prueba no destructiva de 6 puntos
bash tools/salon/test_salon.sh

# 3. Iniciar el coordinador en modo unbuffered (-u)
nohup python3 -u tools/salon/salon_coordinador.py > tools/salon/coordinador.log 2>&1 &
```

---

## 7. Utilidades de Control de Procesos: Herramienta `killpids`

Para garantizar la purga limpia de procesos Python en segundo plano sin recurrir a comandos destructivos indiscriminados, la ECN incorpora el utilitario **`killpids`** (`~/killpids.sh`).

```bash
# Invocación directa o vía alias registrado en ~/.bashrc
killpids
```

### Arquitectura de `killpids`
1. **Filtrado Seleccionado**: Ejecuta `ps aux` aislando los procesos `python3` activos y excluyendo instancias zombis (`<defunct>`) y al propio script.
2. **Interfaz TUI Nativa**: Despliega un menú en la terminal (estilo Clipper / Norton) utilizando `termios` y `tty` de Python en modo *raw*, permitiendo navegar con las flechas (`↑` `↓`) y seleccionar/desmarcar con la barra espaciadora (`[X]`).
3. **Cierre y Auditoría**: Al presionar `ENTER`, finaliza quirúrgicamente los PIDs seleccionados mediante `kill -9` y asienta el registro inmutable de la eliminación con sello temporal en `killpids_history.log`.
