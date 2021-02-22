def get_test_data(input_file, output_file, start_line, end_line):
    for line in input_file.readlines()[start_line:(start_line + end_line)]:
        output_file.write(line)
    input_file.close()
    output_file.close()


input_file = open('/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/sfc_reqs_file.csv', 'r')
output_file = open('/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/sfc_reqs_test.csv', 'w')

a = get_test_data(input_file, output_file, 7000, 100000)

