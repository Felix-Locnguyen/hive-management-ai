from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.farm import Farm
from app.models.hive import Hive
from app.schemas.hive import HiveCreate, HiveRead, HiveUpdate


router = APIRouter(prefix="/api/hives", tags=["Hives"])

# kiem tra id thung co ton tai khong
def _get_or_404(db: Session, hive_id:int):
    hive = db.get(Hive, hive_id)
    if not hive:
        raise HTTPException(status_code=404, detail=f"Khong tin thay hive id = {hive_id}")
    return hive


# Tổng hợp các trạng thái thùng ong để hiển thị lên KPI Dashboard
@router.get("/stats")
def hive_stats(db:Session = Depends(get_db)):
    """GET /api/hives/stats — KPI khớp card '128 thùng' trên dashboard."""
    rows = db.execute(
        select(Hive.status, func.count()).group_by(Hive.status)
    ).all()

    counts = {status: count for status, count in rows}
    return {
        "total": sum(counts.values()),
        "ok": counts.get("ok", 0),
        "watch": counts.get("watch", 0),
        "bad": counts.get("bad", 0),
    }


# API LẤY DANH SÁCH & LỌC DỮ LIỆU (Filtering)
@router.get("", response_model=list[HiveRead])
def list_hives(
    zone: str | None = None,
    status: str | None = None,
    q: str | None = None,
    db: Session = Depends(get_db),
):
    """GET /api/hives?zone=A&status=ok&q=V12 — filter giống hệt filter trên dashboard."""
    stmt = select(Hive)
    if zone:
        stmt = stmt.where(Hive.zone == zone)
    if status:
        stmt = stmt.where(Hive.status == status)
    # Tìm kiếm gần đúng (case-insensitive) theo mã hoặc tên thùng ong
    if q:
        stmt = stmt.where(or_(Hive.code.ilike(f"%{q}%"), Hive.name.ilike(f"%{q}%")))
    return db.scalars(stmt.order_by(Hive.id)).all()


# kiem tra id
@router.get("/{hive_id}", response_model=HiveRead)
def get_hive(hive_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, hive_id)

#khoi tao gia tri cho thung ong 
@router.post("", response_model=HiveRead, status_code=201)
def create_hive(data: HiveCreate, db: Session = Depends(get_db)):
    if db.get(Farm, data.farm_id) is None:
        raise HTTPException(status_code=404, detail="farm_id khong ton tai")
    if db.scalars(select(Hive).where(Hive.code == data.code)).first():
        raise HTTPException(status_code=409, detail="Ma so hive da ton tai")
    hive = Hive(**data.model_dump())
    db.add(hive)
    db.commit()
    db.refresh(hive)
    return hive

# cap nhat thong tin thung ong

@router.put("/{hive_id}", response_model=HiveRead)
def update_hive(hive_id: int, data: HiveUpdate, db: Session = Depends(get_db)):
    hive = _get_or_404(db, hive_id)
    fields = data.model_dump(exclude_unset=True)
    if "code" in fields:
        other = db.scalars(
            select(Hive).where(Hive.code == fields["code"], Hive.id != hive_id)
        ).first()
        if other:
            raise HTTPException(status_code=409, detail="Ma so hive da ton tai")
    for key, value in fields.items():
        setattr(hive,key,value)
    db.commit()
    db.refresh(hive)
    return hive

# xoa thong tin thung ong 

@router.delete("/{hive_id}")
def delete_hive(hive_id: int, db: Session = Depends(get_db)):
    hive = _get_or_404(db, hive_id)
    db.delete(hive)
    db.commit()
    return {"deleted": hive_id}
