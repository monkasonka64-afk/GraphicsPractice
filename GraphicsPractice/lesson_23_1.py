from PIL import ImageDraw, ImageFont, ImageOps


def load_font(size=16):
    """Загружает Arial из системной папки Windows или возвращает шрифт по умолчанию."""
    font_path = "C:/Windows/Fonts/arial.ttf"
    if os.path.exists(font_path):
        return ImageFont.truetype(font_path, size)
    return ImageFont.load_default()


def task_23_2_blurred_window_bg(src_path, dst="output/bg_blurred_800x600_r8.png"):
    """
    Задача 23.2: фото, увеличенное до 800x600 и размытое с радиусом 8.
    """
    with Image.open(src_path) as raw:
        img = raw.convert("RGB")

    # Увеличиваем/подгоняем до 800x600 и применяем GaussianBlur с радиусом 8
    resized = img.resize((800, 600), resample=Image.Resampling.LANCZOS)
    blurred_bg = resized.filter(ImageFilter.GaussianBlur(8))

    blurred_bg.save(dst, format="PNG")
    print(f"[23.2] Сохранён размытый фон 800x600 (radius=8): {dst}")
    return blurred_bg


def task_23_3_sharpen_after_downscale(
    src_path,
    target_size=(32, 32),
    dst_raw="output/icon_downscaled_32.png",
    dst_sharp="output/icon_downscaled_32_sharpen.png",
    dst_compare="output/icon_sharpen_compare.png",
):
    """
    Задача 23.3: после уменьшения иконки применяет SHARPEN
    и сохраняет изображение для сравнения резкости с исходным уменьшенным вариантом.
    """
    icon_candidates = [
        "assets/icons/home.png",
        "assets/icons/settings.png",
        src_path,
    ]
    chosen = next((p for p in icon_candidates if os.path.exists(p)), src_path)

    with Image.open(chosen) as raw:
        base_img = raw.convert("RGBA")

    # Уменьшаем иконку до target_size
    downscaled = base_img.resize(target_size, resample=Image.Resampling.LANCZOS)
    downscaled.save(dst_raw, format="PNG")

    # Применяем SHARPEN после уменьшения
    sharpened = downscaled.filter(ImageFilter.SHARPEN)
    sharpened.save(dst_sharp, format="PNG")

    # Собираем наглядное сравнение (увеличенные копии для удобства осмотра + оригинал 32x32)
    zoom_size = (160, 160)
    left_zoom = downscaled.resize(zoom_size, resample=Image.Resampling.NEAREST)
    right_zoom = sharpened.resize(zoom_size, resample=Image.Resampling.NEAREST)

    pad = 20
    header_h = 34
    canvas = Image.new("RGB", (pad * 3 + zoom_size[0] * 2, pad * 2 + header_h + zoom_size[1]), (241, 245, 249))
    draw = ImageDraw.Draw(canvas)
    font = load_font(16)

    draw.text((pad, pad), f"Уменьшенная ({target_size[0]}x{target_size[1]}) без SHARPEN", fill=(15, 23, 42), font=font)
    draw.text((pad * 2 + zoom_size[0], pad), f"Уменьшенная ({target_size[0]}x{target_size[1]}) + SHARPEN", fill=(15, 23, 42), font=font)

    top_y = pad + header_h
    canvas.paste(left_zoom.convert("RGB"), (pad, top_y))
    canvas.paste(right_zoom.convert("RGB"), (pad * 2 + zoom_size[0], top_y))
    draw.rectangle((pad, top_y, pad + zoom_size[0] - 1, top_y + zoom_size[1] - 1), outline=(148, 163, 184))
    draw.rectangle((pad * 2 + zoom_size[0], top_y, pad * 2 + zoom_size[0] * 2 - 1, top_y + zoom_size[1] - 1), outline=(148, 163, 184))

    canvas.save(dst_compare, format="PNG")
    print(f"[23.3] Сохранены {dst_raw}, {dst_sharp} и сравнение {dst_compare}")


if __name__ == "__main__":
    source_file = get_or_create_source_image()
    print(f"Исходное изображение: {source_file}")
    apply_filters_23_1(source_file, radius=5)
    task_23_2_blurred_window_bg(source_file)
    task_23_3_sharpen_after_downscale(source_file, target_size=(32, 32))