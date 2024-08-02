import pandas as pd
from scipy.stats import ttest_ind

# 定义文件路径
file_path = r'D:\Program Files\Big_nmber\big_num\data\performance_results_extended.csv'

# 加载数据
performance_data = pd.read_csv(file_path)

# 检查数据是否有缺失值
missing_values = performance_data.isnull().sum()
print("缺失值检查：")
print(missing_values)

# 处理缺失值（删除缺失值）
performance_data = performance_data.dropna()

# 计算分组统计量（平均值和标准差）
grouped_data = performance_data.groupby(['Bit Width', 'Algorithm']).agg(
    Execution_Time_Mean=('Execution Time', 'mean'),
    Execution_Time_Std=('Execution Time', 'std'),
    CPU_Usage_Mean=('CPU Usage', 'mean'),
    CPU_Usage_Std=('CPU Usage', 'std'),
    Memory_Usage_Mean=('Memory Usage', 'mean'),
    Memory_Usage_Std=('Memory Usage', 'std')
).reset_index()

# 逐位宽进行t检验，比较两种算法的执行时间是否有显著差异
results = []
bit_widths = performance_data['Bit Width'].unique()
for bit_width in bit_widths:
    subset = performance_data[performance_data['Bit Width'] == bit_width]
    barrett_times = subset[subset['Algorithm'] == 'Barrett']['Execution Time']
    montgomery_times = subset[subset['Algorithm'] == 'Montgomery']['Execution Time']
    t_stat, p_value = ttest_ind(barrett_times, montgomery_times)
    results.append({'Bit Width': bit_width, 't-statistic': t_stat, 'p-value': p_value})

# 创建结果的DataFrame
results_df = pd.DataFrame(results)

# 将结果保存到CSV文件
results_df.to_csv(r'D:\Program Files\Big_nmber\big_num\output_data\t_test_results.csv', index=False)

print("t检验结果已保存到t_test_results.csv")

# 打印t检验结果
print(results_df)
