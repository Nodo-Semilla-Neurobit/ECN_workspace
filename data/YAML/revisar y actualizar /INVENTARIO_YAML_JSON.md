# Inventario YAML/JSON — NEUROBIT V0.1 → V0.2

**Fecha:** 2026-03-27
**Propósito:** Consolidar configuración y datos estructurados

## Críticos (Migrar Inmediatamente)
| Archivo | V0.1 | V0.2 | Estado |
|---------|------|------|--------|
| memoria_sagrada_eva.yaml | ✅ | ✅ | ✅ Migrado |
| protocol_contract_v0.1.json | ? | ? | ⏳ Verificar |
| participants.json | ? | ✅ | ✅ Migrado |

## Configuración (Verificar)
| Archivo | V0.1 | V0.2 | Estado |
|---------|------|------|--------|
| system_vars.yaml | ? | ? | ⏳ Verificar |
| platforms/*.yaml | ? | ✅ | ✅ Migrado |

## Datos (Preservar)
| Archivo | V0.1 | V0.2 | Estado |
|---------|------|------|--------|
| agents_registry.jsonl | ? | ✅ | ✅ Migrado |
| memoria_eva.jsonl | ? | ✅ | ✅ Migrado |
| rounds/*.json | ? | ✅ | ✅ Migrado |

## Migraciones Completadas (2026-03-27)
| Archivo | Acción | Commit |
|---------|--------|--------|
| protocol_contract_v0.1.json | ✅ Migrado a config/ | [PENDIENTE] |
| spec/message_envelope_v1.yaml | ✅ Migrado a spec/ | [PENDIENTE] |
| SALA_SESION_001.yaml | ✅ Migrado a config/ | [PENDIENTE] |

## Archivos Históricos (No Migrar)
- message_*.yaml (17 archivos) → neurobit_salon_v0.1/
- mensaje_*.yaml (3 archivos) → PROTOIDEAS/neurobit/messages/
- SCRUMB_*.json → sala/logs/
