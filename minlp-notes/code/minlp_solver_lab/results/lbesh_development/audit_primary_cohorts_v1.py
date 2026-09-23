import json,math,statistics,hashlib,sys
from collections import Counter
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
import lbesh_results_independent_audit as audit
root=Path('results/lbesh_development'); path=root/'analysis_primary_v1/cohorts.json'
d=json.loads(path.read_text()); raw=root/'main_generated_v1.jsonl'
rows=[json.loads(s) for s in raw.read_text().splitlines()]
for r in rows:r['_file']='main_generated_v1'
assert audit.classify(rows,[],False)==[]
by={(r['instance'],r['method']):r for r in rows}; names=sorted({r['instance'] for r in rows})
assert d['input_sha256']==audit.digest(path.with_name('analysis.json'))
assert d['script_sha256']==audit.digest(path.with_name('derive_cohorts.py'))
groups=[('held_out','all','all'),('pilot','all','all'),('all','all','all')]+[('held_out','family',f) for f in ('exp','log','logsumexp','quadratic','reciprocal','trig')]+[('held_out','size',s) for s in ('small','medium','large')]
assert Counter((r['split'],r['dimension'],r['group'],r['formulation'],r['tree']) for r in d['oracle'])==Counter((s,x,g,f,t) for s,x,g in groups for f in ('hull','bigm') for t in ('single','multi'))
expected={(f'lbesh-{o}-{f}-{t}',f'lbesh-{o}-{f2}-{t2}') for o in ('esh','ecp') for f,t,f2,t2 in (('hull','single','bigm','single'),('hull','multi','bigm','multi'),('hull','single','hull','multi'),('bigm','single','bigm','multi'))}
assert Counter((r['first'],r['second']) for r in d['structure'])==Counter(expected)
fields=0

def close(a,b):
 assert math.isclose(a,b,abs_tol=1e-11,rel_tol=1e-11),(a,b)
for kind in ('oracle','structure'):
 for r in d[kind]:
  split=r.get('split','held_out'); cohort=[n for n in names if split=='all' or audit.dimensions(n)[2]==split]
  if r.get('dimension') in ('family','size'):
   idx=0 if r['dimension']=='family' else 1;cohort=[n for n in cohort if audit.dimensions(n)[idx]==r['group']]
  a,b=r['first'],r['second'];common=[n for n in cohort if by[n,a]['_solved'] and by[n,b]['_solved']]
  assert r['scheduled']==len(cohort) and r['common_instances']==common and r['common_solved']==len(common)
  means=[]
  for m in (a,b):
   means.append(audit.shifted([min(by[n,m]['wall_time'],150) for n in common]));close(means[-1],r[m]['common_wall_sgm'])
   assert r[m]['numerical_solves']==sum(by[n,m]['_solved'] for n in cohort)
   close(r[m]['par10_mean'],statistics.fmean(min(by[n,m]['wall_time'],150) if by[n,m]['_solved'] else 1500 for n in cohort))
   assert r['lp_end_reasons'][m]==dict(Counter(by[n,m]['solver_metrics']['lp_end_reason'] for n in common))
   assert set(r['metrics'][m])=={'cuts','lp_iters','milp_iters','nlp_solves','interior_nlps','nodes','time_master','time_nlp','time_interior','time_cuts','time_setup','time_total'}
   for metric,v in r['metrics'][m].items():
    vals=[by[n,m]['solver_metrics'].get(metric) for n in common];vals=[x for x in vals if audit.finite(x)]
    assert v['available']==len(vals);close(v['mean'],statistics.fmean(vals));close(v['median'],statistics.median(vals));fields+=3
  close(r['first_over_second_wall_sgm'],means[0]/means[1])
discord=[];lp={}
for n in names:
 for m in sorted({r['method'] for r in rows if r['method'].startswith('lbesh-esh-')}):
  a,b=by[n,m],by[n,m.replace('-esh-','-ecp-')]
  if a['_solved']!=b['_solved']:discord.append(dict(instance=n,method=m,esh_solved=a['_solved'],ecp_solved=b['_solved'],esh_wall=a['wall_time'],ecp_wall=b['wall_time'],ecp_feasible=b['_feasible'],ecp_status=b['raw_status']))
for m in sorted({r['method'] for r in rows if r['method'].startswith('lbesh-')}):
 rs=[r for r in rows if r['method']==m and audit.dimensions(r['instance'])[2]=='held_out'];v=[r['solver_metrics'].get('last_lp_max_perspective_violation') for r in rs];v=[x for x in v if audit.finite(x)]
 lp[m]=dict(reasons=dict(Counter(r['solver_metrics']['lp_end_reason'] for r in rs)),max_residual=max(v) if v else None)
out=dict(raw_sha256=audit.digest(raw),cohorts_sha256=audit.digest(path),independent_derivation_sha256=audit.digest(Path(__file__)),oracle_cohorts=len(d['oracle']),structure_cohorts=len(d['structure']),metric_fields_checked=fields,discordance=discord,heldout_lp=lp)
target=root/'audit_primary_cohorts_v1.json';assert not target.exists();target.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
