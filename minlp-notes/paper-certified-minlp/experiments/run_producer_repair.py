#!/usr/bin/env python3
"""Run every primary-campaign case affected by the integer-token producer bug.

The frozen uniform wrapper supplies the identical worker and settings; only the
recorded producer implementation differs. No unaffected case is selected.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
from datetime import datetime,timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from run_uniform import digest


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--primary',type=Path,required=True);ap.add_argument('--lab',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--scip-bin',type=Path,required=True);ap.add_argument('--ipopt',type=Path,required=True);args=ap.parse_args()
    primary=args.primary.resolve();lab=args.lab.resolve();out=args.out.resolve();folder=Path(__file__).resolve().parent
    original=[json.loads(x)for x in(primary/'generation.jsonl').read_text().splitlines()];assert len(original)==289
    affected=[]
    for r in original:
        if r['status']!='worker_error':continue
        log=primary/'worker-logs'/f"{r['instance']}.log";text=log.read_text()
        if 'canonicalize_fractions' in text and 'Exceeds the limit (4300 digits) for integer string conversion'in text:
            affected.append({'instance':r['instance'],'primary_worker_log':digest(log),'cause':'Fraction(int(decimal_numerator), int(decimal_denominator)) exceeded Python decimal conversion guard'})
    names=sorted(r['instance']for r in affected);assert names
    out.mkdir(parents=True,exist_ok=False)
    for d in('artifacts','events','worker-reports','worker-logs'):(out/d).mkdir()
    (out/'names.txt').write_text(''.join(n+'\n'for n in names))
    original_protocol=json.loads((primary/'protocol.json').read_text())
    protocol={'frozen_utc':datetime.now(timezone.utc).isoformat(),'primary_protocol_sha256':digest(primary/'protocol.json')['sha256'],
       'affected_cases':affected,'cohort_size':len(names),'selection':'All and only primary worker errors with the canonicalize_fractions integer-conversion-limit traceback; no quality selection',
       'oa_search_seconds':30,'scip_search_seconds_per_attempt':30,'max_scip_attempts':2,'requested_threads':1,'workers':6,'outer_worker_cap_seconds':360,'separate_replay_cap_seconds':1200,
       'wrapper':digest(__file__),'frozen_worker_wrapper':digest(folder/'run_uniform.py'),'settings':digest(folder/'scip-uniform.set'),
       'sources':[digest(p)for folder in ('certify','lbesh')for p in sorted((lab/folder).glob('*.py'))],
       'model_sources':[digest(lab/'instances/py'/f'{n}.py')for n in names],
       'tools':[digest(args.scip_bin/n)for n in('scip','viprcomp','viprchk')]+[digest(args.ipopt)],
       'package_versions':{p:importlib.metadata.version(p)for p in('pyomo','numpy','sympy','mpmath','python-flint','gurobipy')},'python':sys.version,
       'environment_threads':{k:'1'for k in('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS')}}
    (out/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
    environment=os.environ.copy()
    for k in protocol['environment_threads']:environment[k]='1'
    def run(name):
        t=time.monotonic();cmd=[sys.executable,str(folder/'run_uniform.py'),'--worker','--name',name,'--lab',str(lab),'--out',str(out),'--scip-bin',str(args.scip_bin.resolve()),'--ipopt',str(args.ipopt.resolve()),'--settings',str(folder/'scip-uniform.set')]
        with(out/'worker-logs'/f'{name}.log').open('w')as log:
            process=subprocess.Popen(cmd,stdout=log,stderr=log,env=environment,start_new_session=True);timeout=False
            try:code=process.wait(timeout=360)
            except subprocess.TimeoutExpired:timeout=True;os.killpg(process.pid,signal.SIGKILL);code=process.wait()
            finally:
                try:os.killpg(process.pid,signal.SIGKILL)
                except ProcessLookupError:pass
        report=out/'worker-reports'/f'{name}.json'
        if timeout:r={'instance':name,'status':'hard_timeout'}
        elif code==0 and report.is_file():r=json.loads(report.read_text())
        else:r={'instance':name,'status':'worker_error','returncode':code}
        r['worker_wall_seconds']=time.monotonic()-t;return r
    start=datetime.now(timezone.utc).isoformat();t=time.monotonic()
    with(out/'generation.jsonl').open('x',buffering=1)as stream,ThreadPoolExecutor(max_workers=6)as pool:
        futures=[pool.submit(run,n)for n in names]
        for f in as_completed(futures):
            r=f.result();stream.write(json.dumps(r,default=str)+'\n');print(r['instance'],r['status'],round(r['worker_wall_seconds'],3),flush=True)
    (out/'timing.json').write_text(json.dumps({'started_utc':start,'finished_utc':datetime.now(timezone.utc).isoformat(),'wall_seconds':time.monotonic()-t},indent=2)+'\n')
    checked=[]
    for item in[protocol['wrapper'],protocol['frozen_worker_wrapper'],protocol['settings']]+protocol['sources']+protocol['model_sources']+protocol['tools']:
        current=digest(item['path']);checked.append({'path':item['path'],'sha256':current['sha256'],'matches':current['sha256']==item['sha256']and current['bytes']==item['bytes']})
    assert all(r['matches']for r in checked)
    (out/'postgeneration-integrity.json').write_text(json.dumps({'all_frozen_bytes_unchanged':True,'files':checked},indent=2)+'\n')

if __name__=='__main__':main()
