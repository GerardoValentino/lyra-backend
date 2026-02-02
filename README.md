# lyra-backend
Backend API para el análisis semántico de canciones mediante IA. Construido con FastAPI, utiliza LRCLIB para la obtención de letras y APIFreeLLM para el procesamiento de lenguaje natural y extracción de insights.


# Instrucciones para la instalación y ejecución de este proyecto

Requisitos:
- Tener instalado Python 3.10 o superior
- pip
- git

Configuración del Backend:
En la raíz del proyecto:

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

    Esta API_KEY es necesaria para consumir la API externa de IA (APIFreeLLM) utilizada para el análisis de canciones

4. Ejecutar el servidor FastAPI
    - uvicorn app.main:app --reload

5. Para ver la documentacion en Swagger UI nativa de FastAPI, ir a:
    http://<la_url>/docs

    Ejemplo: http://127.0.0.1:8000/docs

# Desiciones técnicas

Dónde escribir el prompt:
En este caso se considero agregar el "Prompt" directamente en el backend, ya que enviarlo desde el frontend se corren riesgos de seguridad, por ejemplo:

Al mantener el prompt en el frontend, cualquier usuario con conocimientos básicos de la consola del navegador podría ver las instrucciones exactas enviadas a la IA. Moverlo al backend oculta la lógica de negocio y evita que usuarios malintencionados manipulen las instrucciones para obtener respuestas no deseadas o consumir créditos de la API de forma indebida.

Además, enviar la letra de la canción + un prompt extenso desde el navegador aumenta innecesariamente el tamaño de la petición HTTP. Al mover el prompt al backend, el frontend solo envía la información mínima necesaria (la letra), dejando que el servidor ensamble la petición completa hacia el proveedor de IA.


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

En este proyecto, para el enfoque que estamos manejando, los jobs se almacenarian de esta manera, por ejemplo:

analysis_jobs = {
    "job_id": {
        "status": "processing | done | failed",
        "result": {...} | None,
        "error": str | None
    }
}

Para que esto sea adecuado para produccion, los jobs se deben almacenar en bases de datos o en algun sistema de colas.

Pero por simplicidad, para una aplicación sencilla como esta, donde no tendra uso intensivo, se usará la primera opción, donde extendemos el tiempo de espera de la API para recibir la respuesta del LLM. Se omitirán intencionalmente los jobs en el background y websockets.


# Arquitectura del proyecto

La estructura general del proyecto es la siguiente:

app/
├── api/
│   └── v1/
│       ├── routes/
│       ├── services/
│       ├── dependencies.py
│       └── router.py
├── schemas/
├── utils/
├── exceptions.py
├── main.py

Con esta arquitectura se separan responsabilidades de una mejor manera.

El flujo general de una petición es la siguiente:

1. El cliente llama a un endpoint (routes)
2. El endpoint valida la entrada (schemas)
3. El endpoint delega la lógica al service
4. El service ejecuta la lógica o llamadas externas
5. El endpoint traduce el resultado a una respuesta HTTP estándar


Aunque esta aplicación es pequeña y está pensada para pruebas, se decidió usar esta arquitectura desde el inicio para facilitar futuras extensiones.

# Endpoints
La API está organizada bajo la versión v1 y estructurada para una integración sencilla con aplicaciones de frontend.

1. Obtener letra de canción
Busca y retorna la letra plana de una canción específica.

URL: /api/v1/songs/lyrics
Método: GET

Parámetros de consulta (Query Params):

Parámetro   Tipo    Obligatorio     Descripción
--------------------------------------------------------------
song_name	string	    Sí	    Nombre de la canción a buscar.
artist	    string	    Sí	    Nombre del artista o banda.

Ejemplo de respuesta:

{
    "success": true,
    "message": "Letra obtenida correctamente",
    "data": {
        "id": 190929,
        "name": "Chiquitita",
        "trackName": "Chiquitita",
        "artistName": "ABBA",
        ...
    }
}

2. Análisis de letra con IA
Procesa la letra de una canción para generar un análisis profundo utilizando modelos de lenguaje (LLM).

URL: /api/v1/songs/analysis
Método: POST

Cuerpo de la petición (Request Body): 
{
  "song_lyrics": "string (contenido de la letra)"
}

Este endpoint utiliza un System Prompt almacenado en el servidor para garantizar la consistencia del análisis y proteger la lógica de las instrucciones. El análisis incluye clasificación por categorías, interpretación de metáforas y detección de entidades comerciales.

Ejemplo de respuesta:
{
  "success": true,
  "data": {
    "categoria": "Desamor",
    "resumen": "La canción describe la ruptura...",
    "perspectiva": "Masculino"
  }
}