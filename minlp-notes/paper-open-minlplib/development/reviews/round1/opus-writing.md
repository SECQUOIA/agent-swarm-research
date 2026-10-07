# Writing review, round 1: main paper (line level)

Reviewer lens: plain, simple and precise language for an expert reader;
AI-style prose; long or tangled sentences; undefined or inconsistent terms
(against `development/terminology.md`); unclear paragraphs and transitions;
section openings.

Scope: `main.tex` as built, that is, `sections/00`–`11`, `A-semantics.tex`
and `G-proofs-split.tex` (printed as Appendix B), plus the captions of the
tables that the main paper prints. The supplement was not reviewed. Line
numbers refer to the current files in `sections/`.

Checks run (targeted, read-only; nothing was built or edited except this
file):

- `cat -n` of every main-paper section and of the table captions;
- `grep` for the banned words of `style-guide.md`, for intensifiers and
  hedges, for em dashes, and for the terms in `terminology.md` ("reading",
  "class", "family", "bag"/"stage", "authors'", "instance list", "verified",
  "computed", `\dunit`);
- a sentence-length script in `/tmp/opusw/longsent.py` that flags source
  lines of 40 or more words after removing citations, references and inline
  math;
- `pdftotext -layout build/main.pdf` (existing build, not rebuilt) to see
  where headings and floats fall;
- to confirm what a passage means before rewriting it, reading the matching
  passages of `B4-chain-catmix.tex`, `B7-eg.tex`, `B9-ann-kan.tex`,
  `D-literature.tex`, `E-audit.tex` and `development/dossiers/dtoc5-optcdeg2.md`;
- `grep` that every label in the suggested rewrites exists.

## Verdict

**Minor revision of the writing.** The prose is mostly plain and direct, and
an expert can follow it. None of the banned words occurs. There are no em
dashes, no rhetorical questions and no "Moreover/Furthermore" chains. Hedges
are almost always attached to the claim they qualify. The remaining problems
are concentrated in a few places:

1. Some defined terms overlap or collide. The three status words of §2.6
   overlap. "Reading" has five meanings. "Class" has three meanings. "The dual
   bound in the instance list" is used but never defined.
2. Three passages are tangled: the exceptions to separately written code in
   §2.6, the `chain` outline in §4.3 (undefined symbols) and the
   `optcdeg2` motivation in §4.3.
3. Section openings: §3 has none. The opening of §5 is a 51-word list with
   circular glosses. The openings of §7, §8 and §9 do not state their result
   or thesis.
4. The opening of §4 describes the `catmix` certificate with a mechanism that
   §4.1 says it does not use (outline §8.8).

Counts: 0 blocker, 8 major, 44 minor.

---

## Major issues

### 1. [major] The three status words of §2.6 overlap and are hardly used

`sections/02-semantics.tex:204`

**Problem.** The sentence defines *proved* ("possibly including the check of
a stored certificate"), *verified by a separately written implementation*
and *computed* ("one implementation produced it"). Every computer-assisted
proof with one implementation is both proved and computed. Examples are the
displayed duals of `lukvle10`, `catmix` and `etamac`, and the
`etamac`/`pricing050` primal claims (`06-points.tex:82`). The parenthesis
also omits proofs at level `\evid{rerun}`. Later text uses the words
inconsistently:

- `A-semantics.tex:99–100` labels a result "computed, one implementation" and
  then says "we do not claim it";
- `07-audit.tex:59` uses an equally single-implementation exact comparison
  ("one implementation") as the basis of a claim, the extension of the
  refutations to the GAMS form.

The style guide says to use these words exactly. Readers cannot do that with
categories that overlap.

**Fix.** Replace line 204 with:

> We use three words for the status of a statement. It is \emph{proved} if
> a pen-and-paper argument, or a computer-assisted proof at one of the
> evidence levels of \cref{sec:semantics-trust}, establishes it. It is
> \emph{verified by a separately written implementation} if, in addition, a
> second implementation reproduced its computer-assisted part. It is
> \emph{computed} if a single implementation produced it and we do not
> present it as proved; we label such statements with this word and do not
> use them as premises. Interpretation, like numerical evidence, never
> supports a claim.

Then align `07-audit.tex:59`. Either write "proved by one implementation" (an
exact symbolic comparison is a proof) or label it "computed" and present the
GAMS-form extension as unclaimed, as `A-semantics.tex:100` does for binary64
data.

### 2. [major] The exceptions to "separately written" are hard to count

`sections/02-semantics.tex:191–196`

**Problem.** The paragraph opens with "Named shared components are *the*
exception", lists two components ("These are …"), adds "A third is …", and
then introduces "the *other* exception" (the `ann` code whose author read
the first code). A reader has to count to find that there are two kinds of
exception and three shared components. This is the paragraph that qualifies
the paper's main verification claim (outline §8.10), so it must read without
effort.

**Fix.** Replace lines 191–196 with:

> The \emph{first implementation} of a certificate produced it, and a
> \emph{second implementation} checked it; the supplement calls them the
> authors' code and the verifier's code. The second is \emph{separately
> written}, that is, written without importing or reading the first, with
> two exceptions. First, some components are shared: mpmath where
> \cref{tab:trust} lists it, one rigorous exponential and interval core used
> by both KAN bounding codes, and one OSIL reader used by several decoders (a
> separately written reader reproduced its output exactly for
> \inst{ann_cumene_tanh} and the KAN instances). Second, the second bounding
> code for \inst{ann_cumene_tanh} does not import the first, but its author
> read the first in full (\cref{app:annkan-ann-verif}).

### 3. [major] "Reading" has five meanings, two of them in one sentence

**Problem.** "Reading" is the paper's word for the three models (a), (b) and
(c) (`02-semantics.tex:40–44`). It is also used for:

- the four ways a code enters the data (exact, outward, rounded and binary64
  readings): `A-semantics.tex:37–43`, the "Data reading" field of every
  certificate box, and the `tab:trust` column;
- code inspection: "reading the code showed" (`02-semantics.tex:183`) and
  "Reading the codes also found" (`A-semantics.tex:48`);
- OSIL readers, in the sense of parsers;
- interpretation: "In our reading" (`09-interpretation.tex:52`, `:65`,
  `11-conclusion.tex:74`), "a simple reading" (`09:41`) and "The same reading
  applies" (`09:64`), together with the subsection title "Reading"
  (`09:48`).

The worst case is `A-semantics.tex:43`: "Exact, outward and rounded readings
prove the statement for \reading{b}". `terminology.md` fixes the data-reading
labels, but not the interpretive and inspection uses.

**Fix.**

- §9 and §11 (required):
  - `09:48` `\subsection{Interpretation}`;
  - `09:41` "do not fit a simple explanation";
  - `09:52` "In our interpretation, termwise relaxations …";
  - `09:64` "The same interpretation applies, with less force, …";
  - `09:65` "…, which we interpret as too large for tight stage bounds";
  - `11:74` "and, in our interpretation, which we did not test by
    experiment, …".
- Code inspection (required):
  - `02:183` "inspection of the code showed that each certifying code enters
    the data exactly, …";
  - `A:48` "Inspecting the codes also found a latent error: …".
- `A-semantics.tex:43` (at least) "Exact, outward and rounded data readings
  make the certificate valid for the decimal data of \reading{b}; a binary64
  data reading does so only for the data that the code actually uses, which
  we checked case by case."
- Better: rename the code-level notion "data entry" (exact, outward, rounded
  and binary64 entry). This would apply to the certificate-box field, the
  `tab:trust` column (through `make_tables.py`) and §A.2. "Reading" would
  then mean only (a), (b) and (c).

### 4. [major] The §4 opening ascribes the split mechanism to `catmix`

`sections/04-split.tex:8–10` (also `01-introduction.tex:63`)

**Problem.** The opening names all fifteen staged closures, including
`catmix100`–`catmix800`, and then describes one mechanism. In that
mechanism, a function of the shared variables is added to one stage and
subtracted from the next, and "the sum of the stage minima is a dual bound".
Line 70 says the opposite for `catmix`: "\cref{lem:split-minorant} is not
an instance of \cref{lem:split-bound}". Validity there rests on concavity of
the true value functions. Outline §8.8 forbids implying that all staged
certificates are instances of Lemma 4.1. The sentence is also in the passive
voice ("The model is cut …, and a function … is added").

**Fix.** Replace lines 8–10 with:

> Fifteen of the 31 closures form the staged class of \cref{tab:closures}:
> \inst{lnts50}--\inst{lnts400}, \inst{dtoc5}, \inst{optcdeg2},
> \inst{lukvle10}, \inst{chain50}--\inst{chain400} and
> \inst{catmix100}--\inst{catmix800}; the \inst{waterno2} bounds use the
> same idea. We cut the model along its stages, add to each stage a function
> of the variables that it shares with the next stage, and subtract the same
> function from the next stage, so that these terms cancel at every feasible
> point. If each stage problem can be minimized rigorously, the sum of the
> stage minima is a dual bound. The \inst{catmix} certificates use a
> variant: they bound the value functions of the stage recursion from below,
> and their validity rests on concavity of the true value functions
> (\cref{lem:split-minorant}).

At `01-introduction.tex:63` (lesson 2), append "or of the value functions
of the stage recursion" after "a split of the objective along the stage
structure of the model".

### 5. [major] The `chain` outline uses symbols and terms it does not define

`sections/04-split.tex:269–274`

**Problem.** An expert cannot follow these lines without the supplement.

- The end values $z_1,z_N$ appear without definition; the model was stated
  in heights $x_i$ and slopes $u_i$.
- $H$ in $G_H$ and $c_H$ is used before "for all $V$ and $H>0$" reveals that
  it is a free parameter.
- "Here the height multiplier is the cumulative length" uses an undefined
  "height multiplier". In the summation by parts, the cumulative length
  multiplies each height difference.
- "effectively reverse convex" hedges a plain fact: the length row is an
  equality of a convex function.

**Fix.** Replace lines 269–274 with:

> The linear rows express the heights and slopes through the heights
> $z_1,\dots,z_N$ of a polyline over a fixed horizontal mesh; its two end
> pieces depend only on the end values $z_1$ and $z_N$
> (\cref{lem:chain-polyline}). Summation by parts then writes the objective
> with the cumulative length $v$ of the polyline as a second state, started
> at a free value $V$. For a parameter $H>0$ let
> $G_H(v)=\frac12\bigl(v\sqrt{H^2+v^2}+H^2\operatorname{asinh}(v/H)\bigr)$
> and $c_H=2G_H(1/(2N))$. For the split $\varphi_k(z,v)=G_H(v)-vz-k\,c_H$,
> a closed-form inequality makes every interior stage residual nonnegative,
> with equality exactly on discrete catenaries
> (\cref{lem:chain-calibration}). So the objective is at least an explicit
> function $B_N(z_1,z_N;V,H)$ of the end values, for all $V$ and all $H>0$
> (\cref{prop:chain-endvalue}). In this split the multiplier of each height
> difference is the cumulative length, which varies with the configuration
> as the tension of a real chain does. A fixed multiplier on the length row,
> a reverse-convex equality, does worse: about 4.77 against an optimum of
> about 5.07, in a floating-point grid estimate.

### 6. [major] §3 has no opening

`sections/03-results.tex:11–13`

**Problem.** In the PDF, "3 Instances and results at a glance" is followed
directly by "3.1 Selection" (page 12). The reader arrives after six
subsections of definitions and a full-page `tab:trust`, and nothing says
what §3 establishes or how the three tables and Figure 1 divide the 43
instances.

**Fix.** Insert after the `\section` line, before the floats:

> \Cref{tab:closures,tab:unclosed,tab:kan} and \cref{fig:results-headline}
> summarize the results: 31 closures, nine of them attained exact optima
> (\cref{tab:closures}); improved dual bounds without closure for the five
> \inst{waterno2} instances and \inst{ann_cumene_tanh}
> (\cref{tab:unclosed}); and enclosures for two relaxations of the six KAN
> instances, whose stored models have no exactly feasible point
> (\cref{tab:kan}). We first explain how we chose the 43 instances.

### 7. [major] The §5 opening is a 51-word list with circular glosses

`sections/05-other.tex:8–10`

**Problem.** Line 9 glosses each class by restating its name: "\emph{identity},
an identity" and "\emph{convexity}, global duality and convexity". It names
no instance, so the reader cannot map the five subsections to the 16
closures. "Do not use the stage splits of \cref{sec:split} (class
\emph{staged})" uses the awkward "class staged"; `terminology.md` asks for
"the staged class".

**Fix.** Replace lines 8–10 with:

> The other 16 closures fall into five certificate classes
> (\cref{tab:closures}): \emph{comparison} for \inst{camshape}, a discrete
> Sturm comparison along the chain of curvature rows
> (\cref{sec:other-camshape}); \emph{dense rows} for \inst{ex6_2_5},
> \inst{ex6_2_7} and \inst{pricing050}, Lagrangian duality over a few
> coupling rows (\cref{sec:other-dense}); \emph{convexity} for the three
> \inst{powerflow} instances, \inst{etamac} and \inst{pindyck}, SDP duality,
> hidden convexity and concavity on a polytope (\cref{sec:other-convex});
> \emph{identity} for \inst{hvycrash}, whose rows force the objective value
> (\cref{sec:other-hvycrash}); and \emph{reduced space} for the three
> \inst{eg} instances, branch and bound over seven inputs with enclosures
> that keep cancellation (\cref{sec:other-bb}). The reduced-space method
> also bounds \inst{ann_cumene_tanh} and the KAN relaxations
> (\cref{tab:unclosed,tab:kan}).

(4 + 3 + 5 + 1 + 3 = 16.) At `04-split.tex:8`, write "the staged class"
likewise.

### 8. [major] "The dual bound in the instance list" is used but never defined

`sections/03-results.tex:43`; also `07-audit.tex:121–123` and
`11-conclusion.tex:28`

**Problem.** §2.1 defines only the *best listed dual*, the best per-solver
bound on the instance page. In §3.1, line 43 then filters on "the dual bound
in MINLPLib's instance list" and line 45 on "the best listed dual": two
different numbers in adjacent sentences, and only the second is defined.
The instance-list value is MINLPLib's aggregate. For example, for `chain` it
equals the third-best reported value (`B4-chain-catmix.tex:27`). A reader
only learns what it is at `07-audit.tex:123`.

**Fix.** Add to the "Listed data" paragraph after `02-semantics.tex:60`:

> MINLPLib's instance list also gives one dual bound per instance, which the
> library forms from the per-solver bounds by trusting a bound only if other
> solvers confirm it \citep{vigerske2014-minlplib-2}; we call it the
> \emph{dual bound in the instance list}. It can be weaker than the best
> listed dual.

At `07-audit.tex:123`, the relative clause "which it forms by trusting …"
can then be cut.

---

## Minor issues

### 9. [minor] Abstract: missing "at most" and an undefined term

`00-abstract.tex:7, 10`

**Problem.** Line 7, "within a relative gap of \sci{3.1}{-9}", drops the
"at most" that C1 and `01:7` keep. Line 10, "are exactly infeasible", uses
a term defined nowhere.

**Fix.** "within a relative gap of at most \sci{3.1}{-9}"; "The six
Kolmogorov--Arnold network instances in our set have no exactly feasible
point; without their partition-of-unity rows, …".

### 10. [minor] Two long sentences in the opening paragraph

`01-introduction.tex:7–8` (48 and 49 words)

**Problem.** "nine of these with exact optimal values" dangles, and line 8
puts the qualifier in the middle.

**Fix.**

> For 31 of them we prove a dual bound and exhibit an exactly feasible point
> within a relative gap of at most \sci{3.1}{-9}; for nine of these we
> characterize the optimal value exactly. For six more we raise the best
> listed dual bound or, where none is listed, prove one. We apply the same
> standard to the library's records and to solver output. Under a stated
> hypothesis on how MINLPLib's pages display numbers, we prove 22 of its
> listed per-solver dual bounds invalid, and we report a seed-dependent
> error in SCIP~10 that returns wrong optimal values on subproblems of
> \inst{waterno2_06}.

### 11. [minor] Inflated description of MINLPLib

`01-introduction.tex:13`

**Problem.** "the reference against which MINLP solvers and methods are
measured" overstates the library's role.

**Fix.** "MINLPLib, a standard benchmark library for MINLP solvers and
methods, lists …".

### 12. [minor] Ambiguous antecedent

`01-introduction.tex:18–19`

**Problem.** In "No formula for the gap is documented. It is a consensus
label, not a check.", "It" grammatically points to the gap formula.

**Fix.** "The solved mark is thus a consensus label, not a check."

### 13. [minor] A value cannot be feasible

`01-introduction.tex:26`

**Problem.** "If a listed value is feasible only within a tolerance" applies
feasibility to a value.

**Fix.** "If a listed point is feasible only within a tolerance, or a
reported bound is invalid, every such use inherits the error."

### 14. [minor] "Listed gap" is undefined

`01-introduction.tex:40`

**Fix.** "so the gap between the listed bounds compares a valid but weak
dual bound with a value below the optimum."

### 15. [minor] Which verdict changes is unclear

`01-introduction.tex:43–45`

**Problem.** "Even where the listed bounds nearly agree, exact feasibility
can change the verdict." The reader has to infer that "the listed bounds"
are the dual and primal values and that the verdict concerns the listed
point.

**Fix.**

> Even where the listed dual and primal values nearly agree, the listed
> point need not be exactly feasible. For \inst{lnts50} the best listed dual
> bound lies within \sci{3.9}{-5}, relative, of the optimum, yet the best
> listed point, p1, violates rows by up to \sci{9.1}{-10}, and its objective
> lies at least \sci{4.30}{-11} below the exact optimal value
> (\cref{thm:lnts-opt}).

### 16. [minor] Inverted syntax in lesson 1

`01-introduction.tex:62`

**Fix.** "We can only interpret, not demonstrate, why general-purpose solvers
did not find such bounds (\cref{sec:interpretation})."

### 17. [minor] C2 calls definitions "existence tests", and "re-proofs" is jargon

`01-introduction.tex:91–92`

**Problem.** The list "The existence tests are classical: … and exact
algebraic and triangular definitions" includes definitions, which are not
tests. "re-proofs" is jargon, and "What is new is the points" has a number
mismatch.

**Fix.** "The constructions are classical: …"; "What is new are the points
themselves and their second proofs by separately written code." The same
"What is new is …" construction recurs at `:174`.

### 18. [minor] "Development commit" against "development snapshot"

`01-introduction.tex:121`

**Problem.** C6 says "a tested development commit"; `08:44`, `08:81` and
`10:73` say "development snapshot".

**Fix.** "and a development snapshot".

### 19. [minor] The C6 mechanism sentence is opaque

`01-introduction.tex:123`

**Problem.** "a binary64 residual in a cubic equality whose bounds agree in
decimal" does not say which bounds or what disagrees.

**Fix.** "In instrumented runs, reverse propagation declares infeasible a
node that contains a witness: on a row $x^3-y=0$ with $x$ fixed at $0.7$
and $y$ at $0.343$, the binary64 values satisfy $\fl(0.7)^3<\fl(0.343)$,
although $0.7^3=0.343$ exactly (\cref{lem:scip-cube})."

### 20. [minor] C8 uses terms before §4 defines them, and "families" is ambiguous

`01-introduction.tex:139–140`

**Problem.** "chord minorants", "derived enclosures" and "a window of stages"
appear before §4 defines them. "families" here means instance families,
whereas `02:185` defines a *certificate family* as a row of `tab:trust`.

**Fix.** Add pointers: "(\cref{prop:split-affine,lem:split-minorant})",
"derived enclosures (\cref{rem:split-enclosures})", "a window of stages
(\cref{prop:split-window})". Write "Two of the six instance families
involved". Also write "instance families" at `09-interpretation.tex:24`.

### 21. [minor] Three sentences use the same padding frame

`01-introduction.tex:170–173`

**Problem.** "This holds for … The same is true of … It is also true of …"
repeats one frame three times.

**Fix.** Keep "Every mechanism in our certificates predates this work." Then
use one list sentence: "They include Lagrangian decomposition and its use in
nonconvex global optimization [..]; Krotov- and Mangasarian-type sufficiency
and relaxed dynamic programming [..]; …; and rational PSD certificates
[..]." Alternatively, keep the three sentences and start each with "They
include".

### 22. [minor] The second sentence of §2 says nothing specific

`02-semantics.tex:5`

**Problem.** "This choice decides how our results relate to listed values and
to solver output." does not tell the reader what §2 establishes.

**Fix.** "Under this semantics a dual bound must hold for every exactly
feasible point, and a primal value must come from a point proved to satisfy
every row exactly; a listed or reported value that fails either test is a
tolerance artifact or an invalid claim (\cref{sec:semantics-categories})."

### 23. [minor] "The largest violation" is not defined in Definition 2.2

`02-semantics.tex:35`

**Fix.** "The smallest $\varepsilon$ for which a point is
$\varepsilon$-feasible, its largest violation, is the measure that MINLPLib
records for listed points."

### 24. [minor] Causal "as" and a stacked hedge

`02-semantics.tex:44` and `:49–51`

**Problem.** At `:44`, "as exact MILP solvers treat …" can be read as
causal. At `:49–51`, "As far as we checked" hedges the same fact that the
next sentence qualifies.

**Fix.**

- `:44`: "following exact MILP solvers, which treat input data as rational
  numbers …".
- `:49`: "Readings (a) and (b) define the same model for every instance of
  this paper except the four \inst{catmix} instances; the comparison is
  exact for 21 instances and numerical evidence for the others
  (\cref{app:semantics-gams})". Then drop that clause from `:51`.

### 25. [minor] A set described as "holding" constraints, and an undefined "multiplier mass"

`02-semantics.tex:99–101`

**Fix.** "where $X$ is the set defined by the constraints that the
certificate keeps". In the next sentences: "The sum
$\|\lambda\|_1+\|\mu\|_1$ can grow with the length of a chain of coupled
rows."

### 26. [minor] "Covers both directions" leaves the reader to compare signs

`02-semantics.tex:133`

**Fix.** "Category~A covers values on both sides of the optimum. The listed
points p2 of \inst{camshape400} and \inst{camshape800} lie below the
optimal value; the listed points p1 and p2 of \inst{hvycrash} have the value
$-0.21413$, above the value $-0.2185$ of every exactly feasible point."

### 27. [minor] The tolerance-level closure definition has the wrong subject and sits in the wrong place

`02-semantics.tex:137`

**Problem.** "A tolerance-level closure reports …" makes the closure the
actor. The definition is also not a category, yet it sits at the end of the
categories subsection.

**Fix.** "A solver run reaches a \emph{tolerance-level closure} if it
reports a valid dual bound and, at a point feasible within its tolerances,
a value within its optimality tolerance of that bound; we credit such
results by name (\cref{sec:results-prior})." Consider moving it after the
closure discussion at `:79`.

### 28. [minor] `\dunit` is defined twice, differently

`02-semantics.tex:148` against `07-audit.tex:30`

**Problem.** §2.4 defines $\dunit{\sigma}$ as the unit of the last displayed
digit. §7.2 defines it as the largest power of ten of which $\dval{s}$ is an
integer multiple. The two differ for strings with trailing zeros. §2 never
uses the symbol. `A-semantics.tex:99` writes $\dunit{\sigma}$ where §7 writes
$\dunit{s}$.

**Fix.** Delete `02:148` and keep the §7.2 definition. Alternatively, move
the §7.2 wording to §2.4 and delete it from §7. At `A:99` write
$\dunit{s}$.

### 29. [minor] The width rule names graphs vaguely, and a term is used before its definition

`03-results.tex:42`, `:44–45`

**Problem.** "a small heuristic upper bound on the treewidth of one of two
graphs" does not say which graphs. At `:44`, "open by our selection rule" is
used before `:45` defines it.

**Fix.**

- `:42`: "… of the factor-incidence graph or of the nonlinear-primal graph
  of the model".
- `:44–45`: put the definition first, then "Of the 294, 155 are open by
  this rule."

### 30. [minor] "The value $+\infty$" is ambiguous

`04-split.tex:24–25`

**Problem.** "The value $+\infty$ encodes the domain rule" follows
"$\vstar=+\infty$", so it seems to refer to $\vstar$.

**Fix.** "The costs $F_t$ take the value $+\infty$ where an expression of
the model is undefined; this encodes the domain rule of
\cref{def:sem-model}(iv)."

### 31. [minor] "Bag" and "stage" name one object; "stage problem" and "stage infimum" are undefined

`04-split.tex:17–37`; also `:346` and `09-interpretation.tex:65`

**Problem.** The formal object is a *bag*, but the text uses "stage
residual of bag $t$", "stage infimum", "stage problems" and "Large bags".
Line 26 links the two words only for control problems.

**Fix.** After `:36` add: "We also call bag~$t$ the $t$-th stage; its
\emph{stage problem} is the minimization of $F^\varphi_t$ over $K'_t$, with
value the \emph{stage infimum}." Then use "stage" in the §4.5 title ("Large
stages: \inst{waterno2}") and at `09:65`.

### 32. [minor] "Class" has three meanings

`04-split.tex:38`, `:226`, `tab:staged`

**Problem.** "Class" means a certificate class (staged, comparison, …), a
*split class* (the function set for $\varphi_t$) and an audit class ((i),
(i-r), (ii), (iii)). The first two meet in §4: "the staged class" (`:8`)
and "the split class" (`:38`), with "Richer split classes" (`:226`).

**Fix.** Rename the split notion "split form" (affine, quadratic,
cellwise-affine): `:38` "The \emph{split form} is the set of functions
allowed for the $\varphi_t$"; §4.3 title "Richer split forms"; and the
`tab:staged` column header (through `make_tables.py`).

### 33. [minor] Lemma 4.1(d): "Affine splits are the case of the copy rows" is unclear

`04-split.tex:51`

**Fix.** "With the copy rows $\pi^R_tz_t-\pi^L_{t+1}z_{t+1}$ as the $h_k$
and $Y=K'_1\times\dots\times K'_N$, the bound in (d) is $B(\varphi;K')$ for
an affine split (\cref{prop:split-affine})."

### 34. [minor] `optcdeg2` motivation: undefined "certified trajectory" and unclear "loses 0.6258"

`04-split.tex:234–236`

**Problem.** "Certified trajectory" is undefined. In "in floating-point
screening … it loses 0.6258", what is lost relative to what? According to
`dossiers/dtoc5-optcdeg2.md:303`, the bound is 0.6258 below the optimum.

**Fix.**

- `:234`: "At our exactly feasible point the control is …".
- `:236`: "There the stage residual of the costate-affine split is not
  minimized at this point, and a floating-point evaluation with refined
  costates puts its bound about 0.6258 below the optimal value."

### 35. [minor] Wording in §5.1 and §5.3

`05-other.tex:86`, `:148`, `:204`, `:213`

**Problem.**

- `:86`: "The proof lets the identity … accumulate the row violations" is
  awkward.
- `:148`: "Let $\mathcal Q$ keep these identities" describes a set as an
  agent.
- `:204`: "and another is added" does not say what is added.
- `:213`: "the latter" is ambiguous.

**Fix.**

- `:86`: "The proof applies the identity of \cref{lem:camshape-sturm} to a
  point with violations at most $\varepsilon$; the row violations enter with
  the weights $U_m$ (up to 605.9 for $n=800$), and the bounds and slopes are
  relaxed by $\varepsilon$."
- `:148`: "Let $\mathcal Q$ be the set of $(x,y)$ that satisfy these
  identities, …".
- `:204`: name the added term.
- `:213`: "an upper bound $W$ on that degree-one aggregate over
  $\mathcal B$".

### 36. [minor] §5.5: vague title, a long sentence and an implied optimum

`05-other.tex:294`, `:297`, `:324`

**Problem.**

- The title's "strong enclosures" is vague; `tab:closures` says "enclosures
  that keep cancellation".
- `:297` has 46 words.
- `:324`, "the part of \inst{eg_disc2_s} that contains the optimum", implies
  that the optimum is known. Outline §8.5 forbids claiming an exact optimum
  for `eg`. The part meant is part 1 ($x_7\in[24,27]$, `tab:eg-matrix`).

**Fix.**

- Title: "Reduced-space branch and bound with enclosures that keep
  cancellation".
- Split `:297`: "Enclosures that bound each term separately fail there,
  because of cancellation (\inst{eg}) or the depth of the networks
  (\inst{ann_cumene_tanh}, KAN). The certificates therefore use enclosures
  that keep cancellation, and per-box linear programs whose values are
  recomputed by weak duality, so the LP solver is not trusted [..]."
- `:324`: "… for \inst{eg_int_s}, \inst{eg_disc_s} and the part of
  \inst{eg_disc2_s} with $x_7\in[24,27]$, the last under a side condition
  on its LP multipliers (\cref{tab:eg-matrix})."

### 37. [minor] "Authors'" against "first implementation"; "separate" against "separately written"

`05-other.tex:197`, `:324`, `:384`; `10-reproducibility.tex:23`

**Problem.** §2.6 says that the *supplement* calls the codes the authors' and
the verifier's. The main text nevertheless says "the authors' … replays"
(`05:197`), "The authors' search" (`05:324`) and "the authors' checkers"
(`10:23`). At `05:384`, "A separate rerun" invites confusion with the
defined term "separately written".

**Fix.** Use "the first implementation('s)" in the main text. At `:384`
write "A further rerun reproduced …".

### 38. [minor] §6.2 title is awkward; "exactly verified" is undefined

`06-points.tex:69`, `:74`; `11-conclusion.tex:23`

**Fix.**

- Title: `\subsection{Closures whose earlier points were feasible only
  within a tolerance}`.
- `06:74`: "no point proved exactly feasible had been published".
- `11:23`: "Mark listed points as proved exactly feasible or as feasible
  only within a tolerance".

### 39. [minor] The §7 opening does not state the result, and "applied this test to every bound" is loose

`07-audit.tex:6–7`

**Problem.** The text applies the test only to the flagged bounds, not to
every bound.

**Fix.** Replace line 7 with: "We screened every per-solver dual bound on
MINLPLib's instance pages against the listed points, and we settled a
conflict only by proving that an exactly feasible point exists. Under a
stated hypothesis on how the pages display numbers, we prove 22 listed
bounds on 18 instances invalid; none of them contradicts a solved mark. We
state everything for minimization."

### 40. [minor] The audit class (ii) merges two outcomes, one named with a noun

`07-audit.tex:23`

**Problem.** "(ii) proved valid … or repair …" puts two outcomes under one
label, and line 25 then counts them separately. "Repair" is a noun used as
a verdict.

**Fix.** "(ii) \emph{proved valid}, if a rigorous lower bound on $\vstar$ is
at least the bound, or \emph{not refuted after repair}, if the exactly
feasible point found does not lie below it (evidence, not proof)." If
`terminology.md` must keep "repair", define it in one clause here.

### 41. [minor] Undefined "step" in the discussion of Hypothesis H

`07-audit.tex:36–38`

**Problem.** "H holds if at most one step changes the value" relies on
"steps" that the previous sentence calls "roundings … or truncations".

**Fix.** "\Cref{lem:audit-display} shows when Hypothesis~H holds. If $s$
arises from $b$ by finitely many roundings (to nearest or directed) or
truncations to integer multiples of powers of ten, then
$|b-\dval{s}|<\tfrac{10}{9}\dunit{s}$; Hypothesis~H itself holds if at most
one of these operations changes the value, or if the last one that changes
it rounds to nearest."

### 42. [minor] "The classes use only half a unit" is cryptic

`07-audit.tex:55`

**Fix.** "The class rule of \cref{sec:audit-screen} needs a margin above
half a unit, less than \cref{prop:audit-refute}(a) needs. In fact every
class (i) margin exceeds $\tfrac{10}{9}\dunit{s}$ (the smallest is
$1.115\,\dunit{s}$), and every class (i-r) margin is below
$0.44\,\dunit{s}$."

### 43. [minor] A suggested cause two lines after "attribute no cause"

`07-audit.tex:82`

**Problem.** Line 80 says "attribute no cause". Line 82 then adds
"consistent with pruning or reporting at such a tolerance", which suggests a
cause (outline §8.7).

**Fix.** End the sentence at "below the common relative gap tolerance
$10^{-4}$".

### 44. [minor] "Two exceptions" is followed by a structure that does not show two

`07-audit.tex:92–94`

**Problem.** The second exception, the nine instances without an older
copy, reads as a separate fact.

**Fix.** "Archived copies show the models unchanged since before the refuted
and (i-r) bounds, with two exceptions (\cref{app:audit-history}). After both
of its bounds, \inst{ghg_3veh} rewrote three products of constants as
rounded decimals (relative change $\le1.84\cdot10^{-15}$), and the
refutation also holds on the old text. Nine instances added days before
their 2014 bounds have no older copy."

Alternatively, join the two with a colon and a semicolon.

### 45. [minor] The §8 opening states no result, and §8.1 starts with a proposition

`08-solvers.tex:7`, `:9–11`

**Fix.** Append to `:7`: "Many reported values are tolerance artifacts
(\cref{sec:solvers-tolerance}). Three are invalid claims, and only one of
these, the SCIP~10 error, we trace to a defect (\cref{sec:solvers-invalid}).
In one-hour runs no current solver closed an instance under exact
feasibility (\cref{sec:solvers-campaign})." Optionally, add a lead-in before
Proposition 8.1: "BARON's optimality claims on \inst{camshape100} and
\inst{camshape200} are the closest tolerance-level results among current
solver runs."

### 46. [minor] "Three semantics" is a new triple that looks like readings (a)–(c)

`08-solvers.tex:62–67`

**Fix.** In (b), name and number the senses: "(1) decimal data read
exactly, zero tolerance (\reading{b}): …; (2) SCIP's own tolerances: …;
(3) binary64 data, zero tolerance (\reading{c}): …", and change the title
to "The reproducers in three senses". At `:70` write "only in senses (1)
and (2)".

### 47. [minor] The reason given does not support "so"

`08-solvers.tex:131`

**Problem.** No run closes under exact feasibility because the two claiming
runs returned points that are not exactly feasible, not because only two
runs claim optimality.

**Fix.** "Of the 129 runs (\cref{tab:solvers}), only two claim optimality,
BARON's on \inst{camshape100} and \inst{camshape200}
(\cref{prop:baron-camshape}), and their returned points are not exactly
feasible; so no run closes an instance under exact feasibility."

### 48. [minor] The §9 opening hides the thesis

`09-interpretation.tex:15–18`

**Problem.** The opening states two facts and caveats. The interpretation
itself first appears at `:52`.

**Fix.** After `:15` insert: "Our interpretation is that termwise
relaxations cannot see the structure that each certificate uses: free states
along long chains of nonconvex equalities, hidden convexity or monotonicity,
and cancellation among many terms." Then keep the caveat sentences and the
definition of a termwise relaxation. Lines `:50–51` can then be cut, since
they restate lesson 1 and §9.1.

### 49. [minor] Addresses the referee

`10-reproducibility.tex:46`

**Fix.** "They show the order of magnitude to expect and support no speed
comparison."

### 50. [minor] The §11 title does not match its subsections

`11-conclusion.tex:10`

**Problem.** The title says "Implications", but the first subsection is
"Recommendations".

**Fix.** `\section{Recommendations, limitations and conclusion}`.

### 51. [minor] "Changes no string" in §A.4

`A-semantics.tex:80`

**Problem.** Rounding changes values, not strings.

**Fix.** "which changes the value of no string in \inst{lukvle10}, of two
strings in each \inst{lnts} and \inst{chain} file, and of up to 3,332
strings (\inst{eg_disc2_s}) elsewhere."

### 52. [minor] Full statements repeated across sections

**Problem.** The same full statements recur:

- the `eg` trust-base statement: `02:166–167`, Theorem 5.14
  (`05:310`) and `11:52–53`;
- the KAN tolerance disclaimer: `01:105`, `03:72` and `05:388`;
- BARON's tolerance-level closures: `01:133–135`, `05:79`, `08:22–24` and
  `09:43`;
- the `waterno2` priority sentence, almost word for word: `01:97` and
  `03:91`, once "decomposition by periods" and once "period
  decomposition";
- the list of the 13 earlier-violating closures: `01:90`, `06:71` and
  `tab:points`.

**Fix.** Keep the full statement once (§2.5, §5.5, §8.1, §3.4 and §6.2
respectively). Elsewhere, cut it to a clause with a cross-reference, and use
one phrase, "period decomposition". This does not touch the qualifiers that
outline §3 requires in C1–C9.
