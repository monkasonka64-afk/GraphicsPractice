import math
import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("assets/icons", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Задача 24.1: единая палитра из 5 цветов
PALETTE = {
    "primary": (37, 99, 235),    # Основной цвет (насыщенный синий)
    "accent": (14, 165, 233),    # Акцентный цвет (голубой)
    "bg": (248, 250, 252),       # Цвет фона (светло-серый/почти белый)
    "text": (15, 23, 42),        # Цвет текста (тёмно-графитовый)
    "error": (220, 38, 38),      # Цвет ошибки / критических действий (красный)
}

# Единые метрики стиля (Задача 24.2)
STYLE_CONFIG = {
    "icon_size": 48,
    "icon_stroke_ratio": 0.065,
    "btn_size": (160, 48),
    "btn_radius": 10,
    "btn_font_size": 20,
}


def shade(color, k):
    """Меняет яркость RGB-кортежа с коэффициентом k и ограничением [0..255]."""
    return tuple(max(0, min(255, int(round(c * k)))) for c in color)


def to_hex(rgb):
    """Переводит RGB-кортеж в строку HEX (#RRGGBB)."""
    return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"


def load_font(size=20, bold=False):
    """Загружает системный шрифт Arial из Windows или шрифт по умолчанию."""
    candidates = (
        ["C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"]
        if bold
        else ["C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"]
    )
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_centered_text(draw, box_rect, text, font, fill):
    """Рисует текст строго по центру прямоугольника (x1, y1, x2, y2)."""
    x1, y1, x2, y2 = box_rect
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = x1 + (x2 - x1 - text_w) // 2 - bbox[0]
    y = y1 + (y2 - y1 - text_h) // 2 - bbox[1]
    draw.text((x, y), text, font=font, fill=fill)


def make_styled_icon(name, color, size=STYLE_CONFIG["icon_size"]):
    """
    Создаёт иконку в едином стиле: заданный размер size и единая толщина линий
    (stroke = max(2, round(size * icon_stroke_ratio))).
    """
    rgba = (*color, 255) if len(color) == 3 else color
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    stroke = max(2, round(size * STYLE_CONFIG["icon_stroke_ratio"]))
    pad = max(4, round(size * 0.14))
    right = size - pad
    bottom = size - pad
    mid_x = size // 2
    mid_y = size // 2

    if name == "home":
        d.polygon([(mid_x, pad), (pad - 1, mid_y + 1), (right + 1, mid_y + 1)], fill=rgba)
        wall_left = pad + max(3, size // 10)
        wall_right = right - max(3, size // 10)
        d.rectangle((wall_left, mid_y, wall_right, bottom), fill=rgba)
        door_w = max(4, size // 7)
        door_h = max(6, size // 4)
        d.rectangle(
            (mid_x - door_w // 2, bottom - door_h, mid_x + door_w // 2, bottom),
            fill=(0, 0, 0, 0),
        )

    elif name == "settings":
        outer_r = size * 0.29
        inner_r = size * 0.125
        tooth_r = max(2, round(size * 0.08))
        for i in range(8):
            rad = math.radians(i * 45)
            tx = mid_x + math.cos(rad) * outer_r
            ty = mid_y + math.sin(rad) * outer_r
            d.ellipse((tx - tooth_r, ty - tooth_r, tx + tooth_r, ty + tooth_r), fill=rgba)
        d.ellipse((mid_x - outer_r, mid_y - outer_r, mid_x + outer_r, mid_y + outer_r), fill=rgba)
        d.ellipse((mid_x - inner_r, mid_y - inner_r, mid_x + inner_r, mid_y + inner_r), fill=(0, 0, 0, 0))

    elif name == "user":
        head_r = max(5, round(size * 0.15))
        head_cy = pad + head_r + max(1, size // 24)
        d.ellipse((mid_x - head_r, head_cy - head_r, mid_x + head_r, head_cy + head_r), fill=rgba)
        body_left = pad + max(1, size // 16)
        body_right = right - max(1, size // 16)
        body_top = mid_y + max(1, size // 20)
        body_bottom = bottom + max(4, size // 8)
        d.pieslice((body_left, body_top, body_right, body_bottom), start=180, end=360, fill=rgba)

    elif name == "search":
        lens_r = max(7, round(size * 0.21))
        lens_cx = mid_x - max(2, size // 16)
        lens_cy = mid_y - max(2, size // 16)
        d.ellipse(
            (lens_cx - lens_r, lens_cy - lens_r, lens_cx + lens_r, lens_cy + lens_r),
            outline=rgba,
            width=stroke,
        )
        start_x = lens_cx + math.cos(math.radians(45)) * lens_r
        start_y = lens_cy + math.sin(math.radians(45)) * lens_r
        d.line((start_x, start_y, right, bottom), fill=rgba, width=stroke)

    elif name == "exit":
        box_right = mid_x + max(2, size // 12)
        d.line((pad, pad, box_right, pad), fill=rgba, width=stroke)
        d.line((pad, bottom, box_right, bottom), fill=rgba, width=stroke)
        d.line((pad, pad, pad, bottom), fill=rgba, width=stroke)

        arrow_start_x = mid_x - max(2, size // 12)
        head_len = max(5, round(size * 0.14))
        d.line((arrow_start_x, mid_y, right, mid_y), fill=rgba, width=stroke)
        d.line((right - head_len, mid_y - head_len, right, mid_y), fill=rgba, width=stroke)
        d.line((right - head_len, mid_y + head_len, right, mid_y), fill=rgba, width=stroke)

    else:
        raise ValueError(f"Неизвестное имя иконки: '{name}'")

    return img


def make_styled_button(
    text,
    bg,
    fg=(255, 255, 255),
    size=STYLE_CONFIG["btn_size"],
    radius=STYLE_CONFIG["btn_radius"],
    font_size=STYLE_CONFIG["btn_font_size"],
):
    """Создаёт кнопку с едиными размерами, радиусом скругления и шрифтом."""
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=(*bg, 255))

    font = load_font(font_size, bold=False)
    draw_centered_text(d, (0, 0, size[0], size[1]), text, font=font, fill=(*fg, 255))
    return img


def apply_palette_to_assets():
    """
    Задача 24.2: приводит все иконки и кнопки к единой палитре PALETTE
    и единым параметрам стиля.
    """
    icon_colors = {
        "home": PALETTE["primary"],
        "settings": PALETTE["text"],
        "user": PALETTE["accent"],
        "search": PALETTE["primary"],
        "exit": PALETTE["error"],
    }

    styled_icons = {}
    for name, color in icon_colors.items():
        icon = make_styled_icon(name, color, size=STYLE_CONFIG["icon_size"])
        icon.save(os.path.join("assets/icons", f"{name}.png"), format="PNG")
        styled_icons[name] = icon

    primary = PALETTE["primary"]
    styled_buttons = {
        "normal": make_styled_button("Войти", primary, fg=(255, 255, 255)),
        "hover": make_styled_button("Войти", shade(primary, 1.15), fg=(255, 255, 255)),
        "pressed": make_styled_button("Войти", shade(primary, 0.85), fg=(255, 255, 255)),
        "disabled": make_styled_button("Войти", (180, 188, 198), fg=(235, 238, 242)),
        "cancel": make_styled_button("Отмена", PALETTE["error"], fg=(255, 255, 255)),
    }

    styled_buttons["normal"].save("assets/btn_normal.png", format="PNG")
    styled_buttons["hover"].save("assets/btn_hover.png", format="PNG")
    styled_buttons["pressed"].save("assets/btn_pressed.png", format="PNG")
    styled_buttons["disabled"].save("assets/btn_disabled.png", format="PNG")
    styled_buttons["cancel"].save("output/btn_cancel.png", format="PNG")

    print("[24.2] Иконки и кнопки приведены к единому стилю и палитре PALETTE")
    return styled_icons, styled_buttons


def build_logo_256(size=256):
    """Формирует логотип 256x256 в цветах палитры."""
    logo = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(logo)

    r = 74
    cx = size // 2
    cy = 94
    d.ellipse(
        (cx - r, cy - r, cx + r, cy + r),
        fill=(*PALETTE["primary"], 255),
        outline=(*PALETTE["accent"], 255),
        width=4,
    )

    initials_font = load_font(60, bold=True)
    caption_font = load_font(22, bold=True)

    draw_centered_text(d, (cx - r, cy - r, cx + r, cy + r), "ГР", font=initials_font, fill=(255, 255, 255, 255))
    draw_centered_text(d, (0, 180, size, 235), "ГрафМастер", font=caption_font, fill=(*PALETTE["text"], 255))
    return logo


def build_style_sheet_800x500(styled_icons, styled_buttons, dst="output/style_sheet_800x500.png"):
    """
    Задача 24.3: собирает «лист стиля» 800x500 с логотипом, кнопками трёх состояний,
    иконками и образцами палитры.
    """
    w, h = 800, 500
    sheet = Image.new("RGB", (w, h), PALETTE["bg"])
    d = ImageDraw.Draw(sheet)

    title_font = load_font(22, bold=True)
    section_font = load_font(15, bold=True)
    label_font = load_font(12, bold=False)

    # Шапка листа стиля
    d.rectangle((0, 0, w, 54), fill=PALETTE["primary"])
    d.text((24, 15), "ЛИСТ СТИЛЯ ИНТЕРФЕЙСА (800×500)", fill=(255, 255, 255), font=title_font)

    # 1. Блок логотипа (слева вверху)
    d.rounded_rectangle((24, 74, 244, 286), radius=12, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    d.text((36, 82), "Логотип", fill=PALETTE["text"], font=section_font)
    logo_small = build_logo_256(256).resize((160, 160), resample=Image.Resampling.LANCZOS)
    sheet.paste(logo_small, (54, 108), logo_small)

    # 2. Блок палитры из 5 цветов (справа вверху)
    d.rounded_rectangle((264, 74, 776, 286), radius=12, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    d.text((280, 82), "Палитра PALETTE (5 цветов)", fill=PALETTE["text"], font=section_font)

    palette_titles = {
        "primary": "Основной",
        "accent": "Акцентный",
        "bg": "Фон",
        "text": "Текст",
        "error": "Ошибка",
    }
    swatch_w, swatch_h = 86, 68
    start_x = 280
    gap_x = 14
    for idx, (key, title) in enumerate(palette_titles.items()):
        rgb = PALETTE[key]
        sx = start_x + idx * (swatch_w + gap_x)
        sy = 114
        d.rounded_rectangle((sx, sy, sx + swatch_w, sy + swatch_h), radius=8, fill=rgb, outline=(148, 163, 184), width=1)
        d.text((sx, sy + swatch_h + 6), title, fill=PALETTE["text"], font=label_font)
        d.text((sx, sy + swatch_h + 22), to_hex(rgb), fill=(100, 116, 139), font=label_font)

    # 3. Блок кнопок трёх состояний (слева внизу)
    d.rounded_rectangle((24, 304, 540, 476), radius=12, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    d.text((40, 314), "Кнопки состояний (160×48, r=10)", fill=PALETTE["text"], font=section_font)

    btn_states = [
        ("Обычное", styled_buttons["normal"]),
        ("Наведение", styled_buttons["hover"]),
        ("Нажатие", styled_buttons["pressed"]),
    ]
    for idx, (state_name, btn_img) in enumerate(btn_states):
        bx = 40 + idx * 164
        by = 352
        sheet.paste(btn_img, (bx, by), btn_img)
        draw_centered_text(d, (bx, by + 54, bx + 160, by + 76), state_name, font=label_font, fill=PALETTE["text"])

    # 4. Блок иконок единого стиля (справа внизу)
    d.rounded_rectangle((560, 304, 776, 476), radius=12, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    d.text((574, 314), "Иконки (48×48)", fill=PALETTE["text"], font=section_font)

    icon_names = ["home", "settings", "user", "search", "exit"]
    icon_coords = [
        (582, 344),
        (644, 344),
        (706, 344),
        (613, 408),
        (675, 408),
    ]
    for name, (ix, iy) in zip(icon_names, icon_coords):
        ic = styled_icons[name]
        sheet.paste(ic, (ix, iy), ic)

    sheet.save(dst, format="PNG")
    print(f"[24.3] Сохранён лист стиля 800x500: {dst}")


if __name__ == "__main__":
    print("PALETTE:", {k: to_hex(v) for k, v in PALETTE.items()})
    icons, buttons = apply_palette_to_assets()
    build_style_sheet_800x500(icons, buttons)