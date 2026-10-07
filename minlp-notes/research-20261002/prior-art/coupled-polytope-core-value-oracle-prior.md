# Prior-art audit: finite core noise with coupled polytope feasibility

Date: 2026-10-02. This focused audit compares the completed
[coupled-polytope value theorem](../new-direction/coupled-polytope-core-value-oracle.md),
its [convex-value interface](../new-direction/convex-polytope-value-interface.md),
and the [selected-core output variant](../new-direction/coupled-polytope-core-oracle.md)
with convex-underestimator branch-and-bound, low-negative-inertia QP
algorithms, and the closest project smoothed results. The theorem and value
interface passed independent review. This note is not a proof review or a
publication-priority claim.

## Candidate and scope

The domain is any nonempty bounded rational polytope `P` in continuous
variables `(v,z)`, with a selected core `v in [0,1]^k`; arbitrary linear
equalities and inequalities may couple core and residual variables, and `P`
may be lower-dimensional. The objective `F_0` is an explicit rational
polynomial of fixed degree. A supplied, charged certificate establishes

```text
F_0(v,z) + alpha ||v||^2/2 is convex on P,       alpha >= 0.
```

For `alpha>0`, the theorem perturbs only the `k` core coefficients using one
base-input-chosen finite rational uniform law. For every requested precision
`2^-q`, the same draw yields a rational feasible point and a certified
optimal-value interval of that width. Every draw is correct. Expected bit
work and output size are

```text
f(k) (1 + alpha/sigma)^k poly_d(I+q),
```

and one random work factor controls every precision. The theorem makes no
growth, residual strong-convexity, strict-complementarity, or interiority
assumption. It does not handle integer variables or promise optimizer
distance or expanded algebraic optimizer coordinates. The output is a value
Cauchy oracle with a feasible objective approximation.

The companion [selected-core oracle](../new-direction/coupled-polytope-core-oracle.md)
uses the same law and hypotheses. It additionally returns a feasible point
whose core is within `2^-q` of the core projection of a fixed
lexicographically selected global optimizer. It still does not approximate
that optimizer's residual coordinates or promise full-space optimizer
distance. Its analysis uses a random projected-growth tail, but the growth
constant is not a supplied input.

## The convexification and cell solver are established tools

The cell lower model is

```text
F_c(v,z) + (alpha/2) sum_i (v_i-l_i)(v_i-u_i),
```

on a core box `C=prod_i[l_i,u_i]`, intersected with `P`. Since each product
is nonpositive on its interval, this is a lower bound on `F_c`. Its Hessian
in the core adds `alpha I`; by the supplied convexifier, it is convex on
`P intersect {v in C}`. This is precisely the diagonal-shift/secant pattern
of alphaBB, restricted to the selected core and with the needed convexity
certificate supplied directly.

Adjiman, Dallwig, Floudas, and Neumaier's theoretical alphaBB paper treats
twice-continuously-differentiable constrained NLPs. It constructs boxwise
underestimators by subtracting separable quadratic terms and certifies
convexity through a Hessian shift; Theorem 2.1 gives the exact Hessian
condition, while Theorem 3.1 gives a sufficient interval-Hessian condition.
Their deterministic branch-and-bound method converges to an arbitrarily
accurate global solution on its stated bounded domains. This establishes
the convexification and global lower-bound template. It does not give an
expected complexity bound, a finite random perturbation law, or an
all-precision bit guarantee. The candidate's secant correction is not a new
underestimator; the possible addition is its all-scale random cell count and
certified finite-law composition on coupled feasible slices.
([Adjiman et al., Part I](../../literature/papers/adjiman1998-a-global-optimization-method-bb/paper.md),
Theorems 2.1 and 3.1, pp. 3–5.)

## Closest polynomial-perturbation algorithm: Kannan–Rademacher

Kannan and Rademacher's *Optimization of a Convex Program with a Polynomial
Perturbation* is the closest algorithmic precedent. For a convex body `K`,
a convex function `f`, and a degree-`d` polynomial `p` depending on only
`k` coordinates, their Theorem 4 returns a feasible point `x` with

```text
f(x)+p(x) <= min_K(f+p) + epsilon range_K(p),
```

in time `(O(k d^2 / sqrt(epsilon)))^k T(f,K) + T_tilde(K)`. Here
`T(f,K)` is the cost of the convex program for `f`, and `T_tilde(K)` is the
cost of putting the projected body in near-isotropic position. Algorithm 1
grids the `k` perturbed coordinates and minimizes a linear Taylor model of
`p` on each sliced convex set. The near-isotropic preprocessing is supplied
by a randomized high-probability procedure in Theorem 3. Theorem 4 and
Algorithm 1 are in §3, physical/printed PDF p.4. The theorem states an
oracle-style running-time bound, not a rational Turing bit-complexity bound.
([Kannan–Rademacher, author PDF](https://www.math.ucdavis.edu/~lrademac/fplusp.pdf),
Theorem 4 and Algorithm 1; DOI
[10.1016/j.orl.2009.07.002](https://doi.org/10.1016/j.orl.2009.07.002); read
[local primary package](../../literature/papers/kannan2009-optimization-of-a-convex-program/paper.md).)

The candidate's objective has exactly this convex-plus-low-dimensional
polynomial form on each sampled instance:

```text
f(v,z) = F_0(v,z) + alpha ||v||^2/2,
p_c(v) = -alpha ||v||^2/2 - c'v.
```

Thus `p_c` has degree at most two and depends only on the selected core.
Kannan–Rademacher already establish the deterministic grid-approximation
principle for this structure; objective randomization is not needed for
their correctness. Their theorem is phrased for a convex function on the
ambient space and a full-dimensional convex body, while the candidate only
certifies convexity on `P` and also allows lower-dimensional rational
polytopes. Restricting the convex oracle to a convex feasible body and
reducing its rational affine hull are natural extensions of the method, but
are not literal hypotheses of the cited theorem.

The guarantees differ in accuracy and computation. Kannan–Rademacher's
error is relative to `range_K(p)`. For absolute error `delta`, setting
`epsilon=delta/range_K(p)` makes the grid cost scale as
`(O(k d^2 sqrt(range_K(p)/delta)))^k`. It returns an approximate feasible
point, without a certified rational value interval. Its random step rounds
the body geometry; it does not sample objective coefficients. It gives no
single finite noise law for all accuracies and no expected bit bound
polynomial in `q=log_2(1/delta)`.

The candidate therefore should not claim the convex-plus-low-dimensional
polynomial structure, grid search in the selected variables, or pointwise
approximation for such objectives as new. Its narrower possible advance is
to use one base-input-chosen finite core-noise law to replace the
deterministic `delta^(-k/2)` dependence with expected bit work
`f(k)(1+alpha/sigma)^k poly_d(I+q)`, while returning certified value
intervals at every precision on the same draw. This is a scoped comparison,
not a priority finding.

The convex subproblem on each cell is also a standard rational convex
optimization task. The checked GLS bit-model reduction from weak separation
to weak optimization (Theorem 4.2.2, Remark 4.2.5, and Corollary 4.2.7,
printed pp. 105–106; §4.1, pp. 103–104) gives polynomial Turing complexity
when the rational separation oracle runs in polynomial time. Exact rational
LP handles cell feasibility; rational gradients provide tangent
separators, and the candidate repairs weak output by an LP inside a small
error box so the returned point remains feasible in a lower-dimensional
polytope. These are applications of the classical oracle theorem, not a new
convex solver. The actual rational-polytope reduction and its review are in
the [value interface](../new-direction/convex-polytope-value-interface.md)
and the local [GLS source package](../../literature/papers/grotschel1988-geometric-algorithms-and-combinatorial-optimization/paper.md).

For the quadratic subcase, exact rational convex-QP completion is classical.
Kozlov, Tarasov, and Khachiyan give a deterministic polynomial-bit algorithm
for convex quadratic programming with linear constraints, including
singular PSD Hessians and nonunique minimizers; their exact-solution
definition includes an attaining point and the exact rational optimum value
(pp. 1–5). They state integer input data; clearing rational denominators is
the routine encoding-length extension. This solves each convex quadratic
cell exactly, but does not supply the coupled theorem's randomized global
cell-count bound. See the read [local source package](../../literature/papers/kozlov1980-the-polynomial-solvability-of-convex/paper.md).

## Low-negative-inertia methods are close but have different guarantees

Vavasis's approximation method and Luo, Bai, Lim, and Peng's ADMBB algorithm
are direct global-QP precedents. They isolate a rank-`r` negative-curvature
factor, branch over the factor coordinates, and solve convex quadratic
relaxations on a general linearly or convex-quadratically constrained
feasible set. Luo et al. assume a bounded feasible set and Slater's
condition; their Theorem 3.3 gives an additive `epsilon`-approximation and
bounds the number of convex-relaxation subproblems by a product with
`epsilon^(-r/2)`-type dependence (pp. 13–15). This is not an expected bit
bound or an exact value oracle. The candidate shares low-dimensional
convexification and secant lower bounds, but its parameter is a supplied
coordinate core, its hypothesis is convexity after one fixed core-only
quadratic shift on `P`, and its output guarantee is a finite-law expected
value Cauchy oracle. ([Luo et al.](../../literature/papers/luo2019-new-global-algorithms-for-quadratic/paper.md),
Theorem 3.3; [Vavasis source package](../../literature/papers/vavasis1992-approximation-algorithms-for-indefinite-quadratic/paper.md).)

The project already has a stronger exact-output quadratic comparison. Its
[smoothed exact cell-closure theorem](../new-direction/smoothed-exact-cell-closure.md)
handles rational indefinite QPs on bounded rational polytopes using a
factor-aligned finite rational noise law, returns an exact rational
optimizer and value for every draw, and gives expected bit complexity in
the negative-space dimension and numerical range/noise parameters. The
quadratic subcase of the present theorem should therefore not be advertised
as the first exact smoothed QP algorithm. The two formulations are not
identical: the earlier theorem has a supplied spectral factor and a
nullspace condition, and perturbs its factor coordinates; the present
theorem perturbs selected original core coordinates and assumes the
core-only convexification condition. The earlier result is stronger in
optimizer output on its stated quadratic class; the present theorem's
specific extension is to fixed-degree polynomial objectives and coupled
polytope cell constraints, with value-only output. The project's
[ambient-noise QP audit](smoothed-ambient-noise-prior.md) also records an
exact expected-FPT QP result under a different, all-coordinate noise law.

## Closest smoothed polynomial results in the project

The nearest predecessor is the project's
[all-scale core-only value theorem](../new-direction/all-scale-core-value-oracle.md).
It already provides the same one-finite-law, all-accuracy value interface
for arbitrary `k` on a product box, when the residual objective is convex
for every fixed core and core coordinates have a verified upper-curvature
bound. The present theorem replaces product feasibility by an arbitrary
rational polytope and replaces fixed-core residual convexity with the
stronger joint convexifier `F_0+alpha||v||^2/2` on `P`. That condition makes
every coupled core-cell slice a convex polynomial problem. The extension is
about preserving certified lower bounds and feasible upper values despite
core/residual coupling in the constraints; the all-scale probabilistic
principle is inherited.

The project's [smoothed polynomial box-recourse theorem](../new-direction/smoothed-polynomial-box-recourse.md)
is a complementary nonlinear result: it solves fixed-degree polynomial
objectives exactly in an implicit form on a product box, uses independent
finite perturbations on every original coordinate, and needs convexity
only in residual coordinates after fixing the supplied core. It does not
cover arbitrary coupled polytope constraints or core-only noise. It also
returns stronger optimizer information than the present value theorem.
Conversely, the coupled-polytope theorem needs the joint convexifier and
does not provide the prior theorem's exact implicit optimizer on ordinary
instances. The two results should be presented as complementary models,
not as an unqualified strengthening.

The selected-core variant is closest to the project's earlier
[box-core Cauchy certificate](../new-direction/core-only-noise-core-oracle.md):
both recover a selected core to requested accuracy while controlling the
full objective, without asking for residual-coordinate convergence. The
coupled version handles an arbitrary rational polytope but retains the
joint-convexifier condition and the same core-only noise model. This is an
internal extension, not a separate external-priority claim.

The external and local results examined establish alphaBB/secant
underestimators, low-rank QP partitioning, exact convex subproblem oracles,
and smoothed polynomial optimization on product domains. This focused
comparison did not identify a result with the exact combined model here:
arbitrary bounded rational linear coupling, a fixed-degree objective with
the supplied core-only convexifier, one finite core-noise law for every
precision, and expected bit work for certified value intervals. That
bounded search is not evidence of publication priority. The claim should
remain the specific coupled-feasibility extension, with the convexifier,
noise support, and value-only output stated explicitly.

## Source status

The Kannan–Rademacher author PDF was read and is now stored in the local
package at [kannan2009-optimization-of-a-convex-program](../../literature/papers/kannan2009-optimization-of-a-convex-program/paper.md).
The alphaBB, Luo, Vavasis, exact cell-closure, GLS, and
Kozlov–Tarasov–Khachiyan texts cited above were read in the local source
packages. The exact convex QP output source is Kozlov–Tarasov–Khachiyan,
“The Polynomial Solvability
of Convex Quadratic Programming” (1980), Theorem/result discussion on pp.
1–5; this is an exact rational-output result, unlike the weak-optimization
interface used for general convex polynomial cells. No new KB package or
index entry was created for this audit.
