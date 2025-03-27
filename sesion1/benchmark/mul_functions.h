#ifndef MUL_FUNCTIONS_H
#define MUL_FUNCTIONS_H

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int **allocate_matrix(int rows, int columns);
void free_matrix(int rows, int **matrix);
void generate_matrix(int rows, int columns, int **matrix);
void fill_matrix(int rows, int columns, int **matrix, int value);
void row_major_mul(int rows, int columns, int **A, int **B, int **C);
void column_major_mul(int rows, int columns, int **A, int **B, int **C);
void zorder_mul(int rows, int columns, int **A, int **B, int **C, int block_size);

#endif
