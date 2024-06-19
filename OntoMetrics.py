import pandas as pd
import subprocess
import urllib.request
import os.path

df_all = pd.read_csv("output.csv")

with open('OntoMetrics.sh', 'w') as f:
    
     for index, row in df_all.iterrows():
          url = df_all['mirror_from'][index]
          filename = 'all_files/' + df_all['namespace'][index]
          line = f'curl -H "classmetrics: true" "http://opi.informatik.uni-rostock.de/api?url={url}"  > {filename}.xml\n'
          f.write(line)