import random

class RequestSfcByLen:

    @staticmethod
    def gen_sfc_by_len(sfc_len):
        sfc = []
        vnfs = [0, 1, 2, 3, 4, 5, 6, 7]
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
        services = {

            1: {'sfc': [0, 1, 2], 'delay': 100},
            2: {'sfc': [0, 4, 3], 'delay': 100},
            3: {'sfc': [3, 7, 2], 'delay': 100},
            4: {'sfc': [1, 2, 4, 5], 'delay': 200},
            5: {'sfc': [2, 1, 4, 7], 'delay': 200},
            6: {'sfc': [2, 4, 5, 6], 'delay': 200},
            7: {'sfc': [3, 6, 7, 2], 'delay': 200},
            8: {'sfc': [1, 2, 6, 7], 'delay': 200},
            9: {'sfc': [2, 4, 1, 5, 3], 'delay': 350},
            10: {'sfc': [4, 3, 5, 1, 2], 'delay': 350},
            11: {'sfc': [4, 3, 5, 6, 7], 'delay': 350},
            12: {'sfc': [0, 4, 3, 5, 6], 'delay': 350},
            13: {'sfc': [2, 4, 5, 6, 7], 'delay': 350},
            14: {'sfc': [2, 4, 5, 6, 7, 3], 'delay': 400},
            15: {'sfc': [1, 3, 5, 4, 7, 2], 'delay': 420},
            16: {'sfc': [2, 1, 4, 3, 7, 8], 'delay': 420},
            17: {'sfc': [4, 3, 5, 6, 0, 1, 2], 'delay': 450},
            18: {'sfc': [1, 2, 6, 3, 5, 4, 7], 'delay': 450},
            19: {'sfc': [0, 1, 2, 4, 3, 7, 5, 6], 'delay': 500},
            20: {'sfc': [3, 0, 1, 4, 5, 7, 6, 2], 'delay': 500},

        }
        key = random.choice(list(services.keys()))
        return list(services[key]['sfc'])


class RequestVarLenSfc:

    @staticmethod
    def var_len_seq_sfc():
        var_len_sfc = []
        sfcs = {0: 15,  # nat
                1: 25,  # fw
                2: 25,  # ids
                3: 20,  # wanopt
                4: 20,  # lb
                5: 25,  # encrypt
                6: 25,  # decrypts
                7: 30  # dpi
                }


        sfc_len = random.randint(2, 8)
        while sfc_len != 0:
            vnf = random.choice(list(sfcs.keys()))
            if vnf not in var_len_sfc:
                var_len_sfc.append(vnf)
                sfc_len -= 1
                if sfc_len == 0:
                    break

        return var_len_sfc





"""

    services = [[1, 2],  
                    [4, 5],  # [wanopt - lb]​
                    [1, 2, 3],  # [nat - fw - ids]​
                    [2, 3, 5],  # [fw - ids - lb]​
                    [1, 5, 4],  # [nat - lb - wanopt]​
                    [5, 2, 1],  # [lb - fw - nat]​
                    [2, 3, 5, 6],  # [fw - ids - lb - encrypt]​
                    [3, 2, 5, 8],  # [ids - fw - lb - wanopt]​
                    [5, 4, 6, 2, 3],
                    [3, 5, 6, 7, 8],
                     ]# [lb - wanopt - encrypt - fw - ids]​
        return random.choice(services)
        
        
        
    
        services = [
             [1, 2],
             [4, 5],
             [1, 2, 3],
             [2, 3, 5],
             [1, 5, 4],
             [5, 2, 1],
             [2, 3, 5, 6],
             [3, 2, 5, 8],
             [5, 4, 6, 2, 3],
             [3, 5, 6, 7, 8],
        ]    
        
    
    
    

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

    """