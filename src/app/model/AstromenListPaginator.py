from .BaseModel import BaseModel
from typing import Literal
from ..conf.conf import itemsPerPage
import math

numPage = int | Literal['last']


class AstromenListPaginator(BaseModel):
    def __init__(this, currentPage: numPage):
        super().__init__()
        this._itemsPerPage = itemsPerPage
        this._currentPage = currentPage
        this._itemsCount = 0
        this._pages = 0
        this._offset = 0
        this._prepare()

    def _prepare(this):
        itemsCount = this._getItemsCount()
        this._pages = math.ceil(itemsCount / this._itemsPerPage)
        if this._currentPage == 'last':
            this._currentPage = this._pages
        this._offset = this._itemsPerPage * (this._currentPage - 1)

    def _getItemsCount(this) -> int:
        result = this._db.query("SELECT COUNT(*) AS n FROM astroman")
        this._itemsCount = result[0]['n']
        return this._itemsCount

    def getOffset(this) -> int:
        return this._offset

    def getItemsPerPage(this) -> int:
        return this._itemsPerPage

    def getCurrentPage(this) -> int:
        return this._currentPage

    def getPages(this) -> int:
        return this._pages

    def getItemsCount(this) -> int:
        return this._itemsCount
