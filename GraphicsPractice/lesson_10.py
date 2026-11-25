import os
from PIL import Image

if not os.path.exists("output"):
    os.makedirs("output")

image_path = "source/фото.jpg"

try:
    with Image.open(image_path) as img:
        print(f"Исходный размер изображения: {img.size}")
        
        # 1. Поворот на 90 градусов (expand=True сохраняет изображение целиком без обрезки)
        rot_90 = img.rotate(90, expand=True)
        rot_90.save("output/rotate_90.png")
        print("Сохранен поворот на 90°")
        
        # 2. Поворот на 180 градусов
        rot_180 = img.rotate(180, expand=True)
        rot_180.save("output/rotate_180.png")
        print("Сохранен поворот на 180°")
        
        # 3. Поворот на 270 градусов
        rot_270 = img.rotate(270, expand=True)
        rot_270.save("output/rotate_270.png")
        print("Сохранен поворот на 270°")
        
        # 4. Поворот на 45 градусов с прозрачным фоном
        # Для работы с прозрачностью переводим изображение в режим RGBA
        img_rgba = img.convert("RGBA")
        # expand=True расширяет холст, а fillcolor=(0, 0, 0, 0) делает пустые углы прозрачными
        rot_45 = img_rgba.rotate(45, expand=True, fillcolor=(0, 0, 0, 0))
        rot_45.save("output/rotate_45.png")
        print("Сохранен поворот на 45° с прозрачным фоном")
        
        print("\nВсе задачи по повороту успешно выполнены!")

except FileNotFoundError:
    print(f"Ошибка: файл '{image_path}' не найден в папке source.")