import os
import re
import django

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmetic_shop.settings')
django.setup()

from products.models import Product

LOG_FILE = r"C:\Users\admin\Downloads\Cosmetics\deleted_translation_log.txt"

# 🧠 Kiểm tra lỗi dịch
def is_wrong_translation(name):
    n = (name or "").lower().strip()

    # Lip liner mà dịch thành kẻ mắt
    if "lip liner" in n and "kẻ mắt" in n:
        return True

    # Lip nhưng không bắt đầu bằng son/môi
    if any(x in n for x in ["lipstick", "lip cream", "lip tint", "lip colour", "lip color", "lip gloss", "lippie"]) \
       and not (n.startswith("son") or n.startswith("môi")):
        return True

    # Bộ sưu tập sai vị trí
    if any(x in n for x in ["collection", "palette"]) and n.startswith("bộ"):
        return True

    # Màu sắc dư
    if re.search(r"(black|brown|red|pink|very)\s*$", n):
        return True

    # Kí tự lỗi
    if n.endswith("+") or n.endswith("&"):
        return True

    # Mascara không bắt đầu bằng Chuốt Mi
    if "mascara" in n and not n.startswith("chuốt mi"):
        return True

    # Eyeliner không bắt đầu bằng Kẻ Mắt
    if "eyeliner" in n and not n.startswith("kẻ mắt"):
        return True

    # Lippie bị dịch thành phấn phủ
    if "lippie" in n and n.startswith("phấn phủ"):
        return True

    return False

# ✏️ Xử lý sửa hoặc xóa 1 sản phẩm
def handle_product(product, deleted_log, fixed_log):
    name = product.name or ""
    print("--------------------------------------------------")
    print(f"📌 Tên hiện tại: {name}")
    print("👉 [y] Xóa | [s] Sửa tên | [n] Bỏ qua")
    action = input("Lựa chọn: ").strip().lower()

    if action == "y":
        product.delete()
        deleted_log.append(f"❌ Xóa: {name}")
        print("✅ Đã xóa.\n")
        return "deleted"

    elif action == "s":
        new_name = input("✍️  Nhập tên mới: ").strip()
        if new_name:
            product.name = new_name
            product.save()
            fixed_log.append(f"✏️ Sửa: {name} → {new_name}")
            print(f"✅ Đã sửa thành: {new_name}\n")
            return "fixed"
        else:
            print("⚠️ Không nhập gì — bỏ qua.\n")
            return "skipped"

    else:
        print("⏩ Bỏ qua.\n")
        return "skipped"

# 🧹 Chạy kiểm tra lỗi, sau đó duyệt tất cả
def stepwise_delete_or_fix_translations():
    deleted_log = []
    fixed_log = []
    skipped_ids = set()
    count_deleted = 0
    count_fixed = 0

    # 🧭 Giai đoạn 1: Sửa các lỗi dịch
    while True:
        products = Product.objects.all()
        error_products = [p for p in products if is_wrong_translation(p.name) and p.id not in skipped_ids]

        if not error_products:
            print("\n✅ Không còn sản phẩm lỗi dịch.\n")
            break

        print(f"📝 Còn {len(error_products)} sản phẩm lỗi chưa xử lý...\n")

        for product in error_products:
            result = handle_product(product, deleted_log, fixed_log)
            if result == "deleted":
                count_deleted += 1
                break
            elif result == "fixed":
                count_fixed += 1
                break
            elif result == "skipped":
                skipped_ids.add(product.id)

    # 🧭 Giai đoạn 2: Cho phép duyệt thủ công tất cả sản phẩm
    print("\n🔁 Bắt đầu chế độ chỉnh sửa thủ công toàn bộ sản phẩm.")
    products = Product.objects.all().order_by('id')

    for product in products:
        # Nếu sản phẩm đã bị xóa trong bước trước thì bỏ qua
        if not Product.objects.filter(id=product.id).exists():
            continue

        result = handle_product(product, deleted_log, fixed_log)
        if result == "deleted":
            count_deleted += 1
        elif result == "fixed":
            count_fixed += 1

    # Ghi log sau khi kết thúc
    with open(LOG_FILE, "w", encoding="utf-8") as log:
        if deleted_log:
            log.write("\n".join(deleted_log) + "\n")
        if fixed_log:
            log.write("\n".join(fixed_log))

    print(f"\n🧹 Tổng cộng đã xóa {count_deleted} sản phẩm.")
    print(f"✏️ Tổng cộng đã sửa {count_fixed} sản phẩm.")
    if deleted_log or fixed_log:
        print(f"📄 Log lưu tại: {LOG_FILE}")


if __name__ == "__main__":
    stepwise_delete_or_fix_translations()
