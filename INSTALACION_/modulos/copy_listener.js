/*
 * Ecosistema Neurobit - Extensión Bitácora_EVA
 * Módulo: copy_listener.js (Content Script)
 * Función: Captura event-driven del acto de copiar en el DOM.
 *          En el instante del evento 'copy', la selección ES el payload:
 *          sin permisos clipboard-read, sin sondeo, sin fricción.
 * VERSION: v0.1
 */
document.addEventListener('copy', () => {
    const sel = window.getSelection();
    if (!sel || sel.isCollapsed) return;
    const texto = sel.toString();
    if (!texto.trim()) return;
    chrome.runtime.sendMessage({
        action_word: 'captura',
        class_filter: 'dom_copy',
        origen: location.hostname,
        payload: texto
    });
});
