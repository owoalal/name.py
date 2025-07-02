from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QMessageBox
import sys

class NotebookApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Notebook and List Maker")
        self.setGeometry(100, 100, 500, 400)

        # Create layout
        layout = QVBoxLayout()

        # Notebook section
        self.note_label = QLabel("Write your note:")
        layout.addWidget(self.note_label)
        self.note_input = QTextEdit()
        layout.addWidget(self.note_input)

        self.save_note_button = QPushButton("Save Note")
        self.save_note_button.clicked.connect(self.save_note)
        layout.addWidget(self.save_note_button)

        # List maker section
        self.list_label = QLabel("Add an item to your list:")
        layout.addWidget(self.list_label)
        self.list_input = QLineEdit()
        layout.addWidget(self.list_input)

        self.add_item_button = QPushButton("Add Item")
        self.add_item_button.clicked.connect(self.add_item)
        layout.addWidget(self.add_item_button)

        self.list_display = QTextEdit()
        self.list_display.setReadOnly(True)
        layout.addWidget(self.list_display)

        self.save_list_button = QPushButton("Save List")
        self.save_list_button.clicked.connect(self.save_list)
        layout.addWidget(self.save_list_button)

        self.setLayout(layout)

        # Initialize list
        self.list_items = self.load_list()
        self.list_display.setText('\n'.join(self.list_items))

    def load_list(self):
        try:
            with open('list.txt', 'r') as f:
                return [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            return []
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while loading the list: {e}")
            return []

    def save_note(self):
        note = self.note_input.toPlainText()
        if note.strip():
            with open('notes.txt', 'a') as f:
                f.write(note + '\n')
            QMessageBox.information(self, "Success", "Note saved successfully!")
            self.note_input.clear()
        else:
            QMessageBox.warning(self, "Error", "Note cannot be empty.")

    def add_item(self):
        item = self.list_input.text()
        if item.strip():
            self.list_items.append(item)
            self.list_display.setText('\n'.join(self.list_items))
            self.list_input.clear()
        else:
            QMessageBox.warning(self, "Error", "Item cannot be empty.")

    def save_list(self):
        if self.list_items:
            with open('list.txt', 'w') as f:
                f.write('\n'.join(self.list_items))
            QMessageBox.information(self, "Success", "List saved successfully!")
        else:
            QMessageBox.warning(self, "Error", "List is empty.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NotebookApp()
    window.show()
    sys.exit(app.exec_())