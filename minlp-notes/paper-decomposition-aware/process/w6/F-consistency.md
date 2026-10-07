# W6 F-consistency: whole-paper consistency after the W5 moves

Sources checked: `main.tex`, `sections/*.tex` (not edited), PDF
`/tmp/dpaper/out/main.pdf` (127 pp.) and `/tmp/dpaper/out/main.aux`. The
build copy in `/tmp/dpaper` is identical to the repository sources
(`diff -rq` empty); the log has no undefined references or citations.

## Verdict

No critical or major problem. Every `\ref` to a moved object resolves and
reads correctly, every main-text summary of a moved result matches the
appendix statement, and the abstract, Theorems 1.1/1.2, Table 1, the
extension paragraphs, the conclusion and the section roadmaps match the
current statements. All experimental numbers quoted in more than one place
agree with each other and with `experiments/results/*.csv`. Five minor
problems remain; three were introduced by the W5 moves and merges
(F-consistency-1, -4) or are wording slips (F-consistency-2), and two concern
completeness or precision of the front matter and notation table
(F-consistency-3, -5).

## Findings

### F-consistency-1 (minor): Section 6.5 says the instances of Section 11.4 have at most six variables

*Location:* `sections/exact-localized.tex:2-4`.

*Problem:* "as small as about $2^{-315}$ on the instances of
Section~\ref{sec:comp-exact}, which have at most six variables." W5 merged
the old subsections "Exact output" and "Localized acceptance" into 11.4, so
Section 11.4 now also contains S1, whose instances have $n=4,\dots,16$
(`computation.tex:216`). The relative clause is true only of the E4
instances. (Before W5 the sentence said "the exact-output instances of
Section~\ref{sec:comp-exact}", which was then a subsection containing only E4.)

*Evidence:* `process/w6/checks/F-numbers.py`: S1 has $n\in[4,16]$; E4 has
$n\le6$ and required bits (with $\Omega$ of eq. (6.1)) from 21.3 to 315.0; the
largest S1 requirement is 150 bits, so the number 315 itself is right.

*Fix:* replace

    below $1/(\Omega W)$, as small as about $2^{-315}$ on the instances of
    Section~\ref{sec:comp-exact}, which have at most six variables. The filtering

with

    below $1/(\Omega W)$, as small as about $2^{-315}$ on the exact-output
    instances of experiment E4 (Section~\ref{sec:comp-exact}), which have at
    most six variables. The filtering

### F-consistency-2 (minor): Appendix B calls two propositions "examples"

*Location:* `sections/appendix-boundary.tex:224-225`.

*Problem:* "The margin term and strict complementarity are both needed for
certificates of this form, as the next two examples show." The next two
items are Proposition B.5 (`prop:margin`) and Proposition B.6
(`prop:weakcompl`); Section 6.6 (`exact.tex:506-508`) and the conclusion
(`conclusion.tex:70`) correctly call them propositions.

*Fix:* replace "as the next two examples show." with "as the next two
propositions show."

### F-consistency-3 (minor): the notation table omits $\nu$ and the time-bound functions $f$, $f_1$

*Location:* `sections/setting.tex:152-195` (Table 2, `tab:notation`).

*Problem:* The table claims to list "the symbols used in several sections and
the second meanings of a few of them". Two symbols that cross sections are
missing:
* $\nu=\max\{0,-\lambda_{\min}(\nabla^2F)\}$ is used in Section 7.3
  (`recourse-convex.tex:283-316`), Section 10.1 (`limits.tex:184,187`, where it
  is used without a local definition), Section 10.7 (`limits.tex:554-564`) and
  Section 12 (`conclusion.tex:30-36`), and in Appendices C and G.
* $f(p,t)$, $f_1$ and $C_1$ (Theorem 1.1, Theorems 5.7 and 6.14) are used in
  Sections 1, 5, 6, 7 (Theorems 7.2, 7.9), 10 and 12. $f_1$ is a second meaning
  of the reserved letter $f$ (factors $f_a$, $a\in\mathcal A$), which the
  table's lead promises to record.

*Fix:* insert before `\bottomrule` (after the row beginning
`$\bar L$, $\kappa_c$, $\eta$`, line 192):

    $\nu$ & $\max\{0,-\lambda_{\min}(\nabla^2F)\}$, size of the negative curvature & \S\ref{sec:convexrecourse}\\
    $f(p,t)$, $f_1$, $C_1$ & function and exponent in the time bounds of CT and EX (not factors) & Thms.~\ref{thm:approx}, \ref{thm:exact}\\

### F-consistency-4 (minor): "the theorem" at the start of Section 5.5 now points to the wrong theorem

*Location:* `sections/growth.tex:338-340`.

*Problem:* "The first example shows that the theorem covers nonconvex
problems with many local minima and treewidth larger than one." W5 moved the
sharpness subsection (`growth-sharp.tex`) directly before Section 5.5. Its
last paragraph ends with "(Theorem 9.4 with $r=1$ and $\kappa_S=\kappa$)",
so the nearest theorem a reader sees is Theorem 9.4 (UC), not Theorem 5.7.
Example 5.12 itself applies Theorem 5.7.

*Evidence:* rendered text p. 21, `pdftotext` lines 1472-1484: "...(Theorem 9.4
with r = 1 and κS = κ). ... 5.5 Examples. The first example shows that the
theorem covers ...".

*Fix:* replace "The first example shows that the theorem covers nonconvex
problems with many" with "The first example shows that
Theorem~\ref{thm:approx} covers nonconvex problems with many".

### F-consistency-5 (minor): the introduction asserts set growth for "every instance" right after discussing polynomial instances

*Location:* `sections/intro.tex:114-121`.

*Problem:* The sentences before it discuss polynomial factors (Corollary 6.22,
Example 6.23). The next sentence reads "Exactness itself needs no uniqueness:
every instance has a growth constant $g_S>0$ towards its optimal set". For
polynomial instances this is false: $x^4$ on $[-1,1]$ (Example 6.23(b)) has
the single minimizer $0$ and no $g_S>0$. Remark 6.10 (`rem:setgrowth`), which
the sentence cites, is stated for rational mixed box QPs, and
`setting.tex:137-140` qualifies it the same way ("For quadratics, ...").

*Fix:* replace "Exactness itself needs no uniqueness: every instance has a
growth constant" with "Exactness itself needs no uniqueness: every rational
mixed box QP has a growth constant".

## What was checked and found consistent

* **References to moved objects.** All 279 labels resolve (no `??`, no
  undefined references). `process/w6/checks/F-reftypes.py` compares the word
  before every `\ref` ("Lemma", "Proposition", "Section", "Appendix", ...)
  with the environment type recorded by cleveref in `main.aux`: 0 mismatches.
  Every main-text pointer to an appendix object either names the appendix or
  carries the appendix letter in its number (e.g. "Lemma B.1",
  "Proposition C.2 in Appendix C"). Every "Appendix~\ref{...}" pointer was
  checked against the content of its target (Apps A-H). Every part reference
  of the form `\ref{...}(x)` (66 distinct) names an existing part.
  No "above", "below", "next" or "previous" points across sections, except
  F-consistency-2 (wrong object type) and F-consistency-4 (ambiguous "the
  theorem").
* **Summaries of moved results** against the appendix statements:
  Prop. C.1, C.2 (7.2, 10.7 and the Section 7 and 10 roadmaps; "$\kappa<11$" =
  $2(3+\sqrt5)$), C.4, Thm. C.7, Cor. C.9, C.10, Ex. C.11 (8 vs $2M+8$),
  Prop. C.12 ($L^+/g\le\frac{41}4\cdot12=123$), the clipped-piece remark after
  Prop. 7.11; Thm. D.2, Lemma D.1, Prop. D.4, the proof sketch of Lemma 7.23;
  Prop. E.2, Rem. E.1, Ex. E.3 ($2^j+1$ nodes), Alg. E.7 (prose description in
  8.6), Lemma E.10 ($n_c^{p/2}$ for $\varepsilon\le\bar L/64$, $\kappa_c=2$),
  Prop. E.11, Ex. E.12; Ex. F.1, Lemma F.2 ($\frac{99}{256}$, $K_\theta$, bit
  length), Rem. F.3, Prop. F.4 and the coNP-hardness paragraph; Rem. G.1
  ($\kappa$ and $\nu/g$ exponential in the number of variables), Lemma G.3,
  Def. G.4, Prop. G.5 (gap $>\frac18$, $\nabla^2F\succeq-2I$); the proof
  sketches of Props. 10.6-10.10; Cor. 6.19 and Appendix B.1; Thm. B.4,
  Props. B.5, B.6 as summarized in 6.6 and in the conclusion.
* **Abstract, Theorem 1.1, Theorem 1.2** against Theorems 4.7, 5.7, 6.9, 6.14,
  Lemma 5.5, Remark 5.8, Lemma 3.3, Propositions 10.1, 10.3, 10.5, 10.6 and
  Corollary 10.2 (hypotheses, constants $f(p,t)$, $(I+q+1)^5$,
  $(\kappa/(8p))^{p/2}-1$, $\kappa\le2$, $\log\kappa=O(I)$, the
  $\lambda_{\min}\ge2L/\kappa$ and $F(x')-\OPT\ge L\norm{x'-x^*}^2/\kappa$
  consequences of growth).
* **Table 1**, row by row, against Theorems 5.7, 6.14, 7.2, 7.9, 7.15, 7.18,
  D.2, 7.24, 8.9, 9.4, 9.7, Cor. 9.8, Thm. 9.14 and Prop. 7.19, including the
  TU constant $K$ and the caption's hypotheses for the exact bounds.
* **Extension paragraphs** (conditional recourse, coupling constraints,
  several minimizers, further limits), the conclusion and the roadmaps of
  Sections 4-12, including the Section 10 list of what each subsection proves.
* **Algorithm names:** TRIAL, CT, CT with a common mesh, REC, EX, UC, CORE,
  TU-GRID, TU-EXACT, PROX, DISC are used consistently in text, captions and
  appendices; no "Algorithm 1/2", "capped algorithm", "FG" or "pruned grid"
  remains. Caps agree across Lemma 5.5 ($10\theta^{-1}\lceil\log_2(n_P+2)\rceil$),
  Lemma 5.9(G5) and App. B ($8\theta^{-1}\lceil\log_2(n+2)\rceil$), PROX
  ($K_\theta$, App. F: $\le48\sqrt{\hat\kappa}\lceil\log_2(n+2)\rceil$) and
  App. H(b) ($100\cdot2^\mu\lceil\log_2(n+2)\rceil$ = 12.5 times).
* **Numbers quoted in several places** (`process/w6/checks/F-numbers.py` plus
  the inline checks recorded below), all consistent with the CSV results:
  $2^{-315}$ and "21 to 315 bits" (6.5, 11.4); S1: 29 of 30, face candidate
  within nine stages (max index 8), incumbent rule within five, 12 on the full
  box, one CT run up to 72 stages, EX up to 542, 40-72 and 139-157 stages on
  the five hardest instances (6.5, 11.4); E4: 18 of 20 certified, 67-534 stages
  for 49-342 bits with the groups of App. H, gaps $2^{-11}$ vs $2^{-53}$;
  876 stages with ratios 0.28/0.18/0.05 (11.2) = 0.16 of $\frac9{16}$,
  0.18, 5% of the cap and 0.4% of the implementation cap (App. H); 347 of
  3,177 free coordinates; E1 entries 83,161 and 64,879, plateau about 1,000
  and 1,100; E2 plateau 9 to 49; E3 plateaus 7-26, 9-19, 9-17; App. H count
  78 runs / 153 nodes; E5: 21 instances, 12 + 9, shortfall
  $1.8\cdot10^{-6}$-$1.6\cdot10^{-5}$, bound share 51%-94%, epigraph part
  $9.00$-$9.03\cdot10^{-7}$, exact gaps $2.8$-$6.8\cdot10^{-6}$, 27 and 39
  variant runs, CT $\le6.9$ s; E6: 40 instances, 27 unchanged grids, change
  $\le5$, stages 7-9 to 27-29, 11 certified with the listed $\kappa$
  intervals (lower end 4.5), 28 localized, 1 open, 42 of 213 free
  coordinates on the grid; chain: $m\le64$, 5 to 11 nodes (Example 5.13, 11.3,
  Table 3); recourse: six instances, 0.07 s, gaps 0.019 and 1.23, 498 and
  35,600 entries, 0.08 s (11.7, Table 6); replay/solve ratio 0.81 to 2.54.
* **Notation table** against use: all listed symbols have the listed meaning
  and location; the only gaps found are F-consistency-3.

## Commands run (targeted; not CI)

* `pdftotext /tmp/dpaper/out/main.pdf`, `pdftotext -layout ...` (rendered text).
* `diff -rq /tmp/dpaper/sections sections` (build copy = sources).
* `grep` over `main.log` for undefined references/citations (none).
* `python3 process/w6/checks/F-reftypes.py` (0 mismatches).
* `python3 process/w6/checks/F-numbers.py` and inline Python over
  `experiments/results/{E1..E3}_{runs,stages}.csv`, `E4_exact.csv`,
  `S1_localized.csv`, `S1_ex_replay.csv`, `E5_scip*.csv`,
  `E5_grid_runs.csv`, `E6_random_growth.csv` (values listed above).
* `diff` of `process/w5/sections-before-w5/*.tex` against `sections/*.tex`
  to locate text affected by the W5 moves.
* Label map: `process/w6/checks/F-labels.txt`.
