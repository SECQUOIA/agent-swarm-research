# Independent mathematical review of the main reduction and class transfers

Reviewed `main.tex`, `macros.tex`, and Sections 02–04 on 2026-10-06. This is an analytical review of the manuscript, not a review of the earlier audit reports. No computational experiment, literature search, project-wide test, or CI inspection was run. A second independent review of Section 04 is recorded in `referee-class-transfer.md`.

## Verdict

No invalid theorem, reduction gap, or substantive mathematical error was found in Sections 02–04. The exact-cover construction controls every integer vector, not only candidate cover vectors. The scaling proves the claimed strict semidefinite promises and polynomial common denominators on both yes and no instances. The related-family reductions do not infer hardness from inclusion alone: their complete lists of violating inequalities establish the required equivalences.

The NP-membership claims in these sections depend on the polynomial-witness lemmas in Section 05; those lemmas are outside this review's assigned scope. The reductions and the uses of those lemmas are correct provided the lemmas hold as stated.

## Low-severity clarifications

1. **Negative-type separation versus membership.** Section 02, lines 100–105, says that negative-type separation asks whether `M` is positive semidefinite. Under the paper's yes-means-violation decision convention, a separator exists exactly when `M` is not positive semidefinite. Suggested wording: “Negative-type membership is equivalent to `M` being positive semidefinite; a negative direction gives a separator.” This is a wording issue, not an error in the subsequent arguments.

2. **The signed-coefficient family is not finite as a set of data pairs.** Section 02, lines 173–183, and Section 04's subsection heading call the unrestricted-integer-parameter family “finite.” The coefficients of `w` have a finite alphabet, but `s` ranges over all integers. The NP certificate proof at Section 04, lines 187–194, correctly deals with this. Suggested name: “the signed `{0, ±1}` Boros–Hammer family” or “the restricted signed-coefficient family.” Reserve “finite family” for fixed-dimensional families with a bounded parameter range, such as the clique and cut subfamilies.

3. **Complete the all-positive list explicitly.** Section 04, lines 310–324, treats the switched form of the coefficient-sum-one hypermetric vectors. The rounded/odd-clique classification also includes their global negatives. Those negatives cannot produce an all-positive vector after the specified switching because every cover has `q > 0` set coordinates, and their cover coordinates remain `-1`. Add this sentence before concluding that the all-positive list is exhaustive. The conclusion is already correct.

4. **Name the correlation form when introducing it.** Section 02 defines `g_M` and its exact equivalence with cut-form hypermetric inequalities, but later uses “hypermetric correlation inequalities” as a family name without an explicit naming sentence. Add “We call the inequalities `g_M(z) >= 0`, `z` integral, the hypermetric correlation inequalities.” The equivalence itself is established correctly.

## Independent derivations and checks

### Definitions and representations

- On a cut, `Q = a(sigma-a) = (sigma^2-(2a-sigma)^2)/4`. This proves all rows of the inequality table, including the integer rounding, gap parity, and the hypermetric-gap-1 containment.
- The metric inequalities imply coordinate bounds for at least three vertices. The unit-diagonal positive definite `Z` matrix independently proves strict coordinate bounds for every constructed point.
- Direct expansion verifies `Q(b,d) = sigma(b) delta^T z - z^T M z`. The hypermetric map from integral `z` to `(1-sum z,z)` is bijective.
- The covariance and moment congruence identities hold on arbitrary Boolean ambient data, not just vertices. Positive definiteness transfers by an invertible matrix.
- The Boros–Hammer identities, the coefficient-vector map `beta(w,s)`, the pair equivalence `(w,s) ~ (-w,-s-1)`, and the parity split identity are correct, with the indicated factors of two in the finite signed form.
- Switching preserves the rounded slack through the quadratic form `b^T Z b`, preserves parity, gap, and gonality, and need not preserve coefficient sum one. The manuscript observes that distinction.

### Exact-cover reduction

- The displayed Gram generators are linearly independent, hence `M` is positive definite.
- Expanding the slack gives the stated identity. For `k=0,1`, all contributions are nonnegative; for `k>=2`, completion of squares gives a strictly positive lower bound. For `k=-t`, `t>=2`, the exact integer minima and `eta^2>=p/12` give a nonnegative lower bound. No integer layer is omitted.
- At `k=-1`, the nonnegative integral penalty must vanish because the negative offset lies in `(0,1]`. Thus negative slack is equivalent to binary exact coverage in both directions.
- The rational parameter choice `(p-1)/4` lies in the whole stated window, gives slack exactly `-1/2`, and yields the displayed distances and integer numerator bounds.
- The sphere-center projection argument gives `s <= 4n+p+1/(4(p-1)) < N/2`; Cauchy–Schwarz gives the lower bound. The Schur complement therefore proves the strict margin even at `theta=1/2`.
- In the X3C restriction, every cover has exactly `q` sets. The hypermetric gonality and support calculations are correct for `q>=3`.
- The strengthened moment margin excludes every rounded violation with `abs(sigma)>=3`. The two remaining signs reduce exactly to the core slack and give the stated complete split-vector list.
- Gonality excludes every triangle violation; the coefficient-sum bound excludes every perimeter violation. These establish the full metric promise, independent of whether a cover exists.
- The fixed-cutoff padding adds forced triples and gives a bijection of covers. The output has polynomial size and a common denominator `4N`; all numerator bounds are valid, including the separately treated case `n=0`. The strong-hardness formulation matches the explicit rational encoding.

### Class transfers and facets

- Gap-1 NP certificates can consist of switching signs and a short hypermetric certificate on the switched rational input. This avoids needing a large original gap-1 coefficient vector as a certificate.
- The union of gonal classes is the union of odd rounded inequalities and even positive-semidefinite inequalities. Doubling an integral negative direction supplies an even-sum certificate.
- Complementing `g` changes both its coefficient sign and the Boros–Hammer parameter by the amount stated. The original cut inequalities and the switched clique inequalities are exactly the listed data pairs, up to the polynomial equivalence.
- The direct clique facet proof has the necessary range `1 <= r <= t-2`: the compared subsets exist even at both endpoints. The comparisons force a common pair coefficient and then a multiple of the clique slack. Varying outside variables eliminates all extra affine equations, proving zero lifting preserves the facet.
- The pure lift has nonnegative additive slack on all integral coordinates. Its complete hypermetric list and lower gonality bound follow directly from the core theorem.
- The extended Schur complement parameter remains below `3/4`. This excludes every odd coefficient sum of absolute value at least three and preserves the metric and elliptope promises.
- Restricting the lift to `{0, ±1}` leaves exactly the two listed kinds of pure vectors. Their violations are `(q+2)/(4qN)` and `(q+3)/(4qN)` respectively; the latter is the maximum because `m=q-2>=1`.
- The specified switching produces exactly the all-positive support `C union U`, subject to clarification 3 above. The facet arguments are valid both with and without the root in the support.
- The lift and switching retain polynomially bounded common denominators. The zero/nonzero maximum distinction is correctly conditional on the existence of a cover.

## Requested disposition

Address the four minor clarifications above. No additional mathematical development or computational experiment is required to repair Sections 02–04 on the evidence of this review.
