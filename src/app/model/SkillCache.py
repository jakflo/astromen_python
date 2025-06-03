from .BaseModel import BaseModel
from ..utils.ArrayTools import ArrayTools
from ..exceptions.NotFoundException import NotFoundException
from .Skill import SkillListType


class SkillCache(BaseModel):
    def __init__(this, astromanIds: list = []):
        super().__init__()
        this.__items = []
        this.__load(astromanIds)

    def getSkills(this, astromanId: int) -> SkillListType:
        foundSkills = ArrayTools.searchInMultiarray(this.__items, 'id', astromanId)
        if len(foundSkills) > 0:
            return this.__formatSkills(foundSkills)
        else:
            newFoundSkills = this._db.query(f"""
            SELECT ah.astroman_id AS id, s.id AS skill_id, s.name
            FROM astroman_has_skill ah
            JOIN skill s ON ah.skill_id = s.id
            WHERE ah.astroman_id = %(ii)s""",
            {'ii': astromanId})
            if len(newFoundSkills) == 0:
                raise NotFoundException('id not found')
            this.__items.append(newFoundSkills)
            return this.__formatSkills(newFoundSkills)

    def __load(this, astromanIds: list = []):
        if len(astromanIds) == 0:
            return
        preparedIn = this._db.prepareForIn(astromanIds, 'ii')
        this.__items = this._db.query(f"""
            SELECT ah.astroman_id AS id, s.id AS skill_id, s.name
            FROM astroman_has_skill ah
            JOIN skill s ON ah.skill_id = s.id
            WHERE ah.astroman_id IN({preparedIn['keys']})""",
        preparedIn['values']
        )
        return

    def __formatSkills(this, skills: list) -> SkillListType:
        output = []
        for item in skills:
            output.append({'skill_id': item['skill_id'], 'name': item['name']})
        return output
