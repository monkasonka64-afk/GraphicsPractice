import os
from PIL import Image

def create_grid_2x2(image_path, output_path):
    """
    Создает сетку 2x2 из четырех повернутых копий исходного изображения.
    """
    with Image.open(image_path) as img:
        # Убедимся, что изображение небольшое (например, размер логотипа из прошлых уроков)
        # Если нужно, можно использовать thumbnail, но предположим, что берем готовый элемент
        w, h = img.size
        print(f"Размер исходного элемента: {w}x{h}")
        
        # Создаем 4 повернутые копии (0°, 90°, 180°, 270°)
        img_0 = img.copy()
        img_90 = img.rotate(90, expand=True)
        img_180 = img.rotate(180, expand=True)
        img_270 = img.rotate(270, expand=True)
        
        # Новые размеры после поворота с expand=True могут отличаться, 
        # но для квадратного логотипа они будут одинаковыми (w x h).
        # Вычислим размер результирующего холста 2x2
        grid_w = w * 2
        grid_h = h * 2
        
        # Создаем пустой холст под сетку 2x2 (в режиме RGB или RGBA)
        grid_img = Image.new("RGB", (grid_w, grid_h), (255, 255, 255))
        
        # Размещаем изображения по четырем позициям сетки (paste принимает координаты левого верхнего угла)
        # 1. Верхний левый угол (0°, оригинальное)
        grid_img.paste(img_0, (0, 0))
        
        # 2. Верхний правый угол (поворот на 90°)
        grid_img.paste(img_90, (w, 0))
        
        # 3. Нижний левый угол (поворот на 270°)
        grid_img.paste(img_270, (0, h))
        
        # 4. Нижний правый угол (поворот на 180°)
        grid_img.paste(img_180, (w, h))
        
        # Сохраняем результат
        grid_img.save(output_path)
        print(f"Сетка 2x2 успешно создана и сохранена в '{output_path}'. Итоговый размер: {grid_img.size}")

if __name__ == "__main__":
    if not os.path.exists("output"):
        os.makedirs("output")
        
    # Используем любой файл, например логотип или квадратную аватарку
    logo_path = "output/logo_header.png"  # или "output/avatar.png"
    
    if os.path.exists(logo_path):
        create_grid_2x2(logo_path, "output/logo_grid_2x2.png")
    else:
        # Если файл не найден, берем базовое фото
        create_grid_2x2("source/фото.jpg", "output/photo_grid_2x2.png")