import os
from PIL import Image

# Убедимся, что папка output существует
if not os.path.exists("output"):
    os.makedirs("output")

image_path = "source/фото.jpg"

try:
    with Image.open(image_path) as img:
        # 1. Метод ближайшего соседа (Nearest Neighbor)
        img_nearest = img.resize((64, 64), Image.Resampling.NEAREST)
        img_nearest.save("output/thumb_nearest.png")
        
        # 2. Билинейная интерполяция (Bilinear)
        img_bilinear = img.resize((64, 64), Image.Resampling.BILINEAR)
        img_bilinear.save("output/thumb_bilinear.png")
        
        # 3. Фильтр Ланцоша (Lanczos)
        img_lanczos = img.resize((64, 64), Image.Resampling.LANCZOS)
        img_lanczos.save("output/thumb_lanczos.png")
        
        print("Все три фильтра успешно применены, результаты сохранены в папку output.")

except FileNotFoundError:
    print(f"Ошибка: файл '{image_path}' не найден.")