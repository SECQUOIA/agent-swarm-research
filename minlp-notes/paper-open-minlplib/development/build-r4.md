# Final build, claim register and release checks, revision 4 (2026-10-05)

This pass ran after the seven editing groups (G1–G7) of the round-2 revision. It
resolved the cross-group inconsistencies that the editors reported, ran G7-09
(merge of the moved passages, index rebuild, recipe test), regenerated the
tables and figures, built both documents once from an empty `build/`, validated
the claim index, scanned both PDFs, wrote `artifact/RELEASE.md` and measured the
page counts. Nothing was committed. Nothing in `research-20260929/` or
`literature/` was edited. No certified number changed. Every command ran on two
cores (`taskset -c 0,1`). A backup of the paper directory before this pass is
`/tmp/r4/paper-before-build-r4.tar`; the logs of this pass are in
`development/build-r4-logs/`.

All checks below are targeted local checks run in this pass. No CI result was
consulted.

## 1. Result in brief

- `make` from an empty `build/` exits 0: 0 LaTeX errors, 0 undefined
  references or citations (both directions), 0 multiply defined labels
  (400 labels, none defined twice within or across the two documents),
  0 BibTeX warnings, 0 overfull boxes, no other LaTeX warnings, no `??`, and
  no stray `supplement.pdf`/`main.pdf` string in either PDF.
- `build/main.pdf` has 56 pages (revision 3: 60), `build/supplement.pdf` 131
  (revision 3: 135).
- The float check passes (0 flagged pages, 31 of 31 closure names). Every table
  and figure page was inspected by eye. Table 1 (upright) has no overlap; Table 2,
  Figure 1, `tab:trust-full` (Table S37) and the register (Table S38) print in
  full.
- Generators: `make_tables.py` 799 checks, 0 failed; `make_campaign_table.py`
  115 ok; `make_points_table.py` 108 ok; the five figure scripts exit 0 and
  render pixel-identical to their previous versions.
- Claim index rebuilt (schema 2) and validated: `PASS: 65 claims; 5604 SHA-256
  references; 1914 distinct files`. Section S7.1 now quotes these counts.
- The S7.1 recipe, run as printed on a stand-in archive of the final sources,
  passes, and so do the 15 short checks under it; the real `~/.cache` is
  unchanged.
- `artifact/RELEASE.md` holds the SHA-256 of both PDFs, the build date and the
  validator's PASS line.
- Printed placeholders: four declaration `[TODO: …]` items (licence, AI-use
  confirmation, competing interests, funding) and four `[archive DOI]`.
- Length targets are not met: Sections 1–11 run to 41.07 pages (target about
  38; revision 3: 42.85), and the supplement body S1–S7 to 120.11 pages
  (target about 105; revision 3: 124.91). Section 10 gives the figures.

## 2. Cross-group inconsistencies resolved

Each fix is the smallest change that makes the sources agree. Status words,
displays and statements are unchanged.

1. **Reason for the `ann_cumene_tanh` status** (G1 open 2, G5 open 2, G6 open 2).
   §2.6 defines "separately written" by what the code does (no import, no run, no
   copied code) and says that most second sessions read the first code. Four
   places still gave reading as the reason the second `ann` code is not
   separately written. They now give the recorded reason, the copied idiom
   (`rem:ann-saturation`), as §2.6, Table 1 and Table S37 already do:
   - `05-other.tex` (proof sketch of `thm:ann-bound`): "the second code copied one
     idiom of the first, so it is not separately written …";
   - `B9-ann-kan.tex`, paragraph after `rem:ann-saturation`: the session also
     read the first in full, "and the second copied one idiom of the first";
   - `B9-ann-kan.tex`, certificate box, field Implementations;
   - `I-reproduction.tex`, register row of `thm:ann-bound`: "proved (the second
     code copied an idiom of the first)". The builder reads a parenthesis without
     a colon as a qualifier of the whole row, so the status word stays *proved*.
2. **KAN replay time** (`B9-ann-kan.tex`, certificate box, field Replay). Path (II)
   for the `r5` models read "87 s to 19 min". The record is 87.33 to 1083.76 s
   (`research-20260929/publication/integration/runtime-table-r1.md`), that is,
   18 min, as the register and `RUNS.md` R20 say. Now "87 s to 18 min".
3. **QPLIB copy times in the register** (G5 open 4). Row 25 (`prop:qplib-copies`
   and the other reported-value propositions) gave only "seconds". The exact
   optima of the QPLIB copies, which `prop:qplib-copies` uses, take under 2 s
   (second parser) and about 10 + 5 min (first parser), as the S1.3 certificate box
   states after G5-08. The time cell now reads "seconds; QPLIB copy optima under
   2 s and about 15 min (two parsers)", and `RUNS.md` R25 gives the details. The
   tier stays 1 (under 10 min per instance).
4. **Overfull boxes** (G6 open 6):
   - The table of contents: the number "S1.10" was 0.36 pt wider than the
     default number field. `supplement.tex` widens the field of subsection
     entries from 2.3em to 2.7em (with a comment).
   - The 14.7 pt overfull line is in `B5-small.tex` (pricing050 multipliers), not
     in `B4-chain-catmix.tex` as G6 reported. Reordering the inline list made it
     worse (30 pt). The three multipliers are now a display; the text is
     unchanged.
5. **S7.1 counts**: 5,334 and 1,894 became 5,604 and 1,914 (Section 6).
6. **Development records**:
   - `terminology.md`: the line saying that the abstract keeps "calibrations" was
     stale (G1 open 2). It now says that the abstract does not use the word.
   - `labels.md`: §9 lists its labels (`sec:interpretation-structure` with the
     paragraph labels `sec:interpretation-evidence` and
     `sec:interpretation-reading`, and `sec:conclusion-recs`); §11's labels are
     marked as paragraph labels (G4 open 2); `prop:scip-reproducers` and
     `lem:scip-cube` are marked as moved to S6.6. The G2 and G5 label items were
     already done by G7, and no stale entry remains.

Checked and found consistent, so no change was made:

- KAN tiers (`r3` Tier 1, `r5` Tier 2) in Table 7, the S1.9 box, the register,
  `RUNS.md` and the README (G4 open 3).
- The §3.2 class glosses on which G3-09 relies (G3 open 5).
- The `eg` cancellation figures (61.4 against 7.115), which are in S1.7 (G3 open 6).
- The KAN guard wording in S1.9, which agrees with §5.5.
- §9's pointer to the box counts of §1.2, §8's use of "floating-point output"
  (§2.6), and §3.1's pointer to the closure terms in §2.2 (G4 open 4, G2 open 5).
- "Separately written" in §4, §5 and S1 (G2 open 2, G3 open 7). It is
  consistent with the current §2.6 definition. Whether to keep that definition
  is the lead author's decision (Section 10, item 1).

## 3. G7-09: integration of the moved passages

- `artifact/HISTORY.md` §4 now holds the history passages of
  `development/moves/r2-G5.md` and `r2-G6.md`, each under a heading that names
  its source file and label:
  - the provenance of the former S8 table;
  - the earlier interval branch and bound for `eg_int_s`;
  - the stopped `waterno2` multiplier searches;
  - the first run of KAN path (I) with the library exponential.
- `artifact/RUNS.md`, section "Run records moved from the supplement", now holds
  the run records. Its 27 entries are grouped by register row (R01, R03, R05–R08,
  R10, R11, R14–R18, R20, R22–R24, R26) and include `tab:catmix-grids` as a
  Markdown table and the script names of the former S7.4.
- How the passages were merged:
  - The notation is converted to Markdown.
  - "The authors' code" became "the first code", which is the round-2 mapping and
    was checked against the r3 sources, for example for `catmix`.
  - Where the r3 context named the code, it is given (the third `ex6_2`
    implementation, the `chain` scripts).
  - Every path that the merged text names exists.
  - The "destination: none" passages (MINLPLib's own listed data) were not
    copied, as the moves files say.
- The new headings do not match the `### Rnn.` block pattern, so the builder
  and the validator still see 27 register blocks.
- In the README's file table, the `RUNS.md` and `HISTORY.md` rows mention the
  merged material, and the log rows describe the new logs (Section 7).

## 4. Generators, from `/tmp` copies

Each generator was copied to `/tmp/r4/gen/`. The only change in the copy is the
line `HERE = Path(__file__).resolve().parent`, replaced by the absolute path of
the original folder (likewise `P = …` in `check_floats.py`).

```bash
cd /tmp/r4/gen && taskset -c 0,1 python3 make_tables.py          # 799 checks, 0 failed
cd /tmp/r4/gen && taskset -c 0,1 python3 make_campaign_table.py  # 115 ok
cd /tmp/r4/gen && taskset -c 0,1 python3 make_points_table.py    # 108 ok
cd /tmp/r4/gen/fig && taskset -c 0,1 python3 make_fig_<name>.py  # all five exit 0
```

- Every `tables/*.tex` file was reproduced byte for byte.
- In `data/numbers.json` and `data/check.log` only the SHA-256 of
  `development/outline.md` changed (G7 edited §8 item 11). A recursive diff of
  `numbers.json` shows no other difference, so no value or provenance changed.
- Figures rendered at 60 dpi are pixel-identical to the previous PDFs, and the
  headline figure's own checks pass ("all figure checks passed").

## 5. Build and layout

Private builds in `/tmp/r4/priv/` and `/tmp/r4/priv2/` found the overfull boxes
of Section 2, item 4, and confirmed the final layout. After the last source edit:

```bash
rm -rf build && taskset -c 0,1 make                                         # exit 0 (00:53:46–00:54:07)
grep -a 'undefined\|multiply defined' build/main.log build/supplement.log   # nothing
grep -a 'LaTeX Warning' build/*.log | grep -v 'TODO\|archive DOI'           # nothing
grep -a -c Overfull build/main.log build/supplement.log                     # 0, 0
grep -a -i 'warning\|error' build/*.blg                                     # "warning$ -- 0" only
pdftotext build/main.pdf - | grep -c '??'                                   # 0
pdftotext build/supplement.pdf - | grep -c '??'                             # 0
cd /tmp/r4/gen && taskset -c 0,1 python3 check_floats.py                    # 0 + 0 flagged, 31 of 31
```

The final `make` ran once, from an empty `build/`, with no other build running.
Rendered at 40 dpi, its pages are identical to those of the private build that
was inspected, except page S117, where the S7.1 counts changed; that page was
inspected again.

Pages inspected by eye:

- **Main:** all 56 pages on contact sheets (30 dpi), then pages 10 (Table 1; the
  `ann_cumene_tanh` row also at 250 dpi), 12 (Table 2, sideways, rotated and
  read in full: caption and all 31 rows, including the three `eg` rows), 13
  (Figure 1, Table 3), 14 (Table 4), 31 (Table 5), 34 (Table 6), 41 (Table 7)
  and 51 (Table 8), at 80–110 dpi.
- **Supplement:** all 131 pages on contact sheets. Every page with a table,
  figure or longtable continuation was viewed at 50 dpi (pages 3, 5, 8, 13, 16,
  18–20, 25, 41, 45, 47, 52, 53, 58, 64, 66, 76, 78–82, 84–86, 89, 92–95, 98,
  102, 105–109, 111, 118–121). The sideways Tables S1 (page 3), S33 (page 108)
  and S37 (`tab:trust-full`, page 119) were rotated and read at 90–100 dpi, and
  the register (pages 120–121) was read at 90 dpi.

No clipping, overlap or cropped float was found.

Remaining underfull boxes are mild and the same as in revision 3:
`01-introduction.tex:85–90` (badness 1122), `H-solvers.tex:28–33` (the GAMS
command line, 2913), `H-solvers.tex:109` and `:234` (SHA-256 prefixes in two
certificate boxes, 1286–3746), and one bibliography entry in each document
(1308).

## 6. Claim index

```bash
cp $P/artifact/build_claims.py $P/artifact/check_claims.py /tmp/r4/claims/
cd /tmp && python3 /tmp/r4/claims/check_claims.py --repo-root <repo>   # old index (schema 1): KeyError 'runs_file'
cd /tmp && python3 /tmp/r4/claims/build_claims.py --repo-root <repo> \
    --output <repo>/paper-open-minlplib/artifact/claims.json           # BUILT 65 claims; 1914 artifacts; 0 unresolved
cd /tmp && python3 /tmp/r4/claims/check_claims.py --repo-root <repo>   # PASS: 65 claims; 5604 SHA-256 references; 1914 files
# S7.1 counts updated (I-reproduction.tex is hashed), then build and validate again: same counts
# after the final make, validate again: PASS, same counts
```

- The index in the tree was the revision-3 index (schema 1), which the new
  validator cannot read. The rebuilt index has schema 2.
- Its register entries meet LD2-4 and G7-02:
  - `register-07` and `register-08` carry the `waterno2` displays (L, U and gap
    for all five instances).
  - The status word is recorded per instance:
    - `register-17` (`eg`) is *proved* because of `eg_disc2_s` (partial second).
    - `register-21` (points) is *proved* because of `etamac` and `pricing050`.
    - `register-18` (`ann_cumene_tanh`) is *proved*.
    - `register-03`, `-04`, `-06`, `-12` and `-13` are *weaker second*, that is,
      *proved*.
  - `recorded_commands` are matched by full path and working folder.
- `artifact/logs/build_claims.log` and `check_claims.log` record these runs.
- The `/tmp` copies are byte-identical to the artifact scripts.

## 7. Recipe test and short checks

The S7.1 recipe was run as printed (driver `/tmp/r4/recipe/recipe-test.sh`):

- **Archive:** a stand-in at `/tmp/r4/archive`, with the research tree as in the
  repository and the final paper tree without `build/`. Only the `ARCHIVE` line
  differs from the printed recipe.
- **Output changes:** pip ran with `-q`, two lines list the installed versions,
  and the output of `make_tables.py` is cut to its last line.
- **Times:** 00:47:28 to 00:50:59, affinity mask 3 (cores 0 and 1).

Results:

- In the copy, the validator gives the same PASS line as in Section 6.
- pip installed the pinned versions.
- `prepare_paper_inputs.py`: `PASS: saved inputs intact; all 69 paper models
  verified …; 26 manifest models not needed by the paper are absent`.
- `make_tables.py`: 799 checks, 0 failed.
- The short-check runner (`/tmp/minlp-artifact-u00_1o0k`, affinity [0, 1]): all
  15 checks exit 0, and `failed` is empty:

| check | wall s | last line or comparison |
|---|---:|---|
| `lnts` | 13.4 | `PASS: all four models, exact sign certificates, …`; certificate fields all equal |
| `dtoc5` | 21.6 | `PASS`; result fields equal except elapsed time and affinity |
| `kan_r3_h1_n4`, `_n5`, `_n9` | 35.2, 30.7, 67.6 | result fields equal except `time` |
| `test_auditor` | 1.7 | `ALL AUDITOR TESTS PASSED` |
| `test_negative` | 129.0 | `ALL NEGATIVE TESTS PASSED` |
| `boundary_check` | 6.9 | `ALL OK` |
| `check_copies` | 0.1 | `ALL COPY CHECKS PASSED` |
| `dtoc5_displays` | 0.0 | `PASS: paper endpoints, interval width, and both rounded-up gap displays` |
| `dtoc5_boundaries` | 0.4 | `PASS: exact infeasibility, terminal override, and row-sign checks` |
| `kan_audit` | 8.4 | `ALL AUDIT CHECKS PASSED` |
| `independent_numeric` | 3.2 | `PASS` |
| `source_and_range` | 4.1 | `PASS` |
| `verify_artifacts` | 3.6 | `PASS` |

- The real `~/.cache` was listed before and after (278,873 entries, with type,
  size, modification time and path). The listings do not differ, also after the
  negative controls.
- The only new top-level entries in `/tmp` are the runner's folder and `WORK`.
- G7's four negative controls of `prepare_paper_inputs.py` were rerun in the
  same copy (a changed model byte, a missing paper model, `HOME` not isolated,
  `MINLPLIB_OSIL_ROOT` unset). Each fails with its specific message, and the
  restored copy passes.
- The optional `--eg-int` regeneration (about 5 min) was not rerun.
- After the controls, the disposable `WORK` copy and the stand-in archive
  (8 GB) were removed; the short-check runner's folder
  `/tmp/minlp-artifact-u00_1o0k` remains.

Files written:

- `artifact/logs/recipe-test.log` replaces G7's test, which used round-3
  sections.
- `artifact/logs/short-checks.json` and `artifact/logs/short-checks-r4/` (the
  15 outputs) record this run.
- The earlier packaging run is kept as `artifact/logs/short-checks-packaging.json`.
  The README cites it for the `--eg-int` time (323.818 s) and for the initial
  setup failures and their corrections, which the new file does not contain.
- The README's file table and its `--eg-int` paragraph name both files.

## 8. `artifact/RELEASE.md`

| field | value |
|---|---|
| build date | 2026-10-05, 00:53:46–00:54:07 (−04:00), from an empty `build/` |
| `build/main.pdf` | `d281b3131b7f1cecf85819a74ba2615a13a00a0ab6a20f54f12af1a77918772d` (56 pages) |
| `build/supplement.pdf` | `a6e6463ebaa1fc4c48dcde583bf40a9d5c5af8aeb1d70040535ca6a595761472` (131 pages) |
| validator | `PASS: 65 claims; 5604 SHA-256 references; 1914 distinct files; …` |

`RELEASE.md` separates source and evidence validation (`check_claims.py`) from
PDF identification (the two hashes), as S7.1 and the README do. It is not hashed
in the index. The hashes were checked again after the last command of this pass.
Nothing was rebuilt after they were written.

## 9. Scans (pdftotext, line-end hyphens joined)

Outputs: `development/build-r4-logs/scan-*.txt`.

### Placeholders and `??`

- `??`: none in either PDF.
- `[TODO: …]`: four, all in the main paper's declarations:
  - licence of the archived code and data;
  - "authors to confirm, here and in Section 2.6, including which proofs and code
    the authors checked themselves";
  - competing interests;
  - funding.
- `[archive DOI]`: four, on main pages 4, 40 and 42 and supplement page 116.
- No other bracketed placeholder prints.

### Banned phrases (style guide)

- **Main paper:** none. "significant" occurs only in "significant digits"; one
  hit is split by a page break.
- **Supplement:**
  - "If moreover" occurs inside two lemma statements.
  - "we claim no novelty" and "novelty statement" occur in S1 and S3.
  - "leveraging" and "Robust" occur in two cited titles.
  - "significant bits" occurs in S5.
- **"Independent":** in the main paper only "weaker than independent
  development" and "code from independent teams" (§2.6). In the supplement it
  occurs only in the mathematical sense.

### Build-phase scans (adjudication Section 9)

- **"Tier" in §§4–5 (main pages 15–29):** none. In the main paper "Tier" occurs
  only on page 41 (§10, Table 7 and the tier rule).
- **"authors' code/search/script", "verifier's":** none in either PDF.
- **"public archive":** none.
- **Outline §8 item 11 strings:**
  - None prints, with one allowed exception: 352.238025369202, which occurs only
    as the weaker bound that the other `lukvle10` implementation certifies
    (main page 21; supplement pages 8 and 119).
  - The prefix hits for "15.294675643368092" are the correct display
    −15.29467564336809217.
  - The hits for "4.36" are unrelated numbers (−4.3679…, 4.36·10⁻⁷).

### Internal names

- **Main paper:**
  - No script or file name, no `$R`/`$P`, no `development/` or `research-…`
    path, and no register or decision identifier.
  - No "wave", "dossier", "critique", "route", "round …", "workflow" or model
    code name.
  - "AI", "Anthropic Claude" and "OpenAI GPT" occur only in §2.6 and the
    declarations. "Agent session(s)" occurs in the §2.6 sense (§2.5, §2.6, §3.1,
    §7, §8.2, §11, A.2).
- **Supplement outside S7:**
  - No `.py`, `.json` or `.log` name and no internal folder name.
  - The only file names are `noncvx_gurobi.csv`, the public CAMINO file (S6.7),
    and MINLPLib's public `.sol` file type.

## 10. Page counts

Measured from the bookmark positions in the final PDFs (A4, 11 pt, 25 mm
margins) with `/tmp/r4/pages.py`, the revision-3 script
(`development/build-r4-logs/pages.txt`). The declarations and References
headings were located with `pdftotext -bbox`. Floats count where they print. A
count of 1.00 is one full text area. The targets are those of the adjudication
(Section 2).

### Main paper (`build/main.pdf`, 56 pages)

| part | pages | target | difference | revision 3 |
|---|---:|---:|---:|---:|
| Title, abstract, keywords | 0.66 | – | | 0.64 |
| 1 Introduction | 4.34 | 3.8 | +0.54 | 4.59 |
| 2 Semantics (with Table 1) | 5.78 | 5.6 | +0.18 | 6.58 (with Figure 1) |
| 3 Results (with Table 2 (a full sideways page), Figure 1, Tables 3–4) | 3.69 | 3.1 | +0.59 | 3.19 |
| 4 Split certificates | 6.78 | 6.6 | +0.18 | 7.18 |
| 5 Other certificates | 7.24 | 6.6 | +0.64 | 7.09 |
| 6 Points (with Table 5) | 2.51 | 2.2 | +0.31 | 2.49 |
| 7 Audit (with Table 6) | 3.32 | 2.9 | +0.42 | 3.59 |
| 8 Solvers | 3.27 | 3.0 | +0.27 | 3.51 |
| 9 Interpretation and recommendations | 2.12 | 1.6 | +0.52 | 1.40 (interpretation only) |
| 10 Reproducibility (with Table 7) | 1.29 | 1.2 | +0.09 | 1.41 |
| 11 Limitations and conclusion | 0.73 | 0.7 | +0.03 | 1.83 |
| **Main text, Sections 1–11** | **41.07** | **about 38** (37.3) | **+3.07** | **42.85** |
| Statements and declarations | 0.52 | – | | 0.51 |
| References | 6.85 | – | | 7.31 |
| Appendix A Model semantics | 3.29 | ≤ 3.3 | −0.01 | 3.42 |
| Appendix B Proofs for the split certificates | 2.99 (3.61 counting the last page, which is 38% full, as full) | ≤ 3.0 | −0.01 | 4.35 |

Group totals for Sections 1–11:

| group | sections | pages | target |
|---|---|---:|---:|
| G1 | §1–§2 | 10.12 | 9.4 |
| G2 | §3–§4 | 10.47 | 9.7 |
| G3 | §5–§7 | 13.07 | 11.7 |
| G4 | §8–§11 | 7.41 | 6.5 |

Section 3 now holds Figure 1 (about half a page), which printed inside §2 in
revision 3, besides Table 2 (a full sideways page) and Tables 3–4. So the §2/§3
split differs from revision 3 and from the editors' private measurements, whose
float placement differed (G2 measured §3 at 3.13).

### Supplement (`build/supplement.pdf`, 131 pages)

| part | pages | target | difference | revision 3 |
|---|---:|---:|---:|---:|
| Title, note, contents | 1.46 | – | | 1.48 |
| S1 opening (before S1.1) | 0.37 | | | 0.33 |
| S1.1 lnts, lukvle10 | 6.17 | | | 6.61 |
| S1.2 dtoc5, optcdeg2 | 6.50 | | | 6.75 |
| S1.3 camshape | 5.27 | | | 5.47 |
| S1.4 chain, catmix | 9.22 | | | 10.20 |
| S1.5 six small instances | 10.34 | | | 10.75 |
| S1.6 powerflow | 6.02 | | | 6.47 |
| S1.7 eg | 7.11 | | | 7.41 |
| S1.8 waterno2 | 6.13 | | | 6.41 |
| S1.9 ann, KAN | 8.20 | | | 8.35 |
| S1.10 explanatory results on splits (new) | 1.21 | | | – |
| S5 eg rounding-error analysis | 7.68 | | | 7.82 |
| **S1 and S5 (G5)** | **74.22** | **66** | **+8.22** | **76.57** |
| S2 Exactly feasible points | 6.89 | 6.2 | +0.69 | 7.10 |
| S3 Prior literature | 7.38 | 6.8 | +0.58 | 7.05 |
| S4 Audit details | 12.73 | 10.8 | +1.93 | 12.81 |
| S6 Solver campaign, SCIP defect | 12.23 | 10.9 | +1.33 | 12.57 |
| S7 opening, S7.2 (with Table S37, 1 page), S7.4, S7.5 (G6) | 3.59 | 2.3 | +1.29 | – |
| S7.1, S7.3 (G7) | 3.07 | 2.2 | +0.87 | – |
| S7 together | 6.66 | 4.5 | +2.16 | 8.82 (S7 7.02 + S8 1.80) |
| **Content S1–S7** | **120.11** | **about 105** | **+15.11** | **124.91** |
| References | 8.81 (9.43 counting the last page, 38% full, as full) | – | | 8.02 |

Float attribution:

- The sideways Table S37 (`tab:trust-full`, page 119) prints inside S7.3's
  bookmark span. It is counted with S7.2 above, as G7 asked; the bookmark spans
  give S7.2 1.20 and S7.3 2.60.
- Table S17 (S2.4) prints on page 76, inside S3's span (G6 open 5). Counted with
  S2, S2 would be about 0.9 page longer and S3 about 0.9 shorter.

## 11. Open items for the lead author and the authors

1. **G1-02, definition of "separately written" (G1 open 1).** This needs the lead
   author's decision.
   - The tree uses G1's code-based definition: no import, no run and no copied
     code. Under it, only the second `ann_cumene_tanh` code is excluded, because
     it copied an idiom.
   - Table 1, Table S37, the register, `RUNS.md`, the abstract and §§1–7 and S1
     are consistent with this definition after Section 2, item 1.
   - G1 checked the session records against the adjudication's reading-based
     rule. Adopting that rule would relabel about nine families (lnts, dtoc5,
     optcdeg2, camshape, chain, catmix, pindyck, powerflow0039, waterno2) and
     rewrite about 100 sentences, Table 1 and the register.
2. **Length.** The main text is 3.07 pages over about 38 and the supplement body
   15.1 pages over about 105. Each editor stopped at the content floor and listed
   the indispensable material (G1–G7 reports). Their options need a lead-author
   decision:
   - G3: move the ann prior-work note, Corollary 5.12, the §6.1 credit details
     and determinant remark, the glider/topopt details, the powerflow motivation,
     and the camshape gap sentence; about 0.6 page.
   - G4: move §9's related-effects paragraph to S3.1; reduce the
     recommendation evidence to cross-references; about 0.4 page.
   - G6: shorten the `tab:audit-pairs` caption by 2–3 main-text lines (G3 open 3;
     not applied here).
   - G5: move `prop:chain-weierstrass`, `lem:catmix-losses`, `prop:pf-double`
     with `cor:pf-shor`, four remarks and `tab:kan-rerun`; about 4.3 pages,
     which still leaves about 69 against 66.
   - G6: move `tab:campaign-runs` and `tab:audit-inputs` with the hash lists, and
     shorten `tab:literature`; about 1.8 pages (and about 0.25 for pointers in
     S7.4).
   - G7: drop the primal checker names from the register.
3. **Author confirmations and actions** (placeholders print only in the
   declarations):
   - the AI-use wording in §2.6, the declarations and the README (which carries
     its own marker);
   - which proofs and code the authors checked themselves;
   - the licence, the archive DOI, competing interests and funding.
4. **Upstream communication (LD2-3).** §7.4 (MINLPLib maintainer), §8.2 and
   S6.6 (SCIP developers) and the README say that communication is pending at
   the time of writing. If the authors file the report or contact the maintainer before
   submission, these sentences must be updated (R2-04).
5. **Recipe on another machine.** The recipe test used one machine and a
   stand-in archive (G7 open 4). A test on another machine with the deposited
   archive remains for the authors. Once the archive is deposited,
   `RELEASE.md` should be updated if the PDFs change; a rebuild changes their
   bytes.
