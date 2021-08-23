file_1 = open('sfc_reqs_sfc_by_len.csv')
file_2 = open('hon_sfc_by_len_rules.csv')

for line in file_2:
    file_1.write(line)

file_1.close()
file_2.close()