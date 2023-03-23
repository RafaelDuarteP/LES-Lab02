from typing import Type
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

df =  pd.read_csv('dados-repo.csv')

df = df.loc[df['visited'] == True]
df = df.dropna(subset=['dit'])

sns.pairplot(data=df, y_vars='stars', x_vars='lcom', kind="reg",height=10)
plt.show()