# Check of the common-factor novelty reductions

Date: 2026-09-04. Reviewer: independent `review_extension` agent.

Scope: the three mathematical reductions in
[common-factor-anchor-novelty.md](common-factor-anchor-novelty.md), plus
its binary-leaf and integer-anchor observations. This is not an audit of
the full common-factor hull theorem.

Verdict: all the reductions checked are correct under the reciprocal model's
positive bound assumption `0<a<=b`. They support the stated restrictions on
novelty. A singleton factor interval is trivial and needs no box normalization.

For SOCP representability, the graph with bipartition `{X}` and
`{T,Y_1,...,Y_n}`, products `XT,XY_1,...,XY_n`, and equality `XT=1` is
exactly an instance of the one-equality bipartite theorem after affine
normalization of its bounds. The original product coordinates are affine
functions of the normalized variables and products. Projection after fixing
the `XT` coordinate therefore gives precisely the reciprocal graph hull.
Theorem 1(ii) and Remark 1 of the
[Dey, Santana and Wang primary manuscript](https://optimization-online.org/wp-content/uploads/2018/03/6542.pdf)
were opened independently and confirm the needed lifted-graph scope and
the potentially exponential disjunction. This proves finite SOCP
representability, not a polynomial-size formulation.

For the projective map, start with a finite reciprocal mixture of weights
`lambda_k`, factor values `X_k>0`, and leaf vectors `Y_k`. Let
`m=sum_k lambda_k X_k` and define `nu_k=lambda_k X_k/m`. These weights
are nonnegative and sum to one. With `s_k=1/X_k`, their four means are

```
E_nu[s]=1/m,       E_nu[s^2]=t/m,
E_nu[Y]=w/m,       E_nu[sY]=q/m.
```

This proves the displayed map onto the square-anchor star hull directly.
The same algebra in reverse gives its inverse; indeed the coordinate map
`(m,t,q,w)->(1/m,t/m,w/m,q/m)` is an involution on the positive first-coordinate
domain. No equality between a reciprocal mean and the mean reciprocal under
the original weights is assumed. The cited positive projective-hull theory
is consistent with this elementary verification.

For scalar optimization, minimizing each affine leaf term gives
`F(X)=alpha X+beta/X+sum_j min(0,gamma_j+delta_j X)`. Each nonconstant leaf
coefficient changes sign at most once. After sorting its valid roots, every
piece is `A X+B+beta/X`. On a positive interval its only possible interior
minimum is `sqrt(beta/A)` when both `A` and `beta` are positive. If `beta<=0`
the piece is concave or affine; if `beta>0` and `A<=0` it is decreasing.
Thus the candidate list and the arithmetic complexity are correct. At a
breakpoint either active-set convention gives the same value. Zero leaf
coefficients and roots outside the interval are harmless.

Restricting `X` to integers only changes each piece to a consecutive integer
interval. Its endpoints and feasible integers immediately bracketing a
convex stationary point suffice. For a positive rational `p/q`, computing
`floor(sqrt(p/q))` reduces to integer square root of `floor(p/q)`, so the
range need not be enumerated. The objective at every selected integer is
rational. Hence polynomial dependence on the bit length of the range is
valid for the reciprocal case.

Finally, replacing continuous leaves by binary ones does not change the hull:
conditional on a fixed common factor, all retained coordinates are affine
in the leaf vector, which is a convex combination of its binary corners.
This observation does not apply automatically if additional nontrivial
constraints link the leaves. The source note correctly keeps that boundary.
