import ctypes
import numpy as np 
from typing import List

type matrix = List[List[int]]

def print_matrix(matrix: matrix) -> None:
    """Prints a matrix."""
    if len(matrix) > 10:
        print("Matrix too large to print\n")
        return
    
    for row in matrix:
        print(row)
    print()
    
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

def verify_multiplication(a: matrix, b: matrix, c: matrix) -> bool:
    """"Verify the result of a matrix multiplication using numpy."""
    c_expected = np.dot(np.array(a), np.array(b))
    return np.array_equal(np.array(c), c_expected)