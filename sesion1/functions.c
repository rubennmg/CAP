#include "functions.h"

void print_matrix(int rows, int columns, int **matrix)
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

void print_product(int **A, int **B, int **C, int rows, int columns)
{
    if (rows > 10 || columns > 10)
    {
        printf("Matrices are too big to be printed\n");
        return;
    }

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

void check_err(int **matrix)
{
    if (matrix == NULL)
    {
        fprintf(stderr, "Error: Could not allocate.\n");
        exit(1);
    }
}