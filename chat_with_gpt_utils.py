import os
import shutil
import re
import sys
import tkinter as tk
from tkinter import *



image_folder = r"C:\Users\mhd\Downloads\imagepython"
sound_folder = r"C:\Users\mhd\Downloads\sound1"
text_folder = r"C:\Users\mhd\Downloads\text"
executable_folder = r"C:\Users\mhd\Downloads\executable"
rest_folder = r"C:\Users\mhd\Downloads\rest1"
document_folder = r"C:\Users\mhd\Downloads\document123"
video_folder = r"C:\Users\mhd\Downloads\video"


if not os.path.exists(image_folder):
    os.mkdir(image_folder)
if not os.path.exists(sound_folder):
    os.mkdir(sound_folder)
if not os.path.exists(rest_folder):
    os.mkdir(rest_folder)
if not os.path.exists(text_folder):
    os.mkdir(text_folder)
if not os.path.exists(executable_folder):
    os.mkdir(executable_folder)
if not os.path.exists(document_folder):
    os.mkdir(document_folder)
if not os.path.exists(video_folder):
    os.mkdir(video_folder)

image_extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".svg", ".webp"]
sound_extensions = [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma", ".m4a", ".aiff"]
text_extensions = [".txt, .md, .rtf, .doc, .docx, .odt, .pdf, .tex, .wpd"]
executable_extensions = [".exe, .bat, .cmd, .sh, .bin, .com, .run, .msi"]
document_extensions = [".doc, .docx, .odt, .pdf, .rtf, .tex, .wpd"]
video_extensions = [".mp4, .avi, .mkv, .mov, .wmv, .flv, .webm, .mpeg, .mpg, .m4v"]



for file in os.listdir(r"C:\Users\mhd\Downloads"):
    file_path = os.path.join(r"C:\Users\mhd\Downloads", file)
    if os.path.isfile(file_path):
        if any(file.endswith(ext) for ext in image_extensions):
            shutil.move(file_path, image_folder)
            print(f"Moved {file} to image folder")
        elif any(file.endswith(ext) for ext in sound_extensions):
            shutil.move(file_path, sound_folder)
            print(f"Moved {file} to sound folder")
        elif any(file.endswith(ext) for ext in text_extensions):
            shutil.move(file_path, text_folder)
            print(f"Moved {file} to text folder")
        elif any(file.endswith(ext) for ext in executable_extensions):
            shutil.move(file_path, executable_folder)
            print(f"Moved {file} to executable folder")
        elif any(file.endswith(ext) for ext in document_extensions):
            shutil.move(file_path, document_folder)
            print(f"Moved {file} to document folder")
        elif any(file.endswith(ext) for ext in video_extensions):
            shutil.move(file_path, video_folder)
            print(f"Moved {file} to video folder")
        else:
            shutil.move(file_path, rest_folder)
            print(f"Moved {file} to rest folder")