# Writing review, round 2: revised main paper (line level)

Reviewer lens: plain, simple and precise language for an expert reader;
AI-style prose, filler, stacked hedges, announcements, restating summaries;
long or tangled sentences; undefined or inconsistent terms (against
`development/terminology.md` and `style-guide.md`); unclear paragraphs and
transitions; resolution of the round-1 items in `round1/opus-writing.md`.

Scope: `main.tex` as built (`sections/00`–`11`, `A-semantics.tex`,
`G-proofs-split.tex` printed as Appendix B, and the captions of the tables the
main paper prints), plus the supplement front matter (`supplement.tex`,
`B0-families.tex`) and the opening paragraphs of S1.1–S1.9 and S2–S8. Line
numbers refer to the current files in `sections/` and `tables/`.

Checks run (targeted, read-only; nothing was built, edited or committed
except this file; no repository script was run):

- `cat -n` of every main-paper section, of the main-table captions and of
  the first 40 lines of every supplement section;
- `grep` over the main sections for the banned words of `style-guide.md`,
  intensifiers and hedges, em dashes, "reading"/"read", "verified",
  "computed", "independent", "authors'", "by hand", "first implementation",
  the closure terms ("floating-point closure", "near-closure",
  "tolerance-level closure") and the variants of "best listed dual";
- a sentence-length scan (`/tmp/opusw2/longsent.py`, source lines of 45 or
  more words after removing citations, references and inline math);
- abstract word count with `sed`/`wc` (250 words now);
- `pdftotext -layout` of the existing `build/main.pdf` (60 pages) and
  `build/supplement.pdf` (not rebuilt), to see how openings render;
- the pre-revision sources extracted from
  `/workspace/local-home/paper-backups/paper-open-minlplib-r1-20261004-1841.tar`
  into `/tmp/opusw2/r1/` to compare passages;
- to confirm meanings before rewriting: `D-literature.tex` (funnel,
  `:247–292`), `E-audit.tex:32` (half-unit slack), `B4-chain-catmix.tex:30–55`
  (polyline), `tables/tab-trust.tex`, Table 7 in `10-reproducibility.tex`,
  `round1/adjudication.md` and `revise3-result.json` (`edits[].open`).

No CI result was consulted; the checks above are local and targeted.

## Verdict

**Minor revision of the writing.** The revision fixed almost all round-1
items: the status words of §2.6 no longer overlap, "reading" is gone from §9
and §11, §3, §5, §7, §8 and §9 now open with their result, the `catmix`
mechanism is no longer ascribed to the split lemma, the `chain` outline
defines its symbols, and the dual bound in the instance list is defined. No
banned word and no em dash occurs. The prose is plain and mostly precise, and
an expert can follow every section.

What remains:

1. Two major points. The new §3.1 selection sentence is false as written
   (41, not 43, instances come from the 155), and the main text uses
   "floating-point closure" and "near-closure", in the abstract and in C1,
   without defining them next to the defined "tolerance-level closure".
2. Residual tangles: the §1 contribution list still has several 60–80-word
   sentences, an ambiguous "its `.nl` file" and an unintroduced "109"; a few
   one-line wordings in §2 and §4–§8 are unclear ("which other data need not
   satisfy", "toward the infeasible side", "as checks that it does not use",
   "the first implementation's search … is a second complete certificate").
3. One factual inconsistency between two places in the main text: §4.5 puts
   all `waterno2` searches in Tier 3, Table 7 puts two of them in Tier 2.
4. Repetition and length: §1 states the SCIP mechanism twice, and §11 restates
   the full `camshape` deficit statement a fourth time. §1 is about 0.6 page
   over its target (`revise3-result.json`); the rewrites below shorten it
   without dropping a qualifier.

Counts: 0 blocker, 2 major, 29 minor.

## Status of the round-1 items

| round-1 item | status | note |
|---|---|---|
| 1 status words | resolved | `02:194–198`; `07:60`, `A:104` aligned |
| 2 separately written | resolved | residual referent "these exceptions", item 14 |
| 3 "reading" | resolved (rename rejected, R-15) | §9, §11, `02:169`, `A:41`, `A:46` fixed; A.2 term names, item 30 |
| 4 §4 opening | resolved | `04:10–14` |
| 5 `chain` outline | resolved | small repetition "heights … heights", item 18 |
| 6 §3 opening | resolved | announcement sentence `03:15`, item 15 |
| 7 §5 opening | resolved in §5 | circular glosses persist in §3.2 `03:53`, item 15 |
| 8 instance-list dual | resolved | `02:63–64` |
| 9 abstract | resolved | new wording points, item 3 |
| 10–15 §1 wording | resolved | |
| 16 inverted syntax | **open** | `01:59`, `11:65`, item 5 |
| 17 "existence tests" | superseded | residual in C1 `01:77`, item 7 |
| 18–28 | resolved | |
| 29 width rule | resolved (moved to S3.4) | |
| 30–33 | resolved | |
| 31 bag/stage | resolved except `09:57` | item 26 |
| 34 `optcdeg2` motivation | resolved | "There … at this point", item 17 |
| 35–36, 38–41, 43–44, 46–51 | resolved | |
| 37 authors'/first implementation | resolved | new first/second tangle `05:281`, item 21 |
| 42 half a unit | partly | "slack", "both rules" `07:28`, item 23 |
| 45 §8 opening | resolved | optional lead-in before Prop. 8.1 not added, item 25 |
| 52 repetition | partly | item 10 |

---

## Major issues

### 1. [major] §3.1 says all 43 instances come from the 155, and uses the undefined "census"

`sections/03-results.tex:42–44`

**Problem.** Line 42 reads "We chose the 43 instances from the 155 nonconvex
instances that are open by a selection rule stricter than MINLPLib's …".
Line 43 then says that two of the 43, `camshape100` and `lnts50`, "were not
open by that rule". The first sentence is false, and the paragraph
contradicts itself. "In two rounds" also hides that the first 11 instances
were chosen before the rule was fixed. Line 44 then uses "the census", which
the main text never defines; the width census is described only in S3.4.
Read with the defined term "separately written", "Three separately written
programs … ; no separate agent session read the census" sounds
contradictory. This paragraph carries the "not a solve rate" qualifier
(outline §8 item 8, rule 6 home), so it must be exact.

**Evidence.** `D-literature.tex` Table S-funnel: "other instances of the
paper, among the 155: 12"; "closed in the paper, among the 294 but not the
155: 2"; `:282` "we chose our first 11 instances … before the rule was fixed";
`:285` "the other 32 instances from the remaining 146"; `:290` "no separate
agent session read the census or the selection code; all counts …
reproduce with three separately written programs from the saved pages and
census data". `11-conclusion.tex:55`: 29 + 12 + 114 = 155.

**Fix.** Replace lines 42–44 with:

> Of our 43 instances, 41 lie among the 155 nonconvex instances that are open
> by a selection rule stricter than MINLPLib's (\cref{app:literature-funnel}
> gives the rule, the funnel and its caveats). We chose them in two rounds by
> judged tractability, the first 11 before the rule was fixed, so the 29
> closures among the 155 are not a solve rate. The other two closures,
> \inst{camshape100} and \inst{lnts50}, are not open by that rule, because
> their best listed duals were already within \sci{1.22}{-6} and
> \sci{3.9}{-5}, relative, of the best listed points and of our proved optima;
> for them what is new is the exact optimal value, its proof and an exactly
> feasible point. Three separately written programs reproduce every count of
> the funnel from the saved page and width data; no separate agent session
> reviewed the code that computed the widths and applied the rule.

### 2. [major] "Floating-point closure" and "near-closure" are used but not defined in the main paper

`sections/00-abstract.tex:7–8, 13`; `01-introduction.tex:76, 79, 100`;
`02-semantics.tex:82`; `03-results.tex:70`; `08-solvers.tex:40`

**Problem.** The abstract and C1 rest the priority qualifier on
"floating-point closures or near-closures", and §3.4 uses the labels *fp
closure* and *fp near-closure*, glossed circularly as "a floating-point
closure or near-closure was reported". The main paper defines only the
*tolerance-level closure* (§2.2, line 82), and the abstract uses both terms
in adjacent sentences ("floating-point closures … had been reported";
"BARON reached tolerance-level closures"). A reader cannot tell how the two
differ, or what "near" means. The definitions exist only in the supplement
(`D-literature.tex:15`, `:55`: "printed gaps of at most 0.01%"). §8.1 line 40
uses the intended relation without stating it: these runs "close both
instances in floating point; we credit them as tolerance-level closures".

**Fix.** Replace `02-semantics.tex:82` with:

> A solver run reaches a \emph{floating-point closure} if it reports, at a
> point feasible within its tolerances, a value within its optimality
> tolerance of its own dual bound, and a \emph{floating-point near-closure}
> if its printed relative gap is at most $10^{-4}$. A floating-point closure
> is a \emph{tolerance-level closure} if, in addition, its dual bound is
> valid. None of these is a closure in the sense of
> \cref{def:sem-certificate}; we credit them by name
> (\cref{sec:results-prior}).

Then write at `03-results.tex:70` "Seven closures have prior status
\emph{fp closure} or \emph{fp near-closure} (\cref{sec:semantics-cert}): …",
and at `D-literature.tex:15` replace the definition by a pointer to §2.2.

---

## Minor issues

### 3. [minor] Abstract: three unclear phrases

`sections/00-abstract.tex:8, 9, 11, 13`

**Problem.** Line 8: "whose exp variant" leaves the reader to guess the
instance name. Line 9: "we enclose their optima" refers grammatically to the
six stored models, whose optimal value is $+\infty$; the enclosure concerns
the models without the partition-of-unity rows. Line 11 ends on a dangling
", relative." Line 13: "on two" (runs or instances?). The abstract has exactly
250 words; the replacements below keep the count.

**Fix.**

- `:8` "for \inst{ann_cumene_tanh}, whose variant \inst{ann_cumene_exp} has
  floating-point closures, we prove a bound with gap 0.195\%."
- `:9` "Our six Kolmogorov--Arnold network instances have no exactly feasible
  point; dropping their partition-of-unity rows, we enclose the optima within
  \sci{2.42}{-8}."
- `:11` "…; four proved relative margins exceed 1\% and eleven are below
  $10^{-6}$." (one word fewer)
- `:13` "…; BARON reached tolerance-level closures on two instances." (one
  word more)

### 4. [minor] §1.2 observation 3: "lose" what, and which "tabulated" $\varepsilon$?

`sections/01-introduction.tex:63`

**Problem.** "points with violations at most $\varepsilon$ lose at most
$0.61\,n^2\varepsilon$ for the tabulated $\varepsilon$" does not say what is
lost (objective relative to the optimum), and "the tabulated $\varepsilon$"
points to Table S6, which the introduction never names.

**Fix.** "…: for \inst{camshape}, points that violate each row and bound by
at most $\varepsilon$ lie at most $0.61\,n^2\varepsilon$ below the optimum
(proved for the values $\varepsilon\le10^{-8}$ of
\cref{tab:camshape-deficit}), and explicit tolerance-feasible points reach
about 87\% of this bound (numerical evidence)."

### 5. [minor] Inverted syntax returned (round-1 item 16)

`sections/01-introduction.tex:59`; `11-conclusion.tex:65`

**Problem.** "Why general-purpose solvers did not find such bounds we do not
test" and "why general-purpose solvers did not find such bounds we have only
interpreted" front the object clause. The reader parses "Why … bounds" as a
question first.

**Fix.**

- `01:59` "We do not test why general-purpose solvers did not find such
  bounds; \cref{sec:interpretation} offers an interpretation."
- `11:65` "…, little search remained; we have only interpreted, not tested,
  why general-purpose solvers did not find such bounds
  (\cref{sec:interpretation})."

### 6. [minor] Four overlong sentences in §1

`sections/01-introduction.tex:27` (61 words), `:74` (68), `:76` (58), `:80`
(62)

**Problem.** Line 27 joins three unrelated citations with semicolons. In line
74 the appositive "28 continuous and three mixed-integer, from 14 instance
families" sits between subject and verb. Line 76 nests "or for `dtoc5` of a
copy under assumed variable bounds" inside the subject. Line 80 ends with
"they say nothing …", where "they" could be the lower ends or the
enclosures.

**Fix.**

- `:27` "A machine-learning approach to global optimization calls a result on
  a MINLPLib model optimal when its gap is below 0.1\%, while noting that its
  solutions may be infeasible [cite]. The public CAMINO benchmark data record
  Gurobi bounds that equal the recorded objective values [cite]. A study of
  optimization over trained Kolmogorov--Arnold networks (KANs) reports SCIP
  optima at zero gap [cite]."
- `:74` "For 31 instances that are not marked solved (snapshot of
  \cref{sec:semantics-model}) we prove a dual bound that is valid for every
  exactly feasible point of the stored OSIL model, and we exhibit an exactly
  feasible point within a relative gap of at most \sci{3.1}{-9}
  (\cref{tab:closures}). They come from 14 instance families; 28 are
  continuous and three mixed-integer. We chose the instances by judged
  tractability, so 31 is not a solve rate (\cref{sec:results-selection})."
- `:76` "To our knowledge, within the search described in
  \cref{sec:intro-prior} and \cref{app:literature}, no rigorous certificate
  had been published for any of these 31 stored models. For seven of them,
  floating-point closures or near-closures had been reported: for six on the
  same model, for \inst{dtoc5} on a copy under assumed variable bounds;
  \cref{sec:results-prior} credits these and the other earlier results by
  name."
- `:80` "The six KAN instances in our set have no exactly feasible point
  (\cref{prop:kan-infeasible}). For the model $\RP$ without their
  partition-of-unity rows we enclose the optimal value with width at most
  \sci{2.42}{-8} (\inst{kan_r5_h1_n3}) and \sci{1.08}{-10} (the other five),
  and the lower ends also bound the network relaxation $\Rnet$
  (\cref{thm:kan-enclosure}). These enclosures say nothing about points that
  satisfy the OSIL rows only within a tolerance."

(Count of the seven checked against `03-results.tex:71–74`: `lnts50`,
`eg_int_s`, `lnts100`–`lnts400`, `camshape100` on the same model, and
`dtoc5` on a copy.)

### 7. [minor] "Floating-point point(s)", "existence tests" and "closure evidence"

`sections/01-introduction.tex:77`; `06-points.tex:6, 66`

**Problem.** "floating-point points" (`01:77`, `06:66`) and "A floating-point
point" (`06:6`) read as a typo. C1 says the 13 points are replaced "using
classical existence tests", but for `dtoc5`, `chain` and `lukvle10` the
replacements are explicit exact points or triangular definitions, not
existence tests (`tab:points`). "The earlier closure evidence" (`06:66`) is
vague.

**Fix.**

- `01:77` "…; for 13 closures the points computed in floating point that
  first indicated a closure violate rows by \sci{2.4}{-20} to
  \sci{7.91}{-12}, and we replace them by exactly feasible points built with
  classical constructions (\cref{sec:points})."
- `06:6` "A point computed in floating point satisfies nonlinear equality
  rows only up to rounding, …"
- `06:66` "For 13 closures, the points that first indicated a closure violate
  rows slightly: our own points computed in floating point for \inst{lnts},
  \inst{dtoc5} and \inst{chain}, and MINLPLib's listed points p5 for
  \inst{lukvle10} and p1 for the three \inst{powerflow} instances."

### 8. [minor] C3: an ambiguous "its", an unintroduced "109", and "ended within $10^{-6}$"

`sections/01-introduction.tex:96, 99, 100`; `08-solvers.tex:25`

**Problem.** Line 96 is one sentence of about 80 words with two "assuming"
clauses. In its second half, "assuming that its \texttt{.nl} file encodes
…" has CAMINO, the subject of the first half, as its nearest antecedent.
Line 99, "79 of the 109", introduces 109 without a noun. In `01:100` and
`08:25`, "ended within $10^{-6}$" omits "relative gap".

**Fix.**

- `:96` as two sentences: "Assuming that CAMINO used the current MINLPLib
  files and recorded AMPL's \texttt{bestbound}, its bounds for Gurobi 13.0.0
  on \inst{eg_disc2_s}, \inst{eg_disc_s} and \inst{eg_int_s} [cite] exceed the
  objective values of exactly feasible points by at least 4.33\%, 7.48\% and
  80.5\%. Assuming that the \texttt{.nl} file of QPLIB\_8803 encodes the
  MINLPLib model \inst{optcdeg2}, MINOTAUR~0.4.1's infeasibility report for
  it is contradicted by an exactly feasible point."
- `:99` "…, all 109 finite final dual bounds are weaker than our certified
  bounds; 79 of them refer to the same model as a certified bound and carry a
  globality guarantee, and five improve the best listed dual
  (\cref{sec:solvers-campaign})."
- `01:100` "Only BARON's runs on \inst{camshape100} and \inst{camshape200}
  ended with a relative gap of at most $10^{-6}$: …"; `08:25` likewise.

### 9. [minor] §1.4: the reason for not running an interval solver is muddled

`sections/01-introduction.tex:123`

**Problem.** "its bounds would need the same exact existence proofs for points
that our certificates supply" says that bounds need existence proofs.
What would need them is a closure from such a solver.

**Fix.** "We did not run such a solver; a closure from it would still need
exact existence proofs for points, which \cref{sec:points} supplies."

### 10. [minor] Remaining repetition (round-1 item 52)

`sections/01-introduction.tex:64, 94`; `11-conclusion.tex:22, 36`

**Problem.** §1 states the traced SCIP mechanism twice: observation 3 (`:64`)
and C3 (`:94`, with the full cube example). §11 states it again (`:36`).
The `camshape` deficit with "0.61 n²ε" and "87%" appears in §1 (`:63`),
Proposition 5.4, §8.1 (`:41`) and §11 (`:22`, a 55-word sentence). The home
of the deficit is §5.1 and of the SCIP mechanism §8.2 (adjudication §0
rule 6). §1 is about 0.6 page over its target.

**Fix.**

- `01:94` shorten to: "In the 15 instrumented wrong runs, reverse
  propagation declares infeasible a node that contains a witness, because
  $\fl(0.7)^3<\fl(0.343)$ although $0.7^3=0.343$
  (\cref{lem:scip-cube,obs:scip-propagation})."
- `11:22` replace by: "On \inst{camshape}, points that violate each row and
  bound by at most $\varepsilon$ can lie up to $D_n(\varepsilon)$ below the
  optimum (\cref{prop:camshape-deficit}), and listed points of
  \inst{camshape400}, \inst{camshape800} and \inst{lnts50} lie below their
  exact optima (\cref{tab:claims})."

### 11. [minor] §2.2: "which other data need not satisfy"

`sections/02-semantics.tex:117`

**Problem.** "Parts (a) and (b) follow from $\feas\subseteq\mathcal F'$, which
other data need not satisfy" says that data satisfy an inclusion. What is
meant is that a feasibility test on other data can reject exactly feasible
points.

**Fix.** "Parts (a) and (b) need only $\feas\subseteq\mathcal{F}'$. A
feasibility test on binary64 data can reject exactly feasible points at very
tight tolerances, so that this inclusion fails; for the witnesses against
SCIP we therefore record that SCIP's own check accepts them
(\cref{prop:scip-witnesses})."

### 12. [minor] §2.4: "toward the infeasible side"

`sections/02-semantics.tex:143`

**Problem.** A dual bound has no feasible or infeasible side, and the reader
must translate "infeasible side" and "feasible side" into down and up.

**Fix.** "Dual bounds are rounded down and primal values up (reversed for
maximization), so that each display is itself a valid bound."

### 13. [minor] §2.5: three odd word choices

`sections/02-semantics.tex:152, 161, 169`

**Fix.**

- `:152` "No proof of record assumes …" → "No proof in this paper assumes …".
- `:161` "also pad library values of exponentials and integer powers" →
  "also widen library values of exponentials and integer powers by explicit
  error margins". "Pad" is defined only in S5.
- `:169` "each certifying code enters the data exactly, through outward
  enclosures, or as correctly rounded binary64 values …" → "each certifying
  code reads the data exactly, as outward enclosures, or as correctly rounded
  binary64 values … (the data readings of \cref{app:semantics-codes})". This
  matches the defined term "data reading".

### 14. [minor] §2.6: one unclear referent, one mixed paragraph, one tangled clause

`sections/02-semantics.tex:189, 193, 204`

**Problem.** Line 189, "Apart from these exceptions", has no antecedent. The
paragraph never calls anything an exception, and reading the first code is
allowed by the definition. Line 193 defines replay and regeneration at the
head of the paragraph that introduces the three status words, so two
unrelated definitions share one paragraph. Line 204, "MINLPLib's listed
points have small residuals under our readers, which a misread coefficient
that matters at those points would destroy", nests a relative clause in a
relative clause.

**Fix.**

- `:189` "Apart from these shared components and the \inst{ann_cumene_tanh}
  case, every computer-assisted dual certificate has …" (Table 1 gives `ann`
  the separate status "second written after reading the first").
- `:193` end the paragraph after this sentence. Start a new paragraph with
  "We use three words for the status of a statement."
- `:204` "MINLPLib's listed points have small residuals under our readers; a
  misread coefficient that matters at those points would make these
  residuals large."

### 15. [minor] §3: an announcement and circular glosses

`sections/03-results.tex:15, 53, 64, 76`; `05-other.tex:9`

**Problem.**

- `:15`, "We first explain how we chose the 43 instances.", only announces
  the next subsection, whose title says the same (style guide: no sentences
  that only announce).
- `:53` still glosses the classes by their names: "*comparison*, a
  comparison theorem along a chain"; "*convexity*, global duality or
  convexity". Round-1 item 7 fixed this in the §5 opening only. The two
  glosses should agree.
- `:64` "\cref{tab:kan} encloses the optimal values": a table does not
  enclose.
- `:76` "*listed solve* (a listed solve that cannot be checked)" is circular.

**Fix.**

- `:15` delete.
- `:53` "*staged*, a split along the stages of the model (\cref{sec:split});
  *comparison*, a discrete Sturm comparison along a chain of rows; *dense
  rows*, a Lagrangian over a few dense coupling rows; *convexity*, SDP
  duality, hidden convexity or concavity on a polytope; *identity*, rows that
  force the objective value; and *reduced space*, branch and bound over a few
  inputs with enclosures that keep cancellation (\cref{sec:other})." In
  `05:9`, optionally put each gloss before its instances ("*comparison*, a
  discrete Sturm comparison along the chain of curvature rows, for
  \inst{camshape} (\cref{sec:other-camshape}); …"), so that the gloss no
  longer reads as a description of the instance.
- `:64` "…, and \cref{thm:kan-enclosure} encloses the optimal values of two
  related models, $\RP$ and its network relaxation $\Rnet$
  (\cref{tab:kan})."
- `:76` "*listed solve* (a benchmark page lists a solver as solving the
  instance or a copy, without a value or log that we can check)".

### 16. [minor] §4.5 and Table 7 disagree on the `waterno2` tiers

`sections/04-split.tex:324` against `10-reproducibility.tex:62, 64`

**Problem.** §4.5 says "the searches replay in Tier~3 (hours to tens of
CPU-hours)". Table 7 puts the period bounds of `waterno2_09` and
`waterno2_12` in Tier 2 (35 and 49 min), and only `waterno2_18`,
`waterno2_24` and the `waterno2_06` pair bounds in Tier 3. `build-r3.md` §3
item 3 made the same correction in the B8 box but not in §4.5.

**Fix.** "…; the searches replay in Tier~2 for \inst{waterno2_09} and
\inst{waterno2_12} and in Tier~3 for the others (hours to tens of CPU-hours),
the combination in seconds."

### 17. [minor] §4.3 `optcdeg2`: "There … at this point" and a new term

`sections/04-split.tex:222–223`

**Problem.** "There the stage residual of the costate-affine split is not
minimized at this point": "There" refers to the arcs, "this point" to "our
exactly feasible point" two sentences earlier, and "costate-affine split" is
a new compound for the split defined in the preceding sentence.

**Fix.** "With the discrete costates $(p^y_t,p^v_t)$ as slopes, the stage
residual of the affine split contains $-b\,p^v_{t+1}v_t^2$, which is concave
in $v_t$ where $p^v>0$, that is, on both $u=-\frac15$ arcs. On these arcs our
point does not minimize the stage residual, so this affine split is not
exact; a floating-point evaluation with refined costates puts its bound about
0.6258 below the optimal value."

### 18. [minor] §4.3 `chain`: "the heights … through the heights"

`sections/04-split.tex:247`

**Problem.** "The linear rows express the heights and slopes through the
heights $z_1,\dots,z_N$" uses "heights" for two different variables. The
round-1 text that introduced this was mine.

**Fix.** "The linear rows express the variables $x_i$ and $u_i$ through the
vertex heights $z_1,\dots,z_N$ of a polyline over a fixed horizontal mesh;
its two end pieces depend only on $z_1$ and $z_N$
(\cref{lem:chain-polyline})."

### 19. [minor] Certificate sentences in two styles

`sections/04-split.tex:167, 209, 236, 255, 272, 297–298` against
`05-other.tex:67, 118–119, 175, 217`

**Problem.** §4 writes full sentences ("…; its evidence level is
\evid{hand}+\evid{stored}, and it replays in Tier~1."). §5 switches to
fragments ("evidence level \evid{rerun}; Tier~1 (258~s and 77~s)."; at
`:119` even "\evid{stored}; Tier~1." without "evidence level"). These
sentences replace the certificate boxes (`terminology.md` §6), so they should
read alike.

**Fix.** Use the §4 form in §5, for example `05:119` "For \inst{pricing050}
two codes reproduce the bound and one code checks the point; its evidence
level is \evid{stored}, and it replays in Tier~1." Treat `:67`, `:118` and
`:175` likewise.

### 20. [minor] §5.4: "as checks that it does not use"

`sections/05-other.tex:248`

**Fix.** "The proof is at evidence level \evid{hand}
(\cref{app:small-hvycrash}). Computer checks confirm it but are not part of
it: two codes checked the first witness and a third code a second witness in
60-digit \arith{I}, and three codes, with two separately written readers,
matched the stored rows."

### 21. [minor] §5.5: "The first implementation's search … is a second complete certificate"

`sections/05-other.tex:281` (same wording in `B7-eg.tex:344`)

**Problem.** For `eg` the displayed bounds come from the separately written
re-certifier (`:276`). Calling the first implementation "a second complete
certificate" crosses the defined words "first" and "second" of §2.6.

**Fix.** "The first implementation, the search that proposed the leaves, also
certifies on its own, in outward-rounded interval arithmetic without library
functions, the bounds for \inst{eg_int_s} and \inst{eg_disc_s} and for the
part of \inst{eg_disc2_s} with $x_7\in[24,27]$, the last under a side
condition on its LP multipliers (\cref{tab:eg-matrix})."

### 22. [minor] §5.5: one 75-word sentence defines both KAN relaxations

`sections/05-other.tex:317`

**Fix.** "So every number is a valid but vacuous dual bound for the OSIL
models, and we bound two relaxations instead. $\RP$ is the OSIL model without
the partition-of-unity rows. The network relaxation $\Rnet$ has as points
the pairs $(u,k)$ of an input $u$ in the box of the model and a knot choice
$k$ that put every edge argument in its interval and every hidden value in
its box; its objective is the network output $F(u,k)$."

### 23. [minor] §7.1: "slack" and "both rules" are still cryptic (round-1 item 42)

`sections/07-audit.tex:28`

**Problem.** "The screen used a slack of half a unit; … both rules give the
same classes" does not say what the slack was used for, or which two rules
are meant. The meaning is in `E-audit.tex:32`: the audit implementation drew
the line between (i) and (i-r) at half a unit.

**Fix.** "The audit implementation drew the line between classes (i) and
(i-r) at half a unit instead of one; since no margin of a flagged pair lies
between $0.44\,\dunit{s}$ and $1.115\,\dunit{s}$, both lines give the same
classes (\cref{app:audit-screen})."

### 24. [minor] §7.2–§7.4: three awkward constructions

`sections/07-audit.tex:60, 69, 79`

**Fix.**

- `:60` "An exact symbolic comparison by one implementation, rerun from a
  clean copy in a separate agent session, proves the two forms identical for
  14 of the 15 class (i) instances; the refutation on \inst{methanol50} holds
  for both forms (\cref{app:audit-history})." (A comparison is not "proved
  by" an implementation.)
- `:69` "Each refutation was proved a second time by one of two further
  checkers, written separately from the audit code and from each other, each
  with its own OSIL reader (\cref{tab:audit-second})."
- `:79` "We only group the margins by their size relative to $|\dval{s}|$
  and attribute no cause (\cref{fig:audit-margins}): …" ("only" now
  modifies the verb, as meant).

### 25. [minor] §8: a garden-path sentence, two overlong sentences, and no lead-in to Proposition 8.1

`sections/08-solvers.tex:28–29, 44, 103, 135`

**Problem.** `:103`, "One run that was not instrumented first loses the
witness at a $0.85$ station", reads first as "not instrumented first".
`:44` (65 words) ends with the main point, "which are different models with
their own exact optima". `:135` packs the whole protocol into 67 words.
§8.1 starts with Proposition 8.1 right after the heading (round-1 item 45
offered an optional lead-in).

**Fix.**

- `:103` "One further run, which was not instrumented, loses the witness first
  at a $0.85$ station; we do not link it to the mechanism. Two runs with
  small excess were not traced."
- `:44` "MINOTAUR~0.4.1 and ANTIGONE~1.1 report the optimal values $-4.2774$
  and $-4.284302$ in Mittelmann's QPLIB benchmark [cite] for
  \inst{QPLIB_3177} and \inst{QPLIB_2738}. These are QPLIB's copies of
  \inst{camshape800} and \inst{camshape100}, with constants rounded to 8 to
  10 significant digits [cite], and so different models with their own exact
  optima (\cref{prop:camshape-copies})."
- `:135` "We ran BARON~26.5.27, Gurobi~13.0.2 and SCIP~10.0.3, as bundled with
  GAMS~54.3.1, on the unmodified MINLPLib GAMS files of all 43 instances;
  later patch releases of BARON and Gurobi were not tested. Each run used one
  thread, a limit of 3600\,s (CPU time for BARON, wall time for the others),
  requested absolute and relative gaps of $10^{-9}$, no option file and a
  memory cap of 8192\,MiB, on a shared machine (\cref{app:solvers-protocol})."
- Before `:29`: "Among current solver runs, BARON's optimality claims on
  \inst{camshape100} and \inst{camshape200} come closest to a closure."

### 26. [minor] §9: a redundant hedge and "bag" (round-1 item 31)

`sections/09-interpretation.tex:48, 57`

**Problem.** `:48`, "this is our explanation, not a measurement", repeats
the caveat of `:19`–`:20` ("which we did not test by experiment"; "no
certificate depends on this section"), which already covers the whole
section. `:57` uses the formal word "bag", where round 1 and the §4.5 title
use "stage".

**Fix.** `:48` delete the clause after the semicolon. `:57` "They have the
staged structure, but each stage is a period of 166 variables, 9 of them
binary, which we interpret as too large for tight stage bounds; …".

### 27. [minor] §10: "a deterministic search" is narrower than the evidence level it describes

`sections/10-reproducibility.tex:36`

**Problem.** §2.5 (`02:164`) defines \evid{rerun} as rerunning "a search or
the numerical computation that produced its data". §10 says replay at this
level "reruns a deterministic search … in which an LP solver only proposes
multipliers". That does not fit `catmix`, whose rerun recomputes per-stage
chord values without an LP solver (`04:272`).

**Fix.** "…; at level \evid{rerun} it reruns, from the stored inputs, the
deterministic search or computation whose results are not stored; where an
LP solver takes part, it only proposes multipliers that are then checked
rigorously."

### 28. [minor] §11: filler, a clumsy italic, a vague "much" and a missing verb

`sections/11-conclusion.tex:16, 39, 41, 53`

**Fix.**

- `:16` "The recommendations below are proposals, each tied to its evidence;
  precedents …" → "The recommendations below are proposals; precedents …".
- `:39` "\emph{Exploit stage structure, and keep cancellation when bounding
  sums of many similar terms.} This proposal is untested; for circumstantial
  evidence see \cref{sec:interpretation-evidence}." (The current italic
  imperative is interrupted by a parenthesis.)
- `:41` "were much looser than" → "were 44 to 151 times looser than"
  (numerical evidence, `05:267`).
- `:53` "and statements about listed data the pages fetched on the dates of
  …" → "and statements about listed data concern the pages fetched on the
  dates of …".

### 29. [minor] Table 5 caption: "evidence was feasible" and a repeated sentence

`tables/tab-points.tex:8, 11` (via `make_points_table.py`)

**Problem.** "The 13 closures whose earlier primal evidence was feasible only
within a tolerance" makes evidence feasible (the round-1 item 13 error, in a
new place). The last caption sentence repeats `06-points.tex:68` word for
word (G3 open item 2).

**Fix.** "The 13 closures whose earlier points were feasible only within a
tolerance." Delete the last caption sentence.

### 30. [minor] Small term variants

`sections/*` (main); `A-semantics.tex:36–40`; `06-points.tex:69`

**Problem and fix.**

- "best listed dual" (defined, `02:60`; six uses: `01:99`, `02:60`, `02:64`,
  `03:43`, `03:55`, `03:56`) and "best listed dual bound(s)" (nine uses:
  `00:8`, `01:9`, `01:39`, `01:46`, `04:319`, `05:68`, `07:96`, `08:142`,
  `09:34`) alternate. Pick one. "best listed dual bound" is clearer; then
  change the definition at `02:60` and `terminology.md`.
- A.2 defines "an *exact* reading", "an *outward* reading" and so on, and
  then says "Four data readings occur". Write "an *exact* data reading" and so
  on at `:36–40`, so that "exact reading" cannot be confused with reading (b),
  "decimals read exactly".
- `06:69` "As far as we found (\cref{app:literature})" → "To our knowledge,
  within the search of \cref{app:literature}", the qualifier used everywhere
  else.

### 31. [minor] Supplement front matter and section openings

`sections/B1-lnts-lukvle10.tex:20`; `B2-dtoc5-optcdeg2.tex:24`;
`B3-camshape.tex:6`; `B4-chain-catmix.tex:6`; `B5-small.tex:8`;
`B6-powerflow.tex:4`; `B7-eg.tex:10–12`; `D-literature.tex:15`

**Problem.** The front matter (`supplement.tex:45–48`) and the opening of S1
(`B0`) are clear. Among the subsection openings:

- S1.3, S1.4, S1.5 and S1.6 are subsections but open with "This section …";
  S1.1 and S1.2 correctly say "this subsection" or name the content.
- S1.7 has no opening sentence; the subsection heading is followed directly
  by "Model and listed status".
- S1.1 has a paragraph headed "Listed status of Sections S1.1 and S1.2",
  which prints as a cross-reference used as a heading.
- `B2:24` "we read this as a sign that termwise relaxations … are weak" uses
  "read" in the interpretive sense that round 1 removed from the main text.
- `D:15` defines "floating-point closure" for the supplement only (see
  item 2).

**Fix.**

- `B3:6`, `B4:6`, `B5:8`, `B6:4`: "This section" → "This subsection".
- `B7`: after the `\subsection` line add "This subsection gives the model,
  the bounding lemmas, the computations and the exactly feasible points
  behind \cref{thm:eg-bounds}, and proves it; the rounding-error analysis is
  in \cref{app:egrounding}." (This matches the subsubsections at `B7:12`,
  `:78`, `:232`, `:296` and `:332`.)
- `B1:20`: "\paragraph{Listed status of the instances of
  \cref{app:lnts,app:dtoc5}.}" or "\paragraph{Listed status of the seven
  staged instances of S1.1 and S1.2.}"
- `B2:24`: "we take this as a sign …, which is an interpretation …".
- `D:15`: "A *floating-point closure* is defined in \cref{sec:semantics-cert};
  it is not a certificate in the sense of \cref{def:sem-certificate}."

---

## Not flagged

- Hedges are attached to their claims and are precise ("to our knowledge,
  within the search of …", "numerical evidence", "computed, one
  implementation"). The §9 and §11 caveats that LD-5 requires are kept;
  only the redundant one of item 26 is cut.
- No banned word, rhetorical question, "Moreover/Furthermore" chain, inline
  bold pseudo-heading or em dash occurs in the main sections.
- Appendix B (`G-proofs-split.tex`) reads cleanly; the explanatory
  paragraphs say so explicitly ("This is explanatory; no certificate uses
  it").
- The closing paragraph of §11 (`:64–67`) restates the three observations of
  §1 by design (G4-08); it adds the conclusion in its third sentence, so I do
  not flag it.
