import os
from PIL import Image

def crop_corners(path):
    """
    Открывает изображение по пути path, делит его пополам по вертикали и горизонтали
    и сохраняет 4 угловых фрагмента в папку output.
    """
    with Image.open(path) as img:
        w, h = img.size
        print(f"Исходный размер изображения: {w}x{h}")
        
        # Вычисляем середину изображения
        mid_w = w // 2
        mid_h = h // 2
        
        # Определяем координаты для 4 углов (left, upper, right, lower)
        # 1. Верхний левый угол
        top_left = (0, 0, mid_w, mid_h)
        # 2. Верхний правый угол
        top_right = (mid_w, 0, w, mid_h)
        # 3. Нижний левый угол
        bottom_left = (0, mid_h, mid_w, h)
        # 4. Нижний правый угол
        bottom_right = (mid_w, mid_h, w, h)
        
        corners = {
            "corner_top_left.png": top_left,
            "corner_top_right.png": top_right,
            "corner_bottom_left.png": bottom_left,
            "corner_bottom_right.png": bottom_right
        }
        
        # Вырезаем и сохраняем каждый фрагмент
        for filename, box in corners.items():
            cropped_img = img.crop(box)
            output_path = os.path.join("output", filename)
            cropped_img.save(output_path)
            print(f"Фрагмент '{filename}' сохранен. Размер: {cropped_img.size}")

# Пример использования функции:
if __name__ == "__main__":
    if not os.path.exists("output"):
        os.makedirs("output")
        
    image_path = "source/фото.jpg"
    
    try:
        crop_corners(image_path)
        print("\nВсе 4 угловых фрагмента успешно вырезаны и сохранены!")
        
    except FileNotFoundError:
        print(f"Ошибка: файл '{image_path}' не найден в папке source.")