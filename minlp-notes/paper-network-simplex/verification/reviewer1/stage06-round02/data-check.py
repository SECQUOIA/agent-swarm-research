from pathlib import Path
from statistics import median
import copy, hashlib, json, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).parent
PAPER=ROOT/'paper-network-simplex'
data=json.loads((PAPER/'verification/stage06-benchmarks.json').read_text())
archive=PAPER/'verification/stage06-corrections/round1-archive'
hashes=json.loads((archive/'manifest.json').read_text())
for path,digest in hashes.items():
    assert hashlib.sha256((archive/path).read_bytes()).hexdigest()==digest,path
old=json.loads((archive/'paper-network-simplex/verification/stage06-benchmarks.json').read_text())
assert all(data[k]==old[k] for k in ('flat','membership','cold'))
for a,b in zip(data['optimization'],old['optimization']):
    for key in ('name','y','objective_vector','extra_rows','edges','states','observations'):
        assert a[key]==b[key],key
total=0
for case in data['optimization']+data['flat']+data['membership']:
    for method,stats in case['summary'].items():
        for component,values in stats.items():
            raw=[run['measurements'][method][component] for run in case['runs']]
            assert values==dict(minimum=min(raw),median=median(raw),maximum=max(raw))
            total+=1
# Execute the complete validator/table generator in an isolated miniature tree.
private=HERE/'table-check';(private/'verification').mkdir(parents=True,exist_ok=True)
script=private/'verification/stage06-tables.py'
shutil.copy2(PAPER/'verification/stage06-tables.py',script)
source=private/'verification/stage06-benchmarks.json'
shutil.copy2(PAPER/'verification/stage06-benchmarks.json',source)
run=subprocess.run([sys.executable,str(script)],capture_output=True,text=True)
assert run.returncode==0,run.stderr
for table in (private/'tables').glob('*.tex'):
    assert table.read_bytes()==(PAPER/'process/snapshots/stage06-round02/tables'/table.name).read_bytes()
mutants=[]
a=copy.deepcopy(data);a['flat'].pop();mutants.append(('missing_flat',a))
a=copy.deepcopy(data);a['optimization'][0]['name']=a['optimization'][1]['name'];mutants.append(('duplicate_optimization',a))
a=copy.deepcopy(data);a['optimization'][0]['runs'][0]['measurements'].pop('global');mutants.append(('missing_method',a))
a=copy.deepcopy(data);a['membership'][0]['runs'][0]['measurements']['full']['status']=2;mutants.append(('wrong_status',a))
for name,a in mutants:
    source.write_text(json.dumps(a))
    run=subprocess.run([sys.executable,str(script)],capture_output=True,text=True)
    assert run.returncode!=0,name
source.write_text(json.dumps(data))
result=dict(archive_hashes=len(hashes),timing_summaries=total,generated_tables=5,
            rejected_mutations=[x[0] for x in mutants],retained_nonoptimization_data=True,
            optimization_inputs_preserved=True)
print(json.dumps(result,indent=2))
(HERE/'data-check-result.json').write_text(json.dumps(result,indent=2)+'\n')
