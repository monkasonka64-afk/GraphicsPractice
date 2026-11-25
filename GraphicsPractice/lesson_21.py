import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

os.makedirs("output", exist_ok=True)


def lerp(a, b, t):
    """Линейная интерполяция между a и b при t в диапазоне [0.0, 1.0]."""
    return int(round(a + (b - a) * t))


def lerp_color(c1, c2, t):
    """Плавно смешивает два RGB-кортежа по коэффициенту t."""
    return tuple(lerp(c1[i], c2[i], t) for i in range(3))


def load_font(size=20):
    """Загружает Arial из системной папки Windows или возвращает шрифт по умолчанию."""
    font_path = "C:/Windows/Fonts/arial.ttf"
    if os.path.exists(font_path):
        return ImageFont.truetype(font_path, size)
    return ImageFont.load_default()


def task_21_1_vertical_gradient(dst="output/bg_gradient_800x600.png"):
    """
    Задача 21.1: вертикальный градиент 800x600 от тёмно-синего к светло-голубому
    в цикле по строкам с использованием ImageDraw.line.
    """
    width, height = 800, 600
    dark_blue = (15, 23, 42)       # Тёмно-синий
    light_blue = (125, 211, 252)   # Светло-голубой

    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    denom = max(1, height - 1)
    for y in range(height):
        t = y / denom
        color = lerp_color(dark_blue, light_blue, t)
        draw.line([(0, y), (width - 1, y)], fill=color, width=1)

    img.save(dst, format="PNG")
    print(f"[21.1] Сохранён вертикальный градиент: {dst}")
    return img


def task_21_2_horizontal_gradient(dst="output/header_gradient_800x60.png"):
    """
    Задача 21.2: горизонтальный градиент 800x60 для заголовка
    в цикле по столбцам с использованием ImageDraw.line.
    """
    width, height = 800, 60
    start_color = (29, 78, 216)    # Насыщенный синий
    end_color = (14, 165, 233)     # Голубой акцент

    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    denom = max(1, width - 1)
    for x in range(width):
        t = x / denom
        color = lerp_color(start_color, end_color, t)
        draw.line([(x, 0), (x, height - 1)], fill=color, width=1)

    title_font = load_font(24)
    title_text = "Панель управления графическим модулем"
    bbox = draw.textbbox((0, 0), title_text, font=title_font)
    tx = (width - (bbox[2] - bbox[0])) // 2 - bbox[0]
    ty = (height - (bbox[3] - bbox[1])) // 2 - bbox[1]
    draw.text((tx, ty), title_text, font=title_font, fill=(255, 255, 255))

    img.save(dst, format="PNG")
    print(f"[21.2] Сохранён горизонтальный градиент заголовка: {dst}")
    return img


def task_21_3_shadow_card(dst="output/card_with_shadow.png"):
    """
    Задача 21.3: карточка со скруглениями и тенью:
    копия формы чёрного цвета с прозрачностью 40% (alpha = int(255 * 0.4) = 102),
    размытие ImageFilter.GaussianBlur(6) и подложка со смещением (4, 4).
    """
    canvas_size = (260, 140)
    card_rect = (20, 16, 220, 104)
    radius = 16
    offset = (4, 4)

    # Прозрачный холст для композиции тени и карточки
    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))

    # 1. Создаём копию формы чёрного цвета с прозрачностью 40%
    alpha_40 = int(round(255 * 0.40))  # 102
    shadow_layer = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_layer)
    sx1, sy1, sx2, sy2 = (
        card_rect[0] + offset[0],
        card_rect[1] + offset[1],
        card_rect[2] + offset[0],
        card_rect[3] + offset[1],
    )
    shadow_draw.rounded_rectangle(
        (sx1, sy1, sx2, sy2),
        radius=radius,
        fill=(0, 0, 0, alpha_40),
    )

    # 2. Размываем тень
    blurred_shadow = shadow_layer.filter(ImageFilter.GaussianBlur(6))

    # 3. Подкладываем тень и рисуем основной объект поверх
    canvas = Image.alpha_composite(canvas, blurred_shadow)

    card_layer = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card_layer)
    card_draw.rounded_rectangle(
        card_rect,
        radius=radius,
        fill=(255, 255, 255, 255),
        outline=(52, 152, 219, 255),
        width=2,
    )

    font = load_font(18)
    label = "Карточка UI"
    cx = (card_rect[0] + card_rect[2]) // 2
    cy = (card_rect[1] + card_rect[3]) // 2
    bbox = card_draw.textbbox((0, 0), label, font=font)
    tx = cx - (bbox[2] - bbox[0]) // 2 - bbox[0]
    ty = cy - (bbox[3] - bbox[1]) // 2 - bbox[1]
    card_draw.text((tx, ty), label, font=font, fill=(30, 41, 59, 255))

    result = Image.alpha_composite(canvas, card_layer)
    result.save(dst, format="PNG")
    print(f"[21.3] Сохранена карточка с тенью: {dst}")
    return result


if __name__ == "__main__":
    task_21_1_vertical_gradient()
    task_21_2_horizontal_gradient()
    task_21_3_shadow_card()