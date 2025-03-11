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
        fprintf(stderr, "Error allocating memory for matrix\n");
        exit(1);
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
    // TODO
}

// Function to add matrices in column-major order
void column_major_mul(int rows, int columns, int **A, int **B, int **C)
{
    // TODO
}

// Function to add matrices in z-order order
void zorder_mul(int rows, int columns, int **A, int **B, int **C, int block_size)
{
    // TODO
}

int main(int argc, char *argv[])
{
    int rows, columns;                               // Matrix size (rows x columns)
    int **A, **B, **C_rows, **C_columns, **C_zorder; // Matrices
    clock_t start, end;                              // To measure time

    // Get matrices size
    if (argc != 4)
    {
        fprintf(stderr, "Usage: %s <rows> <columns> <block_size>\n", argv[0]);
        exit(1);
    }

    // Allocate memory for matrices
    rows = atoi(argv[1]);
    columns = atoi(argv[2]);
    A = allocate_matrix(rows, columns);
    B = allocate_matrix(rows, columns);

    // Generate random matrices
    srand(time(NULL)); // Initialize the random number generator once
    generate_matrix(rows, columns, A);
    generate_matrix(rows, columns, B);

    printMatrix(A, rows, columns);
    printMatrix(B, rows, columns);

    // Add matrices and measure times

    // Free matrices
    free_matrix(rows, A);
    free_matrix(rows, B);

    return 0;
}