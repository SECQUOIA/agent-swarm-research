# LB-ESH representation and cut-geometry diagnostic

Date: 2026-09-19. This is a supplementary mechanism experiment, not a GDP
performance benchmark or a claim of a new separation principle. It evaluates
the implementation used by the study without modifying its source.
[Independent review](lbesh-review-oracle-diagnostic.md) passed, including a
full replay, mathematical checks, oracle-call tracing, and review of this note.

## Question and fixed design

The [theory note, Section 10](lbesh-development-theory.md) shows that replacing
a differentiable convex row \(q\le0\) by
\(\exp(aq)-1\le0\), \(a>0\), preserves the exact ESH halfspace when the
anchor and exterior point are fixed. ECP generally changes. This experiment
checks that mechanism in the actual `LBESH._esh_cuts` routine, including its
finite bisection tolerance. It also measures the oracle work that a cut count
alone omits.

The [script](../code/minlp_solver_lab/lbesh_oracle_diagnostic.py) constructs a
lightweight `LBESH` object, uses the actual `NLRow` implementation, and supplies
counted analytic function/gradient wrappers. It creates no optimization model,
requests no solver license, and solves no GDP. The wrappers use `expm1` for
stable evaluation of \(\exp(t)-1\); this tests the implemented cut algorithm,
not the Pyomo/SymPy expression compiler. All rows are convex and smooth on
their bounded domains. No held-out instance or tuning outcome was used to
choose the design.

The predetermined exponential scales are \(a=1,2,4,8,16,32\), with an
untransformed base-row control. The largest positive exponential argument
is 66, so overflow is not approached. The oracle's `cut_tol` and `feas_tol`
are both \(10^{-12}\). Its frozen bisection stops when the parameter bracket
is narrower than \(10^{-10}\), taking 34 bisection evaluations here.
All ESH calls are checked to exclude ECP fallback.

1. **Scalar sequence.** Maximize \(x\) on \([0,2]\), subject to
   \(q=x-1\le0\), represented either directly or by the exponential row.
   Fix anchor zero and the initial master to the box alone, hence its first
   optimum is two. Each cut updates the scalar upper bound exactly by
   division of its floating-point affine coefficients. Stop when
   \(\max(0,x-1)\le10^{-8}\), a common geometric and objective criterion.
   In particular, no transformed function-residual stopping rule is used.
2. **Two-dimensional cuts.** Use \(q(x)=x^TQx-1\), with \(Q=I\) or
   \(Q=\operatorname{diag}(1,4)\), anchor zero, and candidates
   \(p=rQ^{-1/2}(\cos\theta,\sin\theta)\). Predetermine
   \(r\in\{1.25,1.75\}\) and \(\theta=2\pi k/16\),
   \(k=0,\ldots,15\). These points all belong to \([-2,2]^2\).
   Compare each cut after dividing by the Euclidean norm of its original
   variable normal. This is a single-oracle diagnostic: there is no iteration
   stopping rule or master trajectory in these 896 cases.
3. **Off-center non-dominance control.** For the untransformed disk use
   candidate \((2,0)\), anchor \((0,0.9)\), and the theory note's two
   witnesses \((1.2,1)\), \((1.3,-2)\). This prevents the centered radial
   examples from suggesting universal ESH cut dominance.

The affine scalar control is deliberately passed through the oracle for
comparison; an actual GDP model extractor would recognize it as affine and
place it in the initial master. The scalar experiment starts with the box
alone for every scale. In particular, the \(a=1\) case does not rely on the
theory note's separate statement about redundant initial anchor tangents for
\(a\ge2\).

## Results and checks

The [complete JSON](../code/minlp_solver_lab/results/lbesh_development/oracle_diagnostic.json)
contains all scalar trajectories, 896 two-dimensional cut records, the
non-dominance witnesses, oracle counts, nine timing samples per scalar run
or two-dimensional cut, environment versions, and SHA-256 hashes of the
script and the two implementation files used.

| Scalar row | ECP cuts | ECP function calls | ECP gradient calls | ESH cuts | ESH function calls | ESH gradient calls |
|---|---:|---:|---:|---:|---:|---:|
| Base \(x-1\) | 1 | 2 | 1 | 1 | 37 | 1 |
| \(a=1\) | 5 | 10 | 5 | 1 | 37 | 1 |
| \(a=2\) | 6 | 12 | 6 | 1 | 37 | 1 |
| \(a=4\) | 8 | 16 | 8 | 1 | 37 | 1 |
| \(a=8\) | 12 | 24 | 12 | 1 | 37 | 1 |
| \(a=16\) | 20 | 40 | 20 | 1 | 37 | 1 |
| \(a=32\) | 36 | 72 | 36 | 1 | 37 | 1 |

Each ESH cut uses one root search with 34 function calls during bisection,
plus one candidate value, one anchor value, and one tangent value. ECP uses
two function calls and one gradient call per cut, with no root search. Total
counts are instrumented at the analytic wrapper. Root counts are obtained
by subtracting the three known non-root value calls from each ESH call;
the script asserts that fallback is absent. The implementation does not
stop bisection early when a midpoint is exactly on the boundary.

All scalar ESH final bounds equal one at recorded floating-point precision.
ECP's largest final geometric error is \(2.56\times10^{-11}\). Its updates
agree with the independent recurrence

\[
p_{k+1}=p_k-\frac{1-\exp[-a(p_k-1)]}{a}
\]

within \(2.23\times10^{-16}\). Thus the implemented algorithm reproduces
the predicted representation sensitivity under a common stopping condition.
The increase in cut count does not imply the same increase in oracle cost:
ESH uses more function calls than ECP through \(a=8\).

In the two-dimensional experiment the unit-normal ESH constant differs from
the exact ellipsoid support constant by at most \(4.45\times10^{-16}\).
Every normal agrees with its analytic normal within \(10^{-12}\), and
every ECP constant agrees with its independent analytic expression within
\(10^{-9}\). All cuts pass an analytic support-function validity check:
for cut \(n^Tx+c\le0\), its maximum over the entire ellipsoid is
\(\sqrt{n^TQ^{-1}n}+c\), checked to be at most \(10^{-10}\).
This is a numerical check of a mathematically valid tangent, not an
interval-arithmetic certificate.

For example, for the disk at \(p=(1.75,0)\), define cut depth as the
positive signed distance \(n^Tp+c\), where \(\|n\|_2=1\).

| Representation | ECP depth | ESH depth |
|---|---:|---:|
| Base disk row | 0.589286 | 0.750000 |
| \(a=1\) | 0.249390 | 0.750000 |
| \(a=2\) | 0.140548 | 0.750000 |
| \(a=4\) | 0.071410 | 0.750000 |
| \(a=8\) | 0.035714 | 0.750000 |
| \(a=16\) | 0.017857 | 0.750000 |
| \(a=32\) | 0.008929 | 0.750000 |

For every centered case ESH and ECP have parallel normals and ESH has the
stronger halfspace. This is a property of this selected radial geometry.
Across these cases ECP's normalized constant differs from the exact support
constant by 0.0125 to 0.741072, whereas ESH's finite-bisection result retains
representation invariance to numerical precision. This does not establish
finite-tolerance invariance for other rows, root solvers, or anchors.

For the off-center disk, ECP is \(x\le1.25\), with depth 0.75 at the
candidate. ESH has unit normal approximately \((0.857795,0.513992)\),
constant \(-1\), and depth 0.715590. Its depth is smaller despite using
a boundary support. The first witness satisfies ECP by 0.05 and violates
ESH by 0.543346. The second satisfies ESH by 0.912852 and violates ECP
by 0.05. Both witnesses are in the common box. Neither halfspace contains
the other; these are witnesses concerning the outer approximations, not
feasible points of the disk.

Timing is descriptive. Nine repeated scalar runs in the recorded environment
give median elapsed times of approximately 41–85 microseconds for ESH and
10–533 microseconds for ECP, depending on the representation. Timing covers
the actual oracle call and Python bookkeeping (plus scalar bound updates),
but excludes imports and object setup. Concurrent research jobs and these
very short durations make ratios unsuitable as robust speed measurements.
There are no LP, MILP, NLP, anchor-computation, or GDP search costs in these
numbers. No total solver speedup follows from them.

## Reproduction and interpretation

Run from `code/minlp_solver_lab`:

```sh
.venv/bin/python lbesh_oracle_diagnostic.py
```

The executed environment uses Python 3.13.11, NumPy 2.5.3, Pyomo 6.10.1,
and gurobipy 13.0.3 on Linux/WSL2. Existing project dependencies and
`uv.lock` provide the environment. Gurobi is an import dependency of the
solver module, but no license is required by this diagnostic. The script
performs its analytic recurrence, cut-validity, cut-separation, deterministic
trajectory, and non-dominance checks on every run. JSON timing values and
generation timestamps vary between runs; the geometry and counts are the
reproducible results.

This gives an implemented explanation of when ESH can avoid a weakness of
exterior-point tangents: convex monotone re-expression can make the latter
shallower without changing the set. It also exposes the line-search cost
and the absence of general cut dominance. The scalar sequence and the
two-dimensional fixed cuts are explanatory examples, not evidence that the
effect dominates realistic GDP computations. Anchor selection is fixed here;
an anchor-computation procedure can itself depend on row representation.
The experiment supports the existing mathematical mechanism, not novelty
of that mechanism, a new framework, or representative computational benefit.
