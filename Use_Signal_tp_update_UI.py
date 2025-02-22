
import time

from PySide6.QtWidgets import QApplication, QTextBrowser
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QIcon
from threading import Thread

# 如果使用的是 PySide6 ， 它目前有个bug， 必须要让 QUiLoader 的实例化在 QApplication 的实例化之前。
# 在QApplication之前先实例化
uiLoader = QUiLoader()

keep_running = True

from PySide6.QtCore import Signal,QObject
print(
    "Start App"
)
# 自定义信号源对象类型，一定要继承自 QObject
class MySignals(QObject):

    # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    text_print = Signal(QTextBrowser,str)
    #text_print = Signal(str) 如果界面上只有一个,那么第一个参数QTextBrowser可以不要.

    # 还可以定义其他种类的信号
    update_table = Signal(str)

# 实例化
global_ms = MySignals()

class Stats:

    def __init__(self):
        # 再加载界面
        self.ui = uiLoader.load('main.ui')
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('main.ui')

        self.ui.Do_task0.clicked.connect(self.task0)
        self.ui.Do_task1.clicked.connect(self.task1)
        self.ui.Do_task2.clicked.connect(self.task2)
        self.ui.StopButton.clicked.connect(self.stoptask)
        self.ui.restart_thread_Button.clicked.connect(self.restartthreadButton)
        self.ui.actionLoad_Seq_File.triggered.connect(self.actionLoadSeqFile)

        # 自定义信号的处理函数
        global_ms.text_print.connect(self.printToGui)


    def printToGui(self,fb,text):
        fb.append(str(text))
        fb.ensureCursorVisible()        #光标移动到最下面，保持可见

    def task0(self):
        for i in range(1,6):
            global_ms.text_print.emit(self.ui.infoBox1, f'task1输出内容:{i}')
            time.sleep(1)

    def task1(self):
        #函数里面再定义函数，可以的
        def threadFunc():
            global keep_running
            # 通过Signal 的 emit 触发执行 主线程里面的处理函数
            # emit参数和定义Signal的数量、类型必须一致
            while keep_running:
                for i in range(1,6):
                    global_ms.text_print.emit(self.ui.infoBox1, f'task1输出内容:{i}')
                    time.sleep(1)

        thread = Thread(target = threadFunc )
        thread.start()

    def task2(self):
        def threadFunc():
            global_ms.text_print.emit(self.ui.infoBox2, 'task2输出内容')
        thread = Thread(target=threadFunc)
        thread.start()

    def actionLoadSeqFile(self):
        def threadFunc():
            global_ms.text_print.emit(self.ui.infoBox2, '使用工具栏的actionLoadSeqFile输出内容')
        thread = Thread(target=threadFunc)
        thread.start()
        self.ui.statusbar.showMessage('        打开文件{filePath}')

    def stoptask(self):
        global keep_running
        keep_running = False  # 停止循环

    def restartthreadButton(self):
        global keep_running
        keep_running = True  # 重启循环


app = QApplication()
#app = QApplication([])
#icon = QIcon('JR Logo.jpg')
#app.setWindowIcon(icon)
app.setWindowIcon(QIcon('JR_Splash_L_50x60'))
stats = Stats()
stats.ui.show()
app.exec()