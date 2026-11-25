import os
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

os.makedirs("assets", exist_ok=True)
os.makedirs("output", exist_ok=True)


def ensure_assets():
    """
    Создаёт assets/app.ico, assets/bg_main.jpg и assets/logo_header.png,
    если они ещё не подготовлены в каталоге assets/.
    """
    ico_path = "assets/app.ico"
    if not os.path.exists(ico_path):
        ico_img = Image.new("RGBA", (64, 64), (31, 58, 95, 255))
        d = ImageDraw.Draw(ico_img)
        d.rounded_rectangle((8, 8, 56, 56), radius=12, fill=(37, 99, 235, 255), outline=(255, 255, 255, 255), width=2)
        d.ellipse((20, 20, 44, 44), fill=(250, 204, 21, 255))
        ico_img.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

    bg_path = "assets/bg_main.jpg"
    if not os.path.exists(bg_path):
        w, h = 800, 600
        bg = Image.new("RGB", (w, h), (226, 232, 240))
        d = ImageDraw.Draw(bg)
        # Верхняя шапка и плавный переход цвета фона
        for y in range(h):
            t = y / max(1, h - 1)
            r = int(226 * (1 - t) + 241 * t)
            g = int(232 * (1 - t) + 245 * t)
            b = int(240 * (1 - t) + 249 * t)
            d.line([(0, y), (w, y)], fill=(r, g, b))
        d.rectangle((0, 0, w, 90), fill=(31, 58, 95))
        d.line([(0, 90), (w, 90)], fill=(59, 130, 246), width=3)
        bg.save(bg_path, format="JPEG", quality=85, optimize=True)

    logo_path = "assets/logo_header.png"
    if not os.path.exists(logo_path):
        logo = Image.new("RGBA", (210, 64), (0, 0, 0, 0))
        d = ImageDraw.Draw(logo)
        d.rounded_rectangle((2, 2, 207, 61), radius=10, fill=(37, 99, 235, 255), outline=(255, 255, 255, 255), width=2)
        d.ellipse((14, 16, 46, 48), fill=(250, 204, 21, 255))
        d.text((58, 24), "ГРАФМАСТЕР UI", fill=(255, 255, 255, 255))
        logo.save(logo_path, format="PNG")

    return ico_path, bg_path, logo_path


def rgb_to_hex(rgb):
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


def sample_logo_bg_hex(bg_path, x=20, y=10, w=210, h=64):
    """Определяет средний цвет фона в области размещения логотипа."""
    with Image.open(bg_path) as raw_bg:
        rgb_bg = raw_bg.convert("RGB")
        crop_box = (
            max(0, x),
            max(0, y),
            min(rgb_bg.width, x + w),
            min(rgb_bg.height, y + h),
        )
        region = rgb_bg.crop(crop_box)
        pixels = list(region.getdata())
        avg_r = sum(p[0] for p in pixels) // len(pixels)
        avg_g = sum(p[1] for p in pixels) // len(pixels)
        avg_b = sum(p[2] for p in pixels) // len(pixels)
        return rgb_to_hex((avg_r, avg_g, avg_b))


def run_lesson_29(fix_bg=True):
    ico_path, bg_path, logo_path = ensure_assets()

    root = tk.Tk()
    root.title("Урок 29 — Иконка окна, логотип и фон")
    root.geometry("800x600")

    # Задача 29.1: установка иконки окна
    if os.path.exists(ico_path):
        try:
            root.iconbitmap(ico_path)
        except tk.TclError:
            pass

    # Задача 29.2: фон на всё окно через place
    with Image.open(bg_path) as raw_bg:
        bg_resized = raw_bg.convert("RGB").resize((800, 600), resample=Image.Resampling.LANCZOS)
        bg = ImageTk.PhotoImage(bg_resized)

    bg_label = tk.Label(root, image=bg)
    bg_label.image = bg
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Логотип в шапке (Задача 29.2 и проверка 29.3)
    with Image.open(logo_path) as raw_logo:
        logo_rgba = raw_logo.convert("RGBA")
        logo = ImageTk.PhotoImage(logo_rgba)

    matched_bg = sample_logo_bg_hex(bg_path, x=20, y=10, w=logo_rgba.width, h=logo_rgba.height)
    # До исправления используем заведомо несовпадающий цвет (#ff00ff), после — цвет фона шапки
    current_bg = matched_bg if fix_bg else "#ff00ff"

    logo_label = tk.Label(root, image=logo, bg=current_bg, bd=0, highlightthickness=0)
    logo_label.image = logo
    logo_label.place(x=20, y=10)

    info_text = (
        f"Режим: {'ПОСЛЕ исправления (bg совпадает с фоном)' if fix_bg else 'ДО исправления (bg не совпадает)'}\n"
        f"Цвет подложки логотипа: {current_bg} | Цвет фона шапки: {matched_bg}"
    )
    status_label = tk.Label(
        root,
        text=info_text,
        font=("Segoe UI", 10),
        bg="#ffffff",
        fg="#0f172a",
        padx=12,
        pady=8,
        justify=tk.LEFT,
    )
    status_label.place(x=20, y=120)

    def toggle_mode():
        nonlocal fix_bg
        fix_bg = not fix_bg
        new_bg = matched_bg if fix_bg else "#ff00ff"
        logo_label.configure(bg=new_bg)
        status_label.configure(
            text=(
                f"Режим: {'ПОСЛЕ исправления (bg совпадает с фоном)' if fix_bg else 'ДО исправления (bg не совпадает)'}\n"
                f"Цвет подложки логотипа: {new_bg} | Цвет фона шапки: {matched_bg}"
            )
        )
        toggle_btn.configure(text="Показать «ДО»" if fix_bg else "Применить «ПОСЛЕ»")

    toggle_btn = tk.Button(
        root,
        text="Показать «ДО»" if fix_bg else "Применить «ПОСЛЕ»",
        font=("Segoe UI", 10, "bold"),
        command=toggle_mode,
        padx=12,
        pady=6,
    )
    toggle_btn.place(x=20, y=185)

    root.mainloop()


if __name__ == "__main__":
    # Для первого скриншота («до») можно передать fix_bg=False, для второго («после») — fix_bg=True
    run_lesson_29(fix_bg=True)