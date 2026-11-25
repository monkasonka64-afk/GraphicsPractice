from PIL import Image

image_path = "source/фото.jpg"

print("--- Задача 4.3: Соотношение сторон и ориентация ---")
try:
    with Image.open(image_path) as img:
        # Вычисляем соотношение сторон (ширина / высота)
        aspect_ratio = img.width / img.height
        print(f"Соотношение сторон: {aspect_ratio:.2f}")

        # Определяем ориентацию с помощью условий
        if img.width > img.height:
            print("Ориентация: Альбомная (Landscape)")
        elif img.width < img.height:
            print("Ориентация: Книжная (Portrait)")
        else:
            print("Ориентация: Квадратная (Square)")

except FileNotFoundError:
    print(f"Ошибка: Файл '{image_path}' не найден.")