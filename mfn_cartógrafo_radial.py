#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ecosistema Neurobit - Capa de Utilidades de Compilación Soberana
Módulo: mfn_cartógrafo_radial.py
Función: Traduce el espacio cartesiano plano al tejido métrico de 7 anillos
         concéntricos (169 compartimentos discretos) sin usar FPU.
"""

import sys

class MFN_Cartografo:
    def __init__(self):
        # Declaración Epistémica de la Matriz Radial
        # Estructura: 4 sectores x 2 porciones = 8 porciones totales concéntricas
        self.config_anillos = {
            'c':  {'bits_por_porcion': 1, 'total_bits': 1},   # Pivote / Observador Central
            'am': {'bits_por_porcion': 1, 'total_bits': 8},   # Anillo 1: Amarillo (Origen de pulsación)
            'na': {'bits_por_porcion': 2, 'total_bits': 16},  # Anillo 2: Naranja (Soporte estructural)
            'vi': {'bits_por_porcion': 3, 'total_bits': 24},  # Anillo 3: Violeta (Transición sináptica)
            'añ': {'bits_por_porcion': 4, 'total_bits': 32},  # Anillo 4: Añil (Procesamiento intermedio)
            'az': {'bits_por_porcion': 5, 'total_bits': 40},  # Anillo 5: Azul (Estabilización de datos)
            'ma':  {'bits_por_porcion': 6, 'total_bits': 48}   # Anillo 6: Marrón (Perímetro BIOS / Frontera Física)
        }
        
        # El Anillo Marrón (m) mapea con los 48 bits de direccionamiento virtual nativo.
        self.orden_ascendente = ['c', 'am', 'na', 'vi', 'añ', 'az', 'ma']

    def calcular_offset_anillo(self, anillo_objetivo):
        """
        Calcula de forma determinista el desplazamiento lineal acumulado (offset) 
        de los anillos internos en la memoria RAM.
        """
        offset = 0
        for anillo in self.orden_ascendente:
            if anillo == anillo_objetivo:
                break
            offset += self.config_anillos[anillo]['total_bits']
        return offset

    def resolver_direccion_absoluta(self, anillo, sector, porcion, bit):
        """
        Resuelve la ecuación canónica de direccionamiento híbrido.
        Convierte coordenadas de localización de cuadrantes en un índice lineal (0-168).
        """
        # Validaciones de integridad estructural (Regla 3)
        if sector not in:
            raise ValueError("[ERROR_ECN] El sector debe estar en el cuadrante angular [1,2,3,4]")
        if porcion not in:
            raise ValueError("[ERROR_ECN] La porción espacial debe ser 1 (Izquierda) o 2 (Derecha)")
        
        if anillo == 'c':
            return 0 # El Observador Central ocupa el índice de casillero cero

        bits_max = self.config_anillos[anillo]['bits_por_porcion']
        if bit < 1 or bit > bits_max:
            raise ValueError(f"[ERROR_ECN] Bit fuera de rango para anillo '{anillo}'. Máximo: {bits_max}")

        # Fase 1: Resolver la porción global concéntrica (Sentido de giro de agujas de reloj)
        porcion_global = (sector - 1) * 2 + (porcion - 1)

        # Fase 2: Resolver posición absoluta dentro del bus lineal de memoria cruda
        offset_anillo = self.calcular_offset_anillo(anillo)
        indice_absoluto = offset_anillo + (porcion_global * bits_max) + (bit - 1)
        
        return indice_absoluto

    def inyectar_estado_mfn(self, coordenadas_marcadas):
        """
        Sintetiza el Logos directamente en un array lineal de estados puros (169 bits).
        Cada tupla representa una tensión geométrica (Yang) sobre el espacio latente (Yin).
        """
        # Inicialización en "Estado Cero" / Vacío Latente Alfa (169 bits apagados)
        grilla_radial = [0] * 169
        
        for (anillo, sector, porcion, bit, valor) in coordenadas_marcadas:
            try:
                idx = self.resolver_direccion_absoluta(anillo, sector, porcion, bit)
                grilla_radial[idx] = 1 if valor else 0
            except ValueError as e:
                print(f"[ALERTA_PARSER] Ruptura de integridad en nodo secundario: {e}")
                # Fallback de Alerta: Rechazo Seguro de la porción inválida
                continue
                
        return grilla_radial

