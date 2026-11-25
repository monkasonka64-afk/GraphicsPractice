import os
from PIL import Image

def fit_image(path, max_w, max_h):
    """
    Открывает изображение по пути path и возвращает его копию,
    вписанную в рамку max_w x max_h с сохранением пропорций.
    """
    img = Image.open(path)
    # Метод thumbnail изменяет изображение на месте, сохраняя пропорции 
    # и не увеличивая картинку, если она изначально меньше рамки
    img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
    return img

# Пример использования функции:
if __name__ == "__main__":
    if not os.path.exists("output"):
        os.makedirs("output")
        
    image_path = "source/фото.jpg"
    
    try:
        # Вызываем нашу функцию для вписывания в рамку 400x300
        fitted_img = fit_image(image_path, 400, 300)
        
        print(f"Исходный файл обработан. Новый размер: {fitted_img.size}")
        
        # Сохраняем результат
        output_path = "output/fitted_image.png"
        fitted_img.save(output_path)
        print(f"Результат сохранен в {output_path}")
        
    except FileNotFoundError:
        print(f"Ошибка: файл '{image_path}' не найден.")