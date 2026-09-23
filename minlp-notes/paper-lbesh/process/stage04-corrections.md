# Stage 4 correction closure and frozen handoff

Correction author: `/root/stage04_corrections`. Date: 19 September 2026.

Read the lead disposition and all five independent Stage 4 round 1 reports. Implemented all six accepted minor correction groups. No subagents were spawned. Changes are confined to `paper-lbesh`; accepted full scientific sections, numerical data and the frozen research supplement remain unchanged. Stage 5 has not begun in this correction task and is not marked accepted.

## Item-by-item closure

1. **Abstract formulation distinction.** The abstract now describes established tangent inequalities lifted as perspective cuts in hull masters or deactivated in big-M masters. It no longer attributes the homogeneous perspective representation to big-M configurations.
2. **Standalone acronym.** The abstract expands nonlinear programming (NLP) on first occurrence, within the common-implementation description.
3. **Conic comparison.** The conclusion states that supported exact conic alternatives have lower common-solved mean times in the reported comparisons and explicitly adds that external coverage is mixed. The full results' FLay05 qualification remains unchanged; no coverage or per-instance dominance is claimed.
4. **Objective-error scope.** The conclusion now says “a general linear objective-error bound without additional joint regularity.” The ledger's matching shorthand also specifies a linear bound. No full proof or counterexample was changed.
5. **Overview assumptions.** The finite-rejection summary explicitly refers to global or selected-term rows at integer candidates. The ESH margin sentence requires a fixed strict anchor with a positive row-specific slack margin. Old-cut satisfaction remains explicit. The limiting-value summary now uses “vanishing valid outer-master suboptimality.” The separate fractional summary and complete theorems are unchanged.
6. **Coverage status.** Removed obsolete pending Stage 3 and unwritten Stage 4 statements. The ledger now consistently records Stages 1–3 accepted, Stage 4 complete with its minor corrections incorporated, and final Stage 5 review/acceptance pending. The empirical diagnostic's former reservation is replaced by its completed Stage 3 status.

## Commands and checks actually run

From the repository root:

```sh
python paper-lbesh/scripts/package.py > paper-lbesh/process/stage04-corrections-package.log 2>&1
```

Passed. The updated PDF has 42 pages. The package contains 62 source payloads plus its embedded manifest. The build log contains no undefined references/citations, multiply-defined labels or overfull boxes. The inherited underfull bibliography URL line remains cosmetic.

From `paper-lbesh`:

```sh
sha256sum -c SHA256SUMS
pdfinfo main.pdf | head -18
rg -n 'Undefined|undefined|Overfull|multiply defined|Underfull|Output written' main.log
pdftotext -layout main.pdf process/stage04-corrections-layout.txt
rg -n 'Separation guarantees|Conclusion|For global' process/stage04-corrections-layout.txt
```

All three delivery hashes passed. PDF metadata and the build log report 42 pages. An inline standard-library Python checker opened `dist/paper-lbesh-source.tar.gz`, checked its exact member set against the embedded manifest, compared the embedded and external manifests, checked the size and SHA-256 of every payload, and compared every payload byte-for-byte with the current source file. All 62 passed. It also checked `main.pdf` and `dist/paper-lbesh.pdf` for byte identity; they match.

Rendered PDF pages 1, 7, 8, 21 and 22 using `pdftoppm` with the following form (for each page number `N`):

```sh
pdftoppm -f N -l N -scale-to 1400 -png -singlefile paper-lbesh/main.pdf /tmp/lbesh-stage04-corrections-pageN
```

Viewed all five rendered images with `view_image`: title/abstract, overview heading and text, and conclusion/reference transition are legible without clipping or missing text. The text search established that the overview heading starts on page 7 and the conclusion on page 21; their substantive continuations occupy pages 8 and 22. These were layout checks, not a repeat scientific audit.

A final inline standard-library Python command wrote `process/stage04-corrected-source-sha256.json` using the union of the prior Stage 4 fingerprint paths and every source-manifest payload. This expanded fingerprint covers **68 files**, including the corrected coverage ledger and all other delivered source payloads, the PDF, source archive, checksums and manifests. This deliberately closes the prior fingerprint's incomplete coverage of a few packaged evidence files.

No data or numerical algorithm changed, so no fresh witness audit, optimizer benchmark, table regeneration, project-wide test or CI inspection was run. Existing independent evidence checks remain applicable.

## Delivery identifiers

- PDF: `f44179e023d34b7f8fefc44cbfa32b8b987faf84975dc240beea92301458ecf2`
- Source archive: `8e0b1caa58e9fce0d967ade10bc36015acb524a3a1f0ac8287c5a4362b885532`
- Unchanged research supplement: `f0399194ca1c9c57421965e236302c62e10eb72846ab807f936f18d9927d4b26`

## Source-frozen handoff

All requested Stage 4 corrections are closed in this snapshot. No further manuscript or packaged source edits are planned by this correction author. The corrected fingerprint above identifies the handoff for lead inspection. Stage 4 acceptance remains the lead's decision; the required Stage 5 whole-manuscript review remains pending.
