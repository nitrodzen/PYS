import face_recognition
import os
import shutil
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import time
import re
from collections import defaultdict

# Создаем папки, если они еще не существуют
for folder in ["input", "known_faces", "output", "output_scheme"]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Загружаем известные лица и их имена
known_face_encodings = defaultdict(list)  # Словарь для хранения кодировок лиц по именам
known_face_names = []  # Список для имен, чтобы сохранить порядок

def load_known_faces(known_faces_dir="known_faces"):
    for filename in os.listdir(known_faces_dir):
        # Проверяем, что файл имеет поддерживаемое расширение
        if filename.lower().endswith((".jpg", ".jpeg", ".png")): 
            base_name = re.sub(r'\d+', '', filename.rsplit('.', 1)[0]).rstrip()
            face_image_path = os.path.join(known_faces_dir, filename)
            face_image = face_recognition.load_image_file(face_image_path)
            face_encoding = face_recognition.face_encodings(face_image)
            if face_encoding:
                known_face_encodings[base_name].append(face_encoding[0])
                if base_name not in known_face_names:
                    known_face_names.append(base_name)

load_known_faces()

font_path = "arial.ttf"
font_size = 56

def process_images(input_image_path):
    print(f"Обработка изображения: {input_image_path}")
    image_to_check = face_recognition.load_image_file(input_image_path)
    face_locations = face_recognition.face_locations(image_to_check)
    face_encodings = face_recognition.face_encodings(image_to_check, face_locations)

    pil_image = Image.fromarray(image_to_check)
    draw = ImageDraw.Draw(pil_image)
    font = ImageFont.truetype(font_path, font_size)

    recognized_faces = []

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        name = "Unknown"
        min_distance = 1.0

        for known_name, encodings_list in known_face_encodings.items():
            distances = face_recognition.face_distance(encodings_list, face_encoding)
            best_match_index = np.argmin(distances)

            if distances[best_match_index] < min_distance:
                min_distance = distances[best_match_index]
                if min_distance < 0.6:
                    name = known_name

        if name != "Unknown":
            recognized_faces.append(name)
            print(f"Распознано лицо: {name} на изображении {os.path.basename(input_image_path)}")
            
            text = f"{name} {round((1 - min_distance) * 100, 2)}%"
            text_bbox = draw.textbbox((left, bottom), text, font=font)
            draw.rectangle(((left, top), (right, bottom)), outline="red", width=5)
            draw.rectangle((text_bbox[0], text_bbox[1], text_bbox[2], text_bbox[3]), fill="red", outline="red")
            draw.text((text_bbox[0], text_bbox[1]), text, fill="white", font=font)

    # Сохраняем изменения на изображении
    output_scheme_path = f"output_scheme/{os.path.basename(input_image_path)}"
    pil_image.save(output_scheme_path)

    # Копирование и удаление обрабатываемого изображения происходит после всех операций
    for name in recognized_faces:
        output_path = f"output/{name}"
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        shutil.copy(input_image_path, output_path)

    if recognized_faces:
        os.remove(input_image_path)
    else:
        print(f"На изображении {os.path.basename(input_image_path)} не найдены известные лица.")

def run_processing_loop():
    try:
        while True:
            print("Проверка папки input и обработка новых изображений... Для остановки нажмите Ctrl+C")
            for image_file in os.listdir("input"):
                if any(image_file.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
                    process_images(f"input/{image_file}")
            time.sleep(60)
    except KeyboardInterrupt:
        print("Остановлено пользователем.")

if __name__ == "__main__":
    run_processing_loop()