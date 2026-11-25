import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("output", exist_ok=True)


def load_font(font_candidates, size):
    """Подбирает первый доступный TTF-шрифт из списка или возвращает шрифт по умолчанию."""
    for path in font_candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_centered_text(draw, canvas_size, text, font, fill="black", offset_y=0):
    """
    Вычисляет границы текста через textbbox и рисует его по центру холста.
    Возвращает координаты (x, y) верхнего левого угла ограничивающего прямоугольника.
    """
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    text_width = right - left
    text_height = bottom - top

    canvas_w, canvas_h = canvas_size
    x = (canvas_w - text_width) // 2 - left
    y = (canvas_h - text_height) // 2 - top + offset_y

    draw.text((x, y), text, font=font, fill=fill)
    return x, y


def task_17_1_and_17_2():
    """Задачи 17.1 и 17.2: надпись через arial.ttf и центрирование по textbbox."""
    font_path = "C:/Windows/Fonts/arial.ttf"
    font = (
        ImageFont.truetype(font_path, 32)
        if os.path.exists(font_path)
        else ImageFont.load_default()
    )

    # 17.1: надпись в заданной точке
    img_17_1 = Image.new("RGBA", (400, 160), (255, 255, 255, 255))
    d_17_1 = ImageDraw.Draw(img_17_1)
    d_17_1.text((20, 20), "Привет", font=font, fill="black")
    out_17_1 = "output/text_17_1.png"
    img_17_1.save(out_17_1, format="PNG")
    print(f"[17.1] Сохранено: {out_17_1}")

    # 17.2: центрирование текста по textbbox
    img_17_2 = Image.new("RGBA", (400, 160), (245, 247, 250, 255))
    d_17_2 = ImageDraw.Draw(img_17_2)
    centered_text = "Привет, мир!"
    bbox = d_17_2.textbbox((0, 0), centered_text, font=font)
    x, y = draw_centered_text(d_17_2, img_17_2.size, centered_text, font=font, fill="#1E293B")
    out_17_2 = "output/text_17_2_centered.png"
    img_17_2.save(out_17_2, format="PNG")
    print(f"[17.2] bbox={bbox}, координаты=({x}, {y}), сохранено: {out_17_2}")


def task_17_3(dst="output/banner_600x150.png"):
    """Задача 17.3: баннер 600x150 на кириллице и казахском языке с проверкой ә, ң, ү, қ."""
    kazakh_font_candidates = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/times.ttf",
    ]

    title_font = load_font(kazakh_font_candidates, 28)
    subtitle_font = load_font(kazakh_font_candidates, 22)
    check_font = load_font(kazakh_font_candidates, 16)

    banner = Image.new("RGBA", (600, 150), (24, 42, 68, 255))
    draw = ImageDraw.Draw(banner)

    draw.rectangle((4, 4, 595, 145), outline=(96, 165, 250, 255), width=2)

    ru_title = "Графический редактор «Өрнек»"
    kz_title = "Бағдарлама атауы: Әлем — Ңұр — Үміт — Қазақ"
    check_letters = "Проверка символов: ә  ң  ү  қ  Ә  Ң  Ү  Қ"

    draw_centered_text(
        draw,
        banner.size,
        ru_title,
        font=title_font,
        fill=(255, 255, 255, 255),
        offset_y=-34,
    )
    draw_centered_text(
        draw,
        banner.size,
        kz_title,
        font=subtitle_font,
        fill=(147, 197, 253, 255),
        offset_y=6,
    )
    draw_centered_text(
        draw,
        banner.size,
        check_letters,
        font=check_font,
        fill=(203, 213, 225, 255),
        offset_y=42,
    )

    banner.save(dst, format="PNG")
    print(f"[17.3] Баннер сохранён: {dst}")


if __name__ == "__main__":
    task_17_1_and_17_2()
    task_17_3()