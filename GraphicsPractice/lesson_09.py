import os
from PIL import Image

# Убедимся, что папка output существует
if not os.path.exists("output"):
    os.makedirs("output")

image_path = "source/фото.jpg"

try:
    with Image.open(image_path) as img:
        print(f"Исходный размер: {img.size}")
        
        w, h = img.size
        # Находим минимальную сторону, чтобы вырезать правильный квадрат
        side = min(w, h)
        
        # Вычисляем координаты для обрезки по центру
        left = (w - side) // 2
        top = (h - side) // 2
        right = left + side
        bottom = top + side
        
        # Обрезаем центральную часть до квадрата
        square = img.crop((left, top, right, bottom))
        
        # Уменьшаем до заданного размера (например, 128×128 или 300×300 в зависимости от задачи)
        square = square.resize((128, 128), Image.Resampling.LANCZOS)
        
        output_path = "output/avatar.png"
        square.save(output_path)
        print(f"Аватарка успешно сохранена в {output_path}. Итоговый размер: {square.size}")

except FileNotFoundError:
    print(f"Ошибка: файл '{image_path}' не найден в папке source.")