#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MFN_LOCATION: tools/salon/
# MFN_LEVEL: 2
# VERSION: v3.0
"""
ECN · Salón Soberano v3.0 · Frontend Nativo (Tkinter)
Reemplaza salon_frontend.html para eludir CORS y garantizar soberanía VFS.
Principio: El filesystem es el bus. El navegador es ruido.
"""
import sys
import os
import json
import time
import threading
from datetime import datetime, timezone
from pathlib import Path

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# ─── PALETA DE COLORES (DARK MODE SOBERANO / FÓSFORO) ─────────────────────
BG_DARK = "#0b0c10"       # Fondo principal
BG_PANEL = "#13131a"      # Fondo de paneles
BG_INPUT = "#1e1e2e"      # Fondo de caja de texto
BORDER_COLOR = "#313244"  # Bordes
TEXT_MAIN = "#cdd6f4"     # Texto primario
TEXT_MUTED = "#6c7086"    # Texto secundario
ACCENT_GREEN = "#5cff72"  # 7SO (EVA)
ACCENT_PURPLE = "#cba6f7" # 9SE (PLIEGO)
ACCENT_CYAN = "#89dceb"   # LLE (DIGITAL)
ACCENT_GOLD = "#f9e2af"   # DIRECTOR
ACCENT_ALERT = "#f38ba8"  # Tensión / Error

class SalonSoberanoTkinter:
    def __init__(self, root):
        self.root = root
        self.root.title("💬 ECN · SALÓN SOBERANO v3.0 · INTERFAZ NATIVA")
        self.root.geometry("1100x750")
        self.root.minsize(900, 600)
        self.root.configure(bg=BG_DARK)

        # ─── DETECCIÓN DE RAÍZ (LEY 1 WRIL) ───
        self.RAIZ = self._detectar_raiz()
        self.SALON_DIR = self.RAIZ / "tools" / "salon" if (self.RAIZ / "tools" / "salon").exists() else self.RAIZ / "salon"
        self.HISTORIAL = self.SALON_DIR / "historial_salon.jsonl"
        self.INBOX = self.SALON_DIR / "inbox"

        self.INBOX.mkdir(parents=True, exist_ok=True)

        self.running = True
        self.last_mtime = 0
        self.filter_var = tk.StringVar(value="TODOS")

        self._setup_styles()
        self._build_ui()
        self._start_auto_refresh()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _detectar_raiz(self):
        p = Path(__file__).resolve().parent
        for c in (p, *p.parents):
            if (c / ".ecn_raiz").exists() or (c / "deploy_neurobit_estacion_v3.2.sh").exists():
                return c
        return p

    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", background=BG_DARK, foreground=TEXT_MAIN)
        self.style.configure("TFrame", background=BG_DARK)
        self.style.configure("Panel.TFrame", background=BG_PANEL, relief="flat")
        self.style.configure("TLabel", background=BG_DARK, foreground=TEXT_MAIN, font=("Courier", 10))
        self.style.configure("Header.TLabel", background=BG_DARK, foreground=ACCENT_GOLD, font=("Courier", 14, "bold"))
        self.style.configure("SubHeader.TLabel", background=BG_PANEL, foreground=ACCENT_CYAN, font=("Courier", 11, "bold"))
        self.style.configure("Muted.TLabel", background=BG_PANEL, foreground=TEXT_MUTED, font=("Courier", 9))
        self.style.configure("StatVal.TLabel", background=BG_PANEL, foreground=ACCENT_GREEN, font=("Courier", 12, "bold"))

        # Combobox y Entry
        self.style.configure("TCombobox", fieldbackground=BG_INPUT, background=BG_PANEL, foreground=TEXT_MAIN)
        self.style.configure("TEntry", fieldbackground=BG_INPUT, foreground=TEXT_MAIN)

    def _build_ui(self):
        # 1. HEADER
        header = ttk.Frame(self.root, padding=(12, 8))
        header.pack(fill=tk.X, side=tk.TOP)
        ttk.Label(header, text="💬 ECN · SALÓN SOBERANO v3.0", style="Header.TLabel").pack(side=tk.LEFT)

        status_pill = tk.Label(header, text="● VFS DIRECTO (SIN CORS)", bg="#064E3B", fg=ACCENT_GREEN,
                               font=("Courier", 9, "bold"), padx=10, pady=3)
        status_pill.pack(side=tk.LEFT, padx=15)

        # 2. MAIN CONTAINER
        main_container = ttk.Frame(self.root, padding=(10, 5))
        main_container.pack(fill=tk.BOTH, expand=True)

        # ─── PANEL IZQUIERDO (STREAM + COMPOSER) ───
        panel_left = ttk.Frame(main_container)
        panel_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # Stream
        stream_frame = ttk.Frame(panel_left, style="Panel.TFrame", padding=2)
        stream_frame.pack(fill=tk.BOTH, expand=True)

        self.stream = scrolledtext.ScrolledText(
            stream_frame, bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=TEXT_MAIN,
            font=("Courier", 10), wrap=tk.WORD, bd=0, highlightthickness=1,
            highlightbackground=BORDER_COLOR
        )
        self.stream.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Tags de sintaxis
        self.stream.tag_config("TIME", foreground=TEXT_MUTED, font=("Courier", 9))
        self.stream.tag_config("ACTION", foreground=ACCENT_CYAN, font=("Courier", 9, "bold"))
        self.stream.tag_config("7SO", foreground=ACCENT_GREEN, font=("Courier", 10, "bold"))
        self.stream.tag_config("9SE", foreground=ACCENT_PURPLE, font=("Courier", 10, "bold"))
        self.stream.tag_config("LLE", foreground=ACCENT_CYAN, font=("Courier", 10, "bold"))
        self.stream.tag_config("DIRECTOR", foreground=ACCENT_GOLD, font=("Courier", 10, "bold"))
        self.stream.tag_config("ASUNTO", foreground="#ffffff", font=("Courier", 10, "bold"))
        self.stream.tag_config("CONTENIDO", foreground=TEXT_MAIN, font=("Courier", 10))

        # Composer
        composer = ttk.Frame(panel_left, style="Panel.TFrame", padding=10)
        composer.pack(fill=tk.X, pady=(10, 0))
        ttk.Label(composer, text="📤 EMITIR CONTENEDOR (DIRECTOR)", style="SubHeader.TLabel").pack(anchor=tk.W, pady=(0, 5))

        # Fila 1: Selectores
        row1 = ttk.Frame(composer, style="Panel.TFrame")
        row1.pack(fill=tk.X, pady=5)

        ttk.Label(row1, text="Destinatario:", style="Muted.TLabel").pack(side=tk.LEFT, padx=(0, 5))
        self.cmb_dest = ttk.Combobox(row1, values=["TODOS", "7SO", "9SE", "LLE"], state="readonly", width=10)
        self.cmb_dest.set("TODOS")
        self.cmb_dest.pack(side=tk.LEFT, padx=(0, 15))

        ttk.Label(row1, text="ACTION_WORD:", style="Muted.TLabel").pack(side=tk.LEFT, padx=(0, 5))
        self.cmb_action = ttk.Combobox(row1, values=["COMUNICADO", "TASK", "CONSULTA", "INFORME"], state="readonly", width=12)
        self.cmb_action.set("COMUNICADO")
        self.cmb_action.pack(side=tk.LEFT)

        # Fila 2: Asunto
        row2 = ttk.Frame(composer, style="Panel.TFrame")
        row2.pack(fill=tk.X, pady=5)
        ttk.Label(row2, text="Asunto:", style="Muted.TLabel").pack(side=tk.LEFT, padx=(0, 5))
        self.ent_asunto = ttk.Entry(row2, font=("Courier", 10))
        self.ent_asunto.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Fila 3: Contenido
        self.txt_contenido = tk.Text(
            composer, bg=BG_INPUT, fg=TEXT_MAIN, insertbackground=TEXT_MAIN,
            font=("Courier", 10), height=4, bd=1, relief="solid", highlightthickness=1,
            highlightbackground=BORDER_COLOR
        )
        self.txt_contenido.pack(fill=tk.X, pady=5)

        # Botón Enviar
        btn_send = tk.Button(
            composer, text="⏎ SELLAR EN INBOX", bg=ACCENT_GOLD, fg="#000000",
            font=("Courier", 10, "bold"), bd=0, padx=15, pady=5, cursor="hand2",
            command=self._enviar
        )
        btn_send.pack(side=tk.RIGHT, pady=(5, 0))

        # ─── PANEL DERECHO (MÉTRICAS Y FILTROS) ───
        panel_right = ttk.Frame(main_container, style="Panel.TFrame", padding=12)
        panel_right.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        panel_right.config(width=250)

        ttk.Label(panel_right, text="📊 ESTADÍSTICAS", style="SubHeader.TLabel").pack(anchor=tk.W, pady=(0, 10))

        stats_box = ttk.Frame(panel_right, style="Panel.TFrame")
        stats_box.pack(fill=tk.X, pady=5)
        ttk.Label(stats_box, text="Total Mensajes:", style="Muted.TLabel").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.lbl_stat_total = ttk.Label(stats_box, text="0", style="StatVal.TLabel")
        self.lbl_stat_total.grid(row=0, column=1, sticky=tk.E, padx=10)

        self.lbl_last_update = ttk.Label(stats_box, text="Última act.: --:--:--", style="Muted.TLabel")
        self.lbl_last_update.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(8, 0))

        ttk.Separator(panel_right, orientation=tk.HORIZONTAL).pack(fill=tk.X, pady=15)

        ttk.Label(panel_right, text="🏷️ FILTROS (DESTINATARIO)", style="SubHeader.TLabel").pack(anchor=tk.W, pady=(0, 10))

        filters = [("☑️ TODOS", "TODOS"), ("🟢 7SO (EVA)", "7SO"), ("🟣 9SE (PLIEGO)", "9SE"), ("🔵 LLE (DIGITAL)", "LLE")]
        for text, val in filters:
            rb = tk.Radiobutton(
                panel_right, text=text, value=val, variable=self.filter_var,
                bg=BG_PANEL, fg=TEXT_MAIN, selectcolor=BG_DARK,
                activebackground=BG_PANEL, activeforeground=ACCENT_CYAN,
                font=("Courier", 10), anchor=tk.W, command=self._render_historial
            )
            rb.pack(fill=tk.X, pady=3)

    def _start_auto_refresh(self):
        def loop():
            while self.running:
                try:
                    if self.HISTORIAL.exists():
                        current_mtime = self.HISTORIAL.stat().st_mtime
                        if current_mtime != self.last_mtime:
                            self.last_mtime = current_mtime
                            self.root.after(0, self._render_historial)
                except Exception:
                    pass
                time.sleep(2)
        threading.Thread(target=loop, daemon=True).start()

    def _render_historial(self):
        self.stream.config(state=tk.NORMAL)
        self.stream.delete("1.0", tk.END)

        records = []
        if self.HISTORIAL.exists():
            with open(self.HISTORIAL, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try: records.append(json.loads(line))
                        except: pass

        self.lbl_stat_total.config(text=str(len(records)))
        self.lbl_last_update.config(text=f"Última act.: {datetime.now().strftime('%H:%M:%S')}")

        filtro = self.filter_var.get()

        # Renderizar en orden cronológico inverso (más reciente arriba)
        for rec in reversed(records):
            dest = rec.get("destinatario", "?")
            emisor = rec.get("emisor", "?")

            if filtro != "TODOS" and dest != filtro and dest != "TODOS":
                continue

            ts = rec.get("timestamp", "")[:19].replace("T", " ")
            action = rec.get("action_word", "?")
            asunto = rec.get("payload", {}).get("asunto", "(sin asunto)")
            contenido = rec.get("payload", {}).get("contenido", "")

            tag_emisor = emisor if emisor in ["7SO", "9SE", "LLE", "DIRECTOR"] else "DIRECTOR"

            self.stream.insert(tk.END, f"[{ts}] ", "TIME")
            self.stream.insert(tk.END, f"[{action}] ", "ACTION")
            self.stream.insert(tk.END, f"{emisor} → {dest}\n", tag_emisor)
            self.stream.insert(tk.END, f"  Asunto: {asunto}\n", "ASUNTO")
            if contenido:
                self.stream.insert(tk.END, f"  {contenido}\n\n", "CONTENIDO")

        self.stream.config(state=tk.DISABLED)

    def _enviar(self):
        dest = self.cmb_dest.get()
        action = self.cmb_action.get()
        asunto = self.ent_asunto.get().strip()
        contenido = self.txt_contenido.get("1.0", tk.END).strip()

        if not asunto or not contenido:
            messagebox.showwarning("Tensión Semántica", "Asunto y Contenido son obligatorios para sellar el contenedor.")
            return

        msg = {
            "boundary": f"|=•'{action}'•=|»",
            "action_word": action,
            "class": "SALON",
            "emisor": "DIRECTOR",
            "destinatario": dest,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": {
                "asunto": asunto,
                "contenido": contenido
            }
        }

        filename = self.INBOX / f"director_{int(time.time())}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(msg, f, ensure_ascii=False, indent=2)

        self.ent_asunto.delete(0, tk.END)
        self.txt_contenido.delete("1.0", tk.END)
        messagebox.showinfo("Logos Emitido", f"Contenedor sellado en inbox/\nEl Coordinador lo validará y ruteará.")

    def _on_close(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SalonSoberanoTkinter(root)
    root.mainloop()
