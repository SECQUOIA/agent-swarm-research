from pathlib import Path
from statistics import median
from copy import deepcopy
import hashlib,json,shutil,subprocess
root=Path.cwd();paper=root/'paper-network-simplex';out=paper/'verification/reviewer5/stage06-round02';snapshot=paper/'process/snapshots/stage06-round02';old=paper/'verification/stage06-corrections/round1-archive'
manifest=json.loads((paper/'verification/stage06-validation.json').read_text())
for f,h in manifest['sha256'].items():assert hashlib.sha256((root/f).read_bytes()).hexdigest()==h,f
for f in list((snapshot/'sections').glob('*.tex'))+[snapshot/'main.tex',snapshot/'references.bib',snapshot/'README.md']+list((snapshot/'tables').glob('*.tex')):assert f.read_bytes()==(paper/f.relative_to(snapshot)).read_bytes(),str(f)
for f in (snapshot/'sections').glob('0[1-7]*'):assert f.read_bytes()==(paper/'process/snapshots/stage06-round01/sections'/f.name).read_bytes()
data=json.loads((paper/'verification/stage06-benchmarks.json').read_text());prior=json.loads((old/'paper-network-simplex/verification/stage06-benchmarks.json').read_text())
for key in ('flat','membership','cold'):assert data[key]==prior[key],key
summaries=0;records=0
for case in data['flat']+data['membership']+data['optimization']:
 for method,stats in case['summary'].items():
  for field,stat in stats.items():
   raw=[r['measurements'][method][field] for r in case['runs']]
   assert stat==dict(minimum=min(raw),median=median(raw),maximum=max(raw));summaries+=1
 for run in case['runs']:
  for record in run['measurements'].values():
   assert record['status']==(0 if case.get('feasible',True) else 2);records+=1
for c,p in zip(data['optimization'],prior['optimization']):
 for key in ('name','edges','states','observations','observed_labels','y','objective_vector','extra_rows'):assert c[key]==p[key],key
 assert abs(c['objective']-p['objective'])<1e-7
 for run,oldrun in zip(c['runs'],p['runs']):
  assert run['order']==oldrun['order']
  for method,measurement in run['measurements'].items():
   assert abs(measurement['objective']-c['objective'])<1e-7
   assert measurement['total_seconds']!=oldrun['measurements'][method]['total_seconds']
check=out/'table-check';(check/'verification').mkdir(parents=True,exist_ok=True);(check/'tables').mkdir(exist_ok=True)
shutil.copy(paper/'verification/stage06-tables.py',check/'verification/stage06-tables.py')
source=check/'verification/stage06-benchmarks.json'
def invoke(d):
 source.write_text(json.dumps(d));return subprocess.run(['/home/sgusev/miniconda3/envs/minlp-notes/bin/python',str(check/'verification/stage06-tables.py')],capture_output=True,text=True)
assert invoke(data).returncode==0
for f in (check/'tables').glob('*.tex'):
 # JSON reformatted privately: compare table content, retaining official hash separately.
 assert f.read_text().split('\n',1)[1]==(snapshot/'tables'/f.name).read_text().split('\n',1)[1]
mutations={}
def try_bad(name,func):
 d=deepcopy(data);func(d);answer=invoke(d);assert answer.returncode!=0,name;mutations[name]='rejected'
try_bad('duplicate-flat',lambda d:d['flat'].__setitem__(1,deepcopy(d['flat'][0])))
try_bad('missing-flat',lambda d:d['flat'].pop())
try_bad('duplicate-member',lambda d:d['membership'].__setitem__(1,deepcopy(d['membership'][0])))
try_bad('wrong-member-labels',lambda d:d['membership'][0].__setitem__('states',17))
try_bad('optimization-order',lambda d:d['optimization'].reverse())
try_bad('missing-optimization',lambda d:d['optimization'].pop())
try_bad('missing-warm-method',lambda d:d['optimization'][0]['warmup'].pop('global'))
try_bad('missing-run-method',lambda d:d['optimization'][0]['runs'][0]['measurements'].pop('full'))
try_bad('wrong-rotation',lambda d:d['optimization'][0]['runs'][1]['order'].reverse())
try_bad('wrong-status',lambda d:d['optimization'][0]['runs'][1]['measurements']['full'].__setitem__('status',2))
try_bad('wrong-summary',lambda d:d['optimization'][0]['summary']['full']['total_seconds'].__setitem__('median',1234))
# Restore correct raw bytes and test exact byte-for-byte regeneration.
source.write_bytes((paper/'verification/stage06-benchmarks.json').read_bytes())
answer=subprocess.run(['/home/sgusev/miniconda3/envs/minlp-notes/bin/python',str(check/'verification/stage06-tables.py')],capture_output=True,text=True);assert answer.returncode==0
for f in (check/'tables').glob('*.tex'):assert f.read_bytes()==(snapshot/'tables'/f.name).read_bytes()
print(json.dumps(dict(status='PASS',hashes=len(manifest['sha256']),timing_summaries=summaries,timed_records=records,unchanged_membership_and_cold=True,original_optimization_inputs_retained=True,new_timings_all_optimization_methods=True,identical_generated_tables=5,mutations=mutations),indent=2))
