import csv

def process_file(input_file, row_col_file, zorder_file):
    with open(input_file, 'r') as infile:
        reader = csv.DictReader(infile, delimiter=';')
        row_col_data = {}
        zorder_data = []

        for row in reader:
            time_value = row.get('Time(s)', '')
            if time_value:
                row['Time(s)'] = time_value.replace('.', ',')
            else:
                row['Time(s)'] = '0,000000'

            if row['Algorithm'] in ['row', 'col']:
                matrix_size = row['Matrix size']
                if matrix_size not in row_col_data:
                    row_col_data[matrix_size] = {'Matrix size': matrix_size, 'Row Time(s)': '', 'Col Time(s)': ''}
                if row['Algorithm'] == 'row':
                    row_col_data[matrix_size]['Row Time(s)'] = row['Time(s)']
                elif row['Algorithm'] == 'col':
                    row_col_data[matrix_size]['Col Time(s)'] = row['Time(s)']
            elif row['Algorithm'] == 'zor':
                zorder_row = {
                    'Matrix size': row['Matrix size'],
                    'Block size': row['Block size'],
                    'Zorder Time(s)': row['Time(s)']
                }
                zorder_data.append(zorder_row)

        with open(row_col_file, 'w', newline='') as outfile:
            fieldnames = ['Matrix size', 'Row Time(s)', 'Col Time(s)']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(row_col_data.values())

        with open(zorder_file, 'w', newline='') as outfile:
            fieldnames = ['Matrix size', 'Block size', 'Zorder Time(s)']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(zorder_data)

input_file = '3.log'
row_col_file = 'row_col_3.csv'
zorder_file = 'zorder_3.csv'

process_file(input_file, row_col_file, zorder_file)