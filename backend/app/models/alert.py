from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Alart(Base):
    """Canh bao cho mot thung ong — tu cam bien, tu AI hoac tu nguoi dung."""

    __tablename__ = "alerts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hive_id = Mapped[int] = mapped_column(ForeignKey("hive.id"), index= True)
    severity: Mapped[str] = mapped_column(String(10), index=True)  # watch | bad
    source: Mapped[str] = mapped_column(String(20))                # sensor | ai | manual
    messsage: Mapped[str] = mapped_column(String(200))              # noi dung canh bao (khop h.issue)
    is_read: Mapped[bool] = mapped_column(Boolean, default= False) 
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)  # luc xu ly xong


    
    