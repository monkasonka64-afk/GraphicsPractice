import os
from PIL import Image

source_dir = "source"
output_dir = "output"

# Автоматически создаем папку output, если её ещё нет
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

report_path = os.path.join(output_dir, "report.txt")

# Открываем текстовый файл для записи отчёта
with open(report_path, "w", encoding="utf-8") as report_file:
    report_file.write("--- Отчет об анализе файлов в папке source ---\n\n")
    
    print(f"--- Анализ файлов в папке '{source_dir}' ---")
    
    if not os.path.exists(source_dir):
        print(f"Папка '{source_dir}' не найдена.")
        report_file.write(f"Папка '{source_dir}' не найдена.\n")
    else:
        files = os.listdir(source_dir)
        
        if not files:
            print("Папка пуста.")
            report_file.write("Папка пуста.\n")
        else:
            for filename in files:
                file_path = os.path.join(source_dir, filename)
                
                if not os.path.isfile(file_path):
                    continue
                
                try:
                    with Image.open(file_path) as img:
                        file_size_bytes = os.path.getsize(file_path)
                        file_size_kb = round(file_size_bytes / 1024, 1)
                        
                        # Формируем строку с информацией о файле
                        info_str = (
                            f"Имя файла: {filename}\n"
                            f"  • Формат: {img.format}\n"
                            f"  • Размер в пикселях: {img.size} (Ширина: {img.width}, Высота: {img.height})\n"
                            f"  • Режим: {img.mode}\n"
                            f"  • Вес файла: {file_size_kb} КБ\n"
                            f"{'-' * 40}\n"
                        )
                        
                        # Выводим в консоль и записываем в файл отчета
                        print(info_str, end="")
                        report_file.write(info_str)
                        
                except OSError:
                    error_str = f"Файл '{filename}' - не изображение или поврежден.\n{'-' * 40}\n"
                    print(error_str, end="")
                    report_file.write(error_str)

print(f"\nОтчет успешно сохранен в файл: {report_path}")