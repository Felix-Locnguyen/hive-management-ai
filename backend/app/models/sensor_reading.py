from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SensorReading(Base):
    """Mot lan doc cam bien cua thung ong (ESP32 gui len dinh ky)."""

    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hive_id: Mapped[int] = mapped_column(ForeignKey("hives.id"), index=True)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)  # thoi diem do (UTC)
    temperature: Mapped[float] = mapped_column(Float)     # nhiet do (°C)
    humidity: Mapped[float] = mapped_column(Float)        # do am (%)
    sound_level: Mapped[float | None] = mapped_column(Float, nullable=True)   # am thanh (dB) — chua co mic thi bo trong
    battery: Mapped[int | None] = mapped_column(Integer, nullable=True)       # muc pin thiet bi (%)
    # activity / mass: tam thoi khong khoi tao do cam bien chua du
