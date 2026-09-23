# Stage 4 independent review 05, round 01

Reviewer: `/root/reviewer05`. Date: 19 September 2026.

Reviewed the complete Stage 4 author report/fingerprint, new abstract, discussion, conclusion, guarantees overview and reproducibility appendix, revised `main.tex`, README files, portable checks/package scripts and delivered archives. Assessed their fit with the previously reviewed content. No other current reviewer report was read; no manuscript source was edited and no agent was spawned. The separate Stage 5 whole-manuscript review remains pending.

## Verdict

**No major issue identified; three minor prose corrections are recommended.** Moving the full separation proofs and oracle analysis to appendices improves the route from the research question to the experimental intervention and results. The overview preserves the mathematical qualifications and points to full statements. The paper is now scientifically self-contained, and the delivered source archive builds independently of repository notes. The practical instructions distinguish presentation regeneration, fresh saved-witness validation, and new optimization runs correctly.

## Actionable minor findings

1. **Distinguish the hull perspective cuts from big-M deactivation in the abstract.** Location: `sections/abstract.tex:2`, “Both policies use established perspective inequalities ... with matched hull or big-$M$ masters.” Read literally, this assigns perspective inequalities to the big-M master too. In the paper's equations, the hull master uses homogeneous perspective cuts while the big-M variant deactivates original-space tangents. Suggested replacement: “We compare both policies in a common implementation using established perspective cuts for hull masters or valid tangent deactivation for big-$M$ masters, with matched single- or multiple-tree execution.” This aligns the abstract with the precise model section without changing the contribution.

2. **Expand NLP on first use in the abstract.** Location: `sections/abstract.tex:2`, first occurrence “NLP-assisted”. Use “nonlinear-programming (NLP) assisted” or an equivalent grammatical construction. The abstract should be readable on its own; the expansion later in the introduction does not accompany an abstract displayed separately by an index or submission system.

3. **Keep the conclusion's conic comparison at the aggregate scope used in the abstract.** Location: `sections/conclusion.tex:2`, “or defeat supported exact conic alternatives.” This loose wording is broader than the measured common-solved mean-time comparison and can suggest per-instance dominance. The accepted external results explicitly include `FLay05`, which some prototype configurations solve while the conic baseline retains an open gap. Replace the phrase with, for example, “or produce lower common-solved mean times than the supported exact conic alternatives tested.” The abstract already uses the appropriately qualified aggregate statement.

## Assessment of integration and standalone delivery

- The concise margin discussion correctly links positive violation to a uniformly positive separation distance only under compactness, gradient bounds and enforcement of old cuts. The residual-calibrated omission rule is kept distinct from the implemented cutoff. The counterexample, limiting value assertion and conditional single-tree contract retain their necessary pointers and do not promise an exact finite objective certificate.
- The main discussion identifies the original empirical intervention, shares the ECP initialization qualification, avoids interpreting repeats with a fixed seed as population-level robustness, and retains the negative recovery ablation and faster supported conic comparisons. The novelty boundary remains consistent with the literature review.
- The source package includes the bibliography, `.bbl`, complete scientific sections, tables, figures, compact data and scripts. It does not depend on research notes to supply a proof or missing model equation. The large research archive is explicitly separate, and the README tells users where to place it.
- The archive verifier fixes the expected archive hash, checks all member names and payload hashes/sizes, and requires a new or empty extraction directory. The example checker requires the extracted research root instead of silently skipping source checks. The audit directions address the editable-GDPlib import path, state that the output file must be new, and distinguish a reused pinned environment from a fresh-install test.
- The final PDF renders the abstract, conclusion/reference transition and reproduction commands clearly. The proof move leaves no unresolved cross-reference. The one inherited underfull bibliography line is not a content or readability defect. The manuscript remains an anonymous submission draft without invented author/funding/DOI information.

## Checks actually executed

1. Verified all listed Stage 4 fingerprint entries against repository file contents: no mismatch. Ran `sha256sum -c SHA256SUMS`: PDF, source archive and research archive all passed.
2. Extracted the delivered source archive into `/tmp/lbesh-stage04-review05-oqgu3_pe/paper-lbesh` with the standard-library safe data filter. Independently checked every embedded manifest size/hash: all 62 payloads passed.
3. In that extracted source directory, ran `latexmk -gg -pdf -interaction=nonstopmode -halt-on-error main.tex`. Result: successful 42-page PDF, no undefined references/citations or overfull boxes; one inherited bibliography underfull-box warning.
4. Used `pdftotext -layout` and rendered/visually inspected pages 1, 22 and 42 with `pdftoppm` and `view_image` (title/abstract, conclusion/reference transition, and executable commands). No clipped or missing text was found.
5. Ran extracted `python scripts/check_evidence.py` and `python scripts/regenerate.py --no-figures`. Both passed; all 19 regenerated table/CSV/table-value outputs matched the embedded source-manifest hashes. Figure regeneration was already reviewed in Stage 3 and was not repeated here.
6. Ran `python scripts/verify_supplement.py supplement/publication_bundle_v1.tar.gz` in verification-only mode. It verified 9,077 members, 9,076 payload files and 174,719,872 payload bytes. Read the archived `pyproject.toml`; its editable GDPlib dependency uses the relative included path `instances/gdplib_src`.

These checks did not rerun the complete fresh primal audit, install a clean Python environment, launch optimization benchmarks, inspect CI, or run project-wide verification. The author's recorded relocation audit remains separate evidence rather than a check claimed by this reviewer.
