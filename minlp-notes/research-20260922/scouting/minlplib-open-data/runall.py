import sys, os, json, pandas as pd
sys.path.insert(0,'/tmp/scout'); from osil import analyze
from concurrent.futures import ProcessPoolExecutor, TimeoutError as TE
O=os.path.expanduser('~/.cache/minlplib/minlplib/osil/')
names=pd.read_csv('/tmp/scout/open.csv').name.tolist()
def job(n):
    p=O+n+'.osil'
    if not os.path.exists(p): return n,{'err':'missing'}
    if os.path.getsize(p)>60e6: return n,{'err':'big %d'%os.path.getsize(p)}
    try: return n,analyze(p)
    except Exception as e: return n,{'err':repr(e)[:200]}
if __name__=='__main__':
    with ProcessPoolExecutor(8) as ex, open('/tmp/scout/struct.jsonl','w') as fh:
        for n,r in ex.map(job,names,chunksize=1):
            r['name']=n; fh.write(json.dumps(r,default=str)+'\n'); fh.flush()
