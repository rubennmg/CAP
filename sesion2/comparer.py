from multiply_matrices import run_phase_1

if __name__ == "__main__":
    matrix_sizes = [16]
    block_sizes = [2]
    iterations = 1
    results = {}
    
    row_major_str = "Row-major order"
    column_major_str = "Column-major order"
    z_order_str = "Z order"

    for matrix_size in matrix_sizes:
        if matrix_size not in results:
            results[matrix_size] = {
                row_major_str: 0.0,
                column_major_str: 0.0,
                z_order_str: {block_size: 0.0 for block_size in block_sizes}
            }

        for block_size in block_sizes:
            for _ in range(iterations):
                current_result = run_phase_1(matrix_size, block_size)

                results[matrix_size][row_major_str] += current_result[row_major_str]
                results[matrix_size][column_major_str] += current_result[column_major_str]
                
                for bz, time in current_result[z_order_str].items():
                    results[matrix_size][z_order_str][bz] += time

    # Encabezado de la tabla
    print("Matrix size;Block-size;Row-major order (s);Column-major order (s);Z order (s)")             
   
    # Imprimir resultados
    for matrix_size in matrix_sizes:
        row_major_avg = results[matrix_size][row_major_str] / iterations
        column_major_avg = results[matrix_size][column_major_str] / iterations

        for block_size, time in results[matrix_size][z_order_str].items():
            zorder_avg = time / iterations
            print(f"{matrix_size};{block_size};{row_major_avg:.6f};{column_major_avg:.6f};{zorder_avg:.6f}")