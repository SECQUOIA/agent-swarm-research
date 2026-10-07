# Final rebuild and scan, revision 2 (2026-10-04)

This pass regenerated the tables and figures, rebuilt both documents from an
empty `build/`, fixed what the build and the text scans found, and measured
the page counts. Nothing was committed. Nothing in `research-20260929/` or
`literature/` was edited. No certified number changed. All commands ran on
two cores (`taskset -c 0,1`). A backup of the paper directory before this
pass is in `/tmp/r2/paper-before-build-r2.tar`.

## 1. Result in brief

- `make` from an empty `build/` exits 0, with 0 LaTeX errors, 0 undefined
  references in either direction, 0 undefined citations, 0 multiply defined
  labels, 0 BibTeX warnings, 0 overfull boxes, 0 other LaTeX warnings, and
  no `??` in either PDF.
- `build/main.pdf` has 62 pages and `build/supplement.pdf` 138.
- The main text (Sections 1 to 11) runs to 45.8 pages, against a target of
  about 46 (45.5 by section). The supplement runs to 130.5 pages before its
  references, against a target of about 95.
- Printed placeholders: only the three declaration `\TODO`s (licence,
  competing interests, funding) and five `\archiveDOI`s remain.
- Six small fixes (Section 3): one printed TODO removed, Figure 1 made to
  fit its page, "verifier" as a person removed from the main text (outside
  the Section 2.6 definition) and from three supplement sentences, and two
  visibly stretched passages fixed.
- Remaining problems are in Section 6: supplement length, the
  "authors' code"/"verifier's code" terminology, "This section …" openings
  in the supplement, and the stale claim index.

## 2. Commands and checks

All in `paper-open-minlplib/`, except the generators (run with `/tmp` as
working directory, as `data/README.md` prescribes; they write only into
`tables/`, `figures/` and `data/`).

```bash
cd /tmp && taskset -c 0,1 python3 $P/data/make_tables.py           # 673 checks, 0 failed
cd /tmp && taskset -c 0,1 python3 $P/data/make_campaign_table.py   # 115 ok
cd /tmp && taskset -c 0,1 python3 $P/data/make_points_table.py     # 88 ok
cd /tmp && taskset -c 0,1 python3 $P/figures/make_fig_<name>.py    # all six, exit 0
rm -rf build && taskset -c 0,1 make                                # exit 0
grep -a 'undefined\|multiply defined' build/main.log build/supplement.log    # nothing
grep -a 'LaTeX Warning: TODO\|archive DOI' build/main.log build/supplement.log   # 8 lines
grep -a 'LaTeX Warning' build/*.log | grep -v 'TODO\|archive DOI'    # nothing
pdftotext build/main.pdf - | grep -c '??'           # 0
pdftotext build/supplement.pdf - | grep -c '??'     # 0
grep -a -c Overfull build/main.log build/supplement.log   # 0, 0
grep -a Warning build/main.blg build/supplement.blg       # nothing
```

Other targeted checks:

- **Generated content.** Every `tables/*.tex`, `data/numbers.json` and
  `data/check.log` is byte-identical to its state before this pass. The six
  figure PDFs differ in bytes only; rendered at 60 dpi, each is
  pixel-identical to its previous version.
- **Labels.** A script over all section and table files found 411 labels
  and no label defined twice, within one document or across the two.
- **Cross-document references.** No "supplement.pdf" or "main.pdf" string
  prints in either PDF.
- **Text scans** (pdftotext, line-end hyphens joined): Section 4.

## 3. Fixes in this pass

1. **Printed TODO in Appendix B** (`sections/G-proofs-split.tex`, first
   paragraph). The note asking for a separate check of the extended-value
   proofs still printed, although `development/open-items.md` item 1 records
   it as moved there (style-check-r1 H3). Removed from the source; the item
   stays in `open-items.md`.
2. **Figure 1 too large for its page** (`sections/03-results.tex`). LaTeX
   reported "Float too large for page by 6.2pt". The image height is now
   `0.72\textheight` instead of `0.74\textheight`. The float page was
   checked visually.
3. **"Verifier" as a person in the main text** (`sections/05-other.tex`,
   style-check-r1 B7). Three places now use the wording of Section 2.6 and
   Table 1:
   - certificate box of `thm:etamac-bound`/`thm:pindyck-bound`:
     "displayed bound from one code, the weaker −15.294675643368096 from a
     separately written one" (etamac) and "displayed bound from one code's
     enclosures, a slightly weaker one from those of a separately written
     code" (pindyck);
   - proof sketch of `thm:kan-enclosure`: "one on the model's own polynomial
     pieces, the other on the ideal C² spline network", and "A separate
     rerun reproduced the searches of the code on the polynomial pieces".

   The only remaining use in the main text is the definition in Section 2.6
   ("the supplement calls the two the authors' code and the verifier's
   code").
4. **"Verifier" as a person in the supplement**, where it named a person
   rather than the defined code:
   - `B5-small.tex` (pindyck): "derived by hand separately by the authors and
     by the verifier" became "derived by hand twice, separately for the
     authors' code and for the verifier's code";
   - `B6-powerflow.tex`, `tab:pf-verification`: "(authors)", "(verifier)"
     became "(authors' code)", "(verifier's code)";
   - `E-audit.tex` (ghg_3veh history): "The audit's verifier on both old
     texts gives" became "The audit implementation, run on both old texts,
     gives" (the term used elsewhere in S4).
5. **Stretched line in a certificate box** (`sections/04-split.tex`,
   certificate of `thm:optcdeg2-bound`). The line before the unbreakable
   number 293.8760750958728 was visibly stretched (badness 4859). It now
   reads "certifies the weaker 293.8760750958728", which is true (the number
   is below L = 293.87607509587509237) and fills the line.
6. **Stretched cells in Table S20** (`sections/B7-eg.tex`, `tab:eg-points`).
   The justified last column showed wide gaps (badness 10000). The column is
   now ragged right (`>{\raggedright\arraybackslash}p{6.5cm}`).

## 4. Scan results

### Printed TODOs and `??`

- `??`: none in either PDF.
- TODOs: three, all in the declarations of `11-conclusion.tex` (licence of
  the archived code and data; competing interests; funding).
- `\archiveDOI`: five, at `01-introduction.tex:145`,
  `10-reproducibility.tex:21`, `11-conclusion.tex:77` and `:82`, and
  `I-reproduction.tex:23`.

### Banned phrases (style guide)

- **Main paper:** none. "significant" occurs only in "significant digits".
  No "independent", no "Moreover"/"Furthermore"/"Additionally", no
  rhetorical question (the one "?" is in a URL). Em dashes occur only as
  empty table cells and in bibliography titles.
- **Supplement:** none of the banned words in our prose. Hits that are
  acceptable: "leveraging" and "Robust" in two cited titles; "we claim no
  novelty" (three times); "If moreover" inside two lemma statements;
  "independent" only in the mathematical sense (linearly independent,
  independent controls, ranging independently).
- **"This section …" openings (style guide, "Also avoid"):** nine
  supplement sections start this way: S1 (`B0-families.tex:5`), S1.3
  (`B3-camshape.tex:4`), S1.4 (`B4-chain-catmix.tex:4`), S1.5
  (`B5-small.tex:5`), S1.6 (`B6-powerflow.tex:4`), S2 (`C-points.tex:6`),
  S3 (`D-literature.tex:12`), S4 (`E-audit.tex:6`), S6 (`H-solvers.tex:6`),
  plus S7.1 (`I-reproduction.tex:22`). Not changed: these sentences list
  which main-text results the section proves, which a reader of a supplement
  needs. If the rule is to apply, the rewrite of style-check-r1 H1 works
  here too ("We prove Theorem 5.3, …").

### Internal names

- **Main paper:** no "wave", "route", "dossier", "critic", "agent", "LLM",
  "AI", "review round", register identifiers or decision numbers; no script
  or file name (no `.py`, `.sh`, `.json`, `.log`, `.csv` and no
  `\nolinkurl` path). "Tier 1–3" and "claim register" are defined in
  Sections 2 and 10. "Verifier" occurs only in the Section 2.6 definition
  (Section 3, item 3).
- **Supplement:** no "route R", "critic", "agent", "LLM" or "AI" (the four
  "AI" hits are the matrix symbol $A_I$). "wave2", "wave3", "dossiers" and
  "r2" occur only inside file paths in S7 (the claim register
  `tab:repro-register` and the setup paragraph), which the style guide
  permits in the reproducibility appendix. "The authors' code" and "the
  verifier's code" remain the supplement's defined pair (Section 6,
  item 3).

### Claims and displays of outline section 8

A scan of both PDFs for the superseded or unsafe strings of outline §8
item 11 found them only in the S8 table of unsafe strings
(`tab:displays-unsafe`), with one exception allowed by §8.11:
352.238025369202 ("valid but superseded; never as the paper's dual")
appears in Table 1, the `lukvle10` certificate box and S1.1 as the weaker
bound that the second code certifies, never as the paper's dual.
"Zero duality gap" appears only negated ("we claim neither … nor a zero
duality gap") and in a cited title; "formally verified" only negated.
"Most closures" (Section 9.3, `sec:interpretation-reading`) refers to the
27 of 31 closures counted in Section 9.1 (`sec:interpretation-structure`)
whose certificates branch in at most three coordinates, not to the
15-of-31 pattern.

## 5. Page counts

Measured from the bookmark positions in the final PDFs (A4, 11 pt, 25 mm
margins) with `/tmp/r2/pages.py` (a copy of `/tmp/r1/pages.py`); the
declarations and References headings were located with `pdftotext -bbox`.
Floats count where they print. A count of 1.00 is one full text area.

### Main paper (`build/main.pdf`, 62 pages)

| part | pages | target | difference |
|---|---:|---:|---:|
| Title, abstract, keywords | 0.64 | – | |
| 1 Introduction | 5.00 | 5 | 0 |
| 2 Semantics (with the full-page Table 1) | 5.79 | 5 | +0.79 |
| 3 Results (with Table 2 and Figure 1) | 3.92 | 4 | −0.08 |
| 4 Split certificates | 7.93 | 8 | −0.07 |
| 5 Other certificates | 7.98 | 8 | −0.02 |
| 6 Points | 2.45 | 2.5 | −0.05 |
| 7 Audit | 3.42 | 3.5 | −0.08 |
| 8 Solvers | 3.42 | 3.5 | −0.08 |
| 9 Interpretation (with Table 9) | 2.52 | 2.5 | +0.02 |
| 10 Reproducibility | 1.42 | 1.5 | −0.08 |
| 11 Conclusion | 1.95 | 2 | −0.05 |
| **Main text, Sections 1–11** | **45.81** | **45.5 (about 46)** | **+0.31** |
| Statements and declarations | 0.34 | – | |
| **with declarations** | **46.15** | | **+0.65** |
| References | 7.07 | – | |
| Appendix A Model semantics | 3.14 | 3 | +0.14 |
| Appendix B Proofs for the split certificates | 4.33 | 4 | +0.33 |

Compared with revision 1, the main text is 2.0 pages shorter (47.78 to
45.81). Appendix B grew from 3.77 to 4.33 pages; its source comment says
that the `lnts` proof moved there from Section 4.2. The last page (62) is
one third full.

### Supplement (`build/supplement.pdf`, 138 pages)

| part | pages |
|---|---:|
| Title, note, contents | 1.48 |
| S1 Certificates by family | 71.52 |
| – S1.1 lnts, lukvle10 | 7.49 |
| – S1.2 dtoc5, optcdeg2 | 8.18 |
| – S1.3 camshape | 5.79 |
| – S1.4 chain, catmix | 10.44 |
| – S1.5 six small instances | 10.20 |
| – S1.6 powerflow | 6.78 |
| – S1.7 eg | 7.68 |
| – S1.8 waterno2 | 6.79 |
| – S1.9 ann, KAN | 7.89 |
| S2 Exactly feasible points | 8.81 |
| S3 Prior literature | 6.60 |
| S4 Audit details | 13.04 |
| S5 eg rounding-error analysis | 8.18 |
| S6 Solver campaign and SCIP defect | 12.51 |
| S7 Reproduction guide and claim register | 6.65 |
| S8 Display record | 1.70 |
| **Content S1–S8** | **129.01** |
| **Before references** | **130.49 (target about 95; +35)** |
| References | 7.21 |

Compared with revision 1, the supplement grew by about 2.3 pages of content
(126.7 to 129.0). Revision 1 gave the front matter as 2.48 pages and the
part before the references as 129.2; the correct figures for that build
were 1.48 and 128.2 (the script prints start positions counted from 1).

## 6. Remaining problems

1. **Placeholders** (expected): three declaration `\TODO`s and five
   `\archiveDOI`s (Section 4).
2. **Supplement length**: 130.5 pages before the references against about
   95. The options of integration-notes-r1 §8 item 1 still apply.
3. **"Authors' code" and "verifier's code" in the supplement.** The
   supplement sources use "verifier's" 28 times, mostly in this defined
   pair, which Section 2.6 introduces. style-check-r1 B7 recommends "first" and "second implementation" throughout, because
   "verifier" suggests a separate person. Section 2.6 also maps the pair
   onto "the first implementation produced [the certificate], and a second
   implementation checked it", but the supplement says that the displayed
   bound comes from the verifier's code for `ex6_2_5`/`ex6_2_7`, `etamac`,
   `pindyck`, `catmix` and `eg`, and that the verifier's code is the
   certificate of record for `chain`. For these families the roles are the
   other way round. Choosing one wording, and correcting the Section 2.6
   sentence, is a terminology decision for the lead author.
4. **"This section …" openings** in nine supplement sections and S7.1
   (Section 4); not changed.
5. **Underfull boxes, not visible as defects:** two certificate-box lines of
   SHA-256 prefixes in S6.5 and S6.6 (`H-solvers.tex:99` and `:220`,
   badness 1286 to 3746, slightly wide spaces) and one bibliography entry in
   each document (Göß, badness 1308).
6. **Claim index is stale** (open-items §4): this pass edited eight section
   files after `artifact/claims.json` was built. Rebuild it with a `/tmp`
   copy of `artifact/build_claims.py` after the last edit, rerun the
   validator, and update the counts in S7.1 if they change.
7. **`figures/fig-camshape-profiles.pdf`** is still generated but not
   included anywhere (integration-notes-r1 §8 item 9).

## 7. Files changed in this pass

- `sections/03-results.tex` (Figure 1 height),
  `sections/04-split.tex` (certificate box line),
  `sections/05-other.tex` (three "verifier" places),
  `sections/G-proofs-split.tex` (TODO removed),
  `sections/B5-small.tex`, `sections/B6-powerflow.tex`,
  `sections/E-audit.tex` (verifier as a person),
  `sections/B7-eg.tex` (Table S20 column).
- `figures/*.pdf` regenerated; rendering unchanged.
- `build/` rebuilt from empty.
- This file.
