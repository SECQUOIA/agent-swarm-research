"""Fresh, serial, repeated computations. Never overwrite historical records.

Thread environment is set before numerical libraries are imported. Every timed
worker has a 90-second external limit; partial/failure records are retained.
Atlas construction and BOTH upper semantics are measured separately. Startup,
input validation, and total wall time are also recorded explicitly.
"""
from pathlib import Path as _CleanupPath
_NOTES_ROOT = _CleanupPath(__file__).resolve().parent.joinpath('../../../..').resolve()

import os
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
os.environ['PYTHONHASHSEED']='0'
from pathlib import Path
import sys,json,time,platform,hashlib,subprocess,random,statistics
PAPER=Path(__file__).resolve().parents[1];ROOT=Path((str(_NOTES_ROOT)))
sys.path.insert(0,str(ROOT/'code/bilevel_nonconvex'))
sys.path.insert(0,str(ROOT/'code/bilevel_reopened'))
import sympy as s
from check_full_task import data

def instance(n,seed):
    rng=random.Random(seed+n)
    d=[s.Rational(rng.randint(8,16),8) for _ in range(n)]
    u=[s.Rational(rng.randint(4,8),4) for _ in range(n)]
    c=[-s.Rational(rng.randint(4,24),8) for _ in range(n)]
    h=s.Rational(7,5)/sum(ui*ui/di for ui,di in zip(u,d))
    return data(d,c,u,h,L=0,U=5)

def datasets():
    out={}
    for n in (2,4,6,12,24,48):
        ins=instance(n,17)
        out[f'heterogeneous_{n}']=dict(instance=ins,rows=[dict(a='0',b=ins['u'],rhs=str(sum(map(s.Rational,ins['u']))/2))],seed=17)
    for n in (20,200,1000):
        m=n//2;ins=data([1]*n,[-1]*m+['-1/2']*m,[1]*n,s.Rational(3,5*m))
        out[f'two_types_{n}']=dict(instance=ins,rows=[dict(a='0',b=['1']*n,rhs=str(m))],seed=None)
    out['jump']=dict(instance=data([1,1],[-1,'-1/2'],[1,1],'3/5'),rows=[dict(a='0',b=['1','1'],rhs='1')],seed=None)
    return out

def encode(out):
    if out is None:return None
    if not isinstance(out,dict):out=out.__dict__
    return {k:(v if k=='attained' else None if v is None else str(v)) for k,v in out.items() if k!='z'}

def worker(method,name):
    from sympy.core.cache import clear_cache
    clear_cache()
    if method=='screening':
        import screening_milp_comparison as mod
        # HiGHS-specific threads option is forwarded by SciPy. Preserve warnings.
        original=mod.milp
        def single_thread(**kwargs):
            kwargs['options']={**kwargs.get('options',{}),'threads':1}
            return original(**kwargs)
        mod.milp=single_thread
        out=mod.run_case(int(name))
        out['exact_end_to_end']=sum(out.get(k,0) for k in ('generation_seconds','surrogate_cover_seconds','screened_solver_seconds','exact_verification_seconds'))
        out['milp_end_to_end']=sum(out.get(k,0) for k in ('generation_seconds','milp_formulation_seconds','milp_solve_seconds'))
        return out
    if method=='convex':
        from quadratic_tariff_benchmarks import tariff_instance
        from quadratic_solver import optimize_aligned_rank_one,dot
        from fractions import Fraction as F
        n=int(name);seed=50000+n+1;t=time.perf_counter();p=tariff_instance(n,seed,1);validated=time.perf_counter()-t
        t=time.perf_counter();answer=optimize_aligned_rank_one(p,0,(0,)*n,[(0,(-1,)*n,-F(n,5))],objective_xz=(-1,)*n);elapsed=time.perf_counter()-t
        g=[q+ci+ci2*answer['x'] for q,ci,ci2 in zip(p.qmul(answer['z']),p.c,p.C)]
        assert all(0<=z<=1 and (gi>=0 if z==0 else gi<=0 if z==1 else gi==0) for z,gi in zip(answer['z'],g))
        assert sum(answer['z'])>=F(n,5)
        return dict(n=n,seed=seed,validation_seconds=validated,sweep_upper_seconds=elapsed,total_seconds=validated+elapsed,thresholds=answer['thresholds'],intervals=answer['response_intervals_visited'],value=str(-answer['objective']),x=str(answer['x']),exact_KKT=True)
    entry=json.loads((PAPER/'data/stage06-instances.json').read_text())[name];ins=entry['instance'];rows=entry['rows']
    start=time.perf_counter()
    if method=='faces':
        import original_faces as mod
        tick=time.perf_counter();atlas=mod.build(ins);buildtime=time.perf_counter()-tick;validate=0
        counts=dict(faces=len(atlas.faces),cuts=len(atlas.cuts),patterns=atlas.patterns_examined,checked_principal_minors=len(atlas.principal_minors)-1)
        call=lambda sem:mod.optimize(atlas,rows,sem)
    else:
        if method=='original':import scalar_solver as mod
        else:import compressed_solver as mod
        tick=time.perf_counter();problem=mod.Instance(**ins);cons=[mod.Constraint(**row) for row in rows];validate=time.perf_counter()-tick
        tick=time.perf_counter();atlas=mod.build_atlas(problem);buildtime=time.perf_counter()-tick
        counts=dict(fiber_pieces=len(atlas.pieces),branches=len(atlas.branches),cuts=len(atlas.points))
        call=lambda sem:mod.optimize_tariff(atlas,cons,sem)
    result=dict(validation_seconds=validate,build_seconds=buildtime,counts=counts,outputs={})
    for sem in ('optimistic','pessimistic'):
        tick=time.perf_counter();out=call(sem);result[sem+'_seconds']=time.perf_counter()-tick;result['outputs'][sem]=encode(out)
    result['total_seconds']=time.perf_counter()-start
    return result

def main():
    (PAPER/'verification/stage06-author').mkdir(parents=True,exist_ok=True)
    (PAPER/'data').mkdir(parents=True,exist_ok=True)
    import numpy,scipy
    from archive_inputs import main as archive_inputs
    archive_inputs()
    sets=datasets();(PAPER/'data/stage06-instances.json').write_text(json.dumps(sets,indent=2)+'\n')
    cpu=next((line.split(':',1)[1].strip() for line in Path('/proc/cpuinfo').read_text().splitlines() if line.startswith('model name')),'unknown')
    out=dict(python=sys.version,executable=sys.executable,platform=platform.platform(),cpu=cpu,
             sympy=s.__version__,numpy=numpy.__version__,scipy=scipy.__version__,thread_environment={k:os.environ[k] for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','PYTHONHASHSEED')},threadpools="threadpoolctl unavailable; environment and forwarded HiGHS option recorded",repetitions=3,timeout_seconds=90,records=[])
    tasks=[]
    for rep in range(3):
        for name in ('jump','heterogeneous_2','heterogeneous_4','heterogeneous_6'):
            for method in (('compressed','faces') if rep%2==0 else ('faces','compressed')): tasks.append((method,name,rep))
        for method in (('original','compressed') if rep%2==0 else ('compressed','original')):tasks.append((method,'heterogeneous_12',rep))
        for name in ('heterogeneous_24','heterogeneous_48','two_types_20','two_types_200','two_types_1000'):tasks.append(('compressed',name,rep))
        for n in (100,1000,10000):tasks.append(('convex',str(n),rep))
        for n in (8,20):tasks.append(('screening',str(n),rep))
    target=PAPER/'data/stage06-results.json'
    if '--resume' in sys.argv and target.exists():out['records']=json.loads(target.read_text())['records']
    done={(r['method'],r['name'],r['repetition']) for r in out['records']}
    for method,name,rep in tasks:
        if (method,name,rep) in done:continue
        transport=PAPER/'verification/stage06-author'/f'worker-{method}-{name}-{rep}.json'
        tick=time.perf_counter();record=dict(method=method,name=name,repetition=rep)
        try:
            p=subprocess.run([sys.executable,__file__,'--worker',method,name,str(transport)],text=True,capture_output=True,timeout=90,env=os.environ.copy())
            record.update(exit_code=p.returncode,worker_wall_seconds=time.perf_counter()-tick,stderr=p.stderr,stdout=p.stdout)
            if p.returncode==0:record['result']=json.loads(transport.read_text())
            else:record['stdout']=p.stdout
        except subprocess.TimeoutExpired as err:record.update(status='timeout',worker_wall_seconds=time.perf_counter()-tick,stdout=str(err.stdout),stderr=str(err.stderr))
        out['records'].append(record);target.write_text(json.dumps(out,indent=2)+'\n')
        print(method,name,rep,record.get('exit_code',record.get('status')),round(record['worker_wall_seconds'],3),flush=True)
    source_paths=[Path(__file__),PAPER/'code/archive_inputs.py',PAPER/'data/stage06-convex-screening-inputs.json',PAPER/'code/check_full_task.py',ROOT/'code/bilevel_reopened/quadratic_tariff_benchmarks.py',PAPER/'code/compressed_solver.py',PAPER/'code/original_faces.py',PAPER/'data/stage06-instances.json',ROOT/'code/bilevel_nonconvex/scalar_solver.py',ROOT/'code/bilevel_reopened/quadratic_solver.py',ROOT/'code/bilevel_reopened/screening_milp_comparison.py',ROOT/'code/bilevel_reopened/approximate_structure_checks.py']
    out['input_hashes']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths}
    target.write_text(json.dumps(out,indent=2)+'\n')
    assert all(r.get('exit_code')==0 for r in out['records']), 'Failed or timed-out tasks retained; inspect results'
    for name in ('jump','heterogeneous_2','heterogeneous_4','heterogeneous_6','heterogeneous_12'):
        results=[r['result']['outputs'] for r in out['records'] if r['name']==name]
        for sem in ('optimistic','pessimistic'):
            first=results[0][sem]
            for result in results:
                other=result[sem]
                assert (first is None)==(other is None)
                if first is not None:assert s.simplify(s.sympify(first['value'])-s.sympify(other['value']))==0 and first['attained']==other['attained']
    print('PASS: all compared full-task exact values and attainment flags agree')

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='--worker':Path(sys.argv[4]).write_text(json.dumps(worker(sys.argv[2],sys.argv[3]))+'\n')
    else:main()
