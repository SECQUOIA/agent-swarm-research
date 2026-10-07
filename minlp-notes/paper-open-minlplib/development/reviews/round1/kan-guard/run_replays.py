"""Six single-threaded /tmp searches; no repository script is executed."""
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path('/tmp/kan-guard')
CHECKS = ROOT / 'checks'
NAMES = ['kan_r3_h1_n4','kan_r3_h1_n5','kan_r3_h1_n9',
         'kan_r5_h1_n3','kan_r5_h1_n5','kan_r5_h1_n8']
THREAD_VARS = ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS',
               'NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS']
env = os.environ.copy()
env.update({k:'1' for k in THREAD_VARS})
env['PYTHONDONTWRITEBYTECODE'] = '1'
env['MINLPLIB_OSIL_ROOT'] = str(ROOT / 'osil')
env['PYTHONPATH'] = ':'.join(str(ROOT / p) for p in [
    'research-20260929/reviews/wave3-verification',
    'research-20260929/open-instances-wave3/kan',
    'research-20260929/open-instances-wave2/small'])
# Six OS processes, one allowed CPU each; numerical libraries also use one thread.
cpus = sorted(os.sched_getaffinity(0))[:6]
assert len(cpus) == 6, cpus
sources = [CHECKS/'kan_bnb_rigexp.py'] + sorted((ROOT/'research-20260929').rglob('*.py'))
inputs = [ROOT/'osil'/(name+'.osil') for name in NAMES]
manifest = dict(start_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
                cpus=cpus, thread_limits={k:'1' for k in THREAD_VARS},
                python=platform.python_version(), source_hashes={
                    str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in sources+inputs},
                command_template='taskset -c <cpu> python3 -u /tmp/kan-guard/checks/kan_bnb_rigexp.py <instance> 4e-11 7200 1024',
                seed=0, third_order=True, extra_starts=None,
                note='Time limit raised from 1800 to 7200 s to allow guards and concurrent load; completion, not timeout, required.')
versions = subprocess.check_output(['python3','-c',
    'import numpy,scipy,mpmath,json; print(json.dumps(dict(numpy=numpy.__version__,scipy=scipy.__version__,mpmath=mpmath.__version__)))'],env=env,text=True)
manifest['versions'] = json.loads(versions)
(CHECKS/'replay-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

def run(item):
    i,name = item
    path = CHECKS/'logs'/(name+'.guard.log')
    command = ['taskset','-c',str(cpus[i]),'python3','-u',str(CHECKS/'kan_bnb_rigexp.py'),name,'4e-11','7200','1024']
    start = time.monotonic()
    print('START',name,'cpu',cpus[i],flush=True)
    with path.open('w') as out:
        proc = subprocess.run(command,cwd=CHECKS,env=env,stdout=out,stderr=subprocess.STDOUT)
    print('END',name,'returncode',proc.returncode,'seconds',round(time.monotonic()-start,2),flush=True)
    return dict(name=name,command=command,returncode=proc.returncode,elapsed=time.monotonic()-start)

with ThreadPoolExecutor(max_workers=6) as pool:
    results = list(pool.map(run,enumerate(NAMES)))
(CHECKS/'replay-driver-results.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(r['returncode']==0 for r in results)
assert all(json.loads((CHECKS/'logs'/(name+'.bnb.json')).read_text())['done'] for name in NAMES)
print('ALL SIX SEARCHES COMPLETE',flush=True)
