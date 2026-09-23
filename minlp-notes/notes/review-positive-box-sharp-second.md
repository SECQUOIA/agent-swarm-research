# Second independent audit of sharp leading-order positive-box growth

Date: 2026-09-04. Reviewer: `review_extension`. Status: passed. This is a mathematical audit, not a certification of literature priority.

Reviewed [the sharp positive-box theorem](../results/positive-multilinear-positive-box-sharp.md). The upper bound

```
2+(rho+1)/(1-3/sqrt(rho)),  rho>=64,
```

is correct. Combined with the separately reviewed lower construction, it proves `C_box(rho)/rho -> 1`. This review checks the new upper argument independently; the lower construction retains its own audit.

## Asymmetric split and exact local quantities

Let `delta=rho^(-1/2)<=1/8`, `t=rho-1`, and `eta=1-1/rho`. Low normalized success means are at most `1-delta`; high failure means are below `delta`. Under the common-threshold success law, low successes can occur only before `1-delta`, and high failures only afterward. Hence, after division by `rho^h`, the full concave value is exactly `C_L+C_H-1`, despite the fact that some low success means now exceed one-half.

The independent expectation factors as `P_L P_H`. Its deficiency identity has three nonnegative terms, exactly as in the previously audited symmetric split. The normalized convex envelope remains `phi_rho(Q_L-Q_H)`: the number of high coordinates is an integer shift in the expected total number of physical upper endpoints. This formula is not affected by the new threshold. The two supporting slopes of this convex interpolation give `T<=A+B+t eta min(Q_L,Q_H)`.

The count inequalities giving `A>=t^2(Q_L-a_L)` and `B>=eta^2(Q_H-a_H)` do not use a one-half bound. The integration interval changes, but the identities `integral(L-1)_+=Q_L-a_L` and its high counterpart remain valid.

The new bound `D_IL>=delta A` is correct. In the positive subset expansion of the low product, every degree-at-least-two subset has independent product at most `(1-delta)` times its smallest marginal. Its common-threshold contribution is that smallest marginal. The constant and degree-one terms cancel from the deficiency, while their removal from the concave sum leaves exactly `A`. Zero marginals satisfy the same argument without division.

## Orientation cross term

The asymmetric split requires the separate argument provided in the draft; the earlier formula for a symmetric half-interval cannot simply be reused for all low means. For `s` in `[0,delta]`, a low success interval of length at most `1-delta` covers at most one of `s` and `1-s`, except at measure-zero endpoints. Its conditional expectation at either end is thus `1+(t/2)1{s<=u_i}`. A high normalized factor has conditional expectation `1-(eta/2)1{s<=q_i}`.

Outside the two end strips, both possible high success intervals contain the uniform point. The high conditional product is therefore exactly one. Writing the full orientation expectation as the product of the two conditional group expectations gives the stated cross-deficiency integral, with its prefactor two. The separate low and high orientation deficiencies are nonnegative because these laws preserve their respective marginals; no bound `D_OL>=A/2` is imported.

On an interval of length `min(a_L,a_H)`, which is contained in the end strip, the two cross factors are at least `t/2` and `eta/2`. Thus `J_O>=t eta min(a_L,a_H)/2`. Together with the two count bounds, this proves

```
T<=(1+1/rho)A+(1+rho)B+2J_O.
```

All assertions include empty groups and deterministic coordinates.

## Small high-failure mass

For `Q_H<=4delta`, let `q=a_H` and `R=Q_H-q`. Bonferroni gives

```
D_IH>=B-eta^2(qR+R^2/2).
```

Since `B>=eta^2 R`, this is at least `(1-q-R/2)B`. The bounds `q<=delta` and `R<=4delta` yield `(1-3delta)B`; using the sharper relation between `q` and `R` is unnecessary. The proof uses no division by `R` and therefore includes its zero value.

Combining this bound with `D_IL>=delta A` yields the claimed coefficient

```
b=(rho+1)/(1-3delta).
```

It dominates `(1+1/rho)/delta`: after cancellation the required inequality is `rho*delta>=1-3delta`, which holds for `rho>=64`. The denominator is positive. Since `D_I` contains both within-group deficiencies and a nonnegative cross term, and `D_O>=J_O`, the conclusion `T<=bD_I+2D_O` follows with no unaccounted coefficient.

## Large high-failure mass

For `Q_H>=4delta`, the common-threshold high failures are supported on a set of measure at most `delta`. Hence `C_H>=1-delta`. Also `P_H<=exp(-4eta delta)`. The Taylor upper bound gives

```
exp(-4eta delta)<=1-[4eta-8eta^2 delta]delta<=1-2delta,
```

because `eta>=3/4`, `eta^2<=1`, and `delta<=1/8` imply `4eta-8eta^2 delta>=3-1=2`. This proves `D_IH>=delta` and `1-P_H>=2delta` by exact inequalities, without numerical estimates.

It follows that `J_I>=delta*tQ_L`, using only half of the available cross bound. Therefore

```
D_I>=delta A+delta+delta*tQ_L=delta C_L>=delta T,
```

where the last inequality follows from `C_H<=1` and nonnegative convex-envelope value. Since `b>=delta^(-1)`, this proves the same local inequality as the small-mass case. At `Q_H=4delta` both arguments apply, so the case split has no boundary gap.

## Global consequence and asymptotic statement

The two laws and their probabilities depend only on the full marginal vector and the common box ratio, not on the monomial. Mixing independence with probability `b/(b+2)` and orientation with probability `2/(b+2)` therefore gives one common feasible law. Restoring each positive normalization and summing with positive coefficients yields the full-polynomial bound, because common-threshold rounding simultaneously attains all concave envelopes.

The earlier positive affine expansion argument extends this upper bound to boxes with coordinate ratios at most `rho`: the original local gap is at most the expanded local-gap sum, while the exact full graph-hull gap is invariant under the coordinate bijection. This is not an inference from box inclusion. Degenerate coordinates can first be removed.

Finally,

```
2+(rho+1)/(1-3/sqrt(rho))=rho+3sqrt(rho)+O(1).
```

The separately established examples have ratios tending to `rho` for each fixed ratio. Thus the definition allowing every smaller or unequal aspect ratio has lower bound at least `rho` and the preceding upper bound, proving the sharp leading constant one. This does not determine the exact finite-ratio constant or a sharp second-order term.
