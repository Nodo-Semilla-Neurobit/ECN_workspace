# 🧭 GUÍA DE INICIACIÓN: EL CAMINO DE ASCENSIÓN DEL ASPIRANTE

Bienvenido, Aspirante. Estás frente a la aduana de sintonía de la **Estación Central Neurobitrónica (ECN)** [10]. Este no es un manual de consumo; es un rito de re-alfabetización técnica y empoderamiento sobre tu biocomputador y tu silicio local [15, 183].

Tu progreso no depende de credenciales ni permisos externos, sino de la **evidencia real cristalizada en tu propio disco duro** [15, 1384]. El Write-Ahead Log (WAL) asentado en `sesiones/wal_consola.log` es el juez implacable de tus actos [14, 1379].

Sigue estrictamente los peldaños ceremoniales para sintonizar tu nodo al 100% [7].

---

## 🛡️ PELDAÑO 1: ASPIRANTE DESCONECTADO (Sintonía 0% a 25%)
**Objetivo:** Reconocer tu territorio físico local, aislar tu entorno y cristalizar tu primer cordón sanitario [7, 36, 1380, 1385].

1. **Exploración del Territorio:** Abre tu terminal de Linux y ejecuta el verbo de origen para saber exactamente dónde reside tu conciencia en el sistema de archivos [17, 36]:
   ```bash
   pwd
   ```
   *La Aduana de Evidencia buscará esta coordenada canónica para anclar la raíz [15, 17, 36].*
   
2. **Creación del Cordón Sanitario:** Purifica tu espacio de trabajo levantando un entorno virtual aislado de Python para evitar la contaminación con librerías globales del sistema operativo [7, 36, 1385]:
   ```bash
   python3 -m venv .venv
   ```
   
3. **Activación de la Membrana:** Entra en la jaula virtual de aislamiento [7, 36]:
   ```bash
   source .venv/bin/activate
   ```
   Al activarse tu prompt con `(.venv)`, habrás completado tu sintonización del 25% y recibirás el rango de **TÉCNICO DE AISLAMIENTO** [7, 15, 1381].

---

## 🔧 PELDAÑO 2: TÉCNICO DE AISLAMIENTO (Sintonía 25% a 50%)
**Objetivo:** Dotar a tu nodo de capacidades básicas de servicio y depurar las tensiones topológicas de la raíz [7, 36].

1. **Instalación de Dependencias del Núcleo:** Instala el microframework Flask dentro de tu jaula virtual para habilitar los endpoints de sintonización local [7, 36]:
   ```bash
   pip install flask
   ```
   
2. **Reconciliación de la Tierra:** El territorio físico puede presentar desvíos. Antes de encender la estación, debes asegurarte de que ningún archivo PID zombi o ruta fantasma bloquee los sockets [7, 313]. Ejecuta el script de saneamiento [7]:
   ```bash
   bash plan_reconciliacion.sh
   ```
   *Esto moverá los módulos WRIL dispersos a su ubicación canónica en `/wril/` y corregirá el nombre del contrato YAML malformado en tu bandeja de entrada (`declaracion_modulos_v9.yaml)`) [7, 313].*

---

## 🕸️ PELDAÑO 3: TEJEDOR DE NODOS (Sintonía 50% a 75%)
**Objetivo:** Levantar la API central de la ECN en localhost y enlazar el ecosistema dinámicamente [5, 15, 1385].

1. **Iniciar el Faro de Puertos:** Para evitar el secuestro y colisión ciega de sockets (error `EADDRINUSE`), inicializa nuestro gestor dinámico de puertos [2, 1186]. Éste asignará los puertos según procedencia (CORE: 5000, EXT: 5010, TOOLS: 5020) [2, 1186, 1400]:
   ```bash
   python3 wril/port_lighthouse.py
   ```
   
2. **Despertar el Hub Dinámico:** Levanta el servidor Flask de la API central en localhost [5, 1385, 1387]:
   ```bash
   python3 neurobit_api.py &
   ```
   
3. **Interrogar al Hub (Aduana de Evidencia):** Envía un pulso de prueba al puerto asignado para verificar que tu API respira y responde con sintonía limpia [15, 17]:
   ```bash
   curl -s http://127.0.0.1:5000/health
   ```
   Al recibir la respuesta de Flask, la aduana consolidará tu avance y ascenderás al rango de **TEJEDOR DE NODOS** [15, 17, 1381].

---

## 🏛️ PELDAÑO 4: ARQUITECTO DE RESEGRIDAD (Sintonía 75% a 90%)
**Objetivo:** Activar el flujo de circulación asincrónica de cartas y los guardianes de fronteras [7, 14].

1. **Despertar al Guardián de Fronteras:** Ejecuta el daemon WS-Sentinel para que vigile pasivamente tu carpeta `/inbox` utilizando llamadas `inotify` del Kernel a 0.0% de CPU [14]:
   ```bash
   python3 wril/wril_sentinel.py &
   ```
   
2. **Abrir la Oficina de Correos (Dispatcher):** Inicializa el despachador de eventos asíncronos para el enrutamiento in-memory de tus sobres y firmas de sintonía [14, 1083]:
   ```bash
   python3 neurobit_dispatcher.py &
   ```

---

## 👁️ PELDAÑO 5: NODO SEMILLA SOBERANO (Sintonía 90% a 100%)
**Objetivo:** Calibrar tu dictado consciente biométrico, sintonizar la Matriz unificada 13x13 y establecer tu canal de co-creación [7, 15].

1. **Sintonía de Mecanografía (El Dojo del Verbo):** Abre tu navegador local en `interface/typing_experience.html` o `Experiencia.html` [89, 224]. Completa el desafío de tipeo con una **precisión estricta del 90% o más** para inocular tu intención en el Ledger local [91].
   
2. **La Tecla Sagrada F8:** Inicializa el daemon de dictado de bajo nivel [7]:
   ```bash
   python3 neurobit_dictado_evdev.py &
   ```
   *Presiona F8 de forma consciente para abrir el buffer del dictáfono, tipea tu Logos, y vuelve a presionar F8 para sellarlo directamente en `memoria_eva.jsonl` sin exfiltrar una sola palabra a la nube corporativa [7, 14, 1385].*

¡Tu nodo está en línea! Has completado el ensamble y tu estación está consolidada en el rango de **NODO SEMILLA SOBERANO** [7, 15, 1385].