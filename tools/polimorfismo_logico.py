#!/usr/bin/env python3
# polimorfismo_logico.py - Selector de Compuertas para MFN
# MFN_LOCATION: tools/ | MFN_LEVEL: 2 | VERSION: v0.1

class PolimorfismoLogico:
    """
    Aplica polimorfismo contextual a un Neuronibble (4 bits).
    El mismo dato produce diferentes estados según la compuerta seleccionada.
    """
    
    COMPUERTAS = {
        0b000: ("NOT",  lambda x: (~x) & 0b1111),
        0b001: ("OR",   lambda x, y: x | y),
        0b010: ("NOR",  lambda x, y: ~(x | y) & 0b1111),
        0b011: ("AND",  lambda x, y: x & y),
        0b100: ("NAND", lambda x, y: ~(x & y) & 0b1111),
        0b101: ("XOR",  lambda x, y: x ^ y),
        0b110: ("XNOR", lambda x, y: ~(x ^ y) & 0b1111),
        0b111: ("RAW",  lambda x: x),  # Estado 8: dato sin compuerta
    }
    
    def aplicar_compuerta(self, dato: int, modo: int, mascara: int = 0b1111) -> int:
        """
        Aplica la compuerta seleccionada al dato.
        
        Args:
            dato: Neuronibble (4 bits, 0-15)
            modo: Selector de compuerta (3 bits, 0-7)
            mascara: Valor de referencia para compuertas binarias (default: 0b1111)
        
        Returns:
            Estado resultante (4 bits)
        """
        if modo not in self.COMPUERTAS:
            raise ValueError(f"Modo inválido: {modo}. Debe ser 0-7.")
        
        nombre, funcion = self.COMPUERTAS[modo]
        
        # Compuertas unarias (NOT, RAW) vs binarias (OR, AND, XOR, etc.)
        if nombre in ("NOT", "RAW"):
            return funcion(dato)
        else:
            return funcion(dato, mascara)
    
    def validar_coherencia(self, dato: int, modo: int, estado_esperado: int, mascara: int = 0b1111) -> bool:
        """
        Valida si el estado resultante coincide con el esperado.
        Retorna True si hay coherencia ontológica (Filtro de Coherencia atómico).
        """
        estado_calculado = self.aplicar_compuerta(dato, modo, mascara)
        return estado_calculado == estado_esperado
    
    def generar_tabla_verdad(self, dato: int, mascara: int = 0b1111) -> dict:
        """
        Genera los 8 estados posibles para un dato dado (una fila de la tabla de verdad).
        """
        tabla = {}
        for modo in range(8):
            nombre, _ = self.COMPUERTAS[modo]
            estado = self.aplicar_compuerta(dato, modo, mascara)
            tabla[nombre] = {
                "modo_bin": format(modo, '03b'),
                "estado_bin": format(estado, '04b'),
                "estado_dec": estado
            }
        return tabla


# Ejemplo de uso
if __name__ == "__main__":
    pl = PolimorfismoLogico()
    
    print("=== POLIMORFISMO LÓGICO - MFN ===\n")
    
    # Dato de entrada: 0011 (3 en decimal)
    dato = 0b0011
    print(f"Dato de entrada: {format(dato, '04b')} ({dato})\n")
    
    # Generar tabla de verdad completa
    tabla = pl.generar_tabla_verdad(dato)
    
    print("Tabla de Verdad (8 modos):")
    print("-" * 50)
    for nombre, info in tabla.items():
        print(f"Modo {info['modo_bin']} ({nombre:>4}): {info['estado_bin']} ({info['estado_dec']})")
    
    print("\n" + "=" * 50)
    print("Validación de Coherencia:")
    print("-" * 50)
    
    # Caso 1: Dato 0011 bajo XOR con máscara 1111 → esperado 1100
    modo_xor = 0b101
    estado_esperado = 0b1100
    coherente = pl.validar_coherencia(dato, modo_xor, estado_esperado)
    print(f"Dato: {format(dato, '04b')} | Modo: XOR | Esperado: {format(estado_esperado, '04b')}")
    print(f"Resultado: {'✓ COHERENTE' if coherente else '✗ DISTORSIÓN'}\n")
    
    # Caso 2: Dato 0011 bajo AND con máscara 1010 → esperado 0010
    modo_and = 0b011
    mascara = 0b1010
    estado_esperado = 0b0010
    coherente = pl.validar_coherencia(dato, modo_and, estado_esperado, mascara)
    print(f"Dato: {format(dato, '04b')} | Modo: AND | Máscara: {format(mascara, '04b')} | Esperado: {format(estado_esperado, '04b')}")
    print(f"Resultado: {'✓ COHERENTE' if coherente else '✗ DISTORSIÓN'}")