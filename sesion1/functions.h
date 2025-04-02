#ifndef FUNCTIONS_H
#define FUNCTIONS_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/**
 * Prints a matrix.
 * @param rows Number of rows in the matrix.
 * @param columns Number of columns in the matrix.
 * @param matrix Pointer to the matrix to be printed.
 */
void print_matrix(int rows, int columns, int **matrix);

/**
 * Prints the product of two matrices.
 * @param A Pointer to the first matrix.
 * @param B Pointer to the second matrix.
 * @param C Pointer to the resulting matrix.
 * @param rows Number of rows in the matrices.
 * @param columns Number of columns in the matrices.
 */
void print_product(int **A, int **B, int **C, int rows, int columns);

/**
 * Checks if the matrix was allocated correctly.
 * @param matrix Pointer to the matrix to be checked.
 */
void check_err(int **matrix);

#endif