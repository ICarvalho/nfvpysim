from nfvpysim.scenarios.requests import *
import csv

class GenerateTraceDrivenRequests:

    @staticmethod
    def gen_sfc_by_len(n_reqs, sfc_len):
        with open("sfc_reqs_file.csv", 'w', newline='\n') as f:
            writer = csv.writer(f)
            for i in range(1, n_reqs + 1):
                req = RequestSfcByLen()
                sfc = req.gen_sfc_by_len(sfc_len)
                file_lines = [str(i), ',',  str(sfc)[1:-1], '\n']
                f.writelines(file_lines)
            f.close()


    @staticmethod
    def gen_random_sfc(n_reqs):
        with open("sfc_reqs_random_sfc.csv" , 'w', newline='\n') as f:
            writer = csv.writer(f)
            for i in range(1, n_reqs + 1):
                req = RequestRandomSfc()
                sfc = req.select_random_sfc()
                file_lines = [str(i), ',', str(sfc)[1:-1], '\n']
                f.writelines(file_lines)
            f.close()

    @staticmethod
    def gen_var_len_sfc(n_reqs):
        with open("sfc_reqs_var_len_sfc.csv", 'w', newline='\n') as f:
            writer = csv.writer(f)
            for i in range(1, n_reqs + 1):
                req = RequestVarLenSfc()
                sfc = req.var_len_seq_sfc()
                file_lines = [str(i), ',', str(sfc)[1:-1], '\n']
                f.writelines(file_lines)
            f.close()



req = GenerateTraceDrivenRequests()
sfc = req.gen_sfc_by_len(10**5, 4)
