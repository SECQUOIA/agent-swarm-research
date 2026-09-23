"""Regenerate manuscript tables and validate the recorded experimental outcomes."""
from pathlib import Path
import json,statistics as st,hashlib,sys
P=Path(__file__).resolve().parents[1];R=P.parent
x=json.loads((P/'data/stage06-results.json').read_text());records=x['records']
assert len(records)==60 and all(r['exit_code']==0 for r in records)
def group(method,name):return [r for r in records if r['method']==method and r['name']==name]
def med(rs,k):return st.median(r['result'][k] for r in rs)
def num(v):return f'{v:.4f}'
lines=[]
for name,label in [('jump','2 (jump)'),('heterogeneous_2','2'),('heterogeneous_4','4'),('heterogeneous_6','6')]:
 for method,ml in [('compressed','Compressed'),('faces','Faces')]:
  rr=group(method,name)
  lines.append(' & '.join([label,ml]+[num(med(rr,k)) for k in ['build_seconds','optimistic_seconds','pessimistic_seconds','total_seconds']]+[num(st.median(r['worker_wall_seconds'] for r in rr))])+r' \\')
(P/'data/table-full-task.tex').write_text('\n'.join(lines)+'\n'+r'\bottomrule'+'\n')
lines=[]
for name,label in [('heterogeneous_12','12'),('heterogeneous_24','24'),('heterogeneous_48','48'),('two_types_20','20 (two types)'),('two_types_200','200 (two types)'),('two_types_1000','1000 (two types)')]:
 rr=group('compressed',name);c=rr[0]['result']['counts']
 lines.append(' & '.join([label,str(c['fiber_pieces']),str(c['cuts'])]+[num(med(rr,k)) for k in ['build_seconds','optimistic_seconds','pessimistic_seconds','total_seconds']])+r' \\')
(P/'data/table-scaling.tex').write_text('\n'.join(lines)+'\n'+r'\bottomrule'+'\n')
lines=[]
history=json.loads((R/'code/bilevel_reopened/screening_milp_comparison.json').read_text())
for source,n,rr in [('Archived',r['N'],[dict(result=r)]) for r in history['cases']]+[('Fresh',n,group('screening',str(n))) for n in (8,20)]:
 exactpre=st.median(r['result']['generation_seconds']+r['result']['surrogate_cover_seconds'] for r in rr)
 exacttotal=st.median(sum(r['result'][k] for k in ['generation_seconds','surrogate_cover_seconds','screened_solver_seconds','exact_verification_seconds']) for r in rr)
 milppre=st.median(r['result']['generation_seconds']+r['result']['milp_formulation_seconds'] for r in rr)
 milptotal=st.median(sum(r['result'][k] for k in ['generation_seconds','milp_formulation_seconds','milp_solve_seconds']) for r in rr)
 lines.append(' & '.join([source,str(n)]+list(map(num,[exactpre,med(rr,'screened_solver_seconds'),exacttotal,milppre,med(rr,'milp_solve_seconds'),milptotal])))+r' \\')
 for r in rr:
  z=r['result'];assert z['screened_status']=='optimal' and z['milp_status_code']==0 and z['exact_solution_checks']
(P/'data/table-screening.tex').write_text('\n'.join(lines)+'\n'+r'\bottomrule'+'\n')
print('PASS: 60 completed workers; exact screening certificates and all numerical statuses checked; three tables regenerated')
