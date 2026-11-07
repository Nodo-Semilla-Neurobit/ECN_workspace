/* ============================================================
ECN · PUENTE DE MISIONES · v0.1
Conecta la interfaz con el backend lúdico (ancla Faro 5005).
Soberanía: solo loopback; cero exfiltración.
Expone: window.ECN_MISIONES (estado) y window.ECN_SellarMision(id, evidencia)
============================================================ */
(function () {
  var API = "http://127.0.0.1:5005";
  window.ECN_MISIONES = { estado: null, error: null };

  function pintar() {
    var e = window.ECN_MISIONES.estado;
    var nodo = document.getElementById("ecn-misiones-badge");
    if (!nodo) {
      nodo = document.createElement("div");
      nodo.id = "ecn-misiones-badge";
      nodo.style.cssText = "position:fixed;right:8px;bottom:8px;z-index:9999;" +
        "font:12px monospace;color:#8dff9a;background:#101018cc;" +
        "border:1px solid #2a2b36;padding:4px 8px;";
      document.body.appendChild(nodo);
    }
    if (!e) { nodo.textContent = "MISIONES: sin backend (" + (window.ECN_MISIONES.error || "?") + ")"; return; }
    var ms = Array.isArray(e.misiones) ? e.misiones :
        Object.keys(e).map(function (k) { return e[k]; })
        .filter(function (x) { return x && typeof x === "object" && x.titulo; });
    var n = ms.filter(function (m) { return m.completada || m.done; }).length;
    nodo.textContent = "RANGO " + (e.rango || e.RANGO || "?") + " · MISIONES " + n + "/" + ms.length;
  }

  function cargar() {
    fetch(API + "/api/misiones")
      .then(function (r) { if (!r.ok) throw new Error("HTTP " + r.status); return r.json(); })
      .then(function (j) { window.ECN_MISIONES.estado = j; window.ECN_MISIONES.error = null; pintar(); })
      .catch(function (err) { window.ECN_MISIONES.error = String(err); pintar(); });
  }

  window.ECN_SellarMision = function (id, evidencia) {
    return fetch(API + "/api/misiones/verificar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: id, evidencia: evidencia || "" })
    }).then(function (r) { return r.json(); })
      .then(function (j) { cargar(); return j; });
  };

  cargar();
  setInterval(cargar, 15000);
})();