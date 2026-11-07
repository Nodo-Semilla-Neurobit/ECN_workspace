/*
 * Ecosistema Neurobit - Extensión Bitácora_EVA
 * Módulo: background.js (Service Worker MV3)
 * Función: Postman HTTP. Entrega la carta del content script al endpoint
 *          local de sala_app.py. Con cola de reintegro si la Estación duerme.
 * VERSION: v0.1
 * manifest: "host_permissions": ["http://127.0.0.1/*"]
 */
const ENDPOINT = "http://127.0.0.1:5000/ingesta_neurobit";

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action_word !== "captura") return false;
    entregar(msg).then(ok => sendResponse({ estado: ok ? "ENTREGADA" : "EN_COLA" }));
    return true;   /* mantiene abierto el canal asíncrono */
});

async function entregar(carta) {
    try {
        const r = await fetch(ENDPOINT, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(carta)
        });
        if (!r.ok) throw new Error("HTTP " + r.status);
        return true;
    } catch (e) {
        const { pendientes = [] } = await chrome.storage.local.get("pendientes");
        pendientes.push(carta);
        await chrome.storage.local.set({ pendientes });
        setTimeout(reintentar, 30000);
        return false;
    }
}

async function reintentar() {
    const { pendientes = [] } = await chrome.storage.local.get("pendientes");
    if (!pendientes.length) return;
    const quedan = [];
    for (const carta of pendientes) {
        try {
            const r = await fetch(ENDPOINT, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(carta)
            });
            if (!r.ok) throw 0;
        } catch (e) { quedan.push(carta); }
    }
    await chrome.storage.local.set({ pendientes: quedan });
}
