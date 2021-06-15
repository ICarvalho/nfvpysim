from itertools import permutations
import csv


file = open('sfc_seq.csv', 'w', newline='')
with file:
    for c in list(permutations([0, 1, 2, 3, 4, 5, 6, 7], r=4)):
        write = csv.writer(file)
        write.writerow(c)
