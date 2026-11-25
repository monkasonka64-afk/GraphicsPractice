import os
from PIL import Image, ImageDraw

os.makedirs("output", exist_ok=True)


def draw_shapes(dst: str = "output/shapes.png") -> None:
    """Задача 16.1: холст 300x300 с прямоугольником, эллипсом, линией и многоугольником."""
    img = Image.new("RGBA", (300, 300), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)

    d.rectangle((20, 20, 140, 140), fill=(52, 152, 219), outline="black", width=3)
    d.ellipse((160, 20, 280, 140), fill=(231, 76, 60))
    d.line((20, 200, 280, 280), fill="green", width=5)
    d.polygon([(150, 160), (200, 250), (100, 250)], fill=(241, 196, 15))

    img.save(dst, format="PNG")
    print(f"[16.1] Сохранено: {dst}")


def draw_home_icon(dst: str = "output/icon_home_64.png") -> None:
    """Задача 16.2: иконка 'Домой' (квадрат и крыша-треугольник) 64x64 на прозрачном фоне."""
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Крыша (треугольник)
    d.polygon([(32, 10), (8, 32), (56, 32)], fill=(231, 76, 60), outline=(44, 62, 80))
    # Основание домика (квадрат)
    d.rectangle((16, 32, 48, 56), fill=(52, 152, 219), outline=(44, 62, 80), width=2)
    # Небольшая дверь по центру
    d.rectangle((28, 42, 36, 56), fill=(241, 196, 15), outline=(44, 62, 80), width=1)

    img.save(dst, format="PNG")
    print(f"[16.2] Сохранено: {dst}")


def draw_close_and_plus_icons(
    close_dst: str = "output/icon_close_24.png",
    plus_dst: str = "output/icon_plus_24.png",
) -> None:
    """Задача 16.3: иконки 'Закрыть' (крестик) и 'Плюс' размером 24x24."""
    # Иконка "Закрыть" (крестик)
    close_img = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
    d_close = ImageDraw.Draw(close_img)
    d_close.line((5, 5, 19, 19), fill=(231, 76, 60), width=3)
    d_close.line((19, 5, 5, 19), fill=(231, 76, 60), width=3)
    close_img.save(close_dst, format="PNG")
    print(f"[16.3] Сохранено: {close_dst}")

    # Иконка "Плюс"
    plus_img = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
    d_plus = ImageDraw.Draw(plus_img)
    d_plus.line((12, 4, 12, 20), fill=(46, 204, 113), width=3)
    d_plus.line((4, 12, 20, 12), fill=(46, 204, 113), width=3)
    plus_img.save(plus_dst, format="PNG")
    print(f"[16.3] Сохранено: {plus_dst}")


if __name__ == "__main__":
    draw_shapes()
    draw_home_icon()
    draw_close_and_plus_icons()