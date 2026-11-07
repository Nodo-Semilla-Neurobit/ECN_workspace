# 09_adapter_correos.md — Puente de Mensajería VFS

## 1. Identidad Declarativa y Ubicación
* **Archivo:** `adapter_correos.py`
* **Ubicación Canónica Declarada:** `core/adapters/`
* **Ubicación Real:** `core/adapters/`
* **Nivel MFN:** `1`
* **Firma de Ubicación MFN:** `### MFN_LOCATION: core/adapters/`
* **Identificación de Orfandad:** **Verificado (Tiene cabecera MFN)**

---

## 2. Propósito y Lógica Operacional
Es el puente transaccional de entrada que conecta el Hub Dinámico (Flask) con el sistema de mensajería basado en el sistema de archivos (VFS) de la ECN [217].

**Solución de Pensamiento Lateral:** Su lógica de diseño rompe con la necesidad de mantener colas de mensajes activas en memoria o sockets abiertos consumiendo recursos. Cuando recibe datos de entrada semánticos (un prompt del usuario, por ejemplo), no invoca una función directa ni procesa la respuesta en ese hilo. En su lugar, empaqueta el contenido en un sobre con el sello protocolar de Neurobit (`ACTION_WORD/CLASS`) y lo escribe físicamente como una **carta sellada** en la carpeta `buzon_salida/` [217].

El kernel del workspace (`neurobit_dispatcher.py`) detecta este archivo mediante señales `inotify` y se encarga del enrutamiento asíncrono [170]. Así, se logra un consumo de CPU del 0.0% en ralentí [169, 170].

---

## 3. Estructura de Métodos y Funciones
* **`class AdapterCorreos(BaseAdapter)`**:
  * **`execute(self, payload: Dict[str, Any]) -> Dict[str, Any]`**: Escribe de forma atómica el archivo de la carta en `buzon_salida/` usando un formato inmutable atado a la fecha y timestamp actual [217].
  * **`input_schema(self)`**: Valida que la solicitud contenga los campos del mensaje protocolar: `action_word`, `class_filter`, `origen`, `payload` [165].
  * **`output_schema(self)`**: Retorna un recibo de entrega que incluye el estado (`ROUTE_OK` o `EN_COLA`) [189].

---

## 4. Endpoints y Conectividad
* **Endpoints HTTP:** Expone lógicamente los endpoints `/ingesta_neurobit` y `/correos/status` para el consumo del frontend [217].
* **Mapeo de Red:** Sus endpoints son expuestos por el `APIEndpointManager` en localhost [217, 220].

---

## 5. Dependencias y Colaboración
* **Dependencias Estándar:** `json`, `datetime`, `pathlib`.
* **Colaboración Directa:**
  * **Hereda de:** `BaseAdapter` [217, 219].
  * **Interactúa con:** `neurobit_dispatcher.py` (Oficina de Correos) de forma asíncrona a través del filesystem (`buzon_salida/`) [217].
  * **Alimentado por:** la extensión del navegador (`background.js` / `copy_listener.js`) que envía las capturas del portapapeles o teclado [189, 190].

---

## 6. Variables Estáticas y Tensiones de Ruta
* **Variables Estáticas:** El directorio de entrega `buzon_salida/` históricamente se definía con rutas relativas frágiles [590]. WRIL ancla y resuelve canónicamente esto asegurando que el adaptador apunte siempre a la raíz operativa de la ECN [123].
* **Tensiones de Orfandad Históricas:** En compendios antiguos, este adaptador carecía de cabeceras MFN y vivía suelto en bandejas de entrada, lo que causaba ModuleNotFoundErrors [11].

---

## 7. Diagrama de Flujo del Envío VFS
```text
  [ Ingesta HTTP (Flask) ] ──► AdapterCorreos.execute()
                                     │
                                     ▼ (Escribe archivo atómico)
                           [ buzon_salida/carta_XYZ.txt ]
                                     │
                                     ▼ (Kernel de Linux levanta señal)
                                 [ inotify ]
                                     │
                                     ▼ (Despierta)
                           [ neurobit_dispatcher.py ]
```