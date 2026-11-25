import os
from PIL import Image

os.makedirs("assets", exist_ok=True)

ICO_SIZES = [
    (16, 16),
    (32, 32),
    (48, 48),
    (64, 64),
    (128, 128),
    (256, 256),
]


def make_square_rgba(img: Image.Image) -> Image.Image:
    """
    Если изображение не квадратное, вписывает его по центру в квадратный
    прозрачный холст (RGBA) с сохранением пропорций.
    """
    rgba = img.convert("RGBA")
    width, height = rgba.size

    if width == height:
        return rgba

    side = max(width, height)
    square_canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    offset_x = (side - width) // 2
    offset_y = (side - height) // 2
    square_canvas.paste(rgba, (offset_x, offset_y), mask=rgba.getchannel("A"))
    return square_canvas


def build_ico(
    src: str,
    dst: str = "assets/app.ico",
    sizes: list[tuple[int, int]] = ICO_SIZES,
) -> None:
    with Image.open(src) as raw_img:
        square_img = make_square_rgba(raw_img)
        # При сохранении в ICO Pillow масштабирует исходник под каждый размер из sizes
        square_img.save(dst, format="ICO", sizes=sizes)

    # Открываем созданный ICO и проверяем доступные размеры
    with Image.open(dst) as ico_img:
        print(f"Файл иконки сохранён: {dst}")
        print(f"Режим: {ico_img.mode}, текущий размер: {ico_img.size}")
        print("Доступные размеры (img.info.get('sizes')):", ico_img.info.get("sizes"))


if __name__ == "__main__":
    # Подбираем доступный исходный файл (приоритет — logo.png / без фона / rotate_45.png)
    candidates = [
        "source/logo.png",
        "output/logo_transparent.png",
        "source/без фона.jpg",
        "output/rotate_45.png",
    ]
    src_path = next((p for p in candidates if os.path.exists(p)), None)

    if src_path:
        print(f"Используется исходный файл: {src_path}")
        build_ico(src_path, "assets/app.ico", ICO_SIZES)
    else:
        print("Исходное изображение не найдено. Укажите путь к файлу в src_path.")