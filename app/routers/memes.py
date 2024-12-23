from http import HTTPStatus
from fastapi import APIRouter, Body, File, UploadFile, HTTPException
from fastapi.responses import Response, JSONResponse

from app.models.meme import Meme
from app.models.schemas import MemeResponse, MemeRequest, MemeResponseExt
from app.services import SessionDependency, crud, io


TAG = "memes"

NOT_FOUND_MESSAGE = "Запись не найдена"
CONFLICT_MESSAGE = "Запись уже существует"
DELETED_MESSAGE = "Запись успешно удалена"

router = APIRouter(prefix=f"/{TAG}", tags=[TAG.title()])

def attach_encoded_image(meme: Meme, data: bytes):
    from base64 import b64encode
    encoded_image = b64encode(data)

    meme.image = encoded_image.decode('UTF-8')


@router.get(f"/", response_model = list[MemeResponseExt])
async def read_memes(db: SessionDependency, page: int = 1, limit: int = 10, images: bool = False):
    """Получить данные набора мемов"""
    memes = crud.get_memes(db, offset=((page or 1) - 1) * limit, limit=limit)

    if not images:
        return memes

    for meme in memes:
        image_response = await io.get_meme_image(meme.id)
        if image_response.status_code == HTTPStatus.OK:
            attach_encoded_image(meme, image_response.read())

    return memes


@router.get("/{meme_id}")  # response_model = MemeResponse
async def read_meme(db: SessionDependency, meme_id: int):
    """Получить данные определенного мема"""
    found_meme: Meme = crud.get_meme(db, meme_id=meme_id)
    if not found_meme:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail=NOT_FOUND_MESSAGE)

    image_response = await io.get_meme_image(meme_id)
    if image_response.status_code == HTTPStatus.OK:
        # attach_image(found_meme, image_response.read())
        return Response(image_response.read(),
                        headers=found_meme.as_json(headers=True),
                        media_type=image_response.headers.get('content-type'))

    return JSONResponse(found_meme.as_json())


@router.post("/", response_model = MemeResponseExt)
async def create_meme(db: SessionDependency,
                      meme: MemeRequest = Body(),
                      image: UploadFile | str | None = File(None, media_type='image/*')):
    """Создать новый мем"""
    found_meme: Meme = crud.get_meme_by_title(db, meme_title=meme.title)
    if found_meme:
        raise HTTPException(HTTPStatus.CONFLICT, detail=CONFLICT_MESSAGE)

    new_meme = Meme(**meme.model_dump())
    crud.add_meme(db, meme=new_meme)

    if not (image is None or isinstance(image, str)):
        image_data = await image.read()
        image_response = await io.put_meme_image(new_meme.id, image.filename, image_data)
        if image_response.status_code == HTTPStatus.OK:
            attach_encoded_image(new_meme, image_data)

    return new_meme


@router.put("/{meme_id}", response_model = MemeResponse)
async def update_meme(db: SessionDependency,
                      meme_id: int, meme: MemeRequest = Body(),
                      image: UploadFile | str | None = File(None, media_type='image/*')):
    """Обновить данные мема"""
    found_meme: Meme = crud.get_meme(db, meme_id=meme_id)
    if not found_meme:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail=NOT_FOUND_MESSAGE)

    meme_data = meme.model_dump()  # dict
    crud.update_meme(db, meme=found_meme, **meme_data)

    if image is None or isinstance(image, str):
        await io.delete_meme_image(meme_id)  # или 204
    else:
        image_data: bytes = await image.read()
        image_response = await io.put_meme_image(meme_id, image.filename, image_data)
        if image_response.status_code == HTTPStatus.OK:
            attach_encoded_image(found_meme, image_data)

    return found_meme


@router.delete("/{meme_id}", status_code = HTTPStatus.NO_CONTENT)
async def delete_meme(db: SessionDependency, meme_id: int):
    """Удалить данные мема"""
    found_meme: Meme = crud.get_meme(db, meme_id=meme_id)
    if not found_meme:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail=NOT_FOUND_MESSAGE)

    await io.delete_meme_image(meme_id)

    crud.delete_meme(db, meme=found_meme)
