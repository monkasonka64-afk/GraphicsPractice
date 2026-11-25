import os
from typing import Optional
from PIL import Image, ImageDraw, ImageEnhance, ImageOps

SRC, DST = "source", "assets"
PALETTE = {
    "main": (31, 58, 95),        # #1F3A5F
    "accent": (52, 152, 219),    # #3498DB
    "accent_dark": (36, 113, 163),
    "disabled": (148, 163, 184),
    "white": (255, 255, 255),
}


def find_source(*candidates: str) -> Optional[str]:
    """Ищет первый существующий исходный файл в папке SRC."""
    for name in candidates:
        path = os.path.join(SRC, name)
        if os.path.isfile(path):
            return path
    return None


def fit_rgba(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Масштабирует изображение с сохранением пропорций и центрирует на прозрачном холсте."""
    work = img.convert("RGBA").copy()
    work.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    offset = ((size[0] - work.width) // 2, (size[1] - work.height) // 2)
    canvas.paste(work, offset, work)
    return canvas


def make_ico():
    """Создаёт assets/app.ico (размеры 16-256 px)."""
    src_path = find_source("icon.png", "app.png", "logo.png", "лого.jpg", "бмп.bmp")
    if not src_path:
        print("[Пропуск] Не найден исходник для иконки приложения (icon.png / app.png / logo.png).")
        return

    with Image.open(src_path) as raw:
        base = fit_rgba(raw, (256, 256))

    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle((6, 6, 250, 250), radius=44, outline=PALETTE["accent"], width=8)

    out_path = os.path.join(DST, "app.ico")
    base.save(
        out_path,
        format="ICO",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    print(f"  -> сохранён {out_path} (из {os.path.basename(src_path)})")


def make_logo():
    """Создаёт assets/logo.png размером 200x60 px с прозрачным фоном."""
    src_path = find_source("logo.png", "лого.jpg", "icon.png", "бмп.bmp")
    if not src_path:
        print("[Пропуск] Не найден исходник для логотипа (logo.png / лого.jpg).")
        return

    with Image.open(src_path) as raw:
        icon_part = fit_rgba(raw, (48, 48))

    logo = Image.new("RGBA", (200, 60), (0, 0, 0, 0))
    draw = ImageDraw.Draw(logo)
    draw.rounded_rectangle((1, 2, 199, 58), radius=10, fill=PALETTE["main"], outline=PALETTE["accent"], width=2)
    logo.paste(icon_part, (8, 6), icon_part)

    draw.rounded_rectangle((66, 20, 184, 40), radius=6, fill=PALETTE["accent"])
    draw.line([(76, 30), (174, 30)], fill=PALETTE["white"], width=3)

    out_path = os.path.join(DST, "logo.png")
    logo.save(out_path, format="PNG", optimize=True)
    print(f"  -> сохранён {out_path} (из {os.path.basename(src_path)})")


def make_background():
    """Создаёт assets/bg.jpg размером 800x600 px."""
    src_path = find_source("bg.jpg", "bg.png", "background.jpg", "background.png", "фото.jpg")
    if not src_path:
        print("[Пропуск] Не найден исходник для фона (bg.jpg / bg.png / фото.jpg).")
        return

    with Image.open(src_path) as raw:
        fitted = ImageOps.fit(raw.convert("RGB"), (800, 600), method=Image.Resampling.LANCZOS)

    fitted = ImageEnhance.Brightness(fitted).enhance(0.85)
    fitted = ImageEnhance.Contrast(fitted).enhance(0.9)

    out_path = os.path.join(DST, "bg.jpg")
    fitted.save(out_path, format="JPEG", quality=85, optimize=True)
    print(f"  -> сохранён {out_path} (из {os.path.basename(src_path)})")


def make_buttons():
    """Создаёт 4 состояния кнопки (160x48 px): normal, hover, pressed, disabled."""
    src_path = find_source("btn.png", "button.png", "btn_normal.png")
    base_icon = None
    if src_path:
        with Image.open(src_path) as raw:
            base_icon = fit_rgba(raw, (28, 28))
    else:
        print("[Инфо] Исходник btn.png не найден — кнопки собраны на базовом шаблоне 160x48.")

    states = {
        "btn_normal.png": (PALETTE["accent"], PALETTE["accent_dark"], PALETTE["white"], 0),
        "btn_hover.png": ((77, 171, 232), PALETTE["accent"], PALETTE["white"], -1),
        "btn_pressed.png": (PALETTE["main"], PALETTE["accent_dark"], (226, 232, 240), 1),
        "btn_disabled.png": (PALETTE["disabled"], (100, 116, 139), (241, 245, 249), 0),
    }

    for filename, (fill_col, border_col, bar_col, shift_y) in states.items():
        btn = Image.new("RGBA", (160, 48), (0, 0, 0, 0))
        draw = ImageDraw.Draw(btn)
        draw.rounded_rectangle(
            (1, 1 + shift_y, 159, 47 + shift_y),
            radius=10,
            fill=fill_col,
            outline=border_col,
            width=2,
        )
        if base_icon is not None:
            btn.paste(base_icon, (14, 10 + shift_y), base_icon)
            draw.rounded_rectangle((50, 19 + shift_y, 142, 29 + shift_y), radius=4, fill=bar_col)
        else:
            draw.rounded_rectangle((32, 19 + shift_y, 128, 29 + shift_y), radius=4, fill=bar_col)

        out_path = os.path.join(DST, filename)
        btn.save(out_path, format="PNG", optimize=True)
        print(f"  -> сохранён {out_path}")


def make_field_icons():
    """Создаёт иконки полей ввода ic_user.png и ic_lock.png размером 24x24 px."""
    user_src = find_source("ic_user.png", "user.png")
    if not user_src:
        print("[Пропуск] Не найден исходник для иконки «Логин» (ic_user.png / user.png).")
    else:
        with Image.open(user_src) as raw:
            ic_user = fit_rgba(raw, (24, 24))
        out_user = os.path.join(DST, "ic_user.png")
        ic_user.save(out_user, format="PNG", optimize=True)
        print(f"  -> сохранён {out_user} (из {os.path.basename(user_src)})")

    lock_src = find_source("ic_lock.png", "lock.png")
    if not lock_src:
        print("[Пропуск] Не найден исходник для иконки «Пароль» (ic_lock.png / lock.png).")
    else:
        with Image.open(lock_src) as raw:
            ic_lock = fit_rgba(raw, (24, 24))
        out_lock = os.path.join(DST, "ic_lock.png")
        ic_lock.save(out_lock, format="PNG", optimize=True)
        print(f"  -> сохранён {out_lock} (из {os.path.basename(lock_src)})")


if __name__ == "__main__":
    os.makedirs(SRC, exist_ok=True)
    os.makedirs(DST, exist_ok=True)
    for step in (make_ico, make_logo, make_background, make_buttons, make_field_icons):
        step()
        print("Готово:", step.__name__)