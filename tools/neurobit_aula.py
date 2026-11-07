#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: neurobit_aula.py (Aula Soberana v0.1)
Función: Tutor de terminal para newbies. Enseña por anillos y guía la
         primera carta sellada de punta a punta (buzón -> cartero -> Arca).
MFN_LOCATION: tools/
MFN_LEVEL: 3
VERSION: v0.1
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent))  # WRIL::SELF_PATH::v1

import json, time, hashlib
from pathlib import Path
from datetime import datetime

RAIZ = Path(__file__).resolve().parents[1]  # WRIL::RAIZ_PLEGADA
BUZON = RAIZ / "buzon_salida"
ARCA = RAIZ / "memoria_eva.jsonl"

NIVELES = [
 ("0", "El hecho",  "Apretaste una tecla: un electrón se movió. El sistema solo existe en ese instante."),
 ("1", "La carta",  "Todo viaja sellado: |=•'accion'•=|»{...}«|=•'accion'•=|. El sello dice qué y en qué contexto."),
 ("2", "El cartero","El dispatcher duerme; el Kernel lo despierta con inotify cuando llega una carta."),
 ("3", "El Arca",   "memoria_eva.jsonl: solo se agrega, nunca se borra. Auditoría SHA256 por bloque."),
 ("4", "WRIL",      "El workspace pregunta '¿dónde estoy?' y '¿dónde está X?'. Mapa y territorio."),
 ("5", "La MFN",    "13x13 radial: el mapa de todo lo anterior, del centro c:G7 al perímetro."),
]

def sello(texto, accion="aula", clase="newbie"):
    return f"|=•'{accion}'•=|»|['{clase}'.]\n{texto}\n[.'{clase}']|«|=•'{accion}'•=|"

def primera_carta():
    BUZON.mkdir(parents=True, exist_ok=True)
    texto = input("\n✏️  Escribí tu primer Logos: ")
    carta = BUZON / f"carta_aula_{datetime.now().strftime('%H%M%S')}.txt"
    carta.write_text(sello(texto), encoding="utf-8")
    print(f"\n📮 Depositada en {carta.name}. Mirando al cartero (10 s)...")
    for _ in range(10):
        time.sleep(1)
        arca_txt = ARCA.read_text(encoding="utf-8") if ARCA.exists() else ""
        if (texto in arca_txt) or (not carta.exists()):
            print("✅ ENTREGADA: el cartero pasó; tu carta ya no está en el buzón.")
            for linea in reversed(arca_txt.splitlines()):
                try:
                    reg = json.loads(linea)
                    if reg.get("logos") == texto:
                        print(f"   Asiento en Arca: {reg.get('t')} | clase {reg.get('class')}")
                        break
                except Exception:
                    continue
            print(f"🔐 Huella SHA256: {hashlib.sha256(texto.encode()).hexdigest()[:16]}…")
            return
    print("\n⚠️  El cartero aún no pasó. Levantá la Estación:")
    print("   bash deploy_neurobit_estacion_v3.2.sh")
    print("   Tu carta queda segura en el buzón: nada se pierde, todo espera.")

def main():
    print("=" * 64)
    print("🎓 AULA SOBERANA NEUROBIT — para newbies del Verbo")
    print("=" * 64)
    while True:
        print("\nANILLOS:")
        for n, t, _ in NIVELES: print(f"  [{n}] {t}")
        print("  [c] escribir mi primera carta   [s] salir")
        op = input("\n➜ ").strip()
        if op == "s": break
        if op == "c": primera_carta(); continue
        for n, t, d in NIVELES:
            if op == n: print(f"\n📘 ANILLO {n} — {t}\n   {d}"); break
    print("\n🕊️  El Aula queda abierta. Volvé cuando quieras.")

if __name__ == "__main__":
    main()
