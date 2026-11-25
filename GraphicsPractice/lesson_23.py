import os
from PIL import Image, ImageDraw, ImageFilter

os.makedirs("source", exist_ok=True)
os.makedirs("output", exist_ok=True)


def get_or_create_source_image(path="source/filter_sample.png"):
    """
    Использует существующее изображение из проекта или создаёт тестовый кадр
    с чёткими контурами и деталями, если подходящего файла ещё нет.
    """
    candidates = [
        path,
        "source/sample_photo.png",
        "source/photo_200.png",
        "output/shapes.png",
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    img = Image.new("RGB", (600, 400), (241, 245, 249))
    d = ImageDraw.Draw(img)
    d.rectangle((40, 40, 240, 190), fill=(37, 99, 235), outline=(15, 23, 42), width=3)
    d.ellipse((320, 45, 520, 195), fill=(239, 68, 68), outline=(127, 29, 29), width=3)
    d.polygon([(140, 350), (300, 210), (460, 350)], fill=(34, 197, 94), outline=(20, 83, 45))
    d.line((40, 260, 560, 260), fill=(245, 158, 11), width=5)
    img.save(path, format="PNG")
    return path


def apply_filters_23_1(src_path, radius=5):
    """
    Задача 23.1: применяет BLUR, SHARPEN, CONTOUR, EDGE_ENHANCE и GaussianBlur(radius)
    к одному изображению и сохраняет результаты.
    """
    with Image.open(src_path) as raw:
        img = raw.convert("RGB")

    img.save("output/filter_0_original.png", format="PNG")

    filters = {
        "BLUR": ImageFilter.BLUR,
        "SHARPEN": ImageFilter.SHARPEN,
        "CONTOUR": ImageFilter.CONTOUR,
        "EDGE_ENHANCE": ImageFilter.EDGE_ENHANCE,
        f"GaussianBlur_{radius}": ImageFilter.GaussianBlur(radius),
    }

    for name, flt in filters.items():
        result = img.filter(flt)
        out_path = f"output/filter_{name.lower()}.png"
        result.save(out_path, format="PNG")
        print(f"[23.1] Применён {name} -> {out_path}")


if __name__ == "__main__":
    source_file = get_or_create_source_image()
    print(f"Исходное изображение: {source_file}")
    apply_filters_23_1(source_file, radius=5)