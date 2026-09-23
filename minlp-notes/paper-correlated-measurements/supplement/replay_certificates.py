"""Recompute archived mathematical witnesses without rerunning optimization.

Historical producer strings and timings are provenance, never input paths or
trusted bounds. All file resolution is relative to this portable supplement.
"""
from pathlib import Path
from fractions import Fraction as Q
from time import perf_counter
import argparse,json,sys,hashlib
sys.set_int_max_str_digits(0);sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;LEGACY=HERE/'legacy';DATA=LEGACY/'results'
sys.path.insert(0,str(LEGACY))
import sympy as s
from certify_noisy_markov import certify as memory, rational, log_enclosure, fraction, require_spd
from certify_dense_design import Problem,certify as dense
from certify_all_splits import certify as allsplits
from certify_diagonal_split import exact_diagonal_point
from certify_spacing_design import certify as spacing
from certify_partial_trace import certify as partial
from certify_robust_design import certify as robust
from certify_latent_separator import certify as separator

def read(name):return json.loads((DATA/(name if name.endswith('.json') else name+'.json')).read_text(),parse_float=str)
def same(a,b):
 if isinstance(a,float):a=str(a)
 if isinstance(b,float):b=str(b)
 if isinstance(a,(list,tuple)):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 if isinstance(a,dict):return set(a)==set(b) and all(same(a[k],b[k]) for k in a)
 if isinstance(a,(str,int,Q)) and isinstance(b,(str,int,Q)):
  try:return Q(a)==Q(b)
  except (ValueError,TypeError):pass
 return a==b

def run(full=True):
 t=perf_counter();rows=[]
 def record(name,result,saved,keys):
  for key in keys:assert same(result[key],saved[key]),(name,key)
  rows.append({'artifact':name,'verified_fields':keys});print('verified',name,flush=True)
 for name in [f'noisy-markov-extended-certificate-{i}' for i in range(6)]+[f'noisy-markov-kinetics-certificate-n{n}-{regime}' for n in (48,96) for regime in ('fast','slow')]:
  saved=read(name);source=read(Path(saved['input_file']).name);case=source['results'][saved['input_case_index']]
  result=memory(case,case['hulls'][saved['input_hull_index']]);record(name,result,saved,['lower_bound','upper_bound','gap','delta','integer_price','selected','priced_selection'])
 for name in ('dense-design-exact-certificates','dense-design-kinetics-n48-certificates','dense-design-kinetics-n96-certificates'):
  for ix,saved in enumerate(read(name)['results']):
   result=dense(Problem.read(saved['problem_data']),saved['tangent_z'],saved['a'],{tuple(saved['incumbent_selection']):['replay']})
   record(f'{name}[{ix}]',result,saved,['upper_bound','continuous_lower_bound','continuous_certificate_gap','incumbent_lower_bound','information_determinant','gradient','split_ldl_pivots'])
 for name in ('dense-all-splits-certificates','dense-all-splits-kinetics-n48-certificates','dense-all-splits-kinetics-n96-certificates'):
  for ix,saved in enumerate(read(name)['results']):
   result=allsplits(Problem.read(saved['problem_data']),saved['feasible_point'],saved['upper_split'])
   record(f'{name}[{ix}]',result,saved,['all_splits_lower_bound','information_determinant','spectral_upper_witness'])
 for n,records in ((None,read('dense-all-splits-certificates')['results']),(48,read('dense-all-splits-kinetics-n48-certificates')['results']),(96,read('dense-all-splits-kinetics-n96-certificates')['results'])):
  for ix,rr in enumerate(records):
   name=f'noisy-markov-extended-certificate-{ix}' if n is None else f'noisy-markov-kinetics-certificate-n{n}-{("fast","slow")[ix]}'
   mm=read(name);assert Problem.read(rr['problem_data'])==Problem.read(mm['problem_data'])
   assert Q(rr['all_splits_lower_bound'])>Q(mm['upper_bound'])
 # Check the stored exact dual factor itself, avoiding a new floating factor proposal.
 saved=read('diagonal-split-kinetics-certificate');prob=Problem.read(saved['problem_data'])
 assert sum(map(Q,saved['selection_point']),Q(0))==prob.k,'all-diagonal point cardinality'
 information,gradient,determinant=exact_diagonal_point(prob,saved['selection_point'],saved['reference_diagonal'])
 determinant=fraction(require_spd(information).det());lo=log_enclosure(determinant)[0]
 dual=saved['dual_certificate'];B=s.Matrix([[s.Rational(v) for v in row] for row in dual['factor']]);c=list(map(Q,dual['diagonal_correction']))
 Y=B*B.T+s.diag(*map(s.Rational,c));assert all(v>=0 for v in c)
 assert all(Y[i,i]>=-s.Rational(gradient[i]) for i in range(prob.n))
 R=s.Matrix(prob.n,prob.n,lambda i,j:s.Rational(prob.latent)*s.Rational(prob.rho)**abs(i-j)+(s.Rational(prob.nugget) if i==j else 0))
 tr=fraction(s.trace(R*Y));assert tr==Q(dual['trace_RY'])
 matching_memory=read('noisy-markov-kinetics-certificate-n48-fast')
 assert Problem.read(matching_memory['problem_data'])==prob
 assert Q(matching_memory['upper_bound'])==Q(saved['memory_upper_bound'])
 value=lo-sum((g*Q(a) for g,a in zip(gradient,saved['reference_diagonal'])),Q(0))-tr
 assert value==Q(saved['all_diagonal_lower_bound'])
 assert value-Q(saved['memory_upper_bound'])==Q(saved['separation'])>Q('0.0925444163328848')
 rows.append({'artifact':'diagonal-split-kinetics-certificate','verified_fields':['exact point','cube and cardinality feasibility','gradient','PSD factor','diagonal domination','trace','lower bound','separation']})
 for name in ('noisy-markov-spacing-kinetics-certificate','noisy-markov-spacing-kinetics-integer-certificate','noisy-markov-spacing-kinetics-refined-certificate'):
  saved=read(name);case=read(Path(saved['input_file']).name)['results'][saved['input_case_index']]
  result=spacing(case,case['hulls'][saved['input_hull_index']],integer_grid=saved.get('integer_coefficient_grid'),refined_pairs='refined' in name)
  record(name,result,saved,['delta','lower_bound','upper_bound','integer_price','selected','priced_selection'])
 for ix in range(4):
  name=f'partial-observation-trace-certificate-{ix}'
  saved=read(name);case=read('partial-observation-trace-probe')['results'][saved['input_case_index']]
  result=partial(case,case['dp'][saved['input_dp_index']]);record(name,result,saved,['delta','lower_bound','upper_bound','relative_gap','integer_price','selected'])
 for name in ('robust-kinetic-n48-certificate','robust-kinetic-n96-certificate','robust-kinetic-n96-polished-certificate'):
  saved=read(name);source=read(f'robust-kinetic-n{saved["n"]}');proposal=dict(source['robust']);proposal['selected']=saved['selected']
  result=robust(source,proposal);record(name,result,saved,['standardized','fixed_offset','integer_price','dual_weights','individual_optimum_lower_bounds','individual_optimum_upper_bounds'])
 for name in ('latent-separator-n48-b8-certificate','latent-separator-n96-b12-certificate','latent-separator-n96-b16-certificate','latent-separator-n192-b12-certificate','latent-separator-n192-b16-certificate'):
  if not full and ('b16' in name or 'n192' in name):continue
  saved=read(name);source=read(Path(saved['input_file']).name);proposal=dict(source['results'][saved['input_case_index']]);proposal['selected']=saved['selected']
  result=separator(source['problem_data'],proposal);record(name,result,saved,['lower_bound','upper_bound','gap','integer_price','selected','priced_selection','anchor_prior_trace'])
 return {'status':'passed','scope':'exact replay; no numerical optimizer or commercial solver invoked','full':full,'certificates':rows,'count':len(rows),'wall_seconds':perf_counter()-t}

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--quick',action='store_true');parser.add_argument('--output',type=Path,default=HERE/'results/certificate-replay.json');args=parser.parse_args()
 result=run(not args.quick);args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'count':result['count'],'wall_seconds':result['wall_seconds']}))
if __name__=='__main__':main()
