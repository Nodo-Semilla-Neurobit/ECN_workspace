#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MFN_LOCATION: core/
# MFN_LEVEL: 1
# MFN_COORD: (7,7)
# VERSION: v1.1
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: core/port_lighthouse.py
Función: Faro de Puertos (PortLighthouse) - Gestor Dinámico de Puertos por Procedencia.
Evita colisiones de sockets (Address already in use), gestiona rangos según
la procedencia de los módulos (CORE, EXT, TOOLS) y asienta la realidad en
el territorio físico (path_map.json) para anular las restricciones CORS de raíz.

SOLITARIO NO, SOLIDARIO SÍ.
"""

import socket
import json
import os
import atexit
from datetime import datetime
import sys
from pathlib import Path

class SOSPortLighthouse:
    """
    Faro de Puertos Soberano de la Estación Central Neurobitrónica.
    Asigna, prueba y valida puertos dinámicos para evitar colisiones y
    facilitar el acoplamiento cero.
    """
    
    # Membranas de direccionamiento por procedencia de módulo
    MEMBRANAS = {
        "CORE": range(5000, 5010),   # 5000-5009: API Core, Dispatcher, api_endpoint_manager
        "EXT": range(5010, 5020),    # 5010-5019: Servidores de Fragmentos (Supersend), Extensions
        "TOOLS": range(5020, 5030)   # 5020-5029: GUIs, Status Monitors, Visualizadores
    }

    # Anclas reservadas: dueño declarado; el Faro no entrega un ancla a otro módulo
    ANCLAS = {5001: "salon_ws", 5002: "mfn_cartografo", 5003: "centinela_legacy", 5005: "backend_instalador_ludico", 8090: "mcp_server"}

    def __init__(self, root_path=None):
        # Auto-detectar la raíz de la ECN si no se especifica
        self.root_path = Path(root_path).resolve() if root_path else Path(__file__).resolve().parent.parent
        # STATE != PATH MAP: el Faro asienta estado en su propio archivo, no en el índice
        self.path_map_file = self.root_path / "data" / "runtime" / "port_map.json"
            
        self.allocated_ports = {}  # Mapeo de module_id -> port
        atexit.register(self._cleanup_sockets)
        self._purge_stale()

    def _purge_stale(self):
        """Descarta identidades cuyo PID ya no vive (kill -9 no corre atexit)."""
        idf = self.root_path / "data" / "runtime" / "api_port.identity"
        if not idf.exists():
            return
        try:
            data = json.load(idf.open(encoding="utf-8"))
            vivos = {k: v for k, v in data.items() if Path(f"/proc/{v.get('pid')}").exists()}
            if len(vivos) != len(data):
                idf.write_text(json.dumps(vivos, indent=4), encoding="utf-8")
                print(f"[✓ FARO] Purgadas {len(data) - len(vivos)} identidades huérfanas.")
        except Exception:
            pass

    def is_port_available(self, port, host="127.0.0.1"):
        """
        Prueba física no invasiva sobre el socket en localhost.
        Verifica la disponibilidad instantánea sin bloquear.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            try:
                # Intentamos enlazar (bind) para comprobar si está ocupado
                s.bind((host, port))
                return True
            except OSError:
                return False

    def request_port(self, module_id, provenance="EXT", default_port=None):
        """
        Asigna dinámicamente un puerto libre basado en la procedencia.
        Aplica el 'Efecto Muelle': si el puerto por defecto o inicial está ocupado,
        desciende o recorre el rango correspondiente hasta encontrar un muelle libre.
        """
        provenance = provenance.upper()
        if provenance not in self.MEMBRANAS:
            raise ValueError(f"Procedencia de módulo inválida: '{provenance}'. Debe ser CORE, EXT o TOOLS.")
        
        rango = self.MEMBRANAS[provenance]
        
        # 1. Si se solicita un puerto por defecto específico y está disponible
        if default_port and default_port in rango:
            if self.is_port_available(default_port):
                self._record_allocation(module_id, default_port, provenance)
                return default_port

        # 2. Escanear el rango asignado a la procedencia
        for port in rango:
            if port in self.ANCLAS and self.ANCLAS[port] != module_id:
                continue
            if self.is_port_available(port):
                self._record_allocation(module_id, port, provenance)
                return port
                
        # 3. Fallback desesperado: si todo el rango está saturado, probar con puerto aleatorio del kernel (puerto 0)
        # pero bajo un principio de alerta de tensión
        print(f"[⚠ FARO] Rango '{provenance}' saturado para '{module_id}'. Buscando muelle de emergencia...", file=sys.stderr)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            emerg_port = s.getsockname()[1]
            self._record_allocation(module_id, emerg_port, "EMERGENCY")
            return emerg_port

    def _record_allocation(self, module_id, port, provenance):
        """
        Registra físicamente la asignación en la RAM de la clase
        y escribe de manera inmutable el estado en el mapa territorial.
        """
        self.allocated_ports[module_id] = {
            "port": port,
            "provenance": provenance,
            "pid": os.getpid(),
            "timestamp": datetime.now().isoformat(),
        }
        print(f"[✓ FARO] Asignado puerto {port} ({provenance}) para módulo '{module_id}' [PID {os.getpid()}]")
        self._update_territorial_map()

    def _update_territorial_map(self):
        """
        Inyecta la realidad del silicio directo en el mapa territorial (path_map.json / port_map.json).
        Las extensiones web leen este JSON en caliente (Option A) superando las barreras de CORS
        sin peticiones cruzadas HTTP.
        """
        try:
            # Crear directorio de datos/runtime si es necesario
            runtime_dir = self.root_path / "data" / "runtime"
            runtime_dir.mkdir(parents=True, exist_ok=True)
            port_identity_file = runtime_dir / "api_port.identity"
            
            # Escribir identidad rápida del puerto actual de este proceso
            with open(port_identity_file, "w", encoding="utf-8") as f:
                json.dump(self.allocated_ports, f, indent=4)
                
            # Intentar actualizar el path_map.json principal si existe
            if self.path_map_file.exists():
                try:
                    with open(self.path_map_file, "r", encoding="utf-8") as f:
                        map_data = json.load(f)
                except Exception:
                    map_data = {}
                
                # Actualizar el bloque de puertos activos
                map_data["PORT_LIGHTHOUSE_ALLOCATIONS"] = self.allocated_ports
                
                with open(self.path_map_file, "w", encoding="utf-8") as f:
                    json.dump(map_data, f, indent=4)
                    
        except Exception as e:
            print(f"[⚠ FARO] Error escribiendo mapa territorial: {e}", file=sys.stderr)

    def _cleanup_sockets(self):
        """
        Liberación Quirúrgica en el atexit.
        Garantiza que al morir el proceso, el muelle del puerto quede inmediatamente
        limpio de sockets huérfanos o zombies.
        """
        # En Python, el bind no mantiene bloqueado el puerto de forma permanente 
        # una vez que el proceso que levantó el socket finaliza (a menos que se creen procesos hijos persistentes).
        # Este cleanup garantiza que avisemos al territorio físico de la desconexión del muelle.
        try:
            runtime_file = self.root_path / "data" / "runtime" / "api_port.identity"
            if runtime_file.exists():
                # En lugar de borrarlo, marcamos los puertos como liberados (o en reposo)
                # para mantener la trazabilidad histórica de la sesión
                with open(runtime_file, "r", encoding="utf-8") as f:
                    current_data = json.load(f)
                
                # Filtrar asignaciones de nuestro PID
                my_pid = os.getpid()
                cleaned_data = {k: v for k, v in current_data.items() if v.get("pid") != my_pid}
                
                with open(runtime_file, "w", encoding="utf-8") as f:
                    json.dump(cleaned_data, f, indent=4)
                    
            print(f"[✓ FARO] Puerto liberado quirúrgicamente para PID {os.getpid()}")
        except Exception:
            pass

if __name__ == "__main__":
    print("=== FARO DE PUERTOS SOBERANO - PRUEBA DE CAMPO ===")
    lighthouse = SOSPortLighthouse()
    # Solicitar puerto para la API Core
    api_port = lighthouse.request_port("neurobit_api", "CORE", default_port=5000)
    # Solicitar puerto para el servidor de fragmentos
    ext_port = lighthouse.request_port("supersend_server", "EXT", default_port=5010)
    # Solicitar puerto para el monitor de visualización
    tool_port = lighthouse.request_port("gtk_monitor", "TOOLS", default_port=5020)
    
    print("\n--- Estado del Territorio Asentado ---")
    print(json.dumps(lighthouse.allocated_ports, indent=4))


# ============================================================================
# EXTENSIÓN DEL LOGOS: PUENTE PASIVO SÍNCRONO POR FIFOS
# ============================================================================
class BridgePortLighthouse(SOSPortLighthouse):
    def iniciar_puente_pasivo(self):
        fifo_pretension = "/tmp/faro_pretension.fifo"
        fifo_respuesta = "/tmp/faro_respuesta.fifo"
        for fifo in (fifo_pretension, fifo_respuesta):
            if not os.path.exists(fifo):
                os.mkfifo(fifo)
        print("[ FARO_PUENTE ] Canales listos. Esperando pretensiones en Silencio Sagrado...")
        while True:
            with open(fifo_pretension, "r") as f_in:
                peticion_cruda = f_in.read().strip()
            if not peticion_cruda:
                continue
            try:
                datos = json.loads(peticion_cruda)
                module_id = datos.get("module_id", "modulo_anonimo")
                provenance = datos.get("provenance", "EXT")
                port_pretendido = datos.get("port", 0)
                puerto_real = self.request_port(module_id=module_id, provenance=provenance, default_port=port_pretendido)
                with open(fifo_respuesta, "w") as f_out:
                    f_out.write(f"{puerto_real}\n")
            except Exception as e:
                import sys
                print(f"[ FARO_PUENTE ] ! Error en mediación semántica: {e}", file=sys.stderr)
                with open(fifo_respuesta, "w") as f_out:
                    f_out.write("0\n")

if __name__ == "__main__":
    faro = BridgePortLighthouse()
    faro._purge_stale()
    faro.iniciar_puente_pasivo()
