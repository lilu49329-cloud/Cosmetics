# Lý thuyết đã sử dụng trong dự án Cosmetics Shop AI

## I. Giới thiệu dự án

### 1. Tổng quan
- **Django Framework:** Nền tảng web Python theo mô hình MTV (Model-Template-View), giúp phát triển nhanh các ứng dụng web, quản lý dữ liệu hiệu quả, bảo mật tốt.
- **Hệ quản trị nội dung (CMS):** Django Admin và Jazzmin hỗ trợ giao diện quản trị hiện đại, dễ tuỳ biến, phù hợp cho quản lý sản phẩm, đơn hàng, khách hàng, thương hiệu, FAQ, khuyến mãi.
- **Thương mại điện tử:** Ứng dụng các mô hình bán hàng trực tuyến, quản lý giỏ hàng, đặt hàng, khuyến mãi, FAQ, hỗ trợ khách hàng qua chatbot.

### 2. Mô hình kinh doanh
- **B2C (Business to Customer):** Website bán lẻ mỹ phẩm trực tiếp cho khách hàng cuối, tập trung vào trải nghiệm người dùng và tự động hóa hỗ trợ.

### 3. Mô hình doanh thu
- **Bán hàng trực tuyến:** Doanh thu chủ yếu từ việc bán sản phẩm qua website, có thể mở rộng thêm các dịch vụ giá trị gia tăng (tư vấn AI, khuyến mãi, quảng cáo...).

### 4. Phạm vi và giới hạn của dự án
- **Phạm vi:** Quản lý sản phẩm, khách hàng, đơn hàng, thương hiệu, khuyến mãi, FAQ, chatbot AI hỗ trợ khách hàng, REST API cho tích hợp.
- **Giới hạn:** Chưa tích hợp thanh toán trực tuyến thực tế, vận chuyển thực tế, các tính năng nâng cao như phân tích dữ liệu lớn, mobile app.

---

## II. Phân tích và thiết kế hệ thống

### 1. Đặc tả yêu cầu phần mềm
- **Phân tích yêu cầu:** Xác định các chức năng chính (CRUD sản phẩm, quản lý đơn hàng, đăng ký/đăng nhập, chatbot AI, quản lý thương hiệu, FAQ, khuyến mãi...).
- **Trải nghiệm người dùng (UX):** Giao diện trực quan, dễ sử dụng, hỗ trợ tìm kiếm, lọc sản phẩm, thao tác nhanh trên admin.

### 2. Thiết kế hệ thống
- **Mô hình MTV (Model-Template-View):** Django tách biệt dữ liệu (Model), giao diện (Template), xử lý logic (View), giúp bảo trì và mở rộng dễ dàng.
- **Thiết kế cơ sở dữ liệu quan hệ:** Sử dụng SQLite (phát triển) hoặc PostgreSQL (triển khai), các bảng chính: Product, Customer, Order, Brand, FAQ, Promotion, ProductImage...
- **RESTful API:** Sử dụng Django REST Framework để xây dựng API cho các chức năng quản lý, xác thực JWT cho bảo mật.
- **Xác thực và phân quyền:** Django Auth, JWT, phân quyền theo nhóm người dùng (admin, staff, khách hàng).
- **Tích hợp AI:** Sử dụng OpenAI API để xây dựng chatbot, ưu tiên trả lời từ dữ liệu FAQ, fallback sang AI khi cần.

---

## III. Thiết kế giao diện website

### 1. Môi trường cài đặt
- **Môi trường ảo (virtual environment):** Sử dụng venv để cô lập môi trường Python, đảm bảo cài đặt package không ảnh hưởng hệ thống.
- **Quản lý package:** Sử dụng requirements.txt để quản lý và cài đặt các thư viện cần thiết.

### 2. Hướng dẫn sử dụng
- **UI/UX:** Giao diện người dùng thân thiện, responsive, dễ thao tác trên cả desktop và mobile.
- **AJAX và JavaScript:** Tăng trải nghiệm động (chatbot AI, cập nhật giỏ hàng, gửi đánh giá sản phẩm không reload trang).
- **Lưu trữ session/localStorage:** Lưu thông tin đăng nhập, lịch sử chat, trạng thái giỏ hàng.
- **Tùy biến giao diện admin:** Jazzmin giúp tuỳ chỉnh giao diện quản trị phù hợp nghiệp vụ.

---

## IV. Kết luận và định hướng mở rộng
- **Mở rộng hệ thống:** Có thể tích hợp thêm thanh toán online (VNPay, Momo...), vận chuyển, AI nâng cao (gợi ý sản phẩm, phân tích hành vi), phát triển mobile app, dashboard phân tích dữ liệu.

---

## V. Tài liệu tham khảo
- Tài liệu chính thức Django, Jazzmin, Django REST Framework, OpenAI API.
- Tài liệu về mô hình thương mại điện tử, quản lý bán hàng, chatbot AI, UX/UI cho web bán hàng.
