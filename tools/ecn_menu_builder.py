#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Orquestador Soberano
Módulo: ecn_menu_builder.py
Función: Escanea los headers MFN y las firmas de oficio para construir
         dinámicamente la cascada de menús en Tkinter.
         Cumple la Invariante 6: Cero rutas hardcodeadas en la UI.
MFN_LOCATION: tools/ | MFN_LEVEL: 3
VERSION: v1.0
"""

import os
import re
import tkinter as tk
from pathlib import Path

# Firmas canónicas de la ECN
RE_MFN_LOC = re.compile(r"MFN_LOCATION\s*[:=]\s*([^\s\"',]+)", re.IGNORECASE)
RE_NB_TASK = re.compile(r"##NB::([A-Z0-9_]+)::v[\d\.]+##")
RE_DEF_MAIN = re.compile(r"^def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", re.MULTILINE)

RUIDO = {'.git', '__pycache__', '.venv', 'node_modules', 'archive', 'backups_wril', 'pids'}
EXTENSIONES = {'.py', '.sh', '.yaml', '.md'}

class ECNMenuBuilder:
    def __init__(self, root_dir: Path, menu_bar: tk.Menu, dispatch_callback):
        self.root_dir = root_dir
        self.menu_bar = menu_bar
        self.dispatch = dispatch_callback  # Función que ejecuta el módulo en background
        self.capabilities = {}  # { "Capa/Categoría": [ {"name": "...", "path": "...", "entry": "..."} ] }

    def scan_territory(self):
        """Escanea el territorio y agrupa por MFN_LOCATION o Capa."""
        self.capabilities.clear()
        
        for root, dirs, files in os.walk(self.root_dir):
            dirs[:] = [d for d in dirs if d not in RUIDO]
            for file in files:
                f_path = Path(root) / file
                if f_path.suffix.lower() not in EXTENSIONES:
                    continue
                
                try:
                    # Leemos solo el encabezado para máxima eficiencia (O(1) fricción)
                    with open(f_path, 'r', encoding='utf-8', errors='ignore') as f:
                        header = f.read(1024)
                except Exception:
                    continue

                # 1. Determinar la Categoría (Menú Padre)
                m_loc = RE_MFN_LOC.search(header)
                category = m_loc.group(1).strip('/') if m_loc else "raiz_desconocida"
                category = category.replace('/', ' / ').title()  # Ej: "Wril / Saneamiento"
                
                if category not in self.capabilities:
                    self.capabilities[category] = []

                # 2. Determinar las Acciones (Submenús)
                tasks = RE_NB_TASK.findall(header)
                if tasks:
                    for task in tasks:
                        self.capabilities[category].append({
                            "display": task.replace('_', ' ').title(),
                            "path": str(f_path),
                            "type": "script"
                        })
                elif f_path.suffix == '.py':
                    # Si no hay ##NB##, buscamos el punto de entrada principal
                    defs = RE_DEF_MAIN.findall(header)
                    if 'main' in defs or 'correr' in defs or 'ritual' in defs:
                        entry = 'main' if 'main' in defs else ('correr' if 'correr' in defs else 'ritual')
                        self.capabilities[category].append({
                            "display": f"Ejecutar {f_path.stem} ({entry})",
                            "path": str(f_path),
                            "type": "python_module",
                            "entry": entry
                        })

    def build_menu(self):
        """Construye la interfaz de Tkinter basada en el territorio escaneado."""
        # Limpiar menú previo
        self.menu_bar.delete(0, tk.END)
        
        # Menú Base de la ECN
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Escanear Territorio (F5)", command=self.scan_territory)
        file_menu.add_command(label="Sincro-Alineación de Deriva (MCO)", command=lambda: self.dispatch("mco_reconciler"))
        file_menu.add_separator()
        file_menu.add_command(label="Plegar Estación (HALT)", command=lambda: self.dispatch("halt"))
        self.menu_bar.add_cascade(label="Estación", menu=file_menu)

        # Menús Dinámicos por Capa/MFN_LOCATION
        for category in sorted(self.capabilities.keys()):
            items = self.capabilities[category]
            if not items:
                continue
                
            cat_menu = tk.Menu(self.menu_bar, tearoff=0)
            for item in items:
                # El lambda captura el contexto para el disparo en background
                cat_menu.add_command(
                    label=item["display"], 
                    command=lambda p=item["path"], t=item["type"]: self.dispatch(p, t)
                )
            self.menu_bar.add_cascade(label=category, menu=cat_menu)

if __name__ == "__main__":
    # Prueba de concepto headless
    from wril_self_root import detectar_raiz
    raiz = detectar_raiz()
    builder = ECNMenuBuilder(raiz, None, lambda *args: print(f"Dispatch: {args}"))
    builder.scan_territory()
    print(f"[✓ MENU] {len(builder.capabilities)} categorías descubiertas en el territorio.")
    for cat, items in builder.capabilities.items():
        print(f"  [{cat}] -> {len(items)} acciones.")
