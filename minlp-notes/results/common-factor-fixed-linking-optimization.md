# Common-factor optimization with a fixed number of linking constraints

Status: mathematically proved and independently audited on 2026-09-04, including integer and signed common factors. Computational checks cover the fixed-total specialization. Publication novelty is **not established**: a targeted search found a close existing bounded-LP basis-enumeration method, though no exact match to the moving-matrix/moving-product-bound theorem below. The result is a structural tractability theorem, not a claim of a compact conic hull.

Independent audit: [common-factor audit](../notes/review-common-factor.md), Section 1, including its follow-up audit paragraph on the integer and signed corollaries. Broader investigation: [common-factor investigation](../notes/common-factor-investigation.md).

## Model and result

Let all data be rational. Fix a nonnegative integer `k`. Consider the compact set

```
S = { (x,y,w): a <= x <= b, l_j <= y_j <= u_j,
                 p_j <= w_j <= q_j, w_j = x y_j (j=1,...,n),
                 A y + B w <= c + d x },                 (1)
```

where `0 < a <= b`, `l,u,p,q` are finite, and the last system has `k` rows. No sign restriction on the leaf variables or product bounds is needed. Linear equalities can be entered as two inequalities. The scalar has a positive lower bound; the theorem as written does not cover zero or sign-changing scalar intervals.

**Theorem 1.** For each fixed `k`, linear optimization over `S` is polynomial in the rational input bit length. An optimizer can be returned using real algebraic numbers of degree bounded by a function of `k`. The algorithm enumerates `binomial(n+k,k)` conditional LP bases and polynomially many univariate sign intervals for each basis. Therefore it also supplies an exact linear-optimization oracle for `conv(S)`.

This is an XP result in `k`; it is not a fixed-parameter tractability claim. It does not assert a polynomial-size conic formulation.

**Corollary 1a (integer common factor).** The same polynomial-time conclusion holds if `x` is additionally required to be an integer, even when `[a,b]` contains exponentially many integers. The bound on the number of linking rows is unchanged, and all leaves remain continuous.

To see this, partition every feasible rational-function piece at its derivative roots. The objective is monotone or constant on each resulting interval. Among the integers in that interval it attains its optimum at the smallest or largest integer, so evaluating the adjacent feasible integers around every endpoint and stationary point suffices. For an open interval `(s,t)`, these integers are `floor(s)+1` and `ceil(t)-1`, provided they belong to the interval; scalar endpoints that are themselves integers are evaluated separately. Floors and ceilings of bounded-degree real algebraic numbers can be computed in polynomial bit complexity. At an integer scalar value the conditional LP has rational data and admits a rational optimal vertex. This is a mixed-integer result; it does not require enumeration of all multiplicities in a large interval.

**Corollary 1b (signed common factor).** Theorem 1 and corollary 1a extend to any finite rational interval `a<=x<=b`, including zero and sign changes. Split the interval at zero. On a negative branch set `X=-x`, `w'=-w`, with product bounds `[-q,-p]`, linking coefficients `B'=-B`, `d'=-d`, and objective coefficients `alpha'=-alpha`, `gamma'=-gamma`. On a positive branch whose left endpoint is zero, use the same rational formulas on the open interval and process zero separately. Feasible formula coordinates remain bounded by the original leaf/slack boxes; any finite one-sided limit at zero belongs to the original compact set. The direct LP at `x=0` also captures isolated feasible zero points. Thus the positive lower bound is a convenience of the main proof, not a complexity boundary.

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

## Literature comparison and novelty limits

Punnen, Sripratak, and Karapetyan, *The bipartite unconstrained 0–1 quadratic programming problem: Polynomially solvable cases* (2015), prove polynomial solvability for fixed-rank objective matrices. Their section 3.2, especially Lemma 1 and its proof (preprint PDF pages 9–10), already enumerates bounded-variable LP bases with a fixed number of rows, uses cost perturbation to orient nonbasic bounds uniquely, and bounds the number of characteristic-region vertices. [Open author manuscript](https://repository.essex.ac.uk/22056/1/1212.3736v3.pdf).

The basic enumeration and perturbation idea is therefore established. The theorem here extends that mechanism to a scalar-dependent matrix `A+xB`, reciprocal bounds induced by simultaneously bounded products, and an integer common factor. The cited paper treats a fixed LP matrix and a Cartesian-box bilinear objective problem. Whether the extension is independently publishable remains unresolved; the current search did not locate an exact earlier theorem covering all these features.

The conference work by Oh, Wiecek, and Yang, *Convexification of a Class of Bilinearly Constrained Sets Sharing a Common Variable*, also directly overlaps the uncoupled common-variable direction. Its 2026 abstract announces extreme-point/facet descriptions and separation for common-variable bilinear inequalities with box constraints. The full theorem was not available in the search. [SIAM Optimization 2026 abstracts](https://www.siam.org/media/r0be0xtr/op26_abstracts_v3.pdf).

The targeted novelty pass used combinations of “bilinear programming,” “fixed rank,” “fixed number of constraints,” “common variable,” “parametric linear programming,” and “bounded variables,” and read the relevant primary fixed-rank argument. This is evidence for cautious positioning, not proof of novelty.

## Computational check of the fixed-total specialization

`code/common-factor-verify.py` implements the fixed-total variant `sum y_j=D`. It forms rational bound and cost-order breakpoints, solves each continuous-knapsack piece, and minimizes its `A x+B+C/x` value using endpoints and square-root stationary points. It evaluates conditional LPs at all endpoints separately, so an isolated feasible scalar is not discarded. The partition and coefficients use exact `Fraction` arithmetic; stationary-point evaluation is floating point.

On 2026-09-04, the script passed 200 seeded comparisons with Gurobi 13's independent global nonconvex solver, with `n=1,...,8`, mixed-sign leaf and product bounds, random signed objectives, and tied zero objectives. It also passed a regression whose only feasible scalar is `x=2`. Objective comparisons use a relative/absolute tolerance of `2e-6`; this is numerical corroboration, not a proof or an implementation of the general exact-bit theorem.

Command:

```
/home/sgusev/miniconda3/envs/minlp-notes/bin/python code/common-factor-verify.py
```

Observed output:

```
Passed 200 seeded mixed-sign balanced-star comparisons against global Gurobi.
Passed isolated feasible scalar regression x=2.
This is numerical corroboration of the fixed-total specialization; it is not a proof.
```
