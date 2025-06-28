from pydantic import BaseModel, EmailStr
from typing import List

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }

class UsersPaginatedResponse(BaseModel):
    data: List[UserRead]
    countData: int