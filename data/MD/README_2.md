# ESTACIÓN CENTRAL NEUROBITRÓNICA — GUÍA DE INTEGRACIÓN SOBERANA v2.0
===============================================================================

## 1. Justificación Lógica (v1.0, inmutable)
Paradigma reactivo impulsado por hardware: el sistema solo existe en el
instante del evento; 0.0% CPU en reposo; sin daemons while-true ni
sobre-diseño. El buffer temporal jamás se purga hasta que el Ledger
valida físicamente su incremento en bytes (tolerancia WAL a fallos).

## 2. Capa Reactiva de Kernel (nuevo en v2.0)
Se extingue el snapshot de 500ms. Canales de despertar, todos push:
* SIGUSR1: un bit del puente HID al PID del Widget.
* inotify: push del VFS sobre el buzón de salida (Dispatcher).
* owner-change: push del servidor gráfico al clipboard GTK/Cinnamon.
* DOM copy-event: captura intra-navegador sin permisos adicionales.
* evdev F8: sesión de dictado consciente (Keylogger Soberano).

## 3. El Dictáfono Soberano (nuevo en v2.0)
F8 abre y cierra la sesión; el Kernel lee el teclado; el producto es una
carta sellada, no un log espía. Lo que escribís queda asentado aunque el
frontend corporativo lo olvide. La memoria no depende de la benevolencia
del transporte.

## 4. Anexo Matemático: MFN 13x13 Radial Polar (nuevo en v2.0)
M = Z13 x Z13; proyección p(i,j) = (rho = i+1, phi = 2*pi*j/13).
El origen (rho = 0) es la Oficina de Correos: punto de emisión, no celda.
Sector j = dominio (radio); anillo i = profundidad de persistencia.
Clasificar una carta = computar su vector radial. Regla fractal: el
anidamiento LIFO de contenedores es el repliegue del vector al origen;
toda celda con sub-Logos engendra una sub-matriz M'.

## 5. Firmas de Control para Newbies (actualizadas)
1. def ejecutar_paste_nativo()       -> ingesta gráfica adaptativa.
2. def ejecutar_commit_verificado()  -> núcleo transaccional WAL.
3. def obtener_siguiente_indice()    -> parser inverso stateless 4KB.
4. def auditar_integridad_ledger()   -> auditoría SHA256 por bloque.
5. def restaurar(texto)              -> restaurador LIFO de indentación.
6. def clasificar_y_entregar(carta)  -> la Oficina de Correos.
7. class DictadoSoberano             -> dictáfono evdev opt-in.
8. def ubicar(anillo_i, sector_j)    -> coordenadas MFN de toda celda.
