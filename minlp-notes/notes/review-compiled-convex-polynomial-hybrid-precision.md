# Independent audit: compact formulations for dense convex polynomials

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**Status: PASS for the complete `p_out<=p_conv+11` scalar theorem and the Section 5 separable transfers (`16r` for sums, `13r` for independent outputs).** Reviewed [the hybrid construction](compiled-convex-polynomial-hybrid-precision.md) and the full [signed monotone-curvature integration dependency](certified-monotone-polynomial-curvature-quantiles.md). The latter dependency is included in this audit, so the conclusion is not conditional on its proof.

The result concerns arbitrary rational dense polynomials convex on the unit interval, with arbitrary coefficient signs and arbitrary curvature monotonicity. It establishes polynomial rational construction and total encoding length. It does not establish sparse binary-degree complexity, practical formulation size, or literature novelty.

## Rational grid and greedy branch

The displayed derivative bound dominates the absolute derivative throughout the domain. Its binary length is polynomial, and the required dyadic exponent `B` is polynomial in the input and tolerance lengths. The uniform grid is accessed through indices; it is not enumerated.

The interval perturbation bound is valid. At either original endpoint, the expanded chord differs from its endpoint function value by at most twice the derivative bound times the added length. This follows from the chord slope bound and the function Lipschitz bound. Linear interpolation carries this `2Mh` difference across the original interval. On either added strip, comparison to its outer endpoint gives chord error at most `2Mh` directly. Thus every subinterval of the expansion has error at most `eta+2Mh`.

Discarding duplicate rounded knots does not invalidate the rounding argument. Between consecutive distinct rounded values, take the last original knot in the first constant run and the immediately following original knot. They are adjacent in the original partition and round to the two desired values. The rounded interval lies in their original interval expanded by at most `h` at each end. Consequently the grid partition has at most `N_(epsilon/4)` intervals and error at most `5epsilon/16<epsilon/2`.

Every one-step grid interval is feasible. Feasibility of extending a fixed left endpoint is monotone in the right endpoint because chord error decreases on restriction of a convex interval. The exact rational sign predicate is therefore suitable for binary search. The chord denominator is at least the grid spacing, so its coefficient bit length is polynomial; exact polynomial evaluation at grid points also has polynomial bit length under dense degree encoding. Root isolation and sign testing decide the nonpositive predicate, including equality and multiple-root cases. There is no numerical comparison of a maximum against the tolerance.

The greedy minimality argument is correct. If its previous endpoint is no earlier than the corresponding endpoint of any feasible grid partition, either that partition's next endpoint has already been passed or its remaining suffix is a feasible extension of the greedy interval. The largest feasible extension therefore reaches at least that next endpoint. Induction proves optimality among feasible grid partitions.

Hence the full greedy count satisfies `G<=N_(epsilon/4)<=9N_epsilon`. Finishing within `9D` cells gives an explicitly enumerable polynomial-size family and count at most `p_conv+5`. Not finishing means the full greedy count is strictly above `9D`; therefore `N_epsilon>D`. The algorithm does not need to compute the latter optimum. The threshold test has polynomial cost because it performs only `9D` iterations, each with polynomially many exact index decisions.

## Curvature pieces and total count

For nonzero `f'''`, distinct interior roots can be enclosed in disjoint rational brackets of width at most `h`, with endpoints that are not roots. Rational roots can be enclosed strictly instead of left as singleton intervals. Refinement to keep brackets inside the unit interval and away from one another requires polynomially many bits: apply the same integer root-separation bounds to the derivative polynomial augmented with factors at zero and one. Endpoint roots do not require brackets. The zero derivative polynomial is treated separately.

Between brackets, the third derivative has constant sign, so curvature is monotone and nonnegative. On each bracket the global Lipschitz estimate gives chord error at most `epsilon/16`, requiring only one cell. The total number of positive-length pieces is at most `3D`, including low-degree cases. An affine normalization preserves vertical error, and reflection changes decreasing nonnegative curvature into increasing nonnegative curvature. The normalized polynomial remains densely represented with polynomial rational coefficient lengths.

Splitting an optimal global epsilon partition at the piece boundaries gives `sum n_j<=N_epsilon+b-1`. The local monotone compiler has `K_j<=120n_j+2`, including zero-depth cases; the one-cell brackets obey the same loose bound. Thus

```
K_total<=120N_epsilon+122b<=120N_epsilon+366D<486N_epsilon.
```

The strict last inequality is licensed by the failed greedy branch. Combining with `N_epsilon<=3*2^p_conv` gives `K_total<1458*2^p_conv<2048*2^p_conv`. The ceiling logarithm therefore proves the stated eleven-bit overhead. No factor equal to the number of pieces is multiplied by the largest local grid count.

## One global index and rational decoding

Local cell counts and their prefix sums have polynomial bit length, even when their numerical values are large. A single global index identifies a piece by comparison and its local index by subtraction. Invalid global codes can be excluded by one integer comparison. A bounded deterministic piece-selection computation can branch on that result; equivalently, other local computations can be fed valid dummy indices and their outputs discarded. Neither choice adds declared integer variables.

The common-denominator argument is valid. Let the fixed denominator contain the product of all rational piece-endpoint denominators and `2^Q`, where `Q` bounds every local dyadic precision. Both each endpoint and each endpoint difference times a local dyadic fraction have denominator dividing that product. Therefore it represents every mapped input knot exactly, including reflected pieces. Its bit length is a sum over polynomially many endpoint lengths plus `Q`, and is polynomial.

The output encoding can also be made uniform. Exact evaluation of the dense polynomial at a polynomial-bit rational knot has polynomial bit length. Round downward on a dyadic grid fine enough for error `epsilon/8`, using nonnegative fractional precision. An integer offset strictly larger than `sum |c_k|` makes the encoded rounded values nonnegative: that offset itself lies on the dyadic grid, and every exact function value lies strictly above its negative. The encoded numerator length and its linear decoding coefficients remain polynomial. Thus a large value offset does not require extra integer variables or an exponential coefficient encoding.

The standard acyclic gate constraints force all internal wires to their Boolean values when the global index bits are integral. Endpoint-bit products with the common interpolation parameter are exact. Each cell is decoded as its own two local endpoints; it need not connect to the next piece in a global polygonal ordering. This matters for reflected pieces: each local path covers its interval, and their union covers the domain regardless of orientation.

The true chord errors are at most `13epsilon/16`, while endpoint rounding contributes a downward error at most `epsilon/8`. The stated band therefore contains the full exact graph and permits only absolute error at most `15epsilon/16`. This remains valid in the small greedy branch, whose true chord bound is tighter. The affine case can be returned exactly without integers.

## Signed monotone-curvature integration

For nonzero nonnegative nondecreasing polynomial curvature, a positive interior zero would force vanishing on a nonempty interval and hence identically. Thus the normalized curvature `H` is positive on `(0,1]`. The cutoff, bounded density, branch-root isolation, and polynomial-branch integration from the previously reviewed routine remain valid without coefficient positivity.

The local rational Taylor test is a correct sufficient analytic certificate. If the sum of nonconstant Taylor coefficient magnitudes times `ell^k` is at most `H(c)/2`, then the entire radius-`ell` complex disk has `Re H>=H(c)/2>0`. The principal square root is holomorphic there, with the stated modulus bound `2U`.

The polynomial-size adaptive-tree proof is sound. Factoring `H(c+t)/H(c)` over its complex roots bounds the normalized Taylor coefficient sum by `product(1+ell/|c-alpha_j|)-1`. If every distance is at least `8d ell`, this is below one half. Failure therefore places the center within `8d ell` of the real part of some root. At a fixed bisection depth the centers are equally spaced by `ell`, so each root accounts for at most `16d+2` failed intervals. At most `d(16d+2)` intervals fail at each depth.

The explicit square-free height and separation estimates are conservative but valid. The primitive square-free part's leading coefficient divides that of the primitive original polynomial. The Cauchy root bound and expansion of the square-free factor give coefficient height at most the stated `2^B`. Its nonzero integer discriminant then gives the weaker separation `2^(-(B+2)n^2)` after bounding all other root differences and the leading coefficient. The artificial roots zero and one ensure separation from real roots outside the interval; conjugate-root separation controls the imaginary part of every nonreal root. Roots at or below zero are at least the cutoff distance away. Hence the distance to all curvature roots is at least `min(lambda,sigma/2)`.

At polynomial depth `K`, every interval is short enough to pass the test. Combining this depth with the polynomial number of failures per depth gives `O(d_0^2 K+1)` total nodes, rather than an exponentially fine uniform mesh. Exact Taylor coefficients at dyadic centers have polynomial rational lengths, so each test and the whole adaptive construction have polynomial bit cost. The constant-curvature case passes immediately.

Intersecting accepted panels with branch and query intervals preserves the certificate: a retained subinterval's radius-equal-to-length disk lies inside the accepted disk. The earlier length-summed Gaussian error bound therefore applies with the same constants. For signed coefficients, the rational derivative bound `sum k|H_k|` replaces the coefficientwise bound. Exact endpoint evaluations still enclose the value at a node because the polynomial is monotone on the real interval. The square-root Hölder inequality supplies absolute value accuracy without a lower bound on the curvature. All remaining quadrature-weight and root-isolation precision arguments were independently verified in the prior integration audit.

The stronger inverse-quantile lemma also survives. The exact positive rational value `H(eta/4)` has polynomial encoding length even when cancellation makes it small. Monotonicity gives the stated lower density on the interior interval, so the same mass-to-input modulus and certified bisection apply. Dependence on the small value enters through its bit length. This closes both the integration and inverse dependencies used by the formulation.

## Independent exact checks

Separate rational checks passed:

- **72 accepted adaptive panels** and **288 rational complex-disk samples** for signed monotone curvature, including substantial cancellation and a small positive constant term.
- **7 greedy-versus-exhaustive-DP comparisons** on a signed convex quartic with nonmonotone curvature.
- **136 interval-expansion checks** for the same quartic, using its sharp derivative bound and an exact algebraic chord-decision comparison.
- **9 global-index and common-denominator cases**, including reflected pieces and a local grid of `2^40` cells, without enumerating that grid.

These checks supplement the uniform symbolic proofs; finite disk samples alone do not certify holomorphy. No substantive mathematical correction was needed. The final theorem retains dense input and convexity of the original polynomial; it does not assert the same result for general nonconvex functions or arbitrary evaluation oracles.

## Final delta: separable dense convex polynomials

The newly added Section 5 was read independently and also passes. In either scalar hybrid branch the actual number of cells is at most `486N_tau`: the enumerated branch has the stronger `9N_tau` bound, and the other branch has the proved large-count estimate. Binary padding gives `2^L<=2K<=972N_tau`. The reviewed maximal-packing cover and three-piece refinement give `N_tau<=6P`, hence the coordinate capacity is at most `5832P`.

For independent outputs the full product packing is incompatible, so summing the coordinate logarithms gives overhead at most `r log2(5832)<13r`. For a scalar sum, local tolerance `epsilon/r` and the reviewed radius-`r` product code give a packing loss of `6^r`; consequently the overhead is at most `r log2(34992)<16r`. Affine terms cancel in the midpoint tests and are restored exactly. Local graph containment and the `15/16` error slack compose as stated.

These transfers use only convexity of the coordinate functions for their geometry; the hybrid scalar procedure supplies the required dense rational polynomial computation. They do not assume coefficient positivity or monotone curvature. The listed output structures and componentwise/scalar tolerances remain essential to the argument, and the all-affine case is handled separately.
