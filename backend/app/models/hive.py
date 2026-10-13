from datetime import date, datetime
from sqlalchemy import Date, Integer, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Hive(Base):
    __tablename__ = "hives"

    id: Mapped[int] = mapped_column(primary_key=True) # id to ong
    farm_id: Mapped[int] = mapped_column(ForeignKey("farms.id"), index=True) 
    code: Mapped[str] = mapped_column(String(10), unique=True, index=True) # ma qr to ong
    name: Mapped[str] = mapped_column(String(80)) # ten loai ong
    zone: Mapped[str] = mapped_column(String(3), default="A") # khu vuc nuoi ong
    status: Mapped[str] = mapped_column(String(10), default="ok") # trang thai cua ong
    issue: Mapped[str] = mapped_column(String(200)) # mo ta van de cua to
    hive_year: Mapped[int] = mapped_column(String(200)) # tuoi doi cua thung ong
    hive_source: Mapped[str] = mapped_column(String(40), default="") #nguon giong
    last_check: Mapped[date | None] = mapped_column(Date, nullable= True) # thoi gian kiem tra gan nhat
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())