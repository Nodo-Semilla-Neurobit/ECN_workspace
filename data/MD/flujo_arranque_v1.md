# FLUJO DE ARRANQUE NORMATIVO v1 — ECN v3.2
## 1. Etapas (entry point · verificador · sello · capa)
| # | Etapa | Entry point | Verificador | Sello | Capa |
|---|---|---|---|---|---|
| 0 | ANCLA | ecn_root_detect.sh / wril_self_root.detectar_raiz() | raíz canónica | [✓ RAIZ] | L0 |
| 1 | CENSO | ecn_artifact_check + ecn_parser_extract + indice_compendio | listas .lst + compendio_base | [✓ CENSO] | L1 |
| 2 | AISLAMIENTO | python3 -m venv .venv + ecn_dependencies.cfg | system_deps_check.txt | [✓ VENV] (m2) | L2 |
| 3 | SANEA | wril_bootstrap + wril_topologia (dry→apply) | tensión ↓ (LEY 3) | [✓ WRIL] (m7,m8) | L3 |
| 4 | PERMISOS | deploy_neurobit_perms.sh (una sola vez) | id -nG input | [✓ UDEV] | L4 |
| 5 | RED | port_lighthouse + despertador_hub + levantar_puente | api_port.identity | [✓ FARO]/[✓ PUENTE] (m4_5,m4_6) | L4 |
| 6 | ORQUESTA | deploy_neurobit_estacion_v3.2.sh | estado_real.json | [✓ HUB] 4/4 (m5) | L5,L6 |
| 7 | VERIFICA | test_integracion_matriz + wril_estado_real | [✓ ARCA] + 4/4 ALIVE | [✓ TEST] | L6 |
| 8 | PEDAGOGÍA | consola verde / awaken_ceremony | rango ascendente | [✓ RANGO] | L7 |
| H | HALT | Ctrl+C / kill -INT | sin huérfanos | 0.0% CPU | — |

## 2. Diagrama esquemático de operación
```text
        membrana de entrada: consola verde(ws8080) · juego · inbox/
                              │ verbo / carta / artefacto
        ┌─────────────────────▼──────────────────────┐
        │ WRIL·SENTINEL (ROUTE): declaración→resguarda│
        │        →MOVE→historial                      │
        └──────┬──────────────────────────┬──────────┘
   artefacto   │                          │ carta sellada
        ┌──────▼───────┐          ┌───────▼────────┐
        │ TERRITORIO   │          │ BUZÓN→DISPATCH │
        │ path_map +   │          │ →postman→ARCA  │
        │ ciclo WRIL:  │          │ (memoria_eva)  │
        │ DISCOVER→    │          └────────────────┘
        │ RESOLVE→     │
        │ RECONCILE→   │
        │ VERIFY→RECORD│
        └──────┬───────┘
               │ identidad/ubicación
        ┌──────▼───────────────────────────────────┐
        │ FARO port_lighthouse → api_port.identity │
        │ CORE 5000-9 · EXT 5010-9 · TOOLS 5020-9  │
        └──────┬───────────────────────┬───────────┘
        ┌──────▼───────┐       ┌───────▼────────┐
        │ HUB API 5000 │       │ PUENTE ws 8080 │
        │ connector→   │       │ → consola/juego│
        │ endpoint_mgr │       └───────┬────────┘
        └──────┬───────┘               │ reflejo
               │ endpoints dinámicos   ▼
        ┌──────▼───────────────────────────────────┐
        │ ADUANA·SUPERPARSER·MEDIADORES            │
        │ capacidad→compartimento→módulo→línea→    │
        │ despacho a inbox/<solicitante>/          │
        └──────────────────────────────────────────┘
```

## 3. Clasificación de la lista base (capa→etapa→órgano)
| Capa | Artefactos | Etapa | Órgano que la consume |
|---|---|---|---|
| L0 | ecn_root_detect.sh · wril_self_root · wril_leyes | 0 | todo el sistema (ancla) |
| L1 | ecn_artifact_check · ecn_parser_extract · ecn_create_system_file · indice/ingest_compendium | 1 | Superparser / instalador |
| L2 | ecn_install.sh · ecn_basic_modules.cfg · ecn_dependencies.cfg · backend_instalador_ludico | 2 | instalador lúdico |
| L3 | wril_backup · path_map · path_resolver · mfn_registry · sentinel · topologia · bootstrap · dependency_scanner | 3 | WRIL (ciclo) |
| L4 | port_lighthouse · despertador_hub · levantar_puente · puente_consola_ws_v2.js | 5 | Faro / puente / consola |
| L5 | neurobit_api · module_connector · api_endpoint_manager · adapters/base | 6 | Hub / orquestación |
| L6 | neurobit_dispatcher · clipboard_core · dictado_evdev | 6,7 | circulación / dictado |
| L7 | consola_verde · pantalla_2 · observatorio · aduana_evidencia · neurobit_aula · INSTRUCCIONES · MANUAL | 8 | pedagogía / render |

## 4. Ciclo de vida del parche (automatizado por inbox)
inbox/<parche> → Aduana verifica (anclas/firma) → apply con backup → verify (py_compile+test)
→ ÉXITO: ruta el parche a su hogar declarado (MFN_LOCATION) o a archive/historical/parches/ si es de un solo uso; **inbox queda limpio** (carta entregada); asienta rubrica+historial.
→ FALLO: cuarentena/ + carta de tensión; inbox retiene.

## 5. Memoria quieta (patrones de saneo, archivar no borrar)
backups encadenados `*_20\d{6}_\d{6}*` · editor `*~` · respaldos de parche `*.pre_*` · duplicados `-D` ya resueltos · borradores `-v0`.

