from multiply_matrices import run_phase_1
from multiply_matrices_hybrid import run_phase_2
from multiply_matrices_hybrid_pro import run_phase_3
from typing import List, Dict

type matrix = List[List[int]]

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
    for block_size in range(2, matrix_size + 1):
        if matrix_size % block_size == 0 and matrix_size // block_size >= 2:
            block_sizes.append(block_size)
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
    for block_size in block_sizes:
        for _ in range(iterations):
            if phase_id == 1:
                current_result = run_phase_1(matrix_size, block_size)
            elif phase_id == 2:
                current_result = run_phase_2(matrix_size, block_size)
            else:
                current_result = run_phase_3(matrix_size, block_size)
            update_results(results, matrix_size, current_result)

def update_results(results: Dict[str, float], matrix_size: int, current_result: Dict[str, float]):
    """Update the results dictionary."""
    results[matrix_size][row_major_str] += current_result[row_major_str]
    results[matrix_size][column_major_str] += current_result[column_major_str]
    for bz, time in current_result[z_order_str].items():
        results[matrix_size][z_order_str][bz] += time


def print_results(phase_id: int, matrix_size: int, iterations: int, results: Dict[str, float]):
    """Print the results stored in the dictionary."""
    row_major_avg = results[matrix_size][row_major_str] / iterations
    column_major_avg = results[matrix_size][column_major_str] / iterations

    for block_size, time in results[matrix_size][z_order_str].items():
        zorder_avg = time / iterations
        print(f"{matrix_size};{block_size};{phase_id};{row_major_avg:.6f};{column_major_avg:.6f};{zorder_avg:.6f}")

if __name__ == "__main__":
    matrix_sizes = [2, 4, 8, 16, 32]
    iterations = 10
    
    run_phase(1, matrix_sizes, iterations)
    run_phase(2, matrix_sizes, iterations)
    run_phase(3, matrix_sizes, iterations)