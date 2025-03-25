#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "functions.h"

// Function to allocate a matrix of size rows x columns
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

// Function to free the memory of the matrix
void free_matrix(int rows, int **matrix)
{
    for (int i = 0; i < rows; i++)
    {
        free(matrix[i]);
    }
    free(matrix);
}

// Function to generate a random matrix of size rows x columns
void generate_matrix(int rows, int columns, int **matrix)
{
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < columns; j++)
        {
            matrix[i][j] = rand() % 10; // Generate numbers between 0 and 9
        }
    }
}

// Function to add matrices in row-major order
void row_major_mul(int rows, int columns, int **A, int **B, int **C)
{
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < columns; j++)
        {
            C[i][j] = 0;
            for (int k = 0; k < columns; k++)
            {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

// Function to add matrices in column-major order
void column_major_mul(int rows, int columns, int **A, int **B, int **C)
{
    for (int j = 0; j < columns; j++)
    {
        for (int i = 0; i < rows; i++)
        {
            C[i][j] = 0;
            for (int k = 0; k < columns; k++)
            {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

// Function to add matrices in z-order order
void zorder_mul(int rows, int columns, int **A, int **B, int **C, int block_size)
{
    if (rows % block_size != 0 || columns % block_size != 0)
    {
        fprintf(stderr, "Error: block_size must be a divisor of rows and columns\n");
        exit(1);
    }

    for (int i = 0; i < rows; i += block_size)
    {
        for (int j = 0; j < columns; j += block_size)
        {
            for (int k = 0; k < columns; k += block_size)
            {
                for (int ii = i; ii < i + block_size && ii < rows; ii++)
                {
                    for (int jj = j; jj < j + block_size && jj < columns; jj++)
                    {
                        for (int kk = k; kk < k + block_size && kk < columns; kk++)
                        {
                            C[ii][jj] += A[ii][kk] * B[kk][jj];
                        }
                    }
                }
            }
        }
    }
}

int main(int argc, char *argv[])
{
    int rows, columns, block_size;                   // Matrix size (rows x columns)
    int **A, **B, **C_rows, **C_columns, **C_zorder; // Matrices
    clock_t start, end;                              // To measure time

    // Get matrices size
    if (argc != 4)
    {
        fprintf(stderr, "Usage: %s <rows> <columns> <block_size>\n", argv[0]);
        exit(1);
    }

    rows = atoi(argv[1]);
    columns = atoi(argv[2]);
    block_size = atoi(argv[3]);

    // Allocate memory for matrices
    A = allocate_matrix(rows, columns);
    B = allocate_matrix(rows, columns);
    C_rows = allocate_matrix(rows, columns);
    C_columns = allocate_matrix(rows, columns);
    C_zorder = allocate_matrix(rows, columns);

    // Generate random matrices
    srand(time(NULL)); // Initialize the random number generator once
    generate_matrix(rows, columns, A);
    generate_matrix(rows, columns, B);

    // Add matrices and measure times
    measureTime(rows, columns, A, B, C_rows, row_major_mul);
    measureTime(rows, columns, A, B, C_columns, column_major_mul);
    start = clock();
    zorder_mul(rows, columns, A, B, C_zorder, block_size);
    end = clock();
    double execution_time = (double)(end - start) / CLOCKS_PER_SEC;
    printf("Time: %f seconds\n", execution_time);

    printProduct(A, B, C_rows, rows, columns);
    printProduct(A, B, C_columns, rows, columns);
    printProduct(A, B, C_zorder, rows, columns);

    // Free matrices
    free_matrix(rows, A);
    free_matrix(rows, B);
    free_matrix(rows, C_rows);
    free_matrix(rows, C_columns);
    free_matrix(rows, C_zorder);

    return 0;
}