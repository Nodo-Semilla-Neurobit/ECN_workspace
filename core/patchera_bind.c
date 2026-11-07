#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <string.h>

// Definición del puntero a la función bind real del sistema
typedef int (*real_bind_t)(int, const struct sockaddr *, socklen_t);

int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen) {
    // 1. Localizar dinámicamente el bind nativo de glibc
    real_bind_t original_bind = (real_bind_t)dlsym(RTLD_NEXT, "bind");
    
    // 2. Verificar si es una conexión IPv4 (AF_INET)
    if (addr->sa_family == AF_INET) {
        struct sockaddr_in *addr_in = (struct sockaddr_in *)addr;
        int puerto_pretendido = ntohs(addr_in->sin_port);
        pid_t mi_pid = getpid();

        // 3. Simulación de la consulta a port_lighthouse.py (Muelle Libre)
        // En producción, aquí se lee /data/runtime/api_port.identity o se invoca al Faro
        int puerto_asignado = puerto_pretendido;
        
        // Ejemplo de mediación: Si pretende el 5000 y está ocupado, muta al rango del Faro
        if (puerto_pretendido == 5000) {
            // El Faro determina que debe ir al muelle dinámico 5001 asignado a su procedencia
            puerto_asignado = 5001; 
            addr_in->sin_port = htons(puerto_asignado);
            
            // Imprimir la traza limpia para el Ledger/WAL sin interferir con stdout
            fprintf(stderr, "[ PATCHERA ] PID %d pretendía puerto %d -> Redirigido a puerto físico %d por el Faro.\n", 
                    mi_pid, puerto_pretendido, puerto_asignado);
        }
    }

    // 4. Entregar el control al Kernel con la estructura mutada en caliente
    return original_bind(sockfd, addr, addrlen);
}

