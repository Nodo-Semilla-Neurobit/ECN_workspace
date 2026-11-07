#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MFN_LOCATION: tools/
# MFN_LEVEL: 2
# MFN_COORD: (5,3)
"""ECN · Detector MFN anclado · lector único de cabeceras (canon M2/M3/M4)."""
import re
from pathlib import Path

VENTANA = 15

def _com(ext):
    if ext in (".py", ".sh", ".bash", ".yaml", ".yml", ".log"): return r"^#\s*"
    if ext in (".js", ".ts", ".c", ".h", ".cc"):                return r"^//\s*"
    if ext in (".md", ".markdown"):                             return r"^"
    return None

def _pats(ext):
    c = _com(ext)
    if c is None: return None
    return {"loc": re.compile(r"(?m)" + c + r"MFN_LOCATION:\s*(\S+)"),
            "lvl": re.compile(r"(?m)" + c + r"MFN_LEVEL:\s*(\d+)"),
            "crd": re.compile(r"(?m)" + c + r"MFN_COORD:\s*\((\d+),\s*(\d+)\)")}

def leer_header(ruta):
    ruta = Path(ruta); p = _pats(ruta.suffix.lower())
    out = {"loc": None, "lvl": None, "crd": None, "tiene": False}
    if p is None: return out
    try:
        with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
            head = "".join([next(f, "") for _ in range(VENTANA)])
    except Exception:
        return out
    m = p["loc"].search(head)
    if m: out["tiene"], out["loc"] = True, m.group(1).strip()
    m = p["lvl"].search(head)
    if m: out["lvl"] = m.group(1)
    m = p["crd"].search(head)
    if m: out["crd"] = f"({m.group(1)},{m.group(2)})"
    return out

def norm_dir(d):
    d = (d or "").strip().replace("\\", "/")
    return "" if d in (".", "./", "") else d.rstrip("/")

def es_tension(hdr, carpeta_real):
    return bool(hdr["tiene"]) and norm_dir(hdr["loc"]) != norm_dir(str(carpeta_real))
