from datetime import datetime
from pydantic import BaseModel, Field

# Hao giua khong doi — dat ten ro de dung lai cho AI/alert_rules.py sau nay
SEVERITY_PATTERN = "^(watch|bad)$"
SOURCE_PATTERN = "^(sensor|ai|manual)$"

# He thong (sensor/AI) hoac nguoi dung tao canh bao
class AlertCreate(BaseModel):
    hive_id: int
    severity: str = Field(pattern=SEVERITY_PATTERN)
    source: str = Field(default="manual", pattern=SOURCE_PATTERN)
    message: str = Field(min_length=3, max_length=200)

# cap nhat trang thai canh bao (da doc / da xu ly xong)
class AlertUpdate(BaseModel):
    is_read: bool | None = None
    resolved_at: datetime | None = None

# Doc canh bao
class AlertRead(BaseModel):
    id: int
    hive_id: int
    severity: str
    source: str
    message: str
    is_read: bool
    created_at: datetime
    resolved_at: datetime | None

    model_config = {"from_attributes": True}