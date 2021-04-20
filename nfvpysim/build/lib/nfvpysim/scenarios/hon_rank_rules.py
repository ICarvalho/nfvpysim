import csv
from operator import itemgetter

reader = csv.reader(open("hon_random_sfc_rules.csv"), delimiter=",")
for line in sorted(reader, key=itemgetter(0)):
    print(line)
