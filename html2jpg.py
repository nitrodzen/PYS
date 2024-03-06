from selenium import webdriver
import os
import base64
import time
import fitz  # pip install PyMuPDF
from datetime import datetime
from shutil import move

# Указание директорий
base_dir = os.path.dirname(os.path.abspath(__file__))
input_directory = os.path.join(base_dir, "input")
output_directory = os.path.join(base_dir, "output")
processed_directory = os.path.join(base_dir, "processed")

# Убедитесь, что все необходимые папки существуют
for directory in [input_directory, output_directory, processed_directory]:
    if not os.path.exists(directory):
        os.makedirs(directory)

def process_html_to_jpg():
    for filename in os.listdir(input_directory):
        if filename.endswith(".html"):
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            driver = webdriver.Chrome(options=options)
            file_path = os.path.join(input_directory, filename)
            driver.get(f"file:///{os.path.abspath(file_path)}")
            time.sleep(2)  # Дать время на загрузку страницы

            # Параметры для сохранения страницы в PDF
            params = {
                'landscape': False,
                'displayHeaderFooter': False,
                'printBackground': True,
                'preferCSSPageSize': True,
            }

            result = driver.execute_cdp_cmd("Page.printToPDF", params)
            pdf_content = base64.b64decode(result['data'])
            driver.quit()

            # Создание временного PDF для конвертации
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            temp_pdf_path = os.path.join(output_directory, f"{timestamp}_temp.pdf")
            with open(temp_pdf_path, 'wb') as pdf_file:
                pdf_file.write(pdf_content)

            # Конвертация всех страниц PDF в JPG
            doc = fitz.open(temp_pdf_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap()
                # Масштабирование изображения до требуемой ширины 590 пикселей
                target_width = 590
                scale = target_width / pix.width
                pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
                output_jpg_path = os.path.join(output_directory, f"{timestamp}_{page_num + 1}.jpg")
                pix.save(output_jpg_path)
                print(f"Сохранено изображение: {output_jpg_path}")
            doc.close()

            # Удаление временного PDF файла
            os.remove(temp_pdf_path)

            # Перемещение обработанных файлов в папку processed
            processed_subdir = os.path.join(processed_directory, timestamp)
            os.makedirs(processed_subdir, exist_ok=True)
            for filename in os.listdir(input_directory):
                move(os.path.join(input_directory, filename), processed_subdir)

if __name__ == "__main__":
    processing_flag = True
    try:
        while processing_flag:
            print("Проверка на наличие файлов для обработки...")
            process_html_to_jpg()
            print("Ожидание следующей проверки... Для остановки нажмите Ctrl+C")
            time.sleep(60)  # Ожидание 1 минуту перед следующим запуском
    except KeyboardInterrupt:
        print("Обработка изображений остановлена пользователем.")
        processing_flag = False
