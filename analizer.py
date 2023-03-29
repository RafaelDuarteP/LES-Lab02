import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('dados-repo.csv')

#removendo os dados vazios
df = df.loc[df['visited'] == True]
df = df.dropna(subset=['dit'])

x_axis = ['stars', 'age', 'releases', 'loc']
y_axis = ['dit', 'cbo', 'lcom']

for x in x_axis:
    for y in y_axis:
        print('Relação', x, y)
        sns.pairplot(data=df, y_vars=y, x_vars=x, kind="reg", height=10)
        plt.show()
        pd.plotting.scatter_matrix(df[[x, y]], diagonal='kde')
        plt.show()
    cols = [x] + y_axis
    corr = df[cols].corr('spearman')
    print(corr)
    plt.matshow(corr)
    plt.xticks(range(len(cols)), cols)
    plt.yticks(range(len(cols)), cols)
    plt.colorbar()
    plt.show()