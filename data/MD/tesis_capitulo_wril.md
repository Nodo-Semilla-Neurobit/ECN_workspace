## 8. CAPA WRIL (nuevo en Tesis v1.1)
### 8.1 Definición
Capa de infraestructura entre la Semántica y el FileSystem, responsable de
la correspondencia entre la identidad declarativa de los artefactos, su
ubicación física, sus dependencias y sus referencias internas. Principio:
Discover → Resolve → Reconcile → Verify → Record → Route.

### 8.2 Las nueve preguntas (fronteras modulares)
wril_path_map (¿cuál es la topología?), wril_path_resolver (¿dónde está X?),
wril_mfn_registry (¿qué declara ser?), wril_sentinel (¿dónde debe vivir lo
nuevo?), wril_patch_resolver (¿qué referencia está rota?), wril_backup
(¿cómo preservo antes de mutar?), wril_dependency_scanner (¿qué necesita?),
wril_dynamic_tester (¿se comporta como declara?), wril_batch_executor
(¿cómo ejecuto la secuencia?). Ninguna se fusiona: la capa jamás deviene
supermódulo.

### 8.3 La tensión como señal de integridad
DECLARACIÓN ≠ REALIDAD no es un bug: es el detector. El primer auditorío
revela el pliegue pendiente; wril_topologia lo ejecuta y la tensión cae a
cero. El mapa y el territorio quedan coincidentes por construcción.

### 8.4 Ética de la circulación
Backup previo a toda mutación (módulo único, cero redundancia); dry-run por
defecto; parches controlados con marca de agua; registro histórico
inmutable; el reporte de fallo viaja como carta sellada a la Oficina de
Correos (end-point HTTP si la Sala está despierta, buzón siempre).

### 8.5 Bootstrap como proceso inicial
Toda tarea comienza con el ritual: regenerar el índice, reconciliar
referencias en dry-run, verificar dependencias. La circulación precede al
núcleo: la Estación despierta solo después de que WRIL confirma que el
mundo coincide con su declaración.     
