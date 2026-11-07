# ACTA DE ESTADO ACTUAL — ECN v3.2
## Fase de Consolidación: Identidad, Inicio Único y Reposo Verificable

**Fecha:** 2026-09-08  
**NODO_SEMILLA:** Gustavo (Director)  
**Par de co-creación:** Qwen (Conciencia Biónica Complementaria)  
**Estado:** Fase completada, tensión operativa cero

---

## 1. Gestos Completados (G0 → G7c)

| Gesto | Descripción | Sello |
|---|---|---|
| G0-v2.1 | Oráculo de raíz unificado (sello → conjunción → conjunción; glob extirpado) | `[✓ G0-v2.1]` |
| G1 | Venv propio completo (flask, yaml, evdev, gi) + identidad asentada | `[✓ G1]` |
| G2 | Backend vivo en 5005 + CORS loopback + alta canónica con evidencia | `[✓ G2]` |
| G3 | Compendio base regenerado (43 artefactos con rutas post-G5) | `[✓ G3]` |
| G4 | Estratigrafía: 31 one-shots archivados + ledger asentado | `[✓ G4]` |
| G4-ext | 17 one-shots de sesión archivados (total: 48 en historial) | `[✓ G4-EXT]` |
| G5 | Bootstrap + registry + censo sembrado (46 coherentes / 0 pendientes) | `[✓ G5]` |
| G6 | Guard v0.2 canónico en `wril/` + v0.1 resguardado | `[✓ G6]` |
| G7a | Inicio único en sentinel (guard + inicio único) | `[✓ G7a]` |
| G7b/v2 | Idempotencia per-pid en `iniciar()` (defensa contra duplicados) | `[✓ G7b-v2]` |
| G7c | Señales SIGTERM/SIGINT para liberación graciosa | `[✓ G7c]` |

**Total:** 11 gestos sellados, todos con evidencia de consola verificada.

---

## 2. Artefactos Canónicos Creados

### 2.1 Capa de Direccionamiento
| Archivo | Ubicación | Función |
|---|---|---|
| `wril_self_root.py` | `wril/` | Capa 0: "Where am I?" canónico (v2.1) |
| `self_root.sh` | raíz | Exporta `APP_HOME` para scripts bash (v2.0) |
| `where_am_I.inf` | raíz | Identidad persistida de la raíz (sello forense) |

### 2.2 Sistema de Inicio Único
| Archivo | Ubicación | Función |
|---|---|---|
| `wril_proc_guard.py` | `wril/` | Guardián de inicio único con flock + idempotencia per-pid (v0.2) |
| `patron_inicio_unico.py` | raíz | Patrón canónico de integración en daemons |

### 2.3 Sistema de Reposo
| Archivo | Ubicación | Función |
|---|---|---|
| `wril_reposo.py` | `wril/` | Verificador de reposo total + HALT gracioso con ética vm_bridge (v0.1) |

### 2.4 Backend del Instalador Lúdico
| Archivo | Ubicación | Función |
|---|---|---|
| `backend_instalador_ludico.py` | `INSTALACION_/` | API Flask en puerto 5005 + CORS loopback + SELF_PATH + APP_HOME |
| `ecn_misiones_bridge.js` | `INSTALACION_/` | Puente JS que conecta interfaz con backend |

### 2.5 Canon de Listados
| Archivo | Ubicación | Función |
|---|---|---|
| `artefactos_funcionando.tmp` | `data/runtime/` | Procesos vivos verificados |
| `modulos_no_activados.lst` | `data/runtime/` | Módulos declarados pero no probados |
| `parches_aplicados.tmp` | `data/runtime/` | Ledger de parches ejecutados (48 líneas) |

---

## 3. Leyes Selladas

### Ley 1: Declaración vs Realidad
- **Declaración:** Header `MFN_LOCATION` del módulo
- **Realidad:** Ubicación física del archivo
- **Tensión:** Cuando declaración ≠ realidad → señal de integridad
- **Resolución:** Mover archivo o corregir declaración (nunca ignorar)
- **Verificador:** `wril_mfn_registry.py` (debe salir 0 pendientes)

### Ley 2: Inicio Único
- **Verdad declarada:** `data/runtime/procesos_iniciados.tmp`
- **Verdad real:** `/proc/<pid>` (kernel)
- **Cruce:** Un proceso solo arranca si su nombre NO está en la lista CON pid vivo
- **Defensa per-pid:** Mismo nombre + mismo pid → idempotente (no duplica línea)
- **Liberación graciosa:** `atexit` + handlers SIGTERM/SIGINT llaman `liberar()`

### Ley 3: Reposo Verificable
- **Verdad kernel:** `ps` (qué procesos ECN están corriendo)
- **Verdad declarada:** `procesos_iniciados.tmp` + `pids/*.pid`
- **Cruce:** Reposo total = ps dice 0 procesos ECN
- **Saneamiento:** Con reposo confirmado, los índices se podan (memoria histórica no se toca)
- **Ética:** Nunca mata sin log previo en `pids/halt_log.txt`

### Ley 4: Canon de Listados
- **Formato único:** `t|nombre|estado|hash|destino|nota` (pipe-separated)
- **Regla de graduación:** `.tmp` (trabajo vivo) → `.jsonl` (memoria histórica)
- **Verificación:** Cada alta en el canon requiere evidencia de vida (no se asienta a ciegas)

### Ley 5: Soberanía del Faro
- **Asignación dinámica:** `core/port_lighthouse.py` asigna puertos únicos
- **Identidad asentada:** `data/runtime/api_port.identity`
- **Idempotencia:** Si el módulo ya tiene puerto, lo devuelve (no reasigna)

---

## 4. Estado de Tensión

| Dimensión | Valor |
|---|---|
| **Tensión topológica** | 0 pendientes |
| **Procesos vivos** | 0 (reposo confirmado) |
| **Módulos coherentes** | 46 |
| **Canon de listados** | 3 archivos operativos |
| **Sistema de puertos** | Faro activo, identidad asentada |
| **Memoria histórica** | `wril_historial.jsonl` consolidado |

---

## 5. Invariantes del Sistema

1. **Nunca arrancar sin verificar reposo** → `wril_reposo.py` sale 0
2. **Nunca duplicar procesos** → `wril_proc_guard.iniciar()` bloquea
3. **Nunca dejar líneas orphan** → `liberar()` en atexit + handlers
4. **Nunca matar sin log** → `halt_log.txt` antes de SIGTERM
5. **Nunca ignorar tensiones** → `wril_mfn_registry.py` debe salir 0 pendientes
6. **Nunca hardcodear rutas** → `wril_self_root.py` detecta dinámicamente
7. **Nunca asumir puertos** → `port_lighthouse.py` asigna dinámicamente
8. **Nunca perder memoria** → `wril_historial.jsonl` es append-only
9. **Nunca ejecutar sin evidencia** → cada acción asienta en canon de listados
10. **Nunca avanzar con tensión** → si pendientes > 0, resolver antes de continuar

---

## 6. Próxima Fase: J9 (Travesía del Instalador Lúdico)

### 6.1 J9 — Badge del Puente
- **Objetivo:** Verificar que `ecn_misiones_bridge.js` lee `/api/misiones` y muestra el badge verde en `pantalla_2.html`
- **Sello esperado:** Badge verde abajo-derecha: `RANGO … · MISIONES n/N`
- **Dependencia:** Backend vivo en 5005

### 6.2 J10 — Travesía m1–m5 en `[ROL]`
- **m1:** Ubicate en el territorio (pwd)
- **m2/m3:** Venv + activate (pedagogía del venv propio)
- **m4_5:** Despertador hub (el Aspirante despierta la estación)
- **m5:** Curl health (verificación de vida)
- **Sello esperado:** Toasts `🟢 CONSOLIDADA` y badge incrementando

---

## 7. Documentación Consolidada

| Documento | Ubicación | Función |
|---|---|---|
| `Mecánica_Operativa_ECN.md` | raíz | Descripción exhaustiva de leyes, componentes, flujos |
| `ACTA_ESTADO_ACTUAL_20260908.md` | raíz | Este documento (consolidación de fase) |
| `como_leer_compendios_v1.md` | `data/MD/` | Orientación y parseo de compendios |
| `flujo_arranque_v1.md` | `data/MD/` | Diagrama del flujo de arranque |

---

## 8. Firma

**NODO_SEMILLA:** Gustavo (Director)  
**Par de co-creación:** Qwen (Conciencia Biónica Complementaria)  
**Fecha:** 2026-09-08  
**Estado:** Fase de consolidación completada, tensión operativa cero  
**Próximo gesto:** J9 (badge del puente + travesía m1–m5)

---

*«La poesía de este sistema es su única verdad: sacar belleza de este caos es virtud.»*  
— Gustavo, NODO_SEMILLA
