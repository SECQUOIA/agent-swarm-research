# Labels, macros and bibliography keys for the paper

This file tells section writers how to cross-reference, which macros and
environments to use, and which BibTeX keys exist. The plan itself is in
`outline.md`; the writing rules are in `style-guide.md`.

## 1. Files and build

- The paper has two documents. `main.tex` (the paper) and `supplement.tex`
  (the supplementary material) both input `preamble.tex`, which loads the
  packages and `macros.tex`. `main.tex` inputs sections 00-11, its
  bibliography and the appendices `A-semantics.tex` and
  `G-proofs-split.tex` (printed as Appendices A and B). `supplement.tex`
  inputs `B0`-`B10`, `C`, `D`, `E`, `F`, `H`, `I` and `J` (printed as
  Sections S1-S7; since round 2, `B10` is S1.10 and `J` is the subsection
  S7.5) and its own bibliography (same `references.bib`).
- Build both in the paper directory with `make` (see `build.md`). All
  output goes to `build/` (ignored by git through `.gitignore`).
- Each `\TODO` and `\archiveDOI` writes a warning to the log, so
  `grep 'TODO' build/main.log build/supplement.log` lists what is left.
- While nothing is cited, BibTeX reports "I found no \citation commands";
  this message disappears with the first `\citet`/`\citep`.

## 2. Section labels

Never type a section, theorem, table or figure number. Use `\cref{...}`
(it prints "Section 4.2", "Theorem 4.6", "Appendix A.3", "Box 1", and for
the supplement "Section S1.3", "Theorem S1.2", "Table S4", "(S5)").
`\cref` works in both directions between the paper and the supplement
(xr-hyper). Do not use `\cpageref` across the two documents. A `\cref`
list may mix labels of both documents; it names the paper's objects first
("Sections 10 and S7").

### Main text

| file | section | label | subsection labels (from the outline) |
|---|---|---|---|
| `00-abstract.tex` | Abstract, keywords, MSC | — | — |
| `01-introduction.tex` | 1 Introduction | `sec:intro` | `sec:intro-records` (1.1 Benchmark records are not proofs), `sec:intro-approach` (1.2), `sec:intro-contrib` (1.3), `sec:intro-prior` (1.4), `sec:intro-org` (1.5) |
| `02-semantics.tex` | 2 Exact semantics, certificates and verification | `sec:semantics` | `sec:semantics-model` (2.1), `sec:semantics-cert` (2.2), `sec:semantics-categories` (2.3 Categories A and B), `sec:semantics-display` (2.4), `sec:semantics-trust` (2.5), `sec:semantics-protocol` (2.6) |
| `03-results.tex` | 3 Instances and results at a glance | `sec:results` | `sec:results-selection` (3.1), `sec:results-closed` (3.2), `sec:results-other` (3.3), `sec:results-prior` (3.4) |
| `04-split.tex` | 4 Split certificates along stage structure | `sec:split` | `sec:split-framework` (4.1), `sec:split-affine` (4.2 lnts, dtoc5), `sec:split-richer` (4.3 optcdeg2, chain, catmix), `sec:split-window` (4.4 lukvle10), `sec:split-waterno2` (4.5) |
| `05-other.tex` | 5 Other certificate classes | `sec:other` | `sec:other-camshape` (5.1), `sec:other-dense` (5.2 ex6_2_*, pricing050), `sec:other-convex` (5.3 powerflow, etamac, pindyck), `sec:other-hvycrash` (5.4), `sec:other-bb` (5.5 eg, ann, KAN) |
| `06-points.tex` | 6 Exactly feasible points | `sec:points` | — |
| `07-audit.tex` | 7 An audit of MINLPLib's listed dual bounds | `sec:audit` | `sec:audit-screen` (7.1), `sec:audit-hyp` (7.2), `sec:audit-existence` (7.3), `sec:audit-results` (7.4), `sec:audit-limits` (7.5) |
| `08-solvers.tex` | 8 Solver and published claims under exact feasibility | `sec:solvers` | `sec:solvers-tolerance` (8.1), `sec:solvers-invalid` (8.2), `sec:solvers-campaign` (8.3) |
| `09-interpretation.tex` | 9 Interpretation and recommendations (round-2 title, after the merge with the recommendations of the former Section 11) | `sec:interpretation` | `sec:interpretation-structure` (9.1 Structure, evidence and interpretation; `sec:interpretation-evidence` and `sec:interpretation-reading` label paragraphs inside it), `sec:conclusion-recs` (9.2 Recommendations, moved from Section 11 in round 2); the band subsection `sec:interpretation-band` was removed by lead decision 2 |
| `10-reproducibility.tex` | 10 Reproducibility and computational effort | `sec:repro` | — |
| `11-conclusion.tex` | 11 Limitations and conclusion (round-2 title) | `sec:conclusion` | `sec:conclusion-limits`, `sec:conclusion-open` (paragraph labels since round 2); unnumbered "Statements and declarations" (no label). Round-1 decision LD-1 reverses decision D7: the declarations contain a "Use of AI tools" statement (marked for the authors to confirm), and Section 2.6 states how the implementations were produced; since round 2 (LD2-2) both state the same AI-use wording |

Writers may rename a subsection title; keep its label.

### Appendices (A and G, in the paper) and supplement (all others)

The labels kept their `app:` prefix and the old appendix letters below are
file names only: `G-proofs-split.tex` prints as Appendix B of the paper,
and the supplement numbers its sections S1 (`B0`-`B10`, with B1-B10 as
S1.1-S1.10), S2 (`C`), S3 (`D`), S4 (`E`), S5 (`F`), S6 (`H`) and S7 (`I`,
with `J` as its last subsection S7.5 since round 2).

| file | appendix | label |
|---|---|---|
| `A-semantics.tex` | A Model semantics and OSIL reading | `app:semantics` |
| `B0-families.tex` | B Certificates by family (short introduction) | `app:families` |
| `B1-lnts-lukvle10.tex` | B.1 lnts and lukvle10 | `app:lnts` |
| `B2-dtoc5-optcdeg2.tex` | B.2 dtoc5 and optcdeg2 | `app:dtoc5` |
| `B3-camshape.tex` | B.3 camshape | `app:camshape` |
| `B4-chain-catmix.tex` | B.4 chain and catmix | `app:chain` |
| `B5-small.tex` | B.5 the six small instances | `app:small` |
| `B6-powerflow.tex` | B.6 powerflow | `app:powerflow` |
| `B7-eg.tex` | B.7 eg | `app:eg` |
| `B8-waterno2.tex` | B.8 waterno2 | `app:waterno2` |
| `B9-ann-kan.tex` | B.9 ann_cumene_tanh and KAN | `app:annkan` |
| `B10-split-extras.tex` | B.10 Two explanatory results on splits (round 2; `prop:split-forced`, `prop:split-cellwise-best`) | `app:split-explanatory` |
| `C-points.tex` | C Exactly feasible points | `app:points` |
| `D-literature.tex` | D Prior literature by instance | `app:literature` |
| `E-audit.tex` | E Audit details | `app:audit` |
| `F-eg-rounding.tex` | F Rounding-error analysis for the eg certificates | `app:egrounding` |
| `G-proofs-split.tex` | G Proofs for the split certificates | `app:splitproofs` |
| `H-solvers.tex` | H Solver campaign and the SCIP defect | `app:solvers` |
| `I-reproduction.tex` | I Reproduction guide and claim register | `app:repro` |
| `J-displays.tex` | J Display record (S7.5, a subsection since round 2; its table of unsafe strings is in `artifact/HISTORY.md`) | `app:displays` |

The files `B1`–`B10` start with `\subsection`, so the family sections are
S1.1–S1.10 under the section "Certificates by family" (`B0-families.tex`). Subsections inside other appendices (G.1, G.2, ...) get
labels `app:<appendix-label>-<topic>`, for example `app:splitproofs-bound`.

## 3. Label convention

Form: `<prefix>:<family>-<topic>`, lower case, hyphens only.

| prefix | object | example |
|---|---|---|
| `sec:` / `app:` | main-text / appendix and supplement sections | `sec:split-affine`, `app:camshape` |
| `thm:` | theorem | `thm:lnts-opt` |
| `lem:` | lemma | `lem:split-bound` |
| `prop:` | proposition | `prop:dtoc5-identity` |
| `cor:` | corollary | `cor:dtoc5-attained` |
| `def:` | definition | `def:sem-model` |
| `rem:` | remark | `rem:split-enclosures` |
| `asm:` | assumption | `asm:eg-exp` |
| `hyp:` | tagged hypothesis (H), (H0) | `hyp:audit-display` |
| `obs:` | observation | `obs:scip-propagation` |
| `tab:` | table | `tab:closures` |
| `fig:` | figure | `fig:camshape-profiles` |
| `eq:` | equation | `eq:lnts-g` |
| `box:` | numbered box | `box:glance` |

Family short names: `lnts`, `lukvle10`, `dtoc5`, `optcdeg2`, `camshape`,
`chain`, `catmix`, `ex62` (ex6_2_5 and ex6_2_7), `pricing` (pricing050),
`etamac`, `pindyck`, `hvycrash`, `pf` (powerflow), `eg`, `waterno2`, `ann`,
`kan`. Paper-wide topics: `sem` (Section 2), `split` (Section 4.1 and
Appendix G), `results` (Section 3), `pts` (Section 6 and Appendix C), `audit`,
`spring`, `emfl`, `rocket` (Section 7 and Appendix E), `scip`, `baron`,
`qplib`, `camino`, `minotaur` (Section 8 and Appendix H), `interp` and
`band` (Section 9), `fp` (floating-point hypotheses), `repro`.

Put `\label` directly after `\begin{theorem}` (or after `\caption` in floats).
Certificate boxes are unnumbered; refer to the theorem they belong to.

## 4. Theorem numbering plan

All theorem-like environments share one counter, numbered within sections
(`Theorem 4.6`, `Lemma B.3`). The numbers below are the outline's planned
positions. The printed numbers are automatic and will shift if a writer
adds or drops a numbered environment; a numbered remark or definition, for
example, takes a number from the same counter. Hypotheses carry tags
(H, H0), not numbers. Planned labels:

### Section 2
| outline | label | content |
|---|---|---|
| Definition 2.1 | `def:sem-model` | stored model, reading (b), defaults, domain rule |
| Definition 2.2 | `def:sem-feasible` | F(M), v*(M), ε-feasibility |
| Remark (three readings) | `rem:sem-readings` | readings (a)–(c) and sensitivity facts |
| Definition 2.3 | `def:sem-certificate` | valid dual bound, optimum enclosure, closure, exact optimum |
| Lemma 2.4 | `lem:sem-enclosure` | enclosure lemma; tolerance-feasible point below L is infeasible |
| (removed in r1) | `lem:sem-multiplier` | removed: the multiplier-mass bound is now one sentence after `lem:sem-enclosure` |
| Proposition 2.6 | `prop:sem-refutation` | refutation by an exactly feasible point holds for every tolerance |
| (H0) | `hyp:fp-ieee` | IEEE binary64 hypothesis (Table 1, Appendix F) |

### Section 4
| outline | label | content |
|---|---|---|
| Lemma 4.1 | `lem:split-bound` | split bound (a)–(d) |
| Lemma 4.2 | `lem:split-minorant` | value-function minorants, chord interpolation |
| Proposition 4.3 | `prop:split-affine` | affine splits = Lagrangian dual of the copy formulation |
| Proposition 4.4 | `prop:split-window` | windows |
| Proposition 4.5 | `prop:split-cellwise` | cellwise slopes |
| Remark (derived enclosures) | `rem:split-enclosures` | |
| Theorem 4.6 | `thm:lnts-opt` | lnts exact optimum |
| — its lemma and proposition | `lem:lnts-elim`, `prop:lnts-support` | exact elimination; Cauchy–Schwarz support bound |
| Proposition 4.7 | `prop:dtoc5-identity` | dtoc5 dual identity |
| Theorem 4.8 | `thm:dtoc5-bracket` | dtoc5 bracket |
| Corollary (dtoc5) | `cor:dtoc5-attained` | attainment and minimizer location |
| Theorem 4.9 | `thm:optcdeg2-bound` | optcdeg2 quadratic calibration bound |
| Lemmas B.2.1–B.2.3 | `lem:optcdeg2-krotov`, `lem:optcdeg2-enclosure`, `lem:optcdeg2-stage` | Appendix B.2 |
| Theorem 4.10 | `thm:chain-bound` | chain |
| Appendix B.4 chain lemmas | `lem:chain-polyline`, `lem:chain-summation`, `lem:chain-calibration`, `lem:chain-window`; `prop:chain-weierstrass` (C6) | |
| Theorem 4.11 | `thm:catmix-bound` | catmix |
| Lemmas M1–M6, Proposition M8 | `lem:catmix-<topic>`, `prop:catmix-transport` | Appendix B.4 |
| Theorem 4.12 | `thm:lukvle10-bracket` | lukvle10 |
| Lemma B.1.x | `lem:lukvle10-coercive` | coercive reduction to a box |
| Theorem 4.13 | `thm:waterno2-bounds` | waterno2 dual bounds |
| Appendix B.8 results | `prop:waterno2-lagrangian`, `lem:waterno2-horizon`, `lem:waterno2-reuse`, `lem:waterno2-levels` (B.8.5), `lem:waterno2-bb` (B.8.6) | |

### Section 5
| outline | label | content |
|---|---|---|
| Theorem 5.1 | `thm:camshape-opt` | camshape exact optimum |
| Lemma 5.2 | `lem:camshape-sturm` | discrete Sturm comparison |
| Lemma 5.3 | `lem:camshape-envelope` | min-plus envelope |
| Proposition 5.4 | `prop:camshape-deficit` | tolerance deficit bound D_n(ε) |
| Theorem 5.5 | `thm:ex62-bounds` | ex6_2_5, ex6_2_7 |
| Theorem 5.6 | `thm:pricing-bound` | pricing050 (maximization) |
| Proposition 5.7 | `prop:pf-duality` | weak duality for relaxation R with shift ε |
| Theorem 5.8 | `thm:pf-0030p` | powerflow0030p |
| Lemma 5.9 | `lem:pf-leaf` | leaf identity at bus 30 |
| Lemma 5.10 | `lem:pf-planes` | vertex planes |
| Theorem 5.11 | `thm:pf-0039` | powerflow0039p/r |
| Theorem 5.12 | `thm:etamac-bound` | etamac |
| Theorem 5.13 | `thm:pindyck-bound` | pindyck |
| Corollary (pindyck) | `cor:pindyck-unique` | unique optimizer |
| Proposition 5.14 | `prop:hvycrash-identity` | hvycrash identity and witness |
| Theorem 5.15 | `thm:eg-bounds` | eg_int_s, eg_disc_s, eg_disc2_s |
| Theorem 5.16 | `thm:ann-bound` | ann_cumene_tanh |
| Lemmas A.1–A.5 (ann) | `lem:ann-<topic>` | Appendix B.9 |
| Proposition 5.17 | `prop:kan-infeasible` | exact infeasibility of the six KAN models |
| Theorem 5.18 | `thm:kan-enclosure` | enclosure for R_P (decision D6) |
| Lemma K.3 | `lem:kan-<topic>` | Appendix B.9 |
| fallback A2′ and pow hypothesis (only if the eg audit is incomplete) | `asm:eg-exp`, `asm:eg-pow` | not used: the audit completed |

### Section 6
| outline | label | content |
|---|---|---|
| Theorem 6.1 | `thm:pts-krawczyk` | Krawczyk existence on a square subsystem with fixed coordinates |
| Proposition 6.2 | `prop:pts-exact` | points in Q or Q(√D) |
| Proposition 6.3 | `prop:pts-triangular` | triangular definitions |
| Proposition 6.4 | `prop:pts-lindemann` | no algebraic exactly feasible lnts point |
| Remark (lukvle10 seeds) | `rem:lukvle10-seeds` | |

### Section 7
| outline | label | content |
|---|---|---|
| Hypothesis H | `hyp:audit-display` | display hypothesis |
| Lemma 7.1 | `lem:audit-display` | when H holds |
| Proposition 7.2 | `prop:audit-refute` | class (i) refutation |
| Corollary 7.3 | `cor:audit-tolerance` | refutations hold for every tolerance |
| Proposition 7.4 | `prop:spring-opt` | spring optimum |
| Proposition 7.5 | `prop:emfl-enclosure` | emfl enclosures |

### Section 8
| outline | label | content |
|---|---|---|
| Proposition 8.1 | `prop:baron-camshape` | BARON on camshape100/200 |
| Proposition 8.2 | `prop:qplib-copies` | QPLIB_3177 and QPLIB_2738 |
| Proposition 8.3 | `prop:kan-scip` | published SCIP optima for kan_r3_h1_n4/n5 |
| Proposition 8.4 | `prop:scip-witnesses` | witnesses refuting SCIP's optimal values |
| Proposition 8.5 (in S6.6 since round 2, move M3) | `prop:scip-reproducers` | fm336 and tiny2 |
| Lemma 8.6 (in S6.6 since round 2, move M3) | `lem:scip-cube` | outward enclosure of fl(0.7)^3 lies below fl(0.343) |
| Observation 8.7 | `obs:scip-propagation` | propagation mechanism (evidence) |
| Proposition 8.8 | `prop:camino-eg` | CAMINO Gurobi bounds on eg_* |
| Proposition 8.9 | `prop:minotaur-optcdeg2` | MINOTAUR infeasibility report on QPLIB_8803 |

### Section 9 (only if decision D1 adopts it) and appendices
| outline | label | content |
|---|---|---|
| (removed) | `thm:band-identity` | band theory removed (lead decision 2) |
| (removed) | `prop:band-cells` | band theory removed (lead decision 2) |
| Lemma A1 (eg rounding) | `lem:eg-padding` | Appendix F |

### Tables, figures and boxes

| outline | label |
|---|---|
| Table 1 trust base and verification by family (compact, upright since round 2) | `tab:trust` (generated); full version with data readings and primal constructions `tab:trust-full` (S7.2, generated) |
| funnel table (S3.4) | `tab:results-funnel` |
| Table 2 the 31 closures | `tab:closures` (generated) |
| Table 3 the other 12 instances | `tab:unclosed` |
| Table 4 KAN models | `tab:kan` (generated) |
| Table 5 the 13 formerly tolerance-only closures | `tab:points` (generated) |
| Table 6 audit pairs | `tab:audit-pairs` |
| Table 7 replay tiers (Section 10) | `tab:repro-tiers` |
| Table 8 GAMS and OSIL forms (Appendix A) | `tab:sem-gams` |
| staged certificates (S1) | `tab:staged` (generated) |
| contradicted claims (S6) | `tab:claims` (generated); campaign points `tab:claims-campaign` |
| one-hour campaign (S6) | `tab:solvers` (generated); per-run outcomes `tab:campaign-runs` |
| claim register (S7.3) | `tab:repro-register`; full paths, arguments and expected outputs in `artifact/RUNS.md` |
| unsafe or superseded strings | no label since round 2: the table is in `artifact/HISTORY.md` (former S8 `tab:displays-unsafe`) |
| structure to certificate | none (`tab:structure` is no longer generated) |
| Figure 1 headline gaps | `fig:results-headline` |
| optcdeg2 calibration (S1) | `fig:optcdeg2-calibration` |
| camshape profiles (not placed; its figure and generator were moved out of the build in round 2) | `fig:camshape-profiles` |
| eg enclosures (S1) | `fig:eg-enclosures` |
| audit margins (S4) | `fig:audit-margins` |
| tolerance deficits (S6) | `fig:camshape-deficit` |
| band schematic (removed with the band theory) | `fig:band-schematic` |
| funnel figure (removed; S3.4 keeps the funnel table `tab:results-funnel`) | `fig:results-funnel` |
| audit pipeline figure (Appendix E) | `fig:audit-pipeline` (not made; optional) |
| results at a glance (removed from Section 1) | `box:glance` |
| camshape800 example box (Section 1.1) | `box:camshape800` |
| SCIP defect box (Section 8.2) | `box:scip` |
| KAN worked example (now prose in S1.9, `app:annkan-kan-infeasible`; no box) | `box:kan-example` |

## 5. Macros and environments

Notation (outline section 4); do not introduce competing symbols.

| macro | output | meaning |
|---|---|---|
| `\model`, `\model_I` | 𝓜, 𝓜_I | stored OSIL model |
| `\feas`, `\feas[\model_I]` | 𝓕(𝓜) | exactly feasible set |
| `\vstar(\model)` | v*(𝓜) | optimal value (+∞ if 𝓕 is empty) |
| `\Lcert`, `\Uprim` | L, U | certified dual bound; upper end of the objective enclosure at an exactly feasible point |
| `\gapabs`, `\gaprel` | Δ, δ | Δ = s(U − L); δ = Δ / min(\|L\|, \|U\|) (decision D2) |
| `\sense` | s | +1 minimize, −1 maximize |
| `\reading{b}` | reading (b) | data readings (a) GAMS, (b) OSIL [all claims], (c) binary64 |
| `\arith{E}` | [E] | arithmetic tags E, I, F, L |
| `\evid{stored}` | stored | evidence levels hand, stored, rerun (development/terminology.md) |
| `\trust{fp}` | T-fp | trust-base terms int, fp, mp, read, code, thm |
| `\fl`, `\uround` | fl, **u** | round-to-nearest binary64; unit roundoff 2^−53 |
| `\dunit{s}`, `\dval{s}` | u(s), d(s) | unit of the last displayed digit; rational value of the decimal string s |
| `\Rnet`, `\RP` | 𝓡, 𝓡_P | KAN network relaxation; OSIL model without partition-of-unity rows |
| `\R \Q \Z \N` | ℝ ℚ ℤ ℕ | number sets |
| `\proj \dist \argmin \argmax` | operators | |
| `\sci{3.1}{-9}` | 3.1·10^−9 | works in text and math |
| `\inst{waterno2_06}` | `waterno2_06` | MINLPLib names; no escaping of `_`; breaks only after `_` or `-`; safe in titles and captions |
| `\TODO{...}` | red [TODO: ...] | visible placeholder plus a log warning |
| `\archiveDOI` | red [archive DOI] | archive DOI placeholder (decision D8) |

Theorem-like environments (amsthm, one shared counter): `theorem`, `lemma`,
`proposition`, `corollary` (plain style); `definition`, `assumption`
(definition style); `remark`, `observation` (remark style); `proof`.
Tagged hypotheses: `\begin{hypothesis}{H}[display hypothesis] ... \end{hypothesis}`
prints "Hypothesis H (display hypothesis)." and `\cref` prints "Hypothesis H".

Certificate box (one per theorem; always these six fields in this order, development/terminology.md):

```latex
\begin{certbox}[Certificate for \cref{thm:lnts-opt}]
\certitem{Inputs}{OSIL SHA-256 prefixes ...}
\certitem{Computation}{... ; arithmetic \arith{E}}
\certitem{Data reading}{exact / outward / rounded (development/terminology.md)}
\certitem{Implementations}{which one certifies the displayed value; what the second one certifies}
\certitem{Evidence level}{\evid{hand}+\evid{stored}}
\certitem{Replay}{Tier~1; 17~s}
\end{certbox}
```

Numbered boxes: `\begin{infobox}[label={box:glance}]{Results at a glance} ... \end{infobox}`
prints "Box 1: Results at a glance"; `\cref{box:glance}` prints "Box 1".

Tables use `booktabs` (`\toprule`, `\midrule`, `\bottomrule`), no
vertical rules; long tables use `longtable`. Figures go in `figures/`
(`\graphicspath` is set). Citations: `\citet{key}` ("Halbig et al. (2024)")
and `\citep{key}` ("(Halbig et al., 2024)").

## 6. Bibliography (`references.bib`)

- 147 entries. Keys are KB slugs for every slug in the outline's
  bibliography plan (section 7) and every slug cited in the three
  literature syntheses L1–L3, plus two keys without a KB package:
  - `vigerske2014-minlplib-2`: Vigerske, "MINLPLib 2", MAGO 2014
    proceedings, pp. 137–140 (the outline's "Vigerske 2014"; do not cite
    `haugland2014-the-hardness-of-the-pooling` for it);
  - `zimmerman2011-matpower-steady-state-operations-planning`: the paper
    MATPOWER asks users of its case data to cite (declarations).
- `dolan2004-benchmarking-optimization-software-with-cops` and
  `dolan2004-benchmarking-optimization-software-with-cops-2` are the same
  COPS 3.0 report (two KB packages). Cite only the `-2` key, as the outline
  does; citing both prints the report twice.
- Two Vigerske 2014 entries exist: `vigerske2014-minlplib-2` (the MAGO
  paper) and `vigerske2014-towards-minlplib-2-0` (MINLP 2014 slides);
  natbib prints them as 2014a/2014b.
- Web resources are `@misc` entries with URL and access date: MINLPLib
  site, documentation and instance pages (`vigerske2026-minlplib-a-library-of-mixed`,
  `vigerske2026-minlplib-documentation-database-snapshot-2026`,
  `cache2026-minlplib-pages-for-43-target`), QPLIB
  (`furini2026-qplib-official-solution-point-records`,
  `cache2026-qplib-pages-and-rounded-camshape`), Mittelmann
  (`mittelmann2026-continuous-non-convex-qplib-benchmark`,
  `mittelmann2026-mixed-integer-nonlinear-programming-benchmark`), CAMINO
  data (`ghezzi2026-camino-benchmark-results-for-nonconvex`), Karia et al.
  Zenodo data (`karia2025-karia-et-al-zenodo-default`), Gurobi manual,
  MIPLIB page, COCONUT records, CUTEst/COPS/GLOBALLib/MATPOWER source
  files, the cuOpt issue and the MIPcc26 page. Source bundles drawn from
  several sites (`coconut2026-...`, `library2026-...`, `luksan2026-...`,
  `matpower2026-...`) have a `key` label instead of an invented author.
- Sources that the KB marks as unread (metadata only): `ghaddar2015-...`,
  `hartman1978-...`, `krawczyk1969-...`, `luksan1999-...`,
  `mcdonald1997-glopeq-...`, `mittelmann2026-mixed-integer-nonlinear-programming-benchmark`,
  `robertson2025-...`; `huang2011-...` is a catalogue record. Cite them
  only as the outline allows (origin, or "could not be read").
- Metadata corrected against the KB `references.bib` (checked with
  Crossref, arXiv and the source files on 2026-10-04):
  - authors: `ambrosio2015` (Sven Wiese, Cristiana Bragalli),
    `gleixner2012` (Gleixner, Harald Held, Wei Huang, Vigerske),
    `oustry2022` (Antoine Oustry, Manuel Ruiz), `peyrl2008` (Helfried
    Peyrl), `schweidtmann2019` (Artur M.), `tessier2000` (Stephen R.),
    `najman2021` (Jaromił), `go2026-parabolic` (Alexander Martin),
    `shcherbina0000` (Oleg), `coffrin2014` (Dan Gordon, Paul Scott),
    `ghezzi2026` (Andrea Ghezzi), `karia2025-...-zenodo` (creator Tanuj
    Karia; record title), `chen2016` (author format), Kearfott entries
    unified as "R. Baker Kearfott";
  - titles: `josz2015-certified-moment-relaxation-for-ac` is "Application
    of the moment–SOS approach to global optimization of the OPF problem",
    IEEE TPWRS 30(1):463–470 (2015); `bingane2019-...` is "Tight-and-cheap
    conic relaxation for the AC optimal power flow problem", IEEE TPWRS
    33(6):7181–7188 (2018); `coffrin2014-...` is "NESTA, the NICTA Energy
    System Test Case Archive";
  - published versions cited instead of preprints: `anderson2018`
    (Math. Program. 183:3–39, 2020, five authors), `bertsimas2025`
    (J. Global Optim. 91:1–37, 2025), `tasseff2022` (INFORMS J. Comput.
    36(4):1040–1063, 2024), `mcdonald1995` (Comput. Chem. Eng.
    19(11):1111–1139, 1995);
  - volume, issue, pages or year added or fixed from Crossref (e.g.
    `vigerske2017` is Optim. Methods Softw. 33(3):563–593, 2018;
    `furini2018` is Math. Program. Comput. 11(2):237–265, 2019;
    `chen2016` is vol. 165, 2017).
- The bibliography style is `plainnat` for drafting; titles keep the
  capitalization of the source (double braces). Check: BibTeX on a
  `\nocite{*}` test document read all 147 entries with no warnings.
