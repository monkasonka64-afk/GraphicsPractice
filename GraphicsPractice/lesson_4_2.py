from PIL import Image

# Специально укажем путь (можете изменить имя файла, чтобы проверить ошибку)
image_path = "source/error.jpg"

print("--- Задача 4.2: Обработка ошибок ---")
try:
    with Image.open(image_path) as img:
        print(f"Успех! Файл '{image_path}' найден и открыт.")
        print("Размер изображения:", img.size)
except FileNotFoundError:
    print(f"Ошибка: Файл '{image_path}' не найден. Проверьте правильность пути!")