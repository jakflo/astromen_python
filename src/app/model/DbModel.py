import mysql.connector
from ..conf.conf import db


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

    def prepareForIn(this, values, prefix):
        keys = []
        x = 1
        dictValues = {}
        for item in values:
            prefixedKey = prefix + str(x)
            keys.append(f"%({prefixedKey})s")
            dictValues[prefixedKey] = item
            x += 1
        return {'keys': ','.join(keys), 'values': dictValues}
