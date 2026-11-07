#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobitrónica - Módulo de Conciliación Ontológica (MCO) v2.1
Módulo Universal de Inspección de Metadatos MFN y Contratos YAML de la Capa WRIL.
v2.1: tail re-indentado; re.MULTILINE; RE_LOC escapado; raíz normalizada;
RUIDO canonizado; backup .pre_mco (Ley 2); ledger append-only; dry-run por diálogo.
MFN_LOCATION: tools/ | MFN_LEVEL: 3
VERSION: v2.1
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

RE_LOC = re.compile(r"MFN_LOCATION\s*[:=]\s*([^\s\"',]+)", re.IGNORECASE)
RE_LOC_FULL = re.compile(r"MFN_LOCATION\s*[:=]\s*[^\s\"',\n]+", re.IGNORECASE)
RE_YAML_KV = re.compile(r"^\s*([a-zA-Z_0-9]+)\s*:\s*['\"]?([^'\"\n]+)['\"]?", re.MULTILINE)


class NeurobitOntologyReconciler:
    RUIDO = {'.git', '__pycache__', '.venv', 'node_modules', 'ARCHIVOS_ORIGINALES',
             'archive', 'backups_wril', 'buzon_salida', 'pids'}
    EXT = {".py", ".sh", ".yaml", ".yml", ".json", ".md", ".lst"}

    def __init__(self, root):
        self.root = root
        self.root.title("Neurobit Ontology Reconciler - Universal MFN/YAML Auditor")
        self.root.geometry("1100x700")
        self.colors = {
            "bg_dark": "#13131a", "bg_panel": "#1b1b22", "accent_mfn": "#5b5ff0",
            "green_logos": "#5cff72", "red_tension": "#ff3048",
            "text_light": "#cdd6f4", "border": "#313244",
        }
        self.project_dir = tk.StringVar(value=os.getcwd())
        self.discrepancies = []
        self.configure_styles()
        self.create_widgets()

    def configure_styles(self):
        self.root.configure(bg=self.colors["bg_dark"])
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", background=self.colors["bg_panel"], foreground=self.colors["text_light"])
        style.configure("TFrame", background=self.colors["bg_dark"])
        style.configure("Panel.TFrame", background=self.colors["bg_panel"])
        style.configure("TLabel", background=self.colors["bg_panel"],
                        font=("Courier", 10), foreground=self.colors["text_light"])
        style.configure("Action.TButton", background=self.colors["accent_mfn"],
                        foreground="#ffffff", font=("Courier", 9, "bold"))
        style.map("Action.TButton", background=[("active", self.colors["green_logos"])])
        style.configure("Treeview", background="#1e1e2e", fieldbackground="#1e1e2e",
                        foreground=self.colors["text_light"], font=("Courier", 9))
        style.configure("Treeview.Heading", background=self.colors["bg_panel"],
                        foreground=self.colors["accent_mfn"], font=("Courier", 10, "bold"))

    def create_widgets(self):
        main_container = ttk.Frame(self.root, style="TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        top_bar = ttk.Frame(main_container, style="Panel.TFrame")
        top_bar.pack(fill=tk.X, side=tk.TOP, pady=(0, 10))
        ttk.Label(top_bar, text="Raíz Territorial (ECN_ROOT):").pack(side=tk.LEFT, padx=10, pady=10)
        entry_path = tk.Entry(top_bar, textvariable=self.project_dir, font=("Courier", 10),
                              bg="#2a2b36", fg=self.colors["text_light"], relief="flat", width=50)
        entry_path.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.X, expand=True)
        ttk.Button(top_bar, text="ESCANEAR CAPA MFN/YAML", style="Action.TButton",
                   command=self.audit_project_alignment).pack(side=tk.RIGHT, padx=10, pady=10)

        middle_frame = ttk.Frame(main_container, style="Panel.TFrame")
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        columns = ("archivo", "tipo", "mfn_location", "identidad_yaml", "estado")
        self.tree = ttk.Treeview(middle_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("archivo", text="Artefacto Local")
        self.tree.heading("tipo", text="Estructura")
        self.tree.heading("mfn_location", text="Declaración MFN")
        self.tree.heading("identidad_yaml", text="Protocolo / Action_Word")
        self.tree.heading("estado", text="Fidelidad Real")
        self.tree.column("archivo", width=220)
        self.tree.column("tipo", width=100)
        self.tree.column("mfn_location", width=180)
        self.tree.column("identidad_yaml", width=250)
        self.tree.column("estado", width=160)
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar = ttk.Scrollbar(middle_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)

        bottom_bar = ttk.Frame(main_container, style="Panel.TFrame")
        bottom_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        self.lbl_status = ttk.Label(bottom_bar, text="Reposo Sincero: Sistema en espera de estímulo.",
                                    font=("Courier", 9))
        self.lbl_status.pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(bottom_bar, text="SINCRO-ALINEACIÓN DE DERIVA", style="Action.TButton",
                   command=self.resolve_all_tensions).pack(side=tk.RIGHT, padx=10, pady=10)

    @staticmethod
    def _norm(p: str) -> str:
        p = p.replace("\\", "/").strip("./").strip()
        return "." if p == "" else p

    def extract_yaml_fields(self, content: str) -> dict:
        fields = {}
        for key, val in RE_YAML_KV.findall(content):
            fields[key.strip()] = val.strip()
        return fields

    def _ledger(self, base: Path, ruta: str, vieja: str, nueva: str):
        lg = base / "mco_ledger.jsonl"
        with lg.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"t": datetime.now().isoformat(), "path": ruta,
                                "decl_vieja": vieja, "decl_nueva": nueva},
                               ensure_ascii=False) + "\n")

    def audit_project_alignment(self):
        base_path = Path(self.project_dir.get().strip())
        if not base_path.is_dir():
            messagebox.showerror("Ruptura Territorial",
                                 "La ruta provista no corresponde a un directorio físico válido.")
            return
        self.discrepancies.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for root, dirs, files in os.walk(base_path):
            dirs[:] = [d for d in dirs if d not in self.RUIDO]
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() not in self.EXT:
                    continue
                rel = str(file_path.relative_to(base_path)).replace("\\", "/")
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        snippet = f.read(4096)
                except Exception:
                    continue
                m = RE_LOC.search(snippet)
                declared = self._norm(m.group(1)) if m else "Soberanía Pendiente"
                actual = self._norm(str(file_path.relative_to(base_path).parent))
                has_deriva = bool(m) and declared != actual
                yaml_info = "No aplica (Código)"
                tipo = "Script"
                if file_path.suffix.lower() in (".yaml", ".yml"):
                    tipo = "Contrato YAML"
                    yf = self.extract_yaml_fields(snippet)
                    pid, aw, mid = yf.get("PROTOCOL_ID"), yf.get("ACTION_WORD"), yf.get("MESSAGE_ID")
                    if pid or aw:
                        yaml_info = f"Pid: {pid or '?'} | Act: {aw or '?'}"
                    elif mid:
                        yaml_info = f"Msg_ID: {mid}"
                    else:
                        yaml_info = "Estructura YAML vacía/parásita"
                if has_deriva:
                    estado = "🚨 DERIVA TERRITORIAL"
                    self.discrepancies.append({"path": file_path, "decl": declared,
                                               "actual_loc": actual})
                elif declared == "Soberanía Pendiente" and tipo == "Script":
                    estado = "🔍 SIN CABECERA"
                else:
                    estado = "✔ SINCRO OK"
                self.tree.insert("", tk.END, values=(rel, tipo, declared, yaml_info, estado))
        self.lbl_status.config(text=f"Censo Completado. Artefactos en deriva: {len(self.discrepancies)}")

    def resolve_all_tensions(self):
        if not self.discrepancies:
            messagebox.showinfo("Estación en Paz",
                                "No se detectan señales de tensión activa en los compartimentos.")
            return
        base_path = Path(self.project_dir.get().strip())
        muestra = "\n".join(f"- {d['path'].name}: {d['decl']} → {d['actual_loc']}"
                            for d in self.discrepancies[:8])
        mas = f"\n… y {len(self.discrepancies) - 8} más" if len(self.discrepancies) > 8 else ""
        if not messagebox.askyesno("Dry-run: confirmá la sincro",
                                   f"Se reescribirán {len(self.discrepancies)} declaraciones.\n"
                                   f"Cada una tendrá backup .pre_mco y asiento en mco_ledger.jsonl.\n\n"
                                   f"{muestra}{mas}\n\n¿Proceder?"):
            return
        resolved = 0
        for disc in self.discrepancies:
            file_path = disc["path"]
            actual_loc = disc["actual_loc"]
            try:
                shutil.copy2(file_path, file_path.with_suffix(file_path.suffix + ".pre_mco"))
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                corrected = RE_LOC_FULL.sub(f"MFN_LOCATION: {actual_loc}", content, count=1)
                tmp = file_path.with_suffix(file_path.suffix + ".tmp")
                with open(tmp, "w", encoding="utf-8") as f:
                    f.write(corrected)
                os.replace(tmp, file_path)
                self._ledger(base_path, str(file_path.relative_to(base_path)),
                             disc["decl"], actual_loc)
                resolved += 1
            except Exception as e:
                messagebox.showerror("Fricción en Disco",
                                     f"No se pudo escribir el cambio en {file_path.name}: {e}")
        self.audit_project_alignment()
        messagebox.showinfo("Consolidación Terminada",
                            f"Se han realineado {resolved} declaraciones de compartimento.")


if __name__ == "__main__":
    root = tk.Tk()
    app = NeurobitOntologyReconciler(root)
    root.mainloop()