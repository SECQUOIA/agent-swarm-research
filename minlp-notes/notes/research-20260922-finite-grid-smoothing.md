# Finite-grid perturbations for exact quadratic-message algorithms

Date: 2026-09-22. Status: coordinator proof with
[fresh independent review](review-20260922-finite-grid-smoothing.md).
This develops the finite-bit question left open in the
[smoothed block-DP investigation](research-20260922-next-frontier.md).
The continuous-noise algorithm passed a separate mathematical review. The
finite-grid review found no substantive gap after explicitly identifying
identical polynomial formulas. Priority of either contribution remains
provisional; internal review is not journal peer review.

## Consequence

The real-noise proof bounds scalar message size by counting random level
crossings. A finite noise grid introduces atoms, so its density hypothesis
cannot simply be reused. For quadratic branches, however, each conditional
level function has only exponentially many monotone arcs. A grid with
exponentially many points, requiring only linearly many random bits per
coefficient, controls the additional contribution from these atoms.

The argument converts the existing expected arithmetic
algorithm into an expected polynomial bit algorithm for rational indicator
quadratic programs with fixed diagonal-dominance parameters and bounded
biconnected block size. It solves the perturbed instance exactly. It does
not assert an exact algorithm for the original unperturbed instance.

## Finite-grid envelope bound

Let `Z` be a nonempty subset of `{0,1}^m`, and let every `q_z` be a quadratic
polynomial that is `L`-Lipschitz on a compact interval `I` of positive length
`T`. Deterministic support-dependent intercepts are allowed. For `sigma>0`
and integer `N>=2`, let the coordinates of `xi` be independent and uniform
on the `N` points

```
-sigma + 2 sigma k/(N-1),    k=0,...,N-1.
```

Write `phi=1/(2 sigma)` and let `K(xi)` count the maximal positive-length
intervals on which the envelope

```
V_xi(t)=min_(z in Z) {q_z(t)+xi dot z}
```

has one quadratic formula. Identical polynomials are identified; an isolated
tie does not introduce a new formula. A polynomial appearing in two separated
intervals is counted twice. This count bounds the number of distinct full
quadratics that an exact message implementation needs to retain.

**Theorem.**

```
E K <= 1 + 2 m phi L T + 4 m 2^m/N.                 (1)
```

The term for `m=0` is interpreted as zero; a single branch needs one formula.

### 1. Interval probabilities after a small continuous perturbation

For every real interval `J`, grid spacing gives

```
Pr(xi_i in J) <= phi length(J) + 1/N.
```

Indeed the number of grid points in an interval of length `ell` is at most
`ell(N-1)/(2 sigma)+1`. Let `U_i` be independent uniforms on `[-1,1]`,
also independent of the grid variables, and set `eta_i=xi_i+delta U_i`.
For each fixed `delta>0`, these variables have continuous densities, and

```
Pr(eta_i in J) <= phi length(J) + 1/N.                 (2)
```

Condition on `U_i` and apply the original interval estimate to the translate
`J-delta U_i`, which has the same length. This sharper argument was supplied
in the independent review and rechecked by the coordinator. The bound is
uniform in the other coordinates and in `delta`.

### 2. Conditional level functions have few monotone arcs

Fix a coordinate `i` for which both support classes are nonempty and condition
on `eta_j`, `j!=i`. Define

```
h_i(t) = min_(z_i=0) [q_z(t)+sum_(j!=i) eta_j z_j]
       - min_(z_i=1) [q_z(t)+sum_(j!=i) eta_j z_j].
```

This function is `2L`-Lipschitz, hence has total variation at most `2LT`.
The two classes have at most `2^(m-1)` branches each. The lower envelope of
`r` full univariate quadratics has at most `2r-1` open pieces: a subsequence
`a,b,a,b` would force three distinct crossings of two quadratic polynomials.
Identical polynomials can be removed before counting.

The common refinement of the two envelopes therefore has fewer than
`2^(m+1)` pieces. On each, `h_i` is quadratic. Splitting at a stationary
point gives at most

```
J_m=2^(m+2)
```

monotone arcs. This intentionally loose bound includes all endpoint cases.
Constant arcs can be omitted when counting level hits for the continuous
variable `eta_i`: their levels, together with all arc endpoint levels, have
conditional probability zero. On every remaining open arc, a given level
is hit at most once.

At any global minimizing-support tie, some coordinate differs between two
minimizers. Their two coordinate-class minima coincide, so `eta_i=h_i(t)`
for that coordinate. Conversely, equality of these class minima gives a
global tie because the two classes partition `Z`.

By summing (2) over the images of the monotone arcs, their image lengths
adding to the total variation, the conditional expected number of level
hits for coordinate `i` is at most

```
2 phi L T + J_m/N.
```

Summing over coordinates bounds all global tie points. Thus the continuous
jittered envelope has expected interval count at most

```
1 + 2 m phi L T + m J_m/N.                           (3)
```

This is not an application of a bounded-density theorem with a fictitious
grid density. It uses the explicit interval-mass estimate and the finite
number of monotone arcs.

### 3. Removing the continuous jitter

For a fixed grid outcome, the unjittered envelope has finitely many distinct
polynomial formulas and finitely many interval pieces. Pick one interior
point from each piece, avoiding equality with every nonidentical polynomial.
At these finitely many points, the winning polynomial has a positive gap
from all other polynomial classes. A class may contain multiple support
labels with identical polynomials; this is why formulas, rather than unique
support labels, are counted in `K`.

For all sufficiently small `delta`, every jittered winner at a selected
point belongs to its original polynomial class. Consecutive selected points
belong to different classes, so they require at least as many interval
pieces in the jittered envelope. For a sequence `delta downarrow 0`,

```
K(xi) <= liminf K(xi+delta U).
```

At each fixed positive `delta`, persistent ties have probability zero. Using
a countable sequence of jitter sizes permits taking this property
simultaneously. Fatou's lemma and (3) now give (1).

## Applying the bound to the block algorithm

Use the notation of the reviewed algorithm. Let the objective be

```
x^T Q x+c^T x+sum_i (lambda_i+xi_i) z_i,
x_i(1-z_i)=0,    z_i in {0,1}.
```

Assume rational data and rational bounds

```
0<d<=Q_ii<=D,
sum_(j!=i)|Q_ij|<=rho Q_ii,    0<=rho<1,
|c_i|<=C,    C>0,
```

and every biconnected block has at most `b` vertices. Set

```
M=C/[2d(1-rho)],    I=[-M,M],    T=2M.
```

The coordinate maximum principle puts every conditional fixed-support
minimizer in this interval when its boundary value belongs to it. Subtract
the boundary's common quadratic, linear, and indicator terms. The remaining
support quadratics have derivative bounded by `L=2 rho D M`. None of these
claims depends on the penalty noise being continuous.

Take `N` to be a power of two with `N>=4n 2^n`, where `n` is the whole
problem's number of indicators. Every message has at most `m<=n` internal
indicators. Equation (1) then gives

```
E K <= 2+8n phi rho D M^2.
```

At each block, different child lists depend on disjoint noise coordinates.
Their lengths remain independent under grid noise. Retain one representative
support for each interval-winning polynomial and identify duplicate formulas.
The candidate count is the product of the child list lengths plus their
inactive alternatives, exactly as in the continuous algorithm. Consequently
the same proof gives the expected operation bound

```
O_b(n^2 (3+8n phi rho D M^2)^(b-1)).                 (4)
```

No support that wins only through a duplicate polynomial must be separately
retained. At a zero-state alternative, any retained representative attaining
the value gives a feasible reconstruction. Future costs depend on that
subtree only through the scalar boundary and its value.

## Why the arithmetic can have polynomial bit cost

Let `B` bound the bit lengths of the original rational input and of `sigma`.
Generating each grid variable uses exactly `log2 N=O(n+log n)` random bits.
Its rational value has polynomial bit length. The perturbed coefficients
therefore also have polynomial bit length.

Every retained quadratic is the exact conditional value of a fixed support
of the original problem. Its coefficients are Schur-complement expressions
from a principal matrix, its linear terms, and the sum of support penalties.
Determinant bounds and Cramer's rule give polynomial bit lengths in
`n,B,log N` for these rational coefficients. Reduced rational arithmetic
prevents an implementation from artificially retaining unreduced large
fractions. The same bound applies to partial combinations at a vertex,
because they too are fixed-support conditional values.

Envelope breakpoints are real roots of differences of two such quadratics.
They have algebraic degree at most two and polynomial coefficient bit lengths.
Exact comparison, sorting, interval restriction, and sign testing for these
numbers can be implemented in polynomial bit time. The block elimination
has bounded dimension, and each of its exact arithmetic operations acts on
polynomial-length rationals. Minimization and backtracking return the
optimal support and its rational continuous minimizer.

Thus (4) is multiplied only by a
polynomial bit-operation factor. With fixed `b,d,D,C,rho` and polynomially
bounded `1/sigma`, the expected total bit complexity is polynomial in the
input length. The statement is not polynomial in the logarithms of all
conditioning and smoothing parameters; fixing or explicitly bounding those
parameters matters.

## A certified additive approximation for the original problem

Let `v_xi` be the exact perturbed optimum and `(x_hat,z_hat)` its returned
optimizer. The original objective value `U` and a valid original lower bound
`L_original` are

```
U=v_xi-xi dot z_hat,
L_original=v_xi-sum_i max(xi_i,0).
```

For every feasible `(x,z)`, its original cost is its perturbed cost minus
`xi dot z`, so it is at least `L_original`. Consequently

```
0 <= U-f_original^* <= U-L_original
   = sum_(z_hat_i=0) max(xi_i,0)
     +sum_(z_hat_i=1) max(-xi_i,0)
   <= sum_i |xi_i| <= n sigma.
```

For any rational tolerance `epsilon>0`, choose `sigma=epsilon/n`. The
finite-grid algorithm then returns a feasible point and a rigorous
`epsilon`-wide objective interval for the original unperturbed problem.
The guarantee holds for every grid outcome; only its running time is
averaged. Under fixed structural and diagonal-dominance bounds, its expected
bit runtime is polynomial in input length and `1/epsilon`. This is an
additive approximation scheme, not a relative-error claim. The elementary
objective-perturbation inequality is classical; the algorithm makes it
applicable here without an assumed support margin.

## Verification, attribution, and unresolved issues

The full-quadratic envelope bound, isolation and level-counting techniques,
and exact algebraic-number operations are established ingredients. The
candidate contribution is their combination with the indicator block
algorithm and an explicit finite grid that preserves its expected bound.
The [primary-source audit](review-20260922-smoothed-dp-priority.md) for the
continuous algorithm is complete and records important antecedents.
The equivalence of pseudopolynomial binary optimization and smoothed
complexity must be compared in its strongest expected-time versions, not
only the original weak-moment formulation.

A fresh reviewer checked the entire grid argument, especially the lower
semicontinuity of formula count under jitter, plateau levels, the monotone-arc
bound, and bit complexity. The review reports 52,266 exact grid-interval
checks and 5,150 atomic-budget checks. No finite experiment could prove
these probabilistic or asymptotic statements. The separate exact block-DP
checker tests the deterministic algorithm, not the noise
distribution theorem. No project-wide verification or CI inspection was run.
