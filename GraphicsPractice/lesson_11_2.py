import os
from PIL import Image

os.makedirs("output", exist_ok=True)

# Берём PNG с прозрачностью (например, rotate_45.png из урока 10)
rgba_path = "output/rotate_45.png"
fixed_jpg_path = "output/rotate_45_white_bg.jpg"

with Image.open(rgba_path) as raw_img:
    rgba_img = raw_img.convert("RGBA")

    # 1. Воспроизводим ошибку прямого сохранения RGBA в JPG
    try:
        rgba_img.save("output/error_test.jpg", format="JPEG")
    except OSError as err:
        print(f"Ошибка при сохранении RGBA в JPG: {err}")

    # 2. Исправляем через белый фон ("RGB") и альфа-канал как маску
    white_bg = Image.new("RGB", rgba_img.size, (255, 255, 255))
    alpha_mask = rgba_img.split()[3]
    white_bg.paste(rgba_img.convert("RGB"), (0, 0), mask=alpha_mask)

    white_bg.save(fixed_jpg_path, format="JPEG", quality=90)
    print(f"Исправленный файл сохранён: {fixed_jpg_path}")