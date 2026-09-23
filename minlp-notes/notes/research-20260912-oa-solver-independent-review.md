# Independent review of the scalar Markov OA solvers and comparison

Date: 2026-09-12. Reviewed [markov_design.py](../code/research_20260912/markov_design.py), [compare_solvers.py](../code/research_20260912/compare_solvers.py), [initial_comparison.json](../code/research_20260912/results/initial_comparison.json), and [strengthened_comparison.json](../code/research_20260912/results/strengthened_comparison.json). This review made no implementation changes and did not repeat the [separate path-oracle audit](research-20260912-path-oracle-independent-review.md).

The two integer formulations, dense gradient, tangent directions, full-selection bound, and added continuous-root phase are correct for the stated fixed-covariance model. Independent enumeration found no wrong successful selection or substantive bound violation in the small tests or saved benchmarks. One reporting defect remains: the comparison script does not save exceptions or the current partial case when a solve raises. The numerical checks also demonstrate why the documented floating-point qualification matters for almost singular covariance matrices.

The reviewed SHA-256 hashes are:

```text
markov_design.py  8d470c16258c97cb50fed6090733b07440571550eaad74766fa032cb615fdcf9
compare_solvers.py a73408cb95a61362ddc74b8476322c744e3fd5b3f57d9464642a0659ca3ffef4
path_oracle.py    61daa250ec278fa2b4770ecd7f2a317d0cf6ffc62002c1cdafd45b0197d9340b
```

The strengthened JSON records these same hashes. The initial JSON has no source hashes, so its endpoints can be checked independently but its exact historical implementation cannot be reconstructed from that file alone.

The model selects exactly `k` scalar observations from one or more independent stationary AR(1) chains, with a common parameter vector, fixed sensitivities, fixed known covariance parameters, and a positive-definite prior information matrix. Its objective is `logdet(prior + sum F_selected.T @ inverse(R_selected) @ F_selected)`. This is the original selected-data Gaussian mean-information objective when sensitivities are derivatives of the mean and covariance is parameter-independent. The reaction example is a local design at specified nominal rates. It does not include information from unknown covariance parameters or integrate uncertainty in the nominal kinetic parameters. The fixed prior is an explicit information contribution or regularizer.

For the path formulation, the first selected observation contributes `f_j f_j.T / sigma**2`. A subsequent selected pair `i<j` contributes `(f_j-rho**(j-i)*f_i)(...).T / (sigma**2*(1-rho**(2*(j-i))))`. These are the conditional innovations of the marginal selected process; skipped candidates are not treated as observed. Each chain has its own unit source-to-sink flow, including the empty path, and all chains share only the cardinality constraint and summed information. A nonnegative unit flow decomposes into ordered paths. Binary visits force every positive-weight path to have the same visited set, and the order fixes that path uniquely. Continuous arcs therefore suffice for integer exactness. The chain offsets and empty selections were checked independently. Chains themselves must be nonempty; `k=0` is supported.

For the dense formulation, each block uses `a=split_fraction*lambda_min(R)`, `S=R-a I`, `D=diag(z)/a`, and `V=(I+S D)^(-1) F`. Its information contribution `F.T D V` is symmetric despite the nonsymmetric linear system. For positive visits this is equivalently `F.T @ inverse(R+a*diag(1/z-1)) @ F`; its continuous extension to zero visits is well defined. At binary visits it gives exactly the selected principal-submatrix information. The derivative in visit `i` is `V[i].T V[i]/a` as a parameter-information matrix, so the logdet derivative is `V[i] @ inverse(J) @ V[i].T / a`. This matches the implementation. The extension is matrix-concave, and logdet is concave and increasing on positive-definite matrices. Thus `t <= value(x) + gradient(x) @ (variables-x)` is a global upper tangent for both formulations. Increasing the fixed scalar split toward one decreases fractional information and strengthens this dense relaxation; `.99` retains binary exactness. This is a check of the implemented Liu extension, not a new formulation claim.

The bound logic is sound in exact arithmetic. Adding observations cannot decrease information, so the full-selection objective bounds every subset. It also bounds convex combinations of path information and the monotone dense extension on `[0,1]^n`. Tangents at the full selection remain valid even though that selection need not satisfy the requested cardinality. A solved LP root master bounds the integer optimum; a MIP master's global `ObjBound` remains an upper bound on time-limited runs. Taking the minimum of these bounds is valid. The root phase retains its cuts when visit variables become binary again, rounds visits to an actual size-`k` subset, and evaluates that subset through the original covariance system. It charges its work to the same deadline. An unfinished root phase can fall back to the previously established bound and seed.

Integer lower bounds use only an actual size-`k` subset evaluated through the original dense covariance system. A master hypograph value or fractional root value never becomes an integer lower bound. Continuous results instead report `relaxation_value` and leave `lower_bound` and `selected` null. Root and outer-round limits can return useful incomplete results. For example, `max_rounds=0` with nonzero root rounds may return `iteration_limit` even when the root already closes the integer gap; this is a conservative status, not a false success. `max_rounds` limits the integer phase separately from `root_rounds`.

Fresh checks used one Gurobi thread and one BLAS/OpenMP thread. The independent reference assembled selected covariance matrices and used Cholesky whitening, rather than calling the implementation's reference objective. The reproducible scripts below performed:

- 1,254 information-matrix comparisons over every subset of four cases with one to three chains; chain lengths included one, correlations included zero, negative values, and `.9999`, and chain noise scales differed. The largest relative discrepancy was `2.61e-12`.
- 96 finite-difference gradient checks, with largest relative discrepancy `1.08e-7`; 10,128 global tangent inequalities, with no positive violation; and 48 checks that `.99` gives no larger fractional information than `.5`.
- 150 integer and 39 continuous solves over cardinalities zero, one, half, and full selection; six additional random two-chain cases; `root_rounds=0/20`; dense splits `.5/.99`; round caps zero and one; and deadlines as small as `1e-9` seconds. All returned integer selections had the required cardinality and valid original objectives. All tested continuous visits satisfied their box and cardinality constraints within `1e-7`. The largest upper-bound undershoot relative to independent enumeration was `1.71e-12`, and the largest incumbent objective discrepancy was `1.77e-12`.
- 24 additional ten-candidate integer solves with `.12`-second budgets, both root settings, both dense splits, and correlations `.9`, `-.99`, `.999999`, and `.9999999999`. These returned 22 time limits and two successful path solves. No returned successful selection missed the independently enumerated optimum.

The 213 fresh OA calls used about 6.10 seconds cumulatively. Every assigned per-solve budget was at most `.5` seconds, and the largest observed call took `.258` seconds. Including both solve batches, statuses were 165 `optimal_tolerance`, 39 `time_limit`, and nine `iteration_limit`. These counts include deliberately trivial and capped cases; they are verification evidence, not a runtime study.

The stress case at `rho=.9999999999` had covariance condition number about `1.95e11`. Its LU-based original objective differed from independent Cholesky evaluation by up to `1.70e-6`, larger than the requested `1e-7` gap. Those runs remained time-limited with ample positive bounds. This does not identify a failed mathematical formulation, but it rules out interpreting the requested tolerance as an arithmetic guarantee over all accepted inputs. The implementation computes the final formulation residual but does not use it to reject success. Bound contradictions smaller than `1e-7*(1+abs(incumbent))` can also be accepted and the displayed gap is clipped at zero. Consequently, very small requested gaps need a numerical qualification even when the status says `optimal_tolerance`.

The continuous solver clips individual variables to `[0,1]` before objective evaluation; this is not a full projection onto its equality constraints. The tests found no material feasibility error, but returned continuous values rely on the LP feasibility tolerance. For the path relaxation, `fractional_visits` alone does not identify the complete arc flow or its information matrix, so the saved JSON does not contain enough information to independently reconstruct that particular fractional value. These qualifications do not affect the independently checked integer subset lower bounds.

The comparison's stated intent to “save every limit and failure” exceeds what [compare_solvers.py](../code/research_20260912/compare_solvers.py) implements. It appends a case and writes the report only after all five methods return. There is no exception handler around solver calls, oracle evaluations, enumeration, or original-objective checks. A synthetic exception on the sixth OA call propagated, left the first completed case saved, and discarded the current case's already completed first solve. A failure in the first case would leave no new report. This is a confirmed persistence defect, not an observed exception in the supplied benchmark. A robust comparison should record each completed solve immediately and represent recoverable solver/evaluation exceptions explicitly before proceeding; alternatively its documentation must limit the claim to returned solver-status failures.

Independent enumeration also checked all eight saved instances, including all 42,504 size-five subsets for each 24-candidate case: 173,184 subsets in total. All 80 saved solve records had valid numerical upper bounds relative to those optima. Every reported successful integer result attained the corresponding optimum. Every integer incumbent had the specified cardinality and its saved objective agreed with independent evaluation within `8.89e-15`; the largest saved upper-bound undershoot was `1.78e-15`.

| Instance | Independently enumerated optimal logdet |
| --- | ---: |
| generic, `n=12`, `rho=.4` | 4.547171306342710 |
| generic, `n=12`, `rho=.9` | 9.276613138241770 |
| reaction, `n=12`, `rho=.4` | 11.575190891562592 |
| reaction, `n=12`, `rho=.9` | 13.374524519296482 |
| generic, `n=24`, `rho=.4` | 6.053545801674002 |
| generic, `n=24`, `rho=.9` | 10.340625152634674 |
| reaction, `n=24`, `rho=.4` | 11.823158637761950 |
| reaction, `n=24`, `rho=.9` | 12.236299252034993 |

The observed performance statement is narrow but supported. Initial integer dense OA closed two of eight cases, strengthened dense OA closed three, and both path implementations closed all eight in each report. In the strengthened run, path OA took `.012–.305` seconds and the count-path method `.002–.028` seconds; dense OA left five time limits. The strengthened split/root settings improved several dense bounds and incumbents while leaving five cases unresolved. These are single-run observations.

This is not a general ranking of dense conic formulations, commercial solvers, or all path methods. There are only eight fixed single-chain cases, one generic seed, three parameters, and cardinality five. The same generic sensitivity sample is reused across correlations; the 12-candidate generic data are the prefix of the 24-candidate data. The reaction family is one nominal kinetic model. Increasing its grid size while fixing correlation per index changes correlation as a function of physical time. No multichain runtime benchmark, scaling distribution, or statistical replication is present.

The stronger comparison changes two choices together: dense split `.5` to `.99`, and integer root-cut initialization from zero to at most 200 rounds for both formulations. It therefore cannot attribute the integer improvement to either choice separately. Dense continuous OA also remains capped at 500 rounds: it hits that cap on four initial and three strengthened cases in roughly `.4` seconds, well before the five-second budget. These unfinished values are accompanied by valid upper bounds, but should not be labeled exact relaxation optima. The count-path method optimizes over mixtures of exactly size-`k` paths; the unlayered path relaxation only fixes the mixture's expected cardinality. Its potentially stronger bound and different pricing/branching implementation are both part of the comparison. The count-path timer also excludes construction of its `scalar_markov` data, whereas OA timing includes oracle construction; this matters when comparing millisecond results. The report records Gurobi thread count but not BLAS thread configuration or CPU details, although the documented strengthened command fixes the BLAS/OpenMP threads.

The existing Lee–Gómez–Atamtürk path-hull priority correction remains applicable. Nothing in this implementation review establishes a new path-hull theorem or a novelty claim. The initial [implementation note](research-20260912-measurement-implementation.md) describes a fixed half-eigenvalue split and no integer root initialization; those statements should be read as historical facts about the initial prototype, since the reviewed APIs now support both options.

The four Python blocks below reproduce the checks and write detailed JSON to `/tmp`; they do not edit the reviewed modules. Run them in order using the extractor below. The first block snapshots the reviewed OA module and prints its hash, so a rerun against later code is distinguishable. Wall times and the number of completed rounds may vary.

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python - <<'PY'
from pathlib import Path
import re, runpy
note = Path('notes/research-20260912-oa-solver-independent-review.md').read_text()
for index, block in enumerate(re.findall(r'```python\n(.*?)\n```', note, re.S), 1):
    script = Path(f'/tmp/oa-independent-review-{index}.py')
    script.write_text(block)
    runpy.run_path(str(script), run_name='__main__')
PY
```

```python
from __future__ import annotations
import hashlib, importlib.util, itertools, json, pathlib, sys, time
import numpy as np

base = pathlib.Path('/home/sgusev/repo/minlp-notes')
source = base/'code/research_20260912/markov_design.py'
raw = source.read_bytes()
snapshot = pathlib.Path('/tmp/oa_review_markov_design.py'); snapshot.write_bytes(raw)
spec = importlib.util.spec_from_file_location('review_oa', snapshot)
m = importlib.util.module_from_spec(spec); sys.modules[spec.name] = m; spec.loader.exec_module(m)
rng = np.random.default_rng(692173)
report = {'source_sha256':hashlib.sha256(raw).hexdigest(), 'counts':{}, 'max_errors':{}, 'solves':[], 'issues':[]}
counts=report['counts']; errors=report['max_errors']

def count(key): counts[key]=counts.get(key,0)+1

def record_error(key, value): errors[key]=max(errors.get(key,0.),float(value))

def independent_info(design, selected):
    J=design.prior.copy(); offset=0
    for chain in design.chains:
        ix=[i-offset for i in selected if offset<=i<offset+len(chain.F)]
        if ix:
            R=np.array([[chain.sigma**2*chain.rho**abs(i-j) for j in ix] for i in ix])
            A=np.linalg.cholesky(R)
            W=np.linalg.solve(A,chain.F[ix])
            J+=W.T@W
        offset+=len(chain.F)
    return J

def objective(design, selected):
    J=independent_info(design,selected)
    return float(2*np.log(np.diag(np.linalg.cholesky(J))).sum())

def optimum(design):
    return max((objective(design,s),s) for s in itertools.combinations(range(design.n),design.k))

# Every subset, gradient directions, and global support inequalities on multi-chain data.
bases=[]
for lengths,rhos,sigmas in [([1],[-.9],[.7]),([2,3],[.8,-.6],[.4,1.7]),([1,2,4],[0.,-.97,.9999],[.2,2.,.07]),([4,4],[-.4,.9],[1.,.5])]:
    chains=tuple(m.Chain(rng.normal(size=(n,3)),rho,sigma) for n,rho,sigma in zip(lengths,rhos,sigmas))
    B=rng.normal(size=(3,3)); d=m.Design(chains,B.T@B+.3*np.eye(3),sum(lengths)//2)
    bases.append(d)
    subsets=[s for k in range(d.n+1) for s in itertools.combinations(range(d.n),k)]
    for oracle in [m.PathOracle(d),m.DenseOracle(d,.5),m.DenseOracle(d,.99)]:
        points=[oracle.subset_point(s) for s in subsets]
        for s,point in zip(subsets,points):
            expected=independent_info(d,s); actual=oracle.information(point)
            err=np.linalg.norm(actual-expected)/max(1,np.linalg.norm(expected))
            record_error('information_relative',err);count('subset_information')
            assert err<2e-9,(type(oracle).__name__,s,err)
        for _ in range(8):
            ids=rng.choice(len(points),size=min(5,len(points)),replace=False)
            weights=rng.dirichlet(np.ones(len(ids)))
            x=sum(w*points[i] for i,w in zip(ids,weights))
            y=sum(w*points[i] for i,w in zip(ids,rng.dirichlet(np.ones(len(ids)))))
            v,g=oracle.value_gradient(x); direction=y-x; h=1e-5
            fd=(oracle.value_gradient(x+h*direction)[0]-oracle.value_gradient(x-h*direction)[0])/(2*h)
            err=abs(fd-g@direction)/max(1,abs(fd))
            record_error('gradient_relative',err);count('gradient_directions')
            assert err<2e-6,(type(oracle).__name__,err)
            for point in [*points,y]:
                excess=oracle.value_gradient(point)[0]-(v+g@(point-x))
                record_error('tangent_excess',excess);count('tangent_checks')
                assert excess<2e-7,excess
    for _ in range(12):
        z=rng.uniform(size=d.n)
        jhalf=m.DenseOracle(d,.5).information(z);jnear=m.DenseOracle(d,.99).information(z)
        eig=np.linalg.eigvalsh(jhalf-jnear)[0]
        assert eig>-1e-6
        count('split_monotonicity')

# Independent solver checks, with a cumulative budget below the assigned 60 seconds.
solver_seconds=0.
def run(design, formulation, integer=True, **options):
    global solver_seconds
    if solver_seconds>48: raise RuntimeError('review solver budget exhausted')
    exact,selection=optimum(design)
    f=m.solve_oa if integer else m.solve_relaxation
    opts=dict(time_limit=.5,absolute_gap=1e-7,max_rounds=150);opts.update(options)
    started=time.perf_counter();result=f(design,formulation,**opts);solver_seconds+=time.perf_counter()-started
    row={'chains':[len(c.F) for c in design.chains],'rhos':[c.rho for c in design.chains], 'exact':exact,'options':opts,**m.asdict(result)}
    report['solves'].append(row);count('integer_solves' if integer else 'continuous_solves')
    tol=2e-7*(1+abs(exact))
    assert result.upper_bound>=exact-tol,row
    if integer:
        assert len(result.selected)==design.k and len(set(result.selected))==design.k,row
        lb=objective(design,result.selected)
        assert abs(lb-result.lower_bound)<tol,row
        assert result.lower_bound<=exact+tol,row
        if result.status=='optimal_tolerance': assert exact-result.lower_bound<=opts['absolute_gap']+tol,row
        record_error('integer_objective_absolute',abs(lb-result.lower_bound))
        record_error('upper_underestimate',exact-result.upper_bound)
    else:
        assert result.lower_bound is None and result.selected is None,row
        visits=np.array(result.fractional_visits)
        assert abs(visits.sum()-design.k)<1e-7 and visits.min()>=-1e-7 and visits.max()<=1+1e-7,row
        assert result.relaxation_value<=result.upper_bound+tol,row
        if formulation=='dense':
            val=m.DenseOracle(design,opts.get('split_fraction',.5)).value_gradient(visits)[0]
            assert abs(val-result.relaxation_value)<tol,row
    return result

configs=[('path',0,.5),('path',20,.5),('dense',0,.5),('dense',20,.5),('dense',0,.99),('dense',20,.99)]
for template in bases:
    for k in sorted(set([0,1,template.n//2,template.n])):
        design=m.Design(template.chains,template.prior,k)
        for formulation,root,split in configs:
            run(design,formulation,root_rounds=root,split_fraction=split)
        if k in (0,template.n,template.n//2):
            for formulation,split in [('path',.5),('dense',.5),('dense',.99)]:
                run(design,formulation,False,split_fraction=split,time_limit=.2)
for seed in range(6):
    rr=np.random.default_rng(913+seed)
    design=m.Design((m.Chain(rr.normal(size=(3,2)),rr.uniform(-.98,.98),.5),m.Chain(rr.normal(size=(4,2)),rr.uniform(-.98,.98),1.3)),np.diag([.02,2.]),3)
    for formulation,root,split in configs:run(design,formulation,root_rounds=root,split_fraction=split,time_limit=.3)

small=m.Design(bases[1].chains,bases[1].prior,2)
for formulation,root,split in configs:
    for options in [dict(time_limit=1e-9),dict(time_limit=.0001),dict(time_limit=.005),dict(max_rounds=0),dict(max_rounds=1)]:
        run(small,formulation,root_rounds=root,split_fraction=split,**options)
for formulation,split in [('path',.5),('dense',.99)]:
    for limit in [1e-9,.0001,.005]:run(small,formulation,False,split_fraction=split,time_limit=limit)

report['solver_seconds']=solver_seconds
report['source_unchanged']=source.read_bytes()==raw
report['status_counts']={s:sum(r['status']==s for r in report['solves']) for s in sorted({r['status'] for r in report['solves']})}
pathlib.Path('/tmp/oa_solver_independent_results.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='solves'},indent=2))
```

```python
import itertools,json,pathlib,time
import numpy as np
base=pathlib.Path('/home/sgusev/repo/minlp-notes/code/research_20260912/results')
reports={name:json.loads((base/name).read_text()) for name in ['initial_comparison.json','strengthened_comparison.json']}
results={'cases':[], 'checks':0,'max_objective_residual':0.,'max_upper_underestimate':0.}
started=time.perf_counter()
for initial,strong in zip(reports['initial_comparison.json']['cases'],reports['strengthened_comparison.json']['cases']):
    for key in ['family','n','p','k','rho','seed','data']:assert initial[key]==strong[key],key
    c=strong;F=np.array(c['data']['sensitivity']);prior=np.array(c['data']['prior']);sigma=c['data']['sigma'];n=c['n']
    R=sigma**2*c['rho']**np.abs(np.subtract.outer(np.arange(n),np.arange(n)))
    def value(s):
        i=list(s);A=np.linalg.cholesky(R[np.ix_(i,i)]);W=np.linalg.solve(A,F[i]);J=prior+W.T@W
        return float(2*np.log(np.diag(np.linalg.cholesky(J))).sum())
    exact,selection=max((value(s),s) for s in itertools.combinations(range(n),c['k']))
    result={'case':[c['family'],n,c['rho']],'exact':exact,'selection':selection,'enumerated_subsets':__import__('math').comb(n,c['k'])}
    for name,record in [('initial',initial),('strengthened',strong)]:
        if 'enumeration' in record:assert abs(exact-record['enumeration'][0])<1e-9
        for solve in record['solves']:
            upper=solve.get('upper_bound',solve.get('upper'))
            assert upper>=exact-1e-8,(result,name,solve)
            results['max_upper_underestimate']=max(results['max_upper_underestimate'],exact-upper)
            if solve.get('integer') or solve['formulation']=='count_path_oracle':
                s=solve.get('selected',solve.get('path'));assert len(s)==c['k'] and len(set(s))==c['k']
                independently_evaluated=value(s);lower=solve.get('lower_bound',solve.get('lower'))
                err=abs(independently_evaluated-lower);assert err<1e-8
                results['max_objective_residual']=max(results['max_objective_residual'],err)
                if solve['status'] in ['optimal','optimal_tolerance']:assert exact-lower<1e-6+1e-8
            else:
                assert solve['lower_bound'] is None and solve['selected'] is None
                z=np.array(solve['fractional_visits']);assert abs(z.sum()-c['k'])<1e-7
            results['checks']+=1
    results['cases'].append(result)
results['wall_seconds']=time.perf_counter()-started
pathlib.Path('/tmp/oa_benchmark_independent_results.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
```

```python
import importlib.util,itertools,json,pathlib,sys,time
import numpy as np
spec=importlib.util.spec_from_file_location('review_limits','/tmp/oa_review_markov_design.py');m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
rows=[];solver_seconds=0.
for seed,rho in [(193,.9),(725,-.99),(12,.999999),(15,.9999999999)]:
    rng=np.random.default_rng(seed);F=rng.normal(size=(10,3));prior=.1*np.eye(3)
    d=m.Design((m.Chain(F,rho,.7),),prior,4)
    R=.7**2*rho**np.abs(np.subtract.outer(np.arange(10),np.arange(10)))
    def obj(s):
        ix=list(s);A=np.linalg.cholesky(R[np.ix_(ix,ix)]);W=np.linalg.solve(A,F[ix]);J=prior+W.T@W
        return float(2*np.log(np.diag(np.linalg.cholesky(J))).sum())
    exact,optimal=max((obj(s),s) for s in itertools.combinations(range(10),4))
    for formulation,split in [('path',.5),('dense',.5),('dense',.99)]:
        for root in [0,20]:
            opts=dict(time_limit=.12,max_rounds=500,root_rounds=root,split_fraction=split,absolute_gap=1e-7)
            started=time.perf_counter();row={'seed':seed,'rho':rho,'condition_R':float(np.linalg.cond(R)),'exact':exact,'options':opts}
            try:
                sol=m.solve_oa(d,formulation,**opts);row.update(m.asdict(sol))
                independent=obj(sol.selected)
                row['independent_incumbent']=independent;row['upper_minus_exact']=sol.upper_bound-exact;row['lower_residual']=sol.lower_bound-independent
                row['false_success']=sol.status=='optimal_tolerance' and exact-independent>opts['absolute_gap']+1e-8
            except Exception as exc:row.update(exception=type(exc).__name__,message=str(exc),formulation=formulation)
            solver_seconds+=time.perf_counter()-started;rows.append(row)
report={'solver_seconds':solver_seconds,'solves':rows}
pathlib.Path('/tmp/oa_limits_scale_results.json').write_text(json.dumps(report,indent=2))
print('solver_seconds',solver_seconds)
for r in rows:
 print(r['rho'],r['formulation'],r['options']['split_fraction'],r['options']['root_rounds'],r.get('status',r.get('exception')),'gap',r.get('absolute_gap'),'UB-exact',r.get('upper_minus_exact'),'residual',r.get('lower_residual'),'false',r.get('false_success'))
```

```python
import contextlib,importlib.util,io,json,pathlib,sys
from dataclasses import dataclass
base=pathlib.Path('/home/sgusev/repo/minlp-notes/code/research_20260912');sys.path.insert(0,str(base))
spec=importlib.util.spec_from_file_location('review_comparison',base/'compare_solvers.py');m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
@dataclass
class Result:
    formulation:str
    integer:bool
    status:str='injected_stub'
    wall_seconds:float=0.
    absolute_gap:float=0.
calls=0
def stub(design,formulation,integer,**options):
    global calls
    calls+=1
    if calls==6:raise ArithmeticError('Injected evaluation failure')
    return Result(formulation,integer)
m.solve_oa=lambda d,f,**kw:stub(d,f,True,**kw)
m.solve_relaxation=lambda d,f,**kw:stub(d,f,False,**kw)
m.solve_branch_bound=lambda d,k,**kw:dict(path=(),status='injected_stub',lower=0.,upper=0.)
path=pathlib.Path('/tmp/oa_injected_failure_report.json');path.unlink(missing_ok=True)
sys.argv=['compare_solvers.py','--output',str(path),'--sizes','1','--seconds','.01']
try:
    with contextlib.redirect_stdout(io.StringIO()):m.main()
except ArithmeticError as exc:
    report=json.loads(path.read_text())
    result={'exception_propagated':str(exc),'completed_cases_saved':len(report['cases']),'current_partial_case_saved':False,'calls_before_abort':calls}
else:raise AssertionError('Injected error unexpectedly caught')
pathlib.Path('/tmp/oa_report_failure_results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
```

Follow-up verification on 2026-09-12: the comparison driver now fixes the solve-exception persistence defect identified above. This follow-up reviews only that change; the OA and path-oracle hashes and all earlier solver/benchmark evidence remain as recorded. The updated `compare_solvers.py` SHA-256 is `bccdbb2916f10c67a26ffd0ab1cd9d1c4ab3a163e5bd80f758b900bbc79a2909`. The supplied strengthened benchmark still records the earlier driver hash and has not been represented as a rerun of the updated driver.

The same synthetic exception on the sixth OA call is now saved with its exception type and message. The current case retains its preceding successful solve, and the driver continues through the remaining methods and cases. Additional injections into the count-path solver and its original-objective evaluation were also recorded correctly. The final JSON contained all four cases, all 20 solve records, and the three intended exception records. Twenty checks made from inside the stubs confirmed that the case and earlier OA solve results were already on disk before the next call. The final case completed normally. These checks made no actual solver calls and did not modify the driver.

This verifies exception handling for the wrapped OA calls, count-path calls, and count-path original-objective evaluation. Input construction, `scalar_markov` preparation, enumeration, serialization, and filesystem errors remain outside those handlers; the broad phrase “every failure” should therefore still be read with that scope. The persistence fix does not change solver formulas, numerical bound qualifications, or conclusions about the saved benchmark.

The fourth Python block above preserves the historical reproducer and expects the earlier driver to propagate its injected exception. For the current driver, run only the final Python block with this command; it writes `/tmp/oa_report_failure_fixed_results.json` and the complete injected report.

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 uv run --project code/research_20260912 python - <<'PYCODE'
from pathlib import Path
import re, runpy
note = Path('notes/research-20260912-oa-solver-independent-review.md').read_text()
block = re.findall(r'```python\n(.*?)\n```', note, re.S)[-1]
script = Path('/tmp/oa-independent-review-followup.py')
script.write_text(block)
runpy.run_path(str(script), run_name='__main__')
PYCODE
```

```python
import contextlib,hashlib,importlib.util,io,json,pathlib,sys
from dataclasses import dataclass
base=pathlib.Path('/home/sgusev/repo/minlp-notes/code/research_20260912');sys.path.insert(0,str(base))
source=base/'compare_solvers.py';raw=source.read_bytes()
spec=importlib.util.spec_from_file_location('review_comparison_fixed',source);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
@dataclass
class Result:
    formulation:str
    integer:bool
    status:str='injected_stub'
    wall_seconds:float=0.
    absolute_gap:float=0.
path=pathlib.Path('/tmp/oa_injected_failure_fixed_report.json');path.unlink(missing_ok=True)
counts={'oa':0,'branch':0,'original':0,'persistence_checks':0}
def saved_case():
    report=json.loads(path.read_text())
    counts['persistence_checks']+=1
    return report['cases'][-1]
def stub(design,formulation,integer,**options):
    counts['oa']+=1
    current=saved_case()
    assert len(current['solves'])==(counts['oa']-1)%4
    if counts['oa']==6:raise ArithmeticError('Injected evaluation failure')
    return Result(formulation,integer)
def branch(design,k,**options):
    counts['branch']+=1
    assert len(saved_case()['solves'])==4
    if counts['branch']==2:raise RuntimeError('Injected path solver failure')
    return dict(path=(),status='injected_stub',lower=0.,upper=0.)
original=m.exact_objective
def evaluate(design,path):
    counts['original']+=1
    if counts['original']==2:raise ValueError('Injected original-objective failure')
    return original(design,path)
m.solve_oa=lambda d,f,**kw:stub(d,f,True,**kw)
m.solve_relaxation=lambda d,f,**kw:stub(d,f,False,**kw)
m.solve_branch_bound=branch;m.exact_objective=evaluate
sys.argv=['compare_solvers.py','--output',str(path),'--sizes','1','--seconds','.01']
with contextlib.redirect_stdout(io.StringIO()):m.main()
report=json.loads(path.read_text())
assert len(report['cases'])==4
assert all(len(c['solves'])==5 for c in report['cases'])
assert report['cases'][1]['solves'][0]['status']=='injected_stub'
for case,index,kind,message in [(1,1,'ArithmeticError','Injected evaluation failure'),(1,4,'RuntimeError','Injected path solver failure'),(2,4,'ValueError','Injected original-objective failure')]:
    result=report['cases'][case]['solves'][index]
    assert result['status']=='exception' and result['exception_type']==kind and result['exception_message']==message
assert all(s['status']=='injected_stub' for s in report['cases'][3]['solves'])
result={'driver_sha256':hashlib.sha256(raw).hexdigest(),'source_unchanged':source.read_bytes()==raw,'cases_saved':len(report['cases']),'solve_records_saved':sum(len(c['solves']) for c in report['cases']),'exception_records_saved':sum(s['status']=='exception' for c in report['cases'] for s in c['solves']),'continued_to_final_case':True,'counts':counts,'actual_solver_calls':0}
assert report['source_sha256']['compare_solvers.py']==result['driver_sha256']
pathlib.Path('/tmp/oa_report_failure_fixed_results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
```
