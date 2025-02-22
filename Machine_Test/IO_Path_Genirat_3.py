import pandas as pd

# Excel文件的路径
file_path = r'D:\JinRay\Copy From UCT Aegis Machine\Public Document\Gas Lab Manager\System.Lam.VDS\default\Hardware\channels.xlsx'

# 读取Excel文件
df = pd.read_excel(file_path)

# 去除列名中的空格
df.columns = df.columns.str.strip()

# 提取所需的列并将每一行转换为一个小列表
data = df[['device_name', 'twincat_datatype', 'io_path']].values.tolist() # 这一行（一步）似乎可以不要

# 创建两个空列表来分别存储 'tfx' 和 'uut' 的数据
A27911_IO_Path = []
A27916_IO_Path = []

# 根据'//#group_name'列的值将数据分配到相应的列表中
"""
使用 iterrows() 遍历每一行，并检查 //#group_name 列的值。
根据该值将每行的 device_name、twincat_datatype 和 io_path 加入到不同的列表中。
如果 //#group_name 为 "tfx"，数据会添加到 A27911_IO_Path 列表，如果为 "uut"，则添加到 A27916_IO_Path 列表。
"""
for i, row in df.iterrows():
    group_name = row['//#group_name'].strip()  # 去除多余的空格
    row_data = [row['device_name'], row['twincat_datatype'], row['io_path']]

    if group_name == 'tfx':
        A27911_IO_Path.append(row_data)
    elif group_name == 'uut':
        A27916_IO_Path.append(row_data)

# 打印结果
print("27911_IO_Path:")
print(A27911_IO_Path)

print("\n27916_IO_Path:")
print(A27916_IO_Path)

"""
请用Python编写一段程序：将一个Excel文件（文件位置和文件是：
D:\JinRay\Copy From UCT Aegis Machine\Public Document\Gas Lab Manager\System.Lam.VDS\default\Hardware\channels）
中每一行的“device_name”列，“twincat_datatype"列和”io_path"列，为一个小列表，然后全部的行再做成两个大列表，其中“//#group_name”
列里是“tfx"的组成一个列表，名字是A27911_IO_Path，“//#group_name”列里是“uut"的组成第二个列表，名字是A27916_IO_Path.
"""
