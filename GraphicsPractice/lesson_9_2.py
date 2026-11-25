import os
from PIL import Image

def square_crop(path, size):
    """
    Открывает изображение по пути path, вырезает центральную квадратную часть
    и масштабирует её до заданного размера (size x size).
    Возвращает готовый объект изображения.
    """
    with Image.open(path) as img:
        w, h = img.size
        
        # Находим минимальную сторону для создания правильного квадрата
        side = min(w, h)
        
        # Вычисляем координаты для обрезки по центру
        left = (w - side) // 2
        top = (h - side) // 2
        right = left + side
        bottom = top + side
        
        # Обрезаем центральную часть до квадрата
        square_img = img.crop((left, top, right, bottom))
        
        # Изменяем размер до требуемого с использованием качественного фильтра LANCZOS
        resized_img = square_img.resize((size, size), Image.Resampling.LANCZOS)
        
        return resized_img

# Пример использования функции:
if __name__ == "__main__":
    if not os.path.exists("output"):
        os.makedirs("output")
        
    image_path = "source/фото.jpg"
    
    try:
        # Создаем квадратную аватарку размером 150x150 пикселей
        avatar = square_crop(image_path, 150)
        
        output_path = "output/avatar_custom.png"
        avatar.save(output_path)
        print(f"Кастомный аватар успешно создан и сохранен в {output_path}. Размер: {avatar.size}")
        
    except FileNotFoundError:
        print(f"Ошибка: файл '{image_path}' не найден в папке source.")