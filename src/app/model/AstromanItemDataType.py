from .AstromanBaseDataType import AstromanBaseDataType
from typing import Annotated, List, TypedDict
from fastapi import Body
from ..utils.ValidatorHelper import ValidatorHelper
from pydantic import validator
from ..model.Skill import Skill
from ..exceptions.ValidationException import ValidationException


class SelectedSkill(TypedDict):
    selected_skill: Annotated[int, Body(gt=0)]


class NewSkill(TypedDict):
    new_skill: Annotated[str, Body(max_length=ValidatorHelper.skillNameMaxLength)]


SkillListDataType = List[SelectedSkill | NewSkill]


class AstromanItemDataType(AstromanBaseDataType):
    skill: SkillListDataType

    @validator('skill')
    def skill_validator(cls, v):
        skillModel = Skill()
        selectedSkills = skillModel.getSelectedSkillsFromFormdata(v)
        try:
            skillModel.checkSkillsExist(selectedSkills)
        except ValidationException as e:
            exceptionArgs = e.args
            notFoundIds = exceptionArgs[1]['skillsNotFoundIds'][0]
            raise ValueError(f"Skill not found (id: {notFoundIds})")
        return v
