import pandas as pd
from git import Repo
import os
import shutil


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

df = pd.read_csv('dados-repo.csv')

if 'visited' not in df.columns:
    df['visited'] = False

for i in range(5):
    row = df.loc[i]
    if not row['visited']:
        os.makedirs('./output-metrics')
        Repo.clone_from(row['url'], 'repo/')
        os.system(ck)
        metrics = pd.read_csv('output-metrics/class.csv')
        df.loc[i, 'loc'] = metrics['loc'].sum()
        df.loc[i, 'cbo'] = metrics['cbo'].median()
        df.loc[i, 'dit'] = metrics['dit'].median()
        df.loc[i, 'lcom'] = metrics['lcom'].median()
        df.loc[i, 'visited'] = True
        shutil.rmtree(r'repo', onerror=onerror)
        shutil.rmtree(r'output-metrics', onerror=onerror)
        df.to_csv('dados-repo.csv', index=False)

df.to_csv('dados-repo.csv', index=False)

print('fim')