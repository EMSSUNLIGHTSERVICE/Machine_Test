from PyQt5.QtWidgets import QToolButton
from PySide6.QtWidgets import QApplication, QLineEdit, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QIcon

import pandas as pd     # 读取 Excel 文件需要
import pyads
import time
from threading import Thread, Event
from PySide6.QtCore import Signal,QObject
import numpy as np  #判断数据类型USINT

from tkinter import filedialog  #tkinter 图形化界面包，给file dialog

# 如果使用的是 PySide6 ， 它目前有个bug， 必须要让 QUiLoader 的实例化在 QApplication 的实例化之前。
# 在QApplication之前先实例化
uiLoader = QUiLoader()

LOG_LINE_NUM = 0        # 日志默认条数
Valve_Pag_Refresh_running = True     # Valve页面刷新正在进行的标志

UUTPowerButtonState = False

AndonRedButtonState=AndonBlueButtonState=AndonYellowButtonState=AndonGreenButtonState=AndonWhiteButtonState=False

Manifold1_Group0=Manifold1_Group1=Manifold1_Group2=Manifold1_Group3=Manifold2_Group0=Manifold2_Group1=Manifold2_Group2=Manifold2_Group3=0

TV1State=TV2State=TV3State=TV4State=TV5State=TV6State=TV7State=TV8State=TV9State=TV10State=TV11State=TV12State=UUT_CDAState=False
TV13State=TV14State=TV15State=TV16State=TV17State=TV18State=TV19State=TV20State=TV21State=TV22State=TV23State=TV24State=SPACE_CDAState=False
TV25State=TV26State=TV27State=TV28State=TV29State=TV30State=TV31State=TV32State=TV33State=TV34State=TV35State=TV36State=False
TV37State=TV38State=TV39State=TV40State=TV41State=TV42State=TV43State=TV44State=TV45State=TV46State=TV47State=TV48State=TV49State=False

# 自定义信号源对象类型，一定要继承自 QObject
class Refresh_Signals(QObject):

    # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    text_print = Signal(QLineEdit,str)      #REAL 数据类型
    text_print_bool = Signal(QToolButton, bool)
    text_print_tv= Signal(QToolButton, int)
    #text_print = Signal(str) 如果界面上只有一个控件QTextBrowser,那么第一个参数QTextBrowser可以不要.
    # 还可以定义其他种类的信号
    update_table = Signal(str)
# 实例化
Pag_Refresh = Refresh_Signals()

class Basics:
    def __init__(self):
        # 再加载界面
        self.ui = uiLoader.load('Main_Window.ui')
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        self.ui = QUiLoader().load('Main_Window.ui')

        self.stop_event = Event()  # 线程停止信号
        # self.ui = self.initialize_ui()  # 这里是你的 UI 初始化逻辑

        # 自定义信号的处理函数
        Pag_Refresh.text_print.connect(self.printToUI)
        Pag_Refresh.text_print_bool.connect(self.printToUIbool)
        Pag_Refresh.text_print_tv.connect(self.printToUItv)


        self.threads_running = True  # 控制线程是否继续运行
        self.plc_27911 = None  # 存储 27911 端口连接
        self.plc_27916 = None  # 存储 27916 端口连接
        self.plc_851 = None    # 存储 851 端口连接
        self.thread_27911 = None  # 线程变量
        self.thread_27916 = None  # 线程变量
        self.thread_851 = None  # 线程变量

        self.ui.DeviceStateButton.clicked.connect(self.devicestateshow)
        self.ui.ValveButton.clicked.connect(self.valveshow)
        self.ui.SubValveButton.clicked.connect(self.subvalveshow)
        self.ui.AIOButton.clicked.connect(self.aioshow)
        self.ui.DIOButton.clicked.connect(self.dioshow)

        self.ui.StartTestButton.clicked.connect(self.handlestarttestbutton)
        self.ui.StopTestButton.clicked.connect(self.handlestoptestbutton)

        self.ui.UUTPowerButton.clicked.connect(self.handleUUTPowerbutton)

        self.ui.AndonRedButton.clicked.connect(self.handleAndonRedButton)
        self.ui.AndonBlueButton.clicked.connect(self.handleAndonBlueButton)
        self.ui.AndonYellowButton.clicked.connect(self.handleAndonYellowButton)
        self.ui.AndonGreenButton.clicked.connect(self.handleAndonGreenButton)
        self.ui.AndonWhiteButton.clicked.connect(self.handleAndonWhiteButton)

        self.ui.TPC1_Control.returnPressed.connect(self.SetTPC1Control)
        self.ui.TPC2_Control.returnPressed.connect(self.SetTPC2Control)

        self.ui.TV1.clicked.connect(self.toggle_TV1button)
        self.ui.TV2.clicked.connect(self.toggle_TV2button)
        self.ui.TV3.clicked.connect(self.toggle_TV3button)
        self.ui.TV4.clicked.connect(self.toggle_TV4button)
        self.ui.TV5.clicked.connect(self.toggle_TV5button)
        self.ui.TV6.clicked.connect(self.toggle_TV6button)
        self.ui.TV7.clicked.connect(self.toggle_TV7button)
        self.ui.TV8.clicked.connect(self.toggle_TV8button)
        self.ui.TV9.clicked.connect(self.toggle_TV9button)
        self.ui.TV10.clicked.connect(self.toggle_TV10button)
        self.ui.TV11.clicked.connect(self.toggle_TV11button)
        self.ui.TV12.clicked.connect(self.toggle_TV12button)
        self.ui.TV13.clicked.connect(self.toggle_TV13button)
        self.ui.TV14.clicked.connect(self.toggle_TV14button)
        self.ui.TV15.clicked.connect(self.toggle_TV15button)
        self.ui.TV16.clicked.connect(self.toggle_TV16button)
        self.ui.TV17.clicked.connect(self.toggle_TV17button)
        self.ui.TV18.clicked.connect(self.toggle_TV18button)
        self.ui.TV19.clicked.connect(self.toggle_TV19button)
        self.ui.TV20.clicked.connect(self.toggle_TV20button)
        self.ui.TV21.clicked.connect(self.toggle_TV21button)
        self.ui.TV22.clicked.connect(self.toggle_TV22button)
        self.ui.TV23.clicked.connect(self.toggle_TV23button)
        self.ui.TV24.clicked.connect(self.toggle_TV24button)
        self.ui.TV25.clicked.connect(self.toggle_TV25button)
        self.ui.TV26.clicked.connect(self.toggle_TV26button)
        self.ui.TV27.clicked.connect(self.toggle_TV27button)
        self.ui.TV28.clicked.connect(self.toggle_TV28button)
        self.ui.TV29.clicked.connect(self.toggle_TV29button)
        self.ui.TV30.clicked.connect(self.toggle_TV30button)
        self.ui.TV31.clicked.connect(self.toggle_TV31button)
        self.ui.UUT_CDA.clicked.connect(self.toggle_UUT_CDAbutton)
        self.ui.SPACE_CDA.clicked.connect(self.toggle_SPACE_CDAbutton)

        self.ui.actionLoad_Test_File.triggered.connect(self.Machine_Test_load_test_file)
        self.ui.SystemOnStateLight.setIcon(QIcon("image\Lighter_Off.png"))
    # 这个函数将对控件的操作与线程分隔开
    def printToUI(self, UIObject, Value):
        #UIObject.clear()
        UIObject.setText(Value)

    def printToUIbool(self, UIObject, Value):
        if Value == True:
            UIObject.setIcon(QIcon("image\Lighter_On.png"))
        else:
            UIObject.setIcon(QIcon("image\Lighter_Off.png"))

    def printToUItv(self, UIObject, Value):
        global TV1State, TV2State, TV3State, TV4State, TV5State, TV6State, TV7State, TV8State

        name = UIObject.objectName()
        print(name)
        if name == "TV1":
            print("2432423441241241224124124142124124124124142424")
            binary_str = bin(Value)[2:].zfill(8)  # 转换为 8 位二进制字符串
            TV1State, TV2State, TV3State, TV4State, TV5State, TV6State, TV7State, TV8State = map(lambda x: x == '1',binary_str)
        print(TV1State)
        print(TV8State)
        if TV8State:
            self.ui.TV1.setIcon(QIcon("image\Lighter_Off.png"))
    """
    def int_to_tv_states(value):
        if not (0 <= value <= 255):
            raise ValueError("Input must be between 0 and 255")

        binary_str = bin(value)[2:].zfill(8)  # 转换为 8 位二进制字符串
        TV1State, TV2State, TV3State, TV4State, TV5State, TV6State, TV7State, TV8State = map(lambda x: x == '1',binary_str)

        return TV1State, TV2State, TV3State, TV4State, TV5State, TV6State, TV7State, TV8State
    """
    # 读取 Excel 文件 channeslnfo.xlsx
    def process_excel(self):
        file_path = r"C:\Users\Public\Documents\Gas Lab Manager\System.Lam.DEP\default\Hardware\channeslnfo.xlsx"
        df = pd.read_excel(file_path)
        # 提取所需字段
        required_columns = ['//port', 'UI_ObjectName', 'twincat_datatype', 'io_path', 'io_direction', 'located']
        df = df[required_columns]
        # 过滤数据并存入元组
        Device27916RefreshList = tuple(
            zip(
                df.loc[
                    (df['//port'] == 27916) & (df['io_direction'] == 'in') & (df['located'] == 'DevicePage'), '//port'],
                df.loc[(df['//port'] == 27916) & (df['io_direction'] == 'in') & (
                        df['located'] == 'DevicePage'), 'UI_ObjectName'],
                df.loc[(df['//port'] == 27916) & (df['io_direction'] == 'in') & (
                        df['located'] == 'DevicePage'), 'twincat_datatype'],
                df.loc[
                    (df['//port'] == 27916) & (df['io_direction'] == 'in') & (df['located'] == 'DevicePage'), 'io_path']
            )
        )
        Valve27911RefreshList = tuple(
            zip(
                df.loc[
                    (df['//port'] == 27911) & (df['io_direction'] == 'in') & (df['located'] == 'ValvePage'), '//port'],
                df.loc[(df['//port'] == 27911) & (df['io_direction'] == 'in') & (
                        df['located'] == 'ValvePage'), 'UI_ObjectName'],
                df.loc[(df['//port'] == 27911) & (df['io_direction'] == 'in') & (
                        df['located'] == 'ValvePage'), 'twincat_datatype'],
                df.loc[
                    (df['//port'] == 27911) & (df['io_direction'] == 'in') & (df['located'] == 'ValvePage'), 'io_path']
            )
        )
        Valve27916RefreshList = tuple(
            zip(
                df.loc[
                    (df['//port'] == 27916) & (df['io_direction'] == 'in') & (df['located'] == 'ValvePage'), '//port'],
                df.loc[(df['//port'] == 27916) & (df['io_direction'] == 'in') & (
                        df['located'] == 'ValvePage'), 'UI_ObjectName'],
                df.loc[(df['//port'] == 27916) & (df['io_direction'] == 'in') & (
                        df['located'] == 'ValvePage'), 'twincat_datatype'],
                df.loc[
                    (df['//port'] == 27916) & (df['io_direction'] == 'in') & (df['located'] == 'ValvePage'), 'io_path']
            )
        )
        return Device27916RefreshList, Valve27911RefreshList, Valve27916RefreshList

    def threadFunc(self, valve_list, port):
        global Valve_Pag_Refresh_running

        # 线程内部打开自己的 TwinCAT 端口
        plc = pyads.Connection('192.168.1.160.1.1', port)
        plc.open()
        print(f"Connected to TwinCAT at 192.168.1.160.1.1:{port}")

        while Valve_Pag_Refresh_running:
            for item in valve_list:
                try:
                    data_type = getattr(pyads, item[2], pyads.PLCTYPE_REAL)  # # 动态获取 pyads 数据类型, 默认值为 REAL
                    Value = plc.read_by_name(item[3], data_type)
                    #Value = plc.read_by_name(item[3], pyads.PLCTYPE_REAL)
                    Value = str(round(Value, 4))

                    # 获取 UI 组件
                    target_widget = getattr(self.ui, item[1], None)
                    if target_widget:
                        Pag_Refresh.text_print.emit(target_widget, Value)
                    else:
                        print(f"Warning: {item[1]} does not exist in self.ui")
                except pyads.ADSError as e:
                    print(f"Error reading {item[3]} on port {port}: {e}")

            time.sleep(0.5)  # 控制刷新频率

        plc.close()
        print(f"Closed TwinCAT connection on port {port}")

    # 打开端口 （ADS相关函数）
    def TwinCAT_port_open(self, AmsNetID, port):
        global Plc
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

    # 向端口写入变量值 （ADS相关函数）
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

    # 从端口读取变量值 （ADS相关函数）
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

        # 从端口读取变量值,没有Log （ADS相关函数）
    def read_value_byname_noLog(self, Vname, data_type):
        global Plc
        # replace函数取消换行，format函数填入变量名，变量类型
        twincatportdata = 'Plc.read_by_name(\'{}\', pyads.PLCTYPE_{})'.format(Vname, data_type).replace('\n', '')
        # 执行读取语句
        Value = eval(twincatportdata)
        return Value

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
        file_path = filedialog.askopenfilename(title="Select seq File", filetypes=[("seq Files", "*.seq")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.ui.Sequence.clear()
                self.ui.Sequence.insertPlainText(content)

    def devicestateshow(self):
        global Valve_Pag_Refresh_running
        Valve_Pag_Refresh_running = True
        self.ui.stackedWidget.setCurrentIndex(4)
        self.TwinCAT_port_open('192.168.1.160.1.1', '27916')
        # 启动1个线程
        thread_27916 = Thread(target=self.threadFuncdevice, args=(device_27916, 27916))
        thread_27916.start()

    def threadFuncdevice(self, valve_list, port):
        global Valve_Pag_Refresh_running

        # 线程内部打开自己的 TwinCAT 端口
        plc = pyads.Connection('192.168.1.160.1.1', port)
        plc.open()
        print(f"Connected to TwinCAT at 192.168.1.160.1.1:{port}")

        while Valve_Pag_Refresh_running:
            for item in valve_list:
                try:
                    data_type = getattr(pyads, item[2], pyads.PLCTYPE_REAL)  # 动态获取 pyads 数据类型, 默认值为 REAL
                    Value = plc.read_by_name(item[3], data_type)

                    # 处理读回Value不同类型的数据
                    if type(Value) is float:
                        Value = str(round(Value, 4))
                        # 获取 UI 组件
                        target_widget = getattr(self.ui, item[1], None)
                        if target_widget:
                            Pag_Refresh.text_print.emit(target_widget, Value)
                        else:
                            print(f"Warning: {item[1]} does not exist in self.ui")

                    elif type(Value) is int and item[2] == "PLCTYPE_USINT":
                        target_widget = getattr(self.ui, item[1], None)
                        if target_widget:
                            print("dddddddddddddddddddddddddddddddddddddddddddddddddd")
                            Pag_Refresh.text_print_tv.emit(target_widget, Value)
                        else:
                            print(f"Warning: {item[1]} does not exist in self.ui")
                        print(item[1])
                        print("Value is USINT (uint8)")
                        print(Value)

                    elif type(Value) is int:
                        Value = str(round(Value/1000000, 4))
                        target_widget = getattr(self.ui, item[1], None)
                        if target_widget:
                            Pag_Refresh.text_print.emit(target_widget, Value)
                        else:
                            print(f"Warning: {item[1]} does not exist in self.ui")

                    elif type(Value) is bool:
                        target_widget = getattr(self.ui, item[1], None)
                        if target_widget:
                            Pag_Refresh.text_print_bool.emit(target_widget, Value)
                        else:
                            print(f"Warning: {item[1]} does not exist in self.ui")

                    elif type(Value) is str:
                        print("Value is a string")
                    else:
                        print("Unknown data type:", type(Value))
                    #print(Value)
                except pyads.ADSError as e:
                    print(f"Error reading {item[3]} on port {port}: {e}")

            time.sleep(0.5)  # 控制刷新频率

        plc.close()
        print(f"Closed TwinCAT connection on port {port}")

    def valveshow(self):
        global Valve_Pag_Refresh_running
        Valve_Pag_Refresh_running = True
        self.ui.stackedWidget.setCurrentIndex(5)
        self.TwinCAT_port_open('192.168.1.160.1.1', '27916')

        # 启动两个线程，每个线程处理不同的端口
        thread_27911 = Thread(target=self.threadFuncdevice, args=(valve_27911, 27911))
        thread_27916 = Thread(target=self.threadFuncdevice, args=(valve_27916, 27916))

        thread_27911.start()
        thread_27916.start()

    def stop_threads(self):
        # 停止线程
        self.threads_running = False  # 修改标志让线程退出
        # 关闭端口连接
        if self.plc_27911:
            self.plc_27911.close()  # 关闭 27911 端口
        if self.plc_27916:
            self.plc_27916.close()  # 关闭 27916 端口
        if self.plc_851:
            self.plc_851.close()  # 关闭 851 端口

        # 等待线程结束
        if self.thread_27911:
            self.thread_27911.join()
        if self.thread_27916:
            self.thread_27916.join()
        if self.thread_851:
            self.thread_851.join()
        print("Ports closed and threads stopped")

    def subvalveshow(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def aioshow(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def dioshow(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def handlestarttestbutton(self):
        #device_27916, valve_27911, valve_27916 = self.process_excel()  # 读取 Excel 文件 channeslnfo.xlsx,赋给3个元组
        self.TwinCAT_port_open('192.168.1.160.1.1', '27916')
        # 再启动两个线程，每个线程处理不同的端口
        thread_27911 = Thread(target=self.threadFunc, args=(valve_27911, 27911))
        thread_27916 = Thread(target=self.threadFunc, args=(valve_27916, 27916))

        thread_27911.start()
        thread_27916.start()

    def handlestoptestbutton(self):
        global Valve_Pag_Refresh_running
        Valve_Pag_Refresh_running = False  # 停止刷新
        self.stop_threads()

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
    def SetTPC2Control(self):
        Value = self.ui.TPC2_Control.text()
        self.write_value_byname('ECAT_SWITCH (CU1128).ALICAT_1000T_PC.SM_2.Setpoint_RxPDO_Map.Setpoint', Value, 'REAL')
    def toggle_TV1button(self):
        global TV1State
        global Manifold1_Group0
        TV1State = not TV1State
        if TV1State:
            Manifold1_Group0 = Manifold1_Group0 + 1
        else:
            Manifold1_Group0 = Manifold1_Group0 - 1
        self.write_value_byname('ECAT_SWITCH (CU1128).CDA Manifold 1 (EX260-SEC1).SM_0.Byte_0_Output', Manifold1_Group0, 'USINT')
        self.update_TVbutton(self.ui.TV1,TV1State)
    def toggle_TV2button(self):
        global TV2State
        global Manifold1_Group0
        TV2State = not TV2State
        if TV2State:
            Manifold1_Group0 = Manifold1_Group0 + 2
        else:
            Manifold1_Group0 = Manifold1_Group0 - 2
        self.write_value_byname('ECAT_SWITCH (CU1128).CDA Manifold 1 (EX260-SEC1).SM_0.Byte_0_Output', Manifold1_Group0, 'USINT')
        self.update_TVbutton(self.ui.TV2,TV2State)
    def toggle_TV3button(self):
        global TV3State
        global Manifold1_Group0
        TV3State = not TV3State
        if TV3State:
            Manifold1_Group0 = Manifold1_Group0 + 4
        else:
            Manifold1_Group0 = Manifold1_Group0 - 4
        self.write_value_byname('ECAT_SWITCH (CU1128).CDA Manifold 1 (EX260-SEC1).SM_0.Byte_0_Output', Manifold1_Group0, 'USINT')
        self.update_TVbutton(self.ui.TV3,TV3State)
    def toggle_TV4button(self):
        global TV4State
        global Manifold1_Group0
        TV4State = not TV4State
        if TV4State:
            Manifold1_Group0 = Manifold1_Group0 + 8
        else:
            Manifold1_Group0 = Manifold1_Group0 - 8
        self.write_value_byname('ECAT_SWITCH (CU1128).CDA Manifold 1 (EX260-SEC1).SM_0.Byte_0_Output', Manifold1_Group0, 'USINT')
        self.update_TVbutton(self.ui.TV4,TV4State)
    def toggle_TV5button(self):
        global TV5State
        global Manifold1_Group0
        TV5State = not TV5State
        if TV5State:
            Manifold1_Group0 = Manifold1_Group0 + 16
        else:
            Manifold1_Group0 = Manifold1_Group0 - 16
        self.write_value_byname('ECAT_SWITCH (CU1128).CDA Manifold 1 (EX260-SEC1).SM_0.Byte_0_Output', Manifold1_Group0,
                                'USINT')
        self.update_TVbutton(self.ui.TV5, TV5State)
    def toggle_TV6button(self):
        global TV6State
        global Manifold1_Group0
        TV6State = not TV6State
        if TV6State:
            Manifold1_Group0 = Manifold1_Group0 + 32
        else:
            Manifold1_Group0 = Manifold1_Group0 - 32
        self.write_value_byname('ECAT_SWITCH (CU1128).CDA Manifold 1 (EX260-SEC1).SM_0.Byte_0_Output', Manifold1_Group0,
                                'USINT')
        self.update_TVbutton(self.ui.TV6, TV6State)
    def toggle_TV7button(self):
        global TV7State
        global Manifold1_Group0
        TV7State = not TV7State
        if TV7State:
            Manifold1_Group0 = Manifold1_Group0 + 64
        else:
            Manifold1_Group0 = Manifold1_Group0 - 64
        self.write_value_byname('ECAT_SWITCH (CU1128).CDA Manifold 1 (EX260-SEC1).SM_0.Byte_0_Output', Manifold1_Group0,
                                'USINT')
        self.update_TVbutton(self.ui.TV7, TV7State)
    def toggle_TV8button(self):
        global TV8State
        global Manifold1_Group0
        TV8State = not TV8State
        if TV8State:
            Manifold1_Group0 = Manifold1_Group0 + 128
        else:
            Manifold1_Group0 = Manifold1_Group0 - 128
        self.write_value_byname('ECAT_SWITCH (CU1128).CDA Manifold 1 (EX260-SEC1).SM_0.Byte_0_Output', Manifold1_Group0,
                                'USINT')
        self.update_TVbutton(self.ui.TV8, TV8State)
    def toggle_TV9button(self):
        global TV9State
        global Manifold1_Group1
        TV9State = not TV9State
        if TV9State:
            Manifold1_Group1 = Manifold1_Group1 + 1
        else:
            Manifold1_Group1 = Manifold1_Group1 - 1
        self.write_value_byname('ECAT_SWITCH (CU1128).CDA Manifold 1 (EX260-SEC1).SM_1.Byte_1_Output', Manifold1_Group1, 'USINT')
        self.update_TVbutton(self.ui.TV9,TV9State)
    def toggle_TV10button(self):
        global TV10State
        global Manifold1_Group1
        TV10State = not TV10State
        if TV10State:
            Manifold1_Group1 = Manifold1_Group1 + 2
        else:
            Manifold1_Group1 = Manifold1_Group1 - 2
        self.write_value_byname('ECAT_SWITCH (CU1128).CDA Manifold 1 (EX260-SEC1).SM_1.Byte_1_Output', Manifold1_Group1, 'USINT')
        self.update_TVbutton(self.ui.TV10,TV10State)
    def toggle_TV11button(self):
        global TV11State
        global Manifold1_Group1
        TV11State = not TV11State
        if TV11State:
            Manifold1_Group1 = Manifold1_Group1 + 4
        else:
            Manifold1_Group1 = Manifold1_Group1 - 4
        self.write_value_byname('ECAT_SWITCH (CU1128).CDA Manifold 1 (EX260-SEC1).SM_1.Byte_1_Output', Manifold1_Group1, 'USINT')
        self.update_TVbutton(self.ui.TV11,TV11State)
    def toggle_TV12button(self):
        global TV12State
        global Manifold1_Group1
        TV12State = not TV12State
        if TV12State:
            Manifold1_Group1 = Manifold1_Group1 + 8
        else:
            Manifold1_Group1 = Manifold1_Group1 - 8
        self.write_value_byname('ECAT_SWITCH (CU1128).CDA Manifold 1 (EX260-SEC1).SM_1.Byte_1_Output', Manifold1_Group1, 'USINT')
        self.update_TVbutton(self.ui.TV12,TV12State)
    def toggle_TV13button(self):
        global TV13State
        global Manifold1_Group1
        TV13State = not TV13State
        if TV13State:
            Manifold1_Group1 = Manifold1_Group1 + 16
        else:
            Manifold1_Group1 = Manifold1_Group1 - 16
        self.write_value_byname('ECAT_SWITCH (CU1128).CDA Manifold 1 (EX260-SEC1).SM_1.Byte_1_Output', Manifold1_Group1,'USINT')
        self.update_TVbutton(self.ui.TV13, TV13State)
    def toggle_TV14button(self):
        global TV14State
        global Manifold1_Group1
        TV14State = not TV14State
        if TV14State:
            Manifold1_Group1 = Manifold1_Group1 + 32
        else:
            Manifold1_Group1 = Manifold1_Group1 - 32
        self.write_value_byname('ECAT_SWITCH (CU1128).CDA Manifold 1 (EX260-SEC1).SM_1.Byte_1_Output', Manifold1_Group1,'USINT')
        self.update_TVbutton(self.ui.TV14, TV14State)
    def toggle_TV15button(self):
        global TV15State
        global Manifold1_Group1
        TV15State = not TV15State
        if TV15State:
            Manifold1_Group1 = Manifold1_Group1 + 64
        else:
            Manifold1_Group1 = Manifold1_Group1 - 64
        self.write_value_byname('ECAT_SWITCH (CU1128).CDA Manifold 1 (EX260-SEC1).SM_1.Byte_1_Output', Manifold1_Group1,'USINT')
        self.update_TVbutton(self.ui.TV15, TV15State)
    def toggle_TV16button(self):
        global TV16State
        global Manifold1_Group1
        TV16State = not TV16State
        if TV16State:
            Manifold1_Group1 = Manifold1_Group1 + 128
        else:
            Manifold1_Group1 = Manifold1_Group1 - 128
        self.write_value_byname('ECAT_SWITCH (CU1128).CDA Manifold 1 (EX260-SEC1).SM_1.Byte_1_Output', Manifold1_Group1,'USINT')
        self.update_TVbutton(self.ui.TV16, TV16State)
    def toggle_TV17button(self):
        global TV17State
        global Manifold1_Group2
        TV17State = not TV17State
        if TV17State:
            Manifold1_Group2 = Manifold1_Group2 + 1
        else:
            Manifold1_Group2 = Manifold1_Group2 - 1
        self.write_value_byname('ECAT_SWITCH (CU1128).CDA Manifold 1 (EX260-SEC1).SM_2.Byte_2_Output', Manifold1_Group2, 'USINT')
        self.update_TVbutton(self.ui.TV17,TV17State)
    def toggle_TV18button(self):
        global TV18State
        global Manifold1_Group2
        TV18State = not TV18State
        if TV18State:
            Manifold1_Group2 = Manifold1_Group2 + 2
        else:
            Manifold1_Group2 = Manifold1_Group2 - 2
        self.write_value_byname('ECAT_SWITCH (CU1128).CDA Manifold 1 (EX260-SEC1).SM_2.Byte_2_Output', Manifold1_Group2, 'USINT')
        self.update_TVbutton(self.ui.TV18,TV18State)
    def toggle_TV19button(self):
        global TV19State
        global Manifold1_Group2
        TV19State = not TV19State
        if TV19State:
            Manifold1_Group2 = Manifold1_Group2 + 4
        else:
            Manifold1_Group2 = Manifold1_Group2 - 4
        self.write_value_byname('ECAT_SWITCH (CU1128).CDA Manifold 1 (EX260-SEC1).SM_2.Byte_2_Output', Manifold1_Group2, 'USINT')
        self.update_TVbutton_H(self.ui.TV19,TV19State)
    def toggle_TV20button(self):
        global TV20State
        global Manifold2_Group0
        TV20State = not TV20State
        if TV20State:
            Manifold2_Group0 = Manifold2_Group0 + 1
        else:
            Manifold2_Group0 = Manifold2_Group0 - 1
        self.write_value_byname('ECAT_SWITCH (CU1128).Box 71 (CU1128-B).CDA Manifold 2 (EX260-SEC1).SM_0.Byte_0_Output', Manifold2_Group0, 'USINT')
        self.update_TVbutton(self.ui.TV20,TV20State)
    def toggle_TV21button(self):
        global TV21State
        global Manifold2_Group0
        TV21State = not TV21State
        if TV21State:
            Manifold2_Group0 = Manifold2_Group0 + 2
        else:
            Manifold2_Group0 = Manifold2_Group0 - 2
        self.write_value_byname('ECAT_SWITCH (CU1128).Box 71 (CU1128-B).CDA Manifold 2 (EX260-SEC1).SM_0.Byte_0_Output', Manifold2_Group0,
                                'USINT')
        self.update_TVbutton(self.ui.TV21, TV21State)
    def toggle_TV22button(self):
        global TV22State
        global Manifold2_Group0
        TV22State = not TV22State
        if TV22State:
            Manifold2_Group0 = Manifold2_Group0 + 4
        else:
            Manifold2_Group0 = Manifold2_Group0 - 4
        self.write_value_byname('ECAT_SWITCH (CU1128).Box 71 (CU1128-B).CDA Manifold 2 (EX260-SEC1).SM_0.Byte_0_Output', Manifold2_Group0,
                                'USINT')
        self.update_TVbutton(self.ui.TV22, TV22State)
    def toggle_TV23button(self):
        global TV23State
        global Manifold2_Group0
        TV23State = not TV23State
        if TV23State:
            Manifold2_Group0 = Manifold2_Group0 + 8
        else:
            Manifold2_Group0 = Manifold2_Group0 - 8
        self.write_value_byname('ECAT_SWITCH (CU1128).Box 71 (CU1128-B).CDA Manifold 2 (EX260-SEC1).SM_0.Byte_0_Output', Manifold2_Group0,
                                'USINT')
        self.update_TVbutton(self.ui.TV23, TV23State)
    def toggle_TV24button(self):
        global TV24State
        global Manifold2_Group0
        TV24State = not TV24State
        if TV24State:
            Manifold2_Group0 = Manifold2_Group0 + 16
        else:
            Manifold2_Group0 = Manifold2_Group0 - 16
        self.write_value_byname('ECAT_SWITCH (CU1128).Box 71 (CU1128-B).CDA Manifold 2 (EX260-SEC1).SM_0.Byte_0_Output', Manifold2_Group0,
                                'USINT')
        self.update_TVbutton(self.ui.TV24, TV24State)
    def toggle_TV25button(self):
        global TV25State
        global Manifold2_Group0
        TV25State = not TV25State
        if TV25State:
            Manifold2_Group0 = Manifold2_Group0 + 32
        else:
            Manifold2_Group0 = Manifold2_Group0 - 32
        self.write_value_byname('ECAT_SWITCH (CU1128).Box 71 (CU1128-B).CDA Manifold 2 (EX260-SEC1).SM_0.Byte_0_Output', Manifold2_Group0, 'USINT')
        self.update_TVbutton(self.ui.TV25,TV25State)
    def toggle_TV26button(self):
        global TV26State
        global Manifold2_Group0
        TV26State = not TV26State
        if TV26State:
            Manifold2_Group0 = Manifold2_Group0 + 64
        else:
            Manifold2_Group0 = Manifold2_Group0 - 64
        self.write_value_byname('ECAT_SWITCH (CU1128).Box 71 (CU1128-B).CDA Manifold 2 (EX260-SEC1).SM_0.Byte_0_Output', Manifold2_Group0, 'USINT')
        self.update_TVbutton(self.ui.TV26,TV26State)
    def toggle_TV27button(self):
        global TV27State
        global Manifold2_Group0
        TV27State = not TV27State
        if TV27State:
            Manifold2_Group0 = Manifold2_Group2 + 128
        else:
            Manifold2_Group0 = Manifold2_Group0 - 128
        self.write_value_byname('ECAT_SWITCH (CU1128).Box 71 (CU1128-B).CDA Manifold 2 (EX260-SEC1).SM_0.Byte_0_Output', Manifold2_Group0, 'USINT')
        self.update_TVbutton(self.ui.TV27,TV27State)
    def toggle_TV28button(self):
        global TV28State
        global Manifold2_Group1
        TV28State = not TV28State
        if TV28State:
            Manifold2_Group1 = Manifold2_Group1 + 1
        else:
            Manifold2_Group1 = Manifold2_Group1 - 1
        self.write_value_byname('ECAT_SWITCH (CU1128).Box 71 (CU1128-B).CDA Manifold 2 (EX260-SEC1).SM_1.Byte_1_Output', Manifold2_Group1, 'USINT')
        self.update_TVbutton(self.ui.TV28,TV28State)
    def toggle_TV29button(self):
        global TV29State
        global Manifold2_Group1
        TV29State = not TV29State
        if TV29State:
            Manifold2_Group1 = Manifold2_Group1 + 2
        else:
            Manifold2_Group1 = Manifold2_Group1 - 2
        self.write_value_byname('ECAT_SWITCH (CU1128).Box 71 (CU1128-B).CDA Manifold 2 (EX260-SEC1).SM_1.Byte_1_Output', Manifold2_Group1,'USINT')
        self.update_TVbutton(self.ui.TV29, TV29State)
    def toggle_TV30button(self):
        global TV30State
        global Manifold2_Group1
        TV30State = not TV30State
        if TV30State:
            Manifold2_Group1 = Manifold2_Group1 + 4
        else:
            Manifold2_Group1 = Manifold2_Group1 - 4
        self.write_value_byname('ECAT_SWITCH (CU1128).Box 71 (CU1128-B).CDA Manifold 2 (EX260-SEC1).SM_1.Byte_1_Output', Manifold2_Group1,'USINT')
        self.update_TVbutton(self.ui.TV30, TV30State)
    def toggle_TV31button(self):
        global TV31State
        global Manifold2_Group1
        TV31State = not TV31State
        if TV31State:
            Manifold2_Group1 = Manifold2_Group1 + 8
        else:
            Manifold2_Group1 = Manifold2_Group1 - 8
        self.write_value_byname('ECAT_SWITCH (CU1128).Box 71 (CU1128-B).CDA Manifold 2 (EX260-SEC1).SM_1.Byte_1_Output', Manifold2_Group1,'USINT')
        self.update_TVbutton(self.ui.TV31, TV31State)
    def toggle_UUT_CDAbutton(self):
        global UUT_CDAState
        global Manifold2_Group1
        UUT_CDAState = not UUT_CDAState
        if UUT_CDAState:
            Manifold2_Group1 = Manifold2_Group1 + 16
        else:
            Manifold2_Group1 = Manifold2_Group1 - 16
        self.write_value_byname('ECAT_SWITCH (CU1128).Box 71 (CU1128-B).CDA Manifold 2 (EX260-SEC1).SM_1.Byte_1_Output', Manifold2_Group1,'USINT')
        self.update_TVbutton(self.ui.UUT_CDA, UUT_CDAState)
    def toggle_SPACE_CDAbutton(self):
        global SPACE_CDAState
        global Manifold2_Group1
        SPACE_CDAState = not SPACE_CDAState
        if SPACE_CDAState:
            Manifold2_Group1 = Manifold2_Group1 + 32
        else:
            Manifold2_Group1 = Manifold2_Group1 - 32
        self.write_value_byname('ECAT_SWITCH (CU1128).Box 71 (CU1128-B).CDA Manifold 2 (EX260-SEC1).SM_1.Byte_1_Output', Manifold2_Group1,'USINT')
        self.update_TVbutton(self.ui.SPACE_CDA, SPACE_CDAState)
    def update_TVbutton(self,button, state):
        if state:
            button.setIcon(QIcon("image\ValveOn.png"))
        else:
            button.setIcon(QIcon("image\ValveOff.png"))
    def update_TVbutton_H(self, button, state):
        if state:
            button.setIcon(QIcon("image\ValveOn_H.png"))
        else:
            button.setIcon(QIcon("image\ValveOff_H.png"))

app = QApplication([])
app.setWindowIcon(QIcon('image\JR Logo.jpg'))
DGTFI = Basics()
device_27916, valve_27911, valve_27916 = DGTFI.process_excel()  # 读取 Excel 文件 channeslnfo.xlsx,赋给3个元组
DGTFI.ui.show()
app.exec()