# Second independent audit of convex polynomial performance design

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS.** The [candidate](potential-flow-convex-polynomial-design.md) correctly replaces the convex quadratic surrogate objective by a densely encoded rational polynomial promised convex on the expanded flow box. The perspective construction gives a globally convex Lipschitz extension with polynomial-bit rational oracles. It preserves the previously proved exact capacity recovery and additive objective guarantee. Global convexity of the original polynomial is unnecessary.

## 1. Bounds, rescaling, and encoding

For `S=B+1>=1`, the displayed coefficient absolute sums bound the polynomial value and every partial derivative on `[-S,S]^m`. Omitting zero derivative terms avoids a meaningless negative exponent from a constant monomial. These bounds have polynomial bit length: the numerical degree is bounded by dense input length, powers of S have bit length growing linearly with their exponents, and there are only as many terms as supplied by the input.

All retained singleton intervals, as well as frozen coordinates, are removed before normalization. Each remaining rational interval has positive width and is an affine image of `[-1,1]`. Its endpoints, midpoint, and half-width have polynomial rational encoding even when its width is very small. There is no numerical condition-number assumption.

The full affine map `x=Tz+a` from the free cube produces only surrogate flows in the expanded flow box. Convexity of f on that box therefore implies convexity of h on the cube. The chain rule bounds each derivative of h by Gf times the corresponding column l1 norm of T. Thus V and G are valid rational bounds of polynomial bit length. Composition can be evaluated without expanding its multivariate coefficient list, so no hidden combinatorial expansion is needed.

## 2. Convex perspective extension

Regard h as a convex function on the closed cube with value positive infinity outside. Its perspective is convex on `t>0, |z_i|<=t`. Adding `M(t-1)` and restricting to `t>=1` gives a jointly convex function over a convex domain. The classical perspective and partial-minimization facts apply to this extended-value formulation. I checked the cited primary textbook passages, Sections 3.2.5–3.2.6, including printed page 89. [Boyd and Vandenberghe, Convex Optimization](https://www.seas.ucla.edu/~vandenbe/cvxbook/bv_cvxbook.pdf).

For fixed z, every feasible t gives `w=z/t` in the cube. The ordinary polynomial derivative is

```
partial_t [t h(z/t)+M(t-1)]
=h(w)-grad h(w)^T w+M
>=-V-kG+(1+V+kG)=1.
```

At the boundary of the feasible t ray, the same one-sided inequality suffices. The objective is strictly increasing along this ray, so its partial minimum is attained at the smallest feasible t, exactly `max(1,||z||_infinity)`. This proves the displayed explicit H is globally convex. Within the cube t equals one, so H agrees with h without any additive offset. Negative polynomial values and negative affine terms introduce no exception.

## 3. Support inequalities and global Lipschitz continuity

The polynomial gradient at a boundary point of the cube is still a supporting gradient for the restricted convex h: its supporting inequality holds for every other point of the cube. Multiplying that inequality by a positive perspective coordinate shows directly that the joint perspective has supporting coefficients `(grad h(w),K(w))`, where

```
K(w)=h(w)-grad h(w)^T w+M,
1<=K(w)<=1+2(V+kG).
```

Apply this joint inequality to `(z,t(z))` and `(z',t(z'))`. For any subgradient tau of the convex function t, its support inequality gives `t(z')-t(z)>=tau^T(z'-z)`. The positive coefficient K permits substitution with the correct inequality direction. Thus

```
s(z)=grad h(w)+K(w)tau
```

is a subgradient of H at every z. There is no unsupported differentiability claim for the maximum norm. Inside the cube tau zero works; outside use a signed maximizing coordinate vector; on the boundary or at ties any convex combination of the active vectors, including the constant branch where active, works. In all cases its infinity norm is at most one.

Consequently the displayed C bounds the infinity norm of an available subgradient at each point. Applying its support inequality first at z and then at z' gives both sides of

```
|H(z)-H(z')|<=C||z-z'||_1<=kC||z-z'||_2.
```

The second bound is conservative and valid for k at least one. The dimension-zero case was already removed. This argument covers lines wholly inside a tie set or on the cube boundary and therefore proves global Lipschitz continuity without an almost-everywhere differentiation argument.

## 4. Rational oracle and convex optimizer

At a rational query z, computing its maximum absolute coordinate, t, w, the affine flow coordinates, f and its gradient, and the displayed H and subgradient requires polynomially many rational operations. Denominator growth under powers is bounded by the dense numerical degree times the current rational bit length. Sum and product sizes are polynomial in the input and query encoding lengths. This proves the exact rational oracle property, not merely real-arithmetic evaluability.

The cube has an exact rational membership oracle, unit Euclidean inner radius, and outer radius at most k. H is globally convex and has the explicit rational Euclidean Lipschitz upper bound kC. These are precisely the hypotheses of Dadush's Theorem 2.5.9 already directly checked in the [original second convex-design audit](review-potential-flow-cactus-convex-design-second.md). That theorem returns a rational point inside the cube with additive objective error epsilon/2 in polynomial bit time. H=h on the cube, so the returned point optimizes the required surrogate objective to the same accuracy. No approximate cube-feasibility correction is being assumed.

## 5. Physical recovery, error budget, and scope

Only optimization over the rational surrogate changes. The underlying exact-capacity algorithm still realizes each retained rational circulation exactly by rational admissible parameters and each frozen coordinate by its stored exactly feasible endpoint or narrow-interval scenario. Its final physical state therefore satisfies every allowed capacity exactly.

With the correlated-cycle projection bound, total flow error in the comparisons is at most `3m eta` before optimization and `m eta` after recovery. All comparison segments remain in the expanded box, on which the gradient bound Gf applies. Thus the total loss is at most

```
4mGf eta+epsilon/2<=3epsilon/4<epsilon.
```

The interval-only method has a smaller projection constant and satisfies the same conservative bound. A zero-flow instance or an edgeless graph is handled directly before dividing by m. Exact final flow constraints do not depend on the objective being quadratic.

The same objective replacement also applies to the separately reviewed [correlated polynomial-law cycle design](review-potential-flow-correlated-polynomial-cycle-design-second.md): it supplies the identical rational surrogate, exact parameter recovery, and flow-error properties. This is a direct composition of the two proofs and does not require new constitutive regularity.

Independently inspected and reran `code/potential_flow_mpd/convex_polynomial_extension_checks.py`. It passed 1,600 exact rational Jensen, Lipschitz, and cube-agreement checks on 20 polynomials, including quartics convex on the cube but not globally. The first reviewer additionally supplied separate exact support checks. These diagnostics supplement the proof and do not purport to implement the imported convex optimizer.

Dense encoding and convexity on the expanded box remain explicit assumptions. Convexity validation, sparse binary exponents, correlations or constraints coupling cycle feasibility, and variable nominations are not inferred. The perspective operation and general convex optimizer are established tools; this audit makes no new priority claim. No correction is required.
