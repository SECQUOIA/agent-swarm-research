"""Run the portable scientific validation suite; no commercial solver needed."""
from pathlib import Path
from time import perf_counter
import argparse,hashlib,json,os,subprocess,sys
HERE=Path(__file__).resolve().parent

def verify_manifests(root=HERE):
 """Check artifact integrity separately from the scientific witness checks."""
 counts={}
 for name,key in (('archive-manifest.json','destination'),('source-manifest.json','path')):
  manifest=json.loads((root/name).read_text())
  entries=manifest if key=='destination' else manifest['files']
  for entry in entries:
   path=root/entry[key]
   if hashlib.sha256(path.read_bytes()).hexdigest()!=entry['sha256']:
    raise ValueError(f'{name}: SHA-256 mismatch: {path}')
  counts[name]=len(entries)
 return counts

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--quick',action='store_true',help='skip the three most expensive separator replays; default checks every main certificate');args=parser.parse_args()
 started=perf_counter();manifest_counts=verify_manifests()
 print('archive and new-source hashes verified:',manifest_counts,flush=True)
 output=HERE/'results';output.mkdir(exist_ok=True)
 env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
 commands=[['checks/stage02.py'],['checks/stage03.py'],['checks/stage04.py'],
  ['source_kinetics/check_rankings.py','--output',str(output/'source-rankings-validation.json')],
  ['validate_models.py'],['replay_certificates.py']+(['--quick'] if args.quick else [])]
 stages=[]
 for cmd in commands:
  t=perf_counter();print('running',cmd[0],flush=True)
  result=subprocess.run([sys.executable,str(HERE/cmd[0]),*cmd[1:]],cwd=HERE,env=env,text=True,capture_output=True)
  (output/(Path(cmd[0]).stem+'.log')).write_text(result.stdout+result.stderr)
  if result.returncode:print(result.stdout+result.stderr);raise SystemExit(result.returncode)
  stages.append({'command':cmd,'seconds':perf_counter()-t});print('passed',cmd[0],flush=True)
 # Validate the freshly stored block witness by an exact recomputation of all
 # schedules, without invoking the nested study's numerical optimizer.
 sys.path.insert(0,str(HERE));from fresh_experiments import blocks,serial
 old=json.loads((output/'fresh-all.json').read_text())['blocks'];new=blocks()
 assert json.loads(json.dumps(new['model'],default=serial))==old['model']
 assert list(new['selected'])==old['selected']
 assert json.loads(json.dumps(new['archived_constant_comparisons'],default=serial))==old['archived_constant_comparisons']
 for key in ('true_lower','exhaustive_true_optimum','local_price','old_delta','sharp_far_delta','old_upper','sharp_far_upper'):
  assert str(new[key])==old[key],key
 report={'status':'passed','full':not args.quick,'manifest_files':manifest_counts['archive-manifest.json'],
  'source_manifest_files':manifest_counts['source-manifest.json'],'stages':stages,
  'fresh_block_exact_replay':'passed','wall_seconds':perf_counter()-started,
  'scope':'Exact rankings/certificates and finite proof checks; sensitivity/random dense checks are numerical diagnostics; no commercial solver'}
 (output/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
