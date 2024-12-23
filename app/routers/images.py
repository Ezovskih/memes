from io import BytesIO
from http import HTTPStatus
from fastapi import APIRouter, Depends, Header, File, UploadFile, Response, HTTPException
from traceback import format_exc as get_traceback

from app.config import STORAGE_API_KEY, STORAGE_NAME
from app.services.s3 import client


TAG = STORAGE_NAME  # "images"

DENIED_MESSAGE = "Доступ к хранилищу запрещен"
NOT_FOUND_MESSAGE = "Объект не найден в хранилище"

async def verify_api_key(x_api_key: str = Header(convert_underscores=True)):
    if x_api_key != STORAGE_API_KEY:
        raise HTTPException(HTTPStatus.FORBIDDEN, detail=DENIED_MESSAGE)

router = APIRouter(prefix=f"/{TAG}", tags=[TAG.title()], dependencies=[Depends(verify_api_key)])


@router.get("/download/{image_id}")
async def download(image_id: str):
    """Получить изображение из хранилища"""
    response = None
    try:
        response = client.get_object(STORAGE_NAME, image_id)
    except Exception:
        raise HTTPException(HTTPStatus.NOT_FOUND, NOT_FOUND_MESSAGE)
    else:
        return Response(response.data, media_type=response.headers.get('Content-Type'))
    finally:
        if response is not None:
            response.close()
            response.release_conn()


@router.put("/upload/{image_id}")
async def upload(image_id: str, image: UploadFile = File(...)):
    """Загрузить изображение в хранилище"""
    try:
        file_data = await image.read()
        meta_data = {'File-Name': image.filename}

        client.put_object(  # заменяет существующий объект!
            STORAGE_NAME, image_id,
            BytesIO(file_data), len(file_data),
            content_type=image.content_type, metadata=meta_data
        )
    except Exception as error:
        raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, f"{type(error)}: {get_traceback()}")


@router.delete("/remove/{image_id}", status_code=HTTPStatus.NO_CONTENT)  # 204
async def remove(image_id: str):
    """Изъять изображение из хранилища"""
    try:
        client.remove_object(STORAGE_NAME, image_id)
    except Exception as error:
        raise HTTPException(HTTPStatus.INTERNAL_SERVER_ERROR, f"{type(error)}: {get_traceback()}")
