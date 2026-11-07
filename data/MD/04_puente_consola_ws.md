# Módulo 04: puente_consola_ws_v2.js (El Canal de Trazabilidad Sincerada)
## Ficha de Identidad
* **Nombre Físico del Archivo:** `puente_consola_ws_v2.js` (también guardado como `puente_consola_ws_v2-D.js`)
* **Ubicación Física Observada:** `~/compendio/ECN.Instalador_Ludico/puente_consola_ws_v2.js`
* **Ubicación MFN Declarada (Cabecera):** *Ninguna (Script Node.js, carece de cabecera MFN)*
* **Nivel de la Capa (MFN_LEVEL):** *Ninguno*
* **Coordenada de la Matriz (MFN_COORD):** *Ninguna*
* **Versión del Script:** `v2.0` (La versión de Trazabilidad Sincerada)

---

## 1. Funcionamiento Simplificado (Para el Aspirante)
El **Puente de Consola WebSocket** es la médula espinal de la pantalla de fósforo verde. Los navegadores web no pueden ejecutar comandos en tu computadora por cuestiones de seguridad. Para resolver esto, el Puente actúa como un puente biónico: levanta un servidor de comunicación rápida en segundo plano y abre una terminal de Linux (`bash`) oculta. Cuando escribes en tu consola web, el puente recibe el texto, lo inyecta en la terminal real, captura el resultado de la máquina y te lo devuelve al instante. Lo mágico de esta versión es que implementa la **Trazabilidad como Ley**: todo lo que tipeas y todo lo que la máquina escupe queda sellado permanentemente en un diario de sesión (`wal_consola.log`) a prueba de cortes de energía, permitiendo que tu maestro o tu par puedan leer el diario mediante un comando especial (`@informe`) para validar tu sintonía sin invadir tu máquina.

---

## 2. Lógica de Operación y Funciones
El script es un servidor WebSocket puro desarrollado bajo principios de minimalismo extremo:
* **RFC6455 de WebSocket "A Mano":** No utiliza librerías pesadas como `socket.io` o paquetes externos npm. Desarrolla el handshake de WebSockets, la decodificación de tramas binarias (`procesarFrames`) y el empaquetado de mensajes (`encodeText` / `encodeFrame`) usando únicamente las APIs criptográficas y de red estándar de Node.js, garantizando **CERO dependencias externas**.
* **El Cartero en Background (spawn de bash):** Inicia un proceso hijo Bash sin configuraciones de sesión personales del sistema (`spawn('bash', ['--norc', '--noprofile'])`).
  * Captura la salida estándar (`stdout`) y de error (`stderr`) del subproceso y las retransmite instantáneamente a todos los clientes web activos (`broadcast`).
* **Diario Transaccional (WAL Append-Only):**
  * Toda interacción entrante (`> `), de salida (`< `) o del sistema (`# `) es estampada con marca de tiempo precisa con precisión de milisegundos en `sesiones/wal_consola.log`.
* **La Aduana del Informe (Comando especial `@informe`):**
  * Cuando se intercepta la cadena `@informe`, el puente genera en caliente un archivo estructurado con cabecera `|=•'INFORME_ACTIVIDADES'•=|»` con la transcripción completa de los comandos ejecutados.
  * Este informe se guarda en `sesiones/informe_actividades.log` y es expuesto mediante un servidor HTTP local embebido en `http://127.0.0.1:8080/informe` para el consumo del Auditor del Territorio.

---

## 3. Variables y Constantes Hardcodeadas
* El puerto del WebSocket central está atado rígidamente al puerto `8080` (con fallback de variable de entorno `ECN_WS_PORT`):
  `const PUERTO = parseInt(process.env.ECN_WS_PORT || '8080', 10);`
* La clave mágica del protocolo WebSocket (`258EAFA5-E914-47DA-95CA-C5AB0DC85B11`) está hardcodeada.

---

## 4. Interacciones y Cooperación
* **Consola Verde CRT (consola_verde_ws_v2.6.html / Experiencia.html):** Se conecta a través del puerto loopback para recibir la sintonía del terminal.
* **Auditor del Territorio (Frontera del Dojo):** Cuando el JS del frontend detecta el comando `@informe`, realiza una consulta HTTP al endpoint `/informe` expuesto por el puente para leer las evidencias físicas reales de tu máquina.

---

## 5. Dependencias
* **Plataforma de Ejecución:** `node.js` (Módulos estándar `http`, `crypto`, `fs`, `path`, `child_process`). Cero paquetes de terceros.
* **Tolerancia a Fallos:**WAL robusto; si ocurre un corte de energía, no hay pérdida de historial, ya que la escritura es `appendFileSync` directa.

---

## 6. Diagrama de Flujo Conceptual
```text
 [ Consola de Fósforo Verde ] ────► (Comando) ────► [ Puente WS (Puerto 8080) ]
                                                            │
                                                   ┌────────┴────────┐
                                                   ▼                 ▼
                                             [ Sella WAL ]      [ spawn(bash) ]
                                                   │                 │
                                                   ▼                 ▼
                                             [ wal_consola.log ] [ Ejecuta ]
                                                                     │
                                                                     ▼
                                             [ Envía salida ] ◄──────┘
```

---

## 7. Tensiones e Inconsistencias (Fase 1)
* **Tensión A (Desconexión del Faro):** El puente de consola corre de forma ciega en el puerto `8080` (fijo), ignorando por completo la autoridad de sintonía dinámica del `PortLighthouse.py`. Debería registrarse en el Faro de Puertos bajo la membrana `TOOLS`.
