import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SEQ File Viewer")
        self.setGeometry(100, 100, 800, 600)

        # MainSequence text edit
        self.MainSequence = QPlainTextEdit(self)
        self.MainSequence.setReadOnly(True)

        # SubSequence text edit
        self.SubSequence = QPlainTextEdit(self)
        self.SubSequence.setReadOnly(True)

        # Layout
        layout = QHBoxLayout()
        layout.addWidget(self.MainSequence)
        layout.addWidget(self.SubSequence)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_seq_file()

    def load_seq_file(self):
        # Open file dialog to choose .seq file (which is actually JSON)
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open SEQ File", "", "SEQ Files (*.seq);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                content = json.load(file)  # Load the JSON content

            # Display content in MainSequence
            json_text = json.dumps(content, indent=4)
            self.MainSequence.setPlainText(json_text)

            # Extract Steps content and create Taskstep list
            self.taskstep = self.extract_steps(content.get("Steps", []))
            print(self.taskstep)  # This will print the Taskstep list in the console for verification

            # Open a fixed file path in SubSequence
            fixed_path = "D:\\JinRay\\Python\\Machine_Test\\Sequences\\853-293393-010\\_Shared\\uut-config3.seq"
            self.open_subsequence(fixed_path)

    def extract_steps(self, steps):
        taskstep = []
        for step in steps:
            task_dict = {}
            for key, value in step.items():
                if isinstance(value, dict):
                    # Nested dictionary: Extract 2nd and 4th fields as key-value pair
                    sub_dict = {}
                    if len(value) > 3:  # Ensure there are enough fields to extract
                        keys = list(value.keys())
                        sub_dict[value.get(keys[1], '')] = value.get(keys[3], '')
                    task_dict[key] = sub_dict
                else:
                    task_dict[key] = value
            taskstep.append(task_dict)
        return taskstep

    def open_subsequence(self, path):
        # Open the referenced SEQ file and display its content in SubSequence
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as file:
                sub_content = json.load(file)
                sub_json_text = json.dumps(sub_content, indent=4)
                self.SubSequence.setPlainText(sub_json_text)
        else:
            self.SubSequence.setPlainText(f"Error: File '{path}' not found.")


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()