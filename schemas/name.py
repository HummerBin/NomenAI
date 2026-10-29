from pydantic import BaseModel,Field
from typing import Annotated,Literal,Optional,List
from .agent import NamneSchema
###校验生成姓名时，前端数据上传的合法性，以及定义生成姓名后的返回格式

class NameIn(BaseModel):
    surname:Annotated[str,Field(...,description="姓氏")]
    gender:Annotated[Literal["不限","男","女"],Field(...,description="性别")]
    length:Annotated[Literal["不限","单字","两字"],Field(...,description="字数")]
    other:Annotated[str|None,Field("",description="其他要求")]
    exclude:Annotated[List[str],Field(...,description="姓氏")]

class NameOut(BaseModel):
    names:List[NamneSchema]