import csv
import os

os.makedirs("output", exist_ok=True)
csv_path = "output/optimization.csv"

src_dir = "source"
dst_dir = "assets"
image_exts = (".png", ".jpg", ".jpeg", ".bmp", ".webp")

rows = []
if os.path.isdir(src_dir):
    for fname in sorted(os.listdir(src_dir)):
        src_path = os.path.join(src_dir, fname)
        if not (os.path.isfile(src_path) and fname.lower().endswith(image_exts)):
            continue

        # Ищем оптимизированный файл в assets (с тем же именем или с расширением .jpg/.png)
        base_name = os.path.splitext(fname)[0]
        candidates = [
            os.path.join(dst_dir, fname),
            os.path.join(dst_dir, f"{base_name}.jpg"),
            os.path.join(dst_dir, f"{base_name}.png"),
        ]
        dst_path = next((p for p in candidates if os.path.exists(p)), None)
        if dst_path is None:
            continue

        before_bytes = os.path.getsize(src_path)
        after_bytes = os.path.getsize(dst_path)

        before_kb = round(before_bytes / 1024, 2)
        after_kb = round(after_bytes / 1024, 2)
        saving_pct = round((before_bytes - after_bytes) / before_bytes * 100, 1) if before_bytes > 0 else 0.0

        rows.append({
            "file": fname,
            "before_kb": before_kb,
            "after_kb": after_kb,
            "saving_pct": saving_pct,
        })

with open(csv_path, mode="w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["Файл", "Размер до, КБ", "Размер после, КБ", "Экономия, %"])
    for r in rows:
        writer.writerow([r["file"], r["before_kb"], r["after_kb"], r["saving_pct"]])

print(f"Сохранено строк: {len(rows)} -> {csv_path}")