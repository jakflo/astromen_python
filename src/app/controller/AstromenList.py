from .BaseController import BaseController
from ..model.AstromenList import AstromenList as AstromenListModel, AstromenListType, AstromenListItemType
from ..model.Skill import Skill, skillListWithIdType, SkillsFormData
from ..conf.extraTypes import ErrorReturned
from .BaseController import DatabaseError
from ..exceptions.NotFoundException import NotFoundException
from ..exceptions.AllreadyExistsException import AllreadyExistsException
from ..model.AstromenListPaginator import numPage, AstromenListPaginator


class AstromenList(BaseController):
    def getAstromen(this, page: numPage) -> AstromenListType | ErrorReturned:
        try:
            astromenListModel = AstromenListModel()
            return astromenListModel.getList(page)
        except DatabaseError as e:
            this._changeResponse(500)
            return {'error': e.msg}

    def getItem(this, id: int) -> AstromenListItemType:
        try:
            astromenListModel = AstromenListModel()
            return astromenListModel.getItem(id)
        except DatabaseError as e:
            this._changeResponse(500)
            return {'error': e.msg}
        except NotFoundException as e:
            this._changeResponse(404)
            return {'not_found_error': str(e)}

    def getAviableSkills(this) -> skillListWithIdType | ErrorReturned:
        try:
            skill = Skill()
            return skill.getAviableSkills()
        except DatabaseError as e:
            this._changeResponse(500)
            return {'error': e.msg}

    def isAstromanExists(
        this,
        firstName: str,
        lastName: str,
        dob: str,
        notId: int
    ):
        try:
            astromenListModel = AstromenListModel()
            return {'response': astromenListModel.isAstromanExists(firstName, lastName, dob, notId)}
        except DatabaseError as e:
            this._changeResponse(500)
            return {'error': e.msg}

    def addItem(
        this,
        firstName: str,
        lastName: str,
        dob: str,
        skillsData: SkillsFormData
    ):
        try:
            astromenListModel = AstromenListModel()
            newItemId = astromenListModel.addItem(firstName, lastName, dob, skillsData)
            paginator = AstromenListPaginator('last')

            return {
                'info': 'new item inserted',
                'new_item_id': newItemId,
                'paginator': {
                    'items_per_page': paginator.getItemsPerPage(),
                    'current_page': paginator.getCurrentPage(),
                    'pages': paginator.getPages(),
                    'items': paginator.getItemsCount()
                }
            }
        except AllreadyExistsException:
            this._changeResponse(422)
            return this.__getItemExistError(firstName, lastName, dob)
        except DatabaseError as e:
            this._changeResponse(500)
            return {'error': e.msg}

    def editItem(
        this,
        id: int,
        firstName: str,
        lastName: str,
        dob: str,
        skillsData: SkillsFormData
    ):
        try:
            astromenListModel = AstromenListModel()
            astromenListModel.editItem(id, firstName, lastName, dob, skillsData)
            return {
                'info': 'item edited',
                'item_id': id
            }
        except NotFoundException as e:
            this._changeResponse(404)
            return {'not_found_error': str(e)}
        except AllreadyExistsException:
            this._changeResponse(422)
            return this.__getItemExistError(firstName, lastName, dob, id)
        except DatabaseError as e:
            this._changeResponse(500)
            return {'error': e.msg}

    def __getItemExistError(this, firstName: str, lastName: str, dob: str, notId: int = 0):
        astromenListModel = AstromenListModel()
        itemDataRaw = astromenListModel.getItemByNameAndDob(firstName, lastName, dob, notId)
        itemData = astromenListModel.getItem(itemDataRaw['id'])
        return {
            'error': 'item allready exists',
            'existing_item_data': itemData
        }
