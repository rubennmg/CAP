import time
import sys

sys.path.append("..")

from multiply_matrices import run_phase_1_row_col, run_phase_1_zorder
from multiply_matrices_hybrid import run_phase_2_row_col, run_phase_2_zorder
from multiply_matrices_hybrid_pro import run_phase_3_row_col, run_phase_3_zorder
from typing import List, Dict

row_major_str = "Row-major order"
column_major_str = "Column-major order"
z_order_str = "Z order"

def run_phase(phase_id: int, matrix_sizes: List[int], iterations: int):
    """Runs a phase of the experiment."""
    results = {}
    
    print("Matrix size;Block size;Phase;Row-major order (s);Column-major order (s);Z order (s)")
    
    for matrix_size in matrix_sizes:
        block_sizes = calculate_block_sizes(matrix_size)
        initialize_results(results, matrix_size, block_sizes)
        process_block_sizes(phase_id, matrix_size, block_sizes, iterations, results)
        print_results(phase_id, matrix_size, iterations, results)

def calculate_block_sizes(matrix_size: int) -> List[int]:
    """Calculate the block sizes for the given matrix size."""
    block_sizes = []
    for block_size in range(1, matrix_size + 1):
        if matrix_size % block_size == 0 and matrix_size // block_size >= 2:
            block_sizes.append(block_size)
    block_sizes.append(matrix_size)
    return block_sizes

def initialize_results(results: Dict[str, float], matrix_size: int, block_sizes: List[int]):
    """Initialize the results dictionary."""
    if matrix_size not in results:
        results[matrix_size] = {
            row_major_str: 0.0,
            column_major_str: 0.0,
            z_order_str: {block_size: 0 for block_size in block_sizes}
        }

def process_block_sizes(phase_id: int, matrix_size: int, block_sizes: List[int], iterations: int, results: Dict[str, float]):
    """Process the block sizes for the given matrix size."""
    for _ in range(iterations):
        if phase_id == 1:
            row_time, col_time = run_phase_1_row_col(matrix_size)
        elif phase_id == 2:
            row_time, col_time = run_phase_2_row_col(matrix_size)
        else:
            row_time, col_time = run_phase_3_row_col(matrix_size)
        
        results[matrix_size][row_major_str] += row_time
        results[matrix_size][column_major_str] += col_time
        for block_size in block_sizes:
            if phase_id == 1:
                zorder_time = run_phase_1_zorder(matrix_size, block_size)
            elif phase_id == 2:
                zorder_time = run_phase_2_zorder(matrix_size, block_size)
            else:
                zorder_time = run_phase_3_zorder(matrix_size, block_size)
            results[matrix_size][z_order_str][block_size] += zorder_time

def print_results(phase_id: int, matrix_size: int, iterations: int, results: Dict[str, float]):
    """Print the results stored in the dictionary."""
    row_major_avg = results[matrix_size][row_major_str] / iterations
    column_major_avg = results[matrix_size][column_major_str] / iterations

    for block_size, time in results[matrix_size][z_order_str].items():
        zorder_avg = time / iterations
        print(f"{matrix_size};{block_size};{phase_id};{row_major_avg:f};{column_major_avg:f};{zorder_avg:f}")

if __name__ == "__main__":
    matrix_sizes = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    iterations = 32
    
    start = time.time()
    run_phase(1, matrix_sizes, iterations)
    run_phase(2, matrix_sizes, iterations)
    run_phase(3, matrix_sizes, iterations)
    end = time.time()
    
    print(f"\nTotal execution time: {end - start:f} seconds")