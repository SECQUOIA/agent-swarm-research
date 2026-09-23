# Independent audit: convex polynomial cactus design

Date: 2026-09-05. Reviewer: potential_flow_review. Verdict: PASS.

I independently checked
[the convex polynomial extension](potential-flow-convex-polynomial-design.md)
against both the exact-capacity interval theorem and its within-cycle
resistance-polytope extension. No extra mathematical assumption is needed
beyond the stated dense rational encoding and convexity on the expanded
flow box. Global convexity of the polynomial is unnecessary. Convexity
validation, sparse binary-degree input, cross-cycle constraints, and variable
nominations remain outside the claim.

## Perspective extension and its boundary subgradients

Extend `h` by infinity outside the cube. It is a closed convex function.
The joint function

```
Phi(z,t)=t h(z/t)+M(t-1),
t>=1,       |z_i|<=t,
```

is convex by the perspective construction. Its feasible `t` values form
`[max(1,||z||_infinity),infinity)`. At all these values, the ordinary
polynomial derivative gives

```
partial_t Phi=h(w)-grad h(w)^T w+M>=1.
```

The lower bound follows from `|h|<=V`, `|partial_i h|<=G`, and
`M=1+V+kG`. Thus the partial minimum is attained at the smallest feasible
`t`, equals the displayed `H`, and is globally convex. It agrees exactly
with `h` on the cube. This argument applies to negative constant terms and
functions convex only on the cube.

Here is a pointwise justification of both the oracle formula and the
Lipschitz bound, including all ties. Put `t=t(z)`, `w=z/t`, and
`K=h(w)-grad h(w)^T w+M`. The joint perspective has supporting coefficients
`(grad h(w),K)` on its convex domain. If `tau` is any subgradient of the
convex gauge `t(z)=max(1,||z||_infinity)`, then `K>=1` and its supporting
inequality imply

```
s=grad h(w)+K tau in partial H(z).
```

In the cube interior take `tau=0`. Outside it, take a signed coordinate
vector at a maximizing absolute coordinate. At the cube boundary, zero
and those active signed coordinate vectors, or their convex combinations,
are valid. All these choices are rational at rational input.

The bound `1<=K<=1+2(V+kG)` and `||tau||_infinity<=1` yield
`||s||_infinity<=C`. Applying the supporting inequality at either endpoint
therefore gives directly

```
|H(z')-H(z)|<=C||z'-z||_1<=kC||z'-z||_2.
```

This avoids any reliance on differentiability of a line lying entirely in
a tie set. It confirms the note's global Lipschitz conclusion and its
subgradient formula at every query point.

## Polynomial bit complexity and optimization import

Under dense encoding, the total degree is polynomially bounded in the
input length. Powers of the rational radius, coefficient sums, and the
gradient bounds consequently have polynomial bit length even though their
numerical magnitudes may be large. Evaluating `f` and its gradient after
a rational affine substitution is polynomial bit arithmetic; expanding
the composed polynomial is unnecessary. At a rational query, division by
the rational `t>=1`, polynomial evaluation, and the subgradient formula
all retain polynomial bit length.

Every zero-width surrogate interval must be removed before rescaling,
including a retained rational singleton as well as a specially frozen
proxy. The author was asked to make this routine case explicit. All
remaining intervals have positive rational widths, and their normalization
and its inverse have polynomial rational encoding. If there are none, the
objective is evaluated directly.

I directly checked
[Dadush's thesis](https://homepages.cwi.nl/~dadush/papers/dadush-thesis.pdf),
Theorem 2.5.9 on printed page 48, together with the input-length convention
in Section 2.5.1. Its global convex Lipschitz value-oracle hypothesis is
met by `H`. The rational cube has the required explicit inner and outer
radii and an exact membership oracle. The theorem returns a rational point
inside the cube with the requested additive objective accuracy in polynomial
bit time. No merely approximate feasibility repair for this cube is needed.

## Exact capacities and the error budget

The objective extension changes only optimization over the rational
surrogate. The parent algorithms retain exact rational resistance recovery
for retained rational circulations and stored exactly capacity-feasible
profiles for frozen coordinates. The new objective cannot change those
feasibility guarantees.

For the correlated-cycle version, projection changes flow by at most
`3m eta` in one-norm and final recovery by at most `m eta`. All these flows
and the joining segments lie in the expanded box, where `G_f` bounds the
absolute partial derivatives. Therefore the total loss is at most

```
4mG_f eta+epsilon/2<=3epsilon/4<epsilon.
```

The interval-only version has the smaller existing projection constant.
Zero nomination and edgeless cases are handled before division by `m`.
The conclusion is a rational resistance scenario with exactly satisfied
capacities; it does not assert rationality of its physical state.

## Independent exact diagnostics

[The separate subgradient checker](../code/potential_flow_mpd/convex_polynomial_extension_subgradient_review.py)
passed 5,580 exact rational supporting-hyperplane inequalities in dimensions
one through three. It includes all cube-boundary and tied-maximum cases on
its test grids, negative affine terms, and quartics convex on the cube but
not globally. The checker supplements the general convexity and bit proof;
it is not an implementation of the imported ellipsoid algorithm.
