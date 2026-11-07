# 10_adapter_centinela.md — Puente del Monitor del Sistema

## 1. Identidad Declarativa y Ubicación
* **Archivo:** `adapter_centinela.py`
* **Ubicación Canónica Declarada:** `core/adapters/`
* **Ubicación Real:** `core/adapters/`
* **Nivel MFN:** `1`
* **Firma de Ubicación MFN:** `### MFN_LOCATION: core/adapters/`
* **Identificación de Orfandad:** **Verificado (Tiene cabecera MFN)**

---

## 2. Propósito y Lógica Operacional
Es el puente operativo encargado de sincronizar el estado del monitor pasivo de la estación (`centinela_monitor.py` o sus procesos de monitoreo) con el Hub Dinámico [215, 216].

Su lógica principal consiste en actuar como interfaz de lectura/escritura no destructiva sobre los indicadores de salud del sistema [215]. Lee un archivo físico inmutable de estado (`.centinela_state`) ubicado en el directorio de datos runtime (`data/`) de la ECN [215]. Este archivo registra los PIDs de los daemons vivos, los consumos instantáneos de recursos y el censo de procesos [215, 247].

Al encapsular el acceso al disco en una clase aislada que hereda de `BaseAdapter`, evita que el `APIEndpointManager` tenga que conocer la ubicación de las variables de runtime del disco, preservando el principio de modularidad estricta [215, 219, 220].

---

## 3. Estructura de Métodos y Funciones
* **`class AdapterCentinela(BaseAdapter)`**:
  * **`execute(self, payload: Dict[str, Any]) -> Dict[str, Any]`**: Lee el estado de los procesos activos desde el disco y retorna la matriz de disponibilidad [215]. Si se le solicita una acción (como revivir un proceso muerto), ejecuta los comandos correspondientes de forma secuencial segura.
  * **`input_schema(self)`**: Espera peticiones de consulta o comandos de control (`status`, `revive`, `target`).
  * **`output_schema(self)`**: Retorna el mapa detallado de salud de los procesos (ALIVE, DEAD, STALE) [247].

---

## 4. Endpoints y Conectividad
* **Endpoints HTTP:** Expone de forma lógica la ruta `/centinela/status` para el tablero y observador visual GTK [9].
* **Mapeo de Red:** Consumido localmente por el Observatorio GTK o la Consola de Fósforo Verde HTML a través del puerto de la API central [172].

---

## 5. Dependencias y Colaboración
* **Dependencias Estándar:** `json`, `subprocess`, `sys`, `pathlib`.
* **Colaboración Directa:**
  * **Consume datos de:** `data/.centinela_state` [215].
  * **Colabora con:** `neurobit_dispatcher.py` (para rastrear el cartero) y `wril_estado_real.py` (para auditar si hay inconsistencias territoriales) [247].

---

## 6. Variables Estáticas y Tensiones de Ruta
* **Constante del Archivo de Estado:** La ruta sagrada `.centinela_state` se localiza mediante resolver dinámico utilizando la constante de ancla de WRIL `ROOT = Path(__file__).resolve().parents[2]` [215]. Esto evita la deriva histórica del directorio de datos [122].
* **Tensiones del Duplicado Centinela:** Existe una versión legacy (`adapter_centinela_legacy.py`) que solía mapear protocolos WebSocket más pesados, pero fue congelada en favor de este adaptador directo para erradicar ciclos ociosos de red [216, 258].

---

## 7. Diagrama de Flujo del Estado
```text
  [ Petición /centinela/status ] ──► execute()
                                           │
                                           ▼ (Lectura autónoma sin loops)
                                 [ data/.centinela_state ]
                                           │
                                           ▼ (Procesa y valida)
                                  [ JSON de Retorno ]
```