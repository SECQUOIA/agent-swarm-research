import json,copy,shutil,subprocess
from pathlib import Path
P=Path('paper-network-simplex');E=P/'verification/reviewer3/stage06-round02';data=json.loads((P/'verification/stage06-benchmarks.json').read_text())
mutations={
'duplicate_flat':lambda d:d['flat'].__setitem__(-1,copy.deepcopy(d['flat'][0])),
'missing_membership':lambda d:d['membership'].pop(),
'wrong_membership_label':lambda d:d['membership'][1].__setitem__('states',129),
'wrong_optimization_order':lambda d:d['optimization'].reverse(),
'missing_warmup_method':lambda d:d['optimization'][0]['warmup'].pop('global'),
'missing_run_method':lambda d:d['flat'][0]['runs'][0]['measurements'].pop('full'),
'missing_summary_method':lambda d:d['membership'][0]['summary'].pop('global'),
'wrong_rotation':lambda d:d['optimization'][0]['runs'][1]['order'].reverse(),
'wrong_status':lambda d:d['flat'][0]['runs'][0]['measurements']['full'].__setitem__('status',2),
'corrupt_summary':lambda d:d['optimization'][0]['summary']['full']['total_seconds'].__setitem__('median',999),
}
out={}
for name,mutate in mutations.items():
 folder=E/'mutations'/name;(folder/'verification').mkdir(parents=True,exist_ok=True)
 altered=copy.deepcopy(data);mutate(altered)
 (folder/'verification/stage06-benchmarks.json').write_text(json.dumps(altered))
 shutil.copy(P/'verification/stage06-tables.py',folder/'verification/stage06-tables.py')
 answer=subprocess.run(['python',str(folder/'verification/stage06-tables.py')],capture_output=True,text=True)
 (folder/'result.log').write_text(answer.stdout+answer.stderr)
 assert answer.returncode!=0 and not (folder/'tables').exists(),name
 out[name]='rejected before table output'
(E/'control-checks.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
