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

d = {}
for index, item in enumerate(services):
    #print(index, item)
    d[index] = item
    print(d)