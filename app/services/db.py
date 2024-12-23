from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME
from app.models import Base


DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(engine, autoflush=False, autocommit=False)


def get_session():
    db: Session = SessionLocal()  # factory

    try:
        yield db
    finally:
        db.close()


def init_db():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


async def _async_init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
