#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "functions.h"

void printMatrix(int rows, int columns, int **matrix)
{
    for (int i = 0; i < rows; i++)
    {
        printf("| ");
        for (int j = 0; j < columns; j++)
        {
            printf("%d ", matrix[i][j]);
        }
        printf("|\n");
    }
    printf("\n");
}

void printProduct(int **A, int **B, int **C, int rows, int columns)
{
    printf("\n");

    for (int i = 0; i < rows; i++)
    {
        printf("|");

        for (int j = 0; j < columns; j++)
            printf("%2d ", A[i][j]);

        printf("|");

        if (i == rows / 2)
            printf(" X ");
        else
            printf("   ");

        printf("|");

        for (int j = 0; j < columns; j++)
            printf("%2d ", B[i][j]);

        printf("|");

        if (i == rows / 2)
            printf(" = ");
        else
            printf("   ");

        printf("|");

        for (int j = 0; j < columns; j++)
            printf("%4d ", C[i][j]);

        printf("|\n");
    }
}

void measureTime(int rows, int columns, int **A, int **B, int **C, void (*function)(int, int, int **, int **, int **))
{
    clock_t start, end;

    start = clock();
    function(rows, columns, A, B, C);
    end = clock();

    printf("Time: %f seconds\n", (double)(end - start) / CLOCKS_PER_SEC);
}