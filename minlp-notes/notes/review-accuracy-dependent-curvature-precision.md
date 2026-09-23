# Independent audit: accuracy-dependent scalar curvature precision

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**Status: PASS for the finite curvature theorem, raw-arclength obstruction, and additional two-bit comparison.** Reviewed:

- [Accuracy-dependent curvature precision](accuracy-dependent-curvature-precision.md).
- [Raw curvature arclength obstruction](curvature-arclength-precision-obstruction.md).
- [Scalar convex graph two-bit gap](scalar-convex-graph-two-bit-gap.md).

The conclusions are finite real-coefficient formulation statements. This audit does not establish efficient integration, quantile access, rational formulation construction, or literature novelty.

## Interval mass estimate

With `A=sqrt(f''/epsilon)`, monotonicity and continuity are sufficient; differentiability of `A` is not used. On the set `(b-t)A(t)<1`, the endpoint remainder integrand is bounded by both branches of the density, so its contribution is at most the total mass `m`.

On the complementary set, let `z=(b-t)A(t)>=1`. The actual density at every later point `s` dominates `min(A(t),(b-s)A(t)^2)`: both its arguments are at least the corresponding displayed arguments. Integrating this lower bound gives exactly `z-1/2`, hence `z<=m+1/2`. On this set the actual density is `A(t)`, since `(1-t)A(t)>=z>=1`. Its endpoint remainder contribution is at most `(m+1/2)m`. Thus `E<=m^2+3m/2` is correct, and `m<=1/2` gives `E<=1`.

For convex `f`, its chord minus its left-end tangent at any point is no larger than the endpoint Taylor remainder; the function lies above that tangent. Hence this remainder bounds the entire chord error. The continuous cumulative density can be partitioned into masses at most one half, using at most `max(1,ceil(2M_epsilon))<=2M_epsilon+1` intervals. Plateaus of zero density do not obstruct this choice. If total density is zero, continuity implies zero curvature throughout, so one affine interval suffices.

## Admissible intervals and the potential

The midpoint Jensen identity has a right-half contribution `(1/2)integral_c^b(b-t)f''(t)dt`. Monotonicity gives its lower bound `f''(c)ell^2/16`. The left part of the endpoint Taylor remainder is at most `3f''(c)ell^2/8`, hence at most six times the midpoint gap. The right part is at most twice that gap. Therefore every epsilon-admissible chord interval has normalized endpoint remainder `E<=8`.

Both cases of the proposed potential inequality are valid. When `ell<=d=1-b`, monotonicity gives `m<=ell A(b)`, and direct subtraction of the potential difference gives

```
m-[chi(b)-chi(a)]
 <=2ell A(a)-(d-ell)(A(b)-A(a))
 <=2ell A(a)<=2sqrt(2E).
```

When `ell>d`, the left part ending at `b-d` satisfies `1-t<=2(b-t)`, so its mass is at most `2E`. The remaining part has length `d` and mass at most `d A(b)=chi(b)`. The potential left at `a` satisfies `chi(a)=(d+ell)A(a)<=2ell A(a)<=2sqrt(2E)`. This proves the full inequality `m<=chi(b)-chi(a)+2E+2sqrt(2E)`.

The case `b=1` is included: `d=0`, the right part is empty, and `chi(1)=0`. There is no division by this zero length. With `E<=8`, the constant is `16+8=24`. Summing over a partition telescopes exactly, leaving `chi(1)-chi(0)=-A(0)<=0`, which can be discarded. Thus `M_epsilon<=24N_epsilon` holds with the displayed sign and constant.

## Parity supports and finite formulations

For an arbitrary convex integer lift, choose one lift of every exact graph point and group points by integer parity. Same-parity midpoints are integer-feasible, giving midpoint Jensen error at most epsilon. Taking support closures preserves this scalar inequality by continuity, without requiring the lifted sets themselves to be closed. The extreme input points of each nonempty compact support therefore obey it.

For a convex function, chord error on a span is a nonnegative concave function of the interpolation parameter, vanishing at both endpoints. Its maximum is at most twice its midpoint value. This proves that each support span has chord error at most `2epsilon`.

A finite closed-interval cover of the unit interval can be trimmed to a partition with no more pieces than covering intervals: extend greedily from the current endpoint to the furthest right endpoint of an interval containing it. The finite cover prevents a gap or a terminal zero-length step before reaching one. Each chosen interval is used at most once. Chord error cannot increase on a subinterval, because the subinterval chord lies below the original chord. Consequently `N_(2epsilon)<=2^p` is justified even though the original parity supports need not be intervals.

Pointwise density comparison gives `rho_epsilon<=2rho_(2epsilon)`. Therefore `M_epsilon<=48*2^p`, and `1+M_epsilon<=49*2^p` since `p>=0`. This proves the stated lower logarithmic constant. The admissible chord-band construction uses `ceil(log2 N_epsilon)` binaries with finite real Hamming-distance disjunction constants and exclusions for unused codes. The bound `N_epsilon<=2(1+M_epsilon)` then proves the stated upper constant two.

All quantities are finite under the stated `C^2` compact-domain assumptions. The existence of a finite partition also follows directly from bounded curvature. Arbitrary affine terms cause no change to these arguments. An algorithm for computing the integral and accessing its quantiles is a separate question, correctly left unresolved.

## Raw-arclength obstruction

For the normalized positive-polynomial family, the intervals associated with successive powers meet only at their endpoints. On the interval of length `1/(2k)`, the selected monomial contributes at least `k^2/(8M)` to curvature, exactly as in the independently reviewed allocation-gap example. Taking square roots and integrating gives `1/(4sqrt(2M))` per interval and `sqrt(M)/(4sqrt(2))` overall.

The function increases continuously from zero to one. Inverse images of sixteen equal output-height increments give sixteen chord intervals with error at most `1/16`. The chord bands admit only that error and use four binary index variables in a finite real formulation. This proves an unbounded overestimate from raw curvature arclength at fixed tolerance. It does not contradict high-accuracy asymptotics for a fixed function, and does not imply that every adaptive density fails.

I flagged two presentation issues and the author corrected them: the obstruction's statement that the proposed density was unproved had become stale, and the main finite benchmark already follows mathematically without a computational model. Efficient computation remains conditional, rather than the finite comparison itself.

## Additional finite two-bit theorem

The support-span argument above needs only continuity and convexity. Uniform continuity supplies a finite chord partition even without bounded derivatives. Hence it applies to every continuous scalar convex function on the closed interval.

For one interval with chord error at most `2epsilon`, let `g` denote that error. If its maximum exceeds epsilon, continuity and concavity make its epsilon-superlevel set a nondegenerate closed interval strictly inside the original interval, with both boundary values equal to epsilon. Splitting at those two endpoints gives at most three pieces. The new chord error of `f` equals `g` minus the chord of `g` on each piece. On the outer pieces this is between zero and `g<=epsilon`; on the middle piece it equals `g-epsilon<=epsilon`. Thus `N_epsilon<=3N_(2epsilon)` is correct, including plateau and asymmetric cases.

It follows that `p_bin<=ceil(log2(3*2^p_conv))=p_conv+2`. This is a universal finite comparison for a scalar continuous convex graph, not a proof of a compact or rational construction from a function oracle. No optimality of the additive constant two is asserted.

## Independent checks

An independent exact rational implementation checked **2,160 interval-mass and potential inequalities** for monotone step values of `A`, including zero regions, sharp jumps, large terminal values and intervals ending at one. The density integrals were evaluated exactly by splitting at their rational branch thresholds; the square-root potential bound was verified by an equivalent rational squared inequality when its left side was positive. These nonsmooth monotone stress cases supplement the full proof for the stated continuous-curvature class.

A further **48 exact concave-gap refinement cases** checked asymmetric tents and plateaus, including the full `2epsilon` height. Every refinement had subinterval chord error at most epsilon. All checks passed. They do not replace the symbolic uniform estimates or supply numerical-integration complexity guarantees.

No mathematical correction was needed in the reviewed proofs.
