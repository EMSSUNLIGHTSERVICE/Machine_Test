import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JSON File Viewer")
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

        self.load_json_file()

    def load_json_file(self):
        # Open file dialog to choose .json file
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                content = json.load(file)  # Load the JSON content

            # Display content in MainSequence
            json_text = json.dumps(content, indent=4)
            self.MainSequence.setPlainText(json_text)

            # Extract Steps content and create Taskstep list
            self.taskstep = self.extract_steps(content.get("Steps", []))
            print(self.taskstep)  # This will print the Taskstep list in the console for verification

            # Check for Sequence Call and open corresponding file if exists
            self.check_sequence_call(self.taskstep)

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

    def check_sequence_call(self, taskstep):
        # Loop through Taskstep list and check for "Sequence Call"
        for step in taskstep:
            if "StepName" in step and step["StepName"] == "Sequence Call":
                # If "Sequence Call" is found, check for "Path" field and open the file
                if "Path" in step:
                    file_path = step["Path"]
                    self.open_subsequence(file_path)

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
