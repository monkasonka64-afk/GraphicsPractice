import os
from PIL import Image

SUPPORTED_FORMATS = {
    "PNG": ".png",
    "JPG": ".jpg",
    "JPEG": ".jpg",
    "BMP": ".bmp",
    "GIF": ".gif",
}


def convert_image(src: str, dst_format: str, output_dir: str = "output") -> str:
    """
    Конвертирует изображение src в допустимый формат dst_format и сохраняет в output_dir.
    Возвращает путь к сохранённому файлу.
    """
    if not isinstance(dst_format, str) or not dst_format.strip():
        raise ValueError("Целевой формат не должен быть пустым.")

    normalized_fmt = dst_format.strip().upper()
    if normalized_fmt not in SUPPORTED_FORMATS:
        allowed = ", ".join(sorted(SUPPORTED_FORMATS.keys()))
        raise ValueError(f"Недопустимый формат '{dst_format}'. Разрешены: {allowed}")

    if not os.path.exists(src):
        raise FileNotFoundError(f"Исходный файл не найден: '{src}'")

    os.makedirs(output_dir, exist_ok=True)

    pil_format = "JPEG" if normalized_fmt in ("JPG", "JPEG") else normalized_fmt
    ext = SUPPORTED_FORMATS[normalized_fmt]
    base_name = os.path.splitext(os.path.basename(src))[0]
    dst_path = os.path.join(output_dir, f"{base_name}_converted{ext}")

    with Image.open(src) as img:
        has_alpha = img.mode in ("RGBA", "LA") or (
            img.mode == "P" and "transparency" in img.info
        )

        if pil_format == "JPEG":
            if has_alpha:
                rgba = img.convert("RGBA")
                canvas = Image.new("RGB", rgba.size, (255, 255, 255))
                canvas.paste(rgba.convert("RGB"), (0, 0), mask=rgba.split()[3])
                canvas.save(dst_path, format="JPEG", quality=90)
            else:
                img.convert("RGB").save(dst_path, format="JPEG", quality=90)

        elif pil_format == "BMP":
            if has_alpha:
                rgba = img.convert("RGBA")
                canvas = Image.new("RGB", rgba.size, (255, 255, 255))
                canvas.paste(rgba.convert("RGB"), (0, 0), mask=rgba.split()[3])
                canvas.save(dst_path, format="BMP")
            else:
                img.convert("RGB").save(dst_path, format="BMP")

        elif pil_format == "GIF":
            if has_alpha:
                rgba = img.convert("RGBA")
                # Переводим альфа-канал в бинарную маску для корректного GIF
                alpha = rgba.split()[3]
                paletted = rgba.convert("RGB").convert(
                    "P", palette=Image.Palette.ADAPTIVE, colors=255
                )
                paletted.save(dst_path, format="GIF")
            else:
                img.convert("RGB").convert(
                    "P", palette=Image.Palette.ADAPTIVE, colors=256
                ).save(dst_path, format="GIF")

        elif pil_format == "PNG":
            if has_alpha:
                img.convert("RGBA").save(dst_path, format="PNG")
            else:
                img.convert("RGB").save(dst_path, format="PNG")

    return dst_path


if __name__ == "__main__":
    test_cases = [
        ("source/фото.jpg", "PNG"),
        ("output/rotate_45.png", "JPG"),
        ("source/фото.jpg", "BMP"),
        ("source/фото.jpg", "GIF"),
    ]

    for src_file, target_fmt in test_cases:
        if os.path.exists(src_file):
            saved = convert_image(src_file, target_fmt)
            print(f"[OK] {src_file} -> {target_fmt}: сохранён '{saved}'")
        else:
            print(f"[SKIP] Файл '{src_file}' отсутствует")

    # Проверка реакции на недопустимый формат
    try:
        convert_image("source/фото.jpg", "WEBP")
    except ValueError as err:
        print(f"[CHECK] Ожидаемая ошибка валидации: {err}")