# Stage 4 independent review 01, round 01

Reviewer: `/root/reviewer01`. Date: 19 September 2026.

## Verdict

**No major issue found. Four minor scope/wording corrections are required.** The reorganization preserves the complete proofs and diagnostics, and the main-paper overview is substantially faithful to them. The new discussion makes the modest matched-policy contribution clear and retains the relevant limitations. The standalone package and supplement match their manifests. The findings below concern concise summaries that should match the more precise full text.

I read only this stage's author materials and manuscript/artifact files, not other current Stage 4 reviews. I did not edit sources or spawn agents. Full-manuscript review remains the planned next stage.

## Required minor corrections

1. **Name integral candidates in the first packing summary.** `sections/guarantees-overview.tex:4` summarizes finite rejection from an unscaled positive row-residual threshold without saying that the candidate is integral and the cut concerns a global or selected-term row. The cited `thm:integral` has exactly that restriction; unscaled residual above a fixed threshold does not supply a uniform transformed margin as a fractional weight tends to zero. The next paragraph correctly develops fractional weighted residuals, so a short explicit qualifier will preserve the distinction: “At integer candidates, for global or selected-term rows…” and “with a fixed positive row-specific anchor margin.” Continue to require satisfaction of all retained cuts. This does not require changing the proof or numerical algorithm.

2. **Avoid saying the big-M configurations use perspective inequalities.** `sections/abstract.tex:2` says “Both policies use established perspective inequalities … with matched hull or big-M masters.” Perspective inequalities are the hull construction; the big-M construction deactivates original-space tangents. The full model section and corrected related-work section already distinguish these correctly. In the abstract, use “established affine cuts” or explicitly say that the common tangents are transformed into perspective or big-M inequalities. This is a local formulation-scope correction, not a challenge to either construction.

3. **Qualify the conic comparison in the conclusion by the measured statistic.** `sections/conclusion.tex:2` says the method does not “defeat supported exact conic alternatives.” This informal unqualified wording can be read as a per-instance or coverage claim, while the external results explicitly retain an open conic `FLay05` case solved by several prototype variants. The abstract appropriately confines the conic advantage to common-solved mean time. Use that same qualification in the conclusion, e.g. “does not improve common-solved mean time over the supported exact conic alternatives in these comparisons.” No numerical correction is needed.

4. **Keep the negative objective-rate conclusion at the proved scope.** `sections/conclusion.tex:4` says the guarantees imply no “general objective-error rate.” The explicit intersection counterexample proves failure of a uniform **linear** objective-error inference from separate-term interior margins. It does not by itself rule out every rate, or an additional problem-dependent modulus. Say “a general linear objective-error bound” (or “a linear objective-error bound without additional joint regularity”), consistently with `guarantees-overview.tex:12` and `ex:intersection`. The full results remain correct; this is over-broad shorthand in the conclusion.

## Overview versus full results

The overview is appropriately a consequences section rather than a replacement theorem. Its opening directs readers to complete assumptions and proofs. Subject to the integral/fractional qualifier above:

- The ECP and ESH original-space violation margins have the correct forms and depend on bounded gradients, compact domains and a positive anchor margin.
- Fractional residual continuity at the inactive origin and the omission test `lambda U <= epsilon_p` agree with the detailed fractional theorem. Fixed experimental cutoffs remain explicitly distinct from this theoretical alternative.
- Separate-disjunction repair is not represented as a simultaneous repair of the globally coupled GDP. The nonlinear intersection counterexample is correctly described in the overview as excluding a linear objective-error inference.
- Vanishing residuals and asymptotically optimized valid outer masters give the previously proved compactness-based value convergence. In context, “master suboptimality” refers to the valid outer masters defined in the preceding model section; a small wording addition “valid outer-master suboptimality” would be harmless but is not a separate required finding.
- The complete callback contract remains in the appendix, including old-cut enforcement, finite old-cut resolution, finite optional refinement, original-model acceptance and the distinction between residual termination and exact feasible objective-gap certification. The overview does not assert the prototype satisfies it.
- The representation summary includes convexity, fixed anchors and an explicit pointer to the full invariance qualifications. The root-zero and positive-derivative hypotheses are preserved in the referenced proposition. The Newton transient, local fixed-representation quadratic convergence, extra oracle cost and non-dominance witness statements are faithful.
- The full finite-arithmetic and approximate-root statements remain available in the appendix and are discussed in the algorithm and discussion. The main paper does not imply numerical certificates from those conditional proofs.

The reordered input files preserve scientific completeness. The model and algorithm precede the computational design; the shortened implications section lets the reader understand the experiment before reading the complete proofs. Cross-references still point to the full sections. Moving the empirical oracle subsection with the diagnostic appendix is reasonable because the main results explicitly distinguish its counted evaluations from the unrecorded GDP root-search counts.

## New narrative and standalone delivery

The abstract, discussion and conclusion retain shared ECP initialization, unchanged search seeds, related synthetic instances, NLP assistance, external nontransfer, numerical acceptance, supported conic competition and the limits of aggregate telemetry. They attribute established ingredients rather than inventing a new cut family or general algorithmic foundation. The four requested qualifiers prevent compressed summaries from exceeding the full evidence.

The reproducibility appendix distinguishes aggregation, fresh witness audit, source/example checks and optimization reruns. It explicitly reports that relocation reused an existing environment rather than claiming a fresh installation. The extracted-source `PYTHONPATH` instruction addresses the editable-install problem recorded by the author. The separately delivered supplement placement is clear in the README. No author identities, affiliations, funding claims, public DOI or blanket third-party license is invented.

The packaging script includes the required TeX/bibliography/generated evidence and independent local scripts, excludes recursive distribution contents and internal reviews, and copies the PDF. The supplement verifier checks the fixed archive digest, member uniqueness, regular-file type, safe relative paths, manifest membership and all payload sizes/hashes. I found no delivery inconsistency in the frozen state.

## Checks actually performed

- Read `process/stage04-author.md`, the Stage 4 fingerprint file, `main.tex`, the five new narrative/overview/reproducibility section files, both READMEs, `scripts/package.py`, `scripts/verify_supplement.py`, and relevant complete theorem/callback statements. Checked directional and cross-reference wording after reordering with targeted `rg`.
- Ran an inline Python fingerprint check: **all 62 Stage 4 recorded fingerprints match**.
- Opened the compact source tar in Python, checked all payload sizes and hashes against its embedded manifest, compared all payload bytes to the current paper directory, and compared the embedded manifest to `dist/source-manifest.json`: **62 payload files, zero mismatches; 63 archive members including the manifest**.
- Compared `main.pdf` and `dist/paper-lbesh.pdf`: **byte-identical**.
- Ran `python paper-lbesh/scripts/verify_supplement.py paper-lbesh/supplement/publication_bundle_v1.tar.gz` without extraction: **passed**, archive hash `f0399194ca1c9c57421965e236302c62e10eb72846ab807f936f18d9927d4b26`, 9,077 members and 9,076 payload files, 174,719,872 uncompressed payload bytes.

These were read-only checks apart from this review report. I did not rebuild TeX, extract archives, modify delivery files, repeat the relocated full raw audit, run optimization benchmarks, inspect CI, or perform project-wide verification. The author's relocated audit/build executions remain attributed to the author. No additional literature search was needed for these integration changes, which make no new historical or novelty claim.
