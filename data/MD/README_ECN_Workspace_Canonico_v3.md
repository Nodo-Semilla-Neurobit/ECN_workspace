# ECN — Estación Central Neurobitrónica
## README de Arranque — Workspace Canónico v3

> Documento modelo de orientación inicial. No sustituye las declaraciones YAML ni los headers MFN de los módulos.

## 1. Propósito

La ECN es el entorno local de integración y orquestación del sistema Neurobit.

Principios operativos: localhost-first, modularidad, bajo acoplamiento, identidad declarativa, resolución dinámica, trazabilidad y verificación antes de ejecución.

WRIL mantiene la correspondencia entre identidad declarada, ubicación física, dependencias y referencias internas.

Ciclo rector:

`DISCOVER → RESOLVE → RECONCILE → VERIFY → RECORD`

WRIL no debe convertirse en un supermódulo: cada componente responde una pregunta diferente.

## 2. Regla del workspace

Existe una única topología canónica de ejecución.

Los artefactos históricos, backups y generaciones superadas no forman parte del runtime canónico.

Antes de retirar físicamente un artefacto:

1. identificarlo;
2. clasificarlo;
3. determinar dependencias activas;
4. registrar la decisión;
5. conservarlo en histórico si corresponde;
6. verificar el workspace.

No se elimina historia sin registro.

## 3. Estructura raíz modelo

```text
ECN-ESTADO_ACTUAL/
├── README.md
├── deploy_neurobit_estacion_v3.2.sh
├── deploy_neurobit_perms.sh
├── ECN.desktop
├── core/
│   ├── neurobit_api.py
│   ├── module_connector.py
│   ├── api_endpoint_manager.py
│   └── neurobit_dispatcher.py
├── adapters/
│   ├── base.py
│   ├── adapter_centinela.py
│   ├── neurobit_adapter_gtk.py
│   └── ...
├── wril/
│   ├── wril_sentinel.py
│   ├── wril_path_map.py
│   ├── wril_path_resolver.py
│   ├── wril_mfn_registry.py
│   ├── wril_patch_resolver.py
│   ├── wril_dependency_scanner.py
│   ├── wril_dynamic_tester.py
│   ├── wril_topologia.py
│   ├── wril_bootstrap.py
│   └── wril_estado_real.py
├── data/
│   ├── metadata.json
│   ├── declaracion_modulos.yaml
│   ├── declaracion_adaptadores.yaml
│   ├── module_spec.yaml
│   ├── secuencia_verificacion_ensamble.yaml
│   └── runtime/
│       ├── path_map.json
│       ├── memoria_eva.jsonl
│       ├── wril_historial.jsonl
│       └── estado_real.json
├── docs/
│   ├── tesis/
│   ├── arquitectura/
│   ├── protocolos/
│   ├── informes/
│   └── historial/
├── extensions/
├── tools/
├── inbox/
├── pids/
└── archive/
    ├── legacy/
    ├── backups/
    └── migraciones/
```

Esta estructura es un modelo de destino. La topología real debe obtenerse primero mediante auditoría y dry-run WRIL.

## 4. Núcleo `core/`

`neurobit_api.py`: punto de entrada de la API local.

`module_connector.py`: descubrimiento y carga dinámica de módulos/adaptadores.

`api_endpoint_manager.py`: administración de endpoints. No contiene lógica de negocio.

`neurobit_dispatcher.py`: despacho interno hacia el procesador correspondiente.

El core debe permanecer pequeño.

## 5. WRIL

`wril_sentinel.py` — `ROUTE`: observa y enruta.

`wril_path_map.py` — `INDEX`: construye el estado indexado del filesystem.

`wril_path_resolver.py` — `RESOLVE`: localiza recursos.

`wril_mfn_registry.py` — `IDENTITY`: interpreta la identidad declarada.

`wril_patch_resolver.py` — `RECONCILE`: detecta y repara referencias obsoletas.

`wril_dependency_scanner.py` — `DEPENDENCY`: determina requisitos.

`wril_dynamic_tester.py` — `VERIFY`: comprueba comportamiento.

`wril_topologia.py` — `RECONCILE TOPOLOGY`: armoniza declaración y territorio.

`wril_bootstrap.py` — inicialización controlada.

`wril_estado_real.py` — lectura del estado observable.

La distinción fundamental es:

`PATH MAP ≠ FILESYSTEM`

`MFN REGISTRY ≠ PATH MAP`

`HISTORIAL ≠ ESTADO ACTUAL`

La documentación WRIL define precisamente estas fronteras y el ciclo `Discover → Resolve → Reconcile → Verify → Record`. fileciteturn2file17L1-L1

## 6. `adapters/`

Los adaptadores representan interfaces hacia dominios externos al núcleo.

Regla:

`CORE no conoce detalles internos del adaptador.`

El adaptador implementa el contrato requerido por el core.

## 7. `data/`

Separar:

- declaraciones;
- datos de runtime;
- historial.

No confundir estado derivado con estado físico real.

## 8. `docs/`

```text
docs/
├── tesis/
├── arquitectura/
├── protocolos/
├── informes/
└── historial/
```

Debe distinguirse documentalmente entre hecho observado, decisión de diseño, hipótesis e interpretación conceptual.

## 9. Scripts `.sh`

Debe existir una única autoridad operacional para el despliegue vigente.

Según el estado actual, `deploy_neurobit_estacion_v3.2.sh` es el maestro vigente; las generaciones anteriores aparecen clasificadas como históricas. fileciteturn2file4L1-L1

No se deben borrar automáticamente. Primero se auditan dependencias y luego se trasladan al archivo histórico.

## 10. Procedimiento educativo de reconstrucción

Cada etapa genera un informe de resultados antes de pasar a la siguiente.

### ETAPA 0 — Congelación

Fotografiar el workspace actual:

- árbol;
- procesos;
- `.sh`;
- versiones;
- YAML;
- duplicados;
- backups;
- referencias sospechosas.

Resultado: `informe_00_estado_inicial.md`

No modificar todavía.

### ETAPA 1 — Clasificación

Clasificar cada artefacto como:

`CANÓNICO / HISTÓRICO / BACKUP / REDUNDANTE / LEGACY / PENDIENTE / DESCONOCIDO`

Resultado: `informe_01_clasificacion.md`

### ETAPA 2 — Identidad

Comparar:

`MFN_LOCATION` ↔ ubicación física

y verificar también:

`MFN_LEVEL / MFN_COORD / VERSION`

Resultado: `informe_02_identidad.md`

### ETAPA 3 — Dependencias

Construir:

`módulo → importaciones → scripts → endpoints → procesos`

No retirar archivos antes de conocer sus consumidores.

Resultado: `informe_03_dependencias.md`

### ETAPA 4 — Canonización de `.sh`

Principio:

`UNA FUNCIÓN → UN SCRIPT AUTORITATIVO`

Resultado: `informe_04_scripts.md`

### ETAPA 5 — Workspace canónico

Construir la topología destino.

Orden obligatorio:

`ESTRUCTURA → MOVE/RECONCILE → VERIFY`

Resultado: `informe_05_workspace_canonico.md`

### ETAPA 6 — WRIL dry-run

Obtener exactamente qué transformaría WRIL sin aplicar modificaciones.

Resultado: `informe_06_wril_dry_run.md`

### ETAPA 7 — Reconciliación

Aplicar únicamente cambios aprobados.

Registrar:

`ORIGEN → CAMBIO → BACKUP → DESTINO → RESULTADO`

Resultado: `informe_07_reconciliacion.md`

### ETAPA 8 — Reindexación

Regenerar `path_map.json`.

Resultado: `informe_08_reindexacion.md`

### ETAPA 9 — Bootstrap

Ejecutar:

`dependency scan → bootstrap`

Resultado: `informe_09_bootstrap.md`

### ETAPA 10 — Verificación

Comprobar importaciones, procesos, API, endpoints, adaptadores, WRIL, herramientas e interfaces.

Resultado: `informe_10_verificacion.md`

### ETAPA 11 — Estado real

Distinguir:

`DECLARADO / DETECTADO / EJECUTADO / VERIFICADO`

Resultado: `informe_11_estado_real.md`

## 11. Plantilla de cada informe

```text
ETAPA:
OBJETIVO:
ENTORNO:
FUENTE:
OPERACIÓN:
RESULTADO:
ERRORES:
ADVERTENCIAS:
CAMBIOS:
BACKUPS:
PENDIENTES:
SIGUIENTE ETAPA:
```

El Director ejecuta y trae el resultado. El análisis se realiza sobre evidencia de campo, no sobre una suposición de éxito.

## 12. Regla de comunicación

`EJECUTAR → INFORMAR → ANALIZAR → DECIDIR → APLICAR → VERIFICAR`

Esta secuencia permite que el proceso sea simultáneamente técnico y educativo.

## 13. Neurobit Protocol

La especificación establece:

`INTENCIÓN → ACTION_WORD → CLASS → PAYLOAD → VALIDACIÓN → DESPACHO → EJECUCIÓN → REGISTRO`

El parser debe validar estructura, identidad, clase, payload y anidamiento antes de entregar el contenido al procesador. fileciteturn2file18L1-L1

Para la reconstrucción de la ECN aplicamos el mismo principio metodológico:

`DECLARAR → VALIDAR → EJECUTAR → REGISTRAR`

## 14. Criterio de finalización

La reconstrucción termina cuando:

- existe una única topología canónica;
- existe una única entrada operacional vigente;
- no existen duplicados activos injustificados;
- los headers MFN coinciden con la topología;
- las dependencias están identificadas;
- WRIL puede reconstruir el mapa;
- el bootstrap es reproducible;
- la API puede verificarse;
- los endpoints responden según contrato;
- el estado real puede consultarse;
- la historia de migración permanece preservada.

El objetivo no es solamente un workspace limpio.

El objetivo es un workspace **comprensible, reproducible y verificable**.

## 15. Estado de reconstrucción

```text
[ ] ETAPA 0 — Congelación
[ ] ETAPA 1 — Clasificación
[ ] ETAPA 2 — Identidad
[ ] ETAPA 3 — Dependencias
[ ] ETAPA 4 — Scripts
[ ] ETAPA 5 — Workspace canónico
[ ] ETAPA 6 — WRIL dry-run
[ ] ETAPA 7 — Reconciliación
[ ] ETAPA 8 — Reindexación
[ ] ETAPA 9 — Bootstrap
[ ] ETAPA 10 — Verificación
[ ] ETAPA 11 — Estado real
```

## 16. Principio rector

> **El workspace debe poder explicar su propio estado.**

La ECN no debería depender de que una persona recuerde dónde está cada módulo.

La declaración, el índice, el resolver, el registro, los contratos y los informes deben permitir reconstruir la situación del sistema.
