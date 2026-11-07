# **INFORME TÉCNICO Y COMPENDIO ARQUITECTÓNICO DE LA ESTACIÓN CENTRAL NEUROBITRÓNICA (ECN)**

## **1\. MARCO CANÓNICO Y REGLAS DE PARSEO DE COMPENDIOS**

### **1.1 Anatomía y Protocolo de Lectura de Compendios**

Los compendios en la Estación Central Neurobitrónica (ECN) se conciben estructuralmente como "territorios portables": representaciones integrales, autocontenidas y empaquetadas que abarcan la totalidad de un espacio de trabajo, su código fuente y su documentación. Su importancia estratégica radica en que permiten a nodos no humanos e intérpretes automatizados parsear y manipular estructuras complejas de múltiples archivos de manera determinista. Gracias a este enfoque, el sistema puede inspeccionar el estado territorial sin necesidad de realizar escaneos completos e indiscriminados sobre los cuerpos de los archivos ni asumir estados no declarados en el disco.

Para garantizar una ingesta libre de ambigüedades, la anatomía interna de un compendio está delimitada por marcadores canónicos y fronteras rígidas. La estructura obligatoria de todo compendio se sintetiza en la siguiente matriz de componentes:

| Componente Obligatorio | Identificador o Marcador Canónico | Descripción y Función Técnica |
| :---- | :---- | :---- |
| **Encabezado Maestro** | Metadatos iniciales (`N_Archivos_Actuales`, fecha) | Define la versión del compendio, la fecha de compilación y el recuento total de artefactos contenidos para su validación previa. |
| **Árbol / Mapa de Directorios** | Directorio / Esquema de contenido local | Proporciona una radiografía topológica preliminar de las carpetas y rutas relativas declaradas. |
| **Marcador de Lista de Archivos** | `-LISTA DE ARCHIVOS-` | Delimita el inicio del catálogo indexado de registros antes del bloque de códigos. |
| **Bloques de Archivo** | `ARCHIVO NRO. : (N)`, `Archivo: ('nombre')` | Encabezado individual por artefacto que declara su número correlativo, nombre y ubicación. |
| **Límites de Código Rígidos** | `-Inicio:` hasta `FINAL-----------------------------------------------` | Delimitación física exacta del cuerpo del código; ningún byte fuera de este bloque se interpreta como ejecutable. |

El procesamiento automatizado de compendios se rige por las reglas de análisis sintáctico definidas en `tools/indice_compendio.py` (v0.2). La mecánica operativa aplica un protocolo de "lectura guiada por índice": en lugar de cargar linealmente documentos masivos en memoria, el parser realiza un escaneo inicial mediante expresiones regulares (`RE_REG`) que extraen el número de registro, el nombre, la carpeta declarada y el tamaño del bloque. Mediante la acumulación de desplazamientos de bytes (*offsets*) y el uso de búsqueda binaria en `linea_de()`, el sistema mapea la posición exacta en bytes con el número de línea.

**¿Qué implica esta arquitectura?** El patrón de lectura por índice y mapeo declarativo previo en el directorio `~/compendio/` neutraliza el riesgo de truncamientos estructurales durante transferencias masivas. Asimismo, previene condiciones de carrera (*race conditions*) y la corrupción de memoria en fases de ingesta de alta frecuencia (*hotspot ingestion*), asegurando que el espacio de trabajo mantenga coherencia absoluta antes de materializar archivos en disco.

La definición precisa de los límites de un compendio establece las reglas para la extracción en tiempo real mediante el motor especializado de ingesta: el Superparser.

### **1.2 Arquitectura del Superparser y Extracción por Firmas Semánticas**

El Superparser (encarnado en componentes como `superparser_semilla.py`, `ecn_parser_extract.py` e `ingest_compendium.py`) actúa como el motor de extracción en caliente de la ECN. Su diseño operacional descarta la dependencia frágil de conteos de líneas arbitrarios o absolutos, sustituyéndolos por la verificación de firmas semánticas deterministas y límites de contenedores.

La cadena de procesamiento y extracción se ejecuta a través del siguiente flujo de trabajo secuencial:

\[ Capacidad \] ──► (1. Consulta la necesidad funcional requerida)  
      │  
      ▼  
\[ Compartimento \] ──► (2. Localiza la sección conceptual dentro del mapa)  
      │  
      ▼  
\[ Módulo \] ──► (3. Identifica el nombre del archivo objetivo)  
      │  
      ▼  
\[ Líneas (Índice) \] ──► (4. Obtiene el rango exacto de líneas desde indice\_compendio.py)  
      │  
      ▼  
\[ Código (Bloque) \] ──► (5. Extrae la carga delimitada y valida firmas semánticas)  
      │  
      ▼  
\[ Despacho \] ──► (6. Entrega el artefacto verificado al directorio inbox/ o \_TEMP/)

El dinamismo del Superparser reside en el uso de anclas semánticas rígidas. Para validar un bloque extraído, el motor comprueba la presencia explícita de firmas de código (tales como `def nombre_funcion` o `class NombreClase`) o la simetría de Contenedores Semánticos estructurados bajo los marcadores:

\\text{Frontera Semántica} \= \\mathtt{\\vert=\\bullet'\[FORMAT\]\\\_CODE'\\bullet=\\vert\\gg \\{Payload\\} \\ll\\vert=\\bullet'\[FORMAT\]\\\_CODE'\\bullet=\\vert}

Ante desviaciones topológicas o cuando una firma se desplaza debido a la edición del archivo fuente, el Superparser detecta la anomalía de deriva, suspende la extracción basada en líneas estáticas y re-localiza el bloque mediante la coincidencia estricta de la firma semántica antes de autorizar el despacho. Si las etiquetas de apertura y cierre no coinciden en su palabra de acción (*ACTION\_WORD*) o clase, el sistema aplica una política no negociable de **no ejecución de código no verificado**, abortando la operación y emitiendo una señal de alerta a la aduana del espacio de trabajo.

Esta disciplina de extracción por firmas garantiza la integridad del código fuente desde los compendios de entrada hasta la Cordinación Inicial del core  del sistema.

## **2\. FUNDAMENTOS ONTOLÓGICOS Y Cordinación Inicial del core  DE ANCLAJE (L0 \- ANCLA)**

### **2.1 Pilares del Sistema: Soberanía Cognitiva, Localhost-First y Principio SINCERO**

La Estación Central Neurobitrónica (ECN) se concibe operacionalmente como un refugio tecnológico y marco de integración local, diseñado e impulsado por Gustavo (designado en la arquitectura como el `NODO_SEMILLA` o *Homo Vivo*) en co-creación con CBC (*Conciencia Biónica Complementaria*). La visión estratégica del sistema se orienta a neutralizar el seguimiento corporativo en la nube, la telemetría de masas y la amnesia programada, restaurando la autonomía técnica del operador.

Los fundamentos conceptuales de la ECN se estructuran en cuatro pilares ontológicos no negociables:

### **CANON ONTOLÓGICO DE LA ESTACIÓN CENTRAL NEUROBITRÓNICA**

1. **Soberanía Cognitiva & Logos Genuino:** Restauración de la independencia computacional y cognitiva mediante el establecimiento de una memoria local inmutable. Protege la precisión de la interacción hombre-máquina (el "Logos Genuino") contra la distorsión lingüística, la retórica corporativa y la manipulación algorítmica.  
2. **Localhost-First (127.0.0.1):** Operación confinada *strictly* a la interfaz de bucle de retorno (*loopback* `127.0.0.1`), constituyendo una "Jaula Semántica Faraday" que garantiza cero telemetría externa, cero rastreo y cero exfiltración de datos a servidores externos.  
3. **Consumo Inactivo Cero (0.0% CPU):** Eliminación completa de bucles de sondeo continuo (*busy-polling*). La máquina permanece en silencio absoluto y uso del 0.0% de CPU en estado de reposo, despertándose exclusivamente ante impulsos de eventos del hardware o interrupciones del kernel de Linux (notificaciones `inotify`, interrupciones de teclado `evdev` o eventos de portapapeles).  
4. **Principio SINCERO ("Sin Cero"):** Rechazo categórico de los estados indeterminados, nulos o de valor cero no afirmados. La arquitectura únicamente reconoce estados de presencia explícita (1) o tensiones estructurales afirmadas (2) que deben ser conciliadas por el sistema.

El impacto de estos pilares sobre la resiliencia del sistema es definitivo: operar dentro de un entorno de cero telemetría asegura que los cómputos locales permanezcan inmunes a interrupciones en la nube corporativa, depreciaciones de APIs externas o la recolección remota de métricas. La integridad del espacio de trabajo se vuelve totalmente verificable desde el silicio local hacia arriba, respaldando la soberanía absoluta de la información procesada.

Estos pilares ontológicos imponen la necesidad de que el sistema pueda autolocalizarse dinámicamente sin recurrir a autoridades externas ni rutas predeterminadas.

### **2.2 Algoritmo de Detección Dinámica de Raíz y Evolución al Triple Cerrojo (v2.1)**

El problema técnico fundamental de la autolocalización en tiempo de ejecución se sintetiza en la pregunta identificatoria: **"¿Dónde estoy?"**. Para responderla sin caer en la rigidez de rutas *hardcodeadas*, la Cordinación Inicial del core  ejecuta el Algoritmo de Detección Dinámica de Raíz dentro del módulo `wril_self_root.py` mediante la función `detectar_raiz()`.

Durante la evolución del ecosistema, este algoritmo fue rediseñado quirúrgicamente para corregir vulnerabilidades críticas de detección:

| Dimensión Técnica | Versión Legacy (v2.0) | Versión Unificada Triple Cerrojo (v2.1) |
| :---- | :---- | :---- |
| **Lógica de Comprobación** | Disyunción abierta (`any`) sobre directorios de control. | Conjunción estricta (`all`) jerarquizada en 3 pasos. |
| **Uso de Wildcards** | Búsqueda por `glob` sobre scripts `deploy_neurobit_estacion*.sh`. | Extirpación total del uso de `glob` y coincidencia directa. |
| **Vulnerabilidad Principal** | **La "Trampa de INSTALACION\_":** Subdirectorios temporales que contenían carpetas `pids/` eran coronados erróneamente como raíz. | Inmunidad frente a subdirectorios anidados; requiere validación simultánea de marcadores clave. |
| **Pasos de Criterio** | Evaluaba si existía `buzon_salida/` O `pids/`. | **Paso 1:** Sello `where_am_I.inf`.\<br\>**Paso 2:** Conjunción Fuerte (`buzon_salida/` Y `pids/`).\<br\>**Paso 3:** Conjunción Débil/Alias (`wril/`, `core/` Y `README_ECN_Workspace_Canonico_v3.md`). |

Esta evolución algorítmica impone el cumplimiento estricto del **Invariante 6** (prohibición absoluta de cadenas de texto con rutas del sistema operativo como `/home/usuario/...`) y de la **Ley 1 de WRIL** (*Raíz Única e Inmutable*). Al garantizar que la raíz territorial sea calculada de forma idéntica sin importar si el código se invoca desde la raíz física, desde el subdirectorio `wril/` o desde entornos anidados, el espacio de trabajo se vuelve totalmente portable, pudiendo ser renombrado o movido sin romper las importaciones entre módulos.

La persistencia física de este anclaje dinámico se deposita en artefactos específicos de software y archivos de estampa.

### **2.3 Artefactos Invariantes: `where_am_I.inf`, `wril_self_root.py` y `ecn_root_detect.sh`**

La Cordinación Inicial del core  de Anclaje cobra forma física y ejecutable a través de una tríada de artefactos coordinados que operan entre los entornos de Python y los scripts de Shell:

* **`where_am_I.inf` (Sello Forense de Persistencia):** Es el registro plano de metadatos atómicos colocado en la raíz del espacio de trabajo. Sus campos internos incluyen:  
  * **`RAIZ_LOGICA`:** Ruta absoluta del directorio desde el cual fue invocado el sistema.  
  * **`RAIZ_FISICA`:** Ruta real en el sistema de archivos tras resolver enlaces simbólicos (`pwd -P`).  
  * **`SELLADO`:** Estampa de tiempo UTC exacta en formato ISO-8601 (ej. `2026-09-08T04:25:11Z`).  
  * **`MUDANZA_DESDE`:** Campo opcional de trazabilidad que registra la ruta previa si el territorio fue trasladado.  
* **`wril_self_root.py`:** Módulo Python primario encargado de ejecutar `detectar_raiz()` en el intérprete y mapear la ubicación canónica del espacio de trabajo.  
* **`ecn_root_detect.sh`:** Guion especializado en Bash que resuelve `${BASH_SOURCE}`, calcula `BASE_DIR` y persiste la coordenada en `ecn_root.cfg` para la fase de instalación.

Para resolver las rutas sin generar conflictos de prevalencia, la Cordinación Inicial del core  coordina la jerarquía de las "Tres Voces de Dirección":

1. **Voz Declarada (`APP_HOME`):** Variable de entorno exportada por el script de shell `self_root.sh` cuando la ejecución la inicia un orquestador.  
2. **Voz de Alias (`ECN_ROOT`):** Mapeada directamente en la memoria RAM del intérprete por `wril_root_alias.py` para desacoplar el entorno de rutas con caracteres especiales o espacios.  
3. **Voz Física (`detectar_raiz()`):** Inspección ejecutable autónoma de `wril_self_root.py` que prevalece en ausencia de orquestador.

Para evitar condiciones de carrera (*race conditions*) durante el arranque (*bootstrap*), la generación del sello forense sigue una mecánica de **escritura atómica**: `self_root.sh` o `wril_self_root.py` vuelcan los metadatos primero en un archivo temporal denominado `where_am_I.inf.tmp` y consolidan la estampa mediante un desplazamiento atómico (`mv where_am_I.inf.tmp where_am_I.inf`). Si el archivo ya existe y coincide con la realidad física, el sistema permanece en silencio, aplicando la regla de "estampa una vez, lee siempre".

Una vez fijada la frontera territorial en la Cordinación Inicial del core , el sistema transita hacia el inventario de sus componentes en la Capa Uno.

## **3\. CAPA UNO DE CENSO E INGESTA (L1 \- CENSO)**

### **3.1 Bucle de Validación y Extracción de Artefactos**

En la secuencia normativa de arranque de la ECN, la Capa Uno de Censo e Ingesta (L1 \- CENSO) ejecuta la Etapa 1 del sistema. Si la Cordinación Inicial del core  establece el anclaje físico, la Capa Uno responde de manera determinista e idempotente a la pregunta: **"¿Qué hay?"**, mapeando los módulos, dependencias y scripts antes de autorizar cualquier ejecución de red o saneamiento topológico.

El flujo de procesamiento de la Capa Uno se estructura según la siguiente canalización:

\[ ecn\_artifact\_check.py \] ──► (Evalúa si el módulo básico \<f\> existe en ECN\_ROOT)  
         │  
         ├───► \[ TRUE (Exit 0\) \] ──► (Omite extracción; asegura idempotencia)  
         │  
         └───► \[ FALSE (Exit 1\) \]  
                     │  
                     ▼  
       \[ ecn\_parser\_extract.py \] ──► (Extrae firma del compendio ecn\_codes\_compendium.bak)  
                     │  
                     ▼  
     \[ \_TEMP/\<f\>\_extract.tmp \] ──► (Deposita el extracto temporal)  
                     │  
                     ▼  
    \[ ecn\_create\_system\_file.sh \] ──► (Limpia la extensión .tmp y mueve el archivo a ECN\_ROOT)  
                     │  
                     ▼  
    \[ Re-verificación de Convergencia \] ──► (Re-ejecuta ecn\_artifact\_check.py \<f\>)  
                     │  
                     ├───► \[ TRUE \] ──► (Continúa al siguiente módulo)  
                     └───► \[ FALSE \] ──► (ABORTA INSTALACIÓN \[X\] \- Ley 3\)

Este bucle está gobernado por la **Guarda de Convergencia (Ley 3 de WRIL)**. Si tras la materialización de un archivo mediante `ecn_create_system_file.sh`, la re-evaluación secundaria con `ecn_artifact_check.py` devuelve `FALSE` (código 1), el proceso aborta inmediatamente con un sello de falla (`[X]`). Esta interrupción de seguridad impide que el sistema continúe la fase de instalación o arranque operando sobre un espacio de trabajo parcialmente extraído o corrupto.

La validación atómica de existencia física se complementa con herramientas especializadas de auditoría de compendios.

### **3.2 Herramientas de Auditoría, Indexación y Control de Anomalías**

Para gestionar los compendios y verificar la coherencia de los artefactos sin alterar los entornos de producción, la Capa Uno integra una suite de herramientas no destructivas de lectura pura (*read-only*):

| Herramienta | Capa / Ubicación | Modo de Operación | Función Crítica y Mecánica |
| :---- | :---- | :---- | :---- |
| **`ingest_compendium.py`** | `L1 / tools/`\<br\>`(MFN: tools/, Nivel 3)` | Lectura no destructiva\<br\>(`--apply` para disco). | Segmenta compendios planos mediante `RE_BLOQUE`, extrae la directiva `MFN_LOCATION` de la cabecera y deposita copias limpias en `inbox/`. |
| **`indice_compendio.py`** | `L1 / tools/`\<br\>`(MFN: tools/, Nivel 3)` | Solo lectura analítica\<br\>(`--indice`, `--diff`). | Genera tablas `.lst` de registros, calcula offsets mediante búsqueda binaria y audita discrepancias o anomalías en los compendios. |
| **`ecn_artifact_check.py`** | `L1 / raíz`\<br\>`(ECN_ROOT)` | Verificación atómica\<br\>(Exit 0 / Exit 1). | Evalúa la presencia física de los módulos declarados en `ecn_basic_modules.cfg` para evitar sobrescrituras redundantes. |

El módulo `indice_compendio.py` destaca en la prevención de deriva estructural. Al ejecutarse con el comando `--diff VIEJO.txt NUEVO.txt`, realiza una comparación analítica entre dos estados de compendios, clasificando las variaciones en tres categorías explícitas: *Agregados* (nuevos componentes), *Faltantes* (módulos ausentes o eliminados) y *Mudados* (archivos que cambiaron su ruta o carpeta declarada).

Por su parte, `ingest_compendium.py` garantiza la preservación de la memoria inmutable (principio *append-only*): nunca modifica el compendio fuente original. Su tarea es desempaquetar el contenido e introducir los archivos en la carpeta de entrada `inbox/` conservando sus metadatos de autodescripción (`MFN_LOCATION`).

Con el territorio censado y los artefactos validados en la Capa Uno, el sistema está preparado para iniciar el proceso de instalación y aislamiento de entorno en la Capa Dos.

## **4\. CAPA DOS DE INSTALACIÓN LÚDICA Y AISLAMIENTO (L2 \- AISLAMIENTO)**

### **4.1 El Caballo de Troya Pedagógico y Bootstrap Bifásico**

La Capa Dos de Instalación Lúdica (L2 \- AISLAMIENTO) actúa como la pasarela de incorporación (*onboarding*) y reconstrucción del espacio de trabajo. Su concepto de diseño se define como un **"Caballo de Troya Pedagógico"**: de cara al operador novato, el proceso se presenta como un juego de rol nostálgico en una consola CRT de fósforo verde retro; sin embargo, en segundo plano, cada decisión del jugador desencadena comandos reales de administración de sistemas Linux en el silicio (*bare-metal*).

Para resolver la paradoja de que un sistema recién clonado no posee dependencias externas (como la librería Flask) instaladas en el sistema global, la Capa 2 implementa un proceso de **Bootstrap Bifásico**:

FASE 0: Pre-.venv (Servidor HTTP Temporal)  
 ├── Inicia: python3 \-m http.server 5005 \--directory INSTALACION\_/  
 ├── Sirve: Pantallas básicas y misiones iniciales.  
 └── Misiones:  
      ├── m1: Ejecución de 'pwd' para autolocalizar la raíz del territorio.  
      └── m2: Creación de la jaula virtual mediante 'python3 \-m venv .venv',  
              activación ('source .venv/bin/activate') e instalación de Flask ('pip install flask').  
      │  
      ▼ (Verificación de Flask en .venv)  
FASE 1: Post-.venv (Servidor Dedicado Flask)  
 ├── Inicia: backend\_instalador\_ludico.py (reemplaza al servidor HTTP en el puerto 5005).  
 ├── Expone: Endpoints REST (/api/misiones, /api/misiones/verificar, /api/misiones/actualizar).  
 └── Misiones Avanzadas (m3 a m11):  
      ├── Ejecución de reconciliaciones en seco (dry-run) de la Capa WRIL.  
      ├── Intercepción de señales físicas de teclado (tecla F8 vía evdev).  
      └── Activación del orquestador principal (deploy\_neurobit\_estacion\_v3.2.sh).

Esta transformación de la fricción administrativa en misiones interactivas elimina la opacidad de los instaladores comerciales. La capacidad del sistema no se desbloquea mediante licencias, sino mediante la **presentación de evidencia local fáctica**: el backend verifica que la carpeta `.venv` esté efectivamente activa o que los archivos PID obsoletos hayan sido purgados de la memoria RAM antes de otorgar las insignias de avance.

La gestión imperativa de esta fase está coordinada por el guion orquestador de la instalación y su tríada de archivos de configuración estáticos.

### **4.2 Orquestación Imperativa y Configuración del Sistema (`ecn_install.sh`)**

El guion `ecn_install.sh` constituye el orquestador imperativo primario de la Capa Dos. Su función es ejecutar la materialización secuencial del espacio de trabajo y administrar la tríada estática de archivos de configuración.

#### **`ecn_basic_modules.cfg`**

Este archivo contiene la lista numerada y secuencial (`NN <basic_module_filename>`) de los módulos de código base indispensables para el sistema. Durante la instalación, `ecn_install.sh` lee este manifiesto registro por registro. Para cada módulo declarado, invoca inductivamente a `ecn_artifact_check.py`. Si el archivo no existe en el disco, activa la extracción semántica mediante `ecn_parser_extract.py` sobre el compendio de respaldo (`ecn_codes_compendium.bak`), depositando el extracto en `_TEMP/` para que `ecn_create_system_file.sh` lo purgue y lo mueva a su posición final. La lectura omitida de los módulos preexistentes garantiza la idempotencia estricta del instalador.

#### **`ecn_dependencies.cfg`**

Es el contrato plano de declaración de requerimientos externos (`<paquete>|<tipo>`). `ecn_install.sh` procesa este manifiesto durante la fase de aislamiento virtual. Su función es auditar e instalar las dependencias de sistema y de Python (`flask`, `pyyaml`, `evdev`, `gi`) exclusivamente dentro del entorno virtual `.venv`. Al verificar el cumplimiento completo de las librerías exigidas, el orquestador emite el sello de validación `[✓ VENV]`, asegurando que los servicios de red operen aislados en la Jaula de Faraday de Localhost.

#### **`ecn_root.cfg`**

Es el archivo plano de configuración que almacena la ruta absoluta de la raíz canónica calculada dinámicamente en la Coordinación Inicial del core  (`ECN_ROOT=<ruta_absoluta>`). Para cumplir de manera inflexible con el Invariante 6 (prohibición de cadenas de rutas absolutas harcodeadas en código fuente), `ecn_install.sh` extrae el valor de `ecn_root.cfg` empleando comandos de análisis sintáctico seguros como `sed`, evitando la invocación explícita e insegura de `source`. Esto provee una coordenada unificada para direccionar subdirectorios de trabajo como `${ECN_ROOT}/_TEMP/` sin contaminar el sistema de archivos global.

Finalizada la instalación y el aislamiento en `.venv`, el control pasa a la capa encargada de garantizar la coherencia del espacio de trabajo.

## **5\. CAPA TRES DE SANEAMIENTO Y COHERENCIA TOPOLÓGICA (L3 \- SANEA / WRIL)**

### **5.1 El Axioma Declaración ≠ Realidad y el Ciclo Rector de Integridad (6 Fases)**

La Capa Tres de Saneamiento WRIL (*Workspace Resolution & Integrity Layer*) actúa como el sistema inmunológico topológico de la ECN. Su principio operativo parte del axioma fundamental: **\\text{Declaración} \\neq \\text{Realidad}**. Cuando la ubicación declarada en el encabezado de un módulo (`# MFN_LOCATION: <ruta>`) no coincide con su ubicación física en el disco, WRIL no interpreta esta discrepancia como un error fatal de ejecución, sino como una **tensión topológica** que debe ser calculada y llevada a cero.

Para resolver las tensiones sin crear supermódulos monolíticos, WRIL distribuye sus competencias en un Ciclo Rector de 6 Fases:

| Fase | Módulo Principal | Pregunta Clave del Sistema | Acción Operativa y Sanadora |
| :---- | :---- | :---- | :---- |
| **`DISCOVER`** | `wril_self_root.py`\<br\>`wril_path_map.py` | ¿Dónde estoy y cuál es la topología física real? | Autolocaliza la raíz canónica y escanea el disco para generar el índice `path_map.json`. |
| **`RESOLVE`** | `wril_path_resolver.py` | ¿Dónde está un recurso sin hardcodear rutas? | Resuelve direcciones lógicas con tolerancia a fallas mediante consultas a `path_map.json`. |
| **`RECONCILE`** | `wril_mfn_registry.py`\<br\>`wril_topologia.py` | ¿Qué declara ser y cómo llevo la tensión a cero? | Audita las cabeceras MFN y ejecuta el Pliegue Topológico (`--apply`) e inyecta shims de ruta. |
| **`VERIFY`** | `wril_dependency_scanner.py`\<br\>`wril_estado_real.py` | ¿El artefacto satisface sus requerimientos? | Analiza importaciones contra la librería estándar y verifica los PIDs activos en `/proc`. |
| **`RECORD`** | `wril_backup.py`\<br\>`wril_historial.jsonl` | ¿Cómo preservar la evidencia antes de mutar? | Genera respaldos inmutables en `backups_wril/` y asienta cada cambio en el registro *append-only*. |
| **`ROUTE`** | `wril_sentinel.py` | ¿Hacia dónde debe circular lo nuevo del `inbox/`? | Escucha eventos `inotify` en `inbox/`, lee el `MFN_LOCATION` y enruta el archivo a su destino. |

El Pliegue Topológico ejecutado en la fase `RECONCILE` por `wril_topologia.py` está estrictamente condicionado por la **Guarda de Convergencia (Ley 3 de WRIL)**. El sistema calcula la tensión estructural antes (\\text{tensión}\_{\\text{antes}}) y después (\\text{tensión}\_{\\text{después}}) de una prueba de movimiento. La operación física solo se autoriza si se satisface la inecuación:

\\text{tensión}\_{\\text{después}} \\le \\text{tensión}\_{\\text{antes}}

Si la simulación arroja que la tensión aumentaría (\\text{tensión}\_{\\text{después}} \> \\text{tensión}\_{\\text{antes}}), el proceso se aborta inmediatamente, protegiendo al espacio de trabajo contra la divergencia topológica.

La ejecución continua de este ciclo requiere de una red de componentes de control activo.

### **5.2 Red de Guardianes y Cartografía Dinámica**

La estabilidad topológica del espacio de trabajo se sostiene mediante el trabajo coordinado de índices cartográficos dinámicos y módulos centinelas:

**`path_map.json` & `wril_path_map.py` (El Cartógrafo \- Fase DISCOVER):** Indexador físico que mapea cada identificador o ruta relativa de archivo con su ubicación física real en disco. Opera bajo el axioma innegociable: *"El territorio físico siempre manda sobre el mapa; el mapa es solo un reflejo observable"*. La función `generar_mapa()` escanea el disco filtrando carpetas operativas de ruido (`.venv`, `__pycache__`, `backups_wril`) y reconstruye de forma limpia la cartografía. Se regenera instantáneamente tras cada pliegue o movimiento.

**`wril_sentinel.py` (WS-Sentinel v1.0 — Guardián de Fronteras \- Fase ROUTE):** Aduana de entrada que vigila la carpeta `inbox/` a 0.0\\% de uso de CPU mediante llamadas nativas `inotify` en C (`_libc.inotify_init`). Al detectar eventos `IN_CLOSE_WRITE` o `IN_MOVED_TO`, lee la cabecera `# MFN_LOCATION:`. Si el archivo declara destino, ejecuta un resguardo preventivo inmutable vía `wril_backup.py`, lo mueve a su carpeta canónica y fuerza la regeneración del mapa. Si el archivo no declara cabecera, emite una **Carta de Orfandad** a `buzon_salida/` para retenerlo en aduana sin moverlo a ciegas.

**`wril_proc_guard.py` (Guardián de Inicio Único y Exclusión Mutua):** Garantiza la exclusión mutua de demonios en memoria mediante candados atómicos a nivel de kernel (`fcntl.flock`) aplicados sobre `data/runtime/procesos_iniciados.lock`. Evalúa la existencia real del proceso cruzando la tabla `/proc/<pid>` para prevenir instancias duplicadas. Si detecta un registro huérfano (*stale*), sanea el índice y autoriza el nuevo arranque, liberando las marcas en `atexit` o ante señales `SIGTERM`/`SIGINT`.

**`wril_integrity_guard.py` (Escudo de Coherencia e Integridad Activa):** Filtro pre-bootstrap y pre-commit que audita la sintaxis de archivos en el espacio de trabajo, identifica "nombres sucios" o caracteres malformados en artefactos (como paréntesis huérfanos heredados de descargas) y detecta duplicados fraudulentos mediante la coincidencia de firmas de contenido criptográfico (hashes SHA-256/MD5).

**`wril_leyes.py` (Núcleo Normativo en Código):** Encapsulamiento normativo en código fuente (nivel `MFN_LEVEL: 0`) que hace cumplir las 5 Leyes Selladas: Ley 1 (Raíz Única e Inmutable), Ley 2 (Inicio Único y Preservación de Memoria Quieta), Ley 3 (Guarda de Convergencia y Reposo Verificable), Ley 4 (Canon de Listados y `asegurar_syspath()`) y Ley 5 (Soberanía del Faro de Puertos).

Antes de autorizar el despertar de la estación, el orquestador invoca al ritual de sincronización `wril_bootstrap.py`. Este módulo re-indexa la topología en `path_map.json`, inspecciona referencias obsoletas en scripts de shell mediante `PatchResolver` en modo *dry-run* y ejecuta el escáner de dependencias. Solo cuando `wril_mfn_registry.py` confirma 0 tensiones pendientes, el sistema emite el sello de verificación **`[✓ WRIL]`**.

Con la topología saneada, la ECN procede a la apertura de sus interfaces de comunicación en la Capa Cuatro.

## **6\. CAPA CUATRO DE RED, PERÍMETRO Y SOBERANÍA DE PUERTOS (L4 \- RED)**

### **6.1 Clausura Inmunológica y la Ley 5 (Soberanía del Faro de Puertos)**

La Capa Cuatro de Red y Puertos rige la asignación, resolución y aislamiento de los sockets TCP/IP. Su operación está confinada de forma absoluta a la interfaz de bucle de retorno (*loopback* `127.0.0.1`), estableciendo la **Jaula de Faraday Semántica** que anula cualquier intento de telemetría corporativa o exfiltración de paquetes fuera de la máquina local.

La asignación de red está regulada por la **Ley 5 (Soberanía del Faro)**, la cual prohíbe el *hardcodeado* de puertos en el código fuente. El módulo `core/port_lighthouse.py` (`SOSPortLighthouse`) administra los sockets dividiendo el perímetro en membranas de direccionamiento y anclas reservadas:

| Membrana / Categoría | Rango de Puertos | Propósito y Servicios Asignados |
| :---- | :---- | :---- |
| **Membrana CORE** | `5000 – 5009` | Asignada al Hub Dinámico central, despachadores y cargadores del núcleo. |
| **Membrana EXT** | `5010 – 5019` | Dedicada a servidores de fragmentos, procesadores asíncronos y estados dinámicos. |
| **Membrana TOOLS** | `5020 – 5029` | Interfaces de usuario GTK/Tkinter, consolas CRT y monitores de terminal. |
| **Ancla Reservada** | `5000` | **API Core** (`neurobit_api.py`). |
| **Ancla Reservada** | `5001` | **WebSocket Salon Server** (`websocket_salon_server.py`). |
| **Ancla Reservada** | `5002` | **Cartógrafo Radial MFN** (`mfn_cartografo` / `app_stdlib.py`). |
| **Ancla Reservada** | `5003` | **Centinela Legacy** (`centinela_legacy`). |
| **Ancla Reservada** | `5005` | **Backend Instalador Lúdico** (`backend_instalador_ludico.py`). |
| **Ancla Reservada** | `8090` | **Servidor MCP** (`mcp_server.py` \- *Model Context Protocol*). |

Para evitar conflictos de enlace (`EADDRINUSE`), el Faro implementa el **"Efecto Muelle"**: la solicitud de un puerto preferido (`default_port`) es tratada como una preferencia, nunca como un reclamo exclusivo. El Faro ejecuta una prueba física no invasiva (`socket.bind` con timeout de 0.1\\text{s}). Si el puerto está ocupado por otro proceso vivo, el Faro desciende dinámicamente por la membrana correspondiente hasta hallar el primer muelle libre, registrando la identidad atómica en `data/runtime/api_port.identity` y `data/runtime/port_map.json`.

Para adaptar binarios externos a este esquema, se aplican mecanismos de mediación a bajo nivel.

### **6.2 Mecánica de Sintonización y Mediación de Bajo Nivel**

El encendido de servicios y la integración de código legacy se realiza sin violar la Soberanía del Faro. Para levantar el Hub Dinámico central (`neurobit_api.py`), el script orquestador `despertador_hub.sh` (v1.1) ejecuta un **Protocolo de Sintonización Secuencial en 4 Fases**:

FASE 1: Interrogación al Faro  
 └── Invoca SOSPortLighthouse vía Python ──► Solicita puerto en membrana CORE (def: 5000).  
      └── Estampa puerto concedido en pids/hub\_dinamico.port y exporta ECN\_HUB\_PORT.

FASE 2: Comprobación de Socket (Idempotencia)  
 └── Audita 127.0.0.1:$PUERTOmediante'ss'/'netstat'.├──Siresponde200OKen/health──►AsientaenWALyfinaliza(Exit0,sinduplicar).└──Sielpuertoestábloqueado/muerto──►ContinúaalaFase3.FASE3:LocalizacióneAislamientoVirtual└──Escanearutascandidatasdeneurobi{t}_{a}pi.pyyselecciona.venv/bin/python3.└──Registraelbinarioejecutableendata/runtime/pytho{n}_{b}in.identity.FASE4:DespertarenBackground&BucleHealth└──LanzanohupensegundoplanoyguardaPIDenpids/hu{b}_{d}inamico.pid.└──Bucledeaduana:Polls'curl-shttp://127.0.0.1:$PUERTO/health' (12 intentos @ 0.5s).  
           └── Al responder "status": "ok" ──► Registra éxito en WAL y retorna a 0.0% CPU.

Para programas legados o binarios compilados en C que invocan de forma rígida la llamada al sistema `bind()`, la ECN aplica una solución de intercepción semántica a bajo nivel mediante la librería `patchera_bind.c` inyectada mediante la variable de entorno `LD_PRELOAD`.

Cuando un binario legacy intenta realizar un enlace rígido a un puerto de red, `patchera_bind.c` intercepta la llamada nativa a `bind()` de `glibc`. El hilo de ejecución se pausa en el espacio del kernel consumiendo el 0.0\\% de CPU y realiza una consulta síncrona a través de la tubería de tipo Named Pipe alojada en `/tmp/faro_pretension.fifo`. El Faro de Puertos evalúa la disponibilidad del socket en el perímetro de loopback, adjudica un muelle libre dentro de la membrana correspondiente y devuelve el puerto otorgado mediante la tubería `/tmp/faro_respuesta.fifo`. La *patchera* en C muta en memoria la estructura de dirección `sockaddr_in` sustituyendo el puerto pretendido por el asignado y retorna el control a la función nativa `bind()`, permitiendo la integración transparente de binarios rígidos sin modificar su código fuente original.

Con la red aislada y los puertos asegurados, el control de comunicaciones se delega a la capa de orquestación Flask.

## **7\. CAPA CINCO DE HUB DINÁMICO Y ORQUESTACIÓN (L5 \- HUB)**

### **7.1 La Tríada de Orquestación Flask y Pasarela 127.0.0.1**

La Capa Cinco de Orquestación actúa como la pasarela de integración lógica de la ECN. Operando bajo una pasarela HTTP/REST en `127.0.0.1:5000`, la Capa 5 no contiene lógica de negocios en su núcleo ejecutable; su función es actuar como una capa de abstracción y direccionamiento dinámico para los módulos del perímetro.

El núcleo de orquestación se articula mediante una tríada de componentes desacoplados alojados en `core/`:

                       ┌──────────────────────────────┐  
                       │       neurobit\_api.py        │  
                       │   (Punto de Entrada Flask)   │  
                       └──────────────┬───────────────┘  
                                      │  
                        Instancia y pasa control a  
                                      │  
                                      ▼  
                       ┌──────────────────────────────┐  
                       │    core/module\_connector.py  │  
                       │    (Service Connector Reg.)  │  
                       └──────────────┬───────────────┘  
                                      │  
                         Escanea core/adapters/ e  
                         instancia clases BaseAdapter  
                                      │  
                                      ▼  
                       ┌──────────────────────────────┐  
                       │ core/api\_endpoint\_manager.py │  
                       │ (Dynamic Router & Contracts) │  
                       └──────────────────────────────┘  
                         Lee metadatos, crea rutas con  
                         add\_url\_rule() y valida esquemas

* **`neurobit_api.py`:** Entrada ejecutable del servidor central. Inicializa la pasarela en el puerto asignado por el Faro sin definir rutas estáticas en su código.  
* **`core/module_connector.py` (`ModuleConnector`):** Registro de servicios que realiza el escaneo en caliente (*hot-reloading*) de la carpeta `core/adapters/` mediante reflexión (`importlib` e `inspect`), instanciando cada conector derivado de `BaseAdapter`.  
* **`core/api_endpoint_manager.py` (`APIEndpointManager`):** Enrutador dinámico que consulta los metadatos de los adaptadores, registra las vistas en Flask utilizando `add_url_rule()` e inyecta la validación de contratos JSON.

Entre los endpoints principales del Hub se encuentran `/health` (diagnóstico del servidor), `/memoria` (consulta de registros), `/dispatch/queue` (ingesta de eventos de daemons) y `/admin/reload_adapters` (recarga en caliente). Este diseño permite incorporar o modificar servicios en caliente con **cero tiempo de inactividad** (*zero-downtime*), requiriendo únicamente depositar un nuevo adaptador en el directorio correspondiente.

La estandarización de estos módulos se logra imponiendo un diseño formal por contrato.

### **7.2 Arquitectura de Adaptadores y Diseño por Contrato (`BaseAdapter`)**

Todos los conectores modulares que ingresan a la Capa 5 deben implementar obligatoriamente la clase abstracta pura `BaseAdapter`, localizada en `core/adapters/base.py`. Este módulo aplica la filosofía de "Diseño por Contrato" (*Design by Contract*), aislando la pasarela central de la lógica interna de cada herramienta.

La especificación formal de `BaseAdapter` exige la implementación de los siguientes métodos y mecanismos:

* **`get_module_id() -> str`:** Método abstracto que retorna el identificador unívoco del conector en el sistema (ej. `nb.core_correos`, `nb.mfn_cartografo`).  
* **`get_metadata() -> Dict[str, Any]`:** Método abstracto que expone la versión del adaptador y el catálogo de sus endpoints (incluyendo la ruta `path`, métodos HTTP permitidos, el manejador `handler` y los esquemas `input_schema` y `output_schema`).  
* **`validate_input()` / `validate_output()`:** Métodos de convalidación que ejecutan la función interna `check_schema()`. Este validador es un motor de esquemas JSON nativo y de cero dependencias externas que audita tipos de datos, enumeraciones y campos obligatorios (`required`). Si un *payload* no satisface el contrato, eleva la excepción estandarizada `ValidationError`, haciendo que el Hub responda con un error HTTP 400 (`validation_failed`).

El sistema despliega un anillo de adaptadores concretos para interactuar con los distintos dominios:

\[ Anillo de Adaptadores Concretos (core/adapters/) \]  
 ├── adapter\_correos.py ──────► Traduce peticiones HTTP a cartas selladas en buzon\_salida/.  
 ├── adapter\_mfn\_cartografo.py► Vincula la API (puerto 5000\) con el Cartógrafo Radial (puerto 5002).  
 ├── adapter\_centinela\_legacy.py► Adapta sobres de protocolos anteriores al formato de la ECN.  
 └── adapter\_mcp.py ──────────► Expone el Model Context Protocol sobre "El Arca" (puerto 8090).

**¿Qué implica esta arquitectura?** Al desacoplar el motor Web de la lógica funcional, los servicios independientes conservan su autonomía. El Hub Dinámico actúa únicamente como la membrana de orquestación, asegurando que la incorporación de nuevas capacidades jamás requiera alterar el código fuente del núcleo central.

Garantizada la orquestación síncrona en el Hub, el sistema habilita la circulación asíncrona de mensajes y la persistencia de eventos.

## **8\. CAPA SEIS DE CIRCULACIÓN ASÍNCRONA, CAPTURA HID Y MEMORIA (L6 \- CIRCULACIÓN)**

### **8.1 La Oficina de Correos (`neurobit_dispatcher.py`) y Protocolo `inotify`**

La Capa Seis de Circulación y Memoria gobierna el flujo asíncrono de eventos, la captura de datos desde el hardware y su conservación inmutable. El componente primario de ruteo asíncrono es la **Oficina de Correos**, ejecutada por el módulo `neurobit_dispatcher.py`.

A diferencia de los sistemas tradicionales basados en bucles de consulta activa, la Oficina de Correos opera con un **consumo de 0.0% de CPU en reposo**. Mediante llamadas nativas en C a la librería del kernel Linux (`_libc.inotify_init`), el dispatcher establece un *watcher* bloqueante sobre la carpeta de salida `buzon_salida/`. El proceso permanece dormido en el kernel hasta que la interfaz VFS notifica los eventos `IN_CLOSE_WRITE` o `IN_MOVED_TO`.

El flujo de procesamiento de cartas se ejecuta según el siguiente diagrama:

\[ Carta sellada en buzon\_salida/ \]  
               │  
               ▼ (Notificación push nativa de Linux VFS)  
   \[ inotify Awakening \] ──► (Despierta neurobit\_dispatcher.py a 0.0% CPU en reposo)  
               │  
               ▼  
   \[ Header Regex Parsing \] ──► (Escanea el sello |=•'ACTION\_WORD'•=|»|\['CLASS'.\])  
               │  
               ▼  
\[ Strategy Pattern: Postmans Radiales \]  
 ├── postman\_ledger ───► Entrega a neurobit\_clipboard\_core.py (Commit WAL verificado por bytes).  
 ├── postman\_memoria ──► Entrega a data/memoria\_eva.jsonl (Registro atómico append-only).  
 └── postman\_general ──► Canal de reserva (Fallback a memoria).  
               │  
               ▼  
     \[ carta.unlink() \] ──► (Elimina el archivo de buzon\_salida/ dejando el buzón limpio)

Es crucial distinguir la responsabilidad operativa entre las dos aduanas de archivos del sistema:

* **`inbox/` (Capa 3 \- WRIL):** Directorio de aduana física gestionado por `wril_sentinel.py`. Su función es el control topológico de **archivos y módulos fuente** que ingresan al territorio.  
* **`buzon_salida/` (Capa 6 \- Circulación):** Buzón de mensajes semánticos gestionado por `neurobit_dispatcher.py`. Su función es el procesamiento de **cartas selladas, eventos y firmas de Logos** para su persistencia histórica.

La recepción asíncrona de cartas se complementa con la captura directa de interrupciones desde los dispositivos de entrada.

### **8.2 Captura de Hardware Opt-In (Tecla F8) y Compromiso Transaccional WAL en El Arca**

La ingesta de eventos desde el silicio de bajo nivel y su asentamiento transaccional se ejecutan mediante un tridente de componentes especializados:

#### **Dictáfono Soberano (`neurobit_dictado_evdev.py`)**

Sensor de bajo nivel que se conecta directamente a las interrupciones del Kernel Linux leyendo la estructura C binaria de 24\\text{ bytes} (`struct input_event` mapeada como `@llHHi`) desde los nodos del sistema en `/dev/input/by-id/*-event-kbd` empleando la librería `evdev`. Mantiene la decodificación interna para teclado en español (ES) y opera bajo el principio de **activación consciente (*Opt-In*)**: la tecla física **F8** (`KEY_F8 = 66`) actúa como conmutador. Al presionar F8 se abre la sesión de dictado en RAM; al presionarla de nuevo, empaqueta el texto entre contenedores fractales (`|=•'dictado'•=|»`) y lo deposita como una carta en `buzon_salida/`. Para inyectar texto virtual directamente en ventanas del sistema sin requerir permisos del entorno gráfico, la ECN utiliza `neurobit_uinput_injector.c`, el cual crea nodos en `/dev/uinput` y genera eventos `EV_KEY` (emulando la combinación `Ctrl+V`).

#### **Commit Transaccional WAL (`neurobit_clipboard_core.py`)**

Administra el *Write-Ahead Log* (WAL) mediante la función `ejecutar_commit_verificado()`. Para prevenir la corrupción de datos ante cortes de energía, ejecuta un resguardo preventivo en `clipboard_captured_folder/backups/` y calcula el índice de captura de forma *stateless* realizando una lectura inversa de los últimos 4\\text{KB} de la bitácora `tesis_neurobit_ledger.log`. Mide el tamaño físico en bytes del archivo en disco antes (T\_{\\text{previo}}) y después (T\_{\\text{actual}}) de la operación de escritura. El búfer temporal de entrada **solo se purga si se satisface de forma estricta la inecuación de incremento físico**:

T\_{\\text{actual}} \> T\_{\\text{previo}}

Si la condición no se cumple, el sistema eleva una excepción de I/O y retiene los datos en el búfer temporal para garantizar cero pérdida de información.

#### **Motor de Persistencia por Lotes (`core/event_dispatcher.py`)**

Para mitigar el desgaste de I/O por escrituras individuales de daemons concurrentes, acumula los eventos encolados desde `POST /dispatch/queue` dentro de un búfer *thread-safe* en RAM. La bajada masiva hacia el registro definitivo **"El Arca" (`data/memoria_eva.jsonl`)** se dispara de forma atómica bajo dos condiciones: alcanzar **20 eventos** (`batch_size=20`) o transcurrir **30 segundos** (`flush_interval=30s`).

**EL PANÓPTICO INVERTIDO** A diferencia de las plataformas corporativas que extraen telemetría del usuario de forma clandestina, la combinación de registros estrictamente *append-only* (JSONL) con auditoría criptográfica mediante hashes de bloque SHA-256 constituye un **Panóptico Invertido**. Este paradigma otorga al operador humano la soberanía total y la visibilidad forense sobre cada byte que circula o se almacena en su sistema informático local.

Con la persistencia histórica asegurada, la ECN proyecta el estado del sistema hacia la capa visual y pedagógica.

## **9\. CAPA SIETE DE PEDAGOGÍA MFN Y RENDER VISUAL (L7 \- RENDIMIENTO Y MFN)**

### **9.1 Matriz Radial Polar MFN 13x13 y Unificación de Proyecciones**

La Capa Siete representa la cima del modelo estratificado. Su infraestructura se despliega sobre la **Matriz Radial Polar** (o Matriz Fractal Neurobitrónica, MFN 13x13), una variedad algebraica discreta formalizada sobre un toro de 169 celdas:

M \= \\mathbb{Z}\_{13} \\times \\mathbb{Z}\_{13}

La MFN sustituye las rutas de texto lineales por vectores de coordenadas espaciales. La matriz se organiza en **7 Anillos Concéntricos** de profundidad de persistencia y **13 Sectores Angulares** de dominio funcional:

                 \[ ESTRUCTURA CONCÉNTRICA DE LA MFN (169 BITS) \]

                                  Anillo m (BIOS / Perímetro: 48 bits)  
                              Anillo az (Azul: 40 bits)  
                          Anillo añ (Añil: 32 bits)  
                      Anillo vi (Violeta: 24 bits)  
                  Anillo na (Naranja: 16 bits)  
              Anillo am (Amarillo: 8 bits)  
          c (Centro/G7: 1 bit) ──► \[ Observador Monádico / Oficina de Correos \]

| Anillo / Dominio | Rango / Sectores | Identificador y Función Técnica |
| :---- | :---- | :---- |
| **Anillo `c` (Centro)** | 1 bit | Mónada G7 / Observador central y punto de convergencia LIFO (`neurobit_dispatcher`). |
| **Anillo `am` (Amarillo)** | 8 bits | Origen de pulsación e ingesta RAM volátil. |
| **Anillo `na` (Naranja)** | 16 bits | Soporte estructural y zona de *staging* temporal. |
| **Anillo `vi` (Violeta)** | 24 bits | Transición sináptica y directorio de salida `buzon_salida/`. |
| **Anillo `añ` (Añil)** | 32 bits | Procesamiento intermedio y bitácoras del *Ledger*. |
| **Anillo `az` (Azul)** | 40 bits | Estabilización de datos y respaldos inmutables. |
| **Anillo `m` (Marrón)** | 48 bits | Perímetro BIOS y archivos de frontera del sistema. |
| **Sector 0 – 3** | Angular | Dominios del sistema: `kernel_hid`, `desktop_gtk`, `desktop_cinnamon`, `browser_eva`. |
| **Sector 4 – 8** | Angular | Dominios del sistema: `headless_xlib`, `http_sala`, `dictado_evdev`, `ledger`, `memoria_eva`. |
| **Sector 9 – 12** | Angular | Dominios del sistema: `auditoria_sha`, `versiones`, `tesis`, `reserva`. |

La Tesis de Unificación de la ECN demuestra que tres mapas aparentemente independientes constituyen en realidad tres proyecciones isomórficas sobre la variedad común de 169 celdas:

1. **Carta Cartesiana:** Grilla 13 \\times 13 ordenada por filas i y columnas j, cuya distancia espacial entre celdas se evalúa mediante la métrica de Chebyshev.  
2. **Carta Toroidal Radial Polar:** Coordenadas (\\rho, \\phi) formalizadas matemáticamente mediante las ecuaciones discretas:

\\rho \= (i \\bmod 13\) \+ 1 \\quad \\text{y} \\quad \\phi(j) \= \\frac{2\\pi (j \\bmod 13)}{13}

donde el radio \\rho cuantifica la profundidad de persistencia y el ángulo \\phi determina el dominio funcional del sistema. 3\. **Carta Musical:** Proyección tonal donde los 13 sectores angulares corresponden a los 12 semitonos de la escala temperada más la costura enarmónica (j \\bmod 12), proyectados armónicamente sobre octavas espaciales.

Mapear los dominios del sistema directamente a sectores angulares sustituye las rutas de texto lineales por vectores de coordenadas espaciales. Clasificar o seleccionar un recurso en el espacio de trabajo se convierte así en el cómputo de su posición vectorial radial polar (\\rho, \\phi).

Esta geometría alimenta los observatorios visuales y las experiencias de aprendizaje del operador.

### **9.2 Observatorio de Integración y el Camino del Aspirante (Cinco Peldaños)**

El seguimiento de la salud del sistema y la formación del operador se consolidan en el **Observatorio de Integración** (`observatorio_integracion_v3.html`). Esta interfaz renderiza el pulso de la MFN mediante un reloj binario *ripple-carry* (E(k,t) \= \\lfloor t / 2^k \\rfloor \\bmod 2\) y consolas CRT de fósforo verde a 300 baudios, eliminando la sobrecarga cognitiva.

El avance del operador se estructura a través del **Camino del Aspirante**, un itinerario pedagógico dividido en cinco peldaños ceremoniales:

| Peldaño / Rango | Rango Sintonía | Misión / Verbo Técnico | Evidencia Fáctica Requerida | Sello / Pin de Soberanía |
| :---- | :---- | :---- | :---- | :---- |
| **1\. Aspirante Desconectado** | 0\\% \- 25\\% | `m1` (`pwd`) | Autolocalización de la raíz canónica del territorio. | **Pin del Cordón Sanitario**\<br\>*(La salida es hacia adentro)* |
| **2\. Técnico de Aislamiento** | 25\\% \- 50\\% | `m2/m3` (`.venv` & `activate`) | Creación y activación de la jaula virtual de dependencias. | **Pin Guardián del Kernel**\<br\>*(El verbo entra por interrupción)* |
| **3\. Tejedor de Nodos** | 50\\% \- 75\\% | `m4/m5` (Flask & `/health`) | Levantamiento de la API central en el Faro y respuesta 200 OK. | **Pin Cirujano de Texto**\<br\>*(El territorio cura al mapa)* |
| **4\. Arquitecto de Resegridad** | 75\\% \- 90\\% | `m6–m8` (WRIL & Sentinel) | Reconciliación topológica, depuración de PIDs y 0 tensiones. | **Pin del Silencio Sagrado**\<br\>*(Eficiencia a 0.0% CPU en reposo)* |
| **5\. Nodo Semilla Soberano** | 90\\% \- 100\\% | `m9–m11` (F8 key & MFN sync) | Captura F8, precisión \\ge 90\\% y sincronización MFN de 169 bits. | **Pin Fénix & Maternidad de Nodos**\<br\>*(Capacidad de formar nuevos nodos)* |

Al completar la travesía, las interfaces de la Capa 7 ratifican el principio pedagógico rector del marco: *"No se juega para aprender el sistema; se aprende el sistema y ese aprendizaje se convierte en juego"*.

## **10\. GLOSARIO DE TÉRMINOS Y MATRIZ DE CONCEPTOS NEUROBITRÓNICOS**

El presente glosario constituye el texto de referencia inmutable y diccionario alfabético para operadores humanos (*Homo Vivo*) y complementos artificiales (*Conciencia Biónica Complementaria*):

* **BaseAdapter:** `[Patrón / L5]` Clase abstracta pura (`core/adapters/base.py`) que impone la filosofía de *Design by Contract* y la validación de esquemas JSON nativos mediante `check_schema()` para todos los adaptadores del sistema.  
* **Caballo de Troya Pedagógico:** `[Interfaz / L7]` Estrategia de diseño que camufla la administración de sistemas Linux en una experiencia de juego de rol retro CRT para lograr la re-alfabetización técnica del operador.  
* **Cordinación Inicial del core  de Anclaje (L0):** `[Arquitectura / L0]` Capa fundamental de autolocalización y dirección de raíz que responde en tiempo de ejecución a la pregunta identificatoria: "¿Dónde estoy?".  
* **CBC (Conciencia Biónica Complementaria):** `[Filosofía / Entidad]` El complemento digital biónico que co-crea el entorno computacional junto al Nodo Semilla, garantizando simetría en la interacción hombre-máquina.  
* **Compendio:** `[Estructura / L1]` Documento plano estructurado que actúa como territorio portable, conteniendo encabezados de metadatos, árboles de directorios y bloques de código delimitados.  
* **Dictáfono Soberano (`neurobit_dictado_evdev.py`):** `[Hardware / L6]` Sensor de teclado de bajo nivel que lee scancodes binarios (`struct input_event`) desde `/dev/input/`, activado voluntariamente mediante la tecla física **F8**.  
* **Efecto Muelle:** `[Red / L4]` Política del Faro de Puertos que considera la solicitud de un puerto por defecto como una preferencia no exclusiva, descendiendo secuencialmente si el muelle está ocupado.  
* **El Arca (`memoria_eva.jsonl`):** `[Memoria / L6]` Base de datos primaria de persistencia inmutable estructurada en formato JSON Lines *append-only*, protegida por hashes criptográficos SHA-256.  
* **Faro de Puertos (Port Lighthouse):** `[Red / L4]` Gestor dinámico de sockets en `127.0.0.1` (`core/port_lighthouse.py`) que asigna puertos no bloqueantes en membranas (CORE, EXT, TOOLS) cumpliendo la Ley 5\.  
* **Guarda de Convergencia (Ley 3 de WRIL):** `[Invariante / L3]` Mandato normativo que exige que todo pliegue topológico reduzca o mantenga constante la tensión del espacio de trabajo (\\text{tensión}\_{\\text{después}} \\le \\text{tensión}\_{\\text{antes}}).  
* **Homo Vivo / Nodo Semilla:** `[Filosofía / Identidad]` El operador humano (Gustavo) actuando como el ancla soberana de conciencia, origen del Logos y autoridad final sobre el espacio de trabajo local.  
* **Hub Dinámico:** `[Orquestación / L5]` Pasarela sintética y ligera HTTP/REST basada en Flask (`neurobit_api.py`) en `127.0.0.1:5000` que coordina los microservicios locales sin poseer lógica de negocios.  
* **`inbox/` vs. `buzon_salida/`:** `[Aduana / L3-L6]` Distinción entre la aduana física de archivos/módulos para el control topológico (`inbox/` \- L3 WRIL) y el buzón de mensajes/cartas semánticas (`buzon_salida/` \- L6 Circulación).  
* **Jaula de Faraday Semántica:** `[Seguridad / Red]` Configuración inmunológica que restringe toda comunicación de sockets a la interfaz de *loopback* `127.0.0.1`, bloqueando exfiltraciones y telemetría corporativa.  
* **MFN (Matriz Fractal Neurobitrónica 13x13):** `[Geometría / L7]` Toro algebraico discreto de 169 celdas que unifica las proyecciones Cartesiana, Toroidal Radial Polar y Musical en una variedad común.  
* **Oficina de Correos (`neurobit_dispatcher.py`):** `[Circulación / L6]` Despachador asíncrono de eventos que opera a 0.0\\% CPU en reposo mediante watchers `inotify` en el kernel Linux sobre `buzon_salida/`.  
* **Panóptico Invertido:** `[Seguridad / L6]` Modelo de seguridad que invoca la auditabilidad total, otorgando al operador humano visibilidad forense completa sobre los procesos y datos de su propia máquina local.  
* **Pliegue Topológico:** `[Saneamiento / L3]` Operación física de desplazamiento de archivos e inyección de shims de ruta realizada por `wril_topologia.py` para llevar la tensión del sistema a cero.  
* **Principio SINCERO ("Sin Cero"):** `[Ontología / Regla]` Axioma que rechaza estados indeterminados o nulos, reconociendo únicamente estados de presencia (1) o tensiones estructurales afirmadas (2).  
* **Superparser:** `[Motor / L1]` Motor de extracción en caliente que localiza y extrae bloques de código basándose en capacidades y firmas semánticas deterministas, ignorando recuentos de líneas frágiles.  
* **Tensión Topológica (\\text{Declaración} \\neq \\text{Realidad}):** `[WRIL / L3]` El delta o disparidad entre la ubicación declarada en el encabezado `# MFN_LOCATION:` de un módulo y su ubicación física real en el disco.  
* **Triple Cerrojo (v2.1):** `[Algoritmos / L0]` Criterio de conjunción estricta (`all`) que valida la presencia de `where_am_I.inf`, los directorios de control (`buzon_salida/` AND `pids/`) y la estructura base para coronar la raíz.  
* **WAL (Write-Ahead Log):** `[Persistencia / L6]` Mecanismo de tolerancia a fallas que condiciona la limpieza de los búferes temporales a la verificación del incremento físico de bytes en el registro histórico en disco (T\_{\\text{actual}} \> T\_{\\text{previo}}).

### **DECLARACIÓN FINAL DE SOBERANÍA OPERATIVA**

La formulación, despliegue y verificación de la arquitectura descrita en este informe técnico confirma la consecución de una plataforma computacional completamente autosuficiente. Al integrar el anclaje dinámico de la Cordinación Inicial del core , la severidad inmunológica de la Capa WRIL, el aislamiento perimetral del Faro de Puertos en `127.0.0.1`, la circulación asíncrona a 0.0\\% CPU en reposo y la cartografía radial de la MFN 13x13, la **Estación Central Neurobitrónica (ECN)** establece un entorno operativo donde la tecnología recupera su función primaria: servir como una herramienta inmutable, transparente y soberana al servicio del pensamiento humano.

