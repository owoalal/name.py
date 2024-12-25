import os
import shutil
import re
import sys
import tkinter as tk
from tkinter import *



image_folder = r"C:\Users\mhd\Downloads\imagepython"
sound_folder = r"C:\Users\mhd\Downloads\sound1"
rest_folder = r"C:\Users\mhd\Downloads\rest"

if not os.path.exists(image_folder):
    os.mkdir(image_folder)
if not os.path.exists(sound_folder):
    os.mkdir(sound_folder)
if not os.path.exists(rest_folder):
    os.mkdir(rest_folder)

image_extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".svg", ".webp"]
sound_extensions = [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma", ".m4a", ".aiff"]

for file in os.listdir(r"C:\Users\mhd\Downloads"):
    file_path = os.path.join(r"C:\Users\mhd\Downloads", file)
    if os.path.isfile(file_path):
        if any(file.endswith(ext) for ext in image_extensions):
            shutil.move(file_path, image_folder)
            print(f"Moved {file} to image folder")
        elif any(file.endswith(ext) for ext in sound_extensions):
            shutil.move(file_path, sound_folder)
            print(f"Moved {file} to sound folder")
        else:
            shutil.move(file_path, rest_folder)
            print(f"Moved {file} to rest folder")