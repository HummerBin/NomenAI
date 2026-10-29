from fastapi import APIRouter
from schemas.name import NameIn,NameOut
from core.agent import generate_names

router = APIRouter(prefix="/name")


@router.post("/",response_model=NameOut)
async def take_names(data:NameIn):
    result_name = await generate_names(data)
    return NameOut(names=result_name.names)