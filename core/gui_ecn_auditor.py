#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Estación Central Neurobitrónica (ECN) v3.2
Módulo: core/gui_ecn_central.py
Función: Panel Orquestador Soberano en Tkinter. Nuclea microsistemas de control,
         censo territorial por listas .lst, inyección de headers MFN,
         auditoría estática/dinámica y despliegue asíncrono en background.
MFN_LOCATION: core/
MFN_LEVEL: 1
VERSION: v3.2
"""
import sys
import os
import re
import json
import shutil
import threading
import subprocess
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# Inyección de self-path para evitar ModuleNotFoundError al invocar hermanos
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "wril"))

class ECNCentralStation(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("☉ ECN · ESTACIÓN CENTRAL NEUROBITRÓNICA v3.2 · PANÓPTICO INVERTIDO")
        self.geometry("1150x750")
        
        # Coordenadas y variables de entorno canónicas
        self.raiz_ecn = self.detectar_raiz()
        self.archivo_actual = None
        self.scanned_files = []
        
        # Paleta de color industrial in-memory (Fósforo verde + Violeta MFN)
        self.colors = {
            "bg_dark": "#0a0c10",      "bg_panel": "#141721",     "border": "#2b303c",
            "ink_logos": "#5cff72",    "neon_violet": "#a394ff",  "tension": "#ff3048",
            "gold_sincerity": "#f9e2af","text_light": "#cdd6f4",  "highlight": "#1e2233"
        }
        
        self.configure_styles()
        self.create_layout()
        self.log_interface(f"[✓ ANCLA] Raíz localizada de forma autónoma: {self.raiz_ecn}")
        self.scan_territorio_init()

    def detectar_raiz(self) -> Path:
        p = Path(__file__).resolve().parent
        for candidato in (p, *p.parents):
            if (candidato / "where_am_I.inf").exists() or (candidato / "deploy_neurobit_estacion_v3.2.sh").exists():
                return candidato
        return p

    def configure_styles(self):
        self.configure(bg=self.colors["bg_dark"])
        style = ttk.Style()
        style.theme_use("clam")
        
        style.configure(".", background=self.colors["bg_panel"], foreground=self.colors["text_light"], fieldbackground=self.colors["bg_dark"])
        style.configure("TFrame", background=self.colors["bg_dark"])
        style.configure("Panel.TFrame", background=self.colors["bg_panel"], relief="flat", borderwidth=1)
        style.configure("TLabel", background=self.colors["bg_panel"], foreground=self.colors["text_light"], font=("Courier", 10))
        style.configure("Header.TLabel", font=("Courier", 11, "bold"), foreground=self.colors["neon_violet"])
        style.configure("TButton", font=("Courier", 9, "bold"), background=self.colors["highlight"], foreground=self.colors["text_light"], relief="flat")
        style.map("TButton", background=[("active", self.colors["neon_violet"])], foreground=[("active", "#ffffff")])
        style.configure("Action.TButton", background=self.colors["neon_violet"], foreground="#ffffff")
        style.map("Action.TButton", background=[("active", self.colors["ink_logos"])])

    def create_layout(self):
        # Menú Superior del Escriba
        menu_bar = tk.Menu(self, bg=self.colors["bg_panel"], fg=self.colors["text_light"], activebackground=self.colors["neon_violet"], relief="flat")
        
        menu_estacion = tk.Menu(menu_bar, tearoff=0, bg=self.colors["bg_panel"], fg=self.colors["text_light"])
        menu_estacion.add_command(label="[Init ECN Daemon]", command=self.background_init_ecn)
        menu_estacion.add_command(label="[Halt Estación (Gracioso)]", command=self.background_halt_ecn)
        menu_estacion.add_separator()
        menu_estacion.add_command(label="[Salir sin rastro]", command=self.quit)
        menu_bar.add_cascade(label="Módulos", menu=menu_estacion)
        
        menu_audit = tk.Menu(menu_bar, tearoff=0, bg=self.colors["bg_panel"], fg=self.colors["text_light"])
        menu_audit.add_command(label="[Auditar Censo Estático]", command=self.run_static_audit)
        menu_audit.add_command(label="[Probar Muelles Dinámicos]", command=self.run_dynamic_audit)
        menu_bar.add_cascade(label="Auditoría", menu=menu_audit)
        
        self.config(menu=menu_bar)

        # Contenedor de paneles distribuidos
        grid_container = ttk.Frame(self, style="TFrame")
        grid_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # PANEL IZQUIERDO: El Censo Territorial por Listas
        self.panel_left = ttk.Frame(grid_container, style="Panel.TFrame")
        self.panel_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        ttk.Label(self.panel_left, text="CENSO TERRITORIAL (.lst)", style="Header.TLabel").pack(anchor=tk.W, padx=10, pady=8)
        
        # Filtro rápido de extensión
        self.var_filtro = tk.StringVar(value="Todos")
        combo_filtro = ttk.Combobox(self.panel_left, textvariable=self.var_filtro, state="readonly", values=["Todos", ".py", ".sh", ".yaml", ".json", ".c", ".md", "Tensiones"])
        combo_filtro.pack(fill=tk.X, padx=10, pady=2)
        combo_filtro.bind("<<ComboboxSelected>>", lambda e: self.filtrar_censo())

        list_frame = ttk.Frame(self.panel_left, style="TFrame")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scry = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.listbox_files = tk.Listbox(list_frame, font=("Courier", 9), bg=self.colors["bg_dark"], fg=self.colors["text_light"], selectbackground=self.colors["neon_violet"], yscrollcommand=scry.set, relief="flat", highlightthickness=1, highlightbackground=self.colors["border"])
        scry.config(command=self.listbox_files.yview)
        scry.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_files.pack(fill=tk.BOTH, expand=True)
        self.listbox_files.bind("<<ListboxSelect>>", self.on_artefacto_selected)

        # PANEL DERECHO: El Visor de Código e Inoculación
        self.panel_right = ttk.Frame(grid_container, style="Panel.TFrame")
        self.panel_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.lbl_editor_title = ttk.Label(self.panel_right, text="VISOR SOBERANO DE ARTEFACTOS", style="Header.TLabel")
        self.lbl_editor_title.pack(anchor=tk.W, padx=10, pady=8)
        
        self.text_editor = scrolledtext.ScrolledText(self.panel_right, font=("Courier", 10), bg=self.colors["bg_dark"], fg=self.colors["text_light"], insertbackground=self.colors["text_light"], relief="flat", highlightthickness=1, highlightbackground=self.colors["border"])
        self.text_editor.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Barra de detalle integrada sanada
        self.lbl_file_details = ttk.Label(self.panel_right, text="Selecciona un glifo del censo...", font=("Courier", 8), foreground=self.colors["gold_sincerity"])
        self.lbl_file_details.pack(anchor=tk.W, padx=10, pady=2)

        # Botonera inferior de control quirúrgico
        panel_acciones = ttk.Frame(self.panel_right, style="Panel.TFrame")
        panel_acciones.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(panel_acciones, text="[Inocular Header MFN]", command=self.inyectar_mfn_header_ui).pack(side=tk.LEFT, padx=5)
        ttk.Button(panel_acciones, text="[Sellar Cambios en Disco]", style="Action.TButton", command=self.guardar_archivo_ui).pack(side=tk.RIGHT, padx=5)

        # PANEL INFERIOR: Consola de Trazabilidad Unificada
        self.panel_bottom = ttk.Frame(self, style="Panel.TFrame")
        self.panel_bottom.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0), padx=10)
        
        ttk.Label(self.panel_bottom, text="TRAZABILIDAD EN BACKGROUND (WAL logs):", font=("Courier", 9, "bold")).pack(anchor=tk.W, padx=10, pady=(5,0))
        self.txt_console = scrolledtext.ScrolledText(self.panel_bottom, height=8, font=("Courier", 9), bg="#050508", fg=self.colors["ink_logos"], insertbackground="white", relief="flat")
        self.txt_console.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def log_interface(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.txt_console.insert(tk.END, f"[{timestamp}] >> {message}\n")
        self.txt_console.see(tk.END)

    def dispatch_background_task(self, cmd, success_msg, error_msg):
        def task():
            try:
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=str(self.raiz_ecn))
                stdout, stderr = proc.communicate()
                if proc.returncode == 0:
                    self.after(0, lambda: self.log_interface(f"[OK] {success_msg}\n{stdout.strip()}"))
                else:
                    self.after(0, lambda: self.log_interface(f"[ERROR] {error_msg}\n{stderr.strip()}"))
            except Exception as e:
                self.after(0, lambda: self.log_interface(f"[CRITICAL] Error de ejecución: {str(e)}"))
        threading.Thread(target=task, daemon=True).start()

    def background_init_ecn(self):
        self.log_interface("Despertando componentes Neurobitrónicos de la ECN...")
        self.dispatch_background_task(["/bin/bash", "deploy_neurobit_estacion_v3.2.sh"], "Estación levantada y sincronizada en background.", "Fallo en el runbook de despliegue.")

    def background_halt_ecn(self):
        self.log_interface("Enviando señal de repliegue ético (HALT gracioso)...")
        # Invoca al Halt atómico mediante matar al orquestador master de la shell
        self.dispatch_background_task(["pkill", "-INT", "-f", "deploy_neurobit_estacion"], "Señal de Halt inyectada al Kernel.", "Fallo al gatillar reposo.")

    def scan_territorio_init(self):
        if not (self.raiz_ecn / "path_map.json").exists():
            try:
                from wril_path_map import generar_mapa
                generar_mapa(self.raiz_ecn, self.raiz_ecn / "path_map.json")
            except ImportError:
                pass
        self.cargar_datos_censo()

    def cargar_datos_censo(self):
        self.scanned_files.clear()
        path_map_file = self.raiz_ecn / "path_map.json"
        if not path_map_file.exists():
            return
        try:
            mapa = json.loads(path_map_file.read_text(encoding="utf-8"))
            for rel_path, abs_path in mapa.items():
                p = Path(abs_path)
                if not p.exists():
                    continue
                with open(p, "r", encoding="utf-8", errors="ignore") as f:
                    snippet = f.read(500)
                
                loc_match = re.search(r"MFN_LOCATION\s*[:=]\s*([^\s\"',]+)", snippet, re.IGNORECASE)
                mfn_loc = loc_match.group(1).strip() if loc_match else None
                
                tension = False
                if mfn_loc:
                    norm_loc = mfn_loc.strip("./").replace("\\", "/")
                    actual_folder = str(p.relative_to(self.raiz_ecn).parent).replace("\\", "/")
                    if actual_folder == ".":
                        actual_folder = ""
                    if norm_loc != actual_folder and mfn_loc not in ["./", "."] and norm_loc != "":
                        tension = True
                
                self.scanned_files.append({
                    "rel": rel_path, "abs": abs_path, "name": p.name,
                    "ext": p.suffix.lower(), "mfn_loc": mfn_loc, "tension": tension
                })
            self.filtrar_censo()
        except Exception as e:
            self.log_interface(f"Error cargando censo: {e}")

    def filtrar_censo(self):
        filtro = self.var_filtro.get()
        self.listbox_files.delete(0, tk.END)
        self.filtered_mapping = []
        for f in self.scanned_files:
            match = False
            if filtro == "Todos": match = True
            elif filtro == "Tensiones" and f["tension"]: match = True
            elif filtro == f["ext"]: match = True
            
            if match:
                self.filtered_mapping.append(f)
                prefix = "[💥T]" if f["tension"] else ("[✓]" if f["mfn_loc"] else "[ ]")
                self.listbox_files.insert(tk.END, f"{prefix} {f['rel']}")
                
                idx = self.listbox_files.size() - 1
                if f["tension"]:
                    self.listbox_files.itemconfig(idx, foreground=self.colors["tension"])
                elif f["mfn_loc"]:
                    self.listbox_files.itemconfig(idx, foreground=self.colors["ink_logos"])

    def on_artefacto_selected(self, event):
        selection = self.listbox_files.curselection()
        if not selection:
            return
        f_data = self.filtered_mapping[selection[0]]
        self.archivo_actual = Path(f_data["abs"])
        self.lbl_file_details.config(text=f"Físico: {f_data['abs']} | Declarado MFN: {f_data['mfn_loc'] or 'AUSENTE'}")
        try:
            content = self.archivo_actual.read_text(encoding="utf-8", errors="ignore")
            self.text_editor.delete("1.0", tk.END)
            self.text_editor.insert(tk.END, content)
        except Exception as e:
            self.log_interface(f"Error al abrir archivo: {e}")

    def inyectar_mfn_header_ui(self):
        if not self.archivo_actual:
            return
        ext = self.archivo_actual.suffix.lower()
        rel_parent = str(self.archivo_actual.relative_to(self.raiz_ecn).parent).replace("\\", "/")
        parent_tag = "./" if rel_parent in (".", "") else f"{rel_parent}/"
        
        header = f"# MFN_LOCATION: {parent_tag}\n# MFN_LEVEL: 1\n# MFN_COORD: (7,7)\n"
        if ext in (".js", ".c", ".h"):
            header = f"// MFN_LOCATION: {parent_tag}\n// MFN_LEVEL: 1\n// MFN_COORD: (7,7)\n"
        elif ext == ".md":
            header = f"<!--\nMFN_LOCATION: {parent_tag}\nMFN_LEVEL: 1\n-->\n"
            
        self.text_editor.insert("1.0", header)
        self.log_interface(f"Header inyectado en búfer para {self.archivo_actual.name}. Guarde para consolidar.")

    def guardar_archivo_ui(self):
        if not self.archivo_actual:
            return
        content = self.text_editor.get("1.0", tk.END)
        if content.endswith("\n"): content = content[:-1]
        try:
            if self.archivo_actual.exists():
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                sub_dir = self.raiz_ecn / "archive" / "backups"
                sub_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(self.archivo_actual, sub_dir / f"{self.archivo_actual.stem}_{ts}{self.archivo_actual.suffix}")
            self.archivo_actual.write_text(content, encoding="utf-8")
            self.log_interface(f"[GUARDADO] {self.archivo_actual.name} consolidado con éxito.")
            self.cargar_datos_censo()
        except Exception as e:
            self.log_interface(f"Fallo al guardar: {e}")

    def generate_report(self) -> Path:
        output_path = self.raiz_ecn / "data" / "runtime" / "sos_linker_report.json"
        return output_path

    def run_static_audit(self):
        self.log_interface("Lanzando Auditoría Estática de imports y huérfanos...")
        self.dispatch_background_task(["python3", "tools/sos_module_linker_tester.py"], "Censo de imports finalizado. Ver data/sos_linker_report.json", "Fallo en el analizador de ast.")

    def run_dynamic_audit(self):
        self.log_interface("Sondeando puertos y contratos en localhost...")
        self.dispatch_background_task(["python3", "wril/wril_integridad_json.py"], "Auditoría dinámica de muelles concluida.", "Fallo en el escáner de sockets.")
    
if __name__ == "__main__":
    app = ECNCentralStation()
    app.mainloop()
