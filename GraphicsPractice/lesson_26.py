import csv
import os
from PIL import Image, ImageDraw

os.makedirs("source", exist_ok=True)
os.makedirs("assets", exist_ok=True)
os.makedirs("output", exist_ok=True)

IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".webp")


def ensure_source_files(src_dir="source"):
    """
    Если в папке source ещё нет файлов, создаёт пару тестовых изображений
    (тяжёлый несжатый/слабо сжатый BMP и PNG) для наглядной проверки.
    """
    existing = [
        f for f in os.listdir(src_dir)
        if os.path.isfile(os.path.join(src_dir, f)) and f.lower().endswith(IMAGE_EXTS)
    ]
    if existing:
        return

    bmp_path = os.path.join(src_dir, "raw_banner.bmp")
    img1 = Image.new("RGB", (600, 300), (226, 232, 240))
    d1 = ImageDraw.Draw(img1)
    d1.rectangle((20, 20, 580, 280), fill=(37, 99, 235))
    d1.ellipse((80, 50, 220, 190), fill=(250, 204, 21))
    d1.text((250, 120), "BANNER SAMPLE", fill=(255, 255, 255))
    img1.save(bmp_path, format="BMP")

    png_path = os.path.join(src_dir, "already_compact.png")
    img2 = Image.new("RGB", (200, 120), (15, 23, 42))
    d2 = ImageDraw.Draw(img2)
    d2.rectangle((20, 20, 180, 100), fill=(14, 165, 233))
    img2.save(png_path, format="PNG", optimize=True)


def optimize_image_file(src_path, dst_path):
    """
    Оптимизирует изображение и сохраняет результат в dst_path.
    - Для фото/крупных кадров (без прозрачности) сохраняет в JPEG quality=82, optimize=True
      (с расширением .jpg).
    - Для изображений с прозрачностью сохраняет в PNG с optimize=True.
    """
    ext = os.path.splitext(src_path)[1].lower()
    with Image.open(src_path) as raw:
        has_alpha = raw.mode in ("RGBA", "LA") or ("transparency" in raw.info)

        if has_alpha:
            base_name = os.path.splitext(os.path.basename(src_path))[0]
            final_dst = os.path.join(os.path.dirname(dst_path), f"{base_name}.png")
            img = raw.convert("RGBA")
            img.save(final_dst, format="PNG", optimize=True)
            return final_dst

        if ext in (".jpg", ".jpeg"):
            final_dst = dst_path
            img = raw.convert("RGB")
            img.save(final_dst, format="JPEG", quality=82, optimize=True)
            return final_dst

        # Для BMP и тяжёлых RGB-изображений оптимизированный JPG даёт заметную экономию,
        # но если сжатый файл вдруг оказался больше исходника — сохраняем оптимизированный PNG.
        base_name = os.path.splitext(os.path.basename(src_path))[0]
        jpg_candidate = os.path.join(os.path.dirname(dst_path), f"{base_name}.jpg")
        png_candidate = os.path.join(os.path.dirname(dst_path), f"{base_name}.png")

        rgb = raw.convert("RGB")
        rgb.save(jpg_candidate, format="JPEG", quality=82, optimize=True)
        rgb.save(png_candidate, format="PNG", optimize=True)

        src_size = os.path.getsize(src_path)
        jpg_size = os.path.getsize(jpg_candidate)
        png_size = os.path.getsize(png_candidate)

        if jpg_size <= png_size:
            if os.path.exists(png_candidate):
                os.remove(png_candidate)
            return jpg_candidate
        else:
            if os.path.exists(jpg_candidate):
                os.remove(jpg_candidate)
            return png_candidate


def explain_lowest_saving(row):
    """Формирует объяснение причины наименьшей экономии для выбранного файла."""
    if row["saving_pct"] <= 0:
        return (
            "файл уже хорошо сжат (например, оптимизированный PNG/JPG с малой цветовой палитрой "
            "или небольшим разрешением), поэтому повторное сжатие не уменьшило его размер."
        )
    if row["saving_pct"] < 15:
        return (
            "исходный файл уже был сжат алгоритмами PNG/JPG, поэтому дополнительная оптимизация "
            "дала лишь небольшой выигрыш."
        )
    return (
        "все файлы сжалиcь достаточно сильно; у данного файла меньше всего лишних метаданных "
        "и мелких деталей."
    )


def run_lesson_26(src_dir="source", dst_dir="assets", csv_path="output/optimization.csv"):
    ensure_source_files(src_dir)

    files = sorted(
        f for f in os.listdir(src_dir)
        if os.path.isfile(os.path.join(src_dir, f)) and f.lower().endswith(IMAGE_EXTS)
    )

    if not files:
        print("В папке source нет изображений для обработки.")
        return

    rows = []
    for fname in files:
        src_path = os.path.join(src_dir, fname)
        planned_dst = os.path.join(dst_dir, fname)
        final_dst = optimize_image_file(src_path, planned_dst)

        size_before_bytes = os.path.getsize(src_path)
        size_after_bytes = os.path.getsize(final_dst)

        before_kb = round(size_before_bytes / 1024, 2)
        after_kb = round(size_after_bytes / 1024, 2)

        if size_before_bytes > 0:
            saving_pct = round((size_before_bytes - size_after_bytes) / size_before_bytes * 100, 1)
        else:
            saving_pct = 0.0

        rows.append({
            "file": fname,
            "out_file": os.path.basename(final_dst),
            "before_kb": before_kb,
            "after_kb": after_kb,
            "saving_pct": saving_pct,
        })

    # Задача 26.1: вывод таблицы в консоль
    print("\n[26.1] Таблица результатов оптимизации (source -> assets):")
    print(f"{'Файл':<26} | {'Размер до, КБ':>13} | {'Размер после, КБ':>16} | {'Экономия, %':>11}")
    print("-" * 76)
    for r in rows:
        print(f"{r['file']:<26} | {r['before_kb']:>13.2f} | {r['after_kb']:>16.2f} | {r['saving_pct']:>10.1f}%")

    # Задача 26.2: сохранение таблицы в CSV модулем csv
    with open(csv_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["Файл", "Размер до, КБ", "Размер после, КБ", "Экономия, %"])
        for r in rows:
            writer.writerow([r["file"], r["before_kb"], r["after_kb"], r["saving_pct"]])

    print(f"\n[26.2] Таблица сохранена в CSV: {csv_path}")

    # Задача 26.3: файл с наименьшей экономией и объяснение
    min_row = min(rows, key=lambda item: item["saving_pct"])
    reason = explain_lowest_saving(min_row)
    print(
        f"\n[26.3] Наименьшая экономия у файла '{min_row['file']}' "
        f"({min_row['saving_pct']}%: {min_row['before_kb']} КБ -> {min_row['after_kb']} КБ): "
        f"{reason}"
    )


if __name__ == "__main__":
    run_lesson_26()