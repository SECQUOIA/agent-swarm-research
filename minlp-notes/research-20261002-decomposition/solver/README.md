# Certified sparse optimization reference solvers

This implementation turns the corrected-grid and min-marginal filtering
method into a reusable exact-arithmetic solver for rational box quadratic
programs. It handles supplied **general tree decompositions**, continuous
and native integer coordinates, fixed coordinates, disconnected interaction
graphs joined by empty separators, and branching decomposition trees.
It returns a feasible point, rational lower and upper bounds on the
**original objective**, and a replayable certificate, including when a
resource limit stops refinement.

The default outer schedule implements the unknown-growth approximation
algorithm in [the October 2 theorem](../../research-20261002/new-direction/pruned-coordinate-grid.md).
The certificate remains valid without uniqueness or a growth assumption.
The second implementation phase adds exact output, automatic decomposition
construction, recourse reductions, constrained models, polynomial factors,
and optimal-set certificates. These are bounded reference implementations;
the experiments do not establish competitive general-purpose MINLP performance.

| Capability | Interface and details |
| --- | --- |
| Rational box-QP bounds | `certified_grid.BoxQP`, `certified_grid.solve`; this page |
| Exact rational optimizer and value | `exact_output.solve_exact`; [exact output](../completion/exact-output.md) |
| Automatic decomposition and shared finite DP | `decomposition.build_decomposition`, `finite_dp.solve_tree`; [finite trees](../completion/finite-tree.md) |
| Exact LP and convex box-QP | `rational_optimization`; [rational oracles](../completion/rational-oracles.md) |
| Affine, minimum-cut, and convex recourse | `recourse.solve_with_recourse`; [recourse](../completion/recourse.md) |
| Coupled TU-fiber constraints | `constrained_grid`; [constrained solver](../completion/constrained-solver.md) |
| Full optimal-set certificates on specified classes | `optimal_sets`; [optimal sets](../completion/optimal-sets.md) |
| Explicit sparse polynomial bounds | `polynomial_grid`; [polynomial solver](../completion/polynomial-solver.md) |
| Exact implicit polynomial boundary output | `polynomial_boundary`; [boundary discovery](../completion/polynomial-boundary.md) |
| Mixed convex/concave submodular residuals | `submodular_recourse`; [mixed recourse](../completion/submodular-recourse.md) |

Each extension documents its accepted class, resource limits, and independent
checker. A theoretical polynomial oracle does not imply that the implemented
simplex or active-face enumeration has polynomial worst-case runtime.

## Interface

`certified_grid.py` uses only the Python standard library. Its objective is

\[
 F(x)=c+b^Tx+\tfrac12x^TAx,
\]

where `A` is symmetric. Acceptable coefficient and endpoint types are
integers, `fractions.Fraction`, and rational strings. Floating-point inputs
are rejected so that the meaning of the rational model is explicit.
Integer endpoints are rounded inward; an empty domain is rejected.

```python
from fractions import Fraction
from certified_grid import BoxQP, solve
from verify_certificate import verify_certificate

problem = BoxQP(
    A=[[2, -3, 0], [-3, 2, -3], [0, -3, 2]],
    b=[0, 0, 0], bounds=[(0, 1)] * 3, integers=[],
    bags=[(0, 1), (1, 2)], edges=[(0, 1)],
    name="nonconvex_path",
)
certificate = solve(problem, epsilon=Fraction(1, 1000),
                    time_limit=2, max_stages=24, max_table_states=20000)
verified = verify_certificate(certificate)
```

`BoxQP.to_dict()` produces the JSON input format. `BoxQP.from_dict()` reads
it. If both `bags` and `edges` are omitted, `BoxQP` constructs a deterministic
minimum-fill decomposition. A supplied decomposition can be preferable;
the heuristic provides an upper bound on width, not an optimality proof.
The decomposition validator checks coverage, interaction coverage, the
tree property, and running intersection. `solve()` returns JSON-compatible
data with `lower`, `upper`, `gap`, and `point` as rational strings, plus
`status`, `stages`, and `stats`. `status="certified"` means that the actual
rational gap meets the requested tolerance. `time_limit`, `table_limit`,
and `stage_limit` report incomplete solves and preserve the latest complete
proof. `warm_start` accepts an original-feasible rational point and validates
its objective. A zero tolerance in `solve` can succeed through exact presolve
or a finite-grid certificate. Use `solve_exact` for rational reconstruction:

```python
from exact_output import solve_exact

exact_certificate = solve_exact(problem, time_limit=2, max_rounds=8,
                                max_table_states=20000)
verified_exact = verify_certificate(exact_certificate)
```

Exact output reconstructs feasible rational candidates and proves optimality
using the original model's optimal-value denominator bound and a checked
lower bound. A stationary candidate alone is insufficient. Resource limits
can stop reconstruction with a valid bound interval and no exact claim.

The command-line interface is:

```bash
python research-20261002-decomposition/solver/certified_grid.py model.json certificate.json --epsilon 1/1000 --time-limit 2 --max-table-states 20000
python research-20261002-decomposition/solver/certified_grid.py model.json exact-certificate.json --exact --max-stages 256 --time-limit 2 --max-table-states 20000
python research-20261002-decomposition/solver/verify_certificate.py certificate.json
```

## Bounds, filtering, and presolve

For coordinate `i` the correction is
`max(0,A[i][i]) * ell[i]**2 / 8`, where `ell` is the largest adjacent grid
interval length. Adjacent native-integer unit intervals contribute zero:
they contain no feasible integer interior. This coordinate-specific
curvature bound is at least as strong as the theorem's common maximum
diagonal bound. It makes no use of Hessian off-diagonal magnitudes.

Coordinates with nonpositive diagonal use only their current endpoints.
The objective is concave or affine in each such coordinate with all others
fixed, so sequential endpoint rounding cannot increase the minimum. Their
correction is zero even on long intervals. This restriction establishes
existence of an endpoint optimum, not that every optimum is an endpoint.

Factors are assigned to the first containing bag. The shared finite-tree
engine performs two directed passes to compute the corrected finite-grid
optimum and every unary min-marginal.
For consecutive nodes `a,b`, the smaller endpoint min-marginal is a valid
lower bound on the original objective when that coordinate belongs to
`[a,b]`. Intervals are removed only when this bound is strictly larger than
the current feasible upper bound. The next domain is the hull of retained
intervals. Interior intervals can be reintroduced by taking this hull;
this weakens filtering without invalidating the proof.

The lower bound returned is the maximum of all completed stage bounds and
an initial exact independent-factor bound. The upper bound is the best
exactly evaluated feasible point found. Exact coordinate descent uses sparse
nonzero interaction lists. Three initial points and each grid witness supply
starting points for improving the upper bound. It makes no
global optimality claim. Integer coordinates remain integral in this
heuristic.

For at most 64 coordinates, an optional presolve attempts an exact rational
PSD factorization `A=L diag(D) L^T` and solves the face suggested by the
incumbent. If the resulting rational point is feasible and satisfies all
box KKT signs, the factorization and point certify a global optimum. This
also works for a mixed instance when the continuous certificate point is
integer-feasible. Failure to obtain the certificate is inconclusive: an
incorrect active face or singular system may prevent it even for a convex
problem. The size cap bounds this optional dense presolve; the main DP
remains sparse. `convex_presolve=False` disables it for algorithm ablations.

## Unknown conditioning and explicit limits

The default `schedule="conditioning"` uses the theorem's outer trials.
Let `L=max(0,max_i A[i][i])`, `s=max_i(hi[i]-lo[i])`, and let `J` be the
smallest nonnegative integer satisfying

\[
 7Lns^2/(8\,4^J)\le\varepsilon.
\]

Rational comparisons compute `J`. A trial uses `theta=2^-mu`, starting at
`mu=2`, and stages `j=0,...,J` with `h=s*2^-j`. Each trial restarts from the
original box, with the best feasible point as its initial center. Before
allocating bag tables, grid generation enforces the proved coordinate cap
`100 * 2**mu * ceil(log2(n+2))`; exceeding it aborts that trial and starts
the next one. Restart records are explicit in the certificate. Earlier
proved lower bounds remain valid after a restart.

With unlimited resources and positive tolerance this schedule terminates
without a uniqueness assumption. For the **default pruned geometric mode**,
under the theorem's global quadratic growth toward a unique optimizer, the first
sufficiently small slope passes the cap and succeeds, giving its
width-and-conditioning bound. Coordinate-specific corrections only reduce
the rounding correction. Endpoint-only variables have zero correction and
at most two labels; they are handled by that separate argument, not by
applying the geometric mesh inequality to their possibly long intervals.

Exact primal polishing can introduce denominators beyond the theorem's
unpolished grid formula. Each coordinate update is a rational affine
expression whose coefficients depend only on the input, or an integer
rounding of that expression. A common denominator acquires at most input
coefficient denominators and diagonal numerators at each update. Thus its
bit length grows polynomially over the bounded number of updates; clipped
values stay within the input box. The small convex presolve uses rational
linear algebra. These additions do not change the parameterized
approximation bound, although their cost matters experimentally.
The `solve_exact` wrapper requests progressively smaller positive tolerances
and checks its separate original-data rational separation criterion.

`max_stages` caps total attempted stages across trials, including a trial
aborted during grid generation. `max_table_states` caps the sum of bag
table sizes at any stage; it is checked before constructing any table.
Grid generation also checks an allocation cap. Time checks occur during
grid generation, table construction, messages, and primal improvement.
A completed DP is retained even if optional primal improvement times out.
The time limit is cooperative, not a hard process deadline: a rational
operation, initial model setup, or proof serialization can cross it.
Experiments therefore also use external worker deadlines and report full
process time. The table-state cap is not a byte-memory guarantee; rational
numerator and denominator sizes and retained proof data also use memory.

For ablations, `pruning=False` preserves the whole box and
`grid_mode="uniform"` uses zero geometric slope. Their validity is
unchanged, but the filtered-grid complexity theorem is not claimed for
unpruned or uniform runs. `schedule="adaptive"` uses one continuing run and halves
its initial slope every `slope_decay_period` stages, default 8. A zero period
keeps the slope fixed; unconditional convergence is not claimed for that
variant. Zero tolerance uses the adaptive schedule because `J` is undefined.

## Independent replay

`verify_certificate.py` does not call grid generation, DP, filtering,
coordinate descent, or the convex presolve. It shares only rational model
parsing, structural validation, and objective evaluation with the solver.
For every completed stage it independently checks:

1. Sorted grid coverage of the current domain and native integrality.
2. The coordinate corrections derived from the grid geometry.
3. Complete separator state coverage and every directed message's exact
   Bellman equality, using independently constructed bag factors.
4. The grid lower bound, all unary min-marginals, and an attaining grid point.
5. Original-box feasibility and the exact objective of each incumbent.
6. Every domain filtering step, the cumulative lower bound, final bounds,
   and the claimed tolerance when the status is `certified`.

The optional convex certificate is checked by exact matrix multiplication
and KKT signs. Floating-point dual bounds are never accepted as proof.
Changing a message, margin, grid coverage, retained domain, or feasible bound
is rejected by the targeted corruption tests. Metadata such as elapsed time,
the grid-generation heuristic, and trial labels is not a mathematical proof
claim. Replay certifies the rational model embedded in the certificate;
an external caller must also match that model to its intended input.

The checker uses finite tables of comparable order to the solve and can be
slower because it deliberately recomputes more arithmetic. It is a separate
implementation of the mathematical checks, not a formally verified checker.
Certificate files contain all completed stages; proof size can become a
practical cost on long or wide runs.

## Targeted validation and experiments

The following topic-only command was run:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python -m unittest discover -s research-20261002-decomposition/solver -p 'test_certified_grid.py' -v
```

The first release passed all 15 tests. They compare general branching-tree DP and all
unary min-marginals with exhaustive enumeration on five rational finite
grids; verify analytic continuous and mixed optima; exercise fixed variables,
empty separators, endpoint reduction, singular PSD/KKT certificates, limits,
outer-trial restarts on a flat optimal set, one-pass integer input iterables,
and ablations; and reject malformed models and corrupted proofs. Later
review and additional checks are recorded in `reviews/`. These tests are
local finite checks, not proofs of the universal complexity theorem. No
project-wide verification or CI status/log inspection was performed.
Current component and integration checks are recorded in
[VALIDATION.md](VALIDATION.md) and the [completion records](../completion/README.md).

The independent [extra benchmark suite](extra-benchmarks/) compares the
complete method, unpruned geometric and uniform variants, and numerical
SCIP on original rational objectives. Its records include independently
computed small-instance reference optima, unmodified compatible QPLIB
inputs, separate solve/replay and total runtimes, per-worker peak memory,
resource-limit outcomes, and source hashes. Its numerical SCIP dual bounds
are explicitly distinguished from rational certificates.

## Practical limits

The implementation demonstrates the complete certifying approximation
method on a supplied decomposition and exposes its overhead. Wider bags
still cause exponentially large tables. Exact rational arithmetic and proof
replay can dominate wall time, even when the dynamic program visits few
states. Automatic decomposition construction and continuous exact output are
implemented. Wider bags, large exact coefficients, and retained proof histories
remain expensive. Verified inexact messages and proof streaming would require
additional algorithms and evidence; they are not features of this release.
The [second benchmark suite](../completion/benchmarks/RESULTS.md) records
the effect of the completed implementations separately from the first release.
