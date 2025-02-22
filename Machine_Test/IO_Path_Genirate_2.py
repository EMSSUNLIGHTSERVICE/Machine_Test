import pandas as pd  # 使用 pandas 读取 Excel 文件，然后提取每一行的指定列，最后将这些列组合成一个列表。

# Excel文件的路径
file_path = r'D:\JinRay\Copy From UCT Aegis Machine\Public Document\Gas Lab Manager\System.Lam.VDS\default\Hardware\channels.xlsx'

# 读取Excel文件
df = pd.read_excel(file_path)

# 去除列名中的空格
df.columns = df.columns.str.strip()

# 提取所需的列并将每一行转换为一个小列表，最后组成一个大列表
IO_Path = df[['device_name', 'twincat_datatype', 'io_path']].values.tolist()

# 打印结果
#print(IO_Path)
for path in IO_Path:
    print(path)