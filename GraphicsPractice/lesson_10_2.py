import os
from PIL import Image, ImageOps

if not os.path.exists("output"):
    os.makedirs("output")

# Предположим, что у нас есть исходная иконка стрелки "вправо"
# (Для демонстрации можно использовать любую картинку из source/photo.jpg или создать стрелку)
image_path = "source/фото.jpg"

try:
    with Image.open(image_path) as img:
        print(f"Исходный размер: {img.size}")
        
        # 1. Отражение по горизонтали (mirror)
        # Превращает стрелку "вправо" в стрелку "влево"
        mirrored_img = ImageOps.mirror(img)
        mirrored_img.save("output/arrow_left.png")
        print("Сохранено зеркальное отражение по горизонтали (arrow_left.png)")
        
        # 2. Отражение по вертикали (flip)
        # Переворачивает изображение сверху вниз (например, для создания стрелки "вверх" или "вниз")
        flipped_img = ImageOps.flip(img)
        flipped_img.save("output/arrow_up.png")
        print("Сохранено отражение по вертикали (arrow_up.png)")
        
        print("\nЗадачи по отражению успешно выполнены!")

except FileNotFoundError:
    print(f"Ошибка: файл '{image_path}' не найден в папке source.")