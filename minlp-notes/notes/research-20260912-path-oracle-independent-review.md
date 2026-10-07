Independent review of path pricing and numerical branch and bound, 2026-09-12.

The reviewed implementation has the claimed path identity and valid branch-and-bound logic in exact arithmetic under its stated model. Independent enumeration found no unresolved correctness failure in the tested intended domain. Two substantive defects found during review were corrected by the author and retested: tolerance pruning lost global upper bounds, and malformed warm paths could produce an infeasible incumbent. Input validation was also strengthened during review.

The final reviewed source is [path_oracle.py](../code/research_20260912/path_oracle.py), SHA-256 `61daa250ec278fa2b4770ecd7f2a317d0cf6ffc62002c1cdafd45b0197d9340b`. Tests used Python 3.13.11, NumPy 2.5.3, and SciPy 1.18.1 through the project environment. The reviewer did not edit the implementation, knowledge base, or literature records. The author made the corrections described below; the final source was reread and tested after those changes.

For selected times $s_1<\cdots<s_k$, put $\phi_r=\rho^{s_r-s_{r-1}}$. A lower bidiagonal transformation sends the selected errors to $e_{s_1}$ and $e_{s_r}-\phi_r e_{s_{r-1}}$. Their covariance is diagonal, with entries $\sigma^2$ and $\sigma^2(1-\phi_r^2)$. This follows directly from $R_{ij}=\sigma^2\rho^{|i-j|}$, including negative $\rho$: each transformed error has zero covariance with every earlier selected error. Consequently,

$$
J_S=J_0+\frac{f_{s_1}f_{s_1}^{\mathsf T}}{\sigma^2}
+\sum_{r=2}^k\frac{(f_{s_r}-\phi_r f_{s_{r-1}})(f_{s_r}-\phi_r f_{s_{r-1}})^{\mathsf T}}
{\sigma^2(1-\phi_r^2)}.
$$

The information for an empty subset is $J_0$. Every displayed increment is positive semidefinite, and $J_0\succ0$ makes every subset and every convex mixture positive definite. The identity is a covariance factorization; deriving it does not require an appeal to a Gaussian likelihood. Interpreting the specified matrix as Fisher information requires the model assumptions used to define that information. Fixed local nonlinear sensitivities satisfy the same algebra. Recomputing sensitivities with the selected design, estimating covariance parameters, or using general vector observation models would require a separate argument.

For any symmetric $H$, tracing this identity turns pricing into an additive path objective. The DP's first-node rule excludes required visits before the first node. Its prefix-count arc mask excludes a required visit strictly between consecutive nodes. Its terminal mask excludes a required visit after the last node. Together these rules include every required visit. Banned endpoints cannot enter a finite DP state. Count layers enforce exactly $k$ distinct, increasing indices; maximizing over predecessor indices is exhaustive. The empty path, contradictory required/forbidden sets, too many required visits, and too few available visits are handled consistently. The DP costs $O(kn^2)$ after scores are formed; storing and tracing the information transitions costs $O(n^2p^2)$.

At an arbitrary SPD reference $M$, concavity gives

$$
\log\det J\leq \log\det M-p+\operatorname{tr}(M^{-1}J).
$$

Pricing the trace over all admissible paths therefore gives an upper bound both on the best subset and on the log-determinant maximum over their information-matrix convex hull. Successful continuous optimization is unnecessary for this inequality. A feasible mixture value is a lower bound on the *relaxation* optimum; it is not an incumbent for the subset problem. The implementation correctly obtains its original-problem `lower` only from an actual admissible path. That incumbent can exceed the last mixture value when a newly priced path has not yet been incorporated into the mixture.

The following implementation invariants were checked analytically and with independent scripts.

- `_correct_weights` clips negative candidate weights, rejects nonfinite or zero-total candidates, normalizes the candidate, and retains it only when its objective does not worsen. An optimizer failure flag alone neither certifies nor invalidates a candidate. Tests covered rejected failed results and an improving feasible failed result that was correctly accepted.
- Every retained warm path is a sorted, distinct sequence of valid integer indices. Paths outside the current face or with the wrong count are filtered out; malformed paths raise `ValueError`. Uniform initialization over the retained paths is feasible. Internal branch warm starts need no assumption about the parent's weights.
- `paths`, `weights`, `visits`, and `relaxation_value` remain consistent at an iteration limit. Appending a newly priced path with zero weight on the last iteration does not change the represented matrix. A priced incumbent need not yet occur in the returned support list.
- The trace gap is computed at the current mixture. In exact arithmetic it is nonnegative. Clipping a negative numerical gap to zero only raises the tangent upper. `upper` is the minimum of all tangent uppers obtained; `relaxation_gap` describes the last iterate and need not equal `upper - relaxation_value`.
- Branching on a free visit partitions a node into exhaustive disjoint faces. Selecting the visit closest to one-half affects search order, not validity. Child upper bounds may be reduced by their parent's upper. The global incumbent is shared across nodes.
- Heap nodes, unprocessed children covered by their parent's bound, and nodes removed by tolerance pruning all contribute to the final global upper. The maximum is also bounded below by the incumbent. A fully fixed feasible face contains one subset, already considered for the incumbent.
- Zero and negative time limits still allow root initialization and at least one certification iteration. Iteration limits of zero or less also result in one iteration because of `max(1, iterations)`. Neither limit claims convergence of the hull relaxation.

The independent test results were:

| Check | Cases | Result |
| --- | ---: | --- |
| Dense covariance versus path information, all subsets of candidate sets with 0, 1, 4, and 6 visits, with five correlations including negative and zero | 415 | Maximum relative difference $7.75\times10^{-15}$ |
| Random required/forbidden pricing faces, arbitrary symmetric trace weights | 750 | Maximum absolute objective difference $7.11\times10^{-14}$ |
| Every free/required/forbidden assignment for five visits, every count | 1,458 | Exact enumerated pricing agreement, including infeasible faces |
| Hull calls with one iteration, including contradictory faces | 145 | Valid feasible incumbents and bounds where feasible |
| Hull calls with all root paths as warm starts, sampled from the exhaustive face suite | 85 | Face filtering, weights, visits, and bounds passed |
| Fully solved small branch-and-bound cases | 55 | Enumerated optimum matched within $2\times10^{-9}$ |
| Negative, zero, and tiny time limits | 25 | Incumbents feasible; reported upper covered enumerated optimum |
| Deterministic expiry before the first child and after the first child | 2 | Parent bound preserved; status `limit` |
| Near-boundary correlations $\rho=\pm0.9999$, prior diagonal $(10^{-4},1,100)$, variance 0.07 | 70 information comparisons; 2 solves | Relative covariance difference below $1.78\times10^{-12}$; optimum matched |
| Invalid count and required/forbidden indices | 8 | Rejected |

Counts of pricing and hull faces include infeasible faces. The tests are deterministic except for elapsed times and the amount of search completed under a real wall-clock deadline. Enumeration is independent of the DP, and dense selected-covariance solves independently check the information identity. Tests use numerical comparison tolerances; they do not certify rounding-error bounds.

The two corrected failures have short reproducible examples.

1. With `rng = np.random.default_rng(2)`, seven rows and three columns of normal sensitivities, `rho=0.7`, `prior=I`, `count=3`, `node_iterations=1`, and outer `tolerance=100`, the true enumerated optimum is `4.5472464880398284`. The original code returned `lower = upper = 3.9325182506042573` after discarding the root by tolerance. The corrected code retains the root upper `12.824323729804759`. Status `optimal` means the requested numerical tolerance has been met; it does not mean the displayed gap is zero.
2. With sensitivities `[[1],[-1],[0],[0]]`, `rho=0.9`, `prior=[[1]]`, `count=4`, and warm path `(0,1,0,1)`, the original code returned an infeasible incumbent of `3.6888794541139363`, above the only feasible subset's value `3.2293471247354963`. The corrected code rejects that path. It also rejects a negative warm index.

The scripts reproduce the former behavior in a separate module by restoring only the two original blocks read at the start of review. That reconstructed module is used only to demonstrate the defects; the reviewed author file is never modified. The regression checks then verify the current implementation's bounds and input rejection.

The author also corrected two input-validation gaps. A prior such as `[[2,100],[0,2]]` formerly passed a Cholesky call because that call consumes only one triangle. The constructor now checks finiteness and symmetry, symmetrizes within its stated tolerance, and checks positive definiteness. Fractional or NaN required indices formerly bypassed the range-only validation and could be silently omitted; required and forbidden indices and the count now require integer types. The constructor checks finite sensitivities and finite positive variance as well.

Remaining limitations concern numerical arithmetic and operational semantics. The implementation uses ordinary floating-point Cholesky factorizations, inverses, traces, and DP sums without outward rounding. Taking the minimum of numerical uppers or pruning against them is therefore not an interval certificate. Conditioning and overflow can still cause failure or inaccurate bounds outside the tested scales. Optimizer or linear-algebra exceptions are not caught by `_correct_weights`; its fallback protects against unsuitable returned weights, not every possible numerical failure. A synthetic test that forces the optimizer to evaluate zero weights raises `LinAlgError`; this is an interface limitation, not a demonstrated trial produced by SLSQP on the tested valid inputs.

The deadline is soft: checks occur after a correction/pricing step and between child nodes, not inside SLSQP or a DP call. A zero-limit run with 160 visits, four parameters, and count 80 took about 0.07–0.09 seconds to establish its root bounds, then returned `limit`. `pricing_calls` counts certification pricing calls using the current inverse matrix; it excludes each hull invocation's identity-objective initialization call, including initial calls that establish infeasibility. `nodes` counts the root and attempted child hull evaluations, including infeasible children. These meanings should be retained when reporting computational results.

The complete independent checks follow. From the repository root, this command extracts the three Python blocks, runs them in order, and leaves their JSON results in `/tmp`. The first block snapshots the reviewed module so that the later checks use identical code. Compare its printed hash with the hash above when reproducing this review.

```bash
uv run --project code/research_20260912 python - <<'PY'
from pathlib import Path
import re
import runpy
note = Path("notes/research-20260912-path-oracle-independent-review.md").read_text()
for index, block in enumerate(re.findall(r"```python\n(.*?)\n```", note, re.S), 1):
    script = Path(f"/tmp/path-oracle-review-{index}.py")
    script.write_text(block)
    runpy.run_path(str(script), run_name="__main__")
PY
```

```python
from __future__ import annotations
import hashlib, importlib.util, itertools, json, pathlib, time
import numpy as np

source = pathlib.Path('/workspace/minlp-notes/code/research_20260912/path_oracle.py')
snapshot = pathlib.Path('/tmp/path_oracle_review_snapshot.py')
raw = source.read_bytes(); snapshot.write_bytes(raw)
spec = importlib.util.spec_from_file_location('review_oracle', snapshot)
m = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = m
spec.loader.exec_module(m)
rng = np.random.default_rng(125791)
counts = dict(dense_information=0, pricing_faces=0, hull_faces=0, branch_bound=0, deadline=0)
errors = dict(information_relative=0., price_absolute=0., hull_underestimate=0., bb_underestimate=0.)
findings = {}

def subsets(n, k, req=(), ban=()):
    return [s for s in itertools.combinations(range(n), k)
            if set(req).issubset(s) and not set(ban).intersection(s)]

cases=[]
for n in (0, 1, 4, 6):
    for rho in (-.97, -.4, 0., .6, .97):
        p=3
        f=rng.normal(size=(n,p)); a=rng.normal(size=(p,p))
        prior=a.T@a+.2*np.eye(p); variance=1.7
        data=m.scalar_markov(f,rho,prior,variance)
        covariance=variance*rho**np.abs(np.subtract.outer(np.arange(n),np.arange(n)))
        for k in range(n+1):
            all_s=subsets(n,k)
            for s in all_s:
                ix=list(s); dense=prior.copy()
                if s: dense += f[ix].T@np.linalg.solve(covariance[np.ix_(ix,ix)],f[ix])
                info=data.information(s)
                np.testing.assert_allclose(info,dense,atol=2e-10,rtol=2e-10)
                errors['information_relative']=max(errors['information_relative'],float(np.linalg.norm(info-dense)/max(1,np.linalg.norm(dense))))
                counts['dense_information']+=1
            for _ in range(10):
                assign=rng.integers(0,3,size=n)
                req=tuple(np.flatnonzero(assign==1)); ban=tuple(np.flatnonzero(assign==2))
                h=rng.normal(size=(p,p)); h=h+h.T
                candidates=subsets(n,k,req,ban)
                priced=m.price_path(data,k,h,req,ban)
                if not candidates: assert priced is None
                else:
                    exact=max(float(np.trace(h@data.information(s))) for s in candidates)
                    assert priced[0] in candidates
                    err=abs(priced[1]-exact)
                    assert err<2e-9
                    errors['price_absolute']=max(errors['price_absolute'],err)
                counts['pricing_faces']+=1
            for req,ban in [((),()), ((0,),(0,))] if n else [((),())]:
                candidates=subsets(n,k,req,ban)
                b=m.hull_bound(data,k,req,ban,iterations=1)
                if not candidates: assert b is None
                else:
                    exact=max(data.value(s) for s in candidates)
                    assert b['path'] in candidates
                    assert b['lower'] <= exact+2e-9
                    assert b['upper'] >= exact-2e-9
                    assert np.all(b['weights'] >= 0)
                    assert abs(b['weights'].sum()-1)<1e-10
                    assert len(b['paths'])==len(b['weights'])
                    assert all(s in candidates for s in b['paths'])
                    weighted=sum(w*data.information(s) for s,w in zip(b['paths'],b['weights']))
                    assert abs(m.logdet(weighted)-b['relaxation_value'])<2e-9
                    assert b['relaxation_value'] <= b['upper']+2e-9
                    errors['hull_underestimate']=max(errors['hull_underestimate'],exact-b['upper'])
                counts['hull_faces']+=1
            if n<=4 or k in (0,2,n):
                exact=max(data.value(s) for s in all_s)
                solved=m.solve_branch_bound(data,k,time_limit=5,tolerance=1e-9,node_iterations=2)
                assert solved['status']=='optimal',solved
                assert solved['path'] in all_s
                assert abs(solved['lower']-exact)<2e-9,solved
                assert solved['upper'] >= exact-2e-9,solved
                counts['branch_bound']+=1
                errors['bb_underestimate']=max(errors['bb_underestimate'],exact-solved['upper'])
            if n==6 and k==3: cases.append((data,k,all_s))

for data,k,all_s in cases:
    exact=max(data.value(s) for s in all_s)
    for limit in (-1.,0.,1e-9,.001,.005):
        solved=m.solve_branch_bound(data,k,time_limit=limit,node_iterations=2)
        assert solved['path'] in all_s
        assert solved['lower'] <= exact+2e-9
        assert solved['upper'] >= exact-2e-9
        counts['deadline']+=1

# A tolerance-optimal result must still report a global upper if called an upper.
for seed in range(100):
    rr=np.random.default_rng(seed)
    data=m.scalar_markov(rr.normal(size=(7,3)),.7,np.eye(3))
    all_s=subsets(7,3); exact=max(data.value(s) for s in all_s)
    root=m.hull_bound(data,3,iterations=1)
    if root['lower'] < exact-1e-3:
        solved=m.solve_branch_bound(data,3,time_limit=5,tolerance=100,node_iterations=1)
        assert solved['upper'] >= exact-2e-9
        assert solved['upper'] > solved['lower']+.1
        findings['tolerance_pruning']={'seed':seed,'exact':exact,'root_lower':root['lower'],'root_upper':root['upper'],'result':solved}
        break
assert 'tolerance_pruning' in findings

# Warm paths are part of the public hull API; they must represent actual subsets.
data=m.scalar_markov(np.array([[1.],[-1.],[0.],[0.]]),.9,np.eye(1))
invalid=(0,1,0,1)
try:
    result=m.hull_bound(data,4,warm_paths=[invalid],iterations=1)
    findings['repeated_warm_path']={'exact':data.value((0,1,2,3)),'path':result['path'],'lower':result['lower'],'upper':result['upper']}
except ValueError as exc: findings['repeated_warm_path']={'exception':type(exc).__name__,'message':str(exc)}
else: raise AssertionError('Repeated warm path accepted')
try:
    result=m.hull_bound(data,1,warm_paths=[(-1,)],iterations=1)
    findings['negative_warm_path']={'path':result['path'],'paths':result['paths']}
except ValueError as exc: findings['negative_warm_path']={'exception':type(exc).__name__,'message':str(exc)}
else: raise AssertionError('Negative warm path accepted')

# The constructor must reject a prior whose Cholesky triangle hides asymmetry.
try:
    asym=m.scalar_markov(np.array([[1.,2.],[2.,1.]]),.7,np.array([[2.,100.],[0.,2.]]))
    findings['asymmetric_prior']={'accepted':True,'stored_prior':asym.prior.tolist()}
except ValueError as exc: findings['asymmetric_prior']={'exception':type(exc).__name__}
else: raise AssertionError('Asymmetric prior accepted')

report={'source_sha256':hashlib.sha256(raw).hexdigest(),'source_unchanged_at_end':source.read_bytes()==raw,'counts':counts,'max_errors':errors,'findings':findings}
pathlib.Path('/tmp/path_oracle_independent_results.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
```

```python
import importlib.util, sys, types, itertools, json, time
import numpy as np
spec=importlib.util.spec_from_file_location('edges_oracle','/tmp/path_oracle_review_snapshot.py')
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
results={}
rng=np.random.default_rng(2);data=m.scalar_markov(rng.normal(size=(7,3)),.7,np.eye(3))
exact=max(data.value(s) for s in itertools.combinations(range(7),3))
original_hull=m.hull_bound; original_time=m.time
class Clock:
    def __init__(self, ticks):self.ticks=iter(ticks);self.last=0.
    def perf_counter(self):self.last=next(self.ticks,self.last);return self.last
for label,ticks in [('before_first_child',[0.,0.,2.]),('after_first_child',[0.,0.,0.,2.])]:
    fake=Clock(ticks)
    def wrapped(*args,**kwargs):
        m.time=original_time
        try:
            kwargs['deadline']=float('inf')
            return original_hull(*args,**kwargs)
        finally:m.time=fake
    m.hull_bound=wrapped;m.time=fake
    solved=m.solve_branch_bound(data,3,time_limit=1,node_iterations=1,tolerance=1e-10)
    assert solved['upper']>=exact-1e-10
    assert solved['lower']<=exact+1e-10
    assert solved['status']=='limit'
    results[label]=solved
m.hull_bound=original_hull;m.time=original_time

# Match author's former implementation using copies of two pre-fix blocks.
raw=open('/tmp/path_oracle_review_snapshot.py').read()
start=raw.index('    valid_warm = []')
end=raw.index('    if initial[0] not in paths:',start)
old='''    paths = list(dict.fromkeys(tuple(p) for p in warm_paths
                               if len(p) == count and req <= set(p)
                               and not ban.intersection(p)))
'''
raw=raw[:start]+old+raw[end:]
raw=raw.replace('    pruned_upper = -float("inf")\n','')
raw=raw.replace('            pruned_upper = max(pruned_upper, -negative_upper)\n','')
raw=raw.replace('            else:\n                pruned_upper = max(pruned_upper, upper)\n','')
raw=raw.replace('    upper = max(lower, unresolved_upper, pruned_upper,\n                -heap[0][0] if heap else lower)','    upper = max(lower, unresolved_upper, -heap[0][0] if heap else lower)')
oldmod=types.ModuleType('old_oracle');sys.modules[oldmod.__name__]=oldmod;exec(compile(raw,'reconstructed_pre_fix','exec'),oldmod.__dict__)
solved=oldmod.solve_branch_bound(data,3,time_limit=5,tolerance=100,node_iterations=1)
assert solved['upper']<exact-.1
results['pre_fix_tolerance']={'exact':exact,'result':solved}
warm_data=m.scalar_markov(np.array([[1.],[-1.],[0.],[0.]]),.9,np.eye(1))
b=oldmod.hull_bound(warm_data,4,warm_paths=[(0,1,0,1)],iterations=1)
assert b['lower']>warm_data.value((0,1,2,3))
results['pre_fix_warm']={key:b[key] for key in ('path','lower','upper')}
results['pre_fix_warm']['exact']=warm_data.value((0,1,2,3))

# All legal faces for one nontrivial instance; warm start with every root path.
rng=np.random.default_rng(849)
data=m.scalar_markov(rng.normal(size=(5,2)),-.85,np.diag([.2,3.]))
faces=0;hulls=0
for k in range(6):
    all_paths=list(itertools.combinations(range(5),k))
    for state in itertools.product((0,1,2),repeat=5):
        req=tuple(i for i in range(5) if state[i]==1);ban=tuple(i for i in range(5) if state[i]==2)
        candidates=[s for s in all_paths if set(req)<=set(s) and not set(ban).intersection(s)]
        h=rng.normal(size=(2,2));h=h+h.T
        price=m.price_path(data,k,h,req,ban)
        assert (price is None)==(not candidates)
        if candidates:
            oracle=max(np.trace(h@data.information(s)) for s in candidates)
            assert price[0] in candidates
            assert abs(price[1]-oracle)<1e-9
        faces+=1
        if faces%17==0:
            b=m.hull_bound(data,k,req,ban,warm_paths=all_paths,iterations=2)
            assert (b is None)==(not candidates)
            if candidates:
                exact_face=max(data.value(s) for s in candidates)
                assert b['path'] in candidates
                assert all(s in candidates for s in b['paths'])
                assert b['lower']<=exact_face+1e-9<=b['upper']+2e-9
                visits=sum(w*np.array([int(i in s) for i in range(5)]) for s,w in zip(b['paths'],b['weights']))
                np.testing.assert_allclose(b['visits'],visits,atol=1e-12)
                assert abs(b['visits'].sum()-k)<1e-10
                for i in req: assert abs(b['visits'][i]-1)<1e-10
                for i in ban: assert abs(b['visits'][i])<1e-10
            hulls+=1
results['exhaustive_faces']={'pricing':faces,'hull_warm_checks':hulls}

# Failure flags do not establish correctness or invalidate feasible repaired weights.
matrices=np.array([np.eye(2),np.diag([2.,.5])]);weights=np.array([.5,.5])
original_minimize=m.minimize
weight_cases={}
for label,x in [('failure_feasible',np.array([0.,1.])),('failure_negative',np.array([-10.,2.])),('failure_nan',np.array([np.nan,1.])),('failure_zero',np.array([0.,0.]))]:
    m.minimize=lambda *a,_x=x,**kw:types.SimpleNamespace(x=_x,success=False)
    out=m._correct_weights(matrices,weights)
    assert np.all(np.isfinite(out)) and np.all(out>=0) and abs(out.sum()-1)<1e-12
    assert m.logdet(np.einsum('n,nij->ij',out,matrices))>=m.logdet(np.einsum('n,nij->ij',weights,matrices))-1e-12
    weight_cases[label]=out.tolist()
m.minimize=original_minimize
results['weight_failure_checks']=weight_cases

# Invalid public count/face indices must be rejected.
invalid_checked=0
for kwargs in [dict(required=[.5]),dict(required=[np.nan]),dict(forbidden=[.5]),dict(required=[-1]),dict(required=[5])]:
    try:m.price_path(data,2,np.eye(2),**kwargs)
    except ValueError:invalid_checked+=1
    else:raise AssertionError(('accepted invalid indices',kwargs))
for count in (2.,-1,6):
    try:m.price_path(data,count,np.eye(2))
    except ValueError:invalid_checked+=1
    else:raise AssertionError(('accepted invalid count',count))
results['invalid_index_checks']=invalid_checked
m.minimize=lambda *a,**kw:types.SimpleNamespace(x=np.array([0.,1.]),success=False)
out=m._correct_weights(np.array([np.eye(2),2*np.eye(2)]),np.array([.5,.5]))
np.testing.assert_equal(out,[0.,1.])
m.minimize=original_minimize
results['weight_failure_checks']['improving_failed_result_accepted']=out.tolist()

print(json.dumps(results,indent=2))
open('/tmp/path_oracle_review_edges_results.json','w').write(json.dumps(results,indent=2))
```

```python
import importlib.util,sys,itertools,json,time
import numpy as np
spec=importlib.util.spec_from_file_location('scale_oracle','/tmp/path_oracle_review_snapshot.py')
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
results={'near_boundary':[]}
rng=np.random.default_rng(77591)
for rho in (-.9999,.9999):
    f=rng.normal(size=(7,3));prior=np.diag([1e-4,1.,100.]);data=m.scalar_markov(f,rho,prior,variance=.07)
    covariance=.07*rho**np.abs(np.subtract.outer(np.arange(7),np.arange(7)))
    relative=[]
    for s in itertools.combinations(range(7),3):
        ix=list(s);dense=prior+f[ix].T@np.linalg.solve(covariance[np.ix_(ix,ix)],f[ix])
        relative.append(np.linalg.norm(data.information(s)-dense)/np.linalg.norm(dense))
    exact=max(data.value(s) for s in itertools.combinations(range(7),3))
    try:
        sol=m.solve_branch_bound(data,3,time_limit=10,node_iterations=2,tolerance=1e-8)
        assert sol['upper'] >= exact-1e-7
        assert sol['lower'] <= exact+1e-7
        assert sol['status']=='optimal'
        results['near_boundary'].append({'rho':rho,'max_relative_covariance_difference':max(relative),'exact':exact,'lower':sol['lower'],'upper':sol['upper']})
    except Exception as exc:results['near_boundary'].append({'rho':rho,'exception':type(exc).__name__,'message':str(exc)})

assert all('exception' not in row for row in results['near_boundary'])
assert all(row['max_relative_covariance_difference'] < 2e-10 for row in results['near_boundary'])
f=rng.normal(size=(160,4));data=m.scalar_markov(f,.8,np.eye(4))
sol=m.solve_branch_bound(data,80,time_limit=0,node_iterations=40)
results['zero_limit_large']={key:sol[key] for key in ('status','seconds','nodes','pricing_calls','lower','upper')}
assert sol['nodes']==1 and sol['pricing_calls']==1

# Singular SLSQP trial evaluation is allowed by its box bounds but infeasible for simplex.
original=m.minimize
def stub(objective,weights,**kwargs):
    objective(np.zeros_like(weights))
m.minimize=stub
try:
    m._correct_weights(np.array([np.eye(2),2*np.eye(2)]),np.array([.5,.5]))
    results['singular_optimizer_trial']='accepted'
except Exception as exc:results['singular_optimizer_trial']={'exception':type(exc).__name__,'message':str(exc)}
m.minimize=original
print(json.dumps(results,indent=2))
open('/tmp/path_oracle_review_scale_results.json','w').write(json.dumps(results,indent=2))
```

