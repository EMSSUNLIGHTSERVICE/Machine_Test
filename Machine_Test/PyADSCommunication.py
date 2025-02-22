# -*- coding:utf-8 -*-
# @Discription:python ADS通讯，图形化界面，读取单个变量，使用变量名或者是变量地址访问单个数据
# @Editor:zy.Shi
# @version:2020-6-26
# @:

# 添加包，ADS通讯包，图形化界面包，时间包

import pyads
import tkinter
import time

# 日志默认条数
LOG_LINE_NUM = 0

class GUI():
    # Gui部分
    def __init__(self, init_windows_name):
        self.init_windows_name = init_windows_name

    # 设置窗口
    def set_init_window(self):
        # 窗口名称
        self.init_windows_name.title('ADS 通讯 by zy.shi')
        # 窗口大小+窗口弹出位置
        self.init_windows_name.geometry('625x300+30+30')
        # 虚化程度
        self.init_windows_name.attributes('-alpha', 0.95)

        # 标签部分 Label，定义Label，然后定义Label的属性，显示文本，显示位置
        # 副标题 通讯参数配置
        self.ads_communication_title = tkinter.Label(self.init_windows_name, text='通讯参数配置')
        self.ads_communication_title.grid(row=0, column=0)
        # 副标题 通讯日志
        self.ads_communication_log = tkinter.Label(self.init_windows_name, text='通讯日志')
        self.ads_communication_log.grid(row=0, column=12)
        # 通讯参数，AmsNetID
        self.ads_communication_netID = tkinter.Label(self.init_windows_name, text='AmsNetID')
        self.ads_communication_netID.grid(row=1, column=0)
        # 通讯参数，Port
        self.ads_communication_port = tkinter.Label(self.init_windows_name, text='Port')
        self.ads_communication_port.grid(row=2, column=0)
        # 通讯参数，变量名
        self.ads_communication_Vname = tkinter.Label(self.init_windows_name, text='变量名')
        self.ads_communication_Vname.grid(row=3, column=0)
        # 通讯参数，变量值
        self.ads_communication_Value = tkinter.Label(self.init_windows_name, text='变量值')
        self.ads_communication_Value.grid(row=4, column=0)
        # 通讯参数，数据类型
        self.ads_communication_data_type = tkinter.Label(self.init_windows_name, text='数据类型')
        self.ads_communication_data_type.grid(row=5, column=0)
        # 通讯参数，indexgroup
        self.ads_communication_group = tkinter.Label(self.init_windows_name, text='group')
        self.ads_communication_group.grid(row=6, column=0)
        # 通讯参数，数据类型
        self.ads_communication_offset = tkinter.Label(self.init_windows_name, text='offset')
        self.ads_communication_offset.grid(row=7, column=0)

        # 文本框部分 Text
        # 通讯日志窗口
        self.log_text = tkinter.Text(self.init_windows_name, width = 45, height = 20)
        self.log_text.grid(row = 1, column = 12, rowspan = 10)
        # 通讯参数窗口 netID
        self.netID_text = tkinter.Text(self.init_windows_name, width = 20, height = 1)
        self.netID_text.grid(row = 1, column = 1)
        # 通讯参数窗口 port
        self.port_text = tkinter.Text(self.init_windows_name, width = 20, height = 1)
        self.port_text.grid(row = 2 , column = 1)
        # 通讯参数窗口 变量名
        self.Vname_text = tkinter.Text(self.init_windows_name, width = 20, height = 1)
        self.Vname_text.grid(row = 3, column = 1)
        # 通讯参数窗口 变量值
        self.Value_text = tkinter.Text(self.init_windows_name, width = 20, height = 1)
        self.Value_text.grid(row = 4, column = 1)
        # 通讯参数窗口 数据类型
        self.data_type_text = tkinter.Text(self.init_windows_name, width = 20, height = 1)
        self.data_type_text.grid(row = 5, column = 1)
        # 通讯参数窗口 indexgroup
        self.indexgroup_text = tkinter.Text(self.init_windows_name, width=20, height=1)
        self.indexgroup_text.grid(row=6, column=1)
        # 通讯参数窗口 indexoffset
        self.indexoffset_text = tkinter.Text(self.init_windows_name, width=20, height=1)
        self.indexoffset_text.grid(row=7, column=1)

        # 按钮部分 button
        # 清空参数
        self.delete_all_button = tkinter.Button(self.init_windows_name, text = '清空参数', bg = 'lightblue', width = 10,
                                                command = self.delete_all_parameter)
        self.delete_all_button.grid(row = 0, column = 1)
        # 清空日志
        self.delete_log_button = tkinter.Button(self.init_windows_name, text = '清空日志', bg = 'lightblue', width = 10,
                                                command = self.delete_log)
        self.delete_log_button.grid(row = 0, column = 2 )
        # 打开端口
        self.open_port_button = tkinter.Button(self.init_windows_name, text = '打开端口', width = 10,
                                               command = self.Plc_port_open)
        self.open_port_button.grid(row = 1, column = 2)
        # 写入变量
        self.write_value_button = tkinter.Button(self.init_windows_name, text = '写入变量', width = 10,
                                                 command = self.write_value_byname)
        self.write_value_button.grid(row = 2, column = 2)
        # 读取变量
        self.read_value_button = tkinter.Button(self.init_windows_name, text = '读取变量', width = 10,
                                                command = self.read_value_byname)
        self.read_value_button.grid(row = 3, column = 2)
        # 写入变量
        self.write_value_by_address_button = tkinter.Button(self.init_windows_name, text='写入变量-地址', width=10,
                                                command=self.write_value_by_address)
        self.write_value_by_address_button.grid(row=4, column=2)
        # 读取变量
        self.read_value_by_address_button = tkinter.Button(self.init_windows_name, text='读取变量-地址', width=10,
                                                            command=self.read_value_by_address)
        self.read_value_by_address_button.grid(row=5, column=2)
        # 打印一条样例日志 测试时候用作日志打印
        self.write_log_button = tkinter.Button(self.init_windows_name, text = '打印样例日志', width = 10,
                                                command = self.write_log)
        self.write_log_button.grid(row= 6 , column = 2)

    # 功能函数部分，包括主逻辑，ADS通讯等，系统辅助程序，日志记录等
    # ADS相关函数
    # 打开端口
    def Plc_port_open(self):
        global Plc
        # 获取netID以及port，测试时候用本机地址 '127.0.0.1.1.1'# '851'#
        AmsNetID = self.netID_text.get(1.0, tkinter.END)
        port = self.port_text.get(1.0, tkinter.END)
        try:
            # 打开PLC端口
            Plc = pyads.Connection(AmsNetID, eval(port))
            Plc.open()
            # 连接成功，输出日志
            self.write_log_to_text('地址{}，端口{}，请输入变量信息'.format(AmsNetID, port).replace('\n', ''))
        except:
            # 连接失败，输出日志
            self.write_log_to_text('地址{}，端口{}，端口连接失败'.format(AmsNetID, port).replace('\n', '')
                                   + '\nADS服务未开启或地址端口不合法')
        # 在终端打印netID和端口，测试用
        print(AmsNetID, port)

    # 写入变量值
    def write_value_byname(self):
        global Plc
        # 获取变量值，变量类型，变量名
        Vname = self.Vname_text.get(1.0, 2.0)
        Value = self.Value_text.get(1.0, 2.0)
        data_type = self.data_type_text.get(1.0, 2.0)
        try:
            # 测试语句 Plc.write_by_name('MAIN.button[0]', True, pyads.PLCTYPE_BOOL)
            # replace函数取消换行，format函数填入变量名，值，数据类型，先formate再replace，不然Vname等变量末尾换行符去不掉
            str = 'Plc.write_by_name(\'{}\', {}, pyads.PLCTYPE_{})'.format(Vname, Value, data_type).replace('\n', '')
            # 打印写入语句到终端，以供检查
            print(str)
            # 执行写入语句
            eval(str)
            # 打印写入成功日志
            self.write_log_to_text('{}型变量{}写入成功'.format(data_type, Vname).replace('\n', ''))
        except:
            # 打印写入失败日志
            self.write_log_to_text('写入失败，找不到变量，请检查参数设置')

    # 读取变量值
    def read_value_byname(self):
        global Plc
        # 获取变量名，变量类型
        Vname = self.Vname_text.get(1.0, 2.0)
        data_type = self.data_type_text.get(1.0, 2.0)
        Value = self.Value_text.get(1.0, 2.0)
        try:
            # 测试语句Value = Plc.read_by_name('MAIN.A', pyads.PLCTYPE_BOOL)
            # replace函数取消换行，format函数填入变量名，变量类型
            str = 'Plc.read_by_name(\'{}\', pyads.PLCTYPE_{})'.format(Vname, data_type).replace('\n', '')
            # 打印读取语句到终端，以供检查
            print(str)
            # 执行读取语句
            Value = eval(str)
            # 打印读取成功日志
            self.write_log_to_text('{}型变量{}读取成功'.format(data_type, Vname).replace('\n', ''))
            # 清除Value显示栏当前值
            self.Value_text.delete(1.0, tkinter.END)
            # 讲读取出来的值显示
            self.Value_text.insert(tkinter.END, Value)
        except:
            # 打印读取失败日志
            self.write_log_to_text('读取失败，找不到变量，请检查参数设置')

    # 写入变量值-地址
    def write_value_by_address(self):
        global Plc
        # 获取地址和数据类型
        indexgroup = self.indexgroup_text.get(1.0, 2.0)
        indexoffset = self.indexoffset_text.get(1.0, 2.0)
        value = self.Value_text.get(1.0, 2.0)
        data_type = self.data_type_text.get(1.0, 2.0)
        try:
            # 测试语句，indexgroup和offset需要16进制表示
            # Plc.write(0x4040, 0x5DCB6, 0, pyads.PLCTYPE_BOOL)
            # replace函数取消换行，format函数填入变量名，值，数据类型
            str = 'Plc.write(0x{}, 0x{}, {}, pyads.PLCTYPE_{})'.format(indexgroup, indexoffset, value, data_type)\
                .replace('\n', '')
            # 输出写入语句以供检查
            print(str)
            # 执行写值语句
            eval(str)
            # 打印写值成功日志
            self.write_log_to_text('指定地址变量写值成功')
        except:
            # 出现错误
            self.write_log_to_text('写入失败，请检查参数设置')

    # 读取变量值-地址
    def read_value_by_address(self):
        global Plc
        indexgroup = self.indexgroup_text.get(1.0, 2.0)
        indexoffset = self.indexoffset_text.get(1.0, 2.0)
        value = self.Value_text.get(1.0, 2.0)
        data_type = self.data_type_text.get(1.0, 2.0)
        try:
            # Plc.read(0x4040, 0x5DCB6, pyads.PLCTYPE_BOOL)
            # replace函数取消换行，format函数填入变量名，值，数据类型
            str = 'Plc.read(0x{}, 0x{}, pyads.PLCTYPE_{})'.format(indexgroup, indexoffset, data_type).replace('\n', '')
            # 输出读取语句以供检查
            print(str)
            # 读取变量值
            value = eval(str)
            # 清除Value显示栏当前值
            self.Value_text.delete(1.0, tkinter.END)
            # 讲读取出来的值显示
            self.Value_text.insert(tkinter.END, value)
            # 打印读取成功日志
            self.write_log_to_text('指定地址变量读取成功')
        except:
            self.write_log_to_text('读取失败，请检查参数设置')

    # 系统相关函数
    # 删除所有参数
    def delete_all_parameter(self):
        try:
            # 所有参数窗口从第一行到最后一行删除数据
            self.netID_text.delete(1.0, tkinter.END)
            self.port_text.delete(1.0, tkinter.END)
            self.data_type_text.delete(1.0, tkinter.END)
            self.Value_text.delete(1.0, tkinter.END)
            self.Vname_text.delete(1.0, tkinter.END)
            self.indexgroup_text.delete(1.0, tkinter.END)
            self.indexoffset_text.delete(1.0, tkinter.END)
            self.write_log_to_text('清空所有参数')
        except:
            self.write_log_to_text('错误')

    # 读取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time

    # 日志打印，需要获取系统时间
    def write_log_to_text(self, logmsg):
        global LOG_LINE_NUM
        # 每次调用记录信息发生的时间
        current_time = self.get_current_time()
        # 日志信息 + 换行
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"
        # 界面上显示的信息数量
        if LOG_LINE_NUM <= 10:
            # 在末尾打印一条日志
            self.log_text.insert(tkinter.END, logmsg_in)
            # 信息条数+1
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            # 删除第一行的内容
            self.log_text.delete(1.0, 2.0)
            # 打印一条新的信息
            self.log_text.insert(tkinter.END, logmsg_in)
        # 移动光标
        self.log_text.focus_force()

    # 删除当前日志栏里的所有日志
    def delete_log(self):
        global LOG_LINE_NUM
        # 删除日志
        self.log_text.delete(1.0, tkinter.END)
        # 条数记录归零
        LOG_LINE_NUM = 0

    # 写一条日志（测试程序）
    def write_log(self):
        self.write_log_to_text('一条测试日志')

# 主程序
def Gui_Start():
    # 实例化窗口
    init_window = tkinter.Tk()
    MAIN_Window = GUI(init_window)
    # 设置窗口属性
    MAIN_Window.set_init_window()
    # 主循环
    init_window.mainloop()

Gui_Start()