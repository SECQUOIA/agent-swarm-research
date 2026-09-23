from pathlib import Path
import subprocess,os,json,time
E=Path(__file__).resolve().parent
private=Path((E/'extraction-path.txt').read_text().strip())
root=private/'computational-supplement'
env=dict(os.environ);env.pop('PYTHONPATH',None);env['PATH']=str(root/'.venv/bin')+os.pathsep+env['PATH'];env['PYTHONDONTWRITEBYTECODE']='1'
commands=[
'sha256sum -c MANIFEST.sha256',
'PYTHONPATH=code python -m unittest network_simplex.test_separator network_simplex.test_flat_chain network_simplex_benchmarks.test_strong_baselines -v',
'python code/network_simplex_review/verify_flat_chain_implementation.py',
'PYTHONPATH=code python -m network_simplex_compressed.verify',
'PYTHONPATH=code python -m network_simplex_compressed.integration',
'python paper-network-simplex/verification/stage02-exact.py',
'python paper-network-simplex/verification/stage03-exact.py',
'python paper-network-simplex/verification/stage04-recovery.py',
'python paper-network-simplex/verification/stage05-padding.py',
'python paper-network-simplex/verification/stage05-profile.py',
'python paper-network-simplex/verification/stage07/integral-hull.py',
'python checks/independent_math.py',
'python checks/independent_elimination.py',
'python checks/fibonacci_facets.py',
'python checks/repairs_and_threshold.py',
'PYTHONPATH=code python checks/exact_contracts.py',
'python paper-network-simplex/verification/stage06-tables.py',
'sha256sum -c MANIFEST.sha256',
'PYTHONPATH=code python -m network_simplex_benchmarks.paper_stage06 --quick --repetitions 1 --output smoke-benchmarks.json',
]
records=[]
for i,cmd in enumerate(commands):
 start=time.monotonic();print('START',i,cmd,flush=True)
 with (E/f'command-{i:02d}.log').open('w') as log:r=subprocess.run(cmd,shell=True,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
 item={'command':cmd,'cwd':str(root),'exit':r.returncode,'seconds':time.monotonic()-start,'log':f'command-{i:02d}.log'};records.append(item)
 (E/'documented-results.json').write_text(json.dumps(records,indent=2)+'\n')
 print('END',i,r.returncode,flush=True)
 if r.returncode:break
