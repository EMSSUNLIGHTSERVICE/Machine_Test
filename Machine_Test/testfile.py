# -*- coding:utf-8 -*-
# @Discription:测试twincat3和pythonADS通讯，包含各种数据类型通讯测试
# @Editor:zy.shi
# @version:2020-6-27
# @:

# 导入ADS包
import pyads

# 通讯地址，端口
plc = pyads.Connection('169.254.77.92.1.1', 851)
# 打开端口
plc.open()

# pyads自带的数据类型，包含bool型，长短整形，浮点型，字符串型，DT日期变量，整形数组浮点型数组
# 先进行值写入，再进行值读取，并且把读取结果打印在终端
# bool型
plc.write_by_name('MAIN.test_bool', True, pyads.PLCTYPE_BOOL)
test_bool = plc.read_by_name('MAIN.test_bool', pyads.PLCTYPE_BOOL)
print(test_bool)

# int，整型
plc.write_by_name('MAIN.test_int',100 , pyads.PLCTYPE_INT)
test_int = plc.read_by_name('MAIN.test_int', pyads.PLCTYPE_INT)
print(test_int)

# real，浮点型
plc.write_by_name('MAIN.test_real', 5.5, pyads.PLCTYPE_REAL)
test_real = plc.read_by_name('MAIN.test_real', pyads.PLCTYPE_REAL)
print(test_real)

# string，字符串
plc.write_by_name('MAIN.test_string', 'string', pyads.PLCTYPE_STRING)
test_string = plc.read_by_name('MAIN.test_string', pyads.PLCTYPE_STRING)
print(test_string)

# int型数组，长度10
plc.write_by_name('MAIN.test_ARR_INT', [1, 2, 3, 4, 5, 6, 7, 8, 9, 0], pyads.PLCTYPE_ARR_INT(10))
test_ARR_INT = plc.read_by_name('MAIN.test_ARR_INT', pyads.PLCTYPE_ARR_INT(10))
print(test_ARR_INT)

# word型变量
plc.write_by_name('MAIN.test_word', 250, pyads.PLCTYPE_WORD)
test_word = plc.read_by_name('MAIN.test_word', pyads.PLCTYPE_WORD)

# 非自带数据类型，如结构体，其他数组等
# pyads包中没有对应的数据类型，可以使用循环语句来进行单个元素的读取和写入
# 非自带数组类型，如bool型数组等
plc.write_by_name('MAIN.test_arr_bool', [True, False, True], pyads.PLCTYPE_BOOL * 3)
test_arr_bool = plc.read_by_name('MAIN.test_arr_bool', pyads.PLCTYPE_BOOL * 3)
print(test_arr_bool)

# 自定义结构体
structure_type = ['BOOL', 'INT', 'STRING', 'REAL']
structure_value = ['True', '100', '\'this is a string\'', '100.5']
structure_struct = ['a', 'b', 'c', 'd']
structure_value2 = [False, 0, '', 0.0]
for i in range(4):
    str = 'plc.write_by_name(\'MAIN.test_structure.{}\', {}, pyads.PLCTYPE_{})'.\
        format(structure_struct[i], structure_value[i], structure_type[i])
    eval(str)
    str2 = 'plc.read_by_name(\'MAIN.test_structure.{}\', pyads.PLCTYPE_{})'.format(structure_struct[i], structure_type[i])
    structure_value2[i] = eval(str2)
print(structure_value2)

# 也可以使用专有的读取指令 read_structure_by_name进行读取，使用这条指令读取，PLC中申明的结构体需要加上{attribute 'pack_mode' := '1'}
# 在python中线定义结构类型
structure_def=(('a', pyads.PLCTYPE_BOOL, 1),
               ('b', pyads.PLCTYPE_INT, 1),
               ('c', pyads.PLCTYPE_STRING, 1),
               ('d', pyads.PLCTYPE_REAL, 1))
structure_value3 = plc.read_structure_by_name('MAIN.test_structure', structure_def, 1, pyads.ads.size_of_structure(structure_def))
print(structure_value3)

# 非自带数据类型，string数组，对于string类型，pyads.PLCTYPE_STRING*3 这种方式是不能使用的，需要额外用循环
arr_string = ['\'string1\'', '\'string2\'', '\'string3\'']
arr_index = ['1', '2', '3']
arr_string2 = ['', '', '']
for i in range(3):
    # plc.write_by_name('MAIN.test_arr_string[1]', 'string1', pyads.PLCTYPE_STRING)
    str = 'plc.write_by_name(\'MAIN.test_arr_string[{}]\', {}, pyads.PLCTYPE_STRING)'.format(arr_index[i], arr_string[i])
    eval(str)
    str2 = 'plc.read_by_name(\'MAIN.test_arr_string[{}]\', pyads.PLCTYPE_STRING)'.format(arr_index[i])
    arr_string2[i] = eval(str2)
print(arr_string2)

# 关闭端口
plc.close()

