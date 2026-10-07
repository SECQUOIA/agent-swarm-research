# Final build, claim register and scans, revision 3 (2026-10-04)

This pass ran after the seven editing groups (G1–G7) of the round-1 revision.
It regenerated the tables and figures, rebuilt both documents from an empty
`build/`, rebuilt and validated the claim register, ran the 15 short artifact
checks, scanned both PDFs and measured the page counts. Nothing was committed.
Nothing in `research-20260929/` or `literature/` was edited. No certified
number changed. Every command ran on two cores (`taskset -c 0,1`). A backup of
the paper directory before this pass is in `/tmp/r3/paper-before-build-r3.tar`.

All checks below are targeted local checks run in this pass. No CI result was
consulted.

## 1. Result in brief

- `make` from an empty `build/` exits 0: 0 LaTeX errors, 0 undefined
  references or citations (both directions), 0 multiply defined labels
  (399 labels, none defined twice within or across the two documents),
  0 BibTeX warnings, 0 overfull boxes, no other LaTeX warnings, no `??` and
  no stray `supplement.pdf`/`main.pdf` string in either PDF.
- `build/main.pdf` has 60 pages, `build/supplement.pdf` 135.
- The float check passes (0 flagged pages, 31 of 31 closure names), and every
  table and figure page was inspected by eye (Section 2.3). Table 2 is
  complete (caption start and the three `eg` rows print); Table 1, Figure 1
  and the sideways Tables S1 and S34 print in full.
- Generators: `make_tables.py` 798 checks, 0 failed; `make_campaign_table.py`
  115 ok; `make_points_table.py` 108 ok; all six figure scripts exit 0 and
  render pixel-identical to their previous versions.
- Claim register rebuilt from the final sources and validated:
  `PASS: 65 claims; 5334 SHA-256 references; 1894 distinct files`. The counts
  quoted in S7.1 are unchanged.
- The 15 short artifact checks pass from a fresh `/tmp` copy on cores 0 and 1.
- Printed placeholders: four declaration `\TODO`s (licence, AI-use wording,
  competing interests, funding) and four `[archive DOI]`s. The Section 2.6
  `\TODO` was folded into the declaration placeholder (Section 3, item 1).
- Length targets are not met: Sections 1–11 run to 42.85 pages (target about
  38; revision 2: 45.81), and the supplement body S1–S8 to 124.91 pages
  (target about 100; revision 2: 129.01). Section 5 gives the figures.

## 2. Commands and checks

`P` is `paper-open-minlplib/`.

### 2.1 Bibliography

All 151 cited keys exist in `references.bib`; there are no duplicate keys. The
six new keys the editors named (`araya2025-…`, `borst2024-…`, `szeider2026-…`,
`hoen2025-…`, `belotti2025-…`, `merx2026-…`) were already present. I compared
each with its KB `paper.md` (authors, title, venue, volume, pages, DOI); they
agree. No entry was added.

### 2.2 Generators, from `/tmp` copies

Each generator was copied to `/tmp/r3/gen/`. The only change in the copy is
the line `HERE = Path(__file__).resolve().parent`, replaced by the absolute
path of the original folder, so that the copies read and write the paper tree
(`diff` shows only that line). Likewise for `development/check_floats.py`
(its `P = …` line).

```bash
cd /tmp/r3/gen && taskset -c 0,1 python3 make_tables.py          # 798 checks, 0 failed
cd /tmp/r3/gen && taskset -c 0,1 python3 make_campaign_table.py  # 115 ok
cd /tmp/r3/gen && taskset -c 0,1 python3 make_points_table.py    # 108 ok
cd /tmp/r3/gen && taskset -c 0,1 python3 make_fig_<name>.py      # all six exit 0
```

- The first run reproduced every `tables/*.tex`, `data/numbers.json` and
  `data/check.log` byte for byte.
- After the fixes of Section 3, only these changed:
  - `tables/tab-claims-campaign.tex`: column width;
  - `data/check.log` and `numbers.json`: the SHA-256 of `development/outline.md`,
    which `make_tables.py` reads for display provenance. No value or
    provenance list changed (checked by a recursive diff of `numbers.json`).
- Figures: rendered at 60 dpi, all six PDFs are pixel-identical to their
  previous versions. The headline figure's own checks pass.

Logs: `development/build-r3-logs/make_*.out`.

### 2.3 Build and layout

```bash
rm -rf build && taskset -c 0,1 make                                  # exit 0
grep -a 'undefined\|multiply defined' build/main.log build/supplement.log   # nothing
grep -a 'LaTeX Warning' build/*.log | grep -v 'TODO\|archive DOI'           # nothing
grep -a -c Overfull build/main.log build/supplement.log                     # 0, 0
grep -a -i 'warning\|error' build/*.blg                                     # "warning$ -- 0" only
pdftotext build/main.pdf - | grep -c '??'                                   # 0
pdftotext build/supplement.pdf - | grep -c '??'                             # 0
cd /tmp/r3/gen && taskset -c 0,1 python3 check_floats.py                    # 0 + 0 flagged, 31 of 31
```

The final `make` was run once, from an empty `build/`, after the last edit, and
no other build was running.

Pages inspected by eye:

- **Main:** pages 11 (Table 1), 12 (Figure 1), 13 (Table 2), 14 (Tables 3
  and 4), 32 (Table 5), 35 (Table 6), 42 (Table 7) and 53 (Table 8), at
  50–110 dpi; the two sideways tables were rotated and read in full. All 60
  pages were also checked on contact sheets at 36 dpi.
- **Supplement:** all 51 pages with a table, figure or longtable (S1–S39,
  Figures S1–S4, the longtables of S3, S5, S7 and S8) at 45 dpi. The sideways
  Tables S1 (page 3) and S34 (page 112) were checked at 100 dpi, and the
  tightest cells of S34 at 200 dpi.

No clipping, overlap or cropped float was found. The tightest spot is in
Table S34, where "above v* = −0.2185" in the position column is followed by
the violation column with about one space between them. The cells do not
overlap.

Remaining underfull boxes are mild and look normal on the page:

- `01-introduction.tex:84`, badness 1122;
- `H-solvers.tex:13` (the GAMS command line), badness 2913;
- `H-solvers.tex:97` and `:219` (SHA-256 prefixes in two certificate boxes),
  badness 1286 to 3746;
- the Göß bibliography entry in each document, badness 1308.

### 2.4 Claim register

```bash
cp $P/artifact/build_claims.py $P/artifact/check_claims.py /tmp/r3/claims/
cd /tmp && python3 /tmp/r3/claims/check_claims.py --repo-root <repo>    # before: FAIL, 211 stale hashes
cd /tmp && python3 /tmp/r3/claims/build_claims.py --repo-root <repo> \
    --output <repo>/paper-open-minlplib/artifact/claims.json            # BUILT 65 claims; 1894 artifacts; 0 unresolved
cd /tmp && python3 /tmp/r3/claims/check_claims.py --repo-root <repo>    # PASS: 65 claims; 5334 SHA-256 references; 1894 files
```

- The rebuilt index differs from the previous one only in 211 `sha256` fields.
  They belong to six files: `data/check.log`, `data/make_tables.py`,
  `data/numbers.json`, `development/outline.md`, `sections/I-reproduction.tex`
  and `tables/tab-claims-campaign.tex`.
- No claim, label, status or recipe changed. The counts in S7.1 (65; 5,334;
  1,894) and in `artifact/README.md` (27 register rows, 38 reported values)
  still hold.
- The validation was repeated after the last source edit and the final build:
  PASS, same counts.
- `artifact/logs/build_claims.log` and `check_claims.log` record this run.

### 2.5 Short artifact checks

```bash
cp $P/artifact/run_short_checks.py /tmp/r3/minlp-short-checks.py
cd /tmp && taskset -c 0,1 python3 /tmp/r3/minlp-short-checks.py \
    --repo-root <repo> --logs /tmp/r3/short-logs        # PASS targeted relocated checks
```

The runner copied the inputs to `/tmp/minlp-artifact-y2y2ztuw`. Under
`taskset` its affinity was `[0, 1]`. All 15 checks exited 0:

| check | wall s | last line or comparison |
|---|---:|---|
| `lnts` | 11.0 | `PASS: all four models, exact sign certificates, …`; certificate fields all equal |
| `dtoc5` | 22.7 | `PASS`; result fields equal except elapsed time and affinity |
| `kan_r3_h1_n4`, `_n5`, `_n9` | 35.1, 33.4, 66.7 | result fields equal except `time`; imported modules from the `/tmp` tree |
| `test_auditor` | 1.6 | `ALL AUDITOR TESTS PASSED` |
| `test_negative` | 130.6 | `ALL NEGATIVE TESTS PASSED` |
| `boundary_check` | 7.2 | `ALL OK` |
| `check_copies` | 0.1 | `ALL COPY CHECKS PASSED` |
| `dtoc5_displays` | 0.0 | `PASS: paper endpoints, interval width, and both rounded-up gap displays` |
| `dtoc5_boundaries` | 0.4 | `PASS: exact infeasibility, terminal override, and row-sign checks` |
| `kan_audit` | 8.4 | `ALL AUDIT CHECKS PASSED` |
| `independent_numeric` | 3.0 | `PASS` |
| `source_and_range` | 4.1 | `PASS` |
| `verify_artifacts` | 3.6 | `PASS` |

The optional `--eg-int` regeneration (about 5 min) was not run. Logs and
`short-checks.json` are copied to `development/build-r3-logs/short-checks/`.
`artifact/logs/short-checks.json` was left unchanged, because it records the
packaging run that includes `--eg-int`.

## 3. Fixes in this pass

1. **Printed TODO in Section 2.6** (`02-semantics.tex`, `11-conclusion.tex`).
   The paragraph on AI use printed its own `\TODO` (authors to confirm the
   wording and state which proofs or codes they read). The scan rule allows
   only declaration placeholders. The request now prints in the declaration
   placeholder: "[TODO: authors to confirm wording, here and in the first
   paragraph of the subsection on the verification protocol, and to state
   there which proofs or codes the authors read themselves]". A source
   comment in Section 2.6 points to it. `development/open-items.md` item 5
   records the move.
2. **Overfull boxes:**
   - Table S33 (`make_tables.py`, `tab_claims_campaign`): value column
     2.6 cm → 2.7 cm. "−1813.829077405652" no longer overflows by 1.6 pt;
     the table still fits the text width.
   - Table S38, `tab:repro-register` (`I-reproduction.tex`): first column
     2.1 → 2.2 cm and checker column 6.2 → 6.1 cm. "Propositions S4.6" and
     "powerflow0039p," no longer overflow by 2.5 and 0.9 pt. Narrowing the
     expected-output column instead produced a new 2.6 pt overflow at the
     `waterno2_06` fraction, so that column keeps 3.1 cm.
3. **`waterno2` replay tiers** (`B8-waterno2.tex`, certificate box). The box
   said "Tier 3 for the period statements of 09–24 (7.4 h)". Section 10
   (Table 7), the register and the artifact README put `waterno2_09` and
   `waterno2_12` in Tier 2 (35 and 49 min), as the editors' tier rule
   requires (G4 open item 6). The box now gives Tier 2 for 09 and 12 and
   Tier 3 for 18 and 24 (2.5 and 3.5 h; 7.4 h in all). The times are the
   register's 35, 49, 150 and 212 min.
4. **Half-unit note scoped to flagged pairs** (`E-audit.tex`, S4.1;
   `development/terminology.md`). The sentence read "no margin lies between
   0.44 and 1.115 units". The `rocket100` margin (1.06 units) lies in that
   range but outside the screen (G3 open item 3). Both now say "no margin of a
   flagged pair", as Section 7.1 already does.
5. **Pointer for the trust label T-mp** (`B1-lnts-lukvle10.tex:252`). The
   pointer now goes to S7.1 (`app:repro-setup`), where the T-labels are
   defined, instead of Section 2.5 (G1 open item 7).
6. **Review-round paths outside S7** (`B7-eg.tex`, `B9-ann-kan.tex`). Two
   supplement passages outside the reproduction guide printed
   `development/reviews/round1/…`, a review-round name that the style guide
   keeps to the reproducibility appendix.
   - S1.7.4 now points to the `eg` row of Table S38, which gives the folder
     and logs. It still says that a separate exponential test, stored in the
     same folder, checks enclosures and reciprocity at 452 arguments.
   - The KAN certificate box now points to S7.4 for the replay logs, keeping
     the SHA-256 prefix of the guarded source (`e5783a24`; checked).
7. **Powerflow certificate pointer** (`05-other.tex:175`). It now cites the
   certificate box (S1.6.6, `app:powerflow-verification`) instead of S1.6, as
   the other certificate sentences of Section 5 do (G6 open item 2).
8. **Development documents** (not printed):
   - `outline.md`: §8 item 11 and the Prop. 8.2 row of the results table
     still prescribed the margins 3.162·10⁻³ and 1.552·10⁻⁴. They now record
     3.11·10⁻³ and 1.54·10⁻⁴, the margins to any value within one unit of the
     last displayed digit (G4-03), and mark the old pair as superseded (G4
     open item 7).
   - `style-guide.md`: "verified by an independent implementation" became
     "verified by a separately written implementation (defined in Section
     2.6; never "independent")".

## 4. Scan results (pdftotext, line-end hyphens joined)

### Placeholders and `??`

- `??`: none in either PDF.
- `[TODO: …]`: four, all in the main paper's "Statements and declarations":
  licence of the archived code and data; AI-use wording (with the Section
  2.6 request); competing interests; funding.
- `[archive DOI]`: four, at `01-introduction.tex:104`,
  `10-reproducibility.tex:28`, `11-conclusion.tex:72` and
  `I-reproduction.tex:20`.

### Banned phrases (style guide)

- **Main paper:** none. "significant" occurs only in "significant digits".
  There is no "Moreover", "Furthermore" or "Additionally", no rhetorical
  question, and no "lesson". Section 9 is titled and introduced as an
  interpretation that "we did not test by experiment". Section 1.2 speaks of
  "three observations" and leaves the explanation to Section 9.
- **Supplement:**
  - "If moreover" occurs inside two lemma statements.
  - "we claim no novelty" and "novelty statement" occur in S1 and S3.
  - "leveraging" and "Robust" occur in two cited titles.
  - "independent" occurs only in the mathematical sense ("independent
    controls", "linearly independent", "range independently").
- **"This section …" openings:** ten supplement sections still open this way
  (S1, S1.3, S1.4, S1.5, S1.6, S2, S3, S4, S6, S7). They are not changed
  (Section 6, item 6).

### Internal names

- **Main paper:**
  - No script or file name, no register or decision identifier, and no
    "wave", "dossier", "critique", "route" or "round1".
  - "Agent session(s)", "AI", "Anthropic Claude" and "OpenAI GPT" occur in
    the Section 2.6 disclosure, the declarations, and sentences that use the
    Section 2.6 term "separate agent session" (Sections 3.1, 7.2 and 11.2).
    Decision 1 asks for this.
  - "Verifier's code" occurs only in the Section 2.6 definition.
- **Supplement:**
  - File paths and folder names (including `round1`, `wave2`, `wave3`,
    `dossiers`) occur only in S7, except `noncvx_gurobi.csv`, the public file
    name of the CAMINO data (S6.7).
  - "Agent session" occurs in the sense of Section 2.6.
  - "The authors' code" and "the verifier's code" remain the supplement's
    defined pair.

### Claims and displays of outline section 8

Scanned for all strings of §8 item 11 and for the banned claims of items 1–10:

- The superseded or unsafe strings occur only in the S8 table
  `tab:displays-unsafe`, with one allowed exception: 352.238025369202, which
  Table 1, the `lukvle10` text and S1.1 give as the weaker bound that the
  second code certifies.
- "Zero duality gap" occurs only negated (dtoc5) and in cited work or titles.
- "Formally verified" occurs only negated.
- "Treewidth" occurs only in cited methods, in the explicit non-claim of
  Section 11 and in the S3 width heuristic.
- "Solve rate" occurs only negated.
- "The trained network" refers to the trained network itself, whose
  coefficients the KAN files round. It is not used for R or R_P.

## 5. Page counts

Measured from the bookmark positions in the final PDFs (A4, 11 pt, 25 mm
margins) with `/tmp/r3/pages.py`, a copy of the revision-2 script. The
declarations and References headings were located with `pdftotext -bbox`.
Floats count where they print. A count of 1.00 is one full text area. The
targets are those in the editors' reports (G1–G7).

### Main paper (`build/main.pdf`, 60 pages)

| part | pages | target | difference | revision 2 |
|---|---:|---:|---:|---:|
| Title, abstract, keywords | 0.64 | – | | 0.64 |
| 1 Introduction | 4.59 | 4.0 | +0.59 | 5.00 |
| 2 Semantics (with Table 1, and Figure 1, which prints before the §3 heading) | 6.58 | 5.0 | +1.58 | 5.79 |
| 3 Results (with Tables 2–4) | 3.19 | 3.25 | −0.06 | 3.92 |
| 4 Split certificates | 7.18 | 6.75 | +0.43 | 7.93 |
| 5 Other certificates | 7.09 | | | 7.98 |
| 6 Points | 2.49 | | | 2.45 |
| 7 Audit | 3.59 | | | 3.42 |
| 5–7 together | 13.17 | 11.4 | +1.77 | 13.85 |
| 8 Solvers | 3.51 | | | 3.42 |
| 9 Interpretation | 1.40 | | | 2.52 |
| 10 Reproducibility (with Table 7) | 1.41 | | | 1.42 |
| 11 Conclusion | 1.83 | | | 1.95 |
| 8–11 together | 8.15 | 7.5 | +0.65 | 9.31 |
| **Main text, Sections 1–11** | **42.85** | **about 38** | **+4.85** | **45.81** |
| Statements and declarations | 0.51 | – | | 0.34 |
| References | 7.31 | – | | 7.07 |
| Appendix A Model semantics | 3.42 | 3.0 | +0.42 | 3.14 |
| Appendix B Proofs for the split certificates | 4.35 | – | | 4.33 |

Figure 1 takes about half a page. Counted with Section 3, Section 2 would be
about 6.0 pages and Section 3 about 3.7. The last page (60) is 8% full.

### Supplement (`build/supplement.pdf`, 135 pages)

| part | pages | target | difference | revision 2 |
|---|---:|---:|---:|---:|
| Title, note, contents | 1.48 | – | | 1.48 |
| S1.1 lnts, lukvle10 | 6.61 | | | 7.49 |
| S1.2 dtoc5, optcdeg2 | 6.75 | | | 8.18 |
| S1.3 camshape | 5.47 | | | 5.79 |
| S1.4 chain, catmix | 10.20 | | | 10.44 |
| S1.5 six small instances | 10.75 | | | 10.20 |
| S1.1–S1.5 | 39.78 | 32 | +7.78 | 42.10 |
| S1 opening (before S1.1) | 0.33 | – | | 0.28 |
| S1.6 powerflow | 6.47 | | | 6.78 |
| S1.7 eg | 7.41 | | | 7.68 |
| S1.8 waterno2 | 6.41 | | | 6.79 |
| S1.9 ann, KAN | 8.35 | | | 7.89 |
| S5 eg rounding-error analysis | 7.82 | | | 8.18 |
| S1.6–S1.9 and S5 | 36.46 | 29 | +7.5 | 37.32 |
| S2 Exactly feasible points | 7.10 | 6 | +1.1 | 8.81 |
| S3 Prior literature | 7.05 | 5.5 | +1.55 | 6.60 |
| S4 Audit details | 12.81 | 10.5 | +2.31 | 13.04 |
| S6 Solver campaign, SCIP defect | 12.57 | 10 | +2.57 | 12.51 |
| S7 Reproduction guide, claim register | 7.02 | 5 | +2.02 | 6.65 |
| S8 Display record | 1.80 | 2 | −0.2 | 1.70 |
| **Content S1–S8** | **124.91** | **about 100** | **+24.9** | **129.01** |
| Before the references | 126.39 | | | 130.49 |
| References | 8.02 | – | | 7.21 |

## 6. Editors' open items after this pass

Done in this pass or found already done:

- **Bibliography (G1-6, G3-7):** all keys present; no entry needed.
- **Single final build (G1-5, G6-6):** done, from an empty `build/`, with no
  concurrent build.
- **79 of the 109 (G1-3, G4-5):** generated and checked.
  - `data/check.log` line 563 checks BARON 23 + Gurobi 30 + SCIP 26 = 79,
    which together with 6 disclaimed, 6 tightened and 18 KAN comparisons
    make up the 109.
  - The §1 sentence and §8.3 agree with it.
- **Tiers (G4-6, G5-3, G6-3):**
  - The register already had catmix 2, lukvle10 1, ex6_2_5/ex6_2_7 1 and eg
    per instance (1, 2, 3).
  - Table 1 already shows catmix at level rerun.
  - The `waterno2` box is now aligned (Section 3, item 3).
- **S6.1 margins and MINOTAUR wording (G4-4):** already 3.11·10⁻³ and
  1.54·10⁻⁴ in Section 8 and S6.5. "Invalid as recorded (cause unknown)"
  appears in Section 8 and S3.
- **`tab:structure` (G4-5):** no longer generated or input.
- **B9 KAN replay (G3-5) and Krawczyk overlap sentence (G5-3):** already
  corrected.
- **Claim register covers the `kan-guard` and `eg-dyadic` folders (G6-5):**
  yes, 43 files.
- **Certificate labels (G2-2, G3-4):** all resolve (0 undefined references).
- **`labels.md` AI statement (G4-7):** already updated.
- **`outline.md` §8 item 11 (G4-7):** updated here.

Open, for the lead author or the authors:

1. **Length.** The main text is 4.85 pages over the target, and the
   supplement body 24.9 pages over. The editors' options are in their reports:
   - G1: a half-page Table 1; moving the §1.4 citation list to S3.
   - G3: folding the §7.4 class (i-r)/emfl/rocket paragraphs; moving the
     Proposition 5.7 proof; dropping Table 5.
   - G4: moving Propositions 8.2–8.3 and Lemma 8.4 to S6.
   - G5 and G6: moving lemmas, remarks, `fig:eg-enclosures`, `tab:pf-models`
     or `tab:eg-matrix`.
   - G7: moving `tab:campaign-runs`, `tab:audit-inputs` or
     `tab:audit-history`.
2. **Author confirmations:**
   - the AI-use wording in Section 2.6 and in the declarations, the sentence
     "No person outside the authors has checked the code or the proofs", and
     which proofs or codes the authors read (now one printed declaration
     placeholder);
   - the G5 wording "read twice, in separate agent sessions" (chain, catmix)
     and "a later separate agent session" (etamac);
   - the time recorded as "Tier 1; minutes on one core" for the QPLIB-copy
     check;
   - the licence, competing interests, funding and archive DOI placeholders.
3. **Superseded displays removed from S1 by G5 (G5-2):**
   - the earlier `lnts` dual (gaps ≤ 6.2·10⁻¹³);
   - two earlier `dtoc5` bounds;
   - the `optcdeg2` progression table (293.2500703, 293.8699938, …);
   - an earlier mpmath-interval `camshape` code.

   None of these was placed in S8 or the artifact README. They are valid
   weaker results, not unsafe displays, so S8's table does not require them.
   The `optcdeg2` values remain in `development/dossiers/dtoc5-optcdeg2.md`.
   Whether to restore a short note is a lead-author choice.
4. **Table 5 caption (G3-2):** the sentence "For lnts, U comes from the
   attaining point; the Krawczyk points are a second, strictly suboptimal
   witness" repeats §6.2. It is left unchanged in `make_tables.py`, which
   writes `tab-points.tex`; dropping it saves about two lines.
5. **SCIP residual check (G4-7):** the 2.93·10⁻¹⁵ check is still recorded
   only in the `08-solvers.tex` source comment and in a `/tmp` log. It is not
   in `data/check.log`.
6. **"This section …" openings** in ten supplement sections (Section 4).
   They are left unchanged, as in revision 2. The rewrite "We prove Theorem
   5.3, …" would apply if the rule is to cover the supplement.
7. **`figures/fig-camshape-profiles.pdf`** is generated but not included
   anywhere.
8. **Not done:** a replay on a second machine (R-03) and filing the SCIP
   issue (authors' action). The dated "to our knowledge (searched
   2026-10-02)" sentence stays until the issue is filed.

## 7. Files changed in this pass

- Sources: `sections/02-semantics.tex`, `05-other.tex`, `11-conclusion.tex`,
  `B1-lnts-lukvle10.tex`, `B7-eg.tex`, `B8-waterno2.tex`, `B9-ann-kan.tex`,
  `E-audit.tex`, `I-reproduction.tex`.
- Generator and generated files: `data/make_tables.py` (one column width),
  `tables/tab-claims-campaign.tex`, `data/numbers.json` and `data/check.log`
  (only the SHA-256 of `outline.md`); `figures/*.pdf` regenerated with
  pixel-identical rendering.
- Artifact: `artifact/claims.json` (211 hashes), `artifact/logs/build_claims.log`,
  `artifact/logs/check_claims.log`.
- Development: `outline.md`, `style-guide.md`, `terminology.md`,
  `open-items.md` (item 5), this file, and `build-r3-logs/` (generator outputs
  and the short-check logs).
- `build/` rebuilt from empty.
