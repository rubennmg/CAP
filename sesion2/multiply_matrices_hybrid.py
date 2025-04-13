import ctypes
import sys
import random
import time
from utils import verify_multiplication, print_matrix, matrix_to_c, matrix_to_python
from typing import List, Tuple

# Load shared library
lib = ctypes.CDLL('./lib/liboperations.so')

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

def generate_matrix(rows: int, cols: int) -> List[List[int]]:
    """Create an array in Python as a list of lists.

    Args:
        rows (int): Number of rows of the matrix
        cols (int): Number of columns of the matrix

    Returns:
        List[List[int]]: Random generated matrix
    """
    return [[random.randint(0, 9) for _ in range(cols)] for _ in range(rows)]

def run_phase_2_row_col(matrix_size: int, algorithm: str) -> float:
    """Run phase 2 of the experiment for row-major or column-major order.
    This function measures the execution time of matrix multiplication usign
    row-major and column-major order algorithms.
    Time measuring starts before the matrix generation with python and ends
    after the multiplication with C.

    Args:
        matrix_size (int): Size of the matrix.
        algorithm (str): Algorithm to use for multiplication ('row' or 'col').

    Returns:
        float: Execution time in seconds.
    """
    start = time.time()
    
    A = generate_matrix(matrix_size, matrix_size)
    B = generate_matrix(matrix_size, matrix_size)
    
    a_c = matrix_to_c(A)
    b_c = matrix_to_c(B)
    
    c_c_result = matrix_to_c([[0] * matrix_size for _ in range(matrix_size)])
    
    if algorithm == "row":
        lib.row_major_mul(matrix_size, matrix_size, a_c, b_c, c_c_result)
    elif algorithm == "col":
        lib.column_major_mul(matrix_size, matrix_size, a_c, b_c, c_c_result)
    
    exec_time = time.time() - start
    
    # Check product results
    # c_python = matrix_to_python(c_c_result, matrix_size, matrix_size)
    
    # assert verify_multiplication(A, B, c_python), f"Error in r{algorithm}-major multiplication"
    
    return exec_time

def run_phase_2_zorder(matrix_size: int, block_size: int) -> float:
    """Run phase 2 of the experiment for Z-order algorithm.
    This function measures the execution time of matrix multiplication using
    Z-order algorithm.
    Time measuring starts before the matrix generation with python and ends
    after the multiplication with C.

    Args:
        matrix_size (int): Size of the matrix.
        block_size (int): Block size for Z-order multiplication.

    Returns:
        float: Execution time in seconds.
    """
    start = time.time()
    
    A = generate_matrix(matrix_size, matrix_size)
    B = generate_matrix(matrix_size, matrix_size)
    
    a_c = matrix_to_c(A)
    b_c = matrix_to_c(B)
    
    c_c_zorder = matrix_to_c([[0] * matrix_size for _ in range(matrix_size)])
    
    lib.zorder_mul(matrix_size, matrix_size, a_c, b_c, c_c_zorder, block_size)
    
    exec_time = time.time() - start
    
    # c_python_zorder = matrix_to_python(c_c_zorder, matrix_size, matrix_size)
    
    # assert verify_multiplication(A, B, c_python_zorder), "Error in Z order multiplication"
    
    return exec_time

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