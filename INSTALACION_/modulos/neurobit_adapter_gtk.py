#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: neurobit_adapter_gtk.py
Función: Adaptador de materialización event-driven (X11/Cinnamon).
         Escucha 'owner-change' del Clipboard GTK: el servidor gráfico
         empuja el evento. Cero sondeo. La persistencia recibe el Logos
         íntegro; el filtro visual vive solo en la capa de presentación.
VERSION: v0.1
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class AdaptadorClipboardGTK:
    def __init__(self, callback_volcado):
        self.callback = callback_volcado
        self._ultimo = ""
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.clipboard.connect('owner-change', self._on_owner_change)

    def _on_owner_change(self, clipboard, event):
        clipboard.request_text(self._on_texto)

    def _on_texto(self, clipboard, texto):
        if not texto or not texto.strip():
            return                   # binario/imagen: descarte silencioso
        if texto == self._ultimo:
            return                   # re-anuncio del owner: duplicado
        self._ultimo = texto
        self.callback(texto)         # el Logos íntegro viaja al buzón
