# Second independent audit of globally correlated total-flow hardness

Date: 2026-09-05. Reviewer: `spatial_sdp_review`.

**Verdict: PASS.** The [candidate](potential-flow-global-correlation-total-flow-hardness.md) establishes strong NP-hardness of maximizing the sum of all arc flows over a globally correlated resistance polytope on the stated bounded-data degree-three cactus family. The restricted weak-threshold and robust-upper problems have the stated NP/coNP membership, and the constant absolute-error value and rational-scenario hardness claims follow. The proof does not make a fixed relative-error claim.

## 1. Physical triangle equations and convex pair

Each triangle has two serial path edges of resistance r and one direct edge of resistance two, with unit through-flow. If f is the path flow, pressure equality is `2r f^2=2(1-f)^2`. Its physical solution is `f=1/(1+sqrt(r))`, strictly between zero and one. Hence the total of all three positive edge flows is `1+f`.

Direct differentiation gives the displayed positive second derivative

```
f''(r)=(1+3sqrt(r))/(4r^(3/2)(1+sqrt(r))^3).
```

The sum `psi(delta)=f(2+delta)+f(2-delta)` is therefore convex and even on `[-1,1]`. For binary parameters, delta is zero or has absolute value one. The two values simplify exactly to `A=2sqrt(2)-2` and `B=sqrt(3)/2`. Their difference satisfies

```
kappa>173/200-283/100+2=7/200>1/32,
```

because the two stated square-root bounds follow by exact squaring. Thus cut edges contribute a positive uniform increment.

## 2. Actual resistance polytope and graph construction

There are 2m disjoint triangles before connecting bridges, contributing 6m vertices and 6m edges. The 2m-1 joining bridges add no vertices and yield 8m-1 edges. A path of n bridges attached before the first triangle adds n new vertices and n edges. Consequently the candidate's counts `V=6m+n`, `E=8m-1+n`, and cycle rank 2m are correct.

Triangle entrance and exit vertices each have two triangle incidences and at most one bridge incidence, giving maximum degree three. Internal triangle vertices and internal path vertices have degree two. The orientation through the chain is acyclic. Each bridge separates the sole unit source from the sole unit sink and therefore carries exactly one unit, including every parameter-storing bridge. Each triangle has unit through-flow. All arc flows are strictly positive, so the signed sum equals the sum of absolute values without changing the objective.

The actual bridge resistance r_i gives `theta_i=r_i-1` in `[0,1]`. The four comparison path resistances are exactly `2+r_i-r_j` or `2-r_i+r_j`, lying in `[1,3]`. The remaining resistances equal two. All relations have fixed bounded integer coefficients. Since the r_i coordinates themselves are retained among the physical edge resistances, the full polytope is an injective affine image of the cube. It has no hidden projection and its vertices correspond exactly to binary theta, hence integer resistances. Isolated vertices of the comparison graph merely give bridge parameters not used by any comparison and cause no exception.

## 3. Exact objective relation

The 2m triangles contribute a constant 2m plus the sum of their path flows. The connecting and parameter bridges contribute `2m-1+n`. This gives precisely

```
T(theta)=4m-1+n+sum_ij psi(theta_i-theta_j).
```

Each summand is convex as a convex function of an affine form. A maximum on the cube occurs at a vertex: express an arbitrary point as a convex combination of vertices and apply convexity. At a binary vertex its value is `C+kappa cut(theta)`, with the stated C. Therefore the global maximum is exactly `C+kappa MaxCut(H)`. No relaxation gap, limiting resistance, or small-error physical approximation is involved.

## 4. Rational threshold size and gap

The threshold center can be written as

```
Q=4m-1+n+(m-K+1/2)A+(K-1/2)B.
```

For the nontrivial source cases both coefficients of A and B are nonnegative and at most m. Enclosing the two square roots by dyadics of width at most `1/(8192(m+1))` and choosing rational representatives gives an error in Q of at most `(2m+m/2)/(8192(m+1))`, which is less than 1/512. A common dyadic denominator can be chosen within a constant factor of `8192(m+1)`. The halves in B and in the two coefficients introduce only a constant factor into the denominator. Thus tau has denominator O(m+1) and numerator polynomial in m+n.

The distinction between numerical magnitude and bit length is correctly handled here: the integer network and polytope data are uniformly bounded, and both numerator and denominator of the rational threshold have polynomial numerical magnitude. Their unary encodings therefore remain polynomial. Unweighted Max-Cut yields the asserted strong hardness without large encoded weights.

In a yes instance,

```
OPT-tau>=kappa/2-|tau-Q|>1/64-1/512=7/512.
```

The symmetric no-instance inequality gives `tau-OPT>7/512`. Hence the weak target `OPT>=tau` exactly represents the source answer, and universal `T<=tau` represents its complement. Equality ambiguity is eliminated by the strict gap.

## 5. Membership and approximation outputs

On the restricted family, an optimal scenario can be chosen at integer bridge parameters, and its total flow has the form `C+kappa k` for an integer cut size. These values lie in the fixed extension `Q(sqrt(2),sqrt(3))` of degree at most four. Exact comparison with an arbitrary rational threshold has polynomial bit complexity. A binary scenario is therefore an NP certificate for weak attainment; it is also an NP certificate for a strict upper-bound violation. This proves the restricted NP/coNP membership claimed in the candidate. It does not establish membership for arbitrary coupled physical objectives or arbitrary global correlation families.

An additive value approximation of error at most 1/256 separates the source cases because that error is smaller than 7/512. If instead an algorithm returns a rational feasible scenario within 1/256 of optimum, its yes-instance value is above `tau+5/512`, while every no-instance scenario is below `tau-7/512`. Evaluate the returned scenario to absolute error 1/512 by independently enclosing its triangle square roots and summing. A polynomial-time rational-output algorithm supplies polynomial-size resistance rationals, so this evaluation has polynomial bit cost. These approximate comparisons still separate the two cases without exact comparison of an arbitrary sum of radicals.

The network objective grows with graph size. Therefore fixed absolute-error hardness does not imply a fixed relative-error or normalized-error hardness claim. The candidate explicitly preserves this distinction.

## 6. Independent exact construction check

Added and ran [the separate checker](../code/potential_flow_mpd/global_correlation_total_flow_second_review.py). It enumerates every nonempty simple comparison graph on two through four vertices, constructs the actual directed physical graph and globally correlated edge resistances, and checks every binary parameter profile. Arithmetic is exact in `Q(sqrt(2),sqrt(3))`.

It passed 71 cactus constructions, 1,068 exact physical profiles, and 205 rational threshold constructions. Checks include vertex and edge counts, maximum degree, directed acyclicity, cactus blocks, every node's conservation, every triangle's pressure equation, actual resistance bounds, the total-flow identity, dyadic threshold encoding, and the claimed strict gap. This supplements the proof and is independent of the author's full-state numerical checker.

The Max-Cut and convex-maximization mechanisms are classical. This audit supports the explicit passive-network scope and constants, not a broad claim of new optimization machinery. No correction is required.
