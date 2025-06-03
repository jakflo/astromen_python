from .BaseModel import BaseModel
from typing import TypedDict


class SkillListType(TypedDict):
    skill_id: int
    name: str


class SkillListWithIdType(TypedDict):
    id: int
    name: str


class Skill(BaseModel):
    def getAviableSkills(this) -> SkillListWithIdType:
        return this._db.query("SELECT * FROM skill")
