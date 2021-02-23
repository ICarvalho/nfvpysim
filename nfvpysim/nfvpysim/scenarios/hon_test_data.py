def get_test_data(input_file, output_file, start_line, end_line):
    for line in input_file.readlines()[start_line:(start_line + end_line)]:
        output_file.write(line)
    input_file.close()
    output_file.close()




#input_file = open('/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/sfc_reqs_sfc_by_len.csv', 'r')
#output_file = open('/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/hon_sfc_by_len_training_data.csv', 'w')

input_file = open('/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/sfc_reqs_random_sfc.csv', 'r')
output_file = open('/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/hon_random_sfc_test_data.csv', 'w')

#input_file = open('/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/sfc_reqs_sfc_var_len.csv', 'r')
#output_file = open('/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/hon_sfc_var_len_training_data.csv', 'w')
a = get_test_data(input_file, output_file, 50000, 100000)

