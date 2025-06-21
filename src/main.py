from fastapi import FastAPI, Response, Query, Path, Body
from typing import Annotated, Union, Literal
from app.controller.AstromenList import AstromenList
from pydantic import Field
from app.model.AstromanItemDataType import AstromanItemDataType
from app.model.AstromanExistsDataType import AstromanExistsDataType

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
    astromanExistsDataType: Annotated[AstromanExistsDataType, Query()]
):
    astromenList = AstromenList(response)
    return astromenList.isAstromanExists(
        astromanExistsDataType.first_name,
        astromanExistsDataType.last_name,
        astromanExistsDataType.dob,
        astromanExistsDataType.not_id
    )

@app.post("/add_item")
def addItem(    
    response: Response,
    newAstromanData: Annotated[AstromanItemDataType, Body()]
):
    astromenList = AstromenList(response)
    return astromenList.addItem(
        newAstromanData.first_name,
        newAstromanData.last_name,
        newAstromanData.dob,
        newAstromanData.skill
    )

@app.put("/edit_item/{id}")
def editItem(
    response: Response,
    id: Annotated[int, Path(gt=0)],
    astromanData: Annotated[AstromanItemDataType, Body()]
):
    astromenList = AstromenList(response)
    return astromenList.editItem(
        id,
        astromanData.first_name,
        astromanData.last_name,
        astromanData.dob,
        astromanData.skill
    )
