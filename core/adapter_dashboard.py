import os
import subprocess
from pathlib import Path
from core.adapters.base import BaseAdapter
from wril_leyes import asegurar_syspath  # Asegura el sys.path local (Ley 4)

class DashboardAdapter(BaseAdapter):
    def get_module_id(self):
        return "nb.dashboard_control"

    def get_metadata(self):
        return {
            "version": "1.1",
            "endpoints": [
                {
                    "path": "/api/dashboard/status",
                    "methods": ["GET"],
                    "handler": self.get_system_status
                },
                {
                    "path": "/api/dashboard/control",
                    "methods": ["POST"],
                    "handler": self.execute_service_control,
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "service": {"type": "string"},
                            "action": {"type": "string", "enum": ["start", "stop"]}
                        },
                        "required": ["service", "action"]
                    }
                }
            ]
        }

    def _get_ecn_root(self):
        """Resuelve de forma forense la ubicación sin rutas fijas (Ley 1)"""
        try:
            # Lee el contrato canónico de anclaje territorial generado en L0
            with open(Path(__file__).resolve().parents[2] / "ecn_root.cfg", "r") as f:
                line = f.read().strip()
                return line.split("=")[1]
        except Exception:
            # Fallback dinámico utilizando inspección de herencia
            return str(Path(__file__).resolve().parents[2])

    def get_system_status(self, payload=None):
        ecn_root = self._get_ecn_root()
        pids_dir = Path(ecn_root) / "pids"
        
        # Mapeo de nombres del HTML hacia archivos de control de PIDs reales
        service_map = {
            "centinela": "dispatcher.pid",  # neurobit_dispatcher
            "keylogger": "dictado.pid",     # neurobit_dictado_evdev
            "flask": "hub_dinamico.pid"     # neurobit_api
        }
        
        states = {}
        for html_name, pid_file in service_map.items():
            pid_path = pids_dir / pid_file
            states[html_name] = "offline"
            
            if pid_path.exists():
                try:
                    pid = int(pid_path.read_text().strip())
                    # Comprobación de Membrana: verifica si el proceso está vivo en el kernel /proc
                    os.kill(pid, 0) 
                    states[html_name] = "online"
                except (ProcessLookupError, ValueError):
                    # El proceso está muerto o es un PID huérfano (zombie)
                    states[html_name] = "offline"
                    
        return {"status": "success", "components": states}

    def execute_service_control(self, payload, path=None):
        service = payload["service"]
        action = payload["action"]
        ecn_root = self._get_ecn_root()
        
        if service == "flask" and action == "start":
            # Ejecuta de forma transparente el spawner biónico de sintonía secuencial
            script_path = Path(ecn_root) / "despertador_hub.sh"
            subprocess.Popen(["bash", str(script_path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return {"status": "loading", "message": "Lanzando Cliente de Sintonía Efímera"}
            
        elif service == "centinela" and action == "start":
            script_path = Path(ecn_root) / "deploy_neurobit_estacion_v3.2.sh"
            # Se levanta en background sin estresar la CPU con bucles (0.0% CPU)
            subprocess.Popen(["bash", str(script_path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return {"status": "loading", "message": "Iniciando Ceremonia de bota de orquestadores"}

        return {"status": "error", "message": "Comando o servicio no mapeado en el territorio"}

