import os
from PIL import Image

os.makedirs("output", exist_ok=True)


def remove_white_background(
    src: str,
    dst: str = "output/logo_transparent.png",
    threshold: int = 235,
) -> Image.Image:
    """
    Делает прозрачными пиксели, у которых R, G и B превышают порог threshold.
    Возвращает объект Image в режиме RGBA.
    """
    if not (0 <= threshold <= 255):
        raise ValueError("Параметр threshold должен находиться в диапазоне от 0 до 255.")

    with Image.open(src) as raw_img:
        img = raw_img.convert("RGBA")
        new_data = []

        for r, g, b, a in img.getdata():
            if r > threshold and g > threshold and b > threshold:
                new_data.append((r, g, b, 0))
            else:
                new_data.append((r, g, b, a))

        img.putdata(new_data)
        img.save(dst, format="PNG")
        return img.copy()


def test_on_backgrounds(
    logo_img: Image.Image,
    output_dir: str = "output",
) -> None:
    """
    Накладывает логотип с альфа-каналом на красный, синий и чёрный фоны
    и сохраняет три отдельных изображения.
    """
    backgrounds = {
        "red": (220, 30, 30, 255),
        "blue": (30, 90, 220, 255),
        "black": (0, 0, 0, 255),
    }

    for name, color in backgrounds.items():
        bg = Image.new("RGBA", logo_img.size, color)
        composited = Image.alpha_composite(bg, logo_img)
        out_path = os.path.join(output_dir, f"logo_on_{name}.png")
        composited.save(out_path, format="PNG")
        print(f"Сохранён вариант на {name} фоне: {out_path}")


if __name__ == "__main__":
    src_logo = "source/без фона.jpg"
    transparent_path = "output/logo_transparent.png"
    chosen_threshold = 235

    if os.path.exists(src_logo):
        logo_rgba = remove_white_background(
            src=src_logo,
            dst=transparent_path,
            threshold=chosen_threshold,
        )
        print(
            f"Фон удалён (threshold={chosen_threshold}), "
            f"сохранено: {transparent_path}"
        )
        test_on_backgrounds(logo_rgba)
    else:
        print(f"Файл '{src_logo}' не найден. Проверьте путь к исходному изображению.")