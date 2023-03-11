import pandas as pd
from git import Repo
import os
import shutil


# correção de erros para deletar pastas
def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.
    
    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


ck = 'java -jar ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar repo false 0 false output-metrics\\'

# Mudar para dados-repo-1.csv ou  dados-repo-2.csv
csv = 'dados-repo.csv'
df = pd.read_csv(csv)

# Verifica se tem o dado visited no csv, se não tiver cria com valor false
if 'visited' not in df.columns:
    df['visited'] = False

# verifica se existem as pastas de repo e output e deleta
if os.path.exists(r'output-metrics'):
    shutil.rmtree(r'output-metrics', onerror=onerror)
if os.path.exists(r'repo'):
    shutil.rmtree(r'repo', onerror=onerror)

# itera sobre os repositórios do csv
for i, row in df.iterrows():
    if not row['visited']:  # verifica se já foi calculado
        # cria a pasta de output e clona o repositório
        os.makedirs('./output-metrics')
        Repo.clone_from(row['url'], 'repo/')
        # calcula as métricas
        os.system(ck)
        metrics = pd.read_csv('output-metrics/class.csv')
        df.loc[i, 'loc'] = metrics['loc'].sum()
        df.loc[i, 'cbo'] = metrics['cbo'].median()
        df.loc[i, 'dit'] = metrics['dit'].median()
        df.loc[i, 'lcom'] = metrics['lcom'].median()
        df.loc[i, 'visited'] = True
        # deleta as pastas
        shutil.rmtree(r'repo', onerror=onerror)
        shutil.rmtree(r'output-metrics', onerror=onerror)
        df.to_csv(csv, index=False)  # salva os dados

df.to_csv(csv, index=False)  # salva novamente os dados

print('fim')