# Cosmetics Shop AI - Dự án quản lý & bán hàng mỹ phẩm tích hợp Chatbot AI

## Giới thiệu

Dự án xây dựng hệ thống quản lý và bán hàng mỹ phẩm với giao diện quản trị hiện đại (Jazzmin), tích hợp chatbot AI (OpenAI) hỗ trợ khách hàng, quản lý sản phẩm, đơn hàng, thương hiệu, FAQ, khuyến mãi, v.v.

## Tính năng nổi bật

- Quản lý sản phẩm, thương hiệu, khách hàng, đơn hàng, giỏ hàng, khuyến mãi, FAQ.
- Chatbot AI tự động trả lời khách hàng, ưu tiên dữ liệu FAQ, fallback sang OpenAI nếu không có câu trả lời phù hợp.
- Giao diện admin đẹp, dễ dùng nhờ Jazzmin.
- Hỗ trợ REST API, xác thực JWT, APScheduler, widget-tweaks.
- Lưu trữ hình ảnh sản phẩm, avatar, banner khuyến mãi.
- Đa dạng script hỗ trợ môi trường ảo, quản lý database, khởi động nhanh.

## Cấu trúc thư mục

- `cosmetic_shop/`: Cấu hình Django (settings, urls, wsgi/asgi).
- `products/`: Models, views, forms, admin, migrations, các chức năng chính.
- `ai_service/`: Tích hợp AI (OpenAI API).
- `templates/`: Giao diện HTML cho admin, sản phẩm, đơn hàng, v.v.
- `media/`: Lưu trữ hình ảnh sản phẩm, avatar, banner.
- `static/`, `staticfiles/`: File tĩnh (CSS, JS, hình ảnh).
- Các file hỗ trợ: `manage.py`, `requirements.txt`, `Procfile`, `db.sqlite3`, `database_management_script.sql`, `data.json`.

## Hướng dẫn cài đặt & sử dụng chi tiết

### 1. Cài đặt Python và pip
- Tải Python >= 3.10 tại https://www.python.org/downloads/
- Chọn tùy chọn "Add Python to PATH" khi cài đặt.
- Kiểm tra cài đặt:
  ```sh
  python --version
  pip --version
  ```

### 2. Tạo và kích hoạt môi trường ảo
- **Windows:**
  ```sh
  python -m venv venv
  .\venv\Scripts\activate
  # Hoặc chạy activate_virtual_environment.bat hoặc ActivateVirtualEnvironment.ps1
  ```
- **Linux/Mac:**
  ```sh
  python3 -m venv venv
  source venv/bin/activate
  # Hoặc chạy virtual_environment_activation.sh
  ```

### 3. Cài đặt package
```sh
pip install -r requirements.txt
```

### 4. Thiết lập biến môi trường OpenAI (nếu dùng AI thật)
- **Windows:**
  ```sh
  set OPENAI_API_KEY=sk-xxxxxx
  ```
- **Linux/Mac:**
  ```sh
  export OPENAI_API_KEY=sk-xxxxxx
  ```

### 5. Chạy migrate database
```sh
python manage.py migrate
```

### 6. Tạo tài khoản admin
```sh
python manage.py createsuperuser
```

### 7. Khởi động server
```sh
python manage.py runserver
```

### 8. Truy cập admin
- Mở trình duyệt: http://localhost:8000/admin
- Đăng nhập bằng tài khoản admin vừa tạo

### 9. Nhập dữ liệu mẫu
- Vào admin, thêm FAQ, thương hiệu, sản phẩm, banner, khuyến mãi, v.v.

## Các script hỗ trợ

- Kích hoạt môi trường ảo: `activate_virtual_environment.bat`, `ActivateVirtualEnvironment.ps1`, `virtual_environment_activation.sh`
- Thiết lập quyền thực thi PowerShell: `SetExecutionPolicy.ps1`
- Quản lý database: `database_management_script.sql`

## Các package sử dụng

- Django, Pillow, whitenoise, dj-database-url, psycopg2-binary, gunicorn, sqlparse, asgiref, pytz
- django-jazzmin, django-allauth, django-widget-tweaks, django-apscheduler
- djangorestframework, djangorestframework-simplejwt, requests, cryptography
- Các package Python chuẩn: os, json, pathlib, typing

## Database

- Mặc định dùng SQLite (`db.sqlite3`), có thể chuyển sang PostgreSQL qua cấu hình `dj-database-url`.

## Lưu ý triển khai

- Đảm bảo đã cài đặt đầy đủ package trong `requirements.txt`.
- Nếu gặp lỗi quyền thực thi script trên Windows, chạy `SetExecutionPolicy.ps1`.
- Đọc kỹ README trước khi deploy lên server thật.
- Để tùy chỉnh giao diện admin, xem tài liệu Jazzmin: https://django-jazzmin.readthedocs.io/

---

Mọi thắc mắc về chatbot AI, liên hệ admin dự án.