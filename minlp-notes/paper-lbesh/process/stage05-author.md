# Stage 5 integration-author pass and frozen handoff

Author: `/root/stage05_author`. Date: 19 September 2026.

**Result: no manuscript correction is needed at this handoff.** The accepted Stage 4 source and all delivery artifacts remain byte-identical. This is the designated integration-author pass before the required five independent whole-manuscript reviews. It is not final acceptance. No subagents were spawned.

## Complete reading and scientific assessment

Read `main.tex`, every included section and appendix, all 17 generated tables, all 27 bibliography entries, the paper and compact-data READMEs, the scientific coverage and literature ledgers, the development plan, and Stage 4 disposition/correction records. Inspected the packaging script and current source manifest. The complete paper is 42 pages.

- **Question, importance and attribution.** The title, abstract, introduction, related work, discussion and conclusion consistently identify a matched separator-policy experiment in an NLP-assisted GDP implementation. They do not claim a new perspective cut, new general algorithm, first GDP/ESH combination or universal superiority. Closest disjunctive strengthening, SHOT, perspective-cut and conic precedents are distinguished by actual procedure and target. Literature records identify primary sources and limits of access, rather than treating a search as proof of absence. No factual doubt requiring an additional online search arose.
- **Model and cut family.** Checked the separation between original integrality and term-set convexification, finite bounded boxes, neighborhood smoothness, affine logic, sparse/full-copy equivalence, the bounded perspective identity, inactive-origin convention for empty terms, complete-tangent characterization, separate-hull target and valid box big-M construction. The objective compactification preserves an optimal lift without falsely claiming it is installed by the prototype.
- **Full proofs and diagnostics.** Re-derived the margin and coefficient estimates, rowwise packing argument, weighted residual continuity and denominator cutoff, geometric repair, intersection counterexample, cluster-point value argument, old-cut/auxiliary-work single-tree contract and coefficient-error allowance. Checked the fixed-anchor composition rule, convexity-based ECP weakening, scalar master/Newton recurrence and strict transient inequality, ellipsoid calculation and off-center opposite witnesses. Their assumptions and limitations agree with the concise overview. No logical or algebraic gap was found.
- **Theory versus code contracts.** The implementation description explicitly distinguishes exact roots from exterior bracket endpoints; transformed from untransformed rejection; residual-calibrated omission from fixed cutoffs; complete separation from LP stalls; exact compactness from an unbounded artificial epigraph; exact evaluation domain from numerical normalization; retained-cut hypotheses from callback behavior; and numerical primal/gap acceptance from exact certification. The negative ablation is consistent with those distinctions.
- **Study and numerical claims.** Checked the eight-batch accounting (1,464 benchmark records), separate 420 reference calls, 18/33 pilot/held-out split, original 42 cone-supported controls plus nine trig controls, 27 external inputs and scope strata, scheduling-only repetitions, numerical acceptance formulas, and conditional versus penalized timing summaries. Abstract and conclusion numbers match the results and tables. Mean work savings are not confused with medians; total separator time is not per-cut time; the cone advantage is conditional timing with mixed coverage; repeated and follow-up records do not replace primary outcomes. All negative and interface outcomes remain represented.
- **Model/cone appendix.** Checked allocation normalization and domain margins, positive costs and box epigraph bounds, deterministic witnesses, region congestion/variation bounds, stated coefficient draw order, four scalar perspective epigraphs, exponential-cone zero slice, SOC product identity, zero-weight aggregate closure, quadratic slack lift and declared adapter scope. Generated smooth compact controls remain distinct from external stress models.
- **Structure and standalone delivery.** The main article retains the question, model, accessible guarantees overview, actual implementation and computational interpretation; full derivations and detailed model/results/reproduction specifications follow in appendices. Definitions and proofs do not require repository notes. Read all reproduction instructions and the stated boundary between table regeneration, saved-witness audit and optimization reruns. Authorship, affiliations, funding and a public DOI are not fabricated. Stage 5 remains explicitly pending in the packaged status ledger.

No scientific source, script, compact data, figure, table, frozen solver/model file or research supplement was changed. No speculative stylistic rewrite was made.

## Actual checks and limitations

An inline standard-library Python check from the repository root verified:

1. All **68 paths** in `process/stage04-accepted-source-sha256.json` still have their accepted hashes.
2. The source archive has exactly its 62 payloads plus embedded manifest; embedded and external manifests match; every payload has the declared size/hash and matches the current source byte-for-byte.
3. `main.pdf` and `dist/paper-lbesh.pdf` are byte-identical.
4. All 83 labels are unique, all 59 distinct reference targets resolve, and the set of 27 cited keys equals the bibliography key set. No scientific TODO/TBD/FIXME/PLACEHOLDER token occurs outside comments. The current build log has no undefined reference/citation, multiply-defined label or overfull box. The rendered text has no unresolved `??` marker.

Commands actually run include:

```bash
pdftotext -layout paper-lbesh/main.pdf paper-lbesh/process/stage05-author-rendered.txt
pdftotext -bbox paper-lbesh/main.pdf paper-lbesh/process/stage05-author-bbox.html
```

The first bounding-box checker attempted XML parsing, which rejected a control character emitted in mathematical text by `pdftotext`. This was a checker-format issue, not a failed paper assertion. The corrected narrow check parsed the numeric page/word tag attributes directly. All **21,446 word boxes on 42 pages** lie inside their pages. It wrote `stage05-author-checks.json`; this coordinate test alone does not establish aesthetic quality or absence of overlap.

The initial command `sha256sum -c paper-lbesh/SHA256SUMS` was mistakenly issued from the repository root, so the checksum file's relative delivery paths could not be opened. Reissued the documented command from `paper-lbesh`:

```bash
sha256sum -c SHA256SUMS
```

All three delivery hashes passed. Neither initial invocation issue changed a file or indicated a scientific failure.

Reviewed the inherited Stage 4 page images as context, then rendered the **current** PDF pages 1, 17, 30 and 42 with:

```bash
pdftoppm -f N -l N -scale-to 1400 -png -singlefile \
  paper-lbesh/main.pdf /tmp/lbesh-stage05-author-pageN
```

Viewed those four current images: corrected abstract, work table/figure, proof/counterexample, and reproduction instructions are readable without clipping. The accepted Stage 4 full build/layout and relocation checks remain applicable because all delivered bytes are unchanged. No new build or `scripts/package.py` run was needed; repackaging a no-change manuscript would add no confidence. No table regeneration, optimizer run, full witness audit, project-wide check or CI inspection was repeated.

## Explicit freeze for five independent final reviewers

`process/stage05-round01-source-sha256.json` fingerprints the same complete 68-path delivery/source set as accepted Stage 4. The supplement hash remains `f0399194ca1c9c57421965e236302c62e10eb72846ab807f936f18d9927d4b26`; PDF hash remains `f44179e023d34b7f8fefc44cbfa32b8b987faf84975dc240beea92301458ecf2`; source archive hash remains `8e0b1caa58e9fce0d967ade10bc36015acb524a3a1f0ac8287c5a4362b885532`.

Source is now frozen for the five required independent whole-manuscript reviews. I plan no further edits. The lead must evaluate those reports, assign all accepted corrections to a separate author, repeat five reviews if any accepted major issue occurs, and close valid minors before final acceptance. **Final-review status remains pending.**
