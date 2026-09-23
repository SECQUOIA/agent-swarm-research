# Optimal finite good-aggregation accuracy for the HHC example

Date: 2026-09-22. Status: author proof complete;
[independent adversarial review](review-20260922-aggregation-accuracy.md)
passed; the finite-aggregation bounds and exact rational constructions now
have Lean proofs in the scope below. This is a quantitative consequence of the construction in
[the main result](../results/infinite-quadratic-aggregation-hhc.md), not a
separate claim of a major approximation-theory advance.

The [Lean package](../formal/topics/31-aggregation-accuracy/README.md)
verifies the actual Euclidean metric, extended Hausdorff error and infimum,
both explicit optimal-error bounds, including the lower bound for arbitrary
good cut families, the rational mesh
with exact cut count and binary coefficient-size bounds, and the uniform
rate and constructive tolerance-budget consequences. It builds on the
[verified exact hull and SDP package](../formal/topics/30-infinite-aggregation-hull/README.md).
The formal proof uses the two alternative estimates described below.
The support-function interpretation and single-objective proposition in
Section 4 remain outside this Lean package, as do novelty and numerical
performance claims. See the [verification record](../formal/topics/31-aggregation-accuracy/VERIFICATION.md)
and [paper supplement](../paper-quadratic-aggregation/formal-aggregation-accuracy.tex).

## 1. What is approximated

For any `r>=2`, put

```
f1(u,v)=||u||²-1,   f2(u,v)=||v||²-1,   f3(u,v)=1/2-u·v,
K={lambda>=0: lambda3²<=4lambda1lambda2},
f_lambda=sum_i lambda_i f_i,
C=cl conv{(u,v): f1<0,f2<0,f3<0}.
```

The main result establishes

```
C = intersection_{lambda in K\{0}} {f_lambda<=0}
  = {||u||<=1, ||v||<=1,
     u·v+sqrt((1-||u||²)(1-||v||²))>=1/2}.
```

Thus `C` is compact and convex. For a finite family `F subset K\{0}`,
define `P_F=intersection_{lambda in F}{f_lambda<=0}`. Count inequalities,
allow arbitrary rescaling and arbitrary interior or extreme multipliers,
and measure distance in the Euclidean norm on `R^(2r)`. Set

```
e_N = inf_{|F|<=N} d_H(C,P_F).
```

The extended Hausdorff distance is infinite if `P_F` is unbounded. The
infimum definition does not assert that an optimal family exists.

**Theorem.** For every integer `N>=2`,

```
sqrt(2)(log 2)²/(1600 N²) <= e_N
                         <= 5sqrt(2)pi²/[16(N-1)²].       (1)
```

In particular `e_N=Theta(N^-2)`. The constants are uniform in `r>=2`.
Equivalently, a uniform Hausdorff guarantee `epsilon` requires and suffices
with `Theta(epsilon^-1/2)` good quadratic aggregations as `epsilon` tends
to zero. Constants are deliberately loose.

## 2. Upper bound: angle sampling and radial repair

Write

```
A(x)=[[1-||u||², u·v-1/2],
      [u·v-1/2, 1-||v||²]],
q(theta)=(cos theta,sin theta),
lambda(theta)=(cos²theta,sin²theta,2sin theta cos theta),
h_x(theta)=q(theta)^T A(x) q(theta)=-f_lambda(theta)(x).
```

These multipliers, for `0<=theta<=pi/2`, generate `K`. This includes its
two coordinate rays at the endpoints. Hence `x in C` exactly when
`h_x(theta)>=0` throughout that interval. Only nonnegative directions are
required: `A(x)` need not be positive semidefinite.

Take the `N` equally spaced angles, including both endpoints, with spacing
`Delta=pi/[2(N-1)]`, and call their relaxation `P_N`. Endpoint cuts imply
`||u||,||v||<=1` on `P_N`. There the diagonal entries of `A(x)` lie in
`[0,1]`, and its off-diagonal entry lies in `[-3/2,1/2]`. Consequently
`||A(x)||_op<=5/2`, by the maximum absolute row sum. Differentiation gives

```
h_x''(theta)=2q'(theta)^T A(x)q'(theta)-2q(theta)^T A(x)q(theta),
|h_x''(theta)|<=10.
```

Let `theta_*` minimize `h_x` on `[0,pi/2]`. If it is an endpoint, its
value is nonnegative. Otherwise `h_x'(theta_*)=0`; a mesh point is at
distance at most `Delta/2`. Taylor's theorem and nonnegative sampled
values therefore give

```
h_x(theta)>=-a for every theta,   a=5Delta²/4.             (2)
```

The sign follows from `0<=h_x(theta_j)<=h_x(theta_*)+5Delta²/4`.

Now `A(0)=[[1,-1/2],[-1/2,1]] >= (1/2)I`, and for `0<=s<=1`,

```
A(sx)=s²A(x)+(1-s²)A(0).
```

Choose `s=(1+2a)^(-1/2)`. Equation (2) implies
`h_sx(theta)>=-s²a+(1-s²)/2=0`, so `sx in C`. Thus

```
dist(x,C)<=||x-sx||<=sqrt(2)(1-s)<=sqrt(2)a.
```

The last inequality uses convexity of `(1+2a)^(-1/2)` and its tangent
`1-a` at zero. Taking the supremum over `P_N` proves the upper bound in
(1). All bounds hold for every point of the relaxation, not only its
boundary or selected witness points.

The Lean proof obtains the same angular estimate without formalizing this
second-derivative bound. At an interior minimizing angle `t`, stationarity
and the exact rotation identity give

```
h_x(s)=h_x(t)+(A11+A22-2h_x(t))*sin²(s-t).
```

The coefficient is at most `5`, since `A11,A22≤1` and `h_x(t)≥-3/2`.
A sample within `rho` and `|sin(s-t)|≤|s-t|` imply `h_x(t)≥-5rho²`.
The same radial repair completes the verified uniform upper bound.

**Exact rational coefficients.** For `N>=3`, set `m=floor((N-1)/2)`.
The rays `(m²,j²,2mj)` and `(j²,m²,2mj)`, for `j=0,...,m`, give
`2m+1<=N` distinct cuts including both endpoints. Their angular mesh has
maximum gap at most `1/m`, since `arctan` is 1-Lipschitz. The same proof
gives error at most `5sqrt(2)/(4m²)`. Each coefficient is a nonnegative
integer at most `2m²`, so the same asymptotic rate requires only
`O(log N)` bits per coefficient. The rank-one relation holds exactly;
independently rounding three coefficients need not preserve membership
in `K`. This construction, supplied in the review and independently
rechecked by the coordinator, makes no claim about numerical solution
error or conditioning.

## 3. Lower bound for arbitrary good cuts

Fix a family of at most `N` good cuts and set

```
eta=(log 2)²/(320N²),   e=1/10.
```

For each `tau in [1,2]`, choose vectors with Gram matrix

```
G_tau,eta=[[1-e/tau, 2/5-eta],
           [2/5-eta, 1-e*tau]],
x_tau,eta=(u_tau,eta,v_tau,eta).
```

Such vectors exist in `R²` and embed into `R^r`: `0<eta<1/10`, both
diagonal entries are at least `4/5`, and the determinant is at least
`16/25-4/25=12/25>0`. They satisfy both unit-ball bounds. Their values are

```
f(x_tau,eta)=(-e/tau,-e*tau,e+eta).                        (3)
```

Consider any nonzero `lambda in K`. If either `lambda1` or `lambda2`
vanishes, then `lambda3=0`, and its cut is strictly satisfied at every
witness. Otherwise set `t=sqrt(lambda1/lambda2)>0`. If its cut excludes a
witness, meaning `f_lambda(x_tau,eta)>0`, then

```
e(lambda1/tau+lambda2*tau-lambda3)<eta*lambda3,
lambda1/tau+lambda2*tau-2sqrt(lambda1lambda2)
                            <20eta*sqrt(lambda1lambda2),
t/tau+tau/t-2 <20eta,
|log tau-log t| < arcosh(1+10eta).                         (4)
```

The second line uses `lambda3<=2sqrt(lambda1lambda2)` on both sides;
this is why the argument covers interior good multipliers too. Since
`cosh z>=1+z²/2`, each cut excludes witnesses only in an interval of the
coordinate `log tau` having length at most

```
2arcosh(1+10eta)<=4sqrt(5eta)=(log 2)/(2N).
```

The union of at most `N` such intervals has total length at most
`(log 2)/2`, less than the length of `[0,log 2]`. Some `tau in [1,2]`
is therefore excluded by none of the cuts. Its witness belongs to `P_F`.
This argument requires no bound on the cut ratio `t`.

Use the good multiplier `lambda_*=(tau,1/tau,2)`. At this witness,

```
f_lambda_*(x_tau,eta)=2eta>0.
```

On the convex product of the two unit balls, the gradient of this quadratic
has norm at most `5sqrt(2)`: its quadratic matrix is
`[[tau,-1],[-1,1/tau]] tensor I_r`, which is PSD with operator norm
`tau+1/tau<=5/2`, and `||(u,v)||<=sqrt(2)`. Every `y in C` lies in this
same product, and `f_lambda_*(y)<=0`. The mean-value inequality gives

```
2eta <= f_lambda_*(x_tau,eta)-f_lambda_*(y)
      <= 5sqrt(2)||x_tau,eta-y||.
```

Consequently

```
d_H(C,P_F)>=dist(x_tau,eta,C)>=sqrt(2)eta/5
                                  =sqrt(2)(log 2)²/(1600N²).
```

The lower bound also holds for unbounded `P_F`, where the Hausdorff
distance is infinite. This finishes the proof of (1).

The Lean proof uses a finite-grid alternative that gives the stronger
bound `1/(2000N²)`. Take `eta=1/(400N²)` and `N+1` parameters
`tau_j=1+j/N`. If one good multiplier excludes witnesses at two parameters
`tau,sigma∈[1,2]`, its cone inequality implies

```
(tau-sigma)² < 16*((1+10eta)²-1) < 1/N².
```

Each cut therefore excludes at most one grid point, so at most `N` cuts
leave an actual witness admitted. An elementary Euclidean Lipschitz bound
of `10` for the separating ray quadratic gives distance at least
`2eta/10=1/(2000N²)`. Lean also checks that this is at least the lower
constant in (1). This proof needs neither a logarithmic interval cover nor
a multiplier-ratio bound, and it includes arbitrary interior good cuts.

## 4. Uniform linear objectives versus a chosen objective

For compact convex sets `C subset P`, Hausdorff distance equals
`sup_{||c||=1}(h_P(c)-h_C(c))`, where `h` is the support function.
For the upper bound this follows directly from nearest-point distance.
For the reverse inequality, take a point `x in P`, project it onto `C`,
and use the separating unit normal from that projection. Thus (1) also
quantifies the worst linear-objective gap over unit objective vectors
for one common, bounded aggregation relaxation.

The family may be chosen adaptively, but once its final size is `N`,
the same lower bound applies to its uniform guarantee. This does **not**
give an iteration lower bound when solving a prescribed linear objective.
In fact the following complementary observation shows why.

**Proposition.** For every nonzero linear objective `c`, there exists one
good multiplier `lambda` such that

```
min{c·x: x in C}=min{c·x: f_lambda(x)<=0}.                 (5)
```

This is a standard convex-duality consequence, included to prevent
misinterpretation of the approximation lower bound. Choosing the right
multiplier can still require solving the original convex problem.

Here is a self-contained separation proof. Let `F(x)=(f1(x),f2(x),f3(x))`,
and let `K*` be the dual cone of `K`. Every `f_lambda`, `lambda in K`,
is convex, so `F` is convex in the order induced by `K*`. The set

```
E={(F(x)+z,c·x+t): x in R^(2r), z in K*, t>=0}
```

is therefore convex and has nonempty interior. Let `v=min_C c·x` and
choose a minimizer `x_*`, which exists by compactness. Then `(0,v) in E`
is a boundary point: `(0,v-delta)` is not in `E` for any `delta>0`.
A supporting hyperplane yields a nonzero pair `(lambda,mu)` with

```
lambda in K, mu>=0,
f_lambda(x)+mu*c·x>=mu*v for all x.
```

The signs follow by adding arbitrary `z in K*` and `t>=0`. Moreover
`F(0)=(-1,-1,1/2)` pairs strictly negatively with every nonzero multiplier
in `K`: `f_lambda(0)<=-(lambda1+lambda2)/2<0`. Thus `mu=0` is impossible.
Normalize `mu=1`. Substitution of `x_*` gives `f_lambda(x_*)=0`.
If `lambda=0`, the displayed inequality would bound a nonzero linear
function on all of `R^(2r)`, which is impossible. Hence this is a good
nonzero multiplier, and every `x` with `f_lambda(x)<=0` satisfies
`c·x>=v-f_lambda(x)>=v`. The feasible point `x_*` proves (5).

A single fixed aggregation cannot serve all objective vectors, by (1).
An objective-dependent aggregation can attain the exact bound. Neither
statement establishes the numerical cost of finding or using that cut.

## 5. Literature, significance, and limitations

The main construction's sources and qualified novelty assessment are in
[its literature section](../results/infinite-quadratic-aggregation-hhc.md).
The theorem here uses its exact hull and good-multiplier classification.
It does not provide an independent proof of hidden hyperplane convexity.

Additional openly accessible sources examined on 2026-09-22:

- Arya, da Fonseca, Mount, [Optimal Area-Sensitive Bounds for Polytope
  Approximation, v2](https://arxiv.org/html/2306.15648v2), Sections 1 and
  1.1, and Theorems 1 and 2. They prove general polytope and convex-function
  approximation results and explicitly compare the classical
  `O(epsilon^(-(d-1)/2))` facet/vertex bounds of Dudley and
  Bronshteyn–Ivanov. The one-dimensional parameter and quadratic local
  error in the present proof are consistent with that classical geometry.
  Their approximants are linear halfspaces; ours are a prescribed family
  of convex quadratic sublevel sets in `R^(2r)`. Their results do not
  directly give the above constants or the lower bound for arbitrary
  interior good multipliers.
- Dudley, [Metric Entropy of Some Classes of Sets with Differentiable
  Boundaries](https://www.personal.soton.ac.uk/cz1y20/Reading_Group/ep-2022/week2/metric%20entrophy%20of%20some%20classes%20of%20sets%20with%20differentiable%20bondaries.pdf)
  (1974). The accessible abstract/introduction was inspected; it concerns
  metric entropy of families with controlled boundary regularity. No
  theorem from the paper is needed for (1).
- Bronshtein and Ivanov, [The approximation of convex sets by
  polyhedra](https://m.mathnet.ru/php/archive.phtml?jrnid=smj&option_lang=eng&paperid=4199&wshow=paper)
  (1975). The publication record was inspected, rather than the Russian
  proof; the modern paper above supplies the explicit comparison used
  here. No priority claim is based on this bibliographic check.

The proved consequence is a dimension-independent accuracy law for the
specific good-cut architecture. It quantifies a tradeoff between retaining
a finite bank of quadratic aggregations and using the exact small SDP lift
already available for this hull. It could guide a representation choice
in models containing this block. Solver benefit remains speculative until
cut selection, numerical conditioning, composition with other constraints,
and computational performance are studied.

The exponent two is familiar approximation geometry, and no broad new
approximation principle is claimed. The potentially useful addition is
the two-sided guarantee for this exact HHC example, including arbitrary
non-extreme good cuts and a clear separation between a uniform cut bank
and an objective-dependent exact aggregation. The rate does not cover
arbitrary original-space quadratic inequalities, nonlinear objectives,
arbitrary Boolean combinations, or lifted formulations. It gives no
runtime or branch-and-bound node lower bound.

## 6. Verification status

The finite-aggregation conclusions in Sections 1–3 and their rate and
tolerance-budget consequences are now verified in Lean, with the exact
scope stated above. The implementation uses explicit Euclidean coordinates
and extended Hausdorff distance; unbounded relaxations have infinite error.
It constructs an actual family for tolerance sufficiency and never assumes
that the infimum defining `e_N` is attained.

The [formal record](../formal/topics/31-aggregation-accuracy/VERIFICATION.md)
contains the targeted builds, transitive axiom audit, individual kernel
replays, source fingerprints, independent semantic reviews, and related
paper checks. No project-wide verification or CI inspection was run.
Section 4's support-function and single-objective claims remain
mathematically reviewed but outside this formal package.

Earlier verification consisted of mathematical review, file-format checks,
and exact computations on 64 rational meshes and 10,100 Gram witnesses.
Those finite checks did not establish the universal statements and are
not used as premises of the Lean proofs. The coordinator independently
re-derived the original angle estimate, logarithmic covering argument,
and rational mesh construction before formalization.
