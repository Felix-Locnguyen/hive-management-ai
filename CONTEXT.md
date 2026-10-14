# 📋 VietBee — Bối cảnh dự án (Context Checkpoint)

> **Cập nhật:** 14/10/2026 · **Trạng thái:** Bước0 ✅ · Bước1 ✅ · **Bước2 ✅ (đã fix8 lỗi + verify thật, server/seed/curl PASS)** · Git: các file backend chờ user commit
> **Mục đích:** tài liệu này để khôi phục toàn bộ bối cảnh khi mở session mới (hoặc bàn giao), tiếp tục đúng chỗ dừng.

---

## 1. Dự án & quy tắc làm việc (bắt buộc tuân thủ)

- **VietBee** — dashboard quản lý trại ong (`frontend/Static/`), backend FastAPI dạy qua dự án.
- **Tiến độ theo phần:** "mỗi phần show code cho tôi code theo khi tôi tiếp tục thì mới được qua phần mới" — show đủ code từng bước trong chat, user gõ theo, chỉ sang bước mới khi user nhắn **"tiếp theo" / "Bước N"**.
- **UI:** tiếng Việt; tiền `186.5M VNĐ`; ngày dd/mm; mobile-first (360/390/412/768/1024/1280); vanilla HTML/CSS/JS — **cấm Tailwind, cấm localStorage**; Chart.js + qrcodejs từ cdnjs.
- **Màu:** xanh/đỏ/hổ cho status; ngoại lệ `--nav-active`, pill `#6BAA75/#E8A93B/#D9695F`, nền pill `#FBEFD5/#B07A12`.
- **Cấm** đổi tên biến/hàm/API cũ; tái dùng filter/sort/search có sẵn khi mở rộng; **user tự git commit** (không commit thay).
- **Không sửa** `ai_engine/`, `firmware/`, `frontend/src/`, `docker-compose.yml`, `.gitignore` (backend/ được user cho phép làm).
- **Mock data chuẩn:** 128 ong = 112🟢/10🟡/6🔴; revenue Σ186.5M; expense Σ72.4M; profit 114.1M; zone A32/B30/C34/D32; trại "Trại ong Long Khánh, Đồng Nai · thành lập 03/2019".
- **Mapping dashboard ↔ bảng:** `HIVES↔hives`, `ITEMS↔items`, `INV_LOG↔stock_txns`, `TXNS↔finance_txns`, `h.hist↔hive_records`, `h.issue/status↔alerts`, `series()↔sensor_readings`.

---

## 2. Frontend — HOÀN THÀNH (đã commit)

- Tách3 file: `frontend/Static/Index.html` (HTML-only) + `Style.css` + `App.js` (App.js cuối `<body>`, không defer); CDN Chart.js/qrcodejs giữ nguyên.
- Test harness `/tmp/opencode/domtest/` (boot.js inline CSS+JS vào HTML trước khi JSDOM; 7 suite, **199 assert pass**): invcat96 · history19 · overlays22 · routes2 11 · zonefilter2 13 · account2b 14 · record24.
- Tính năng đã làm: card kho (INV_PAGE=4, ngưỡng/threshold, menu ⋯), form kho có category + tạo mới `nextCode()`→VT049, form record có `#rStatus` sync `h.issue/h.mins` + history, nav/overlay/route/account tests.
- ⚠️ `frontend/package.json` = 0byte → `node --check` fail (`ERR_INVALID_PACKAGE_CONFIG`) — copy sang `/tmp` để check cú pháp.
- Git: user tự commit (HEAD gần nhất `7f2c024 update backend` trước khi fix Bước2).

---

## 3. Backend — trạng thái các bước

Cấu trúc (README quy định): FastAPI + SQLAlchemy2.0 + SQLite (`vietbee.db`) + pydantic-settings; vào lệnh từ `backend/`.

```
backend/
├── requirement.txt        ← tên LẺ (chuẩn là requirements.txt) — user giữ
├── .env                   ← APP_NAME/APP_VERSION/DEBUG/DATABASE_URL (không commit)
├── run.py                 ← uvicorn.run("app.main:app", port=8000, reload=True)
├── seed.py                ← idempotent: guard theo Hive; users/farm chỉ tạo nếu thiếu
├── vietbee.db             ← ĐÃ seed:2 users +1 farm +128 hives — ⚠️ VẪN GIT TRACK, .gitignore thiếu *.db
└── app/
    ├── __init__.py        ← 0byte cố ý
    ├── config.py          ← Settings (pydantic-settings, env_file=".env") ✅
    ├── database.py        ← engine/SessionLocal/Base(DeclarativeBase)/get_db ✅
    ├── main.py            ← create_all + include users,farms,hives ✅
    ├── models/{user,farm,hive}.py
    ├── schemas/{user,farm,hive}.py     ← Pydantic Create/Update/Read (from_attributes)
    ├── api/{users,farms,hives}.py       ← CRUD pattern, prefix /api/*
    └── services/          ← 0byte (ai_service, notifier) — chưa dùng
```

### Bước0 — Khung app ✅
User chạy thành công `GET /` → `{"app":"VietBee API","version":"1.0.0","docs":"/docs"}`.

### Bước1 — Users + Farms ✅
- Pattern đã dạy: **Model (SQLAlchemy Mapped/mapped_column) → Schema (Pydantic) → Router (5 method REST) → Seed**.
-8 lỗi đầu tiên user đã tự sửa hết (dattime, `__table__`→`__tablename__`, tên file users/farms, run.py location, created_at, `db.scalar().first()`, `return farm`, `date()` trong seed).
- Kiến thức: `model_dump(exclude_unset=True)` cho update, `_get_or_404`, 409 email trùng, `server_default=func.now()`, `from_attributes`.
- ⚠️ `UserRead` **cố ý thiếu `email`** (user giữ nguyên) → API không trả email.

### Bước2 — Bảng Hives ✅ HOÀN THÀNH (14/10)
- Files: `models/hive.py`, `schemas/hive.py`, `api/hives.py`, `seed.py` (viết lại, seed128 ong), `main.py` nối router hives.
- **8 lỗi runtime đã fix** (user gõ có lỗi, mình tìm + sửa):
 1-2. `models/hive.py`: `hive_year/hive_source` (sai tên, `String(200)` cho int) → `queen_year: Mapped[int|None](Integer, nullable)` + `queen_source` — khớp schema/seed/router.
 3. (hệ quả1-2: trước đó mọi endpoint hives500 + seed TypeError)
 4. `api/hives.py`: `if not Hive:` (kiểm tra class,404 không kích hoạt) → `if not hive:`
 5. route `"/start"` → `"/stats"`
 6. `.all()` trong ngoặc `db.execute(...)` → `db.execute(...).all()`
 7. `{status: counts ...}` NameError → `{status: count ...}`
 8. `db.scalars(select(...).first())` → `db.scalars(select(...)).first()`
- Nhỏ: `issue` thêm `default=""`; seed `BAD_HIVES` không dấu tiếng Việt (user tự chọn — WATCH_ISSUES có dấu).
- **Verify thật (server uvicorn + seed +15 HTTP test): PASS0 lỗi** — `stats {"total":128,"ok":112,"watch":10,"bad":6}` · zone A=32 · bad=6 có issue · q=V12→10 row · GET /1 có `queen_year/queen_source/last_check` · GET /9999→404 · POST trùng→409 · POST V129→201 (id129) · PUT status→200 · PUT mã trùng→409 · DELETE→200 · stats cuối về128/112/10/6 · users=2 · farms/1="Trại ong Long Khánh"/2019-03-01.

---

## 4. Pattern đã dạy (mẫu lặp lại cho bảng sau)

1. **Model:** `Mapped[...]` + `mapped_column`, `__tablename__`, FK `index=True`, `server_default=func.now()`.
2. **Schema:** Create (bắt buộc) / Update (optional + `pattern`/`ge`/`le`, gom regex vào hằng) / Read (đóng khung output, `model_config from_attributes`).
3. **Router:** `_get_or_404` · GET list (filter query param `zone/status/q` + `or_`/`ilike`) · GET/1 · POST (validate FK + unique → 201/409) · PUT (`exclude_unset` + check unique khi đổi khóa) · DELETE · **route `/stats` phải khai TRƯỚC `/{id}`** · `group_by` + `func.count()`.
4. **Seed idempotent:** guard `if select(Hive).first(): return`, users/farm conditional, `db.flush()` để lấy id, `add_all` hàng loạt, chạy **sau** server (vì `create_all` nằm trong `main.py`).
5. **Bài học code thật:** luôn verify runtime —8 lỗi Bước2 (sai tên field model/schema, kiểm tra class thay vì biến, sai vị trí method, sai biến trong dict comp) đều parse OK nhưng crash khi chạy.

---

## 5. Việc cần làm tiếp (khi mở session mới)

1. **Bước3 — HiveRecords** (lịch sử `h.hist`, "25/10 · kiểm tra tổng quát…"): model `hive_records` (hive_id FK, checked_at, note, inspector…) → schema → router `GET /api/hives/{id}/records` + POST → seed ~10 bản ghi cho V12 khớp dashboard. **Chờ user nhắn "tiếp theo".**
2. Roadmap còn lại: **Bước4** IoT/Sensors (`sensor_readings`: temp/hum/mass series) · **Bước5** Alerts (`alerts` ↔ `h.issue`) · **Bước6** Kho Items + StockTxns (INV_PAGE=4, ngưỡng) · **Bước7** Finance (TXNS Σ186.5M/72.4M) · **Bước8** Auth JWT (`password_hash`, role, đăng ký/đăng nhập).
3. **Chặng2:** Camera/AI/stream/docker + nối dashboard fetch API thật (thay mock `HIVES/ITEMS/TXNS`).

## 6. Việc dọn dẹp (user tự làm, mình nhắc)

- [ ] Thêm `*.db` vào `.gitignore` + `git rm --cached backend/vietbee.db` (giờ DB đã có dữ liệu thật, sẽ commit nhầm binary).
- [ ] Commit các fix Bước2 (user tự commit).
- [ ] (tuỳ) `requirement.txt` → `requirements.txt`; cân nhắc `email` vào `UserRead`.

## 7. Ghi chú môi trường

- **Mode:** đã thoát plan mode (14/10) → được ghi file project bình thường; MD này tồn tại ở plan dir + bản copy `CONTEXT.md` ở root.
- `/tmp` bị wipe giữa session (đã 3 lần) → test harness phải dựng lại (`npm i jsdom`; venv: `python3 -m venv .venv && pip install sqlalchemy`); venv smoke-test sẵn có tại `/tmp/opencode/apitest/.venv` (nếu chưa wipe).
- Không có browser trong env → kiểm tra visual là việc của user.
- Python env: 3.14 (pyc `cpython-314`); deps global: fastapi 0.143 / sqlalchemy 2.1.4 / pydantic 2.14 (`requirement.txt` dùng `>=` không ghim).
- User hay gõ lại/sửa file giữa chừng → **luôn đọc lại file + `git status` trước khi kết luận**.
- Verify backend độc lập với frontend: `cd backend && python run.py` (port 8000) — test script mẫu dùng port 8765 để tránh đụng server thật.
