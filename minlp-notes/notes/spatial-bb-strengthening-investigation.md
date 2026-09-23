# Spatial branch-and-bound with full SDP–RLT: candidate strengthening

Date: 2026-09-05. Status: promoted after independent review to
`results/spatial-bb-sdp-rlt-exponential-lower-bound.md`; 809 targeted constraint
checks passed. The candidate text below records the original derivation. This strengthens
`results/spatial-bb-exponential-lower-bound.md`; do not treat novelty as settled.

## Candidate theorem

Let `P_n` be the continuous concave quadratic program

```
min sum_i (x_i - x_i^2),  sum_i x_i = K := k + 1/2,  0 <= x_i <= 1.
```
Its optimum is `1/4`. Fix a box `B = prod_i [a_i,b_i]` with
`0<=a_i<=b_i<=1`. Define `SDP(B)` as the
minimum of `sum_i (x_i-X_ii)` subject to:

- `a <= x <= b`, `sum_i x_i = K`;
- `[[1,x^T],[x,X]] >=PSD 0`, with `X` symmetric;
- `sum_j X_ij = K x_i` for every `i`;
- all box RLT inequalities: the linearizations of `u_i v_j >= 0`, where
  `u_i` is either `x_i-a_i` or `b_i-x_i`, and `v_j` is either `x_j-a_j` or
  `b_j-x_j`, for every `i,j`, including `i=j`.

Infeasible boxes have bound `+infinity`. A box is pruned at tolerance epsilon
when `SDP(B) >= 1/4-epsilon`. These constraints include all pairwise
McCormick inequalities, diagonal secants, and all linear-equality products.
The relaxation is valid for `P_n` by taking `X=xx^T`.

**Theorem (candidate).** Let `n=k+m+z`, with integers `k,m,z>=1`, and
`0<epsilon<1/4`. Set

```
h = m(1/2-2epsilon),   q = min(k,z,h).
```

Any cover of the feasible set by SDP-pruned boxes has at least

```
min{ (n/(n-k))^(q/2), (n/(n-z))^(q/2) }
```

members. In particular, `n=3t`, `k=m=z=t` gives the same lower bound
`(3/2)^[t(1/4-epsilon)]` as the separable-relaxation result, now with full
nodewise SDP–RLT. Every spatial variable-branching certificate using this
relaxation (or any weaker valid bound) therefore has exponentially many
leaves at a fixed epsilon. The original chord certificate gives `O(2^n)`
nodes because SDP–RLT dominates the chord objective bound.

## Proof

Choose uniformly an ordered partition `(H,M,Z)` of `[n]` with sizes `k,m,z`.
Let `p=1/(2m)` and `w=1_H+p 1_M`, a feasible point. For a box containing `w`,
write

```
A={i:a_i>0}, D={i:b_i<1}, R=A union D, U=[n] minus R.
```

The essential lemma is: if `|R|<min(k,z)`, there is a feasible SDP–RLT point
with objective `|M intersect R| p(1-p)`.

To prove it, fix all coordinates in `R` deterministically to their witness
values `w_i`. Put `s=|U|`,

```
t = K - sum_{i in R} w_i = |H intersect U| + p |M intersect U|.
```

Because `|R|<k,z`, there is at least one `H` coordinate and one `Z` coordinate
in `U`. Hence `s>=2` and `1<=t<=s-1`. Define `c=t/s` and
`d=t(t-1)/(s(s-1))`. On `U`, set `x_i=c`, `X_ii=c`, and `X_ij=d` for
`i!=j`. On `R`, set `x_i=w_i`, and set `X_ij=x_i x_j` whenever at least one
index is in `R`.

Verification:

1. Every `U` interval is exactly `[0,1]`, so first moments satisfy their
   bounds; on `R` they do so because `w in B`. Also `sum x=K`.
2. Covariance `X-xx^T` is zero on every row or column indexed by `R`. Its
   `U` block is `(c-d)I+(d-c^2)J`. Its eigenvalue along the all-ones vector
   is zero since `c+(s-1)d=t c`; every orthogonal eigenvalue is
   `c-d=t(s-t)/(s(s-1))>=0`. Thus the moment matrix is PSD.
3. For `i in U`, `sum_j X_ij=c+(s-1)d+c sum_{j in R}w_j=cK`. For `i in R`,
   `sum_j X_ij=w_i sum_j x_j=w_i K`. All equality products hold.
4. For two distinct `U` coordinates, the four box RLT expressions are
   `d`, `c-d`, `c-d`, and `1-2c+d`. All are nonnegative: the final expression
   is `(s-t)(s-t-1)/(s(s-1))`, using `t<=s-1`; the others use `t>=1`.
   When the coordinates coincide, the relevant expressions are `c`, `0`,
   and `1-c`. If at least one index belongs to `R`, a product of bound
   slacks has expectation equal to a nonnegative deterministic slack times
   another nonnegative expected slack. Thus all RLT constraints hold.
5. Every `U` objective term is zero, while `R` contributes exactly
   `sum_{i in R} w_i(1-w_i)=|M intersect R|p(1-p)`.

If a box containing a witness has `|R|<q`, the lemma applies and its SDP
bound is at most `|R|p(1-p)<h/(2m)=1/4-epsilon`. Therefore every pruned box
containing a witness has `|R|>=q`, and then `|A|>=q/2` or `|D|>=q/2`.

Every witness in that box has `Z intersect A=empty` and
`H intersect D=empty`. Consequently, its fraction of all witnesses is at
most

```
min{ ((n-z)/n)^|A|, ((n-k)/n)^|D| }
<= max{ ((n-z)/n)^(q/2), ((n-k)/n)^(q/2) } = rho.
```

A cover must contain at least `1/rho` boxes. No part of the argument
requires disjoint boxes or a particular branching rule. QED.

## What this does and does not cover

The result covers all PSD cuts on the full second-moment matrix, all box
RLT cuts, equality products, arbitrary coordinate split points, and arbitrary
feasibility-based bound tightening. It also covers products of any two
valid affine inequalities for `B intersect F`: by linear-programming duality,
each such affine slack is a nonnegative combination of box slacks and a
constant, plus a multiple of the equality; expand the product, and every
resulting expectation is nonnegative or vanishes by the existing constraints.
This last closure observation needs independent verification as well.

Objective-based bound tightening is counted through an augmented cover:
include each removed slab certified above the target, as well as the final
leaf boxes. The final leaf boxes alone need not cover the feasible set.
If at most `r` such slab deletions occur per processed node, the same lower
bound divided by `r+1` holds for processed-node count.

The result does not cover arbitrary valid quadratic cuts. For example,
the global inequality `sum_i(x_i-X_ii)>=1/4` is valid on the lifted graph
and closes the problem immediately. It is the desired conclusion itself.
Symmetry-breaking constraints, general branching disjunctions, and stronger
moment hierarchies require separate analysis.

## Initial literature pointers

A search on 2026-09-05 found a close predecessor requiring careful reading:
[Best case exponential running time of a branch-and-bound algorithm using an
optimal semidefinite relaxation](https://optimization-online.org/2018/07/6729/)
(2018). Novelty cannot be assessed without checking its exact branching and
relaxation model. Grigoriev's fractional-knapsack pseudomoments are also a
known ingredient; the new candidate is their use inside arbitrary real
spatial boxes, combined with a cover argument at fixed objective tolerance.


## Verification and prior-art comparison

The reproducible script
`code/spatial_bb_lower_bound/check_sdp_rlt_strengthening.py` passed **809**
constructed-point checks. It uses exact rational arithmetic for every
first-moment, box RLT, equality-product, and objective identity, and numerical
eigenvalues for the full PSD matrix (whose eigenvalues are proved above).
Cases include all admissible `k,m,z` and restricted sets of size below
`min(k,z)` for `n<=9`, plus larger balanced and asymmetric cases and
some degenerate node intervals.

[Jarre's 2018 paper](https://optimization-online.org/wp-content/uploads/2018/07/6729.pdf)
was read in full. Its branch-and-bound model fixes binary variables to zero
or one (pages 2–3), and its SDP is the standard max-cut relaxation after
transforming a binary knapsack equality (pages 4–5). Its lower bound does
not cover continuous variables, arbitrary real split points, or full box
RLT. It is a close conceptual predecessor and must be cited; it does not
imply the candidate theorem. The potentially new part is the fixed-gap
cover lower bound for arbitrary real spatial boxes after nodewise SDP–RLT
strengthening. This is a bounded novelty assessment, not proof of priority.


### Updated literature scope (2026-09-05)

A [follow-up literature comparison](../notes/spatial-bb-strengthening-novelty.md)
identified Coniglio's ICLR 2026 spatial lower bound under midpoint branching,
in addition to Jarre's binary SDP lower bound. Thus exponential spatial
lower bounds in general are already known. The tentative novelty claim here
is restricted to the specified arbitrary-split, fixed-gap relaxation model.
The literature note records which source portions were read and which
appendix proof remained inaccessible after a browser challenge.
