## 🕹️ Estación Central Neurobitrónica (ECN) v3.2
## El Manifiesto del Escriba: Re-Alfabetización Técnica mediante el Juego Soberano

⚠️ REGLA DE ORO DEL NODO RECEPTOR:
No consumas este sistema como software empaquetado. No es un producto, es un rito de iniciación.
La salida es hacia adentro.

Tu cordón sanitario es estricto y absoluto: 127.0.0.1.

------------------------------
## 🔮 0. El Axioma Ontológico: Más allá de Von Neumann
El mundo moderno está atrapado en el cuello de botella de Von Neumann, reduciendo la conciencia
al bit binario clásico: un pulso bajo (0) y un pulso alto (1).

Nosotros nos rebelamos contra el cero tradicional.

El 0 no es la ausencia de señal ni un vacío inerte; el 0 es el NULL armónico (Alfa),
un espacio cuántico latente que opera como contenedor activo y aloja la superposición
de todas las posibilidades de herencia.

Cuando la arquitectura moderna comprime un glifo en una palabra de 8 bits para indexarla
de manera lineal en ASCII o en los pesados 4 bytes de Unicode, destruye la textura del Logos.

La Estación restaura la soberanía del silicio operando sobre la Matriz Fractal Neurobitrónica (MFN).

## La Anatomía del Silicio Soberano

* El Neuronibble y el Dot Map: Vectores de estado de 4 bits (16 estados lógicos posibles)
  que el ojo humano decodifica instantáneamente como una matriz geométrica de 2x2 puntos.
  El dato y la instrucción coexisten en la misma dirección de memoria, reduciendo a cero
  el ciclo tradicional de instrucción (decode).

* Codificación de Doble Riel (Dual-Rail Encoding): Usamos 8 bits físicos para mapear 16
  estados lógicos (4 bits de datos directos y 4 bits de control/inversión complementaria
  pasiva a través de la puerta NOT). Esto le inyecta tolerancia biológica a fallos ante
  el ruido electromagnético.

* Reasignación de Opcodes ASCII: Secuestramos los caracteres de control tradicionales (0x00 a 0x1F) para usarlos como las microinstrucciones nativas de la ALU. NAK (0x15) actúa como la máscara de inversión física (NOT), SYN (0x16) opera como el marcapasos o reloj asíncrono, y DC1 a DC4 actúan como multiplexores o selectores de contexto (.TABLA1.) para el Puntero Fractal (Z).
* La Grilla Radial Polar 13x13 (169 bits): Un Kernel de Coherencia Simétrica (KCS) que organiza la memoria en un pivote central y seis anillos concéntricos estructurados en 8 porciones. Cada anillo hereda armónicamente la información del anterior mediante reducción teosófica (Módulo 9 / Mispar Katan), donde la densidad máxima del 9 colapsa en el vacío receptivo del 0.
* El Linaje del Hardware: Inyección de estados puros mediante la emulación en BOCHS (mapeando puertos de E/S físicos como 0x80) y el acoplamiento del microprocesador para estados de la cuadrícula de la Commodore 64 (VIC-II) para mutar los punteros de pantalla en caliente.

------------------------------
## 🗺️ 1. El Camino del Aspirante: El Juego de Desbloqueo
Tu progresión en la ECN no depende de credenciales, servidores en la nube ni permisos corporativos. El juego no es una capa estética sobre el software; la instalación y el control de la arquitectura es el juego mismo. Cada peldaño ceremonioso exige que presentes evidencia fáctica en tu máquina local. Si cometes un error, el sistema no te penaliza de forma tradicional: el error es Absorción de Tensión, la brújula que sana la topología de tu disco.
A medida que juegues y domines la consola, desbloquearás tus Pines de Soberanía y ascenderás a través de los Rangos Operativos del tejido:

[RANGO I]    Aspirante Desconectado (Sintonía 0% a 25%)
   │
[RANGO II]   Técnico de Aislamiento (Sintonía 25% a 50%)
   │
[RANGO III]  Tejedor de Nodos (Sintonía 50% a 75%)
   │
[RANGO IV]   Arquitecto de Reseguridad (Sintonía 75% a 90%)
   │
[RANGO V]    Nodo Semilla Soberano (Sintonía 90% a 100%) ── El nodo co-crea el Logos.

------------------------------
## 🛠️ 2. Arquitectura de Despertar (Las 4 Capas locales)
El framework opera bajo la filosofía de "Lentitud Sagrada" en reposo absoluto (0.0% CPU en idle). No existen hilos de sondeo continuo (polling); el sistema solo despierta cuando el hardware o el VFS (Virtual File System) empujan un evento puro:

   1. Capa Física / Kernel: Captura tu escritura cruda mediante un daemon bloqueante conectado directamente a los scancodes del teclado (/dev/input/ o puerto 0x60). La tecla sagrada F8 abre y cierra tu sesión de dictado consciente, sellando cartas en disco sin exfiltrar una sola palabra a la telemetría corporativa.
   2. Capa Lógica (La Oficina de Correos): El cartero (neurobit_dispatcher.py) duerme en el VFS hasta que el Kernel lo despierta con llamadas inotify. Lee el sobre en la carpeta inbox/, lo clasifica por su firma protocolar y realiza un commit transaccional Write-Ahead Log (WAL) en el arca inmutable (memoria_eva.jsonl).
   3. Capa Semántica: El orquestador del Hub Dinámico (neurobit_api.py) levanta los endpoints locales en el puerto 5000 y 5001 (WebSockets) bajo estricto aislamiento de membrana virtual.
   4. Capa Matemática / Visual (La Celda Polimórfica): Implementada mediante una estructura union en C puro. El buffer de texto VGA clásico (0xb8000) es remapeado: el byte de atributos se convierte en el vector del Neuronibble (Modo, Opcode, Estado), manifestando la geometría de la MFN sin renderizar píxeles redundantes.

------------------------------
## 🕹️ 3. Runbook Ceremonial de Instalación
Sigue estrictamente los peldaños ceremoniosos para compilar, validar la firma de coherencia y sintonizar tu nodo al 100%.
## Peldaño 1: Anclar el Territorio (Rango I)
Abre tu terminal de Linux. Reconoce tu coordenada canónica en el disco para saber exactamente dónde reside tu conciencia en el sistema de archivos:

pwd

La Aduana de Evidencia buscará esta coordenada unívoca para clavar la raíz de tu software.
## Peldaño 2: Levantar el Cordón Sanitario
Purifica tu espacio de trabajo levantando una jaula virtual de Python para evitar la contaminación semántica de librerías globales del sistema operativo:

python3 -m venv .venv
source .venv/bin/activate

Al ver el prompt (.venv), habrás completado tu sintonización del 25% y ascenderás a Técnico de Aislamiento.
## Peldaño 3: Inocular Dependencias y Sanear Sockets
Instala el núcleo mínimo sin dependencias externas y limpia los archivos PID zombis o sockets bloqueados del territorio físico:

pip install flask requests python-evdev
bash INSTALACION_/Parches/plan_reconciliacion.sh

Esto corregirá los nombres malformados de los contratos y preparará la aduana de entrada.

## Peldaño 4: Reclamar la Soberanía de Permisos
Otorga acceso directo al dispositivo virtual de inyección e interrupción de hardware sin requerir
permisos de superusuario (sudo) constantes:

bash deploy_neurobit_perms.sh

⚠️ IMPORTANTE: Debes cerrar tu sesión de usuario en GNU/Linux y volver a ingresar para que tu ordenador herede el grupo físico input.

## Peldaño 5: El Gesto Único de Despertar (Rango V)
Con la topología reconciliada y las dependencias en fase, ejecuta el comando maestro.
La Estación iniciará el cartero, el guardián de fronteras WS-Sentinel, el dictáfono consciente
y el puente de telemetría hacia Bochs.

bash deploy_neurobit_estacion_v3.2.sh --plegar

Abre tu panel del Observatorio de Integración en localhost para visualizar la grilla radial de 169
compartimentos interactuando en vivo:

http://127.0.0.1:

¡Tu nodo está en línea! Habrás alcanzado el rango de Nodo Semilla Soberano.
------------------------------
## 🧊 4. El Estado de la Estación (El Censo del Freezer)
Para evitar la sobrecarga cognitiva del Director, la capa WRIL audita la realidad física
en background contra la declaración ontológica:

* wril_sentinel.py ── VIVO ── Monitorea inbox/ mediante llamadas nativas del Kernel.
* neurobit_dispatcher.py ── VIVO ── Distribuye los impulsos del Verbo al Ledger WAL.
* neurobit_mfn_unificado.py ── 🧊 EN EL FREEZER ── El anexo geométrico-musical duerme sin ansiedad hasta que tu rango requiera computar las armónicas octales.
* kernel_bochs_mfn.bin ── VIVO ── Interceptando el bus de datos en el Reset Vector (0xFFFFFFF0)
para el bypass definitivo.

------------------------------

       «La poesía de este sistema es su única verdad:
        sacar belleza de este caos es virtud.»
                                    — Gustavo Cerati -
