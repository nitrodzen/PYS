# FACEHUGGER

Folders will be created automatically:
- input/ # Folder for input images
- output/ # Folder for cropped images
- processed/ # Folder for already processed images
- errors/ # Folder for images with or without faces

====How to use====

- Place the input images in the input folder.
- Open folder with .py file with terminal.
- Run the facehugger.py by type "facehugger.py" or "python facehugger.py" and press Enter.
- The processed images will appear in the output folder, the original processed files will be moved to processed, and the images with errors will be moved to errors.
- To stop processing press Ctrl+C in terminal.

====Requirements====

-Python 3.6+
-Libraries: face_recognition, Pillow

Installing dependencies:

- CMake
- dlib (for your version of python, if you observes an errors, find correct whl dlib file)
- pip install face_recognition Pillow



# HTML2PNG

This code is a Python script for processing HTML files and converting them into PNG images using the Selenium, PyMuPDF, and Chrome WebDriver libraries.

The script performs the following steps:

1) Specify the necessary directories: 
- input_directory for input HTML files.
- output_directory for saving PNG images.
- and processed_directory for moving processed files.
    
2) Check if the specified directories exist, and create them if needed.

3) Define the path to the Chrome WebDriver (driver_path). If not specified, the script uses the WebDriver available in the system.

4) Create the process_html_to_png function, which processes HTML files in the specified directory.

5) For each file:
- Create an instance of the Chrome WebDriver with the specified options, including the "headless" mode.
- Open the HTML file in the browser.
- Set parameters for saving the page as a PDF.
- Execute the Page.printToPDF command to save the page as a PDF.
- Decode the PDF content from base64 and save it to a temporary PDF file.
- Open the temporary PDF file using PyMuPDF, extract the first page, and convert it to a PNG image.
- Delete the temporary PDF file.
- Move all files from the input_directory to a subdirectory with the current date and time in the processed_directory.
- Print the path of the saved PNG image.
    
6) Wait for 1 minute before the next check.

7) If the user interrupts the script (by pressing Ctrl+C), print a message indicating that the image processing has been stopped.
