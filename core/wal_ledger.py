# MFN_LOCATION: core/
# MFN_LEVEL: 1
# MFN_COORD: (4,4) - El Altar de los Contratos
# VERSION: v1.3 (Ledger Dinámico Unificado)

import json
from pathlib import Path
from datetime import datetime
from wril_self_root import detectar_raiz  # ancla inmutable del filesystem

class WALLedger:
    def __init__(self):
        self.raiz = detectar_raiz()
        self.wal_path = self.raiz / "data" / "runtime" / "wril_historial.jsonl"
        self.wal_path.parent.mkdir(parents=True, exist_ok=True)

    def estampar_glifo(self, pid: int, modulo: str, fase: str, semantica: str, payload: dict):
        """
        Sello inmutable Write-Ahead Log (WAL) para trazabilidad absoluta.
        Operación atómica append-only en el silicio.
        """
        glifo = {
            "t": datetime.utcnow().isoformat() + "Z",
            "pid": pid,
            "modulo": modulo,
            "fase": fase,       # Ej: "ORQUESTACION_OK", "MEDIACION_PUERTO", "EXTRACCION_ESTATICA"
            "semantica": semantica, # Ej: "HERMITIANA" (Normal) o "ANTIHERMITIANA" (Alerta de tensión)
            "payload": payload
        }
        
        # Escritura atómica lineal (Append-only)
        with open(self.wal_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(glifo, ensure_ascii=False) + "\n")

    def analisis_resiliente_post_instalacion(self):
        """
        El Parser del orquestador realiza un barrido reverso del archivo WAL.
        Recompone el estado actual del mapa territorial de forma 100% determinista.
        """
        if not self.wal_path.exists():
            return {"estado": "SISTEMA_VIRGEN", "detalles": "No hay trazas en el Ledger."}

        mapa_puertos_activos = {}
        modulos_analizados = set()
        tension_detectada = 0

        # Barrido lineal para reconstruir la verdad histórica sin daemons parasitarios
        with open(self.wal_path, "r", encoding="utf-8") as f:
            for linea in f:
                if not linea.strip():
                    continue
                try:
                    registro = json.loads(linea)
                    payload = registro.get("payload", {})
                    fase = registro.get("fase")
                    
                    # 1. Rastrear mutaciones dinámicas de puertos
                    if fase == "MEDIACION_PUERTO":
                        p_real = payload.get("puerto_real")
                        if p_real:
                            mapa_puertos_activos[payload.get("module_id")] = p_real
                            
                    # 2. Registrar módulos validados por los extractores de firmas
                    elif fase == "EXTRACCION_ESTATICA":
                        modulos_analizados.add(registro.get("modulo"))
                        
                    # 3. Contabilizar anomalías (Tensión antihermitiana)
                    if registro.get("semantica") == "ANTIHERMITIANA":
                        tension_detectada += 1
                        
                except json.JSONDecodeError:
                    continue # Cuarentena silenciosa de líneas corruptas

        return {
            "estado": "ORQUESTADO_COHERENTE" if tension_detectada == 0 else "ORQUESTADO_CON_TENSION",
            "puertos_activos": mapa_puertos_activos,
            "modulos_en_trazabilidad": list(modulos_analizados),
            "alertas_de_colision": tension_detectada
        }

