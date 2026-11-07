#!/usr/bin/env python3
# WRIL::SELF_PATH::v1
# -*- coding: utf-8 -*-
"""
Ecosistema Neurobit - SOS CORE
Módulo: tools/sos_module_linker_tester.py
Función: Auditoría estática de enlaces. Analiza imports vía AST, valida sintaxis
         y detecta módulos huérfanos sin dependencias externas.
MFN_LOCATION: tools/  |  MFN_LEVEL: 3
VERSION: v1.0
"""
import sys as _ws
from pathlib import Path as _wp
_ws.path.insert(0, str(_wp(__file__).resolve().parent.parent / "wril"))

import ast
import os
import sys
import json
import py_compile
from pathlib import Path
from wril_self_root import detectar_raiz

RAIZ = detectar_raiz()

class SOSModuleLinkerTester:
    def __init__(self, workspace_root: Path = RAIZ):
        self.root = workspace_root
        self.api_file = self.root / "neurobit_api.py"
        self.report = {
            "api_imports": [],
            "modules_status": [],
            "orphans": [],
            "syntax_errors": []
        }

    def extract_api_imports(self):
        """Extrae los módulos que neurobit_api.py realmente necesita via AST."""
        if not self.api_file.exists():
            return
        try:
            tree = ast.parse(self.api_file.read_text(encoding="utf-8"), filename=self.api_file.name)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.report["api_imports"].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self.report["api_imports"].append(node.module)
        except Exception as e:
            self.report["syntax_errors"].append({"file": "neurobit_api.py", "error": str(e)})

    def check_syntax(self, py_file: Path) -> bool:
        """Valida la sintaxis sin ejecutar el código."""
        try:
            py_compile.compile(str(py_file), doraise=True)
            return True
        except py_compile.PyCompileError as e:
            self.report["syntax_errors"].append({
                "file": str(py_file.relative_to(self.root)),
                "error": str(e).strip()
            })
            return False

    def scan_modules(self):
        """Recorre las carpetas core, wril y tools para cruzar datos en frío."""
        dirs_to_scan = ["core", "wril", "tools"]
        api_imports_set = set(self.report["api_imports"])

        for d in dirs_to_scan:
            dir_path = self.root / d
            if not dir_path.exists():
                continue
            for py_file in dir_path.rglob("*.py"):
                if any(p in py_file.parts for p in ('.venv', '__pycache__', 'backups_wril')):
                    continue

                rel_path = py_file.relative_to(self.root)
                module_name = str(rel_path.with_suffix('')).replace(os.sep, '.')

                is_linked = any(module_name in imp or imp in module_name for imp in api_imports_set)
                syntax_ok = self.check_syntax(py_file)

                self.report["modules_status"].append({
                    "module": module_name,
                    "linked_to_api": is_linked,
                    "syntax_ok": syntax_ok,
                    "path": str(rel_path)
                })

                if not is_linked and syntax_ok:
                    self.report["orphans"].append(module_name)

    def generate_report(self) -> Path:
        output_path = self.root / "data" / "runtime" / "sos_linker_report.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(self.report, indent=2, ensure_ascii=False), encoding="utf-8")
        return output_path

if __name__ == "__main__":
    tester = SOSModuleLinkerTester()
    tester.extract_api_imports()
    tester.scan_modules()
    out = tester.generate_report()
    print(f"[✓ LINKER] Escaneados: {len(tester.report['modules_status'])} | Huérfanos: {len(tester.report['orphans'])} | Errores: {len(tester.report['syntax_errors'])}")
