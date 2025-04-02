#include "mul_functions.h"

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

void free_matrix(int rows, int **matrix)
{
    for (int i = 0; i < rows; i++)
        free(matrix[i]);

    free(matrix);
}

void init_matrices(int matrix_size, int ***A, int ***B, int ***C_rows, int ***C_columns, int ***C_zorder)
{
    *A = allocate_matrix(matrix_size, matrix_size);
    *B = allocate_matrix(matrix_size, matrix_size);
    *C_rows = allocate_matrix(matrix_size, matrix_size);
    *C_columns = allocate_matrix(matrix_size, matrix_size);
    *C_zorder = allocate_matrix(matrix_size, matrix_size);

    if (*A == NULL || *B == NULL || *C_rows == NULL || *C_columns == NULL || *C_zorder == NULL)
    {
        fprintf(stderr, "Error: Could not allocate memory for matrices.\n");
        exit(1);
    }

    srand(time(NULL));
    generate_matrix(matrix_size, matrix_size, *A);
    generate_matrix(matrix_size, matrix_size, *B);
}

void free_matrices(int matrix_size, int **A, int **B, int **C_rows, int **C_columns, int **C_zorder)
{
    free_matrix(matrix_size, A);
    free_matrix(matrix_size, B);
    free_matrix(matrix_size, C_rows);
    free_matrix(matrix_size, C_columns);
    free_matrix(matrix_size, C_zorder);
}

void generate_matrix(int rows, int columns, int **matrix)
{
    for (int i = 0; i < rows; i++)
        for (int j = 0; j < columns; j++)
            matrix[i][j] = rand() % 10; // Generate numbers between 0 and 9
}

void fill_matrix(int rows, int columns, int **matrix, int value)
{
    for (int i = 0; i < rows; i++)
        for (int j = 0; j < columns; j++)
            matrix[i][j] = value;
}

bool check_matrices(int matrix_size, int **A, int **B)
{
    for (int i = 0; i < matrix_size; i++)
    {
        for (int j = 0; j < matrix_size; j++)
        {
            if (A[i][j] != B[i][j])
            {
                return false;
            }
        }
    }

    return true;
}

void row_major_mul(int rows, int columns, int **A, int **B, int **C)
{
    for (int i = 0; i < rows; i++)
        for (int j = 0; j < columns; j++)
            for (int k = 0; k < columns; k++)
                C[i][j] += A[i][k] * B[k][j];
}

void column_major_mul(int rows, int columns, int **A, int **B, int **C)
{
    for (int j = 0; j < columns; j++)
        for (int i = 0; i < rows; i++)
            for (int k = 0; k < columns; k++)
                C[i][j] += A[i][k] * B[k][j];
}

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