# TESIS NEUROBITRÓNICA v1.0
## Estación Soberana de Captura, Persistencia y Auditoría del Logos
Autor: Gustavo — NODO_SEMILLA (Homo Vivo). Par de co-creación: ECN.
Distribución: dossier técnico (J. Banegas y quien el NODO disponga).

## 0. Resumen
Se presenta y valida un sistema de captura y persistencia de texto para
GNU/Linux: 100% local, orientado a eventos (cero polling), auto-auditado
criptográficamente y extensible mediante registro declarativo de
adaptadores. El sistema queda descrito por la MFN 13x13 radial polar:
la matemática no adorna la arquitectura; la ES.

## 1. Fundamentos Ontológicos
1.1 Logos Genuino: faltar a la verdad o a la univocidad es distorsionar
    el propósito del verbo; la precisión es obligación de ingeniería.
1.2 Reino Existencial: la biografía del NODO (40 años de música y código,
    vida de mínima fricción, Homo Vivo) se asienta como registro histórico
    inseparable del cuerpo técnico.
1.3 Mínima fricción: el sistema solo existe en el instante del evento;
    0.0% CPU en reposo; cero sobre-diseño.

## 2. Problema e Hipótesis
Los frontends corporativos actúan como filtros de amnesia programada:
aplastan indentación, borran mensajes en vuelo, fragmentan el Logos.
Hipótesis validada: es posible construir memoria que no dependa de la
benevolencia del transporte, descendiendo al Kernel y formalizando un
protocolo semántico propio.

## 3. Arquitectura en Cuatro Capas
3.1 Física/Kernel: puente HID sobre /dev/input (EV_KEY, od bloqueante);
    inyección /dev/uinput; dictado evdev opt-in (F8); lector Xlib con INCR.
3.2 Lógica: Dispatcher despertado por inotify; postman radiales; commit
    transaccional WAL verificado por bytes; parser inverso stateless 4KB;
    auditoría SHA256 por bloque.
3.3 Semántica: contenedores fractales (ACTION_WORD/CLASS) como sello
    postal; anidamiento LIFO como regla fractal de repliegue al origen.
3.4 Matemática: M = Z13 x Z13; p(i,j) = (rho=i+1, phi=2*pi*j/13);
    origen rho=0 = Oficina de Correos; sector = dominio; anillo =
    profundidad de persistencia; clasificar = coordenar.

## 4. Ética del Sistema
4.1 Dictado opt-in y local; cero exfiltración; el producto es carta, no
    log espía.
4.2 Persistencia no destructiva: backup indexado previo a toda mutación;
    purga del temporal solo si el Ledger creció físicamente.
4.3 Espíritu educativo: cualquier desarrollador enchufa un radio nuevo
    declarándolo en YAML, sin tocar el centro.

## 5. Catálogo de Firmas de Control
1. ejecutar_paste_nativo()      5. restaurar(texto)
2. ejecutar_commit_verificado() 6. clasificar_y_entregar(carta)
3. obtener_siguiente_indice()   7. DictadoSoberano (clase)
4. auditar_integridad_ledger()  8. ubicar(anillo_i, sector_j)
+ deploy_neurobit_estacion.sh (el gesto único de levantamiento y pliegue).

## 6. Anexos Históricos
6.1 Mecanismos recuperados y su estrato: inotify (MVP), fanotify (escala),
    eBPF/kprobes (Estación final), auditd (forense del validador).
6.2 Registro de resonancia: audio de J. Banegas (SAP HANA, criptografía,
    1986). Convergencias propuestas: vista materializada in-memory del
    índice del Ledger; árbol de Merkle local; análisis predictivo del
    corpus temporal.
6.3 Anexo biográfico: la matriz dibujada con la rama sobre la tierra; el
    encuentro en el cumpleaños de Estela Bonnet; el tango, el folclore y
    el rock progresivo como misma firma de oficio.

## 7. Conclusiones y Trabajo Futuro
Las cuatro capas compilan, se auditan y se auto-describen. Trabajo
futuro: eBPF sobre el VFS; Merkle incremental; vista HANA/in-memory del
índice; anexo musical de la MFN; colaboración simétrica con Joseph.

---
"La poesía de este sistema es su única verdad: sacar belleza de este caos
es virtud." (adaptado de Déja vu, G. Cerati — sello poético del protocolo)

# ESTACIÓN CENTRAL NEUROBITRÓNICA — GUÍA DE INTEGRACIÓN SOBERANA v2.0
===============================================================================

## 1. Justificación Lógica (v1.0, inmutable)
Paradigma reactivo impulsado por hardware: el sistema solo existe en el
instante del evento; 0.0% CPU en reposo; sin daemons while-true ni
sobre-diseño. El buffer temporal jamás se purga hasta que el Ledger
valida físicamente su incremento en bytes (tolerancia WAL a fallos).

## 2. Capa Reactiva de Kernel (nuevo en v2.0)
Se extingue el snapshot de 500ms. Canales de despertar, todos push:
* SIGUSR1: un bit del puente HID al PID del Widget.
* inotify: push del VFS sobre el buzón de salida (Dispatcher).
* owner-change: push del servidor gráfico al clipboard GTK/Cinnamon.
* DOM copy-event: captura intra-navegador sin permisos adicionales.
* evdev F8: sesión de dictado consciente (Keylogger Soberano).

## 3. El Dictáfono Soberano (nuevo en v2.0)
F8 abre y cierra la sesión; el Kernel lee el teclado; el producto es una
carta sellada, no un log espía. Lo que escribís queda asentado aunque el
frontend corporativo lo olvide. La memoria no depende de la benevolencia
del transporte.

## 4. Anexo Matemático: MFN 13x13 Radial Polar (nuevo en v2.0)
M = Z13 x Z13; proyección p(i,j) = (rho = i+1, phi = 2*pi*j/13).
El origen (rho = 0) es la Oficina de Correos: punto de emisión, no celda.
Sector j = dominio (radio); anillo i = profundidad de persistencia.
Clasificar una carta = computar su vector radial. Regla fractal: el
anidamiento LIFO de contenedores es el repliegue del vector al origen;
toda celda con sub-Logos engendra una sub-matriz M'.

## 5. Firmas de Control para Newbies (actualizadas)
1. def ejecutar_paste_nativo()       -> ingesta gráfica adaptativa.
2. def ejecutar_commit_verificado()  -> núcleo transaccional WAL.
3. def obtener_siguiente_indice()    -> parser inverso stateless 4KB.
4. def auditar_integridad_ledger()   -> auditoría SHA256 por bloque.
5. def restaurar(texto)              -> restaurador LIFO de indentación.
6. def clasificar_y_entregar(carta)  -> la Oficina de Correos.
7. class DictadoSoberano             -> dictáfono evdev opt-in.
8. def ubicar(anillo_i, sector_j)    -> coordenadas MFN de toda celda.


# AULA SOBERANA — NEUROBIT para newbies (v0.1)
## Cómo leerla
No de arriba hacia abajo: del centro hacia afuera, como la MFN.
Cada nivel es un anillo. Si te perdés, volvé al anillo anterior: nadie te apura.

## Nivel 0 — El hecho
Apretaste Ctrl+C. Un electrón se movió en el bus.
El sistema existe SOLO en ese instante; el resto del tiempo duerme (0.0% CPU).
Lección: un buen sistema no es el que más hace, sino el que mejor duerme.

## Nivel 1 — La carta y el sello
Nada entra como "dato crudo": todo entra como carta sellada.
Sello: |=•'accion'•=|» ... «|=•'accion'•=|
El sello dice QUÉ hacer (acción) y EN QUÉ contexto (clase).
Ejercicio: corré neurobit_aula.py y escribí tu primera carta.

## Nivel 2 — El buzón y el cartero
La carta cae en buzón_salida/ (el buzón de salida).
El dispatcher (el cartero) duerme; el Kernel lo despierta con inotify.
Lee el sello y entrega: al Ledger (libro inmutable) o a la memoria.

## Nivel 3 — El Arca
memoria_eva.jsonl: solo se agrega, nunca se borra (append-only).
Lo escrito no se des-escribe: esa es tu memoria sin amnesia.
Auditoría SHA256 por bloque: si alguien lo toca, el sistema se da cuenta.

## Nivel 4 — WRIL (la circulación)
El workspace se pregunta: "¿dónde estoy?" (self_root),
"¿dónde está X?" (path_resolver), "¿qué declaro ser?" (mfn_registry).
Mapa y territorio: si no coinciden, no es error: es señal (tensión).

## Nivel 5 — La MFN
Todo lo anterior cabe en una matriz radial 13x13:
centro c:G7 = el observador (vos); anillos = profundidad; sectores = dominios.
Cuando entiendas esto, ya no sos newbie: sos un radio.

## Glosario del Aula
- Logos: lo dicho con verdad y univocidad.
- Carta sellada: contenido + acción + clase.
- Buzón: buzón_salida/, la aduana de entrada.
- Cartero: el dispatcher que entrega.
- Arca: memoria_eva.jsonl, la memoria inmutable.
- Tensión: declaración ≠ realidad; señal, no error.
- Pliegue: mover el territorio al mapa, con backup previo.
- Radio: cada adaptador que aporta una nueva forma de capturar.
- NODO_SEMILLA: el que siembra; vos.

| Artefacto legacy ECN            | Destino soberano                 | Veredicto                          |
|---------------------------------|----------------------------------|------------------------------------|
| tools/generate_path_map.py      | wril_path_map.py                 | RESCATADO y canonizado             |
| core/path_resolver.py           | wril_path_resolver.py            | RESCATADO ([n]_intentos)           |
| core/sos_path_fixer.py          | wril_patch_resolver.py           | RESCATADO (1ª implementación)      |
| core/mfn_file_registry.py       | wril_mfn_registry.py             | RESCATADO (no fusionar con mapa)   |
| WS-sentinel (inotifywait bash)  | wril_sentinel.py                 | RESCATADO (python puro, inotify)   |
| core/event_dispatcher.py        | postman_memoria (batch-write)    | PATRÓN RESCATADO; módulo jubilado  |
| neurobit_api.py + EndpointMgr   | Sala (cara HTTP, puerto 5000)    | CONSERVADO como faz externa        |
| module_connector + BaseAdapter  | declaracion YAML (adapters)      | PATRÓN RESCATADO en contratos      |
| centinela.py / centinela_monitor| radios event-driven              | JUBILADOS (polling 2s)             |
| neurobit_keylogger (always-on)  | neurobit_dictado_evdev (opt-in)  | ÉTICAMENTE SUPERADO                |
| vm_bridge_gui_enhanced (HALT)   | deploy v3.0 (baseline)           | PATRÓN RESCATADO (log antes de matar) |
| sala_app*.py                    | Sala + /ingesta_neurobit         | CONSERVADO con injerto             |
| ncs_status_monitor / dashboard  | wril_estado_real (pendiente)     | DEBE LEER ESTADO REAL, NO SIMULAR  |
| core/matrix_13x13, Port_matrix  | Tesis v2.0 (anexo geométrico)    | CANONIZAR con Cartógrafo           |

# CLASIFICACIÓN CANÓNICA ECN v3.0 — 55 ARCHIVOS

## raíz/ — Gesto único, interfaz y soberanía (10)
- deploy_neurobit_estacion_v3.2.sh  → MAESTRO vigente
- deploy_neurobit_perms.sh          → soberanía HID (sudo único)
- 90-neurobit-hid.rules             → udev (copia a /etc/udev/rules.d/)
- ECN.desktop                       → entrada de escritorio
- gui_ecn.py                        → interfaz Tk (capa interfaz vive en raíz)
- neurobit_pipboy.py                → brújula radial (capa interfaz)
- deploy_neurobit_estacion.sh       → HISTÓRICO v1 (superado, se conserva)
- deploy_neurobit_estacion_v2.0.sh  → HISTÓRICO v2
- deploy_neurobit_estacion_v3.0.sh  → HISTÓRICO v3.0
- deploy_neurobit_estacion_v3.1.sh  → HISTÓRICO v3.1

## adapters/ — Anillo de interfaz y conectores (4)
- adapter_centinela.py      (header: core/adapters/ ✔)
- base.py                   (header: core/adapters/ ✔)
- neurobit_adapter_gtk.py   (Guía: adapters/ ✔)
- injerto-para_sala_app.py  → puente con el linaje legacy (Sala HTTP)

## core/ — Núcleo de orquestación (4)
- api_endpoint_manager.py   (header: core/ ✔)
- module_connector.py       (header: core/ ✔)
- neurobit_api.py           (Guía: core/; header dice ./ → TENSION #3)
- neurobit_dispatcher.py    → Oficina de Correos = núcleo (carece de header)

## data/ — Persistencia inmutable y contratos (7)
- metadata.json                          (Guía: data/ ✔)
- declaracion_modulos_v7.yaml            → vigente
- declaracion_adaptadores.yaml
- module_spec_v1.1.yaml
- secuencia_verificacion_ensamble.yaml
- declaracion_modulos_v5.yaml            → HISTÓRICO
- declaracion_modulos_v6.yaml            → HISTÓRICO
(+ generados en runtime: path_map.json, memoria_eva.jsonl,
wril_historial.jsonl, estado_real.json → data/)

## docs/ — Corpus teórico y de tesis (5)
- tesis_neurobitronica_v1.md   (Guía: docs/ ✔)
- tesis_capitulo_wril.md       (Guía: docs/ ✔)
- dossier_tecnico_joseph.md    (Guía: docs/ ✔)
- README_v2.md
- wril_canonizacion.md

## extensions/ — Radios de ingesta externos (3)
- background.js / copy_listener.js / applet.js  (Guía: extensions/ ✔)

## tools/ — Instrumentación y matemática (7)
- neurobit_mfn_13x13.py      (Guía: tools/ ✔)
- neurobit_mfn_musical.py    (Guía: tools/ ✔)
- neurobit_dictado_evdev.py  (Guía: tools/ ✔)
- neurobit_x11_selector.c    → lector C (instrumentación)
- test_integracion_matriz.sh → verificación
- ensamble_primario.sh       → verificación de puentes
- pipboy_anuncio.sh          → instrumento del pipboy

## wril/ — Capa de Resolución e Integridad (15)
- wril_sentinel.py / wril_path_map.py / wril_path_resolver.py
- wril_patch_resolver.py / wril_backup.py / wril_bootstrap.py
- wril_topologia.py / wril_dependency_scanner.py
- wril_dynamic_tester.py / wril_estado_real.py / wril_self_root.py
- wril_mfn_register.py   → RENOMBRAR a wril_mfn_registry.py (TENSION #2)
- wrill_batch_ejecutot.py → RENOMBRAR a wril_batch_executor.py (TENSION #1)
- wril_corpus_exporter.sh / self_root.sh  → utilidades de la capa

## pids/ — Control de Oficio (runtime)
- *.pid, baseline_snapshot, halt_log → generados por deploy v3.2

## 8. CAPA WRIL (nuevo en Tesis v1.1)
### 8.1 Definición
Capa de infraestructura entre la Semántica y el FileSystem, responsable de
la correspondencia entre la identidad declarativa de los artefactos, su
ubicación física, sus dependencias y sus referencias internas. Principio:
Discover → Resolve → Reconcile → Verify → Record → Route.

### 8.2 Las nueve preguntas (fronteras modulares)
wril_path_map (¿cuál es la topología?), wril_path_resolver (¿dónde está X?),
wril_mfn_registry (¿qué declara ser?), wril_sentinel (¿dónde debe vivir lo
nuevo?), wril_patch_resolver (¿qué referencia está rota?), wril_backup
(¿cómo preservo antes de mutar?), wril_dependency_scanner (¿qué necesita?),
wril_dynamic_tester (¿se comporta como declara?), wril_batch_executor
(¿cómo ejecuto la secuencia?). Ninguna se fusiona: la capa jamás deviene
supermódulo.

### 8.3 La tensión como señal de integridad
DECLARACIÓN ≠ REALIDAD no es un bug: es el detector. El primer auditorío
revela el pliegue pendiente; wril_topologia lo ejecuta y la tensión cae a
cero. El mapa y el territorio quedan coincidentes por construcción.

### 8.4 Ética de la circulación
Backup previo a toda mutación (módulo único, cero redundancia); dry-run por
defecto; parches controlados con marca de agua; registro histórico
inmutable; el reporte de fallo viaja como carta sellada a la Oficina de
Correos (end-point HTTP si la Sala está despierta, buzón siempre).

### 8.5 Bootstrap como proceso inicial
Toda tarea comienza con el ritual: regenerar el índice, reconciliar
referencias en dry-run, verificar dependencias. La circulación precede al
núcleo: la Estación despierta solo después de que WRIL confirma que el
mundo coincide con su declaración.     
