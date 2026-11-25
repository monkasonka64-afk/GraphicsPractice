import os
from PIL import Image

os.makedirs("output", exist_ok=True)

# Путь к PNG с прозрачностью (можно заменить на свой файл, например output/rotate_45.png)
src_png = "source/logo.png"
if not os.path.exists(src_png):
    src_png = "output/rotate_45.png"

# --- Задача 13.1. Режим, разделение каналов и значения альфа-канала в 5 точках ---
with Image.open(src_png) as raw_img:
    img_13_1 = raw_img.convert("RGBA")
    print(f"[13.1] Режим изображения: {img_13_1.mode}, размер: {img_13_1.size}")

    r, g, b, a = img_13_1.split()
    w, h = img_13_1.size

    # 5 контрольных точек: углы и центр
    points = [
        (0, 0),
        (w - 1, 0),
        (0, h - 1),
        (w - 1, h - 1),
        (w // 2, h // 2),
    ]

    for px, py in points:
        alpha_val = a.getpixel((px, py))
        print(f"  Точка ({px}, {py}) -> альфа-канал: {alpha_val}")

# --- Задача 13.2. Полупрозрачное изображение (альфа 50%) ---
with Image.open(src_png) as raw_img:
    img_50 = raw_img.convert("RGBA")
    alpha_50 = img_50.getchannel("A").point(lambda p: int(p * 0.5))
    img_50.putalpha(alpha_50)
    logo_50_path = "output/logo_50.png"
    img_50.save(logo_50_path, format="PNG")
    print(f"[13.2] Сохранено: {logo_50_path}")

# --- Задача 13.3. Наложение логотипа на фон через Image.alpha_composite ---
# Подбираем фоновое изображение (если нет source/bg.jpg, берём source/фото.jpg или создаём фон)
bg_candidates = ["source/bg.jpg", "source/фото.jpg", "source/photo.jpg"]
bg_path = next((p for p in bg_candidates if os.path.exists(p)), None)

with Image.open(src_png) as raw_logo:
    base_logo = raw_logo.convert("RGBA")

    if bg_path:
        with Image.open(bg_path) as raw_bg:
            bg_rgba = raw_bg.convert("RGBA").resize(base_logo.size, Image.Resampling.LANCZOS)
    else:
        bg_rgba = Image.new("RGBA", base_logo.size, (230, 235, 245, 255))

    base_alpha = base_logo.getchannel("A")

    for factor, label in [(0.25, "25"), (0.50, "50"), (0.75, "75")]:
        variant_logo = base_logo.copy()
        scaled_alpha = base_alpha.point(lambda p, k=factor: int(p * k))
        variant_logo.putalpha(scaled_alpha)

        composited = Image.alpha_composite(bg_rgba, variant_logo)
        out_path = f"output/composite_{label}.png"
        composited.save(out_path, format="PNG")
        print(f"[13.3] Вариант {label}% (множитель альфа {factor}): сохранён '{out_path}'")