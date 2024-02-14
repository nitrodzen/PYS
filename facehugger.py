import face_recognition
from PIL import Image

# Загрузка изображения
image = face_recognition.load_image_file("C:\\Users\\nitro\\Downloads\\IMAGES\\Alba_Morales_Armchair_Sitting_Brown_haired_Dress_576426_1600x1200.jpg")

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

# Сохранение обрезанного изображения
pil_image = Image.fromarray(face_image)
pil_image.save('facehug.jpg')