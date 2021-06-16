from itertools import permutations
import csv
import pandas as pd




file = open('sfc_seq.csv', 'w', newline='')
with file:
    for c in list(permutations([0, 1, 2, 3, 4, 5, 6, 7], r=8)):
        write = csv.writer(file)
        write.writerow(c)
    file.close()


df = pd.read_csv('sfc_seq.csv')
df.to_csv('sfc_seq_indexed.csv', index=True, header=None)