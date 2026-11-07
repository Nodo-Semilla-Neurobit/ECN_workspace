/*
 * Ecosistema Neurobit - Estación Central Neurobitrónica
 * Módulo: neurobit_uinput_injector.c
 * Función: Inyección de eventos EV_KEY a nivel de Kernel para forzar 
 * un pegado nativo (Ctrl+V) en la ventana con foco activo (GUI/Browser).
 * VERSION: v1.0
 */

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <linux/uinput.h>
#include <string.h>
#include <errno.h>

#define UINPUT_PATH "/dev/uinput"

// Emite un evento de entrada y sincroniza el bus
void emit_event(int fd, int type, int code, int val) {
    struct input_event ie;
    memset(&ie, 0, sizeof(ie));
    ie.type = type;
    ie.code = code;
    ie.value = val;
    write(fd, &ie, sizeof(ie));
    
    // Sincronización (SYN_REPORT) para que el Kernel procese el evento
    memset(&ie, 0, sizeof(ie));
    ie.type = EV_SYN;
    ie.code = SYN_REPORT;
    ie.value = 0;
    write(fd, &ie, sizeof(ie));
}

int main() {
    int fd = open(UINPUT_PATH, O_WRONLY | O_NONBLOCK);
    if (fd < 0) {
        fprintf(stderr, "[X ERROR] No se pudo abrir %s. Requiere permisos de root o grupo 'input'.\n", UINPUT_PATH);
        return 1;
    }

    // 1. Configurar el dispositivo virtual para aceptar eventos de teclas
    ioctl(fd, UI_SET_EVBIT, EV_KEY);
    ioctl(fd, UI_SET_KEYBIT, KEY_LEFTCTRL);
    ioctl(fd, UI_SET_KEYBIT, KEY_V);

    struct uinput_user_dev uidev;
    memset(&uidev, 0, sizeof(uidev));
    snprintf(uidev.name, UINPUT_MAX_NAME_SIZE, "Neurobit-HID-Injector");
    uidev.id.bustype = BUS_USB;
    uidev.id.vendor  = 0x1337;
    uidev.id.product = 0x0001;
    uidev.id.version = 1;

    write(fd, &uidev, sizeof(uidev));
    ioctl(fd, UI_DEV_CREATE);

    // Breve pausa para que el Compositor Gráfico registre el nuevo hardware
    usleep(200000); 

    // 2. Secuencia de Inyección: Presionar CTRL, Presionar V
    emit_event(fd, EV_KEY, KEY_LEFTCTRL, 1);
    emit_event(fd, EV_KEY, KEY_V, 1);
    
    // 3. Secuencia de Liberación: Soltar V, Soltar CTRL
    emit_event(fd, EV_KEY, KEY_V, 0);
    emit_event(fd, EV_KEY, KEY_LEFTCTRL, 0);

    // 4. Destrucción atómica del dispositivo virtual (Higiene del Kernel)
    ioctl(fd, UI_DEV_DESTROY);
    close(fd);
    
    return 0;
}
