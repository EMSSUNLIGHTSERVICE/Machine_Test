import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QFileDialog, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QSyntaxHighlighter


class JSONHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []

        # Highlighter rule for "Steps" block
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
        self.setWindowTitle("SEQ File Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.MainSequence = QPlainTextEdit(self)
        self.MainSequence.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.MainSequence)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_seq_file()

    def load_seq_file(self):
        # 1. Open file dialog to choose .seq file (which is actually JSON)
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open SEQ File", "", "SEQ Files (*.seq);;All Files (*)",
                                                   options=options)
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                content = json.load(file)  # Load the JSON content

            # 2. Display content in MainSequence and highlight the "Steps" block
            json_text = json.dumps(content, indent=4)
            self.MainSequence.setPlainText(json_text)

            # Apply highlighter for the first Steps block
            highlighter = JSONHighlighter(self.MainSequence)

            # 3. Extract Steps content and create Taskstep list
            self.taskstep = self.extract_steps(content.get("Steps", []))
            print(self.taskstep)  # This will print the Taskstep list in the console for verification

    def extract_steps(self, steps):
        taskstep = []
        for step in steps:
            task_dict = {}
            for key, value in step.items():
                if isinstance(value, dict):
                    # Nested dictionary: Extract 2nd and 4th fields as key-value pair
                    sub_dict = {}
                    if len(value) > 3:  # Ensure there are enough fields to extract
                        sub_dict[value.get(list(value.keys())[1], '')] = value.get(list(value.keys())[3], '')
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