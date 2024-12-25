import os
import shutil
print("this app will organise your pc")


# Ask for the path to clean
path2 = input("please enter he path you want to clean:")


# validate the path
while not os.path.exists(path2):
    print(f"Error: The path '{path2}' does not exist. Please provide a valid path.")
    path2 = input("Please enter a valid path you want to clean: ")



# Define folders for each category
image_folder = os.path.join(path2, "imagepython")
sound_folder = os.path.join(path2, "sound1")
text_folder = os.path.join(path2, "text")
executable_folder = os.path.join(path2, "executable")
rest_folder = os.path.join(path2, "rest1")
document_folder = os.path.join(path2, "document123")
video_folder = os.path.join(path2, "video")


# List of all folders
folders = [image_folder, sound_folder, text_folder, executable_folder, rest_folder, document_folder, video_folder]


# Create folders if they don't exist
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


# Define file extensions for each category
image_extensions = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".svg", ".webp"]
sound_extensions = [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma", ".m4a", ".aiff"]
text_extensions = [".txt", ".md", ".rtf"]
executable_extensions = [".exe", ".bat", ".cmd", ".sh", ".bin", ".com", ".run", ".msi"]
document_extensions = [".doc", ".docx", ".odt", ".pdf", ".tex", ".wpd"]
video_extensions = [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".mpeg", ".mpg", ".m4v"]


# for moving the files to their respective folders
for file in os.listdir(path2):
    file_path = os.path.join(path2, file)
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

print("All files have been organized successfully!")


# define empty folders
empty_folders = [folder for folder in folders if os.path.exists(folder) and not os.listdir(folder)]



# Ask for confirmation before removing empty folders
if empty_folders:
    confirm = input(f"Do you wish to remove (all) empty folders ? (yes/no): ")
    if confirm.lower() == 'yes':
        for folder in empty_folders:
            os.rmdir(folder)
            print(f"Removed empty folder: {folder}")

print("All files have been organized successfully!")
print("Thank you for using this app!")