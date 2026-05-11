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


## Phân loại file theo mô hình MVT (Django)

### 1. Model (Quản lý dữ liệu, logic nghiệp vụ)
- `products/models.py`: Định nghĩa các bảng dữ liệu chính như Product, Brand, Order, Customer, Review, Promotion, ProductImage, FAQ...
- `products/models/` (nếu có): Các model phụ hoặc mở rộng.
- `products/migrations/`: Lưu trữ các file migration cho database.
- `cosmetic_shop/models/` (nếu có): Các model mở rộng hoặc dùng chung cho toàn dự án.
- `db.sqlite3`: File database SQLite (mặc định).
- `stores_backup.json`, `products_backup.csv`, `productimage_backup.csv`: File dữ liệu backup/phục hồi liên quan đến model.

### 2. View (Xử lý logic, điều hướng dữ liệu)
- `products/views.py`: Xử lý các request/response, truy vấn dữ liệu, trả về template hoặc JSON.
- `products/admin.py`: Tùy chỉnh giao diện quản trị Django admin.
- `products/chatbot_api.py`: Xử lý API chatbot, giao tiếp với AI.
- `products/api.py`: Xử lý các API khác (nếu có).
- `products/context_processors.py`: Bổ sung context cho template.
- `products/forms.py`: Định nghĩa các form xử lý dữ liệu người dùng.
- `products/password_reset_views.py`: Xử lý logic quên mật khẩu.
- `products/cart.py`: Xử lý logic giỏ hàng.
- `products/tasks.py`: Định nghĩa các tác vụ nền (background tasks).
- `products/signals.py`: Xử lý các tín hiệu (signals) trong Django.
- `products/tests.py`: Các test case cho view và logic nghiệp vụ.
- `ai_service/main.py`: Tích hợp AI, xử lý logic liên quan đến OpenAI.
- `cosmetic_shop/views.py` (nếu có): View tổng hợp hoặc dùng chung.
- `productListUrlPatterns.py`: Định nghĩa các url patterns cho sản phẩm (nếu có).

### 3. Template (Giao diện người dùng)
- `templates/`: Thư mục chứa các file HTML cho toàn bộ dự án.
- `templates/admin/`: Giao diện quản trị (admin dashboard, quản lý sản phẩm, thương hiệu, đơn hàng...)
- `templates/products/`: Giao diện chi tiết, danh sách, chỉnh sửa sản phẩm, thêm/sửa/xóa sản phẩm.
- `templates/data_deletion.html`: Trang xóa dữ liệu người dùng.
- `templates/privacy_policy.html`: Trang chính sách bảo mật.
- `product_list_template.html`: Giao diện danh sách sản phẩm (có thể dùng chung hoặc riêng ngoài thư mục templates).
- `templates/products/` có thể chứa các file như: `product_detail.html`, `product_form.html`, `product_confirm_delete.html`, `product_list.html`...
- `templates/admin/` có thể chứa: `base_site.html`, `login.html`, `dashboard.html`, ...
- Các file HTML khác: `templates/faq.html`, `templates/promotion.html`, `templates/login.html`, `templates/register.html`, `templates/cart.html`, `templates/checkout.html`, ...
- Các template cho các chức năng: FAQ, khuyến mãi, đăng nhập, đăng ký, giỏ hàng, thanh toán, đổi mật khẩu, xác nhận email, v.v.

### 4. Các thành phần hỗ trợ khác
- `cosmetic_shop/settings.py`: Cấu hình toàn bộ dự án Django.
- `cosmetic_shop/urls.py`, `products/urls.py`: Định tuyến URL cho toàn bộ dự án và từng app.
- `productListUrlPatterns.py`: Định nghĩa url patterns cho sản phẩm (nếu có).
- `manage.py`: Script quản lý dự án Django.
- `requirements.txt`: Danh sách package cần cài đặt.
- `Procfile`: Cấu hình deploy trên Heroku hoặc nền tảng cloud khác.
- `static/`, `staticfiles/`: Chứa file tĩnh (CSS, JS, hình ảnh).
- `media/`: Lưu trữ hình ảnh upload (sản phẩm, avatar, banner, ...).
- Các script hỗ trợ: `activate_virtual_environment.bat`, `ActivateVirtualEnvironment.ps1`, `virtual_environment_activation.sh`, `run_project.ps1`, `SetExecutionPolicy.ps1`, ...
- `database_management_script.sql`: Script quản lý database.
- `README.md`, `ly_thuyet_da_dung.md`, `alter_fields_to_text.py`, `auto_fill_products.py`, `import_makeup_data.py`, `import_product_images.py`, `delete_bad_brands.py`, `delete_bad_products.py`, `restore_flash_sale_products.py`, `update_name_product.py`, `translate_product_descriptions.py`: Các script, tài liệu, công cụ hỗ trợ quản trị, nhập/xuất dữ liệu, xử lý dữ liệu.

---

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