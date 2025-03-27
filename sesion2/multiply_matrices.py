import sys
import random
import time
from utils import verify_multiplication, print_matrix
from typing import List, Dict

type matrix = List[List[int]]

def generate_matrix(rows, cols) -> matrix:
    """Create an array in Python as a list of lists."""
    return [[random.randint(0, 9) for _ in range(cols)] for _ in range(rows)]

def row_major_mul(a: matrix, b: matrix, c: matrix) -> None:
    """Multiplication of matrices in row-major order."""
    rows = len(a)
    columns = len(b[0])
    for i in range(rows):
        for j in range(columns):
            for k in range(columns):
                c[i][j] += a[i][k] * b[k][j]
 
def column_major_mul(a: matrix, b: matrix, c: matrix) -> None:
    """Multiplication of matrices in column-major order."""
    rows = len(a)
    columns = len(b[0])
    for j in range(columns):
        for i in range(rows):
            for k in range(columns):
                c[i][j] += a[i][k] * b[k][j]

def zorder_mul(a: matrix, b: matrix, c: matrix, block_size: int) -> None:
    """Matrix multiplication in Z order (Morton Order)."""
    if block_size % 2 != 0:
        print("Block size must be a power of 2")
        sys.exit(1)
    
    rows = len(a)
    columns = len(b[0])
    for i in range(0, rows, block_size):
        for j in range(0, columns, block_size):
            for k in range(0, columns, block_size):
                for ii in range(i, min(i + block_size, rows)):
                    for jj in range(j, min(j + block_size, columns)):
                        for kk in range(k, min(k + block_size, columns)):
                            c[ii][jj] += a[ii][kk] * b[kk][jj]

def run_phase_1(matrix_size: int, block_size: int) -> Dict[str, float]:
    """Run phase 1 of the experiment with validation."""

    def measure_time(mul_func: callable, a: matrix, b: matrix) -> float:
        """Measure the execution time of matrix multiplication functions used in phase 1."""
        C = [[0] * matrix_size for _ in range(matrix_size)]
        start = time.time()
        mul_func(a, b, C)
        exec_time = time.time() - start
        
        assert verify_multiplication(a, b, C), f"Error in {mul_func.__name__}!"
        return exec_time

    A = generate_matrix(matrix_size, matrix_size)
    B = generate_matrix(matrix_size, matrix_size)

    return {
        "Row-major order": measure_time(row_major_mul, A, B),
        "Column-major order": measure_time(column_major_mul, A, B),
        "Z order": {block_size: measure_time(lambda a, b, c: zorder_mul(a, b, c, block_size), A, B)}
    }
    
if __name__ == "__main__":  
    if len(sys.argv) != 4:
        print("Usage: python 2-multiply_matrices.py <rows> <columns> <block_size>")
        sys.exit(1)
    
    # Get matrices size
    rows = int(sys.argv[1])
    columns = int(sys.argv[2])
    block_size = int(sys.argv[3])
    
    # Generate random matrices
    A = generate_matrix(rows, columns)
    B = generate_matrix(rows, columns)
    
    # Row-major order matrix multiplication
    C_rows = [[0] * columns for _ in range(rows)] # Initialize C_rows with zeros
    start = time.time()
    row_major_mul(A, B, C_rows)
    print(f"Row-major order: {time.time() - start:.6f} seconds")
    print_matrix(C_rows)
    
    # Column-major order matrix multiplication
    C_columns = [[0] * columns for _ in range(rows)] # Initialize C_columns with zeros
    start = time.time()
    column_major_mul(A, B, C_columns)
    print(f"Column-major order: {time.time() - start:.6f} seconds")
    print_matrix(C_columns)
    
    # Z order matrix multiplication
    C_zorder = [[0] * columns for _ in range(rows)] # Initialize C_zorder with zeros
    start = time.time()
    zorder_mul(A, B, C_zorder, block_size)
    print(f"Z order: {time.time() - start:.6f} seconds")
    print_matrix(C_zorder)
