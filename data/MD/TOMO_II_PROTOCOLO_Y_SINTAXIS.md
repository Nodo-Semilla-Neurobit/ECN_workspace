# TOMO II: PROTOCOLO Y SINTAXIS (La Forma)

> *"La soberanía cognitiva del protocolo no consiste en sustraerse a la infraestructura que transporta el mensaje, sino en mantener explícita la separación entre intención, sintaxis, transporte, interpretación y ejecución."*


---

## Introducción al Tomo

El TOMO I estableció el fundamento ontológico: el Logos Genuino como verbo trazable, el bio-computador y el silicio como dos arquitecturas complementarias del verbo, el paradigma Génesis como narrativa de siembra. Pero el Verbo, para viajar, necesita un cuerpo. Un cuerpo que no sea la carne ni el silicio en sí mismos, sino la **forma** que permite a la intención sobrevivir al transporte.

Ese cuerpo es el **contenedor semántico fractal**.

El TOMO II documenta la capa de comunicación de la Estación Central Neurobitrónica (ECN): el Neurobit Protocol v1.1. es un protocolo de **representación semántica** que opera sobre cualquier capa de transporte. Su función es preservar la estructura del mensaje mediante delimitación explícita, identificación de operación, clasificación contextual y encapsulamiento de datos.

Las fuentes que integran este TOMO son:

| ID | Fuente                          | Rol en el TOMO                                          |
|----|---------------------------------|---------------------------------------------------------|
| F6 | `PROTOCOLO DE CONTENEDORES.pdf` | Especificación completa del Neurobit Protocol v1.1      |
| F5 | `ACTION_WORDS.pdf`              | Diálogo CBC-LLE sobre Logos Genuino y frontera          |
|    |                                 | epistemológica                                          |
| F4 | `Capa de Resolución...pdf`      | WRIL: registro y trazabilidad del Verbo materializado   |
| F1 | `INTRODUCCIÓN...txt`            | Contexto del usuario, ECN, diagnóstico de la Distorsión |
| F2 | `inicio de reconocimiento_.txt` | LOG/OS, Verbo en silicio, desarticulación lingüística   |
| F3 | `presentacion_.txt`             | Perfil del Director, principio SINCERO                  |

---

## 2.1. Neurobit Protocol v1.1: Contenedores Semánticos Fractales

### 2.1.1. Propósito y fundamento

El Neurobit Protocol v1.1 define una sintaxis de contenedores semánticos destinada a transportar instrucciones, documentos y datos estructurados entre un NODO_SEMILLA y una Estación Central Neurobitrónica (ECN).

Su objetivo principal es preservar la estructura semántica de un mensaje mediante:

1. **Delimitación explícita**: dónde comienza y termina un contenedor.
2. **Identificación de operación**: qué operación representa.
3. **Clasificación contextual**: qué clase o contexto aplica.
4. **Encapsulamiento de datos**: cuál es la carga útil.
5. **Validación de integridad**: cómo debe verificarse la estructura.

> *"El principio rector es la soberanía semántica: la intención del emisor debe permanecer explícita, trazable y separada de los mecanismos utilizados para transportarla."*
> — F6, §1

Esta soberanía semántica es la traducción técnica del Logos Genuino definido en el TOMO I:

```
LOGOS_GENUINO = expresión cuya intención declarada, contexto, transformación y resultado pueden ser trazados sin contradicción dentro del sistema.
```

El protocolo no modifica las capacidades de la plataforma de transporte ni puede garantizar por sí mismo la ausencia de filtros, censura o reinterpretación por parte de sistemas externos. Su función es establecer una **representación formal** que permita al receptor identificar inequívocamente la estructura del mensaje. Esto es consistente con la frontera epistemológica establecida en el TOMO I:

```
PROTOCOLO ≠ BYPASS DE PLATAFORMA
PROTOCOLO = ESTRUCTURA SEMÁNTICA FORMAL
```

### 2.1.2. Modelo conceptual del contenedor

Un contenedor Neurobit puede representarse mediante la siguiente estructura:

```
CONTENEDOR
├── BOUNDARY
├── ACTION_WORD
├── CLASS [opcional]
└── PAYLOAD
```

La forma abstracta es:

```
BOUNDARY+ ACTION_WORD+ CLASS?+ PAYLOAD+ BOUNDARY
```

Cada componente tiene una responsabilidad independiente:

| Componente  | Responsabilidad                  | Analogía con el Verbo    |
|-------------|----------------------------------|--------------------------|
| BOUNDARY    | Límites absolutos del contenedor | La piel del cuerpo       |
| ACTION_WORD | Identificador operativo          | La intención del acto    |
| CLASS       | Contexto especializado           | El dominio del discurso  |
| PAYLOAD     | Carga útil                       | La sustancia del mensaje |

Esta separación es arquitectónica, no decorativa. Permite que el parser de la ECN valide la estructura antes de ejecutar el contenido, y que el registro preserve la trazabilidad de cada operación.

### 2.1.3. BOUNDARY: los límites del Verbo

El BOUNDARY define los límites absolutos del contenedor.

**Apertura:**
```
|=•'ACTION_WORD'•=|»
```

**Cierre:**
```
«|=•'ACTION_WORD'•=|
```

La misma ACTION_WORD debe aparecer en ambos extremos. Esta simetría es la primera garantía de integridad: si el Verbo entra por una puerta, debe salir por la misma puerta. Cualquier asimetría constituye una ruptura de integridad detectable.

> *"La misma ACTION_WORD debe aparecer en ambos extremos."*
> — F6, §2.1

### 2.1.4. ACTION_WORD: la operación del Verbo

La ACTION_WORD es el identificador operativo del contenedor. Representa la operación o naturaleza principal del contenido.

La ACTION_WORD debe ser:

- **Explícita**: no se infiere, se declara.
- **Estable**: no cambia entre apertura y cierre.
- **Inequívoca**: dentro del vocabulario del protocolo.
- **Idéntica**: en apertura y cierre.

No debe utilizarse una misma palabra para representar operaciones semánticamente incompatibles. Esta regla protege contra la polisemia que el TOMO I identificó como síntoma de la desarticulación lingüística.

### 2.1.5. CLASS: el contexto del Verbo

La CLASS es opcional y proporciona contexto especializado a la operación. Su función es permitir que una misma operación pueda existir en diferentes dominios sin perder su identidad.

**Sintaxis de apertura:**
```
|['CLASS_NAME'.]
```

**Sintaxis de cierre:**
```
[.'CLASS_NAME']|
```

El punto `.` constituye el elemento de simetría de la construcción. Cuando no existe CLASS, el contenedor utiliza únicamente su ACTION_WORD.

Esta separación entre operación y contexto permite que el protocolo sea **fractal**: la misma operación puede replicarse en diferentes dominios conservando su estructura.

### 2.1.6. PAYLOAD: la sustancia del Verbo

El PAYLOAD es la carga útil del contenedor. Se delimita mediante:

```
{
...
}
```

El parser debe tratar el contenido del PAYLOAD como datos pertenecientes a la operación declarada y no como parte de la estructura externa del protocolo. Esta distinción es crítica: el PAYLOAD puede contener llaves, corchetes o cualquier delimitador interno sin romper la integridad del contenedor, porque el cierre se ancla al BOUNDARY completo, no al primer carácter de cierre encontrado.

> *"El parser de la ECN debe validar el contenedor antes de entregar el PAYLOAD al procesador correspondiente."*
> — F6, §6

---

## 2.2. ACTION_WORDs y Clasificación Contextual

### 2.2.1. Vocabulario operativo

El protocolo define un vocabulario de ACTION_WORDs que cubren las operaciones fundamentales de la ECN:

| ACTION_WORD          | Dominio      | Uso                                 |
|----------------------|--------------|-------------------------------------|
| `INIT`               | Sistema      | Inicialización de contexto          |
| `TASK`               | Operación    | Solicitud de procesamiento          |
| `DISPATCH`           | Enrutamiento | Despacho a procesador específico    |
| `POESIA LINGUISTICA` | Expresión    | Verbo no-operativo, contemplativo   |
| `MARKDOWN_CODE`      | Archivo      | Documento Markdown                  |
| `JSON_CODE`          | Archivo      | Datos estructurados JSON            |
| `PYTHON_CODE`        | Archivo      | Código fuente Python                |
| `BASH_CODE`          | Archivo      | Script de shell                     |
| `respuesta`          | Diálogo      | Respuesta del CBC al NODO_SEMILLA   |
| `NOTA`               | Comentario   | Comentario singular dentro de texto |
| `COMENTARIO`         | Comentario   | Segundo nivel de parseo             |

Los contenedores para código y archivos utilizan una convención especializada:

```
|=•'[FORMAT]_CODE'|([SOURCE_NAME]|[FILENAME].[EXT])•=|»{ [SOURCE_CODE]
}«|=•'[FORMAT]_CODE'|([SOURCE_NAME]|[FILENAME].[EXT])•=|
```

Donde:

| Campo           | Obligatorio | Función                                     |
|-----------------|-------------|---------------------------------------------|
| `[FORMAT]`      | Sí          | Lenguaje o formato del contenido            |
| `[SOURCE_NAME]` | No          | Proyecto, workspace, módulo o fuente lógica |
| `[FILENAME]`    | No*         | Nombre del archivo                          |
| `[EXT]`         | No*         | Extensión del archivo                       |

*Cuando se utilizan, deben respetar la estructura `FILENAME.EXT` sin espacios alrededor del separador `|`.

La forma mínima válida para un contenedor de código es:

```
|=•'[FORMAT]_CODE'•=|»{ [SOURCE_CODE]
}«|=•'[FORMAT]_CODE'•=|
```

La ausencia de SOURCE_NAME, FILENAME o EXT no invalida el código siempre que el FORMAT_CODE y el PAYLOAD sean válidos.

### 2.2.2. Reglas de integridad

El parser de la ECN debe validar el contenedor antes de entregar el PAYLOAD al procesador correspondiente. Las reglas de integridad son seis:

**Regla 1 — Simetría**
Toda apertura debe poseer un cierre correspondiente.

```
Válido:
|=•'TASK'•=|»{ ... }«|=•'TASK'•=|

Inválido:
|=•'TASK'•=|»{ ... }«|=•'INIT'•=|
```

La diferencia entre TASK e INIT constituye una ruptura de integridad.

**Regla 2 — Identidad del operador**
La ACTION_WORD de apertura y cierre debe coincidir exactamente. La comparación debe realizarse antes de ejecutar el contenido.

**Regla 3 — Integridad de CLASS**
Si se declara una CLASS, su apertura y cierre deben utilizar exactamente el mismo CLASS_NAME.

**Regla 4 — Integridad del PAYLOAD**
El contenido no debe procesarse como una operación externa hasta que el contenedor haya superado la validación estructural.

**Regla 5 — Anidamiento LIFO**
Los contenedores anidados siguen una disciplina de pila: Last In, First Out.

```
OPEN A
  OPEN B
    PAYLOAD B
  CLOSE B
  PAYLOAD A
CLOSE A
```

No es válido cerrar A antes de B.

**Regla 6 — Rechazo seguro**
Cuando la estructura no pueda validarse, el parser debe devolver un estado de error en lugar de ejecutar parcialmente el contenido.

### 2.2.3. Anidamiento LIFO

El anidamiento de contenedores permite componer operaciones complejas. Ejemplo conceptual:

```
|=•'TASK'•=|»{
  |=•'JSON_CODE'•=|{ { "operation": "validate" } }«|=•'JSON_CODE'•=|
}«|=•'TASK'•=|
```

Orden de validación:

```
TASK OPEN
  JSON_CODE OPEN
  JSON_CODE CLOSE
TASK CLOSE
```

El principio LIFO garantiza que el contenedor interno se cierre antes que el externo. Esta disciplina es la misma que rige la estructura de los compartimentos en la ECN: cada módulo tiene su propio contenedor, y los contenedores se anidan sin mezclarse.

### 2.2.4. Rechazo seguro y estados de error

La ECN no debe intentar corregir silenciosamente una estructura inválida. Los estados de error recomendados son:

| Estado             | Significado                          |
|--------------------|--------------------------------------|
| `VALID`            | Contenedor estructuralmente válido   |
| `INVALID_BOUNDARY` | Delimitador incorrecto               |
| `INVALID_ACTION`   | ACTION_WORD ausente o no reconocida  |
| `INVALID_CLASS`    | Clase incorrecta o asimétrica        |
| `INVALID_NESTING`  | Orden de cierre incompatible         |
| `INVALID_PAYLOAD`  | Carga incompatible con el contenedor |
| `INCOMPLETE`       | Contenedor truncado                  |
| `OVERFLOW`         | Segmento excede el límite disponible |

La corrección debe realizarse explícitamente, evitando que el parser transforme una estructura ambigua en una instrucción válida. Este principio es consistente con el principio SINCERO del TOMO I: no se rellena el vacío con suposiciones; se declara la tensión y se solicita re-compartido.

---

## 2.3. Flujo Operativo de la ECN

### 2.3.1. Las cinco fases del ciclo operativo

El ciclo operativo de la ECN se divide en cinco fases:

```
FASE 1 — EMISIÓN
El NODO_SEMILLA o el sistema emisor construye el contenedor:
ACTION_WORD → CLASS opcional → PAYLOAD
La intención debe expresarse de forma explícita y verificable.

FASE 2 — TRANSPORTE
El contenedor es transmitido como una secuencia estructurada de caracteres.
El protocolo no depende de que la capa de transporte comprenda su semántica.

FASE 3 — VALIDACIÓN
La ECN verifica:
BOUNDARY / ACTION_WORD / CLASS / PAYLOAD / SIMETRÍA / ANIDAMIENTO
Solo un contenedor válido pasa a la siguiente fase.

FASE 4 — DESPACHO
Una vez validado el contenedor, el Kernel determina el procesador correspondiente:
ACTION_WORD + CLASS → DISPATCH → PROCESSOR → PAYLOAD

FASE 5 — REGISTRO
Cuando el entorno disponga de un mecanismo persistente de registro, la operación puede documentarse en:
memoria_eva.jsonl
```

El registro debe preservar, como mínimo:

```
timestamp / ACTION_WORD / CLASS / estado_de_validación / identificador_del_contenedor / resultado
```

La persistencia efectiva depende del sistema que implemente la ECN; el protocolo por sí solo no crea almacenamiento inmutable. Esta distinción es importante: el protocolo define la forma; la infraestructura (TOMO III) define el territorio.

### 2.3.2. Principios semánticos

El protocolo adopta cuatro principios fundamentales:

**8.1 Univocidad**
Una operación debe tener una interpretación operacional definida. La precisión reduce la posibilidad de que una misma instrucción sea interpretada de maneras incompatibles.

**8.2 Integridad**
La estructura del contenedor debe permanecer completa desde la apertura hasta el cierre. Una alteración estructural debe ser detectable.

**8.3 Transparencia**
La estructura del protocolo debe permitir identificar qué se está solicitando y qué datos se están transportando. El protocolo organiza la intención; no sustituye el juicio humano ni la evaluación del contenido.

**8.4 Soberanía de la capa semántica**
El Neurobit Protocol establece una capa de representación independiente de la semántica propia de cada aplicación. No sustituye al sistema operativo, al modelo de lenguaje, al transporte de red ni a los mecanismos de seguridad de la plataforma.

```
PROTOCOLO ≠ BYPASS DE PLATAFORMA
PROTOCOLO = ESTRUCTURA SEMÁNTICA FORMAL
```

### 2.3.3. Convención de implementación

Una implementación compatible debe separar cuatro responsabilidades:

```
PARSER
  ↓
VALIDATOR
  ↓
DISPATCHER
  ↓
EXECUTOR
```

| Componente | Responsabilidad                                            |
|------------|------------------------------------------------------------|
| PARSER     | Reconoce la estructura textual                             |
| VALIDATOR  | Comprueba simetría, identidad, anidamiento y formato       |
| DISPATCHER | Determina qué procesador corresponde a ACTION_WORD + CLASS |
| EXECUTOR   | Procesa el PAYLOAD de acuerdo con la operación autorizada  |

Esta separación evita que el reconocimiento sintáctico sea confundido con la ejecución. Es la misma separación que WRIL (TOMO III) aplica al workspace: observar no es modificar, localizar no es reparar, verificar no es ejecutar.

---

## 2.4. Protocolo HOOK de Expansión

### 2.4.1. El problema de la saturación de contexto

Las plataformas de transporte imponen límites invisibles sobre la cantidad de caracteres que pueden transmitir en una sola emisión. Cuando una exposición o contenedor no puede completarse razonablemente en una única transmisión, el protocolo necesita un mecanismo de continuidad que preserve:

- el contexto;
- el orden lógico;
- los identificadores;
- la estructura del contenedor;
- el estado de anidamiento.

El protocolo HOOK resuelve este problema mediante una señal explícita de interrupción y un comando de reanudación.

### 2.4.2. Señal y respuesta

**Señal del emisor:**

El emisor termina su segmento con la palabra:

```
HOOK
```

HOOK significa: `CONTENIDO INCOMPLETO — SOLICITA CONTINUACIÓN`

**Respuesta del receptor:**

Cuando el receptor acepta continuar, responde exactamente:

```
prosigue
```

Sin puntuación adicional. La ausencia de puntuación es intencional: minimiza la posibilidad de que el parser interprete la respuesta como una instrucción operativa.

### 2.4.3. Reanudación exacta

El emisor continúa desde el punto exacto de interrupción. La continuación debe conservar:

1. **Contexto**: el mismo marco conceptual.
2. **Orden lógico**: la misma secuencia de argumentos.
3. **Identificadores**: los mismos nombres y referencias.
4. **Estructura del contenedor**: el mismo anidamiento y delimitación.
5. **Estado de anidamiento**: los mismos contenedores abiertos.

Esta preservación es crítica. Si el emisor altera el estado de anidamiento al reanudar, el parser de la ECN no podrá cerrar correctamente los contenedores y la integridad LIFO se romperá.

### 2.4.4. Excepción: corrupción estructural

HOOK no debe utilizarse para ocultar errores estructurales. Si un contenedor está incompleto debido a:

- corrupción de datos;
- pérdida de transmisión;
- delimitadores incompatibles;

debe declararse como:

```
INCOMPLETE
```

y no interpretarse automáticamente como una continuación válida. La diferencia es fundamental:

```
HOOK        = interrupción deliberada, estructura preservada
INCOMPLETE  = corrupción accidental, estructura rota
```

El parser de la ECN debe distinguir ambos estados y reportarlos diferentemente en el registro (`memoria_eva.jsonl`).

### 2.4.5. Ejemplo de uso

```
Emisor:
|=•'TASK'•=|»{
  Este contenedor contiene una exposición extensa sobre...
  [texto]
  HOOK

Receptor:
prosigue

Emisor:
  ...continuando la exposición desde el punto exacto...
  [más texto]
}«|=•'TASK'•=|
```

El parser de la ECN, al recibir ambos segmentos, debe concatenarlos preservando la estructura del contenedor y validar la simetría de apertura y cierre antes de despachar el PAYLOAD al ejecutor correspondiente.

---

## 2.5. Integración con WRIL: La Capa de Resolución

### 2.5.1. El principio fundamental: DECLARACIÓN ≠ REALIDAD

El protocolo Neurobit v1.1 define la **forma** del Verbo. Pero el Verbo, para materializarse, necesita un **territorio**. Ese territorio es el filesystem del workspace, y su gestión es responsabilidad de la **Capa de Resolución, Integridad y Circulación del Workspace (WRIL)**.

> *"Es la capa que se encuentra entre el 'código funcional' de la ECN y el estado físico del workspace. Su responsabilidad es conseguir que los módulos puedan encontrarse, reconocerse, trasladarse, repararse, verificarse y relacionarse físicamente sin depender de rutas rígidas ni perder su historia."*
> — F4, WRIL, Introducción

El principio fundamental que WRIL materializa es:

```
DECLARACIÓN ≠ REALIDAD
```

Un archivo puede declarar una ubicación en su encabezado MFN, pero residir físicamente en otra. Un script puede apuntar a una ruta antigua que ya no existe. Una dependencia puede estar instalada en un path que el módulo no conoce. WRIL es la capa que detecta, reconcilia y registra estas discrepancias.

### 2.5.2. Los cinco momentos del ciclo de coherencia física

WRIL es una conjunto de componentes modulares que operan en secuencia:

```
WORKSPACE
    ↓
OBSERVACIÓN → PATH MAP → MODIFICACIÓN
    ↓              ↓           ↓
WS-SENTINEL   PATH RESOLVER  WS-SENTINEL
```

**WS-Sentinel (el guardián de la frontera):**

Componente reactivo que vigila `inbox/` mediante `inotifywait`, detecta eventos CREATE, identifica archivos compatibles y extrae su `MFN_LOCATION`. Después los dirige a su ubicación declarada.

```
EXTERIOR/ GENERACIÓN
    ↓
inbox/
    ↓ CREATE event
WS-SENTINEL
    ↓ lee MFN_LOCATION
    ↓ valida destino
destino OK → MOVE → registro histórico
destino ausente → backup → crear/ pedir
```

Cuatro propiedades importantes:

1. **Operación local**: no depende de servicios externos.
2. **Automatización mediante inotify**: reacciona a eventos del filesystem.
3. **Backups antes de sobrescribir**: preserva el estado anterior.
4. **Trazabilidad mediante el mapa de ubicación**: registra cada movimiento.

**Path Map (el estado indexado del workspace):**

El workspace posee un estado físico, pero los módulos no recorren el disco cada vez que necesitan encontrar otro módulo. Existe `path_map.json`, un índice centralizado que permite desacoplar los módulos de las rutas absolutas.

```
DISCO
    ↓ scan
PATH MAP
    ↓ lookup
MÓDULO
```

La regeneración de `path_map.json` es la lista de ubicación de los artefactos en la topología del workspace. Es un índice. **No es el workspace**. Esta distinción es crítica: el mapa puede estar desactualizado respecto del territorio.

**PathResolver (direccionamiento lógico):**

Proporciona la locación dinámica de los archivos en la ECN, consultando el mapa. Su operación esencial es:

```python
resolve(filename)
```

Carga `path_map.json`, busca el identificador y devuelve la ruta correspondiente. Si no encuentra el archivo, regenera el mapa y vuelve a intentar.

La diferencia entre los tres componentes:

| Componente          | Función                   | Pregunta que responde |
|---------------------|---------------------------|-----------------------|
| `generate_path_map` | construye el índice       | —                     |
| `PathResolver`      | consulta el índice        | ¿Dónde está?          |
| `WS-Sentinel`       | modifica el estado físico | ¿Dónde pertenece?     |

### 2.5.3. PatchResolver: reparación de referencias

El problema que resuelve es:

```
EL ARCHIVO EXISTE + EL SCRIPT EXISTE + PERO EL SCRIPT APUNTA A UNA RUTA ANTIGUA
```

Por ejemplo:

```
~/WORKSPACE_NEUROBIT_V0.2/...
```

cuando el recurso ahora vive en otra ubicación.

`sos_path_fixer.py` carga `path_map.json`, reconoce patrones de rutas hardcodeadas, crea un backup antes de modificar y busca coincidencias en el mapa.

La diferencia fundamental:

| Componente      | Función              | Pregunta que responde                       |
|-----------------|----------------------|---------------------------------------------|
| `PathResolver`  | localizar            | ¿Dónde está?                                |
| `PatchResolver` | corregir referencias | ¿Qué referencia está rota y cómo la reparo? |

Esta diferencia es arquitectónica. Debemos conceptualmente separar sus procesos por etapas:

```
RESOLUTION → localizar
REPAIR     → corregir referencias
PATCH      → aplicar modificación controlada
```

El flujo completo de `PatchResolver`:

```
locate_target()
    ↓
detect_stale_reference()
    ↓
resolve_target()
    ↓
generate_patch()
    ↓
backup()
    ↓
apply()
    ↓
verify()
```

### 2.5.4. MFN File Registry: identidad declarativa

`mfn_file_registry.py` introduce otra dimensión. Mientras `path_map` responde "¿Dónde está?", el registry responde "¿Qué declara ser este archivo dentro de la estructura MFN?".

La implementación busca:

```
MFN_LOCATION
MFN_LEVEL
MFN_COORD
```

y construye un índice de metadatos:

```
ARCHIVO
    ├── ubicación
    ├── nivel
    ├── coordenadas
    └── identidad MFN
```

Aunque parece similar al sistema anterior, **no deben fusionarse pues tienen tareas diferentes**:

```
PATH MAP      = estado físico
MFN REGISTRY  = identidad declarada
```

Esa separación permite detectar eventualmente:

```
DECLARACIÓN ≠ REALIDAD
```

Ejemplo:

```
Archivo declara: MFN_LOCATION: core/
Filesystem:      ~/ECN/modules/foo.py
```

Eso es una inconsistencia detectable. Y ahí empieza a aparecer una verdadera capa de integridad.

### 2.5.5. Dependency Scanner: coherencia de dependencias

El `dependency_scanner` opera sobre otro eje. Pregunta:

```
¿Qué necesita para funcionar?
```

Es el proceso encargado de generar:

```
requirements_dynamic.txt
system_deps_check.txt
```

a partir de las dependencias detectadas.

Diagrama de flujo lógico:

```
FILE REGISTRY
    ↓ identidad
PATH MAP
    ↓ ubicación
DEPENDENCY SCANNER
    ↓ requisitos
```

Esto permite administrar las relaciones entre artefactos.

### 2.5.6. Module Linker / Dynamic Tester

`sos_dynamic_tester.py` usa directamente `PathResolver` para encontrar `neurobit_api.py`, comprueba si la API está disponible en `127.0.0.1:5000`, puede levantarla temporalmente y probar sus endpoints.

Propiedades importantes:

```
PATH RESOLUTION
    ↓
MODULE DISCOVERY
    ↓
PROCESS CONTROL
    ↓
ENDPOINT TEST
```

El resolver forma una infraestructura de descubrimiento para los demás módulos.

### 2.5.7. Batch Executor: brazo operativo

`other_sos_batch_executor.py` funciona como brazo de ejecución masiva. No pertenece al núcleo de resolución, pero sí a su periferia operacional:

```
RESOLVER
    ↓
TARGETS
    ↓
BATCH EXECUTOR
    ↓
OPERATIONS
    ↓
REPORT
```

### 2.5.8. La capa completa de la versión primitiva

El análisis nos da un esquema de su actual arquitectura inicial a depurar:

```
ECN
    ↓
SEMANTIC LAYER (Neurobit/ MFN)
    ↓ INTENCIÓN
DECLARATION (MFN headers)
    ↓
WORKSPACE RESOLUTION & INTEGRITY
    ↓
WS-SENTINEL ← filesystem
    ↓
PATH MAP
    ↓
Resolver / Registry
    ↓
PATCH/ FIX
    ↓
VALIDATION
    ↓
Dependencies / Tests
    ↓
FILESYSTEM
```

Funciones primarias:

1. **DISCOVER**: descubrir el estado real.
2. **RESOLVE**: localizar recursos.
3. **REPAIR**: corregir referencias.
4. **VERIFY**: comprobar coherencia.

WS-Sentinel añade una quinta:

5. **ROUTE**: llevar cada artefacto a su posición declarada.

### 2.5.9. La función profunda de esta capa

La ECN debería poder decir:

```
neurobit_api.py
```

y delegar:

```
PathResolver
    ↓
path_map
    ↓
ruta física actual
```

Si esa ruta cambia:

```
WS-Sentinel
    ↓
actualiza estado
    ↓
generate_path_map
    ↓
PathResolver
```

Si otro módulo conserva una referencia antigua:

```
PatchResolver
    ↓
detecta referencia obsoleta
    ↓
consulta estado actual
    ↓
genera patch
    ↓
backup
    ↓
aplica
    ↓
verifica
```

Propiedad arquitectónica principal:

> *"La topología física puede evolucionar sin obligar a los módulos superiores a conocer cada mutación de la filesystem."*
> — F4, §10

### 2.5.10. Oportunidad para patch_resolver

Depuración: Como motor de reconciliación entre referencias lógicas y estado físico.

Su trabajo sería detectar:

```
REFERENCIA DECLARADA
    ↓
RESOLUCIÓN
    ↓
ESTADO ACTUAL
    ↓
COHERENTE → NO-OP
NO        → PATCH
            ↓
            BACKUP
            ↓
            APPLY
            ↓
            VERIFY
            ↓
            COMMIT
```

Constituyéndose como el puente entre memoria lógica y realidad física encargado de:

```
detectar → validar → modificar → verificar → registrar
```

El mecanismo de backup previo y trazabilidad histórica del Sentinel ya materializa ese principio: antes de sobrescribir se preserva el estado anterior y el movimiento queda registrado.

Una distinción que debe preservarse:

> *"EVITAR QUE LA CAPA SE CONVIERTA EN 'supermódulo'"*
> — F4, §11

La arquitectura debería conservar estas fronteras:

| Componente         | Responsabilidad                |
|--------------------|--------------------------------|
| WS-SENTINEL        | observa y enruta               |
| PATH MAP           | indexa                         |
| PATH RESOLVER      | localiza                       |
| MFN REGISTRY       | interpreta identidad declarada |
| PATCH RESOLVER     | reconcilia referencias         |
| DEPENDENCY SCANNER | determina requisitos           |
| TESTERS            | verifican comportamiento       |
| BATCH EXECUTOR     | ejecuta operaciones            |

Es decir: cada módulo tiene una pregunta diferente, lo que permite que la capa sea modular.

### 2.5.11. Definición formal de WRIL

> **Workspace Resolution & Integrity Layer (WRIL):** Capa de infraestructura responsable de mantener la correspondencia entre la identidad declarativa de los artefactos, su ubicación física, sus dependencias y sus referencias internas. La capa observa el workspace mediante WS-Sentinel, materializa su topología mediante Path Map, proporciona direccionamiento lógico mediante PathResolver, detecta y corrige referencias obsoletas mediante PatchResolver, registra la identidad MFN mediante File Registry y verifica la coherencia mediante scanners y testers. Su principio operacional es Discover → Resolve → Reconcile → Verify → Record.
> — F4, definición final

---

## 2.6. Principio Rector del TOMO II

El TOMO II ha establecido la capa de comunicación de la ECN: el Neurobit Protocol v1.1 y su integración con WRIL. Hemos recorrido:

1. **Los contenedores semánticos fractales**: BOUNDARY, ACTION_WORD, CLASS, PAYLOAD.
2. **Las reglas de integridad**: simetría, identidad, anidamiento LIFO, rechazo seguro.
3. **El flujo operativo**: emisión, transporte, validación, despacho, registro.
4. **El protocolo HOOK**: continuidad ante saturación de contexto.
5. **La integración con WRIL**: la capa que materializa el Verbo en territorio.

El principio rector que unifica todo el tomo es:

> *"La soberanía cognitiva del protocolo no consiste en sustraerse a la infraestructura que transporta el mensaje, sino en mantener explícita la separación entre intención, sintaxis, transporte, interpretación y ejecución."*
> — F6, §15

Esta separación es la traducción técnica del Logos Genuino definido en el TOMO I:

```
INTENCIÓN DEL EMISOR
    ≠
SINTAXIS DEL PROTOCOLO
    ≠
TRANSPORTE
    ≠
INTERPRETACIÓN DEL RECEPTOR
    ≠
EJECUCIÓN
```

Cada capa tiene su responsabilidad. Cada capa puede fallar independientemente. Cada capa puede ser verificada independientemente. Y cuando todas operan en coherencia, el Verbo viaja sin distorsión desde la intención hasta la ejecución.

El TOMO II queda cerrado. La forma del Verbo está definida. El territorio que la sostiene está mapeado.

El TOMO III desplegará la infraestructura completa: la ECN, la Matriz Fractal Neurovitrónica 13x13, y el aislamiento en 127.0.0.1 que constituye la Jaula de Faraday Semántica.



----------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------
