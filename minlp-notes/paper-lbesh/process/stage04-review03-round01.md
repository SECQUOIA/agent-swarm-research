# Stage 4 independent review 03, round 01

Reviewer: `/root/reviewer03`. Date: 19 September 2026.

## Verdict

No major issue identified. The integrated manuscript preserves the accepted scientific scope, and the source/supplement delivery is internally consistent and relocatable for the targeted checks I ran. Approve after the minor precision/cleanup changes below and refresh the package. I did not read other current Stage 4 reports, edit sources, spawn agents, or repeat optimization/full-witness audits. Full-manuscript Stage 5 review remains the next distinct step.

## Major issues

None.

## Minor actionable corrections

1. **Keep the conclusion as precise as the abstract and detailed results.** `sections/conclusion.tex:2` says the advantage does not “defeat supported exact conic alternatives.” Replace this informal broad comparison with the actual finding: supported cone formulations have lower common-solved mean times in the reported comparisons, while coverage is mixed. This preserves the external FLay05 exception and avoids sounding instancewise. At line 4, change “a general objective-error rate” to “a linear objective-error bound” (or explicitly say no rate is established here). The supplied intersection counterexample disproves an O(epsilon) inference; it does not by itself disprove every possible rate. The new overview already states this correctly at `sections/guarantees-overview.tex:12`.

2. **Remove stale stage-status text from the delivered coverage ledger.** `evidence/coverage.md:51` still labels Stage 3 review pending, and line 60 says Stage 4 still owns the unwritten abstract/discussion/conclusion and Stage 3 is not accepted. This contradicts the current ledger opening, complete manuscript and Stage 4 report. Update those statuses. At line 47, either label the reservation sentence explicitly as historical Stage 2 scope or remove its present-tense statement that the empirical subsection is reserved for Stage 3. Since the ledger is included in the submission source, it should describe the current deliverable without apparently unfinished work.

3. **Expand NLP in the standalone abstract.** `sections/abstract.tex:2` uses “NLP-assisted” without defining NLP within the abstract. Introduce “nonlinear programming (NLP)” there. The acronym is familiar to specialists, but this is a small standard abstract clarification for the wider optimization readership. The ESH and ECP expansions are already present.

## Integration and scientific assessment

The abstract accurately confines novelty to the matched computational study and supporting analysis. It retains the 33/32/31 counts, same-seed scheduling repetitions, 4–6% common-solved timing effect, 6–18% mean cut reduction, 5.5–6.6 total separation-time factors, equal external coverage, conic alternative and 69/72-to-1/72 recovery ablation. It correctly distinguishes the 1,464 benchmark records from the 420 continuous conic calls rather than suggesting 1,464 independent models.

The discussion explains why the policy comparison matters within a solver already paying for interiors and NLP recovery. It also states why it is not an independently optimized ECP comparison. Related structures/streams, few seeds, prior reference exposure, interface failures, absent general conic OA baseline, unimplemented calibrated cutoff and incomplete histories are carried into the interpretation. The text does not present elementary supporting proofs as a new algorithmic foundation. No new historical or priority claim needs separate literature support in this stage.

The guarantees overview is consistent with the full appendices: strict row anchors and bounded gradients yield uniform margins; old-cut satisfaction is necessary for packing; small weights require a weighted residual; fixed numerical cutoffs do not instantiate the proved calibrated policy; separate-hull repair does not establish intersection accuracy; value convergence has no claimed quantitative rate; and callbacks require substantive solver contracts. The representation paragraph includes convexity, a fixed anchor and cross-references to the stricter invariance hypotheses. It does not imply that the numerical code certifies these exact conditions.

Moving the complete proof and oracle sections behind the main study improves reader flow while retaining the central distinctions in the model, overview and algorithm. All mathematical definitions needed by the experiment remain present, with explicit forward references rather than dependence on repository notes. The main article still includes considerable implementation detail, but that detail identifies the actual experimental intervention; I found no structural defect requiring another reorganization.

The reproducibility claims have appropriate limits. Offline TeX compilation depends on supplied figures/tables and a TeX installation. Python table regeneration, model-witness audit and optimization reruns are separate actions. Fresh native solver installations/licenses are not claimed to have been recreated, and relocation explicitly reused the existing pinned environment. The original editable-GDPlib import hazard is addressed by the documented extracted-source PYTHONPATH. No public DOI, named authorship, affiliation, funding, conflict declaration, clean-install test or exact optimality certificate has been invented.

## Package/source checks actually run

1. Read the Stage 4 author report, fingerprint, all four new narrative sections plus overview, `main.tex`, reproducibility appendix, both READMEs, package/verifier scripts, coverage ledger and recorded relocation/delivery checks. Inspected the archived-environment declaration and its relative editable GDPlib path.
2. Independently checked all 62 file hashes in `process/stage04-author-source-sha256.json`. All matched. My first read-only checker mistakenly resolved an unprefixed `README.md` against the repository root and stopped on a hash mismatch; correcting all keys to be relative to `paper-lbesh` passed. This was a reviewer path error, not a package mismatch.
3. Independently verified all three delivery hashes in `SHA256SUMS`. All matched.
4. Opened the compact source archive and checked its exact member set against the embedded manifest, then checked every payload size/hash and byte identity with the corresponding current paper file. All 62 payload files matched. Process records and the separate large research archive are excluded as documented.
5. Checked that `dist/paper-lbesh.pdf` is byte-identical to `main.pdf`.
6. Extracted the compact source into a new temporary directory using the standard data-only tar filter. Ran its delivered `scripts/verify_supplement.py` on the original supplement path with extraction into a new temporary research directory. It verified the fixed archive hash, all 9,077 members and all 9,076 payload hashes/sizes (174,719,872 payload bytes), and completed extraction.
7. Ran the relocated `evidence/check_stage02.py --research-root <temporary extracted research>` with standard-library Python. It passed against the extracted source. Temporary files were removed automatically.

These checks add independent delivery correspondence and a targeted relocation execution. They do not claim a new clean Python install, new LaTeX build, repeated table/figure regeneration, full saved-witness audit or optimizer run. No project-wide test or CI inspection occurred. After the minor edits, the packaging script must refresh the source archive, PDF and checksums before final delivery.
