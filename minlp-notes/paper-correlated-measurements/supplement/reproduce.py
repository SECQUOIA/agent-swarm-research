"""Run historical numerical producers in an isolated writable copy.

The frozen legacy archive is never written by this wrapper. Expensive studies
are explicit choices. Failed producer status and complete logs are retained.
"""
from pathlib import Path
import argparse,json,os,shutil,subprocess,sys,tempfile
from time import perf_counter
HERE=Path(__file__).resolve().parent

def main():
 parser=argparse.ArgumentParser();parser.add_argument('study',choices=['synthetic','kinetics48','kinetics96','spacing','block4','block16','partial','robust48','robust96','robustdense48','robustdense96','grid','separator48','separator96','separator192','diagonal-kinetics']);args=parser.parse_args()
 destination=HERE/'results/reproduced'/args.study
 if destination.exists():raise SystemExit(f'{destination} already exists; choose a new supplement copy or move that generated directory before rerunning')
 destination.mkdir(parents=True)
 with tempfile.TemporaryDirectory(prefix='correlated-measurements-') as td:
  root=Path(td)/'work';shutil.copytree(HERE/'legacy',root)
  commands={
   'synthetic':['noisy_markov_extended_benchmark.py'],
   'kinetics48':['noisy_markov_kinetics_probe.py','--n','48'],
   'kinetics96':['noisy_markov_kinetics_probe.py','--n','96','--output',str(root/'results/noisy-markov-kinetics-n96-probe.json')],
   'spacing':['noisy_markov_spacing_design.py','first-case'],
   'block4':['block_snapshot_design.py','probe','--d','4','--output',str(root/'results/block-snapshot-d4-probe.json')],
   'block16':['block_snapshot_design.py','probe','--d','16','--output',str(root/'results/block-snapshot-d16-probe.json')],
   'partial':['partial_observation_trace_probe.py','probe','--output',str(root/'results/partial-observation-trace-probe.json')],
   'robust48':['robust_kinetic_design.py','probe','--n','48','--output',str(root/'results/robust-kinetic-n48.json')],
   'robust96':['robust_kinetic_design.py','probe','--n','96','--output',str(root/'results/robust-kinetic-n96.json')],
   'robustdense48':['robust_dense_comparison.py','compare','--source',str(root/'results/robust-kinetic-n48.json'),'--output',str(root/'results/robust-dense-n48.json')],
   'robustdense96':['robust_dense_comparison.py','compare','--source',str(root/'results/robust-kinetic-n96.json'),'--output',str(root/'results/robust-dense-n96.json')],
   'grid':['fixed_physical_grid_benchmark.py'],
   'separator48':['latent_separator_design.py','--n','48','--blocks','4','6','8'],
   'separator96':['latent_separator_design.py','--n','96','--blocks','12','16'],
   'separator192':['latent_separator_design.py','--n','192','--blocks','12','16'],
   'diagonal-kinetics':['diagonal_split_probe.py','--input',str(root/'results/dense-design-kinetics-n48-certificates.json'),'--memory',str(root/'results/noisy-markov-kinetics-certificate-n48-fast.json'),'--output',str(root/'results/diagonal-split-kinetics-probe.json')]}
  cmd=commands[args.study];env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
  t=perf_counter();result=subprocess.run([sys.executable,str(root/cmd[0]),*cmd[1:]],cwd=root,env=env,text=True,capture_output=True)
  elapsed=perf_counter()-t;(destination/'producer.log').write_text(result.stdout+result.stderr)
  changed=[]
  for p in root.rglob('*'):
   if p.is_file():
    rel=p.relative_to(root);original=HERE/'legacy'/rel
    if not original.exists() or original.read_bytes()!=p.read_bytes():
     target=destination/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target);changed.append(str(rel))
  (destination/'run.json').write_text(json.dumps({'study':args.study,'command':cmd,'returncode':result.returncode,'wall_seconds_including_producer_serialization':elapsed,'changed_files':changed,'scope':'new numerical proposal run; historical producer may explicitly reuse matching archived inputs/results'},indent=2)+'\n')
  print(destination)
  if result.returncode:print(result.stderr);raise SystemExit(result.returncode)
if __name__=='__main__':main()
