import face_recognition
from PIL import Image, ImageDraw
import os
import datetime
import time
import shutil
import numpy as np

# Пути к папкам
base_dir = os.path.dirname(os.path.abspath(__file__))
input_directory = os.path.join(base_dir, "input")
output_directory = os.path.join(base_dir, "output")
output_circle_directory = os.path.join(base_dir, "output_circle")
processed_directory = os.path.join(base_dir, "processed")
errors_directory = os.path.join(base_dir, "errors")
log_file_path = os.path.join(base_dir, "log.txt")

# Убедитесь, что все необходимые папки существуют
for directory in [input_directory, output_directory, output_circle_directory, processed_directory, errors_directory]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Функция для записи в лог
def log_message(message):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"{current_time}, {message}\n"
    print(message)
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(full_message)

# Функция для создания круглой обрезки изображения
def crop_circle(original_image, face_location):
    height_correction_factor=0.15
    width, height = original_image.size
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    
    # Определение центра и радиуса для круга с учетом коррекции положения
    top, right, bottom, left = face_location
    face_height = bottom - top
    
    # Коррекция верхней границы на заданный процент высоты лица для центрирования круга
    corrected_top = top - int(face_height * height_correction_factor)
    corrected_center_y = (corrected_top + bottom) // 2

    center_x, center_y = (left + right) // 2, corrected_center_y
    initial_radius = max(right - left, bottom - top) // 2
    
    # Проверка, не выходит ли круг за границы изображения, и коррекция радиуса если необходимо
    max_x_distance = min(center_x, width - center_x)
    max_y_distance = min(center_y, height - center_y)
    max_allowed_radius = min(max_x_distance, max_y_distance)
    radius = min(initial_radius, max_allowed_radius)
    
    # Рисуем круг на маске
    draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=255)
    
    # Применяем маску к изображению и обрезаем
    result = Image.new('RGBA', (width, height))
    result.paste(original_image, (0, 0), mask=mask)
    
    # Убедимся, что обрезка не выходит за границы изображения
    crop_left = max(center_x - radius, 0)
    crop_top = max(center_y - radius, 0)
    crop_right = min(center_x + radius, width)
    crop_bottom = min(center_y + radius, height)
    return result.crop((crop_left, crop_top, crop_right, crop_bottom))


# Функция для обработки изображений
def process_images():
    if os.path.exists(input_directory):
        files = os.listdir(input_directory)
        if len(files) > 0:
            for filename in files:
                file_path = os.path.join(input_directory, filename)
                original_file_path = file_path  # Сохраняем путь к исходному файлу для возможного перемещения
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    attempts = 0
                    success = False
                    while attempts < 4 and not success:
                        try:
                            image = face_recognition.load_image_file(file_path)
                            face_locations = face_recognition.face_locations(image)
                            if len(face_locations) == 1:
                                top, right, bottom, left = face_locations[0]
                                top_fraction = 1.0
                                bottom_fraction = 1.7
                                left_fraction = 1.3
                                right_fraction = 1.3
                                top_offset = int((bottom - top) * top_fraction)
                                bottom_offset = int((bottom - top) * bottom_fraction)
                                left_offset = int((right - left) * left_fraction)
                                right_offset = int((right - left) * right_fraction)
                                top = max(top - top_offset, 0)
                                bottom = min(bottom + bottom_offset, image.shape[0])
                                left = max(left - left_offset, 0)
                                right = min(right + right_offset, image.shape[1])
                                face_image = image[top:bottom, left:right]
                                cropped_file_path = os.path.join(output_directory, filename)
                                pil_image = Image.fromarray(face_image)
                                pil_image.save(cropped_file_path)
                                log_message(f"Изображение {filename} успешно обрезано") # и сохранено в 'output'.
                                #shutil.move(original_file_path, os.path.join(processed_directory, filename))
                                #log_message(f"Исходное изображение {filename} перемещено в 'processed'.")
                                # Создание и сохранение круглого изображения лица
                                pil_original_image = Image.open(file_path) #загружаем исходное изображение
                                circle_image = crop_circle(pil_original_image, (top, right, bottom, left))
                                circle_filename = os.path.splitext(filename)[0]+"_circle.png"
                                circle_file_path = os.path.join(output_circle_directory, circle_filename)
                                circle_image.save(circle_file_path, format='PNG')
                                success = True
                                log_message(f"Круглое изображение {filename} успешно сохранено в 'output'.")
                                shutil.move(original_file_path, os.path.join(processed_directory, filename))
                                log_message(f"Исходное изображение {filename} перемещено в 'processed'.")
                                break
                            else:
                                raise ValueError("На изображении обнаружено несколько лиц или их отсутствие.")
                        except Exception as e:
                            log_message(f"Попытка {attempts + 1}: ошибка при обработке изображения {filename}, причина: {e}")
                            attempts += 1
                            if attempts < 4:
                                pil_image = Image.open(file_path)
                                pil_image = pil_image.rotate(90, expand=True)
                                pil_image.save(file_path)  # Поворачиваем и сохраняем изменения в том же файле
                                log_message(f"Изображение {filename} было повернуто на 90 градусов.")
                            else:
                                shutil.move(original_file_path, os.path.join(errors_directory, filename))
                                log_message(f"Изображение {filename} перемещено в 'errors'. Причина: {e}")
                                break
                else:
                    shutil.move(original_file_path, os.path.join(errors_directory, filename))
                    log_message(f"Файл {filename} не является изображением формата .jpg или .png и перемещен в 'errors'.")
        else:
            log_message("Файлы не обнаружены в папке 'input'.")
    else:
        log_message("Папка 'input' не существует.")

# Простой текстовый интерфейс
if __name__ == "__main__":
    processing_flag = True
    try:
        while processing_flag:
            print("Обработка изображений запущена. Для остановки нажмите Ctrl+C")
            process_images()
            time.sleep(60)  # Ожидание 1 минуту перед следующим запуском
    except KeyboardInterrupt:
        log_message("Обработка изображений остановлена пользователем.")
        processing_flag = False