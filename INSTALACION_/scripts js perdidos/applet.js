/*
 * Ecosistema Neurobit - Estación Central Neurobitrónica
 * Módulo: applet.js (Applet de Cinnamon - CJS)
 * Función: Radio de escritorio. Escucha 'owner-change' del clipboard
 *          (push del servidor, cero polling) y deposita la carta en el
 *          buzón de salida con destello de entrega en el ícono.
 * VERSION: v0.1
 * Instalación: ~/.local/share/cinnamon/applets/neurobit@estacioncentral/
 */
const Applet = imports.ui.applet;
const Gtk = imports.gi.Gtk;
const Gdk = imports.gi.Gdk;
const GLib = imports.gi.GLib;

const RUTA_BUZON = GLib.get_home_dir() + "/NEUROBIT-Widget/buzon_salida/";

class NeurobitApplet extends Applet.IconApplet {
    constructor(metadata, orientation, panelHeight, instanceId) {
        super(metadata, orientation, panelHeight, instanceId);
        this.set_applet_icon_name("edit-paste-symbolic");
        this.set_applet_tooltip("NEUROBIT - Oficina de Correos Soberana (0.0% CPU)");
        this._ultimo = "";
        GLib.mkdir_with_parents(RUTA_BUZON, 0o755);
        this._clipboard = Gtk.Clipboard.get_default(Gdk.Display.get_default());
        this._clipboard.connect('owner-change', () => this._on_owner_change());
    }

    _on_owner_change() {
        this._clipboard.request_text((cb, texto) => this._on_texto(texto));
    }

    _on_texto(texto) {
        if (!texto || !texto.trim() || texto === this._ultimo) return;
        this._ultimo = texto;
        let ts = new Date().toISOString().replace(/[-:.TZ]/g, "").slice(0, 14);
        GLib.file_set_contents(RUTA_BUZON + "carta_applet_" + ts + ".txt", texto);
        this.set_applet_icon_name("mail-send-symbolic");   /* destello de entrega */
        GLib.timeout_add(GLib.PRIORITY_DEFAULT, 1200, () => {
            this.set_applet_icon_name("edit-paste-symbolic");
            return false;
        });
    }
}

function main(metadata, orientation, panelHeight, instanceId) {
    return new NeurobitApplet(metadata, orientation, panelHeight, instanceId);
}
