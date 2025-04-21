#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "functions.h"

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

/**
 * Processes command line arguments.
 * @param argc Number of arguments.
 * @param argv Array of arguments.
 * @param rows Pointer to the number of rows.
 * @param columns Pointer to the number of columns.
 * @param block_size Pointer to the block size.
 */
void process_arguments(int argc, char *argv[], int *rows, int *columns, int *block_size)
{
    if (argc != 4)
    {
        fprintf(stderr, "Usage: %s <rows> <columns> <block_size>\n", argv[0]);
        exit(1);
    }

    *rows = atoi(argv[1]);
    *columns = atoi(argv[2]);
    *block_size = atoi(argv[3]);
}

/**
 * Main function.
 * @param argc Number of arguments.
 * @param argv Array of arguments.
 * @return 0 if the program ends successfully, 1 otherwise.
 */
int main(int argc, char *argv[])
{
    int rows, columns, block_size;                   // Matrix size (rows x columns)
    int **A, **B, **C_rows, **C_columns, **C_zorder; // Matrices
    clock_t start, end;                              // To measure time
    double execution_time;                           // Time in seconds

    // Process arguments
    process_arguments(argc, argv, &rows, &columns, &block_size);

    // Allocate memory for matrices
    A = allocate_matrix(rows, columns);
    check_err(A);
    B = allocate_matrix(rows, columns);
    check_err(B);
    C_rows = allocate_matrix(rows, columns);
    check_err(C_rows);
    C_columns = allocate_matrix(rows, columns);
    check_err(C_columns);
    C_zorder = allocate_matrix(rows, columns);
    check_err(C_zorder);

    // Generate random matrices
    srand(time(NULL)); // Initialize the random number generator once
    generate_matrix(rows, columns, A);
    generate_matrix(rows, columns, B);

    // Initialize result matrices with zeros
    fill_matrix(rows, columns, C_rows, 0);
    fill_matrix(rows, columns, C_columns, 0);
    fill_matrix(rows, columns, C_zorder, 0);

    // Row major multiplication
    start = clock();
    row_major_mul(rows, columns, A, B, C_rows);
    end = clock();
    execution_time = (double)(end - start) / CLOCKS_PER_SEC;
    printf("\n************************************************************\n");
    printf("Row major multiplication with %d rows and %d columns:\n", rows, columns);
    printf("\t- Time: %f seconds\n", execution_time);
    printf("************************************************************\n");

    // Column major multiplication
    start = clock();
    column_major_mul(rows, columns, A, B, C_columns);
    end = clock();
    execution_time = (double)(end - start) / CLOCKS_PER_SEC;
    printf("\n************************************************************\n");
    printf("Column major multiplication with %d rows and %d columns:\n", rows, columns);
    printf("\t- Time: %f seconds\n", execution_time);
    printf("************************************************************\n");

    // Z-order multiplication
    start = clock();
    zorder_mul(rows, columns, A, B, C_zorder, block_size);
    end = clock();
    execution_time = (double)(end - start) / CLOCKS_PER_SEC;
    printf("\n************************************************************\n");
    printf("Z-order multiplication %d rows, %d columns and %d block_size:\n", rows, columns, block_size);
    printf("\t- Time: %f seconds\n", execution_time);
    printf("************************************************************\n");

    // Print matrices (development purposes)
    printf("\nRow major multiplication:");
    print_product(A, B, C_rows, rows, columns);
    printf("\nColumn major multiplication:");
    print_product(A, B, C_columns, rows, columns);
    printf("\nZ-order multiplication:");
    print_product(A, B, C_zorder, rows, columns);

    // Free matrices
    free_matrix(rows, A);
    free_matrix(rows, B);
    free_matrix(rows, C_rows);
    free_matrix(rows, C_columns);
    free_matrix(rows, C_zorder);

    return 0;
}