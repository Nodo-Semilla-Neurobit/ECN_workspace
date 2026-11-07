# 08_api_endpoint_manager.md — Enrutador Dinámico (Hub Central)

## 1. Identidad Declarativa y Ubicación
* **Archivo:** `api_endpoint_manager.py`
* **Ubicación Canónica Declarada:** `core/`
* **Ubicación Real:** `core/`
* **Nivel MFN:** `1`
* **Firma de Ubicación MFN:** `### MFN_LOCATION: core/`
* **Identificación de Orfandad:** **Verificado (Tiene cabecera MFN)**

---

## 2. Propósito y Lógica Operacional
Representa el cerebro del **Hub Dinámico** de la estación [220]. Su única responsabilidad es actuar como una capa de orquestación y mapeo entre el protocolo de red HTTP local (Flask) y los adaptadores de la ECN [220].

**Principio de diseño estricto:** El Endpoint Manager **no contiene lógica de negocios** [220]. 
Su flujo operacional es:
1. Recibe el registro consolidado de adaptadores desde el `ModuleConnector` [220].
2. Lee los metadatos de entrada/salida y los esquemas (`input_schema`, `output_schema`) declarados por cada adaptador [219, 220].
3. Construye dinámicamente las rutas HTTP en Flask atadas estrictamente a localhost (`127.0.0.1`) [220].
4. Intercepta las solicitudes HTTP entrantes, valida el payload contra el contrato in situ usando el validador del adaptador, despacha la ejecución, y formatea la respuesta de retorno [219, 220].

---

## 3. Estructura de Métodos y Funciones
* **`class APIEndpointManager`**:
  * **`__init__(self, connector: ModuleConnector)`**: Vincula el registrador in-memory de adaptadores [222].
  * **`register_routes(self, app: Flask)`**: Escanea los adaptadores registrados y monta las rutas Flask de forma automatizada mediante decoradores de bajo nivel o llamadas directas a `app.add_url_rule`.
  * **`_dispatch_call(self, adapter_name: str)`**: Enrutador genérico interno que recibe la llamada HTTP, valida schemas y redirige de forma transaccional el control al adaptador adecuado [219].

---

## 4. Endpoints y Conectividad
* **Endpoints HTTP:** Monta los endpoints dinámicos autodeclarados (ej: `/ingesta_neurobit`, `/correos/status`, `/health`) [9, 217].
* **Mapeo de Red:** Operación en localhost (`127.0.0.1`) para garantizar el cordón sanitario de aislamiento absoluto (Jaula de Faraday Semántica) [5, 119].

---

## 5. Dependencias y Colaboración
* **Dependencias Estándar:** `pathlib`, `sys`, `json`.
* **Dependencias de Terceros:** `Flask`.
* **Colaboración Directa:**
  * **Consume a:** `ModuleConnector` (para leer los adaptadores) y `BaseAdapter` (para forzar la validación de contratos) [219, 222].
  * **Orquestado por:** `neurobit_api.py` (quien arranca el servidor Flask y le pasa el control) [177].

---

## 6. Variables Estáticas y Tensiones de Ruta
* **Fricción del Reload (Limitación de Diseño):** El Endpoint Manager tiene un comportamiento de acumulación. Si agregas un adaptador nuevo, `reload_adapters` registrará el endpoint, pero si lo retiras, el endpoint antiguo permanecerá en la RAM del proceso de Flask hasta que se reinicie el servidor de forma física [220]. Esto es una limitación explícita asumida para simplificar la estabilidad de Flask [220].
* **Tensiones de Puerto:** Su arranque es solidario con `port_lighthouse.py`. Si el faro asigna un puerto del rango `CORE` (5000-5009), este administrador debe plegar dinámicamente su socket a ese muelle real [6, 157].

---

## 7. Diagrama de Flujo del Despacho HTTP
```text
  [ Petición HTTP ] ──► /ingesta_neurobit ──► [ APIEndpointManager ]
                                                    │
                                                    ▼
                                          [ Validar input_schema ]
                                                    │
                                           ├─► (Válido) ─► [ Invocación Adapter.execute() ]
                                           └─► (Fallo)  ─► [ ValidationError 400 Bad Request ]
```