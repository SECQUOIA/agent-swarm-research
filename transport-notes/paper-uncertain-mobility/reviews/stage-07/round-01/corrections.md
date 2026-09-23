# Corrections: Stage 07, round 01

Fixer: `/root/paper_stage_fixer`, distinct from the Stage 07 author. Date: 2026-09-07.

Input reviewed snapshot: `d383884b23d489bd685197e179c0e74be518161c6cf0575298800612eae383c0`, preserved in [snapshot.json](snapshot.json). The [coordinator adjudication](adjudication.md) accepts four minor finding groups and no major issue.

| Accepted finding | Corrected locations | Correction and verification |
|---|---|---|
| Reviewer 1 R1-07-1 | `sections/07-numerics.tex`, lines 221–224 | Explained that the η=0 and η=2 mesh differences are smaller than remaining discrete optimization uncertainty. These comparisons show stability of returned objective values without separately resolving spatial discretization error. No further optimization or stronger error claim was added. |
| Reviewer 2 M1; reviewer 3 R3-01; reviewer 5 R5-01 | Same section, line 136 | Corrected the rounded mean-trial percentage from 0.0159% to 0.0158%. Recomputed from saved main and spatial-refinement values: relative change 0.00015841231081359375, or 0.015841231081359375%. |
| Reviewer 4, “unnormalized responses” | Same section, line 89 | Replaced this phrase with “unscaled ensemble moments,” accurately describing the saved aggregate quantities after equal discrete mobility-budget normalization. |
| Coordinator, missing spaces in new audit prose | `README.md`, `PLAN.md`, `claims-map.md`, `notation.md`, Stage 07 author handoff, literature audit, coordinator-check record, and Stage 07 portion of the build record | Inserted spaces in stage/section labels, prose before numerals, software-name/version boundaries, page references, and bibliographic prose. Corrected the joined prose “nonzeroV” and “finitevolume” in the new coordinator audit. Preserved code, identifiers, equations, version numbers, DOI/arXiv numbers, URLs, hashes, and original reviewer reports. The coordinator's quoted examples of the original defects remain unchanged as historical evidence. |

The README, plan, claim inventory, and notation introduction now accurately say that Stage 07 has completed its review and corrections, pending coordinator verification; the separate complete-manuscript review remains pending. No acceptance ledger or decision was changed. The author handoff remains a historical author record, with spacing corrections only.

Numerical checks from the unchanged saved data:

| η | Absolute 200-to-400-cell objective difference | 400-cell tangent gap | 200-cell tangent gap |
|---|---|---|---|
| 0 | 0.0005111343226911202 | 0.0016841067725783532 | 0.0006665439965025666 |
| 2 | 0.0009008384312663154 | 0.0021949839858290687 | 0.00019412667715235088 |

These values support the added limitation: each difference is below the remaining optimization uncertainty and cannot by itself isolate mesh error. The percentage rounding was checked separately from the same saved JSON. Numerical code, data, and figures were not altered or regenerated.

Verification:

- Forced the LaTeX/BibTeX build with `latexmk -g -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex` in the manuscript folder. It exited with status 0 and produced a 54-page PDF.
- Scanned the final `main.log`: no warnings, undefined-reference notices, or overfull/underfull boxes.
- Directly checked all nine edited source/document files for trailing whitespace, control bytes other than newlines, and final newlines. All checks passed; they include untracked files and do not rely on a Git diff.
- Compared every file against the 27-file frozen manifest. The seven listed changes below that belong to the manifest are exactly the changed manifest files. Accepted mathematical Sections 01–06, introduction/discussion, bibliography, numerical code/data/figures, and imported numerical scripts retain their frozen hashes.
- The coordinator-check and build-record prose files are also listed below although the original Stage 07 manifest did not include them. Original reviewer reports and the manifest remain untouched.

Corrected file hashes, relative to the manuscript folder:

| File | SHA-256 |
|---|---|
| `sections/07-numerics.tex` | `668c4dec64bf985066358398f2700b40327197e4057d76ba3dd1f0427404fea6` |
| `README.md` | `ea372940dd9efe308a901d1c8586e82a0757561ad996a51d116b8fc6b140e0ee` |
| `PLAN.md` | `6fb78d693abb5da83319214bee049229380d8f28502e850d2f9120ca625c54af` |
| `claims-map.md` | `1d3910f7ac95c94157a8164bb9f56f01c165646f78239fd6fe0887b878b119d1` |
| `notation.md` | `47033f56077122cae081664e4fd22ad8d829f98a99b0651ec70c43991a7f1753` |
| `reviews/stage-07/author-handoff.md` | `5267d372cde8a399f792081e0e3091b801206bd0d5ae8bba9980cab4183285d0` |
| `reviews/stage-07/literature-audit.md` | `f31994d9082164bc962f012181e4933d7eab2253496569ab4c61006a89e69ae0` |
| `reviews/stage-07/coordinator-checks.md` | `5bd3f4666efe4128ee38be9ab016c1248cf64ad8682d61952c94b1113a764d2d` |
| `reviews/build-and-reproducibility.md` | `9d289cba6e1e9d852abafab96d85ec3237d1bd7b6e72188bb4c24d81a90d7750` |

Editing is complete. No substantive claim changed and no major issue emerged. Coordinator verification and stage acceptance remain required before the separately mandated five-reviewer complete-manuscript audit. This correction record accepts neither the stage nor the manuscript.
