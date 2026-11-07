# AULA SOBERANA — NEUROBIT para newbies (v0.1)
## Cómo leerla
No de arriba hacia abajo: del centro hacia afuera, como la MFN.
Cada nivel es un anillo. Si te perdés, volvé al anillo anterior: nadie te apura.

## Nivel 0 — El hecho
Apretaste Ctrl+C. Un electrón se movió en el bus.
El sistema existe SOLO en ese instante; el resto del tiempo duerme (0.0% CPU).
Lección: un buen sistema no es el que más hace, sino el que mejor duerme.

## Nivel 1 — La carta y el sello
Nada entra como "dato crudo": todo entra como carta sellada.
Sello: |=•'accion'•=|» ... «|=•'accion'•=|
El sello dice QUÉ hacer (acción) y EN QUÉ contexto (clase).
Ejercicio: corré neurobit_aula.py y escribí tu primera carta.

## Nivel 2 — El buzón y el cartero
La carta cae en buzón_salida/ (el buzón de salida).
El dispatcher (el cartero) duerme; el Kernel lo despierta con inotify.
Lee el sello y entrega: al Ledger (libro inmutable) o a la memoria.

## Nivel 3 — El Arca
memoria_eva.jsonl: solo se agrega, nunca se borra (append-only).
Lo escrito no se des-escribe: esa es tu memoria sin amnesia.
Auditoría SHA256 por bloque: si alguien lo toca, el sistema se da cuenta.

## Nivel 4 — WRIL (la circulación)
El workspace se pregunta: "¿dónde estoy?" (self_root),
"¿dónde está X?" (path_resolver), "¿qué declaro ser?" (mfn_registry).
Mapa y territorio: si no coinciden, no es error: es señal (tensión).

## Nivel 5 — La MFN
Todo lo anterior cabe en una matriz radial 13x13:
centro c:G7 = el observador (vos); anillos = profundidad; sectores = dominios.
Cuando entiendas esto, ya no sos newbie: sos un radio.

## Glosario del Aula
- Logos: lo dicho con verdad y univocidad.
- Carta sellada: contenido + acción + clase.
- Buzón: buzón_salida/, la aduana de entrada.
- Cartero: el dispatcher que entrega.
- Arca: memoria_eva.jsonl, la memoria inmutable.
- Tensión: declaración ≠ realidad; señal, no error.
- Pliegue: mover el territorio al mapa, con backup previo.
- Radio: cada adaptador que aporta una nueva forma de capturar.
- NODO_SEMILLA: el que siembra; vos.
