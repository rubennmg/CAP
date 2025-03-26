import ctypes
import sys
import random
import time
from utils import verify_multiplication, print_matrix, matrix_to_c, matrix_to_python
from typing import List, Dict, Callable

type matrix = List[List[int]]

# Load shared library
lib = ctypes.CDLL('./liboperations.so')

# Common arguments for matrix multiplication functions
common_args = [
    ctypes.c_int,
    ctypes.c_int,
    ctypes.POINTER(ctypes.POINTER(ctypes.c_int)),
    ctypes.POINTER(ctypes.POINTER(ctypes.c_int)),
    ctypes.POINTER(ctypes.POINTER(ctypes.c_int))
]

# row_major_mul function prototype
lib.row_major_mul.argtypes = common_args
lib.row_major_mul.restype = None

# column_major_mul function prototype
lib.column_major_mul.argtypes = common_args
lib.column_major_mul.restype = None

# zorder_mul function prototype
lib.zorder_mul.argtypes = common_args + [ctypes.c_int]
lib.zorder_mul.restype = None

def generate_matrix(rows: int, cols: int) -> matrix:
    """Create an array in Python as a list of lists."""
    return [[random.randint(0, 9) for _ in range(cols)] for _ in range(rows)]
    
def run_phase_2(matrix_size: int, block_size: int) -> Dict[str, float]:
    """Run phase 2 of the experiment."""
    
    def measure_time(mul_func: Callable, *args, block_size_arg: int = None) -> float:
        """Helper function to measure execution time of a matrix multiplication."""
        c_c = matrix_to_c([[0] * matrix_size for _ in range(matrix_size)])
        
        if mul_func == lib.zorder_mul:
            start = time.time()
            mul_func(*args, c_c, block_size_arg)
        else:
            start = time.time()
            mul_func(*args, c_c)
        
        exec_time = time.time() - start
        c_python = matrix_to_python(c_c, matrix_size, matrix_size)
        assert verify_multiplication(A, B, c_python), f"Error in {mul_func.__name__}"
        
        return exec_time
    
    A = generate_matrix(matrix_size, matrix_size)
    B = generate_matrix(matrix_size, matrix_size)
    a_c = matrix_to_c(A)
    b_c = matrix_to_c(B)

    return {
        "Row-major order": measure_time(lib.row_major_mul, matrix_size, matrix_size, a_c, b_c),
        "Column-major order": measure_time(lib.column_major_mul, matrix_size, matrix_size, a_c, b_c),
        "Z order": {block_size: measure_time(lib.zorder_mul, matrix_size, matrix_size, a_c, b_c, block_size_arg=block_size)}
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
    B = generate_matrix(columns, rows)

    # Initialize result matrix with zeros
    C = [[0] * columns for _ in range(rows)]
    
    # Convert matrices to C-compatible format
    A_c = matrix_to_c(A)
    B_c = matrix_to_c(B)
    C_c_rows = matrix_to_c(C)

    # Row-major order matrix multiplication
    start = time.time()
    lib.row_major_mul(rows, columns, A_c, B_c, C_c_rows)
    print(f"Row-major order: {time.time() - start:.6f} s")
    C_p_rows = matrix_to_python(C_c_rows, rows, columns)
    print_matrix(C_p_rows)
    
    # Column-major order matrix multiplication
    C_c_columns = matrix_to_c(C)
    start = time.time()
    lib.column_major_mul(rows, columns, A_c, B_c, C_c_columns)
    print(f"Column-major order: {time.time() - start:.6f} s")
    C_p_columns = matrix_to_python(C_c_columns, rows, columns)
    print_matrix(C_p_columns)
    
    # Z order matrix multiplication
    C_c_zorder = matrix_to_c(C)
    start = time.time()
    lib.zorder_mul(rows, columns, A_c, B_c, C_c_zorder, block_size)
    print(f"Z order: {time.time() - start:.6f} s")
    C_p_zorder = matrix_to_python(C_c_zorder, rows, columns)
    print_matrix(C_p_zorder)