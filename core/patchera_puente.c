#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <string.h>

typedef int (*real_bind_t)(int, const struct sockaddr *, socklen_t);

int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen) {
    real_bind_t original_bind = (real_bind_t)dlsym(RTLD_NEXT, "bind");

    if (addr->sa_family == AF_INET) {
        struct sockaddr_in *addr_in = (struct sockaddr_in *)addr;
        int puerto_pretendido = ntohs(addr_in->sin_port);

        // Omitimos la redirección si el proceso ya pide el puerto 0 (dinámico nativo)
        if (puerto_pretendido != 0) {
            char peticion[256];
            char respuesta[32];
            
            // Construir el glifo semántico que el Módulo Parser de Python comprende
            // En producción, puedes extraer el nombre del proceso real leyendo /proc/self/cmdline
            snprintf(peticion, sizeof(peticion), 
                     "{\"module_id\": \"modulo_inyectado\", \"provenance\": \"EXT\", \"port\": %d}", 
                     puerto_pretendido);

            // 1. Enviar pretensión al Faro de Puertos por la tubería de entrada
            FILE *f_out = fopen("/tmp/faro_pretension.fifo", "w");
            if (f_out) {
                fprintf(f_out, "%s\n", peticion);
                fclose(f_out);

                // 2. Leer la asignación real del Faro desde la tubería de respuesta
                // Esta llamada pausa el hilo del binario a nivel de Kernel (0% CPU) hasta que Python responde
                FILE *f_in = fopen("/tmp/faro_respuesta.fifo", "r");
                if (f_in) {
                    if (fgets(respuesta, sizeof(respuesta), f_in)) {
                        int puerto_asignado = atoi(respuesta);
                        if (puerto_asignado > 0) {
                            addr_in->sin_port = htons(puerto_asignado);
                            fprintf(stderr, "[ SHIM ] Redirección exitosa: %d -> %d\n", 
                                    puerto_pretendido, puerto_asignado);
                        }
                    }
                    fclose(f_in);
                }
            }
        }
    }

    // Entregar el control al Kernel con la estructura mutada sin modificar el código original
    return original_bind(sockfd, addr, addrlen);
}

