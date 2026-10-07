# Full optimizer approximation for residual-convex cubics under core noise

Date: 2026-10-03. Status: complete proof; passed an
[independent actual-file review](../reviews/cubic-extension/review.md)
relative to the stated predecessor interfaces.

This note closes the point-output extension left open in the
[residual-convex cubic boundary note](../../research-20261002/new-direction/residual-convex-cubic-boundary.md).
It removes the supplied joint quadratic core convexifier from the cubic
full-point theorem on a product box. The new ingredients are an exact
core-face certificate obtained from nearby linear tilts, and an integer
lattice certificate for the implicit family of residual Hoffman minors.
Probability controls their cost; neither certificate assumes a probable
event when accepting an answer.

## 1. Statement and inherited interfaces

Let `F(v,z)` be an explicitly represented rational polynomial of total
degree at most three on `[0,1]^k x [0,1]^n`. Assume that `F(v,.)` is
convex for every core `v`, and supply verified rational bounds
`F_{v_i v_i}<=L`, with `L>=0`. Let `sigma>0` be rational. Include the
polynomial, bounds, noise width, and structural certificates in length
`I`. The work bound presumes polynomial certificate verification;
otherwise add its actual cost. No joint convexifier, residual strong
convexity, unique residual optimizer, or numerical condition bound is
assumed. Fixed coordinates may be substituted before normalization.

For `gamma` sampled from one endpoint-inclusive uniform rational product
grid in `[-sigma,sigma]^k`, write `F_gamma=F+gamma'v`. Let `a` be the
lexicographically first globally optimal core, and define

```
S_a = argmin_{z in [0,1]^n} F(a,z),
p = argmin_{z in S_a} ||z||_2^2.
```

The set `S_a` is nonempty, compact, and convex, so `p` is unique.

**Theorem.** There is a base-computable grid with `log M=poly(I)` such
that, on every draw and for every integer `q>=0`, an evaluator returns a
rational feasible `(v_q,z_q)` satisfying

```
||(v_q,z_q)-(a,p)||_2 <= 2^(-q).
```

Expected bit work and proof/output length are

```
f(k) (1+L/sigma)^k poly(I+q),
```

where `f(k)` is the computable parameter factor inherited from the
selected-core theorem and the polynomial exponent is absolute. One
random work factor bounds all precision
queries. The sampled objective and selector do not change with `q`.
A sampled objective-gap certificate of accuracy `2^(-q)` may also be
returned at the same order of cost. This is point-distance output for
the sampled objective, not expanded algebraic coordinates.

The proof uses the established
[selected-core oracle](../../research-20261002/new-direction/core-only-noise-core-oracle.md),
the polynomial-time rational convex residual value interface, and the
[exact polynomial fallback](../../research-20261002/new-direction/polynomial-exact-fallback.md).
The selected-core interface has a common all-precision random work
factor, accepts any sufficiently fine grid chosen before sampling, and
returns certified short rational core approximations. Its rare fallback
is included in that work factor. These are inherited results, not newly
proved counting or convex-optimization theorems.

If `n=0`, use the core oracle directly. If `k=0`, use the deterministic
[convex cubic point theorem](../../research-20261002/new-direction/convex-cubic-point-oracle.md)
with minimum-norm selection. Below assume `k,n>=1`.

## 2. Exact core faces from nearby tilts

Put `Lbar=max(1,L)`, and choose a base rational `0<t<=1/2`. For each
coordinate `i`, query selected cores for the two auxiliary objectives

```
F(v,z)+(gamma-t e_i)'v,
F(v,z)+(gamma+t e_i)'v.
```

Only accuracy `r<=t/(8Lbar)` is needed. Let `[ell_i^-,u_i^-]` and
`[ell_i^+,u_i^+]` be certified intervals for coordinate `i` of their
respective selected cores. Apply the sound rules

```
u_i^- < t/Lbar       => fix v_i=0,
ell_i^+ > 1-t/Lbar   => fix v_i=1.                    (1)
```

These rules fix a coordinate in **every** global optimizer of the
original draw. They cannot conflict.

To prove this, fix `gamma_{-i}` and project all other variables out:

```
W(s)=min_{v_{-i},z} [F(v,z)+gamma_{-i}'v_{-i}],
                      with v_i=s.
```

The minimum is continuous and attained on a fixed compact domain.
Every function being minimized has second derivative in `s` at most
`Lbar`; hence `W(s)-Lbar s^2/2` is concave. If `a_i` minimizes
`W(s)+gamma_i s` and `b_i` minimizes `W(s)+(gamma_i-t)s`, comparison of
their two optimality inequalities gives `a_i<=b_i`. At an interior
global minimizer of a semiconcave function plus a linear tilt, the
function is differentiable and its derivative equals minus the tilt.
Concavity then gives, whenever both cores are interior,

```
t = W'(b_i)-W'(a_i) <= Lbar(b_i-a_i).                (2)
```

If the first test in (1) passes and `a_i>0`, both cores are interior,
since `a_i<=b_i<t/Lbar<=1/2`. Equation (2) is impossible. The upper
rule follows by replacing `s` with `1-s`.

There is also a simple failure-probability bound. Define

```
theta = sup_{s>0} (W(0)-W(s))/s.
```

The value is finite because coefficient bounds make `W` Lipschitz.
An original optimizer can have `a_i=0` only if `gamma_i>=theta`.
If `gamma_i>theta+t`, every optimizer after the negative shift has
coordinate zero, and its interval upper endpoint is at most `2r`, so
the first test passes. Thus an original zero coordinate missed by the
test requires `gamma_i in [theta,theta+t]`. There is an analogous
interval of length `t` for an upper endpoint. Conditional on the other
noise labels, an endpoint-inclusive grid with `M` labels puts mass at
most `t/(2sigma)+2/M` in any interval of length `t`. A union bound gives

```
Pr{some endpoint of the selected original core is missed}
    <= k t/sigma + 4k/M.                            (3)
```

No residual solution or exact active-gradient sign is used in (1).
All unforced coordinates are provisionally free. A missed endpoint
will be rejected by the lattice certificate below, so (3) is used only
to bound fallback probability.

## 3. Certifying the unknown fiber's error bound

Let `A` be the face obtained from (1), with `m` free coordinates, and
let `c_A` be its relative center. Put

```
c_z=(1/2,...,1/2),
H_A = nabla_zz^2 F(c_A,c_z),
g_A(v) = nabla_z F(v,c_z),
B_A(v) = [H_A ; g_A(v)' ; I_n].
```

Write `H(v,z)=nabla_zz^2 F(v,z)`. The earlier residual-cubic structure
theorem proves

```
ker H_A subseteq ker H(v,z)       on A x [0,1]^n,
ker H(v,c_z) = ker H_A           for v in relint(A).
```

Individual residual boundary Hessians can have larger kernels. Provided
`a in relint(A)`, as lattice acceptance below certifies, the optimizer
fiber has the equality description

```
S_a = {z in [0,1]^n: H_A(z-y)=0, g_A(a)'(z-y)=0}
```

for any `y in S_a`. Only the single row `g_A` varies with the core, and
each square minor of `B_A` has degree at most two in the free core.

Compute uniform integers `D,B>=1`, of polynomial binary length, such
that every such minor on every original face, multiplied by `D`, is an
integer polynomial with coefficient magnitude at most `B`. No minor or
face enumeration is required. For example, a common denominator `d`
for all possible entry coefficients can be obtained by multiplying the
input coefficient denominators and a factor eight. Substitution of
core coordinates by `0`, `1`, or `1/2`, and residual center coordinates
by `1/2`, has denominator dividing this choice. A coefficient-sum bound
gives an integer `C>=1` for every cleared coefficient, uniformly over
faces. With `s_max=(k+1)(k+2)/2`, the conservative choices

```
D=d^n,              B=D n! (s_max C)^n
```

suffice. Their logarithms are polynomial in `I`.

Apply the [lattice certificate](lattice-certificate.md) to the free
coordinates of the exact selected core, using its established Cauchy
oracle, coefficient bound `B`, and a base scale `T`. On acceptance it
certifies, with `s=(m+1)(m+2)/2`,

```
|h'phi(a)| > xi := sB/T
for every nonzero integer h with ||h||_infinity<=B.    (4)
```

The monomial vector `phi` includes `1`, all free coordinates, and all
quadratics. Since `v_i` and `1-v_i` are among the tested polynomials,
acceptance proves that the provisionally free coordinates are truly
interior and have distance greater than `xi` from the face boundary.
Every minor polynomial is either identically zero or has its scaled
coefficient vector in this family. Thus (4) gives sound margins

```
delta=min(1/2,xi),        mu=min(1,xi/D).              (5)
```

Here `delta` bounds distances of free coordinates from endpoints, and
`mu` bounds absolute values of all nonzero minors at `a`. For `m=0`,
the face is already an exact rational vertex; use `delta=1/2` and
`mu=min(1,1/D)` directly, with no lattice step.

The conditional error bound in the residual-cubic structure theorem
now supplies, by rational arithmetic, a number `Gamma>=1` such that

```
dist(z,S_a) <= Gamma [F(a,z)-min_w F(a,w)]^(1/4)
                       whenever the gap lies in [0,1].     (6)
```

Its logarithm is polynomial in `I+log T`; the algorithm computes it
without exact knowledge of `a`. Rank-zero `H_A` and identically zero
minors are explicitly covered by that theorem. The LLL certificate
proves precisely the margin premise needed there.

## 4. Why these certificates usually succeed

Choose a rational `U>=1` with `nabla_vv^2 F(v,z)<=U I_k` everywhere,
using coefficient sums. Its numerical magnitude is not a parameter in
the final work bound; only its logarithm enters the base precision.

The [margin-tail proof](margin-tail.md) establishes two elementary facts.
On an open core face of dimension `m`, the map from an interior globally
optimal core to its free noise coefficients is locally `U`-Lipschitz.
It follows that, for any measurable core subset `E`, the continuous
uniform-noise probability of an optimizer in `E` on that face is at
most `(U/(2sigma))^m vol_m(E)`. For every nonzero integer polynomial
`p` of total degree at most two and `0<eta<1`,

```
vol_m{v in [0,1]^m: |p(v)|<=eta} <= 8 sqrt(eta).      (7)
```

Set `R=2^(s_max) 4s_max B`. A union bound over all faces and all
nonzero degree-two integer polynomials of coefficient height at most
`R` gives

```
Pr_cont{some such |p(a)|<=eta on the true open face}
 <= A sqrt(eta),
A=8 3^k max(1,U/(2sigma))^k (2R+1)^(s_max).           (8)
```

Zero-dimensional faces have no bad nonzero integer constants when
`eta<1`. The factor `A` has polynomial binary length. The family is
used for the union bound, never enumerated by the algorithm.

The same event has the finite-grid bound

```
Pr_grid{bad margin} <= A sqrt(eta)+C_tail/M,          (9)
```

with a base-computable `C_tail=2^poly(I)`. Indeed each face/polynomial
event says that an optimal witness lies on that relative face and
satisfies `|p(a)|<=eta`. It has one existential full-variable witness
block and one universal competitor block. Fixed-block real algebraic
elimination bounds its one-dimensional coefficient sections by
`2^poly(I)`, independently of the numerical margin and noise bit
lengths. Sum this bound over the finite polynomial family and faces,
then use the same marginal-replacement argument as the inherited
finite-noise theorem. An event defined through the LLL algorithm itself
need not have such a description: (9) bounds a sufficient condition
for its success instead.

If all polynomials of height at most `R` on the true free face have
absolute value greater than `eta`, the lattice certificate accepts
provided

```
T eta > (s_max+1)R.                                  (10)
```

Thus a fixed base `T` suffices on a high-probability event. It is not
increased with the requested point accuracy.

## 5. One finite law and the same-draw fallback

First choose `B_0=2^poly(I)>=2` large enough to cover the exact selected
full-point fallback described below, apart from its polynomial factor
in sampled coefficient length and requested accuracy. Set

```
t=min(1/2, sigma/(16kB_0)),
eta=min(1/4, (16 A B_0)^(-2)),
T=the least power of two strictly exceeding (s_max+1)R/eta.
```

These choices precede the noise mesh and have polynomial bit length.
The auxiliary shifted baselines `F +/- t v_i` also have polynomial
input length. Instantiate the inherited selected-core evaluator for
the original baseline and these `2k` baselines, using the **same**
random vector `gamma`. Choose a common grid size `M` large enough for
all their base mesh requirements and also for

```
(4k+C_tail)/M <= 1/(8B_0).
```

Each inherited mesh requirement is a lower bound; taking their maximum
is valid. Their fallback/count caps are computed from their respective
base lengths before `M` is chosen. Since there are only `2k+1` such
instances and each base length is polynomial in `I`, `log M=poly(I)`.
No accuracy-dependent or newly sampled perturbation is introduced.

Run the face tests and one lattice test at this base scale. If the
lattice test fails, retain the draw and use the exact fallback.
Equations (3), (8)--(10) give total failure probability at most

```
1/(16B_0)+1/(16B_0)+1/(8B_0) = 1/(4B_0).
```

Every accepted certificate is valid independently of this estimate.
On a missed boundary, the coordinate polynomial makes acceptance
impossible. On a tied-core draw, the face and lattice certificates may
still succeed; they concern the fixed selected core returned by the
inherited oracle and require no uniqueness premise.

The fallback selector is expressible by a fixed-block formula: a point
is globally optimal; every equal-value competitor has lexicographically
larger core, or has the same core and residual squared norm at least
that of the selected point. Convexity of the residual fiber makes that
point unique. The polynomial degree remains at most three and the
lexicographic test has linear-size Boolean syntax. The inherited
singleton-coordinate construction therefore gives short feasible
rational approximations to this **same** `(a,p)` in
`B_0 poly(I+b+q)` bit work, where `b` is noise coefficient length.
Clipping to the box preserves coordinate error. The exponential
factor is independent of `b,q`, as required before choosing the mesh.

## 6. Canonical residual completion at arbitrary precision

On the accepting branch, `Gamma` is fixed for the draw and has
polynomial base bit length. Take `epsilon=2^(-q)`, a rational
`R_z>=max(1,sqrt(n))`, and a rational bound
`G>=max(1,sup ||nabla_v F(v,z)||_2)`. Put `e=epsilon/2` and choose

```
tau=e^6/(1024 R_z^4 Gamma^4),
eta_q=tau e^2/8,
d_q=min(epsilon/2, tau e^2/(32G)).                    (11)
```

Obtain a short rational core `b in A` with `||b-a||<=d_q`; set the
certified fixed coordinates exactly to their face endpoints and clip
the others to `[0,1]`. Obtain a rational feasible residual `z_hat` of
objective gap at most `eta_q` for the rational convex cubic

```
Q_b(z)=F(b,z)+tau ||z||^2.                            (12)
```

All needed coefficient lengths and requested oracle accuracies are
polynomial in `I+q`.

For completeness, let `z_tau` minimize
`F(a,z)+tau||z||^2`. This problem is strictly convex even though its
coefficients need not be rational. Comparison with the minimum-norm
point `p` gives `||z_tau||<=||p||<=R_z`. If `s` is its nearest point
in `S_a`, and `d=||z_tau-s||`, (6) and the projection characterization
of `p` give

```
d^4/Gamma^4 <= F(a,z_tau)-F(a,p) <= 2 R_z tau d,
||z_tau-p||^2 <= 2 R_z d.
```

The initial gap is at most `tau R_z^2<=1`, so (6) applies. Equation
(11) implies `d<=e^2/(8R_z)` and `||z_tau-p||<=e/2`.
Uniformly over residual points, `|F(b,z)-F(a,z)|<=G d_q`. Hence the
true regularized objective gap of `z_hat` is at most

```
eta_q+2G d_q <= tau e^2/4.
```

Strong convexity gives `||z_hat-z_tau||<=e/2`. Therefore
`||z_hat-p||<=e`, while `||b-a||<=epsilon/2`; the combined Euclidean
error is at most `epsilon`. This completes the point guarantee.

For an additional objective-gap guarantee, request point accuracy
smaller by a polynomial-bit uniform gradient bound for `F_gamma`, and
pair the resulting feasible objective with an inherited certified
value lower bound at the desired accuracy. This changes only the
polynomial factor.

The ordinary stage uses a polynomial number of base-precision auxiliary
queries, one original core query at `poly(I)+O(q)` bits, LLL, and convex
rational optimization. Add the `2k+1` inherited common random work
factors and `B_0` times the indicator of the single base-stage failure
event. This sum is one random factor controlling every `q`, with the
claimed expectation. Independence between these work factors and the
certificate events is unnecessary. The large numerical upper Hessian
bound `U`, the lattice height, and the certified error constant enter
only through their polynomial bit lengths.

## 7. Scope

This result covers the earlier examples `F(v,z)=v z^2` and
`F(v,z)=gamma v-v^2 z`, which have no finite quadratic core convexifier.
It does not assert continuity of minimum-norm residual selection across
cores: exact boundary identification and error-controlled
regularization avoid assuming it. Exact bad algebraic relations and
unresolved boundary events are handled on their original finite-noise
draw, with the declared selector preserved.

The product box matters in the nearby-tilt projection, fixed rational
face kernels, and conditional error bound. The theorem does not extend
these arguments to arbitrary coupled domains or to degree four.
There is no publication-priority claim. The independent review records
the inherited interfaces and the limits of its internal verification.

## 8. Targeted verification

The exact diagnostic
[`check_cubic_recourse.py`](check_cubic_recourse.py) uses the cubic
`F(v,z)=v^2(2-z)-v`, whose residual fibers are affine and whose mixed
Hessian rules out a quadratic core convexifier. Its projected objective
and selected full optimizer are explicit. The command actually run was

```
python3 -B research-20261003-arithmetic/cubic-recourse/check_cubic_recourse.py
```

It passed 257 finite-noise face cases, including 124 sound forced
endpoints; 24 exact residual regularization completions, including
positive cores of size `2^(-120)`; nine actual LLL acceptances with 234
exhaustive height-one polynomial margin checks; and nine rejections in
the presence of exact integer relations. Six rejected fixtures have a
relation inside the tested height-one family; three have a short
height-two relation and illustrate the permitted conservative rejection
outside that family. The LLL changes of basis were checked to be unimodular.
These small exact fixtures exercise distinct composition boundaries.
They do not implement the general core oracle, convex value solver, or
probabilistic expected-work experiment. No project-wide verification or
CI inspection was performed.

The integrated-section review also prompted an explicit clarification
in Section 3: common-kernel inclusion holds on the whole face product,
whereas equality with `ker H_A` is asserted at residual center `c_z`
and an interior core. The fiber description is conditional on that core
interiority, which lattice acceptance certifies. This matches the
reviewed structural theorem and changes no algorithm or work bound.
