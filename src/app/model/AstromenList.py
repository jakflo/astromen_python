from .BaseModel import BaseModel
from .SkillCache import SkillCache
from ..utils.ArrayTools import ArrayTools
from .AstromenListPaginator import AstromenListPaginator
from typing import TypedDict
from .Skill import skillListType, Skill as SkillModel, SkillsFormData
from ..exceptions.NotFoundException import NotFoundException
from ..exceptions.AllreadyExistsException import AllreadyExistsException


class AstromanRecord(TypedDict):
    id: int
    first_name: str
    last_name: str
    dob: str


class AstromenListItemType(AstromanRecord):
    dob_cz: str
    skill_names: list['str']
    skills: skillListType


class PaginatorType(TypedDict):
    items_per_page: int
    current_page: int
    pages: int
    items: int


class AstromenListType(TypedDict):
    paginator: PaginatorType
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
        return this.getItemByNameAndDob(firstName, lastName, dob, notId) is not None

    def getItemByNameAndDob(this, firstName: str, lastName: str, dob: str, notId: int = 0) -> AstromanRecord | None:
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

        if len(found) == 0:
            return None
        return found[0]

    def addItem(
        this,
        firstName: str,
        lastName: str,
        dob: str,
        skillsData: SkillsFormData
    ) -> int:
        skillModel = SkillModel()
        if this.isAstromanExists(firstName, lastName, dob):
            raise AllreadyExistsException('inserting item allready exists')

        this._db.execute(
            """
            INSERT INTO astroman(first_name, last_name, DOB)
            VALUES (%(fn)s, %(ln)s, %(dob)s)
            """,
            this.__getParamsForInsertSql(firstName, lastName, dob)
        )

        newItemId = this._db.getLastInsertId()
        skillsId = skillModel.processSkillsFromFormdata(skillsData)
        skillModel.addSkillsToItem(skillsId, newItemId)

        return newItemId

    def editItem(
        this,
        id: int,
        firstName: str,
        lastName: str,
        dob: str,
        skillsData: SkillsFormData
    ):
        skillModel = SkillModel()
        
        this.getItem(id)
        if this.isAstromanExists(firstName, lastName, dob, id):
            raise AllreadyExistsException('inserting item allready exists')

        params = this.__getParamsForInsertSql(firstName, lastName, dob)
        params['iid'] = id
        this._db.execute(
            """
            UPDATE astroman
            SET first_name = %(fn)s, last_name = %(ln)s, DOB = %(dob)s
            WHERE id = %(iid)s
            """,
            params
        )

        skillsId = skillModel.processSkillsFromFormdata(skillsData)
        if skillModel.isSkillsChanged(skillsData, id):
            skillModel.deleteAllSkillsFromItem(id)
            skillModel.addSkillsToItem(skillsId, id)

    def deleteItem(this, id: int):
        skillModel = SkillModel()
        this.getItem(id)
        skillModel.deleteAllSkillsFromItem(id)
        this._db.execute("DELETE FROM astroman WHERE id = %s", [id])

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

    def __getParamsForInsertSql(this, firstName: str, lastName: str, dob: str) -> dict:
        return {
            'fn': firstName,
            'ln': lastName,
            'dob': dob
        }
