from datetime import date, datetime
from pydantic import BaseModel, Field

# Thiet bi gui du lieu cam bien ve server
# Thiet bi gui du lieu cam bien len
class SensorReadingCreate(BaseModel):
    recorded_at: datetime | None = None           # bo trong -> server lay hien tai (UTC)
    temperature: float = Field(ge=-10, le=60)     # nhiet do (�C)
    humidity: float = Field(ge=0, le=100)         # do am (%)
    sound_level: float | None = Field(default=None, ge=0, le=200)  # am thanh (dB)
    battery: int | None = Field(default=None, ge=0, le=100)        # muc pin thiet bi (%)

class SensorReadingRead(BaseModel):
    id: int
    hive_id: int
    recorded_at: datetime
    temperature: float
    humidity: float
    sound_level: float | None
    battery: int | None

    model_config = {"from_attributes": True}