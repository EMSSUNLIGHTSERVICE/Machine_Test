import pandas as pd

# Excel文件的路径
file_path = r'D:\JinRay\Copy From UCT Aegis Machine\Public Document\Gas Lab Manager\System.Lam.VDS\default\Hardware\channels.xlsx'

# 读取Excel文件
df = pd.read_excel(file_path)

# 提取'O'列的数据并转换为列表
IO_Path = df['io_path'].tolist()

# 打印结果
# print(IO_Path)
for path in IO_Path:
    print(path)