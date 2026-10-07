# Implemented exact rational output for general box QP

The general corrected-grid solver now returns an exact rational optimizer
when its stored bounds prove exactness. This closes the earlier gap between
the exact-output theorem and the approximation-only implementation. It
supports continuous, integer, and mixed rational box QPs, including fixed
rational coordinates. Certificate safety and eventual exact recovery do not require uniqueness or
a supplied growth constant. The default conditioning schedule, with
sufficiently increased resource caps including LP pivots, eventually
recovers an optimizer of every bounded rational box QP. This is a finite
completion guarantee; it supplies no efficient bound for arbitrary optimal
sets. The stronger parameterized bound remains the existing unique-point
growth result.

Implementation:

- [exact_output.py](../solver/exact_output.py): rational heights, candidate
  recovery, a bounded sequence of approximation calls, and exact acceptance.
- [verify_certificate.py](../solver/verify_certificate.py): independent replay
  of every approximation certificate and the final exactness argument.
- [test_exact_output.py](../solver/test_exact_output.py): twelve targeted tests.
- [independent review](exact-output-review.md): arithmetic, mixed and singular
  cases, adversarial mutations, and resource-limit checks.

The existing approximation API and `certified-grid-qp-v1` certificates remain
supported. New exact results use `certified-grid-qp-exact-v1`, an envelope
containing those original proofs. Historical benchmark files are unchanged.

## The exactness argument

Write the original objective as

\[
F(x)=\tfrac12 x^TAx+b^Tx+c=x^TQx+b^Tx+c,\qquad Q=A/2.
\]

Round integer endpoints inward before defining the model. Let `D` be the
least common multiple of denominators of all entries of `Q`, `b`, `c`, and
the original rounded box endpoints. Let `C` denote the continuous
coordinates whose original interval has positive width, and define

\[
H=\prod_{i\in C}\max\left\{1,\sum_{j\in C}|DA_{ij}|\right\},\qquad
R=DH,\qquad V=DR^2.
\]

The empty product is one. These are positive integers of polynomial binary
length. In particular, they are bounds, not enumeration limits. Refined box
endpoints and approximate iterates never enter their definition.

**Height lemma.** Some global optimizer has a common coordinate denominator
at most `R`, and the reduced denominator of the global minimum is at most
`V`. This holds even when there are multiple optimizers.

To prove this, choose an optimal integer assignment and an optimizer on a
continuous face of minimum dimension. On the free coordinates `J`, the
Hessian is positive semidefinite and nonsingular. Otherwise a nonzero null
direction would preserve the stationary quadratic objective until it met a
smaller face. Put `u=Dx`. The free stationarity equations have integer matrix
`DA[J,J]` and an integer right-hand side: the fixed coordinates are original
rational endpoints or integers. Hadamard's inequality, with each Euclidean
row norm bounded by its one-norm, gives

\[
1\le |\det(DA[J,J])|\le H.
\]

Cramer's rule gives a common denominator at most `D H` for all coordinates.
Substitution into the original objective bounds the value denominator by
`D R^2`. A zero-dimensional face has determinant one. Fixed rational
coordinates, integer slices, and a singular full Hessian therefore present
no exception.

**Candidate-value separation.** Suppose a replayed certificate proves
`L <= f*`, and a feasible rational candidate has value `r`, with reduced
positive denominator `W`. If

\[
0\le r-L<\frac1{VW},
\]

then `r=f*`. Indeed, distinct rationals whose denominators are respectively
at most `V` and exactly `W` differ by at least `1/(VW)`. Since
`L <= f* <= r`, a strict improvement over `r` is impossible.

This test does **not** assume that every feasible objective has denominator
at most `V`. The candidate may have denominator larger than `V`. A tiny
floating-point gap, box KKT conditions, or a stationary point alone never
certifies exactness. Equal certified lower and upper bounds provide a
second, immediate exact proof.

## Candidate recovery and refinement

`solve_exact` calls the original certified approximation algorithm with
`epsilon = 2^-q`, starting at `q=4` and doubling `q` after each completed
accuracy target. Every round uses the original problem. The best certified
lower bound and feasible objective value are retained across rounds.

Candidate generation tries, in order:

1. The rational incumbent already supplied by the approximation solver.
2. Coordinate reconstruction with denominator at most `R`. A reconstructed
   coordinate must lie within `1/(4R^2)` of its incumbent coordinate;
   integer coordinates retain their actual integer value.
3. Exact stationarity on a proposed active face. Continuous coordinates
   within `tau = 1/(4nR)` of an original endpoint are fixed there; other
   continuous coordinates remain free, and integer coordinates remain
   fixed. Nonsingular equations are solved by rational elimination.
   Singular equations use the exact bounded linear-feasibility routine in
   [rational_optimization.py](../solver/rational_optimization.py).

Each proposal is checked in the original domain. A feasible improvement is
recorded and may warm-start the next approximation round. These proposals
are untrusted for globality: only equal bounds or candidate-value separation
can produce `status="exact"`. The independent verifier never invokes a
stationarity solver, LP solver, grid optimizer, or reconstruction procedure.
It checks the proposed point, objective, replayed lower bounds, and the
integer height calculation directly.

For a unique optimizer satisfying positive quadratic growth, sufficiently
small approximation error places the incumbent within `1/(4R^2)` of its
optimizer. Two distinct rationals of denominator at most `R` differ by at
least `1/R^2`, so coordinate reconstruction then recovers the optimizer.
Its value denominator is at most `V`; once the gap is smaller than `1/V^2`,
separation accepts it. This gives the implementation counterpart of the
existing exact-output theorem. Safety holds for nonunique problems too,
and stationary recovery supplies the general finite-completion guarantee
below. The implementation does not claim a polynomial or fixed-parameter
bound for arbitrary unknown optimal sets.

## General finite recovery, including nonunique optimal sets

**Theorem.** For every nonempty bounded rational mixed box QP, the default
`solve_exact` algorithm returns an exact rational optimizer and value with
sufficiently large finite limits on rounds, total stages, table size, LP
pivots, and runtime. Its proof remains independently replayable. The theorem
assumes the default geometric grid with the conditioning-trial schedule; it
does not cover arbitrary user-selected fixed-slope schedules. No growth
constant or optimizer is supplied. The theorem does not give a general
polynomial or fixed-parameter complexity bound.

There are two additional ingredients beyond value heights.

**Near-set stationary recovery.** Let `S` be the entire optimal set and
`tau=1/(4nR)`. If a feasible point `y` has distance at most `tau/2` from `S`,
the implemented endpoint-snapping rule and exact bounded stationarity
system have a solution, and every solution is globally optimal.

Choose a nearest optimizer `s`. Integer labels agree because their distance
is less than one. Every continuous coordinate active at `s` is snapped to
its correct endpoint. Distinct original rational endpoints differ by at
least `1/D`, whereas `2 tau < 1/D`, so the selection is unambiguous and
cannot switch an active coordinate to the opposite endpoint. Original
singleton coordinates remain fixed. Let `J0` be the continuous coordinates
strictly interior at `s`, and let `J` be those left free by snapping; thus
`J` is a subset of `J0`.

Consider the stationary polytope `P` obtained by fixing the integer and
active coordinates to their values at `s`, retaining the original box, and
requiring all equations `gradient[J0] F = 0`. It is nonempty and bounded.
Every point of `P` has the same objective as `s`: differences are supported
on `J0`, the free gradients vanish, and subtraction of the stationarity
equations annihilates the free Hessian action.

Let `E=J0\J` be the additional coordinates snapped by the rule. For a
selected lower endpoint use slack `x_i-l_i`; for a selected upper endpoint
use `u_i-x_i`. Their sum `q(x)` is nonnegative on `P`, and

\[
q(s)\le |E|(\tau+\tau/2)\le 3n\tau/2=3/(8R)<1/R.
\]

In scaled variables `u=Dx`, each vertex of `P` is determined by independent
stationarity rows and unit bound rows with integer right-hand sides.
Expanding along the bound rows leaves a possibly **nonprincipal** minor of
`DA[J0,J0]`. The same original row-norm product `H` bounds its nonzero
absolute determinant: each chosen row norm is at most its original
continuous row norm, and unused factors in `H` are at least one. Thus every
vertex has a common scaled-coordinate denominator at most `H`. The
quantity `D q` has integer coefficients and constant term in those scaled
variables. If its minimum at a vertex were positive, `min_P q` would be at
least `1/(DH)=1/R`, contradicting the displayed bound. Therefore an
optimizer `s'` in `P` meets **all** selected endpoints simultaneously.

This proves feasibility of the implemented selected-face stationarity
system. If `x` is any other feasible solution, `d=x-s'` is supported on
`J`. Both free gradients vanish, so `A[J,J] d[J]=0`; the exact quadratic
expansion gives `F(x)=F(s')=f*`. No nonsingularity or positive definiteness
of the selected Hessian is needed. The exact LP is essential when the
selected system is singular. This argument specializes the earlier
[proximal recovery lemma](../../research-20261002/new-direction/proximal-exact-recovery.md)
to the implemented row-product height bound; it is not inferred solely from
the existence of a rational optimizer.

**Every requested approximation accuracy is eventually reached.** Let
`s0` be the largest original interval width and
`L=max(0,max_i A[i,i])`. The zero-width and zero-curvature cases give exact
bounds directly or by the endpoint DP. Otherwise a trial uses stage widths
`h_j=s0*2^-j`. Its last stage `J` is chosen so that

\[
7Ln s_0^2 4^{-J}/8\le\varepsilon.
\]

A sufficiently late conditioning trial has `theta <= 2^-J`. Any positive-
curvature continuous gap at stage `J` is at most
`h_J + theta*s0 <= 2h_J`. For integer coordinates, a gap longer than one
satisfies the same bound; unit gaps need zero correction. Nonpositive-
curvature coordinates also need zero correction. Consequently the
corrected-grid minimizer provides

\[
U-LB\le Ln(2h_J)^2/8
       =Ln h_J^2/2\le 4\varepsilon/7<\varepsilon.
\]

The trial's coordinate cap cannot prevent this conclusion. Continuous
steps are at least `h_j`; integer steps are at least `h_j/2` when `h_j>=1`
and at least one otherwise. Counting both directions from the center gives
at most `2*2^J+3` nodes per coordinate throughout the trial. This is smaller
than `100*theta^-1*ceil(log2(n+2))`. Each earlier trial and each exact finite
DP is finite; sufficiently expanded external limits therefore allow a
successful trial. This statement gives finite convergence, even when a
flat optimal set prevents useful coordinate-hull contraction.

Finally, compactness of the original mixed box implies that every feasible
sequence with objective approaching `f*` has distance tending to zero from
`S`. More explicitly, outside any fixed neighborhood of `S`, the continuous
objective attains a strictly larger minimum on the remaining compact set.
Thus sufficiently accurate incumbents satisfy the near-set recovery lemma.
The recovered candidate then has objective denominator at most `V`, and a
gap below `1/V^2` passes the existing value-separation gate. Bland's rule
makes each relevant exact feasibility LP finite; only finitely many
original integer assignments and selected faces are possible, so a finite
LP pivot cap sufficient for all relevant systems exists. Every other
resource requirement in this successful finite prefix is also finite.

This closes the **existence of a terminating exact implementation** for
nonunique problems. It does not close the research question of an efficient
width-and-conditioning bound for unknown optimal sets, and it does not
return a representation of every optimizer.

## API and resource behavior

```python
from certified_grid import BoxQP
from exact_output import solve_exact
from verify_certificate import verify_certificate

problem = BoxQP(
    A=[[2, 1], [1, -2]], b=["-7/3", 0],
    bounds=[(0, 1), (0, 2)], integers=[])
result = solve_exact(problem, max_stages=256, time_limit=30,
                     max_table_states=100000)
checked = verify_certificate(result)
assert checked["exact"]
assert result["point"] == ["1/6", "2"]
assert result["upper"] == "-145/36"
```

Omitting both `bags` and `edges` selects the deterministic min-fill
heuristic. Supplied decompositions remain supported and are checked. The
resolved decomposition is serialized, so replay does not depend on a
heuristic choice.

The command-line entry point also accepts exact mode:

```sh
python research-20261002-decomposition/solver/certified_grid.py \
  problem.json result.json --exact --max-rounds 8 \
  --max-stages 256 --time-limit 30 --max-table-states 100000
python research-20261002-decomposition/solver/verify_certificate.py result.json
```

`max_stages` counts all attempted stages across all precision rounds.
`max_rounds`, `max_table_states`, and the LP pivot cap are explicit. Grid
arithmetic, recovery elimination, and LP pivots share cooperative wall-clock
checks; one arithmetic operation or checking interval can overrun the wall
clock cap. This is not an operating-system process deadline.

If proof is not completed, the result reports `stage_limit`, `table_limit`,
`time_limit`, or `round_limit`, retains valid original-domain bounds and a
feasible point, and carries no exact proof. The verifier checks these
incomplete results as well. A resource limit does not establish infeasibility,
nonuniqueness, or difficulty intrinsic to the mathematical problem.

The implementation uses the shared exact finite-tree engine for messages
and all min-marginals. Sparse neighbor lists now eliminate dense zero-product
work from coordinate polishing and KKT gradients. Dense input storage and
small convex-presolve factorizations remain; this change does not claim a
fully sparse matrix backend.

## Targeted verification

Commands actually run after the final implementation changes:

```sh
python -m unittest discover -s research-20261002-decomposition/solver \
  -p 'test_certified_grid.py'
python -m unittest discover -s research-20261002-decomposition/solver \
  -p 'test_exact_output.py'
```

Results: **16 approximation/integration tests and 12 exact-output tests
passed**. The exact tests cover indefinite rational face recovery without
coordinate polishing, a mixed optimum `(0,1/6)` of value `1/18`, fixed rational
coordinates, singular stationary recovery, two nonunique mixed optimal segments,
extra bound snaps on a singular optimal line with a fixed rational coordinate,
tied endpoint optima, every
wrapper resource limit, rejection of a nonglobal box KKT point, corruption
of heights/models/points/separation proofs, and optimizer-free replay.

Independent review additionally compared 36 small rational continuous,
mixed, and fixed-coordinate models with exhaustive face enumeration. All
36 bounds and certificate replays passed; 20 runs returned exact output and
16 stopped at a stage limit. The strengthened nonunique theorem received
a second adversarial review: six additional near-set recovery checks
covered disconnected mixed optimal segments, simultaneous extra bound
snaps, singular stationarity, and fixed rational coupling. A nonunique
nonconvex example also certified accuracy `1/100` in five grid stages
(160 table states) with convex presolve and polishing disabled. These are
targeted correctness checks, not performance claims. Broader frozen-source measurements are recorded by the
[completion benchmark work](benchmarks/README.md). No project-wide checks or
CI duplication were run for this module.
