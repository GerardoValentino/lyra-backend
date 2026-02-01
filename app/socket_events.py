from app.socket import sio

@sio.event
async def connect(sid, environ):
    print(f"Cliente conectado: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Cliente desconectado: {sid}")

@sio.event
async def join_job(sid, data):
    job_id = data["job_id"]
    await sio.enter_room(sid, job_id)