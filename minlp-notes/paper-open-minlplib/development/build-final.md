# Final build and release checks after the round-3 revision (2026-10-05)

This pass ran after the four round-3 editing groups (F1–F4). It resolved the
cross-group inconsistencies that the editors reported, regenerated the tables
and figures from `/tmp` copies of the generators, built both documents once
from an empty `build/`, inspected every table and figure page, rebuilt and
validated the claim index, ran the 15 short checks from a fresh copy of the
runner, scanned both PDFs, wrote `artifact/RELEASE.md` and measured the page
counts.

- Nothing was committed.
- Nothing in `research-20260929/` or `literature/` was edited.
- No certified number changed.
- Every command ran on at most two cores (`taskset -c 0,1`).
- A backup of the paper tree before this pass (without `build/`) is
  `/tmp/final/paper-before-final.tar`.
- The pre-round-3 sources used for the diffs are `/tmp/suppgrp-orig/` (F4's
  copy, taken before any round-3 edit; its main sections are byte-identical to
  F1's and F2's own backups).
- The logs of this pass are in `development/build-final-logs/`.

All checks below are targeted local checks run in this pass. No CI result was
consulted.

## 1. Result in brief

- `make` from an empty `build/` exits 0. Both logs show 0 LaTeX errors and 0
  overfull boxes. There are no undefined references or citations in either
  direction and no other LaTeX warnings besides the placeholders. No label is
  defined twice (400 labels: 137 in the main paper, 263 in the supplement, none
  shared). BibTeX reports 0 warnings, and neither PDF contains `??`.
- Page counts: `build/main.pdf` has **56 pages** and `build/supplement.pdf`
  **131 pages**, as in revision 4.
- The float check passes: 0 flagged pages, and all 31 closure names print.
  Every table and figure page was inspected by eye (Section 5).
- Generators:
  - `make_tables.py`: 851 checks, 0 failed.
  - `make_campaign_table.py`: 115 checks; `make_points_table.py`: 108 checks.
  - Every `tables/*.tex`, `data/numbers.json` and `data/check.log` is
    reproduced byte for byte.
  - The five figures render pixel-identically to the editors' versions.
- Claim index rebuilt and validated: `PASS: 65 claims; 5632 SHA-256
  references; 1918 distinct files`. These are the counts that S7.1 already
  printed, so no count changed.
- The 15 short checks pass from a fresh copy of the runner.
- `artifact/RELEASE.md` holds the SHA-256 of both PDFs, the build time and the
  validator's PASS line.
- Printed placeholders: only the declared ones, that is, four `[TODO: …]` in
  the declarations and four `[archive DOI]`.

## 2. Cross-group inconsistencies resolved

1. **`pricing050` primal: one implementation or two (sol-status 2; F1 dev. 8,
   F2 open 1, F4 dev. 2 and open 1).** F4 chose the "verified" branch: B5, C,
   `tab:points-all`, `tab:trust-full`, register rows R11 and R21, `RUNS.md` R11
   and the builder all say two separately written implementations. F1 and F2
   kept the conservative wording in the main text. Before choosing, I checked
   the records myself:
   - Neither checker imports first code. The earlier
     `development/dossiers/small-checks/pricing_check.py` imports only
     `xml.etree`, `fractions` and `mpmath`. `r2/pricing_check.py` imports its own
     `osil.py`.
   - The session record of the later check is
     `~/.claude/projects/-workspace-minlp-notes/64e03191-…/subagents/workflows/wf_59980c30-1d9/agent-a14f29dbb97bbc878.jsonl`.
     It shows that the session read the earlier dossier's text (`small.md`).
     Before writing its own `pricing_check.py` at 2026-10-04T07:29:27Z, it did
     not open the earlier `pricing_check.py`. It read the earlier log, and
     grepped the earlier code for "gap", only at 07:29:46Z, after writing.
   - It did read the second dual code `v_pricing050.py` first. This is what
     the "yes" in the `tab:trust-full` read-first column records for the dual.

   So the records support F4's branch, and it was also the smaller change. I
   changed three main-text sentences to match:
   - `02-semantics.tex` (§2.6): "Every primal claim has two implementations
     except that of \inst{etamac}, which comes from one implementation".
   - `06-points.tex` (§6.3): "The claim of \inst{etamac} rests on one
     implementation in mpmath interval arithmetic, and those of
     \inst{pricing050} and \inst{pindyck} on two."
   - `05-other.tex` (§5.2): "two codes reproduce the bound and two separately
     written codes check the point".

   Both files carry a source comment that records the decision. In the rebuilt
   index, `register-11` is *verified* and `register-21` is
   `verified (etamac: proved)`.
2. **Dated upstream-communication statements (F2 open 2, F3 open 4).** The four
   places used three different forms. All now say "As of 2026-10-05, we have
   not yet …":
   - `07-audit.tex` (§7.5): "we have not yet sent these refutations to the
     MINLPLib maintainer" (was "our report … is pending");
   - `08-solvers.tex` (§8.2): "we have not yet reported the defect to the SCIP
     developers" (was "had not yet");
   - `H-solvers.tex` (S6.6): this wording, unchanged;
   - `artifact/README.md`: "the authors have not yet reported the SCIP defect
     … or sent the refutations to the MINLPLib maintainer", unchanged.
3. **Float order in S7 (layout).** After the edits, S7.2 started one page
   earlier. The sideways Table S37 (`tab:trust-full`) was then deferred past
   the start of the register longtable (Table S38) and printed after it, on
   page 121.
   - Fix: `I-reproduction.tex` now inputs `tables/tab-trust-full` directly
     after `tab-sem-hashes`, still in S7.2, with a comment explaining why. No
     text changed.
   - Result: S37 prints on page 119 and the register on pages 120–121, the same
     order as in revision 4.

Checked and found consistent, so no change was made:

- **Sample-only GAMS/OSIL correspondence (sol-referee 1).** The qualification
  appears in the abstract, C3, the Figure 1 caption, the §8 opening, §8.3, S6.1
  and S6.3 (F1 open 3, F3 open 6).
- **Accuracy auditor (opus-writing 4).** The term is defined in
  `thm:eg-bounds` and used in Table 1, Table 7, Table S37, S5.4 (renamed "The
  accuracy auditor", label unchanged) and the register (F2 open 3, F3 open 1,
  F4 open 2).
- **Selection funnel (opus-writing 1).** §3.1 defines it, and §11 and S3.4
  ("the remaining 146 of the 155") use it (F3 open 2).
- **`fct` (opus-referee 6, opus-writing 14).** §8.2, S6.6, S3.4 and S4.1 all
  give the same reason: its page offers no OSIL file (F3 open 3).
- **`catmix` tier (sol-referee 3).** The wording is the same in Table 7, the
  S1.4 certificate box, the register row and caption, `RUNS.md` R06 and the
  README (F3 open 5, F4 open 2).
- **Read-first column of Table S37 (opus-referee 2).** The column exists
  (`TRUST_READ` in `make_tables.py`). So the §2.6 parenthetical "(\cref{tab:trust-full}
  names these families)" stays (F1 open 1).
- **Guarded KAN recipe (sol-referee 2).**
  - The command blocks in the README and `RUNS.md` are identical.
  - Syntax checks pass: `bash -n` on the block, and `compile()` on its embedded
    Python.
  - The archived guarded code lives under `development/`, which the archive
    contains. The register already hashes it, so the recipe needs no copy in
    `artifact/`.
  - S7.1 and S7.4 point to the README.
  - F4's recorded run of the staging and the three `r3` replays is
    `artifact/logs/kan-guard-recipe-test.log`. I did not repeat it.
- **Abstract length.** 250 words by the counting rule of `/tmp/abscount.sh`.
  The abstract fits on page 1, and Figure 1 and Table 1 are on pages 13 and 10,
  as in revision 4 (F1 open 6).
- **Lemma S6.3 restatement in §8.2 (opus-referee 1).** It agrees with the
  lemma's statement and with the residuals and spacings in its proof.
- **`emfl` register times.** The register gives "2–13 s (V2); 3–26 s (2nd)".
  This agrees with the saved run times of `emfl_bounds.py` (2.21, 4.76, 3.00
  and 12.79 s, in `research-20260929/publication/reproduction/README.md`).

## 3. Generators, from `/tmp` copies

Each generator was copied to `/tmp/final/gen/`. The only change in each copy is
its path line: `HERE = Path(__file__).resolve().parent` (or `P = …` in
`check_floats.py`) became the absolute path of the original folder. A diff that
ignores that line shows each copy otherwise identical.

```bash
cd /tmp/final/gen && taskset -c 0,1 python3 make_tables.py          # 851 checks, 0 failed
cd /tmp/final/gen && taskset -c 0,1 python3 make_campaign_table.py  # 115 ok
cd /tmp/final/gen && taskset -c 0,1 python3 make_points_table.py    # 108 ok
cd /tmp/final/gen/fig && taskset -c 0,1 python3 make_fig_<name>.py  # all five exit 0; "all figure checks passed"
md5sum -c /tmp/final/before-gen.md5                                 # tables, numbers.json, check.log: OK
```

The figure PDFs differ only in their embedded creation date. Rendered at
60 dpi, the new and old figures are identical.

## 4. Build

```bash
rm -rf build && taskset -c 0,1 make                                   # exit 0 (02:01:31–02:01:52)
grep -a 'undefined\|multiply defined' build/main.log build/supplement.log   # nothing
grep -a 'LaTeX Warning' build/*.log | grep -v 'TODO\|archive DOI'           # nothing
grep -a -c Overfull build/main.log build/supplement.log                     # 0, 0
grep -a -i 'warning\|error' build/*.blg                                     # "warning$ -- 0" only
pdftotext build/<doc>.pdf - | grep -c '??'                                  # 0, 0
cd /tmp/final && taskset -c 0,1 python3 gen/check_floats.py                 # 0 + 0 flagged, 31 of 31
```

- **Private builds first.** Two private builds in `/tmp/final/priv/` came
  first. The first found the S37 ordering of Section 2, item 3; the second
  confirmed the fix.
- **Final build.** The final `make` ran once, in the paper directory, with no
  other build running. Its pages, rendered at 40 dpi, are identical to those
  of the second private build (187 of 187 pages).
- **Underfull boxes.** The remaining ones are the same mild set as in
  revision 4: `01-introduction.tex` (1122), `H-solvers.tex` (the GAMS command
  line, 2913, and two SHA-256 prefixes, 1286–3746) and one bibliography entry
  in each document (1308).

## 5. Pages inspected by eye

- **Main paper.**
  - All 56 pages were viewed on contact sheets (25 dpi).
  - These pages were viewed at 80–110 dpi:
    - p. 1 (abstract and keywords on the first page);
    - p. 10 (Table 1, upright, no overlap);
    - p. 12 (Table 2, sideways, at 110 dpi: caption and all 31 rows);
    - p. 13 (Figure 1 and Table 3);
    - p. 14 (Table 4);
    - p. 31 (Table 5, and the new §6.3 sentence);
    - p. 34 (Table 6);
    - p. 42 (Table 7, and the §11 limitations);
    - p. 52 (Table 8).
- **Supplement.**
  - Every page with a table, figure or longtable continuation was viewed at
    50 dpi: pages 3, 5, 8, 13, 16, 18–20, 25, 41, 45, 47, 52, 53, 58, 64, 66,
    76, 78–82, 84–86, 89, 92–95, 98, 99, 102, 105–109, 111, 112 and 118–121.
  - Pages 116–122 were also viewed on a contact sheet.
  - Table S37 (p. 119, sideways, with the new "read first" column) was rotated
    and read in full at 100 dpi. The register (pp. 120–121) was read at 100 dpi.

No clipping, overlap, cropped float or out-of-order float was found.

## 6. Claim index

```bash
cp $P/artifact/build_claims.py $P/artifact/check_claims.py /tmp/final/claims/
cd /tmp && python3 /tmp/final/claims/check_claims.py --repo-root <repo>    # old index: FAIL, 318 stale hashes (expected)
cd /tmp && python3 /tmp/final/claims/build_claims.py --repo-root <repo> \
    --output <repo>/paper-open-minlplib/artifact/claims.json               # BUILT 65 claims; 1918 artifacts; 0 unresolved
cd /tmp && python3 /tmp/final/claims/check_claims.py --repo-root <repo>    # PASS: 65 claims; 5632 SHA-256 references; 1918 files
# after the final make (02:06:07) and after the short checks (02:08:40): PASS, same counts
```

- **S7.1 counts.** The counts equal those that F4 had already written in S7.1,
  so `I-reproduction.tex` needed no count edit.
- **Copies.** The `/tmp` copies are byte-identical to the artifact scripts.
- **Register entries:**
  - `register-11` (`pricing050`): *verified*.
  - `register-21` (points): `verified (etamac: proved)`, label *proved*.
  - `register-23`: `status_by_component` = `{emfl enclosures: weaker second}`,
    label *proved*.
  - `register-27`: "Directed rounding of generated certified displays",
    level `stored`.
  - `register-06` (`catmix`) and `register-12` (`etamac`): *weaker second*.
  - `register-17` (`eg`): *proved* because of `eg_disc2_s`.
  - `register-18` (`ann_cumene_tanh`): *proved*.
- **Reported values.** Of the 38 entries, 37 are *proved* and 1 (`etamac` p1,
  `value_evaluation` `numerical`) is *computed*.
- **Logs.** `artifact/logs/build_claims.log` and `check_claims.log` record
  these runs. `claims.json` hashes no file under `artifact/logs/`.

## 7. Short checks

```bash
cp $P/artifact/run_short_checks.py /tmp/final/short/
cd /tmp && taskset -c 0,1 python3 /tmp/final/short/run_short_checks.py \
    --repo-root /workspace/minlp-notes --logs /tmp/final/short/logs   # PASS, exit 0, 3 min 5 s
```

The runner worked in `/tmp/minlp-artifact-gtio41xd` with affinity [0, 1], and
`failed` is empty.

| check | wall s | last line or comparison |
|---|---:|---|
| `lnts` | 9.0 | `PASS: all four models, exact sign certificates, …`; all fields equal |
| `dtoc5` | 22.4 | `PASS`; equal except elapsed time and affinity |
| `kan_r3_h1_n4`, `_n5`, `_n9` | 33.0, 36.6, 68.7 | equal except `time` |
| `test_auditor` | 1.7 | `ALL AUDITOR TESTS PASSED` |
| `test_negative` | 131.2 | `ALL NEGATIVE TESTS PASSED` |
| `boundary_check` | 7.7 | `ALL OK` |
| `check_copies` | 0.1 | `ALL COPY CHECKS PASSED` |
| `dtoc5_displays` | 0.0 | `PASS: paper endpoints, interval width, and both rounded-up gap displays` |
| `dtoc5_boundaries` | 0.4 | `PASS: exact infeasibility, terminal override, and row-sign checks` |
| `kan_audit` | 8.4 | `ALL AUDIT CHECKS PASSED` |
| `independent_numeric` | 3.3 | `PASS` |
| `source_and_range` | 4.0 | `PASS` |
| `verify_artifacts` | 3.6 | `PASS` |

The outputs are in `development/build-final-logs/short-checks/`.
`artifact/logs/short-checks.json` was left unchanged: the README describes it
as the short checks of the recipe test (`logs/recipe-test.log`), and this pass
did not rerun the S7.1 recipe.

Not run in this pass:

- the full S7.1 recipe (pip and venv setup on a stand-in archive). Its commands
  did not change since revision 4.
- the guarded KAN replays, beyond the syntax checks of Section 2.
- `--eg-int`.

## 8. `artifact/RELEASE.md`

| field | value |
|---|---|
| build | 2026-10-05, 02:01:31–02:01:52 (−04:00), from an empty `build/` |
| `build/main.pdf` | `65069e02fba1d969aa38e2644fdd070c60415b44f7140641c00a98cca0582aba` (56 pages) |
| `build/supplement.pdf` | `4fee2118624dcdf5da435b5fcc1d5aef4cc417d93794357c27c6af52e26794c6` (131 pages) |
| validator | `PASS: 65 claims; 5632 SHA-256 references; 1918 distinct files; all paths, LaTeX labels, displayed values, status labels and register rows valid` |

- **Separation of checks.** `RELEASE.md` still separates source and evidence
  validation from PDF identification.
- **Rewritten section.** Its "Other checks" list now gives the counts of this
  pass. It also says that the S7.1 recipe was last run on the sources of the
  previous build.
- **No later changes.** No source file is newer than `build/main.pdf`, and
  nothing was rebuilt after the hashes were written.

## 9. Scans (pdftotext, line-end hyphens joined)

Outputs: `development/build-final-logs/scan-*.txt`. The scripts are the
revision-4 scan scripts, with paths updated.

**Placeholders.** No `??`, `TBD`, `FIXME` or other bracketed placeholder
prints. The ones that print:

- `[TODO: …]`, four, all in the declarations on main p. 43:
  - licence;
  - "authors to confirm, here, in Section 2.6 and in the limitations of
    Section 11, including which proofs and code the authors checked
    themselves";
  - competing interests;
  - funding.
- `[archive DOI]`, four: main pp. 4, 41 and 43, and supplement p. 116.

**Banned phrases (style guide).**

- Main paper: none. "significant" occurs only in "significant digits".
- Supplement:
  - "If moreover" occurs inside two lemma statements.
  - "no novelty" and "novelty statement" occur in S1 and S3.
  - "leveraging" and "Robust" occur only in cited titles.
  - "significant bits" occurs in S5.
- Terminology (`terminology.md`): no "proven", "independently verified",
  "same-model", "listed duals" in prose, "hand-written", "on paper" or "the
  auditor" in the main text.
- Kept as before:
  - "best listed dual" in table headers and in the Table 2 legend, and
    "duals" in two cells of Table S33;
  - "audited rerun" in S5.5, where "the auditor" is defined in S5.4.
- "Independent" occurs in the main paper only in "weaker than independent
  development" and "code from independent teams" (§2.6). Elsewhere it has its
  mathematical sense.

**Internal names.**

- Main paper:
  - no script or file name, `$R`/`$P`, `development/` or `research-…` path,
    "wave", "dossier", "round …", "workflow" or register/decision identifier;
  - "AI", "Anthropic Claude", "OpenAI GPT" and "agent session(s)" occur only
    in the §2.6 sense;
  - "Tier" occurs only on pp. 41–42 (§10, Table 7).
- Supplement outside S7: no internal name. The only file names are the public
  `noncvx_gurobi.csv` (S6.7) and MINLPLib's `.sol` file type.

**Stale strings (outline §8 item 11).** As in revision 4, the only hit is
352.238025369202, the weaker `lukvle10` bound (main p. 21; supplement pp. 8 and
119).

## 10. Page counts

Measured from the bookmark positions (A4, 11 pt, 25 mm margins) with the
revision-4 script, copied to `/tmp/final/pages.py`. Headings without bookmarks
were located with `pdftotext -bbox`. Floats count where they print, and 1.00 is
one full text area. Raw output: `development/build-final-logs/pages.txt`.

### Main paper (`build/main.pdf`, 56 pages)

| part | pages | target | revision 4 |
|---|---:|---:|---:|
| Title, abstract, keywords | 0.66 | – | 0.66 |
| 1 Introduction | 4.34 | 3.8 | 4.34 |
| 2 Semantics (with Table 1) | 5.82 | 5.6 | 5.78 |
| 3 Results (Table 2, Figure 1, Tables 3–4) | 3.74 | 3.1 | 3.69 |
| 4 Split certificates | 6.79 | 6.6 | 6.78 |
| 5 Other certificates | 7.19 | 6.6 | 7.24 |
| 6 Points (with Table 5) | 2.52 | 2.2 | 2.51 |
| 7 Audit (with Table 6) | 3.38 | 2.9 | 3.32 |
| 8 Solvers | 3.42 | 3.0 | 3.27 |
| 9 Interpretation and recommendations | 2.14 | 1.6 | 2.12 |
| 10 Reproducibility (with Table 7) | 1.38 | 1.2 | 1.29 |
| 11 Limitations and conclusion | 0.77 | 0.7 | 0.73 |
| **Sections 1–11** | **41.49** | **about 38** | **41.07** |
| Statements and declarations | 0.54 | – | 0.52 |
| References | 6.88 | – | 6.85 |
| Appendix A | 3.31 | ≤ 3.3 | 3.29 |
| Appendix B | 3.07 (3.14 counting the last page, 93% full, as full) | ≤ 3.0 | 2.99 |

The round-3 text changes add 0.42 pages to Sections 1–11. Most of this comes
from §8 (the GAMS/OSIL correspondence sentences), §10 (the tier rule) and §3
(the funnel description).

### Supplement (`build/supplement.pdf`, 131 pages)

| part | pages | revision 4 |
|---|---:|---:|
| Title, note, contents | 1.46 | 1.46 |
| S1 Certificates by family | 66.72 | 66.54 |
| S5 eg rounding-error analysis | 7.77 | 7.68 |
| S2 Exactly feasible points (now with Table S17, p. 76) | 7.82 | 6.89 |
| S3 Prior literature (Table S17 no longer in its span) | 6.27 | 7.38 |
| S4 Audit details | 12.77 | 12.73 |
| S6 Solver campaign, SCIP defect | 12.59 | 12.23 |
| S7 Reproduction guide and register (Table S37, p. 119, inside S7.2) | 6.76 | 6.66 |
| **Content S1–S7** | **120.71** | **120.11** |
| References | 8.76 (8.83 counting the last page, 93% full, as full) | 8.81 |

## 11. Open items for the lead author and the authors

1. **Author placeholders.** The four declaration `[TODO: …]` items and the four
   `[archive DOI]` remain, as instructed. §2.6 and §11 still say "No person
   outside the authors has checked the code or the proofs". The authors must
   state what they checked themselves (opus-referee's submission condition).
2. **Upstream communication.** The dated sentences in §7.5, §8.2, S6.6 and the
   README must be updated if the SCIP report or the message to the MINLPLib
   maintainer is sent before submission (opus-referee 9). After any such
   change: rebuild and revalidate the index if a hashed file changed, then
   rebuild the PDFs and rewrite `RELEASE.md`.
3. **Definition of "separately written".** The lead author still needs to
   record the decision (build-r4 §11 item 1; sol-status asks for it). The
   per-family reading facts are now printed in Table S37: 11 of the 15
   families whose status rests on a second implementation read first, 2 did
   not, and 2 were not checked.
4. **Optional cuts (opus-referee 8).**
   - F1 deleted the `lnts50` paragraph of §1. The fact remains in Table S33
     and in §9.2. The deletion can be reverted.
   - F3 did not make the two optional §9.1 moves, and F4 added nothing to S3.1
     or S6.3.
5. **Length.** Sections 1–11 take 41.49 pages against about 38, and the
   supplement body takes 120.71 against about 105. sol-referee accepted the
   length in round 3.
6. **Recipe and replays.**
   - The S7.1 recipe was not rerun on these sources. Its commands are
     unchanged, and the short checks pass.
   - The README calls `logs/short-checks.json` the checks of "the final recipe
     test". That run is the revision-4 recipe test.
   - The guarded `r5` KAN replays (12–20 min each) were not rerun under the new
     recipe (F4 open 7).
   - A test on another machine with the deposited archive remains.
7. **Temporary folders.** These can be deleted after review:
   - `/tmp/final` (backup tar, private builds, generator copies, short-check
     runner logs);
   - `/tmp/minlp-artifact-gtio41xd`;
   - the editors' `/tmp/suppgrp` (3.7 GB), `/tmp/suppgrp-orig`, `/tmp/g811`,
     `/tmp/r3-g2` and `/tmp/g-intro*`.

## 12. Last touch (2026-10-05, after the round-3 final verification)

This pass applied the remaining items R1–R3 and the five optional wording
points of `development/reviews/round3/final-verification.md` §7. Nothing was
committed, nothing in `research-20260929/` or `literature/` was edited, no
scientific script ran in place, and every command ran on cores 0 and 1. Backup
of the paper tree before this pass (without `build/`):
`/tmp/lasttouch/paper-before.tar`. Logs: `development/build-final-logs/last-touch/`.

### Changes, with the facts checked first

- **R1 (`artifact/build_claims.py`, `artifact/README.md`).** New constants
  `SAMPLED_GAMS` (the families that `tab:sem-gams` compares only at sample
  points; checked against `A-semantics.tex:61–72`) and `SAMPLED_QUALIFIER`.
  For campaign entries on these instances, `trust_qualifiers` now says that the
  conclusion assumes that the GAMS and OSIL forms define the same model
  (`app:solvers-points`, `H-solvers.tex:71`), and `status` adds "(under the
  assumption in trust_qualifiers)". In the rebuilt index exactly `reported-20`
  to `-25`, `-27` and `-28` changed (`etamac`, `pricing050`, `pindyck`,
  `chain50`, KAN); `camshape` and `powerflow0039p` (identical forms) did not.
  The `verification_note` and one README sentence say the same.
- **R2 (`artifact/RUNS.md` R11; `register-11` `expected_output`, which the
  builder copies from `RUNS.md`).** Checked in
  `$R/reviews/wave2-small-verification/logs/pricing050.log` and
  `v_pricing050.py:255–297`. The script prints `upper_bound`
  −1813.8290784519730577 (= L of `tab:closures`). It also prints the objective
  of its own point: the minimizers of the F_j at the 20-digit multipliers,
  rounded to 25 digits, not saved. That value is −1813.8290784519730578 to 20
  digits. It lies between U = −1813.8290784519730769 and the upper bound (exact
  `Fraction` comparison), and U comes from the two primal checkers, whose logs
  print it. The new text states this.
- **R3 (`01-introduction.tex:102`).** "on the stored models" → "on these
  instances".
- **Optional points.**
  - `08-solvers.tex:106`: "smaller in absolute value than one binary64
    spacing", as in the proof of Lemma S6.3.
  - `07-audit.tex:41`: "…consistent with this rule, 122 others differ only in
    the sign of zero (…)"; matches `E-audit.tex:164` and
    `development/dossiers/audit.md:94–96`.
  - `03-results.tex:51`: "relative gaps above $10^{-4}$ or infinite (a missing
    bound or point counts as infinite)". Checked against S3.4, the funnel table,
    `relgap` in `$R/open-instances-scout/parse_pages.py` (missing value → ∞) and
    the census `gap` field (`inf` for `catmix100`, `ann_cumene_tanh` and the
    pages without a primal value).
  - `A-semantics.tex:49`: "the outward data readings".
  - `02-semantics.tex:196–197`: the reader list now reads "one OSIL reader for
    …", and the next sentence ends "; for \inst{pricing050}, a third code with
    its own reader also reproduces the displayed bound". Checked: the first code
    and `v_pricing050.py` both import `osilx`, and `r2/pricing_check.py` uses
    `r2/osil.py` ("shares no code with osilx.py").

**Layout.** The first in-place build (02:33) gave 57 main pages. The two
lines added to §2.6 pushed §3.1 off page 11, Table 5 moved behind the §7 heading
(p. 32), and the last page overflowed. Private builds in `/tmp/lasttouch/priv/`
showed that dropping the redundant "used by both implementations" (the sentence
already says "shared by both implementations") and moving the `pricing050`
clause after the readers sentence keep the paragraph's line count. The final
layout equals the previous one: every section and float starts on the same page
(Table 5 on p. 31, Table 6 on p. 34). Rendered at 30 dpi and compared with
`/tmp/final/priv/paper2/build/` (whose pages equal those of the previous final
build, Section 4), only main pages 4, 11, 13, 14, 32–35, 37 and 51 differ (the
edited text), and all 131 supplement pages are identical.

### Checks (targeted, local)

```bash
# generators from /tmp/lasttouch/gen (only the HERE/P line changed)
taskset -c 0,1 python3 make_tables.py          # 851 checks, 0 failed
taskset -c 0,1 python3 make_campaign_table.py  # 115 ok
taskset -c 0,1 python3 make_points_table.py    # 108 ok
taskset -c 0,1 python3 fig/make_fig_*.py       # all exit 0; "all figure checks passed"
md5sum -c /tmp/lasttouch/before-gen.md5        # 14 tables, numbers.json, check.log: OK
# figures: pixel-identical at 60 dpi (only the embedded date differs)
# claim index from /tmp/lasttouch/claims (byte-identical copies)
check_claims.py   # before rebuild: FAIL, 66 stale hashes (RUNS.md x65, 08-solvers.tex), expected
build_claims.py   # BUILT 65 claims; 1918 distinct artifacts; 0 unresolved
check_claims.py   # PASS: 65 claims; 5632 SHA-256 references; 1918 distinct files (also after the final make)
rm -rf build && taskset -c 0,1 make            # exit 0, 02:39:25-02:39:46
# logs: 0 errors, 0 undefined/multiply defined, no warnings besides TODO/archive DOI,
#       0 overfull (main, supplement), BibTeX 0 warnings; pdftotext: 0 "??" in each PDF
taskset -c 0,1 python3 gen/check_floats.py     # 0 + 0 flagged, 31 of 31
scan.py, scan2-4.py (copies of /tmp/final/scan)  # output identical to the previous pass
```

- The S7.1 counts did not change, so `I-reproduction.tex` needs no edit.
- The printed placeholders are only the declared ones: four `[TODO: …]` on main
  p. 43, and four `[archive DOI]` (main pp. 4, 41 and 43; supplement p. 116).
- The short checks were not rerun. None of their inputs changed (`RELEASE.md`
  says so).
- `artifact/RELEASE.md` now has the new hashes, the new build time and the
  PASS line. `logs/build_claims.log` and `logs/check_claims.log` record the
  runs of this pass.

### Final files

| file | pages | SHA-256 |
|---|---:|---|
| `build/main.pdf` | 56 | `4b183b233cc4d2eded6c7381a7057b9ecf26ca83952c38eb83d2daff43166784` |
| `build/supplement.pdf` | 131 | `f8547c05fb3135a37e73bb0ea6b9eb5650d33676b93593e4b9dd5831ef8595ab` |

Section positions are unchanged except for §7–§8 (§7 3.41 pages, was 3.38; §8
starts at p. 35.48, was 35.44). Sections 1–11 still take 41.49 pages.
`/tmp/lasttouch` can be deleted after review.
