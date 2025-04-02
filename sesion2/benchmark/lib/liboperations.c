#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/**
 * Allocates memory for a matrix.
 * @param rows Number of rows in the matrix.
 * @param columns Number of columns in the matrix.
 * @return Pointer to the matrix.
 */
int **allocate_matrix(int rows, int columns)
{
    int **matrix = (int **)malloc(rows * sizeof(int *));
    if (matrix == NULL)
    {
        fprintf(stderr, "Error: Out of memory\n");
        return NULL;
    }

    for (int i = 0; i < rows; i++)
    {
        matrix[i] = (int *)malloc(columns * sizeof(int));
        if (matrix[i] == NULL)
        {
            fprintf(stderr, "Error: Out of memory\n");
            return NULL;
        }
    }

    return matrix;
}

/**
 * Frees memory allocated for a matrix.
 * @param rows Number of rows in the matrix.
 * @param matrix Pointer to the matrix.
 */
void free_matrix(int rows, int **matrix)
{
    for (int i = 0; i < rows; i++)
        free(matrix[i]);

    free(matrix);
}

/**
 * Generates random numbers for a matrix.
 * @param rows Number of rows in the matrix.
 * @param columns Number of columns in the matrix.
 * @param matrix Pointer to the matrix.
 */
void generate_matrix(int rows, int columns, int **matrix)
{
    srand(clock());
    for (int i = 0; i < rows; i++)
        for (int j = 0; j < columns; j++)
            matrix[i][j] = rand() % 10; // Generate numbers between 0 and 9
}

/**
 * Fills a matrix with a specific value.
 * @param rows Number of rows in the matrix.
 * @param columns Number of columns in the matrix.
 * @param matrix Pointer to the matrix.
 * @param value Value to fill the matrix with.
 */
void fill_matrix(int rows, int columns, int **matrix, int value)
{
    for (int i = 0; i < rows; i++)
        for (int j = 0; j < columns; j++)
            matrix[i][j] = value;
}

/**
 * Multiplies two matrices in row-major order.
 * @param rows Number of rows in the matrices.
 * @param columns Number of columns in the matrices.
 * @param A Pointer to the first matrix.
 * @param B Pointer to the second matrix.
 * @param C Pointer to the resulting matrix.
 */
void row_major_mul(int rows, int columns, int **A, int **B, int **C)
{
    for (int i = 0; i < rows; i++)
        for (int j = 0; j < columns; j++)
            for (int k = 0; k < columns; k++)
                C[i][j] += A[i][k] * B[k][j];
}

/**
 * Multiplies two matrices in column-major order.
 * @param rows Number of rows in the matrices.
 * @param columns Number of columns in the matrices.
 * @param A Pointer to the first matrix.
 * @param B Pointer to the second matrix.
 * @param C Pointer to the resulting matrix.
 */
void column_major_mul(int rows, int columns, int **A, int **B, int **C)
{
    for (int j = 0; j < columns; j++)
        for (int i = 0; i < rows; i++)
            for (int k = 0; k < columns; k++)
                C[i][j] += A[i][k] * B[k][j];
}

/**
 * Multiplies two matrices in Z-order.
 * @param rows Number of rows in the matrices.
 * @param columns Number of columns in the matrices.
 * @param A Pointer to the first matrix.
 * @param B Pointer to the second matrix.
 * @param C Pointer to the resulting matrix.
 * @param block_size Size of the block to be processed. Must be a divisor of rows and columns.
 */
void zorder_mul(int rows, int columns, int **A, int **B, int **C, int block_size)
{
    if (rows % block_size != 0 || columns % block_size != 0)
    {
        fprintf(stderr, "Error: block_size must be a divisor of rows and columns\n");
        exit(1);
    }

    for (int i = 0; i < rows; i += block_size)
        for (int j = 0; j < columns; j += block_size)
            for (int k = 0; k < columns; k += block_size)
                for (int ii = i; ii < i + block_size && ii < rows; ii++)
                    for (int jj = j; jj < j + block_size && jj < columns; jj++)
                        for (int kk = k; kk < k + block_size && kk < columns; kk++)
                            C[ii][jj] += A[ii][kk] * B[kk][jj];
}