# Stage 4 independent review 04, round 1

Date: 19 September 2026. Scope: integration narrative and overview, portable artifacts, packaging/verifier scripts, mandatory source checker, extraction/import instructions, and delivered source/PDF correspondence. Read the Stage 4 author report and source fingerprint. No other current review reports were inspected.

## Verdict

No major issue found. The portable source and research supplement are internally consistent; their manifests match the actual delivered files. A clean build from a fresh source extraction produces exactly the authoritative PDF's text. The documented import override selects the extracted model/checker sources. The required research-root check fails when its argument or source is missing. Isolated repackaging reproduces the delivered source archive byte-for-byte.

The integrated narrative remains scientifically qualified and the concise guarantees overview agrees with the full results and their assumptions. Two small scope corrections would make the abstract and conclusion as precise as the body.

## Major findings

None.

## Minor findings

1. **Restrict perspective inequalities to the hull master in the abstract.** `sections/abstract.tex`, sentence beginning “Both policies use established perspective inequalities …”, places that description immediately before both hull and big-M masters. The big-M variants use deactivated original-space tangents, not the displayed lifted perspective inequalities. The body already makes this distinction correctly. Suggested replacement: “Both policies generate established tangent inequalities, lifted as perspective cuts in hull masters or deactivated in big-$M$ masters, within a common NLP-assisted implementation with single- or multiple-tree execution.” Equivalent shorter wording is fine; retain the shared-framework and non-novelty message.

2. **State the conic conclusion in terms of the measured statistic.** `sections/conclusion.tex`, first paragraph, says the advantage does not “defeat supported exact conic alternatives.” This is imprecise relative to the actual mixed coverage findings (for example, some prototype configurations solve `FLay05` while the conic formulation leaves it open). The abstract already uses the accurate common-solved mean-time qualifier. Replace the concluding phrase with a direct result such as “does not improve common-solved mean time over the supported exact conic baselines.” This preserves the unfavorable aggregate timing result without implying coverage or per-instance dominance.

## Scientific integration assessment

Read `abstract.tex`, `discussion.tex`, `conclusion.tex`, `guarantees-overview.tex`, and the revised `main.tex` in full. The overview preserves the compact-domain, finite-row, bounded-gradient and retained-cut premises; the fixed-weight rule is correctly distinguished from the residual-calibrated rule. It does not turn residual rejection into a gap or exact-optimality guarantee. Its representation discussion now expressly requires a convex increasing re-expression and references the stronger detailed qualifications. The per-disjunction repair limitation and lack of a general dominance statement are retained. Moving the proofs/diagnostics into appendices does not remove their references or change their mathematical statements.

The discussion retains the shared ECP initialization, related controls, same-seed repetitions, preliminary cone exposure, negative external coverage result, conic alternative, numerical interface follow-ups, and dependence on NLP recovery. It does not claim a first-ever algorithmic framework, a new perspective-cut family, or a universal empirical advantage. The final reproducibility appendix clearly distinguishes numerical validation, independent aggregation, fresh model construction, optimization reruns and exact certification.

## Portable artifact checks actually performed

- Read `scripts/package.py`, `scripts/verify_supplement.py`, the mandatory `evidence/check_stage02.py`, main/supplement README files, and `appendix-reproducibility.tex` in full. Inspected extracted `gdp_instances.py` and `pyproject.toml` to check relative example paths and the editable local GDPlib dependency.
- Verified all 62 entries of `process/stage04-author-source-sha256.json` against the current files; no mismatch. Ran `sha256sum -c SHA256SUMS`; all three deliveries passed. `main.pdf` and `dist/paper-lbesh.pdf` are byte-identical.
- Independently opened the source archive with Python `tarfile`, checked regular safe member names, compared its embedded manifest to `dist/source-manifest.json`, verified every payload size/hash, and compared every payload's bytes with the corresponding current working file. All 62 payload files plus the manifest matched.
- Extracted the checked source archive into `/tmp/lbesh-r04-stage4-f465kmij/paper-lbesh`. A clean `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` completed there, producing 42 pages. `pdftotext -layout` output is identical to that of the authoritative PDF. The final log has no unresolved references/citations, overfull boxes or multiply-defined labels; the inherited underfull bibliography URL remains cosmetic.
- Ran `verify_supplement.py` once without extraction, then with `--extract /tmp/lbesh-r04-stage4-f465kmij/research`. Both passed: fixed archive SHA-256 `f0399194ca1c9c57421965e236302c62e10eb72846ab807f936f18d9927d4b26`, 9,077 members, 9,076 verified payload files and 174,719,872 uncompressed payload bytes.
- From the isolated source, ran `scripts/check_evidence.py` and `evidence/check_stage02.py --research-root /tmp/lbesh-r04-stage4-f465kmij/research`; both passed. Separate calls with no research-root argument and with an incorrect root both failed, as required. These are selected example/default checks, not blanket theorem or source certifications.
- From the extracted `research/code/minlp_solver_lab`, reused the pinned virtual-environment interpreter with `PYTHONPATH` set to the extracted `instances/gdplib_src`. An import probe confirmed that `gdplib`, `gdp_instances`, and `lbesh_research.validation` all loaded from the extracted research tree. The archived example loader's `EXAMPLES` path is relative to its extracted file, so that route also does not refer to the original checkout.
- Copied the separately delivered frozen supplement into the isolated paper's `supplement/` directory and ran `scripts/package.py` twice there. Both source archives were byte-identical to each other and to the delivered source archive, SHA-256 `dcb7950a4e9a74812291b3da289fc12dfbbeacad62db90ace88413bb6c544324`. This verifies the documented separation of the large supplement from the compact source package and the deterministic source packaging on unchanged inputs.

The full extracted-model audit had already passed during Stage 4 authoring and was not duplicated: no concrete inconsistency found here justified another 1,464-witness replay. No fresh dependency installation, optimization benchmark, broad project check, or CI inspection was performed. All build, extraction and packaging mutations were isolated under `/tmp`; only this report was added to the repository. Final whole-paper review remains the next prescribed stage after corrections and Stage 4 acceptance.
