import os
import time
from PIL import Image

SRC_DIR = "source"
DST_DIR = "output/batch"
TARGET_SIZE = (256, 256)


def batch_process(src_dir: str = SRC_DIR, dst_dir: str = DST_DIR) -> None:
    start_time = time.perf_counter()

    if not os.path.isdir(src_dir):
        print(f"Папка '{src_dir}' не найдена.")
        return

    os.makedirs(dst_dir, exist_ok=True)

    # Берём только файлы из директории source (без подпапок)
    entries = sorted(
        name for name in os.listdir(src_dir)
        if os.path.isfile(os.path.join(src_dir, name))
    )
    total = len(entries)

    if total == 0:
        print(f"В папке '{src_dir}' нет файлов для обработки.")
        return

    processed = 0

    for name in entries:
        src_path = os.path.join(src_dir, name)
        stem, _ = os.path.splitext(name)
        dst_path = os.path.join(dst_dir, f"{stem}_256.png")

        try:
            with Image.open(src_path) as raw_img:
                img = raw_img.convert("RGBA")
                img.thumbnail(TARGET_SIZE, Image.Resampling.LANCZOS)
                img.save(dst_path, format="PNG")

            processed += 1
            print(f"Обработано {processed} из {total}")
        except OSError:
            print(f"Пропущен: {name}")

    elapsed = time.perf_counter() - start_time
    print(f"Готово. Успешно обработано: {processed} из {total}. Время работы: {elapsed:.4f} с")


if __name__ == "__main__":
    batch_process()