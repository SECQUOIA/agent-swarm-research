# Pairwise contact chords do not control a multivariate convex hull

Date: 2026-09-05. Status: elementary supporting obstruction for continuous convex functions. This does not claim a convex polynomial counterexample or an integer-formulation lower bound.

Let `Delta` be an n-dimensional simplex with `n>=2`, vertices `v_0,...,v_n`, and affine barycentric coordinate functions `lambda_i`. For any `M>0`, define

```
f(x)=-M min_i lambda_i(x)=max_i (-M lambda_i(x)).
```

This is a convex piecewise-affine function on the simplex. It is zero at every vertex and along every segment joining two distinct vertices: at least one remaining barycentric coordinate is zero throughout such a segment. Thus every pairwise chord of the vertex contact set has zero error, including every midpoint test.

At the simplex barycenter, however,

```
f((v_0+...+v_n)/(n+1))=-M/(n+1),
```

while the corresponding convex combination of vertex graph outputs is zero. The convex-hull Jensen error can therefore be arbitrarily large despite exact pairwise chord compatibility on the contact set.

Consequently the one-input argument that replaces a parity contact set by its interval hull cannot be transferred merely by replacing intervals with multivariate convex hulls. Its midpoint-to-whole-chord estimate is intrinsically one-dimensional. A multivariate proof needs additional information about higher-order combinations, the contact set, or function structure.

The coupled-separable construction avoids this issue through coordinate packings and a product code. This example does not disprove a multivariate theorem with other techniques. It also does not itself supply an admissible integer lift whose full fibers realize these contacts: integrality of higher-order combinations would need separate analysis.

The nonsmoothness is material to this exact example. A differentiable convex function that is affine on every simplex edge and agrees with one affine function at the vertices must equal that affine function throughout the simplex: the incident edge directions fix its vertex gradient, whose supporting affine function then meets the convex upper interpolation bound. A polynomial analogue would therefore need approximate edge flatness, not identical zero edge gaps. No such polynomial construction is asserted here.
