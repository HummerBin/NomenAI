from fastapi import APIRouter,Depends
from schemas.name import NameIn,NameOut
from core.agent import generate_names
from core.auth import AuthHandler

auth_handler = AuthHandler()

router = APIRouter(prefix="/name")


@router.post("/",response_model=NameOut)
async def take_names(
        data:NameIn,
        user_id: int = Depends(auth_handler.auth_access_dependency)
    ):
    result_name = await generate_names(data)
    return NameOut(names=result_name.names)