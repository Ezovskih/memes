from sqlalchemy.orm import Session

from app.models.meme import Meme


def get_memes(db: Session, offset: int = 0, limit: int = 10) -> list[Meme]:
    return db.query(Meme).offset(offset).limit(limit).all()


def get_meme(db: Session, meme_id: int) -> Meme | None:
    return db.query(Meme).filter(Meme.id == meme_id).first()


def get_meme_by_title(db: Session, meme_title: str) -> Meme | None:
    return db.query(Meme).filter(Meme.title == meme_title).first()  # index


def add_meme(db: Session, meme: Meme) -> Meme:
    db.add(meme)

    try:
        db.commit()
    except:
        db.rollback()
        raise
    else:
        db.refresh(meme)  # id

    return meme


def update_meme(db: Session, meme: Meme, **updated) -> Meme:
    # db.query(Meme).filter(Meme.id == meme.id).update(updated)
    for key, value in updated.items():
        if hasattr(meme, key): setattr(meme, key, value)

    try:
        db.commit()
    except:
        db.rollback()
        raise

    return meme


def delete_meme(db: Session, meme: Meme):
    db.delete(meme)

    try:
        db.commit()
    except:
        db.rollback()
        raise
