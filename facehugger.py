import face_recognition
from PIL import Image

# Загрузка изображения
image = face_recognition.load_image_file("C:\\Users\\nitro\\OneDrive\\Pictures\\-35.jpg")

# Нахождение лиц на фотографии
face_locations = face_recognition.face_locations(image)

# Предполагаем, что на фотографии одно лицо и обрезаем его
top, right, bottom, left = face_locations[0]
face_image = image[top:bottom, left:right]
pil_image = Image.fromarray(face_image)
pil_image.save('facehug.jpg')
