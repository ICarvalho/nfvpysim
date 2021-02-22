from nfvpysim.scenarios.requests import RequestSfcByLen
import csv

class GenerateTraceDrivenRequests:

    @staticmethod
    def gen_sfc_reqs(n_reqs, sfc_len):
        with open("sfc_reqs_file.csv", 'w', newline='\n') as f:
            writer = csv.writer(f)
            for i in range(1, n_reqs + 1):
                req = RequestSfcByLen()
                sfc = req.gen_sfc_by_len(sfc_len)
                file_lines = [str(sfc)[1:-1], '\n']
                f.writelines(file_lines)
            f.close()


