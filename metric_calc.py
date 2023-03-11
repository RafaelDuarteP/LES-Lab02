import pandas as pd
from git import Repo
import os
import shutil
from git import RemoteProgress
from tqdm import tqdm


class CloneProgress(RemoteProgress):

    def __init__(self):
        super().__init__()
        self.pbar = tqdm()

    def update(self, op_code, cur_count, max_count=None, message=''):
        self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.refresh()


# correção de erros para deletar pastas
def onerror(func, path, exc_info):
    import stat
    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


ck = 'java -jar ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar repo false 0 false output-metrics\\'

# Mudar para dados-repo-1.csv ou  dados-repo-2.csv
csv = 'dados-repo-1.csv'
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
        print('começou', i)
        # cria a pasta de output e clona o repositório
        os.makedirs('./output-metrics')
        Repo.clone_from(row['url'], 'repo/', progress=CloneProgress())
        # calcula as métricas
        os.system(ck)
        metrics = pd.read_csv('output-metrics/class.csv')
        df.loc[i, 'loc'] = metrics['loc'].sum()
        df.loc[i, 'cbo'] = metrics['cbo'].median()
        df.loc[i, 'dit'] = metrics['dit'].median()
        df.loc[i, 'lcom'] = metrics['lcom'].median()
        # deleta as pastas
        shutil.rmtree(r'repo', onerror=onerror)
        shutil.rmtree(r'output-metrics', onerror=onerror)
        df.loc[i, 'visited'] = True
        df.to_csv(csv, index=False)  # salva os dados
        print('salvou', i)

df.to_csv(csv, index=False)  # salva novamente os dados

print('fim')