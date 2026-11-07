/*
 * Ecosistema Neurobit - Estación Central Neurobitrónica
 * Módulo: neurobit_x11_selector.c
 * Función: Lector de selecciones X11 de mínima fricción. Habla directo con
 *          el servidor X (XConvertSelection + UTF8_STRING), maneja INCR para
 *          payloads grandes y timeout silencioso. Jubila a xclip.
 * VERSION: v0.1
 * Compilar: gcc -O2 -o neurobit_x11_selector neurobit_x11_selector.c -lX11
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/select.h>
#include <sys/time.h>
#include <X11/Xlib.h>
#include <X11/Xatom.h>

static Atom A_CLIP, A_UTF8, A_INCR, A_PROP;

static int esperar_evento(Display *dpy, XEvent *ev, int seg) {
    int fd = ConnectionNumber(dpy);
    for (;;) {
        if (XPending(dpy)) { XNextEvent(dpy, ev); return 1; }
        fd_set rfds; FD_ZERO(&rfds); FD_SET(fd, &rfds);
        struct timeval tv; tv.tv_sec = seg; tv.tv_usec = 0;
        if (select(fd + 1, &rfds, NULL, NULL, &tv) <= 0) return 0;
    }
}

static unsigned char *leer_incr(Display *dpy, Window win, size_t *total) {
    unsigned char *buf = NULL; size_t cap = 0; *total = 0;
    XDeleteProperty(dpy, win, A_PROP);   /* habilita el primer chunk */
    XFlush(dpy);
    for (;;) {
        XEvent ev;
        if (!esperar_evento(dpy, &ev, 2)) break;
        if (ev.type != PropertyNotify || ev.xproperty.atom != A_PROP ||
            ev.xproperty.state != PropertyNewValue) continue;
        Atom type; int format; unsigned long nitems, after;
        unsigned char *data = NULL;
        XGetWindowProperty(dpy, win, A_PROP, 0, 0x1FFFFFFF, True,
                           AnyPropertyType, &type, &format, &nitems, &after, &data);
        if (nitems == 0) { if (data) XFree(data); break; }   /* fin de INCR */
        size_t need = *total + nitems + 1;
        if (need > cap) { cap = cap ? cap * 2 : 65536;
                          while (cap < need) cap *= 2;
                          buf = realloc(buf, cap); }
        memcpy(buf + *total, data, nitems);
        *total += nitems;
        XFree(data);
    }
    if (buf) buf[*total] = '\0';
    return buf;
}

int main(void) {
    Display *dpy = XOpenDisplay(NULL);
    if (!dpy) { fprintf(stderr, "[X ERROR] Sin DISPLAY X11 activo.\n"); return 1; }

    A_CLIP = XInternAtom(dpy, "CLIPBOARD", False);
    A_UTF8 = XInternAtom(dpy, "UTF8_STRING", False);
    A_INCR = XInternAtom(dpy, "INCR", False);
    A_PROP = XInternAtom(dpy, "NEUROBIT_SEL", False);

    Window win = XCreateSimpleWindow(dpy, DefaultRootWindow(dpy),
                                     0, 0, 1, 1, 0, 0, 0);
    XConvertSelection(dpy, A_CLIP, A_UTF8, A_PROP, win, CurrentTime);
    XFlush(dpy);

    XEvent ev; memset(&ev, 0, sizeof(ev));
    int ok = 0;
    while (esperar_evento(dpy, &ev, 2)) {
        if (ev.type == SelectionNotify && ev.xselection.requestor == win) { ok = 1; break; }
    }
    if (!ok || ev.xselection.property == None) { XCloseDisplay(dpy); return 0; }

    /* Peek del tipo sin consumir (long=0, delete=False) */
    Atom type; int format; unsigned long nitems, after;
    unsigned char *data = NULL;
    XGetWindowProperty(dpy, win, ev.xselection.property, 0, 0, False,
                       AnyPropertyType, &type, &format, &nitems, &after, &data);
    XFree(data);

    unsigned char *texto = NULL; size_t total = 0;
    if (type == A_INCR) {
        texto = leer_incr(dpy, win, &total);
    } else {
        XGetWindowProperty(dpy, win, ev.xselection.property, 0, 0x1FFFFFFF, True,
                           AnyPropertyType, &type, &format, &nitems, &after, &data);
        if (data && nitems) {
            texto = malloc(nitems + 1);
            memcpy(texto, data, nitems);
            texto[nitems] = '\0';
            total = nitems;
        }
        if (data) XFree(data);
    }

    if (texto) { fwrite(texto, 1, total, stdout); free(texto); }
    XCloseDisplay(dpy);
    return 0;
}
