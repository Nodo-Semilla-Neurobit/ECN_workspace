# Módulo 01: backend_instalador_ludico.py
## Ficha de Identidad
* **Nombre Físico del Archivo:** `backend_instalador_ludico.py`
* **Ubicación Física Observada:** `~/compendio/ECN.Instalador_Ludico/backend_instalador_ludico.py`
* **Ubicación MFN Declarada (Cabecera):** *Ninguna (Carece de cabecera MFN)*
* **Nivel de la Capa (MFN_LEVEL):** *Ninguno*
* **Coordenada de la Matriz (MFN_COORD):** *Ninguna*
* **Versión del Módulo:** `v0.1`

---

## 1. Funcionamiento Simplificado (Para el Aspirante)
El `backend_instalador_ludico.py` es el orquestador del **Dojo de Sintonía**. Su objetivo es servir una interfaz lúdica local para que puedas dar tus primeros pasos en la Estación sin sufrir frustración por la terminología técnica o las barreras de la shell. Este módulo "desbloquea" de forma secuencial las herramientas (misiones) a medida que demuestras que has asimilado una capacidad real en tu disco duro (ej: anclar tu territorio, crear el entorno virtual isolated `.venv`, etc.). Al superar cada hito, este backend te premia depositando en tu bandeja de entrada el módulo correspondiente para que continúes armando tu cibernave.

---

## 2. Lógica de Operación y Funciones
El módulo es un microservidor Flask de un solo archivo.
* **Control de Rutas Físicas:** Define la constante `RAIZ` de forma relativa a su propia ubicación de ejecución, autocreando los compartimentos del territorio:
  * `INBOX_DIR = RAIZ / "inbox"`
  * `MODULOS_DIR = RAIZ / "modulos"`
  * `SESIONES_DIR = RAIZ / "sesiones"`
* **CORS Manual:** Incorpora un middleware artesanal (`add_cors_headers`) para permitir peticiones HTTP provenientes de cualquier frontend local (`Experiencia.html` u `awaken_ceremony.html`), esquivando las trabas de CORS corporativas de los navegadores.
* **MISIONES_CONTENIDO (La Base de Datos de Sintonía):** Almacena en memoria el diccionario del Camino de Ascensión:
  * **Misión `m1` (Coordenada de Origen - pwd):** Comando canónico: `pwd`. Recompensa física: Inyección del archivo de la Capa 0 `wril_self_root.py` en tu espacio de trabajo.
* **Endpoints REST Soportados:**
  * `GET /health`: Comprobación rápida de latido de sintonía. Devuelve la membrana como `"aislada"`.
  * `GET /api/misiones`: Lista las misiones para consumo del frontend. Protege los contenidos de recompensa (código fuente) eliminándolos del JSON devuelto.
  * `POST /api/misiones/verificar`: Recibe la evidencia de la shell copiada por el usuario, valida contra el comando canónico del Atanor y desbloquea el siguiente nivel.

---

## 3. Variables y Constantes Hardcodeadas
* Puerto de escucha de Flask rígido: `port=5005` en la llamada `app.run(host='127.0.0.1', port=5005)`.
* Las rutas de carpetas de almacenamiento (`inbox`, `modulos`, `sesiones`) asumen que viven dentro de la subcarpeta del instalador lúdico, en lugar de referenciar el alias global `ECN_ROOT`.

---

## 4. Interacciones y Cooperación
* **Frontend Lúdico (Consola Verde / Experiencia.html):** Alimenta los indicadores de "Barras de Sintonía" y es el cliente que consume `/api/misiones`.
* **Capa WRIL (Capa 0 - wril_self_root.py):** Actúa como la primera recompensa inyectada físicamente en la bandeja de entrada del usuario para enseñarle a anclarse al disco real.

---

## 5. Dependencias
* **Ecosistema Python:** `flask`, `json`, `pathlib`, `os`.
* **Módulos / Scripts Complementarios:** Ninguno externo; opera de forma asilada y autocontenida.

---

## 6. Diagrama de Flujo Conceptual
```text
  [ Aspirante copia salida de "pwd" ]
                 │
                 ▼ (Petición POST)
     [ /api/misiones/verificar ]
                 │
      ┌──────────┴──────────┐
      ▼ (Validación OK)     ▼ (Validación FALLIDA)
[ Inyecta wril_self_root ] [ Absorbe la Tensión ]
      │                     │
      ▼                     ▼
[ Rango Consolidado ]   [ Muestra Pista / Reintento ]
```

---

## 7. Tensiones e Inconsistencias (Fase 1)
* **Tensión A (Ausencia de Identidad):** Carece por completo de cabecera MFN. Es un módulo "huérfano" de declaración pero crítico para la inducción de los newbies.
* **Tensión B (Puerto Secuestrado):** Al no utilizar el Faro de Puertos `port_lighthouse.py`, asume que el puerto `5005` estará libre de forma incondicional en loopback.
