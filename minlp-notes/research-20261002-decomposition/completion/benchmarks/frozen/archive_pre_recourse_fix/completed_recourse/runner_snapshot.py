"""Sequential frozen-source benchmarks, with separate bounded proof replay.

Use --freeze only after module owners approve source readiness, then --run LANE.
Every solver and checker process has a hard five-second wall deadline and a
512 MiB address-space limit. Solver's cooperative time budget is two seconds.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import gzip
import hashlib
import importlib
import json
import os
from pathlib import Path
import platform
import resource
import shutil
import subprocess
import sys
from time import perf_counter

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[1]/'solver'
FROZEN=HERE/'frozen'
RESULTS=HERE/'results'
THREADS=('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS')
for key in THREADS: os.environ[key]='1'
sys.path.insert(0,str(HERE))
from corpus import cases, exact_face_minimum, minimum_degree_decomposition, value


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def dump(path,obj): path.write_text(json.dumps(obj,indent=2,sort_keys=True,default=str)+'\n')
def rss():
    return int(next(line.split()[1] for line in Path('/proc/self/status').read_text().splitlines() if line.startswith('VmHWM:')))


def freeze(lane):
    target=FROZEN/lane
    if target.exists(): raise ValueError('Refusing to overwrite a frozen source snapshot: '+str(target))
    target.mkdir(parents=True)
    paths=[]
    # Copy dependencies in their original relative positions for dynamic imports.
    for directory in ('solver','conditional-messages','negative-curvature','degeneracy','constraints'):
        src=HERE.parents[1]/directory
        for path in sorted(src.glob('*.py')):
            if path.name.startswith(('check_','test_')): continue
            destination=target/directory/path.name
            destination.parent.mkdir(exist_ok=True)
            shutil.copy2(path,destination);paths.append((path,destination))
    for relative in ('completion/theory/piecewise-recourse/scalar_piecewise.py',):
        path=HERE.parents[1]/relative
        if path.exists():
            destination=target/relative
            destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(path,destination);paths.append((path,destination))
    shutil.copy2(Path(__file__),target/'runner_snapshot.py')
    shutil.copy2(HERE/'corpus.py',target/'corpus_snapshot.py')
    shutil.copy2(HERE/'constrained_cases.py',target/'constrained_cases_snapshot.py')
    shutil.copy2(HERE/'cases.json',target/'cases_snapshot.json')
    shutil.copy2(HERE/'constrained_references.json',target/'constrained_references_snapshot.json')
    dump(target/'manifest.json',{'python':sys.version,'platform':platform.platform(),
          'lane':lane,'source_sha256':{str(p.relative_to(HERE.parents[1])):digest(q) for p,q in paths},
          'runner_sha256':digest(Path(__file__)),'corpus_sha256':digest(HERE/'corpus.py'),
          'threads':1,'memory_limit_mib':512,'solver_time_limit_seconds':2,'worker_wall_limit_seconds':5})


def load_solver(lane):
    location=FROZEN/'baseline' if lane=='baseline' else FROZEN/lane/'solver'
    sys.path.insert(0,str(location))
    return importlib.import_module('certified_grid')


def make_problem(name,lane):
    started=perf_counter();p=cases()[name];module=load_solver(lane)
    dstarted=perf_counter()
    if lane=='baseline':
        bags,edges=minimum_degree_decomposition(p)
        method='archived greedy minimum degree'
    else:
        from decomposition import decompose_qp
        decomposition=decompose_qp(p.A)
        bags,edges=decomposition['bags'],decomposition['edges'];method='automatic minimum fill'
    dtime=perf_counter()-dstarted
    vstarted=perf_counter()
    problem=module.BoxQP(p.A,p.b,p.bounds,p.integers,bags,edges,constant=p.c,name=p.name)
    return p,problem,{'n':len(p.b),'decomposition_width':max(map(len,bags))-1,
                     'decomposition_method':method,'decomposition_seconds':dtime,
                     'validation_seconds':perf_counter()-vstarted,
                     'load_and_preprocessing_seconds':perf_counter()-started}


def solve_worker(args):
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    started=perf_counter()
    if args.method in ('constrained','constrained_exact','constrained_union','constrained_exact_union'):
        load_solver(args.lane)
        from constrained_cases import cases as constrained_cases
        from decomposition import build_decomposition
        from constrained_grid import ConstrainedQP
        p,kwargs=constrained_cases()[args.case]
        scopes=[(i,j) for i in range(len(p.b)) for j in range(i) if p.A[i][j]]
        scopes += [tuple(i for i,v in enumerate(row) if v) for row in kwargs['rows']]
        d=build_decomposition(len(p.b),scopes)
        metadata={'n':len(p.b),'decomposition_width':d['width'],'decomposition_method':'automatic minimum fill including constraints'}
        try:
            problem=ConstrainedQP(H=p.A,b=p.b,bounds=p.bounds,bags=d['bags'],edges=d['edges'],constant=p.c,name=p.name,**kwargs)
        except ValueError as exc:
            if args.case!='invalid_tu_input':raise
            dump(args.output,dict(metadata,case=args.case,lane=args.lane,method=args.method,
                status='input_rejected',reason=str(exc),worker_seconds=perf_counter()-started,peak_rss_kib=rss()))
            return
        metadata['load_and_preprocessing_seconds']=perf_counter()-started
    else:
        p,problem,metadata=make_problem(args.case,args.lane)
    solve_started=perf_counter()
    if args.method in ('constrained','constrained_exact','constrained_union','constrained_exact_union'):
        from constrained_grid import solve
        certificate=solve(problem,epsilon=F(1,1024),exact='exact' in args.method,time_limit=2,max_stages=256,
                          max_table_states=30000,max_exact_faces=0 if args.case=='disconnected_tu_optima' else 10000,
                          retain_unions='union' in args.method)
    elif args.method=='grid':
        from certified_grid import solve
        certificate=solve(problem,epsilon=F(1,1024),time_limit=2,max_stages=128,max_table_states=30000)
    elif args.method in ('exact','exact_no_convex'):
        from exact_output import solve_exact
        options={'convex_presolve':False} if args.method=='exact_no_convex' else {}
        certificate=solve_exact(problem,time_limit=2,max_stages=256,max_table_states=30000,max_rounds=8,**options)
    elif args.method in ('recourse','recourse_convex'):
        from recourse import solve_with_recourse
        options={}
        if args.method=='recourse_convex':
            options={'backend':'convex','blocks':[[1]] if args.case=='clipped_response' else [[1,2]],'discover':False}
        certificate=solve_with_recourse(problem,epsilon=F(1,1024),time_limit=2,max_stages=128,max_table_states=30000,**options)
    elif args.method=='endpoint_set':
        from optimal_sets import solve_endpoint_set
        certificate=solve_endpoint_set(problem,time_limit=2,max_table_states=30000)
    elif args.method=='diagonal_set':
        from optimal_sets import discover_diagonal_set
        certificate=discover_diagonal_set(problem,time_limit=2,max_trials=8,max_stages=128,max_table_states=30000)
    else: raise ValueError(args.method)
    outcome=certificate
    if args.method in ('endpoint_set','diagonal_set'):
        metadata.update({key:outcome[key] for key in ('trials','table_states','reason') if key in outcome})
        if 'certificate' not in outcome:
            metadata.update(case=args.case,lane=args.lane,method=args.method,status=outcome['status'],
                            solve_seconds=perf_counter()-solve_started,worker_seconds=perf_counter()-started,peak_rss_kib=rss())
            dump(args.output,metadata)
            return
        certificate=outcome['certificate']
    assert certificate['problem']==problem.to_dict(), 'Certificate describes another input model'
    metadata['certificate_input_bound']=True
    metadata.update({'case':args.case,'lane':args.lane,'method':args.method,'solve_seconds':perf_counter()-solve_started,
                     'status':outcome.get('status'),'certificate_schema':certificate.get('schema')})
    for key in ('point','lower','upper','gap','stats','minimum','value'):
        if key in certificate: metadata[key]=certificate[key]
    if certificate.get('point') is not None and certificate.get('upper') is not None:
        point=tuple(map(F,certificate['point']))
        assert problem.feasible(point)
        assert value(p,point)==F(certificate['upper'])
        metadata['independent_objective_checked']=True
    if 'minimum' in certificate:
        point=tuple(map(F,certificate['point']))
        assert problem.feasible(point) and value(p,point)==F(certificate['minimum'])
        metadata['independent_objective_checked']=True
        metadata['lower']=metadata['upper']=certificate['minimum']
        metadata['gap']='0'
    certpath=args.output.with_suffix('.certificate.json.gz')
    with gzip.open(certpath,'wt') as stream:json.dump(certificate,stream)
    metadata.update({'certificate_file':certpath.name,'certificate_bytes_gzip':certpath.stat().st_size,
                     'worker_seconds':perf_counter()-started,'peak_rss_kib':rss()})
    dump(args.output,metadata)


def check_worker(args):
    resource.setrlimit(resource.RLIMIT_AS,(512*1024**2,512*1024**2))
    started=perf_counter();load_solver(args.lane)
    with gzip.open(args.certificate,'rt') as stream:certificate=json.load(stream)
    check_started=perf_counter()
    if args.method in ('constrained','constrained_exact','constrained_union','constrained_exact_union'):
        from verify_constrained import verify
        checked=verify(certificate)
    elif args.method in ('recourse','recourse_convex'):
        from verify_recourse import verify_pipeline
        checked=verify_pipeline(certificate)
    elif args.method in ('endpoint_set','diagonal_set'):
        from verify_optimal_sets import verify_certificate
        checked=verify_certificate(certificate)
        from verify_optimal_sets import contains
        name=certificate['problem']['name']
        membership_cases={
            'flat_diagonal':[(['0']*4,True),(['1/2']*4,True),(['1','0','0','0'],False)],
            'tilted_disconnected':[(['0','0','0'],True),(['1/2','1/2','0'],True),(['0','1/2','1'],True),(['1/2','1','1'],True),(['0','1/4','1/2'],False)],
            'false_growth_trap':[(['1','1'],True),(['0','0'],False)],
            'endpoint_branch_8':[(['-1']*7+['0'],True),(['1']*7+['2'],True),(['1']*7+['1/2'],False),(['0']*8,False)]}
        count=0
        for point,expected in membership_cases.get(name,[(certificate['point'],True)]):
            assert contains(certificate,tuple(map(F,point)))==expected,(name,point,expected)
            count+=1
        checked['membership_examples_checked']=count
    else:
        from verify_certificate import verify_certificate
        checked=verify_certificate(certificate)
    dump(args.output,{'certificate_check':checked,'check_seconds':perf_counter()-check_started,
                      'checker_worker_seconds':perf_counter()-started,'checker_peak_rss_kib':rss()})


def launch(command):
    started=perf_counter()
    try:
        process=subprocess.run(command,capture_output=True,text=True,timeout=5,env=dict(os.environ))
        return {'returncode':process.returncode,'seconds':perf_counter()-started,
                'stderr':process.stderr[-4000:] if process.returncode else ''}
    except subprocess.TimeoutExpired:
        return {'returncode':None,'seconds':perf_counter()-started,'stderr':'hard worker wall limit'}


def configurations(lane):
    if lane in ('baseline','completed_grid'):
        names=['fresh_path_5','fresh_width2_6','fresh_mixed_5','random_tree_7','fresh_path_5_shuffled',
               'fresh_path_16','fresh_path_32','fresh_path_64','random_tree_32','rational_face','mixed_rational',
               'flat_diagonal','affine_star_5_shuffled','affine_star_17_shuffled','QPLIB_3852','QPLIB_5881']
        return [(name,'grid') for name in names]
    if lane=='completed_exact':
        return [(name,'exact') for name in ('fresh_path_5','fresh_width2_6','fresh_mixed_5','rational_face',
                                            'mixed_rational','flat_diagonal','clipped_response','false_growth_trap')]+[('rational_face','exact_no_convex')]
    if lane=='completed_recourse':
        return [(name,'recourse_convex') for name in ('clipped_response','piecewise_convex_1','piecewise_convex_100')]+[(name,'recourse') for name in ('affine_star_5_shuffled','affine_star_17_shuffled','singular_affine',
                                               'clipped_response','dense_mincut_7','dense_mincut_33','fresh_path_5','QPLIB_3852')]
    if lane=='completed_constraints':
        return [('disconnected_tu_optima',method) for method in ('constrained','constrained_union','constrained_exact','constrained_exact_union')]+[(name,method) for name in ('network_mixed_5','ordered_nonconvex_4','weighted_integer_column',
               'large_equality_energy_full','large_equality_energy_projected','infeasible_flow','invalid_tu_input')
               for method in (('constrained',) if name in ('infeasible_flow','invalid_tu_input') else ('constrained','constrained_exact'))]
    if lane=='completed_sets':
        return [(name,'diagonal_set') for name in ('flat_diagonal','tilted_disconnected','false_growth_trap','fresh_path_5')]+[('endpoint_branch_8','endpoint_set')]
    raise ValueError(lane)


def run(lane):
    RESULTS.mkdir(exist_ok=True)
    outputs=[];reference=json.loads((HERE/'cases.json').read_text())
    if lane=='completed_constraints':
        reference={k:{'exact_reference':v} for k,v in json.loads((HERE/'constrained_references.json').read_text()).items()}
    watched=[Path(__file__),HERE/'corpus.py',HERE/'constrained_cases.py']
    watched += sorted((FROZEN/lane).rglob('*.py'))
    watched += sorted((FROZEN/'baseline').rglob('baseline_corpus.py'))
    watched += sorted((FROZEN/'baseline'/'data').glob('*'))
    watched += [HERE/'cases.json',HERE/'constrained_references.json']
    watched=list(dict.fromkeys(watched))
    before={str(p.relative_to(HERE)):digest(p) for p in watched}
    dump(RESULTS/(lane+'_run_manifest.json'),{'source_sha256':before,'time_limit_seconds':2,'worker_wall_limit_seconds':5,'threads':1,'memory_limit_mib':512})
    for name,method in configurations(lane):
        tag=f'{lane}__{name}__{method}';out=RESULTS/(tag+'.json')
        if out.exists():raise ValueError('Refusing to overwrite published run '+str(out))
        base=[sys.executable,str(Path(__file__).resolve()),'--lane',lane,'--method',method]
        run_result=launch(base+['--worker','--case',name,'--output',str(out)])
        if run_result['returncode']!=0:
            row={'case':name,'lane':lane,'method':method,'status':'worker_wall_limit' if run_result['returncode'] is None else 'worker_failed',
                 'worker_stderr':run_result['stderr']}
        else:row=json.loads(out.read_text())
        row['solve_subprocess_seconds']=run_result['seconds']
        if 'certificate_file' in row:
            checkpath=out.with_suffix('.check.json');certpath=out.parent/row['certificate_file']
            result=launch(base+['--check','--certificate',str(certpath),'--output',str(checkpath)])
            if result['returncode']==0:
                row.update(json.loads(checkpath.read_text()));checkpath.unlink()
            else:
                row['certificate_check']='worker_wall_limit' if result['returncode'] is None else 'worker_failed'
                row['checker_stderr']=result['stderr']
            row['check_subprocess_seconds']=result['seconds']
        if 'exact_reference' in reference[name] and reference[name]['exact_reference']['objective'] is not None:
            optimum=F(reference[name]['exact_reference']['objective']);row['exact_reference']=str(optimum)
            if row.get('lower') is not None and row.get('upper') is not None:
                assert F(row['lower'])<=optimum<=F(row['upper']),(tag,row,optimum)
                row['exact_reference_enclosed']=True
        row['total_subprocess_seconds']=row['solve_subprocess_seconds']+row.get('check_subprocess_seconds',0)
        dump(out,row);outputs.append(row)
        print(name,method,row['status'],row.get('certificate_check'),flush=True)
    after={str(p.relative_to(HERE)):digest(p) for p in watched}
    assert before==after, 'Benchmark or frozen sources changed during run'
    dump(RESULTS/(lane+'.json'),outputs)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--freeze');parser.add_argument('--run')
    parser.add_argument('--worker',action='store_true');parser.add_argument('--check',action='store_true')
    parser.add_argument('--lane');parser.add_argument('--case');parser.add_argument('--method')
    parser.add_argument('--output',type=Path);parser.add_argument('--certificate',type=Path)
    args=parser.parse_args()
    if args.freeze:freeze(args.freeze)
    elif args.run:run(args.run)
    elif args.worker:solve_worker(args)
    elif args.check:check_worker(args)
    else:parser.error('choose --freeze, --run, --worker, or --check')
if __name__=='__main__':main()
