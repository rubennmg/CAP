import ctypes
import sys
import random
import time
from typing import List

type matrix = List[List[int]]

# Load shared library
lib = ctypes.CDLL('./liboperations.so')

# allocate_matrix and free_matrix function prototypes
lib.allocate_matrix.argtypes = [ctypes.c_int, ctypes.c_int]
lib.allocate_matrix.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_int))

# free_matrix function prototype
lib.free_matrix.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_int))]
lib.free_matrix.restype = None

# generate_matrix function prototype
lib.generate_matrix.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.POINTER(ctypes.c_int))]
lib.generate_matrix.restype = None

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

    # Allocate space for matrices
    A = lib.allocate_matrix(rows, columns)
    B = lib.allocate_matrix(rows, columns)
    C_rows = lib.allocate_matrix(rows, columns)
    C_columns = lib.allocate_matrix(rows, columns)
    C_zorder = lib.allocate_matrix(rows, columns)
    
    # Generate random matrices
    lib.generate_matrix(rows, columns, A)
    lib.generate_matrix(rows, columns, B)

    # Row-major order matrix multiplication
    start = time.time()
    lib.row_major_mul(rows, columns, A, B, C_rows)
    print(f"Row-major order: {time.time() - start:.6f} s")
    C_p_rows = matrix_to_python(C_rows, rows, columns)
    print_matrix(C_p_rows)
    
    # Column-major order matrix multiplication
    start = time.time()
    lib.column_major_mul(rows, columns, A, B, C_columns)
    print(f"Column-major order: {time.time() - start:.6f} s")
    C_p_columns = matrix_to_python(C_columns, rows, columns)
    print_matrix(C_p_columns)
    
    # Z order matrix multiplication
    start = time.time()
    lib.zorder_mul(rows, columns, A, B, C_zorder, block_size)
    print(f"Z order: {time.time() - start:.6f} s")
    C_p_zorder = matrix_to_python(C_zorder, rows, columns)
    print_matrix(C_p_zorder)