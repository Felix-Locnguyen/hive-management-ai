"""
Du lieu mau
"""
from sqlalchemy import select
from datetime import date

from app.database import SessionLocal
from app.models.farm import Farm
from app.models.user import User

def seed():
    db = SessionLocal()
    try:
        if db.scalars(select(User)).first():
            print("DB da co du lieu -bo qua seed")
            return
        admin = User(name="Quan tri vien",
                     email="admin@vietbee.vn",
                     phone="0999555888",
                     role= "admin",    
                    )
        member = User(name="Anh Hùng",
                      email="hung@vietbee.vn",
                      phone="0912345678",
                      role="member")
        db.add_all([admin, member])
        db.flush() # INSERT tạm để có id (chưa commit)


        # them thong tin farm
        db.add(Farm(
            name="Trại ong Ben Tre",
            address="Ben Tre, An Khanh",
            established=date(2019, 3, 1),               # dashboard: thành lập 03/2019
            owner_id=admin.id,
        ))
        db.commit()
        print("Seed OK:2 user +1 farm")
    finally:
        db.close()

if __name__ == "__main__":
    seed()