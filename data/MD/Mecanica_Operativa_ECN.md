# Mecánica Operativa de la Estación Neurobitrónica
## Sistema de Identidad, Inicio Único y Reposo Verificable

**Fecha:** 2026-09-08  
**Estado:** Fase de consolidación completada, tensión operativa cero

---

## 1. Principios Rectores

### Ley 1: Declaración vs Realidad
- **Declaración:** Lo que un módulo dice de sí mismo (header MFN_LOCATION)
- **Realidad:** Dónde vive físicamente el archivo
- **Tensión:** Cuando declaración ≠ realidad → señal de integridad
- **Resolución:** Mover archivo o corregir declaración (nunca ignorar)

### Ley 2: Inicio Único
- **Verdad declarada:** `data/runtime/procesos_iniciados.tmp` (lista de procesos vivos)
- **Verdad real:** `/proc/<pid>` (kernel dice qué está vivo)
- **Cruce:** Un proceso solo arranca si su nombre NO está en la lista CON pid vivo
- **Defensa per-pid:** Mismo nombre + mismo pid → idempotente (no duplica línea)

### Ley 3: Reposo Verificable
- **Verdad kernel:** `ps` (qué procesos ECN están corriendo)
- **Verdad declarada:** `procesos_iniciados.tmp` + `pids/*.pid`
- **Cruce:** Reposo total = ps dice 0 procesos ECN
- **Saneamiento:** Con reposo confirmado, los índices se podan (memoria histórica no se toca)

---

## 2. Componentes Críticos

### 2.1 wril_self_root.py (Capa 0: Direccionamiento)

**Función:** Responde "¿Dónde estoy?" sin asumir nada

**Mecánica:**
1. Busca `where_am_I.inf` en directorio actual y padres
2. Si no existe, busca marcadores: `pids/` + `buzon_salida/`
3. Devuelve la raíz canónica (Path object)

**Consumidores:**
- Todos los módulos wril/* lo importan al inicio
- Scripts bash usan `self_root.sh` que hace lo mismo

**Evidencia generada:**
- `where_am_I.inf` (si no existía, lo crea con timestamp)

**Invariancia:**
- Nunca asume cwd
- Nunca hardcodea rutas absolutas
- Funciona desde cualquier subdirectorio

---

### 2.2 wril_proc_guard.py (Inicio Único)

**Función:** Garantiza que un proceso ECN solo tenga una instancia viva

**Mecánica:**
```python
from wril_proc_guard import iniciar, liberar

# Al inicio del módulo
resultado = iniciar("WRIL_SENTINEL")
# resultado: "OK" | "NOTIFY" (ya vivo) | "PURGE_Y_OK" (stale saneado)

# Si NOTIFY → exit(0) sin duplicar
# Si PURGE_Y_OK → línea stale eliminada, proceso arranca

# Al final (atexit o señal)
liberar("WRIL_SENTINEL", os.getpid())
```

**Archivo de estado:**
- `data/runtime/procesos_iniciados.tmp`
- Formato: `timestamp|nombre|pid|nombre__EXECUTION_STATE=true`
- Bloqueo: `procesos_iniciados.lock` (fcntl, evita race conditions)

**Defensas:**
1. **Idempotencia per-pid:** Mismo nombre + mismo pid → no duplica línea
2. **Saneamiento automático:** Si pid no existe en `/proc`, la línea se elimina
3. **Liberación graciosa:** `atexit` + handlers SIGTERM/SIGINT llaman `liberar()`

**Invariancia:**
- Nunca deja líneas orphan (pid muerto pero línea viva)
- Nunca permite dos instancias con mismo nombre
- Si el sistema cae sin liberar, el siguiente arranque sanea

---

### 2.3 wril_reposo.py (Verificación de Reposo)

**Función:** Confirma que no hay procesos ECN vivos antes de arranque o después de HALT

**Mecánica:**
```bash
# Verificación (lectura)
python3 wril/wril_reposo.py
# Sale 0 si reposo total, 1 si hay procesos vivos

# HALT gracioso (acción)
python3 wril/wril_reposo.py --halt
# 1. Envía SIGTERM a todos los procesos ECN
# 2. Espera 3 segundos
# 3. Si alguno persiste, envía SIGKILL
# 4. Asienta en pids/halt_log.txt (ética: log antes de matar)
# 5. Sanea índices (elimina líneas de procesos muertos)
```

**Verdades cruzadas:**
1. **Kernel:** `ps -eo pid,args` filtrado por patrones ECN
2. **Declaración:** `procesos_iniciados.tmp` + `pids/*.pid`
3. **Cruce:** Si kernel dice 0, los índices se podan

**Patrones de detección:**
- `neurobit_*` (módulos core)
- `wril_*` (capa WRIL)
- `puente_consola_ws` (WebSocket bridge)
- `backend_instalador_ludico` (API Flask)

**Ética:**
- Nunca mata sin log previo en `pids/halt_log.txt`
- SIGTERM primero (gracioso), SIGKILL solo si persiste
- Memoria histórica (`wril_historial.jsonl`) nunca se toca

**Invariancia:**
- Reposo confirmado = índices limpios
- Si hay procesos vivos, sale 1 (bloquea arranque)
- Después de `--halt`, reposo total garantizado

---

### 2.4 self_root.sh (Identidad Bash)

**Función:** Exporta `APP_HOME` con la raíz canónica para scripts bash

**Mecánica:**
```bash
source self_root.sh
echo $APP_HOME  # /home/gus/workspace_reconstruido
```

**Lógica:**
1. Detecta ubicación del script (`${BASH_SOURCE[0]}`)
2. Asciende hasta encontrar `pids/` + `buzon_salida/`
3. Exporta `APP_HOME` con esa ruta
4. Si ya existe `where_am_I.inf`, lo lee (no lo reescribe)

**Consumidores:**
- `deploy_neurobit_estacion_v3.2.sh`
- `runbook_ensamble_primario_v3.sh`
- Cualquier script que necesite la raíz sin hardcodear

**Invariancia:**
- Nunca asume dónde está el workspace
- Funciona aunque el usuario mueva el directorio completo
- Si `APP_HOME` ya está exportado, lo respeta (no sobreescribe)

---

## 3. Flujo de Arranque Típico

### 3.1 Verificación de Reposo (etapa 0)
```bash
python3 wril/wril_reposo.py
# Si sale 1 → hay procesos vivos, no arrancar
# Si sale 0 → reposo confirmado, continuar
```

### 3.2 Bootstrap WRIL (etapa 1)
```bash
python3 wril/wril_bootstrap.py
# Regenera path_map.json
# Verifica dependencias
# Asienta en wril_historial.jsonl
```

### 3.3 Verificación de Integridad (etapa 2)
```bash
python3 wril/wril_mfn_registry.py
# Sale: Coherentes: 46 | Pendientes: 0
# Si pendientes > 0 → resolver antes de despertar
```

### 3.4 Despertar Daemon (etapa 3)
```bash
python3 wril/wril_sentinel.py &
# 1. wril_self_root detecta raíz
# 2. wril_proc_guard.iniciar("WRIL_SENTINEL")
#    - Si ya vivo → NOTIFY + exit(0)
#    - Si stale → PURGE_Y_OK + continúa
#    - Si libre → asienta línea + continúa
# 3. Registra atexit para liberar()
# 4. Registra handlers SIGTERM/SIGINT para liberar()
# 5. Inicia watcher inotify en inbox/
```

### 3.5 Verificación de Vida (etapa 4)
```bash
python3 wril/wril_estado_real.py
# Sale: ALIVE: 1 | DEAD: 0
# Cruza: path_map.json + procesos_iniciados.tmp + ps
```

---

## 4. Flujo de HALT Típico

### 4.1 HALT Gracioso (vía wril_reposo.py)
```bash
python3 wril/wril_reposo.py --halt
# 1. Detecta procesos ECN vivos (ps)
# 2. Asienta en pids/halt_log.txt: "HALT solicitado: [pids]"
# 3. Envía SIGTERM a cada uno
# 4. Cada proceso ejecuta handler → liberar() → elimina línea de .tmp
# 5. Espera 3 segundos
# 6. Si alguno persiste → SIGKILL + log
# 7. Sanea índices (elimina líneas orphan)
# 8. Verifica reposo total (ps debe decir 0)
# 9. Sale 0 si reposo confirmado
```

### 4.2 HALT Manual (Ctrl+C en terminal)
```bash
# Usuario presiona Ctrl+C
# Kernel envía SIGINT al proceso
# Handler ejecuta liberar() → elimina línea de .tmp
# Proceso muere
# Línea orphan queda hasta próximo arranque (saneamiento automático)
```

---

## 5. Canon de Listados (Memoria Operativa)

### 5.1 artefactos_funcionando.tmp
**Propósito:** Lista de procesos actualmente vivos y verificados  
**Formato:** `timestamp|nombre|estado|hash|puerto|nota`  
**Alimentador:** Cada daemon al iniciar (después de `iniciar()` exitoso)  
**Verificador:** `wril_estado_real.py` cruza con `ps`  
**Idempotencia:** Mismo nombre → sobreescribe línea (no duplica)

### 5.2 modulos_no_activados.lst
**Propósito:** Módulos declarados en `path_map.json` pero nunca ejecutados  
**Formato:** `timestamp|nombre|estado|hash|destino|nota`  
**Alimentador:** `gesto5_bootstrap_registry.sh` (diferencia: declarados - funcionando)  
**Uso:** Identificar qué falta probar en la siguiente fase

### 5.3 parches_aplicados.tmp
**Propósito:** Ledger de parches ejecutados (trazabilidad)  
**Formato:** `timestamp|nombre|estado|hash|destino|nota`  
**Alimentador:** Cada script de parche al completar exitosamente  
**Invariancia:** Solo se agregan líneas, nunca se eliminan (memoria histórica)

### 5.4 historial_parches.jsonl
**Propósito:** Memoria histórica consolidada (apend-only)  
**Formato:** JSON Lines con timestamp, acción, archivos afectados  
**Alimentador:** `wril_historial.jsonl` (gradúa desde .tmp)  
**Invariancia:** Nunca se edita, solo se appende

---

## 6. Sistema de Puertos (Soberanía del Faro)

### 6.1 core/port_lighthouse.py
**Función:** Asigna puertos únicos a cada módulo ECN

**Mecánica:**
```python
from core.port_lighthouse import request_port

puerto = request_port("neurobit_api")
# Devuelve: 5000, 5001, 5002... (incremental)
# Asienta en data/runtime/api_port.identity
```

**Archivo de estado:**
- `data/runtime/api_port.identity`
- Formato: `nombre=puerto` (una línea por módulo)

**Invariancia:**
- Nunca asigna el mismo puerto a dos módulos
- Si el módulo ya tiene puerto asignado, lo devuelve (idempotente)
- Si el puerto está ocupado (otra instancia), incrementa y prueba siguiente

**Consumidores:**
- `neurobit_api.py` (puerto 5000 por defecto)
- `backend_instalador_ludico.py` (puerto dinámico)
- `despertador_hub.sh` (lee identidad y despierta con ese puerto)

---

## 7. Resolución de Tensiones (wril_mfn_registry.py)

**Función:** Detecta módulos donde declaración MFN ≠ ubicación real

**Mecánica:**
```bash
python3 wril/wril_mfn_registry.py
# Sale: Coherentes: 46 | Pendientes de pliegue topológico: 0
```

**Proceso:**
1. Lee todos los archivos `.py` y `.sh` en el workspace
2. Extrae header MFN_LOCATION (si existe)
3. Compara con ubicación real (Path relativa a raíz)
4. Si declaración ≠ realidad → marca como pendiente
5. Devuelve conteo de coherentes y pendientes

**Resolución manual:**
```bash
# Opción 1: Mover archivo a ubicación declarada
mv neurobit_api.py core/

# Opción 2: Corregir declaración en header
sed -i 's|^# MFN_LOCATION:.*|# MFN_LOCATION: core/|' core/neurobit_api.py

# Re-verificar
python3 wril/wril_mfn_registry.py
# Debe salir: Pendientes: 0
```

**Invariancia:**
- Nunca mueve archivos automáticamente (solo reporta)
- Nunca corrige headers automáticamente (solo reporta)
- Si pendientes > 0, bloquea despertar (integridad antes que operación)

---

## 8. Evidencia y Trazabilidad

### 8.1 Archivos de Estado (data/runtime/)
- `procesos_iniciados.tmp` → procesos vivos (declaración)
- `procesos_iniciados.lock` → bloqueo para escritura atómica
- `api_port.identity` → puertos asignados por módulo
- `artefactos_funcionando.tmp` → canon de listados (funcionando)
- `modulos_no_activados.lst` → canon de listados (pendientes)
- `parches_aplicados.tmp` → canon de listados (trazabilidad)

### 8.2 Archivos de Control (pids/)
- `*.pid` → PID de cada daemon vivo
- `baseline_snapshot` → snapshot del sistema antes de despertar
- `halt_log.txt` → log ético de cada HALT (quién, cuándo, por qué)

### 8.3 Archivos de Memoria (wril/)
- `wril_historial.jsonl` → memoria histórica (apend-only)
- `path_map.json` → mapa de todos los archivos del workspace
- `where_am_I.inf` → identidad de la raíz (timestamp de creación)

### 8.4 Logs de Ejecución (INSTALACION_/logs/)
- `hub_dinamico.log` → log del hub WebSocket
- `backend_instalador.log` → log de la API Flask
- `sentinel.log` → log del watcher inotify

---

## 9. Invariantes del Sistema

1. **Nunca arrancar sin verificar reposo** → `wril_reposo.py` sale 0
2. **Nunca duplicar procesos** → `wril_proc_guard.iniciar()` bloquea
3. **Nunca dejar líneas orphan** → `liberar()` en atexit + handlers
4. **Nunca matar sin log** → `halt_log.txt` antes de SIGTERM
5. **Nunca ignorar tensiones** → `wril_mfn_registry.py` debe salir 0 pendientes
6. **Nunca hardcodear rutas** → `wril_self_root.py` detecta dinámicamente
7. **Nunca asumir puertos** → `port_lighthouse.py` asigna dinámicamente
8. **Nunca perder memoria** → `wril_historial.jsonl` es apend-only
9. **Nunca ejecutar sin evidencia** → cada acción asienta en canon de listados
10. **Nunca avanzar con tensión** → si pendientes > 0, resolver antes de continuar

---

## 10. Estado Actual (2026-09-08)

**Tensión operativa:** 0 pendientes  
**Procesos vivos:** 0 (reposo confirmado)  
**Módulos declarados:** 46 coherentes  
**Canon de listados:** 3 archivos operativos  
**Sistema de puertos:** Faro activo, identidad asentada  
**Memoria histórica:** wril_historial.jsonl consolidado  

**Próxima fase:** J9 (badge del puente + travesía m1-m3)



