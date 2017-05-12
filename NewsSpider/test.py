import pandas as pd

df = pd.read_csv('NewsList_20170512.csv')
print(df['url'].values.tolist())
