import os
from PIL import Image, ImageDraw, ImageOps

os.makedirs("source", exist_ok=True)
os.makedirs("output", exist_ok=True)


def get_or_create_source_photo(path="source/photo_200.png"):
    """
    Возвращает путь к исходному изображению или создаёт тестовый кадр 200x200,
    если файл ещё не подготовлен.
    """
    candidates = [
        path,
        "source/logo.png",
        "output/shapes.png",
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    img = Image.new("RGB", (200, 200), (226, 232, 240))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, 200, 120), fill=(59, 130, 246))
    d.ellipse((135, 25, 175, 65), fill=(250, 204, 21))
    d.polygon([(0, 200), (70, 95), (145, 200)], fill=(34, 197, 94))
    d.polygon([(95, 200), (165, 115), (220, 200)], fill=(21, 128, 61))
    img.save(path, format="PNG")
    return path


def task_20_1_rounded_photo(src_path, dst="output/rounded.png", radius=30):
    """Задача 20.1: скругление углов изображения 200x200 с помощью маски."""
    with Image.open(src_path) as raw:
        img = ImageOps.fit(raw.convert("RGBA"), (200, 200), method=Image.Resampling.LANCZOS)

    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, *img.size), radius=radius, fill=255)
    img.putalpha(mask)

    img.save(dst, format="PNG")
    print(f"[20.1] Сохранено: {dst}")
    return img


def task_20_2_circular_avatar(src_path, dst="output/avatar_96.png", size=(96, 96)):
    """Задача 20.2: круглый аватар 96x96 по маске-эллипсу."""
    with Image.open(src_path) as raw:
        avatar = ImageOps.fit(raw.convert("RGBA"), size, method=Image.Resampling.LANCZOS)

    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size[0] - 1, size[1] - 1), fill=255)
    avatar.putalpha(mask)

    avatar.save(dst, format="PNG")
    print(f"[20.2] Сохранено: {dst}")
    return avatar


def task_20_3_bordered_rounded(
    src_path,
    dst="output/rounded_bordered.png",
    radius=30,
    border_width=2,
    border_color=(52, 152, 219, 255),
):
    """
    Задача 20.3: добавляет тонкую рамку (2 px) вокруг скруглённого изображения,
    согласованную с палитрой кнопок/баннера интерфейса.
    """
    rounded = task_20_1_rounded_photo(src_path, dst="output/rounded.png", radius=radius).copy()
    draw = ImageDraw.Draw(rounded)
    w, h = rounded.size

    # Смещаем контур на половину толщины рамки, чтобы 2 px не обрезались по краю
    inset = border_width / 2
    draw.rounded_rectangle(
        (inset, inset, w - 1 - inset, h - 1 - inset),
        radius=max(1, radius - border_width // 2),
        outline=border_color,
        width=border_width,
    )

    rounded.save(dst, format="PNG")
    print(f"[20.3] Сохранено: {dst}")
    return rounded


if __name__ == "__main__":
    source_file = get_or_create_source_photo()
    print(f"Исходный файл: {source_file}")

    task_20_1_rounded_photo(source_file)
    task_20_2_circular_avatar(source_file)
    # Цвет (52, 152, 219, 255) взят из базовой палитры элементов интерфейса
    task_20_3_bordered_rounded(
        source_file,
        radius=30,
        border_width=2,
        border_color=(52, 152, 219, 255),
    )