import csv
from collections import defaultdict

def process_file(input_file):
    row_col_data = defaultdict(lambda: defaultdict(dict))
    zorder_data = defaultdict(list)

    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile, delimiter=';')

        for row in reader:
            time_value = row.get('Time(s)', '')
            if time_value:
                row['Time(s)'] = time_value.replace('.', ',')
            else:
                row['Time(s)'] = '0,000000'

            phase = row['Phase']

            if row['Algorithm'] in ['row', 'col']:
                matrix_size = row['Matrix size']
                if matrix_size not in row_col_data[phase]:
                    row_col_data[phase][matrix_size] = {'Matrix size': matrix_size, 'Phase': phase, 'Row Time (s)': '', 'Col Time (s)': ''}
                if row['Algorithm'] == 'row':
                    row_col_data[phase][matrix_size]['Row Time (s)'] = row['Time(s)']
                elif row['Algorithm'] == 'col':
                    row_col_data[phase][matrix_size]['Col Time (s)'] = row['Time(s)']
            elif row['Algorithm'] == 'zor':
                zorder_row = {
                    'Matrix size': row['Matrix size'],
                    'Block size': row['Block size'],
                    'Phase': phase,
                    'Zorder Time (s)': row['Time(s)']
                }
                zorder_data[phase].append(zorder_row)

    for phase, data in row_col_data.items():
        row_col_file = f'row_col_phase_{phase}.csv'
        with open(row_col_file, 'w', newline='') as outfile:
            fieldnames = ['Matrix size', 'Phase', 'Row Time (s)', 'Col Time (s)']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(data.values())

    for phase, data in zorder_data.items():
        zorder_file = f'zorder_phase_{phase}.csv'
        with open(zorder_file, 'w', newline='') as outfile:
            fieldnames = ['Matrix size', 'Block size', 'Phase', 'Zorder Time (s)']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(data)

    print("Archivos separados por fase generados con éxito.")

input_file = '1.log'

process_file(input_file)