import os
from PIL import Image

image_path = "source/фото.jpg"
output_dir = "output"

# Создаем папку, если её нет
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

try:
    with Image.open(image_path) as img:
        # Конвертируем и сохраняем
        img_gray = img.convert("L")
        gray_path = os.path.join(output_dir, "photo_gray.jpg")
        img_gray.save(gray_path)

        img_rgba = img.convert("RGBA")
        rgba_path = os.path.join(output_dir, "photo_rgba.png")
        img_rgba.save(rgba_path)

        # Выводим точный путь, куда сохранены файлы
        print("Файлы успешно сохранены в папку:")
        print(os.path.abspath(output_dir))

except FileNotFoundError:
    print(f"Ошибка: Файл '{image_path}' не найден.")
except Exception as e:
    print(f"Произошла ошибка: {e}")