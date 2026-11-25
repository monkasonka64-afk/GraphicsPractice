import os
from PIL import Image

source_dir = "source"

# Проверяем, существует ли папка source
if not os.path.exists(source_dir):
    print(f"Папка '{source_dir}' не найдена. Создайте её и добавьте изображения.")
else:
    print(f"--- Анализ файлов в папке '{source_dir}' ---")
    
    # Обходим все файлы в папке source
    files = os.listdir(source_dir)
    
    if not files:
        print("Папка пуста.")
    else:
        for filename in files:
            file_path = os.path.join(source_dir, filename)
            
            # Пропускаем, если это не файл (например, вложенная папка)
            if not os.path.isfile(file_path):
                continue
            
            try:
                # Пытаемся открыть файл как изображение с помощью Pillow
                with Image.open(file_path) as img:
                    # Получаем размер файла в байтах и переводим в КБ
                    file_size_bytes = os.path.getsize(file_path)
                    file_size_kb = file_size_bytes / 1024
                    
                    print(f"Имя файла: {filename}")
                    print(f"  • Формат: {img.format}")
                    print(f"  • Размер в пикселях: {img.size} (Ширина: {img.width}, Высота: {img.height})")
                    print(f"  • Режим: {img.mode}")
                    print(f"  • Вес файла: {file_size_kb:.2f} КБ")
                    print("-" * 40)
                    
            except IOError:
                # Если файл не является изображением или поврежден
                print(f"Файл '{filename}' не является поддерживаемым изображением.")
                print("-" * 40)