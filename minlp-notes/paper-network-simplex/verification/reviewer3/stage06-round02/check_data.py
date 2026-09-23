from pathlib import Path
import json,hashlib,statistics,ast
P=Path('paper-network-simplex'); E=P/'verification/reviewer3/stage06-round02'; S=P/'process/snapshots/stage06-round02'; A=P/'verification/stage06-corrections/round1-archive'
v=json.loads((P/'verification/stage06-validation.json').read_text())
for name,digest in v['sha256'].items(): assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,name
archive=json.loads((A/'manifest.json').read_text())
for name,digest in archive.items(): assert hashlib.sha256((A/name).read_bytes()).hexdigest()==digest,name
old=json.loads((A/'paper-network-simplex/verification/stage06-benchmarks.json').read_text());new=json.loads((P/'verification/stage06-benchmarks.json').read_text())
for k in ('flat','membership','cold'): assert old[k]==new[k],k
for a,b in zip(old['optimization'],new['optimization']):
 for k in ('name','edges','states','observations','observed_labels','y','objective_vector','extra_rows','unconstrained_resource','reference_resource'): assert a.get(k)==b.get(k),k
 assert abs(a['objective']-b['objective'])<1e-7
rev=new['optimization_revision'];assert rev['source_data_sha256']==hashlib.sha256((A/'paper-network-simplex/verification/stage06-benchmarks.json').read_bytes()).hexdigest()
for p in S.glob('sections/0[1-7]-*.tex'): assert p.read_bytes()==(P/'process/snapshots/stage06-round01/sections'/p.name).read_bytes()
for p in (S/'tables').glob('*.tex'): assert p.read_bytes()==(E/'build/tables'/p.name).read_bytes()
functions=lambda p:{n.name:ast.dump(n) for n in ast.parse(p.read_text()).body if isinstance(n,ast.FunctionDef)}
f=functions(Path('code/network_simplex_benchmarks/strong_baselines.py'));g=functions(A/'code/network_simplex_benchmarks/strong_baselines.py')
for name in ('membership_ef','optimize_independent_states','_finish','_rational'): assert f[name]==g[name]
assert Path('code/network_simplex/flat_chain.py').read_bytes()==(A/'code/network_simplex/flat_chain.py').read_bytes()
fields=count=0
for case in new['flat']+new['membership']+new['optimization']:
 methods=list(case['warmup']);assert len(case['runs'])==5
 for k,run in enumerate(case['runs']):
  assert run['order']==methods[k%len(methods):]+methods[:k%len(methods)]
  assert set(run['measurements'])==set(methods)
  for method,raw in run['measurements'].items():
   count+=1;assert raw['status']==(0 if case.get('feasible',True) else 2)
   assert raw['total_seconds']>=raw['build_seconds']+raw['solve_seconds']-1e-9
   if 'stats' in raw and method!='cuts':assert raw['stats']==case['warmup'][method]['stats']
   if 'objective' in case:assert abs(raw['objective']-case['objective'])<1e-7
 for method in methods:
  expected={k for k in case['warmup'][method] if k.endswith('_seconds')}
  assert set(case['summary'][method])==expected
  for key in expected:
   values=[run['measurements'][method][key] for run in case['runs']]
   assert case['summary'][method][key]==dict(minimum=min(values),median=statistics.median(values),maximum=max(values));fields+=1
for case in new['optimization']:
 e,m,a=case['edges'],case['states'],case['observed_labels']
 assert case['warmup']['full']['stats']['variables']==(m+1)*e
 assert case['warmup']['global']['stats']['variables']==(a+1)*e
for case in new['flat']:
 assert case['warmup']['full']['stats']['variables']==(2 if case['weights']=='boundary' else 3)*(2*case['gadgets']+1)
out=dict(current_hashes=len(v['sha256']),archive_hashes=len(archive),timed_runs=count,summary_fields=fields,tables_identical=5,unchanged_membership_cold_and_inputs=True,unchanged_mathematical_sections=7)
(E/'data-checks.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
