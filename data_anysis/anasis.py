import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def pre_data():

    # 加载数据
    file_path = r'D:\Program Files\Big_nmber\big_num\data\performance_results_extended.csv'
    performance_data = pd.read_csv(file_path)
    # 检查数据是否有缺失值
    print(performance_data.isnull().sum())
    # 处理缺失值和异常值（如有需要）
    performance_data = performance_data.dropna()
    # 将执行时间转换为毫秒
    performance_data['Execution Time'] = performance_data['Execution Time'] * 1000  # 转换为毫秒
    # 计算分组统计量（平均值和标准差）
    grouped_data = performance_data.groupby(['Bit Width', 'Algorithm']).agg(
        Execution_Time_Mean=('Execution Time', 'mean'),
        Execution_Time_Std=('Execution Time', 'std'),
        CPU_Usage_Mean=('CPU Usage', 'mean'),
        CPU_Usage_Std=('CPU Usage', 'std'),
        Memory_Usage_Mean=('Memory Usage', 'mean'),
        Memory_Usage_Std=('Memory Usage', 'std')
    ).reset_index()
    return  grouped_data


grouped_data=pre_data()

# 设置图表风格
sns.set(style="whitegrid")

# 绘制执行时间折线图
plt.figure(figsize=(12, 6))
sns.lineplot(x='Bit Width', y='Execution_Time_Mean', hue='Algorithm', data=grouped_data, marker='o', palette="viridis", errorbar=None)
plt.errorbar(grouped_data['Bit Width'], grouped_data['Execution_Time_Mean'], yerr=grouped_data['Execution_Time_Std'], fmt='o', capsize=5)
plt.xlabel('Bit Width')
plt.ylabel('Execution Time (ms)')
plt.title('Average Execution Time by Bit Width and Algorithm (in ms)')
plt.legend(title='Algorithm')
plt.grid(True)
# 保存图表
plt.savefig(r'D:\Program Files\Big_nmber\big_num\data\execution_time_plot_ms.png')
plt.show()

# 绘制CPU使用率折线图
plt.figure(figsize=(12, 6))
sns.lineplot(x='Bit Width', y='CPU_Usage_Mean', hue='Algorithm', data=grouped_data, marker='o', palette="viridis", errorbar=None)
plt.errorbar(grouped_data['Bit Width'], grouped_data['CPU_Usage_Mean'], yerr=grouped_data['CPU_Usage_Std'], fmt='o', capsize=5)
plt.xlabel('Bit Width')
plt.ylabel('CPU Usage (%)')
plt.title('Average CPU Usage by Bit Width and Algorithm')
plt.legend(title='Algorithm')
plt.grid(True)
# 保存图表
plt.savefig(r'D:\Program Files\Big_nmber\big_num\data\cpu_usage_plot.png')
plt.show()

