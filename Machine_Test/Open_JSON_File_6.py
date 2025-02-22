import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QTextCharFormat, QSyntaxHighlighter

class JSONHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # Highlighter rule for "Steps" block
        self.steps_rule = QTextCharFormat()
        self.steps_rule.setForeground(QColor('blue'))

        # Match the "Steps" key and the opening bracket of the array
        self.highlighting_rules.append((r'\"Steps\":\s*\[', self.steps_rule))  # Match "Steps" key with [ after it
        self.highlighting_rules.append((r'\{', self.steps_rule))  # Match the opening brace of objects inside Steps

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)


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

            # Display content in MainSequence and highlight the "Steps" block
            json_text = json.dumps(content, indent=4)
            self.MainSequence.setPlainText(json_text)

            # Apply highlighter for the first Steps block
            highlighter = JSONHighlighter(self.MainSequence)

            # Extract Steps content and create Taskstep list
            self.taskstep = self.extract_steps(content.get("Steps", []))
            print(self.taskstep)  # This will print the Taskstep list in the console for verification

            # If there are Sequence Calls, open the referenced file and display it in SubSequence
            for step in self.taskstep:
                if "Sequence Call" in step:
                    path = step.get("Path")
                    if path and os.path.exists(path):
                        with open(path, 'r', encoding='utf-8') as file:
                            sub_content = json.load(file)
                            sub_json_text = json.dumps(sub_content, indent=4)
                            self.SubSequence.setPlainText(sub_json_text)

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


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
