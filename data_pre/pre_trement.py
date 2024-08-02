import pandas as pd

# 读取CSV文件
file_path = r'D:\Program Files\Big_nmber\big_num\data\performance_results_extended.csv'
df = pd.read_csv(file_path)

# 转换Execution Time单位，从秒到毫秒
df['Execution Time'] = df['Execution Time'] * 1000  # s 转换为 ms

# 更新表头
df.columns = ["Bit Width (bits)", "Algorithm", "Execution Time (ms)", "CPU Usage (%)", "Memory Usage (MiB)"]

# 保存预处理后的数据到新的CSV文件
output_file_path = r'D:\Program Files\Big_nmber\big_num\output_data\performance_results_processed.csv'
df.to_csv(output_file_path, index=False)

# 显示预处理后的数据
print(df.head())
