import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("assets/icons", exist_ok=True)
os.makedirs("output", exist_ok=True)


def load_font(font_candidates, size):
    """Возвращает первый доступный системный шрифт или шрифт по умолчанию."""
    for path in font_candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_centered_text(draw, canvas_size, text, font, fill="white", offset_x=0, offset_y=0):
    """Центрирует текст на холсте с учётом смещений textbbox."""
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    text_w = right - left
    text_h = bottom - top
    canvas_w, canvas_h = canvas_size
    x = (canvas_w - text_w) // 2 - left + offset_x
    y = (canvas_h - text_h) // 2 - top + offset_y
    draw.text((x, y), text, font=font, fill=fill)


def make_icon(name, color, size=48):
    """
    Задача 18.3: создаёт иконку единого стиля с помощью ImageDraw.
    Поддерживаемые имена: 'home', 'settings', 'user', 'search', 'exit'.
    """
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    stroke = max(2, round(size * 0.065))
    pad = max(4, round(size * 0.14))
    right = size - pad
    bottom = size - pad
    mid_x = size // 2
    mid_y = size // 2

    if name == "home":
        roof_top = (mid_x, pad)
        roof_left = (pad - 1, mid_y + 1)
        roof_right = (right + 1, mid_y + 1)
        d.polygon([roof_top, roof_left, roof_right], fill=color)

        wall_left = pad + max(3, size // 10)
        wall_right = right - max(3, size // 10)
        wall_top = mid_y
        d.rectangle((wall_left, wall_top, wall_right, bottom), fill=color)

        door_w = max(4, size // 7)
        door_h = max(6, size // 4)
        d.rectangle(
            (mid_x - door_w // 2, bottom - door_h, mid_x + door_w // 2, bottom),
            fill=(0, 0, 0, 0),
        )

    elif name == "settings":
        outer_r = size * 0.30
        inner_r = size * 0.13
        teeth = 8

        # Лучи/зубцы шестерёнки
        for i in range(teeth):
            angle_deg = i * (360 / teeth)
            import math

            rad = math.radians(angle_deg)
            tx = mid_x + math.cos(rad) * outer_r
            ty = mid_y + math.sin(rad) * outer_r
            tooth_r = max(2, round(size * 0.085))
            d.ellipse((tx - tooth_r, ty - tooth_r, tx + tooth_r, ty + tooth_r), fill=color)

        d.ellipse(
            (mid_x - outer_r, mid_y - outer_r, mid_x + outer_r, mid_y + outer_r),
            fill=color,
        )
        d.ellipse(
            (mid_x - inner_r, mid_y - inner_r, mid_x + inner_r, mid_y + inner_r),
            fill=(0, 0, 0, 0),
        )

    elif name == "user":
        head_r = max(5, round(size * 0.15))
        head_cy = pad + head_r + max(1, size // 24)
        d.ellipse(
            (mid_x - head_r, head_cy - head_r, mid_x + head_r, head_cy + head_r),
            fill=color,
        )

        # Плечи / корпус (полуовал)
        body_left = pad + max(1, size // 16)
        body_right = right - max(1, size // 16)
        body_top = mid_y + max(1, size // 20)
        body_bottom = bottom + max(4, size // 8)
        d.pieslice((body_left, body_top, body_right, body_bottom), start=180, end=360, fill=color)

    elif name == "search":
        lens_r = max(7, round(size * 0.22))
        lens_cx = mid_x - max(2, size // 16)
        lens_cy = mid_y - max(2, size // 16)

        d.ellipse(
            (lens_cx - lens_r, lens_cy - lens_r, lens_cx + lens_r, lens_cy + lens_r),
            outline=color,
            width=stroke,
        )

        # Рукоятка лупы
        import math

        start_x = lens_cx + math.cos(math.radians(45)) * lens_r
        start_y = lens_cy + math.sin(math.radians(45)) * lens_r
        end_x = right
        end_y = bottom
        d.line((start_x, start_y, end_x, end_y), fill=color, width=stroke)

    elif name == "exit":
        box_left = pad
        box_top = pad
        box_right = mid_x + max(2, size // 12)
        box_bottom = bottom

        # Рамка двери/выхода (левая, верхняя, нижняя стороны)
        d.line((box_left, box_top, box_right, box_top), fill=color, width=stroke)
        d.line((box_left, box_bottom, box_right, box_bottom), fill=color, width=stroke)
        d.line((box_left, box_top, box_left, box_bottom), fill=color, width=stroke)

        # Стрелка вправо
        arrow_y = mid_y
        arrow_start_x = mid_x - max(2, size // 12)
        arrow_tip_x = right
        head_len = max(5, round(size * 0.14))

        d.line((arrow_start_x, arrow_y, arrow_tip_x, arrow_y), fill=color, width=stroke)
        d.line(
            (arrow_tip_x - head_len, arrow_y - head_len, arrow_tip_x, arrow_y),
            fill=color,
            width=stroke,
        )
        d.line(
            (arrow_tip_x - head_len, arrow_y + head_len, arrow_tip_x, arrow_y),
            fill=color,
            width=stroke,
        )

    else:
        raise ValueError(f"Неизвестное имя иконки: '{name}'")

    return img


def generate_icons_48():
    """Задача 18.2: генерация 5 иконок 48x48 в assets/icons."""
    icons_spec = {
        "home": (52, 152, 219, 255),
        "settings": (100, 116, 139, 255),
        "user": (46, 204, 113, 255),
        "search": (243, 156, 18, 255),
        "exit": (231, 76, 60, 255),
    }

    for name, color in icons_spec.items():
        icon_img = make_icon(name=name, color=color, size=48)
        out_path = os.path.join("assets/icons", f"{name}.png")
        icon_img.save(out_path, format="PNG")
        print(f"[18.2] Сохранена иконка: {out_path}")


def generate_program_logo(dst="output/program_logo_256.png"):
    """
    Задача 18.1: логотип вымышленной программы 256x256 на прозрачном фоне
    (цветной круг, инициалы по центру, подпись под ним).
    """
    size = 256
    logo = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(logo)

    font_candidates = [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf",
    ]
    initials_font = load_font(font_candidates, 64)
    caption_font = load_font(font_candidates, 24)

    # Цветной круг в верхней/центральной части холста
    circle_r = 76
    circle_cx = size // 2
    circle_cy = 96
    d.ellipse(
        (circle_cx - circle_r, circle_cy - circle_r, circle_cx + circle_r, circle_cy + circle_r),
        fill=(37, 99, 235, 255),
        outline=(29, 78, 216, 255),
        width=4,
    )

    # Инициалы по центру круга
    initials = "ГР"
    draw_centered_text(
        d,
        canvas_size=(size, size),
        text=initials,
        font=initials_font,
        fill=(255, 255, 255, 255),
        offset_x=0,
        offset_y=circle_cy - (size // 2),
    )

    # Подпись под кругом
    caption = "ГрафМастер"
    draw_centered_text(
        d,
        canvas_size=(size, size),
        text=caption,
        font=caption_font,
        fill=(30, 41, 59, 255),
        offset_x=0,
        offset_y=92,
    )

    logo.save(dst, format="PNG")
    print(f"[18.1] Сохранён логотип: {dst}")


if __name__ == "__main__":
    generate_program_logo()
    generate_icons_48()