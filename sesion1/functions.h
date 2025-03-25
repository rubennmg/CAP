void printMatrix(int rows, int columns, int **matrix);
void printProduct(int **A, int **B, int **C, int rows, int columns);
void measureTime(int rows, int columns, int **A, int **B, int **C, void (*function)(int, int, int **, int **, int **));