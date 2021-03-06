import pandas as pd

df = pd.read_csv('/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/hon_sfc_by_len_rules.csv', header=None)

sorted_df = df.sort_values(1, ascending=False)

sorted_df.to_csv('hon_sfc_by_len_sorted.csv', index=False)