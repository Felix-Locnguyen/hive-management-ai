```text
hive-manage-ai/
│
├── .gitignore
├── README.md
├── docker-compose.yml             # Triển khai backend, frontend, database
│
├── firmware/                      # Mã nguồn phần cứng / IoT (ESP32 / Camera stream)
│   ├── platformio.ini (hoặc .ino)
│   ├── src/
│   │   ├── main.cpp               # Logic thu thập cảm biến, stream RTSP/HTTP
│   │   ├── wifi_manager.cpp
│   │   └── sensors.cpp            # Đọc DHT22/DS18B20 (nhiệt độ, ẩm)
│   └── include/
│
├── ai_engine/                     # Pipeline AI & Thị giác máy tính
│   ├── weights/                   # File trọng số (yolov8n.pt, best.onnx)
│   ├── data/                      # Dataset mẫu (train/val/test/yaml)
│   ├── notebooks/                 # Jupyter notebook thực nghiệm mô hình
│   ├── src/
│   │   ├── detector.py            # Load model, inference (phát hiện ong, thiên địch)
│   │   ├── tracker.py             # Đếm số lượt ra/vào cửa tổ (ByteTrack / BoT-SORT)
│   │   ├── stream_reader.py       # Đọc feed camera (OpenCV / RTSP)
│   │   └── alert_rules.py         # Logic kích hoạt cảnh báo (ong bắp cày, mật độ sụt)
│   ├── requirements.txt
│   └── Dockerfile
│
├── backend/                       # Web API & Xử lý thời gian thực (Flask / FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py              # Biến môi trường, database URL
│   │   ├── models/                # ORM schema (Thùng ong, Dữ liệu cảm biến, Cảnh báo)
│   │   │   ├── hive.py
│   │   │   ├── log.py
│   │   │   └── alert.py
│   │   ├── api/                   # REST API routes
│   │   │   ├── hives.py           # CRUD thông tin đàn/thùng
│   │   │   ├── logs.py            # Lịch sử cho ăn, tách đàn, thu mật
│   │   │   └── stream.py          # WebSocket / SSE gửi tọa độ bbox & video
│   │   ├── services/              # Kết nối với AI Engine và gửi thông báo
│   │   │   ├── ai_service.py
│   │   │   └── notifier.py        # Gửi Telegram / Zalo / Webhook khi có mối nguy
│   │   └── database.py
│   ├── run.py
│   ├── requirements.txt
│   └── Dockerfile
│
└── frontend/                      # Web Dashboard quản lý (React / Next.js / HTML-JS)
    ├── package.json
    ├── public/
    └── src/
        ├── assets/
        ├── components/
        │   ├── VideoPlayer.jsx    # Màn hình xem camera trực tiếp kèm bbox
        │   ├── HiveCard.jsx       # Thẻ tóm tắt trạng thái từng thùng
        │   ├── MetricChart.jsx    # Biểu đồ tần suất bay, nhiệt độ/độ ẩm
        │   └── AlertBanner.jsx    # Cảnh báo tức thì (ong bắp cày, chuồn chuồn...)
        ├── pages/
        │   ├── Dashboard.jsx
        │   ├── HiveDetail.jsx
        │   └── LogBook.jsx        # Sổ tay nhật ký chăm sóc
        ├── services/              # Gọi API backend, socket.io
        └── App.jsx
```