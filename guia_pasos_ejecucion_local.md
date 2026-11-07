# GUÍA DE PASOS PARA EJECUCIÓN LOCAL — ECN v3.2 con WRIL

## Contexto

Tu ordenador local está sincronizado con este workspace y necesita aplicar las correcciones identificadas en el informe exhaustivo. Esta guía sigue el principio de **mínima fricción** y **máxima seguridad**.

---

## FASE 0: PREPARACIÓN (5 minutos)

### Paso 0.1: Verificar estado actual del workspace

```bash
cd "/home/gus/workspace_reconstruido/"  # O tu ruta equivalente

# Contar archivos totales
find . -type f -name "*.py" -o -name "*.sh" | wc -l

# Verificar procesos Neurobit activos
ps aux | grep -E "neurobit_|wril_" | grep -v grep

# Listar PIDs existentes
ls -la pids/ 2>/dev/null || echo "Directorio pids/ no existe"
```

**Resultado esperado:** 
- Deberías ver ~114 archivos Python/Shell
- Posiblemente procesos huérfanos de ejecuciones anteriores
- Directorio pids/ con archivos .pid residuales

---

## FASE 1: SANEAMIENTO INICIAL (10 minutos)

### Paso 1.1: Detener procesos huérfanos

```bash
# Purgar procesos Neurobit/WRIL existentes
for pidfile in pids/*.pid; do
    if [ -f "$pidfile" ]; then
        kill -15 "$(cat "$pidfile")" 2>/dev/null && echo "[✓] Detenido $(cat "$pidfile")"
        rm -f "$pidfile"
    fi
done

# Matar por nombre cualquier residuo
pkill -f "neurobit_gnome_widget.py" 2>/dev/null
pkill -f "neurobit_dispatcher.py" 2>/dev/null
pkill -f "neurobit_dictado_evdev.py" 2>/dev/null
pkill -f "wril_sentinel.py" 2>/dev/null

echo "[✓] Saneamiento completado"
```

### Paso 1.2: Crear directorios base si no existen

```bash
mkdir -p inbox buzon_salida pids archive/historical/deploy archive/historical/runbooks archive/backups_wril clipboard_captured_folder/backups

echo "[✓] Estructura de directorios verificada"
```

---

## FASE 2: BOOTSTRAP WRIL (15 minutos)

### Paso 2.1: Ejecutar wril_bootstrap.py

```bash
cd "/home/gus/workspace_reconstruido/"

# Asegurar que estamos en la raíz
pwd

# Ejecutar bootstrap (genera path_map, verifica dependencias)
python3 wril/wril_bootstrap.py
```

**Resultado esperado:**
```
[0.1 WRIL] Regenerando path_map.json...
[✓ WRIL] Índice construido: XXX artefactos.
[0.2 WRIL] PatchResolver (dry-run) sobre scripts .sh ...
    [✓ REFERENCIA] deploy_neurobit_estacion_v3.2.sh: coherente.
    [⚠ REFERENCIA] otros_scripts.sh: X obsoletas (sin mutar)
[0.3 WRIL] Dependency scanner...
[✓ SCANNER] Terceros: X | Sistema: Y
[✓ WRIL] Bootstrap completo: topología y estado coinciden.
```

### Paso 2.2: Revisar path_map.json generado

```bash
# Verificar que se creó el mapa
ls -la path_map.json wril/path_map.json

# Contar entradas
python3 -c "import json; print(len(json.load(open('path_map.json'))))"

# Buscar colisiones potenciales (archivos con mismo nombre)
python3 << 'EOF'
import json
from collections import Counter
mapa = json.load(open('path_map.json'))
nombres = [k.split('/')[-1] for k in mapa.keys()]
colisiones = {k: v for k, v in Counter(nombres).items() if v > 1}
if colisiones:
    print(f"⚠ COLISIONES DETECTADAS: {colisiones}")
else:
    print("✓ Sin colisiones de nombres")
EOF
```

---

## FASE 3: AUDITORÍA TOPOLOGÍA (10 minutos)

### Paso 3.1: Ejecutar wril_topologia.py en modo dry-run

```bash
python3 wril/wril_topologia.py
```

**Resultado esperado:**
```
[✓ TOPOLOGIA] DRY-RUN: X artefactos por plegar.
    archivo1.py -> wril/archivo1.py
    archivo2.py -> core/archivo2.py
    ...
(ejecutá con --apply para materializar el pliegue)
```

### Paso 3.2: RevisarMFN Registry

```bash
python3 wril/wril_mfn_registry.py
```

**Resultado esperado:**
```
[✓ REGISTRY] Coherentes: X | Pendientes de pliegue topológico: Y
    INSTALACION /modulos/neurobit_dispatcher.py: declara ./ / vive en INSTALACION /modulos/
    ...
```

**Acción:** Anotá el número de inconsistencias. Si es > 10, hay trabajo de reconciliación pendiente.

---

## FASE 4: CORRECCIONES CRÍTICAS (30 minutos)

### Paso 4.1: Corregir wril_path_map.py (CRÍTICO)

```bash
# Backup del archivo original
cp wril/wril_path_map.py wril/backups_wril/wril_path_map.py.backup.$(date +%Y%m%d_%H%M%S)

# Editar wril/wril_path_map.py
nano wril/wril_path_map.py
```

**Cambiar la función `generar_mapa` de esto:**

```python
def generar_mapa(root_dir: Path, output_file: Path) -> dict:
    path_map = {}
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in RUIDO]
        for f in files:
            if f.endswith(EXT):
                path_map[f] = str(Path(root) / f)
    output_file.write_text(json.dumps(path_map, indent=2), encoding="utf-8")
    return path_map
```

**A esto:**

```python
def generar_mapa(root_dir: Path, output_file: Path) -> dict:
    path_map = {}
    colisiones = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in RUIDO]
        for f in files:
            if f.endswith(EXT):
                clave = str(Path(root).relative_to(root_dir) / f)
                if f in path_map:
                    colisiones.append(f"COLISIÓN: {f} en {path_map[f]} y {clave}")
                path_map[clave] = str(Path(root) / f)
    
    # Registrar colisiones en historial si existen
    if colisiones:
        from datetime import datetime
        with open(root_dir / "wril_historial.jsonl", "a") as h:
            h.write(json.dumps({"t": datetime.now().isoformat(), 
                               "tipo": "COLISION_NOMBRES",
                               "detalle": colisiones}) + "\n")
    
    output_file.write_text(json.dumps(path_map, indent=2), encoding="utf-8")
    return path_map
```

**Guardar y salir** (Ctrl+X, Y, Enter en nano)

### Paso 4.2: Corregir wril_patch_resolver.py (MANEJO DE ERRORES)

```bash
cp wril/wril_patch_resolver.py wril/backups_wril/wril_patch_resolver.py.backup.$(date +%Y%m%d_%H%M%S)

nano wril/wril_patch_resolver.py
```

**Modificar el método `reconcile` (líneas 65-73):**

```python
def reconcile(self, script: Path, dry_run: bool = True) -> dict:
    try:
        script = self.locate_target(script)
    except FileNotFoundError:
        return {"archivo": str(script), "error": "NO_LOCALIZABLE", "cambios": [], "aplicado": False}
    
    try:
        contenido = script.read_text(encoding="utf-8")
    except Exception as e:
        return {"archivo": str(script), "error": f"LECTURA: {e}", "cambios": [], "aplicado": False}
    
    cambios = self.generate_patch(contenido)
    reporte = {"archivo": str(script), "cambios": cambios, "aplicado": False}
    if cambios and not dry_run:
        self.backup(script)
        self.apply(script, cambios)
        reporte["aplicado"] = self.verify(script)
    return reporte
```

### Paso 4.3: Crear archivo 90-neurobit-hid.rules (FALTANTE)

```bash
cat > 90-neurobit-hid.rules << 'EOF'
# Reglas udev para Neurobit - Captura HID soberana
# Copiar a: /etc/udev/rules.d/90-neurobit-hid.rules

# Acceso a uinput para inyección HID
KERNEL=="uinput", MODE="0660", GROUP="input", OPTIONS+="static_node=uinput"

# Acceso a teclados por ID (dictado evdev)
SUBSYSTEM=="input", KERNEL=="event*", ATTRS{name}=="*Keyboard*", MODE="0660", GROUP="input"

# Acceso genérico a dispositivos de entrada
SUBSYSTEM=="input", KERNEL=="event*", MODE="0660", GROUP="input"
EOF

echo "[✓] Archivo 90-neurobit-hid.rules creado"
```

---

## FASE 5: APLICAR PERMISOS (5 minutos + reboot)

### Paso 5.1: Ejecutar deploy_neurobit_perms.sh

```bash
bash deploy_neurobit_perms.sh
```

**Resultado esperado:**
```
[✓ UDEV] Reglas cristalizadas. Re-iniciá sesión para aplicar el grupo 'input'.
```

### Paso 5.2: Verificar grupo input

```bash
# Agregar usuario al grupo input (si no está)
sudo usermod -aG input $USER

# Verificar grupos del usuario
id -nG

# IMPORTANTE: Cerrar sesión y volver a entrar para aplicar grupos
echo "[⚠] REINICIÁ SESIÓN para aplicar permisos de grupo input"
```

---

## FASE 6: RECONCILIACIÓN TOPOLÓGICA (OPCIONAL, 20 minutos)

**NOTA:** Este paso mueve archivos físicamente. Solo ejecutar si estás seguro.

### Paso 6.1: Backup masivo previo

```bash
# Crear backup completo antes de reconciliar
FECHA=$(date +%Y%m%d_%H%M%S)
mkdir -p "archive/backups_pre_reconciliacion_$FECHA"

# Copiar archivos críticos
cp -r wril/ "archive/backups_pre_reconciliacion_$FECHA/wril/"
cp -r core/ "archive/backups_pre_reconciliacion_$FECHA/core/" 2>/dev/null
cp *.sh "archive/backups_pre_reconciliacion_$FECHA/" 2>/dev/null

echo "[✓] Backup completado en archive/backups_pre_reconciliacion_$FECHA"
```

### Paso 6.2: Aplicar pliegue topológico

```bash
# Ejecutar con --apply para mover archivos
python3 wril/wril_topologia.py --apply
```

**Advertencia:** Esto moverá archivos según sus declaraciones MFN_LOCATION.

### Paso 6.3: Verificar resultado

```bash
# Re-ejecutar auditoría
python3 wril/wril_mfn_registry.py

# Debería mostrar menos inconsistencias
```

---

## FASE 7: ARCHIVAR SCRIPTS HISTÓRICOS (15 minutos)

### Paso 7.1: Mover versiones antiguas de deploy

```bash
mkdir -p archive/historical/deploy

# Mover todo menos v3.2
mv deploy_neurobit_estacion.sh archive/historical/deploy/ 2>/dev/null
mv deploy_neurobit_estacion_v2.sh archive/historical/deploy/ 2>/dev/null
mv deploy_neurobit_estacion_v3.sh archive/historical/deploy/ 2>/dev/null
mv "deploy_neurobit_estacion_v3 (copia).sh" archive/historical/deploy/ 2>/dev/null
mv deploy_neurobit_estacion_v3.1.sh archive/historical/deploy/ 2>/dev/null

echo "[✓] Scripts históricos archivados"
```

### Paso 7.2: Archivar runbooks antiguos

```bash
mkdir -p archive/historical/runbooks

mv INSTALACION\ /Parches/runbook_ensamble_primario*.sh archive/historical/runbooks/ 2>/dev/null

echo "[✓] Runbooks históricos archivados"
```

---

## FASE 8: VERIFICACIÓN FINAL (10 minutos)

### Paso 8.1: Checklist de verificación

```bash
echo "=== CHECKLIST DE VERIFICACIÓN ==="

# 1. Soberanía de Permisos
id -nG | grep -qw input && echo "[✓] Grupo input presente" || echo "[⚠] Falta grupo input"

# 2. Integridad WRIL
[ -f path_map.json ] && echo "[✓] path_map.json existe" || echo "[⚠] path_map.json ausente"

# 3. Archivos críticos accesibles
[ -f wril/wril_sentinel.py ] && echo "[✓] wril_sentinel.py accesible" || echo "[⚠] wril_sentinel.py faltante"
[ -f "INSTALACION /modulos/neurobit_dispatcher.py" ] && echo "[✓] neurobit_dispatcher.py accesible" || echo "[⚠] neurobit_dispatcher.py faltante"
[ -f "INSTALACION /modulos/neurobit_gnome_widget.py" ] && echo "[✓] neurobit_gnome_widget.py accesible" || echo "[⚠] neurobit_gnome_widget.py faltante"
[ -f "INSTALACION /modulos/neurobit_dictado_evdev.py" ] && echo "[✓] neurobit_dictado_evdev.py accesible" || echo "[⚠] neurobit_dictado_evdev.py faltante"

# 4. Reglas udev
[ -f /etc/udev/rules.d/90-neurobit-hid.rules ] && echo "[✓] Reglas udev instaladas" || echo "[⚠] Reglas udev faltantes"

# 5. Device uinput
[ -e /dev/uinput ] && echo "[✓] /dev/uinput disponible" || echo "[⚠] /dev/uinput ausente"

echo "=== FIN CHECKLIST ==="
```

### Paso 8.2: Test de importaciones Python

```bash
python3 << 'EOF'
import sys
sys.path.insert(0, '.')

try:
    from wril import wril_sentinel
    print("[✓] wril_sentinel importa correctamente")
except Exception as e:
    print(f"[⚠] wril_sentinel falló: {e}")

try:
    from wril import wril_path_map
    print("[✓] wril_path_map importa correctamente")
except Exception as e:
    print(f"[⚠] wril_path_map falló: {e}")

try:
    from wril import wril_bootstrap
    print("[✓] wril_bootstrap importa correctamente")
except Exception as e:
    print(f"[⚠] wril_bootstrap falló: {e}")

print("=== TEST DE IMPORTACIONES COMPLETADO ===")
EOF
```

---

## FASE 9: PRIMER DESPLIEGUE (OPCIONAL)

**Solo si todas las verificaciones anteriores fueron exitosas.**

### Paso 9.1: Ejecutar deploy maestro

```bash
# En una terminal con sesión renovada (para permisos input)
bash deploy_neurobit_estacion_v3.2.sh
```

**Lo que debería ocurrir:**
1. Auditoría topológica (dry-run)
2. Bootstrap WRIL
3. Verificación de dependencias
4. Compilación C (si existe el .c)
5. Verificación de permisos
6. Purga de huérfanos + baseline
7. Levantamiento secuencial:
   - WS-Sentinel en inbox/
   - Dispatcher en buzon_salida/
   - Widget GTK visible
   - Dictáfono en reposo (F8 activa)
8. Estado real escrito en estado_real.json

### Paso 9.2: Verificar estado

```bash
# En otra terminal
python3 wril/wril_estado_real.py
cat estado_real.json
```

**Deberías ver:**
```json
{
  "t": "2026-08-25T...",
  "componentes": [
    {"nombre": "WS_SENTINEL", "pid": 12345, "estado": "ALIVE"},
    {"nombre": "DISPATCHER", "pid": 12346, "estado": "ALIVE"},
    {"nombre": "VISOR_SOBERANO", "pid": 12347, "estado": "ALIVE"},
    {"nombre": "DICTAFONO", "pid": 12348, "estado": "ALIVE"}
  ]
}
```

### Paso 9.3: Probar flujo básico

```bash
# 1. Escribir algo en inbox/
echo "MFN_LOCATION: tools/\n# Archivo de prueba" > inbox/test_file.py

# 2. Esperar 2-3 segundos (Sentinel procesa)

# 3. Verificar que fue movido
ls -la tools/test_file.py

# 4. Verificar historial WRIL
tail -5 wril_historial.jsonl
```

### Paso 9.4: Plegar estación (cuando termines)

```bash
# Ctrl+C en la terminal donde corre deploy
# O ejecutar:
pkill -f "deploy_neurobit_estacion_v3.2.sh"
```

---

## SOLUCIÓN DE PROBLEMAS COMUNES

### Problema: "Permission denied" en /dev/input/*

**Solución:**
```bash
# Verificar grupos
id -nG

# Si no ves 'input', agregar y reiniciar sesión
sudo usermod -aG input $USER
# Cerrar sesión completamente y volver a entrar
```

### Problema: wril_sentinel no detecta archivos en inbox/

**Solución:**
```bash
# Verificar que inotify esté disponible
cat /proc/sys/fs/inotify/max_user_watches

# Si es < 8192, aumentar
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Reiniciar sentinel
pkill -f wril_sentinel
python3 wril/wril_sentinel &
```

### Problema: ImportError: No module named 'gi'

**Solución:**
```bash
# Instalar GTK bindings para Python
sudo apt-get install python3-gi gir1.2-gtk-3.0
```

### Problema: neurobit_dictado_evdev no encuentra teclado

**Solución:**
```bash
# Listar dispositivos de entrada disponibles
ls -la /dev/input/by-id/

# Si está vacío, probar con event genéricos
ls -la /dev/input/event*

# Modificar neurobit_dictado_evdev.py para usar fallback
# (ver línea 89 del archivo)
```

### Problema: Caracteres especiales en ruta causan errores

**Solución:**
```bash
# Crear symlink ASCII-only
ln -s "/home/gus/workspace_reconstruido/" ~/ecn_workspace

# Usar el symlink para operaciones bash
cd ~/ecn_workspace

# O forzar encoding UTF-8 en scripts
export PYTHONIOENCODING=utf-8
export LC_ALL=C.UTF-8
```

---

## PRÓXIMOS PASOS RECOMENDADOS

Después de completar esta guía:

1. **Semana 1:** Operar la ECN en modo estable, reportar bugs menores
2. **Semana 2:** Ejecutar ETAPA 2-7 del procedimiento de reconstrucción del README
3. **Semana 3:** Implementar mejoras de prioridad media del informe
4. **Semana 4:** Documentar lecciones aprendidas y actualizar README canónico

---

## CONTACTO Y SOPORTE

Si encontrás problemas no documentados aquí:

1. Revisar `wril_historial.jsonl` para logs de WRIL
2. Consultar `estado_real.json` para estado de componentes
3. Revisar informes en `data/md/` para contexto arquitectural
4. El workspace debe poder explicar su propio estado

---

*"La poesía de este sistema es su única verdad"*
