import face_recognition
from PIL import Image
import tkinter as tk
from tkinter import filedialog
import os

# Создание диалогового окна выбора файла
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

# Проверка, выбрал ли пользователь файл
if file_path:
    # Загрузка изображения
    image = face_recognition.load_image_file(file_path)
    # Загрузка изображения
    #image = face_recognition.load_image_file("C:\\Users\\nitro\Downloads\\IMAGES\\IMG_3849.jpg")

    # Нахождение лиц на фотографии
    face_locations = face_recognition.face_locations(image)

    # Предполагаем, что на фотографии одно лицо и обрезаем его
    top, right, bottom, left = face_locations[0]

    # Доля, на которую нужно обрезать
    top_fraction = 0.5  # сверху
    bottom_fraction = 0.9  # снизу
    left_fraction = 0.7  # слева
    right_fraction = 0.7  # справа

    # Проверка координат обрезки
    top = max(top, 0)
    bottom = min(bottom, image.shape[0])
    left = max(left, 0)
    right = min(right, image.shape[1])

    # Расчет координат обрезки
    top_offset = int((bottom - top) * top_fraction)
    bottom_offset = int((bottom - top) * bottom_fraction)
    left_offset = int((right - left) * left_fraction)
    right_offset = int((right - left) * right_fraction)

    # Применение обрезки с учетом проверок
    top -= min(top_offset, top)
    bottom += min(bottom_offset, image.shape[0] - bottom)
    left -= min(left_offset, left)
    right += min(right_offset, image.shape[1] - right)

    # Обрезанное изображение
    face_image = image[top:bottom, left:right]

    # Формирование пути для сохранения обрезанного изображения
    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    cropped_directory = os.path.join(directory, "cropped")
    os.makedirs(cropped_directory, exist_ok=True)
    cropped_file_path = os.path.join(cropped_directory, filename)

    # Сохранение обрезанного изображения
    pil_image = Image.fromarray(face_image)
    pil_image.save(cropped_file_path)

    print("Изображение успешно обрезано и сохранено.")
else:
    print("Файл не выбран.")