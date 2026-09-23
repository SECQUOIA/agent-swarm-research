# Independent audit of the fixed positive-box gap bound

Date: 2026-09-04. Reviewer: `review_extension`. Status: the bound 67 on `[1,2]^n` passed a complete independent audit. The subsequent sections also audit the general-ratio extension and its stronger `45/2` consequence for boxes of aspect ratio at most four.

Reviewed the complete proof in [the co-development note](positive-box-independent-investigation.md), including its all-high lemma. For every positive multilinear polynomial on `[1,2]^n`, the exact termwise monomial gap is at most 67 times the exact scalar graph-hull gap. The bound is uniform in dimension, degree, positive coefficients, monomial frequency, and the evaluation point. Correctness does not depend on numerical search. Neither sharpness of 67 nor literature novelty is established by this review.

## Exact envelopes and normalization

Write each physical variable as `1+X_i`, with Bernoulli mean `u_i`. Conditional independent rounding of a point in the continuous cube preserves every multilinear function and all means, so vertex distributions suffice for the exact envelopes.

At a binary vertex, the monomial is `2^K`, where `K=sum X_i`. Its minimum expectation is the adjacent-integer interpolation `phi(sum u_i)`: convexity gives the lower bound, and the cube slab `floor(sum u_i)<=sum X_i<=ceil(sum u_i)` is integral. A fractional vertex would have either two fractional coordinates permitting a sum-preserving perturbation, or one permitting a perturbation unless an integer sum bound forced it to be integral. Thus the prescribed mean vector is a convex combination of binary vectors with the two adjacent cardinalities, proving attainment. Common-threshold rounding attains the concave envelope by the usual positive-product rearrangement, or by expanding the product into positive binary monomials and attaining every upper intersection probability simultaneously.

These physical product envelope formulas also agree with [Adams–Gupte–Xu, Proposition 4.1](https://www.pure.ed.ac.uk/ws/files/137020380/1704.00424.pdf), which attributes them to earlier work. Their role here is established input, not a new envelope formula.

Classify `u_i<=1/2` as low with `q_i=u_i`, and the others as high with `q_i=1-u_i`. If there are `h` highs, division by `2^h` is correct even when some coordinates are deterministic. Since `sum u_i=h+Q_L-Q_H`, integer translation gives the normalized convex envelope `phi(Q_L-Q_H)`, including a negative argument. It must not be replaced by a convex envelope of separately expanded submonomials.

Under common-threshold rounding, the first half of the uniform interval contributes `2^L` after normalization, and the second half contributes `2^(-H)`. Under fair independent endpoint orientations, each half contributes `(3/2)^L(3/4)^H`. This proves the displayed normalized integral formulas, including the factor two in the orientation expectation. Independence gives exactly `P_L P_H`.

## Deficiency decomposition and elementary bounds

The identities

```
D_I=D_(I,L)+D_(I,H)+(P_L-1)(1-P_H),
D_O=D_(O,L)+D_(O,H)+2 integral[((3/2)^L-1)(1-(3/4)^H)]
```

have the correct signs. Every constituent is nonnegative. Both within-group laws have the required marginals and their expectations cannot exceed the group's common-threshold maximum. The low orientation inequality also follows term by term from the binomial expansion; its coefficient `1-2^(1-j)` is at least `1/2` for every `j>=2`, yielding `D_(O,L)>=A/2`. For the high orientation term, convexity gives `2(3/4)^H<=1+2^(-H)` for every integer `H>=0`.

If `a,b` are the largest low/high deviations, then integrating `(L-1)_+` and `(H-1)_+` gives `Q_L-a` and `Q_H-b`. The integer inequalities in the note therefore prove `Q_L<=a+A` and `Q_H<=b+4B`. On the common interval of length `min(a,b)`, both counts are positive, and the full cross integrand, including its prefactor two, is at least `1/4`. Hence `J_O>=min(a,b)/4`.

The lines `1+delta` for `delta>=0` and `1+delta/2` for `delta<=0` underlie `phi`. Substituting `C=1+Q_L-Q_H/2+A+B` gives exactly

```
T<=A+B+(1/2)min(Q_L,Q_H).
```

All these arguments permit empty groups, zero deviations, and ties at one-half.

## All-high lemma

Order high deviations decreasingly and write `a=q_1`, `R=Q-a`, and `b0=sum_i 2^(-i)q_i`. Then `C_H=1-b0`. If `Q<=1`, the exact high gap is `T_H=Q/2-b0=B`, and `T_H>=R/4`. The two-term Bonferroni upper bound for the independent product yields

```
D_(I,H)>=T_H-(aR+R^2/2)/4
        >=(1-a-R/2)T_H
        >=T_H/4.
```

The middle inequality uses `R<=4T_H`; it is not a reversal of that estimate. The final inequality follows from `R<=1-a` and `a<=1/2`. The zero-tail case gives `T_H=0` and is harmless.

For `Q>=1`, maximizing `b0` under `q_i<=1/2` fills the largest weights first. Linear interpolation and convexity give `C_H>=1/2+(1/2)4^(-Q)`. Independence gives `P_H<=exp(-Q/2)`. Their difference `g(Q)` increases for `Q>=1`, as the derivative calculation in the note shows. This can also be checked without decimal estimates using `e<4` and `log 2<1` in the derivative comparison. Finally,

```
exp(1/2)>79/48>64/39
```

gives `g(1)=5/8-exp(-1/2)>1/64`. Thus the absolute deficiency bound, not merely a relative bound, is valid in this case. The failed factor-two all-high example is correctly retained and is not used as a lemma.

## Mixed cases and the constant 67

When `Q_H<=1`,

```
min(Q_L,Q_H)<=min(a,b)+A+4B
```

implies `T<=3A/2+3B+2J_O`. Applying `A<=2D_(O,L)` and `B<=4D_(I,H)` gives `T<=3D_O+12D_I`.

When `Q_H>=1`, independence gives `J_I>=Q_L(1-exp(-Q_H/2))>=Q_L/3`. Also `C_H<=1`, `V>=0`, and the absolute all-high bound imply

```
T<=1+A+Q_L<=64D_(I,H)+2D_O+3J_I<=64D_I+2D_O.
```

Combining the two cases proves `T<=64D_I+3D_O`. At `Q_H=1` both valid arguments apply; there is no missing boundary case.

The independent and orientation laws are each defined globally using the full vector of means. Restricting either law to a monomial gives exactly the expectation used in the proof. Mixing them with probabilities `64/67` and `3/67` therefore gives one common feasible law whose deficiency from each monomial's concave envelope is at least its local gap divided by 67. The normalization factor `2^h` can be restored separately in every monomial because this inequality is homogeneous; the mixture weights themselves remain unchanged.

Positive coefficients permit summation. Common-threshold rounding simultaneously attains the polynomial's upper envelope, while the mixture is a feasible candidate for its lower envelope. Consequently the hull gap is at least the sum of local gaps divided by 67. Affine terms have fixed expectation and cancel; zero hull gap forces zero termwise gap through the same inequality. This proves the advertised scope without assumptions on monomial overlap.

## Independent exact checks and limitations

I wrote and ran [audit-positive-box-67.py](../code/audit-positive-box-67.py). It computes concave and orientation expectations directly from their full normalized-mean integrals, then independently checks the low/high formulas, decompositions, intermediate bounds, branch-specific bounds, and final inequality. All 1,043 exact rational cases passed: all quarter-grid multisets through degree seven, 250 skewed hundredth-grid cases through degree 30, and the recorded troublesome three-coordinate example. No floating-point tolerance or sampled maximum is a proof premise.

The result addresses the original monomials on the physical positive box. It does not follow merely by rescaling the unit-cube theorem, and it does not assert the conjectured sharper factor four. The distinction between these exact physical envelopes and termwise relaxation after affine expansion is preserved throughout the proof.

## Subsequent audit: arbitrary fixed ratio

I separately checked the complete general proof in [the canonical result](../results/positive-multilinear-positive-box.md). Put `t=rho-1`, `eta=1-1/rho`, and `alpha=1/rho`. The same normalization now divides a monomial by `rho^h`. Its exact convex envelope becomes `phi_rho(Q_L-Q_H)` by integer translation, and the two common global laws retain their definitions.

The new integer count bounds are valid: the degree-two binomial term gives `rho^L-1-tL>=t^2(L-1)_+`, and successive increments of `alpha^H-1+eta H` beyond `H=1` are at least `eta^2`. Hence `A>=t^2(Q_L-q_L)` and `B>=eta^2(Q_H-q_H)`. The orientation calculation gives `D_O>=A/2+J_O` and `J_O>=t eta min(q_L,q_H)/2`.

For `Q_H<=1`, the same Bonferroni argument uses `B>=eta^2 R` and proves `D_IH>=B/4`. For `Q_H>=1`, saturation at the deviation cap `1/2` yields

```
D_IH >= g(Q_H),
g(Q)=1/2+alpha^(2Q)/2-exp(-eta Q).
```

The monotonicity argument is correct. Since `-log alpha<=eta/alpha`, its derivative is at least `eta[exp(-eta Q)-alpha^(2Q-1)]`. Also `alpha<=exp(-eta)` and `2Q-1>=Q` for `Q>=1`, so this derivative is nonnegative. The fourth-order Taylor upper bound for `exp(-eta)` gives

```
g(1)=1-eta+eta^2/2-exp(-eta)
    >=eta^3/6-eta^4/24>=eta^3/8>0.
```

The left and right slopes of `phi_rho` at zero are `eta` and `t`. Thus `T<=A+B+t eta min(Q_L,Q_H)`. Using `t/eta=rho`, the small-high-mass case gives

```
T<=2(1+1/rho) D_O+4(1+rho) D_I.
```

In the large-high-mass case, `J_I>=t eta Q_L/2` and `T<=1+A+tQ_L`, so

```
T<=2D_O+8eta^(-3)D_IH+2eta^(-1)J_I
 <=2D_O+8eta^(-3)D_I.
```

These prove the canonical constant. The stronger version using

```
g_rho=1-eta+eta^2/2-exp(-eta)
```

also passes: `g_rho<=1-exp(-eta)` because `-eta+eta^2/2<=0`. Hence `1/g_rho` dominates both the constant-term cost through `D_IH` and the cross-term cost through `J_I`. The resulting audited constant is

```
2(1+1/rho)+max{4(1+rho),1/g_rho}.
```

## Subsequent audit: nonuniform boxes and the bound 45/2

The co-developer proposed transferring the general-ratio result to any positive box with coordinate aspect ratios at most an ambient `R`. This step is valid, but needs positive affine expansion rather than an unsupported monotonicity claim under box inclusion.

For a coordinate interval `[a_i,b_i]`, take `w_i` in `[1,R]` and set

```
s_i=(b_i/a_i-1)/(R-1),
x_i=a_i[(1-s_i)+s_i w_i].
```

If `b_i/a_i<=R`, then both affine coefficients are nonnegative. After removing fixed coordinates, this is a bijection of the boxes. Expanding any original positive monomial gives a positive sum of monomials in `w`. Their concave envelopes are simultaneously attained by the same threshold law, so their upper-envelope sum equals the original monomial's upper envelope. Their summed convex envelopes are at most the original monomial's convex envelope, because the infimum of a sum is at least the sum of the infima. Therefore the original termwise gap is at most the termwise gap of the fully expanded positive polynomial. The full graph-hull gap is invariant under the affine coordinate bijection. The general-ratio bound applied to the expansion consequently proves the same bound for the original monomials. This is an existence proof and makes no claim that explicitly forming the expansion is polynomial time.

Finally choose `R=max{4,max_i b_i/a_i}`. Even the simpler canonical bound suffices: since `1-1/R>=3/4`,

```
8(1-1/R)^(-3)<=512/27<20<=4(1+R).
```

Its audited constant therefore simplifies to

```
4R+6+2/R.
```

In particular, every positive box with aspect ratio at most four, including `[1,2]^n`, has gap ratio at most `45/2`. This improvement passes the independent audit. It leaves the original bound 67 valid but supersedes it as the strongest constant verified in this review. No claim of optimality or literature novelty follows.
