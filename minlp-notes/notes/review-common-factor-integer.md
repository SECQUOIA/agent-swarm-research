# Independent audit of the integer reciprocal-anchor hull

Date: 2026-09-04. Reviewer: common-factor audit agent, independent of the integer extension's author.

Scope: [the integer anchored common-factor hull](../results/common-factor-integer-anchor-hull.md), including exactness, separation, and constructive complexity. The theorem and both telescoping identities pass this audit. Novelty is a separate question and is not certified here.

## 1. The least integer-supported common-factor distribution

Let `C_*` be the least continuous feasible call function from the independently reviewed continuous theorem. For any law supported on the integers, its call function is affine on every unit interval, including intervals containing no positive mass. If it dominates `C_*` at the two endpoints of a unit interval, it must dominate the chord interpolating those values throughout that interval. Thus every feasible integer call function dominates the stated `C_Z`.

Conversely, the chords through the sampled values of a convex function form a convex piecewise affine function. Here all secant slopes remain in `[-1,0]`; the exterior pieces join correctly because McCormick gives `C_*(a)=m-a` and `C_*(b)=0`. Therefore `C_Z` is a call function of a probability distribution on the permitted integers with mean `m`. Its chord segments dominate `C_*`, so it permits every leaf moment by the threshold-submeasure criterion.

The rounding construction gives exactly this law. At any integer strike `k`, the hinge `(X-k)_+` is affine on every unit interval `[j,j+1]`, including when its kink is an endpoint. Replacing an atom inside that interval by its mean-preserving endpoint mixture leaves its expected hinge value unchanged. Hence the rounded law agrees with `C_*` at all integer strikes and has precisely `C_Z` as its call function.

This proves minimality in convex order. The reciprocal is convex on the positive interval, so the rounded law minimizes its expectation among all feasible integer laws. The endpoint law maximizes it, remains feasible for every leaf, and is integer-supported. Mixtures cover every intermediate reciprocal value while retaining the call-function lower bounds. No discrete support point is being implicitly omitted.

## 2. The discrete reciprocal formula and telescoping sums

The reciprocal interpolant has first slope

```
f(a+1)-f(a) = -1/[a(a+1)].
```

Its slope jump at an interior integer `k` is

```
d_k = 1/(k-1)-2/k+1/(k+1)
    = 2/[k(k^2-1)] > 0.
```

Consequently its hinge expansion, and thus formula (2) in the result note, is correct. The two summation identities follow directly from

```
d_k = [1/(k-1)-1/k] - [1/k-1/(k+1)],
k d_k = 1/(k-1)-1/(k+1).
```

Summing over `L,...,R` yields exactly the displayed endpoint expressions. The possible ranges always have `L>=a+1>=2`, so their denominators are nonzero. Positive endpoints and the consecutive-integer assumption are essential to the displayed formulas.

For `b=a+1`, the interior hinge sum is empty. The initial affine interpolant then equals the reciprocal secant, so the lower and upper reciprocal bounds coincide. For `n=0`, the envelope is `max(0,m-s)` and the rounded law is the usual adjacent-integer mixture preserving `m`. The theorem correctly adds `a<=m<=b` explicitly in this case. The excluded case `a=b` is a trivial linear hull if desired; it must not be evaluated with formulas involving a nonexistent first unit interval.

## 3. Separation and bit complexity

The upper envelope has `O(n+1)` pieces. Assigning every interior integer to one of its active pieces produces `O(n+1)` runs; if a breakpoint is an integer, either tied line may own that integer. The two lines have the same value at the candidate, and both remain valid global lower bounds on the maximum. Thus tie choices do not affect tightness or validity.

At a candidate, fixed run boundaries plus fixed active-line choices turn the telescoped hinge sum into an affine function of `(m,q,w)`. Every omitted maximum is replaced by a globally smaller affine function and every weight is positive. Therefore the resulting cut is globally valid and tight at the candidate, which establishes exact separation when `t<T_Z`.

No loop over the scalar range is required: build the continuous envelope, round its breakpoints to determine integer runs, and apply the endpoint sums once per run. All breakpoint and run-endpoint numerators and denominators have polynomial bit length. Reciprocals of possibly large integer endpoints have bit length proportional to the encoded endpoints; taking their rational sums does not introduce dependence proportional to the range width. The claimed polynomial bit complexity is therefore justified. For the degenerate `n=0` count, interpret the stated envelope complexity as constant work, or use `O((n+1) log(n+2))` uniformly.

## 4. Constructive decomposition

The continuous least law has at most `2n+1` atoms, so rounding produces at most `4n+2` atom locations before aggregation. Mixing with the two endpoint locations gives at most `4n+4`. This is a valid bound, including zero-mass and coincident-location cases; no minimality claim is needed.

For rational candidate data, continuous-envelope atoms and masses are rational, their rounding weights are rational, and the mixture weight fixing `t` is rational. If the lower and upper reciprocal extrema coincide, simply keep the least law instead of dividing by a zero interval length.

For each leaf, its lower and upper threshold selections on this finite law have rational probabilities and moments. Interpolating between these selections gives the desired first moment `w_j` at mass `q_j`; if the two endpoint moments coincide, either selection suffices. Set the continuous leaf to that selection value at each scalar atom. This yields a polynomial-size rational convex combination of original integer-scalar graph points.

## 5. Binary leaves preserve both anchored hulls

**Additional checked corollary.** The continuous and integer anchored hulls are unchanged if any subset of the leaves is required to be binary, provided there are no additional restrictions coupling the leaves or restricting their products.

To prove this, take any one scalar atom with continuous leaf vector `theta in [0,1]^n`. Let `B` be the set of binary leaves. Keeping all other leaves at their original values, choose a common `U` uniform on `[0,1]` and set

```
Y_j = 1{U<=theta_j},  j in B.
```

Then `E[Y_j]=theta_j` and, since the scalar is fixed at this atom, `E[XY_j]=X theta_j`. Sorting the `|B|` thresholds divides `[0,1]` into at most `|B|+1` intervals, yielding that many binary patterns with nonnegative weights. Their weights are rational when `theta` is rational. This is an explicit finite decomposition, without enumeration of all binary patterns.

Apply it at each scalar atom. The continuous hull therefore has a rational decomposition with at most `(2n+3)(|B|+1)` original points, and the integer hull with at most `(4n+4)(|B|+1)`. This proves polynomial-size decomposition for binary leaves as well as exact hull preservation. The result note's original exclusion of all integer-valued leaves can accordingly be narrowed; the checked corollary concerns binary leaves, not arbitrary integer constraints or linking restrictions.

The binary endpoint replacement itself is elementary and should not be presented as a novelty claim.
