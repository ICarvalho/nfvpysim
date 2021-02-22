import csv
from operator import itemgetter

reader = csv.reader(open("sfc_reqs_training_rules.csv"), delimiter=",")
for line in sorted(reader, key=itemgetter(0)):
    print(line)
