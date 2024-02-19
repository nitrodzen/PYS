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
