from .BaseController import BaseController
from ..model.AstromenList import AstromenList as AstromenListModel
from ..model.AstromenList import AstromenListType
from ..model.AstromenList import AstromenListItemType
from ..model.Skill import Skill
from ..model.Skill import skillListWithIdType
from ..conf.extraTypes import ErrorReturned
from ..conf.extraTypes import ValidationErrorReturned
from .BaseController import DatabaseError
from ..exceptions.ValidationException import ValidationException
from ..exceptions.NotFoundException import NotFoundException
from datetime import date


class AstromenList(BaseController):
    def getAstromen(this, page: int) -> AstromenListType | ErrorReturned:
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


    def isAstromanExists(this, firstName: str, lastName: str, dob: str, notId: int) -> bool | ErrorReturned | ValidationErrorReturned:
        try:
            this._validate(dob)
            astromenListModel = AstromenListModel()
            return {'response': astromenListModel.isAstromanExists(firstName, lastName, dob, notId)}
        except DatabaseError as e:
            this._changeResponse(500)
            return {'error': e.msg}
        except ValidationException as e:
            this._changeResponse(400)
            return {'validation_error': str(e)}

    def _validate(this, dob: str):
        try:
            date.fromisoformat(dob)
        except ValueError:
            raise ValidationException('dob must be in YYYY-mm-dd format')
