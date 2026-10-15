from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime, timedelta, timezone

from app.database import get_db
from app.models.hive import Hive
from app.models.sensor_reading import SensorReading
from app.schemas.sensor_reading import SensorReadingCreate, SensorReadingRead

router = APIRouter(prefix="/api/hives/{hive_id}/readings", tags=["Sensors"])

def _get_or_404(db: Session, hive_id: int) -> Hive:
    """Lay thung ong theo id hoac tra ve 404 neu khong ton tai."""
    hive = db.get(Hive, hive_id)
    if not hive:
        raise HTTPException(status_code=404, detail="Hive not found")
    return hive

# ban ghi nhan moi nhat
@router.get("/latest", response_model=SensorReadingRead)
def latest_reading(hive_id: int, db: Session = Depends(get_db)):
    """GET /api/hives/12/readings/latest — du lieu cam bien moi nhat."""
    _get_or_404(db, hive_id)
    reading = db.scalars(                    # scalars() tra ve collection -> dung .first()
        select(SensorReading)
        .where(SensorReading.hive_id == hive_id)
        .order_by(SensorReading.recorded_at.desc(), SensorReading.id.desc())
    ).first()
    if not reading:
        raise HTTPException(status_code=404, detail="Thung chua co du lieu cam bien")
    return reading


# Chuoi du lieu theo thoi gian — ve bieu do (24h / 7d / 30d)
@router.get("/chart", response_model=list[SensorReadingRead])
def list_readings(
    hive_id: int,
    hours: int = Query(default=24, ge=1, le=720), # gio (1d / 7d / 30d)
    limit: int = Query(default=200, ge=1, le=1000), # gioi han so luong ban ghi tra ve
    db: Session = Depends(get_db),
):
    """GET /api/hives/12/readings/chart?hours=24&limit=100 — tra ve cu -> moi de ve chart."""
    # kiem tra thung ong ton tai
    _get_or_404(db, hive_id)
    # tinh thoi diem gioi han (UTC)
    since = datetime.now(timezone.utc) - timedelta(hours=hours)
    # lay du lieu cam bien tu thoi diem gioi han den hien tai, sap xep moi nhat truoc
    row = db.scalars(                        # chu y: KHAC db.scalar (lay 1 gia tri)
        select(SensorReading)
        .where(SensorReading.hive_id == hive_id, SensorReading.recorded_at >= since)
        .order_by(SensorReading.recorded_at.desc())
        .limit(limit)
    ).all()
    return list(reversed(row))  # dao nguoc de tra ve tu cu -> moi, chart can cu -> moi

# thiet bi gui du lieu cam bien len server
@router.post("", response_model=SensorReadingRead, status_code = 201)
def create_reading(hive_id: int,  data: SensorReadingCreate,
                    db: Session = Depends(get_db)):
    """POST /api/hives/12/readings — thiet bi gui du lieu cam bien len server."""
    _get_or_404(db, hive_id)
    payload = data.model_dump() # lay du lieu tu request body
    when = payload.get("recorded_at") # lay thoi diem do tu request body
    if when is None:
        payload["recorded_at"] =  datetime.now(timezone.utc)
    elif when.tzinfo is None: # .tzinfo la ham kiem tra xem datetime co timezone hay khong
        payload["recorded_at"] = when.replace(tzinfo=timezone.utc)   # client gui naive -> gan UTC
    reading = SensorReading(**payload, hive_id=hive_id)
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading
