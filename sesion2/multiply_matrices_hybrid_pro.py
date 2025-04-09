import ctypes
import sys
import time
from utils import verify_multiplication, print_matrix, matrix_to_python
from typing import List, Tuple

# Load shared library
lib = ctypes.CDLL('./lib/liboperations.so')

# allocate_matrix and free_matrix function prototypes
lib.allocate_matrix.argtypes = [ctypes.c_int, ctypes.c_int]
lib.allocate_matrix.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_int))

# free_matrix function prototype
lib.free_matrix.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_int))]
lib.free_matrix.restype = None

# generate_matrix function prototype
lib.generate_matrix.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_int))]
lib.generate_matrix.restype = None

# fill_matrix function prototype
lib.fill_matrix.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_int)), ctypes.c_int]
lib.fill_matrix.restype = None

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

def run_phase_3_row_col(matrix_size: int, algorithm: str) -> Tuple[float, float]:
    """Run phase 3 of the experiment for row-major and column-major order."""
    start = time.time()
    
    A = lib.allocate_matrix(matrix_size, matrix_size)
    B = lib.allocate_matrix(matrix_size, matrix_size)
    c_result = lib.allocate_matrix(matrix_size, matrix_size)

    lib.generate_matrix(matrix_size, matrix_size, A)
    lib.generate_matrix(matrix_size, matrix_size, B)

    lib.fill_matrix(matrix_size, matrix_size, c_result, 0)

    if algorithm == "row":
        lib.row_major_mul(matrix_size, matrix_size, A, B, c_result)

    elif algorithm == "col":
        lib.column_major_mul(matrix_size, matrix_size, A, B, c_result)

    # Check product results
    # c_python = matrix_to_python(c_result, matrix_size, matrix_size)
    # a_python = matrix_to_python(A, matrix_size, matrix_size)
    # b_python = matrix_to_python(B, matrix_size, matrix_size)

    # assert verify_multiplication(a_python, b_python, c_python), f"Error in {algorithm}-major multiplication"

    lib.free_matrix(matrix_size, A)
    lib.free_matrix(matrix_size, B)
    lib.free_matrix(matrix_size, c_result)
    
    exec_time = time.time() - start

    return exec_time

def run_phase_3_zorder(matrix_size: int, block_size: int) -> float:
    """Run phase 3 of the experiment for Z order."""
    start = time.time()
   
    A = lib.allocate_matrix(matrix_size, matrix_size)
    B = lib.allocate_matrix(matrix_size, matrix_size)
    c_zorder = lib.allocate_matrix(matrix_size, matrix_size)

    lib.generate_matrix(matrix_size, matrix_size, A)
    lib.generate_matrix(matrix_size, matrix_size, B)

    # Fill result matrices with zeros
    lib.fill_matrix(matrix_size, matrix_size, c_zorder, 0)

    lib.zorder_mul(matrix_size, matrix_size, A, B, c_zorder, block_size)

    # c_python_zorder = matrix_to_python(c_zorder, matrix_size, matrix_size)
    # a_python = matrix_to_python(A, matrix_size, matrix_size)
    # b_python = matrix_to_python(B, matrix_size, matrix_size)

    # assert verify_multiplication(a_python, b_python, c_python_zorder), "Error in Z order multiplication"

    lib.free_matrix(matrix_size, A)
    lib.free_matrix(matrix_size, B)
    lib.free_matrix(matrix_size, c_zorder)
    
    exec_time = time.time() - start

    return exec_time
    
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python 2-multiply_matrices.py <rows> <columns> <block_size>")
        sys.exit(1)

    # Get matrices size
    rows = int(sys.argv[1])
    columns = int(sys.argv[2])
    block_size = int(sys.argv[3])

    # Allocate space for matrices
    A = lib.allocate_matrix(rows, columns)
    B = lib.allocate_matrix(rows, columns)
    C_rows = lib.allocate_matrix(rows, columns)
    C_columns = lib.allocate_matrix(rows, columns)
    C_zorder = lib.allocate_matrix(rows, columns)
    
    # Generate random matrices
    lib.generate_matrix(rows, columns, A)
    lib.generate_matrix(rows, columns, B)
    
    # Fill result matrices with zeros
    lib.fill_matrix(rows, columns, C_rows, 0)
    lib.fill_matrix(rows, columns, C_columns, 0)
    lib.fill_matrix(rows, columns, C_zorder, 0)

    # Row-major order matrix multiplication
    start = time.time()
    lib.row_major_mul(rows, columns, A, B, C_rows)
    end = time.time()
    print(f"Row-major order: {end - start:f} s")
    C_p_rows = matrix_to_python(C_rows, rows, columns)
    print_matrix(C_p_rows)
    
    # Column-major order matrix multiplication
    start = time.time()
    lib.column_major_mul(rows, columns, A, B, C_columns)
    end = time.time()
    print(f"Column-major order: {end - start:f} s")
    C_p_columns = matrix_to_python(C_columns, rows, columns)
    print_matrix(C_p_columns)
    
    # Z order matrix multiplication
    start = time.time()
    lib.zorder_mul(rows, columns, A, B, C_zorder, block_size)
    end = time.time()
    print(f"Z order: {end - start:f} s")
    C_p_zorder = matrix_to_python(C_zorder, rows, columns)
    print_matrix(C_p_zorder)
    
    # Free matrices
    lib.free_matrix(rows, A)
    lib.free_matrix(rows, B)
    lib.free_matrix(rows, C_rows)
    lib.free_matrix(rows, C_columns)
    lib.free_matrix(rows, C_zorder)