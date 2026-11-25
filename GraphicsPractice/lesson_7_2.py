import os
from PIL import Image

# Убедимся, что папка output существует
if not os.path.exists("output"):
    os.makedirs("output")

# Путь к исходному файлу (при необходимости замените имя файла)
image_path = "source/фото.jpg"

try:
    with Image.open(image_path) as img:
        print(f"Исходный размер: {img.size}")
        
        # Задача 7.2: Изменение размера с помощью thumbnail с сохранением пропорций
        img.thumbnail((400, 300), Image.Resampling.LANCZOS)
        
        print(f"Размер после thumbnail: {img.size}")
        
        # Сохраняем результат
        output_path = "output/thumb.png"
        img.save(output_path)
        print(f"Изображение успешно сохранено в {output_path}")

except FileNotFoundError:
    print(f"Ошибка: файл '{image_path}' не найден. Проверьте путь к изображению в папке source.")