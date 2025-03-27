#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "mul_functions.h"

#define ROW_MAJOR_STR "Row-major order"
#define COLUMN_MAJOR_STR "Column-major order"
#define Z_ORDER_STR "Z order"

typedef struct
{
    double row_major_time;
    double column_major_time;
    double *zorder_times;
} Result;

int *calculate_block_sizes(int matrix_size, int *num_block_sizes)
{
    int *block_sizes = (int *)malloc(matrix_size * sizeof(int));
    if (block_sizes == NULL)
    {
        fprintf(stderr, "Error: Could not allocate memory for block sizes.\n");
        exit(1);
    }

    int count = 0;
    for (int i = 2; i < matrix_size; i++)
    {
        if (matrix_size % i == 0)
        {
            block_sizes[count++] = i;
        }
    }

    *num_block_sizes = count;

    return block_sizes;
}

void benchmark(int rows, int columns, int block_size, Result *result, int block_index)
{
    int **A, **B, **C_rows, **C_columns, **C_zorder;
    clock_t start, end;

    A = allocate_matrix(rows, columns);
    B = allocate_matrix(rows, columns);
    C_rows = allocate_matrix(rows, columns);
    C_columns = allocate_matrix(rows, columns);
    C_zorder = allocate_matrix(rows, columns);

    if (A == NULL || B == NULL || C_rows == NULL || C_columns == NULL || C_zorder == NULL)
    {
        fprintf(stderr, "Error: Could not allocate memory for matrices.\n");
        exit(1);
    }

    srand(time(NULL));
    generate_matrix(rows, columns, A);
    generate_matrix(rows, columns, B);
    fill_matrix(rows, columns, C_rows, 0);
    fill_matrix(rows, columns, C_columns, 0);
    fill_matrix(rows, columns, C_zorder, 0);

    // Row major benchmark
    start = clock();
    row_major_mul(rows, columns, A, B, C_rows);
    end = clock();
    result->row_major_time += (double)(end - start) / CLOCKS_PER_SEC;

    // Column major benchmark
    start = clock();
    column_major_mul(rows, columns, A, B, C_columns);
    end = clock();
    result->column_major_time += (double)(end - start) / CLOCKS_PER_SEC;

    // Z-order benchmark
    start = clock();
    zorder_mul(rows, columns, A, B, C_zorder, block_size);
    end = clock();
    result->zorder_times[block_index] += (double)(end - start) / CLOCKS_PER_SEC;

    free_matrix(rows, A);
    free_matrix(rows, B);
    free_matrix(rows, C_rows);
    free_matrix(rows, C_columns);
    free_matrix(rows, C_zorder);
}

void print_results(int matrix_size, int num_blocks, int *block_sizes, Result *result)
{
    for (int i = 0; i < num_blocks; i++)
    {
        printf("%d;%d;%.6f;%.6f;%.6f\n", matrix_size, block_sizes[i], result->row_major_time, result->column_major_time, result->zorder_times[i]);
    }
}

void run_benchmark(int matrix_sizes[], int size_count, int iterations)
{
    for (int i = 0; i < size_count; i++)
    {
        int matrix_size = matrix_sizes[i];
        int num_blocks;
        int *block_sizes = calculate_block_sizes(matrix_size, &num_blocks);

        Result result = {0.0, 0.0, (double *)malloc(num_blocks * sizeof(double))};
        for (int j = 0; j < num_blocks; j++)
        {
            result.zorder_times[j] = 0.0;
        }

        for (int j = 0; j < iterations; j++)
        {
            for (int k = 0; k < num_blocks; k++)
            {
                benchmark(matrix_size, matrix_size, block_sizes[k], &result, k);
            }
        }

        result.row_major_time /= iterations;
        result.column_major_time /= iterations;
        for (int k = 0; k < num_blocks; k++)
        {
            result.zorder_times[k] /= iterations;
        }
        print_results(matrix_size, num_blocks, block_sizes, &result);

        free(block_sizes);
        free(result.zorder_times);
    }
}

int main()
{
    int matrix_sizes[] = {4, 8, 16, 32, 64};
    int iterations = 10;

    printf("Matrix size;Block size;Row-major order (s);Column-major order (s);Z order (s)\n");

    run_benchmark(matrix_sizes, sizeof(matrix_sizes) / sizeof(matrix_sizes[0]), iterations);

    return 0;
}
