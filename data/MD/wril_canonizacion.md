| Módulo canónico            | Pregunta que responde            | Función  | Predecesor (codigos_implementados) |
|----------------------------|----------------------------------|----------|------------------------------------|
| wril_sentinel.py           | ¿Dónde debe vivir lo nuevo?      | ROUTE    | WS-Sentinel v1.0 (inotifywait)     |
| wril_path_map.py           | ¿Cuál es la topología actual?    | DISCOVER | generate_path_map.py               |
| wril_path_resolver.py      | ¿Dónde está X?                   | RESOLVE  | path_resolver.py                   |
| wril_mfn_registry.py       | ¿Qué declara ser este archivo?   | INTERPRET| mfn_file_registry.py               |
| wril_patch_resolver.py     | ¿Qué referencia está rota?       | REPAIR   | sos_path_fixer.py (1ª implementación)|
| wril_dependency_scanner.py | ¿Qué necesita para funcionar?    | REQUIRE  | (pendiente de cristalizar)         |
| wril_dynamic_tester.py     | ¿Se comporta como declara?       | VERIFY   | sos_dynamic_tester.py              |
| wril_batch_executor.py     | ¿Cómo ejecuto la secuencia?      | EXECUTE  | other_sos_batch_executor.py        |
| wril_backup.py             | ¿Cómo preservo antes de mutar?   | RECORD   | EXTRAÍDO de Sentinel/Fixer (cero redundancia) |

Regla de no-fusión asentada: PATH MAP = estado físico; MFN REGISTRY = identidad declarada.
La tensión entre ambos (DECLARACIÓN ≠ REALIDAD) no es un bug: es el detector de integridad de la capa.
