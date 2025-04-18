import csv
from collections import defaultdict

def process_file(input_file):
    row_col_data = {}
    zorder_data = defaultdict(list)

    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile, delimiter=';')

        for row in reader:
            if not row['Matrix size']:
                continue
            
            row['Row-major order (s)'] = row['Row-major order (s)'].replace('.', ',') if row['Row-major order (s)'] else '0,000000'
            row['Column-major order (s)'] = row['Column-major order (s)'].replace('.', ',') if row['Column-major order (s)'] else '0,000000'
            row['Z order (s)'] = row['Z order (s)'].replace('.', ',') if row['Z order (s)'] else '0,000000'

            matrix_size = row['Matrix size']
            phase = row['Phase']

            if (matrix_size, phase) not in row_col_data:
                row_col_data[(matrix_size, phase)] = {
                    'Matrix size': matrix_size,
                    'Phase': phase,
                    'Row Time (s)': row['Row-major order (s)'],
                    'Col Time (s)': row['Column-major order (s)']
                }

            zorder_row = {
                'Matrix size': matrix_size,
                'Block size': row['Block size'],
                'Phase': phase,
                'Zorder Time (s)': row['Z order (s)']
            }
            zorder_data[phase].append(zorder_row)

    for phase, data in zorder_data.items():
        zorder_file = f'zorder_phase_{phase}.csv'
        with open(zorder_file, 'w', newline='') as outfile:
            fieldnames = ['Matrix size', 'Block size', 'Phase', 'Zorder Time (s)']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(data)

    row_col_file = 'row_col_phase_1.csv'
    with open(row_col_file, 'w', newline='') as outfile:
        fieldnames = ['Matrix size', 'Phase', 'Row Time (s)', 'Col Time (s)']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(row_col_data.values())

input_file = '1.log'

process_file(input_file)