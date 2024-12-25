import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# File to store the username
USER_DATA_FILE = "user_data.txt"


class LoginPage:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("Login Page")
        self.root.geometry("450x200")
        self.root.config(bg="grey")

        # Username variable
        self.username = tk.StringVar()

        # Load user data if it exists
        self.saved_username = self.load_username()

        if self.saved_username:
            # If a username is already saved, skip login
            self.on_login_success()
        else:
            # Show login interface
            self.create_widgets()

    def create_widgets(self):
        # Create the "Enter Username" input field
        username_entry = tk.Entry(self.root, textvariable=self.username, font=("Arial", 12), bg="white", fg="black")
        username_entry.pack(pady=40)

        # Label (purple) to the right of the username field
        username_label = tk.Label(self.root, text="Enter Username", font=("Arial", 12), bg="grey", fg="purple")
        username_label.place(x=0,y=40)

        # Save button
        tk.Button(self.root, text="Submit", font=("Arial", 12), command=self.validate_login, bg="purple",
                  fg="white").pack(pady=20)

    def validate_login(self):
        username = self.username.get().strip()

        if username:
            # Save the username for future use
            self.save_username(username)
            messagebox.showinfo("Welcome", f"Hello, {username}!")
            self.on_login_success()
        else:
            messagebox.showerror("Error", "Please enter a valid username!")

    def save_username(self, username):
        with open(USER_DATA_FILE, "w") as file:
            file.write(username)

    def load_username(self):
        # Check if username is already saved
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, "r") as file:
                return file.read().strip()
        return None


class FileOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Organizer App")
        self.root.geometry("600x600")
        self.root.config(bg="#D8BFD8")

        # Get the saved username
        self.username = self.load_username()

        # Create a source folder variable
        self.source_folder = tk.StringVar()

        # Track file movements for undo functionality
        self.file_movements = []

        # Define categories for auto-organization
        self.file_categories = {
            "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".svg", ".webp"],
            "Sounds": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma", ".m4a", ".aiff"],
            "Texts": [".txt", ".md", ".rtf", ".doc", ".docx", ".odt", ".pdf", ".tex", ".wpd"],
            "Executables": [".exe", ".bat", ".cmd", ".sh", ".bin", ".com", ".run", ".msi"],
            "Documents": [".doc", ".docx", ".odt", ".pdf", ".rtf", ".tex", ".wpd"],
            "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".mpeg", ".mpg", ".m4v"]
        }

        self.create_widgets()

    def create_widgets(self):
        # Box for Welcome Message (with your username displayed)
        welcome_frame = tk.Label(self.root, text=f"Welcome, {self.username}", font=("Arial", 12), bg="#D8BFD8",
                                 fg="black")
        welcome_frame.pack(pady=10)

        # Box for "Source Folder"
        source_frame = tk.LabelFrame(self.root, text="Source Folder", font=("Arial", 12), bg="#D8BFD8", fg="black",
                                     bd=3, relief="groove")
        source_frame.pack(pady=10, padx=20, fill="x")
        tk.Entry(source_frame, textvariable=self.source_folder, font=("Arial", 12), bg="white", fg="black").pack(pady=5,
                                                                                                                 padx=5)
        tk.Button(source_frame, text="Browse", font=("Arial", 10), command=self.browse_folder, bg="purple",
                  fg="white").pack(pady=5)

        # Box for "Organize and Undo Buttons"
        button_frame = tk.LabelFrame(self.root, text="Actions", font=("Arial", 12), bg="#D8BFD8", fg="black", bd=3,
                                     relief="groove")
        button_frame.pack(pady=10, padx=20, fill="x")
        tk.Button(button_frame, text="Organize Files", font=("Arial", 12), command=self.organize_files, bg="purple",
                  fg="white").pack(pady=5)
        tk.Button(button_frame, text="Undo Last Action", font=("Arial", 12), command=self.undo_last_action, bg="purple",
                  fg="white").pack(pady=5)

        # Box for log area
        log_frame = tk.LabelFrame(self.root, text="Log", font=("Arial", 12), bg="#D8BFD8", fg="black", bd=3,
                                  relief="groove")
        log_frame.pack(pady=10, padx=20, fill="both", expand=True)
        self.log_box = tk.Text(log_frame, font=("Arial", 10), bg="white", fg="black", wrap="word")
        self.log_box.pack(pady=5, padx=5, fill="both", expand=True)

    @staticmethod
    def load_username():
        # Load username from the file
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, "r") as file:
                return file.read().strip()
        return "User"

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.source_folder.set(folder_selected)

    def organize_files(self):
        source = self.source_folder.get()
        if not source:
            messagebox.showerror("Error", "Please select a source folder!")
            return

        # Clear previous file movements
        self.file_movements = []

        # Create category folders if they don't exist
        for category in self.file_categories.keys():
            category_folder = os.path.join(source, category)
            if not os.path.exists(category_folder):
                os.mkdir(category_folder)

        # Create a folder for unrecognized files
        rest_folder = os.path.join(source, "Others")
        if not os.path.exists(rest_folder):
            os.mkdir(rest_folder)

        # Move files to the appropriate category
        moved_files = []
        for file_name in os.listdir(source):
            file_path = os.path.join(source, file_name)
            if os.path.isfile(file_path):
                # Move based on file extensions
                moved = False
                for category, extensions in self.file_categories.items():
                    if any(file_name.lower().endswith(ext) for ext in extensions):
                        destination = os.path.join(source, category, file_name)
                        shutil.move(file_path, destination)
                        self.file_movements.append((destination, file_path))
                        moved_files.append(f"Moved {file_name} to {category}")
                        moved = True
                        break

                # If no extension matches, move to "Others"
                if not moved:
                    destination = os.path.join(rest_folder, file_name)
                    shutil.move(file_path, destination)
                    self.file_movements.append((destination, file_path))
                    moved_files.append(f"Moved {file_name} to Others")

        # Populate the log box
        self.log_box.delete(1.0, tk.END)
        if moved_files:
            self.log_box.insert(tk.END, "\n".join(moved_files))
        else:
            self.log_box.insert(tk.END, "No files to organize.")

        messagebox.showinfo("Success", "Files organized successfully!")

    def undo_last_action(self):
        if not self.file_movements:
            messagebox.showinfo("Info", "No actions to undo!")
            return

        # Undo all file movements
        undo_logs = []
        while self.file_movements:
            destination, source = self.file_movements.pop()
            shutil.move(destination, source)
            undo_logs.append(f"Moved {os.path.basename(destination)} back to its original location")

        # Update the log box
        self.log_box.delete(1.0, tk.END)
        self.log_box.insert(tk.END, "\n".join(undo_logs))

        messagebox.showinfo("Success", "Undo completed!")


def on_login_success():
    login_root.destroy()
    main_root = tk.Tk()
    FileOrganizerApp(main_root)
    main_root.mainloop()


if __name__ == "__main__":
    login_root = tk.Tk()
    LoginPage(login_root, on_login_success)
    login_root.mainloop()