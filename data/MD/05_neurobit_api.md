# Módulo 05: neurobit_api.py (El Hub Dinámico del Núcleo)
## Ficha de Identidad
* **Nombre Físico del Archivo:** `neurobit_api.py`
* **Ubicación Física Observada:** `~/compendio/neurobit_api.py` (y duplicado bajo la ruta transitoria de instalación en `INSTALACION/modulos/neurobit_api.py`)
* **Ubicación MFN Declarada (Cabecera):** `./` (Ambiguo / Carpeta Raíz)
* **Nivel de la Capa (MFN_LEVEL):** `1` (Kernel Semántico / Orquestación)
* **Coordenada de la Matriz (MFN_COORD):** `(7,7)` (Comparte el centro con el Faro de Puertos)
* **Versión del Módulo:** `v2.0` (Orquestación dinámica integrada)

---

## 1. Funcionamiento Simplificado (Para el Aspirante)
El `neurobit_api.py` es el sistema nervioso central de tu estación. Actúa como el **Hub Dinámico** (conector unificado). Su única tarea es levantar la pasarela de control local (en localhost) para que los adaptadores puedan comunicarse con el núcleo sin tener que conocer las rutas de disco ni saber de programación de red compleja. El Hub no contiene lógica de negocios; solo se encarga de cargar dinámicamente los conectores declarados en las carpetas y levantar la API en un entorno cerrado y seguro (Jaula de Faraday Semántica).

---

## 2. Lógica de Operación y Funciones
El módulo es un disparador minimalista integrado con las clases de orquestación de la estación:
* **ModuleConnector:** Instancia el cargador dinámico de adaptadores. Este escanea la carpeta `core/adapters/` en caliente, buscando clases hijas de `BaseAdapter` y cargando en la RAM únicamente aquellas autorizadas en los contratos de la estación.
* **APIEndpointManager:** Toma el conector, analiza las firmas semánticas de cada adaptador e inyecta dinámicamente los endpoints HTTP correspondientes en el microframework Flask.
* **Arranque localhost loopback:** Llama al manager forzando el arranque en la interfaz exclusiva `127.0.0.1` (Jaula de Faraday Semántica), prohibiendo la escucha en la interfaz abierta `0.0.0.0` para evitar la telemetría gráfica corporativa y mantener un cordón sanitario inexpugnable.

---

## 3. Variables y Constantes Hardcodeadas
* El puerto de Flask por defecto está configurado rígidamente en la interfaz de arranque: `port=5000` si es ejecutado de forma directa.

---

## 4. Interacciones y Cooperación
* **module_connector.py:** Motor de descubrimiento dinámico.
* **api_endpoint_manager.py:** Administrador dinámico de los endpoints del microframework Flask.
* **despertador_hub.sh (Módulo 3):** Es el script que se encarga de despertar este Hub inyectándole la variable de entorno del puerto sintonizado.

---

## 5. Dependencias
* **Ecosistema Python:** `flask`, `flask_sock` (para WebSockets concurrentes), `requests`.
* **Capa Core Interna:** `core.module_connector`, `core.api_endpoint_manager`.

---

## 6. Diagrama de Flujo Conceptual
```text
     [ Inicia neurobit_api.py ]
                 │
                 ▼
      [ Carga ModuleConnector ] ────► [ Escanea core/adapters/ ]
                 │
                 ▼
    [ Carga APIEndpointManager ] ───► [ Inyecta Endpoints Flask ]
                 │
                 ▼
  [ Levanta Web Server 127.0.0.1:5000 ] (Jaula de Faraday)
```

---

## 7. Tensiones e Inconsistencias (Fase 1)
* **Tensión A (La Ubicación Ambivalente):** El archivo físico tiene declarada la ubicación `MFN_LOCATION: ./` en su cabecera de la versión de instalación, obligándolo a residir suelto en la raíz del espacio de trabajo. Sin embargo, el plano canónico de la ECN establece que debe vivir dentro de `core/neurobit_api.py`. Esta discrepancia es la **Tensión #3** explícitamente citada por el Auditor en los runbooks de ensamble de la Estación.
