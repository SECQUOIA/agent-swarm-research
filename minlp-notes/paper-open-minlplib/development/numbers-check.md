# Numbers consistency check of the full draft (2026-10-04)

Scope: every `.tex` file in `paper-open-minlplib/sections/` and `paper-open-minlplib/tables/`.
Reference: `data/numbers.json` (with `data/check.log`, 672 checks, 0 failed), the dossiers and
critiques, the three adopted reviews, the decision register, and, where a number is not in
`numbers.json`, the raw source it came from (`R/` = `research-20260929/`).
No `.tex` file was edited.

## Method

- Read every section and table file in full.
- Extracted every decimal with 7 or more fractional digits (script) and matched it against
  `numbers.json`; for every number within 1e-7 relative of a certified end, checked the rounding
  direction against the exact end (dual down, primal up, reversed for `pricing050`).
- Checked every `\gapabs`/`\gaprel` display against `numbers.json`.
- Recomputed counts (classes, arithmetic tags, evidence levels, prior codes, branching
  dimensions, audit classes and solver splits, funnel, campaign counts) from `numbers.json`,
  `R/bound-audit/pages.json` and `R/publication/solver-runs/results_table.csv`.
- Recomputed by exact arithmetic a sample of derived numbers (margins, percentages,
  factors, leaf-bound differences, multiplier sums).
- Grepped for every string on the outline's "claims not to make" list (section 8).

## Result in brief

No certified bound, primal value or gap cell in the text or tables differs from `numbers.json`,
and every one is on the safe side. The only bound-like strings on the unsafe side are the ones
that Appendix J lists on purpose, and the `eg_disc_s` level `5.760539610694994` (item 12).
The headline counts agree everywhere they appear: 31 closures; 9 exact optima; 13 formerly
tolerance-only closures; 19 bounds on 15 instances (15 distinct conflicts); 22 bounds on 18
instances with `rocket`; 129 kept runs, 109 finite duals (91 + 18), 0 accepted closures,
5 improvements of the best listed dual; funnel 1,633 / 1,257 / 596 / 360 / 294 / 155 with
29 + 12 + 2 = 43.

The problems below are ordered by severity. "Correct text" is a proposed replacement.

## Problems

### Medium

**1. Wrong factor for summed term ranges (eg).**
- Where: `sections/11-conclusion.tex:151`.
- Wrong text: "interval bounds that add up the ranges of the 97 kernel terms of a row were 15 to 19 times looser at medium box sizes than Taylor models that keep the signed moments".
- Correct text: "interval bounds that add up the ranges of the 97 kernel terms of a row were 44 to 151 times looser at relative box widths 0.1 to 0.003 than Taylor models that keep the signed moments, and still 15 to 19 times looser at widths 0.1 and 0.03 when intersected with a mean-value form".
- Source: `sections/B7-eg.tex:348`; `sections/05-other.tex:467`; `development/dossiers/eg.md` section 3.5 (ratios 3.2, 19, 15, 7.1, 2.9 are for the earlier, mean-value-intersected enclosure). The source comment of section 11 also attributes 15 to 19 to the wrong enclosure.

**2. Listed chain duals stated outside their range.**
- Where: `sections/B4-chain-catmix.tex:31`.
- Wrong text: "ANTIGONE's, between $0.08$ and $0.17$".
- Correct text: "ANTIGONE's, between $0.08$ and $0.18$" (the values are 0.17451499, 0.09367008, 0.08256615, 0.09563835).
- Source: `numbers.json` `instances.chain50.listed.best_dual.value` = 0.17451499; `sections/03-results.tex:117` already says "below 0.18".

**3. Claim for the binary64 reading (c).**
- Where: `sections/A-semantics.tex:184`.
- Wrong text: "It shows that the refuted bounds are invalid also for the binary64 models that the solvers read, under the display hypothesis of \cref{sec:audit-hyp}."
- Correct text: "It suggests that the refutations transfer to the binary64 models that the solvers read; we do not claim this."
- Source: outline section 8, item 2 ("Any claim for reading (c)"); decision register G-01; the paper itself contradicts the sentence at `sections/E-audit.tex:557` ("not a claim of the paper"), `sections/07-audit.tex:75` ("as a check and not as a claim") and `sections/11-conclusion.tex:170` ("plausible ... but it is not proved").

**4. Branching of the remaining closures misdescribed (pindyck).**
- Where: `sections/11-conclusion.tex:189`.
- Wrong text: "branching was absent in 12 closures, at most three-dimensional in 15 more, and confined to the original variables in the rest".
- Correct text: "branching was absent in 12 closures, at most three-dimensional in 15 more, and small (\inst{pindyck}, 9 boxes in 112 per-period quantities) or confined to the 7 original variables (\inst{eg}) in the rest".
- Source: `sections/09-interpretation.tex:88-91,142-144`; `tables/tab-structure.tex:81` ("9 boxes in 112 dimensions"); outline section 8, item 8 ("That branching was always low-dimensional (pindyck, eg)").

**5. Unconditional claim that no affine split can be exact on optcdeg2.**
- Where: `sections/04-split.tex:145`; `sections/09-interpretation.tex:49-52`.
- Wrong text (04): "affine where an exact or nearly exact affine split exists (\inst{lnts}, \inst{dtoc5}, \inst{lukvle10}), and richer where it does not (\inst{optcdeg2}, \inst{chain}, \inst{catmix})". Wrong text (09): "Where an affine split cannot be exact, the certificate uses a richer split class (quadratic for \inst{optcdeg2}, ...".
- Correct text (04): "affine where an exact or nearly exact affine split was found (...), and richer where the affine splits we tried were not (...)". Correct text (09): "Where the affine split we tried was not exact (for \inst{optcdeg2}, the costate-affine split; \cref{prop:split-affine}(c) ties exact affine slopes to the costates only under its hypotheses), the certificate uses a richer split class ...".
- Source: outline section 8, item 8 ("That no affine split can be exact on optcdeg2 (without hypotheses)"); what is shown is only that the costate-affine split is not exact (`sections/B2-dtoc5-optcdeg2.tex:12,262-265`) plus a floating-point screening loss of 0.6258 (`sections/04-split.tex:353`).

### Low

**6. Displays of the displayed-dual "second implementation" count omit pindyck.**
- Where: `sections/01-introduction.tex:66` ("in four families, a slightly weaker one"); `sections/02-semantics.tex:269` ("among them \inst{lukvle10}, \inst{optcdeg2}, \inst{catmix} and \inst{etamac}"); `sections/11-conclusion.tex:165` ("The displayed dual bounds of \inst{optcdeg2}, \inst{lukvle10}, \inst{etamac} and the \inst{catmix} instances rest on one certifying implementation each").
- Correct text: add \inst{pindyck} ("in five families"; "... \inst{etamac}, \inst{pindyck} and the \inst{catmix} instances ..."), or state why pindyck is excluded. 02:269 says "several ... among them", the other two say exactly four.
- Source: `sections/B5-small.tex:586-587,619` and `tab:small-verification` (line 645): the displayed bound comes from the verifier's enclosures alone; the authors' enclosures give only $\gapabs<\sci{6}{-29}$, a slightly weaker bound.

**7. pindyck dual trust base understated.**
- Where: `sections/02-semantics.tex:257` ("for one constant of the \inst{pindyck} concavity proof"); `sections/11-conclusion.tex:162` ("of the \inst{pindyck} concavity proof").
- Correct text: "for the \inst{pindyck} concavity proof and the enclosures of $J(p^*)$ and $\|g\|^2$ that enter its bound".
- Source: `sections/B5-small.tex:572-577,613,617`: $\Lcert=-J^+-\|g\|^2/(2\mu)$ uses the verifier's mpmath interval-Newton enclosures; `tab-closures` gives the dual arithmetic "F+I" and `03-results.tex:110` counts pindyck under mpmath.

**8. Stage loss displayed larger than the total.**
- Where: `sections/B2-dtoc5-optcdeg2.tex:297-298`.
- Wrong text: "the differences sum to $8.978\cdot10^{-16}$ ... Stage 3091 accounts for \sci{8.98}{-16}".
- Correct text: "Stage 3091 accounts for about \sci{8.9777}{-16}" (or "almost all of it").
- Source: `development/dossiers/dtoc5-optcdeg2.critique.md:70-73` (stage 3091: 8.9777e-16; stage 47290: 4.0776e-20; others at most 7.2e-25); `numbers.json` `optcdeg2.gap_abs.exact_decimal` = 8.9781e-16.

**9. "At most" bound rounded down.**
- Where: `sections/E-audit.tex:556`.
- Wrong text: "changed by at most $2.1\cdot10^{-10}$ (\inst{nd_netgen-2000-3-4-b-a-ns_7})".
- Correct text: "changed by at most $2.13\cdot10^{-10}$".
- Source: `sections/A-semantics.tex:182` ("at most \sci{2.13}{-10} in absolute terms").

**10. Solver dual bounds quoted rounded toward the wrong side or as truncated gaps.**
- Where and wrong text:
  - `sections/09-interpretation.tex:105-106`: "range from $-1673.2$ to $-36.2$" (GUROBI on chain50 returned −36.24364053; −36.2 lies above it).
  - `sections/09-interpretation.tex:119-120`: "stopped 5.7\% short of the optimum" (exact 5.715%).
  - `sections/09-interpretation.tex:133`: "$41{,}618.5$ rectangular" (GUROBI on powerflow0039r returned 41618.4939762).
  - `sections/B4-chain-catmix.tex:31-32`: "between $-37.1$ and $-286.8$" (−286.8087 lies outside) and "between $-36$ and $-1673$" (−1673.16 lies outside).
- Correct text: "$-1673.2$ to $-36.3$" (or "about $-1673$ to $-36$"); "5.8\% short" (or "about 5.7\%"); "$41{,}618.4$"; "between about $-37.1$ and $-286.81$"; "between about $-36$ and $-1673$".
- Source: `R/publication/solver-runs/results_table.csv` (dual column); `development/dossiers/pattern-theory.md:942` ("5.71% gap"); display rules of `sections/02-semantics.tex:213-217` and the style guide ("Never round a bound to nearest"). These are solver outputs, not certified claims, so the risk is presentational.

**11. fct footnote inconsistent with Appendix D.**
- Where: `sections/03-results.tex:65`.
- Wrong text: "it would pass the next two steps, raising the fifth row to 295".
- Correct text: "it would pass the next two steps, raising the fourth and fifth rows to 361 and 295".
- Source: `sections/D-literature.tex:253` ("it would add one instance to the 360 and the 294"); `development/dossiers/pattern-theory.md:87` (295).

**12. String that numbers.json says not to print.**
- Where: `sections/05-other.tex:454` ("against the decimal levels ..., $5.760539610694994$ and ...") and `:464` ("the binary64 number just below $5.760539610694994$").
- Problem: `numbers.json` `instances.eg_disc_s.note` = "do not print 5.760539610694994 (eg_disc_s)"; outline section 8, item 5 ("5.760539610694994: use …993"); register N-34 deleted the paragraph that explained the …994 versus binary64 issue. Printing it as the re-certifier's level is defensible (`sections/B7-eg.tex:297`, `sections/F-eg-rounding.tex:412-421`, `J-displays.tex:65`), but a reader can take it for a bound.
- Correct text (454): "against the targets $\theta^*_I$ (equal to the displayed bounds for \inst{eg_int_s} and \inst{eg_disc2_s}, and $10^{-15}$ above it for \inst{eg_disc_s})"; (464): "For \inst{eg_disc_s} it certifies only a binary64 number slightly below that target, hence our display."

**13. "Up to 1.1e6 leaves" understates the maximum.**
- Where: `tables/tab-structure.tex:83` (generated by `data/make_tables.py`); `sections/09-interpretation.tex:90-91`.
- Wrong text: "up to $1.1\cdot10^6$ leaves".
- Correct text: "up to $1.12\cdot10^6$ leaves" (or "about $1.1\cdot10^6$").
- Source: `sections/B7-eg.tex:322` and `05-other.tex:454`: 1,114,361 leaves for `eg_disc2_s`.

**14. Run times quoted inconsistently.**
- `ann_cumene_tanh` re-certification: `sections/05-other.tex:517` and `sections/B9-ann-kan.tex:155,170` say "about 2.6 CPU-hours"; `sections/10-reproducibility.tex:81` says "1.2 h on two processes (2.0 CPU-hours)" (source comment: user times 5,234 + 1,159 + 924 s = 2.03 h). State which run each figure belongs to, or use one figure.
- `powerflow0030p` replay: `sections/05-other.tex:290` says "under 1~s"; `sections/10-reproducibility.tex:67` and `sections/I-reproduction.tex:135` say "4\,s".
- Source: `sections/10-reproducibility.tex:2-13,45` (times are not in `numbers.json`; section 10 admits that boxes quote other runs). Low risk, but a referee will notice the 2.6 versus 2.0.

**15. Ambiguous antecedent for the count 110.**
- Where: `sections/07-audit.tex:16-17`.
- Wrong text: "... and 131 (instance, solver) pairs. In 110 of them the point is listed under ``other points''".
- Correct text: "In 110 of the 158 pairs the point is listed under ``other points''".
- Source: `development/dossiers/audit.md:717` ("158 / 46 / 56 / 131; 110 pairs from 'other points'"); `audit.critique.md:31`.

**16. Exact CAMINO percentages misquoted in Appendix J.**
- Where: `sections/J-displays.tex:81`.
- Wrong text: "the last two exceed the exact $7.48\%$ and $80.6\%$".
- Correct text: "the last two exceed the exact $7.487\ldots\%$ and $80.598\ldots\%$". (80.6% is a round-to-nearest of 80.598% and would itself be unsafe as an "at least" margin; the register's N-38 "80.6%" has the same flaw. The paper's own displays, 4.33/7.48/80.5% at `08-solvers.tex:160` and 4.3/7.4/80% at `01-introduction.tex:134`, are correct floors.)
- Source: exact recomputation from `08-solvers.tex:159` values and `numbers.json` U values: 4.3352%, 7.4870%, 80.5977%.

**17. "Independent review" without the paper's defined term.**
- Where: `sections/05-other.tex:574` ("An independent review reproduced ... Points re-proved by an independent review"); `sections/I-reproduction.tex:234` ("An independent review reran ..."); `sections/B1-lnts-lukvle10.tex:149` ("two independent existence proofs"); `sections/B5-small.tex:233` ("An independent check").
- Correct text: "a separate review" / "separately written" (the terms defined in `sections/02-semantics.tex:266-279`).
- Source: outline section 8, item 10 ("'Independent' without the definition and the AI-agent disclosure"; "Independently reviewed by humans, unless true"); with decision D7 there is no disclosure to point to.

**18. Off-by-one exponent.**
- Where: `sections/06-points.tex:98`.
- Wrong text: "seed errors grow by a factor of about $2.73^{999}\approx10^{436}$".
- Correct text: "$2.73^{998}\approx10^{435}$" (rows 0–997 apply the recurrence 998 times; `2.73^998 = 10^435.4`).
- Source: `development/dossiers/lnts-lukvle10.md:126` ("2.73^998 ≈ 1e436"); `sections/B1-lnts-lukvle10.tex:216` (2.73 per step).

## Checked and consistent (no action)

- Every L, U, Δ and δ display in `tab-closures`, `tab-unclosed`, `tab-kan`, `tab-points-all` and in the running text (theorems 4.x, 5.x, B.x) equals `numbers.json` and is on the safe side, including the 44-decimal dtoc5 bracket, the 30-decimal pindyck bracket, the 25-decimal ex6_2_5 ends and the lnts 40-decimal enclosures.
- Chain gaps 9.58e-15 / 1.01e-14 / 9.34e-15 / 9.78e-15 follow `numbers.json` (exact ends), not the display-based 9.62e-15 / 9.41e-15 of register N-13/N-15; both are valid.
- Margins: 4.30e-11 (lnts50 p1), 5.25e-7 and 2.05e-6 (BARON; the outline's 5.26e-7 was unsafe), 1.23e-7 / 4.80e-7, 1.70e-3 / 2.03e-3 (KAN), 1.45 (optcdeg2 p2), 1.02e-3 (lukvle10 SOLTN), 3.162e-3 / 1.552e-4 (QPLIB), 8.15e-6 / 3.27e-5 (camshape p2), rocket 1.06e-7 / 4.70e-8 / 1.89e-7, emfl 1.41e-5 / 1.98e-3 / 2.92e-4 / 6.86e-6, CAMINO 0.2445944 / 0.4312902 / 5.2010558, KAN rerun margins in `tab:kan-rerun`.
- Counts: classes A 15, A' 4, B 3, C 5, D 1, E 3; dual arithmetic 14 E, 9 I, 7 F, 1 F+I; 10 closures at level S; prior codes 4 F + 3 f, 2 Lst + 3 T + 1 K + 2 U, 16 N (7 + 8 + 16 = 31); branching 12 / 6 / 7 / 2 plus pindyck and eg; "12 of the 31 closures" with listed dual below U by more than |U|/2; audit tables `tab:audit-classes` and `tab:audit-solvers` (row and column sums, per-solver bound counts against `pages.json`); campaign table against `numbers.json` `campaign`.
- Derived numbers recomputed: waterno2 factors and percent gaps, ann 0.195% / 0.194%, camshape listed gaps 1.22e-6 / 8.27% / 16.31% / 19.93%, QPLIB shifts, powerflow leaf-bound differences 3.0e-3 / 2.6e-5, pricing050 multiplier sums, ex6_2 λᵀb, eg leaf and audit totals (1,234,542 leaves; 63,017,129,222 audited values; 16,703 s), waterno2 cell-pair counts (117,736 = 79,919 + 37,817), ann covering (1,644,110 + 208,223 = 1,852,333).
- Outline section 8 strings: none of the unsafe displays of item 11 appears outside Appendix J; no "first" without qualifier, no "zero duality gap", no "reported upstream", no "1.67%", "6.22", "7.2e-43", "600-fold", "3.73e-10", "16.01%" or "4.3/7.5/81%" in the main text.
