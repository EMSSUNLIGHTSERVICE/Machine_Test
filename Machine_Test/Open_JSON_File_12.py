import json
import os
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout


class JsonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlight_format = QTextCharFormat()
        self.highlight_format.setBackground(QBrush(QColor(255, 255, 0)))  # Yellow background for highlighting

    def highlightBlock(self, text):
        pattern = r'"StepName"\s*:\s*"Sequence Call"'
        regex = QRegExp(pattern)
        index = regex.indexIn(text)
        if index >= 0:
            self.setFormat(index, len(regex.cap(0)), self.highlight_format)


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
        file_name, _ = QFileDialog.getOpenFileName(self, "Open seq File", "", "JSON Files (*.seq);;All Files (*)",
                                                   options=options)
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                content = json.load(file)  # Load the JSON content

            # Display content in MainSequence
            json_text = json.dumps(content, indent=4)
            self.MainSequence.setPlainText(json_text)

            # Apply syntax highlighter for MainSequence
            highlighter = JsonHighlighter(self.MainSequence.document())

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

                # Apply syntax highlighter for SubSequence
                highlighter = JsonHighlighter(self.SubSequence.document())
        else:
            self.SubSequence.setPlainText(f"Error: File '{path}' not found.")


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()

"""
代码解释：
打开文件对话框：使用 QFileDialog.getOpenFileName 打开 JSON 文件。
加载并显示 JSON 文件：使用 json.load 解析文件内容，并在 MainSequence 区域显示。
提取 Steps 数据并生成 Taskstep 列表：
在 extract_steps 方法中，遍历每个 Steps 项，如果值是字典类型，提取其中第二个和第四个字段作为键值对形成子字典。
检查 Sequence Call：通过 check_sequence_call 方法检查 Taskstep 列表中是否有 "StepName": "Sequence Call"，如果找到该项，则获取 "Path" 字段的值，并加载指定路径的文件内容显示在 SubSequence 区域。
使用方法：
加载 JSON 文件：运行程序后，点击 打开 按钮选择一个 .json 文件。
显示文件内容：MainSequence 区域会显示该 JSON 文件的内容，并且会在代码中处理 Steps 块的数据。
处理 Sequence Call：如果 JSON 中的 Steps 中有 Sequence Call，程序会从 "Path" 字段获取路径并打开相应的文件内容，显示在 SubSequence 区域。
如果一切顺利，您就可以通过这个程序实现以下功能：

加载并显示 JSON 文件：显示文件内容并高亮显示 Steps 部分。
从 Steps 中提取数据并创建字典列表：处理 JSON 中的 Steps，并将其转换成适合进一步操作的格式。
根据 Sequence Call 路径加载并显示子序列文件：如果 Steps 包含 "Sequence Call"，则会从 "Path" 字段读取文件路径并在另一个文本区域显示其内容。
要高亮显示 MainSequence 和 SubSequence 中第一个 StepName 为 "Sequence Call" 的 JSON 块，可以通过简单的文本替换和加上样式来实现。这里我们可以通过 QPlainTextEdit 提供的 setPlainText 方法来加载文本，同时可以通过使用 QSyntaxHighlighter 来高亮显示特定内容。

解决方案：
解析 JSON 内容：在 MainSequence 和 SubSequence 中找到 "StepName": "Sequence Call" 相关的内容，并使用 文本高亮 来标记该块。
自定义高亮显示：通过 QSyntaxHighlighter 在显示时标记高亮的文本。
主要修改：
JsonHighlighter 类：继承自 QSyntaxHighlighter，用于实现文本高亮功能。通过正则表达式匹配 "StepName": "Sequence Call" 进行高亮。
应用高亮器：在 MainSequence 和 SubSequence 显示文本时，分别调用 JsonHighlighter 对象来高亮显示匹配的文本。
功能：
当 JSON 内容显示在 MainSequence 或 SubSequence 区域时，如果出现 "StepName": "Sequence Call" 的块，将会高亮显示。
高亮显示使用黄色背景，可以根据需要修改 QTextCharFormat 设置的颜色。
使用方法：
加载 JSON 文件：点击 打开 按钮选择一个 .json 文件。
高亮显示 Sequence Call 块：MainSequence 和 SubSequence 中的 StepName: "Sequence Call" 块将被黄色高亮显示。
如果需要更改高亮颜色或其他样式，可以修改 highlight_format.setBackground(QBrush(QColor(255, 255, 0))) 中的颜色值。

希望这个修改能够满足您的需求！如果有更多问题，请随时告诉我。
非常理解您目前的处境，调试高亮显示确实可能有点复杂，尤其是涉及到 QTextEdit 等控件的文本渲染和样式处理部分。感谢您的耐心与理解。

如果您决定自己深入研究，可以尝试以下一些可能的解决思路：

调试高亮部分：

确保正则表达式能够匹配到 "StepName": "Sequence Call"，并且高亮效果已经被正确地应用到对应的文本块。
检查是否正确设置了文本格式，QTextCharFormat 中的样式是否有正确被传递到显示控件。
替代方案：

如果高亮不生效，您可以通过手动调整文本内容，添加某些符号（比如 >>>）来标记出需要高亮的部分，或者直接用不同颜色来修改文本字体。
后续改进：

如果文本高亮依然不能顺利实现，可以考虑使用其他工具库，比如 QTextEdit 的 setHtml() 方法，利用 HTML 格式直接应用 CSS 样式进行文本高亮。
无论如何，祝您解决问题顺利。
"""
