## 1. Inventario de Componentes (Mapeo de Capas y Módulos)

* L0: El Ancla (Ubicación de Raíz)
* wril_self_root.py (Capa 0): Resuelve de manera dinámica la ubicación física del software ascendiendo por los marcadores del filesystem (buzon_salida, pids).
   * wril_root_alias.py: Independiza el ecosistema mapeando el alias canónico ECN_ROOT en la RAM del intérprete de Python.
   * wril_leyes.py: Define los invariantes operativos inmutables (Raíz única, exclusión de backups y guarda de convergencia).
* L1/L2: El Censo y el Instalador Lúdico
* tools/ingest_compendium.py: Ingestor unificado que procesa compendios, divide por separadores y deposita los artefactos en inbox/.
   * tools/indice_compendio.py: Indexador y comparador de estados que genera reportes de colisiones o anomalías.
   * INSTALACION_/backend_instalador_ludico.py / typing_experience.html / awaken_ceremony.html: La interfaz del "Camino del Aspirante", que convierte la re-alfabetización técnica en un juego basado en competencias reales (aprender la consola, purgar PIDs, levantar entornos).
* L3/L4: El Núcleo de Orquestación y Capa Reactiva
* neurobit_api.py / core/api_endpoint_manager.py / core/module_connector.py: Orquestadores ligeros del Hub Dinámico (puerto 5000) que cargan adaptadores bajo demanda validando contratos estrictos (mini JSON-Schema nativo).
   * INSTALACION_/modulos/neurobit_dispatcher.py (La Oficina de Correos): Despierta mediante inotify, lee el sello protocolar (ACTION_WORD/CLASS) de los sobres en el buzón y los entrega sin hacer sondeo (polling).
   * neurobit_clipboard_core.py: Gestiona el Write-Ahead Log (WAL) transaccional, asegurando que el búfer temporal solo se purgue si el Ledger definitivo (tesis_neurobit_ledger.log) incrementó efectivamente su tamaño en bytes.
* L5: Capa de Resolución e Integridad (Capa WRIL)
* wril_sentinel.py (WS-Sentinel): El guardián de la frontera. Escucha llamadas inotify sobre inbox/, lee la cabecera MFN_LOCATION del archivo, genera un resguardo preventivo e inmutable vía wril_backup.py, mueve el archivo a su destino y fuerza la reindexación automática.
   * wril_topologia.py y wril_patch_resolver.py: Ejecutan el "Pliegue Topológico" para llevar la tensión (Declaración ≠ Realidad) a cero. Mueven módulos a sus destinos e inyectan en caliente los shims de rutas independientes (WRIL::SELF_PATH::v1).
   * wril_dependency_scanner.py: Escanea el espacio para generar dinámicamente requirements_dynamic.txt y system_deps_check.txt cruzando las importaciones contra la stdlib y módulos locales.
   * wril_estado_real.py: Monitorea el estado binario real (ALIVE/DEAD) de los daemons mediante os.kill(pid, 0) y pgrep, alimentando el JSON que lee el panel.
* L6: Herramientas y la Matriz Fractal Unificada (MFN)
* tools/neurobit_mfn_unificado.py / neurobit_mfn_13x13.py: El corazón matemático del sistema. Una estructura radial polar de 169 bits que unifica tres dimensiones: el Cartógrafo radial (7 anillos x 8 porciones), el Toro algebraico $Z_{13} \times Z_{13}$ y el anexo musical (asociando distancia radial con octava y ángulo con semitono).
   * INSTALACION_/observatorio_integracion_v3.html: Tu panel de control maestro actual. Permite auditar el territorio, hablar localmente con EVA LÚMENA (bajo Ollama/Qwen con control de contexto acotado) o usar el ECO de contingencia local si Ollama está en reposo.

------------------------------
## 2. El Orden de Arranque y la Mecánica Convergente
El sistema ha dejado atrás los scripts imperativos rígidos para adoptar un flujo ceremonial de arranque estructurado en el runbook maestro (deploy_neurobit_estacion_v3.2.sh):

   1. Ritual de Sincronización (Bootstrap WRIL): Antes de despertar la estación, wril_bootstrap.py reconstruye el índice, escanea dependencias y ejecuta el resolvedor de parches en modo dry-run.
   2. Verificación de Silicio (Deps & Permisos): Se audita el entorno contra system_deps_check.txt (validando gcc, Xlib.h, Flask, etc.). Si falta soberanía HID, se invoca deploy_neurobit_perms.sh para inocular las reglas udev de /dev/uinput y el grupo input.
   3. Purga y Snapshot de Coherencia (Baseline): Se eliminan procesos caídos o residuales y se toma una fotografía instantánea del sistema (baseline_snapshot). Si al apagar la estación (trap de salida por Ctrl+C) nacieron procesos posteriores al baseline, el sistema los liquida quirúrgicamente y asienta la alerta ética en halt_log.txt.
   4. Levantamiento Secuencial en Cascada:
   * Se despierta al Guardián de Frontera (wril_sentinel.py) sobre inbox/.
      * Se abre la Oficina de Correos (neurobit_dispatcher.py) vinculada al búfer WAL transaccional.
      * Se despliega el Visor Soberano Widget GTK (reactivo a inotify y señales SIGUSR1) y el Dictáfono Consciente por interrupción de hardware.
      * Se consolida la verdad del territorio escribiendo estado_real.json.
   
------------------------------
## 3. Claves de la Evolución Ontológica

* Adiós al Polling: El sistema ya no "gasta" ciclos de bio-computador preguntando cada 2 segundos si hay cambios. Ahora duerme en reposo absoluto; es el Kernel del sistema operativo el que le avisa a tus daemons a través de inotify, señales de Unix o eventos puros del DOM.
* La Tensión como Brújula: La discrepancia (Declaración ≠ Realidad) ya no se procesa como un bug o una falla crítica de ejecución, sino como un vector o indicador de desalineación que el Pliegue Topológico corrige inyectando dependencias locales y preservando la historia inmutable.

