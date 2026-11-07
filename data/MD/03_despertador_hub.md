# Módulo 03: despertador_hub.sh (Cliente de Sintonía Efímera)
## Ficha de Identidad
* **Nombre Físico del Archivo:** `despertador_hub.sh` (también guardado como `despertador_hub-D.sh`)
* **Ubicación Física Observada:** `~/compendio/ECN.Instalador_Ludico/despertador_hub.sh`
* **Ubicación MFN Declarada (Cabecera):** *Ninguna (Es un script Bash, carece de cabecera MFN)*
* **Nivel de la Capa (MFN_LEVEL):** *Ninguno*
* **Coordenada de la Matriz (MFN_COORD):** *Ninguna*
* **Versión del Script:** `v1.1`

---

## 1. Funcionamiento Simplificado (Para el Aspirante)
El **Despertador del Hub** (`despertador_hub.sh`) es el interruptor biónico de tu estación. Su única tarea es asegurar que la API central (`neurobit_api.py`) se despierte, sintonice el puerto que le corresponde y corra de forma segura en background bajo tu entorno aislado de Python (`.venv`), todo con un solo comando. Si la API ya está corriendo, el despertador se da cuenta, comprueba su salud enviando un pulso de salud (`/health`) y evita duplicar procesos innecesariamente. Al sintonizarse correctamente, escribe la coordenada de puerto en un archivo para que la consola verde de tu pantalla sepa a dónde enviar tus misiones.

---

## 2. Lógica de Operación y Funciones
Es un script Bash secuencial que sigue la siguiente rutina de sintonización:
* **Fase 1: Interrogación al Faro de Puertos:**
  * Lanza una llamada rápida a Python para importar `core.port_lighthouse` y ejecutar `request_port('neurobit_api', 'CORE', default_port=5000)`.
  * Si el Faro no responde o no está disponible, el script imprime una advertencia y realiza un fallback forzado al puerto `5000`.
  * El puerto real obtenido es estampado en `pids/hub_dinamico.port` para el consumo del frontend.
* **Fase 2: Comprobación de Procesos Preexistentes:**
  * Utiliza herramientas de red de la shell (`ss` o `netstat`) para verificar si ya existe un socket activo en localhost escuchando en el puerto asignado.
  * Si detecta vida en el puerto, envía un pulso rápido de `/health` usando `curl`. Si responde, escribe en el Write-Ahead Log (`sesiones/wal_consola.log`) que la API ya vive, imprime el éxito y termina limpiamente.
* **Fase 3: Búsqueda Ciega de la API en el Territorio:**
  * Para evitar romperse ante traslados físicos de directorios, interroga de forma consecutiva las siguientes rutas candidatas:
    * `"$AQUI/neurobit_api.py"`
    * `"$AQUI/core/neurobit_api.py"`
    * `"$AQUI/INSTALACION/modulos/neurobit_api.py"`
  * Si la API es hallada, la arranca en background inyectando la variable de entorno `ECN_HUB_PORT` y forzando el binario Python del entorno virtual (`.venv/bin/python3`).
* **Fase 4: Verificación de Salud con Timeout (Aduana de Red):**
  * Realiza un bucle de hasta 12 reintentos enviando `curl` secuenciales con retardos de 0.5s. Si sintoniza, escribe el éxito y el PID correspondiente en `pids/hub_dinamico.pid`, cerrando su ciclo de vida y regresando la CPU a un estricto 0% nominal.

---

## 3. Variables y Constantes Hardcodeadas
* El script asume que el directorio de proceso local (`pids`, `logs`, `sesiones`) se encuentra ubicado en el mismo directorio que el script (`AQUI`), en lugar de resolverse de forma dinámica usando el canónico `wril_self_root.py`.

---

## 4. Interacciones y Cooperación
* **port_lighthouse.py (Módulo 2):** Es invocado mediante Python in-line para resolver la negociación de sockets.
* **neurobit_api.py (Módulo 5):** Es el programa hijo que el despertador ejecuta y monitorea.
* **WAL Central (sesiones/wal_consola.log):** Escribe el estado de salud de la API (`HUB_DINAMICO: VIVO`) para mantener la trazabilidad de los ritos del Dojo.

---

## 5. Dependencias
* **Binarios del Sistema:** `bash`, `python3`, `curl`, `ss` / `netstat`.
* **Entorno de Red:** Aislamiento loopback estricto en `127.0.0.1`.

---

## 6. Diagrama de Flujo Conceptual
```text
      [ Inicia despertador_hub.sh ]
                   │
                   ▼
     [ Consulta Faro / PortLighthouse ]
                   │
         ┌─────────┴─────────┐
         ▼ (Puerto Libre)    ▼ (Puerto Ocupado)
    [ Corre neurobit_api ]  [ Comprueba /health via curl ]
         │                        │
         ▼                  ┌─────┴─────┐
    [ Espera /health ]      ▼ (VIVO)    ▼ (MUERTO)
         │               [ Escribe WAL ] [ ERROR ]
         ▼                  [ OK ]
 [ Sella pid & port ]
```

---

## 7. Tensiones e Inconsistencias (Fase 1)
* **Tensión A (El bucle de búsqueda desesperado):** El hecho de que el script tenga que buscar `neurobit_api.py` en tres carpetas candidatas diferentes es una muestra explícita de deuda técnica. Esto se resuelve de raíz delegando la resolución de rutas canónicas a la Capa WRIL (`wril_path_resolver.py`).
