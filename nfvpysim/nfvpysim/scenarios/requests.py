import random

class RequestSfcByLen:

    @staticmethod
    def gen_sfc_by_len(sfc_len):
        vnfs = [1, 2, 3, 4, 5, 6, 7, 8]
        sfc = []
        for i in range(0, sfc_len):
            vnf = random.choice(vnfs)
            if vnf not in sfc:
                sfc.append(vnf)

        return sfc

class RequestRandomSfc:

    @staticmethod
    def select_random_sfc():
        services = [
            [1, 2],  # [nat - fw]
            [4, 5],  # [wanopt - lb]
            [1, 2, 3],  # [nat - fw - ids]
            [2, 3, 5],  # [fw - ids - lb]
            [1, 5, 4],  # [nat - lb - wanopt]
            [5, 2, 1],  # [lb - fw - nat]
            [2, 3, 5, 6],  # [fw - ids - lb - encrypt]
            [3, 2, 5, 8],  # [ids - fw - lb - wanopt]
            [5, 4, 6, 2, 3],  # [lb - wanopt - encrypt - fw - ids]
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




