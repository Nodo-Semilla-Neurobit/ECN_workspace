# 🔮 MANUAL DE RECONCILIACIÓN TOPOLÓGICA Y CAPA WRIL

En la Estación Central Neurobitrónica (ECN), la tensión entre **Declaración y Realidad** (Declaración ≠ Realidad) no se considera un fallo de programación, sino la brújula territorial que guía la sanación del espacio físico en disco [14, 1378, 1390]. 

Este manual describe el funcionamiento de la capa **WRIL (Workspace Resolution & Integrity Layer)** y las intervenciones quirúrgicas para sanar la deuda tipográfica de tu raíz [7, 31].

---

## 🗺️ 1. Filosofía de Autonomía de Ruta: El Alias `ECN_ROOT`
El software corporativo tradicional se rompe cuando cambias el nombre de una carpeta o la mueves de directorio, porque depende de rutas absolutas rígidas (*hardcoded*) escritas en el código [39, 1390]. 

La capa WRIL erradica esto mediante dos mecanismos soberanos:
1. **`wril_self_root.py` (Capa 0):** Resuelve dinámicamente la ubicación física del software ascendiendo por el árbol de directorios hasta encontrar los marcadores atómicos `buzon_salida/` y `pids/` [14, 453, 1347, 1348].
2. **`wril_root_alias.py`:** Mapea el alias canónico `ECN_ROOT` en la memoria del intérprete de Python, independizando el ecosistema de cualquier ruta física ruidosa o con caracteres especiales [1342].

---

## ⚠️ 2. Auditoría Forense de Discrepancias Activas (Tensiones de Fase 1)

Hemos detectado tres picos de tensión en la topología de archivos que colapsan el arranque automático de la ECN si no se reconcilian [7]:

### A. Desplazamiento de Módulos WRIL
* **Declaración (Header MFN):** `MFN_LOCATION: INSTALACION_ [706, 1287]
* **Realidad del disco:** 16 archivos de control WRIL (incluyendo `wril_sentinel.py`, `wril_path_resolver.py`, `wril_bootstrap.py`) viven sueltos en el directorio raíz de la instalación.
* **Tensión:** El resolvedor dinámico entra en conflicto al intentar localizarlos, interpretando el descalce como una señal de corrupción territorial.

### B. Rutas Fantasma en `path_map.json`
* **Realidad del disco:** El índice autogenerado `path_map.json` contiene referencias duplicadas que apuntan al subdirectorio inexistente `/wril/wril/` (ej. `/home/gus/.../wril/wril/wril_sentinel.py`) [1335].
* **Tensión:** Cualquier importación dinámica asíncrona lanzada por el `APIEndpointManager` fallará con un `ModuleNotFoundError` [11, 1335].

### C. Paréntesis Parásito en Contrato de Módulos
* **Realidad del disco:** El archivo de configuración de nivel 9 fue guardado físicamente bajo el nombre malformado `declaracion_modulos_v9.yaml)` (con un paréntesis colgado al final) [313, 621].
* **Tensión:** El parser YAML de Python aborta el arranque al no poder localizar el contrato base de los adaptadores de la estación [11, 313, 621].

---

## 🛠️ 3. El Ritual de Reconciliación (Plan de Saneamiento)

Para llevar la tensión topológica a cero absoluto, debes ejecutar de manera secuencial los siguientes pasos en tu terminal local [1363]:

1. **Corregir el nombre del contrato YAML:**
   ```bash
   mv "inbox/declaracion_modulos_v9.yaml)" "inbox/declaracion_modulos_v9.yaml"
   ```
   
2. **Correr el Pliegue Topológico (Dry-Run):**
   Verifica qué archivos serán movidos y repatriados a su destino canónico sin realizar modificaciones directas [1363, 1365]:
   ```bash
   python3 wril/wril_topologia.py
   ```
   
3. **Aplicar el Pliegue Físico:**
   Materializa los cambios en el disco. Esto moverá los módulos sueltos a `/wril/` y purgará los archivos `.pid` obsoletos de ejecuciones muertas en `pids/` [7, 1363, 1365]:
   ```bash
   python3 wril/wril_topologia.py --apply
   ```
   
4. **Regenerar el Mapa Canónico:**
   Fuerza un re-escaneo limpio del disco para actualizar las rutas físicas reales en el archivo SRAM de transiciones [1335]:
   ```bash
   python3 wril/wril_path_map.py
   ```

Una vez completado el ritual, la tensión en el visor del censo pasará instantáneamente de **[⚠ TÉNSION: DESPLAZADO]** a **[✓ COHERENCIA VERIFICADA]** en color verde fósforo [14].