from datetime import timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.hive import Hive
from app.models.alert import Alert
from app.schemas.alert import AlertCreate, AlertRead, AlertUpdate

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])

# kiem tra id canh bao co ton tai khong
def _get_or_404(db:Session, alert_id:int) -> Alert:
    alert = db.get(Alert, alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail=f"khong tin thay alert id = {alert_id}")
    return alert


# So canh bao chua doc — day len badge 🔔 tren header
@router.get("/count")
def alert_count(hive_id: int | None = None, db: Session = Depends(get_db)):
    """GET /api/alerts/count — {"unread": n, "bad_unread": m} cho badge bellCount()."""
    stmt = select(func.count()).select_from(Alert).where(Alert.is_read.is_(False))
    if hive_id:
        stmt = stmt.where(Alert.hive_id == hive_id)
    unread = db.scalar(stmt) or 0
    bad_unread = db.scalar(stmt.where(Alert.severity == "bad")) or 0
    return {"unread": unread, "bad_unread": bad_unread}


# Danh sach canh bao — filter nhu filter dashboard
@router.get("", response_model=list[AlertRead])
def list_alerts(
    hive_id: int | None = None,
    severity: str | None = None,
    unread: bool | None = None,
    limit: int = Query(default=50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """GET /api/alerts?hive_id=12&severity=bad&unread=true&limit=20"""
    stmt = select(Alert)
    if hive_id:
        stmt = stmt.where(Alert.hive_id == hive_id)
    if severity:
        stmt = stmt.where(Alert.severity == severity)
    if unread is True:
        stmt = stmt.where(Alert.is_read.is_(False))  # ?unread=true  -> canh bao CHUA doc
    elif unread is False:
        stmt = stmt.where(Alert.is_read.is_(True))   # ?unread=false -> canh bao DA doc
    # canh bao moi nhat len truoc
    return db.scalars(stmt.order_by(Alert.created_at.desc()).limit(limit)).all()


# Lay 1 canh bao
@router.get("/{alert_id}", response_model=AlertRead)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, alert_id)


# Tao canh bao (tu sensor / AI / nguoi dung)
@router.post("", response_model=AlertRead, status_code=201)
def create_alert(data: AlertCreate, db: Session = Depends(get_db)):
    if db.get(Hive, data.hive_id) is None:
        raise HTTPException(status_code=404, detail="hive_id khong ton tai")
    alert = Alert(**data.model_dump())
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


# Cap nhat trang thai: da doc? da xu ly xong luc nao?
@router.put("/{alert_id}", response_model=AlertRead)
def update_alert(alert_id: int, data: AlertUpdate, db: Session = Depends(get_db)):
    alert = _get_or_404(db, alert_id)
    fields = data.model_dump(exclude_unset=True)
    when = fields.get("resolved_at")
    if when is not None and when.tzinfo is None:
        fields["resolved_at"] = when.replace(tzinfo=timezone.utc)  # quy uoc UTC (Cach B)
    for key, value in fields.items():
        setattr(alert, key, value)
    db.commit()
    db.refresh(alert)
    return alert


# Xoa canh bao
@router.delete("/{alert_id}")
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = _get_or_404(db, alert_id)
    db.delete(alert)
    db.commit()
    return {"deleted": alert_id}