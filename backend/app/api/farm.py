from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.farm import Farm
from app.models.user import User
from app.schemas.farm import FarmCreate, FarmRead, FarmUpdate

router = APIRouter(prefix="/api/farms", tags=["Farms"])

# kiem tra su ton tai cua farm id
def _get_or_404(db:Session, farm_id:int) -> Farm:
    farm = db.get(Farm, farm_id)
    if not farm:
        raise HTTPException(status_code= 404, detail=f"Khong tim thay farm id= {farm_id}")
    return farm

# lay thong tin danh sach trang trai
@router.get("", response_model= list[FarmRead])
def list_farms(db: Session = Depends(get_db)):
    return db.scalars(
        select(Farm).order_by(Farm.id)
    ).all()


# lay thong tin trang trai
@router.get("/{farm_id}", response_model=FarmRead)
def get_farm(farm_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, farm_id)


# khoi tao trang trai 
@router.post("", response_model= FarmRead, status_code= 201)
def create_farm(data: FarmCreate, db: Session = Depends(get_db)):

    # Kiểm tra owner_id có tồn tại trong hệ thống hay không
    if data.owner_id is not None and db.get(User, data.owner_id) is None:
        raise HTTPException(status_code=404, detail="owner_id khong ton tai")
    farm = Farm(**data.model_dump())
    db.add(farm)
    db.commit()
    db.refresh(farm)
    return farm


# cap nhat thong tin trang trai
@router.put("/{farm_id}", response_model=FarmRead)
def update_farm(farm_id:int, data: FarmUpdate, db: Session = Depends(get_db)):
    farm = _get_or_404(db, farm_id)
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(farm, key, value)
    db.commit()
    db.refresh(farm)
    return 

# xoa thong tai trang trai
@router.delete("/{farm_id}")
def delete_farm(farm_id: int, db: Session = Depends(get_db)):
    farm = _get_or_404(db, farm_id)
    db.delete(farm)
    db.commit()
    return {"deleted": farm_id}