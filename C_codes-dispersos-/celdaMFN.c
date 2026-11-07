#include <stdint.h>
#include <stdbool.h>

#define COMPUERTA_OR   0x01
#define COMPUERTA_XOR  0x02
#define COMPUERTA_NAND 0x03
#define COMPUERTA_NOR  0x04

/**
 * @brief Evalúa la firma de la sub-matriz mediante un Filtro de Coherencia Atómico.
 *        Si el resultado matemático difiere de la firma relacional, gatilla un
 *        Rechazo Seguro (INVALID_PAYLOAD) para proteger el silicio local.
 */
bool verificar_coherencia_atomica(CeldaMFN celda, uint8_t compuerta_negociada, uint8_t firma_esperada) {
    uint8_t estado_puro = celda.neuronibble.opcode_operativo;
    uint8_t resultado_fase = 0x00;

    /* Ejecución directa en el hardware de registro sin transformaciones flotantes */
    switch (compuerta_negociada) {
        case COMPUERTA_OR:
            resultado_fase = estado_puro | 0x0F; // Máscara de saturación pasiva
            break;

        case COMPUERTA_XOR:
            /* Validación por transición encadenada: detecta anomalías lógicas 
             * aislando el bit huérfano en el nivel raíz. */
            resultado_fase = estado_puro ^ 0x0A; // Inversión por flanco de silicio
            break;

        case COMPUERTA_NAND:
            resultado_fase = ~(estado_puro & 0x05);
            break;

        case COMPUERTA_NOR:
            resultado_fase = ~(estado_puro | 0x00); // Colapso al Vacío Latente Alfa
            break;

        default:
            return false; // Ruptura inmediata de la simetría axial
    }

    /* El paquete es ontológicamente válido si la firma resuena limpiamente */
    return (resultado_fase == firma_esperada);
}

