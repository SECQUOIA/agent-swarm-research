# Exact rational QP output from a core and value Cauchy oracle

Date: 2026-10-02. Status: the product-box and coupled-polytope corollaries
passed a
[fresh independent actual-file review](../reviews/qp-core-cauchy-reconstruction-review.md),
including the general height and reconstruction argument. The Cauchy
oracle premises are separately reviewed. The coupled application has an
additional fresh interface and arithmetic check in that review's addendum.
No publication-priority claim is made.

## 1. A reviewed box-QP consequence

Let `x=(v,z) in [0,1]^k x [0,1]^m` and

```
q_gamma(x)=1/2 x'Ax+c'x+c_0+gamma'v,                    (1)
```

with rational symmetric `A`, rational base coefficients, and positive
semidefinite residual block `A_zz`.
Supply `L>=max(0,max_i A_vi,vi)` and rational `sigma>0`. Perturb only
the specified original core coordinates by the one finite rational law
of the reviewed [core Cauchy theorem](core-only-noise-core-oracle.md).
The law has polynomially many sampling bits and is fixed independently
of all accuracy queries.

**Corollary.** Every draw has an exact rational global optimizer and
value computable with expected bit work

```
f(k) (1+L/sigma)^k poly(I),                             (2)
```

where `I` is the base rational encoding length and the polynomial
exponent does not depend on `k,m`. The output has polynomial bit length
on every draw. For `k<=2`, the sharper inherited bound is
`(1+L/sigma) poly(I)`.

There is no residual strong-convexity, unique-optimizer, or supplied
growth assumption. The residual Hessian may be singular and core/residual
cross terms are arbitrary. One exact convex QP solve after core
reconstruction finishes the algorithm. When `k=0`, this is simply exact
convex QP. The ordinary finite-law oracle and its exceptional fallback
always use the same sampled objective.

Sections 2--4 give a polytope height lemma and an abstract reconstruction
step. Section 5 applies the separately reviewed coupled-polytope oracle.
Neither application asserts that such an oracle follows from fiber
convexity alone on an arbitrary coupled feasible domain.

## 2. Polynomial height of a lexicographic QP optimizer

Let `P={x:Ex<=d}` be a nonempty bounded rational polytope in `R^n`,
`n>=1`, and let

```
q(x)=1/2 x'Ax+c'x+c_0                                  (3)
```

have rational symmetric data. The full lexicographic ordering can put
any chosen core coordinates first. Denote the resulting lexicographically
first global optimizer by `x*`. Compactness ensures it exists.

Let `F` be the minimal face containing `x*`. Choose independent active
rows `R` whose equality system `Rx=d_R` defines its affine hull. Let
the columns of a rational matrix `N` span `ker R`. Since `x*` is in
the relative interior of this face, both signs of every small tangent
displacement are feasible. Therefore

```
N'(Ax*+c)=0,   N'AN>=0.                                (4)
```

Consider the rational stationary-face polytope

```
S=P intersect {Rx=d_R, N'(Ax+c)=0}.                    (5)
```

It contains `x*`. If `x,y in S` and `w=x-y`, then `w in ker R`.
Stationarity at both points implies
`w'(Ay+c)=0` and `w'Aw=0`. The exact quadratic difference formula
gives `q(x)=q(y)`. Thus every point of `S` has value `q(x*)`, so
every one is globally optimal. This constancy argument needs no inverse
of `N'AN`; indeed it does not need its positive semidefiniteness.

The point `x*` is the lexicographic minimum of `S` and hence a vertex
of this polytope. To see the latter statement, a nontrivial segment
through `x*` in `S` has one endpoint lexicographically smaller, using
the first coordinate at which its endpoints differ. That contradicts
the selection rule. This handles singular optimal faces without assuming
an isolated optimum or introducing the unknown optimal value as a
coefficient of a linear constraint.

Here is an effective denominator bound uniform over all faces. Choose
an even positive integer `D` that clears every data denominator and
makes `DA` entrywise even; twice the product of all denominators suffices.
Choose an integer `C>=1` bounding the absolute entries of

```
DA, Dc, Dc_0, DE, Dd.
```

Define

```
C_1 = n n! C^(n+1),
U   = n! C_1^n,
Q   = D U^2.                                            (6)
```

An integer nullspace basis for any independent active-row matrix can
be constructed using minors. If its rank is `r`, fix a nonsingular
`r`-column submatrix, set each free coordinate in turn to its determinant,
and determine the pivot coordinates by its adjugate. Every basis entry
has magnitude at most `r! C^r<=n! C^n`. Rank zero gives the identity
basis; rank `n` gives no tangent equations.

Consequently the scaled stationary equations in (5) have integer
coefficients and right-hand sides bounded by `C_1`. The original face
and polytope constraints satisfy this bound too. A vertex is specified
by `n` independent active equations. Cramer's rule therefore represents
all its coordinates with one nonzero integer denominator `Delta`, with

```
|Delta|<=U,   |coordinate numerators|<=U.               (7)
```

Substituting these coordinates into (3) gives an objective denominator
dividing `D Delta^2`, because `DA/2`, `Dc` and `Dc_0` are integral.
Thus the reduced denominator of every coordinate of `x*`, and of
`q(x*)`, is at most `Q`. Numerators also have polynomial bit length,
by (7) and the quadratic evaluation. The bound applies simultaneously
to every possible active face; the algorithm does not find or enumerate
those faces to use it.

The binary lengths of `D,C,U,Q` are polynomial in the full rational
input length. In particular, additional rational noise bits are counted.
The lemma is about a selected rational optimizer: other points of a
flat optimal set can have irrational coordinates.

## 3. One polynomial precision reconstructs exact core and value

Suppose an already established same-law Cauchy oracle returns a feasible
rational point `(v_t,z_t)`, a value interval `[ell_t,U_t]`, and the
guarantees

```
ell_t<=q*<=U_t,  U_t-ell_t<=2^(-t),
||v_t-v*||_2<=2^(-t),                                  (8)
```

where `v*` is the core of the full lexicographic optimizer used above.
Choose an integer `t` with

```
2^(-t)<=1/(8Q^2).                                      (9)
```

Each interval `[v_t,i-2^(-t),v_t,i+2^(-t)]` contains its exact
rational core coordinate and has width at most `1/(4Q^2)`. The value
interval is narrower still. Distinct reduced rationals with positive
denominators at most `Q` differ by at least `1/Q^2`. Hence each interval
contains exactly one rational of that denominator class.

Recover those rationals in polynomial bit time using continued fractions
or Euclidean interval reconstruction, as in the reviewed
[rational reconstruction lemma](../geometric-dp/exact-box-qp.md).
For example, enumerate convergents of the rational interval midpoint
with denominator at most `Q`, retaining the unique one in the interval.
The true rational is within `1/(8Q^2)` of that midpoint, so the standard
continued-fraction criterion guarantees its presence. Signed values,
zero, and exact rational midpoints cause no difficulty.

The noise law is chosen first. For its common endpoint-inclusive grid,

```
gamma_i = sigma (2j_i-(M-1))/(M-1),
```

one may then choose `D` uniformly over every draw: take twice a product
of base denominators, the denominator of `sigma`, and `M-1`.
Choose `C` using the base coefficients and `|gamma_i|<=sigma`.
These choices clear and bound every sampled coefficient. Thus (6)--(9)
give one fixed reconstruction precision for all atoms, with

```
t=poly(I+log M)=poly(I).                               (10)
```

There is no requirement to increase `M` after choosing `t`. The oracle
already supports all accuracies for that law, so there is no sampling
precision loop or adaptive-query expectation issue.

Use the established rational-QP face-enumeration fallback inside this
Cauchy evaluator, rather than return expanded generic algebraic records.
It can preserve the full lexicographic selector: on the minimal face of
that selected point, a nonzero tangent null direction would allow both
small signs at the same value, one lexicographically smaller. Thus its
tangent Hessian is positive definite, with a zero-dimensional face
allowed. Enumerating independent active-row sets, solving nonsingular
stationary KKT systems, discarding infeasible candidates, and selecting
least value then least lexicographic point consequently includes and
selects exactly `x*`. This is the
rational face fallback already used by the aligned-QP theorem, with its
selection rule specified. It has a base-only exponential number of
polynomial-bit rational solves and returns a polynomial-size rational
answer. Include that whole cost in the preselected fallback budget.

On that branch the final exact answer is already available. On an
ordinary branch the query depth in (10) is polynomial, so its rational
primal and interval outputs have polynomial bit length, and rational
reconstruction has ordinary polynomial cost. The corollary never applies
a nonlinear-time postprocessor to an exponentially large algebraic proof
record while charging only its expected length.

## 4. Exact convex completion and complexity

After reconstructing `v*`, the fiber

```
P_v*={z:(v*,z) in P}
```

is a nonempty rational polytope. If the original quadratic is convex
on this fiber, solve that convex QP exactly in polynomial bit work.
If necessary, first reduce to the rational affine hull of the fiber;
for a quadratic, convexity there means a positive semidefinite restricted
Hessian. This includes lower-dimensional and singleton fibers. No
residual optimizer is reconstructed from an approximate residual point.

The resulting rational feasible pair is globally optimal because `v*`
is an exact globally optimal core. Its exact value equals the separately
reconstructed `q*`. Both input and output lengths of the completion are
polynomial. Any exact residual optimizer suffices; a full lexicographic
residual selection is unnecessary for the output claim.

For the box model in Section 1, fiber convexity follows from `A_zz>=0`
and the reviewed core/value oracle gives (8). Its one-query expected
bound with (10), followed by deterministic polynomial reconstruction
and convex completion, proves (2). Rare fallback draws are already
paid for by that oracle; every atom is still solved correctly.

## 5. Coupled-polytope corollary under the reviewed convexifier premise

Let `P` be a nonempty bounded rational polytope in `(v,z)`, with
`v in [0,1]^k` and a supplied rational bounding box for `z`. Suppose
the rational quadratic `q_0` has a supplied verified `alpha>=0` for which

```
q_0(v,z)+(alpha/2)||v||^2 is convex on P.                (11)
```

The [coupled value theorem](coupled-polytope-core-value-oracle.md) and
[selected-core extension](coupled-polytope-core-oracle.md) now have
separate completed actual-file reviews. With their one finite rational
law for independent core coefficients, the reconstruction above returns
an exact rational global optimizer and value on every draw, in expected
work

```
f(k)(1+alpha/sigma)^k poly(I).                          (12)
```

If necessary, normalize only the residual bounding intervals for the
core-oracle interface. This leaves the core noise and the convexifier
in (11) unchanged and preserves polynomial input length. Fixed residual
coordinates can be substituted. Lower-dimensional `P` and projected
core sets are allowed; projected-value continuity is not a premise.

Apply the general height lemma directly to this rational polytope and
instantiate the Cauchy evaluator with the rational QP fallback above.
The reviewed compact-domain projected-growth tail and actual retained
hull test give (8) for the fixed lexicographic core. Choose the common
denominator bound and polynomial precision after the law has been fixed,
exactly as in Section 3. On a fixed reconstructed core, the correction
in (11) is constant. Therefore the original quadratic is convex on
that fiber, and the exact convex completion in Section 4 applies.
This proves (12). If `alpha=0`, direct exact convex QP is already
deterministic polynomial work; no smoothing is needed for this case.

This application retains its supplied convexification parameter. It
does not replace it by the box model's possibly much smaller upper
coordinate curvature `L`. Fiber convexity alone is insufficient for
the coupled cell oracle.

## 6. Relation to the existing exact-QP theorem

The earlier [aligned-noise exact cell-closure theorem](smoothed-exact-cell-closure.md)
already proves expected exact rational optimization in every supplied
negative-space dimension on a bounded rational polytope. This note
does not claim that general all-dimensional exactness as new. Its main
difference is proof and oracle interface: polynomial rational height
and a core/value Cauchy name replace extraction and exact closure of
quadratic recourse regions.

For the particular supplied factor in that earlier proof, smooth
recourse uses a kernel condition. The box corollary here instead uses
the specified original core coordinates and the PSD residual block.
For example `q(v,z)=vz` has a zero residual Hessian and no finite
addition `alpha v^2/2` makes its full Hessian positive semidefinite.
It still fits the box interface (and is itself an easy endpoint case).
The example distinguishes the supplied-coordinate hypotheses, not the
overall class of QPs solvable by alternative aligned normalizations.

The coupled corollary supplies a different proof from the already
reviewed aligned-noise exact theorem, rather than a claim of the first
exact all-dimensional result on rational polytopes. Its numerical
curvature and any core normalization factors remain explicit.

## Verification status

The author read the actual core Cauchy theorem, generic lexicographic
fallback, earlier rational reconstruction lemma and aligned-QP theorem.
The fresh independent arithmetic review passed the singular-face
argument, exact denominator constants, uniform sampling precision,
signed reconstruction, rational fallback and convex completion. It
requested explicit rejection of infeasible KKT candidates; that step
is now stated before objective and lexicographic comparison. Scoped
local-link, whitespace and fence checks passed. No generic QP solver
implementation, new probability
experiment, index edit, project-wide check or CI inspection is claimed.
The final coupled application was added only after both its value and
selected-core premises passed actual-file review. Its short transfer
also passed a separate fresh arithmetic check, including preservation
of the convexification parameter and noise law under residual scaling.
