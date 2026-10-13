from datetime import datetime
from pydantic import BaseModel, Field


# khoi tao tai khoan nguoi dung
class UserCreate(BaseModel):
    name: str = Field(min_length= 2, max_length= 80)
    email: str = Field(max_length= 120)
    phone: str = Field(default="", max_length= 15)
    role: str = Field(default="member", pattern= "^(admin|member)$")
# cap nhat tai khoan nguoi dung
class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length= 2, max_length= 80)
    email:str | None = Field(default= None, max_length= 120)
    phone:str | None = Field(default=None, max_length= 15)
    role: str | None = Field(default=None, pattern="^(admin|member)$")
    is_active: bool | None = None

# doc tai khoan khoan 
class UserRead(BaseModel):
    id:int
    name:str
    phone:str
    role:str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes":True} # cho phep doc tu ORM object

