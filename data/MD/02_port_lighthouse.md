# Módulo 02: port_lighthouse.py (Faro de Puertos Soberano)
## Ficha de Identidad
* **Nombre Físico del Archivo:** `port_lighthouse.py` (también empaquetado como `core/port_lighthouse.py`)
* **Ubicación Física Observada:** `~/compendio/core/port_lighthouse.py` (duplicado en la raíz principal `./port_lighthouse.py` y bajo la versión lúdica `port_lighthouse-D.py`)
* **Ubicación MFN Declarada (Cabecera):** `core/`
* **Nivel de la Capa (MFN_LEVEL):** `1` (Kernel Semántico / Infraestructura Base)
* **Coordenada de la Matriz (MFN_COORD):** `(7,7)` (El centro geométrico del Atanor)
* **Versión del Módulo:** `v1.0`

---

## 1. Funcionamiento Simplificado (Para el Aspirante)
El **Faro de Puertos Soberano** (`PortLighthouse`) es el inspector de red de tu estación central. En Linux tradicional, cuando intentas levantar varios servidores locales (como la API en el 5000 o el Cartógrafo en el 5002), es común sufrir el molesto error "Address already in use" (Puerto ya ocupado). El Faro elimina este dolor por completo: antes de que un módulo intente abrir un puerto, le pregunta al Faro. Este realiza un sondeo físico no invasivo y silencioso en localhost. Si el puerto deseado está ocupado, la asignación se desliza suavemente por el rango de puertos libres asignados a su membrana (Efecto Muelle). Al sintonizarse, escribe el número de puerto real en un pequeño papel inmutable en el disco, permitiendo que tu navegador y tus complementos se orienten en caliente leyendo el archivo, sin necesidad de hacer peticiones de red cruzadas (Bypass de CORS).

---

## 2. Lógica de Operación y Funciones
El objeto `SOSPortLighthouse` implementa un mecanismo determinista de resolución de sockets en localhost:
* **MEMBRANAS (Segmentación de Puertos por Procedencia):**
  * `CORE`: Rango `5000–5009` (API Central, Despachadores).
  * `EXT`: Rango `5010–5019` (Servidores de fragmentos / extensiones).
  * `TOOLS`: Rango `5020–5029` (Interfaces lúdicas, terminales de monitoreo).
* **is_port_available(port, host="127.0.0.1"):** Abre un canal de socket TCP rápido sobre localhost con un timeout estricto de 0.1s e intenta hacer un `bind()`. Si el kernel responde con una excepción `OSError`, el Faro sabe que el puerto físico está secuestrado y retorna `False` sin interrumpir la ejecución.
* **request_port(module_id, provenance="EXT", default_port=None):** Orquesta la asignación dinámica. Busca primero el puerto solicitado por defecto dentro de la membrana correspondiente. Si el muelle está ocupado, recorre linealmente el rango de la membrana hasta encontrar la primera coordenada libre, registrando la asignación y escribiendo la identidad en el disco real.
* **_cleanup_sockets():** Atado al ciclo de vida del intérprete mediante el gestor `atexit`. Cuando el proceso muere (ya sea de forma limpia o por un `SIGTERM` abrupto), el Faro remueve quirúrgicamente los puertos declarados de la tabla global para evitar la amnesia de puertos zombis tras reinicios.

---

## 3. Variables y Constantes Hardcodeadas
* Los rangos de membranas están estancados en el diccionario `MEMBRANAS` (`5000..5009`, `5010..5019`, `5020..5029`).
* La ruta del archivo físico de concordancia está atada a `wril/path_map.json` y la identidad a `data/runtime/api_port.identity`.

---

## 4. Interacciones y Cooperación
* **despertador_hub.sh (Módulo 3):** Es el principal cliente del Faro. Al levantarse el entorno del Hub, el script Bash ejecuta en línea el Faro de Puertos para mapear dónde debe sintonizar la API de Flask.
* **neurobit_api.py (Módulo 5):** Consume el conector de módulos para garantizar que arranca en la interfaz asignada por el Faro.

---

## 5. Dependencias
* **Ecosistema Python standard:** `socket`, `json`, `os`, `atexit`, `sys`, `pathlib`.
* **Librerías de Terceros:** Cero dependencias externas.

---

## 6. Diagrama de Flujo Conceptual
```text
  [ Módulo solicita Puerto 5000 ]
                 │
                 ▼
    [ is_port_available(5000)? ]
        ┌────────┴────────┐
        ▼ (SÍ)            ▼ (NO)
   [ Retorna 5000 ]   [ Efecto Muelle ]
        │             [ Busca en Membrana CORE ]
        │                         │
        ▼                         ▼
   [ Sella puerto en api_port.identity / path_map.json ]
```

---

## 7. Tensiones e Inconsistencias (Fase 1)
* **Tensión A (Triple Duplicidad de Archivo):** El archivo físico se encuentra triplicado en tu territorio real (raíz `./port_lighthouse.py`, subdirectorio `core/port_lighthouse.py` y bajo el Instalador Lúdico como `port_lighthouse-D.py`). Debe unificarse en `core/port_lighthouse.py` y sanear los punteros duplicados de `path_map.json`.
