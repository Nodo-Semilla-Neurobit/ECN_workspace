#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Estación Central Neurobitrónica (ECN) v3.2
Módulo: core/gui_ecn_central.py
Función: Panel de Orquestación Tkinter con Consola Fósforo Verde, Filtro de Mensajes, Acceso Directo [+] y Puente Web.
"""

import sys
import os
import queue
import threading
import subprocess
import webbrowser
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
from pathlib import Path

# Constantes de Estilo CRT Fósforo Verde
COLOR_BG = "#0b0c10"
COLOR_PANEL = "#13131a"
COLOR_FOSFORO = "#5cff72"
COLOR_TEXTO = "#cdd6f4"
COLOR_ALERT = "#ff3048"
FUENTE_MONO = ("Courier New", 10, "bold")


class ECNOrquestadorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("☉ ECN · ORQUESTADOR SOBERANO v3.2 · LOCALHOST")
        self.geometry("1100x700")
        self.configure(bg=COLOR_BG)

        self.cola_logs = queue.Queue()
        self.filtro_activo = "TODOS"

        self._crear_menu_superior()
        self._crear_botonera_herramientas()
        self._crear_barra_filtro()
        self._crear_consola_crt()

        # Bucle de escucha asíncrono para 0.0% de congelamiento de la UI
        self.after(100, self._procesar_cola_logs)

    def _crear_menu_superior(self):
        menu_bar = tk.Menu(self, bg=COLOR_PANEL, fg=COLOR_FOSFORO)

        # Menú Archivo & Módulos
        menu_archivo = tk.Menu(menu_bar, tearoff=0)
        menu_archivo.add_command(label="Cargar Módulo Python", command=self._cargar_script_custom)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.quit)
        menu_bar.add_cascade(label="Archivo", menu=menu_archivo)

        # Menú de Acceso Directo [+] (Estructura Dinámica)
        self.menu_plus = tk.Menu(menu_bar, tearoff=0)
        self.menu_plus.add_command(label="📄 Ver Log Activo (.log)", command=lambda: self._abrir_visor_file(".log"))
        self.menu_plus.add_command(label="📊 Ver Censo (.lst)", command=lambda: self._abrir_visor_file(".lst"))
        self.menu_plus.add_command(label="📖 Ver Especificación (.md)", command=lambda: self._abrir_visor_file(".md"))
        menu_bar.add_cascade(label="[+] Accesos", menu=self.menu_plus)

        # Botón directo para lanzar la interfaz Web en el Navegador (Puerto 5000 API)
        menu_bar.add_command(label="🌐 Abrir en Navegador", command=self._lanzar_consola_web)
        self.config(menu=menu_bar)

    def _crear_botonera_herramientas(self):
        # Corrección forense: 'px=5' corregido a 'padx=5'
        frame_toolbar = tk.Frame(self, bg=COLOR_PANEL, pady=5, padx=5)
        frame_toolbar.pack(fill=tk.X)

        # Comandos que disparan scripts de la Capa WRIL y Reconciliador MCO
        acciones = [
            ("⚡ DISCOVER", lambda: self.ejecutar_comando("python3 wril/wril_path_map.py")),
            ("🔍 RESOLVE", lambda: self.ejecutar_comando("python3 wril/wril_path_resolver.py")),
            ("🌅 BOOTSTRAP", lambda: self.ejecutar_comando("python3 wril/wril_bootstrap.py")),
            ("🛡️ SENTINEL", lambda: self.ejecutar_comando("python3 wril/wril_sentinel.py")),
            ("📊 MMP SCAN", lambda: self.ejecutar_comando("python3 tools/mco_reconciler.py")),
        ]

        for texto, cmd in acciones:
            btn = tk.Button(
                frame_toolbar,
                text=texto,
                command=cmd,
                bg="#1f232a",
                fg=COLOR_FOSFORO,
                font=("Courier New", 9, "bold"),
                bd=1,
                relief=tk.RAISED,
                activebackground=COLOR_FOSFORO
            )
            btn.pack(side=tk.LEFT, padx=4)

    def _crear_barra_filtro(self):
        # Corrección forense: 'px=5' corregido a 'padx=5'
        frame_filtro = tk.Frame(self, bg=COLOR_BG, pady=4, padx=5)
        frame_filtro.pack(fill=tk.X)

        tk.Label(
            frame_filtro, text="FILTRO CONSOLA:", bg=COLOR_BG, fg=COLOR_TEXTO, font=("Courier New", 9)
        ).pack(side=tk.LEFT, padx=5)

        self.combo_filtro = ttk.Combobox(
            frame_filtro, values=["TODOS", "WS", "WRIL", "CORE", "ERR"], state="readonly", width=10
        )
        self.combo_filtro.set("TODOS")
        self.combo_filtro.bind("<<ComboboxSelected>>", self._actualizar_filtro)
        self.combo_filtro.pack(side=tk.LEFT, padx=5)

    def _crear_consola_crt(self):
        self.txt_consola = scrolledtext.ScrolledText(
            self, bg=COLOR_BG, fg=COLOR_FOSFORO, insertbackground=COLOR_FOSFORO, font=FUENTE_MONO
        )
        self.txt_consola.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.txt_consola.insert(
            tk.END,
            "=== ESTACIÓN CENTRAL NEUROBITRÓNICA v3.2 — CONSOLA CRT ===\n[SYSTEM] Sistema listo a 127.0.0.1. En espera de instrucciones...\n"
        )

    def ejecutar_comando(self, comando):
        def worker():
            self.cola_logs.put(f"[EXEC] > {comando}\n")
            p = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in p.stdout:
                self.cola_logs.put(line)
            p.wait()
            self.cola_logs.put(f"[EXIT] Código de salida: {p.returncode}\n")

        threading.Thread(target=worker, daemon=True).start()

    def _procesar_cola_logs(self):
        while not self.cola_logs.empty():
            linea = self.cola_logs.get()
            if self._pasa_filtro(linea):
                self.txt_consola.insert(tk.END, linea)
                self.txt_consola.see(tk.END)
        self.after(100, self._procesar_cola_logs)

    def _pasa_filtro(self, linea):
        filtro = self.combo_filtro.get()
        if filtro == "TODOS":
            return True
        return filtro in linea

    def _actualizar_filtro(self, event):
        self.cola_logs.put(f"[INFO] Filtro cambiado a: {self.combo_filtro.get()}\n")

    def _lanzar_consola_web(self):
        # Corrección forense: Apuntando al endpoint canónico en el Puerto 5000 (neurobit_api.py)
        url = "http://127.0.0.1:5000"
        webbrowser.open(url)
        self.cola_logs.put(f"[WEB] Abriendo navegador local en: {url}\n")

    def _cargar_script_custom(self):
        f = filedialog.askopenfilename(filetypes=[("Archivos Python/Bash", "*.py *.sh")])
        if f:
            self.ejecutar_comando(f"python3 '{f}'" if f.endswith(".py") else f"bash '{f}'")

    def _abrir_visor_file(self, ext):
        f = filedialog.askopenfilename(filetypes=[(f"Archivos {ext}", f"*{ext}")])
        if f:
            with open(f, "r", encoding="utf-8", errors="ignore") as content:
                self.txt_consola.insert(
                    tk.END, f"\n--- LECTURA: {f} ---\n" + content.read() + "\n--- FIN ARCHIVO ---\n"
                )


if __name__ == "__main__":
    app = ECNOrquestadorGUI()
    app.mainloop()
