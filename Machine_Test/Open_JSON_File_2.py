import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QSyntaxHighlighter


class JSONHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # Highlighter rule for Steps block
        self.steps_rule = QTextCharFormat()
        self.steps_rule.setForeground(QColor('blue'))
        self.highlighting_rules.append((r'"Steps":\s*{', self.steps_rule))

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
        self.setWindowTitle("JSON File Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.MainSequence = QPlainTextEdit(self)
        self.MainSequence.setReadOnly(True)

        self.SubSequence = QPlainTextEdit(self)
        self.SubSequence.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.MainSequence)
        layout.addWidget(self.SubSequence)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_json_file()

    def load_json_file(self):
        # 1. Open file dialog to choose JSON file
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "", "JSON Files (*.json);;All Files (*)",
                                                   options=options)
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                content = json.load(file)

            # 2. Show content in MainSequence and highlight the "Steps" block
            json_text = json.dumps(content, indent=4)
            self.MainSequence.setPlainText(json_text)

            # Create highlighter for MainSequence
            highlighter = JSONHighlighter(self.MainSequence)

            # 3. Extract Steps content and create Taskstep list
            self.taskstep = self.extract_steps(content.get("Steps", []))

            # 4. Check for "Sequence Call" in Taskstep and load SubSequence file if found
            self.handle_sequence_call()

    def extract_steps(self, steps):
        taskstep = []
        for step in steps:
            task_dict = {}
            for i, value in enumerate(step.values()):
                if isinstance(value, dict):
                    # Nested dictionary, create a sub-dictionary from 2nd and 4th fields
                    sub_dict = {list(value.keys())[1]: list(value.values())[3]}
                    task_dict[list(step.keys())[0]] = sub_dict
                else:
                    task_dict[list(step.keys())[0]] = value
            taskstep.append(task_dict)
        return taskstep

    def handle_sequence_call(self):
        for task in self.taskstep:
            if "Sequence Call" in task:
                path = task.get("Path", "")
                if path and os.path.exists(path):
                    # Open the sequence file at the given path
                    with open(path, 'r', encoding='utf-8') as sub_file:
                        sub_content = json.load(sub_file)

                    # Display the content in SubSequence QPlainTextEdit
                    sub_json_text = json.dumps(sub_content, indent=4)
                    self.SubSequence.setPlainText(sub_json_text)

                    # Highlighter for SubSequence
                    sub_highlighter = JSONHighlighter(self.SubSequence)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()