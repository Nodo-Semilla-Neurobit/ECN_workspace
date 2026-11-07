#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ECN · Salón Soberano v3.0 · Coordinador Local
Lee inbox/, valida contenedores Neurobit, rutea a outbox/, sella en historial.
Sin API externa. Sin postman humano. Filesystem como bus de comunicación.
"""
import json
import os
import sys
import time
import hashlib
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ---------- Configuración ----------
SALON_ROOT = Path(__file__).resolve().parent
INBOX = SALON_ROOT / "inbox"
OUTBOX = SALON_ROOT / "outbox"
HISTORIAL = SALON_ROOT / "historial_salon.jsonl"
AGENTES_DIR = SALON_ROOT / "agentes"

# Crear estructura si no existe
for d in [INBOX, OUTBOX, AGENTES_DIR]:
    d.mkdir(exist_ok=True)
for sub in ["para_7so", "para_9se", "para_lle", "para_todos"]:
    (OUTBOX / sub).mkdir(exist_ok=True)


# ---------- Validación de contenedores Neurobit ----------
def validar_contenedor(msg: dict) -> tuple[bool, str]:
    """Valida que el mensaje cumpla Neurobit Protocol v1.1"""
    campos_requeridos = ["boundary", "action_word", "emisor", "destinatario", "timestamp", "payload"]
    for campo in campos_requeridos:
        if campo not in msg:
            return False, f"Campo requerido faltante: {campo}"
    
    # Validar BOUNDARY (debe abrir y cerrar con la misma ACTION_WORD)
    boundary = msg["boundary"]
    if not boundary.startswith("|=•'") or "•=|»" not in boundary:
        return False, "BOUNDARY malformado (apertura)"
    
    action_word = msg["action_word"]
    expected_open = f"|=•'{action_word}'•=|»"
    if boundary != expected_open:
        return False, f"BOUNDARY no coincide con ACTION_WORD ({action_word})"
    
    # Validar ACTION_WORD (debe estar en el vocabulario canónico)
    action_words_validos = [
        "INIT", "TASK", "DISPATCH", "CONSULTA", "INFORME", 
        "POESIA", "LINGUISTICA", "RESPUESTA", "COMUNICADO"
    ]
    if action_word not in action_words_validos:
        return False, f"ACTION_WORD no reconocido: {action_word}"
    
    # Validar destinatario
    destinatarios_validos = ["7SO", "9SE", "LLE", "TODOS", "DIRECTOR"]
    if msg["destinatario"] not in destinatarios_validos:
        return False, f"Destinatario no válido: {msg['destinatario']}"
    
    return True, "OK"


def calcular_hash(mensaje: dict) -> str:
    """Calcula hash SHA-256 del mensaje para integridad"""
    contenido = json.dumps(mensaje, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(contenido.encode('utf-8')).hexdigest()[:16]


# ---------- Handler de eventos de filesystem ----------
class SalonHandler(FileSystemEventHandler):
    """Escucha inbox/ y procesa cada mensaje entrante"""
    
    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith(".json"):
            return
        
        ruta_archivo = Path(event.src_path)
        print(f"\n[· SALON] Nuevo mensaje detectado: {ruta_archivo.name}")
        
        # 1. Leer y parsear
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as f:
                msg = json.load(f)
        except Exception as e:
            print(f"[X SALON] Error al leer {ruta_archivo.name}: {e}")
            return
        
        # 2. Validar contenedor
        valido, motivo = validar_contenedor(msg)
        if not valido:
            print(f"[X SALON] Contenedor inválido: {motivo}")
            # Mover a cuarentena
            cuarentena = INBOX / "cuarentena"
            cuarentena.mkdir(exist_ok=True)
            ruta_archivo.rename(cuarentena / ruta_archivo.name)
            return
        
        # 3. Clasificar por ACTION_WORD
        action = msg["action_word"]
        emisor = msg["emisor"]
        destinatario = msg["destinatario"]
        
        print(f"[✓ SALON] {emisor} → {destinatario} [{action}]")
        
        # 4. Ruteo
        destino_dir = OUTBOX / f"para_{destinatario.lower()}"
        if destinatario == "TODOS":
            # Broadcast: copiar a todos los outboxes
            for sub in OUTBOX.iterdir():
                if sub.is_dir():
                    destino_archivo = sub / ruta_archivo.name
                    import shutil
                    shutil.copy2(ruta_archivo, destino_archivo)
            print(f"[✓ SALON] Broadcast a todos los agentes")
        else:
            # Unicast: mover al outbox específico
            destino_archivo = destino_dir / ruta_archivo.name
            ruta_archivo.rename(destino_archivo)
        
        # 5. Sellar en historial (append-only)
        msg["_hash"] = calcular_hash(msg)
        msg["_procesado_en"] = datetime.now().isoformat()
        
        with open(HISTORIAL, "a", encoding="utf-8") as f:
            f.write(json.dumps(msg, ensure_ascii=False) + "\n")
        
        print(f"[✓ SALON] Sellado en historial_salon.jsonl")


# ---------- Main ----------
def main():
    print("=" * 60)
    print("ECN · SALÓN SOBERANO v3.0 · COORDINADOR LOCAL")
    print("=" * 60)
    print(f"INBOX:      {INBOX}")
    print(f"OUTBOX:     {OUTBOX}")
    print(f"HISTORIAL:  {HISTORIAL}")
    print(f"AGENTES:    {AGENTES_DIR}")
    print("=" * 60)
    print("[✓ SALON] Coordinador vivo. Escuchando inbox/...")
    print("[· SALON] Ctrl+C para detener\n")
    
    observer = Observer()
    observer.schedule(SalonHandler(), str(INBOX), recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[· SALON] Deteniendo coordinador...")
        observer.stop()
    observer.join()
    print("[✓ SALON] Coordinador detenido.")


if __name__ == "__main__":
    main()
