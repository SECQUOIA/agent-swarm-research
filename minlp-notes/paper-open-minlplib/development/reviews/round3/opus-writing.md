# Writing review, round 3: final line-level check

Lens: plain, simple and precise language for an expert reader; generic
AI-style prose, filler, stacked hedges, announcements, restating summaries;
overlong or tangled sentences; undefined or inconsistent terms (against
`development/terminology.md`, `style-guide.md` and `outline.md` §8); sentences
an expert would misread; resolution of `round2/opus-writing.md`.

Scope: the main paper as built (`sections/00`–`11`, `A-semantics.tex`,
`G-proofs-split.tex`, and the captions of the tables and the figure that the
main paper prints), plus the openings of every supplement section and
subsection (`supplement.tex`, `B0`–`B10`, `C`–`J`). Line numbers refer to the
current files in `sections/`, `tables/` and `data/`.

Checks run (targeted and read-only; nothing was built, edited or committed
except this file; no repository script was run):

- `cat -n` of every main section and of the main-table captions; the first
  20–30 lines of every supplement section;
- `grep` over the main sections for the banned words of `style-guide.md`,
  filler words, em dashes, "independent", "authors'", "by hand"/"hand-written"/
  "on paper", "best listed dual" without "bound", "floating-point point",
  "duals", "same-model", "auditor"/"audited", "selection rule", "reading";
- a sentence-length scan, `/tmp/r3w/longsent.py` (sentences of 50 or more words
  after removing citations, references and inline math);
- an abstract word count with `sed`/`wc` (about 250 words);
- `pdftotext -layout` of the existing `build/main.pdf` (56 pages) and
  `build/supplement.pdf` into `/tmp/r3w/`, to see how passages render;
- for meanings: `D-literature.tex:240–295` (selection rule, width rule,
  funnel), `E-audit.tex:9–17, 164`, `F-eg-rounding.tex` (the auditor),
  `B2-dtoc5-optcdeg2.tex:221`, `B5-small.tex:431–510`, `B6-powerflow.tex:237–243`,
  `B8-waterno2.tex:257`, `data/make_tables.py:642, 1273, 1522`,
  `round2/adjudication.md` §10 (rejections R2-01 to R2-17).

No CI result was consulted.

## Verdict

**Minor revision of the writing.** Round 2 fixed almost every writing item:
the floating-point closure terms are defined in §2.2, the §3 and §5 glosses
agree, the `optcdeg2`, `chain`, `eg` and KAN passages are clear, the
certificate sentences of §4 and §5 read alike, and §9 and §11 are shorter.
No banned word, filler chain, rhetorical question or em dash remains. The
prose is plain, the hedges are attached to their claims, and Appendix B reads
cleanly.

What remains is local, but two items are definitional:

1. **Major.** §3.1 and §11 call the 155 instances "open by a selection rule
   stricter than MINLPLib's", but S3.4 defines that rule by the gap condition
   alone; the 155 also pass a width rule and an instance-list gap condition.
   The paragraph that carries the "not a solve rate" qualifier therefore
   misdescribes its denominator, and "width data" is undefined in the main
   text.
2. **Major.** The §2.6 definition of "verified by a separately written
   implementation" requires only "a second implementation", so the
   `ann_cumene_tanh` bound would qualify. Two sentences earlier the same
   section says that it does not. The definition of "proved" also treats
   `\evid{hand}` as if it were not an evidence level.
3. **Minor (20 items).** A few long or tangled sentences remain in §1 (the
   observations and C4) and in §7.4. An undefined "auditor" is used in the
   hypotheses of `thm:eg-bounds`. Some qualifiers drift ("which §8.3
   qualifies"), and a handful of one-line wordings an expert would stumble on
   remain.

Counts: 0 blocker, 2 major, 20 minor.

## Status of the round-2 items

| round-2 item | status | note |
|---|---|---|
| 1 §3.1 selection | resolved as asked | new residual on the funnel description, item 1 |
| 2 closure terms | resolved | `02:80–82`; `D:5` points there |
| 3 abstract | resolved | `00:8, 9, 11, 13` |
| 4 observation 3 | resolved | `01:63`; still 69 words, item 6 |
| 5 inverted syntax | resolved | `01:59`, `11:41` |
| 6 four long §1 sentences | resolved | `01:26–28`, `01:74–76`, `01:78–79`, `01:82` |
| 7 "floating-point points" | resolved | `06:6`, `06:66` |
| 8 C3 | resolved; 109 lead rejected (R2-16) | "which §8.3 qualifies", item 3 |
| 9 §1.4 interval solver | resolved in other words | `01:122` |
| 10 repetition | resolved | C3 no longer repeats the cube; `09:61` |
| 11–14 §2 | resolved | `02:117–118`, `:143`, `:152`, `:161`, `:169`, `:191`, `:195–197`, `:208` |
| 15 §3 glosses | resolved | `03:21`, `:60`, `:71`, `:83` |
| 16 `waterno2` tiers | resolved | tiers removed from §4–5 (R2-05) |
| 17 `optcdeg2` | mostly | "at this point" remains at `04:222`, item 11 |
| 18 `chain` heights | resolved | `04:243` |
| 19 certificate sentences | resolved | `05:66, 117–118, 173, 215–217, 246` |
| 20–22 §5 | resolved | `05:246–247`, `:279`, `:315–318` |
| 23–24 §7 | resolved | `07:28`, `:60`, `:69`, `:79` |
| 25 §8 | resolved; lead-in rejected (R2-06) | `08:60–61`, `:105–106`, `:139–140` |
| 26–28 §9, §10, §11 | resolved | `09:49`, `09:57`, `09:76–79`, `10:48`, `11:30` |
| 29 Table 5 caption | resolved | `tables/tab-points.tex:8–10` |
| 30 term variants | partly | prose uses "best listed dual bound"; A.2 reverts to "rounded reading" etc., item 10 |
| 31 supplement openings | resolved | every S1 subsection opens with its content; `B2:13`, `D:5` fixed |

---

## Major issues

### 1. [major] §3.1 and §11 misdescribe the 155 and leave "width" undefined

`sections/03-results.tex:48, 51`; `11-conclusion.tex:32`; `D-literature.tex:285`

**Problem.** `03:48` reads "41 lie among the 155 nonconvex instances that are
open by a selection rule stricter than MINLPLib's". S3.4 defines "open by our
selection rule" by the condition $g(p,d)>10^{-4}$ alone (`D:247`). The 155,
however, is the last row of a funnel that also requires the width rule (596 →
360) and an instance-list gap above $10^{-4}$ (360 → 294) (`D:250–272`). The
nonconvex instances that are open by the rule as S3.4 defines it are therefore
more than 155. `11:32` ("114 of the 155 open by our selection rule") and
`D:285` ("the remaining 146 instances open by our selection rule") repeat this
error. The main text also never says what the "width data" (`03:51`) and the
"computed widths" are. This paragraph carries the "not a solve rate"
qualifier (outline §8), so its denominator must be described exactly.

**Fix.** Replace `03:48–51` with:

> Of our 43 instances, 41 lie among the 155 nonconvex instances that pass our
> selection funnel: they are listed as open, meet a width rule (heuristic upper
> bounds on treewidth), and have relative gaps above $10^{-4}$ both in the
> instance list and between the best listed dual bound and the best listed
> point (\cref{app:literature-funnel} gives the rules, the funnel and its
> caveats). We chose the 43 in two rounds by judged tractability, the first 11
> before the rules were fixed, so the 29 closures among the 155 are not a solve
> rate. The other two closures, \inst{camshape100} and \inst{lnts50}, fail only
> the last condition: their best listed dual bounds were already within
> \sci{1.22}{-6} and \sci{3.9}{-5}, relative, of the best listed points and of
> our proved optima; for them what is new is the exact optimal value, its proof
> and an exactly feasible point. Three programs, written in at least two
> separate agent sessions, reproduce every funnel count from the saved pages
> and width estimates; no separate agent session reviewed the code that
> estimated the widths and applied the rules.

("Fail only the last condition" is from the funnel row "closed in the paper,
among the 294 but not the 155: 2".) At `11:32`, write "did not attempt 114 of
the 155 instances that pass our selection funnel". At `D:285`, write "from the
remaining 146 of the 155".

### 2. [major] §2.6 status definitions: "verified" does not require separate writing, and "proved" sets `\evid{hand}` apart from the evidence levels

`sections/02-semantics.tex:198–199` (compare `:188`, `tables/tab-trust.tex:13`)

**Problem.** `:199` reads: "verified by a separately written implementation
if, in addition, a second implementation reproduced its computer-assisted
part". The `ann_cumene_tanh` bound has a second implementation that reproduces
it. Under this wording it would be verified, yet `:188` and Table 1 say its
status is proved, not verified. `:198` reads "a pen-and-paper argument, or a
computer-assisted proof at one of the evidence levels of §2.5". This implies
that the evidence levels concern only computer-assisted proofs, but
`\evid{hand}` is one of them (`:164`). It also introduces a third name for that
level, next to "a proof written out in full" (`:164`) and "a written proof"
(`06:78`, Table 1).

**Fix.**

> It is \emph{proved} if a proof at one of the evidence levels of
> \cref{sec:semantics-trust} establishes it. It is \emph{verified by a
> separately written implementation} if, in addition, a separately written
> second implementation reproduced its computer-assisted part.

---

## Minor issues

### 3. [minor] C3 and the §8 opening: the qualifier of "the 30 other finite ones" is only a pointer

`sections/01-introduction.tex:97`; `08-solvers.tex:41`

**Problem.** "…are weaker than our certified bounds, and so are the 30 other
finite ones, which §8.3 qualifies". The sentence makes the claim and moves the
qualifier to §8.3 (style guide: "never let a qualifier drift away from its
claim"). Read literally, it is also imprecise: 18 of the 30 are values on the
KAN models, where our bounds concern $\Rnet$, not the stored model, and §8.3
compares them "only descriptively" (`08:145`). R2-16 kept the 79 in the lead,
"the 30 others follow with their qualifier"; the qualifier itself is missing.

**Fix.** At `01:97`:

> …, all 79 final dual bounds with a globality guarantee for the unmodified
> models of the non-KAN instances are weaker than our certified bounds, and
> five final dual bounds improve the best listed dual bound. \Cref{sec:solvers-campaign}
> discusses the 30 other finite bounds: values without a globality guarantee,
> bounds on models that SCIP modified, and values on the KAN instances, for
> which our bounds concern $\Rnet$.

At `08:41`: "…were weaker than our certified bounds (\cref{sec:solvers-campaign}
discusses the other 30), and only BARON's two optimality claims ended with a
relative gap of at most $10^{-6}$."

### 4. [minor] "The auditor" is undefined in a theorem's hypotheses, and "audit" now has two meanings

`sections/05-other.tex:268, 275`; `tables/tab-trust.tex:35` (generated, `data/make_tables.py:1522–1523`); `10-reproducibility.tex:70, 72, 74`

**Problem.** `thm:eg-bounds` assumes "the correctness of … the auditor". The
main text never defines it; it is the S5.4 program that checks the accuracy
of the library exponentials and powers. `:275` then speaks of "an audited
rerun", Table 1 of "audited exp and powers", and Table 7 of "audited leaf
re-certification". In this paper "audit" names §7, the audit of MINLPLib's
listed bounds, and `07:15` uses "26 audited" in that sense. An expert reading
Table 7 can take the `eg` rows for part of the §7 audit.

**Fix.** Define the term once in the theorem and qualify it elsewhere in the
main text:

- `05:268`: "…, the enclosure code, the accuracy auditor (a program that checks
  each library exponential and power value that the enclosure code uses;
  \cref{app:egrounding-auditor}), the exact arithmetic and the coverage
  checker, …".
- `05:275`: "an audited rerun checked this" → "a rerun under the accuracy
  auditor checked this".
- `make_tables.py:1522` (Table 1): "audited exp and powers" → "exp and powers
  checked by the accuracy auditor".
- `10:70, 72, 74` (Table 7): "audited leaf re-certification" → "leaf
  re-certification under the accuracy auditor".

### 5. [minor] Observation 1: a wrong connective and an unexplained exception; "split coordinates" in §9

`sections/01-introduction.tex:58`; `09-interpretation.tex:34`

**Problem.** `01:58` (58 words) joins "at most three-dimensional in 15 more" to
"although the `ex6_2_5` bound needed 131,111 two-dimensional boxes". The
contrast meant is few dimensions but many boxes. The sentence then sets
`pindyck` apart ("splits one box into 9") without saying why. The reason is
that its box lies in $\R^{112}$ (`B5:431`), which is also why R2-17 excludes it
from "low-dimensional". "Splits" is also the defined term of §4. `09:34` says
"these dimensions count split coordinates", which mixes the defined "split"
with branching coordinates.

**Fix.**

- `01:58`: "Once a bound fitted to the structure of the model was in place, 12
  closures needed no branching and 15 more branched in at most three
  dimensions, the \inst{ex6_2_5} bound with 131,111 two-dimensional boxes. The
  \inst{pindyck} certificate divides one box in $\R^{112}$ into 9 leaves, and
  the three \inst{eg} certificates branch on their 7 original variables, with
  up to 1,114,361 leaves."
- `09:34`: "these dimensions count the coordinates on which the certificate
  branches, not boxes".

### 6. [minor] Observation 3: one 69-word sentence and a cryptic "binary64 residual of decimal data"

`sections/01-introduction.tex:63–64`

**Problem.** `:63` joins two claims with "and" and then adds a colon clause
with two parentheses. In `:64`, "a binary64 residual of decimal data triggered
the error" does not say which residual. Without the cube example, which was
removed from C3 in round 2, an expert cannot decode it.

**Fix.**

> Some listed and published optimal values hold only within tolerances.
> Along long chains of coupled rows, a tolerance can lower the objective by far
> more than its own size: on \inst{camshape}, points that violate each row and
> bound by at most $\varepsilon$ lie at most $0.61\,n^2\varepsilon$ below the
> optimum (proved for the values $\varepsilon\le10^{-8}$ of
> \cref{tab:camshape-deficit}), and explicit tolerance-feasible points reach
> about 87\% of this bound (numerical evidence).
> SCIP~10 returns wrong optimal values on some subproblems; in the 15 wrong
> runs that we traced, the error is triggered by the decimal identity
> $0.7^3=0.343$, which fails after rounding to binary64
> (\cref{sec:solvers-invalid}).

### 7. [minor] C4 is one 88-word sentence

`sections/01-introduction.tex:102`

**Fix.**

> The archive that accompanies this paper (\archiveDOI) holds the models with
> their SHA-256 hashes, the certificate data, the exact point definitions, and
> the first and the separately written implementations. A number file gives
> the exact value, source and rounding direction of every generated certified
> display (bounds, primal ends, gaps and derived margins), and a claim register
> maps each result to its checkers and inputs. Replay commands come in three
> tiers of effort (\cref{sec:repro,app:repro}); the archive separates replay of
> stored certificates from regeneration, which may produce a different valid
> certificate (\cref{sec:semantics-protocol}).

### 8. [minor] §1: a non sequitur, a duplicated caveat, an announcement and an unexplained "verbatim"

`sections/01-introduction.tex:21, 53, 69–70, 81`

**Problem and fix.**

- `:21` "The solved mark is thus a consensus label, not a check." follows "No
  formula for the gap is documented", which does not imply it. Delete "thus",
  or move "No formula for the gap is documented." to the end of `:19`.
- `:53` "We built each dual bound individually for each instance" says
  "individually" twice, and `:69` states the same caveat one paragraph later.
  Write "We built each dual bound from the structure of its model and
  evaluated it …" and keep `:69`.
- `:70` "Within this scope we make the following contributions." only
  announces the list (style guide). Delete it; the C1–C4 labels introduce
  themselves.
- `:81` "it applies verbatim to `ann_cumene_exp`" gives no reason. Write "it
  also holds for \inst{ann_cumene_exp}, which writes $\tanh$ through $\exp$ and
  which SCIP and LINDO closed in floating point [cite]; our bound is weaker
  than their values."

### 9. [minor] Remark 2.1(1) says 17 instances were compared exactly; §2.6 says 21

`sections/02-semantics.tex:49` (against `:207` and Table A.1)

**Problem.** "Readings (a) and (b) define the same model for the 17 instances
whose forms we compared exactly, and differ for the four `catmix` instances"
reads as if `catmix` was not compared exactly. Table A.1 and `:207` give 21
exact comparisons: 17 identical and four `catmix` with differing rows.

**Fix.** "(1) Of the 21 instances whose GAMS and OSIL forms we compared
exactly, readings (a) and (b) define the same model for 17 and differ for the
four \inst{catmix} instances, whose OSIL files print … ; for the other 22, a
comparison at sample points found no difference (numerical evidence;
\cref{app:semantics-gams})."

### 10. [minor] Appendix A.2 drops "data" from the defined term "data reading" (round-2 item 30)

`sections/A-semantics.tex:41, 43–45`

**Problem.** A.2 now defines "exact/outward/rounded/binary64 data reading"
(`:36–40`), but `:43–45` return to "an exact, outward or rounded reading", "a
rounded reading", "Binary64 readings" and "exact or outward readings". Next to
readings (a)–(c), a "rounded reading" or "binary64 reading" is easily taken
for reading (c), which also means "the data rounded to binary64". `:41`, "does
so only for the data that the code actually uses", is also unclear about the
condition.

**Fix.** At `:43–45`, write "data reading" in all four places. At `:41`:
"Exact, outward and rounded data readings make the certificate valid for the
decimal data of \reading{b}. A binary64 data reading does so only if every
datum that the code uses is a binary64 number or is entered again exactly; we
checked this case by case."

### 11. [minor] §4: four wordings an expert would stumble on

`sections/04-split.tex:86, 207, 222, 304`

**Fix.**

- `:86` "Exact affine slopes are not free" can be read as "are costly". Write
  "The slopes of an exact affine split are determined by the model: at a
  minimizer whose bag components are interior points of the $K_t$, they are
  the copy-row multipliers, …".
- `:207` "\cref{thm:dtoc5-bracket} is a rigorous rational evaluation below the
  dual function" (a theorem "is" an evaluation). Keep the wording that outline
  §8 prescribes and fix only the subject: "The lower end in
  \cref{thm:dtoc5-bracket} is a rigorous rational evaluation below the dual
  function at $\hat\lambda$; we claim …".
- `:222` "slightly convex in $v$ at this point": "this point" could be the
  exactly feasible point of `:218` or the refined local solution of `:221`.
  `B2:221` says "at the trajectory" $\bar v$. Write "at the refined trajectory
  $\bar v$".
- `:304` "the exact shortest path is $39157472136693483/2^{47}$" → "the exact
  shortest-path value is …".

### 12. [minor] §5: five wordings

`sections/05-other.tex:67, 154, 169, 188, 330`

**Fix.**

- `:67` "for \inst{camshape100} and \inst{camshape200} the gain is in rigor"
  follows a listed gap of 8.27\% for `camshape200`, so the reader looks for
  the reason. Write "for \inst{camshape100} and \inst{camshape200}, which
  BARON closes at tolerance level in our runs (\cref{prop:baron-camshape};
  earlier results in \cref{sec:results-prior}), the gain is in rigor."
- `:154` "(a numerical observation)" → "(numerical evidence)", the term used
  everywhere else.
- `:169` "The stored \inst{powerflow0039p} certificate uses
  $\varepsilon=10^{-8}$; with its tiny angle-row multipliers set to zero, it
  needs no shift" says that the same certificate both uses a shift and needs
  none. Following `B6:238–243`, write: "The stored \inst{powerflow0039p}
  certificate uses $\varepsilon=10^{-8}$; setting its tiny angle-row
  multipliers to zero gives a certificate that needs no shift
  (\cref{rem:pf-anglefree}), so no trigonometric bound enters any of the three
  dual proofs."
- `:188` "The primal point fixes saved 17-digit decisions" → "The primal point
  fixes the decision variables at stored 17-digit values".
- `:330` "A review found" → "A code review in a separate agent session found"
  (`terminology.md`, "who checked").

### 13. [minor] Proposition 8.1(a) reads as a contradiction

`sections/08-solvers.tex:47`

**Problem.** "they lie below the exact optima by at least \sci{5.25}{-7} and
\sci{2.05}{-6}, and by at most \sci{1.23}{-7} and \sci{4.80}{-7} relative" puts
"at least" and a smaller "at most" on one verb. Only the final word "relative"
tells the reader that the second pair is a different quantity.

**Fix.** "(a) Both reported dual bounds are valid. They lie below the exact
optima by at least \sci{5.25}{-7} and \sci{2.05}{-6} in absolute terms, and by
at most \sci{1.23}{-7} and \sci{4.80}{-7} relative to the optima."

### 14. [minor] §8: "1,632 OSIL files" is unexplained, and "5 for $\Rnet$" is imprecise

`sections/08-solvers.tex:107, 147`; `D-literature.tex:292`; `E-audit.tex:16`

**Problem.** The main text counts 1,633 instance pages throughout, then scans
"the 1,632 OSIL files of the MINLPLib snapshot" (`:107`). The supplement gives
two different reasons for the missing file: `fct` "has a page but no OSIL
file" (`E:16`) and "its OSIL file was not in our cache" (`D:292`). At `:147`,
"(30 for OSIL models, 5 for $\Rnet$)" says that the solvers returned values
for $\Rnet$. They returned values for the stored KAN models, which we compare
with our lower bounds for $\Rnet$.

**Fix.**

- `:107` "A syntactic scan of the 1,632 cached OSIL files (every instance
  except \inst{fct}; \cref{app:audit-screen}) finds …". Make `D:292` and `E:16`
  give the same reason, after checking which is true.
- `:147` "(30 against our dual bounds for the stored models, 5 against our
  lower bounds for $\Rnet$ on KAN instances)".

### 15. [minor] §7.4 and §7.5: three tangled sentences and a repeated statement

`sections/07-audit.tex:87, 90, 91, 102`

**Problem and fix.**

- `:87` (55 words): "except that \inst{ghg_3veh}, after both of its bounds, wrote
  three products …" makes the instance the actor, and "nine instances added
  days before their 2014 bounds" is a garden path. Write: "Archived copies
  show that the models have not changed since before the refuted and (i-r)
  bounds were listed, with two exceptions. After both of its bounds, the file
  of \inst{ghg_3veh} was changed to write three products of constants as
  rounded decimals (relative change $\le\sci{1.84}{-15}$); the refutation also
  holds for the old file. Nine instances were added a few days before their
  2014 bounds and have no older copy (\cref{app:audit-history})."
- `:90`: "for \inst{spring} page rounding explains them" reads first as "spring
  page". Write: "The 12 class (i-r) bounds, on four instances, date from
  2013-09-17. On \inst{spring}, rounding on the page explains them
  (\cref{prop:spring-opt}). If stored as displayed, the six-digit bounds on
  \inst{eniplac}, \inst{lop97icx} and \inst{stockcycle} are invalid by far more
  than the display rounding; an unproved rounding to six digits before storage
  would explain them (\cref{app:audit-spring})."
- `:91` (69 words): split after "(category~A)" and start the second sentence
  with "On \inst{emfl050_3_3}, which is marked solved, the best listed dual
  bound lies more than MINLPLib's gap tolerance below the optimum; …".
- `:102` "which only the unproved six-digit rounding explains; no solved mark is
  contradicted" → "which are consistent only with the unproved six-digit
  rounding (\cref{app:audit-screen})". Delete the solved-mark clause, which
  `07:8` and `07:80` already state.

### 16. [minor] §7: three small precision points

`sections/07-audit.tex:27, 41, 71`

**Fix.**

- `:27` "Every bound with a positive margin has $\dval{s}\neq0$." does not say
  why this matters. Write "…, so its unit $\dunit{s}$ is defined."
- `:41` "almost all displayed values fit this rule" → "13,723 of the 13,847
  finite displayed values are consistent with this rule" (`E:164`).
- `:71` "These assume IEEE binary64 arithmetic for matrix products" → "These
  assume \cref{hyp:fp-ieee} for matrix products", the named hypothesis.

### 17. [minor] §9: a term used before its definition, and a recommendation that mixes fonts and claims

`sections/09-interpretation.tex:27, 29, 64, 65`

**Problem and fix.**

- `:27` uses "termwise relaxations", which `:29` defines two sentences later.
  Move `:29` directly after `:26`.
- `:64`: the italic recommendation is interrupted by a roman parenthesis and a
  roman phrase and then resumes in italics, the pattern that round 2 fixed at
  the old `11:39`. Write "\emph{Store each per-solver bound, rounded in the
  safe direction, with its provenance (solver version, options, tolerances,
  termination status); flag per-solver bounds that a listed point
  contradicts; and keep the three-solver aggregate.}"
- `:65` joins two unrelated reasons with "and". Write "Without provenance a
  contradicted display cannot be traced, as the class (i-r) bounds show
  (\cref{sec:audit-results}). The aggregate stayed consistent with every
  proved point except two six-digit instance-list entries
  (\cref{sec:audit-limits})."

### 18. [minor] §10: one 65-word sentence on regeneration

`sections/10-reproducibility.tex:51`

**Fix.** "For \inst{waterno2_18}, \inst{waterno2_24} and \inst{powerflow0030p},
regeneration gives weaker valid bounds, and the reported values rest on the
stored certificates. The \inst{topopt-cantilever_60x40_50} existence
certificate of the audit stores no basis, so it is regenerated rather than
replayed; regeneration proved another exactly feasible point, which also
satisfies its row of \cref{tab:audit-pairs}."

### 19. [minor] §11: an undefined "extended-value proofs" and a second wording of the human-check statement

`sections/11-conclusion.tex:26`

**Problem.** "The extended-value proofs of Appendix B" uses a phrase that the
reader of §11 has not met; only Appendix B's first sentence explains it.
"No human reviewer outside the authors has checked any proof" restates §2.6
(`02:179`, "No person outside the authors has checked the code or the
proofs") in other words.

**Fix.** "The proofs of \cref{app:splitproofs} and the \inst{eg} primal check
were rechecked by separate agent sessions; no person outside the authors has
checked the code or the proofs (\cref{sec:semantics-protocol})."

### 20. [minor] Table 3 caption: "one slope per separator on a 113–162-cell partition"

`tables/tab-unclosed.tex:11` (generated, `data/make_tables.py:642`)

**Problem.** "one slope per separator" and "a cell partition" seem to
contradict each other, and §4.5 mentions no intermediate bound. Per `B8:257`,
the intermediate bound used one slope vector per separator, with pair bounds
over 113 to 162 cells per separator.

**Fix.** "272.584700 (one slope vector per separator, with pair bounds over
113--162 cells per separator, $\delta\le3.78\%$)".

### 21. [minor] "Same-model" and "duals" in the abstract and the Figure 1 caption

`sections/00-abstract.tex:13`; `03-results.tex:30`

**Problem.** "All 79 same-model one-hour BARON, Gurobi and SCIP dual bounds
with a globality guarantee" piles four modifiers in front of the noun, and
"same-model" (also "same-model bounds" in the Figure 1 caption) is defined
nowhere. The caption also uses "duals" as a noun in prose ("Certified and
listed duals"). The terminology rule allows the short form only in headers
and legends.

**Fix.**

- `00:13` (same word count): "All 79 globally guaranteed one-hour BARON,
  Gurobi and SCIP bounds on the same models were weaker than ours; …".
- `03:30`: "(a)~Certified and listed dual bounds refer to the stored model;
  among the one-hour values, only filled triangles are bounds with a
  globality guarantee for the unmodified stored model."

### 22. [minor] Other names for the `\evid{hand}` level

`data/make_tables.py:1273` (Table 1, `hvycrash` row); `sections/10-reproducibility.tex:43`; `J-displays.tex:11`

**Problem.** Besides `02:198` (item 2), Table 1 says "identity on paper", and
§10 and S7.5 say "hand-written tables". `terminology.md` keeps "hand" for the
evidence level and asks for "a written proof" in prose. A reader may connect
"hand-written tables" with `\evid{hand}`.

**Fix.** Table 1: "written proof of an identity, checked in \arith{E}". §10
and S7.5: "tables typed in the LaTeX sources" instead of "hand-written tables".

---

## Not flagged

- Hedges are attached to their claims and are specific ("to our knowledge,
  within the search of …", "numerical evidence", "computed, one
  implementation"). The interpretive caveats of §9 occur once, in its opening.
- No banned word, "Moreover/Furthermore" chain, rhetorical question, inline
  bold pseudo-heading or em dash occurs in the main sections. Filler words are
  absent apart from the items above.
- The long sentences that remain after the items above are definitions or
  lists (the arithmetic tags at `02:151`, the evidence levels at `02:164`, the
  class glosses at `03:60`, the citation list at `01:127`, the Table 7 cells),
  where splitting would not help.
- "Bag" and "stage" name the same object in §4.1 and Appendix B. `04:42`
  defines the second name explicitly, so I do not flag it.
- The AI-use sentence (`02:177`, `11:53`) is long but is the agreed
  disclosure (LD2-2) and reads clearly.
- §11's closing paragraph restates the three observations of §1 by design and
  adds the conclusion in its third sentence.
- Appendix B (`G-proofs-split.tex`) reads cleanly; every proof step names the
  fact it uses.
- Supplement front matter and section openings: every S1 subsection opens with
  a sentence that names its content (`B1:3–4` to `B10:3`); S2 to S7 open with
  their scope or reading convention. `B2:13` and `D:5` now carry the round-2
  wording.
- Placeholders (authors, funding, competing interests, licence, archive DOI,
  "[authors to confirm …]") are expected and not flagged.
