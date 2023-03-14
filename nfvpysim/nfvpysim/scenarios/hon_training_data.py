def get_training_data(input_file, output_file, start_line, end_line):
    for line in input_file.readlines()[start_line:(start_line + end_line)]:
        output_file.write(line)
    input_file.close()
    output_file.close()


input_file = open('/home/vitor/PycharmProjects/nfvpysim/nfvpysim/nfvpysim/scenarios/sfc_reqs_random_sfc.csv', 'r')
output_file = open('/home/vitor/PycharmProjects/nfvpysim/nfvpysim/nfvpysim/scenarios/hon_random_sfc_training_data.csv', 'w')

# input_file = open('/home/vitor/PycharmProjects/nfvpysim/nfvpysim/scenarios/sfc_reqs_sfc_var_len.csv', 'r')
# output_file = open('/home/vitor/PycharmProjects/nfvpysim/nfvpysim/scenarios/hon_sfc_var_len_training_data_1000_000.csv', 'w')

# input_file = open('/home/vitor/PycharmProjects/nfvpysim/nfvpysim/scenarios/sfc_reqs_sfc_by_len.csv', 'r')
# output_file = open('/home/vitor/PycharmProjects/nfvpysim/nfvpysim/scenarios/hon_sfc_by_len_training_data.csv', 'w')


start_train_index = 0
end_train_index = 1 * 10 ** 6
get_training_data(input_file, output_file, start_train_index, end_train_index)
