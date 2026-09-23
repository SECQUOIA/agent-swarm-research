# Stage 1 independent review 4

Verdict: **No major issues found.** The main metric, allocation, and step-count arguments withstand the boundary checks below. Two local hypothesis omissions should be corrected before freezing the stage.

Scope: `main.tex`, `macros.tex`, `sections/01-foundations.tex`, `sections/02-exact-distance.tex`, `bibliography.bib`, `audit/source-map.md`, and `audit/literature.md`. I did not read other reviewers' reports. Future sections, temporary front matter, and `audit/root-radial-upper.md` are outside this review.

## Valid minor issues

1. **State the accuracy range in the logarithmic-allocation corollary.** Location: `sections/02-exact-distance.tex:326–348`, especially the assertion that the optimizer has a positive multiplier in (eq:Lambert). The previous theorem assumes `0 < epsilon < W_0`, but the intervening paragraph explicitly discusses `epsilon >= W_0` and `epsilon = 0`, and the corollary does not reinstate the range. For `epsilon >= W_0`, the optimizer is `s=0`, and no positive `gamma` satisfies the claimed optimizer equations. For `epsilon=0`, there is no feasible finite vector. **Repair:** begin the corollary with “Let `0 < epsilon < W_0`.” The proof and formulas are then correct without further changes.

2. **Make the allowed step-radius range explicit in both counting corollaries.** Locations: `sections/01-foundations.tex:128–142` and `sections/02-exact-distance.tex:348–353`. The preceding lemma quantifies `0<R<1` only locally; neither the forward-R definition nor the corollaries impose that range. As literally stated, the denominators can be undefined or zero. **Repair:** fix `0<R<1` before the forward-R definition and/or include it in each counting corollary. No constant or proof change is needed.

These are minor because their intended hypotheses are evident and the corrections do not change any result in its useful range.

## Mathematical checks passed

- **Positive scales:** The exact metric claims only require positive scales. The restriction to scales at least one is correctly reserved for standard self-concordance and local-step conversion. A box with heterogeneous coordinate scales is included as a product of rank-one factors.
- **Chord orientation and quantifiers:** The global inequality uses the norm at the starting point. Concatenating feasible chords yields the stated lower bound; partitioning an attained shortest curve yields the upper bound. No unjustified general completeness theorem is used. The zero-distance attained case is covered.
- **Singular and repeated spectra:** The Hermitian dilation correctly contributes paired eigenvalues, producing `2 g'' = b''`. At repeated spectra the divided-difference limit is correct, and the almost-everywhere eigenvalue derivative argument handles crossings and zero singular values. No differentiability of a chosen singular frame along the entire curve is required.
- **Jordan normalization:** With the trace inner product, primitive idempotents have norm one. The Peirce off-diagonal Hessian coefficient has the right normalization: in the matrix specialization its norm squared already contains the factor two. The inversion derivative coefficient is `-(z_i z_j)^{-1}`; differentiating `z circ z^{-1}=e` in each Peirce component verifies it. Repeated-eigenvalue limits and the exceptional-algebra scope are consistent with the argument.
- **Attainment:** The constructed paths remain in the domain, have constant metric speed, and attain the spectral lower bound. The allocation objective diverges when any coordinate approaches one, so a finite sublevel compactness argument gives an attained accurate endpoint. This suffices for all later counting applications in this stage.
- **Alignment and inactive coordinates:** Von Neumann alignment and the Jordan doubly stochastic overlap matrix justify reducing to positive weights. Inactive coordinates can be zeroed. Equal factor scales ensure the allocation is coordered with weights within a spectral factor.
- **KKT:** The strict convexity calculation is correct. Slater holds for positive accuracy. The active constraint and positive multiplier follow for `epsilon<W_0`; stationarity excludes zero coordinates. The Lambert equation correctly absorbs the factor two into `gamma`, and the spurious zero root is explicitly excluded.
- **Least barrier parameter:** The radial gradient dual norm is `alpha sum_i 2t_i^2/(1+t_i^2)`, whose supremum is `alpha` times rank. Products add these suprema. The scalar `rank=1` limit and repeated full-rank boundary limits agree.

## Attribution and readability

The stage appropriately credits Nesterov–Todd for local-step geometry/product distances and Nesterov–Nemirovski for central-path/geodesic and target-set comparisons. I checked the local primary extractions of NT2002 Sections 4–6 and NN2008 Theorems 4.1 and 5.3; the stated comparisons match them. The treatment of Lewis–Sendov as the real-symmetric classical source while directly deriving the trace-separable complex formula avoids overstating its scope. The literature audit honestly distinguishes read full texts from metadata-only Baes evidence and avoids priority claims at this stage.

The proof order is intelligible for an optimization audience familiar with matrix spectral calculus. No further mandatory exposition issue was identified. A standard Jordan-algebra textbook citation would be a useful optional addition for readers seeking the spectral theorem and Peirce calculus, but it is not a gap in the displayed Hessian derivation.
