from fastapi import FastAPI, Response, Query, Path
from typing import Annotated, Union, Literal
from app.controller.AstromenList import AstromenList
from pydantic import Field

app = FastAPI()

positiveIntOrLast = Annotated[
    Union[Literal["last"], Annotated[int, Field(gt=0)]],
    Query(description="Positive integer (>0) or 'last'")
]

@app.get("/get_list")
def getList(response: Response, page: positiveIntOrLast = 1):
    astromenList = AstromenList(response)
    return astromenList.getAstromen(page)
    
@app.get("/get_item/{id}")
def getItem(response: Response, id: Annotated[int, Path(gt=0)]):
    astromenList = AstromenList(response)
    return astromenList.getItem(id)

@app.get("/get_aviable_skills")    
def getAviableSkills(response: Response):
    astromenList = AstromenList(response)
    return astromenList.getAviableSkills()

@app.get("/is_astroman_exists")
def isAstromanExists(
    response: Response,
    first_name: Annotated[str, Query(max_length=32)],
    last_name: Annotated[str, Query(max_length=32)],
    dob: str,
    not_id: Annotated[int, Query(gte=0)] = 0
):
    astromenList = AstromenList(response)
    return astromenList.isAstromanExists(first_name, last_name, dob, not_id)
