import os
from PIL import Image

def pad_image_to_fit(path, target_width, target_height, bg_color=(255, 255, 255)):
    """
    Открывает изображение, пропорционально уменьшает его под заданные размеры (target_width, target_height),
    создает новый холст с фоновым цветом bg_color и вставляет уменьшенное изображение строго по центру.
    """
    with Image.open(path) as img:
        # 1. Пропорционально уменьшаем изображение, чтобы оно поместилось в рамку
        img.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
        img_w, img_h = img.size
        
        # 2. Создаем новый холст нужного размера с фоновым цветом
        # Используем режим 'RGB' (или 'RGBA', если нужна прозрачность)
        result_img = Image.new("RGB", (target_width, target_height), bg_color)
        
        # 3. Вычисляем координаты для вставки по центру
        paste_x = (target_width - img_w) // 2
        paste_y = (target_height - img_h) // 2
        
        # 4. Вставляем изображение на холст
        # Если у изображения есть альфа-канал (прозрачность), передаем его же в качестве маски
        if img.mode == 'RGBA':
            result_img.paste(img, (paste_x, paste_y), img)
        else:
            result_img.paste(img, (paste_x, paste_y))
            
        return result_img

# Пример использования для задачи центрирования под размер главного окна (800x600):
if __name__ == "__main__":
    if not os.path.exists("output"):
        os.makedirs("output")
        
    image_path = "source/фото.jpg"
    
    try:
        # Создаем изображение размером 800x600 с белым фоном
        centered_img = pad_image_to_fit(image_path, 800, 600, bg_color=(255, 255, 255))
        
        output_path = "output/centered_bg.jpg"
        centered_img.save(output_path)
        print(f"Изображение успешно центрировано и сохранено в {output_path}. Размер холста: {centered_img.size}")
        
    except FileNotFoundError:
        print(f"Ошибка: файл '{image_path}' не найден в папке source.")