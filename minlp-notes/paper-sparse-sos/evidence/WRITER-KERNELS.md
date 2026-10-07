# Kernel sections: completion and integration record

Date: 2026-10-05. Sol fallback writer following the kernel author's saved draft. Ownership for this task: `sections/03-kernels.tex`, `sections/04-ordinary.tex`, `sections/05-sharpness.tex`, optional `appendices/A-kernels.tex`, and this report. No other manuscript sources were edited.

## Completion

All three sections are complete mathematical sections, with their proofs in the main text. The saved author's exposition and public labels were preserved. No kernel appendix is needed or was created. The optional `appendices/A-kernels` input in `main.tex` can be removed by its owner.

Section 3 contains the explicit squared-Fejer/Jackson kernel, all-frequency multiplier bound, interval/preordering degree ledger, nonnegative densities and exact separator marginals, the every-feasible-point rounding theorem, exact quadrature and grid extraction proof, and the real certificate corollary. Its use of compact primal attainment and finite SDP Slater is through the fully proved Section 2 interfaces.

Section 4 contains the ordinary SOS source kernel, even-series square identity, directly computed source degree, full defect-identity derivation, coefficient estimate with the intermediate-versus-combined degree distinction, weighted residual Cauchy–Schwarz, exact signed-density marginals, common correction and objective identity, explicit all-order parameter conversion and threshold, and real certificate corollary. Its treatment of empty individual bags is now explicit. The displayed mass polynomial is also explicitly declared and proved globally SOS, which makes the downstream constrained-section contract available directly from the kernel lemma.

Section 5 contains general moment-matching/approximation duality, the explicit all-order Fourier witness, actual locally supported measure lower bounds, matching preordering upper bound with transformed budget `A=10`, the ordinary-module lower/upper distinction, dense degree-four preordering certificate, the polynomial separator obstruction, and both exact small-order certificates and witnesses. The long order-two identity, its positive definite Gram matrices, and the witness are all supplied in the text; no numerical record or external appendix is needed to use them. Higher-order equality remains a conjecture.

## Changes to the reviewed draft

These changes are small repairs to the saved complete proofs rather than a replacement of their exposition.

1. **One-sided comparison for arbitrary feasible moments, Section 3.** The prose after `cor:pre-grid` previously said the grid optimum was “within” the error of every feasible moment objective. The proved assertion is `grid_min <= moment_objective+E`. The prose now says that, and reserves the two-sided error comparison for the optimal moment value, where `rho <= f* <= grid_min` supplies the other direction. The theorem display was already correct.
2. **Globally SOS mass polynomial, Section 4.** `lem:sos-kernel` now explicitly states that `omega=p_{s,N}M_s` is globally SOS. Its proof notes that both factors are globally SOS. This is an existing consequence of the definitions, required by later violation estimates.
3. **Normalization obstruction, Section 4.** The remark's title and conclusion now restrict the impossibility to polynomial kernels with nonconstant input dependence that are globally nonnegative/SOS in that input. It acknowledges `K=1` and distinguishes interval-module certification from global SOS certification. The proof's source-independence conclusion was already correct.
4. **Empty bags, Section 4.** Defined `Delta_v` for `v>=0` with `Delta_0=Delta_1=0`, restricted its recurrence to `v>=1`, and stated that an empty bag has `hbar=h^+=1` and an exactly preserved constant objective. The common correction remains `Delta_w` in every bag.
5. **General residual subsets, Section 4.** In `lem:residual-products` proof (b), nonnegativity of `L(G)` now cites the explicit SOS representation of `G`. The former citation to part (a), restricted to residual count at most one, was not valid for arbitrary subsets; the required SOS fact was already present at the start of the proof.
6. **Calibration interpretation, Section 4.** The introductory sentence now says the first three rows use the corollary prescription and the final row uses a different admissible parameter pair. No calibration calculation was rerun.
7. **Fourier intermediate equality, Section 5.** Corrected `sin(k pi/2)/pi` to `sin(k pi/2)/(2pi)` in the displayed evaluation of `int phi T_k dmu`. The final coefficient `-2sin(k pi/2)/(pi k(k^2-4))`, all subsequent pairings, and the lower-bound constant were already correct. The repair removes a factor-two inconsistency within that display.
8. **Explicit exact witness identities, Section 5.** Added the normalization and vanishing first/third moment identities for the order-two separator masses, with their positivity reason. This makes the reflected-law consistency check visible directly in the proof.

Items 1, 3–6 incorporate the independent reviewer's requested repairs. Items 2, 7, and 8 came from this writer's completion check against `AUDIT-KERNELS.md`. The independent reviewer separately confirmed the Section 5 exact Gram identity, leading minors, witness odd-moment cancellation, and witness objective by algebra.

## Mathematical validation and dependencies

The Section 5 formulas were checked against the earlier independent mathematical audit, including the distinct hierarchy conventions, actual-measure witness direction, transformed budgets, dense generator products, and exact values. In addition, the writer checked the corrected Fourier equality by integrating `cos^2 theta=(1+cos 2theta)/2` directly. The intermediate factor is one half; the final odd-frequency coefficient and theorem constant remain unchanged.

The independent reviewer supplied the final residual-proof and calibration fixes and reported independent verification of the exact small-order algebra. Its role was not duplicated here. The writer checked that the statements and proof ingredients needed by the Section 2 interfaces and later constrained/finite-state sections are present. No new unsupported mathematical extension or numerical claim was added.

Public dependencies are the proved Section 2 lemmas for interval positivity, moment control, running-intersection gluing, compactness, and finite SDP Slater. The general moment-matching lemma is exported for the recourse section. External standard statements and literature attribution remain the sole literature agent's responsibility; no literature research was performed by this writer. The saved citation keys were preserved. The already-recorded numerical calibration table was trusted as instructed.

At the final targeted reference check, all reference targets in Sections 4 and 5 existed. Section 3 still referenced `sec:certificates`, which was not yet present in the current section-file snapshot; this is the Section 9 integration dependency, not a missing kernel proof. The earlier missing `sec:extensions` target had appeared by the final check. No proof in these sections depends on a missing kernel appendix.

## Targeted checks actually run

Read-only commands inspected the saved sections, `macros.tex`, `main.tex`, Section 2, the architecture, and the prior audit. Inline `python3 -B` structural checks inspected only the three owned sections for balanced LaTeX environments and braces, unfinished proof markers or hidden proof inputs, and reference targets against currently present manuscript labels.

The initial reference check stopped at the then-absent external `sec:certificates` target. The completed final check reported:

```text
03-kernels.tex PASS: environments and braces balanced; no unfinished proof markers;
  unresolved external references: ['sec:certificates']
04-ordinary.tex PASS: environments and braces balanced; no unfinished proof markers;
  unresolved external references: []
05-sharpness.tex PASS: environments and braces balanced; no unfinished proof markers;
  unresolved external references: []
```

Final source hashes for reviewers to distinguish the amended snapshot:

```text
aa99f3f741b7fd0d61d4bd395b4a4f236589952d1c721645aac6985f7f1c8a2a  sections/03-kernels.tex
ca6da25fad4c8f14502e8599d96ecac40e327fd858bf49fd47a3712f07355197  sections/04-ordinary.tex
92835b3988400ec22a363886b66abe8663cd9ca341d1f97d3b5f545e033588f9  sections/05-sharpness.tex
```

No LaTeX build, experiment rerun, project-wide check, CI inspection, bibliography research, or commit was performed by this fallback writer. A submission build and bibliography/reference integration remain root's separate work. Structural checks do not establish typesetting quality; the mathematical validation is the proof review described above.
