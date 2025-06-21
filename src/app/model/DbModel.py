import mysql.connector
from ..conf.conf import db
from typing import TypedDict


class PrepareForInDatatype(TypedDict):
    keys: str
    values: dict[str, any]


class DbModel:
    def __init__(this):
        this.__conn = mysql.connector.connect(
            host=db['host'],
            user=db['user'],
            password=db['password'],
            database=db['database']
        )

    def query(this, sql: str, params: list | dict = []) -> list:
        mycursor = this.__conn.cursor(dictionary=True)
        mycursor.execute(sql, params)
        return mycursor.fetchall()

    def execute(this, sql: str, params: list | dict = [], commit: bool = True):
        mycursor = this.__conn.cursor(dictionary=True)
        mycursor.execute(sql, params)
        if commit:
            this.__conn.commit()

    def commit(this):
        this.__conn.commit()

    def getLastInsertId(this) -> int:
        result = this.query("SELECT LAST_INSERT_ID() AS id")
        return result[0]['id']

#    pripravi sql retezec a dict s paramatry pro hodnoty uvnitr SQL IN(...) termu
    def prepareForIn(this, values: list, prefix: list[str]) -> PrepareForInDatatype:
        keys = []
        x = 1
        dictValues = {}
        for item in values:
            prefixedKey = prefix + str(x)
            keys.append(f"%({prefixedKey})s")
            dictValues[prefixedKey] = item
            x += 1
        return {'keys': ','.join(keys), 'values': dictValues}
