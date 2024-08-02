import random
import csv

bit_widths = [64, 256, 512, 1024, 2048, 4096]
n_tests = 100


def generate_random_number(bit_width, N):
    return random.randint(0, N - 1)


def generate_test_data(bit_width, n_tests):
    N = 2 ** bit_width - 1  # 生成一个大于测试所需位宽的N
    test_data = []

    for _ in range(n_tests):
        x = generate_random_number(bit_width, N)
        y = generate_random_number(bit_width, N)
        test_data.append((x, y))

    return test_data


# 生成每个位宽的测试数据并保存到文件
for bit_width in bit_widths:
    test_data = generate_test_data(bit_width, n_tests)
    filename = f'test_data_{bit_width}.csv'

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x', 'y'])  # 写入表头
        writer.writerows(test_data)

    print(f'Test data for bit width {bit_width} saved to {filename}')
