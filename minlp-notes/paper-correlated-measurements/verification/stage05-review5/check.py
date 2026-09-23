from pathlib import Path
import hashlib, importlib.util, json, os, shutil, subprocess, sys, tempfile
PAPER=Path('/home/sgusev/repo/minlp-notes/paper-correlated-measurements')
SRC=PAPER/'supplement'
OUT=PAPER/'verification/stage05-review5'
base=Path(tempfile.mkdtemp(prefix='correlated-review5-'))
copy=base/'supplement'
shutil.copytree(SRC,copy,ignore=shutil.ignore_patterns('.venv','__pycache__','reproduced'))
report={'copy':str(copy),'python':sys.executable,'optional_absent':{m:importlib.util.find_spec(m) is None for m in ['gurobipy','cvxpy','clarabel']}}
assert all(report['optional_absent'].values())
manifest=json.loads((copy/'archive-manifest.json').read_text())
for row in manifest:assert hashlib.sha256((copy/row['destination']).read_bytes()).hexdigest()==row['sha256']
source=json.loads((copy/'source-manifest.json').read_text())['files']
for row in source:assert hashlib.sha256((copy/row['path']).read_bytes()).hexdigest()==row['sha256']
report['valid_archive_hashes']=len(manifest);report['valid_source_hashes']=len(source)
env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
def run(name,args):
 p=subprocess.run([sys.executable,*args],cwd=copy,env=env,text=True,capture_output=True)
 (OUT/(name+'.log')).write_text(p.stdout+p.stderr)
 report[name]={'returncode':p.returncode,'tail':(p.stdout+p.stderr)[-1200:]}
 return p
p=run('spacing-wrapper',['reproduce.py','spacing']);assert p.returncode==2 and 'command' in p.stdout+p.stderr
p=run('spacing-existing-output-refusal',['reproduce.py','spacing']);assert p.returncode!=0 and 'already exists' in p.stderr
p=run('partial-wrapper',['reproduce.py','partial']);assert p.returncode==0
p=run('fresh-blocks',['fresh_experiments.py','blocks','--output','results/reviewer-blocks.json']);assert p.returncode==0
p=run('source-winners',['source_kinetics/check_rankings.py','--winners','--output','results/reviewer-source.json']);assert p.returncode==0
for row in manifest:assert hashlib.sha256((copy/row['destination']).read_bytes()).hexdigest()==row['sha256']
report['frozen_hashes_unchanged_after_runs']=True
# Negative archive tampering is rejected before any scientific tests run.
f=copy/manifest[0]['destination'];f.write_bytes(f.read_bytes()+b'\n')
p=run('archive-tamper-rejection',['validate.py','--quick']);assert p.returncode!=0 and 'AssertionError' in p.stderr
(OUT/'results.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
