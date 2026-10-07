# Full optimizer Cauchy output from a convexifiable cubic core

Date: 2026-10-02. Status: complete; the
[fresh full review](cubic-core-full-point-independent-review.md) and
[focused bit review](../reviews/cubic-core-completion-bit-review.md) passed.
The total objective has degree at most three. Convex cubic residual
slices alone are not the hypothesis used here.

## 1. Statement and selected optimizer

Let `P` be a nonempty bounded rational polytope in continuous variables
`x=(v,z)`, with `v in [0,1]^k` and supplied rational bounds on all remaining
coordinates. Let `F_0` be an explicit rational polynomial of total degree
at most three. Supply `alpha>=0` with a valid verified premise that

```
G_alpha(x)=F_0(x)+(alpha/2)||v||^2
```

is convex on `P`. The polynomial work bound assumes polynomial-time
verification of any supplied convexity certificate; otherwise add its
actual verification cost. Include these data and rational `sigma>0` in
base input length `I`. Perturb only the core:

```
F_c(x)=F_0(x)-c'v.
```

There is one base-computable endpoint-inclusive uniform rational product
law on `[-sigma,sigma]^k`, with polynomially many sampling bits, for which
the following holds. Let `a` be the lexicographically first optimal core,
and let

```
S_a={x in argmin_P F_c : v=a},
p_a=the minimum-Euclidean-norm point of S_a.             (1)
```

The set `S_a` is nonempty, compact and convex by the argument below, so
`p_a` exists and is unique. For every draw and every `q>=0`, an evaluator
returns a rational feasible `x_q in P` satisfying

```
||x_q-p_a||_2 <= 2^(-q).                                (2)
```

It may also return a certified original objective gap at most `2^(-q)`.
Expected bit work and expected proof/output size are

```
f(k)(1+alpha/sigma)^k poly(I+q),                         (3)
```

with `f(k)=k^{O(k)}` up to absolute constants and an absolute polynomial
exponent. A single random work factor bounds every precision query.
The law does not change with `q`. Every draw is correct, including ties.

When `alpha=0`, the expected bound improves to `poly(I+q)` using the
[jointly convex selected-core theorem](joint-convex-core-point-oracle.md).
When `k=0`, the [deterministic polytope cubic point theorem](convex-cubic-polytope-point-oracle.md)
applies; the selector is simply the minimum-norm global optimizer. Empty and
zero-dimensional polytopes are handled by exact rational LP.

This is full point-distance output for the sampled objective, with a fixed
selector across queries. It is not an expanded algebraic representation
or an exact active-set decision. There is no uniform numerical growth
modulus in the input.

## 2. A separate completion penalty leaves the search parameter unchanged

Set `beta=alpha+1`, and define

```
G(x)=F_0(x)+(beta/2)||v||^2.
```

This is a convex cubic on `P`, and `beta>=1`. For the exact selected core
`a`, define the possibly irrational-coefficient convex cubic

```
T_a(x)=G(x)-(beta a+c)'v+(beta/2)||a||^2
      =F_c(x)+(beta/2)||v-a||^2.                         (4)
```

Writing `f*=min_P F_c`, every feasible point satisfies `T_a>=f*`, with
equality exactly when it belongs to `S_a`. Therefore

```
argmin_P T_a=S_a,
Delta(x):=T_a(x)-f* >= (beta/2)||v-a||^2.                (5)
```

This proves convexity of the target fiber even when `F_c` is nonconvex
and its full optimizer set has several components. Strict positivity of
`beta` is important on tied draws, including when `alpha=0`.

The core search still uses the supplied `alpha`, not `beta`. The larger
coefficient appears only in polynomial-bit convex completion. Thus it
does not introduce an additional numerical `1/sigma` factor into (3).
The evaluator will never need exact coefficients of `T_a`.

## 3. A rational matrix describes the target fiber

Use the exact LP affine-hull reduction in the
[polytope value interface](convex-polytope-value-interface.md):

```
x=x_0+B w,   w in R={w:A w<=b},
B(0,r) subset R subset B(0,R_0),                        (6)
```

where `R` has dimension `m>=1`, `r>0` is rational, and choose a rational
`R_0>=1`. All data have polynomial binary length and are computable in
polynomial time. The core becomes `v=v_0+E w`. A rational bound on
`||B||_2` is available, for example its entrywise one-norm.

Put

```
h(w)=G(x_0+B w),  H(w)=nabla^2 h(w),
H_0=H(0),        g_0=nabla h(0),        K=ker H_0.
```

Convexity is relative to `aff(P)`: the matrices here are the reduced
Hessians, not ambient Hessians outside that affine hull. They are positive
semidefinite on `R`. Since `H` is affine, reflecting toward the known
inner ball proves

```
0 <= H(w) <= B_0 H_0,   B_0=1+R_0/r.                    (7)
```

Indeed `-(r/R_0)w` belongs to `R`, and the affine combination of its
Hessian with `H(w)` giving `H_0` has positive weights. Consequently `K`
is the common kernel of all feasible Hessians. The function
`h(w)-g_0'w` has gradient in `K^perp` and is constant along feasible
segments parallel to `K`.

Fix any `y in S_a` and write its reduced coordinate as `u`. Then

```
S_a={x_0+B w : w in R,
                  H_0(w-u)=0, g_0'(w-u)=0, E(w-u)=0}.   (8)
```

To see necessity, both points minimize the convex cubic `T_a`, so its
cubic transverse-gap argument below forces `H_0(w-u)=0`. Equation (5)
gives the core equality; along the common kernel the change in `h` is
`g_0'(w-u)`, which must vanish. Conversely the three equalities preserve
the core and the value of `G`, hence preserve `F_c` and optimality.

The coefficient matrix in (8) is rational and base-computable, although
its right-hand side can be irrational. The unknown vector `a` does not
occur in that matrix. This is the main distinction from applying a
rational-coefficient error bound directly to the irrational slope of
`T_a`.

## 4. A uniform polynomial-bit fourth-root error bound

All constants in this section are computed without knowing `a` or `u`.
Take a rational `M>=max(1,||H_0||_2)`. First suppose `H_0` has positive
rank, and let `lambda_0>0` be a rational lower bound on its smallest
positive eigenvalue, with polynomial binary length. For example, if
`D_H` clears its denominators, the principal-minor bound gives

```
lambda_0=D_H^(-m) M^(-(m-1)).
```

For `d=w-u`, let `P_K` denote projection onto `K^perp`, and put
`a_0=d'H(u)d`, `b_0=d'H(w)d`, and `s=a_0+b_0`. Exact cubic Taylor
expansion and first-order optimality for `T_a` give

```
Delta(x) >= (2a_0+b_0)/6 >= s/6.                        (9)
```

Symmetry of the cubic third derivative gives

```
d'H_0 d=a_0-u'(H(w)-H(u))d.
```

Using (7), positive semidefiniteness, `||u||<=R_0`, and
`||d||<=2R_0`,

```
d'H_0 d <= s+R_0 sqrt(2 B_0 M s)
         <= 3R_0 sqrt(2 B_0 M s).
```

Consequently

```
||P_K d|| <= C_perp Delta(x)^(1/4),
C_perp=108 R_0^2 B_0 M/lambda_0^2.                     (10)
```

The fourth power of the sharper bound is at most the displayed rational
quantity; that quantity is at least one, so the coarser form (10) is
valid and has polynomial binary length. If `H_0=0`, all feasible Hessians
vanish, set `C_perp=0`, and the same inequality holds with zero left
side. No positive-eigenvalue claim is then made.

The gradient of `h-g_0'w` has norm at most `B_0 M R_0`. With
`N=k(beta+sigma)` and `||beta a+c||_2<=N`, equations (4)--(5) imply

```
||E d|| <= 2 sqrt(Delta),
|g_0'd| <= Delta+N||E d||+B_0 M R_0 ||P_K d||.           (11)
```

For `0<=Delta<=1`, the stacked rational equality residual in (8) is
therefore at most

```
C_res Delta^(1/4),
C_res=3+2N+M(1+B_0 R_0)C_perp.                         (12)
```

Here the sum of the three block norms bounds their stacked Euclidean
norm. The estimate `sqrt(2/beta)<=2` used in (11) is uniform because
`beta>=1`.

Clear denominators of `A` and `[H_0;g_0';E]` by a positive integer `D`,
and let `C>=1` bound the absolute entries of both resulting integer
matrices. The polyhedral Hoffman bound, using at most `m` independent
rows in the projection argument, gives for `w in R`

```
dist(w,{t in R:H_0(t-u)=0, g_0'(t-u)=0, E(t-u)=0})
 <= (m C)^(m-1) D ||[H_0;g_0';E](w-u)||.               (13)
```

The bound is uniform in the possibly irrational equality right-hand
side. Its coefficient heights, rather than a numerical condition
promise, control its logarithm. One can prove (13) by the same integer
minor argument as the
[reviewed cubic Hoffman lemma](convex-cubic-point-oracle.md#5-an-explicit-rational-hoffman-bound),
using active rows of `A` in place of active box normals. Feasibility of
`w` makes their inner-product contribution nonpositive. Redundancies
and lower-dimensional target slices do not change this argument.

Taking a rational `B_norm>=max(1,||B||_2)`, define

```
Gamma=max(1,B_norm (m C)^(m-1) D C_res).
```

Combining (8), (12), and (13) proves the effective bound

```
dist(x,S_a) <= Gamma [T_a(x)-f*]^(1/4)
       whenever 0<=T_a(x)-f*<=1.                        (14)
```

The algorithm computes `Gamma` in polynomial bit time, with
`log Gamma=poly(I)`. The bound is uniform in every exact selected core
and every coefficient vector `c in [-sigma,sigma]^k`, including finite
law atoms with several optimal cores. Only the known magnitude bound
on `c` enters it.

## 5. Canonical completion using only short rational core approximations

Let `epsilon=2^(-q)`, and take rational `R_x>=1` bounding `||x||_2` on
`P`. Set

```
tau=epsilon^6/(1024 R_x^4 Gamma^4),
eta=tau epsilon^2/8,
delta=tau epsilon^2/(32 beta k).                        (15)
```

Let `x_tau` minimize `T_a(x)+tau||x||^2` on `P`. This strictly convex
problem has one minimizer. The standard fixed-fiber regularization
argument, included here to fix the rate, compares it with `p_a`:

```
T_a(x_tau)-f* <= tau(||p_a||^2-||x_tau||^2),
||x_tau||<=||p_a||<=R_x.
```

The gap is at most `tau R_x^2<=1`. If `s` is a nearest point in `S_a`
and `e=||s-x_tau||`, (14) and the minimum-norm property yield

```
e^4/Gamma^4 <= T_a(x_tau)-f* <= 2R_x tau e,
||x_tau-p_a||^2 <= 2R_x e.
```

Thus `e<=(2R_x tau Gamma^4)^(1/3)<=epsilon^2/(8R_x)`, and

```
||x_tau-p_a|| <= epsilon/2.                             (16)
```

Now request only a short dyadic vector `b` from the
[selected-core oracle](coupled-polytope-core-oracle.md), with
`||b-a||<=delta`. The opposite noise sign used in some source interfaces
has the same symmetric product law. Its coordinates have polynomial length
in `I+q`: request error `delta/2`, round each coordinate to a sufficiently
fine dyadic mesh, and clip to `[0,1]`. This requires only
`poly(I)+O(q)` core accuracy bits. Feasibility of `b` as a projected
point is unnecessary.

On an exact fallback branch, refine the selected algebraic core directly
to that dyadic precision. The base-only fallback budget and finite law
are chosen to cover this short-output query. The completion consumes
only the short dyadic vector, not an expanded algebraic record whose
length might be exponential. Reading or transforming such a record is
not silently charged as polynomial-time postprocessing.

Use the convex polytope value interface to obtain a feasible rational
`x_hat` with objective gap at most `eta` for the explicit rational cubic

```
Q_b(x)=G(x)-(beta b+c)'v+tau||x||^2.                    (17)
```

The corresponding `Q_a` differs from `T_a+tau||x||^2` by a constant,
and `|Q_b(x)-Q_a(x)|<=beta sqrt(k) delta` throughout `P`. Hence

```
Q_a(x_hat)-min_P Q_a
 <= eta+2 beta sqrt(k) delta
 <= tau epsilon^2/4.                                   (18)
```

Strong convexity in original Euclidean coordinates gives
`||x_hat-x_tau||<=sqrt((Q_a(x_hat)-min Q_a)/tau)<=epsilon/2`.
Together with (16), this proves (2). The norm penalty is the original
`||x||^2`, not the norm of affine-hull or normalized coordinates; this
preserves the declared selector on nonunit or lower-dimensional domains.

All coefficients and requested precisions in (15)--(17) have polynomial
length in `I+q`. The final solve is convex and has polynomial bit cost
without a numerical strong-convexity factor. Uniform constants in (14)
make the number of requested core bits polynomial, independent of the
draw. Thus the core oracle's common random work factor is inherited by
the full-point evaluator.

For a simultaneous objective-gap request, let `G_1>=max(1,sup_P
||nabla F_c||_2)` be a rational polynomial-bit bound, uniform over the
noise support. Run the point procedure with accuracy
`epsilon/(2G_1)`. Its feasible output has original gap at most
`epsilon/2`. A value-oracle interval of width `epsilon/2` supplies a
certified lower bound; pairing that bound with the point's objective
value gives width at most `epsilon`. This adds only polynomial accuracy
bits and another query governed by the same sampled law and work factor.

## 6. Scope and verification boundary

The total-degree-three and joint-convexifier assumptions are both used.
A merely convex cubic residual objective at each fixed core does not
provide the rational common Hessian kernel in Section 3. A quartic
Hessian is not affine, so the uniform argument also does not follow for
arbitrary convexifiable quartics. Moving-fiber discontinuity is avoided
by optimizing a convex surrogate on the fixed original polytope, rather
than assuming that residual optimizers depend continuously on the core.

The result complements the deterministic convex cubic point theorem and
the finite-noise core Cauchy theorem. For quadratic objectives, exact
rational reconstruction is already available in the
[QP reconstruction note](qp-core-cauchy-reconstruction.md); no new exact-QP
claim is made here. For cubics, the output is a fixed full-point Cauchy
name, not an exact boundary label or polynomial-size algebraic expansion.
The [cubic source comparison](../prior-art/convex-cubic-point-oracle-prior.md)
distinguishes the effective cubic error constant from classical weak
convex value optimization, qualitative polynomial error bounds, and
convexity recognition. It also records Kannan--Rademacher's algorithm
for a convex objective plus a low-dimensional polynomial perturbation:
that method gives an accuracy-dependent objective approximation, rather
than the fixed-selector point-distance guarantee here. The
[coupled-value comparison](../prior-art/coupled-polytope-core-value-oracle-prior.md)
covers the convexification and finite-noise predecessor. The additional
step proved in this note is the uniform rational-row bound for the
unknown-core surrogate and its canonical completion. These focused
comparisons do not establish publication priority.

The [focused bit-composition review](../reviews/cubic-core-completion-bit-review.md)
passed a fresh complete-file read. It checked the rational-row error
bound, tied and zero-shift cases, canonical selector, and short-output
safeguard. The [separate full review](cubic-core-full-point-independent-review.md)
also passed the actual completed file. The parent independently read
the full derivation and reported no gap; that was a separate analytic
check.

The distinct exact diagnostic
[check_cubic_core_completion.py](check_cubic_core_completion.py) uses
`F_c=z^2-2vz+v^3-(1/4+c)v`, `alpha=2`, and the coupled equality
`t=v+z`, with a flat coordinate in `[-2,1]`. Its three sampled coefficients
have explicit irrational optimal cores. Arithmetic in their quadratic
radical fields is exact. The rational surrogate solves reduce to a
monotone scalar derivative and receive exact tangent-gap certificates;
the norm penalty includes the lifted coordinate `t`.

The [saved results](cubic-core-completion-results.json) report 60 rational-row
checks, 42 lifted fourth-root error bounds, nine actual rational canonical
completion solves and tangent certificates, nine perturbation budgets,
five tied-core selector checks and 12 affine rank-zero checks. Dyadic
core approximations use up to 297 denominator bits. The command actually
run was:

```
python3 -B research-20261002/new-direction/check_cubic_core_completion.py
```

These are small exact composition fixtures, not an implementation of the
general core oracle or GLS solver, and not a stochastic work estimate.
No index edits, project-wide verification, or CI inspection are part of
this work.
