from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    # Cấu hình nguồn đọc: lấy biến từ file .env với bảng mã utf-8
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Các giá trị mặc định của ứng dụng (nếu không tìm thấy trong .env)
    app_name: str = "VietBee API"
    app_version: str = "1.0.0"
    debug: bool = False
    database_url: str = "sqlite:///./vietbee.db"


# Khởi tạo một instance duy nhất (Singleton) để dùng chung cho toàn bộ app
settings = Settings()