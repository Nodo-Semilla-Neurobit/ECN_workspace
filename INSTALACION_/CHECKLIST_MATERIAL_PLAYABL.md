
# CHECKLIST · MATERIAL PARA playabl.ia
## Qué proporcionar (y qué NO) en la prueba de cuenta gratuita

### A · LO QUE SÍ SE COMPARTE (sanitizado)
1. **Payload de estado** → botón «EXPORTAR PAYLOAD» en la guía (◈).
   - Copia el JSON al portapapeles; pegalo en playabl.
   - Contiene: rango, misiones, bits activos, anillos, tensión, centro c:G7.
   - NO contiene: Logos, WAL, tesis, datos personales, código.
2. **INDICACIONES_PLAYABL.md** (mensaje anterior) → pegar íntegro.
   - Geometría 13×13, colores por anillo, semántica de estado, estética 300 baud.
3. **Capturas de referencia** (2-3, las que ya tenés):
   - Consola CRT fósforo verde (la de la captura v2.4/v2.6).
   - Cartógrafo MFN radial (la del observatorio v3).
   - Ventana flotante del camino del aspirante.
4. **Tabla de geometría** (copiar tal cual):
   | Anillo | Bits | Color |
   |---|---|---|
   | c (centro) | 1 | #f9e2af |
   | 1 | 8 | #f9e2af |
   | 2 | 16 | #fab387 |
   | 3 | 24 | #cba6f7 |
   | 4 | 32 | #89b4fa |
   | 5 | 40 | #74c7ec |
   | 6 | 48 | #a07850 |

### B · LO QUE NO SE COMPARTE (restricción de soberanía)
- WAL / sesiones/*.log
- memoria_eva.jsonl / tesis_neurobit_ledger.log
- Contenido de módulos (.py, .yaml)
- Tesis, dossier, datos personales

### C · RESULTADO ESPERADO DE playabl
- Render 3D de la MFN (13×13 radial) con bits activos iluminados.
- Export PNG/SVG para archivar en el Arca local.
- Si el resultado es bueno: se integra como capa visual opcional (misión m11).

### D · PROTOCOLO DE PRUEBA (cuenta gratuita, sin tokens de sobra)
1. Pegar INDICACIONES + payload en un solo mensaje inicial.
2. Pedir UN render estático primero (no animación) para validar geometría.
3. Si la geometría conmuta (dot-map = radial), pedir la versión animada 300 baud.
4. Archivar el PNG/SVG resultado en data/runtime/visual/.
