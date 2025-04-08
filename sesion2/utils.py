import ctypes
import numpy as np 
from typing import List

def print_matrix(matrix: List[List[int]]) -> None:
    """Prints a matrix."""
    if len(matrix) > 10:
        print("Matrix too large to print\n")
        return
    
    for row in matrix:
        print(row)
    print()
    
def matrix_to_c(matrix: List[List[int]]) -> ctypes.POINTER:
    """Convert a list of Python lists to an array of pointers in C."""
    row_pointers = (ctypes.POINTER(ctypes.c_int) * len(matrix))()
    for i, row in enumerate(matrix):
        row_pointers[i] = (ctypes.c_int * len(row))(*row)
    return row_pointers

def matrix_to_python(matrix_c: List[List[int]], rows: int, columns: int) -> List[List[int]]:
    """Convert a matrix in C format to a list of Python lists."""
    matrix = [[0] * columns for _ in range(rows)]
    for i in range(rows):
        for j in range(columns):
            matrix[i][j] = matrix_c[i][j]
    return matrix

def verify_multiplication(a: List[List[int]], b: List[List[int]], c: List[List[int]]) -> bool:
    """"Verify the result of a matrix multiplication using numpy."""
    c_expected = np.dot(np.array(a), np.array(b))
    return np.array_equal(np.array(c), c_expected)