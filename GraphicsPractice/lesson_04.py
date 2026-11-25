from PIL import Image

# Открываем изображение из папки source
jpg = Image.open("source/фото.jpg")

print("--- Задача 4.1: Свойства изображения ---")
print("Формат:", jpg.format)
print("Размер (ширина, высота):", jpg.size)
print("Ширина:", jpg.width, "Высота:", jpg.height)
print("Режим:", jpg.mode)

# Показать картинку в стандартном просмотрщике ОС
jpg.show()