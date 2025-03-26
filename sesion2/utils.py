import numpy as np 
from typing import List

type matrix = List[List[int]]

def verify_multiplication(a: matrix, b: matrix, c: matrix) -> bool:
    """"Verify the result of a matrix multiplication using numpy."""
    c_expected = np.dot(np.array(a), np.array(b))
    return np.array_equal(np.array(c), c_expected)