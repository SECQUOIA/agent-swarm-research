# Effective point approximation for globally convex polynomials

Date: 2026-10-02. Status: complete, with two independent actual-file
reviews passing: the [first review](globally-convex-polynomial-point-oracle-review.md)
and [second review](globally-convex-polynomial-point-scout-review.md).
The [focused prior comparison](../prior-art/globally-convex-polynomial-point-prior.md)
is complete and makes no publication-priority claim. This finishes the
already-started global-convexity direction.

## 1. Statement and the global assumption

Fix an integer degree bound `D>=2`. Let `f` be an explicitly represented
rational polynomial of degree at most `D`, convex on **all of `R^n`**.
Let `P={x:Bx<=b}` be a nonempty bounded rational polytope with a supplied
rational bounding box. The base length `I` includes these data. Global
convexity is a promise, or has a supplied certificate whose verification
cost is charged. The polynomial-time claim presumes polynomial-time
verification if that verification is part of the task; recognizing
arbitrary polynomial global convexity is not an uncharged step.

Write `S=argmin_P f`. There is a polynomial-time computable rational
`Gamma>=1`, with `log Gamma=poly_D(I)`, such that

```
dist_2(x,S) <= Gamma [f(x)-min_P f]^(1/D)
                 for x in P with 0<=f(x)-min_P f<=1.     (1)
```

Consequently a deterministic algorithm returns a feasible rational point
within `2^(-q)` of `S` in `poly_D(I+q)` bit work. More strongly, it can
approximate the fixed minimum-Euclidean-norm point of `S` to this distance
in the same bound. Any requested certified objective gap can be obtained
simultaneously. The exponent of the polynomial work bound depends on
fixed `D`, not on dimension. Affine and constant objectives are included
by taking the same bound `D>=2`.

The assumption is stronger than convexity merely on `P` or on a bounded
box. The proof evaluates the polynomial outside that set and uses global
supporting planes and global convexity there. The reviewed bounded-box
quartic point-extraction comparisons do not contradict this theorem.
Neither exact active labels nor short expanded algebraic optimizer
representations are asserted.

If the domain is empty, exact rational LP detects it. A zero-variable
domain is direct evaluation. Lower-dimensional nonempty polytopes need
no special geometric assumption in the error-bound proof; the convex
value solver performs its usual rational affine-hull reduction.

## 2. Elementary univariate interpolation bounds

Define constants depending only on `D`:

```
C_D=(D+1)D^D,       J_D=(D+1)D^(D+1).                  (2)
```

For a real polynomial `r` of degree at most `D`, its values at
`j/D`, `j=0,...,D`, determine it by Lagrange interpolation. Every
denominator in those basis polynomials has absolute value
`j!(D-j)!/D^D>=D^(-D)`. Therefore

```
|r(t)| <= C_D (1+|t|)^D max_(0<=j<=D)|r(j/D)|.         (3)
```

If instead `|p(t)|<=W` on `[0,R]`, with `R>0`, apply interpolation
to `p(Rs)`. At zero each derivative of a basis polynomial has absolute
value at most `D^(D+1)`: differentiate its product into `D` terms,
bound each remaining factor by one, and use the denominator bound.
It follows that

```
|p'(0)| <= J_D W/R.                                    (4)
```

These deliberately coarse constants require no root finding, asymptotic
error-bound theorem, or numerical smoothness modulus.

## 3. Global convexity turns a small gap into small rational row residuals

Fix an optimizer `y in S` and a feasible `x`, and put

```
d=x-y,       E=f(x)-f(y).
```

Constrained first-order optimality and convexity imply
`0<=grad f(y)'d<=E`. Introduce the translated Bregman polynomial

```
h_y(u)=f(y+u)-f(y)-grad f(y)'u.                         (5)
```

Global convexity gives `h_y(u)>=0` for every `u in R^n`. On `0<=s<=1`,
convexity along the feasible segment gives

```
0 <= h_y(sd) <= s[f(x)-f(y)-grad f(y)'d] <= E.           (6)
```

Hence (3) implies the extrapolation bound, for every real `t`,

```
|h_y(2td)| <= C_D E(1+2|t|)^D.                         (7)
```

For a fixed rational sample point `c`, define the univariate polynomial

```
p_c(t)=h_y(c-y+td).
```

Global convexity and the midpoint identity give

```
0 <= p_c(t)
  <= (1/2)h_y(2(c-y))+(1/2)h_y(2td).                  (8)
```

The points in (8) need not lie in `P`. This is the indispensable global
step.

Here are explicit uniform bounds for the first term. Let
`U>=max(1,sup_(y in P)||y||_infinity)` be a rational bound from the input
box, and use only sample points with `||c||_infinity<=D`. Put `K=U+2D`.
If `f(x)=sum_alpha f_alpha x^alpha`, compute rational coefficient bounds

```
V=sum_alpha |f_alpha| K^|alpha|,
G=sum_(alpha,i:alpha_i>0)
                   |f_alpha| alpha_i K^(|alpha|-1),
H=max(1,2V+2G(D+U)),
W=H+3^D C_D.                                          (9)
```

They have polynomial binary length for fixed `D`. They bound `|f|`
and `||grad f||_1` on the relevant expanded box and give
`0<=h_y(2(c-y))<=H`, uniformly over the unknown optimizer and all
chosen sample points.

For `0<E<=1`, take `R=E^(-1/D)>=1`. Equations (7)--(9) give
`0<=p_c(t)<=W` on `[0,R]`, since
`E(1+2R)^D<=3^D`. Applying (4) now yields

```
|(grad f(c)-grad f(y))'d| <= J_D W E^(1/D).
```

Adding `0<=grad f(y)'d<=E<=E^(1/D)` proves

```
|grad f(c)'(x-y)| <= C_* E^(1/D),
C_*=1+J_D W.                                          (10)
```

If `E=0`, equation (6) says that the polynomial `h_y(sd)` vanishes
on an interval, hence identically. Equation (8) then bounds `p_c(t)`
between zero and `H/2` for every real `t`. A polynomial bounded on
the real line is constant, so its derivative vanishes. Also
`grad f(y)'d=0`. Thus (10) holds with zero right-hand side. No limiting
sequence of feasible positive-gap points is required.

## 4. Polynomially many rational gradients identify the whole optimizer set

Take the integer sample set

```
T={c in N^n: sum_i c_i<=D-1},
N=|T|=binom(n+D-1,D-1).                                (11)
```

It has polynomial cardinality for fixed `D`. It is unisolvent for
polynomials of total degree at most `D-1`. One direct proof uses the
basis `prod_i binom(x_i,alpha_i)`, `|alpha|<=D-1`. At integer node
`c`, its value is zero if any `alpha_i>c_i`; ordering by total degree
therefore gives a triangular evaluation matrix with diagonal one.

Let `A_rat` have rows `grad f(c)'`, one for each `c in T`. For any
direction `d`, the polynomial `z -> grad f(z)'d` has degree at most
`D-1`. Unisolvence consequently gives

```
A_rat d=0  iff  grad f(z)'d=0 for every z in R^n
           iff  f(z+td)=f(z) for every z and real t.     (12)
```

Thus its kernel is the global translation-invariance space of `f`.
Equation (10) at zero gap shows that the difference of any two
constrained optimizers belongs to this kernel. Conversely, invariance
preserves the objective. For every fixed optimizer `y`,

```
S={x in P:A_rat x=A_rat y}.                            (13)
```

The right-hand side may be irrational, but the matrix is rational,
known, and polynomially encoded. Affine objectives are handled correctly:
their constant gradient is a row of this matrix, so directions with a
nonzero affine slope are not mistakenly declared invariant.

All sample coordinates are bounded by `D-1`. Rational evaluation of the
fixed-degree gradient at the `N` nodes is polynomial-time, and all entry
lengths are polynomial in `I`. Choose an integer `Q>=1` clearing their
denominators and put `A=Q A_rat`. The product of the positive denominators
is one polynomial-bit choice.

## 5. A coefficient-height Hoffman bound makes the constant effective

Scale the rows of the rational inequality description of `P` by positive
integers so its coefficient matrix is integral. Let `C>=1` bound the
absolute entries of that matrix and of `A`. Both `C` and `Q` have
polynomial binary length. The following RHS-uniform estimate applies to
every nonempty slice `Z={z in P:Az=b_0}` and every `x in P`:

```
dist_2(x,Z) <= (nC)^(n-1) ||Ax-b_0||_2.                (14)
```

The vector `b_0` need not be rational. To verify (14), project `x` onto
`Z`, and express its projection normal using equality rows and active
inequality normals. Conic elimination modulo the equality row space
leaves independent rows, at most `n` in total. If their matrix is `R`,
then `RR'` has positive integer determinant at least one, and all its
eigenvalues are at most `(nC)^2`. Hence
`sigma_min(R)>=(nC)^(-(n-1))`. The coefficient vector in the normal
representation is bounded by this inverse singular value times the
projection distance. Inner products with active outward inequality
normals are nonpositive because `x in P`. The remaining equality-row
term is bounded by the displayed residual. Dividing by the distance
proves (14); zero distance is immediate. This is the same elementary
integer-minor proof used in the
[reviewed cubic Hoffman bound](convex-cubic-point-oracle.md#5-an-explicit-rational-hoffman-bound),
with general inequality normals replacing box normals.

From (10), `||A(x-y)||_2<=Q N C_* E^(1/D)`. Define

```
Gamma=max(1,(nC)^(n-1) Q N C_*).                        (15)
```

Equations (13)--(15) prove (1). All constants are computed in polynomial
time and have polynomial binary length. In particular, no unknown
algebraic optimizer height or numerical error-bound constant is an input
to the algorithm. The argument applies directly to lower-dimensional
`P`: global convexity is ambient, and (14) permits redundant or
universally tight inequalities.

## 6. Deterministic point and fixed-selector evaluation

For distance `epsilon=2^(-q)`, use the
[reviewed convex polytope value interface](convex-polytope-value-interface.md)
to obtain a feasible rational point of certified gap at most
`(epsilon/Gamma)^D`. Equation (1) proves distance at most `epsilon`
to the optimizer set. The required value precision is
`Dq+D log Gamma=poly_D(I)+Dq`, so bit work and certificate size are
`poly_D(I+q)`.

For a fixed point selector, let `p` be the minimum-original-Euclidean-norm
point of the compact convex set `S`, and let a rational `R_x>=1` bound
the norm of every point of `P`. Set

```
tau=epsilon^(2D-2)/(2*8^(D-1)*R_x^D*Gamma^D),
eta=tau epsilon^2/4.                                  (16)
```

Let `x_tau` minimize `f(x)+tau||x||^2` on `P`. Comparison with `p` gives
`||x_tau||<=||p||<=R_x` and objective gap at most `tau R_x^2<=1`.
If `s` is a nearest point of `S` to `x_tau` and `e=||s-x_tau||`,
the error bound and minimum-norm property give

```
e^D/Gamma^D <= f(x_tau)-f* <= 2R_x tau e,
||x_tau-p||^2 <= 2R_x e.                               (17)
```

For positive `e`, this implies
`e<=(2R_x tau Gamma^D)^(1/(D-1))=epsilon^2/(8R_x)`;
the zero case is immediate. Thus `||x_tau-p||<=epsilon/2`.
The regularized objective is strongly convex with modulus `2tau` in
the original coordinates. A feasible rational point of its certified
gap at most `eta` is within `sqrt(eta/tau)=epsilon/2` of `x_tau`.
It therefore approximates `p` within `epsilon`.

All precision and coefficient lengths in (16) are polynomial in `I+q`.
The convex value solver has a bit bound in those lengths, not in the
numerical inverse of `tau`. The penalty is the original norm; using a
norm in transformed relative coordinates could select a different point.
This proves a deterministic Cauchy oracle for one fixed optimizer,
without expanding its algebraic representation.

For a simultaneous objective-gap request, compute a rational
`G_0>=max(1,sup_P||grad f||_2)` of polynomial bit length and run the
point procedure at accuracy `epsilon/(2G_0)`. Its feasible point has
gap at most `epsilon/2`. A separate global value enclosure of width
`epsilon/2` supplies a lower bound that pairs with this point's exact
rational objective to give total width at most `epsilon`. This changes
only polynomially many accuracy bits.

## 7. Bounded transfer to the already-current core-completion interface

The same argument completes the existing selected-core Cauchy interface
under a stronger convexification promise than mere convexity on `P`.
Suppose an explicit fixed-degree polynomial `F_0(v,z)` and rational
`alpha>=0` satisfy

```
G_alpha=F_0+(alpha/2)||v||^2 is convex on ALL R^n,       (18)
```

with `v in [0,1]^k` on the bounded rational feasible polytope `P`.
The base length here includes `alpha`, the noise half-width `sigma`,
the completion data and its verification certificate, as in the inherited
core interface. If `k=0`, use Sections 1--6 directly; the following
completion assumes `k>=1`.
Keep the same finite core-noise law and expected core-output bound from
the [reviewed coupled core theorem](coupled-polytope-core-oracle.md).
For its fixed selected optimal core `a`, take `beta=alpha+1` and set
`G=F_0+(beta/2)||v||^2`. Then

```
T_a=G-(beta a+c)'v+(beta/2)||a||^2
    =F_0-c'v+(beta/2)||v-a||^2                         (19)
```

is globally convex of fixed degree, with optimizer set exactly the
optimal fiber `S_a`. The convention here is `F_c=F_0-c'v`.
The core search retains its original parameter `alpha`; `beta` is only
an auxiliary completion coefficient.

Although the slope of `T_a` can be irrational, its effective error bound
can again use a rational matrix. Apply Sections 2--3 to `T_a`, using a
uniform coefficient bound for `||a||<=sqrt(k)` and `|c_i|<=sigma`.
For example, majorize each unknown linear tilt coefficient by
`beta+sigma` and its constant term by `beta k/2`, and add these bounds
to the rational coefficient majorants of `G` in (9).
These bounds need no exact coefficients of `a`. At the fixed integer
sample points `s_j in T`, let the rational row matrix consist of
`grad G(s_j)'` together
with the core extraction rows. Write `Delta=T_a(x)-min T_a`. Equation
(19) gives `||v-a||<=sqrt(2Delta/beta)`. Thus for `Delta<=1`,

```
|grad G(s_j)'(x-y)|
 <= |grad T_a(s_j)'(x-y)|
      +||beta a+c|| ||v-a||
 <= C Delta^(1/D),                                    (20)
```

with a uniformly computable polynomial-bit rational `C`; here
`sqrt(Delta)<=Delta^(1/D)` since `D>=2`. The additional core-row
residuals obey the same bound. Their zero slice is precisely `S_a`:
core equality removes the unknown tilt, and unisolvence then certifies
global invariance of `G` along the displacement. Rational Hoffman gives
a uniform polynomial-bit `Gamma` for distance to `S_a`, independent of
the exact selected core.

Use (16) for this `Gamma`, replacing the regularized solve tolerance
by `eta=tau epsilon^2/8`. Request a short rational core approximation
`b` of error at most `tau epsilon^2/(32 beta k)` and solve

```
G(x)-(beta b+c)'v+tau||x||^2                            (21)
```

to that value gap. Its objective differs from the exact-core version
by at most `beta sqrt(k)||b-a||` uniformly on `P`. The same perturbation
calculation as the reviewed
[cubic completion](cubic-core-full-point-oracle.md) bounds its exact-core
regularized gap by `tau epsilon^2/4`. Strong convexity gives `epsilon/2`
solve error, and (17) gives `epsilon/2` selection bias.

Consequently this bounded composition returns the fixed minimum-norm
point in the lex-optimal-core fiber as a full-point Cauchy oracle, with
the inherited expected bound

```
f_D(k)(1+alpha/sigma)^k poly_D(I+q).                    (22)
```

When `alpha=0`, the
[jointly convex selected-core theorem](joint-convex-core-point-oracle.md)
improves this to ordinary expected `poly_D(I+q)` work. The completion
itself is polynomial-time in either case.

The core approximation is shortened to dyadic polynomial-length output
before postprocessing, as in the cubic completion; an expanded rare
fallback record is not treated as a short input. No new probability
event or resampling is required. This paragraph extends that existing
completion only under global promise (18); it makes no claim for an
arbitrary fixed-core convex residual or a convexifier valid only on `P`.

## 8. Limits and verification status

The quantitative point is effectiveness: both the exponent and the
logarithm of the error-bound constant have fixed-degree polynomial
control from rational input data. The
[completed source comparison](../prior-art/globally-convex-polynomial-point-prior.md)
credits Li's constrained qualitative error bounds, the project's broader
qualitative compact-polytope bound, and GLS convex value optimization.
Those qualitative bounds alone do not supply this computable precision
schedule. Globally convex polynomials of degree at most three are quadratic,
so exact convex-QP algorithms already cover those cases. The additional
algorithmic range here begins at fixed degree at least four. No priority
conclusion is made.

The reviewed [affine-power convexifier](affine-power-core-point-oracle.md)
is a concrete, polynomial-time-verifiable certificate class for the
global premise in Section 7. Its separate direct bound remains useful;
the representation does not certify every globally convex polynomial.

The assumptions do not permit replacing global convexity by bounded-domain
convexity beyond the separately reviewed cubic theorem. Nor does a point
Cauchy oracle decide exact active labels or provide short expanded
algebraic numbers. The proof's affine optimizer slice can have an
irrational right-hand side, which is not computed exactly by the
ordinary algorithm.

Both fresh actual-file reviews passed the complete proof and Section 7.
Their final rereads include the zero-core branch, charged input data,
uniform unknown-tilt coefficient majorants, and short-core output interface.
The parent independently checked the proof and ran the distinct diagnostic

```text
python3 -B research-20261002/new-direction/check_global_convex_point.py
```

It passed 168 exact interpolation/extrapolation formula checks for degrees
two through five, 84 derivative checks, 2,165 falling-factorial unisolvent
entries, 72 Bregman extrapolations, 1,680 global Jensen checks, 420 rational
gradient residual bounds, and 175 zero-gap invariance checks. The rational
sample-gradient matrix has rank three in dimension four. The fixture
`(x+2y)^4+(y-z)^2+t` includes sample nodes outside the feasible polytope,
rational gaps `r^4`, and a flat direction. This diagnostic was run by the
parent and was not duplicated here. It does not implement a generic convex
solver or experimentally verify the canonical algorithm or asymptotic bound.

Final scoped document checks cover local links, paired fences and math
delimiters, whitespace, control characters, and checker syntax; a scoped
`git diff --check` also passed. No index edits, project-wide tests, or CI
inspection were performed. This work is complete; no further directions
or extensions are proposed.
