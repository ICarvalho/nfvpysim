def get_test_data(input_file, output_file, start_line, end_line):
    for line in input_file.readlines()[start_line:(start_line + end_line)]:
        output_file.write(line)
    input_file.close()
    output_file.close()


input_file = open('/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/sfc_reqs_file.csv', 'r')
output_file = open('/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/hon_test_data.csv', 'w')

a = get_test_data(input_file, output_file, 50000, 100000)

