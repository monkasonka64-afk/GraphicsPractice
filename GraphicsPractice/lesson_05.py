from PIL import Image

image_path = "source/photo.jpg"

try:
    with Image.open(image_path) as img:
        print("--- Задача 5.1: Получение цвета пикселей ---")
        print(
            "Режим изображения:", img.mode
        )  # RGB или RGBA (для понимания формата цвета)

        # 1. Цвет в точке (0, 0) - левый верхний угол
        pixel_0_0 = img.getpixel((0, 0))
        print(f"Цвет пикселя в точке (0, 0): {pixel_0_0}")

        # 2. Цвет в точке (10, 10)
        pixel_10_10 = img.getpixel((10, 10))
        print(f"Цвет пикселя в точке (10, 10): {pixel_10_10}")

        # 3. Цвет в центре изображения
        # Вычисляем координаты центра (делим ширину и высоту на 2 и округляем до целого)
        center_x = img.width // 2
        center_y = img.height // 2
        pixel_center = img.getpixel((center_x, center_y))
        print(
            f"Цвет пикселя в центре ({center_x}, {center_y}): {pixel_center}"
        )

except FileNotFoundError:
    print(f"Ошибка: Файл '{image_path}' не найден.")
except Exception as e:
    print(f"Произошла ошибка: {e}")