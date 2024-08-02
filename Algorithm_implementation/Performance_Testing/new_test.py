import time
import gmpy2
import csv
from gmpy2 import mpz
from tqdm import tqdm

from Algorithm_implementation.Barrett.barrett_reduction import BarrettMul
from Algorithm_implementation.Montgomery.montgomery_code import MontMul


def generate_random_int(bit_width, N):
    """生成小于 N 的指定位宽的大数"""
    while True:
        num = gmpy2.mpz(gmpy2.mpz_urandomb(gmpy2.random_state(), bit_width))
        if num < N:
            return num


def run_experiment():
    bit_widths = [64, 128, 256, 512, 1024, 2048]
    N = mpz(
        'FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF',
        16)

    results = []

    total_tests = len(bit_widths) * 100

    with tqdm(total=total_tests) as pbar:
        for bit_width in bit_widths:
            for _ in range(100):
                a = generate_random_int(bit_width, N)
                b = generate_random_int(bit_width, N)

                montgomery = MontMul(bit_width, N)
                barrett = BarrettMul(N, bit_width)

                start_time = time.time()
                montgomery_result = montgomery.modmul(a, b)
                montgomery_time = time.time() - start_time

                start_time = time.time()
                barrett_result = barrett.multiply(a, b)
                barrett_time = time.time() - start_time

                results.append([bit_width, 'Montgomery', montgomery_time])
                results.append([bit_width, 'Barrett', barrett_time])

                pbar.update(1)

    with open('performance_comparison.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Bit Width', 'Algorithm', 'Execution Time (s)'])
        writer.writerows(results)


if __name__ == '__main__':
    run_experiment()
