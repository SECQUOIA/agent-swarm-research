# Exact anchored common-factor hull for an integer scalar

Date: 2026-09-04.

Status: proved and independently audited on 2026-09-04, including the telescoping separator, endpoint cases, and binary-leaf corollary. No publication novelty claim. This extends the independently reviewed continuous [full anchored hull](common-factor-reciprocal-anchor-full-hull.md) to a complete mixed-integer hull with an arbitrarily large binary-encoded scalar range.

Independent audit: [integer common-factor review](../notes/review-common-factor-integer.md).

## Statement

Let `1<=a<b` be integers and define

```
K_Z = conv{(X,1/X,Y,XY): X in {a,a+1,...,b}, Y in [0,1]^n}.
```

For a candidate `(m,t,q,w)`, impose the same McCormick bounds as in the continuous theorem and form

```
C_*(s)=max{0,m-s,w_j-q_j s,m-w_j-(1-q_j)s : j=1,...,n}.
```

Let `mu_*` be the least common-factor law obtained from the slope jumps of `C_*`. Replace every atom at a noninteger `r` by atoms at `floor(r)` and `ceil(r)`, in the unique proportions preserving its mass and mean. Keep integer atoms unchanged. Write the resulting law as `mu_Z` and define

```
T_Z(m,q,w)=E_mu_Z[1/X].
```

**Theorem.** A candidate belongs to `K_Z` exactly when it satisfies the McCormick inequalities and

```
T_Z(m,q,w) <= t <= (a+b-m)/(ab).                       (1)
```

For `n=0`, also impose `a<=m<=b`; these bounds otherwise follow from McCormick. Membership, exact rational separation, and a rational convex decomposition are computable in polynomial bit time, including polynomial dependence on `log(b-a+1)`. One need not enumerate all integer scalar values. The upper-envelope computation uses `O(n log n)` rational operations; its least-law support has `O(n)` atoms before and after rounding.

## Proof of exactness

The continuous full-hull theorem proves that a law on `[a,b]` realizes all leaf moments if and only if its call function dominates `C_*`. Every law supported on integers has a call function that is affine between consecutive integers. Hence it dominates the piecewise linear interpolation

```
C_Z(s) = linear interpolation of C_*(k), k=a,...,b,
```

extended as `m-s` below `a` and zero above `b`. The interpolation is convex because the sampled sequence comes from the convex function `C_*`, so it is a valid integer-supported call function. It also dominates `C_*`, because a convex function lies below every chord.

Mean-preserving rounding constructs exactly this call function. For every integer `k`, the hinge `(r-k)_+` is affine on each interval `[j,j+1]`. Rounding an atom within that interval therefore leaves its call value at `k` unchanged. The rounded law has call function `C_*` at all integer knots, and its call function is affine in between them. It follows that its call function is `C_Z`.

Thus `mu_Z` is the least feasible integer-supported law in convex order. In particular it minimizes the reciprocal moment. The endpoint law on `{a,b}` is integer-supported and maximizes that moment. Mixing the two laws realizes every `t` in (1), and the mixture still permits all leaf moments. The threshold selection construction in the continuous theorem produces leaf values on its atoms, hence a finite convex combination of points with integer `X`. This proves exactness.

The continuous least law has at most `2n+1` atoms. Rounding doubles this number at most, and adding the endpoint law gives at most `4n+4` atom locations. On these locations, the leaf threshold/interpolation construction uses rational arithmetic for rational candidate data. This yields a polynomial-size rational convex decomposition. No optimal support-cardinality claim is made. ∎

## Exact separation without enumerating integers

Let `g` be the linear interpolant of `1/k` on the integer knots. Then `g` is convex and

```
T_Z = E_mu_*[g(X)]
    = 1/a + (1/(a+1)-1/a)(m-a)
      + sum_{k=a+1}^{b-1} d_k C_*(k),                 (2)
d_k = 1/(k-1)-2/k+1/(k+1) = 2/[k(k^2-1)] > 0.
```

The first equality is the definition of mean-preserving rounding; the second is the hinge expansion of the convex piecewise linear function `g`.

Although the sum in (2) may have exponentially many terms, the active line of `C_*` changes only `O(n)` times. On a consecutive run of integers `L,...,R` with active line `U-V k`, compute the contribution in constant many rational operations using

```
sum_{k=L}^R d_k
  = 1/(L-1)-1/L-1/R+1/(R+1),

sum_{k=L}^R k d_k
  = 1/(L-1)+1/L-1/R-1/(R+1).                         (3)
```

Only runs inside `{a+1,...,b-1}` are used. Their endpoints are obtained by rounding upper-envelope breakpoints and resolving ties consistently. Empty runs are skipped. When `b=a+1`, there is no sum and both bounds in (1) coincide, as expected for a scalar with two allowed values.

For a separating cut, retain the active line assigned to each integer run at the candidate, treat run endpoints as fixed, and substitute those affine lines for `C_*(k)` in (2). Since every `d_k` is positive and every chosen line lies below the maximum for all other candidates, the resulting affine function is a global lower bound for `T_Z`, tight at the candidate. Equation (3) computes its rational coefficients without expanding the run. Therefore a violated lower bound produces an exact rational linear separator in polynomial bit time. The remaining separators are McCormick bounds and the reciprocal secant.

## Scope and novelty limits

**Binary-leaf corollary.** The hull is unchanged if any subset of the normalized leaves is restricted to `{0,1}`. At each scalar atom, let their current continuous values be `theta_1,...,theta_r`. A common uniform threshold `U in [0,1]` and assignments `Y_j=1{U<=theta_j}` preserve each leaf's mean and its product with that fixed scalar. Sorting the `r` threshold values gives at most `r+1` binary patterns and rational weights. Thus the polynomial decomposition can also be converted to a polynomial-size decomposition into points with the requested binary leaves. This argument applies equally to the continuous-scalar hull. It does not preserve additional relationships between the leaves or their products.

The scalar range is an interval of consecutive integers. The proof also applies to an explicitly listed finite ordered scalar set by interpolation between adjacent allowed values, but its complexity then depends on that list's length. No claim is made for arbitrary succinctly specified scalar subsets or additional linking restrictions.

Mean-preserving rounding, convex order, and piecewise linear interpolation are established tools. The possible contribution is their combination with the full common-factor hull and a telescoping rational separator whose complexity depends on the encoded range rather than the number of allowed scalar values. The [focused anchor comparison](../notes/common-factor-anchor-novelty.md) also treats the integer and binary-leaf extensions; it identifies an elementary polynomial optimization route and does not establish priority for the more explicit separator. See the [common-factor literature audit](../notes/common-factor-literature-audit.md) for the continuous theorem's classical foundations.

## Computational verification

`code/common-factor-anchor-verify.py` checked 120 seeded instances with up to eight leaves and integer scalar support `{1,...,11}`. The rounded-envelope reciprocal value matched an independent LP that enumerates all eleven allowed scalar values and explicitly enforces shared masses, leaf submeasures, and target moments. Exact rational threshold decompositions and the telescoping formula were also checked. The LP comparisons are numerical, while the formula and decomposition comparisons use exact `Fraction` arithmetic. These tests support the proof; they do not establish novelty.

An additional exact-arithmetic check used `10^12` permitted scalar values. The telescoping formula and atom rounding agreed using four envelope pieces and five integer atom locations, without enumerating the scalar range.
