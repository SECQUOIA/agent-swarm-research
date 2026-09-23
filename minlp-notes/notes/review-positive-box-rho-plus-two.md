# Independent audit of the rho-plus-two positive-box bound

Date: 2026-09-04. Reviewer: `review_extension`. Status: the coefficient lemma, physical-box bound, and unequal-box transfer passed a complete independent audit. This does not certify literature priority or exact finite-ratio optimality.

Reviewed [the complete coefficient proof](positive-box-rho-plus-two-proof.md), including the revised finite-spread argument, and completed a final reread of [the canonical result](../results/positive-multilinear-positive-box-sharp.md). The conclusion is valid:

```
termwise_gap <= (rho+2) * hull_gap
```

for every positive multilinear polynomial on a strictly positive box whose coordinate aspect ratios are at most `rho>1`. In particular, the bound on `[1,2]^n` is four. The proof has no dimension, degree, support, overlap, or positive-coefficient restriction beyond those stated.

## Moment definitions and the physical envelope

For each rounding law, the elementary symmetric moment is `E binom(K,j)`, with `K` the binary success count. The common-threshold moment is the sum of the subset minima, the independent moment is the elementary symmetric polynomial in the means, and the orientation moment uses one common uniform variable plus independent fair endpoint choices. All four order-zero moments equal one, negative orders are zero, and moments above the dimension are zero. These conventions make the proposed coefficient formula valid also at its lower and upper indices.

The balanced-cardinality law for `V_j` exists with the complete vector of prescribed marginals: the vector lies in the cube slab between its two adjacent integer total sums, and that slab is integral. A fractional vertex would either have two fractional coordinates admitting a sum-preserving perturbation, or a single fractional coordinate that cannot be forced by an integer sum bound. Therefore the prescribed vector is a mixture of binary vertices on those two cardinality levels.

This law minimizes the expected physical product `(1+t)^K`, because its piecewise linear interpolation in the integer count is convex. The same reasoning applies to each `binom(K,j)` for `j>=2`, whose second discrete differences are nonnegative. The order-zero and order-one cases have fixed expectations. Consequently `V(t)=sum_j V_j t^j` is the exact physical convex-envelope value, rather than a sum of potentially incompatible lower envelopes.

Common-threshold rounding attains every positive subset product's upper envelope simultaneously, so `C(t)=sum_j C_j t^j` is the exact physical concave value. Independence and orientation supply feasible expectations `P(t)` and `O(t)` with the same expansion. Thus the coefficient of `t^j` in

```
(rho+1)C+V-rho P-2O=(2+t)C+V-(1+t)P-2O
```

is precisely

```
F_(n,j)=2C_j+V_j-P_j-2O_j+C_(j-1)-P_(j-1).
```

There is no missing coefficient from the factor `rho=1+t`.

## Base orders and boundary recursion

The formulas give `F_(n,0)=F_(n,1)=0`. At order `n+1`, only `C_n-P_n` remains, and it is nonnegative because `prod u_i<=min u_i`. Higher orders vanish.

For order two, equal endpoint orientations of a pair produce intersection probability `min(u_i,u_k)`, and opposite orientations produce `max(0,u_i+u_k-1)`. Both orientation patterns have probability one-half. Hence `2O_2=C_2+L_2`. The proposed decomposition

```
F_(n,2)=(C_2-P_2)+(V_2-L_2)
```

is correct. The first term is nonnegative by the pairwise upper bound. Every joint law with the prescribed marginals, including the balanced-cardinality law, satisfies each pairwise lower bound; summing proves the second term is nonnegative. This does not assume that all pairwise lower bounds can be attained simultaneously.

A zero-mean coordinate is deterministically zero under all laws, so deleting it leaves every moment unchanged. A one-mean coordinate adds one to the count under every law, including the balanced-cardinality law. Pascal's identity therefore gives

```
F_(n,j)(u,0)=F_(n-1,j)(u),
F_(n,j)(u,1)=F_(n-1,j)(u)+F_(n-1,j-1)(u).
```

These statements include the dimension-overflow orders under the stated zero conventions. Dimension one has identical expectations under every law and zero coefficients. Thus the boundary step of induction is complete.

## Finite spreading of a global minimum and maximum

For the remaining orders `3<=j<=n`, choose distinct coordinates carrying a global minimum `x` and maximum `y`, then move to `x-h,y+h`, where `0<=h<=min(x,1-y)`. If all means are equal, any two different coordinates may be chosen. Their roles as a minimum and maximum persist throughout the move. The total mean is unchanged, so `V_j` is unchanged, including when the total is an integer.

For every common-threshold moment of order at least two, reducing the chosen global minimum reduces the minimum of each subset containing it by exactly `h`; increasing the chosen maximum does not change any subset minimum of size at least two. This remains true at ties. Therefore, writing

```
A0=binom(n-1,j-1),   B0=binom(n-1,j-2),
```

the change in `2C_j+C_(j-1)` is exactly `-h(2A0+B0)`. The restriction `j>=3` is essential because it ensures both common-threshold moments have order at least two; order two was already handled separately.

Writing `E_k` for an elementary symmetric polynomial of the remaining `n-2` means gives the exact product-moment change

```
Delta(P_j+P_(j-1))=-h(y-x+h)(E_(j-2)+E_(j-3)).
```

The multiplier `y-x+h` lies in `[0,1]`, and each remaining mean lies in `[0,1]`. Pascal's identity then bounds the increase in `-P_j-P_(j-1)` by `h B0`. All quantities have the signs needed in this comparison.

The orientation law admits a direct common coupling when one mean changes. Enlarging one success interval by `h` changes its indicator only from zero to one, with probability exactly `h`, regardless of dependence on the other indicators. On that event, the change in `binom(K,j)` is `binom(K_rest,j-1)`, between zero and `A0`. Thus `O_j` is coordinatewise nondecreasing with coordinate Lipschitz constant `A0`.

First decreasing the minimum and then increasing the maximum proves the finite bound `Delta O_j>=-h A0`. Hence the increase of `-2O_j` is at most `2h A0`. Adding the three comparisons gives

```
Delta F_(n,j)<=-h(2A0+B0)+hB0+2hA0=0.
```

Taking `h=min(x,1-y)` reaches a boundary. Its coefficient is nonnegative by the dimension induction, so the original coefficient is nonnegative too. This proves every remaining order in every dimension.

The finite comparison is a necessary clarification of the original derivative presentation. Ambient partial derivatives of the orientation function need not exist along a prescribed spread line lying in a breakpoint hyperplane, such as a line preserving a complementary pair of means. The revised coupled finite argument proves the required inequality on every line directly. No differentiability or tie-breaking regularity is needed.

The global-minimum/global-maximum restriction must be retained. Arbitrary pairwise spreading need not decrease the coefficient; the note's exact non-Schur-concavity counterexample is correct.

## Polynomial sum and unequal positive boxes

Since every coefficient is nonnegative and `t=rho-1>0`, their finite polynomial sum is nonnegative. Rearrangement gives exactly

```
C-V <= rho(C-P)+2(C-O).
```

There is no division by a local gap. Therefore boundary means and zero gaps are covered. Mixing independence with probability `rho/(rho+2)` and endpoint orientation with probability `2/(rho+2)` gives one global law. Its restriction to every monomial is the law used above. Restoring positive coefficients and summing therefore gives a deficiency of at least the termwise gap divided by `rho+2`. Common-threshold rounding attains the full concave envelope, while the mixture is feasible for the full lower-envelope optimization, so the scalar graph-hull gap is at least that deficiency.

For unequal positive intervals `[ell_i,r_i]` with `r_i/ell_i<=rho`, remove fixed coordinates and apply

```
s_i=(r_i/ell_i-1)/(rho-1),
z_i=ell_i[(1-s_i)+s_i x_i],   x_i in [1,rho].
```

All affine coefficients are nonnegative. Each original monomial expands into positive monomials, and its exact gap is at most their summed exact gaps: the supremum of a sum is at most the sum of suprema, and its infimum is at least the sum of infima. The full graph-hull gap is invariant under the affine coordinate bijection. Applying the proven polynomial bound to the expansion establishes the same `rho+2` constant for the original box. This argument does not assume monotonicity under box inclusion and does not require explicitly constructing an exponential expansion algorithm.

For the stronger statement that the same pulled-back law captures each original monomial's gap, its concave envelope equals the sum of the expanded concave envelopes: common-threshold rounding attains all positive expanded terms simultaneously. Therefore its deficiency under the mixture is exactly the sum of the expanded deficiencies, and the local guarantee also transfers. Sampling the law uses the original endpoint means and does not require forming the expansion.

## Independent exact checks

I wrote and ran [audit-positive-box-coefficients.py](../code/audit-positive-box-coefficients.py). It computes common-threshold and orientation moments by direct exact integration on all marginal and reflected-marginal breakpoints. Conditional orientation moments are computed by an independent elementary-symmetric-polynomial recurrence. The checks do not use the spread formulas to evaluate moments.

All 1,589 cases passed: every quarter-grid multiset through dimension eight, 300 hundredth-grid cases through dimension fifteen, and two additional tied/complementary spread examples. The script checks nonnegativity of every coefficient, the order-two identity, the top-order coefficient, exact boundary recursions, and finite global-minimum/maximum spreading for every relevant order. It also reproduces the reported arbitrary-spreading counterexample exactly, including its increase `231/10000000`.

These finite checks supplement the induction proof. They are not used to infer the result for arbitrary dimension or marginal vectors. The earlier audited positive-box results remain correct, but this bound supersedes their constants. Combined with the separately audited lower bound `max{2,rho}`, it confines the worst gap constant to an interval of additive width at most two for large `rho` and yields constant four on `[1,2]^n`.
