import os
from PIL import Image, ImageDraw

os.makedirs("source", exist_ok=True)
os.makedirs("output", exist_ok=True)


def get_or_create_source_image(path="source/window_bg.png"):
    """
    Берёт существующее изображение из проекта или создаёт тестовый фоновый кадр 800x600.
    """
    candidates = [
        path,
        "output/bg_gradient_800x600.png",
        "output/bg_blurred_800x600_r8.png",
        "source/sample_photo.png",
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate

    img = Image.new("RGB", (800, 600), (30, 64, 175))
    d = ImageDraw.Draw(img)
    for y in range(600):
        t = y / 599
        r = int(round(15 + (125 - 15) * t))
        g = int(round(23 + (211 - 23) * t))
        b = int(round(42 + (252 - 42) * t))
        d.line([(0, y), (799, y)], fill=(r, g, b))
    d.ellipse((520, 90, 720, 290), fill=(56, 189, 248))
    d.rounded_rectangle((80, 360, 460, 520), radius=24, fill=(29, 78, 216))
    img.save(path, format="PNG")
    return path


def task_25_1_jpg_qualities(src_path):
    """
    Задача 25.1: сохранение изображения в JPG с качеством 95, 85, 70, 50, 30
    и вывод размеров файлов для сравнения.
    """
    with Image.open(src_path) as raw:
        rgb_img = raw.convert("RGB")

    print("[25.1] Сравнение качества JPG:")
    for q in (95, 85, 70, 50, 30):
        out_path = f"output/bg_q{q}.jpg"
        rgb_img.save(out_path, format="JPEG", quality=q, optimize=True)
        size_kb = round(os.path.getsize(out_path) / 1024, 1)
        print(f"  quality={q:2d} -> {out_path} ({size_kb} КБ)")


def task_25_2_png_optimization_and_quantize(src_path):
    """
    Задача 25.2: сохранение PNG с optimize=False и optimize=True,
    а также уменьшение числа цветов через img.quantize(colors=64).
    """
    with Image.open(src_path) as raw:
        img = raw.convert("RGB")

    no_opt_path = "output/opt_no_optimize.png"
    with_opt_path = "output/opt_with_optimize.png"
    quant_path = "output/opt_quant_64.png"

    img.save(no_opt_path, format="PNG", optimize=False)
    img.save(with_opt_path, format="PNG", optimize=True)

    quantized = img.quantize(colors=64, method=Image.Quantize.MEDIANCUT)
    quantized.save(quant_path, format="PNG", optimize=True)

    print("[25.2] Сравнение PNG:")
    for label, p in [
        ("Без optimize (optimize=False)", no_opt_path),
        ("С optimize (optimize=True)", with_opt_path),
        ("Квантование 64 цвета (quantize)", quant_path),
    ]:
        size_kb = round(os.path.getsize(p) / 1024, 1)
        print(f"  {label}: {p} ({size_kb} КБ)")


if __name__ == "__main__":
    source_file = get_or_create_source_image()
    print(f"Исходный файл: {source_file}")
    task_25_1_jpg_qualities(source_file)
    task_25_2_png_optimization_and_quantize(source_file)