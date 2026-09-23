"""Focused checks for the eight accepted Stage 5 corrections."""
from pathlib import Path
import ast,copy,hashlib,importlib.util,json,os,shutil,subprocess,sys,tempfile
from time import perf_counter
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
SUP=ROOT/'supplement'
sys.path.insert(0,str(SUP))
import sympy as s
import validate,validate_models as vm,replay_certificates as replay

def reject(call,message):
 try:call()
 except AssertionError as exc:
  assert message in str(exc),(message,str(exc))
 else:raise AssertionError('invalid witness accepted')

def main():
 started=perf_counter();report={}
 assert all(importlib.util.find_spec(p) is None for p in ('gurobipy','cvxpy','clarabel'))
 report['environment']={'python':sys.version,'commercial_and_conic_packages':'absent'}
 report['manifests']=validate.verify_manifests()
 captured=[];original=vm.verify_mixture_information
 def capture(M,p,G,stored):
  result=original(M,p,G,stored);captured.append((M,p,G,stored));return result
 vm.verify_mixture_information=capture
 report['models']=vm.run()
 vm.verify_mixture_information=original
 assert len(captured)==4
 M,p,G,stored=next(r for r in captured if r[2].rows)
 badG=G.copy();badG[0,0]+=s.Rational(1,100)
 E=s.eye(p).col_join(badG);quadratic=E.T*M*E
 # This malformed witness satisfies the old inverse-weight premise exactly.
 assert quadratic.inv()*quadratic==s.eye(p)
 reject(lambda:original(M,p,badG,stored),'not stationary')
 badstored=s.Matrix(stored);badstored[0,0]+=1
 reject(lambda:original(M,p,G,badstored),'information mismatch')
 reject(lambda:original(s.diag(1,-1),1,s.zeros(1,1),[[1]]),'not SPD')
 report['mixture_negative_checks']=['perturbed actual nuisance witness rejected despite inverse-weight identity','changed stored Schur matrix rejected','indefinite nuisance block rejected']
 # Execute the unchanged all-diagonal portion of the actual replay wrapper,
 # without repeating unrelated archived certificate families.
 tree=ast.parse((SUP/'replay_certificates.py').read_text())
 run=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run')
 begin=next(i for i,n in enumerate(run.body) if isinstance(n,ast.Assign) and ast.unparse(n.value)=="read('diagonal-split-kinetics-certificate')")
 end=next(i for i in range(begin,len(run.body)) if isinstance(run.body[i],ast.For))
 code=compile(ast.Module(body=run.body[begin:end],type_ignores=[]),str(SUP/'replay_certificates.py'),'exec')
 env=dict(vars(replay),rows=[]);exec(code,env)
 assert env['prob'].k==16 and sum(map(replay.Q,env['saved']['selection_point']))==16
 assert 'cube and cardinality feasibility' in env['rows'][0]['verified_fields']
 report['diagonal']=env['rows'][0]
 def badread(name):
  data=replay.read(name)
  if name=='diagonal-split-kinetics-certificate':
   data['selection_point'][0]=str(replay.Q(data['selection_point'][0])+replay.Q(1,1000000))
  return data
 reject(lambda:exec(code,dict(vars(replay),rows=[],read=badread)),'point cardinality')
 report['diagonal_negative_check']='non-cardinality point rejected by actual replay assertion'
 with tempfile.TemporaryDirectory(prefix='stage05-corrections-') as td:
  dest=Path(td)/'supplement';shutil.copytree(SUP,dest,ignore=shutil.ignore_patterns('.venv','__pycache__'))
  report['isolated_manifests']=validate.verify_manifests(dest)
  rejected=[]
  for name in ('validate_models.py','results/fresh-all.json','legacy/certify_noisy_markov.py'):
   path=dest/name;original_bytes=path.read_bytes();path.write_bytes(original_bytes+b'\n')
   result=subprocess.run([sys.executable,str(dest/'validate.py')],cwd=dest,capture_output=True,text=True)
   assert result.returncode!=0 and 'SHA-256 mismatch' in result.stderr
   assert 'running ' not in result.stdout
   rejected.append(name);path.write_bytes(original_bytes)
  report['tampered_preflight_rejections']=rejected
  result=subprocess.run([sys.executable,str(dest/'reproduce.py'),'spacing'],cwd=dest,capture_output=True,text=True)
  (ROOT/'verification/stage05-corrections/spacing-wrapper.log').write_text(result.stdout+result.stderr)
  assert result.returncode==0,result.stderr
  generated=dest/'results/reproduced/spacing'
  run_record=json.loads((generated/'run.json').read_text())
  assert run_record['command']==['noisy_markov_spacing_design.py','first-case'] and run_record['returncode']==0
  assert 'results/noisy-markov-spacing-kinetics-probe.json' in run_record['changed_files']
  shutil.copytree(generated,ROOT/'verification/stage05-corrections/spacing-reproduced',dirs_exist_ok=True)
  report['spacing_reproduction']=run_record
  assert validate.verify_manifests(dest)==report['isolated_manifests']
 report['status']='passed';report['wall_seconds']=perf_counter()-started
 (ROOT/'verification/stage05-corrections/checks.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
