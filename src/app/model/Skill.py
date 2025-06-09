from .BaseModel import BaseModel
from typing import TypedDict


class SkillType(TypedDict):
    skill_id: int
    name: str


class SkillWithIdType(TypedDict):
    id: int
    name: str


skillListType = list[SkillType]
skillListWithIdType = list[SkillWithIdType]


class Skill(BaseModel):
    def getAviableSkills(this) -> skillListWithIdType:
        return this._db.query("SELECT * FROM skill")
