"""Distinct existing diagnostics, redirected to the paper solver without source edits."""
from pathlib import Path
import sys,subprocess,time,json,hashlib,os
P=Path(__file__).resolve().parents[1];R=Path('/home/sgusev/repo/minlp-notes');out=P/'verification/stage06-author'
out.mkdir(parents=True,exist_ok=True)
env=os.environ.copy()
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):env[key]='1'
commands=[('full_task',[sys.executable,str(P/'code/check_full_task.py')]),
('convex_certificates',[sys.executable,str(R/'code/bilevel_reopened/quadratic_review_checks.py')])]
for name in ('review_one','review_two','check_scalar_examples'):
 source=R/'code/bilevel_nonconvex'/f'{name}.py'
 if name=='review_one':
  text=source.read_text().replace("Path(__file__).with_name('scalar_solver.py')",repr(str(P/'code/compressed_solver.py')))
  target=out/'review_one_paper.py';target.write_text(text);command=[sys.executable,str(target)]
 else:
  code="import sys,runpy;sys.path.insert(0,"+repr(str(P/'code'))+");import compressed_solver;sys.modules['scalar_solver']=compressed_solver;runpy.run_path("+repr(str(source))+",run_name='__main__')"
  command=[sys.executable,'-c',code]
 commands.append((name,command))
records=[]
for name,cmd in commands:
 start=time.perf_counter();result=subprocess.run(cmd,cwd=R,env=env,text=True,capture_output=True,timeout=180)
 (out/f'{name}.log').write_text(result.stdout+result.stderr)
 records.append(dict(name=name,command=cmd,exit_code=result.returncode,seconds=time.perf_counter()-start))
 print(name,result.returncode,flush=True)
(out/'diagnostics.json').write_text(json.dumps(records,indent=2)+'\n')
assert all(r['exit_code']==0 for r in records)
