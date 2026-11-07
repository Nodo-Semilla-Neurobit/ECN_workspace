#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Orquestador Soberano
Módulo: ecn_orquestador.py
Función: Interfaz gráfica nativa (Tkinter) para la administración del workspace.
         Reemplaza al IDE corporativo. Integra Menú Dinámico, Consola Asíncrona
         y el Lienzo de la MFN. 0.0% de fricción en el mainloop.
MFN_LOCATION: tools/ | MFN_LEVEL: 3
VERSION: v1.0
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1


import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import queue
import json
import math
import os
from pathlib import Path

# Importación del constructor de menús dinámicos (Fase 1)
try:
    from ecn_menu_builder import ECNMenuBuilder
except ImportError:
    ECNMenuBuilder = None

# ============================================================================
# CONSTANTES ESTÉTICAS (Fósforo Verde / CRT Retro)
# ============================================================================
COLOR_BG = "#0b0c10"
COLOR_PANEL = "#13131a"
COLOR_FOSFORO = "#5cff72"
COLOR_ALERTA = "#ff3048"
COLOR_TEXTO = "#cdd6f4"
FUENTE_MONO = ("Courier", 10)

# ============================================================================
# 1. EL DESPACHADOR ASÍNCRONO (Background Dispatcher)
# ============================================================================
class BackgroundDispatcher:
    """
    Ejecuta comandos del sistema operativo en hilos secundarios.
    Utiliza una cola (queue) para enviar la salida (stdout/stderr) al hilo
    principal de Tkinter sin bloquear el renderizado (0.0% fricción).
    """
    def __init__(self, text_widget: tk.Text, root_dir: Path):
        self.terminal = text_widget
        self.root_dir = root_dir
        self.q = queue.Queue()
        self.proceso_activo = None

    def ejecutar(self, comando: str, tipo: str = "shell"):
        if self.proceso_activo and self.proceso_activo.poll() is None:
            self._escribir_log("[⚠ WRIL] Ya hay un proceso en ejecución. Esperá o cancelá.\n", COLOR_ALERTA)
            return

        self._escribir_log(f"\n[>] {comando}\n", COLOR_FOSFORO)
        thread = threading.Thread(target=self._correr_proceso, args=(comando, tipo), daemon=True)
        thread.start()
        self._leer_cola()

    def _correr_proceso(self, comando: str, tipo: str):
        try:
            if tipo == "python_module":
                # Ejecución de módulo Python usando el intérprete del .venv si existe
                venv_python = self.root_dir / ".venv" / "bin" / "python3"
                python_exec = str(venv_python) if venv_python.exists() else "python3"
                self.proceso_activo = subprocess.Popen(
                    [python_exec, comando],
                    cwd=self.root_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
            else:
                self.proceso_activo = subprocess.Popen(
                    comando, shell=True,
                    cwd=self.root_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )

            for linea in self.proceso_activo.stdout:
                self.q.put(linea)
            
            self.proceso_activo.wait()
            self.q.put(f"\n[✓ FIN] Código de salida: {self.proceso_activo.returncode}\n")
        except Exception as e:
            self.q.put(f"[X ERROR] {str(e)}\n")
        finally:
            self.proceso_activo = None

    def _leer_cola(self):
        try:
            while True:
                linea = self.q.get_nowait()
                color = COLOR_ALERTA if "[X ERROR]" in linea or "Error" in linea else COLOR_TEXTO
                self._escribir_log(linea, color)
        except queue.Empty:
            pass
        # Polling suave cada 100ms para vaciar la cola sin saturar la CPU
        if self.proceso_activo or not self.q.empty():
            self.terminal.after(100, self._leer_cola)

    def _escribir_log(self, texto: str, color: str):
        self.terminal.configure(state='normal')
        self.terminal.insert(tk.END, texto, color)
        self.terminal.see(tk.END)
        self.terminal.configure(state='disabled')

# ============================================================================
# 2. EL LIENZO DE LA MFN (Visualización de Estado)
# ============================================================================
class MFN_Lienzo(tk.Canvas):
    """
    Dibuja los 7 anillos concéntricos de la Matriz Fractal Neurobitrónica.
    Lee estado_real.json para iluminar los radios vivos.
    """
    ANILLOS = ["c", "am", "na", "vi", "añ", "az", "m"]
    COLORES_ANILLOS = {
        "c": "#f9e2af", "am": "#f38ba8", "na": "#fab387", 
        "vi": "#cba6f7", "añ": "#89b4fa", "az": "#94e2d5", "m": "#a6adc8"
    }

    def __init__(self, parent, root_dir: Path, **kwargs):
        super().__init__(parent, bg=COLOR_BG, highlightthickness=0, **kwargs)
        self.root_dir = root_dir
        self.bind("<Configure>", self.redibujar)

    def redibujar(self, event=None):
        self.delete("all")
        w, h = self.winfo_width(), self.winfo_height()
        cx, cy = w / 2, h / 2
        max_r = min(cx, cy) - 20

        # Dibujar anillos base
        for i, anillo in enumerate(self.ANILLOS):
            r = max_r * ((i + 1) / len(self.ANILLOS))
            color = self.COLORES_ANILLOS[anillo]
            self.create_oval(cx-r, cy-r, cx+r, cy+r, outline=color, width=1, dash=(2, 4))
            self.create_text(cx, cy - r - 5, text=anillo, fill=color, font=("Courier", 8))

        # Dibujar centro (Observador c:G7)
        self.create_oval(cx-5, cy-5, cx+5, cy+5, fill=self.COLORES_ANILLOS["c"])

    def actualizar_estado(self):
        """Lee el territorio y enciende los radios vivos."""
        estado_file = self.root_dir / "estado_real.json"
        if not estado_file.exists():
            return
        
        try:
            with open(estado_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            w, h = self.winfo_width(), self.winfo_height()
            cx, cy = w / 2, h / 2
            max_r = min(cx, cy) - 20
            r_am = max_r * (2 / len(self.ANILLOS)) # Anillo 'am' (radios)

            componentes = {c["nombre"]: c["estado"] for c in data.get("componentes", [])}
            
            # Mapeo de radios al anillo 'am' (4 radios principales)
            radios = ["WS_SENTINEL", "DISPATCHER", "VISOR_SOBERANO", "DICTAFONO"]
            for i, radio in enumerate(radios):
                angulo = (math.pi / 2) + (i * (2 * math.pi / len(radios)))
                x = cx + r_am * math.cos(angulo)
                y = cy - r_am * math.sin(angulo)
                
                vivo = componentes.get(radio) == "ALIVE"
                color = COLOR_FOSFORO if vivo else "#333333"
                self.create_oval(x-6, y-6, x+6, y+6, fill=color, outline=color)
                
        except Exception:
            pass

# ============================================================================
# 3. EL ORQUESTADOR SOBERANO (Ventana Principal)
# ============================================================================
class ECN_Orquestador(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ECN · Orquestador Soberano · 127.0.0.1")
        self.geometry("1000x700")
        self.configure(bg=COLOR_BG)
        
        # Detección de Raíz (Ley 1)
        self.root_dir = self._detectar_raiz()
        
        self._construir_interfaz()
        self._iniciar_monitoreo()

    def _detectar_raiz(self) -> Path:
        # Lógica simplificada de wril_self_root para la GUI
        p = Path(__file__).resolve().parent
        for candidato in (p, *p.parents):
            if (candidato / "where_am_I.inf").exists() or \
               (candidato / "wril").exists() and (candidato / "core").exists():
                return candidato
        return p

    def _construir_interfaz(self):
        # 1. Barra de Menú Dinámica
        self.menu_bar = tk.Menu(self, bg=COLOR_PANEL, fg=COLOR_TEXTO, activebackground=COLOR_FOSFORO)
        self.config(menu=self.menu_bar)
        
        if ECNMenuBuilder:
            self.builder = ECNMenuBuilder(self.root_dir, self.menu_bar, self._dispatch_comando)
            self.builder.scan_territory()
            self.builder.build_menu()
        else:
            m = tk.Menu(self.menu_bar, tearoff=0)
            m.add_command(label="Escaneo fallido (ecn_menu_builder no encontrado)", state="disabled")
            self.menu_bar.add_cascade(label="Territorio", menu=m)

        # 2. Panel Principal (Dividido: Consola Izquierda, MFN Derecha)
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Panel Izquierdo: Consola de Trazabilidad
        frame_consola = tk.Frame(paned, bg=COLOR_BG)
        self.terminal = tk.Text(
            frame_consola, bg=COLOR_BG, fg=COLOR_FOSFORO, 
            font=FUENTE_MONO, insertbackground=COLOR_FOSFORO,
            state='disabled', wrap=tk.WORD
        )
        self.terminal.tag_config(COLOR_FOSFORO, foreground=COLOR_FOSFORO)
        self.terminal.tag_config(COLOR_TEXTO, foreground=COLOR_TEXTO)
        self.terminal.tag_config(COLOR_ALERTA, foreground=COLOR_ALERTA)
        
        scroll = ttk.Scrollbar(frame_consola, command=self.terminal.yview)
        self.terminal.config(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.terminal.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        paned.add(frame_consola, weight=3)

        # Panel Derecho: Lienzo MFN
        frame_mfn = tk.Frame(paned, bg=COLOR_BG)
        self.lienzo = MFN_Lienzo(frame_mfn, self.root_dir)
        self.lienzo.pack(fill=tk.BOTH, expand=True)
        paned.add(frame_mfn, weight=1)

        # Dispatcher
        self.dispatcher = BackgroundDispatcher(self.terminal, self.root_dir)

    def _dispatch_comando(self, ruta: str, tipo: str = "shell"):
        """Callback que recibe las órdenes del Menú Dinámico."""
        if tipo == "python_module":
            self.dispatcher.ejecutar(ruta, "python_module")
        else:
            # Si es un script .sh o comando de terminal
            if ruta.endswith(".sh"):
                self.dispatcher.ejecutar(f"bash {ruta}", "shell")
            else:
                self.dispatcher.ejecutar(ruta, "shell")

    def _iniciar_monitoreo(self):
        """Actualiza el lienzo de la MFN cada 2 segundos."""
        self.lienzo.redibujar()
        self.lienzo.actualizar_estado()
        self.after(2000, self._iniciar_monitoreo)

if __name__ == "__main__":
    app = ECN_Orquestador()
    app.mainloop()
