# Positive polynomial feature-curve geometry

Date: 2026-09-05. Status: elementary supporting identities verified in the
[independent shape-precision audit](review-positive-polynomial-linear-shape-precision.md).
No novelty claim is made for these norm and convexity identities.

## 3. A degree-uniform Euclidean feature comparison

For the scalar-sum model, remove the affine terms, which have zero Jensen
gap. Write the remaining summand as `phi_i(x)=sum_(k>=2) c_ik x^k`, with
`c_ik>=0`, and define its feature curve:

```
psi_i(x)=(sqrt(c_ik) x^(k/2))_(k>=2:c_ik>0).
```

The feature coordinates are nonnegative and increasing. For every `a,b in[0,1]`,

```
(1/4)||psi_i(a)-psi_i(b)||²
 <=J_(phi_i)(a,b)
 <=(1/2)||psi_i(a)-psi_i(b)||².                        (5)
```

The lower bound follows termwise from convexity of `x^(k/2)` for `k>=2`.
For the upper bound, arithmetic-geometric mean gives
`((a+b)/2)^k>=(ab)^(k/2)`, so

```
(a^k+b^k)/2-((a+b)/2)^k
 <=(a^(k/2)-b^(k/2))²/2.
```

Sum with the nonnegative coefficients. The comparison constants are independent
of the degrees and the number of nonzero monomials. Irrational feature coefficients
appear only in this geometric proof; the constructed MILP remains rational.

An ordered sequence on a feature curve has coordinatewise nonnegative increments.
Therefore squared distances are superadditive along the sequence:

```
||psi_i(x_k)-psi_i(x_j)||²
 >=sum_(h=j)^(k-1)||psi_i(x_(h+1))-psi_i(x_h)||².        (6)
```

This follows by expanding the square and observing that all cross inner products
of the increments are nonnegative.


The feature comparison is useful geometrically, but the main separable graph
precision proof now uses direct Jensen-gap superadditivity, which holds for
every continuous convex function and gives a stronger constant.
