import os
from PIL import Image

# Убедимся, что папка output существует
if not os.path.exists("output"):
    os.makedirs("output")

# Укажите точное имя файла, который у вас лежит в папке source
image_path = "source/фото.jpg" 

try:
    with Image.open(image_path) as img:
        img_resized = img.resize((400, 300))
        img_resized.save("output/resized.png")
        print("Изображение успешно изменено и сохранено в output/resized.png")
except FileNotFoundError:
    print(f"Ошибка: файл '{image_path}' не найден. Проверьте имя файла в папке source.")