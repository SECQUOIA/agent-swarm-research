# Prior-art audit: core-only noise with strongly convex polynomial recourse

Date: 2026-10-02. This focused comparison covers the reviewed
[core-only-noise boundary-recourse theorem](../new-direction/core-only-noise-boundary-recourse.md).
It credits classical sensitivity, generic-tilt, partial-convexity, and
low-rank methods. It does not establish publication priority.

## Candidate result and scope

The candidate is a fixed-degree rational polynomial on a product box. A
supplied coordinate core has size `k`, and a supplied rational certificate
proves that the residual Hessian block is uniformly at least `mu I` on the
whole box. Core diagonal curvature is bounded above by `L`. Independent
finite rational linear perturbations are applied only to the core. Residual
coordinates may be at, near, or switching between box bounds; no active set,
interior selector, strict complementarity, or multiplier margin is supplied.

For one base-chosen finite noise law, the expected initial bit work and
proof-record size are

```text
8^k [3+(1+k)L/(2 sigma)]^k poly_d(I).
```

The solver usually returns an exact implicit optimizer as the unique minimizer
of a certified strongly convex polynomial on a rational product patch. It
provides polynomial-bit point and value refinement. A same-draw algebraic
fallback handles unresolved samples, with polynomial expected cost. The
global pruning trace has an expected-size bound, not a uniform per-draw bound.
The finite noise law and core-only perturbation are material: the theorem
does not perturb residual objective coefficients or solve the unperturbed
problem.

The residual modulus `mu`, mixed derivatives, and coefficient heights enter
the polynomial bit factor through localization and precision thresholds. The
displayed exponential/numerical factor uses the original core curvature
`L/sigma`; it does not substitute the potentially much larger
`(M_1+M_1^2/mu)/sigma`.

## Standard mechanisms and their limits

Strong convexity of the fixed-domain residual problem gives a unique
conditional minimizer and a Lipschitz solution map by strong monotonicity of
the variational inequalities. Danskin's theorem then gives the derivative of
the partial-minimum value function from the core derivative at that
minimizer. On a region with a fixed residual active pattern, the implicit
function theorem gives the usual Schur-complement Hessian. These are standard
parametric-convex-analysis mechanisms, and the candidate proves the required
bounds directly. The important boundary distinction is that the candidate
does not need a globally fixed active pattern: it uses algebraic tube bounds
to avoid branch transitions near the sampled optimum, and releases weakly
active residual bounds instead of needing a multiplier lower bound.

Bonnans and Ioffe characterize quadratic and strong growth, including
stability consequences for smooth convex constrained problems with possibly
nonisolated solution sets. This is analytic sensitivity prior art, not a
randomized search or a complexity theorem. Their hypotheses and conclusions
do not give the finite-law tail, the exact same-draw optimizer, or the
core-dimension runtime bound. [[bonnans1995-quadratic-growth-and-stability-in]]
pp.2-5, 14-15

Exact multiparametric methods also provide a useful boundary. For convex
piecewise-quadratic parametric problems, Patrinos and Sarimveis show that the
value function is piecewise quadratic and the solution map is polyhedral;
their adjacency algorithm traverses full-dimensional critical regions.
It allows nonunique solutions without strict convexity, and a unique
piecewise-affine selector in the strictly convex case. The stated traversal
is output-sensitive but has no general polynomial bound on the number of
regions. It applies to convex piecewise-quadratic parametric programs, not
the candidate's general fixed-degree conditional polynomial value function
or its smoothed expected closure. [[patrinos2011-convex-parametric-piecewise-quadratic-optimization]]
pp.7-9, 14-17

## Generic tilts and smoothed optimization

Lee and Phạm give the closest qualitative genericity baseline. On a compact
semialgebraic feasible set, a generic vector of polynomial objective
coefficients yields a unique optimizer and global quadratic growth; their
Theorem 6.1 gives an open dense semialgebraic coefficient set. Their later
Theorem A treats generic full-dimensional linear tilts of a fixed regular
semialgebraic set, with a locally constant active manifold, local uniform
quadratic growth, and a global sharp-minimum inequality. These results credit
generic uniqueness, growth, and local active-manifold sensitivity. They do
not quantify the probability of small growth or a near-active transition,
do not establish genericity under noise restricted to a prescribed
`k`-coordinate subspace, and give no expected bit-work or finite-grid
algorithm. The candidate also permits weak residual multipliers and does
not compute or enumerate the active manifolds. [[lee2016-stability-and-genericity-for-semi]]
pp.20-21; [[lee2017-generic-properties-for-semialgebraic-programs]]
pp.3-4

Beier and Vöcking provide the close finite-perturbation analogue for discrete
optimization: independent random objective coefficients isolate the best
and second-best feasible values, enabling smoothed algorithms from
pseudopolynomial procedures. A continuous feasible box has no positive
second-best gap, so winner isolation does not replace the candidate's
distance-normalized growth tail or local patch closure. Kelner and Nikolova
give an expected smoothed algorithm for constant-rank quasi-concave
minimization under random rotation of a low-rank objective subspace. That
work establishes expected global optimization at low nonconvex dimension,
but it has a different objective class and random model and does not give
exact rational output for every finite-grid sample. These sources are
compared in more detail in the existing
[smoothed exact QP audit](smoothed-exact-qp-prior.md).

## Low-rank convexification is an existing representation

The theorem does not introduce a new class beyond low-rank concave-quadratic
perturbations of convex functions. If `M_1` bounds the relevant Hessian
operator blocks and `H_RR >= mu I`, a Schur-complement estimate gives

```text
H_F + alpha diag(I_C,0) >= 0,
alpha = M_1 + M_1^2/mu.
```

Thus `F = G - (alpha/2)||x_C||^2` on the box for a convex polynomial `G`;
the concave quadratic has rank at most `k`. This credits the standard
low-rank DC/convexification viewpoint. Vavasis and Luo et al. give global
algorithms for low-negative-inertia quadratic programs by branching in the
negative-curvature coordinates and solving convex relaxations. Their
guarantees are accuracy-dependent and their objectives are quadratic; they
do not give the candidate's expected exact finite-noise bit bound for
nonlinear dense convex recourse.
[[vavasis1992-approximation-algorithms-for-indefinite-quadratic]]
pp.2-7; [[luo2019-new-global-algorithms-for-quadratic]] pp.2-4, 13-15

The distinction that remains is quantitative and algorithmic. The natural
convexification scale `alpha` can be much larger than `L` when cross-Hessian
blocks are large or `mu` is small. The candidate's cell count is controlled
by the original core upper curvature `L` and noise width `sigma`; residual
conditioning changes the polynomial-bit cutoff and exact-recourse work, but
does not replace `L` in the exponential factor. It also avoids expanding the
conditional value function or enumerating its active regions. This is a
scoped comparison, not a claim that existing low-rank methods cannot be
adapted.

## Algebraic boundary-set tail

The active-stratum argument uses a quantitative source rather than generic
measure-zero reasoning. Basu and Lerario's Theorem 1.1 states that if a real
algebraic set `Z` in `R^q`, defined by polynomials of degree at most `D`, has
dimension at most `m`, then for a uniform point in any radius-`S` Euclidean
ball,

```text
Pr{dist(x,Z) <= eps}
 <= 4 (4 q D eps/S)^(q-m)
       (1+(4D+1)eps/S)^m.
```

There is no smoothness or coefficient-height assumption, and no dependence
on the number of defining polynomials. For a nonzero polynomial hypersurface
take `m=q-1`; enclosing a cube of radius `R` in a radius-`sqrt(q)R` ball and
using `eps<=R` yields the safe bound

```text
vol(N_eps(Z) intersect [-R,R]^q)/(2R)^q
 <= 16 q^(q+1) D (4D+2)^(q-1) eps/R.
```

This is a direct specialization of an established tube theorem. The
candidate's use is the application-specific step: three-block elimination
puts all residual-face gradient transition values in a bounded-degree
algebraic hypersurface, then exact equal-volume grid-cell jitter transfers
the tube bound to its finite core-noise law. The algorithm does not compute
that hypersurface. Its coefficient height can be large; the tube estimate
does not depend on it.

The primary text inspected was the author-posted arXiv version of Basu and
Lerario, [*Hausdorff Approximations and Volume of Tubes of Singular
Algebraic Sets*](https://arxiv.org/pdf/2104.05053), Theorem 1.1 (PDF p.1)
and Theorem 3.2 (PDF p.9). It covers singular real algebraic sets, arbitrary
ambient balls, and all `eps>0` in the first displayed bound; the separate
sharper inequality has a small-`eps` condition. The 2023 journal version is
DOI [10.1007/s00208-022-02458-w](https://doi.org/10.1007/s00208-022-02458-w);
the journal landing page was not used as a substitute for the read primary
text.

## Assessment

The literature already supplies the individual mechanisms: strong-convex
parametric recourse and envelope differentiation, generic growth under
objective tilts, active-manifold stability under stronger regularity,
low-rank convexification and spatial approximation, and quantitative tube
bounds for singular algebraic sets. The candidate's possible contribution
is their specific combination for polynomial boxes: perturb only a
prescribed core, retain its original `L/sigma` in the expected search factor,
control residual active-face changes without strict complementarity, leave
weak residual bounds free, and certify exact implicit optimization on every
draw with a same-draw fallback.

This audit found no checked source stating that combination. That is a
bounded comparison, not evidence of novelty by absence. In particular, the
result assumes a supplied and verifiable uniform residual strong-convexity
certificate; it is not a solver that discovers the core or the certificate.

The sensitivity, genericity, parametric-QP, and low-rank-QP comparisons are
read in the local literature packages cited above. Basu–Lerario's arXiv
primary PDF has been read directly and its package promotion is queued with
the sole literature ingester. No KB or index files were changed for this
audit.
