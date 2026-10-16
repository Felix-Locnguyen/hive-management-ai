"""
Du lieu mau
"""
from sqlalchemy import select
from datetime import date, datetime, timedelta, timezone

from app.database import SessionLocal
from app.models.hive_record import HiveRecord
from app.models.sensor_reading import SensorReading

from app.models.farm import Farm
from app.models.user import User
from app.models.hive import Hive


# khoi tao gia tri cac thung ong co van de (status= bad)
BAD_HIVES = {
    12: "Mat ong chua",
    44: "Nhiem doc do thuoc",
    58: "Sau benh",
    92: "Thieu mat",
    103: "Nhiem doc do thuoc",
    123: "Mat ong chua"
}

# khoi tao gia tri cac thung can theo doi (status= watch)
WATCH_HIVES = [7, 21, 33, 55, 67, 71, 88, 97, 110, 119]
WATCH_ISSUES = ["Cần kiểm tra mật độ", "Theo dõi nguy cơ đóng tổ", "Kiểm tra tổ chúa định kỳ"]

def _zone(i:int) -> str: # i : index
    "Phan khu theo dashboard: A=32, B=30, C=34, D=32"
    if i <= 32:
        return "A"
    if i <= 62:
        return "B"
    if i <= 96:
        return "C"
    return "D"


# khoi tao 10 ghi chu cho thung ong v12 

RECORDS_V12 = [
    (date(2026, 10, 5), "Kiểm tra tổng quát", "Đàn ổn định, chúa đẻ tốt, khung cầu sạch", "Anh Hùng"),
    (date(2026, 10, 3), "Cho ăn", "1 lít siro đường 1:1", "Chị Lan"),
    (date(2026, 9, 28), "Xử lý bệnh", "Mật ong chua — khoanh vùng, thay khung cầu mới", "Anh Hùng"),
    (date(2026, 9, 25), "Kiểm tra tổng quát", "Phát hiện mật lên men chua ở khung giữa", "Chị Lan"),
    (date(2026, 9, 20), "Thay khung cầu", "Thay 2 khung cầu mới", "Anh Hùng"),
    (date(2026, 9, 14), "Xử lý bệnh", "Acid oxalic, liều chuẩn chống varroa", "Chị Lan"),
    (date(2026, 9, 8), "Cho ăn", "0,5 lít siro đường 1:1", "Anh Hùng"),
    (date(2026, 9, 2), "Kiểm tra tổng quát", "Vệ sinh đáy thùng, dọn xác ong", "Chị Lan"),
    (date(2026, 8, 26), "Kiểm tra tổng quát", "Đàn ổn định, tổ phát triển tốt", "Anh Hùng"),
    (date(2026, 8, 19), "Thu hoạch", "3,4 kg mật", "Anh Hùng"),
]







def seed():
    db = SessionLocal()
    try:
        # 1. Hives — idempotent: da co thi bo qua phan nay
        if db.scalars(select(Hive)).first():
            print("DB da co hives — bo qua seed hives.")
        else:
            if not db.scalars(select(User)).first():
                admin = User(name="Quản trị viên", email="admin@vietbee.vn", phone="0999555888", role="admin")
                member = User(name="Anh Hùng", email="hung@vietbee.vn", phone="0912345678", role="member")
                db.add_all([admin, member])
                db.flush()

            farm = db.scalars(select(Farm)).first()
            if farm is None:
                farm = Farm(
                    name="Trại ong Long Khánh",
                    address="Long Khánh, Đồng Nai",
                    established=date(2019, 3, 1),
                    owner_id=db.scalars(select(User).where(User.role == "admin")).first().id,
                )
                db.add(farm)
                db.flush()

            hives = []
            for i in range(1, 129):
                if i in BAD_HIVES:
                    status, issue = "bad", BAD_HIVES[i]
                elif i in WATCH_HIVES:
                    status, issue = "watch", WATCH_ISSUES[i % len(WATCH_ISSUES)]
                else:
                    status, issue = "ok", ""
                hives.append(Hive(
                    farm_id=farm.id,
                    code=f"V{i}",
                    name=f"{'Ong ngoại' if i % 3 == 0 else 'Ong nội'} {i:02d}",
                    zone=_zone(i),
                    status=status,
                    issue=issue,
                    queen_year=2021 + (i % 5),
                    queen_source="Nhập giống" if i % 4 == 0 else "Tại chỗ",
                    last_check=date(2026, 9, (i % 28) + 1),
                ))
            db.add_all(hives)
            db.commit()
            print("Seed OK: 2 user + 1 farm + 128 hive")

        # 2. Lich su cham soc — guard rieng
        if db.scalars(select(HiveRecord)).first():
            print("DB da co hive_records — bo qua seed records.")
        else:
            hive = db.scalars(select(Hive).where(Hive.code == "V12")).first()
            if hive is None:
                print("Khong tim thay hive V12 — bo qua seed records.")
            else:
                db.add_all([
                    HiveRecord(hive_id=hive.id, checked_at=d, record_type=t, note=n, inspector=w)
                    for d, t, n, w in RECORDS_V12
                ])
                db.commit()
                print("Seed OK: 10 ban ghi nhan cho V12")

        # 3 Du lieu cam bien (gia dinh cho thung v12)
        if db.scalars(select(SensorReading)).first():
            print("DB da co sensor_readings — bo qua seed sensor data.")
        else:
            hive = db.scalars(
                select(Hive).where(Hive.code == "V12")
            ).first()
            if hive is None:
                print("khong tim thay hive v12 - bo qua seed readings")
            else:
                now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0) 
                readings = []
                for i in range(24):
                    readings.append(SensorReading(
                        hive_id = hive.id,
                        recorded_at = now - timedelta(hours=23-i),
                        temperature=round(33.0 + i * 0.12, 1),  # tang dan -> 35.8 (khop hive V12 status=bad)
                        humidity=round(62 + i * 0.7, 1),        # tang dan -> 78.1
                        sound_level=round(55 + i * 0.8, 1),     # ong dong -> am thanh to hon
                        battery=95 - i // 3,                    # pin giam dan
                        ))
        db.add_all(readings)
        db.commit()
        db.refresh(hive)
        print("Seed OK: 24 sensor readings cho V12")
    finally:
        db.close()


if __name__ == "__main__":
    seed()