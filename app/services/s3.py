from minio import Minio
from urllib3 import PoolManager

from app.config import STORAGE_HOST, STORAGE_PORT, STORAGE_ACCESS_KEY, STORAGE_SECRET_KEY, STORAGE_NAME


STORAGE_ENDPOINT = f"{STORAGE_HOST}:{STORAGE_PORT}"

client = Minio(
    STORAGE_ENDPOINT,
    access_key=STORAGE_ACCESS_KEY,
    secret_key=STORAGE_SECRET_KEY,
    secure=False,
    http_client=PoolManager(num_pools=10, retries=False)
)

try:
    if not client.bucket_exists(STORAGE_NAME):
        client.make_bucket(STORAGE_NAME)
except Exception as error:
    print(f"Ошибка подключения к хранилищу: {error}")
