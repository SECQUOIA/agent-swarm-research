# Stage 3 independent review 4

Reviewed 2026-09-13. Focus: reader comprehension, formalization coverage, trust and novelty wording, correspondence of the paper/README/coverage map with actual Lean statements, and the saved validation evidence. No full Lean build was run, avoiding conflict with the separately assigned build reviewer. No manuscript or formal source was edited.

## Verdict

**No major issue found. One minor citation-completeness correction is requested.** The formal development proves the advertised mathematical interfaces without assuming the final rational-cut conclusion. The manuscript correctly separates these proofs from executable certification and benchmark replay.

## Valid minor issue

**Cite the proof assistant and mathematical library directly.** In `sections/05-formalization.tex`, the opening paragraph and “Build and trust boundary” introduce Lean and mathlib as substantive tools underlying a new paper component, but `references.bib` has no Lean or mathlib citation. Add appropriate primary software/paper references at their first substantive mention. A citation to CvxLean credits adjacent optimization work, not the proof assistant and library used here. The official [mathlib repository](https://github.com/leanprover-community/mathlib4) provides a `CITATION.md`; use the project's recommended citation or a pinned software citation, preserving the separate exact-version information already supplied. This is attribution and literature completeness, not an unsupported novelty or correctness problem.

## Statement-to-source review

- `Coordinate` has the four advertised cases, rational finite endpoints, real membership, and no numeric infinities. `accepts` requires ordered rational residual bounds and the stated half-line signs or free-coordinate zeros. `correction` is exactly the enclosure-table expression.
- `coordinate_correction_sound` accepts a real residual enclosed by rational endpoints, two box members, and the acceptance predicate. Its bounded and half-line arguments have the correct multiplication signs. The free case derives residual zero. `fixed_correction` and `correction_nonneg` establish the two described subsidiary assertions.
- `safe_affine_of_shift_bounds` assumes support and shift inequalities and an intercept bound, then proves the affine conclusion by a finite-sum identity. `rational_enclosure_cut` instantiates the coordinate bounds and casts the rational intercept condition into the real inequality. It does not smuggle in the desired underestimator. An arbitrary `Fintype` permits the empty coordinate type as claimed.
- Generic transfer assumes the embedding and objective equality; the epigraph specialization actually defines its master and constructs the graph point using the base inclusion and cut-validity hypotheses. The manuscript explicitly identifies these assumptions, including propagation and parser obligations outside the formalization.
- `incumbent_cutoff_lifting` establishes only the lifting step: the witness belongs to the cutoff, its objective bounds the reported lower bound, and every point outside the cutoff is worse. It neither assumes optimal attainment nor proves the VIPR invariant. Paper, README, and coverage table agree.
- `primal_infimum_bounds` establishes nonemptiness of the objective image and boundedness below before applying real `sInf` theorems. Thus there is no accidental use of real empty-set infimum as extended-real positive infinity. Matching-witness equality and pointwise optimality are explicit in the separate theorem.

## Exposition, positioning, and coverage

Section 5 is understandable without reading Lean syntax: it explains each mathematical object, shows the core coordinate inequality, and relates named declarations to the earlier mathematical development. It explains why support-vector and enclosure assumptions matter rather than presenting machine acceptance as a substitute for them. The definition of `LowerBoundOn` is given in prose before its uses.

The introduction's revised paragraph claims coordinate correction, rational composition, and selected transfer/primal statements only. Section 5 and `COVERAGE.md` expressly exclude convexity-to-support derivation, interval computation, propagation, parser/master identity, the VIPR invariant and executable replay, and individual artifact proofs. The prior-work discussion remains consistent with these limits and does not imply priority over formal nonlinear optimization, CvxLean, or CakeML VIPR checking.

The coverage table's current theorem-number references match `build/main.aux`: Corollary 3.3, Theorem 3.6, and Corollary 3.8. The table also supplies stable declaration names and warns that manuscript numbering can change.

## Saved evidence and source integrity

Inspected the proof files, umbrella module, `Verify.lean`, import-coverage script, verification shell script, dependency manifest, README, coverage map, and saved isolated log. The script uses warning-failing project builds, audits module-owned declarations and their transitive axioms, and invokes kernel replay. Its allowed axioms are exactly the three listed in the manuscript. The manuscript correctly calls replay a second pass with the installed kernel and retains compiled dependency trust; it does not advertise an independent kernel implementation or a fresh replay of all mathlib declarations.

The isolated log reports successful builds of the three proof modules and umbrella, an audit of 95 declarations, the expected standard axiom lists, and replay of all four project modules. Reusing pinned dependency caches is disclosed in both the author record and README; the standalone claim concerns project-source independence, not independent dependency rebuilding.

Independently ran `sha256sum -c verification/SHA256SUMS` from the formal directory. All 13 listed source/configuration/documentation files matched. No current source/log mismatch was found. I did not rerun compilation or treat saved logs alone as mathematical evidence; the statement and proof inspection above supplies this review's separate check.
