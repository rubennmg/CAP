#ifndef MUL_FUNCTIONS_H
#define MUL_FUNCTIONS_H

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>

/**
 * Allocates memory for a matrix.
 * @param rows Number of rows in the matrix.
 * @param columns Number of columns in the matrix.
 * @return Pointer to the matrix.
 */
int **allocate_matrix(int rows, int columns);

/**
 * Frees memory allocated for a matrix.
 * @param rows Number of rows in the matrix.
 * @param matrix Pointer to the matrix.
 */
void free_matrix(int rows, int **matrix);

/**
 * Initializes all matrices for the benchmark.
 * A and B are filled with random numbers.
 * @param matrix_size Size of the matrices.
 * @param A Pointer to the first matrix.
 * @param B Pointer to the second matrix.
 * @param C_rows Pointer to the result matrix in row-major order.
 * @param C_columns Pointer to the result matrix in column-major order.
 * @param C_zorder Pointer to the result matrix in Z-order.
 */
void init_matrices(int matrix_size, int ***A, int ***B, int ***C_rows, int ***C_columns, int ***C_zorder);

/**
 * Frees memory allocated for all matrices used in the benchmark.
 * @param matrix_size Size of the matrices.
 * @param A Pointer to the first matrix.
 * @param B Pointer to the second matrix.
 * @param C_rows Pointer to the result matrix in row-major order.
 * @param C_columns Pointer to the result matrix in column-major order.
 * @param C_zorder Pointer to the result matrix in Z-order.
 * @note This function assumes that all matrices have been allocated and initialized.
 *       It does not check for NULL pointers.
 */
void free_matrices(int matrix_size, int **A, int **B, int **C_rows, int **C_columns, int **C_zorder);

/**
 * Generates random numbers for a matrix.
 * @param rows Number of rows in the matrix.
 * @param columns Number of columns in the matrix.
 * @param matrix Pointer to the matrix.
 */
void generate_matrix(int rows, int columns, int **matrix);

/**
 * Fills a matrix with a specific value.
 * @param rows Number of rows in the matrix.
 * @param columns Number of columns in the matrix.
 * @param matrix Pointer to the matrix.
 * @param value Value to fill the matrix with.
 */
void fill_matrix(int rows, int columns, int **matrix, int value);

/**
 * Checks if two matrices are equal
 * @param matrix_size Size of the matrices
 * @param A First matrix
 * @param B Second matrix
 * @return true if the matrices are equal, false otherwise
 */
bool check_matrices(int matrix_size, int **A, int **B);

/**
 * Multiplies two matrices in row-major order.
 * @param rows Number of rows in the matrices.
 * @param columns Number of columns in the matrices.
 * @param A Pointer to the first matrix.
 * @param B Pointer to the second matrix.
 * @param C Pointer to the resulting matrix.
 */
void row_major_mul(int rows, int columns, int **A, int **B, int **C);

/**
 * Multiplies two matrices in column-major order.
 * @param rows Number of rows in the matrices.
 * @param columns Number of columns in the matrices.
 * @param A Pointer to the first matrix.
 * @param B Pointer to the second matrix.
 * @param C Pointer to the resulting matrix.
 */
void column_major_mul(int rows, int columns, int **A, int **B, int **C);

/**
 * Multiplies two matrices in Z-order.
 * @param rows Number of rows in the matrices.
 * @param columns Number of columns in the matrices.
 * @param A Pointer to the first matrix.
 * @param B Pointer to the second matrix.
 * @param C Pointer to the resulting matrix.
 * @param block_size Size of the block to be processed. Must be a divisor of rows and columns.
 */
void zorder_mul(int rows, int columns, int **A, int **B, int **C, int block_size);

#endif
