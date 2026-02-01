# lyra-backend
Backend API para el análisis semántico de canciones mediante IA. Construido con FastAPI, utiliza LRCLIB para la obtención de letras y APIFreeLLM para el procesamiento de lenguaje natural y extracción de insights.


# Instrucciones para la instalación y ejecución de este proyecto

Requisitos:
- Tener instalado Python 3.10 o superior
- pip
- git

Configuración del Backend:
1. Crear y activar el entorno virtual
    - python3 -m venv venv
    
    (Para Linux / macOS)
    - source venv/bin/activate

    (Para Windows) 
    - venv\Scripts\activate

2. Instalar dependencias
    - pip install -r requirements.txt

3. Crear un archivo .env en la raiz del proyecto que contenga:
    API_KEY=tu_api_key

    Esta API_KEY es necesaria para consumir la API externa de IA utilizada para el análisis de canciones

4. Ejecutar el servidor FastAPI
    - uvicorn app.main:app --reload



# Desiciones técnicas

Problematica: Análisis de canciones con IA (LLM)

El endpoint encargado de analizar la letra de una canción usando una API externa de IA (LLM) presenta un problema con el tiempo de respuesta.

El problema es que la API externa de IA puede tardar mucho tiempo en responder, el servidor backend mantiene bloqueado el worker durante toda la espera,
y en muchos casos el servidor “se cansa” de esperar y termina la conexión antes de que la IA responda.

Esto provoca timeouts, errores, mala experiencia de usuario, y si hay muchas solicitudes puede causar bajo rendimiento.

Hay varias opciones para manejar este caso, por ejemplo:

Una primera aproximación es extender el tiempo de espera al llamar a la API, como puede ser "httpx.AsyncClient(timeout=90.0)"

Con esto el backend espera hasta 90 segundos la respuesta del LLM, pero tiene algunas desventajas, como de que el worker del servidor queda bloqueado durante toda la espera, no escala bien bajo carga, no es ideal para producción.
Esta solución puede servir para prototipos o tráfico muy bajo.

Otra solución más robusta puede ser la siguiente:

1. El frontend envía la solicitud POST /analysis.
2. El backend crea un job_id y responde inmediatamente (202 Accepted).
3. El análisis con la IA se ejecuta en background.
4. El frontend consulta periódicamente el estado del job (polling), por ejemplo cada 3 segundos: GET /analysis/{job_id}

Con esto el backend no bloquea workers, el servidor no se “cansa” esperando la respuesta y la experiencia de usuario es mejor.
Pero esto requiere múltiples peticiones HTTP y el frontend debe manejar polling y estados intermedios.

Una solución más eficiente es usar WebSockets para este caso de uso.
El flujo seria el siguiente:

1. El frontend inicia el análisis (POST /analysis) y obtiene un job_id.
2. El frontend abre una conexión WebSocket asociada a ese job_id.
3. El backend ejecuta el análisis en background.
4. Cuando la IA responde, el backend empuja el resultado directamente al frontend a través del WebSocket.

La ventaja de esto es que no hay polling y se obtiene una respuesta en tiempo real
con un backend más eficiente.

En este proyecto, para el enfoque que estamos manejando, los jobs se almacenarian de esta manera:

analysis_jobs = {
    "job_id": {
        "status": "processing | done | failed",
        "result": {...} | None,
        "error": str | None
    }
}

Para que esto sea adecuado para produccion, los jobs se deben almacenar en bases de datos o en algun sistema de colas.

Pero por simplicidad, para una aplicación sencilla como esta, donde no tendra uso intensivo, se usara la primera opción, donde extendemos el tiempo de espera de la API para recibir la respuesta del LLM. Se omitirán intencionalmente los jobs en el background y websockets.



