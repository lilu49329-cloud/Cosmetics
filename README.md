
# Chatbot AI Cosmetics
## Giao diện quản trị hiện đại với Jazzmin

1. Đã cài đặt sẵn Jazzmin trong dự án (xem requirements.txt và INSTALLED_APPS trong settings.py).
2. Giao diện admin sẽ tự động đẹp, hiện đại khi truy cập /admin.
3. Nếu muốn tùy chỉnh thêm, xem tài liệu: https://django-jazzmin.readthedocs.io/


## Hướng dẫn cấu hình AI thật (OpenAI)

1. Đăng ký tài khoản OpenAI và lấy API key tại https://platform.openai.com/api-keys
2. Thêm biến môi trường vào hệ điều hành hoặc file `.env` (nếu dùng):

	```sh
	set OPENAI_API_KEY=sk-xxxxxx
	```
	(Windows: dùng lệnh trên trong PowerShell/cmd, hoặc thêm vào cấu hình môi trường)

3. Khởi động lại server Django để nhận biến môi trường.

## Hướng dẫn nhập dữ liệu FAQ, tags, thương hiệu

### FAQ:
Vào admin Django, thêm các câu hỏi thường gặp (FAQ), ví dụ:

| Question                                 | Answer                                    | Tags                        | is_active |
|-------------------------------------------|-------------------------------------------|-----------------------------|-----------|
| Làm sao để đặt hàng?                      | Bạn chỉ cần chọn sản phẩm và nhấn Mua ngay| đặt hàng, mua, order        |   ✓       |
| Shop có khuyến mãi gì hôm nay?            | Shop luôn có ưu đãi, xem tại trang khuyến mãi| khuyến mãi, giảm giá    |   ✓       |
| Sản phẩm A có phù hợp da nhạy cảm không?  | Sản phẩm A phù hợp cho da nhạy cảm nhé!   | da nhạy cảm, sensitive, A   |   ✓       |

### Thương hiệu:
Vào admin Django, thêm các Brand (thương hiệu) như: L'Oreal, Innisfree, The Face Shop...

### Gợi ý:
- Nên nhập tags liên quan, tên thương hiệu vào tags của FAQ để chatbot nhận diện tốt hơn.
- Nếu không có câu trả lời phù hợp, chatbot sẽ tự động hỏi AI thật (OpenAI) để trả lời khách hàng.

---
Mọi thắc mắc về chatbot AI, liên hệ admin dự án.
# Cosmetic