#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>
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

void benchmark(int matrix_size, int *block_sizes, int num_blocks, Result *result,
               int **A, int **B, int **C_rows, int **C_columns, int **C_zorder)
{
    clock_t start, end;

    // Initialize matrices with zeros
    fill_matrix(matrix_size, matrix_size, C_rows, 0);
    fill_matrix(matrix_size, matrix_size, C_columns, 0);

    // Row major benchmark
    start = clock();
    row_major_mul(matrix_size, matrix_size, A, B, C_rows);
    end = clock();
    result->row_major_time += (double)(end - start) / CLOCKS_PER_SEC;

    // Column major benchmark
    start = clock();
    column_major_mul(matrix_size, matrix_size, A, B, C_columns);
    end = clock();
    result->column_major_time += (double)(end - start) / CLOCKS_PER_SEC;

    // Check row major and column major results
    if (!check_matrices(matrix_size, C_rows, C_columns))
    {
        fprintf(stderr, "Error: Results do not match.\n");
        exit(1);
    }

    // Z-order benchmark
    for (int i = 0; i < num_blocks; i++)
    {
        // Initialize z-order matrix with zeros
        fill_matrix(matrix_size, matrix_size, C_zorder, 0);

        // Z-order multiplication
        start = clock();
        zorder_mul(matrix_size, matrix_size, A, B, C_zorder, block_sizes[i]);
        end = clock();
        result->zorder_times[i] += (double)(end - start) / CLOCKS_PER_SEC;

        // Check z-order results
        if (!check_matrices(matrix_size, C_rows, C_zorder))
        {
            fprintf(stderr, "Error: Results do not match for z-order multiplication.\n");
            exit(1);
        }
    }
}

void print_results(int matrix_size, int num_blocks, int *block_sizes, Result *result)
{
    for (int i = 0; i < num_blocks; i++)
    {
        printf("%d;%d;%f;%f;%f\n",
               matrix_size, block_sizes[i],
               result->row_major_time,
               result->column_major_time,
               result->zorder_times[i]);
    }
}

Result init_results(int num_blocks)
{
    Result result = {0.0, 0.0, (double *)malloc(num_blocks * sizeof(double))};
    if (result.zorder_times == NULL)
    {
        fprintf(stderr, "Error: Could not allocate memory for z-order times.\n");
        exit(1);
    }

    for (int i = 0; i < num_blocks; i++)
    {
        result.zorder_times[i] = 0.0;
    }

    return result;
}

void calc_results(Result *result, int iterations, int num_blocks)
{
    result->row_major_time /= iterations;
    result->column_major_time /= iterations;
    for (int i = 0; i < num_blocks; i++)
    {
        result->zorder_times[i] /= iterations;
    }
}

void run_benchmark(int matrix_sizes[], int size_count, int iterations)
{
    for (int i = 0; i < size_count; i++)
    {
        int **A = NULL, **B = NULL, **C_rows = NULL, **C_columns = NULL, **C_zorder = NULL;
        int matrix_size = matrix_sizes[i];
        int num_blocks;

        int *block_sizes = calculate_block_sizes(matrix_size, &num_blocks);
        Result result = init_results(num_blocks);
        init_matrices(matrix_size, &A, &B, &C_rows, &C_columns, &C_zorder);

        for (int j = 0; j < iterations; j++)
        {
            benchmark(matrix_size, block_sizes, num_blocks, &result, A, B, C_rows, C_columns, C_zorder);
        }

        calc_results(&result, iterations, num_blocks);
        print_results(matrix_size, num_blocks, block_sizes, &result);

        free(block_sizes);
        free(result.zorder_times);
        free_matrices(matrix_size, A, B, C_rows, C_columns, C_zorder);
    }
}

int main()
{
    clock_t start, end;
    int matrix_sizes[] = {512};
    int iterations = 3;

    start = clock();
    printf("Matrix size;Block size;Row-major order (s);Column-major order (s);Z order (s)\n");
    run_benchmark(matrix_sizes, sizeof(matrix_sizes) / sizeof(matrix_sizes[0]), iterations);
    end = clock();

    printf("\nTotal execution time: %f seconds\n", (double)(end - start) / CLOCKS_PER_SEC);

    return 0;
}
