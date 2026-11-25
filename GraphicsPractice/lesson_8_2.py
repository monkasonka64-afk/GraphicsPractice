import os
from PIL import Image

# Убедимся, что папка output существует
if not os.path.exists("output"):
    os.makedirs("output")

image_path = "source/фото.jpg"

# Список элементов интерфейса из таблицы (имя файла, максимальная ширина, максимальная высота)
ui_elements = [
    ("logo_header.png", 200, 60),
    ("bg_main.jpg", 800, 600),
    ("thumb_list.png", 64, 64),
    ("icon_btn.png", 24, 24)
]

try:
    for filename, max_w, max_h in ui_elements:
        with Image.open(image_path) as img:
            # Вписываем в рамку с сохранением пропорций и качественным фильтром LANCZOS
            img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
            
            output_path = os.path.join("output", filename)
            img.save(output_path)
            print(f"Элемент '{filename}' успешно создан, итоговый размер: {img.size}")
            
    print("\nВсе элементы интерфейса успешно подготовлены и сохранены в папку output.")

except FileNotFoundError:
    print(f"Ошибка: исходный файл '{image_path}' не найден в папке source.")