import sys
from pickle import GLOBAL

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QIcon

import tkinter
import pyads
import time
import threading

timer_thread = threading.Thread()
timer_thread.daemon = True  # 将线程设置为守护线程

import tkinter as tk
from tkinter import filedialog  #tkinter 图形化界面包

# 在QApplication之前先实例化
uiLoader = QUiLoader()

LOG_LINE_NUM = 0        # 日志默认条数
keep_running = True     # 控制循环的标志

UUTPowerButtonState = False

AndonRedButtonState = False
AndonBlueButtonState = False
AndonYellowButtonState = False
AndonGreenButtonState = False
AndonWhiteButtonState = False

class Stats:
    def __init__(self):
        # 再加载界面
        self.ui = uiLoader.load('Main_Window.ui')

        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('Main_Window.ui')

        self.ui.DeviceStateButton.clicked.connect(self.devicestateshow)
        self.ui.ValveButton.clicked.connect(self.valveshow)
        self.ui.SubValveButton.clicked.connect(self.subvalveshow)
        self.ui.AIOButton.clicked.connect(self.aioshow)
        self.ui.DIOButton.clicked.connect(self.dioshow)

        self.ui.StartTestButton.clicked.connect(self.handlestarttestbutton)
        self.ui.UUTPowerButton.clicked.connect(self.handleUUTPowerbutton)

        self.ui.AndonRedButton.clicked.connect(self.handleAndonRedButton)
        self.ui.AndonBlueButton.clicked.connect(self.handleAndonBlueButton)
        self.ui.AndonYellowButton.clicked.connect(self.handleAndonYellowButton)
        self.ui.AndonGreenButton.clicked.connect(self.handleAndonGreenButton)
        self.ui.AndonWhiteButton.clicked.connect(self.handleAndonWhiteButton)


        self.ui.TPC1_Control.returnPressed.connect(self.SetTPC1Control)

        self.ui.actionLoad_Test_File.triggered.connect(self.Machine_Test_load_test_file)

    # 打开端口 （ADS相关函数）
    def TwinCAT_port_open(self, AmsNetID, port):
        global Plc
        # 获取netID以及port，测试时候用本机地址 '127.0.0.1.1.1'# '851'#
        # AmsNetID = self.netID_text.get(1.0, tkinter.END)
        #AmsNetID = '192.168.1.160.1.1'
        # port = self.port_text.get(1.0, tkinter.END)
        #port = '27916'
        try:
            # 打开TwinCAT端口
            Plc = pyads.Connection(AmsNetID, eval(port))
            Plc.open()
            self.write_log_to_text('Adress{}，Port{}，Communication port status is normal.'.format(AmsNetID, port).replace('\n', ''))
        except:
            self.write_log_to_text('Adress{}，Port{}，Port connection failed'.format(AmsNetID, port).replace('\n', '')
                                   + ': ADS service is not enabled or the address port is illegal')

    # 读取当前时间
    def get_current_time(self):
        current_time = time.strftime('%H:%M:%S %d-%m-%Y', time.localtime(time.time()))
        return current_time

    # 写入变量值 （ADS相关函数）
    def write_value_byname(self, Vname, Value, data_type):
        global Plc
        try:
            # replace函数取消换行，format函数填入变量名，值，数据类型，先formate再replace，不然Vname等变量末尾换行符去不掉
            str = 'Plc.write_by_name(\'{}\', {}, pyads.PLCTYPE_{})'.format(Vname, Value, data_type).replace('\n', '')
            # 打印写入语句到终端，以供检查
            #print(str)
            # 执行写入语句
            eval(str)
            self.write_log_to_text('{} type variable {} Write Success. '.format(data_type, Vname).replace('\n', ''))
        except:
            self.write_log_to_text(' Writing failed, variable not found, please check parameter settings.')

    # 读取变量值 （ADS相关函数）
    def read_value_byname(self, Vname, data_type):
        global Plc
        try:
            # replace函数取消换行，format函数填入变量名，变量类型
            twincatportdata = 'Plc.read_by_name(\'{}\', pyads.PLCTYPE_{})'.format(Vname, data_type).replace('\n', '')
            # 打印读取语句到终端，以供检查
            print(twincatportdata)
            # 执行读取语句
            Value = eval(twincatportdata)
            #print(Value)
            return Value
            self.write_log_to_text('{} type variable {} Read Success. '.format(data_type, Vname).replace('\n', ''))
        except:
            # 打印读取失败日志
            self.write_log_to_text(' Reading failed, variable not found, please check parameter settings.')

    # 日志打印，需要获取系统时间
    def write_log_to_text(self, logmsg):
        global LOG_LINE_NUM
        # 每次调用记录信息发生的时间
        current_time = self.get_current_time()
        # 日志信息 + 换行
        logmsg_in = str(current_time) + " " + str(logmsg)
        # 界面上显示的信息数量
        if LOG_LINE_NUM <= 1000:
            # 在末尾打印一条日志
            self.ui.LogText.append(logmsg_in)       # 在编辑框末尾添加文本
            self.ui.LogText.ensureCursorVisible()       # 自动翻滚到当前添加的这行
            # 信息条数+1
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            # 删除第一行的内容
            #self.ui.LogText.clear()
            self.ui.LogText.move(1.0,2.0)
            # 打印一条新的信息
            self.ui.LogText.append(logmsg_in)
        # 移动光标
        #self.ui.LogText.focus_force()

    def Machine_Test_load_test_file(self):
        file_path = filedialog.askopenfilename(title="选择seq文件", filetypes=[("seq Files", "*.seq")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.ui.MainSequence.clear()
                self.ui.MainSequence.insertPlainText(content)

    def devicestateshow(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        self.TwinCAT_port_open('192.168.1.160.1.1', '27916')

    def valveshow(self):
        self.ui.stackedWidget.setCurrentIndex(5)
        self.TwinCAT_port_open('192.168.1.160.1.1', '27911')

        Value = self.read_value_byname('ALICAT_100PSIG_PC.SM_3.Device_Readings_TxPDO_Map.Reading_1', 'REAL')
        # 清除Value显示栏当前值
        self.ui.TPC1_Read.clear()
        # 讲读取出来的值显示
        self.ui.TPC1_Read.setText(str(Value))

    def subvalveshow(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.TwinCAT_port_open('192.168.1.160.1.1', '27911')

    def aioshow(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def dioshow(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def handlestarttestbutton(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        self.TwinCAT_port_open('192.168.1.160.1.1', '27916')

    def handleUUTPowerbutton(self):
        global UUTPowerButtonState
        if UUTPowerButtonState == False:
            UUTPowerButtonState = True
            self.write_value_byname('POWER MEASURE (EK1100).RELAY_CONTROL (EL2008).SM_0.ENABLE_15V_Output', 'True', 'BOOL')
            self.write_value_byname('POWER MEASURE (EK1100).RELAY_CONTROL (EL2008).SM_0.ENABLE_POWER_Output', 'True', 'BOOL')

        else:
            UUTPowerButtonState = False
            self.write_value_byname('POWER MEASURE (EK1100).RELAY_CONTROL (EL2008).SM_0.ENABLE_15V_Output', 'False', 'BOOL')
            self.write_value_byname('POWER MEASURE (EK1100).RELAY_CONTROL (EL2008).SM_0.ENABLE_POWER_Output', 'False', 'BOOL')


    def handleAndonRedButton(self):
        global AndonRedButtonState
        if AndonRedButtonState == False:
            AndonRedButtonState = True
            self.write_value_byname('POWER MEASURE (EK1100).RELAY_CONTROL (EL2008).SM_0.RED_Output', 'True', 'BOOL')
            self.ui.AndonRedButton.setIcon(QIcon('image\Andon Red On.png'))
        else:
            AndonRedButtonState = False
            self.write_value_byname('POWER MEASURE (EK1100).RELAY_CONTROL (EL2008).SM_0.RED_Output', 'False', 'BOOL')
            self.ui.AndonRedButton.setIcon(QIcon('image\Andon Red Off.png'))

    def handleAndonBlueButton(self):
        global AndonBlueButtonState
        if AndonBlueButtonState == False:
            AndonBlueButtonState = True
            self.write_value_byname('POWER MEASURE (EK1100).RELAY_CONTROL (EL2008).SM_0.BLUE_Output', 'True', 'BOOL')
            self.ui.AndonBlueButton.setIcon(QIcon('image\Andon Blue On.png'))
        else:
            AndonBlueButtonState = False
            self.write_value_byname('POWER MEASURE (EK1100).RELAY_CONTROL (EL2008).SM_0.BLUE_Output', 'False', 'BOOL')
            self.ui.AndonBlueButton.setIcon(QIcon('image\Andon Blue Off.png'))

    def handleAndonYellowButton(self):
        global AndonYellowButtonState
        if AndonYellowButtonState == False:
            AndonYellowButtonState = True
            self.write_value_byname('POWER MEASURE (EK1100).RELAY_CONTROL (EL2008).SM_0.YELLOW_Output', 'True', 'BOOL')
            self.ui.AndonYellowButton.setIcon(QIcon('image\Andon Yelow On.png'))
        else:
            AndonYellowButtonState = False
            self.write_value_byname('POWER MEASURE (EK1100).RELAY_CONTROL (EL2008).SM_0.YELLOW_Output', 'False', 'BOOL')
            self.ui.AndonYellowButton.setIcon(QIcon('image\Andon Yelow Off.png'))

    def handleAndonGreenButton(self):
        global AndonGreenButtonState
        if AndonGreenButtonState == False:
            AndonGreenButtonState = True
            self.write_value_byname('POWER MEASURE (EK1100).RELAY_CONTROL (EL2008).SM_0.GREEN_Output', 'True', 'BOOL')
            self.ui.AndonGreenButton.setIcon(QIcon('image\Andon Green On.png'))
        else:
            AndonGreenButtonState = False
            self.write_value_byname('POWER MEASURE (EK1100).RELAY_CONTROL (EL2008).SM_0.GREEN_Output', 'False', 'BOOL')
            self.ui.AndonGreenButton.setIcon(QIcon('image\Andon Green Off.png'))

    def handleAndonWhiteButton(self):
        global AndonWhiteButtonState
        if AndonWhiteButtonState == False:
            AndonWhiteButtonState = True
            self.write_value_byname('POWER MEASURE (EK1100).RELAY_CONTROL (EL2008).SM_0.WHITE_Output', 'True', 'BOOL')
            self.ui.AndonWhiteButton.setIcon(QIcon('image\Andon White On.png'))
        else:
            AndonWhiteButtonState = False
            self.write_value_byname('POWER MEASURE (EK1100).RELAY_CONTROL (EL2008).SM_0.WHITE_Output', 'False', 'BOOL')
            self.ui.AndonWhiteButton.setIcon(QIcon('image\Andon White Off.png'))

    def SetTPC1Control(self):
        Value = self.ui.TPC1_Control.text()
        self.write_value_byname('ALICAT_100PSIG_PC.SM_2.Setpoint_RxPDO_Map.Setpoint', Value, 'REAL')

    def start_timer(self):
        global keep_running
        while keep_running:
            self.read_value_byname()
            time.sleep(0.5)  # 500毫秒
        else:
            timer_thread.stop()

app = QApplication([]) # 开APP
app.setWindowIcon(QIcon('image\JR Logo.jpg'))
stats = Stats()
stats.ui.show()
app.exec()