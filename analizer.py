from typing import Type
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

df =  pd.read_csv('dados-repo.csv')

#removendo os dados vazios
df = df.loc[df['visited'] == True]
df = df.dropna(subset=['dit'])

x_axis = ['stars', 'age', 'releases', 'loc']
y_axis = ['dit', 'cbo', 'lcom']

for x in x_axis:
    for y in y_axis:
        sns.pairplot(data=df, y_vars=y, x_vars=x, kind="reg",height=10)
        plt.show()
        