from pydantic import BaseModel, validator
from ..utils.ValidatorHelper import ValidatorHelper


class AstromanBaseDataType(BaseModel):
    first_name: str
    last_name: str
    dob: str

    @validator('first_name')
    def first_name_validator(cls, v):
        return ValidatorHelper.stringNotEmptyMaxLength(v, ValidatorHelper.firstNameMaxLength)

    @validator('last_name')
    def last_name_validator(cls, v):
        return ValidatorHelper.stringNotEmptyMaxLength(v, ValidatorHelper.lastNameMaxLength)

    @validator('dob')
    def dob_validator(cls, v):
        return ValidatorHelper.enDate(v)
