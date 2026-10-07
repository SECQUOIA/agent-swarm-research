"""Run only the small round-2 checks, serially, and retain exact command records."""
import json
import os
from pathlib import Path
import shlex
import subprocess

W = Path(__file__).resolve().parent
ROOT = W.parents[3]
P = ROOT/'research-20260929/publication'
env = os.environ.copy()
env.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
prefix = 'OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 '
records = []


def run(script, out, args=(), append=False):
    argv = ['python3',str(script.relative_to(ROOT)),*map(str,args)]
    cmd = prefix+shlex.join(argv)+(' >> ' if append else ' > ')+str(out.relative_to(ROOT))
    with out.open('a' if append else 'w') as f:
        r = subprocess.run(argv,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
    records.append(dict(command=cmd,exit_code=r.returncode))
    (W/'commands-r2.json').write_text(json.dumps(records,indent=2)+'\n')
    print(r.returncode,cmd,flush=True)
    assert r.returncode == 0


run(W/'check_r2.py',W/'check_r2.log')
run(P/'primal/water-ann-kan/code/minor_review_check.py',P/'primal/water-ann-kan/logs/minor_review_check.log')
run(P/'primal/lnts/minor_review_check.py',P/'primal/lnts/logs/review_r2_check.log')
run(P/'scip-bug/minor_review_check.py',P/'scip-bug/logs/review_r2_check.log')
run(P/'literature/control/checks/dtoc5_reference_check.py',P/'literature/control/checks/dtoc5_reference_check.log')
src = P/'literature/control/sources/qplib/camshape_copies'
log = P/'literature/control/checks/qplib_camshape_compare.log'
for i,(n,k) in enumerate([(100,2738),(200,2480),(400,2703),(800,3177)]):
    args = [src/f'camshape{n}.gms',src/f'QPLIB_{k}.gms',
            ROOT/f'research-20260929/open-instances/minlplib_sol/camshape{n}.p1.sol',src/f'QPLIB_{k}.sol']
    run(P/'literature/control/checks/qplib_camshape_compare.py',log,
        [p.relative_to(ROOT) for p in args],append=i>0)
print('PASS: all targeted round-2 checks; serial execution, one CPU thread per process.')
