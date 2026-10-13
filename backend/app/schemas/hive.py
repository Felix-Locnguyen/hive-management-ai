from datetime import datetime, date
from pydantic import BaseModel, Field

# ZONE_PATTERN = "^(A|B|C|D)$"
STATUS_PATTERN = "^(ok|watch|bad)$"

# tao thong tin thung ong
class HiveCreate(BaseModel):
    farm_id: int
    code: str = Field(min_length=1, max_length=10)
    name: str = Field(min_length=2, max_length=80)
    zone: str = Field(default="A", max_length=3)
    status: str = Field(default="ok", pattern=STATUS_PATTERN)
    issue: str = Field(default="", max_length=200)
    queen_year: int | None = Field(default=None, ge=2000, le=2100)
    queen_source: str = Field(default="", max_length=40)
    last_check: date | None = None


# cap nhat hong tin thung ong
class HiveUpdate(BaseModel):
    farm_id: int | None = None
    code: str | None = Field(default=None, min_length=1, max_length=10)
    name: str | None = Field(default=None, min_length=2, max_length=80)
    zone: str | None = Field(default=None, pattern=ZONE_PATTERN)
    status: str | None = Field(default=None, pattern=STATUS_PATTERN)
    issue: str | None = Field(default=None, max_length=200)
    queen_year: int | None = Field(default=None, ge=2000, le=2100)
    queen_source: str | None = Field(default=None, max_length=40)
    last_check: date | None = None


# doc du lieu tu thung ong 
class HiveRead(BaseModel):
    id: int
    farm_id: int
    code: str
    name: str
    zone: str
    status: str
    issue: str
    queen_year: int | None
    queen_source: str
    last_check: date | None
    created_at: datetime

    model_config = {"from_attributes": True}