#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# MFN_LOCATION: ./
# MFN_LEVEL: 1
"""
Ecosistema Neurobit - Estación Central Neurobitrónica
Módulo: neurobit_api.py
Función: Punto de entrada del Hub Dinámico (puerto 5000, localhost-first).
VERSION: v2.0 (orquestación 100% dinámica)
"""
from core.module_connector import ModuleConnector
from core.api_endpoint_manager import APIEndpointManager

if __name__ == "__main__":
    connector = ModuleConnector()
    manager = APIEndpointManager(connector)
    manager.run(host="127.0.0.1", port=5000)
