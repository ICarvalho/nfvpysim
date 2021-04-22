import pandas as pd

data = { 'name': ['AA', 'IBM', 'GOOGLE'],
         'data': ['22/01/65', '11/05/86', '30/12/66'],
         'shares': [100, 30 ,90],
         'prince': [10, 20, 30]

}

df = pd.DataFrame(data)
df['foo'] = None
print(df['shares'])