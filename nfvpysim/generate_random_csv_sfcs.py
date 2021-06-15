import csv
import random

file = open('sfc_seq_shuffled.csv', 'r', newline='')
output_file = 'sfc_seq_len_5_test.csv'
with file:
    csv_reader = csv.reader(file)
    sfcs = list(csv_reader)
    with open(output_file, "w", newline='') as result:
        writer = csv.writer(result)
        for i in range(1, 10 **4 + 1):
            random_question = random.choice(sfcs)
            writer.writerow([random_question])
            print(random_question)
