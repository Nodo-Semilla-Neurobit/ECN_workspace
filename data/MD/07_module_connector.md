# 07_module_connector.md — Registro Dinámico de Adaptadores

## 1. Identidad Declarativa y Ubicación
* **Archivo:** `module_connector.py`
* **Ubicación Canónica Declarada:** `core/`
* **Ubicación Real:** `core/`
* **Nivel MFN:** `1`
* **Firma de Ubicación MFN:** `### MFN_LOCATION: core/`
* **Identificación de Orfandad:** **Verificado (Tiene cabecera MFN)**

---

## 2. Propósito y Lógica Operacional
Actúa como el **Service Registry** o Registro Dinámico de Adaptadores del sistema [222]. Es el engranaje encargado del descubrimiento y la inyección en caliente de los módulos del ecosistema [222].

Su lógica consiste en escanear recursivamente la carpeta de adaptadores (por defecto `core/adapters/`), buscar todos los archivos con extensión `.py`, cargarlos dinámicamente en el intérprete de Python en caliente mediante el subsistema de bajo nivel `importlib`, e inspeccionar sus clases con el módulo estándar `inspect` [222]. Si localiza una clase que es subclase de `BaseAdapter` y que no es abstracta, la instancia y la guarda en su base de datos interna de adaptadores [222].

Esto permite que se puedan agregar nuevos adaptadores arrojándolos en `core/adapters/` sin necesidad de reiniciar el orquestador principal, logrando un desacoplamiento absoluto [222].

---

## 3. Estructura de Métodos y Funciones
* **`class ModuleConnector`**:
  * **`__init__(self, adapters_dir=None)`**: Inicializa la ruta de escaneo dinámica. Si no se especifica, utiliza la ruta canónica basada en el resolvedor de la ECN [222].
  * **`reload_adapters(self)`**: Ejecuta el censo territorial de adaptadores. Vacía y reconstruye `self._registry` [222].
  * **`get_adapter(self, name: str) -> Optional[object]`**: Recupera la instancia de un adaptador por su clave identificadora.

---

## 4. Endpoints y Conectividad
* **Endpoints HTTP:** No expone sockets directamente.
* **Mapeo de Red:** Operación puramente local. Provee las referencias de memoria para que la API o el Dispatcher puedan invocar las operaciones.

---

## 5. Dependencias y Colaboración
* **Dependencias Estándar:** `importlib.util`, `inspect`, `pathlib`, `typing`.
* **Dependencias de Terceros:** Ninguna.
* **Colaboración Directa:**
  * **Provee datos a:** `APIEndpointManager` para que éste monte los endpoints HTTP de Flask en caliente de forma automatizada [220].
  * **Carga físicamente a:** todos los scripts que viven dentro de `core/adapters/` [222].

---

## 6. Variables Estáticas y Tensiones de Ruta
* **Resolvedor de Raíz Canónica:** Utiliza `Path(__file__).resolve().parent.parent` para anclar el directorio de adaptadores relative a su propia ubicación de forma autónoma [222]. Esto evita errores de rutas absolutas si la estación cambia de carpeta [122].
* **Tensiones Identificadas:** Si un adaptador malformado (con un error de sintaxis) es arrojado a la carpeta, el cargador dinámico puede colapsar o levantar alertas silenciosas según la política de contención de excepciones del `reload_adapters`.

---

## 7. Diagrama de Flujo del Censo
```text
  [ reload_adapters() ]
            │
            ▼
    [ Listar *.py ] ──► (Para cada archivo en core/adapters/)
            │
            ▼
    [ importlib.util ] ──► Carga el módulo en memoria
            │
            ▼
     [ inspect.getmembers() ] ──► ¿Hereda de BaseAdapter?
            │
            ├─► (Sí) ──► [ Instanciar y registrar en _registry ]
            └─► (No) ──► Ignorar / Descartar
```