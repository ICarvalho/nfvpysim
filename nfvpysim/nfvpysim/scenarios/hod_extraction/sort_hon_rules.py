import pandas as pd
import csv

df = pd.read_csv('/home/igor/PycharmProjects/nfvpysim/nfvpysim/nfvpysim/scenarios/hod_extraction/hon_random_sfc_rules.csv', header=None)

sorted_df = df.sort_values(1,  ascending=False)

sorted_df.to_csv('hon_random_sfc_sorted.csv', index=False)