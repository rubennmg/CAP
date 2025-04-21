#include "mul_functions.h"

#define ROW_MAJOR_STR "Row-major order"
#define COLUMN_MAJOR_STR "Column-major order"
#define Z_ORDER_STR "Z order"

/**
 * Struct to hold the results of the benchmark
 */
typedef struct
{
    double row_major_time;    /* Execution time with row major algorithm */
    double column_major_time; /* Execution time with column major algorithm */
    double *zorder_times;     /* Execution time with z-order algorithm */
} Result;

/**
 * Prints the results of the benchmark
 * @param matrix_size Size of the matrices
 * @param num_blocks Number of blocks for z-order algorithm
 * @param block_sizes Array of block sizes
 * @param result Pointer to the result struct
 */
void print_results(int matrix_size, int num_blocks, int *block_sizes, Result *result)
{
    printf("%d;%s;%s;%f\n", matrix_size, "-", "row", result->row_major_time);
    printf("%d;%s;%s;%f\n", matrix_size, "-", "col", result->column_major_time);
    for (int i = 0; i < num_blocks; i++)
    {
        printf("%d;%d;%s;%f\n", matrix_size, block_sizes[i], "zor", result->zorder_times[i]);
    }
}

/**
 * Calculates the average execution times for the benchmark
 * @param result Pointer to the result struct
 * @param iterations Number of iterations
 * @param num_blocks Number of blocks for z-order algorithm
 */
void calc_results(Result *result, int iterations, int num_blocks)
{
    result->row_major_time /= iterations;
    result->column_major_time /= iterations;
    for (int i = 0; i < num_blocks; i++)
    {
        result->zorder_times[i] /= iterations;
    }
}

/**
 * Runs the benchmark for the given matrices and block sizes
 * It fills the matrices with zeros, runs the row major, column major, and z-order algorithms,
 * checks the results, and stores the execution times
 * @param matrix_size Size of the matrices
 * @param block_sizes Array of block sizes
 * @param num_blocks Number of blocks for z-order algorithm
 * @param result Pointer to the result struct
 * @param A First matrix
 * @param B Second matrix
 * @param C_rows Result matrix for row major algorithm
 * @param C_columns Result matrix for column major algorithm
 * @param C_zorder Result matrix for z-order algorithm
 */
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

/**
 * Initializes the result struct
 * @param num_blocks Number of blocks for z-order algorithm
 * @return Initialized result struct
 */
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

/**
 * Calculates the block sizes for the given matrix size
 * It is used to determine the block sizes for the z-order algorithm
 * @param matrix_size Size of the matrix
 * @param num_block_sizes Pointer to the number of block sizes
 * @return Array of block sizes
 */
int *calculate_block_sizes(int matrix_size, int *num_block_sizes)
{
    int *block_sizes = (int *)malloc(matrix_size * sizeof(int));
    if (block_sizes == NULL)
    {
        fprintf(stderr, "Error: Could not allocate memory for block sizes.\n");
        exit(1);
    }

    int count = 0;
    block_sizes[count++] = 1;
    for (int i = 2; i < matrix_size; i++)
    {
        if (matrix_size % i == 0)
        {
            block_sizes[count++] = i;
        }
    }
    block_sizes[count++] = matrix_size;

    *num_block_sizes = count;

    return block_sizes;
}

/**
 * Runs the benchmark for the given matrix sizes and iterations
 * It initializes the matrices, runs the benchmark, and prints the results
 * @param matrix_sizes Array of matrix sizes
 * @param size_count Number of matrix sizes
 * @param iterations Number of iterations to run the benchmark
 */
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

/**
 * Main function
 */
int main()
{
    clock_t start, end;
    int matrix_sizes[] = {2, 4, 8, 16, 32, 64, 128, 256, 398, 512, 636, 774, 892, 1024, 1152, 1280, 1408, 1536};
    int iterations = 32;

    start = clock();
    printf("Matrix size;Block size;Algorithm;Time(s)\n");
    run_benchmark(matrix_sizes, sizeof(matrix_sizes) / sizeof(matrix_sizes[0]), iterations);
    end = clock();

    printf("\nTotal execution time: %f seconds\n", (double)(end - start) / CLOCKS_PER_SEC);
    printf("Iterations: %d\n", iterations);
    printf("Benchmark completed.\n");

    return 0;
}
