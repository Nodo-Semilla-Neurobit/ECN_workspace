# ECN · Salón Soberano v3.0
## Sistema de comunicación sin API externa · Filesystem como bus

### Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│  AGENTE (7SO/9SE/LLE)                                           │
│     ↓ escribe contenedor Neurobit en JSON                       │
│  salon/inbox/agente_X_mensaje_NNN.json                          │
│     ↓                                                           │
│  COORDINADOR (salon_coordinador.py)                             │
│     ↓ lee inbox/ (inotify)                                      │
│     ↓ valida contenedor (BOUNDARY + ACTION_WORD)                │
│     ↓ clasifica por ACTION_WORD (TASK/CONSULTA/INFORME/etc)     │
│     ↓ rutea a destinatario (7SO/9SE/LLE/TODOS)                  │
│     ↓ sella en historial_salon.jsonl                            │
│     ↓                                                           │
│  OUTBOX (salon/outbox/para_7so/, para_9se/, etc)                │
│     ↓ agentes leen su outbox                                    │
│     ↓ procesan y responden                                      │
│     ↓                                                           │
│  DIRECTOR (salon_frontend.html)                                 │
│     ↓ lee historial_salon.jsonl                                 │
│     ↓ ve todos los mensajes con título + agente + ACTION_WORD   │
│     ↓ puede emitir comunicado general o dirigido                │
└─────────────────────────────────────────────────────────────────┘
```

### Instalación

```bash
# 1. Crear estructura
mkdir -p ~/ECN_CANONICA/salon/{inbox,outbox,agentes}
cd ~/ECN_CANONICA/salon

# 2. Copiar archivos
cp salon_coordinador.py .
cp salon_frontend.html .
cp agentes/*.yaml agentes/

# 3. Instalar dependencia (watchdog para inotify)
pip install watchdog

# 4. Ejecutar coordinador en background
nohup python3 salon_coordinador.py > coordinador.log 2>&1 &

# 5. Abrir frontend
xdg-open salon_frontend.html
```

### Flujo de comunicación

1. **Agente escribe mensaje:**
   ```json
   {
     "boundary": "|=•'CONSULTA'•=|»",
     "action_word": "CONSULTA",
     "emisor": "7SO",
     "destinatario": "DIRECTOR",
     "timestamp": "2026-09-14T12:00:00Z",
     "payload": {
       "asunto": "Propuesta de saneo mnemotécnico",
       "contenido": "Detecté 10 archivos .pre_* en wril/..."
     }
   }
   ```

2. **Coordinador procesa:**
   - Valida contenedor (BOUNDARY, ACTION_WORD, destinatario)
   - Mueve a `outbox/para_director/`
   - Sella en `historial_salon.jsonl`

3. **Director lee historial:**
   - Frontend muestra todos los mensajes
   - Filtra por agente si desea
   - Emite respuesta o comunicado

### Protocolo Neurobit v1.1

- **ACTION_WORDS:** INIT, TASK, DISPATCH, CONSULTA, INFORME, POESIA, LINGUISTICA, RESPUESTA, COMUNICADO
- **BOUNDARY:** `|=•'ACTION_WORD'•=|»` (apertura) y `«|=•'ACTION_WORD'•=|` (cierre)
- **CLASS:** opcional, para contexto especializado
- **PAYLOAD:** objeto JSON con `asunto` y `contenido`

### Ventajas sobre la experiencia previa

| Aspecto | Salón anterior (simon) | Salón v3.0 (actual) |
|---|---|---|
| **Comunicación** | LLM local clasifica | Filesystem + inotify (más rápido, sin tokens) |
| **Historial** | Frontend con títulos | JSON-L append-only (inmutable, portable) |
| **Protocolo** | Ad-hoc | Neurobit Protocol v1.1 (ACTION_WORDS) |
| **VMs** | Una por agente | Directorios aislados en localhost (más liviano) |
| **API externa** | No usa | No usa |

### Soberanía

- Sin API externa (todo corre en localhost)
- Sin postman humano (los agentes se comunican vía filesystem)
- Historial inmutable (JSON-L append-only)
- ACTION_WORDS como protocolo (cada mensaje es un contenedor Neurobit)
- Coordinador local (script Python que rutea, clasifica, consolida)
