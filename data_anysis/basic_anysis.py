import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 假设已经从CSV文件中加载了数据
file_path = r'D:\Program Files\Big_nmber\big_num\data\performance_results_extended_better.csv'
performance_data = pd.read_csv(file_path)

# Grouping data by 'Bit Width' and 'Algorithm', then calculating the mean for each group
grouped_data = performance_data.groupby(['Bit Width', 'Algorithm']).mean().reset_index()

# Display the grouped data for user comparison
print(grouped_data)

# Function to plot performance metrics
def plot_performance_metric(metric, ylabel, title):
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Bit Width', y=metric, hue='Algorithm', data=grouped_data, palette="viridis")
    plt.xlabel('Bit Width')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend(title='Algorithm')
    plt.grid(True)
    plt.show()

# Plotting the average execution time
plot_performance_metric('Execution Time', 'Execution Time (s)', 'Average Execution Time by Bit Width and Algorithm')

# Plotting the average CPU usage
plot_performance_metric('CPU Usage', 'CPU Usage (%)', 'Average CPU Usage by Bit Width and Algorithm')

# Plotting the average memory usage
plot_performance_metric('Memory Usage', 'Memory Usage (MB)', 'Average Memory Usage by Bit Width and Algorithm')
