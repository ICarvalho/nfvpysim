import pandas as pd
import csv

df = pd.read_csv('/home/igor/PycharmProjects/TESE/nfvpysim/nfvpysim/scenarios/hon_sfc_by_len_rules.csv', header=None, error_bad_lines=False, warn_bad_lines=False)

sorted_df = df.sort_values(0,  ascending=False)

sorted_df.to_csv('hon_sfc_by_len_sorted.csv', index=False)