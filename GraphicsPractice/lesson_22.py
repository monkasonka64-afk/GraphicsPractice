import os
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

os.makedirs("source", exist_ok=True)
os.makedirs("output", exist_ok=True)


def get_or_create_source_image(path="source/sample_photo.png"):
    """
    Берёт существующее изображение из проекта или создаёт тестовый цветной кадр,
    если подходящего файла ещё нет.
    """
    candidates = [
        path,
        "output/bg_gradient_800x600.png",
        "source/photo_200.png",
        "output/shapes.png",
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    img = Image.new("RGB", (600, 400), (219, 234, 254))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 600, 230), fill=(37, 99, 235))
    d.ellipse((430, 45, 520, 135), fill=(250, 204, 21))
    d.polygon([(0, 400), (190, 170), (390, 400)], fill=(22, 163, 74))
    d.polygon([(260, 400), (470, 210), (600, 400)], fill=(21, 128, 61))
    d.rounded_rectangle((50, 55, 290, 145), radius=14, fill=(239, 68, 68))
    img.save(path, format="PNG")
    return path


def load_font(size=20):
    """Загружает Arial из системной папки Windows или возвращает шрифт по умолчанию."""
    font_path = "C:/Windows/Fonts/arial.ttf"
    if os.path.exists(font_path):
        return ImageFont.truetype(font_path, size)
    return ImageFont.load_default()


def draw_centered_text(draw, box_rect, text, font, fill="white"):
    """Рисует текст по центру прямоугольника (x1, y1, x2, y2)."""
    x1, y1, x2, y2 = box_rect
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = x1 + (x2 - x1 - text_w) // 2 - bbox[0]
    y = y1 + (y2 - y1 - text_h) // 2 - bbox[1]
    draw.text((x, y), text, font=font, fill=fill)


def task_22_1_enhancements(src_path):
    """Задача 22.1: изменение яркости, контраста и насыщенности через ImageEnhance."""
    with Image.open(src_path) as raw:
        img = raw.convert("RGB")

    bright = ImageEnhance.Brightness(img).enhance(1.3)
    contrast = ImageEnhance.Contrast(img).enhance(1.4)
    color = ImageEnhance.Color(img).enhance(0.5)

    bright.save("output/enhance_bright_1_3.png", format="PNG")
    contrast.save("output/enhance_contrast_1_4.png", format="PNG")
    color.save("output/enhance_color_0_5.png", format="PNG")
    print("[22.1] Сохранены варианты коррекции яркости, контраста и насыщенности")

    return img, bright, contrast, color


def task_22_2_collage_2x2(original, bright, contrast, color, dst="output/collage_2x2.png"):
    """Задача 22.2: коллаж 2x2 из оригинала и трёх коррекций с подписями."""
    cell_w, cell_h = 360, 240
    label_h = 34
    pad = 16

    collage_w = pad * 3 + cell_w * 2
    collage_h = pad * 3 + (cell_h + label_h) * 2
    collage = Image.new("RGB", (collage_w, collage_h), (241, 245, 249))
    draw = ImageDraw.Draw(collage)
    label_font = load_font(18)

    items = [
        ("Оригинал", original),
        ("Яркость (x1.3)", bright),
        ("Контраст (x1.4)", contrast),
        ("Насыщенность (x0.5)", color),
    ]

    positions = [
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
    ]

    for (row, col), (caption, variant_img) in zip(positions, items):
        x = pad + col * (cell_w + pad)
        y = pad + row * (cell_h + label_h + pad)

        fitted = ImageOps.fit(variant_img, (cell_w, cell_h), method=Image.Resampling.LANCZOS)
        collage.paste(fitted, (x, y))
        draw.rectangle((x, y, x + cell_w - 1, y + cell_h - 1), outline=(148, 163, 184), width=1)

        label_box = (x, y + cell_h, x + cell_w, y + cell_h + label_h)
        draw.rectangle(label_box, fill=(30, 41, 59))
        draw_centered_text(draw, label_box, caption, font=label_font, fill=(255, 255, 255))

    collage.save(dst, format="PNG")
    print(f"[22.2] Сохранён коллаж 2x2: {dst}")


def task_22_3_darken_for_text(src_path, dst_bg="output/bg_darkened_40.png", dst_preview="output/darkened_with_text.png"):
    """
    Задача 22.3: затемнение фона на 40% (яркость 0.6) и проверка читаемости белого текста.
    """
    with Image.open(src_path) as raw:
        bg = ImageOps.fit(raw.convert("RGB"), (800, 450), method=Image.Resampling.LANCZOS)

    # Затемнение на 40% -> остаётся 60% яркости (множитель 0.6)
    darkened = ImageEnhance.Brightness(bg).enhance(0.6)
    darkened.save(dst_bg, format="PNG")

    preview = darkened.copy()
    draw = ImageDraw.Draw(preview)

    heading_font = load_font(34)
    body_font = load_font(22)

    draw_centered_text(
        draw,
        (40, 110, 760, 190),
        "Заголовок поверх затемнённого фона",
        font=heading_font,
        fill=(255, 255, 255),
    )
    draw_centered_text(
        draw,
        (60, 200, 740, 310),
        "Яркость снижена на 40% (коэффициент 0.6) для уверенной читаемости белого текста",
        font=body_font,
        fill=(248, 250, 252),
    )

    preview.save(dst_preview, format="PNG")
    print(f"[22.3] Сохранён затемнённый фон: {dst_bg} и скриншот проверки: {dst_preview}")


if __name__ == "__main__":
    source_img_path = get_or_create_source_image()
    print(f"Исходное изображение: {source_img_path}")

    orig, br, ct, cl = task_22_1_enhancements(source_img_path)
    task_22_2_collage_2x2(orig, br, ct, cl)
    task_22_3_darken_for_text(source_img_path)