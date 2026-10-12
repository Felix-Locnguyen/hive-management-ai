from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# SQLite bắt buộc check_same_thread=False vì FastAPI phục vụ request từ nhiều thread
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args)

# sessionmaker: "nhà máy" tạo session DB — mỗi request 1 session
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    """Mọi ORM model (User, Hive, Item...) sẽ kế thừa từ lớp này."""
    pass


def get_db():
    """Dependency của FastAPI: mở session → nhường vào route → đóng lại (finally)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()