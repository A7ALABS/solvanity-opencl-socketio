`import json
import socketio
import logging
from src.generator import search_pubkey, get_result
from fastapi import FastAPI
from fastapi_socketio import SocketManager
import uvicorn
import asyncio
logging.basicConfig(level="INFO", format="[%(levelname)s %(asctime)s] %(message)s")



app = FastAPI()
sio=socketio.AsyncServer(cors_allowed_origins='*',async_mode='asgi', transports=['websocket'])
socket_app = socketio.ASGIApp(sio)
app.mount("/", socket_app)


async def generate_address(prefix, jobId,  isCaseSensitive=True):
    starts_with_prefix = prefix
    ends_with_suffix = ""
    num_keys_to_generate = 1
    select_specific_device = False
    iteration_bits_value = 24
    if(len(starts_with_prefix) > 4):
        starts_with_prefix = starts_with_prefix.lower()
    generated_result = search_pubkey(
                starts_with_prefix,
                ends_with_suffix,
                num_keys_to_generate,
                select_specific_device,
                iteration_bits_value,
                isCaseSensitive
            )
    logging.info("Generation finished, making private and public key")
    privateKey, pubKey = get_result(generated_result)
    logging.info("Pub/secret key made, emitting result")
    await sio.emit('on-generated', json.dumps({"privateKey": privateKey, "pubKey": pubKey, "jobId":jobId}))
    logging.info("Result emitted")

def process_generation(prefix, jobId,  isCaseSensitive):
    asyncio.run(generate_address(prefix, jobId,  isCaseSensitive))

@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)

@sio.on('generate')
async def generate(sid, prefix, jobId,  isCaseSensitive=True):
    try:
        logging.info("Generation started")
        loop = asyncio.get_event_loop()
        loop.create_task(generate_address(prefix, jobId,  isCaseSensitive))

    except Exception as e:
        print(e)
        logging.info("Error while generation, sending error event")
        await sio.emit('on-error', json.dumps({"error": str(e), "jobId":jobId}))


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)

if __name__=="__main__":
    uvicorn.run("socketapp:app", host="0.0.0.0", port=5002, lifespan="on", reload=True)`