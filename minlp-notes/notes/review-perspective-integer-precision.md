# Independent review: perspective transfer of integer precision

Date: 2026-09-05. Reviewer: `potential_flow_review`.

Reviewed candidate: [perspective-integer-precision-investigation.md](perspective-integer-precision-investigation.md).

**Verdict: PASS.** The binary formulation transfer is exact, and its upper error bound and affine-slice lower bound preserve the stated leading integer-dimension coefficient. The quadratic-over-linear consequences hold on both described domains. This review treats the separately reviewed quadratic noncommutative-rank theorem as an imported result; it does not repeat its proof or certify novelty of the perspective consequence.

Two small wording clarifications were sent to the author: the transformation adds `p` continuous **auxiliary** variables, and `p+1` continuous variables if the new input `t` is counted; preservation of rational coefficients assumes that the newly supplied bounds `ell,u` are rational too. Neither affects the theorem.

## Exact binary products

For each retained binary `z_i`, the four proposed inequalities impose `v'_i=t z_i` exactly. If `z_i=0`, the first pair forces `v'_i=0`, and the second pair follows from `ell<=t<=u`. If `z_i=1`, the second pair forces `v'_i=t`, and the first follows from the same bounds. There is no relaxation error in this step and no additional binary coordinate.

The positive lower bound on `t` is not needed merely for exact binary-product encoding, but it is needed for the subsequent division and the graph-equivalence statement as formulated. The finite upper bound is used both for the bounded binary-product construction and the uniform error conversion.

## Row homogenization and unbounded auxiliaries

Fix a feasible original point `(y,v,a,z)` and any admissible positive `t`. Set

```
x=t y, w=t v, a'=t a, v'=t z.
```

Multiplying each original linear inequality by positive `t` gives precisely the proposed homogenized row. Conversely, at every feasible transformed point the binary-product equations give `v'/t=z`; dividing each row by `t` recovers an original feasible point with `y=x/t`, `v=w/t`, and `a=a'/t`.

Thus the correspondence is exact for every fixed positive `t`. Continuous auxiliary variables need not be bounded: they are replaced by new independent continuous coordinates `a'`, and the inverse map is always available. No product envelope for `t a` is being asserted. Arbitrary signs, affine right-hand sides, and equalities represented by paired inequalities all behave correctly under positive scaling.

The argument preserves every original constraint, including domain constraints when these are explicitly included. If the original relaxation convention instead permits points outside `D` and measures error only over `D`, the same proof still works over `D_pers`: the recovered input is in `D` exactly when `(x,t)` is in the specified perspective domain. No off-domain error guarantee is required.

The row count grows by `4p+2`: four binary-product inequalities per integer coordinate and two bounds on `t`. The old continuous auxiliaries are replaced one for one, the input dimension increases by one, and there are `p` new product auxiliaries. If all old data and `ell,u` are rational, every new row has rational coefficients with polynomial encoding size. This algebraic preservation statement does not assert that an arbitrary real-coefficient quadratic upper construction can first be found with polynomial-bit rational data.

## Graph containment and upper error

For an exact perspective graph point, divide the input by `t`, select a feasible lift of the exact original graph point, and scale it. This proves containment for every point of the full perspective graph. At any admitted transformed point with `(x,t)` in the perspective domain, the recovered original point has componentwise error at most `delta`, so

```
|w_j-t F_j(x/t)|
= t |w_j/t-F_j(x/t)|
<= t delta <= u delta.
```

The bound is simultaneous for all output coordinates and uses the stated componentwise maximum-error metric. Taking base accuracy `delta=epsilon/u` therefore gives an admissible perspective relaxation of accuracy `epsilon` with exactly the same binary count.

The construction is specific to binary variables. It does not scale an unrestricted integer coordinate while preserving integer semantics; the candidate correctly excludes that inference.

## Affine-slice lower transfer

Restrict any perspective convex integer lift to a fixed `t=t0` in `[ell,u]`. Intersection with this affine equation preserves convexity and the integer-coordinate count, regardless of closedness or boundedness of the integer variables. The positive linear rescaling `(x,w)=(t0 y,t0 v)` then produces a graph-containing relaxation of `F`, with error `epsilon/t0`.

The same operation preserves polyhedrality for the binary-linear formulation class. Consequently both lower inequalities in the candidate are correct. Combining them with the binary upper transfer and the inclusion of binary linear lifts among convex integer lifts gives the complete sandwich needed for the asymptotic conclusion.

For fixed positive `u,t0`, replacing accuracy by `epsilon/u` or `epsilon/t0` changes `log2(1/epsilon)` by an additive constant. Thus matching base lower and binary upper laws with leading coefficient `c` imply the same coefficient for both perspective minima. The bounds and original map are fixed while accuracy decreases; no uniform statement for bounds changing with accuracy is inferred.

## Quadratic-over-linear systems

For every component,

```
t[(1/2)(x/t)^T H_j(x/t)+a_j^T(x/t)+b_j]
= (x^T H_j x)/(2t)+a_j^T x+b_j t.
```

The imported quadratic theorem applies to the original Hessian space on every full-dimensional bounded ratio box. Its noncommutative rank `r` determines the base leading coefficient `r/2`, so the transfer gives that same coefficient for the perspective system. The compact upper construction is preserved: the base binary count, row count, and variable count are logarithmic in reciprocal accuracy, and the extra count is linear in the binary count. If all Hessians vanish, the perspective is affine and requires no integers exactly.

On a ratio-box truncated cone, the domain is exactly described by

```
ell<=t<=u, D_lower t<=x<=D_upper t.
```

These are linear inequalities even when ratio-box endpoints are negative. The domain is bounded because both the ratio box and the positive scale interval are bounded. A degenerate scale interval `ell=u` does not invalidate the proof; its fixed positive slice already has the original full input dimension.

For an ordinary box in `(x,t)`, choose any full-dimensional bounded ratio box containing every `x/t`. For example, if `x_i` lies in `[L_i,U_i]`, the interval `[-M_i,M_i]`, with `M_i=max(|L_i|,|U_i|)/ell`, suffices; positive original coordinate width makes `M_i>0`. Apply the upper construction on this larger ratio box and add the desired original `x` bounds as linear rows.

For the ordinary-box lower bound, a fixed positive `t0` leaves the full-dimensional ratio box `[L_i/t0,U_i/t0]`. The quadratic theorem applies on that box with the same Hessian tuple. It is not necessary for this slice to recover the larger ratio box used for the upper bound. Thus both domains have the same leading coefficient.

## Rank-one example

For `g(x,t)=x^2/t`, direct differentiation gives

```
H_g(x,t)=(2/t) [1,-x/t]^T [1,-x/t].
```

It has rank one at every admissible point, including `x=0`. At `(0,1)` and `(1,1)` the Hessians are respectively

```
[2,0;0,0] and [2,-2;-2,2].
```

Their sum is `[4,-2;-2,2]`, with positive leading entry and determinant four, hence positive definite. Both points belong to the stated domain. The global Hessian span therefore contains a matrix of rank two, while perspective transfer gives leading integer coefficient one half. This correctly demonstrates that taking half the maximum rank, or noncommutative rank, of that global Hessian span would overestimate the sharp coefficient in this rational nonquadratic example.

## Attribution and limits

The perspective definition and its positive domain agree with Boyd and Vandenberghe's [primary book](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf), Section 3.2.6, which was independently opened during this review. The underlying transformation and bounded binary-product encoding are standard. The note properly locates its claimed contribution in transferring the separately established sharp formulation-precision laws.

No numerical tests are necessary for this transfer: both directions are explicit algebraic bijections for fixed positive scale, and the Hessian example is verified directly above. The review certifies the transfer and its stated consequences, not a new algorithmic hardness classification, cone-apex result, or exact equality of the two finite-accuracy minima.
