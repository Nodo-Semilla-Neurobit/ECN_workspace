#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os

class ECN_Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("ECN - Estación Central Neurobitrónica")
        self.root.geometry("650x500")
        self.root.configure(bg="#1e1e2e") # Estética oscura industrial

        # Estilos de la interfaz
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Courier', 11, 'bold'), foreground='#ffffff', background='#313244')
        self.style.configure('TLabel', font=('Courier', 10), background='#1e1e2e', foreground='#cdd6f4')

        # --- PANEL SUPERIOR: BOTONES DE CONTROL GENERAL ---
        self.frame_top = tk.Frame(root, bg="#1e1e2e", padx=10, pady=10)
        self.frame_top.pack(fill=tk.X)

        # botones superiores
        buttons = [
            ("[Add Modules]", self.action_add_modules),
            ("[Adapter_Create]", self.action_adapter_create),
            ("[Assembly]", self.action_assembly),
            ("[Init ECN]", self.action_init_ecn),
            ("[Config]", self.action_config),
            ("[Exit]", root.quit)
        ]

        for text, command in buttons:
            btn = ttk.Button(self.frame_top, text=text, command=command)
            btn.pack(side=tk.LEFT, padx=4, pady=5, expand=True, fill=tk.X)

        # --- PANEL INFERIOR: EXPLORADOR Y ESTADO ---
        self.frame_bottom = tk.Frame(root, bg="#181825", bd=2, relief=tk.SUNKEN)
        self.frame_bottom.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.lbl_status = ttk.Label(self.frame_bottom, text="Sistema ECN Listo. Esperando Inicialización...", background="#181825")
        self.lbl_status.pack(anchor=tk.W, padx=10, pady=5)

        # Consola integrada para ver la salida de los procesos de trazabilidad
        self.txt_console = tk.Text(self.frame_bottom, bg="#11111b", fg="#a6e3a1", font=('Courier', 10), insertbackground='white')
        self.txt_console.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # --- CONTROLADORES DE EVENTOS (ACCIONES) ---
    
    def log(self, message):
        """Escribe eventos en la consola interna de la GUI"""
        self.txt_console.insert(tk.END, f">> {message}\n")
        self.txt_console.see(tk.END)

    def action_init_ecn(self):
        self.log("Iniciando componentes Neurobitrónicos en background...")
        self.lbl_status.config(text="Estado: ECN Inicializándose (Background activos)")
        
        # Ejecución en Background No Bloqueante de  scripts de inicio del sistema
        try:
            # Reemplazar por script real de arranque de la última versión.
            subprocess.Popen(["/bin/bash", "init_system.sh"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.log("[OK] Demonio de inicio acoplado con éxito.")
        except Exception as e:
            self.log(f"[ERROR] No se pudo lanzar el script de inicio: {str(e)}")

    def action_add_modules(self):
        self.log("Abriendo explorador para añadir nuevo módulo .py...")
        # Lógica de exploración integrada para seleccionar el .py
        file_selected = filedialog.askopenfilename(
            title="Seleccionar Módulo Python para ECN",
            filetypes=[("Módulos Python", "*.py")]
        )
        
        if file_selected:
            self.log(f"Módulo detectado: {os.path.basename(file_selected)}")
            # Aquí es donde se dispara la rutina automática de trazabilidad (.OLD, backups y tests)
            self.log(f"Lanzando secuencia de trazabilidad para {os.path.basename(file_selected)}...")
            
            try:
                # Ejecutar script de trazabilidad (ej.sh creado en el paso anterior)
                process = subprocess.Popen(
                    ["/bin/bash", "[REAL_NAME].sh", file_selected], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate()
                self.log(stdout.strip())
                if stderr:
                    self.log(f"[WARN] {stderr.strip()}")
            except Exception as e:
                self.log(f"[CRITICAL] Error en pipeline de trazabilidad: {str(e)}")

    def action_adapter_create(self):
        self.log("Ejecutando rutina: [Adapter_Create]")
        # Lógica o llamada a .sh aquí

    def action_assembly(self):
        self.log("Ejecutando rutina: [Assembly]")
        # Lógica o llamada a .sh aquí

    def action_config(self):
        self.log("Abriendo panel de configuración interna de la ECN...")
        # Lógica o llamada a .sh aquí

if __name__ == "__main__":
    root = tk.Tk()
    app = ECN_Dashboard(root)
    root.mainloop()

