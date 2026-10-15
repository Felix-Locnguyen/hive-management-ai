from datetime import datetime, date
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base

class SensorReading(Base):
    __tablename__ = "sensor_readings"

class SensorReading(Base):
    """Mot lan doc cam bien cua thung ong (ESP32 gui len dinh ky)."""

    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hive_id: Mapped[int] = mapped_column(ForeignKey("hives.id"), index=True)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), index=True)  # thoi diem do
    temperature: Mapped[float] = mapped_column(Float)     # nhiet do (�C)
    humidity: Mapped[float] = mapped_column(Float)        # do am (%)
    sound_level: Mapped[float] = mapped_column(Float)     # am thanh (dB)
    pin: Mapped[int] = mapped_column(Integer, nullable=True)             # pin cua thi bi
    # activity / mass: tam thoi khong khoi tao do cam bien chua du