import csv

from nfvpysim.scenarios.requests import *


class GenerateTraceDrivenRequests:

    @staticmethod
    def gen_sfc_by_len(n_reqs, sfc_lens):
        with open("sfc_reqs_sfc_by_len.csv", 'w', newline='\n') as f:
            writer = csv.writer(f)
            for i in range(1, n_reqs + 1):
                for j in sfc_lens:
                    req = RequestSfcByLen()
                    sfc = req.gen_sfc_by_len(j)
                    file_lines = [str(i),',', str(sfc)[1:-1], '\n']
                    f.writelines(file_lines)
                    continue

        f.close()


    @staticmethod
    def gen_random_sfc(n_reqs):
        with open("sfc_reqs_random_sfc.csv" , 'w', newline='\n') as f:
            writer = csv.writer(f)
            for i in range(1, n_reqs + 1):
                req = RequestRandomSfc()
                sfc = req.select_random_sfc()
                file_lines = [str(i),',',str(sfc)[1:-1],'\n']
                f.writelines(file_lines)
            f.close()

    @staticmethod
    def gen_var_len_sfc(n_reqs):
        with open("sfc_reqs_sfc_var_len.csv", 'w', newline='\n') as f:
            writer = csv.writer(f)
            for i in range(1, n_reqs + 1):
                req = RequestVarLenSfc()
                sfc = req.var_len_seq_sfc()
                file_lines = [str(i),',',str(sfc)[1:-1], '\n']
                f.writelines(file_lines)
            f.close()



#req_sfc_by_len = GenerateTraceDrivenRequests()
#req_sfc_by_len.gen_sfc_by_len(10 ** 2, [2,3])


req_rand_sfc = GenerateTraceDrivenRequests()
req_rand_sfc.gen_random_sfc(1 * 10 ** 6)

#req_var_len_sfc = GenerateTraceDrivenRequests()
#req_var_len_sfc.gen_var_len_sfc(1 * 10 ** 6)
