# Integration notes (2026-10-04)

Integration of the full draft of "Rigorous certificates for open MINLPLib
instances and an audit of listed dual bounds". Nothing was committed. Nothing
in `research-20260929/` or `literature/` was edited.

## 1. Build

Command, run in `paper-open-minlplib/`:

```bash
latexmk -pdf -interaction=nonstopmode -outdir=build main.tex
```

Result of the final build (`build/main.pdf`):

- 223 pages; latexmk exit code 0.
- 0 LaTeX errors, 0 undefined references, 0 undefined citations, 0 multiply
  defined labels; BibTeX: 0 warnings.
- 3 overfull lines, all under 1.4 pt (about 0.5 mm; not visible in print):
  B.9 line 18 (`\texttt{objvar}` and inline math), G line 449 (inline
  math), H line 294 (16-character `\texttt` hash). 9 underfull boxes.
- Warnings that remain on purpose: 13 `\TODO` and 5 `\archiveDOI`
  placeholders (Section 4).

The build failed for every writer only because `main.tex` did not load
`array` and `rotating`. Both are now loaded (see Section 3).

The per-writer build directories (`build-B1B2`, …, `build-split`) were
removed. They held only build outputs, copies of `references.bib` and
test drivers (`intro-test.tex`, `main-sem.tex`, `main-results.tex`,
`main-full.tex`, `main-solvers.tex`, `test.tex`) that existed only to add the
two missing packages. `build/` is git-ignored. The whole paper directory is
still untracked.

## 2. Page counts

Measured from the heading positions in the final PDF (A4, 11 pt, 25 mm
margins), to the nearest tenth of a page. Floats count where they print.

| part | pages | start | outline budget |
|---|---:|---:|---:|
| Title, abstract, keywords | 0.6 | 1 | – |
| 1 Introduction | 5.7 | 1 | 4.5 |
| 2 Exact semantics, certificates and verification (with Table 1) | 6.5 | 7 | 4 |
| 3 Instances and results at a glance | 7.5 | 13 | 3 |
| 4 Split certificates along stage structure | 14.1 | 21 | 7 |
| 5 Other certificate classes | 13.5 | 35 | 6 |
| 6 Exactly feasible points | 4.2 | 48 | 2 |
| 7 Audit of listed dual bounds | 5.9 | 53 | 3.5 |
| 8 Solver and published claims | 6.7 | 59 | 3 |
| 9 Interpretation (with the band subsection, D1) | 5.1 | 65 | 2.5 |
| 10 Reproducibility | 2.1 | 70 | 1.5 |
| 11 Conclusion, with statements and declarations | 3.0 | 73 | 2 |
| **Main text** | **about 75** | 1–75 | **39** |
| References | 9.3 | 76 | – |
| A Model semantics and OSIL reading | 5.1 | 85 | 2 |
| B Certificates by family (introduction) | 0.2 | 90 | – |
| B.1 lnts, lukvle10 | 7.2 | 90 | |
| B.2 dtoc5, optcdeg2 | 7.9 | 97 | |
| B.3 camshape | 6.8 | 105 | |
| B.4 chain, catmix | 11.2 | 112 | |
| B.5 six small instances | 11.2 | 123 | |
| B.6 powerflow | 6.9 | 134 | |
| B.7 eg | 8.1 | 141 | |
| B.8 waterno2 | 6.8 | 149 | |
| B.9 ann, KAN | 8.2 | 156 | |
| B total | 74.3 | 90–163 | 30 |
| C Exactly feasible points | 8.2 | 164 | 5 |
| D Prior literature | 5.7 | 173 | 4 |
| E Audit details | 12.6 | 178 | 6 |
| F eg rounding-error analysis | 8.5 | 191 | 3 |
| G Proofs for Section 4 (and band theory) | 6.8 | 199 | 3 + 2 |
| H Solver campaign and SCIP defect | 9.7 | 206 | 5 |
| I Reproduction guide and claim register | 5.0 | 216 | 3 |
| J Display record | 2.7 | 221 | 1 |
| **Appendices** | **about 139** | 85–223 | **about 64** |

The main text is about 1.9 times its budget, and the appendices about 2.2
times theirs. Trimming is an author decision (Section 5, item 1).

## 3. Inconsistencies found and fixed

No number was changed except where noted, and each change makes one file
agree with the others or with the verified source.

### Shared files

1. `main.tex`: added `array` and `rotating` (needed by every generated
   sideways table and every `>{...}` column). Added
   `\setlength{\emergencystretch}{1em}` for small overfull lines.
2. Instance names in generated tables printed literal backslashes
   (`kan\_r3\_h1\_n4`), because `\inst` is URL-based and the generators
   escaped underscores. `data/make_tables.py` (`inst_tex` and three
   captions) and `data/make_campaign_table.py` now emit plain underscores
   inside `\inst{}`; `make_points_table.py` already did. `macros.tex` is
   unchanged.
3. `data/make_tables.py`, Table 1 (`tab:trust`):
   - removed "all implementations and reviews were produced by separate
     AI-agent sessions" from the caption (decision D7); the caption now
     points to Section 2.6 for "separately written";
   - "Thm.~4.6" (the lnts theorem prints as Theorem 4.7) is now
     `\cref{thm:lnts-opt}`, and the internal name "Lemma A1" is now
     `\cref{lem:eg-padding}`;
   - camshape: "three exact codes agree to 30 digits" became "two exact
     codes and one with directed rounding agree to all printed digits"
     (B.3; Section 5.1 certificate box);
   - hvycrash: "two codes check the identity" became "proof by hand; one
     code checks the identities exactly" (B.5 verification table). The
     primal cell now says feasibility is proved by hand
     (`\cref{prop:hvycrash-identity}`) and the witness is checked in [I] by
     two codes. The last column is now "mpmath-free computer proof", with
     the hvycrash cell "no (proof by hand)", matching Table C.
4. `data/make_tables.py`, the staged-certificates table (`tab:staged`): the
   hard-coded "L.~4.1(a)", "Prop.~4.4" and so on are now `\cref`. The
   lukvle10 validity cell was "L. 4.1(a), Prop. 4.4"; Section 4.4 uses
   Lemma 4.1(d) and the row form of Proposition 4.4, and the cell now says
   so.
5. `data/make_tables.py`, other captions: `tab:kan` read
   "$\min_R F\le\min_{R_P}$" (missing $F$); `tab:claims-campaign` said "All
   returned points …", but the table lists only the 15 points evaluated at
   50 digits, out of 35 (Appendix H), and now says so; `tab:claims` used
   `Table~\ref` instead of `\cref`. Two narrow header columns were widened
   slightly to remove overfull headers.
6. Tables were regenerated from `/tmp`, as `data/README.md` documents:
   `make_tables.py` (672 checks, 0 failed), `make_campaign_table.py` and
   `make_points_table.py` (all checks ok). `tab-points-all.tex` came out
   byte-identical. `numbers.json` changed only in the five Table 1 text
   fields above; no number changed.
7. `development/labels.md`: five planned table labels never existed. The
   generated tables define `tab:staged`, `tab:points`, `tab:claims`,
   `tab:solvers` and `tab:structure`, and every section uses these. The
   plan now lists the actual labels, and `fig:audit-pipeline` is marked as
   not made.

### Section files

8. **A proof was lost in deduplication.** Section 4 deferred the proof of
   `cor:dtoc5-attained` to Appendix B.2, but the B.2 writer had removed it
   as a duplicate of Section 4. Section 4 now proves the corollary in six
   lines, using only the argument its old sketch stated: the identity
   `eq:dtoc5-squares` with $\hat\lambda_t\le0$, so $A_t\ge h$, compactness of the level set,
   and the deviation bound $(7.21\cdot10^{-43}/h)^{1/2}<1.9\cdot10^{-19}$.
9. **Circular proof pointers.** Appendix H said the proofs of
   `prop:camino-eg` and `prop:minotaur-optcdeg2` are in B.7 and B.2, while
   B.2 and B.7 point back to Section 8, which does prove both. H now says
   Section 8 proves them. The B.7 paragraph that repeated Proposition 8.8
   and its numbers became one pointer sentence, and the Section 8 proof
   points to Appendix H for the inputs.
10. `04-split.tex`: "$V_t\subseteq[-1,1.2134]$" was false; the computed
    maximum is 1.2134054 (`states_check.json`, `V_max = 1.213405434126372`).
    It now reads 1.2135, as in B.2. **This is a number change.**
11. `04-split.tex`: "to $q_0=-34.10$ and $q_N=0.286$" now reads "to about
    $-34.1$ at the start and $0.286$ at $t=N$", matching B.2 (the
    schedule is used only for $t\ge1$; $q_1\approx-34.08$).
12. `05-other.tex`: the smallest eg_int_s LP margin was "7.69e-11",
    rounded to nearest. The log gives 7.687113e-11 and B.7 prints
    7.68e-11; it now reads 7.68e-11. **This is a number change.**
13. `05-other.tex`, Section 5.2: it called all three dense-row certificates
    instances of Lemma 4.1(d). That holds for the equality rows of
    ex6_2_5/7; pricing050 has inequality rows with $\mu\ge0$, so the text
    now calls it Lagrangian weak duality.
14. `05-other.tex`, pindyck sketch: the noise-symbol count $K$ clashed with
    the constant $K$ in $e^{-Ks}$; it is now $m$.
15. QPLIB_8803 versus optcdeg2: B.2, Section 8 and Appendix H record
    three differences besides comments: a redundant declaration, the
    formatting of one option line, and the solve statement. Section 3.4,
    Appendix A.5 and Appendix D omitted the option line; all now include
    it. Section 3.4's "one model attribute" for dtoc5 became "one option",
    the term the other files use.
16. KAN count: MINLPLib has ten KAN instances, and the infeasibility proof
    covers our six. The introduction's "All six KAN models in MINLPLib"
    (C4) and "all six" (Box 1) now say "the six … among the 43 instances".
    The abstract was already correct.
17. waterno2 under reading (c). Sections 6, C and B.8 state that our
    waterno2 points are infeasible under binary64 data, which register
    WN-07 adopts and B.8 proves from $\fl(\omega)^k<\fl(\omega^k)$.
    Section 2.1 (`rem:sem-readings`, item 2), Appendix A.4 and Section 11.2 listed only dtoc5, chain and
    powerflow. They now include waterno2, and B.8's "We claim nothing for
    reading (c)" (right after the claim) now reads "Beyond this, we claim
    nothing for reading (c)". This conflicts with outline section 8, item 2
    (see Section 5, item 4).
18. Snapshot date: Sections 2.1 and 7.1 said "the site was last updated on
    2026-09-14". That date is the footer of the documentation page; the
    homepage copy shows 2026-07-29, and instance pages carry no date. Both
    now say "the documentation page … was last updated on 2026-09-14".
19. `B0-families.tex` was a stub (`\TODO{appendix B introduction}`). It is
    now a five-sentence introduction: what each family subsection contains,
    where the main text already proves results, what "Certificate details"
    boxes are, and the pointers to G, C and F. The repeated definitions of
    "the authors' code" and "the verifier's code" in B.5 and B.7 were
    removed; B introduction points to Section 2.6, which defines them.
20. eg review TODOs: Sections 2.5 and 5.5 still described the review as
    pending, or its corrections as not yet applied. All three TODOs (2.5,
    5.5, F) now say the same thing: the review exists (verdict verified),
    B.7 and F apply its four corrections, and the wording is an author
    decision (Section 5, item 3).

### Checked and found consistent (no change)

- Every main-text theorem, proposition, lemma and corollary is either
  proved where it is stated or has its full proof in the appendix that the
  text names. I checked all 57 by script and read the doubtful ones.
- Every table, figure and box label is referenced at least once. All
  planned theorem labels in `labels.md` exist. Only the optional fallback
  assumptions `asm:eg-exp`/`asm:eg-pow` are unused, because the audit
  completed.
- Repeated text: a shingle comparison of all section files found no
  repeated blocks beyond theorem restatements and short summaries in the
  introduction and Section 3. Earlier writers had already removed the
  duplicated proofs.
- Headline numbers agree across the abstract, introduction, Section 3 and
  the conclusion: 3.1e-9, nine exact optima, 1.68–6.21, 10.82%, 0.195%,
  2.42e-8, 1.08e-10, 11,086. The branching profile is 12 + 6 + 7 + 2 plus
  pindyck and eg, which matches Table 9.
- No local macro redefinitions; only one tagged Hypothesis H0 (the second
  one in F is now prose); no "Lemma A1" outside TODO text; no AI wording
  (D7); the SCIP text says only that a minimal reproducer is in the
  supplement (D4).
- Section 3.4 carries the credits that the introduction condensed
  (Octeract on QPLIB_2480, MINOTAUR 0.2.1 on QPLIB_8803, Ghaddar et al.
  2016, McDonald–Floudas 1997).
- Printed table numbers differ from the outline's plan (Table 2 is the
  funnel, so the closures table is Table 3; the staged table is Table 6;
  the lnts theorem is Theorem 4.7). All references use `\cref`, so this
  needs no change.

## 4. Remaining TODOs and placeholders

| location | content |
|---|---|
| `sections/02-semantics.tex:234` | eg review wording (author decision; see Section 5, item 3) |
| `sections/05-other.tex:462` | same decision, for Section 5.5 and its certificate box |
| `sections/F-eg-rounding.tex:439` | same decision; the review read the markdown proof, not this LaTeX, whose underflow paragraph differs |
| `sections/B7-eg.tex:380` | the dyadic eg primal check needs one review with a saved exponential test before it is called independent (register EG-07, C-54) |
| `sections/E-audit.tex:484` | the reviewer rerun of the second rocket proof and the exact GAMS/OSIL comparison (register C-44, AU-03/AU-04); Section 7 already relies on both |
| `sections/09-interpretation.tex:215` | read and cite the antecedents of the band theory (de Farias–Van Roy 2003; Grimm–Netzer–Schweighofer 2007; Korda–Magron–Ríos-Zertuche 2025; Han–Jiao–Weissman 2018; Junge–Osinga 2004; cost-shifting papers); not in the KB |
| `sections/G-proofs-split.tex:30` | independent confirmation of the extended-value proofs (G.3, G.5, G.6–G.7), outline section 9, item 5 |
| `sections/C-points.tex:115` | bibliography entry for Lindemann–Weierstrass (Baker, *Transcendental Number Theory*, 1975, Thm. 1.4; theorem number to check). No KB slug exists |
| `sections/D-literature.tex:245` | update the unread-source list after the pre-submission reading (register O-8), and add BibTeX entries for the sources named without a key |
| `sections/I-reproduction.tex:44` | build `claims.json` (paths and SHA-256 per register row); make the review scripts relocatable (they contain absolute paths) |
| `sections/11-conclusion.tex:100` | release licence (D8) |
| `sections/11-conclusion.tex:107` | confirm the competing-interests statement |
| `sections/11-conclusion.tex:110` | funding statement |
| `\archiveDOI` | `01-introduction.tex:153`, `10-reproducibility.tex:16`, `11-conclusion.tex:93` and `:100`, `I-reproduction.tex:16` (D8) |

The B introduction TODO was resolved (Section 3, item 19).

## 5. Decisions for the authors

1. **Length.** The main text runs to about 75 pages against 39, and the
   appendices to about 139 against 64. The writers proposed these cuts:
   - Section 4: move the chain, catmix, lukvle10 and waterno2 certificate
     boxes to their appendices, or move the lnts proof to B.1;
   - Section 5: shorten the camshape, pindyck and ann sketches that B.3,
     B.5 and B.9 prove in full, and the eg search-route paragraph;
   - Section 3: move the funnel table to Appendix D; shorten Section 3.4,
     which the introduction promises in detail;
   - Section 8: move the Table 7 discussion and the scope paragraph after
     Observation 8.7 to Appendix H;
   - Section 6: move the paragraph after Proposition 6.3 and parts of 6.2
     and 6.4 to Appendix C;
   - Appendices: merge or condense the verification and listed-status
     tables in B.1–B.4; trim B.7/F and D.
2. **Disclosure of how checks were done (D7 versus outline section 8,
   item 10).** D7 removes every AI statement from the text. The outline
   forbids "independent" without the definition and the AI-agent
   disclosure. Table 1 now defines "separately written" without the AI
   clause. B.3 and B.4 still say "none of the checks is a human review",
   while B.1 and B.2 say nothing; make the verification-record tables
   consistent once the disclosure wording is decided. The solvers writer
   also notes that the QPLIB copy bounds (Proposition 8.2) rest only on
   separately written implementations, with no human review.
3. **eg review.** An independent review exists
   (`development/reviews/sol-eg-audit.md`, verdict verified, four minor
   issues), and `revision-notes.md` asks for its corrections and its
   trust-base wording. B.7 and F apply both and avoid "reviewed" and
   "assumption-free". Decide whether the paper may now say "reviewed"
   (outline section 8, item 5), then update Table 1, Sections 2.5 and 5.5
   and Appendix F together. The new underflow paragraph in F differs from
   what the review read; ideally it should be checked.
4. **waterno2 under binary64 data.** The paper now follows register WN-07
   and states that our waterno2 points are infeasible under reading (c),
   proved in B.8. Outline section 8, item 2 forbids binary64 infeasibility
   claims beyond dtoc5, chain and powerflow. If the authors prefer the
   outline, remove the claim from Sections 2.1, 6.4, 11.2 and Appendices A.4,
   B.8 and C.
5. **dtoc5 uniqueness.** Register DO-02 wants the critic's uniqueness
   proof. D3 allows it only if independently checked, and the dtoc5 review
   did not check it. Uniqueness is not claimed.
6. **Notation.** Section 4.5 writes the horizon constant $c_T$ and B.8
   writes $r_T$, because $c$ is a pump coefficient there. Section 4.3
   writes the optcdeg2 reference velocity $\bar v_t$, and B.2 writes $c_t$;
   B.2 also uses $c_t$ for the dtoc5 rows. Both appendices state the
   mapping. Unify the symbols if desired.
7. **Optional references.** Hansen (1992) is credited by name in Section 6
   and cited through Kearfott (1998). The KB has
   `hansen2004-global-optimization-using-interval-analysis`, but marks it
   unread, so it was not added.
8. **SCIP report (D4).** No upstream report has been filed; the text says
   only that a minimal reproducer is in the supplement. Update the text if
   a report is filed.
9. **Figure 6** (`fig:camshape-deficit`) was added by the Section 8 writer
   and is referenced from Sections 5 and 8. Drop it if one figure fewer is
   preferred.

## 6. Errors in source documents (not in the paper; for the register)

The writers found these while checking. The paper uses the corrected
values.

- Register SV-09 / N-38: "80.6%" for eg_int_s is rounded to nearest (exact
  80.597%); the paper uses 80% (introduction) and 80.5% (Section 8).
- Register AU-16 and the outline: the audit range ends "7.3e-5" and
  "3.3e-7" are rounded to nearest (true extremes 7.328e-5 and 3.322e-7);
  the paper uses 7.4e-5 and 3.4e-7.
- Register AU-13 / audit critique C1: the `.solu` matches are not "within
  6e-9 relative" (near zero the relative difference reaches 1); all 589
  match within half a display unit.
- waterno2 dossier: the listed waterno2_18 gap 583.71% and the primal
  improvements 29.54 / 245.66 / 368.93 are rounded in the unsafe
  direction; the paper uses 583.72% and 29.53 / 245.65 / 368.92.
- waterno2 critique C1: "5.0e-4 below the stored bound" is the difference
  of certified values; the replay log shows about 4.0e-4.
- camshape dossier: |E2−E1| for n = 400, 800 printed as 1.96e-5 and
  4.92e-6 (rounded to nearest); the paper uses 1.97e-5 and 4.93e-6.
- lnts-lukvle10 dossier: multiplier range [0.2342, 0.4078]; the smallest
  multiplier is 0.234183, so the paper uses [0.2341, 0.4078].
- small critique: pindyck gap "≤ 5.6e-29" from the authors' enclosures is
  rounded unsafely (true 5.62e-29); the paper uses < 6e-29.
- eg-lemma-A1.md: the underflow argument is wrong (later factors reach
  about 7e15, not 1e8); F replaces it.
- data-semantics.md labels the first-wave dtoc5 and camshape author codes
  "O" in its table and "B̂" in DS-3 (no effect on any claim).
- pattern-theory dossier, section 5.4: the ex6_2_5/7 box counts belong to
  a different certificate from the displayed one (the paper uses 131,111
  and 42,111).
- `R/…/powerflow0039p.bb3t.log` FINAL line prints a wrongly scaled
  rational (2093.45); nothing uses it.
- Outline section 4.5 attaches "113–162 cells per link" to the final
  waterno2_06 certificate; those counts belong to the superseded
  intermediate step (final: 148–240).
- Outline C8: "two of the fifteen closures add a window" should be two of
  the six families (lukvle10 and chain, five closures).

## 7. Checks run (targeted, local)

- `latexmk -pdf -interaction=nonstopmode -outdir=build main.tex`, five
  times; final run as reported in Section 1.
- From `/tmp`: `make_tables.py` (672 checks, 0 failed),
  `make_campaign_table.py`, `make_points_table.py` (all checks ok). These
  write the paper tables in place, as documented in `data/README.md`. The
  previous tables, `numbers.json`, `check.log` and the generator sources
  are backed up in `/tmp/integ/backup/`.
- Read-only scripts in `/tmp/integ/`: proof-location map, repeated-text
  search, label coverage, a scan of displayed numbers for rounding
  variants, and scans for internal names, banned words and priority
  claims.
- `pdftotext` checks of the final PDF: no `??`, no literal `\_`; Table 1,
  Table 6 (staged certificates) and the claim register page were rendered
  and inspected.
- No scientific script was run. CI runs project-wide verification; none
  was run or inspected here.
