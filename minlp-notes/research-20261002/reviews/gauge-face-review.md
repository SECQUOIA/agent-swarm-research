# Adversarial review of the coordinate-face construction

Date: 2026-10-02. Scope: the synchronized and selected-face algorithms in
[the exploration](../new-direction/gauge-face-exploration.md), using the
rounding and mesh lemmas of [the grid theorem](../geometric-dp/theorem.md).
This is a mathematical review with targeted exact-arithmetic checks, not a
literature review or a claim of originality.

## Verdict

Both algorithms and their stated contraction, certificate, and solve-count
bounds pass this review. In particular, the selected-face algorithm does not
assume growth about the minimizer of each face. A canonical reference outside
the box causes no gap in its proof.

The original comparison with anchor-zero substitution needed a qualification:
invariance only inside the box does not justify evaluating the objective at
an infeasible anchor-zero representative. Also, a quadratic objective with a
positive-length optimal translation orbit must have a positive semidefinite
Hessian. The general theorem can cover nonconvex functions with an interval
of optima, but indefinite quadratics cannot demonstrate that particular case.
Neither issue invalidates the face algorithms. The author corrected both
scope statements, clarified the path feasibility condition, and added
nonconvex examples during this review. I read the revised scope section;
these findings are resolved in the current exploration.

## Certificate and synchronized contraction

Subtracting the minimum lower-bound slack preserves every upper and lower
coordinate bound and reaches a lower face. Thus the face-cover identity is
valid. Each face solve has its own valid lower bound, and their minimum is a
global lower bound. Selecting the minimizing face is essential for using
global growth: an arbitrary face lower bound need not lie below `f*`.

For a point on the selected face, nonexpansiveness of clipping bounds its
distance to the clipped center by its distance to the unclipped center.
The two nearest optima need not coincide, but their difference lies in the
kernel of `T_j`. Consequently the bound
`||z_k-c_k^j|| <= sqrt(n)(r_k+r_(k-1))` holds even when the iterates approach
different ends of the optimal interval.

The mesh correction is therefore bounded by

    D <= Ln h_k^2/4 + Ln theta^2 (r_k^2+r_(k-1)^2)/2.

With `Ln theta^2/2 <= g/16`, rearranging growth gives exactly the stated
coefficients `4Ln/(15g)` and `1/15`. The induction with
`B=max{1,4L/(11g)}` works at stage zero and at subsequent stages. The two
cases for `n theta^2 B` give the claimed `7Ln h_k^2/8` certificate. The
specified `J` also handles `J=0` correctly. If every stage is executed, the
synchronized algorithm uses exactly `n(J+1)` face solves through stage `J`;
early stopping can only reduce this count.

## Selected-face algorithm and nonoptimal faces

Stored bounds remain valid when another face changes its grid. At every
selection their minimum is at most `f*`, so the selected stored solution
satisfies the growth inequality needed in the proof. Neither monotonicity
of the bounds nor simultaneous grids is required.

Write `alpha=sqrt(g/n)` and `w=sqrt(D)`. The two inequalities are
`alpha d <= w <= A+b(d+r)`, with `b/alpha<=1/4`. Thus

    w <= (A+b r)/(1-b/alpha) <= (4/3)(A+b r).

A failure means `w>sqrt(eps)=4A`. Hence `br>2A`, which is exactly `r>R`.
Also

    d <= (A+b r)/(alpha-b) < (3br/2)/(3b)=r/2.

These are strict inequalities even at the allowed parameter threshold.
They concern distance to the fixed canonical reference, whether or not it
is feasible. The reference identity uses an actual optimum only to bound
distance; it never evaluates the objective at that reference.

Initially every squared distance is at most `ns^2`. After `m` failures on
one face, its center has distance at most `R` (strictly less if `m>0`), so
that face cannot fail again when selected. There are at most `nm` failures.
Initialization costs `n` solves, each failure causes one new solve, and
successful selection causes none: the stated `n+nm` bound counts actual
solves without an extra terminal solve. The `m=0` case is valid.

## Scope, sparsity, and attempted counterexamples

Fixing a coordinate and adding unary correction terms preserves existing
factor scopes and cannot increase the supplied bag sizes. Per-face grid
counts and summation of stage costs give the displayed table-work bounds.
These are exact-oracle table-work statements, not new bit-complexity claims.
The dependence on `theta^-p`, dimension through admissible `theta`, and a
logarithmic exponent depending on `p` supports the note's explicit refusal
to claim a uniform fixed-parameter algorithm in bag size alone.

The gauge operator constant is sharp. For `v_j=0` and all other entries
equal to one, `||v||^2=n-1` and
`dist(v,span{1})^2=(n-1)/n`. This proves sharpness of this norm argument,
not a lower bound on every possible algorithm.

The original anchor-zero sentence is false for a generic box-only symmetry.
For example, on `X=[1,2]^2`, let

    F(x)=(x_2-x_1)^2 + sum_i max(1-x_i,0)^4.

On the box this has translation invariance, diagonal optimal set, `g=2`,
and `L=2`. Yet `F(1,1)=0` while `F(0,0)=2`. Its off-box expression cannot
be substituted at anchor zero. The comparison is repaired by requiring a
globally invariant extension for this identity, or by retaining the shift
and substituting `x_i=u_i+t` into each original factor. The latter gives
bags of size at most `p+1` without any off-box evaluation. Quotient values
are well-defined on feasible fibers, but a sparse formula for them does not
follow merely by evaluating an arbitrary extension at anchor zero.

For path edge differences, exact quotient feasibility on a unit box is
that the range of prefix sums, including the initial zero, is at most one.
Equivalently every contiguous sum lies in `[-1,1]`. Bounding only each prefix
sum is insufficient: edge differences `(3/4,-3/4,-3/4)` have prefixes
`(0,3/4,0,-3/4)` and all individual edges and prefixes meet those bounds,
but the prefix range is `3/2`. “Every cumulative difference” should mean
every contiguous sum, rather than only prefixes.

If the optimal orbit has positive length, an interior orbit point is an
interior point of every nondegenerate coordinate interval. For a quadratic
objective, second-order necessity at this interior minimum forces `H>=0`.
For a nonconvex example genuinely covered by the general theorem, use
`F=(x_1-x_2)^2-(x_1-x_2)^4/2` on the unit square. Its optimal set is the
diagonal, `g=1`, and `L=2`; its Hessian has a negative eigenvalue near the
corners. There it is negative semidefinite, not strictly indefinite.

The added connected-graph family also checks out. Every edge difference
lies in `[-1,1]`, so each quartic term dominates half the squared difference.
The coordinate mean lies in `[0,1]`, hence projection onto the full diagonal
line is also projection onto the optimal segment. The Laplacian spectral
inequality gives `g=lambda_2/2`, and summing edgewise diagonal second
derivatives gives `L=2 max_degree`. The negative second derivative at the
specified corner persists at nearby interior points, establishing
nonconvexity on the feasible box.

No counterexample to either algorithm was found. The coordinate-face idea
and elementary gauge substitution alone do not establish novelty. No
external prior-art investigation was performed for this review.

## Targeted verification record

Commands actually run were the following local reads and three inline
Python invocations; no project-wide verification or CI inspection ran:

- `pwd && rg --files -g 'AGENTS.md' -g '*gauge*' -g 'theorem.md'`
- `cat AGENTS.md`
- `cat research-20261002/new-direction/gauge-face-exploration.md`
- `cat research-20261002/geometric-dp/theorem.md`
- `rg --files research-20261002 | rg '(checks/|reviews/)'`
- `sed -n '185,300p' research-20261002/new-direction/gauge-face-exploration.md && git diff --check -- research-20261002/reviews/gauge-face-review.md`
  read the revised scope and returned no whitespace diagnostics. Since the
  review was newly added and untracked, the diff command is not represented
  as an independent content check.
- `python3 - <<'PY' ... PY`, first two-dimensional harness: failed with an
  `IndexError` in the harness's adjacent-interval construction before any
  mathematical assertions ran. The endpoint indexing was then corrected.
- `python3 - <<'PY' ... PY`, corrected two-dimensional harness: passed
  96 synchronized stages, 192 face solves, and 2,264 grid vertices, including
  four selections of nonoptimal faces. Passed nine selected-face cases,
  22 actual solves, and 346 grid vertices. Also checked the two explicit
  anchor-zero and path-prefix counterexamples above.
- `python3 - <<'PY' ... PY`, three-dimensional selected-face harness: passed
  five actual solves and 3,989 exhaustive grid assignments, including one
  failed selection with an infeasible canonical reference.

The harnesses used `fractions.Fraction`, built each full geometric grid,
computed endpoint penalties from the largest adjacent interval, and
exhaustively minimized the corrected objective. The two-dimensional family
was `F=(x_2-x_1-delta)^2` on `[0,1]^2`, with
`delta in {0,1/2,1}`, `L=2`, and the valid common growth bound `g=1`.
Synchronized runs used all four corner initial centers, `theta=1/8`, and
eight stages. Lazy runs used `theta=1/4` and
`eps in {2^-4,2^-8,2^-12}`. Assertions checked the global lower bound,
certificate, synchronized recurrence and gap, lazy strict halving and
failure radius, termination, and actual solve-count bound.

The three-dimensional family was `[0,1]^3` with

    offset=(0,1/100,3/4),
    F=sum_(i<j) ((x_i-offset_i)-(x_j-offset_j))^2,
    L=4, g=1, theta=1/8, h=1/128, eps=3/1024.

Here `S=offset+[0,1/4]1`. To see `g=1`, project `x-offset` onto the common
shift interval. If its mean is feasible, the objective is three times the
squared distance. If the projection hits an endpoint, one residual has
sign opposite the residual sum; Cauchy–Schwarz on the other two residuals
then gives `F>=dist(x,S)^2`.

Smallest-stored-bound selection caused failure counts `[1,1,0]`. The
second face has infeasible reference `(-1/100,0,74/100)` and nevertheless
passed the strict halving assertion on its failed selection. The terminal
selected solve passed its global lower-bound certificate. This finite
example exercises the principal nonoptimal-face concern; it does not
replace the general proof above or establish numerical solver performance.
