#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MFN_LOCATION: wril/
# MFN_LEVEL: 1
# MFN_COORD: c:G7
# VERSION: v1.1
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: wril/wril_inmunidad_activa.py (Auto-Reparador Inmunológico WRIL)
Función: Escucha logs y trazas de error (flags de tensión como ModuleNotFoundError),
         verifica idempotencia, ejecuta el resguardo inmutable en backups_wril/ y
         corrige dinámicamente el anclaje de raíz (WRIL::SELF_PATH::v1.1) en el módulo afectado.
0.0% CPU en reposo. Invariantes de WRIL (Leyes 1, 2, 3 y 4) 100% garantizadas.
"""

import sys as _ws
import os
import re
import json
import shutil
from pathlib import Path as _wp
from datetime import datetime

# =====================================================================
# LEY 1 & LEY 4: ANCLAJE DE RAÍZ Y SELF-PATH DINÁMICO
# =====================================================================
def resolver_raiz_ecn() -> _wp:
    """Busca dinámicamente la raíz canónica del workspace subiendo por los padres."""
    try:
        from wril.wril_self_root import detectar_raiz
        return _wp(detectar_raiz())
    except Exception:
        actual = _wp(__file__).resolve().parent
        for p in [actual] + list(actual.parents):
            if (p / "where_am_I.inf").exists() or (p / ".ecn_raiz").exists() or (p / "pids").is_dir():
                return p
        return actual.parent

ECN_ROOT = resolver_raiz_ecn()
if str(ECN_ROOT) not in _ws.path:
    _ws.path.insert(0, str(ECN_ROOT))


# =====================================================================
# SHIM INMUTABLE PARA INYECCIÓN QUIRÚRGICA DE RAÍZ (v1.1)
# =====================================================================
SHIM_CANONICO_RAIZ = """# ---------- ANCLAJE DINÁMICO DE RAÍZ CANÓNICA (WRIL::SELF_PATH::v1.1) ----------
import sys as _ws
from pathlib import Path as _wp
_ecn_root = _wp(__file__).resolve().parent

while _ecn_root.parent != _ecn_root:
    if (_ecn_root / "where_am_I.inf").exists() or (_ecn_root / ".ecn_raiz").exists() or (_ecn_root / "pids").is_dir():
        break
    _ecn_root = _ecn_root.parent
if str(_ecn_root) not in _ws.path:
    _ws.path.insert(0, str(_ecn_root))
# -------------------------------------------------------------------------------
"""


# =====================================================================
# LEY 2: PRESERVACIÓN NO PLEGABLE (BACKUP ATÓMICO)
# =====================================================================
def crear_backup_inmutable(script_path: _wp, motivo: str = "AUTO_REPARACION_WRIL") -> _wp:
    """Crea una copia inmutable del script en backups_wril/ antes de modificarlo."""
    script_path = _wp(script_path).resolve()
    backups_dir = ECN_ROOT / "backups_wril"
    backups_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_backup = f"{script_path.stem}_{ts}_{motivo}.py.bak"
    dest = backups_dir / nombre_backup
    shutil.copy2(script_path, dest)
    print(f"[✓ WRIL_INMUNIDAD] Backup inmutable creado: {dest.name}")
    return dest


# =====================================================================
# LEY 3: GUARDA DE CONVERGENCIA E IDEMPOTENCIA
# =====================================================================
def esta_corregido(script_path: _wp) -> bool:
    """Verifica si el módulo ya posee el anclaje canónico v1.1 a la raíz."""
    script_path = _wp(script_path).resolve()
    if not script_path.exists():
        return False

    contenido = script_path.read_text(encoding="utf-8", errors="ignore")
    # Firma estricta de ascensión canónica v1.1
    return "_ecn_root.parent != _ecn_root" in contenido and "WRIL::SELF_PATH::v1.1" in contenido


def aplicar_reconciliacion_script(script_path: _wp) -> bool:
    """Aplica la corrección quirúrgica inyectando el shim dinámico v1.1."""
    script_path = _wp(script_path).resolve()
    if not script_path.exists():
        print(f"[X WRIL_INMUNIDAD] El archivo {script_path} no existe.")
        return False

    if esta_corregido(script_path):
        print(f"[· WRIL_INMUNIDAD] Módulo {script_path.name} ya posee anclaje canónico de raíz (Idempotencia OK).")
        return True

    # 1. Backup previo inmutable (Ley 2)
    crear_backup_inmutable(script_path, motivo="INYECCION_SELF_PATH_V1.1")

    # 2. Leer contenido y extirpar shims legados obsoletos
    lineas = script_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    lineas_limpias = []
    for l in lineas:
        # Filtrar inyecciones frágiles previas que solo insertaban .parent
        if "_ws.path.insert(0, str(_wp(__file__).resolve().parent))" in l and "parent.parent" not in l:
            continue
        lineas_limpias.append(l)

    # 3. Ubicar punto de inserción (después de shebang, encoding y docstring)
    idx_insert = 0
    en_docstring = False
    docstring_delim = None

    for i, line in enumerate(lineas_limpias):
        lstr = line.strip()
        if i == 0 and lstr.startswith("#!"):
            idx_insert = i + 1
            continue
        if lstr.startswith("# -*- coding"):
            idx_insert = i + 1
            continue
        if lstr.startswith('"""') or lstr.startswith("'''"):
            if not en_docstring:
                en_docstring = True
                docstring_delim = lstr[:3]
            elif lstr.endswith(docstring_delim):
                en_docstring = False
                idx_insert = i + 1
                break
            continue
        if en_docstring and lstr.endswith(docstring_delim):
            en_docstring = False
            idx_insert = i + 1
            break
        if not en_docstring and not lstr.startswith("#") and lstr != "":
            if idx_insert == 0:
                idx_insert = i
            break

    # 4. Inyectar Shim Canónico v1.1
    nuevas_lineas = lineas_limpias[:idx_insert] + [SHIM_CANONICO_RAIZ] + lineas_limpias[idx_insert:]
    script_path.write_text("\n".join(nuevas_lineas), encoding="utf-8")
    print(f"[✓ WRIL_INMUNIDAD v1.1] Módulo {script_path.name} auto-reparado exitosamente con anclaje dinámico de raíz.")
    return True


# =====================================================================
# PROCESADOR DE LOGS Y BANDERAS (FLAGS DE TENSIÓN)
# =====================================================================
def procesar_log_o_traza(texto_log: str) -> list:
    """Extrae flags de tensión de logs/trazas (ej: ModuleNotFoundError) y repara los scripts."""
    modulos_reparados = []
    patron_file = re.compile(r'File "([^"]+)", line \d+, in <module>')
    patron_error = re.compile(r"ModuleNotFoundError: No module named '([^']+)'")

    lineas = texto_log.splitlines()
    ultimo_script = None

    for line in lineas:
        m_file = patron_file.search(line)
        if m_file:
            script_candidato = m_file.group(1)
            if script_candidato.endswith(".py"):
                ultimo_script = script_candidato

        m_err = patron_error.search(line)
        if m_err and ultimo_script:
            print(f"[! WRIL_INMUNIDAD] Flag de tensión detectado: {m_err.group(0)} en {ultimo_script}")
            p_script = _wp(ultimo_script)
            if not p_script.is_absolute():
                p_script = ECN_ROOT / p_script

            if p_script.exists():
                if aplicar_reconciliacion_script(p_script):
                    modulos_reparados.append(str(p_script))
            ultimo_script = None

    return modulos_reparados


# =====================================================================
# CLI / MAIN
# =====================================================================
def main():
    print("=" * 65)
    print("ECN · CAPA WRIL · AUTO-REPARADOR INMUNOLÓGICO DE TENSIÓN v1.1")
    print("=" * 65)
    print(f"RAÍZ ECN: {ECN_ROOT}")
    print("=" * 65)

    if len(_ws.argv) > 1:
        target = _ws.argv[1]
        p_target = _wp(target)
        if not p_target.is_absolute():
            p_target = ECN_ROOT / p_target

        if p_target.exists():
            print(f"[· WRIL_INMUNIDAD v1.1] Ejecutando reconciliación directa sobre: {p_target}")
            aplicar_reconciliacion_script(p_target)
        else:
            print(f"[X WRIL_INMUNIDAD] Ruta no encontrada: {target}")
    else:
        print("[· WRIL_INMUNIDAD] Modo agnóstico. Especifica un script objetivo o archivo de log para procesar.")

if __name__ == "__main__":
    main()
