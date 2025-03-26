from multiply_matrices import run_phase_1
from multiply_matrices_hybrid import run_phase_2

row_major_str = "Row-major order"
column_major_str = "Column-major order"
z_order_str = "Z order"

def run_phase(id: int, matrix_sizes, iterations):
    results = {}
    
    for matrix_size in matrix_sizes:
        block_sizes = calculate_block_sizes(matrix_size)
        initialize_results(results, matrix_size, block_sizes)
        process_block_sizes(id, matrix_size, block_sizes, iterations, results)
    
    print_results(matrix_sizes, iterations, results)


def calculate_block_sizes(matrix_size):
    block_sizes = []
    for block_size in range(2, matrix_size + 1):
        if matrix_size % block_size == 0 and matrix_size // block_size >= 2:
            block_sizes.append(block_size)
    return block_sizes


def initialize_results(results, matrix_size, block_sizes):
    if matrix_size not in results:
        results[matrix_size] = {
            row_major_str: 0.0,
            column_major_str: 0.0,
            z_order_str: {block_size: 0 for block_size in block_sizes}
        }

def process_block_sizes(id, matrix_size, block_sizes, iterations, results):
    for block_size in block_sizes:
        for _ in range(iterations):
            current_result = run_phase_1(matrix_size, block_size) if id == 1 else run_phase_2(matrix_size, block_size)
            update_results(results, matrix_size, current_result)


def update_results(results, matrix_size, current_result):
    results[matrix_size][row_major_str] += current_result[row_major_str]
    results[matrix_size][column_major_str] += current_result[column_major_str]
    for bz, time in current_result[z_order_str].items():
        results[matrix_size][z_order_str][bz] += time


def print_results(matrix_sizes, iterations, results):
    print("Matrix size;Block-size;Row-major (s);Column-major (s);Z order (s)")
    
    for matrix_size in matrix_sizes:
        row_major_avg = results[matrix_size][row_major_str] / iterations
        column_major_avg = results[matrix_size][column_major_str] / iterations

        for block_size, time in results[matrix_size][z_order_str].items():
            zorder_avg = time / iterations
            print(f"{matrix_size};{block_size};{row_major_avg:.6f};{column_major_avg:.6f};{zorder_avg:.6f}")

if __name__ == "__main__":
    matrix_sizes = [2, 4, 8, 16, 32]
    iterations = 10
    
    run_phase(1, matrix_sizes, iterations)
    run_phase(2, matrix_sizes, iterations)