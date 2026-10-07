# Three-variable proof audit

Scope: sections/05-three-variables.tex and appendices/B-three-variables.tex. No archived searches, samplers, experiments, or CI checks were rerun. The chapter was reconstructed by mathematical reasoning rather than transcription.

## New repairs and improvements

1. **The disjoint cone is closed.** Each of the finitely many weighted SOS Gram blocks is bounded by the integral of its polynomial: the weighted affine moment matrix is positive definite because the weight is positive in the cube interior. Bounded coefficient vectors therefore have bounded PSD Gram representations and a convergent subsequence. This proves K_D closed, hence D3 closed, with high-degree cancellation explicitly retained.
2. **An explicit quadratic order unit exists.** Summing all 27 weights with identity affine Gram matrices gives 8+4 sum x_i^2. The Gram map is onto V because every basis monomial is a generator. Therefore this quadratic lies in int(K_D) intersect W. Bounded positive functional extensions then prove projection closedness and exact extension duality by the bipolar theorem. No closure of D3 is needed.
3. **Caps have an explicit decomposition in every dimension.** For each negative diagonal coefficient b_i, coordinate interpolation rho_i(q)=q+b_i x_i(1-x_i) preserves cube nonnegativity and deletes that coefficient. This gives q=qplus+sum max(-b_i,0) cap_i without conic duality or a sum-closedness argument. Mixed coefficients remain unchanged.
4. **The blocking lemma now excludes the closure.** Since D3 is closed, the original exact-certificate zero-set obstruction suffices to exclude limiting certificates as well.
5. **Boundary extremality no longer depends on symbolic rank computations.** Appendix B reconstructs every coefficient of a contact-preserving quadratic from its z-square coefficient. Its three regimes cover all five original strata, including every zero-parameter boundary and zero-edge case. No exceptional minor or computer algebra assertion is used as a proof.

## Result-by-result contracts

- three:closed and three:extension: complete self-contained finite-dimensional cone proofs.
- three:caps: complete constructive proof for all n, including finite-atom measure rounding.
- three:rounding: exact generator identities and pure-coefficient positive functionals; cancellation is respected.
- three:two-dimensional: only external input is two-variable Shor plus box RLT plus caps exactness (Anstreicher--Burer 2010, Theorem 6, p.7). Luna confirmed the primary-source contract; statements (ii)-(iv) then have full proofs.
- three:sign: only external input is BNW arXiv:2504.03996v3 Theorem 1 for submodular quadratics in n<=3. Luna confirmed all ordered entrywise upper bounds Y<=m1^T, PSD Shor, no diagonal or linear-coefficient restrictions; the input is objective-value exactness, not hull exactness. Canonical bibliography key retains first-posted year 2025.
- three:sum: proof uses compact integral base of P3, finite conic sums, finite-dimensional bipolar duality, and normalized zero-mass extension argument. Family cones are explicitly closed conic hulls, not just scalar multiples of individual family members.
- three:reduction: all complement signs and strict-sign limits checked algebraically. Six copies are a conclusion for strictly supermodular extreme rays, not a claim that those six alone describe the whole hull.
- three:blocking and three:three-edges: complete direct zero-set proofs.
- three:boundary: complete contact-inheritance proof, with full coefficient/rank ledger in Appendix B. Includes zero d1/d2 only in regimes where their formulas make sense; d3 is strictly positive because k>0.

## Remaining non-theorems

P3plus=S remains unproved. It is stated as the exactness question, not as a theorem, and its equivalence to full cap-corrected moment hull exactness is proved. Boundary extremality does not assert exposedness or exclusion from D3. No general runtime benefit is claimed.

## Literature and integration notes

Verified bibliography keys: AnstreicherBurer2010 and BurerNatarajanWillemsen2025. Chapter expects family:definition, family:valid, family:exposed, family:lmi, sec:evidence, and root setting equation anchors as listed in evidence/BRIEF.md.

Targeted check actually run: one independent inline `python -` SymPy check verified the five exact family edge restrictions and the 27-block identity 8+4 sum x_i^2 (passed). This was a new focused algebra check, not an archived experiment or sampler. Manuscript integration/TeX checks are root-owned. No computational experiment was rerun.
