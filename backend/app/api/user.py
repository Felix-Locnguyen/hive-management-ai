from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/api/users", tags=["Users"])

# Truong hop loi khong tim thay api
def _get_or_404(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"khong tim thay user i= {user_id}")
    return user

# lay tat ca danh sach nguoi dung
@router.get("", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    """GET /api/users — danh sách tất cả user."""
    return db.scalars(select(User).order_by(User.id)).all()

# lay thong tin nguoi dung 
@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get /api/users/1"""
    return _get_or_404(db,user_id)


@router.post("", response_model=UserRead, status_code = 201) # ma 201: client gui yeu cau va tao thanh cong
def create_user(data: UserCreate, db: Session= Depends(get_db)):
    '''POST /api/users - tao user moi (validate emial trung lap)'''
    
    # kiem tra email co trung lap khong
    exists = db.scalar(
        select(User).
        where(User.email == data.email)
        ).first()
    if exists:
        raise HTTPException(status_code=409, detail="email da ton tai")

    # Them du lieu nguoi dung vao data
    user = User(**data.model_dump()) # ep schema sang ORM object
    db.add(user)
    db.commit()
    db.refresh(user)
    return user 



@router.put("/{user_id}", response_model= UserRead)
def update_user(user_id: int, data:UserUpdate, db: Session = Depends(get_db)):
    '''PUT /api/users/1 - chi update cac field co gui len'''
    # kiem tra id nguoi dung
    user = _get_or_404(db, user_id)

    # lay cac du lieu nguoi dung thay doi va gui len 
    fields = data.model_dump(exclude_unset= True)

    if "email" in fields:
        other = db.scalars(
            select(User).where(User.email == fields["email"],
                                User.id != user_id)
            ).first()

    # truong hop nguoi dung thay doi email trung voi email hien tai    
        if other:
            raise HTTPException(status_code=409, detail="Email da toan tai")
    for key, value in fields.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user



# xoa thong tin nguoi dung
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """DELETE /api/users/1"""
    user = _get_or_404(db, user_id)
    db.delete(user)
    db.commit()
    return {"deleted": user_id}
