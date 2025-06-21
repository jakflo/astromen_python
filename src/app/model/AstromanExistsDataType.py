from pydantic import Field
from .AstromanBaseDataType import AstromanBaseDataType


class AstromanExistsDataType(AstromanBaseDataType):
    not_id: int = Field(default=0, ge=0)
