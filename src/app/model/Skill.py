from .BaseModel import BaseModel
from typing import TypedDict
from ..utils.ArrayTools import ArrayTools
from ..exceptions.ValidationException import ValidationException


class SkillType(TypedDict):
    skill_id: int
    name: str


class SkillWithIdType(TypedDict):
    id: int
    name: str


skillListType = list[SkillType]
skillListWithIdType = list[SkillWithIdType]


class SelectedSkill(TypedDict):
    selected_skill: int


class NewSkill(TypedDict):
    new_skill: str


SkillsFormData = list[SelectedSkill | NewSkill]


class Skill(BaseModel):
    def getAviableSkills(this) -> skillListWithIdType:
        return this._db.query("SELECT * FROM skill")

    def getSelectedSkillsFromFormdata(this, skillsFormData: SkillsFormData) -> list[int]:
        selectedSkills = ArrayTools.arrayUnique(ArrayTools.arrayColumn(skillsFormData, 'selected_skill'))
        ArrayTools.remove(selectedSkills, None)
        return selectedSkills

    def getNewSkillsFromFormdata(this, skillsFormData: SkillsFormData) -> list[str]:
        newSkills = ArrayTools.arrayUnique(ArrayTools.arrayColumn(skillsFormData, 'new_skill'))
        ArrayTools.remove(newSkills, None)
        return newSkills

    def checkSkillsExist(this, skillsIds: list[int]):
        if len(skillsIds) == 0:
            return None

        preparedIn = this._db.prepareForIn(skillsIds, 'ii')
        foundSkills = this._db.query(
            f"SELECT id FROM skill WHERE id IN({preparedIn['keys']})",
            preparedIn['values']
        )

        if len(foundSkills) == len(skillsIds):
            return None

        foundSkillsIds = ArrayTools.arrayColumn(foundSkills, 'id')
        skillsNotFound = ArrayTools.arrayDiff(skillsIds, foundSkillsIds)
        raise ValidationException('Skill not found', {'skillsNotFoundIds': skillsNotFound})

    def findOrCreateSkill(this, skillName: str) -> int:
        foundSkill = this._db.query(
            "SELECT id FROM skill WHERE name = %(sn)s",
            {'sn': skillName}
        )
        if len(foundSkill) > 0:
            return foundSkill[0]['id']

        this._db.execute("INSERT INTO skill(name) VALUES(%s)", [skillName])
        return this._db.getLastInsertId()

    def processSkillsFromFormdata(this, skillsFormData: SkillsFormData) -> list[int]:
        skillsId = this.getSelectedSkillsFromFormdata(skillsFormData)
        this.checkSkillsExist(skillsId)

        for newSkill in this.getNewSkillsFromFormdata(skillsFormData):
            skillsId.append(this.findOrCreateSkill(newSkill))
        return skillsId

    def addSkillsToItem(this, skills: list[int], itemId: int):
        for skill in skills:
            this._db.execute(
                "INSERT INTO astroman_has_skill(astroman_id, skill_id) VALUES(%(iid)s, %(sid)s)",
                {'iid': itemId, 'sid': skill},
                False
            )
        this._db.commit()

    def deleteAllSkillsFromItem(this, itemId: int):
        this._db.execute("DELETE FROM astroman_has_skill WHERE astroman_id = %s", [itemId])

    def isSkillsChanged(this, skillsData: SkillsFormData, itemId: int) -> bool:
        skillsId = this.processSkillsFromFormdata(skillsData)

        allSkillsInItemCount = this._db.query(
            "SELECT COUNT(*) AS n FROM astroman_has_skill WHERE astroman_id = %(iid)s",
            {'iid': itemId}
        )
        allSkillsInItemCount = allSkillsInItemCount[0]['n']
        if len(skillsId) != allSkillsInItemCount:
            return True

        if len(skillsId) == 0 and len(allSkillsInItemCount) == 0:
            return False

        preparedIn = this._db.prepareForIn(skillsId, 'sid')
        params = preparedIn['values']
        params['iid'] = itemId
        selectedSkillsInItemCount = this._db.query(
            f"""
            SELECT COUNT(*) AS n FROM astroman_has_skill
            WHERE astroman_id = %(iid)s AND skill_id IN({preparedIn['keys']})
            """,
            params
        )
        selectedSkillsInItemCount = selectedSkillsInItemCount[0]['n']

        if len(skillsId) != selectedSkillsInItemCount:
            return True
        else:
            return False
