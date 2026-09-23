# A certified scalar-leader quadratic prototype

Date: 2026-09-06. Status: implemented, tested, and
[independently reviewed](review-bilevel-reopened-quadratic-algorithm.md).
This is an implementation contribution supporting the
[fixed-rank quadratic corollary](bilevel-fixed-rank-quadratic-corollary.md),
not a claim of a new general parametric-QP method.

## Scope and practical purpose

Consider the unique response

\[
 z(x)=\arg\min_{0\le z\le1}
 \tfrac12 z^TQz+(c+Cx)^Tz,
 \qquad x\in[\ell,u],
 \qquad Q=D+UHU^T\succ0,
\]

where every input is rational, `D` has positive diagonal, `H` is symmetric,
and `x` is scalar. The leader minimizes an affine function of `(x,z)`, optionally
plus a term `a*x^2+x*b^Tz`,
subject to explicit affine upper constraints, including constraints on the
response. The code produces an exact rational description of the full response
path, then solves each upper problem by interval clipping. A path can be reused
for many upper objectives and policy constraints without another follower solve.

This answers the implementation gap left by the abstract arrangement theorem:
on the synthetic instances recorded here, exact response certificates for up to
120 followers are inexpensive enough to compute directly. It does not establish
industrial performance, dominance over MILP, or a polynomial implementation of
the full arrangement theorem.

## Exact active-pattern certificate

Give every coordinate a label lower, free, or upper. Write `F` for the free
indices and `B` for the upper indices. The active-pattern equations are

\[
 z_B=1,\quad z_L=0,\quad
 Q_{FF}z_F=-(c_F+C_Fx)-U_FH\sum_{i\in B}U_i^T.
\]

Every principal matrix `Q_FF` is positive definite, so this determines an affine
rational vector `a+bx`. It is the unique follower response exactly on the closed
interval defined by

\[
 0\le a_i+b_ix\le1\ (i\in F),\qquad
 (Q(a+bx)+c+Cx)_i\ge0\ (i\in L),\qquad
 (Q(a+bx)+c+Cx)_i\le0\ (i\in B).
\]

All these inequalities are affine in `x`. Intersecting their rational half-lines
with `[ell,u]` gives either an empty set, a singleton, or a closed interval.
No strict complementarity or distinct-breakpoint assumption is needed.
The proof is simply the necessary and sufficient box KKT conditions for a
strictly convex quadratic objective.

The verifier checks box feasibility and gradient signs at both interval
endpoints, and checks that bound-labeled coordinates are identically at their
stated bounds. For free coordinates it checks zero gradient at both endpoints.
Affineness establishes the corresponding conditions throughout each interval;
on a singleton the checks are just the fixed-point KKT conditions. It also checks
that the interval union covers the entire leader domain. Consequently a verified
path proves every response, not just the numerical sampling points.

## Small exact linear systems

The implementation does not form or invert the dense free Hessian. Put

\[
 S=U_F^TD_F^{-1}U_F,\qquad
 t=U_F^TD_F^{-1}v.
\]

For either affine coefficient right-hand side `v`, solve

\[
 (I+SH)w=t,\qquad
 z_F=D_F^{-1}(v-U_FHw).
\]

The determinant identity
`det(Q_FF)=det(D_FF) det(I+SH)` proves that the small system is invertible.
This formula permits singular or indefinite `H`; it does not invert `H`.
Its arithmetic operation count per active pattern is `O(N(1+k^2)+k^3)`,
excluding rational bit growth and the numerical proposal solve.
Exact input validation first checks whether `H` is positive semidefinite. If it
is, `D>0` already proves `Q>0`. For negative rank-one `H=(h)`, it checks
`1+h*sum_i u_i^2/d_i>0`, an exact necessary and sufficient condition. For other
indefinite `H` the prototype forms `Q` and applies exact dense elimination.
Thus the stated fast per-pattern cost does not imply a fast initial SPD check
for arbitrary indefinite `H`.

## Discovering a complete path

1. Choose the rational midpoint of an uncovered parameter gap.
2. Solve the follower numerically there with L-BFGS-B and use the numerical
   vector only to propose active labels.
3. Recover the affine response and its maximal validity interval in exact
   rational arithmetic. Accept only a verified interval containing the sample.
4. Add the interval and repeat until the union covers the domain.

The numerical solver is not trusted for optimality or even successful
termination. Several tolerances propose labelings; every labeling must pass
exact checks. For at most nine followers, failure triggers exhaustive `3^N`
pattern recovery. Larger recovery failures raise an explicit exception, and
the caller receives no certified answer. A user-supplied segment-count cap also
raises an exception rather than returning an incomplete path. Raising
`exhaustive_limit` does not itself make the numerical proposal universally
applicable: float conversion or numerical libraries can fail before that
fallback is reached. The separate `exhaustive_path` function is a finite exact
algorithm on arbitrary rational inputs, but it is exponential and is not a
competitive general-purpose design.

Why the idealized process terminates: every pattern has one fixed maximal
validity interval, and there are finitely many patterns. A chosen midpoint is
outside the already certified union, so its accepted interval cannot have been
added before. A singleton at a breakpoint splits a gap without discarding either
side. With exact recovery available and no cap, at most `3^N` additions are
possible before coverage is complete. The implementation avoids a homotopy pivot
rule, so simultaneous switches and persistent zero multipliers require no
tie-breaking theorem.

The fixed-rank corollary separately proves polynomial solvability for fixed rank
and leader dimension by arrangement enumeration. That theorem should not be
represented as a proved polynomial runtime bound for this heuristic-plus-
exhaustive prototype.

## Exact upper optimization, including isolated feasibility

On each certified interval substitute `z=a+bx` in the upper constraints.
Keep the closed feasible intersection, including an interval of length zero.
The affine upper objective attains its minimum at one of its endpoints, selected
by the sign of its slope. Comparing these rational candidates solves the global
upper problem. If every intersection is empty, infeasibility is certified.
Two weak inequalities encode an equality. Therefore a single feasible point at
a response breakpoint, or inside a response cell, is retained exactly.

There is no leader mesh and no tolerance for upper feasibility. The exact
certificate remains useful when a numerical upper solver would blur a narrow
feasible region or an equality. This is a consequence of classical parametric
QP structure, not a new exact-arithmetic complexity barrier result.

### Quadratic upper costs and tariff revenue

More generally, any rational quadratic function of `(x,z)` becomes a rational
univariate quadratic after substituting an affine response. Its minimum on a
closed interval is attained at an endpoint or, when its leading coefficient is
positive, at its rational stationary point if that point lies in the interval.
Thus the scalar specialization still returns a rational global optimum.

The implemented objective class is

\[
 o_x\,x+o_z^Tz+o_{xx}x^2+x\,o_{xz}^Tz.
\]

In code the arguments are `objective_x`, `objective_z`, `objective_xx`, and
`objective_xz`. This includes negative tariff revenue `-x*sum(z)` for revenue
maximization, and an additional quadratic price penalty. It does not implement
arbitrary `z_i*z_j` upper terms. Affine upper constraints are unchanged.

For `z=a+bx`, the quadratic coefficients are

\[
 \alpha=o_z^Ta,\quad
 \beta=o_x+o_z^Tb+o_{xz}^Ta,\quad
 \delta=o_{xx}+o_{xz}^Tb.
\]

Compare both endpoints and, if `delta>0`, `-beta/(2*delta)` when feasible.
This is a classical elementary consequence of the response path, retained
because tariff revenue is a more useful application than an affine proxy.

## A complete exact sweep for an aligned rank-one price

There is a useful complete specialization that avoids numerical recovery. Suppose

\[
 Q=D+h uu^T\succ0,\qquad C=\gamma u,\qquad \gamma>0.
\]

Signed and zero coordinates of `u` and either sign of `h` are permitted. Introduce
the effective price

\[
 t=\gamma x+h u^Tz,\qquad
 z_i(t)=\operatorname{clip}_{[0,1]}\left(-\frac{c_i+u_it}{d_i}\right),\qquad
 A(t)=u^Tz(t).
\]

Then `x(t)=(t-h*A(t))/gamma`. Each nonzero `u_i` contributes two rational
thresholds `-c_i/u_i` and `-(c_i+d_i)/u_i`. Between successive thresholds,

\[
 A(t)=A_0+A_1t,\qquad
 A_1=-\sum_{i\in F}\frac{u_i^2}{d_i},\qquad
 \frac{dx}{dt}=\frac{1+h\sum_{i\in F}u_i^2/d_i}{\gamma}>0.
\]

For `h>=0`, positivity is immediate. For `h<0`, the rank-one SPD condition is
`1+h*sum_all u_i^2/d_i>0`, and every free-set sum is smaller, proving the displayed
strict inequality. The clipped response and `A(t)` are continuous. At either
infinite tail `A(t)` is constant, so `x(t)` tends to the corresponding infinity.
Consequently `x(t)` is a continuous strictly increasing bijection of the real
line. On every threshold interval it can be inverted exactly:

\[
 t=\frac{\gamma x+hA_0}{1-hA_1}.
\]

This proves at most `2N+1` response intervals, with ties grouped. It also proves
that sorting the effective-price thresholds enumerates the entire response
without a numerical QP or an exhaustive pattern fallback. Upper constraints may
still cut a response interval down to a singleton, which the implementation
preserves.

The sweep keeps weighted response intercepts and slopes for `u`, the upper
objective vectors, and each upper constraint. At an event only the switching
coordinates change, so it updates these sums directly. With `m` explicitly
supplied upper constraints, sorting and all updates use
`O(N log N+N(m+1))` rational operations and `O(N(m+1))` storage, apart from bit
costs. It reconstructs the full response only at the final optimal price.
Rational bit lengths remain polynomial: breakpoints, sums, affine inversions,
and quadratic stationary points use rational arithmetic on explicit input
coefficients and sums with at most `N` terms. The operation bound is not a
unit-cost wall-clock assertion for arbitrarily large coefficients.

The API is `optimize_aligned_rank_one`, with the same objective/constraint
convention as `optimize_path` and optional `gamma=1`. The `Problem` constructor
verifies the SPD assumption, including the negative rank-one case, exactly.
This is a classical breakpoint-sweep specialization rather than a new general
algorithm; its value here is the complete fast exact implementation and the
direct handling of response-constrained tariff optimization.

## Implementation and reproducible evidence

- [Solver](../code/bilevel_reopened/quadratic_solver.py): `Problem`,
  `solve_response_path`, `verify_path`, `optimize_path`, and `exhaustive_path`.
- [Benchmark driver](../code/bilevel_reopened/quadratic_benchmarks.py).
- [Saved data](../code/bilevel_reopened/quadratic_benchmark_results.json).

Run from the repository root:

```sh
python code/bilevel_reopened/quadratic_benchmarks.py
```

Input numbers must be integers, `Fraction` objects, or exact decimal strings.
Binary floating point inputs and certificate coefficients are rejected.
The numerical proposal uses NumPy/SciPy; all accepted path coefficients and upper
solutions use Python `Fraction` arithmetic.

The saved run includes 12 random four-follower cases checked against all active
patterns and an independently constructed numerical KKT MILP, plus eight scaling
cases. The MILP has separate binary lower/upper activity indicators and a valid
box-derived gradient bound. All 18 MILP comparisons completed to reported
optimality, and the largest objective difference was `1.22e-13`. The MILP is an
independent numerical comparison, not the source of the exact certificate.
All paths passed exact verification. No exhaustive recovery was needed in these
20 generated cases.

| Followers | Rank | Certified intervals | Path seconds | Upper seconds | KKT MILP seconds |
|---:|---:|---:|---:|---:|---:|
| 10 | 1 | 7 | 0.010 | 0.001 | 0.007 |
| 10 | 2 | 9 | 0.016 | 0.003 | 0.046 |
| 30 | 1 | 21 | 0.072 | 0.016 | 0.050 |
| 30 | 2 | 25 | 0.091 | 0.025 | 0.146 |
| 60 | 1 | 48 | 0.226 | 0.044 | 0.198 |
| 60 | 2 | 45 | 0.322 | 0.071 | 0.290 |
| 120 | 1 | 87 | 0.679 | 0.245 | not run |
| 120 | 2 | 112 | 1.357 | 0.355 | not run |

These are single runs in a shared environment, without timing isolation, so
they cannot support a scaling-law or speed superiority claim. The generated
costs model positive scalar price exposure,
with signed aggregate loadings, diagonal convex local costs, and a response-
dependent service floor. They are synthetic data, not a calibrated application.

Boundary checks cover simultaneous switches, an isolated feasible leader point,
an isolated feasible response equality, infeasibility, indefinite `H` with SPD
`Q`, a singleton leader domain, persistent zero multipliers, and rejection of a
non-SPD Hessian. The [independent review](review-bilevel-reopened-quadratic-algorithm.md)
adds dense KKT-face LP comparisons, quadratic objective comparisons, exact
narrow-feasibility checks, and extreme rational-input sweep checks.

### Larger exact tariff sweeps

The separate [tariff driver](../code/bilevel_reopened/quadratic_tariff_benchmarks.py)
and [saved data](../code/bilevel_reopened/quadratic_tariff_benchmark_results.json)
maximize `x*sum(z)` under `sum(z)>=N/5` and `0<=x<=3`. Local quadratic costs and
linear utility coefficients are randomly generated rational numbers;
`u_i=1` and `h=+/-1/(10N)`. This is an uncalibrated synthetic common-price demand
model, included to test the exact algorithm rather than infer actual prices.

| Followers | Sign of h | Distinct thresholds | Visited response intervals | Sweep seconds | Optimal price |
|---:|---:|---:|---:|---:|---:|
| 100 | positive | 199 | 151 | 0.012 | 0.930180 |
| 1,000 | positive | 1,955 | 1,443 | 0.141 | 0.952713 |
| 10,000 | positive | 15,372 | 11,033 | 1.047 | 0.967309 |
| 1,000 | negative | 1,947 | 1,518 | 0.126 | 0.954607 |

All outputs are exact rationals in the saved data; the table rounds only for
display. Input/SPD validation took at most 0.048 seconds in this run and is
reported separately. Every returned response passed exact KKT checks and the
service floor. The 100-follower case also matched the general certified response
path's global quadratic upper optimum exactly. This is evidence that the aligned
case permits substantially larger exact computations, not evidence of superior
performance over a state-of-the-art specialized implementation.

## Literature and novelty boundary

The parametric-QP response being continuous and piecewise affine, and solving
an upper problem on response regions, are established ideas. Relevant openly
accessible primary sources located on 2026-09-06 include:

- Bemporad, Morari, Dua, and Pistikopoulos (2002), *The explicit linear quadratic
  regulator for constrained systems*, Automatica 38, 3–20.
  [Author-hosted full text](https://cse.lab.imtlucca.it/~bemporad/publications/papers/automatica-mpqp.pdf).
  This develops explicit parametric quadratic solutions and their affine regions.
  Its [2003 corrigendum](https://cse.lab.imtlucca.it/~bemporad/publications/papers/automatica-mpqp-corrige.pdf)
  corrects a numerical example.
- Tøndel, Johansen, and Bemporad (2003), *An algorithm for multi-parametric
  quadratic programming and explicit MPC solutions*, Automatica 39, 489–497.
  [Author publication page](https://torarnj.folk.ntnu.no/optimization.html),
  [publisher abstract](https://doi.org/10.1016/S0005-1098(02)00250-9).
  It studies region geometry and an active-set exploration strategy. The
  author-page PDF link redirected unsuccessfully during this audit; the
  comparison here is limited to the abstract and author bibliographic record.
- Arnström and Axehill (2020 preprint), *A Unifying Complexity Certification
  Framework for Active-Set Methods for Convex Quadratic Programming*.
  [Open preprint](https://arxiv.org/abs/2003.07605).
  Its object of certification is an active-set algorithm's iteration complexity;
  that is distinct from this prototype's rational certificate of the complete
  follower response. This distinction does not establish novelty for the latter.
- The earlier corollary already cites Megiddo and Tamir (1993) for
  low-dimensional multiplier arrangements in separable quadratic optimization.
- Kiwiel (2002 technical report; later Mathematical Programming 112, 473–491,
  2008), *Breakpoint searching algorithms for the continuous quadratic knapsack
  problem*. [Open technical report](https://rcin.org.pl/Content/139441/PDF/RB-2002-77.pdf).
  Its introduction explicitly describes the clipped scalar-multiplier response,
  `2N` breakpoints, and earlier `O(N log N)` sorting methods, as well as faster
  selection methods for finding one target multiplier. This is the direct
  antecedent for the aligned sweep's elementary breakpoint mechanism. The
  present use maps the effective price back to the leader price and optimizes
  an upper objective along all intervals; neither the clipping mechanism nor
  the sorting complexity should be claimed as new.

The contribution recorded here is a working, independently checkable scalar
specialization and its computational evidence. It should appear as implementation
support in a broader structured-bilevel paper, not as a claimed new general
parametric programming algorithm.
