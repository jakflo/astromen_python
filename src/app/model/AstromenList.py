from .BaseModel import BaseModel
from .SkillCache import SkillCache
from ..utils.ArrayTools import ArrayTools
from .AstromenListPaginator import AstromenListPaginator
from typing import TypedDict
from .Skill import skillListType
from ..exceptions.NotFoundException import NotFoundException


class AstromenListItemType(TypedDict):
    id: int
    first_name: str
    last_name: str
    dob: str
    dob_cz: str
    skill_names: list['str']
    skills: skillListType


class AstromenListType(TypedDict):
    items_per_page: int
    current_page: int
    pages: int
    items: list[AstromenListItemType]


class AstromenList(BaseModel):
    def getList(this, page: int) -> AstromenListType:
        astromenListPaginator = AstromenListPaginator(page)
        list = this._db.query("""
        SELECT *
        FROM astroman
        LIMIT %(li)s
        OFFSET %(os)s""",
        {
            'li': astromenListPaginator.getItemsPerPage(),
            'os': astromenListPaginator.getOffset()
        }
        )
        return {
            'paginator': {
                'items_per_page': astromenListPaginator.getItemsPerPage(),
                'current_page': astromenListPaginator.getCurrentPage(),
                'pages': astromenListPaginator.getPages(),
                'items': astromenListPaginator.getItemsCount()
            },
            'items': this._processList(list)
        }

    def getItem(this, id: int) -> AstromenListItemType:
        item = this._db.query("SELECT * FROM astroman WHERE id = %(iid)s", {'iid': id})
        if len(item) == 0:
            raise NotFoundException(f"Item id = {id} not found")
        return this._processList(item)[0]

    def isAstromanExists(this, firstName: str, lastName: str, dob: str, notId: int = 0) -> bool:
        params = {
            'fname': firstName.strip(),
            'lname': lastName.strip(),
            'dob': dob
        }

        if notId != 0:
            params['notId'] = notId
            notIdTerm = " AND id != %(notId)s"
        else:
            notIdTerm = ''

        found = this._db.query(f"""
        SELECT *
        FROM astroman
        WHERE first_name = %(fname)s
            AND last_name = %(lname)s
            AND dob = %(dob)s {notIdTerm}
        LIMIT 1
        """,
        params
        )
        return len(found) == 1

    def _processList(this, list) -> list[AstromenListItemType]:
        skillCache = SkillCache(ArrayTools.arrayColumn(list, 'id'))
        output = []
        for item in list:
            skills = skillCache.getSkills(item['id'])
            output.append({
                'id': item['id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'dob': item['DOB'],
                'dob_cz': item['DOB'].strftime('%-d. %-m. %Y'),
                'skill_names': ArrayTools.arrayColumn(skills, 'name'),
                'skills': skills
            })
        return output
