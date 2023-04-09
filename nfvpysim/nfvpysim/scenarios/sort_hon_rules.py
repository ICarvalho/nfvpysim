import pandas as pd
import csv

df = pd.read_csv('/home/vitor/PycharmProjects/nfvpysim/nfvpysim/nfvpysim/scenarios/hon_random_sfc_rules.csv', header=None, error_bad_lines=False, warn_bad_lines=False)

sorted_df = df.sort_values(1,  ascending=False)

sorted_df.to_csv('hon_random_sfc_sorted.csv', index=False)