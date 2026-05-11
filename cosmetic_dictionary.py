# -*- coding: utf-8 -*-
# 📘 TỪ ĐIỂN DỊCH MỸ PHẨM MỞ RỘNG — bao phủ tên + mô tả sản phẩm
# Không cần Google Translate

# ⚠️ 1. Từ KHÔNG DỊCH
keep_original = {
    "maybelline", "covergirl", "l'oreal", "revlon", "nyx", "mac", "nars", "fenty",
    "urban decay", "cargo", "glossier", "epic", "proof", "superstay", "fit", "tattoo",
    "pro", "studio", "hyper", "mega", "lash", "vinyl", "ink", "colorstay", "colourpop",
    "epic ink", "liquid ink", "prime", "no", "filter", "#nofilter", "super", "glow up",
    "maybelline new york", "milani", "sephora", "too faced", "benefit", "it", "this", "that’s",
}

# 🧩 2. Từ DỊCH BÁN PHẦN (ghép ngữ cảnh)
partial_translate = {
    "volume": "làm dày",
    "length": "làm dài",
    "curl": "cong",
    "wear": "bền màu",
    "finish": "hiệu ứng",
    "effect": "hiệu ứng",
    "look": "phong cách",
    "shine": "độ bóng",
    "base": "lớp nền",
    "primer": "lót",
    "liner": "kẻ",
    "ink": "mực kẻ",
    "matte": "lì",
    "dewy": "căng bóng",
}

# 🧴 3. Loại sản phẩm
cosmetic_dict = {
    "lip": "môi", "lipstick": "son môi", "lip gloss": "son bóng", "lip balm": "son dưỡng",
    "lip oil": "dầu dưỡng môi", "lip tint": "son tint", "lip stain": "son lì lâu trôi",
    "eyeliner": "kẻ mắt", "liner": "kẻ mắt", "mascara": "chuốt mi",
    "eyeshadow": "phấn mắt", "shadow": "phấn mắt", "palette": "bảng màu",
    "foundation": "kem nền", "concealer": "kem che khuyết điểm",
    "blush": "phấn má hồng", "bronzer": "phấn tạo khối", "powder": "phấn phủ",
    "primer": "kem lót", "highlighter": "phấn bắt sáng", "setting spray": "xịt cố định lớp trang điểm",
    "tint": "son tint", "stain": "son lì", "cushion": "phấn nước",
    "brow": "mày", "eyebrow": "chân mày", "brow gel": "gel định hình mày",
    "brow pencil": "bút kẻ mày", "brow powder": "phấn mày", "pomade": "sáp kẻ mày",
    "liner pen": "bút kẻ mắt", "crayon": "bút sáp", "stick": "dạng thỏi",
    "liquid": "dạng lỏng", "cream": "dạng kem", "gel": "dạng gel",
    "serum": "serum", "toner": "nước hoa hồng", "moisturizer": "kem dưỡng ẩm",
    "cleanser": "sữa rửa mặt", "mask": "mặt nạ", "scrub": "tẩy da chết",
    "balm": "dưỡng", "mist": "xịt dưỡng", "fixer": "xịt cố định", "remover": "tẩy trang",

    # ⚡ Finish & texture
    "matte": "lì", "soft matte": "lì mềm", "semi matte": "bán lì", "velvet": "mịn mượt",
    "dewy": "căng bóng", "radiant": "rạng rỡ", "shimmer": "ánh nhũ nhẹ",
    "glitter": "nhũ lấp lánh", "metallic": "ánh kim", "silky": "mịn màng",
    "creamy": "mịn kem", "powdery": "dạng phấn", "sheer": "mỏng nhẹ",
    "full coverage": "che phủ cao", "medium coverage": "che phủ vừa",
    "buildable": "có thể tăng độ che phủ", "long lasting": "lâu trôi",
    "smudge-proof": "chống lem", "waterproof": "chống nước",
    "lightweight": "nhẹ mặt", "blurring": "làm mờ khuyết điểm",
    "luminous": "bắt sáng", "glow": "hiệu ứng sáng da",

    # 🌿 Công dụng
    "hydrating": "dưỡng ẩm", "moisturizing": "dưỡng ẩm", "brightening": "làm sáng da",
    "anti-aging": "chống lão hóa", "oil control": "kiểm soát dầu", "soothing": "làm dịu da",
    "firming": "săn chắc da", "repairing": "phục hồi da", "whitening": "làm trắng",
    "pore minimizing": "làm mịn lỗ chân lông", "anti-oxidant": "chống oxy hóa",
    "uv protection": "chống tia UV", "spf": "chống nắng", "broad spectrum": "phổ rộng",
    "non greasy": "không nhờn", "quick absorbing": "thấm nhanh",

    # 🧪 Thành phần
    "vegan": "thuần chay", "cruelty-free": "không thử nghiệm trên động vật",
    "paraben-free": "không chứa paraben", "sulfate-free": "không chứa sulfate",
    "fragrance-free": "không hương liệu", "dermatologist tested": "kiểm nghiệm da liễu",
    "hypoallergenic": "dịu nhẹ", "non-comedogenic": "không gây bít tắc",
    "alcohol-free": "không chứa cồn", "silicone-free": "không chứa silicone",
    "mineral": "khoáng chất", "hyaluronic acid": "axit hyaluronic",
    "niacinamide": "niacinamide", "retinol": "retinol", "vitamin c": "vitamin C",
    "ceramide": "ceramide", "peptide": "peptide", "collagen": "collagen",

    # 📢 Mô tả marketing
    "all day wear": "bền màu suốt ngày", "perfect finish": "hiệu ứng hoàn hảo",
    "effortless look": "trang điểm tự nhiên", "soft focus": "làm mịn da",
    "blur effect": "che mờ khuyết điểm", "skin-like": "tự nhiên như da thật",
    "weightless": "nhẹ như không", "high impact": "hiệu ứng nổi bật",
    "high pigment": "màu đậm rõ", "easy to blend": "dễ tán đều",
    "smooth texture": "kết cấu mịn", "seamless": "liền mượt",
    "buildable coverage": "tăng độ che phủ", "effortless": "dễ dàng",
    "universal": "phù hợp mọi tông da", "flawless": "hoàn hảo",
    "soft touch": "cảm giác mềm mịn", "airbrush finish": "hiệu ứng mịn lì như phun sương",

    # 🎨 Màu sắc mở rộng
    "black": "đen", "white": "trắng", "ivory": "trắng ngà", "cream": "kem", "nude": "màu da",
    "beige": "be", "sand": "cát", "almond": "hạnh nhân", "toffee": "toffee",
    "caramel": "caramen", "honey": "mật ong", "coffee": "cà phê", "mocha": "mocha",
    "brown": "nâu", "chestnut": "hạt dẻ", "rosewood": "gỗ hồng", "peach": "đào",
    "coral": "san hô", "rose": "hồng phấn", "pink": "hồng", "fuchsia": "hồng đậm",
    "red": "đỏ", "burgundy": "đỏ rượu", "plum": "mận", "wine": "rượu vang",
    "bronze": "đồng", "gold": "vàng ánh kim", "silver": "bạc",
    "champagne": "champagne", "taupe": "nâu xám", "charcoal": "xám đậm",
    "grey": "xám", "blue": "xanh dương", "navy": "xanh navy", "teal": "xanh ngọc lam",
    "green": "xanh lá", "mint": "xanh bạc hà", "olive": "xanh oliu",
    "purple": "tím", "lavender": "oải hương", "violet": "tím đậm",
    "clear": "trong suốt", "transparent": "trong suốt",

    # 🧰 Packaging / dụng cụ
    "applicator": "dụng cụ tán", "brush": "cọ", "blender": "mút trang điểm",
    "puff": "bông phấn", "mirror": "gương", "case": "hộp đựng",
    "tube": "tuýp", "compact": "hộp phấn", "jar": "hũ", "pump": "chai có vòi",
    "dropper": "ống nhỏ giọt", "stick": "dạng thỏi", "roller": "đầu lăn",

    # 🧮 Đơn vị / định lượng
    "ml": "ml", "oz": "oz", "g": "g", "pcs": "cái", "pack": "gói", "set": "bộ",
    "kit": "bộ trang điểm", "size": "kích thước", "mini": "mini",
    "full size": "phiên bản đầy đủ", "limited edition": "phiên bản giới hạn",
    "collection": "bộ sưu tập",
}
