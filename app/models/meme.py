from sqlalchemy import Column, Integer, String, Text

from app.models import Base


class Meme(Base):
    __tablename__ = "memes"

    id = Column(Integer, index=True, primary_key=True)  # Base -> autoincrement

    title = Column(String(255), index=True, nullable=False)
    desc = Column(Text, default=None, nullable=True)

    def as_json(self, headers = False) -> dict:
        prefix = 'meme-' if headers else ''

        return {prefix + col.name: str(getattr(self, col.name))
                for col in list(self.__table__.columns)}
