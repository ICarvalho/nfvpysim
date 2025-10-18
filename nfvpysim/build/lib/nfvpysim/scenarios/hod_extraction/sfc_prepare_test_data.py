import csv

input_file = '/home/vitor/PycharmProjects/nfvpysim/nfvpysim/scenarios/hon_sfc_by_len_test_data.csv'
output_file = '/home/vitor/PycharmProjects/nfvpysim/nfvpysim/nfvpysim/scenarios/sfc_test_data.csv'


cols_to_remove = [0] # Column indexes to be removed (starts at 0)

cols_to_remove = sorted(cols_to_remove, reverse=True) # Reverse so we remove from the end first
row_count = 0 # Current amount of rows processed

with open(input_file, "r") as source:
    reader = csv.reader(source)
    with open(output_file, "w", newline='') as result:
        writer = csv.writer(result)
        for row in reader:
            row_count += 1
            print('\r{0}'.format(row_count), end='') # Print rows processed
            for col_index in cols_to_remove:
                del row[col_index]
            writer.writerow(row)
