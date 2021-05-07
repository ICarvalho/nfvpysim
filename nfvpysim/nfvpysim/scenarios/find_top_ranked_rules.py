import pandas as pd

#file = "hon_sfc_var_len_rules.csv"
file = "hon_sfc_by_len_rules.csv"
#file = "hon_random_sfc_rules.csv"
df = pd.read_csv(file,  header=None, delimiter=',', names=list(range(2)))
print(df.nlargest(50, columns=[1]))