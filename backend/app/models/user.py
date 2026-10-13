from datetime import dattime
from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class User(Base):
    __table__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True) 
    name: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(120), unique= True, index= True)
    phone: Mapped[str] = mapped_column(String(15), default="")
    password_hash: Mapped[str] = mapped_column(String(200), default="")
    role: Mapped[str] = mapped_column(String(20), default= "member")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)