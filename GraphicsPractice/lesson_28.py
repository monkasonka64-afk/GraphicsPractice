import os
import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

os.makedirs("assets/icons", exist_ok=True)
os.makedirs("output", exist_ok=True)


def ensure_header_logo(path="assets/logo_header.png"):
    """Возвращает путь к логотипу шапки или создаёт резервное изображение."""
    if os.path.exists(path):
        return path

    img = Image.new("RGBA", (220, 80), (37, 99, 235, 255))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((4, 4, 215, 75), radius=14, outline=(255, 255, 255, 255), width=2)
    d.text((28, 30), "ГРАФМАСТЕР UI", fill=(255, 255, 255, 255))
    img.save(path, format="PNG")
    return path


def get_thumbnail_sources(count=3):
    """Собирает до 3 изображений для миниатюр из проекта или создаёт временные."""
    candidates = [
        "assets/icons/home.png",
        "assets/icons/settings.png",
        "assets/icons/user.png",
        "output/bg_q85.jpg",
        "output/style_sheet_800x500.png",
    ]
    found = [p for p in candidates if os.path.exists(p)]
    while len(found) < count:
        idx = len(found) + 1
        fallback = f"output/thumb_fallback_{idx}.png"
        if not os.path.exists(fallback):
            img = Image.new("RGBA", (120, 120), (29 + idx * 20, 78 + idx * 25, 216, 255))
            d = ImageDraw.Draw(img)
            d.text((34, 52), f"IMG {idx}", fill=(255, 255, 255, 255))
            img.save(fallback, format="PNG")
        found.append(fallback)
    return found[:count]


def run_lesson_28():
    root = tk.Tk()
    root.title("Практика РО 5.2")
    root.geometry("800x600")
    root.configure(bg="#F8FAFC")

    # Задача 28.1: вывод основного изображения через Label
    logo_path = ensure_header_logo("assets/logo_header.png")
    with Image.open(logo_path) as raw_logo:
        photo = ImageTk.PhotoImage(raw_logo)

    header_label = tk.Label(root, image=photo, bg="#F8FAFC")
    header_label.image = photo  # храним ссылку, иначе картинка исчезнет
    header_label.pack(pady=(24, 16))

    tk.Label(
        root,
        text="Миниатюры ассетов (3 в ряд)",
        font=("Segoe UI", 12, "bold"),
        bg="#F8FAFC",
        fg="#0F172A",
    ).pack(pady=(8, 8))

    # Задача 28.3: 3 миниатюры в ряд через Frame и цикл
    thumbs_frame = tk.Frame(root, bg="#FFFFFF", padx=12, pady=12, highlightbackground="#CBD5E1", highlightthickness=1)
    thumbs_frame.pack(pady=10)

    thumb_paths = get_thumbnail_sources(count=3)
    for path in thumb_paths:
        with Image.open(path) as raw_thumb:
            resized = raw_thumb.copy()
            resized.thumbnail((96, 96), resample=Image.Resampling.LANCZOS)
            thumb_photo = ImageTk.PhotoImage(resized)

        item_box = tk.Frame(thumbs_frame, bg="#FFFFFF", padx=10)
        item_box.pack(side=tk.LEFT)

        img_lbl = tk.Label(item_box, image=thumb_photo, bg="#FFFFFF")
        img_lbl.image = thumb_photo  # сохраняем ссылку на каждый объект PhotoImage
        img_lbl.pack()

        tk.Label(
            item_box,
            text=os.path.basename(path),
            font=("Segoe UI", 9),
            bg="#FFFFFF",
            fg="#334155",
        ).pack(pady=(4, 0))

    root.mainloop()


if __name__ == "__main__":
    run_lesson_28()