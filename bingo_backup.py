import pandas as pd
import random
import bingo_df
import random


df = bingo_df.get_latest_bingo()

df['rank'] = df['rank'].astype(int)


df1 = df[df['rank']==1]
df2 = df[df['rank']==2]
df3 = df[df['rank']==3]



goals = []
for i in range(5):
    
    df3t = df3.sample(1)
    df2t = df2.sample(2)
    df1t = df1.sample(2)
    
    df1 = df1[~df1.index.isin(df1t.index)]
    df2 = df2[~df2.index.isin(df2t.index)]
    df3 = df3[~df3.index.isin(df3t.index)]
    
    dft = list(df1t.append(df2t).append(df3t)['goal'])
    
    random.shuffle(dft)    
    goals.append(dft)
    
    
    





for i in goals:
    for i2 in i:
        print(i2)