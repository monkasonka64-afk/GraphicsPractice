import os
from PIL import Image

os.makedirs("assets/icons", exist_ok=True)
os.makedirs("output", exist_ok=True)

ICON_NAMES = ["home", "settings", "user", "search", "exit"]
ICON_SIZE = 48


def build_sprite(icon_names=ICON_NAMES, size=ICON_SIZE, dst="assets/sprite.png"):
    """
    Задача 27.1: склеивает 5 иконок 48×48 в один файл-спрайт 240×48.
    """
    sheet = Image.new("RGBA", (size * len(icon_names), size), (0, 0, 0, 0))
    for i, name in enumerate(icon_names):
        icon_path = f"assets/icons/{name}.png"
        with Image.open(icon_path) as raw:
            icon = raw.convert("RGBA")
            if icon.size != (size, size):
                icon = icon.resize((size, size), resample=Image.Resampling.LANCZOS)
            sheet.paste(icon, (i * size, 0), icon)

    sheet.save(dst, format="PNG")
    print(f"[27.1] Спрайт сохранён: {dst} ({sheet.width}×{sheet.height})")
    return sheet


def get_icon(sheet, index, size=ICON_SIZE):
    """
    Задача 27.2: вырезает нужную иконку из горизонтального спрайта через crop.
    """
    max_index = sheet.width // size - 1
    if index < 0 or index > max_index:
        raise IndexError(f"Индекс {index} вне диапазона [0..{max_index}]")

    left = index * size
    box = (left, 0, left + size, size)
    return sheet.crop(box)


if __name__ == "__main__":
    sprite_sheet = build_sprite()

    # Проверка Задачи 27.2: извлекаем иконку по индексу (например, index=2 -> 'user')
    test_index = 2
    extracted = get_icon(sprite_sheet, index=test_index, size=ICON_SIZE)
    test_out = f"output/sprite_extracted_{ICON_NAMES[test_index]}.png"
    extracted.save(test_out, format="PNG")
    print(
        f"[27.2] Извлечена иконка index={test_index} ('{ICON_NAMES[test_index]}') "
        f"размером {extracted.size} -> {test_out}"
    )