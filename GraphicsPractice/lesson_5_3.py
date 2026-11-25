from PIL import Image
import os

# Создаём папку output, если её ещё нет
os.makedirs("output", exist_ok=True)

# Создаём красное изображение размером 200 на 200
img = Image.new("RGB", (200, 200), (255, 0, 0))

# Сохраняем изображение
img.save("output/red.png")

print("Изображение успешно создано!")
