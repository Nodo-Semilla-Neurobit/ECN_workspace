#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MFN_LOCATION: ./
# MFN_LEVEL: 2
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: neurobit_gnome_widget.py (Visor Soberano v2.0)
Función: Visor GTK3 del Staging Buffer sin polling: despierta con inotify
         (IN_MODIFY/IN_CLOSE_WRITE) y con SIGUSR1 del puente HID.
         Commit transaccional al Ledger inmutable.
VERSION: v2.0
"""
import os
import signal
import subprocess
import ctypes
import ctypes.util
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

from neurobit_clipboard_core import (
    ARCHIVO_TEMPORAL, capturar_evento_hid, ejecutar_commit_verificado)

_libc = ctypes.CDLL(ctypes.util.find_library("c"), use_errno=True)
IN_MODIFY = 0x00000002
IN_CLOSE_WRITE = 0x00000008

class NeurobitSovereignWidget(Gtk.Window):
    def __init__(self):
        super().__init__(title="NEUROBIT — Visor Soberano v2.0")
        self.set_default_size(460, 360)
        self.set_keep_above(True)
        self._ultimo_tamanio = -1
        self._init_ui()
        self._init_reactiva()
        self._recargar()
        self.show_all()

    def _init_ui(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        for m in ("start", "end", "top", "bottom"):
            box.set_margin_start(12) if m == "start" else None
        box.set_margin_start(12); box.set_margin_end(12)
        box.set_margin_top(12); box.set_margin_bottom(12)
        self.add(box)
        self.buf = Gtk.TextBuffer()
        view = Gtk.TextView(buffer=self.buf)
        view.set_editable(False); view.set_monospace(True)
        scroll = Gtk.ScrolledWindow(); scroll.set_vexpand(True)
        scroll.add(view)
        box.pack_start(scroll, True, True, 0)
        btn = Gtk.Button(label="⚡ Confirmar y volcar al Ledger")
        btn.connect("clicked", self._on_commit)
        box.pack_start(btn, False, False, 0)
        self.connect("destroy", lambda w: Gtk.main_quit())

    def _init_reactiva(self):
        # Canal A: inotify sobre el buzón de staging (cero polling)
        fd = _libc.inotify_init()
        _libc.inotify_add_watch(
            fd, str(ARCHIVO_TEMPORAL.parent).encode(),
            IN_MODIFY | IN_CLOSE_WRITE)
        GLib.io_add_watch(fd, GLib.IO_IN, self._on_vfs)
        # Canal B: SIGUSR1 del puente HID
        GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGUSR1,
                             self._on_usr1)

    def _on_vfs(self, fd, cond):
        os.read(fd, 4096)
        self._recargar()
        return True

    def _on_usr1(self):
        capturar_evento_hid()
        self._recargar()
        return True

    def _recargar(self):
        try:
            t = ARCHIVO_TEMPORAL.stat().st_size \
                if ARCHIVO_TEMPORAL.exists() else 0
        except OSError:
            t = 0
        if t != self._ultimo_tamanio:
            self._ultimo_tamanio = t
            self.buf.set_text(
                ARCHIVO_TEMPORAL.read_text(encoding="utf-8") if t else
                "--- Buffer vacío: esperando interrupción HID (F8) ---")

    def _on_commit(self, btn):
        try:
            if ejecutar_commit_verificado():
                self._notificar("Éxito",
                    "Captura asentada de forma inmutable en el Ledger.")
        except Exception as e:
            self._notificar("Error crítico VFS", str(e))
        self._recargar()

    def _notificar(self, titulo, mensaje):
        d = Gtk.MessageDialog(
            transient_for=self, flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK, text=titulo)
        d.format_secondary_text(mensaje)
        d.run(); d.destroy()

if __name__ == "__main__":
    # Control de Oficio: purga huérfanos de sí mismo
    pid_actual = os.getpid()
    try:
        for p in subprocess.check_output(
                ["pgrep", "-f", "neurobit_gnome_widget.py"]
                ).decode().split():
            if int(p) != pid_actual:
                os.kill(int(p), signal.SIGTERM)
    except Exception:
        pass
    win = NeurobitSovereignWidget()
    Gtk.main()
