# Review round 2: writing, structure and presentation

Manuscript: "Certified support cuts for shared nonlinear expressions and quadratic blocks"
(main.pdf of 2026-10-03 19:12; identical to development/draft-round2/main.pdf, and the
snapshot sources match sections/ exactly).

## Overall assessment

The paper reads well. The prose is mostly plain and precise, actors and actions are clear,
section openings state their purpose, and there is little filler: no "notably", "crucially",
"delve" or similar, and only a handful of informal phrases. The theory sections (2-6) are
well ordered, and each result is placed against prior work. The round-1 writing problems
(post hoc labeling, campaign-1 exception, conclusions that contradicted Section 9, notation
overload in the old Section 7) have mostly been fixed.

The remaining problems are concentrated where an expert is most likely to lose the thread:

1. Two summary claims in the introduction and Section 9 say more than the data show. One
   says the whole-row direction is necessary, which Part C4 and Table 5 contradict. The
   other attributes the sample minimum's 38% error rate to local minimization too.
2. The abstract misstates the star bound (it omits m_0), lists only two of the four validity
   conditions, and does not say that the path families are constructed or that the winning
   configuration was chosen after a diagnostic on earlier instances.
3. The names of modes, limits and parts are hard to follow in Section 8 and the tables.
   "mech."/"mechanism limits" is never defined, "frozen" has three meanings, each mode has
   three or four names, "rem." means different modes in two halves of Table 12, and "Part D"
   can be confused with Part 3D.
4. "Remainder" means the affine part in Section 5 and the nonlinear part in Sections 6-8,
   which collides with the key experimental term "remainder directions".
5. The paragraph that attributes the path-family result (Section 8.5) is the crux of the
   computational story, and it is the hardest paragraph in the paper to follow.

The abstract has 250 words by my count (math tokens counted as one word), exactly at JOGO's
limit, so any addition must be paid for elsewhere. A rewrite of 250 words is given below.

## Checks run (targeted, read-only on the manuscript)

- Read the whole typeset text (development/draft-round2/main.txt, 56 pages) and the
  corresponding sources.
- `diff -rq sections development/draft-round2/sections` and `cmp main.pdf
  development/draft-round2/main.pdf`: the text snapshot and current source agree.
- Rendered pages 8, 21, 24 and 29 with `pdftoppm` (temporary directory from `mktemp -d`) to
  inspect Figures 1-2 and Tables 1, 2, 5.
- Wrote and ran `verification/R9_writing_sentences.py` (abstract word count; sentence
  lengths per file; longest sentences with file:line). Result: abstract 250 words;
  06-certification has 9 sentences above 50 words, 08e-path 7; longest sentence 79 words
  (08c-minlplib.tex:12-20).
- grep counts of terminology variants (remainder, frozen, mech., rowdir, extra, glued,
  pair-hull level, block closure, support value/cut/inequality, Part labels).
- Read experiments/v3/runs/partA-full, partA-root and partB records.jsonl for the objective
  sense (syn05m, pointpack02 and pointpack04 are maximization models).
- Checked experiments/v4/README.md and experiments/campaign-v4-protocol.md: path-family root
  runs were SCIP modes only; Gurobi had full runs only.
- Read evidence/campaign4-c4-digest.md section (c) for C4 solved counts.
- Read SCIP 10.0.3 source cons_nonlinear.c (isSingleLockedCand, presolveSingleLockedVars) and
  the checkvarlocks parameter description from PySCIPOpt 6.2.1 (no solve).

No SCIP or Gurobi solve was run. No project-wide test or CI check was run.

---

## [major] W1. The introduction and Section 9 say the whole-row direction is necessary; the data say otherwise

**Location.** sections/01b-results.tex:14-17 (PDF p. 3, Section 1);
sections/09-conclusions.tex:30-33 (PDF p. 32, Section 9).

**Issue.** Introduction: "A post hoc diagnostic, confirmed by a later prospective control,
showed that the separator closes the gap beyond that level only if it may add enough cuts per
block and tries the exact support of each whole row first." Section 9: "They did so only with
the exact support of each whole row as a first direction, enough cuts per block, and, when a
coupling row binds, a direction search that finds sloped cuts." Both state a necessity that
the paper's own results contradict:

- Part C4 (binding row): the remainder directions with wide limits (`frozen-wide`) closed a
  median of 93-98% of SCIP's root gap and solved all 20 instances (Table 5, p. 29; Table 12,
  p. 56; Section 8.5, 08e-path.tex:143-148). The whole-row direction was not needed there.
- Campaign-3 instances: the remainder directions with wide limits were "above [the pair-hull
  level] on 7 of the 20 instances" (08e-path.tex:121-122), so going beyond that level does not
  require whole-row directions either.

What the data support is weaker: the wide limits account for most of the closure, and on the
non-binding family the whole-row directions supplied most of the rest and raised the solved
count from 13 to 20. Section 8.5 itself says this (08e-path.tex:126-127).

**Fix.** Introduction (01b-results.tex:14-17), replace the sentence with: "A post hoc
diagnostic, completed by a prospective run of the missing configuration, showed that most of
this closure requires allowing more cuts per block, and that trying the exact support of each
whole row first supplies most of the rest when the coupling row does not bind." Section 9:
see the rewrite of the second paragraph in W13, which states the same thing.

---

## [major] W2. The 38% error rate of the sample minimum is attributed to local minimization as well

**Location.** sections/01b-results.tex:5-7 (PDF p. 3); sections/09-conclusions.tex:17-20
(PDF p. 31).

**Issue.** Introduction: "Constants computed without a certificate, from samples or from a
local solver, would have been wrong for 38% of the cuts on MINLPLib models and for nearly all
cuts on the path family". Section 9: "constants taken from samples or from a local solver were
wrong for a large share of the cuts". Table 2 (p. 24) shows that 38% and "nearly all" are the
rates for the sample minimum U1 (1,969/5,116 = 38.5%; 976/1,000). With local minimization (U2)
the rates are 230/5,116 = 4.5% and 73/1,000 = 7.3%. An expert reading the introduction would
conclude that a local solver is wrong 38% of the time, which overstates the case. The correct
and still strong point is that even U2 left wrong constants that cut off feasible solutions
(132 rows on 2 MINLPLib models; 13 sampled path-family rows cut off the known optimum).

**Fix.** Introduction: "Constants taken from the sample minimum would have been wrong for 38%
of the cuts on MINLPLib models and for almost all sampled cuts on the path family; local
minimization lowered these shares to 4.5% and 7.3%, but the remaining wrong constants still
cut off feasible solutions, including known optima." Section 9: see W13.

---

## [major] W3. The abstract misstates the star bound, the validity conditions and the status of the path-family result

**Location.** sections/00-abstract.tex:1-21 (PDF p. 1).

**Issue.**
1. "an exact rational support algorithm with O((m+k)log(m+k)) operations": Theorem 4.4
   (p. 13) and the introduction (01-introduction.tex:65) give O(m_0 + (m+k)log(m+k)). Without
   m_0 the bound is false for domains with many rows in the center alone (round 1 raised this;
   the introduction was fixed, the abstract was not).
2. "valid as stored if a lower bound is certified for the exact binary64 direction and the
   stored row is checked": Section 6.1 needs four conditions (C1-C4); exact elimination and
   bound-corrected rounding are missing, so the stated condition is not sufficient.
3. "a configuration fixed in advance solved all instances": true for the 40 fresh instances,
   but the configuration was chosen after a post hoc diagnostic on the campaign-3 instances
   (Section 8.5). The abstract also calls the families "path-structured" without saying they
   were constructed to have the structure that favors block cuts (Section 8.5, 08e-path.tex:
   164-171). Round 1 asked for the post hoc status to be visible in the abstract.
4. "changed neither which models SCIP solved nor its own solving time": "its own solving
   time" can be read as total time. The runs were slower (median per-run factors 1.3-2.7,
   Table 3); the introduction says so, the abstract does not.
5. δ, "the trivial bound", "interface", "local zero sets" and "do not compose" are not defined
   for an abstract reader; "Support cuts ... recover it" has an unclear antecedent ("it" =
   "their dependence").

**Fix.** Replace the abstract with (250 words by the same count as the original):

> Global solvers for nonconvex mixed-integer nonlinear programs relax nonlinear expressions
> one at a time and lose the dependence of expressions that share variables. Support cuts of
> the convex hull of their joint graph keep it. We study when such cuts add strength, how to
> compute them exactly, and how to keep them valid as stored. Gluing exact pair hulls on
> shared moments loses strength: on a three-variable path, for a family of quadratic
> directions, the glued relaxation misses either nothing or $\delta^2/2$, where $\delta$ is
> the distance between two point sets, depending on whether they interleave; an interface
> that shares $\kappa$ moments gives no positive bound exactly when the local zero sets
> alternate at least $\kappa+1$ times. For quadratic stars with $k$ leaves, $m$ center--leaf
> rows and $m_0$ rows in the center alone, we give an exact rational support algorithm with
> $O(m_0+(m+k)\log(m+k))$ operations. Eliminating the model rows exactly gives cuts in the
> original variables; a stored cut is valid if its bound is certified for the exact binary64
> direction, rounding is corrected, and the stored row is checked. All 143,267 recorded SCIP
> cuts passed replay, whereas sample-based constants would have cut off feasible solutions.
> On MINLPLib models the cuts changed neither which models SCIP solved nor SCIP's own solving
> time, the Python separator slowed the runs, and SCIP's disabled-by-default separators were
> stronger. On 40 fresh instances of constructed path families, a configuration chosen on
> earlier instances solved all 40 within 300 seconds, against 19 for SCIP and 11 for Gurobi.

If the journal counts math differently and the text is over the limit, drop "for a family of
quadratic directions,".

---

## [major] W4. Mode, limit and configuration names: one concept, three or four names, and two undefined terms

**Location.** sections/08a-setup.tex:52-76 (Table 1, p. 24); 08d-funnel.tex:29-33 (Table 4,
p. 27); 08e-path.tex:45-79 (Table 5, p. 29), 101-139 (pp. 29-30); 08c-minlplib.tex:10, 128
(pp. 25-27); 08g-summary.tex:22 (p. 31); 07-implementation.tex:129-131 (p. 22);
A-instances.tex:5, 44-62 (Table 7, p. 51); B-tables.tex:142 (Table 11, p. 55), 171-200
(Table 12, p. 56).

**Issue.** Section 8 and the tables are where a referee checks the headline result, and the
names change from place to place:

| Concept | Names used |
|---|---|
| SCIP with the concavity presolve step off | `baseline-novarlocks` (Table 7), "checkvarlocks off" (Table 1), "SCIP, checkvarlocks off" (Table 5), "SCIP locks off" (Table 11) |
| SCIP with its optional nonconvex separators on | `baseline-extra`, "extra", "SCIP, disabled separators on", "SCIP with its disabled separators" |
| campaign-3 path separator | `all-diag-mech`, "remainder, mech.", "remainder, mech. limits", "the separator with remainder directions and mechanism limits", "rem." |
| remainder + wide limits | `frozen-wide`, "remainder, wide", "remainder, wide limits", "rem." |
| whole row + wide limits | `rowdir-wide`, "whole row, wide", "the whole-row variant with wide limits" |
| whole row + campaign-3 limits | "whole-row variant" (Table 1), "whole row, mech. (post hoc)"; no mode name in Table 7 |

Specific problems:
- "mech." and "mechanism limits" are never defined. Table 5's caption says they "are the
  limits of Table 7", but Table 7 has no "mech." column, only the row `all-diag-mech`. The
  word comes from the internal protocol name (mechanism-protocol.md). Section 3.3 uses
  "mechanism" in its ordinary sense ("The same mechanism defeats any interface", 03-composition.
  tex:158), and Appendix F uses "mechanism cases" for something else.
- "frozen" has three meanings: the limits of modes all/auto ("frozen limits", 08c:10,
  08g:22, A-instances.tex:5), the campaign-3 code ("frozen separator", 08c:128; "frozen code",
  A-campaigns12.tex:66), and the remainder directions (`frozen-wide`, whose contrast is
  `rowdir-wide`). It is never defined; Section 8 defines "prospective" instead.
- "SCIP with its disabled separators solved 22" (01b-results.tex:21) reads as the opposite of
  what is meant.
- In Table 12, the column "rem." is `all-diag-mech` for the C3 rows and `frozen-wide` for the
  C4 rows. A reader comparing down the column compares different configurations.

**Fix.** Use one descriptive scheme in the text and all tables, and keep code names only in
Table 7 as a mapping:

| Table 7 code name | Name in text and tables |
|---|---|
| `baseline` | SCIP |
| `baseline-novarlocks` | SCIP-nolocks |
| `baseline-extra` | SCIP-extra |
| `all`, `auto` | all, auto (default limits) |
| `all-diag`, `all-diag-rowdir` | all, raised limits; all, raised limits, whole row |
| `all-diag-mech` | remainder, base limits |
| (none; Part 3D) | whole row, base limits (add this row to Table 7) |
| `frozen-wide` | remainder, wide limits |
| `rowdir-wide` | whole row, wide limits |

Define the two path-family limit sets once, in Section 7.2 or at the start of Section 8.5:
"For the path family we use limits proportional to the number of copies $n$: base limits ($n$
blocks, $4n$ cuts, $n$ per callback, $20n$ support calls) and wide limits ($16n$ cuts, $4n$ per
callback, $40n$ support calls)." Define SCIP-extra once in Section 8.1: "SCIP-extra is SCIP
with its disabled-by-default nonconvex separators switched on (Table 7)." Replace "frozen
limits" with "default limits" and "frozen separator" with "the separator with default
limits"; keep "frozen" only for code snapshots (99-availability.tex:5) or drop it. Split the
"rem." column of Table 12 into two labeled columns, or head the C3 and C4 blocks with the
configuration name.

---

## [major] W5. "Remainder" means the affine part in Section 5 and the nonlinear part in Sections 6-8

**Location.** sections/05-original.tex:24, 99, 186, 188, 210-211 (PDF pp. 15-17);
06-certification.tex:78 (p. 19); 07-implementation.tex:79-95, 131 (pp. 22); Section 8 and
Tables 4, 5, 7, 11, 12.

**Issue.** Section 5 writes the rows as $g(Sv)+Av\le b$ "with ... affine remainders $Av$" and
names Proposition 5.5 "Free remainders" (the free affine columns). Sections 6.2 and 7.2 use
"remainder" for the nonlinear part: "polynomial remainders in one or two variables", "writes
each finite side ... exactly as a nonlinear remainder plus an affine part". Section 8 then
builds its main comparison on "remainder directions" ($a=0$, $\lambda=e_j$, which bound only
the nonlinear part). A reader who has absorbed Section 5's "affine remainders" will read
"remainder directions" as directions on the affine part, the opposite of what is meant.

**Fix.** Keep "remainder" for the nonlinear part (Sections 6-8) and rename Section 5's term:
05-original.tex:24 "with $g:D\to\R^m$ and affine parts $Av$ that may involve any variables";
line 99 "nonlinear rows and affine parts on arbitrary variables"; line 186 "Equality holds when
every row has its own free direction in the affine parts."; Proposition 5.5 title "Free affine
columns"; lines 210-211 "covered by Proposition 5.5. Without free affine columns the gap can be
strict." Then define the nonlinear remainder at its first use in Section 6.2 (06-certification.
tex:78): "For polynomial remainders (the nonlinear part of a row, Section 7.2) in one or two
variables ...".

---

## [major] W6. The attribution paragraph of Section 8.5 is the crux of the computational story and is hard to follow

**Location.** sections/08e-path.tex:101-127 (PDF p. 29, Section 8.5, "The prospective
separator and the attribution").

**Issue.** This 27-line paragraph carries the paper's most delicate claim: which results are
prospective, which are post hoc, and what each change contributed. Problems:
- "A post hoc diagnostic, designed after these results and reported separately" — "reported
  separately" does not say where (it is Part 3D in Table 1).
- "tried the whole-row direction first, with the same limits and with four times as many cuts
  per callback and in total and twice as many support calls" — two runs are described in one
  clause; the reader cannot tell that "the same limits" and "four times as many" are two
  configurations.
- "Before it, we had checked the wide limits by hand on two of the 20 instances" is a needed
  disclosure, but it interrupts the description of the diagnostic.
- The fact that the $n$ cuts $t_i\ge\min\Phi^{(i)}$ give the optimum is repeated from the
  previous page.
- The load argument ("the four additional instances were solved in 9 to 168 s") does not
  bear on the conclusion; the cut-cap argument does.

**Fix.** Replace the paragraph with:

> **The prospective separator and the attribution.** The campaign-3 separator (remainder
> directions, base limits) improved the root bound on all 20 instances but closed only a
> median of 19-35% of the root gap, less than the pair-hull level. It solved the same 9
> instances as SCIP, with fewer nodes and a shifted geometric mean time of 6.7 s instead of
> 10.3 s. After seeing these results we identified two limitations. First, the first
> directions bound only the nonlinear remainder of a row (Section 7.2), whereas the support
> of the whole row is the block minimum. Second, the first blocks of a callback take up to
> four cuts each, so with $n$ cuts per callback the later blocks receive none. A post hoc
> diagnostic (Part 3D) tried whole-row directions first, once with base limits and once with
> wide limits; we had tried the wide limits by hand on two of the 20 instances before. With
> base limits, whole-row directions raised the median closure to 43-46% and solved 10
> instances; with wide limits they closed the root gap on all 20 instances and solved all 20,
> 12 at the root node. Campaign 4 ran the remaining combination prospectively: remainder
> directions with wide limits closed 86-90%, close to the pair-hull level and above it on 7
> of the 20 instances, and solved 13. Every run of these four configurations stopped at its
> cut cap, so the root bounds do not depend on the host load, which was lower in campaign 4.
> The wide limits therefore account for most of the closure; the whole-row directions supply
> most of the rest and raise the solved count from 13 to 20.

Consider also adding a "Part" column (3C, 3D, 4C2) to Table 5 so the 2 x 2 design is visible
there (see W9).

---

## [major] W7. Section 8.5 claims a root-bound comparison with Gurobi that was not measured

**Location.** sections/08e-path.tex:166-168 (PDF p. 30, last paragraph of Section 8.5).

**Issue.** "They show that exact block support supplies strength that neither SCIP, with or
without its disabled separators, nor Gurobi obtains at the root". The path-family root runs
were SCIP modes only; Gurobi had only full 300-second runs (experiments/v4/README.md lines
105, 111; experiments/campaign-v4-protocol.md:110). Table 5 and Tables 11-12 accordingly show
no Gurobi root values. The claim about Gurobi's root bound is therefore unsupported. What is
supported: Gurobi solved 5-7 of 20 instances per set, and its final gap on $n\ge40$ was 53-121%.

**Fix.** "On these families, exact block support supplied root strength that SCIP did not
obtain with or without its disabled-by-default separators, and the separator solved instances
that neither SCIP nor Gurobi solved within 300 s. This strength reached the solver only when
the separator could add enough cuts per block in useful directions. The families are not
evidence about other models."

---

## [minor] W8. Part labels collide ("Part D" vs 3D, "C4" vs campaign 4) and the text drops the campaign prefix

**Location.** sections/08a-setup.tex:52-76 (Table 1, p. 24); 08b-validity.tex:8, 48;
08c-minlplib.tex:12-20, 82, 112; 08d-funnel.tex:46, 56; 08e-path.tex:27, 31, 141;
B-tables.tex:135, 171, 200; A-instances-D.tex.

**Issue.** Table 1 labels parts 3A-3D and 4C2, 4C3, 4C4, 4B2, 4D, 4U, 4S. The text writes
"Part D" for 4D (the larger models), while Table 1's "3D" is the post hoc diagnostic; "Part
C4" (the binding-row variant) reads like "campaign 4"; "B2", "C2", "C3", "C4" suggest missing
parts B1, C1; "protocol Part U" and "Part S" drop the prefix. A reader who meets "Part D" on
p. 25 has just seen "3D (post hoc)" in Table 1.

**Fix.** Use the Table 1 labels verbatim everywhere ("Part 4D", "Part 4C4", "Part 4U",
"Part 4S"), and rename 3D to 3P (post hoc) so that no label is a suffix of another. Better,
use short descriptive labels: 4C2 -> 4C-rerun, 4C3 -> 4C-fresh, 4C4 -> 4C-binding,
4B2 -> 4B-noaggr, 4D -> 4D-large.

---

## [minor] W9. Table 5 does not show where each row comes from, and several cells are unexplained

**Location.** sections/08e-path.tex:43-82 (Table 5, PDF p. 29).

**Issue.**
- Only some rows carry provenance ("(campaign 3)", "(post hoc)"). The rows "SCIP,
  checkvarlocks off", "SCIP, disabled separators on", "Gurobi" and "remainder, wide" for
  seeds 0-4 come from Part 4C2 (campaign 4), which the table does not say.
- "SCIP default" shows "---" where the closure is 0 by definition; "Gurobi" rows have blank
  closure cells because Gurobi had no root runs. Neither is explained.
- The binding-row block lacks its own reference row. Section 8.5 says "the reference that
  matters is the best root bound that cuts on the blocks can give" (08e-path.tex:149-151), but
  this bound appears only in Table 12 as a difference column.
- Decimals: 0.997 in one cell, two decimals elsewhere.

**Fix.** Add a column "Part" (3C, 3P, 4C2, 4C3, 4C4). Add to the caption: "SCIP default
closes 0 by definition. Gurobi had no root runs." Add a row "block closure (exact)" to the
binding-row block with its median closure. Use three decimals in the binding-row block, or
write 1.00 with a footnote "0.997".

---

## [minor] W10. Appendix tables: a dangling label, a missing objective sense, unexplained symbols

**Location.** B-tables.tex:171-176 (Table 12, p. 56); B-tables.tex Tables 8-9 (pp. 52-53);
08b-validity.tex:22-44 (Table 2, p. 24); 08a-setup.tex:54-57 (Table 1 caption, p. 24).

**Issue.**
- Table 12 has a column "opt.-(ii): optimum minus bound (ii)". Section 8.5 lists the two
  reference values without labels (i) and (ii) (08e-path.tex:31-38), so "(ii)" points nowhere.
- Tables 8 and 9 give no objective sense. pointpack02 and pointpack04 (Part B) and syn05m
  (Part A) are maximization models (checked in experiments/v3/runs/*/records.jsonl). In
  Table 9, pointpack04 goes from 1.164 to 1.109 under all-diag, an improvement that reads as a
  worsening. Table 10 has a "Sense" column; Tables 8-9 do not.
- Table 2: the "Optimum" column shows "---" for MINLPLib without explanation; the header
  "Removes" is unclear.
- Table 1 says root runs have a node limit of one but not their time limits, which differ
  (60 s in Tables 8-9, 120 s in Tables 10-12).

**Fix.** Table 12: rename the column "opt. - block closure" and the caption text to "optimum
minus the block closure (Section 8.5)". Tables 8-9: add a "Sense" column, or a caption note
"syn05m (Table 8), pointpack02 and pointpack04 (Table 9) are maximization models; for them a
smaller bound is stronger". Table 2: header "Cuts off incumbent (models)"; caption "---:
optimal solutions are not available for all models." Table 1 caption: "root runs have a node
limit of one and a time limit of 60 s (Parts 3A, 3B, 4B2) or 120 s (Parts 4D and the path
family)."

---

## [minor] W11. Both figures have label collisions; Figure 1(b) does not name its sets

**Location.** figures/pipeline.tex:23 (Figure 2, PDF p. 21); figures/chords.tex:15-17 and
caption (Figure 1, PDF p. 8).

**Issue.** Figure 2: the dotted "LP point" arrow runs along the top of the "exact support" box
and strikes through its first line (rendered at 200 dpi; round 1 reported the same overlap).
"DAG check" uses an abbreviation not defined in the text. Figure 1(a): the label 5/8 sits on
top of the "(1/2, 5/16)" label and both are hard to read. Figure 1(b): the caption says
"Nested sets" without giving them (the figure shows A = {0, 3/4}, C = {1/4, 1/2}).

**Fix.** pipeline.tex:23: route the arrow to the top of the LP box, e.g. `\draw[->,dotted]
([xshift=2mm]scip.south west) -- ++(0,-6mm) -| node[pos=0.25,above,font=\small] {LP point}
(lp.north);` and change "DAG check" to "expression check". chords.tex:15: place 5/8 below
right of its point and move the crossing label to the left, e.g. `node[left]`. Caption (b):
"Nested sets $A=\{0,\tfrac34\}$, $C=\{\tfrac14,\tfrac12\}$: the chords do not meet ...".

---

## [minor] W12. Broken cross-reference to the availability statement

**Location.** sections/A-separation.tex:234 (PDF p. 48, Appendix E).

**Issue.** "An exact version ... is part of the verification scripts (Section 9)". The label
`sec:availability` sits on a `\section*`, so `\ref` prints the number of the last numbered
section, 9 (Discussion and conclusions), which does not mention the scripts.

**Fix.** "... is part of the verification scripts (see Code and data availability)", or give
the availability section a `\phantomsection` and refer to it by name with `\nameref`.

---

## [minor] W13. The computational outcome is stated four times; Section 9's second paragraph adds little and repeats W1-W2

**Location.** sections/00-abstract.tex:15-21; 01b-results.tex:1-21 (p. 3);
08g-summary.tex:1-17 (p. 31); 09-conclusions.tex:17-33 (pp. 31-32). Also the roadmap in
02-setting.tex:44-49 (p. 4) duplicates 01-introduction.tex:102-108 (p. 3).

**Issue.** The same results (replay, uncertified constants, neutrality on MINLPLib, SCIP's
disabled separators, path-family success) appear in the abstract, the introduction, Section
8.7 and Section 9. Section 9's second paragraph opens with "The computations sharpen these
conclusions. Certification is a real safeguard, not a formality" and repeats Section 8.7. It
carries one point not stated as a conclusion elsewhere (the presolve obstacle), plus the
overstatements of W1 and W2. Section 8.7 also says "a separator configuration fixed in advance
... solved all instances" (08g-summary.tex:11-14), which is true only for the fresh instances.

**Fix.** Replace 09-conclusions.tex:17-33 with:

> The computations add two findings to the theory. First, certification matters in practice:
> the sample minimum would have given wrong constants for 38% of the MINLPLib cuts and for
> almost all sampled path-family cuts, and even local minimization left wrong constants that
> cut off feasible solutions, including known optima. Second, the stored-row check exposed an
> obstacle that the theory does not see: presolve aggregates or fixes the variables to which a
> block refers, so a separator stated in the original variables loses cuts unless it works in
> the presolved space or prevents these reductions, and preventing them weakens SCIP's own
> relaxation. On MINLPLib models the cuts did not help SCIP, whose disabled-by-default
> separators were stronger. On the constructed families, where the theory predicts a gap,
> native SCIP stopped at the level of glued pair relaxations; the certified cuts went beyond
> it when the separator could add about 16 cuts per block, and in the best configuration they
> solved every instance. With a non-binding coupling row, that configuration needed the
> support of each whole row as a first direction (remainder directions solved 13 of 20); with
> a binding row, both direction orders solved all instances, and the useful cuts came from
> the LP direction search.

In 08g-summary.tex:11-14 write "a separator configuration chosen after the campaign-3
diagnostic and fixed before the fresh instances were generated closed at least 97% of the
root gap and solved all 40 fresh instances". Delete the roadmap paragraph 02-setting.tex:44-49
(the introduction already gives it), or keep it and shorten the introduction's outline to one
sentence.

---

## [minor] W14. Three generalizations that the paper does not support

**Location.** sections/04-quadratic.tex:97-98 (p. 12); 09-conclusions.tex:13 (p. 31);
09-conclusions.tex:45-47 (p. 32); 08d-funnel.tex:67-69 (p. 28).

**Issue.**
- "Section 3 shows that the blocks worth merging are often stars" and "For stars, the most
  common merged blocks". Section 3 studies three-variable paths (stars with two leaves) and
  Proposition 3.5; it does not show that stars are common, and in the experiments no block
  needed the star oracle (Section 8.6).
- "on our MINLPLib samples SCIP's own relaxation already contained what the cuts could add".
  The certified cuts did improve the default root bound on four Part B models (08c-minlplib.
  tex:59-65); SCIP's disabled-by-default separators then closed the same gaps.
- "a compiled implementation would remove most of it": no measurement supports "most".

**Fix.** 04-quadratic.tex:97-98: "The merged blocks of Section 3 are stars: several pairs that
share one variable." 09-conclusions.tex:13: "For stars, the merged blocks of Section 3, the
support problem ...". 09-conclusions.tex:45-47: "... on our MINLPLib samples SCIP's default
relaxation already implied most certified rows, and its disabled-by-default separators closed
the few gaps that the cuts closed." 08d-funnel.tex:67-68: "a compiled implementation would
reduce it, but on these models it would at best break even ...".

---

## [minor] W15. "Support cut" is defined twice, differently, and the strength claim applies only to one version

**Location.** sections/01-introduction.tex:17-20 (p. 1); 02-setting.tex:33-35 (p. 4).

**Issue.** The introduction defines support cuts with right-hand side equal to the minimum;
Section 2 calls $a^Tx+b^Tw\ge\beta$ a support cut for any $\beta\le h_D(a,b)$ and then says
"Support cuts are as strong as possible for the block", which holds only for
$\beta=h_D(a,b)$. Later the paper uses "support inequality" for the tight version
(Proposition 3.1, Corollary 4.2) without defining it.

**Fix.** 02-setting.tex:33: "We call $a^Tx+b^Tw\ge\beta$ a support cut, and a support
inequality when $\beta=h_D(a,b)$. Support inequalities are as strong as possible for the
block: ...".

---

## [minor] W16. The description of SCIP's concavity presolve step is imprecise

**Location.** sections/02-setting.tex:157-160 (p. 5).

**Issue.** "Its presolve fixes a variable that occurs in a single nonlinear constraint, in which
the constraint function is concave in that variable, to one of its bounds, and makes it binary
when its bounds are [0,1]." SCIP does not fix the variable. In SCIP 10.0.3
(cons_nonlinear.c, isSingleLockedCand and presolveSingleLockedVars) the candidate must also
have no objective coefficient and finite bounds; with the default `checkvarlocks = t`, SCIP
changes the type to binary when the bounds are [0,1], and with `b` it adds a bound disjunction
instead. The parameter text reads "forced to be at their lower or upper bounds". This step is
central to the path-family discussion (Section 8.5), so the description should be exact.

**Fix.** "If a variable with finite bounds and no objective coefficient occurs in a single
nonlinear constraint whose function is concave in it, some optimal solution has the variable
at a bound; SCIP's presolve then makes the variable binary when its bounds are [0,1] (by
default) or adds a bound disjunction (optionally) [11, Section 4.2.7]."

---

## [minor] W17. Terms used before they are defined, or never attached to a definition

**Location.** sections/03-composition.tex:27-31 (p. 6); 07-implementation.tex:93-99, 129-131
(p. 22); 08e-path.tex:84-91, 161 (pp. 28-30); 09-conclusions.tex:10, 44 (pp. 31-32);
01-introduction.tex:53; 01b-results.tex:7 (p. 3).

**Issue.**
- The set R of Section 3.1 is never named, yet the paper calls it "glued pair relaxation",
  "glued relaxation", "glued exact pair hulls" and "glued pair hulls"; Section 8 adds
  "pair-hull level" for its bound.
- "remainder directions" is defined in the last sentence of Section 7.2 (line 131), after the
  directions are described (lines 93-99) and the contrasting term "whole-row directions" is
  introduced (line 98).
- "block closure" (08e-path.tex:161; 09-conclusions.tex:44) is never defined; the concept is
  "the best root bound that cuts on the blocks can give" (08e-path.tex:34, 149-150).
- "the trivial bound zero" (01-introduction.tex:53; 09-conclusions.tex:10) and Section 3's
  "no positive bound" (03-composition.tex:285) name the same thing differently.
- The introduction uses "the path family" (01b-results.tex:7) four lines before it introduces
  "constructed instances with the path structure".

**Fix.** 03-composition.tex:31: "... share $m_y$ and $s_y$. We call $R$ the glued pair
relaxation." 07-implementation.tex:93-95: "At an LP solution the separator first tries, for
each block and each of its source sides $j$, the remainder direction $a=0$, $\lambda=e_j$. It
bounds only the side's nonlinear remainder; ..." and delete the clause at line 131.
08e-path.tex:34: "... the best root bound that cuts on the blocks $(x_i,y_i,z_i)$ can give,
which we call the block closure, ...". Use "no positive bound" throughout (abstract,
introduction, Section 9). 01b-results.tex:7: "on the constructed path family of Section 3".

---

## [minor] W18. Undefined abbreviations and uncited tools

**Location.** RLT: 02-setting.tex:100 (p. 4); SOC: 04-quadratic.tex:203 (p. 14); SLSQP:
08b-validity.tex:26, 50 (p. 24); HiGHS: 07-implementation.tex:6 (p. 20); OSiL:
08a-setup.tex:33 (p. 23); "soft budget": 08a-setup.tex:26 (p. 23); DAG: figures/pipeline.tex:10.

**Issue.** RLT and SOC are never expanded. SLSQP and HiGHS are used without a citation (HiGHS
is credited only as part of SciPy in the availability statement). OSiL is not explained.
"soft budget" is not defined anywhere.

**Fix.** "semidefinite and reformulation-linearization (RLT) constraints"; "second-order cone
(SOC) descriptions"; "SciPy's SLSQP (sequential least squares programming; Kraft 1988)";
"HiGHS [Huangfu and Hall 2018] through SciPy"; "in OSiL, the XML instance format of
Optimization Services"; "wall times charged to the 300-second budget".

---

## [minor] W19. Notation clashes within Section 3 and Section 8.1

**Location.** 03-composition.tex:136-137 and A-composition.tex:9-10 ($\kappa_A,\kappa_C$);
03-composition.tex:217 (Dirac $\delta_t$); 08a-setup.tex:43 (dual bounds $a$, $b$).

**Issue.** In the proof of Theorem 3.2 (p. 7), $\kappa_A,\kappa_C$ are constants; one page
later $\kappa$ is the number of shared moments, the central parameter of Theorem 3.3. On p. 8
$\delta_{15/32}$ denotes a point mass in the same passage where $\delta$ is the distance of
Theorem 3.2. In Section 8.1, "Dual bounds $a$ and $b$" reuses the direction symbols.

**Fix.** Rename $\kappa_A,\kappa_C$ to $\eta_A,\eta_C$. Write the measures of p. 8 as "$\nu_A$
puts mass $\tfrac{57}{112}$ at $\tfrac{15}{32}$ and $\tfrac{55}{112}$ at $\tfrac{57}{32}$", or
use $[t]$ for the point mass. Write "Dual bounds $z$ and $z'$".

---

## [minor] W20. A few informal or note-like sentences

**Location.** 07-implementation.tex:20-21 (p. 20); 08b-validity.tex:13 (p. 23);
08g-summary.tex:19 (p. 31); 09-conclusions.tex:17-18 (p. 31); 03-composition.tex:224 (p. 9).

**Issue.** "A third paragraph describes the bounds that certificates use." (a note to the
reader about layout); "Two observations show that the checks are not idle."; "The study has
limitations that the reader should weigh." (round 1 flagged it; still there); "The
computations sharpen these conclusions. Certification is a real safeguard, not a formality";
"Every $\kappa$ is nevertheless defeated by some quadratic configuration." The paper also opens
six paragraphs with "Two/Three X ..." announcements (04-quadratic.tex:45, 06-certification.
tex:85, 07-implementation.tex:117, 08b-validity.tex:13, 08d-funnel.tex:4, 09-conclusions.tex:3);
each is fine, together they read as a template.

**Fix.** 07:20-21: "We also describe the bounds that certificates use." 08b:13: "The checks
also changed what reached SCIP." 08g:19: delete the sentence and start a paragraph
"\paragraph{Limitations.} The MINLPLib parts use ...". 09:17-18: see W13. 03:224: "For every
$\kappa$, however, some quadratic configuration has a full gap." Rephrase two of the six
announcements (for example 08b:13 as above, and 06:85 "A certificate depends on two
hypotheses.").

---

## [minor] W21. Three overlong sentences in places a referee reads closely

**Location.** 08c-minlplib.tex:12-20 (79 words, p. 25); 06-certification.tex:35-42 (68 words,
p. 18); 08b-validity.tex:46-52 (75 words, p. 24). Counts from
verification/R9_writing_sentences.py.

**Fix.**
- 08c: "Part D, in campaign 4, addresses this. Its pool consists of the 322 MINLPLib models with
  121 to 1,000 variables that are not convex by the library's metadata, contain a quadratic or
  polynomial function and were not used before. Of these, 85 have a block that auto admits,
  and 58 of those are not solved by SCIP within 60 seconds; Part D takes the first 20 of the 58
  in a fixed hash order (Appendix G)."
- 06: "Two points are specific to support cuts. The bound must be certified for the final
  direction on the whole block domain, which is a global nonconvex minimization. And the stored
  row must be checked: outside its exact mode, SCIP 10 rounds a row coefficient that is
  integral within its tolerance to that integer without adjusting the sides (functions
  rowAddCoef, rowChgCoefPos and rowMerge in src/scip/lp.c [105])."
- 08b: "To measure what the certificate itself buys (Part 4U), we recomputed, for the recorded
  binary64 direction of each cut, the constant that an uncertified pipeline would use. U1 is
  the minimum over the separator's own sample set, which is what the direction LP sees. U2 is
  the better of U1 and SLSQP local minimizations started from the three best samples, on the
  block box and the affine domain rows. Up to binary64 rounding, both are upper bounds on the
  true support value."

---

## [minor] W22. Front matter required by the journal is missing

**Location.** main.tex:17-19.

**Issue.** `\author{}` is empty; there are no keywords and no MSC 2020 codes; there is no
"Declarations" section (funding, competing interests, data availability), which Springer
journals including JOGO ask for. The availability statement names a "supplementary archive"
but no persistent identifier.

**Fix.** Add authors and affiliations; keywords (e.g. simultaneous convexification; support
cuts; safe rounding; nonconvex quadratic programming; MINLP); MSC codes (90C26, 90C11, 90C20,
65G30); a Declarations section; and a DOI for the archive (for example Zenodo) in the
availability statement.

---

## [suggestion] W23. Structure and length: optional cuts and small reorderings

**Location.** Whole paper (main text pp. 1-32, appendices pp. 40-56).

**Issue and fix.**
- The main text runs 32 pages. Candidates for the appendix without loss to the main line:
  the worked examples after Proposition 3.5 (03-composition.tex:391-410), the hierarchy
  paragraph and its example at the end of Section 5.3, the corruption list of Section 6.3, and
  the "Relation to forest algorithms" paragraph cut to its first four sentences plus the
  novelty sentence.
- Contribution bullet 3 (01-introduction.tex:73-88) covers Sections 5-8 in one bullet; split
  into "Cuts in the original variables and their certification (Sections 5-6)" and
  "Implementation and evaluation (Sections 7-8)".
- 01-introduction.tex:21-23 attaches six citations to four topics in one block; place each
  citation after its topic. 01-introduction.tex:11-12 names pooling, heat exchange and gas
  networks without citations.
- Section 8.3 opens with a long selection paragraph; add a lead sentence: "On MINLPLib models
  the cuts were neutral for SCIP: they changed neither which models it solved nor its own
  solving time."
- The proof of Proposition 3.1 depends on Theorem 3.2 ("the case ... of Theorem 3.2 below");
  either state the minimum of Φ directly in the proof or present the example after the theorem.
- Table 7 (mode definitions) is needed to read every table of Section 8 but sits in
  Appendix G; consider moving it to Section 8.1.
