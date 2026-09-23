# Independent audit: degree-independent pure-power integer count

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**Status: PASS for the stated finite real-coefficient result and the separately stated compact rational bound.** Reviewed [the candidate](pure-power-degree-independent-integer-count.md). This audit establishes mathematical consistency; it does not certify literature novelty or a compact rational construction attaining the stronger finite bound.

## Lower bound

For `D>=2`, convexity of `x^(D/2)` implies

```
((a+b)/2)^D <= ((a^(D/2)+b^(D/2))/2)^2,
```

which gives the claimed Jensen lower bound with coefficient `1/4`. It holds for odd as well as even degrees, including either endpoint zero.

Take closures of graph contact supports for each integer parity class before applying the coordinate homeomorphism `t_i=x_i^(D_i/2)`. Continuity and closedness of the error body preserve the pairwise Jensen condition. The images remain compact and cover the transformed unit cube. Positive-volume images have a positive definite covariance; zero-volume images require no volume estimate. No Jacobian estimate or preservation of original volume is needed.

For independent uniform transformed points, the expected squared coordinate difference is `2 Sigma_ii`. Therefore `(1/2) C diag(Sigma)` is coordinatewise dominated by an expected nonnegative Jensen vector in `K`. Convexity, compactness and unconditionality justify feasibility of `p_i=Sigma_ii/2`; `Sigma_ii<=1/4` gives the allocation cap. The standard covariance volume inequality and Hadamard yield the stated support-volume factor `2^(r/2) omega_r(r+2)^(r/2) sqrt(D_alloc)`. Covering by at most `2^p` supports gives `p>=Phi-A_r`.

The allocation optimum exists on a compact set and has positive determinant because zero lies in the interior of `K`. Thus it is valid to use a positive optimal allocation in the upper bound. The Gaussian unit-ball bound gives `A_r<7r/2` for every positive integer `r`.

## Chord estimate and formulation

The split into `A<=B/2` and `A>B/2` is exhaustive. In the first case the chord is bounded by `B^2<=4(B-A)^2`. In the second case the second-derivative interpolation bound and the mean-value inequality give the displayed coefficient

```
[(D-1)/(2D)] (b/a)^(D-2).
```

Here `(b/a)^(D/2)<2` and `D-2>=0`, so the coefficient is at most `2`. This also handles `D=2`. Consequently the deliberately weaker uniform constant `4` is valid for all degrees.

On each nonuniform cell, `chord-f` lies in `[0,4h_i^2]`. The proposed band therefore contains the exact graph and bounds the absolute approximation error by `4h_i^2`, not by twice that quantity. Shared scalar variables across outputs ensure coordinatewise output error at most `Cp`; unconditionality then gives membership in `K`.

The Hamming-distance formulation correctly encodes the union of all cell bands with exactly `L_i` bits per coordinate. Global bounds `0<=x_i<=1` and `-1<=z_i<=1` suffice, since `L_i>=1` and hence `4h_i^2<=1`. Every cell inequality has finite maximum violation on this box, so finite real big-M constants exist. Each binary word activates one complete cell, and constraints for all other cells can be made redundant. There is no Cartesian product enumeration across coordinates and no additional integer variable.

The ceiling estimate gives `sum L_i<=Phi+2r`. The real, generally irrational knots and the potentially exponential number of cells are explicitly outside any polynomial-bit-size claim. Combining the lower and upper bounds gives the degree-independent overhead `11r/2`. The inherited compact rational upper bound instead retains `sum log2 D_i`; its comparison constant `9r/2+1` follows correctly from the improved lower bound.

A minor presentation detail was sent to the author: there are `O(sum_i 2^(L_i))` rows for four inequalities per cell; the nonzero coefficient count can have the additional factor `L_i`. The candidate's larger row-count wording does not invalidate any claim.

## Independent exact checks

An independent Python `Fraction` check verified **8,316** chord and Jensen cases. It used rational squared endpoints so that the transformed endpoints are rational even at odd degrees, all degrees `2,...,32` plus `50` and `100`, and seven interior convex combinations for each endpoint pair. Every inequality passed. These finite checks supplement the complete symbolic arguments above.

## Scope

The result needs a single common exponent per coordinate across outputs, nonnegative coefficients, the original nonnegative cube, and an unconditional convex error body. It does not establish the same degree-independent allocation law for arbitrary mixtures of powers on one coordinate. No new algorithmic or literature claim beyond the explicitly bounded candidate was audited here.
