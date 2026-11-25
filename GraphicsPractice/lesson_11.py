import os
from PIL import Image

os.makedirs("output", exist_ok=True)

source_path = "source/фото.jpg"
base_name = "output/format_test"

with Image.open(source_path) as img:
    # Приводим к RGB для корректного сохранения во всех перечисленных форматах
    rgb_img = img.convert("RGB")

    saved_files = {
        "PNG": f"{base_name}.png",
        "JPG (quality=90)": f"{base_name}.jpg",
        "BMP": f"{base_name}.bmp",
        "GIF": f"{base_name}.gif",
    }

    rgb_img.save(saved_files["PNG"], format="PNG")
    rgb_img.save(saved_files["JPG (quality=90)"], format="JPEG", quality=90)
    rgb_img.save(saved_files["BMP"], format="BMP")
    # GIF поддерживает палитру до 256 цветов; адаптивная палитра сохраняет больше оттенков
    rgb_img.convert("P", palette=Image.Palette.ADAPTIVE).save(saved_files["GIF"], format="GIF")

    print(f"{'Формат':<20} {'Вес, КБ':>10}")
    print("-" * 32)
    for label, path in saved_files.items():
        size_kb = os.path.getsize(path) / 1024
        print(f"{label:<20} {size_kb:>10.2f}")