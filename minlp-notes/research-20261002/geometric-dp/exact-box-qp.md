# Exact rational mixed-integer box quadratic optimization under bounded conditioning

Date: 2026-10-02. Status: complete corollary, supported by a
[fresh mathematical review](../reviews/exact-box-qp-adversary.md) and targeted
exact-arithmetic checks; literature comparison continues. This combines the
[geometric-grid theorem](theorem.md) and its
[rational-arithmetic bound](extensions.md) with elementary rational-height
and reconstruction arguments. No novelty claim is made for those standard
arithmetic arguments, or for the combined result before literature review.

A rational mixed-integer box quadratic program with a supplied fixed-width tree
decomposition and a polynomially bounded upper-curvature/growth ratio has
an exact polynomial-time algorithm in the Turing model. The growth
constant need not be supplied. More generally, the algorithm terminates
on every rational mixed-integer box quadratic program with a unique global optimizer;
the conditioning restriction gives the polynomial-time guarantee. The
output includes the exact rational optimizer and optimum value, with a
certificate whose validity does not require trusting the growth assumption.

Both continuous intervals and integer intervals are allowed, including
purely continuous and purely integer special cases. Exactness follows from
the bounded denominators of quadratic-program optima, not from a positive
gap between the objective values of arbitrary feasible points. Such a gap
does not exist when the objective varies continuously on a feasible slice.

## 1. Input and statement

Let

```
F(x) = x^T Q x + d^T x + e,
X = product_i X_i,
X_i = [a_i,b_i] or [a_i,b_i] intersect Z,
```

where `Q` is symmetric and all data are rational. Round integer interval
endpoints inward and reject any empty domain. The resulting mixed box is
nonempty and bounded, with integer endpoints on integer coordinates.
Fixed coordinates can be eliminated and reinserted; a singleton domain
is immediate. Below there are `n>=1` nonfixed coordinates and
`s=max_i(b_i-a_i)>0`.

A tree decomposition of the supplied quadratic factorization is part of
the input, with `N` bags of size at most `p=w+1`. Let `I` denote the total
binary encoding length, including the decomposition and factor data.
Rewriting monomial coefficients as a symmetric quadratic matrix only
introduces factors of two and preserves the interaction graph.

Assume that for some unknown `g>0` and unique optimizer `x*`,

```
F(x)-F(x*) >= g ||x-x*||_2^2       for every x in X.          (1)
```

This growth condition is on the actual mixed domain. Strong convexity of
the continuous extension does not control the gap between nearly tied
integer assignments and does not by itself give a useful mixed-domain
growth constant.

The coordinate upper curvature is known directly from the input:

```
L0 = max_i 2 Q_ii.
```

If `L0<=0`, the continuous extension is concave in each coordinate
separately. A minimum is attained at a box vertex: replacing one coordinate
by a minimizing endpoint never increases the objective, and integer
endpoints are feasible. Exact finite-state DP with two endpoint values per
coordinate solves the problem in polynomial bit time
at fixed width, without (1). Hence consider `L=L0>0`, and put
`kappa=max(1,L/g)`.

**Theorem.** There is an exact algorithm whose bit complexity is polynomial
in `I` and `kappa` for every fixed `p`. It does not require `g` or a bound
on `kappa` as input. In particular, the promised class with fixed width
and `kappa` polynomially bounded in `I` is solvable in polynomial time.
The algorithm uses rational arithmetic, finite-state DP, and rational
reconstruction; no real-valued comparison or nonlinear optimization oracle
is required.

The constants and polynomial degree may depend on `p`. This is not a
uniform polynomial-time result over arbitrarily bad conditioning, or a
fixed-parameter tractability claim in width alone. All calculations below
use the original coordinates, so rescaling the box does not silently
change the curvature/growth ratio.

**Qualitative growth lemma.** A quadratic on a compact mixed box with a
unique global optimizer has a positive global growth constant as in (1).

*Proof.* Suppose otherwise. There are `x_j!=x*` for which
`r_j=(F(x_j)-F(x*))/||x_j-x*||^2` tends to zero. Boundedness makes the
numerators tend to zero, and compactness and uniqueness imply `x_j->x*`.
Every integer coordinate of `x_j` therefore equals its value in `x*`
for all sufficiently large `j`. Discard the preceding finite prefix.
If every coordinate is integer, this already contradicts `x_j!=x*`.
Put `t_j=||x_j-x*||` and, after taking a subsequence,
`u_j=(x_j-x*)/t_j -> u`, with `||u||=1`. Write
`ell=grad F(x*)`. These directions have zero integer components.
First-order optimality within that fixed integer slice gives
`ell dot u_j>=0`. It is not asserted for arbitrary chords that change
integer assignments. The exact quadratic expansion is

```
r_j = (ell dot u_j)/t_j + u_j^T Q u_j.
```

Since the quadratic term is bounded, `ell dot u_j->0`, so
`ell dot u=0`; nonnegativity of the first term also gives
`u^T Q u<=0`. The limiting direction has zero integer components and
belongs to the closed continuous-box tangent cone: its continuous
components point inward at active bounds. Consequently
`x*+tau u` is feasible for every sufficiently small positive `tau`.
Optimality on that ray gives `u^T Q u>=0`. Equality follows, and the
exact quadratic expansion makes the whole short ray optimal, contradicting
uniqueness. QED.

Thus the existence of some `g>0` is automatic here. This qualitative fact
does not provide a useful numerical lower bound on `g`; that constant may
still be exponentially small relative to the input length.

## 2. A computable height bound

Polynomial-size rational certificates for quadratic programming are
classical; see Vavasis, [*Quadratic programming is in NP*](https://doi.org/10.1016/0020-0190(90)90100-C),
and the rational-QP discussion in Del Pia, Dey, and Molinaro,
[*Mixed-integer quadratic programming is in NP*](https://arxiv.org/abs/1407.4798).
The explicit denominator bound needed here is proved directly below.

Let `D` be a common positive denominator of every entry of `Q,d,e` and
all box endpoints, including fixed-coordinate values removed during
preprocessing. Taking their least common multiple suffices. Write

```
F(x) = (x^T H x + h^T x + k)/D,
```

where `H=DQ`, `h=Dd`, and `k=De` are integral and `H` is symmetric.
Each endpoint also has the form `integer/D`. If starting directly from
monomial coefficients, first account for the factor of two in off-diagonal
matrix entries when choosing `D`.

Define the positive integers

```
C = max(1, max_(i,j) |H_ij|),
Delta = (2 n C)^n,
R = D Delta,
V = D R^2.                                                (2)
```

Their binary lengths are polynomial in `I`; in particular they are
`O(n(I+log n))`. Their numerical values may be exponentially large.
They are denominator bounds, not quantities to enumerate.

**Lemma 1.** Every rational mixed-integer box quadratic program has a global optimizer
all of whose coordinates share a denominator at most `R`. Its optimum
value has reduced denominator at most `V`. Every isolated global optimizer
satisfies the coordinate bound. In particular, this holds for the unique
optimizer, or for every optimizer when the optimal set is finite.

*Proof.* Compactness supplies a global optimizer. Fix its integer
assignment, and among global optimizers in that slice choose one whose
smallest containing continuous-box face has minimum dimension. Let `S`
be its free continuous coordinates, strictly between their bounds, and
let `A` contain every integer coordinate and the active continuous
coordinates. Write `x_A=t_A/D`, where `t_A` is integral. In particular,
an integer coordinate `z_i` contributes `t_i=D z_i`.

The continuous free first-order equations hold, and the free Hessian `2H_SS/D` is
positive semidefinite. If it were singular, a nonzero null direction
supported on `S` would have zero linear and quadratic objective change.
The objective would remain constant along that line. Moving until a free
coordinate first reaches a box bound would give a global optimizer on a
strictly smaller face, a contradiction. Thus `2H_SS` is positive definite
and invertible. When `S` is empty, set its determinant to one.

The free equations are

```
(2H_SS)(D x_S) = -D h_S - 2H_SA t_A.                       (3)
```

The right side is integral. Cramer's rule shows that every coordinate
has a denominator dividing the common integer

```
q = D det(2H_SS).
```

For `m=|S|`, the determinant expansion gives

```
1 <= det(2H_SS) <= m! (2C)^m <= (2nC)^n = Delta.
```

Thus `q<=R`. Substituting a vector with common denominator `q` into
the integer-coefficient representation of `F` shows that the reduced
denominator of its objective divides `D q^2`, and is therefore at most
`V`. This objective equals the global optimum.

For any isolated global optimizer, its own free continuous Hessian is
positive definite: a singular direction would give a nontrivial short
segment of optimizers in its fixed integer slice, contradicting isolation.
The same Cramer calculation therefore applies directly to that point.
QED.

Fixing the integer assignment in this proof is an existence argument,
not an enumeration step. Its encoded coordinates have bit length bounded
by the input's integer endpoints. Neither the determinant bound nor the
algorithm incurs the product of the integer-domain cardinalities.

Under (1), an alternative direct argument gives
`2Q_SS >= 2g I` at the unique optimizer: perturb in any free continuous direction
and use the exact quadratic expansion. The minimum-face argument is
stronger for certification because its value-denominator conclusion
needs neither uniqueness nor a growth hypothesis.

The input's box bounds also bound coordinate numerators. Substituting
those bounds into the quadratic gives a polynomial-bit magnitude bound
for the optimum value. Thus the result concerns polynomial binary output
length as well as denominators.

## 3. Turning a narrow interval into an exact value

Distinct reduced rationals with positive denominators at most `K` differ
by at least `1/K^2`. Consequently a valid interval

```
LB <= f* <= UB,          UB-LB <= 1/(4V^2)                  (4)
```

contains exactly one rational with reduced denominator at most `V`.
Lemma 1 proves that this rational is `f*`.

This is algorithmic in polynomial bit time. Use ordinary continued-fraction
or Euclidean rational-interval reconstruction. For example, at the midpoint
`m=(LB+UB)/2` the desired rational lies within `1/(8V^2)`. The standard
continued-fraction approximation criterion puts any such rational among
the convergents of `m`; enumerate those with denominator at most `V`
and retain the unique one in the interval. Negative optimum values cause
no change when signed rational arithmetic is used.

Coordinate reconstruction works similarly. Set

```
rho = 1/(4R^2).
```

Each interval `[y_i-rho,y_i+rho]` has length `1/(2R^2)` and therefore
contains at most one rational of denominator at most `R`. If
`||y-x*||_2<rho`, it contains exactly `x_i*`. The same polynomial-time
reconstruction applies to each coordinate.

A coordinate candidate obtained before the point is sufficiently accurate
need not be optimal. Accept a reconstructed vector only after checking
every box bound, all prescribed integrality conditions, and the exact
equality `F(candidate)=f*`. A vector of
separately reconstructed coordinates need not itself have a common
denominator at most `R`; the equality check is performed with its actual
rational coordinates, without assuming an objective denominator bound for
that arbitrary candidate.

## 4. An exact algorithm without the growth constant

Compute `D,R,V,L` from the rational input, handle `L<=0` as above, and
choose any rational feasible initial center, such as the lower endpoint
vector. For `m=0,1,2,...`, set

```
theta_m = 2^(-m-1),
eps_m = min(1/(4V^2), L theta_m^2/(16R^4)),
J_m = max(0, ceil((1/2) log2(7 L n s^2/(8 eps_m)))).        (5)
```

The integer stage bound can be found by rational comparisons with powers
of two; evaluating a transcendental logarithm is unnecessary.

For this trial, start from the fixed initial center and run stages
`0,...,J_m` of the exact rational geometric-grid algorithm. If a stage
produces `F(y)-LB<=eps_m`, do the following:

1. Reconstruct the unique denominator-`V` rational `v` in `[LB,F(y)]`.
2. Reconstruct a denominator-`R` rational in each
   `[y_i-rho,y_i+rho]`, if one exists.
3. Return the vector and `v` if all coordinate reconstructions exist,
   the vector satisfies all interval and integrality requirements, and
   its exact objective equals `v`.

If reconstruction or verification fails, abandon this trial and continue
to the next `m`. If no stage attains its gap target, continue after stage
`J_m`. Every accepted answer is exactly globally optimal: the lower
bound is valid for every trial parameter, Lemma 1 identifies `v=f*`, and
the final feasible point has that objective. This validity argument does
not use (1) or a guessed growth constant.

**Lemma 2.** Under (1), the first trial satisfying
`theta_m^2<=g/(8L)` succeeds.

*Proof.* The geometric-grid theorem gives a gap at most `eps_m` by stage
`J_m`. At any stage meeting that target, (1) and (5) imply

```
||y-x*||_2^2 <= eps_m/g
            <= L theta_m^2/(16gR^4)
            <= 1/(128R^4)
             < rho^2.
```

All coordinate intervals therefore contain their true optimizer
coordinates. Equation (4) identifies the optimum value, so every final
check passes. QED.

If a rational valid `g` is known, one may instead make a single sufficiently
accurate call, with target at most
`min(1/(4V^2),g/(32R^4))`, and choose an admissible mesh parameter. The
unknown-constant schedule removes that input requirement.

## 5. Bit complexity and the exact certificate

Let `m*` be the first admissible trial. As in the main theorem,

```
theta_(m*)^-1 = O(sqrt(kappa)),
m* = O(1+log kappa).
```

The denominator bounds have polynomial bit length, and the rational
curvature, side lengths, and coefficients have polynomial bit length.
It follows from (5) that

```
J_(m*) = poly(I) + O(log kappa).
```

The rational-polynomial bit theorem applies with degree two. It includes
factor evaluation, grid-coordinate denominators, DP messages, comparisons,
and backtracking. At fixed `p` its bound is polynomial in `I` and
`kappa` here. The targets `eps_m` decrease and the stage bounds increase
with `m`. Earlier trials are dominated by the successful trial's common
bit-length bound and a geometric sum of their `theta_m^-p` table-work
factors. Rational reconstruction, exact feasibility, and objective
evaluation have polynomial bit cost as well. This proves the theorem.

The returned exact certificate can consist of the final rational grids
and DP lower-bound evidence, a feasible exact optimizer, and the rational
interval satisfying (4). A checker verifies the DP lower bound using
the explicitly known diagonal curvature bound, computes the candidate
objective, and checks bounded-denominator isolation using (2). No growth
constant is needed to validate the certificate. The height argument is
uniform over rational mixed-integer box quadratics and is part of the certificate
theorem, not an unverified numerical assertion.

More explicitly, the checker verifies that the exact candidate objective
belongs to the displayed interval and has reduced denominator at most
`V`; the interval contains at most one such rational. For `L0<=0`, use
the separate endpoint-DP certificate and the known coordinatewise
concavity. That branch needs neither a positive-curvature correction nor
a narrow isolating interval.

This does not say that every nearby feasible objective value is rational
with denominator at most `V`. Only an optimal value has that guaranteed
bound. Nor does approximate arithmetic alone yield an exact answer: the
final reconstruction and rational equality checks are essential.

The [finite-optimum companion](exact-nonunique-box-qp.md) removes uniqueness
by combining the same height and reconstruction arguments with the
coordinate-anchor discovery algorithm. Its complexity also depends on
the number of distinct optimal coordinate values.

## 6. Scope and significance

The corollary removes the arbitrary-real oracle qualification for a natural
mixed-integer class and obtains an exact optimizer, rather than merely an
epsilon solution. It allows nonconvex quadratic objectives and interaction
graphs with cycles. It does not require the whole Hessian to be positive
semidefinite, only the global growth promise for the stated complexity.
The positive-definite free-continuous-face Hessian used in the height proof is a
necessary local property of the selected optimizer, not an additional
input promise.

For example, on `[0,1]^3`, write `u=x-1/3` and `v=y-2/5`, and set

```
F(x,y,z) = u^2+v^2+uv/3 + z-z^2/2 + z(u+v)/4.
```

Its interaction graph is a triangle and its Hessian is indefinite because
the `zz` entry is negative. Nevertheless, `z-z^2/2>=z^2/2` and elementary
cross-term bounds give

```
F(x,y,z) >= (17/24)(u^2+v^2) + z^2/4.
```

Indeed, the difference is
`(u+v)^2/6+(u+z)^2/8+(v+z)^2/8+z(1-z)`, which is nonnegative on the box.

Thus its unique optimizer is `(1/3,2/5,0)`, with `g=1/4`, `L=2`, and
`kappa<=8`. This is an illustrative class member, not evidence of practical
superiority or a difficult benchmark.

The same example remains valid if `z` is restricted to `{0,1}`. More
generally, the proof handles long integer intervals through the same
compressed grids as the main theorem. The existing pure-integer exact
stopping theorem has a more direct stopping rule; the new corollary also
recovers continuous optimizer coordinates exactly.

The global conditioning restriction remains essential to the complexity
claim. Even rational instances of short encoding length can have an
exponentially small global growth constant because of near-tied distant
solutions or nearly tied integer assignments. This result does not make all bounded-width box QPs easy or
contradict unrestricted hardness results. Establishing the precise prior-art
position of this conditioned class is separate work.

The rational-height lemma, continued-fraction reconstruction, and the
principle of recovering an exact rational answer from a sufficiently
accurate approximation are classical. The contribution asserted here is
only the corollary obtained when those facts are combined with the proposed
conditioned sparse global algorithm. Its novelty depends on the status of
that underlying algorithm and on the literature comparison.

## 7. Verification record

The height calculation and reconstruction thresholds were independently
derived by a second agent. The [fresh full review](../reviews/exact-box-qp-adversary.md)
found no substantive mathematical gap, confirmed the qualitative growth
lemma, and then separately rechecked the mixed-integer extension. Its inline
exact-rational checks covered 11,376 signed continued-fraction reconstructions,
a rational active-bound normalization example, and the stopping thresholds.

The targeted integration command actually run was

```
python3 research-20261002/geometric-dp/checks/exact_box_qp_checks.py > research-20261002/geometric-dp/checks/exact-box-qp-results.json
```

The [script](checks/exact_box_qp_checks.py) and [results](checks/exact-box-qp-results.json)
record 199 rational QP cases, including 30 with integer coordinates;
144 small integer slices, 5,931 continuous faces, and 2,228 height checks;
199 optimal-value and 505 coordinate reconstructions. All assertions passed.
The suite includes singular and nonunique slices, an integrality rejection
for a fractional point with the exact optimal value, the triangle's exact
growth identity, and an analytic optimum on an integer interval containing
`2*10^80+8` values, none of which were enumerated for that case.

These finite checks support the height and reconstruction arguments; they
do not implement or benchmark the full exact geometric-DP algorithm.
No project-wide checks or CI inspection were used.
