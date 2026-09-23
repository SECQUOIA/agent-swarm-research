# Second independent audit of global-correlation arc validation

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS.** The [candidate](potential-flow-global-correlation-arc-validation.md) gives an exact rational LP formulation for cactus arc-capacity feasibility under a single globally correlated parameter polytope, rational LP tests for robust capacity satisfaction, and exact individual arc optimization over the original or capacity-filtered polytope. Independence between cycles is unnecessary for these tasks.

## 1. Physical decomposition remains valid

For each fixed global parameter vector, the continuous strictly increasing zero-at-zero edge laws have coercive strictly convex energy and a unique passive state, as checked in the [polynomial-law application review](review-potential-flow-correlated-polynomial-cycle-design-second.md). This pointwise argument never uses independence among the parameters. Positive-flow acyclicity gives the same uniform flow bound B.

Fixed nominations determine bridge flows and the rational offsets on each cactus cycle by conservation. Sharing parameter coordinates across cycles changes their equations' coefficients but introduces no new cycle equation. After solving every scalar cycle equation for a fixed global parameter vector, potentials can be assembled along the block tree. Articulation potentials impose no additional restriction in the absence of potential bounds.

Consistent cycle orientation and the law replacement `-g_e(-x;theta)` on reversed edges give the stated strictly increasing H. Rational arc bounds, or a rational flow inequality whose variable part is confined to one cycle coordinate, reduce to rational interval constraints on that coordinate. Bridge constraints are constant rational checks. Clipping to `[-B,B]` is legitimate after choosing the coordinate as a reference-edge flow.

## 2. Capacity feasibility and robust directions

For each fixed theta, if q is the unique root of H, strict increase gives

```
a<=q iff H(a,theta)<=0,
q<=b iff H(b,theta)>=0.
```

The displayed feasibility inequalities therefore have exactly the correct directions and retain equality. At rational a and b, fixed-breakpoint polynomial evaluation yields rational affine expressions in theta, with polynomial encoding length. An affine constant term is simply moved to the right-hand side of its linear inequality.

Appending all these inequalities to the input polytope describes precisely the physically capacity-feasible scenarios. It is a single rational polytope in the original global parameter coordinates. There is no relaxation or projection of separate cycle choices, so arbitrary correlations are preserved. A rational feasible point returned by LP is an exactly feasible original scenario even if its physical flow is irrational or lies at a singleton algebraic boundary.

Universal satisfaction over the original nonempty P requires the maximum lower-bound expression to be nonpositive and the minimum upper-bound expression to be nonnegative. These are exactly the proposed robust LP tests. If either fails, an LP optimizer is a rational violating scenario, and the strict LP value sign certifies the physical violation without algebraic root evaluation.

An empty imposed circulation interval or a violated fixed bridge bound is handled directly. I requested an explicit zero-flow/edgeless branch before invoking the nontrivial-bracket root lemma; the author added it. This is a degenerate-case clarification and changes no claimed result.

## 3. Exact individual extrema with filters

The target cycle's H has a fixed rational piece partition and dense polynomial coefficients affine in the full global parameter vector. Its strictly increasing root remains bracketed by `[-B,B]`. Thus all hypotheses of the reviewed piecewise monotone-root optimization theorem hold over P, whose dimension is allowed to grow.

After adding capacity filters, the new domain is still a bounded rational polytope. If it is empty there is no filtered scenario. Otherwise passivity, strict increase, continuity, and the common root bracket remain true on this subset. Lower-dimensional or singleton filtered polytopes are covered by the root lemma. Its rational optimizing vertex is a point in the original parameter space and satisfies every filter exactly.

Target arc extrema follow by rational shifts and possible sign reversal of the scalar target coordinate. A fixed bridge has a constant rational extremum and any feasible filtered parameter point realizes it. No field containing roots from different cycles is needed, because only one scalar target equation is optimized at a time.

All coefficient evaluations, added inequalities, and piece partitions have polynomial bit size under dense encoding. The abstract root algorithm's Cramer bounds automatically apply to the new rational inequality description. No additional encoding assumption is needed after filtering.

## Scope and attribution

This proof does not show that the globally correlated flow image is an affine box or convex. It does not optimize a coupled multi-cycle performance function. It also does not admit inequalities coupling several circulation coordinates merely because their parameter polytope is global. Those distinctions are consistent with the companion total-flow hardness result.

Capacity linearization is an elementary consequence of strict scalar monotonicity and has relevant earlier coefficient-space formulations; source comparison is assigned separately. This audit establishes correctness of the stated generality and exact-output guarantees, not priority. No remaining correction is required.
