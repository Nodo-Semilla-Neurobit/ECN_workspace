# 06_base_adapter.md — Interfaz de Adaptadores de la ECN

## 1. Identidad Declarativa y Ubicación
* **Archivo:** `base.py`
* **Ubicación Canónica Declarada:** `core/adapters/`
* **Ubicación Real:** `core/adapters/`
* **Nivel MFN:** `1`
* **Firma de Ubicación MFN:** `# MFN_LOCATION: core/adapters/`
* **Identificación de Orfandad:** **Verificado (Tiene cabecera MFN)**

---

## 2. Propósito y Lógica Operacional
Es el contrato formal del sistema que implementa el patrón **Design by Contract** (Diseño por Contrato). Define la clase abstracta pura `BaseAdapter` y una clase de excepción personalizada `ValidationError` [219].

Su objetivo es aislar la lógica de negocio y las interfaces externas del núcleo de la estación central. Cualquier módulo que actúe como un adaptador de entrada o salida debe heredar obligatoriamente de esta clase e implementar sus esquemas de validación de datos de entrada/salida [219].

Posee un **validador de esquemas JSON ultra-liviano integrado** que no utiliza librerías de terceros (cero dependencias de npm o pip externas), manteniendo la máxima soberanía y compatibilidad técnica [219].

---

## 3. Estructura de Métodos y Funciones
* **`class ValidationError(Exception)`**: Excepción lanzada cuando los datos entrantes o salientes violan los contratos definidos.
* **`class BaseAdapter(ABC)`**: Clase base abstracta.
  * **`execute(self, payload: Dict[str, Any]) -> Dict[str, Any]`**: Método abstracto de ejecución que debe procesar la tarea.
  * **`input_schema(self) -> Dict[str, Any]`**: Esquema esperado de entrada (JSON-like).
  * **`output_schema(self) -> Dict[str, Any]`**: Esquema esperado de retorno.
  * **`validate_data(self, data: Dict[str, Any], schema: Dict[str, Any])`**: Lógica de validación interna no-invasiva por coincidencia de tipos y claves obligatorias.

---

## 4. Endpoints y Conectividad
* **Endpoints HTTP:** No posee endpoints.
* **Mapeo de Red:** Operación puramente local en el espacio de memoria del proceso de Python.

---

## 5. Dependencias y Colaboración
* **Dependencias Estándar:** `abc` (Abstract Base Classes), `typing` (Dict, Any).
* **Dependencias Externas:** Ninguna (0% dependencias de terceros).
* **Scripts Complementarios Necesarios:** No requiere scripts adicionales para ejecutarse, actúa como la biblioteca base inmutable.
* **Colaboración Directa:**
  * Invocado y parseado por `ModuleConnector` para verificar que las clases cargadas sean verdaderos adaptadores [222].
  * Heredado por `AdapterCorreos`, `AdapterCentinela`, y `AdapterMfnCartografo` [215, 217, 218].

---

## 6. Variables Estáticas y Tensiones de Ruta
* **Rutas Hardcodeadas:** Ninguna.
* **Tensiones Identificadas:** Ninguna. Es una pieza de diseño pura y genérica.

---

## 7. Diagrama de Flujo del Contrato
```text
  [ Entrada: Payload ]
          │
          ▼
   [ validate_data() ] ──(Falla Tipo/Clave)──► [ ValidationError ]
          │
          ├─► (OK)
          ▼
    [ execute() ]  ◄── (Implementación obligatoria del adaptador)
          │
          ▼
   [ validate_data() ] (Verifica output) ────► [ Retorno Validado ]
```