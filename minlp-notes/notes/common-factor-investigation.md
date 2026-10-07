# Common-factor products with linking constraints

Status: theorem 1 and lemma 2 passed an independent mathematical audit; see [the audit](review-common-factor.md). No claim of publication novelty. The unrestricted local common-variable convexification direction has a direct 2026 conference overlap described below. Additional exact small-block hull results discovered during the audit appear there with their own review status.

## 1. Fixed linking-row algorithm

Let all data be rational. Fix a nonnegative integer `k`. Consider the compact set

```
S = { (x,y,w): a <= x <= b, l_j <= y_j <= u_j,
                 p_j <= w_j <= q_j, w_j = x y_j (j=1,...,n),
                 A y + B w <= c + d x },                 (1)
```

where `0 < a <= b`, `l,u,p,q` are finite, and the last system has `k` rows. No sign restriction on the leaf variables or product bounds is needed. Linear equalities can be entered as two inequalities. The scalar has a positive lower bound; the theorem as written does not cover zero or sign-changing scalar intervals.

**Candidate theorem 1.** For each fixed `k`, linear optimization over `S` is polynomial in the rational input bit length. An optimizer can be returned using real algebraic numbers of degree bounded by a function of `k`. The algorithm enumerates `binomial(n+k,k)` conditional LP bases and polynomially many univariate sign intervals for each basis. Therefore it also supplies an exact linear-optimization oracle for `conv(S)`.

This is an XP result in `k`; it is not a fixed-parameter tractability claim. It does not assert a polynomial-size conic formulation.

**Candidate corollary 1a (integer common factor).** The same polynomial-time conclusion holds if `x` is additionally required to be an integer, even when `[a,b]` contains exponentially many integers. The bound on the number of linking rows is unchanged, and all leaves remain continuous.

To see this, partition every feasible rational-function piece at its derivative roots. The objective is monotone or constant on each resulting interval. Among the integers in that interval it attains its optimum at the smallest or largest integer, so evaluating the adjacent feasible integers around every endpoint and stationary point suffices. For an open interval `(s,t)`, these integers are `floor(s)+1` and `ceil(t)-1`, provided they belong to the interval; scalar endpoints that are themselves integers are evaluated separately. Floors and ceilings of bounded-degree real algebraic numbers can be computed in polynomial bit complexity. At an integer scalar value the conditional LP has rational data and admits a rational optimal vertex. This is a mixed-integer result; it does not require enumeration of all multiplicities in a large interval.

**Candidate corollary 1b (signed common factor).** Theorem 1 and corollary 1a extend to any finite rational interval `a<=x<=b`, including zero and sign changes. Split the interval at zero. On a negative branch set `X=-x`, `w'=-w`, with product bounds `[-q,-p]`, linking coefficients `B'=-B`, `d'=-d`, and objective coefficients `alpha'=-alpha`, `gamma'=-gamma`. On a positive branch whose left endpoint is zero, use the same rational formulas on the open interval and process zero separately. Feasible formula coordinates remain bounded by the original leaf/slack boxes; any finite one-sided limit at zero belongs to the original compact set. The direct LP at `x=0` also captures isolated feasible zero points. Thus the positive lower bound is a convenience of the main proof, not a complexity boundary.

### Proof

For fixed `x`, eliminate `w` and set

```
L_j(x) = max(l_j,p_j/x),    U_j(x) = min(u_j,q_j/x).
```

The remaining problem is an LP with `k` linking inequalities and interval bounds. A support objective has the form `alpha x + (beta+gamma x)^T y`.

Introduce `k` nonnegative slack variables. Each slack can be given a finite rational upper bound without excluding any feasible point: interval arithmetic bounds the expression `c_i+d_i x - sum_j (A_ij+B_ij x)y_j` on the original finite box. Increase the resulting upper bound to a positive number if necessary. Write the resulting equality system as

```
M(x) z = h(x),   L(x) <= z <= U(x),
M(x) = [A+xB, I_k],    h(x)=c+dx.                         (2)
```

There are `N=n+k` variables. `M(x)` has row rank `k` for every `x` because it contains the identity. Every bound function, on each of `O(n)` initial scalar intervals, has the form `r+s/x`. Initial interval endpoints include all crossings between a constant leaf bound and a reciprocal leaf bound, and all points at which `L_j=U_j`; infeasible initial intervals are discarded. Slack bounds are constant.

Degenerate costs require care. Use the lexicographic objective consisting of the original objective followed by `z_1,...,z_N`; equivalently use formal objective coefficients

```
C_j(x,epsilon) = C_j(x) + epsilon^j,
```

where `C_j` is affine for a leaf and zero for a slack. Formal signs mean the sign of the first nonzero coefficient as `epsilon` decreases to zero. This perturbation selects an original-objective minimizer. Its purpose is to orient nonbasic bounds even when an original reduced cost is identically zero.

Enumerate every `k`-column basis `J`. Discard bases whose determinant polynomial `D_J(x)` is identically zero. It has degree at most `k`. Outside its roots, define

```
lambda_J = M_J(x)^(-T) C_J(x,epsilon),
r_j = C_j(x,epsilon) - M_j(x)^T lambda_J,  j not in J.
```

After multiplication by `D_J`, each coefficient in `epsilon` is a polynomial in `x` of degree at most `k+1`. Each reduced cost has at most `k+2` potentially nonzero coefficients: the original cost coefficient and the perturbation indices in `J union {j}`. No nonbasic reduced cost is identically zero as a formal function: its own perturbation index has coefficient one before the basis correction, and that index does not occur in `C_J`.

Partition each initial scalar interval at the roots of the nonzero reduced-cost coefficient polynomials and the determinant. On any open resulting interval, all formal reduced-cost signs are constant. Choose

```
z_j(x)=L_j(x) if r_j>0, and z_j(x)=U_j(x) if r_j<0,
z_J(x)=M_J(x)^(-1)(h(x)-sum_{j not in J} M_j(x)z_j(x)).   (3)
```

All entries in (3) are rational functions. Their common denominator can be taken as `x D_J(x)`, of degree at most `k+1`, and each numerator has degree at most `k+1`. Partition further at roots expressing a basic variable meeting either of its bounds. Feasibility is constant on every remaining open interval and can be checked at one algebraic sample point. A feasible candidate is optimal for the original objective at every point of that interval: the identity

```
C^T(z'-z) = sum_{j not in J} r_j(z'_j-z_j)
```

proves optimality for the formally perturbed objective, hence its leading original coefficient cannot be negative.

Conversely, at every fixed scalar where the conditional LP is feasible, bounded-variable LP optimal-basis theory supplies a basis optimal for a sufficiently small lexicographic cost perturbation. Our enumeration includes it, and its nonbasic bound choices are exactly the signs in (3). Thus all scalar points outside the finite partition endpoint set are covered. This uses existence of a primal-dual optimal basis, not the false assertion that any arbitrary basis of an optimal vertex is dual feasible.

On each feasible open interval the original objective is `P(x)/(x D_J(x))` with numerator degree at most `k+2`. Its derivative numerator has degree at most `2k+2`. Isolate its roots and compare objective values at stationary points and one-sided endpoints. Every finite feasible endpoint limit gives a feasible point by compactness; coordinates in (3) are bounded on a feasible interval, so any apparent endpoint pole is removable there. In addition, solve the conditional LP directly at every partition endpoint, including endpoints where the determinant vanishes. This captures isolated feasible scalar points and endpoints of zero-length intervals.

For fixed `k` there are `O(N^k)` bases. Each has `O_k(N)` sign-changing polynomial roots before feasibility refinement and polynomially many after combining with the `O(n)` initial intervals. All relevant polynomial degrees are bounded in terms of `k`, and their rational coefficient bit lengths are polynomial in the input size. Standard exact univariate real-root isolation and rational-function evaluation at algebraic arguments therefore have polynomial bit complexity. Endpoint LPs can be solved by the same basis enumeration over the endpoint's fixed-degree algebraic field: evaluate reduced-cost signs, set nonbasic bounds, and test the basic solution. Some nonsingular basis always exists because of the slack identity columns. This avoids needing a separate general algebraic-input LP complexity theorem. Comparison of the polynomially many candidate values also has polynomial bit complexity: each candidate has bounded algebraic degree and polynomial coefficient height. This proves the claim. ∎

### Why the cost perturbation cannot be omitted

For `y_1+y_2=3/2`, `0<=y<=1`, and zero objective, every reduced cost vanishes. Choosing all nonbasic variables at their lower bounds makes each one-column basis infeasible, even though the LP is feasible. A generic or lexicographic perturbation is necessary for the basis enumeration proof.

### Special case: total-flow linking constraints

If the only coupling specifies bounds on `sum y_j` and `sum w_j`, fixing `x` gives a continuous knapsack. The marginal costs are `beta_j+gamma_j x`; partition at their pairwise order changes and their zero crossings, for `O(n^2)` initial points. All conditional capacity and saturation transitions are rational scalar points. On every final interval the value is `A x+B+C/x`; endpoints and square-root stationary points suffice. If the total is fixed, the cost-zero crossings can be omitted. This simpler special case should be preferred in implementations of balanced mixer blocks.

## 2. A reciprocal anchor transmits convexification across products

Take an anchor leaf with `w_0=p>0`, so `y_0=p/x`. In any convex combination of feasible points let `m=E[X]`, `t=E[1/X]=y_0/p`. Consider another leaf with `l<=Y<=u`, `y=E[Y]`, `w=E[XY]`. Set `r=(l+u)/2`, `h=(u-l)/2`. Assume `h>0`; a fixed leaf is linear and needs no cut.

**Candidate lemma 2.** The following affine `3 by 3` positive-semidefinite constraint is valid for the joint convex hull:

```
[ m,              1,                (w-r m)/h ]
[ 1,              t,                (y-r)/h   ] >=PSD 0.  (4)
[ (w-r m)/h,      (y-r)/h,           m         ]
```

Proof. Put `Z=(Y-r)/h`, so `|Z|<=1`. The expectation of the outer product of `(sqrt(X),1/sqrt(X),sqrt(X)Z)` is positive semidefinite and agrees with (4) except for its last diagonal entry, which is `E[X Z^2]<=E[X]=m`. Adding the nonnegative difference to that diagonal preserves positive semidefiniteness. ∎

For every real fixed `s`, (4) implies the rotated-SOC cut

```
[w-rm-s(y-r)]^2 <= h^2 m [m-2s+s^2 t].                 (5)
```

The converse follows by the Schur complement with respect to the last diagonal `m>0`: checking (5) for every `s`, including its limiting leading coefficient, tests the remaining two-dimensional quadratic form. Thus (4) packages an infinite one-parameter family of SOC cuts.

These cuts propagate a tight anchor across all other products. If `m t=1`, the leading `2 by 2` block of (4) is singular, and positive semidefiniteness forces `w=m y`. The same conclusion follows from strict Jensen equality: the anchor then forces `X` to be constant in every representing convex combination.

### Minimal failure of intersecting individual bounded-product hulls

Let `x in [1,2]`, `y_0=1/x`, `w_0=1`, and let `y_1 in [0,1]`, `w_1=x y_1`. The point

```
x=3/2, y_0=2/3, w_0=1, y_1=1/2, w_1=1
```

belongs to each individual product hull: the anchor is an actual point, and the second triple is the midpoint of `(1,0,0)` and `(2,1,2)`. It is outside the joint hull since `x y_0=1` forces `X=3/2` almost surely, hence `w_1=(3/2)(1/2)=3/4`. Constraint (4), or (5) with `s=3/2`, excludes it. This does not contradict forest exactness of McCormick on a Cartesian box; the anchor product equality changes the domain.

No claim is made that (4), together with the individual hulls, completely describes the joint hull. It is a moment-derived strengthening, and its novelty relative to rational-function moment relaxations remains unverified.

The independent audit produced a [separate hull result](../results/common-factor-reciprocal-anchor-hulls.md): (4), the reciprocal secant, and McCormick inequalities give the **exact hull for one unrestricted bounded leaf**; two rotated SOC constraints suffice in a lift. That note also gives a rational two-leaf counterexample showing that intersecting these exact anchor-leaf hulls is still insufficient. The exactness result does not permit additional product bounds or linking rows on that leaf without further convexification.

## 3. Literature and novelty audit (2026-09-04)

The fixed-linking theorem has been promoted to [its own result file](../results/common-factor-fixed-linking-optimization.md). Its dedicated novelty comparison identifies the bounded-LP basis enumeration and perturbation mechanism in Punnen, Sripratak, and Karapetyan (2015); those mechanisms are established, while the moving matrix/product bounds and integer scalar extension were not located in that source.

- Anstreicher, Burer, Park, *Convex hull representations for bounded products of variables*, JGO 80 (2021), 757–778, handles one bounded product with SOC descriptions. Open author manuscript: <https://sburer.github.io/papers/055-bounded-xyz.pdf>; arXiv <https://arxiv.org/abs/2004.07233>. This is the baseline, not a new result here.
- **Direct overlap warning:** Hyun-Ju Oh, Margaret Wiecek, Boshi Yang, *Convexification of a Class of Bilinearly Constrained Sets Sharing a Common Variable*, appears in the 2026 INFORMS Optimization Society program and SIAM Optimization 2026 abstracts. The abstracts announce a complete extreme-point/facet characterization and separation for box plus bilinear inequalities sharing one variable. Programs: <https://ios2026.isye.gatech.edu/sites/default/files/2026-03/program-book.pdf> and <https://www.siam.org/media/r0be0xtr/op26_abstracts_v3.pdf>. No full paper was found in the targeted search. Therefore the uncoupled-star direction is not a safe novelty claim.
- Baltean-Lugojan and Misener, *Piecewise parametric structure in the pooling problem: from sparse strongly-polynomial solutions to NP-hardness* (2018), uses concentration parameterization for pooling subclasses. Open full text: <https://pmc.ncbi.nlm.nih.gov/articles/PMC6417401/>. The methods are adjacent; a full theorem-by-theorem comparison remains needed before calling the linking-row result new.
- The local `results/rank-one-row-column-hardness.md`, Theorem 2, already has a fixed-number-of-rows algorithm for a different rank-one model. Candidate theorem 1 permits arbitrarily many bounded products and arbitrary fixed linking rows, including product-dependent rows. It should be positioned as a structural extension rather than a wholly new parametric technique.
- Targeted web queries for common-variable bilinear hulls, fixed linking constraints, fixed-constraint parametric LP, and continuous-knapsack bilinear optimization found no exact match for Candidate theorem 1. This search result is not proof of novelty.

## 4. Earlier follow-up list and final status

1. Completed: the one-leaf hull and two-leaf incompatibility passed the [root review](review-common-factor-root.md), in addition to the earlier review. The later full reciprocal-anchor hull has its own completed proof and audit.
2. Extend computational checking beyond the implemented fixed-total special case to arbitrary fixed linking rows.
3. Determine whether the fixed-linking-row theorem is already implicit in general low-rank bilinear or fixed-constraint parametric optimization results.
4. Check whether the reciprocal-anchor PSD cut has a pre-existing named formulation; study exact small-leaf hulls before proposing larger relaxations.

## 5. Computational check of the fixed-total specialization

`code/common-factor-verify.py` implements the fixed-total variant `sum y_j=D`. It forms rational bound and cost-order breakpoints, solves each continuous-knapsack piece, and minimizes its `A x+B+C/x` value using endpoints and square-root stationary points. It evaluates conditional LPs at all endpoints separately, so an isolated feasible scalar is not discarded. The partition and coefficients use exact `Fraction` arithmetic; stationary-point evaluation is floating point.

On 2026-09-04, the script passed 200 seeded comparisons with Gurobi 13's independent global nonconvex solver, with `n=1,...,8`, mixed-sign leaf and product bounds, random signed objectives, and tied zero objectives. It also passed a regression whose only feasible scalar is `x=2`. Objective comparisons use a relative/absolute tolerance of `2e-6`; this is numerical corroboration, not a proof or an implementation of the general exact-bit theorem.

Command:

```
/workspace/local-home/miniconda3/envs/minlp-notes/bin/python code/common-factor-verify.py
```

Observed output:

```
Passed 200 seeded mixed-sign balanced-star comparisons against global Gurobi.
Passed isolated feasible scalar regression x=2.
This is numerical corroboration of the fixed-total specialization; it is not a proof.
```
