# Stage 4 independent review 02, round 1

Reviewer: `/root/reviewer02`. Date: 19 September 2026. Scope: all Stage 4 narrative, organization and packaging changes, with emphasis on summary quantifiers, theory/data distinctions, frozen source provenance and reproducibility claims. Read the Stage 4 author record/fingerprint, all new section files, main document organization, reproducibility appendix, README files, portable source checker and both packaging/verifier scripts. No other current review report was read; no manuscript or delivered artifact was edited.

## Verdict

**Pass after two minor wording corrections; no major issue identified.** The integrated draft preserves the accepted arithmetic and important qualifications. Its proofs remain available in the appendices, and the overview distinguishes exact sufficient conditions from the numerical policy actually benchmarked. The source and research packages are internally consistent with their advertised frozen identifiers and the authoritative files.

## Major findings

None. A fresh installation of the Python environment is explicitly not claimed; reusing a pinned installation with relocated sources is correctly distinguished from that stronger test. The missing public archive DOI is disclosed, and neither journal acceptance nor invented administrative facts are asserted.

## Minor findings requiring correction

1. **Qualify the abstract's cut representation by formulation.** Location: `sections/abstract.tex:2`, “Both policies use established perspective inequalities ... with matched hull or big-$M$ masters.” Both ESH and ECP use perspective inequalities in the hull variant, whereas the big-M variant adds deactivated original-variable tangents (`eq:bigm-cut`), not the displayed perspective inequalities. State, for example, that both policies use the same established tangent family, with perspective cuts in hull masters and valid big-M deactivation in original-variable masters. The underlying algorithm section is already precise. This is a compact-summary wording issue, not a cut-validity or empirical problem.

2. **Retain the common-solved aggregate qualifier in the conic conclusion.** Location: `sections/conclusion.tex:2`, “it does not ... defeat supported exact conic alternatives.” The abstract correctly limits the conic advantage to common-solved mean time; the conclusion's broad verb drops that scope. In the external data the prototype solves FLay05 in several configurations while the conic adapter leaves its gap open (`sections/results.tex:66`). Replace the broad phrase with the measured fact that common-solved aggregate timings favor the tested exact conic alternatives. This prevents the standalone conclusion from suggesting that the conic method wins every supported instance or dominates coverage. The body already states the qualification, so this is minor.

## Narrative and theorem consistency

Rechecked the abstract's numerical assertions against the accepted Stage 3 tables and data: 1,464 benchmark records; 51 generated/27 external models; 420 reference calls; 33 versus 32/31 single-tree accepted counts; approximately 4–6% common-solved repeated timing advantage; 6–18% mean cut-count reduction; 5.5–6.6 total cut-generation-time ratio; and 69/72 versus 1/72 recovery ablation. Their numerical values agree. The four primary work configurations are distinct from the two formulation pairs repeated in single-tree mode; the current use of “primary” preserves that distinction.

The overview's ECP and ESH margins, compact packing implication, residual-calibrated omission bound, fixed-cutoff limitation, per-disjunction repair caveat, vanishing-residual value result and single-tree enforcement contract match the full appendix statements. It expressly refers readers to full assumptions/proofs. The representation discussion includes convexity of the increasing re-expression and the fixed-anchor/exact-boundary qualifications through its cited proposition. No new priority, uniform dominance or runtime theorem is asserted.

The discussion preserves the ECP shared-interior cost and its effect on initial tangents, related generated controls, unchanged search seeds, external and conic limitations, unimplemented residual-calibrated policy, missing complete failure histories, and absence of interval certificates. Moving the complete theory and oracle material to appendices changes reader order without discarding scientific content. Main-file includes retain all scientific sections, detailed tables and model specifications.

## Artifact verification actually performed

Independent inline Python checks, without calling the package mutator, established:

- All **62** paths in `process/stage04-author-source-sha256.json` match their frozen hashes.
- Every one of the **62 source-archive payloads** matches both its embedded manifest size/hash and the corresponding authoritative repository file; the archive also contains the manifest itself.
- All three hashes in `SHA256SUMS` match the delivered files.
- `main.pdf` and `dist/paper-lbesh.pdf` are byte-identical.
- The nested original executable freeze has SHA-256 `6c9eaf9898f04d08a12381879ab9bae79f83b800f0db9e4cc696ccbff6be84ad`, matching the reproducibility appendix.
- The research archive has 9,077 members. Its PDFs are model illustrations or generated analysis figures, not redistributed downloaded literature articles; this is consistent with the stated exclusion.

Executed:

```sh
python paper-lbesh/scripts/verify_supplement.py \
  paper-lbesh/supplement/publication_bundle_v1.tar.gz
```

It passed the fixed archive hash, member-name/type/uniqueness checks, and all **9,076** payload size/hash checks (174,719,872 payload bytes). The archive hash is `f0399194ca1c9c57421965e236302c62e10eb72846ab807f936f18d9927d4b26` as stated.

Extracted only the archived solver source to the new temporary research root `/tmp/lbesh-stage04-review02-4clrptd9` and invoked the portable `evidence/check_stage02.py` from `/tmp` with that explicit root. All analytic/example/source-default checks passed. Invoking it without `--research-root` returned the expected argument error (exit 2), confirming that source validation is not silently bypassed after relocation.

## Packaging and reproduction review

Inspected the deterministic source packaging inputs and fixed tar/gzip metadata, generated manifest, PDF refresh, separate research archive delivery and exclusion of recursive `dist/` and process records. The supplement verifier checks the expected complete archive before extraction, accepts only regular uniquely named relative members, and requires an empty/new destination. The README and appendix explain that the research archive must be placed separately alongside the compact source package.

Checked the archived dependency declaration and documented `uv sync --frozen` path, distinct conic environment, external native solvers/licenses, mandatory source-root argument, explicit extracted GDPlib `PYTHONPATH`, and refusal to overwrite an existing audit output. The claimed verification boundary correctly separates table regeneration, original-model numerical validation, independently implemented aggregation and optimization timing reruns. It explicitly notes reuse of the original feasibility checker. The recorded relocation audit is distinct from the original frozen verification report.

No full audit, optimizer run, project-wide check, CI inspection or duplicate LaTeX build was performed in this review. Stage 3 already independently reconciled the raw arithmetic, and no changed data or new concern justified repeating that work. Final whole-manuscript Stage 5 review remains pending.
