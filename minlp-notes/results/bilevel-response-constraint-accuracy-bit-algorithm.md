# Response-dependent upper constraints: exact safety with an accuracy-bit guarantee

Date: 2026-09-06. Status: two independent full proof reviews passed for Sections 1–12; see the [first audit](../notes/review-bilevel-reopened-response-constraints.md) and [second audit](../notes/review-bilevel-reopened-response-constraints-second.md). The convex aggregate dependency also passed two full reviews. Publication priority remains qualified by the bounded source search.
This is a continuation of the [fixed-resource accuracy-bit theorem](bilevel-fixed-resource-accuracy-bit-algorithm.md), including its signed-polynomial extension. The new claim is a conditional global bit-complexity extension of that theorem. Constraint tightening, Lipschitz safety margins, convex interpolation, and perturbation arguments are established techniques and are not claimed as new.

## 1. What this adds

The previous theorem excludes upper constraints involving the follower response. This result proves three useful additions, first for affine upper data and then for general explicitly encoded polynomial objectives and constraints in Section 12:

1. Without regularity assumptions, global optimization with separately prescribed objective error and upper-constraint violation, both polynomial in accuracy bits.
2. Exact upper feasibility and global additive optimization when the objective cost of tightening all upper inequalities has a supplied effective modulus.
3. Two explicit sufficient conditions for that modulus: convex reduced upper constraints with a strict feasible anchor, or reserve/offset decisions that do not affect follower behavior and provide uniform safe headroom.

The second sufficient condition allows nonconvex reduced upper feasibility. The first allows a nonconvex reduced upper objective. Both retain arbitrarily many follower coordinates and upper inequalities. Only the leader and lower resource dimensions are fixed. These are proved complexity algorithms using the existing polynomial-surrogate construction, not implemented scalable solvers.

A counterexample shows why a strict feasible point alone is insufficient. Another shows why unrestricted exact rational feasible output is impossible even for two affine upper inequalities.

## 2. Model and notation

Use exactly the rational input, fixed leader dimension `r`, fixed resource-row count `k`, dense strictly increasing polynomial marginals, numerical degree bound `P`, and leader-independent resource matrix of the existing theorem. Write

```
X' = {x in X: there exists z in [0,1]^N with Cz <= b(x)},
z(x) = unique follower optimum,
H(x) = d_0 + d^T x + c_0^T z(x),
f_j(x) = a_j0 + a_j^T x + c_j^T z(x),   j=1,...,m.
```

The upper problem minimizes `H` over `x in X'` with `f_j(x)<=0`. The number `m` is part of the input and need not be fixed. The existing construction supplies an explicit rational polytope `X'` and continuity of `z` on it. Thus the upper feasible set is compact and its minimum is attained if nonempty.

The proofs below assume `N>=1`. If `N=0`, the affine upper problem is a rational LP and is solved directly. The polynomial-upper extension in Section 12 treats its response-free case by fixed-dimensional polynomial optimization with the same margin qualifications. The response-surrogate construction must still run when the upper objective is response-independent but any upper constraint depends on the response; the original objective-only `c=0` LP shortcut does not apply in that case.

Leader-only affine inequalities and equalities should be included in `X`; they need not be tightened. Upper equalities involving `z` can be represented by opposite inequalities for the outer approximation, but the exact-feasibility guarantees below require positive tightening margins and therefore do not cover such equalities in general.

For `t>=0`, define

```
V(t) = min{H(x): x in X', f_j(x)<=-t for every j},
```

with `V(t)=+infinity` when that set is empty. All tolerances below are positive rationals; logarithmic accuracy means polynomial in their binary encodings, including `log(1/t)` for a dyadic tolerance.

## 3. Quantitative response graph inherited from the existing proof

We first isolate the interface actually needed, so no exact radical comparisons are hidden in an optimization oracle.

For any rational `rho in (0,1)`, the construction in Sections 3–6 of the existing theorem builds polynomially many compact rational cells `Q` in fixed dimension `r+k`, polynomials `p_i(v)` on each cell, and compact semialgebraic candidate sets `S_Q subset Q`, with the following properties:

- Every feasible leader `x in X'` has a lift `v=(x,theta)` in some `S_Q`, and at this lift `||p(v)-z(x)||_infinity<=rho`.
- Every `v in S_Q` has `x in X'` and `||p(v)-z(x)||_infinity<=rho`.
- A selected algebraic minimizer in `S_Q` can be rounded to a rational `vhat in Q`, preserving `xhat in X'`, so that the same response error bound holds at `vhat` and any prescribed finite list of polynomial values changes by at most a supplied positive tolerance.
- All sizes and running times are polynomial in input bits, numerical `P`, and `log(1/rho)`, for fixed `r,k`.

Here the rounded point need not remain in `S_Q`. The last property uses the residual slack explicitly budgeted in the original proof, rather than an assertion that arbitrary nonlinear feasibility survives rounding.

For clarity, take its `tau=rho/2` and choose its inverse tolerance `eta<=rho/2` using equation (9) with this `tau`. Its candidate set has resource residual allowance `S eta` and complementarity allowance `k Lambda S eta`. Rounding is chosen to change those two residual polynomials by at most these same allowances. The actual inverse response then has resource residual at most `3S eta` and complementarity error at most `3k Lambda S eta`. Equation (8) gives response error at most `tau`, and adding the polynomial inverse error gives `||p-z(xhat)||<=rho`. At unrounded candidates the allowances are smaller. A true KKT lift belongs to a candidate set. Additional polynomial rounding tolerances cost only more accuracy bits because the cells and polynomials have polynomial encoding length. The case `k=0` uses the original diagonal inverse arrangement and needs no residual argument.

All new affine upper polynomials have the form

```
F_j(v)=a_j0+a_j^T x+c_j^T p(v),
H_Q(v)=d_0+d^T x+c_0^T p(v).
```

Their response errors are bounded by `A_j rho`, where `A_j=||c_j||_1`. Their degrees and encodings remain polynomial; adding `m` inequalities does not increase the number of variables used by fixed-dimensional real algebraic optimization.

## 4. Outer and inner algorithms

**Theorem 1 (outer guarantee).** Given objective tolerance `epsilon>0` and violation tolerance `delta>0`, a polynomial accuracy-bit algorithm either certifies that the original upper problem is infeasible, or returns a rational `xhat in X'` such that

```
f_j(xhat)<=delta for every j.
```

If the original upper problem is feasible, the algorithm returns a point and also guarantees

```
H(xhat)<=V(0)+epsilon.
```

A returned point is not a certificate of original feasibility, and its objective may be lower than `V(0)`.

**Proof.** Put `A=max(1,A_0,...,A_m)` and

```
rho=min(1/4, epsilon/(8A), delta/(8A)).
```

On every response candidate set impose `F_j<=A_j rho` and minimize `H_Q`. Every true feasible leader has a lift satisfying these inequalities. Hence emptiness of all augmented sets certifies original infeasibility, and otherwise an exact winning minimizer `v*` has `H_Q(v*)<=V(0)+A_0 rho` when `V(0)` is finite. Round within its rational cell, changing `H_Q` by at most `epsilon/4` and each `F_j` by at most `delta/4`, while retaining the response-graph guarantees above. Then

```
f_j(xhat)<=2A_j rho+delta/4<=delta/2,
H(xhat)<=V(0)+2A_0 rho+epsilon/4<=V(0)+epsilon/2.
```

The stated weaker bounds follow. The algebraic winner is computed only in fixed dimension. No sum of exact inverse values is compared. QED.

**Theorem 2 (inner guarantee).** Given `epsilon>0` and `delta>0`, a polynomial accuracy-bit algorithm either reports that its inner surrogate is empty, or returns a rational `xhat in X'` satisfying every original upper inequality exactly. If `V(delta)<+infinity`, it returns a point with

```
V(0)<=H(xhat)<=V(delta)+epsilon.
```

Emptiness certifies `V(delta)=+infinity`, but does not certify original infeasibility.

**Proof.** Use the same `A,rho` and impose `F_j<=-delta/2`. Every point feasible for `V(delta)` has a lift because `A_j rho<=delta/8`. Round so that each `F_j` changes by at most `delta/8`, the objective changes by at most `epsilon/4`, and response error remains at most `rho`. Thus

```
f_j(xhat)<=-delta/2+delta/8+A_j rho<=-delta/4<0.
```

The objective ledger is `H(xhat)<=V(delta)+2A_0 rho+epsilon/4<=V(delta)+epsilon/2`. If the augmented sets are nonempty without the premise `V(delta)<infinity`, the same feasibility conclusion still holds; only that comparison is vacuous. QED.

For either output, evaluating `H_Q(vhat)` gives a rational estimate of the achieved objective within `A_0 rho`. This is not automatically an estimate of `V(0)` for the outer algorithm.

### 4.1 A posteriori global objective certificates

The outer and inner procedures also supply a computable global gap without a margin assumption. Suppose they both return. Let `h_out` and `h_in` be their rational rounded surrogate objective values. Let `rho_out,rho_in` be their respective response tolerances, and `omega_out` the absolute objective rounding allowance used by the outer procedure. Then

```
Lower=h_out-omega_out-A_0 rho_out,
Upper=h_in+A_0 rho_in
```

are rational numbers satisfying

```
Lower<=V(0)<=H(x_in)<=Upper.
```

Indeed the exact outer surrogate minimum is at most `V(0)+A_0 rho_out`, and rounding changes it by at most `omega_out`. The inner point is exactly feasible and its true objective is at most `h_in+A_0 rho_in`. Thus `Upper-Lower` is a valid global optimality certificate without trusting an unverified regularity promise. If the original upper problem were infeasible, no inner point could be returned, so the comparison has no hidden feasibility premise.

As all tolerances decrease to zero, the outer lower bounds converge to `V(0)` whenever the original problem is feasible: an allegedly smaller limiting value would, by compactness and continuity of the true response, yield an exactly feasible leader of smaller objective. Inner upper bounds converge as well if `V(t)` tends to `V(0)` from the right. A supplied modulus makes this quantitative in accuracy bits. Without such a modulus the gap may fail to close; Section 8.1 gives an example. The interval is useful even before convergence, but no general finite stopping guarantee follows merely from strict feasibility somewhere.

## 5. Exact feasibility under a tightening modulus

**Corollary 3.** Suppose positive rational data `D,sigma` and a positive integer `q` are supplied, with the promise

```
V(t)<=V(0)+D(t/sigma)^(1/q)   for 0<t<=sigma.             (M)
```

Suppose `V(0)` is finite. Then a rational exactly upper-feasible leader within additive `epsilon` of `V(0)` is computable in time polynomial in input bits, numerical `P`, numerical `q`, and `log(1/epsilon)`. The modulus parameters enter through their encodings. The algorithm need not verify the promise.

**Proof.** Take

```
t=sigma min{1/2, (epsilon/(2D))^q},
```

and apply Theorem 2 with tightening `t` and objective tolerance `epsilon/2`. Condition (M) makes the inner set nonempty and bounds its loss by `epsilon/2`. The encoding of `t` has polynomial length in the stated parameters. QED.

One can also compute a rational absolute-error estimate of `V(0)`: run the construction at, for example, one quarter of the requested error and use its rational estimate of `H(xhat)`. Exact feasibility gives a lower bound on `H(xhat)` by `V(0)`, while the inner guarantee bounds their difference. No exact value representation is required.

## 6. Concrete condition A: convex reduced upper constraints

The composition `f_j(x)=a_j0+a_j^T x+c_j^T z(x)` need not be convex. Here convexity is an additional promise about each reduced upper inequality. We do not claim that it follows from convexity of the follower objective, or that checking it is polynomial.

Let `K,L,mu` be the polynomial-bit rational constants in the existing fixed-resource proof, with the signed-polynomial choice of `mu` when appropriate. Let

```
B_b=max_j ||coefficient_vector(b_j)||_1       (zero if k=0),
B_ell=sum_i ||coefficient_vector(ell_i)||_1,
T=2 L K B_b+B_ell,
C_z=K B_b+max(1,T/mu),
C_H=max(1,||d||_1+||c_0||_1 C_z),
q=P+1.
```

**Lemma 4 (explicit global modulus).** For `x,x' in X'` and `h=||x-x'||_infinity`,

```
||z(x)-z(x')||_infinity <= C_z h^(1/q),
|H(x)-H(x')| <= C_H h^(1/q).                            (15)
```

**Proof.** Assume `h>0`; all leaders lie in the unit cube so `h<=1`. Repair `z(x')` into a feasible point `y` for the follower at `x` with distance at most `K B_b h`. Similarly repair `z(x)` into a feasible point `w` at `x'` with the same bound. Both points remain in the follower cube. Write `F_x` for the follower objective. Its uniform infinity-norm Lipschitz bound is `L`. Optimality of `z(x')` at `x'` gives

```
F_x(y)-F_x(z(x))
 <= L K B_b h + F_x(z(x'))-F_x(z(x))
 <= 2 L K B_b h + |(ell(x)-ell(x'))^T(z(x')-z(x))|
 <= T h.
```

The second inequality uses `F_x'(z(x'))<=F_x'(w)` and `|F_x'(w)-F_x'(z(x))|<=L K B_b h`. The coordinatewise difference of the two responses is at most one, which bounds the displayed dot product by `B_ell h`. The existing uniform convexity inequality and first-order optimality at `z(x)` imply `mu ||y-z(x)||_infinity^q<=T h`. Hence

```
||z(x')-z(x)||_infinity
 <= K B_b h+(T/mu)^(1/q) h^(1/q)
 <= C_z h^(1/q).
```

The second claim follows by the affine upper objective and `h<=h^(1/q)`. QED.

**Corollary 5.** Suppose each reduced `f_j` is convex on `X'` and a point `x_s in X'` satisfies `f_j(x_s)<=-sigma` for a supplied rational `sigma>0`. Then Corollary 3 applies with `D=C_H` and `q=P+1`.

**Proof.** For an original optimizer `x*`, set `x_t=(1-t/sigma)x*+(t/sigma)x_s`. Convexity of `X'` and the reduced constraints gives `f_j(x_t)<=-t` for `0<=t<=sigma`. Its distance from `x*` is at most `t/sigma`, so (15) yields (M). QED.

The anchor may be supplied with an analytic certificate; verifying its exact response margin is not silently assumed easy. The algorithm itself uses the promised `sigma` and does not need to evaluate the anchor's follower response exactly.

A concrete subclass has no shared resource rows, convex increasing marginals `g_i` with `g_i(0)=0`, and affine incentives `ell_i(x)>=0` throughout `X`. Then `z_i(x)=min(1,g_i^(-1)(ell_i(x)))` is concave: the inverse is increasing concave on its domain, and extending it by the constant one preserves concavity. Thus every upper constraint `a_j0+a_j^T x-sum_i w_ji z_i(x)<=0` with `w_ji>=0` is convex. These include minimum weighted production/service constraints. A signed affine objective can remain nonconvex. The condition `ell_i>=0` matters: clipping a negative affine incentive to zero generally destroys concavity. This subclass is an illustration, not an assertion for shared resources.

## 7. Concrete condition B: reserve decisions with uniform headroom

Write the leader as `(u,s)` with rational polytope `U` for `u` and a fixed-dimensional rational reserve polytope `S subset [0,1]^p`; assume `X=U times S`. Let follower costs and resource right-hand sides depend only on `u`, so the follower-feasible leader set is `U' times S` and the response is `z(u)`. Let

```
f_j(u,s)=a_j0+a_j^T u+c_j^T z(u)-R_j s,
H(u,s)=h(u)+w^T s.
```

The matrix `R` need not have a particular sign. Assume there exists `s_safe in S` and a supplied rational `sigma>0` such that

```
f_j(u,s_safe)<=-sigma  for every u in U' and every j.     (16)
```

This is uniform headroom at the safe reserve choice. A readily checkable sufficient certificate is the stronger affine bound over the explicit rational polytope `U' times [0,1]^N`:

```
a_j0+a_j^T u+c_j^T z-R_j s_safe<=-sigma.
```

It can be checked by rational LP, and is conservative because it ignores follower response structure.

**Corollary 6.** If `U'` is nonempty and (16) holds, Corollary 3 applies with `q=1` and `D=max(1,||w||_1)`. Thus exact rational upper feasibility and global additive optimization are polynomial in accuracy bits, without convexity of the reduced upper constraints or a lower curvature bound.

**Proof.** Keep the incentive `u*` of an original optimum and move its reserve to

```
s_t=(1-t/sigma)s*+(t/sigma)s_safe.
```

The follower response is unchanged. Affinity in `s` and (16) give `f_j(u*,s_t)<=-t`. The upper objective increases by at most `||w||_1 t/sigma` because both reserve vectors lie in the unit cube. This proves (M). QED.

Reserve must be a real modeled control, such as external procurement or certified offsets. Adding an artificial slack to an existing hard constraint changes the original model and is not justified by this result. Uniform headroom is substantive: it rules out capacities exhausted at some leader choices. The safe reserve needs not be an optimal reserve, and reserve dimension counts toward the fixed leader dimension.

## 8. Necessary cautions and useful negative examples

### 8.1 A strict feasible point alone does not justify inner convergence

Let `x,z in [0,1]`, with no resources, and follower marginal

```
g(z)=z+z^2(z-1/2),
F_x(z)=z^2/2+z^4/4-z^3/6-xz.
```

It is strongly convex because

```
g'(z)=1+3z^2-z=3(z-1/6)^2+11/12>=11/12.
```

The response is the unique inverse `z(x)=g^(-1)(x)` since `g(0)=0`, `g(1)=3/2` and `x in [0,1]`. Impose the one affine upper inequality `z(x)-x<=0` and minimize `x`. Since `g` is increasing,

```
z(x)<=x iff x<=g(x) iff x^2(x-1/2)>=0.
```

The upper feasible leaders are exactly `{0} union [1/2,1]`. The optimum is zero; `x=1` is strictly feasible. Yet every positively tightened feasible leader has `x>1/2`, so `V(t)>1/2` whenever finite, and `lim_(t down to 0) V(t)=1/2`. The limit follows from continuity and strict feasibility for every `x>1/2`. There is no modulus (M) around the original optimum. This defeats a generic global-Slater-only argument even with uniformly strong follower curvature and one scalar leader/follower.

### 8.2 Exact rational feasible output can be impossible

Let the follower minimize `z^3/3-xz` on `[0,1]`, with `x in [0,1]`, so `z(x)=sqrt(x)`. Impose the affine upper equality `z-x=1/8`, represented by two inequalities. Then

```
x=(x+1/8)^2,
x=3/8 plus or minus sqrt(2)/4.
```

Both roots lie in `[0,1]` and satisfy the original unsquared equality; both are irrational. The upper problem is feasible but has no rational feasible leader. Strictly increasing polynomial marginals alone therefore cannot yield unrestricted exact rational upper-feasible output.

### 8.3 Exact feasibility decision remains an arithmetic issue

The existing [aggregate-response result, Section 6](bilevel-fixed-aggregate-response-algorithm.md) embeds sum-of-square-roots comparison using independent cubic local costs and one upper inequality. This note does not bypass that exact decision problem: Theorem 1 permits small violation, and Corollaries 3, 5 and 6 have margin promises. Empty inner surrogates are not certificates of original infeasibility.

## 9. Literature and contribution boundary

Sources were inspected on 2026-09-06. No matching combined fixed-dimension polynomial accuracy-bit theorem was located in the inspected open primary sources. This is a limited search conclusion, not proof of priority.

- [Besançon, Anjos and Brotcorne, Robust bilevel optimization for near-optimal lower-level solutions, JGO 2024, open published paper](https://publications.polymtl.ca/65063/1/2024_Besancon_Robust_Bilevel_Optimization_Near-optimal_Lower-level.pdf). Proposition 4 and Corollary 1 on published pages 822–823 use upper-constraint Lipschitz bounds to turn response distance and strict margins into feasibility for near-optimal lower-level responses. This directly precedes the safety-margin principle used here. Their robust model concerns allowed lower-level suboptimality; this note uses numerical approximation of the unique exact response and establishes conditional global bit complexity. No novelty is claimed for margin conversion.
- [Boyd and Vandenberghe, Convex Optimization, open author PDF](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf), Section 5.6, establishes the standard perturbation-value viewpoint for tightened and relaxed inequalities. Convex interpolation toward a strict point is likewise standard. Our use permits a nonconvex reduced objective and obtains its effective modulus from the existing separable polynomial response bound.
- [Cesaroni, Liuzzi and Lucidi, Derivative-Free Bilevel Optimization with Inexact Lower-Level Solutions, arXiv 2603.20759](https://arxiv.org/abs/2603.20759) studies adaptive lower-level accuracy and stationary-point convergence, including general constraints through penalties. Its abstract was checked; no detailed theorem comparison is asserted. The present target is global optimization with polynomial dependence on binary accuracy in a restricted structural model.

The candidate paper addition is Theorems 1–2 and Corollaries 3, 5–6 as a carefully qualified extension of the existing accuracy-bit theorem, plus the explicit limitations in Section 8. It is not a standalone new theory of robust feasibility. The reserve case is particularly simple to explain and provides an exactly safe planning output for a practically relevant subclass.

## 10. Verification record

[Exact diagnostic script](../code/bilevel_reopened/response_constraints_checks.py) covers the strongly convex disconnected-feasibility example, the irrational feasible-set example, reserve interpolation margins, all response/rounding error-ledger inequalities on a rational grid, and separate polynomial upper-function Lipschitz bounds on the enlarged response box. The current run passes 4,553 exact cases. It supplements the proofs and does not implement the quantifier-elimination optimizer. The [independent full review](../notes/review-bilevel-reopened-response-constraints.md) passed all Sections 1–12. Its [separate exact checker](../code/bilevel_reopened/response_constraints_review.py) passed 10,091 cases, including 2,500 polynomial-upper enlarged-box checks. The diagnostic counts are finite checks, not a substitute for the general proofs.

## 11. Composition with convex aggregate coupling

This section uses the separately and doubly reviewed [convex aggregate theorem](bilevel-convex-aggregate-accuracy-bit-algorithm.md). It records the additional upper-constraint argument explicitly; the nonlinear branch cells make a direct appeal to Section 3's rational-cell interface invalid.

Use that theorem's fixed aggregate dimension and convex polynomial aggregate cost `phi(x,Uz)`. Its algebraic candidate winner `v*` lies in valid inverse branches, with `||p(v*)-q(v*)||inf<=eta`. Its rational recovery preserves the enclosing rational polytope, and may cross nonlinear branch boundaries. The proved bounds are

```
||xhat-x*||inf<=h,
||q(vhat)-q(v*)||inf<=eta,
||q(vhat)-z(xhat)||inf<=tau.
```

Here `x*` denotes the leader component of the algebraic candidate, not necessarily an optimum of the true constrained problem. Consequently, for each affine upper polynomial `F_j(v*)`,

```
|f_j(xhat)-F_j(v*)|
 <=||a_j||_1 h+||c_j||_1(2eta+tau).                       (17)
```

The same formula holds for the upper objective. This compares to the polynomial at its valid algebraic argument. It does not evaluate that branch polynomial at an invalid rounded point.

To obtain outer and inner guarantees with tolerances `epsilon,delta`, put

```
A=max(1,||d||_1,||c_0||_1,max_j ||a_j||_1,max_j ||c_j||_1),
kappa=min(1/4,epsilon/(16A),delta/(16A)).
```

In the aggregate theorem choose target response error `tau<=kappa`, inverse tolerance `eta<=kappa`, and recovery distance `h<=kappa`, in addition to its existing sufficient inequalities. These choices have polynomial logarithmic precision. Equation (17) is then at most `min(epsilon,delta)/4` for every row including the objective.

For the outer construction impose `F_j(v*)<=||c_j||_1 eta`; every true feasible optimum still has an admissible lift, and the final true constraint violation is at most `delta/16+delta/4`. Objective loss is at most `epsilon/16+epsilon/4`. For the inner construction impose `F_j(v*)<=-delta/2`; every leader feasible for `V(delta)` still has an admissible lift, and the final true constraints are at most `-delta/4`. The same objective comparison holds with `V(delta)`.

Therefore Theorems 1–2 and the tightening-modulus Corollary 3 transfer to the convex aggregate model, conditional on that theorem. Upper-constraint count remains unrestricted. The posterior interval also transfers: approximate each algebraic surrogate winner value by a rational number within a chosen `omega`; subtract `omega+||c_0||_1 eta` for the outer lower bound, and add `omega` plus the objective bound (17) for the inner upper bound.

The reserve Corollary 6 transfers when the complete follower objective, including `phi`, and its constraints are independent of the reserve coordinates. The convex reduced-constraint Corollary 5 transfers using the aggregate theorem's global response modulus. Explicitly, let `T_x` be a polynomial-bit rational constant with

```
|F_x(z)-F_x'(z)|<=T_x ||x-x'||inf
```

uniformly for `z` in the follower cube. Absolute coefficient sums after normalizing `Uz` provide such a bound. The two-repair proof gives

```
||z(x)-z(x')||inf
 <=K B_b h+[2(T_x+L K B_b)h/mu]^(1/(P+1)).
```

One may use the rational overestimate
`C_z=K B_b+max(1,2(T_x+L K B_b)/mu)` in (15). No uniform positive curvature of the aggregate is required. The example of concave independent responses in Section 6 remains an example for the independent subclass only; aggregate convexity does not imply convexity of the reduced upper constraints.


## 12. Polynomial upper objectives and performance inequalities

The affine upper restriction can be removed without increasing the compressed optimization dimension. This extension includes tariff revenue, interactions between output measures, and polynomial performance requirements. It changes neither the follower model nor the exact-feasibility qualifications.

Let the upper objective `H(x,z)` and upper constraints `G_j(x,z)<=0` be rational polynomials supplied as explicit monomial lists (dense encoding is also allowed). Let `D_up` be their maximum numerical total degree. Running time is polynomial in their input lengths and numerical `D_up`, as well as the original parameters. This is not a polynomial-time guarantee in sparse binary exponent lengths alone.

For any such polynomial write

```
G(x,z)=sum_(alpha,beta) a_(alpha,beta) x^alpha z^beta.
```

Define rational constants

```
L_x(G)=sum |a_(alpha,beta)| |alpha|_1 2^(|beta|_1),
L_z(G)=sum |a_(alpha,beta)| |beta|_1 2^(|beta|_1).
```

They bound its separate infinity-norm Lipschitz constants in `x` and `z` on
`[0,1]^r times [-1,2]^N`, by bounding and summing the absolute first partial derivatives. They can be zero for a constant or an absent group of variables. Their encoding lengths are polynomial in the explicit input and numerical `D_up`. The enlarged response box is necessary because inverse polynomials can slightly leave `[0,1]`.

**Corollary 7 (polynomial upper data).** Theorems 1–2 and Corollary 3 hold with these polynomial upper functions, with the stated additional numerical-degree dependence. Corollary 5 holds when the reduced polynomial constraints `G_j(x,z(x))` are convex and have the stated strict anchor. The same claims transfer to the convex aggregate model under Section 11's dependency.

**Proof of complexity.** On each candidate set substitute `z_i=p_i(v)` into every explicitly listed upper monomial and expand in the fixed-dimensional variable `v`. If the inverse polynomials have degree at most `d_p`, each resulting upper polynomial has degree at most `D_up max(1,d_p)`. In fixed dimension the number of possible monomials is polynomial in that degree. Repeated multiplication and addition form the expansion in polynomial time, with coefficient bit length polynomial in `D_up`, input coefficient lengths, and the existing inverse coefficient lengths. This does not introduce `N` new optimization variables. Both the upper-polynomial count and their explicitly listed terms remain part of the ordinary input size.

**Proof of error and recovery bounds.** On every valid candidate, `p` lies in `[-1,2]^N` since its uniform inverse error is at most `1/4`. In the resource-only model the same holds at rational recovery, which preserves its rational branch cell. Replace `A_j` everywhere in Sections 3–5 by `L_z(G_j)`, and replace `A_0` by `L_z(H)`. The polynomial rounding arguments are already valid for any finite list of polynomials. Thus the same outer and inner error ledgers apply without change. When the number of response variables is zero, the response errors vanish and only fixed-dimensional algebraic optimization and rational recovery with upper margins are needed.

For the convex-anchor modulus use

```
C_H=max(1,L_x(H)+L_z(H) C_z).
```

The proof is the triangle inequality between `H(x,z(x))`, `H(x',z(x))`, and `H(x',z(x'))`, followed by the response modulus. No convexity of `H` is required.

For aggregate recovery, replace (17) by

```
|G_j(xhat,z(xhat))-G_j(x*,p(v*))|
 <=L_x(G_j) h+L_z(G_j)(2eta+tau).                         (18)
```

The same formula holds for `H`. Both response endpoints lie in `[-1,2]^N`; the mean-value bound applies even though the branch polynomial is not evaluated at `vhat`. Set `A` in Section 11 to the maximum of one and all `L_x,L_z` constants. Its `kappa` ledger then transfers word for word. True lifts have upper-function error at most `L_z eta`. Posterior interval constants use the same replacements. QED.

In particular, with no response-dependent upper constraints, any polynomial upper objective has the original global additive accuracy-bit guarantee without a tightening assumption. The recovered leader stays exactly in `X'`. For example, `H(x,z)=-sum_i x_1 z_i+d(x)` minimizes negative tariff revenue plus a polynomial intervention cost; bilinear revenue is explicitly covered. The theorem does not assert concavity of revenue.

The reserve condition also has a polynomial version. Keep reserve coordinates absent from the complete follower model. Suppose `G_j(u,s,z(u))` is convex as a function of `s` on `S` for each `u`, and the same uniform safe reserve margin holds. Let `L_s(H)` bound the reserve-coordinate infinity-norm Lipschitz constant of `H` on the leader and follower cubes; the displayed coefficient formula, restricted to reserve exponents, supplies one. Interpolation toward the safe reserve gives margin `t` by convexity and increases the objective by at most `L_s(H)t/sigma`. Thus Corollary 6 holds with modulus coefficient `max(1,L_s(H))` in (M) and tightening exponent `q=1`. These convexity and safe-margin conditions are promises or separately certified structure; polynomial follower convexity does not imply them.

An upper polynomial equality is still not generally compatible with positive tightening. Polynomial upper data do not remove the irrational-output or arithmetic obstacles, and exact feasible output is claimed only with the same stated margins. This is a closure corollary of the surrogate construction, not a separate claim of a new polynomial approximation technique.
