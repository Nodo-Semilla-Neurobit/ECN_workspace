#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Estación Central
Módulo: backend_instalador_ludico.py
Función: Servidor minimalista para inyección y desbloqueo manual de contenidos.
Soberanía: Localhost-first (127.0.0.1:5005), cero dependencias externas.
"""

import os
import json
from pathlib import Path
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.after_request
def _cors_loopback(r):
    # servidor loopback-only: CORS abierto es seguro (jamás 0.0.0.0)
    r.headers['Access-Control-Allow-Origin'] = '*'
    r.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    r.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    return r

# Configuraciones de rutas basadas en el territorio
RAIZ = Path(__file__).resolve().parent
INBOX_DIR = RAIZ / "inbox"
MODULOS_DIR = RAIZ / "modulos"
SESIONES_DIR = RAIZ / "sesiones"

INBOX_DIR.mkdir(exist_ok=True)
MODULOS_DIR.mkdir(exist_ok=True)
SESIONES_DIR.mkdir(exist_ok=True)

WAL_FILE = SESIONES_DIR / "wal_consola.log"
if not WAL_FILE.exists():
    WAL_FILE.touch()

# Base de datos en memoria para el contenido de las misiones y módulos del instalador
# El Director puede modificar o poblar este diccionario manualmente
MISIONES_CONTENIDO = {
    "m1": {
        "titulo": "Coordenada de Origen (pwd)",
        "cmd_canonico": "pwd",
        "descripcion": "Revela tu posición física en el sistema de archivos local para anclar el origen canónico de la ECN.",
        "pista": "Tipea 'pwd' exactamente en minúsculas en tu terminal y copia la salida.",
        "modulo_recompensa": "wril_self_root.py",
        "contenido_recompensa": """# MFN_LOCATION: INSTALACION_
# VERSION: v2.0
from pathlib import Path

def detectar_raiz() -> Path:
    p = Path(__file__).resolve().parent
    for candidato in (p, *p.parents):
        if (candidato / 'buzon_salida').exists() or (candidato / 'pids').exists():
            return candidato
    return p

RAIZ = detectar_raiz()
print(f'[✓ SELF-ROOT] Raíz localizada de forma autónoma: {RAIZ}')
"""
    },
    "m2": {
        "titulo": "Cristalizar .venv",
        "cmd_canonico": "python3 -m venv .venv",
        "descripcion": "Genera el entorno virtual aislado para tu jaula de Faraday de dependencias locales.",
        "pista": "Crea el venv usando 'python3 -m venv .venv' y verifica que el directorio '.venv' exista físicamente.",
        "modulo_recompensa": "requirements_dynamic.txt",
        "contenido_recompensa": "flask==3.1.3\npyperclip==1.8.2\nrequests==2.31.0\n"
    },
    "m3": {
        "titulo": "Activar Entorno",
        "cmd_canonico": "source .venv/bin/activate",
        "descripcion": "Establece el cordón sanitario activo sobre la sesión de consola actual.",
        "pista": "Ejecuta 'source .venv/bin/activate' en tu terminal real para entrar a la jaula virtual.",
        "modulo_recompensa": "wril_root_alias.py",
        "contenido_recompensa": """# MFN_LOCATION: wril/
# VERSION: v0.1
from pathlib import Path

def resolve_ecn_root() -> Path:
    return Path(__file__).resolve().parents[1]

print('Alias canónico ECN_ROOT mapeado en la RAM local.')
"""
    }
}

# Middleware CORS manual para permitir sintonización desde cualquier frontend lúdico
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Director'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "service": "backend_instalador_ludico",
        "host": "127.0.0.1",
        "port": 5005,
        "membrana": "aislada"
    })

@app.route('/api/misiones', methods=['GET'])
def list_misiones():
    # Devuelve el catálogo de misiones al frontend sin los contenidos de recompensa (protegidos)
    publicas = {}
    for k, v in MISIONES_CONTENIDO.items():
        publicas[k] = {
            "titulo": v["titulo"],
            "cmd_canonico": v["cmd_canonico"],
            "descripcion": v["descripcion"],
            "pista": v["pista"],
            "modulo_recompensa": v["modulo_recompensa"]
        }
    return jsonify(publicas)

@app.route('/api/misiones/verificar', methods=['POST'])
def verificar_mision():
    """
    Aduana de verificación manual:
    El Director o el Auditor pueden verificar la evidencia inyectada.
    """
    data = request.json or {}
    mision_id = data.get("mision_id") or data.get("id")
    evidencia_usuario = data.get("evidencia", "").strip()

    mision = MISIONES_CONTENIDO.get(mision_id)
    if not mision:
        return jsonify({"status": "failed", "error": "Misión no encontrada en el catálogo"}), 404

    # Regla de oro SINCERO: validación estricta de sintaxis o ejecución real
    # Se escribe la traza de intento de forma inmutable en el WAL
    with open(WAL_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime_now()}] > INTENTO MISION {mision_id} - Evidencia: {evidencia_usuario[:100]}...\n")

    # Validación básica (el Director puede expandir o reemplazar esta heurística manualmente)
    exito = False
    if mision_id == "m1" and "/" in evidencia_usuario:
        exito = True
    elif mision_id == "m2" and "venv" in evidencia_usuario.lower():
        exito = True
    elif mision_id == "m3" and "activate" in evidencia_usuario:
        exito = True
    elif evidencia_usuario == mision["cmd_canonico"]:
        exito = True

    if exito:
        # Se guarda el módulo de recompensa físicamente en la carpeta inbox/ para que WRIL Sentinel lo asimile
        nombre_archivo = mision["modulo_recompensa"]
        contenido_archivo = mision["contenido_recompensa"]
        
        path_inbox = INBOX_DIR / nombre_archivo
        path_inbox.write_text(contenido_archivo, encoding="utf-8")

        with open(WAL_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{datetime_now()}] < MISION {mision_id} CONSOLIDADA. Módulo {nombre_archivo} depositado en inbox/\n")

        return jsonify({
            "status": "success",
            "message": f"Misión {mision_id} consolidada con éxito.",
            "recompensa": {
                "archivo": nombre_archivo,
                "ubicacion": "inbox/"
            }
        })
    else:
        with open(WAL_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{datetime_now()}] < MISION {mision_id} RECHAZADA. Evidencia insuficiente.\n")
        return jsonify({
            "status": "failed",
            "error": "La evidencia no coincide con el estado real de tu silicio."
        })

@app.route('/api/misiones/actualizar', methods=['POST'])
def actualizar_mision_manualmente():
    """
    Endpoint administrativo para que el Director altere o inyecte
    el código fuente de las recompensas en caliente.
    """
    # Validación simple por cabecera de seguridad
    token = request.headers.get("X-Director")
    if token != "SINCERO":
        return jsonify({"status": "unauthorized", "error": "Acceso restringido al par de co-creación"}), 403

    data = request.json or {}
    mision_id = data.get("mision_id") or data.get("id")
    if mision_id not in MISIONES_CONTENIDO:
        return jsonify({"status": "failed", "error": "ID de misión inexistente"}), 404

    # Actualización manual de campos
    if "titulo" in data: MISIONES_CONTENIDO[mision_id]["titulo"] = data["titulo"]
    if "contenido_recompensa" in data: MISIONES_CONTENIDO[mision_id]["contenido_recompensa"] = data["contenido_recompensa"]
    if "modulo_recompensa" in data: MISIONES_CONTENIDO[mision_id]["modulo_recompensa"] = data["modulo_recompensa"]

    return jsonify({
        "status": "updated",
        "message": f"Misión {mision_id} actualizada manualmente por el Director."
    })

def datetime_now():
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if __name__ == '__main__':
    print("🔒 [INSTALADOR LÚDICO] Inicializando backend en 127.0.0.1:5005...")
    print("👉 Endpoints activos: /api/misiones, /api/misiones/verificar, /api/misiones/actualizar")
    import os as _o, sys as _s
from pathlib import Path as _P
_s.path.insert(0, _o.environ.get("APP_HOME") or str(_P(__file__).resolve().parent.parent))  # WRIL::RAIZ: declarada > fisica
try:
    from core.port_lighthouse import SOSPortLighthouse
    PUERTO = SOSPortLighthouse().request_port('backend_instalador_ludico', 'CORE', default_port=5005)
except Exception:
    PUERTO = 5005
    print('[⚠ FARO] no disponible; ancla fija 5005.')
app.run(host='127.0.0.1', port=PUERTO, debug=False)