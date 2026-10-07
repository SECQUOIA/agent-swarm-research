# Integration notes, revision 1 (2026-10-04)

Integration of the revised paper (`main.tex`) and the new supplement
(`supplement.tex`) after the editors' round (m-intro-sem, m-results, m-split,
m-other, m-points-audit, m-solvers, m-interp-concl, s-b1b2, s-b3b4, s-b5b6,
s-b7f, s-b8b9, s-cd, s-eh, s-ij). Nothing was committed. Nothing in
`research-20260929/` or `literature/` was edited. No scientific script was
run; the table and figure generators were run from `/tmp` as `data/README.md`
prescribes. All commands ran on at most two cores (`taskset -c 0,1`). A
backup of the paper directory before this pass is in
`/tmp/r1/paper-before-r1.tar`.

## 1. Result in brief

- Both documents build with `make`, from a clean `build/`: exit 0, 0 LaTeX
  errors, 0 undefined references in either direction, 0 undefined
  citations, 0 multiply defined labels, 0 BibTeX warnings, 0 overfull boxes,
  and no `??` in either PDF.
- `build/main.pdf` has 63 pages and `build/supplement.pdf` 135.
- The main text (Sections 1 to 11) runs to 47.8 pages, plus 0.7 page of
  declarations, against a target of about 46. The supplement runs to about
  129 pages before its references, against a target of about 95.
- Every move in `development/moves/` has landed, or the receiving editor
  replaced it with prose that keeps its facts (Section 4).
- Fifteen inconsistencies were fixed (Section 3). One displayed number
  changed: "up to $1.1\cdot10^6$ leaves" became "up to $1.12\cdot10^6$
  leaves" in Table 9 (`tab:structure`), numbers-check item 13.
- Placeholders that remain: 9 `\TODO` and 5 `\archiveDOI` (Section 7).

## 2. Build and checks

Commands, run in `paper-open-minlplib/`. The checks are those of
`development/build.md`.

```bash
taskset -c 0,1 make clean && taskset -c 0,1 make
grep -a 'undefined\|multiply defined' build/main.log build/supplement.log   # nothing
grep -a 'LaTeX Warning: TODO\|archive DOI' build/main.log build/supplement.log   # 14 lines
pdftotext build/main.pdf - | grep -c '??'         # 0
pdftotext build/supplement.pdf - | grep -c '??'   # 0
grep -a -c Overfull build/main.log build/supplement.log   # 0, 0
grep -a Warning build/main.blg build/supplement.blg       # nothing
```

Underfull boxes: 2 in main (a certificate-box line, a bibliography entry)
and 8 in the supplement, none visible.

Other targeted checks:

- Labels, by script over all section and table files: no label is defined
  twice, within one document or across the two. Every label quoted in a
  moves file exists, except the four labels of the three deviations noted in
  Section 4.
- Every theorem, proposition, lemma and corollary of the main text has a
  proof in place, a prose proof right after it, or a "Proof of \cref{...}"
  in Appendix B (G) or the supplement (script, then read). Every supplement
  sentence of the form "Section X proves ..." points to a main-text result
  whose proof is still in the main text: `thm:lnts-opt`,
  `prop:dtoc5-identity`, `thm:dtoc5-bracket`, `prop:pf-duality`,
  `prop:camino-eg` and `prop:minotaur-optcdeg2`.
- Every table, figure and box label is cited at least once, except
  `box:scip` (Section 8; the box is shown but not cited) and the inline
  lemma `lem:pindyck-polytope` (S1.5). Neither needs a citation.
- Text scans for the decisions: no "independent" except in its
  mathematical sense; no AI or agent wording; no band theory outside two
  source comments; no "all six KAN" or "six KAN models"; no banned style
  phrases; em dashes only as empty table cells; no hard-coded section,
  table, figure or theorem numbers (the only ones left are numbers in cited
  external works).

## 3. Inconsistencies fixed

### Shared files

1. **`macros.tex`, `\inst` in italic text.** In theorem statements the
   slanted typewriter font left a visible gap after every underscore
   ("waterno2_ 06", "QPLIB_ 8803"). This affected Sections 4, 5 and 8, H
   and E. `\inst` now always uses upright typewriter type
   (`\def\UrlFont{\ttfamily\upshape}`), as tested in a small document. This
   completes the `\inst` part of decision 5.
2. **`data/make_tables.py`, instance names.** Table 1 (`tab:trust`),
   `tab:staged`, `tab:points`, `tab:structure`, `tab:claims` and
   `tab:claims-campaign` printed instance names as plain text with escaped
   underscores. They now use `\inst`, as the style guide requires. For the
   claims tables, a new helper `model_tex` wraps the name and the "copy of"
   name.
3. **Table 1, pindyck row** (m-intro-sem open 3; numbers-check item 7).
   - Dual column: "bound [E]" became "bound [E] from [I] enclosures".
   - Certifier column: "bound from exact enclosures" became "bound from the
     verifier's [I] enclosures; the authors' enclosures give a slightly
     weaker one".
   - This matches S1.5 (`B5-small.tex`, trust-base paragraph) and the
     Section 5 certificate box.
4. **Table 1, eg row** (s-b7f open 5). "A second certificate covers part of
   the domain" was true only for `eg_disc2_s`. It now reads "a second
   certificate covers `eg_int_s`, `eg_disc_s` and part of `eg_disc2_s`"
   (S1.7, `tab:eg-matrix`; S5 certificate box).
5. **Table 1, KAN row (decision 6).** "KAN (six models)" became "KAN (the
   six instances of our set)", and $R_P$ became `\RP`.
6. **`tab:kan` caption** (m-results open 2). "The six KAN models" became
   "The six KAN instances of our set" (decision 6). $R$ and $R_P$ became
   `\Rnet` and `\RP`, as in the text. The claims tables likewise print
   `\Rnet` in the model and position columns.
7. **`tab:closures` caption.** The prior code N read "none found". It now
   uses the definition of Section 3.4 and S3: "no prior global result
   consistent with our certificates found".
8. **`tab:structure`, eg branching (numbers-check item 13).** "Up to
   $1.1\cdot10^6$ leaves" understated the maximum of 1,114,361 leaves. It
   now reads "up to $1.12\cdot10^6$ leaves". **This is a number change.**
9. **`tab:claims` caption** (s-eh open 4). The caption said that no exactly
   feasible point attains any listed value, but the last row is our own
   floating-point KKT point of `optcdeg2`, which lies above $U$. The
   caption now says so.

### Section files

10. **Hash pointers** (s-ij open 1, m-intro-sem open 7). The SHA-256
    prefixes moved to S7.2 (`tab:sem-hashes`). Three sentences still pointed
    elsewhere:
    - `10-reproducibility.tex` cited Appendix A, which no longer has them;
    - `02-semantics.tex` and `A-semantics.tex` cited all of S7.
    All three now cite `tab:sem-hashes`.
11. **Pointer for the camshape sensitivity result** (s-b3b4 open 6).
    `A-semantics.tex` now cites `rem:camshape-robust` instead of the whole
    camshape section.
12. **The ANN codes were called "separately written", against the paper's
    own definition** (s-b8b9 open 2). Section 2.6 defines separately
    written code as written "without importing or reading the checked code".
    The author of the second `ann_cumene_tanh` bounding code read the first
    in full and copied one idiom from it (S1.9, `rem:ann-saturation` and the
    paragraph after it; dossier `ann-kan.md`, issue I12 and the proof of
    Theorem A.2). Four places now agree with the definition:
    - Section 2.6 names this as a second exception and says "apart from
      these exceptions";
    - Section 1 says "by separately written code apart from named
      exceptions";
    - Section 3.3 says "two codes";
    - Section 5.5 says "two codes", adding that the second does not import
      the first but its author read it.

    No claim changes, because the bound is valid if either code is correct.
13. **Claim register, eg row** (s-b7f open 4). The primal checker was given
    as `verify_primal.py`, which is a 50-digit mpmath evaluation. The proof
    the paper uses is the library-free dyadic check. The row now names
    `$P/development/dossiers/primal-points-checks/eg_dyadic_check.py`
    (log in its `logs/` folder) and keeps `verify_primal.py` as the program
    that writes the points and checks them at 50 digits.
14. **Scope of the eg trust statement in Section 11.2** (decision 7). The
    sentence said that no accuracy guarantee is assumed "for the NumPy, libm
    or Intel SVML functions". The review's code-correctness premise does
    include NumPy's basic arithmetic. The sentence now reads "for the
    exponential and power functions of NumPy, libm or Intel SVML", as in
    Sections 2.5, 5.5 and S5.6.
15. **`development/labels.md`.** It still listed 10 labels that no longer
    exist or were never placed (`lem:sem-multiplier`, `thm:band-identity`,
    `prop:band-cells`, `sec:interpretation-band`, `fig:band-schematic`,
    `fig:results-funnel`, `fig:camshape-profiles`, `box:glance`,
    `box:kan-example`, and the unused `asm:eg-exp`/`asm:eg-pow`). Each is
    now marked as removed or unused, with the reason.

## 4. Generators and moves

### Generators (run from `/tmp`)

- `data/make_tables.py`: 673 checks, 0 failed.
  - Tables that changed: `tab-trust`, `tab-staged`, `tab-points`,
    `tab-structure`, `tab-closures`, `tab-kan`, `tab-claims` and
    `tab-claims-campaign`, all from the edits in Section 3.
  - `tab-audit-pairs` is byte-identical.
  - In `numbers.json`, only the text fields of `trust_table` changed; no
    number changed.
- `data/make_campaign_table.py` (115 ok) and `data/make_points_table.py`
  (88 ok): all checks pass, and their tables are byte-identical.
- The six figure scripts in `figures/` all ran. Rendered at 60 dpi, every
  figure is pixel-identical to its previous version; only the PDF metadata
  changed.
- `figures/fig-camshape-profiles.pdf` is generated but not used anywhere
  (see Section 8, item 9).

### Moves

Every block in the seven moves files has landed in the supplement, with
three deliberate deviations:

- `box:kan-example` (m-other move 2). The S1.9 editor took the alternative
  the moves file offers: the worked example is prose after the proof of
  `prop:kan-infeasible`, with all its numbers, and nothing cites the box.
- `tab:sem-operators` and `tab:sem-gams-detail` (m-intro-sem moves 2 and 3)
  became prose paragraphs in S7.2. Nothing cites them.
- `fig:camshape-profiles` (m-other move 3, recommended only) was not placed.

Facts listed as "cut without a move" were spot-checked, and each still
exists where the moves files say:

- the `optcdeg2` p2 margin 1.45 (S1.2 and `tab:claims`);
- the BARON violations $9.995\cdot10^{-11}$ (S6);
- MINOTAUR's 5.3897 (S1.2 and S3);
- the powerflow shunt data and the angle limit 0.26 (S1.6);
- the QPLIB copy shifts $8.539\cdot10^{-7}$ and $8.699\cdot10^{-5}$ (S1.3);
- the p4 violation $1.08\cdot10^{-11}$ (S2);
- how far the powerflow points moved from p1 (S2);
- the "ten of the 19" observation (S4.1);
- the benchmark-check literature (S3).

## 5. Lead-author decisions: compliance check

| decision | status |
|---|---|
| 1 Structure | Main: abstract, Sections 1–11, references, Appendix A, Appendix G (printed as Appendix B). Supplement: S1 (B0–B9), S2 (C), S3 (D), S4 (E), S5 (F), S6 (H), S7 (I), S8 (J), with its own references. `\cref` works both ways. |
| 2 Band theory | Removed from Section 9 and Appendix G, with its TODO; no band label remains. Section 9 is an interpretation with no theorems. |
| 3 Page targets | Not met; see Section 6. |
| 4 Condensing | Main text cut from about 75 to 48 pages. Qualifiers checked at the places edited here. |
| 5 Generated tables | The AI-session sentence is gone, theorem numbers use `\cref`, the camshape row is corrected, names use `\inst` everywhere, and `\inst` is fixed in italic text. |
| 6 KAN | "The six KAN instances of our set" in the abstract, Sections 1, 3 and 5, `tab:kan`, Table 1 and S1.9; S1.9 notes the four further KAN instances. |
| 7 eg trust base | Review wording in Sections 2.5, 5.5 (hypothesis of `thm:eg-bounds`) and 11.2, S5.6 and the claim register; scoped to exp/pow everywhere. No TODO says that no review exists. |
| 8 Declarations | Short block with marked placeholders for licence, competing interests and funding, and `\archiveDOI` for data and code; no AI statement. |
| 9 Wording | "Separately written implementation" throughout; no "independent review". |

**numbers-check.md: all 18 items are resolved in the current tree**
(checked by grep and reading):

- Items 1–4: "44 to 151"; "0.18"; the reading-(c) sentence in Appendix A;
  the branching sentence.
- Items 5–7: affine-split wording; pindyck added in three places; pindyck
  trust base, now also in Table 1.
- Items 8–9: stage loss "about $8.9777\cdot10^{-16}$"; $2.13\cdot10^{-10}$.
- Item 10: about −1673 to −36, about 5.7%, 41,618.4 and −286.81.
- Items 11–13: 361 and 295 (S3.4); 5.760539610694994 printed only in S8;
  $1.12\cdot10^6$.
- Items 14–15: times 4 s and 2.0 CPU-hours; "110 of the 158".
- Items 16–18: 7.487…% and 80.598…%; no "independent"; $2.73^{998}$.

**revision-notes.md:** items 1–4 are applied in S1.7 and S5. They were
checked in S5 (`F-eg-rounding.tex`): the power-auditor domain, the
approximate thresholds 1.954e-14 and 1.077e-14, the $3\uround$ allowance,
the root-box restriction, and bit identity claimed for `eg_disc2_s` only.

## 6. Page counts

The counts come from heading positions in the final PDFs (A4, 11 pt, 25 mm
margins), measured with a pypdf script (`/tmp/r1/pages.py`). The
References headings are located by pdftotext. Floats count where they print.

### Main paper (`build/main.pdf`, 63 pages)

| part | pages | target | difference |
|---|---:|---:|---:|
| Title, abstract, keywords | 0.64 | – | |
| 1 Introduction | 5.05 | 5 | +0.05 |
| 2 Semantics (with the full-page Table 1) | 5.72 | 5 | +0.72 |
| 3 Results (with the closures table and Figure 1) | 4.30 | 4 | +0.30 |
| 4 Split certificates | 8.72 | 8 | +0.72 |
| 5 Other certificates | 8.57 | 8 | +0.57 |
| 6 Points | 2.50 | 2.5 | 0 |
| 7 Audit | 3.78 | 3.5 | +0.28 |
| 8 Solvers | 3.59 | 3.5 | +0.09 |
| 9 Interpretation (with the full-page Table 9) | 2.52 | 2.5 | +0.02 |
| 10 Reproducibility | 1.46 | 1.5 | −0.04 |
| 11 Conclusion | 1.57 | 2 | −0.43 |
| Statements and declarations | 0.71 | – | |
| **Main text, Sections 1–11** | **47.78** | **45.5 (about 46)** | **+2.3** |
| **with declarations** | **48.49** | | **+3.0** |
| References | 6.97 | – | |
| Appendix A Model semantics | 3.13 | 3 | +0.13 |
| Appendix B (G) Proofs for Section 4 | 3.77 | 4 | −0.23 |

The excess sits in Sections 2, 4 and 5, about 2 pages together. No page of
the main paper except the last is less than 80% filled (checked by
script), so float placement wastes nothing. Further savings would mean moving content.

### Supplement (`build/supplement.pdf`, 135 pages)

| part | pages |
|---|---:|
| Title, note, contents | 2.48 |
| S1 Certificates by family (B0–B9) | 70.42 |
| – S1.1 lnts, lukvle10 | 7.32 |
| – S1.2 dtoc5, optcdeg2 | 7.78 |
| – S1.3 camshape | 6.15 |
| – S1.4 chain, catmix | 10.35 |
| – S1.5 six small instances | 9.99 |
| – S1.6 powerflow | 6.47 |
| – S1.7 eg | 7.56 |
| – S1.8 waterno2 | 6.73 |
| – S1.9 ann, KAN | 7.79 |
| S2 Exactly feasible points (C) | 8.53 |
| S3 Prior literature (D) | 6.47 |
| S4 Audit details (E) | 12.77 |
| S5 eg rounding-error analysis (F) | 8.33 |
| S6 Solver campaign and SCIP defect (H) | 12.46 |
| S7 Reproduction guide and claim register (I) | 6.08 |
| S8 Display record (J) | 1.68 |
| **Content S1–S8** | **126.7** |
| **Before references** | **129.2 (target about 95; +34)** |
| References | 5.8 |

All S editors report that the 20–30% cut was not reachable without removing
complete proofs, certificate boxes or verified facts. The material moved in
from the main text adds about 8 pages. Their options are in Section 8,
item 1.

## 7. Remaining TODOs and placeholders

The build log shows 14 warnings: in main, 4 `\TODO` and 4 `\archiveDOI`;
in the supplement, 5 `\TODO` and 1 `\archiveDOI`.

| location | content | note |
|---|---|---|
| `sections/G-proofs-split.tex:13` | confirm the extended-value proofs (minorant induction, finite potentials) by a separate check | m-split proposes dropping it, since outline §9 item 5 was tied to D1. Register PT-06 asks for the check whenever these proofs are included, and `thm:catmix-bound` and `thm:waterno2-bounds` rest on them. Recommendation: keep. |
| `sections/11-conclusion.tex:83` | licence of the archived code and data | D8 |
| `sections/11-conclusion.tex:88` | competing interests | placeholder (decision 8) |
| `sections/11-conclusion.tex:91` | funding | placeholder (decision 8) |
| `sections/B7-eg.tex:348` | the dyadic eg primal check needs one review with a saved log of its exponential test before it is called reviewed | register EG-07, C-54. The text does not call it reviewed. |
| `sections/C-points.tex:131` | bibliography entry for Lindemann–Weierstrass (Baker 1975, Thm. 1.4 suggested; theorem number unchecked) | `references.bib` has none |
| `sections/D-literature.tex:236` | update the unread-source list after the reading of register O-8; add BibTeX entries for sources named without a key | |
| `sections/E-audit.tex:494` | reviewer rerun of the second rocket proof and of the exact GAMS/OSIL comparison | register C-44 (AU-03, AU-04). Section 7 relies on both. |
| `sections/I-reproduction.tex:50` | build `claims.json`; make the review scripts relocatable | before archiving |
| `\archiveDOI` | `01-introduction.tex:135`, `10-reproducibility.tex:21`, `11-conclusion.tex:78` and `:83`, `I-reproduction.tex:23` | D8 |

## 8. Decisions left for the lead author

1. **Length.** The main text is about 2.3 pages over its target (3.0 with
   the declarations); the supplement is about 34 pages over. The editors'
   options, roughly in order of savings:
   - **Main text:**
     - move `prop:camshape-deficit`, or `lem:pf-leaf` and `lem:pf-planes`,
       to the supplement (Section 5, about 0.5 page);
     - move the lnts lemma and proof to S1.1 (Section 4, about 0.5 page);
     - move part of Section 2.6 to Section 10, or drop Remark 2.3(3)
       (Section 2);
     - move the corollary, the rocket paragraph or the class (i-r)
       discussion to S4 (Section 7);
     - trim the generated captions of `tab:unclosed` and `tab:kan` (about
       0.1 page).
   - **Supplement:**
     - move the two padding-lemma error tables of S5 to an archived note
       (about 2.7 pages; this breaks the complete-proofs rule);
     - merge `tab:claims` and `tab:claims-campaign` (about 0.5–1 page);
     - replace `tab:audit-inputs` with a pointer to the archive (0.4);
     - cut `prop:chain-weierstrass` with `rem:chain-boundary` (1.2) or
       `lem:catmix-losses` (0.8);
     - keep only the decisive leaves of `tab:pf-leaves` (0.4);
     - trim the "Certificate details" boxes of S1.1–S1.2 (0.3);
     - move the claim register to `claims.json` with a short table (S7,
       about 2 pages).
2. **waterno2 under binary64 data (reading c).** Sections 2 (Remark 2.3),
   6 and 11, Appendix A and S1.8 state that our waterno2 points are
   infeasible under binary64 data; S1.8 proves this and register WN-07
   adopts it. This conflicts with outline §8 item 2. Same status as in
   integration-notes §5 item 4.
3. **How the verification records describe who checked.** D7 removes AI
   statements, and the files now differ:
   - S1.1 and S1.2 say nothing;
   - S1.3 and S1.4 say "made within this project with separately written
     implementations …; none is peer review" (this dropped the earlier
     "none is a human review");
   - S1.5 says "a separate review" and "a later check read … line by line";
   - S1.6 says "third code" and "separate check";
   - S5 adds one sentence on "a separate review" of an earlier form of the
     proofs.

   The format also differs: tables in S1.1, S1.2, S1.5 and S1.6, prose in
   S1.3 and S1.4. Choose one wording and one format.
4. **S5's sentence on the separate review.** The eg review read an earlier
   written form of the proofs, not S5's new underflow paragraph. The
   sentence does not claim that it did. Keep it, or drop it, or have the
   paragraph checked.
5. **The ANN qualification of Section 3, item 12.** Confirm the wording, or
   decide to describe the second ANN code differently.
6. **Certificate boxes.** Section 4's boxes have six fields and Section 5's
   have four.
7. **Replay times.** Some boxes quote other runs than the claim register
   (for example `optcdeg2`: 16–18 s in Section 4, 5 s + 17 s in S1.2, about
   20 s in S7). Section 10 says so. Pick one run per result if a single
   figure is wanted.
8. **Notation.** $c_T$ (Section 4.5) and $r_T$ (S1.8) for the waterno2
   horizon constant; S1.8 states the mapping.
9. **`fig:camshape-profiles`.** Generated but not placed. Add it to S1.3
   (about 0.4 page) or delete the figure and its script.
10. **Removed boxes.** The outline's Box 1 ("Results at a glance") and the
    notation box were removed from Sections 1 and 2. Restoring Box 1 would
    cost about 0.45 page.
11. **Unchanged from earlier notes:**
    - dtoc5 uniqueness is not claimed (DO-02);
    - no upstream SCIP report has been filed (D4); the text says only that
      a minimal reproducer is in the supplement;
    - Hansen (1992) is credited by name without a bibliography entry;
    - the Basu et al. (2023) entry in `references.bib` is no longer cited
      (BibTeX omits it).
12. **Errors in source documents (for the register; `R/` is read-only
    here).**
    - `R/publication/primal/dtoc5-lukvle10/report.md` and the lnts-lukvle10
      dossier give $2.73^{999}\approx10^{436}$ and a seed range up to
      353.00.
    - The log gives exponent 998 and a maximum of 353.0047; the paper uses
      $2.73^{998}\approx10^{435}$ and 353.01 (s-cd).

## 9. Files changed in this pass

- `macros.tex` (`\inst` upright).
- `data/make_tables.py`; regenerated `data/numbers.json` (text fields of
  `trust_table` only) and `tables/tab-{trust,staged,points,structure,closures,kan,claims,claims-campaign}.tex`.
- `figures/*.pdf`: regenerated; the rendering is unchanged.
- `sections/01-introduction.tex`, `02-semantics.tex`, `03-results.tex`,
  `05-other.tex`, `10-reproducibility.tex`, `11-conclusion.tex`,
  `A-semantics.tex`, `I-reproduction.tex`.
- `development/labels.md` and this file.
