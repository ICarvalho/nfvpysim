import random

class RequestSfcByLen:

    @staticmethod
    def gen_sfc_by_len(sfc_len):
        sfc = []
        vnfs = [1, 2, 3, 4, 5, 6, 7, 8]
        len = 0
        while len < sfc_len:
            vnf = random.choice(vnfs)
            if vnf not in sfc:
                sfc.append(vnf)
                len += 1
        return sfc

class RequestRandomSfc:

    @staticmethod
    def select_random_sfc():
        services = [
            [1, 2],
            [4, 5],
            [6, 3],
            [4, 8],
            [5, 7],
            [1, 2, 3],
            [2, 3, 5],
            [1, 5, 4],
            [5, 2, 1],
            [3, 1, 7],
            [2, 3, 5, 6],
            [3, 2, 5, 8],
            [4, 1, 3, 6],
            [8, 5, 1, 4],
            [1, 8, 7, 2],
            [1, 8, 7, 6, 2],
            [5, 4, 6, 2, 3],
            [2, 3, 7, 8, 1],
            [3 ,5, 7, 8, 1],
            [1, 3, 5, 7, 8],
            [2, 3, 5, 6, 7, 8],
            [8, 4, 2, 1, 2, 3],
            [7, 8, 3, 5, 4, 1],
            [2, 3, 5, 6, 7, 8],
            [4, 3, 1, 2, 6, 7],
            [1, 3, 4, 2, 7, 8, 5],
            [4, 1, 2, 3, 8, 5, 6],
            [7, 8, 1, 3, 2, 5, 6],
            [1, 2, 7, 8, 4, 5, 3],
            [8, 1, 2, 4, 7, 3, 6],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [8, 7, 6, 5, 4, 3, 2, 1],
            [2, 8, 1, 6, 5, 4, 3, 7],
            [5, 6, 1, 4, 7, 3, 2, 8],
            [1, 7, 8, 6, 3, 2, 5, 4]

        ]
        return random.choice(services)


class RequestVarLenSfc:

    @staticmethod
    def var_len_seq_sfc():
        var_len_sfc = []
        sfcs = {1: 15,  # nat
                2: 25,  # fw
                3: 25,  # ids
                4: 20,  # wanopt
                5: 20,  # lb
                6: 25,  # encrypt
                7: 25,  # decrypts
                8: 30,  # dpi
                }
        sfc_len = random.randint(1, 8)
        sum_cpu = 0
        while sfc_len != 0:
            vnf, cpu = random.choice(list(sfcs.items()))
            if vnf not in var_len_sfc:
                var_len_sfc.append(vnf)
                sfc_len -= 1
                sum_cpu += cpu
                if sum_cpu > 100 or sfc_len == 0:
                    break
                elif sum_cpu <= 100 and sfc_len != 0:
                    sfc_len -= 1
        return var_len_sfc



