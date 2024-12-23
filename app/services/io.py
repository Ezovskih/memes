from httpx import AsyncClient, Response

from app.config import SERVER_HOST, SERVER_PORT, STORAGE_API_KEY
from app.routers import images


async def put_meme_image(meme_id: int, file_name: str, file_data: bytes) -> Response:
    async with AsyncClient() as client:
        response = await client.put(
            f"http://{SERVER_HOST}:{SERVER_PORT}/{images.TAG}/upload/{meme_id}",
            files={'image': (file_name, file_data)},
            headers={'x-api-key': STORAGE_API_KEY},
        )

    return response


async def get_meme_image(meme_id: int) -> Response:
    async with AsyncClient() as client:
        response = await client.get(
            f"http://{SERVER_HOST}:{SERVER_PORT}/{images.TAG}/download/{meme_id}",
            headers={'x-api-key': STORAGE_API_KEY},
        )

    return response


async def delete_meme_image(meme_id: int) -> Response:
    async with AsyncClient() as client:
        response = await client.delete(
            f"http://{SERVER_HOST}:{SERVER_PORT}/{images.TAG}/remove/{meme_id}",
            headers={'x-api-key': STORAGE_API_KEY},
        )

    return response
