#!/bin/bash
PLIEGUE DE SOBERANÍA: habilitar el origen del navegador ante Ollama.
Seguro: el servicio sigue atado a 127.0.0.1; el cordón sanitario no se toca.
0) En la terminal del pull duplicado: Ctrl+C (suspendé la bajada).
1) Override de la unit (requiere sudo):
sudo mkdir -p /etc/systemd/system/ollama.service.d
printf '[Service]\nEnvironment="OLLAMA_ORIGINS=*"\n' | sudo tee /etc/systemd/system/ollama.service.d/origins.conf
sudo systemctl daemon-reload
sudo systemctl restart ollama
2) VERIFICACIÓN (DECLARACIÓN ≠ REALIDAD): simular el Origin del navegador.
Debe imprimir 200. Si persiste 403, usar lista explícita:
Environment="OLLAMA_ORIGINS=null,http://localhost:*,http://127.0.0.1
:*"
curl -s -o /dev/null -w "%{http_code}\n" -H "Origin: null" http://127.0.0.1:11434/api/tags
3) LINAJE: rescatar la persona ya inscrita en el territorio.
ollama show neurobit-qwen35-4b --modelfile
