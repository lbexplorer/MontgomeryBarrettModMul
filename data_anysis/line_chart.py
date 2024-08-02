# Function to plot performance metrics with line plots
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd

from data_anysis.basic_anysis import grouped_data


def plot_performance_metric_line(metric, ylabel, title):
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='Bit Width', y=metric, hue='Algorithm', data=grouped_data, marker='o', palette="viridis")
    plt.xlabel('Bit Width')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend(title='Algorithm')
    plt.grid(True)
    plt.show()

# Plotting the average execution time as line plot
plot_performance_metric_line('Execution Time', 'Execution Time (s)', 'Average Execution Time by Bit Width and Algorithm')

# Plotting the average CPU usage as line plot
plot_performance_metric_line('CPU Usage', 'CPU Usage (%)', 'Average CPU Usage by Bit Width and Algorithm')

# Plotting the average memory usage as line plot
plot_performance_metric_line('Memory Usage', 'Memory Usage (MB)', 'Average Memory Usage by Bit Width and Algorithm')
