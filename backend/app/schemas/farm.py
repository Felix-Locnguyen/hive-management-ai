from datetime import date, datetime
from pydantic import BaseModel, Field

# khoi tao trang trai 
class FarmCreate(BaseModel):
    name: str = Field(min_length= 2, max_length= 120)
    address: str = Field(default="", max_length= 200)
    established: date | None = None
    owner_id: int | None = None

# Cap nhat trang trai
class FarmUpdate(BaseModel):
    name: str | None= Field(default=None, min_length= 2, max_length= 120)
    address: str | None= Field(default=None, max_length= 200)
    established: date | None = None
    owner_id: int | None = None

# doc du lieu tu trang trai

class FarmRead(BaseModel):
    id:int
    name: str
    address: str
    established: date | None 
    owner_id: int | None
    created_at: datetime

    model_config = {"from_attributes": True}