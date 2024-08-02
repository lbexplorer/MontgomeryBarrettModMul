import pandas as pd
import numpy as np

# 加载数据
file_path = r'D:\Program Files\Big_nmber\big_num\data\performance_results_extended.csv'
performance_data = pd.read_csv(file_path)

# 检查数据是否有缺失值
print(performance_data.isnull().sum())

# 处理缺失值和异常值（如有需要）
performance_data = performance_data.dropna()

# 计算分组统计量（平均值、标准差和变异系数）
grouped_data = performance_data.groupby(['Bit Width', 'Algorithm']).agg(
    Execution_Time_Mean=('Execution Time', 'mean'),
    Execution_Time_Std=('Execution Time', 'std'),
    Execution_Time_CV=('Execution Time', lambda x: np.std(x) / np.mean(x)),
    CPU_Usage_Mean=('CPU Usage', 'mean'),
    CPU_Usage_Std=('CPU Usage', 'std'),
    CPU_Usage_CV=('CPU Usage', lambda x: np.std(x) / np.mean(x)),
    Memory_Usage_Mean=('Memory Usage', 'mean'),
    Memory_Usage_Std=('Memory Usage', 'std'),
    Memory_Usage_CV=('Memory Usage', lambda x: np.std(x) / np.mean(x))
).reset_index()

# 保存分组统计量到CSV文件
output_file_path = r'D:\Program Files\Big_nmber\big_num\output_data\grouped_performance_data.csv'
grouped_data.to_csv(output_file_path, index=False)

# 打印结果以供检查
print(grouped_data)
