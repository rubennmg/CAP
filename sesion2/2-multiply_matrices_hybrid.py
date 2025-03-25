import ctypes
import sys
import random
import time
from typing import List

type matrix = List[List[int]]

# Load shared library
lib = ctypes.CDLL('./liboperations.so')

# row_major_mul function prototype
lib.row_major_mul.argtypes = [
    ctypes.c_int, 
    ctypes.c_int,
    ctypes.POINTER(ctypes.POINTER(ctypes.c_int)),
    ctypes.POINTER(ctypes.POINTER(ctypes.c_int)),
    ctypes.POINTER(ctypes.POINTER(ctypes.c_int))
]
lib.row_major_mul.restype = None

# column_major_mul function prototype
lib.column_major_mul.argtypes = [
    ctypes.c_int, 
    ctypes.c_int,
    ctypes.POINTER(ctypes.POINTER(ctypes.c_int)),
    ctypes.POINTER(ctypes.POINTER(ctypes.c_int)),
    ctypes.POINTER(ctypes.POINTER(ctypes.c_int))
]
lib.column_major_mul.restype = None

# zorder_mul function prototype
lib.zorder_mul.argtypes = [
    ctypes.c_int, 
    ctypes.c_int,
    ctypes.POINTER(ctypes.POINTER(ctypes.c_int)),
    ctypes.POINTER(ctypes.POINTER(ctypes.c_int)),
    ctypes.POINTER(ctypes.POINTER(ctypes.c_int)),
    ctypes.c_int
]
lib.zorder_mul.restype = None

def generate_matrix(rows: int, cols: int) -> matrix:
    """Create an array in Python as a list of lists."""
    return [[random.randint(0, 9) for _ in range(cols)] for _ in range(rows)]

def matrix_to_c(matrix: matrix) -> ctypes.POINTER:
    """Convert a list of Python lists to an array of pointers in C."""
    row_pointers = (ctypes.POINTER(ctypes.c_int) * len(matrix))()
    for i, row in enumerate(matrix):
        row_pointers[i] = (ctypes.c_int * len(row))(*row)
    return row_pointers

def matrix_to_python(matrix_c: matrix, rows: int, columns: int) -> matrix:
    """Convert a matrix in C format to a list of Python lists."""
    matrix = [[0] * columns for _ in range(rows)]
    for i in range(rows):
        for j in range(columns):
            matrix[i][j] = matrix_c[i][j]
    return matrix

def print_matrix(matrix: matrix) -> None:
    """Prints a matrix."""
    if len(matrix) > 10:
        print("Matrix too large to print\n")
        return
    
    for row in matrix:
        print(row)
    print()

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