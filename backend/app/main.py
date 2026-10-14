from fastapi import FastAPI

from app.api import farms, users, hives
from app.config import settings
from app.database import Base, engine


# Quét tất cả các model đã kế thừa từ Base và tự động tạo bảng tương ứng trong CSDL
# (Ở giai đoạn đầu chưa có model nào được viết, dòng này chạy qua nhưng chưa tạo bảng gì)
Base.metadata.create_all(bind=engine)

# Khởi tạo đối tượng ứng dụng FastAPI chính, lấy thông tin cấu hình trực tiếp từ tệp .env
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

app.include_router(users.router)
app.include_router(farms.router)
app.include_router(hives.router)  

# Định nghĩa API Endpoint cho đường dẫn gốc (Root)
@app.get("/", tags=["Health"])
def root():
    # Trả về thông tin tổng quan của ứng dụng dưới dạng JSON
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
    }


# Định nghĩa API Endpoint dùng để kiểm tra trạng thái sống/chết của server (Health Check)
@app.get("/healthz", tags=["Health"])
def healthz():
    # Trả về trạng thái "ok" để các hệ thống giám sát server (Docker, K8s) nhận biết app đang chạy tốt
    return {"status": "ok"}