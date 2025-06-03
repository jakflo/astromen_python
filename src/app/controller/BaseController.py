from fastapi import Response
from mysql.connector.errors import DatabaseError


class BaseController:
    def __init__(this, response: Response):
        this._response = response
        this._databaseConnectionErrorMsg = {'error': 'Database connection error'}

    def _changeResponse(this, code: int):
        this._response.status_code = code
