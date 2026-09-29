# Independent review of the numerical rate checks

Date: 2026-09-28. This is an independent adversarial review of
[check_numerical_rates.py](check_numerical_rates.py), including targeted
checks after a generator-list correction. It reviews the numerical
formulation and its interpretation. It does not establish the rate
theorems, numerical certificates, or novelty.

## Findings and correction

The initial affine implementation used
`(1-y^2, 1-v^2, z-y, z+y)`, where `z=(v+1)/2`. The
[affine recourse note](affine-recourse-rate-boundary.md) instead defines
`G2=(1-y^2, z, 1-z, z-y, z+y)`. These lists define the same feasible set
but different truncated preorderings and quadratic modules. Consequently,
the initial implementation did not compute the precise hierarchy defined
in that note. This was a substantive comparison issue even though its
rate mechanism also applies to the quadratic-generator variant.

The numerical author replaced `1-v^2` by the transformed linear
generators `z=(1+v)/2` and `1-z=(1-v)/2`. I independently read the
correction and reran the assembly checks. The current affine list matches
the note exactly under its affine coordinate change. Earlier affine
numbers from the quadratic-generator variant are superseded.

I found no remaining errors in these parts of the formulation:

- The full preordering enumerates square-free subsets of the generator
  list. The quadratic module uses the empty subset and single generators.
- A product `g` has localizing basis degree
  `floor((2r-deg(g))/2)`, so every matrix entry uses moments of degree at
  most `2r`. Products exceeding degree `2r` are omitted.
- Matrix entries and the column-major reshape use the same indexing.
- Each bag has mass one, and the two bags match all separator moments
  `y^j` for `1<=j<=2r`. Their constant moments already agree.
- The transformed quadratic and affine objectives agree with the source
  problems. The dense generator list is the embedded union, with duplicate
  generators removed.
- The reported dual diagnostics have the correct signs. For equality
  constraint `Ew=b` and PSD maps `A_i w`, stationarity is
  `c+E^T lambda-sum_i A_i^T Y_i=0`, and the dual objective is
  `-b^T lambda`.

The script's exact polynomial identities and the displayed dense
certificates are consistent with the chosen generators. In particular,
its affine certificate can use products of `1-x^2` with `z-y` or
`z+y`, which are allowed in the dense full preordering.

## Targeted checks run

From the repository root, I ran this command before and after the
correction:

```bash
python3 -B research-20260928/solver/check_numerical_rates.py --check-only
```

The corrected version passed its symbolic objective and certificate
identities, 7,831 exact Dirac localizer-entry checks, and exact normalization,
separator-equality, and objective-evaluation checks. The localizer checks
cover orders two and three, both examples, dense and sparse formulations,
and both positivity cones. They evaluate the assembled maps at a fixed
rational point. These finite checks supplement inspection of the assembly
rules; they are not an all-order proof of the implementation.

I also ran the following command on the corrected implementation. The
first loop reruns two affine SDPs. The second independently formulates
the finite-grid local-measure problem, using two nonnegative probability
vectors with equal separator moments. It does not reuse the minimax LP's
constraint construction.

```bash
python3 -B - <<'PY'
import importlib.util, json, numpy as np
from scipy.optimize import linprog
p='research-20260928/solver/check_numerical_rates.py'
spec=importlib.util.spec_from_file_location('rates_review',p)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for dense in [True,False]:
    print(json.dumps(m.solve_moment_sdp('affine',2,True,dense,'CLARABEL')))
for example in ['quadratic','affine']:
    count=101; degree=4
    grid=np.cos(np.linspace(0,np.pi,count))
    target=np.maximum(grid,0)**2 if example=='quadratic' else np.abs(grid)
    moments=np.polynomial.chebyshev.chebvander(grid,degree).T[1:]
    eq=np.vstack([np.r_[np.ones(count),np.zeros(count)],np.r_[np.zeros(count),np.ones(count)],np.hstack([moments,-moments])])
    rhs=np.r_[1.,1.,np.zeros(degree)]
    answer=linprog(np.r_[-target,target],A_eq=eq,b_eq=rhs,bounds=(0,None),method='highs')
    approximation=m.grid_approximation(example,degree,count)
    print(json.dumps({'example':example,'independent_measure_LP':float(answer.fun),'negative_twice_grid_minimax':-approximation['ideal_gap_estimate'],'objective_sum_residual':float(answer.fun+approximation['ideal_gap_estimate']),'measure_matching_residual':float(np.max(np.abs(eq@answer.x-rhs)))}))
PY
```

The corrected affine SDP results were:

| Formulation, order two | Primal objective | Solver status | Maximum dual stationarity residual |
| --- | ---: | --- | ---: |
| Dense preordering | `4.2704850767e-9` | `optimal_inaccurate` | `2.2583161972e-8` |
| Sparse preordering | `-0.135241797811` | `optimal_inaccurate` | `1.8440583435e-9` |

These values are numerically consistent with dense exactness and a
nonzero sparse gap. The small positive dense value, despite the known
zero optimum, directly illustrates why the returned numbers are not
certified bounds.

For the independent 101-node measure LP, with degree-four moment matching:

| Target | Measure LP objective | Negative twice minimax-grid objective | Absolute difference |
| --- | ---: | ---: | ---: |
| `max(y,0)^2` | `-0.027606927044243335` | `-0.027606927044238512` | `<4.9e-15` |
| `abs(y)` | `-0.1351812600588484` | `-0.13518126005884895` | `<5.6e-16` |

The maximum normalization and moment-matching residuals were below
`1.6e-14`. This supports the factor-two interpretation of the finite-grid
minimax calculation. It is a floating-point crosscheck of a distinct
primal formulation, not an exact proof of LP duality or of the continuous
local-measure identity.

## Interpretation and limits

In exact arithmetic, restricting the uniform-approximation constraints
to a finite grid gives a minimax error no greater than the true continuous
uniform error. The numerical LP result estimates this finite-grid value.
Twice that value therefore estimates the corresponding finite-grid
moment-matching gap; it is not a certified lower bound obtained from the
floating-point solver.

The denser validation grid measures the residual of the fitted polynomial
only at its sampled points. It is a useful approximation diagnostic, but
it supplies neither a certified continuous residual bound nor, by itself,
an upper or lower bound on the best continuous approximation error.

Small PSD eigenvalue errors, equality residuals, dual residuals, and
primal-dual gaps help assess numerical consistency. They do not certify
feasibility or global optimality. These experiments cannot establish the
asymptotic convergence exponent, an exact equality between the SDP and
local-measure optima, or priority of the theoretical results. The script's
warnings appropriately retain these distinctions.

No Lean formalization, project-wide verification, or CI inspection was
performed. This review changed no numerical implementation; the only file
authored by the reviewer is this record.
