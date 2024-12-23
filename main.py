from contextlib import asynccontextmanager
from uvicorn import run as uvicorn_run
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.config import SERVER_HOST, SERVER_PORT
from app.routers import memes, images
from app.services.db import init_db


def dump_api_schema():
    from json import dumps
    schema: dict = app.openapi()
    with open("openapi.json", 'w+') as file:
        file.write(dumps(schema, indent=2))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # до начала работы сервера...
    # dump_api_schema()
    init_db()
    yield  # ...после завершения работы сервера

app = FastAPI(lifespan=lifespan)  # TODO meme_app/image_app?

app.include_router(memes.router)
app.include_router(images.router)

app.add_event_handler('startup', init_db)


@app.get("/", tags=["Root"])
async def root():
    """Приветственное сообщение"""
    return HTMLResponse("<h1>«Коллекция мемов»</h1>")  # 200


if __name__ == "__main__":
    uvicorn_run(app, host=SERVER_HOST, port=SERVER_PORT)
