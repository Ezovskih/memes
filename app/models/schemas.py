from json import loads
from pydantic import BaseModel, ConfigDict, model_validator


class MemeBase(BaseModel):
    title: str
    desc: str | None = None


class MemeRequest(MemeBase):

    @model_validator(mode='before')  # включает @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**loads(value))
        return value


class MemeResponse(MemeBase):
    model_config = ConfigDict(from_attributes=True)  # orm_mode

    image: str | None = None


class MemeResponseExt(MemeResponse):
    id: int
