# Style and clarity check, round 1 (main paper)

Date: 2026-10-04. Scope: `main.tex` as built, that is, sections 00–11,
Appendix A (`A-semantics.tex`) and Appendix B (`G-proofs-split.tex`), with the
generated tables that the main paper prints (`tab-trust`, `tab-closures`,
`tab-unclosed`, `tab-kan`, `tab-points`, `tab-audit-pairs`, `tab-structure`).
The supplement was not reviewed. I read the files as a Mathematical
Programming Computation (MPC) referee would and checked them against
`development/style-guide.md` and outline §3 and §8. No file was edited
except this report.

Line numbers refer to the current files in `sections/` and `tables/`. "Rewrite"
gives replacement text or a precise instruction. Where a rewrite changes a
number or a count, have the numbers-check owner confirm it first.

Commands run (targeted, read-only):

- `cat -n` of each main-paper section and table;
- grep for the banned phrases of the style guide and for terminology variants;
- a sentence-length script (`/tmp/stylecheck/longsent.py`), which flags
  sentences of 38 or more words after citations and inline math are stripped;
- `pdftotext` and `pdfinfo` on the existing `build/main.pdf` (63 pages; not
  rebuilt), to see pages 1–3 and where headings and floats fall.

No project-wide build or check was run.

**Item count: 140** (B 8, T 20, J 25, L 20, R 21, S 38, H 8).

---

## 1. Overall judgment

**Contribution on pages 1–2.** The abstract states both contributions clearly:
certificates for open instances and the audit. The opening paragraph of §1
poses the question and the approach, and Box 1 (`camshape800`) on page 2 is a
strong, concrete motivating example. The headline results, however, do not
appear in the body until C1 on page 3: 31 closures, gaps of at most
3.1·10⁻⁹, nine exact optima, invalid listed bounds and the SCIP defect.
There they sit inside long paragraphs in which the sentences crediting prior
work outnumber those stating our results. A referee who reads only pages 1–2
learns the question and one example, but not the main results.

Recommendation: end the opening paragraph of §1 (`01-introduction.tex:8`) with
two result sentences. Suggested text, with numbers as in C1, C3 and §7:

> For 31 of the 43 instances we prove a dual bound and an exactly feasible
> point within a relative gap of at most 3.1·10⁻⁹, nine of them with exact
> optimal values; for six more we raise or supply the dual bound. We also
> prove 22 of MINLPLib's listed per-solver dual bounds invalid and report a
> seed-dependent error in SCIP 10.

Then shorten C1–C4 (item R1). This costs about three lines and saves more.

**Structure.** The order of sections is logical, and each section has one job:
semantics, results, certificates, points, audit, solvers, interpretation,
reproduction, conclusion. Three things make the paper harder to follow than
it needs to be.

1. *The same results appear three or four times before a proof.* The reader
   meets each result in the abstract, in C1–C9 (pages 3–5, about 2.5 pages),
   in §3, and again in the openings of §4–§8. Items R1–R21 list the
   repetitions. Removing them would also cover most of the 2.3 pages by which
   the main text exceeds its target.
2. *Letter codes collide.* A, B, C, D, E, F, K, P and S each name two to four
   different things (item T1). S alone is the solved mark, an evidence level,
   the supplement prefix and several symbols (item T2). On pages 12–15, for
   example, `tab:closures` prints class "A", arithmetic "F/E" and prior code
   "F" in one row, while the text speaks of "category A".
3. *§2 asks for a lot before any result appears.* Six subsections of
   definitions are followed by a full-page sideways Table 1 (`tab:trust`).
   That table uses abbreviations defined nowhere in the main text (item J18)
   and refers to theorems in §4–§5. Say in §2.5 that Table 1 is a reference
   table for later use. Consider moving §2.4 (display rules) to Appendix A,
   keeping one sentence in §2.

**Style-guide compliance.** No banned phrase occurs. There are no em dashes,
no rhetorical questions and no "Moreover/Furthermore" chains. The one
"first" (`01-introduction.tex:110`) carries its qualifier, but see item B8.
The main problems are long sentences (S), qualifier drift in the abstract and
§1 (B), and undefined local jargon in §4.3–§4.5 and §7 (J).

**Top five fixes, by value to a referee:**

1. Resolve the letter-code collisions and the overloaded S (T1, T2).
2. Cut the repetitions between §1.3 and §3 and those listed in R4–R21.
3. Fix qualifier drift and counts in the abstract and §1: B1 (exceptions to
   the second implementation), B2 (SCIP cause), B5 (19 against 22 invalid
   bounds) and B8 ("decides each conflict").
4. Define local jargon at first use: KAN, ANN, bag, stage residual, targets,
   pair boxes, margin and Tier (J1–J6, J12, J17).
5. Split the long sentences of §1.3, §2.5–§2.6, §7.2, §8.3 and Appendix A
   (S items).

---

## 2. Banned phrases

No item. The grep found none of the listed words or patterns in the main
paper. Near misses are listed elsewhere:

- section-announcing openings (H1);
- inline italic labels used as pseudo-headings (H2);
- closing sentences that restate a section (R21).

---

## 3. Overclaims and qualifier drift (B)

**B1.** `00-abstract.tex:11`. "separately written code rechecks them,
sometimes for a slightly weaker bound". This drops the exceptions of §2.6:

- shared mpmath, KAN core and OSIL reader;
- the second `ann` code, whose author read the first;
- the `eg_disc2_s` second certificate, which covers only part of the domain;
- the `etamac` and `pricing050` primal enclosures, which come from one code
  each.

Outline §8.10 forbids the implication that every result was checked twice.
Rewrite: "Apart from named exceptions, separately written code rechecks each
certificate family, in some cases only for a slightly weaker bound or part of
the domain."

**B2.** `01-introduction.tex:64`. "SCIP 10 has an error caused by a binary64
residual". The mechanism is traced only in instrumented runs, and one wrong
run is not linked to it (`08-solvers.tex:91`). Outline §8.6 forbids saying
that the mechanism explains every wrong run. Rewrite: "SCIP 10 returns wrong
optimal values on some subproblems; in the runs we traced, a binary64
residual of decimal data triggers the error."

**B3.** `05-other.tex:312`. "at the `eg_int_s` optimum". We claim no exact
optimum for `eg` (outline §8.5). Rewrite: "at our exactly feasible point of
`eg_int_s`, the active objective row has …".

**B4.** `07-audit.tex:133`. "MINLPLib's rule … kept the aggregates consistent
with every proved point". This is a causal claim we did not test. Rewrite:
"Apart from these two listed duals, the aggregates, which MINLPLib forms by
trusting a bound only when other solvers confirm it (Vigerske 2014), are
consistent with every proved point, and no S mark is contradicted."

**B5.** `00-abstract.tex:12` against `07-audit.tex:119` and C5
(`01-introduction.tex:106`). The abstract says "Of the 11,086 per-solver dual
bounds … we prove 19 on 15 instances invalid". The three `rocket` bounds are
also among the 11,086, so the paper proves 22 invalid on 18 instances. A
referee will read 19 as the total. Rewrite: "Of the 11,086 per-solver dual
bounds MINLPLib lists, we prove 22 on 18 instances invalid (19 of them found
by a screen against listed points), under a stated hypothesis on how its pages
display numbers." Confirm that the `rocket` refutations also rest on
Hypothesis H: the `rocket100` margin is 1.06 display units, which is below
10/9.

**B6.** `02-semantics.tex:95` and `05-other.tex:84`. "D_n(ε) is about
0.6 n²ε". This hedges a proved upper bound. The supplement table gives
D_n(ε)/(n²ε) ≤ 0.605 for the tabulated ε ≤ 10⁻⁸. Rewrite: "for the tabulated
ε ≤ 10⁻⁸, D_n(ε) ≤ 0.61 n²ε (`tab:camshape-deficit`)". "Grows like n²ε" at
`11-conclusion.tex:22` is fine.

**B7.** `02-semantics.tex:176` and `tab:trust`. The terms "authors' code" and
"verifier's code" suggest a verifier independent of the authors. Line 184
says that all implementations were written within the project, and decision
9 asks us to avoid suggesting independent review. Rewrite: "The first
implementation produced a certificate; a second, separately written
implementation, written without importing or reading the first, checked it."
Use "first" and "second implementation" in `tab:trust` (through
`make_tables.py`), in the certificate boxes, at `05-other.tex:257` and at
`A-semantics.tex:46`.

**B8.** `01-introduction.tex:110` and `:152`. "decides each conflict by
proving that an exactly feasible point exists". The audit leaves 63 repaired
and 25 undecided pairs, so not every conflict is decided. Rewrite line 110:
"… the first systematic screen of MINLPLib's listed per-solver bounds that
settles conflicts by proving that an exactly feasible point exists". Rewrite
line 152: "our audit settles a conflict only by proving that an exactly
feasible point exists".

---

## 4. Inconsistent terminology and notation (T)

**T1.** Letter labels mean many different things:

| letters | meaning | where |
|---|---|---|
| A, B | categories of disagreement | §2.3 |
| A, A′, B–E | certificate classes | `tab:closures`, §5 line 9, §9, `tab:structure` |
| (A)–(D); A–C | point constructions; point methods | §6.1; `tab:points` |
| A–D | audit "routes" | §7.3, `tab:audit-pairs` |
| E, O, M, B | reading types | App. A.2, `tab:trust` |
| [E], [I], [F], [L] | arithmetic tags | §2.5 |
| F, f, Lst, T, K, U, N | prior-result codes ("F" next to the arithmetic column "F/E") | `tab:closures` |
| K, E, LK | proof codes ("K" = Krawczyk, but prior code K = value known without proof) | `tab:audit-pairs` |
| P, C, S | evidence levels | §2.5 |
| (C1)–(C5) | camshape checks, against contributions C1–C9 | §5.1 |
| (F1), (F2) | facts | App. B |

Rewrite:

- Keep categories A/B and the tags [E]/[I]/[F].
- Name the certificate classes by words in both tables and the text: split,
  comparison, dense rows, duality/convexity, identity, enclosure.
- Describe the point constructions and audit methods by name, not by letter
  (see H2 and J10).
- Rename the prior codes F/f to "fp"/"fp-near", or spell them out.
- Rename the camshape checks (K1)–(K6) (item L11).

**T2.** S is the solved mark, the evidence level, the supplement prefix and
several symbols (S_t in optcdeg2, S_j in camshape, S(μ,ν) in lnts). It
collides worst at `03-results.tex:49–51`, where "the tolerance 10⁻⁶ of the S
mark" is followed by "the ten closures at level S". Rewrite: rename the
evidence level to R, for "rerun", in `\evid` uses and in `make_tables.py`
(`02-semantics.tex:165`, `03-results.tex:51`, `05-other.tex:307`,
`10-reproducibility.tex:31,46`, certificate boxes, `tab:trust`).

**T3.** "GUROBI" and "Gurobi" are mixed:

- GUROBI: `00:14`, `01:123`, `03:39`, `08:125,131,138`, `09:35,36,45`,
  `10:73` and the tables;
- Gurobi: `01:23,78,118`, `03:86`, `08:43,99,100,110`.

Rewrite: use "Gurobi" in prose. Keep MINLPLib's label "GUROBI" only in the
solver cells of listed bounds and say so once in the `tab:closures` caption.

**T4.** The letter F has six meanings:

- the feasible set 𝓕(𝓜);
- the stage costs F_t (§4);
- the Krawczyk map F in Theorem 6.1 (`06-points.tex:25`), whose conclusion
  also uses 𝓕(𝓜) (`:38`);
- the pindyck price set F (`05-other.tex:231`);
- the KAN objective F(u,k) (`05:377`);
- the powerflow function F(P_g,Q_g,W) (`05:180`).

Rewrite: in Theorem 6.1 rename the map G: ℝ^m→ℝ^m (G_i(z) = g_i(ξ,z) − t_i).
In pindyck call the set P (P = {p ≥ 0 : d_t(p) ≥ 0}).

**T5.** `07-audit.tex:20` says "let f be the upper end of its objective
enclosure", but f is the objective, and Proposition 7.2 (`:43`) uses φ for
the same number. The `tab:audit-pairs` column is also "f ≤". Rewrite: "let φ
be the upper end of its objective enclosure", and rename the table column φ
in `make_tables.py`.

**T6.** `05-other.tex:176` says "let L and N index buses 30 and 2" (W_LL,
W_NN), which clashes with the dual bound L in the same subsection's theorems
and with N for stages. `08-solvers.tex:49` uses "lower bounds L and L³", and
`lem:scip-cube` (`:78`) uses fl(L)^k. Rewrite: use k and m for the buses
(W_kk, W_mm), and ℓ for the pump speed bound (ℓ, ℓ³, fl(ℓ)^k).

**T7.** The letter d has several meanings:

- d(σ), the decimal value (`\dval`);
- d(λ), the dtoc5 dual function (`04-split.tex:239`);
- d, the displayed bound (`01:107`, `07:87`, `tab:audit-pairs`), which is
  d(s) of §7.2 under another name;
- d_i in camshape, d_t in pindyck, d_t(D) in App. B.

Rewrite:

- Call the dtoc5 dual function q(λ) (in Proposition 4.9, Theorem 4.10, the
  certificate box and the `tab:trust` dtoc5 row).
- In C5 and §7.4 write "d(s), the value of the displayed bound s".
- In App. B write dist_t(D).

**T8.** "Open" is overloaded:

- the instance status ("listed as open", "open in sense (b)");
- "the triangle is open" (`03-results.tex:39`);
- "final open boxes" (`05-other.tex:349`);
- "remain open" for audit pairs (`07-audit.tex:124`).

Also, §3.1 introduces "sense (b)" without any "sense (a)" in the main text;
§2.1 says "listed as open". Rewrite:

- `03:39`: "the triangle is hollow";
- `05:349`: "1,644,110 pruned regions and 208,223 unsplit leaf boxes";
- `07:124`: "remain undecided";
- `03:18`: "open by our selection rule". Define this term once and drop
  "sense (b)" everywhere, including `03:20,25` and `11:63,72`.

**T9.** KAN "models" and "instances" are mixed. C4's heading and `01:97` say
"ten KAN models", `02:53` and `05:305` say "the KAN models", while `05:359`
says "ten KAN instances" and `03:75` "six KAN instances". Rewrite: "instance"
for MINLPLib entries and "model" only for 𝓜, 𝓡_P or 𝓡. C4 heading: "C4 (KAN
instances)". `01:97`: "MINLPLib contains ten KAN instances; the six in our
set …".

**T10.** The KAN optimum is written three ways:

- v*(𝓡) ≤ v*(𝓡_P) at `03:78` and in the Figure 1 caption;
- min_𝓡 F ≤ min 𝓡_P at `05:378,382`;
- min_𝓡 F ≤ min_{𝓡_P} F in `tab:kan`.

Rewrite: use v*(𝓡) ≤ v*(𝓡_P) throughout, after stating at `05:377` that F is
the objective of both.

**T11.** One object has three names. Line `04-split.tex:290` calls it the
"quadratic verification functions in Krotov's sense, S_t", and `:294` the
"split functions S_t … calibration data". The certificate box says
"calibration arrays", the abstract and C8 say "calibrations", and the chain
uses "split φ_k". Rewrite: at `04:290` write "The certificate adds curvature
in the velocity only, with the split φ_t(y,v) = p^y_t y + p^v_t v +
(q_t/2)(v − v̄_t)² (a quadratic verification function in Krotov's sense)".
In Theorem 4.11 write "Let the split φ_t be given by the stored binary64 data,
read as exact rationals". Use "calibration" only for the stored data, or
define it once at `04:37`.

**T12.** "Tolerance-level closure" is defined at `02-semantics.tex:130`, but
the abstract (`00:14`, "BARON closed two within its tolerances") and C7
(`01:125`, "a closure to MINLPLib's tolerance by one solver") use other
words. Rewrite: abstract "BARON reached a tolerance-level closure on two";
C7 "a tolerance-level closure by one solver (Section 2.3)".

**T13.** "Listing duals" at `11-conclusion.tex:29` is undefined; §7 says "the
dual bound in the instance list". Rewrite: "except the six-digit
instance-list dual bounds of `eniplac` and `stockcycle`".

**T14.** "OSiL conventions" at `11-conclusion.tex:55` should match "OSIL"
elsewhere; the `02:37` footnote naming the schema is fine. Rewrite: "OSIL
conventions".

**T15.** "Proven valid" at `07-audit.tex:24,26` differs from "proved"
everywhere else. Rewrite: "proved valid".

**T16.** One quantity is printed at two precisions:

- the listed-dual gap of `camshape100`: 1.3·10⁻⁶ (`01:161`, `03:20`) and
  1.22·10⁻⁶ (`05:78`);
- the CAMINO margins: 4.3%, 7.4% and 80% (`01:118`) and 4.33%, 7.48% and
  80.5% (`08:101`).

Both forms are valid "at least" displays, but readers will see two numbers.
Rewrite: use one display per quantity, for example 1.22·10⁻⁶ and
4.33/7.48/80.5% throughout, after confirming with numbers-check.

**T17.** `tab:trust` cells use "a separate code confirms" (ex6_2),
"re-derived by a separate check" (pricing050) and "verifier only" (etamac);
`05-other.tex:135` says "a separately written code confirms". Rewrite (in
`make_tables.py`): use the defined term "separately written" and the
first/second terminology of B7, for example "second implementation;
separately written code confirms".

**T18.** Dates mix formats: ISO (2026-10-02) in most places,
"2 October 2026" at `08:47,97` and `10:73`, and "4 October 2026" at
`01:162`. Rewrite: use ISO dates throughout.

**T19.** The certificate boxes of §4 have six fields (Inputs, Computation,
Data reading, Implementations, Evidence level, Replay). Those of §5 have four
(Inputs, Computation, Implementations, Level and replay), and the §5 boxes
fold the data reading into Inputs. Rewrite: use one field set; the six-field
form is clearer (integration-notes-r1 §8 item 6).

**T20.** "Certificate family" at `01:51` and `02:179` and "family" elsewhere
are used without saying that a family is an instance group of `tab:trust`.
Rewrite at `02:179`: "every certificate family (a row of Table 1)".

---

## 5. Undefined jargon, internal names, forward references (J)

**J1.** KAN is used without expansion at `01-introduction.tex:23` ("over
trained KANs") and in C4 (`:96`). It is expanded only in the abstract and at
`03-results.tex:75`. Rewrite `01:23`: "a study of optimization over trained
Kolmogorov–Arnold networks (KANs) reports SCIP optima at zero gap".

**J2.** `02-semantics.tex:177` says "for the ANN and KAN models"; ANN is never
expanded. Rewrite: "for `ann_cumene_tanh` and the KAN instances".

**J3.** C4 (`01:100`) uses "a larger network relaxation 𝓡" before §5.5
defines it. Rewrite: "The lower ends also bound the network relaxation 𝓡, in
which only the inputs and the knot choices are free (Section 5.5); …".

**J4.** `04-split.tex:17` uses "bag", a tree-decomposition term, without
introduction. Rewrite: "Bag t (a block of variables, as in a tree
decomposition) holds a vector z_t …".

**J5.** "Stage residual" (`04:288,291,301,324`) is never defined. Rewrite: add
at `04:35`, after (4.2): "We call F^φ_t the stage residual of the split."

**J6.** The waterno2 paragraph (`04:406–418`) uses undefined terms: "targets",
"link", "pair-box bounds" and "cell pairs". Rewrite:

- `04:408`: "For `waterno2_06`, each separator is divided into 148 to 240
  cells of tank-level vectors, each with its own slope vector (Proposition
  4.5) …".
- `04:409`: "Here rigorous bounds on 49,315 boxes, each covering a pair of
  consecutive periods, give the arc weights b_t for all 117,736 pairs of
  cells through an exact linear correction (Lemma S…)".
- Before `04:411`, add: "Each period search stops when its lower bound
  reaches a target value taken from a SCIP solve; a target affects the
  strength of a bound, not its validity."

**J7.** The chain paragraph (`04:327–328`) uses "box-wise (V,H)" and "chord
condition". Rewrite `04:327`: "… then proves, on each leaf box, either
B_N ≥ L_N for some (V,H) chosen for that box, or that the box contains no
feasible end values …". Rewrite `04:328`: "The reduction to the end values
loses nothing where the end values satisfy the chord inequality of
Lemma S… strictly (Proposition S…)."

**J8.** `04:356` (catmix certificate box) says "verified cone ranges". Rewrite:
"per ray and control interval, a proved range of the cones that contain the
image, and Dinkelbach bounds of quadratic ratios".

**J9.** `03-results.tex:15–17` uses "funnel" and "a structural width rule";
the rule is explained only at `:24`. Rewrite `03:17`: "Of these, 360 pass a
structural rule, a heuristic upper bound on the treewidth of the constraint
graph (Section S3.4), and 294 of the 360 …". Shorten `:24` accordingly.

**J10.** `07-audit.tex:72–74` and `tab:audit-pairs` use "Route A", "Route B",
"Route C" and "route D". These are internal labels and collide with T1.
Rewrite: "Some proofs check a listed point in rational arithmetic. Others fix
integer and near-bound variables at exact values, apply Theorem 6.1 to the
equality and nearly active rows, and enclose all other rows, the bounds and
the objective over the proof box. A degenerate point is first moved into the
interior, and a few cases use dedicated certificates (Section S4.x)." In the
table, use words ("listed point", "Krawczyk", "shift + Krawczyk",
"dedicated").

**J11.** `fm336` and `tiny2` (`08-solvers.tex:48,66–73`) are archive file
names, and `tiny2` is never introduced. Rewrite:

- Box 2: "A model with 15 variables and three pumps (archived as `fm336`)
  reproduces the error …".
- Proposition (a): "The optimal value of `fm336` is 187/270, and that of
  `tiny2`, a smaller reproducer derived from it (Section S6.x), is −1.337."

**J12.** "Margin" is used at `01:107` and `07:55,87,93` without a definition.
Rewrite C5: "With d(s) the displayed bound and φ the objective bound of the
refuting point, the margin d(s) − φ exceeds 10⁻⁶|d(s)| for eleven bounds and
0.01|d(s)| for four". Define the margin once at `07:20`.

**J13.** "Dyadic" (`05:328`, `tab:trust`, `tab:points`) is unexplained.
Rewrite `05:328`: "in exact dyadic-rational arithmetic (rationals with
power-of-two denominators) and in mpmath interval arithmetic".

**J14.** `01:13` says "The points are polished". Rewrite: "MINLPLib adjusts the
points so that integrality and variable bounds hold exactly, but algebraic
rows may keep residuals."

**J15.** `01:160` says "the two-sided verification". Rewrite: "the
verification of both the dual bound and the point on the stored models".

**J16.** "Tolerance-only" appears in the heading at `06-points.tex:68` and at
`11:24`. Rewrite the heading: "Thirteen closures with only tolerance-feasible
earlier points". Rewrite `11:24`: "Mark listed points as exactly verified or
as feasible only within a tolerance".

**J17.** "Tier 1/2/3" is used in every certificate box from `04:220` on, but
§10 defines the tiers. Rewrite: add to §2.6 (end of `02:181`): "Replay tiers
(Section 10): 1, seconds to minutes; 2, up to one hour; 3, hours or more."

**J18.** `tab:trust` cells use abbreviations undefined in the main text: "IVT
bracket", "B₂₅₆ ≤ d(λ)", "ℚ(√R_N)", "E→O" and "E/O". Rewrite (in
`make_tables.py`):

- "intermediate-value bracket";
- "two exact codes (full rational q(λ); a lower bound with each subtracted
  fraction rounded up to 2⁻²⁵⁶)";
- "explicit point in a real quadratic field [E]";
- in the caption: "E→O: read exactly, then enclosed outward; X/Y: the two
  implementations read the data differently".

**J19.** `08-solvers.tex:22` says "at the binary64 levels in BARON's
savepoints". These are GAMS terms. Rewrite: "Evaluated exactly at the binary64
variable values in BARON's GAMS savepoint files, …".

**J20.** `06-points.tex:42` names "Hansen's device" without a citation; the
bibliography has no Hansen entry. Rewrite: add the Hansen (1992) entry and
cite it, or write "Fixing coordinates, a device for underdetermined systems
that Kearfott (1998, Sect. 3) implemented …".

**J21.** "Payoff" (`01:53`, `03:25`) is vague. Rewrite: "chosen because we
judged them tractable and informative, not at random".

**J22.** `05-other.tex:69` says "The optimal cam follows the line R", but R_j
is a sequence, and 𝓡 is the KAN relaxation. Rewrite: "The optimal cam follows
the comparison radii R_j, rises with maximal slope α, and stays at the cap
r = 2".

**J23.** `02-semantics.tex:24` says "our points of `pricing050` and `waterno2`
contain cubes of zero" without saying why this matters. Rewrite: "for
example, our points of `pricing050` and `waterno2` contain cubes of zero,
which rule (iii) evaluates as integer powers, so they are defined."

**J24.** `05-other.tex:306` says "Termwise interval enclosures fail there
because of cancellation or depth" before §9 defines "termwise". Rewrite:
"Enclosures that bound each term separately fail there, because the terms
cancel (`eg`) or the networks are deep (`ann`, KAN), so …".

**J25.** `03-results.tex:28` mentions `fct` without saying why it is missing
from the census. Rewrite: "The one nonconvex instance listed as open that is
missing from the census, `fct`, whose OSIL file was not in our cache, would
not change the 155."

---

## 6. Unclear logic (L)

**L1.** `01-introduction.tex:57–58` (lesson 1) says "branching was absent in
12 closures and at most three-dimensional in 15 more". Here 12 + 15 = 27 of
31, and the reader is left asking about the other four. Rewrite: "After this
step, branching was absent in 12 closures and at most three-dimensional in 15
more; in the other four it covered 9 boxes (`pindyck`) or the 7 original
variables (`eg`)."

**L2.** `01:51` and `02-semantics.tex:179`. "Every certificate family was
implemented at least twice" is contradicted inside the same sentence at
`02:179` ("the primal enclosures of `etamac` and `pricing050` come from one
implementation each"). Rewrite `02:179` as two sentences:

> Apart from these exceptions, every dual certificate has at least two
> separately written implementations, which need not certify the same value
> (Table 1): for `optcdeg2`, `lukvle10`, `catmix`, `etamac` and `pindyck` the
> second certifies only a slightly weaker bound, and for `eg_disc2_s` it
> covers only part of the domain. Every primal claim has two implementations
> except those of `etamac` and `pricing050`.

Adjust `01:51` to "Every dual certificate was implemented at least twice …".

**L3.** `02-semantics.tex:94`. The Hölder paragraph lacks a topic sentence, so
the reader does not know what is being bounded. Rewrite:

> A tolerance-feasible point can lie below L, but only by an amount that the
> multipliers control. Let L ≤ inf_{x∈X}[f(x)+λᵀh(x)+μᵀg(x)] with μ ≥ 0,
> where X holds the constraints that a certificate keeps and h, g are the
> dualized rows in their written scaling. Then every x̃ ∈ X with
> |h_i(x̃)| ≤ τ and g_j(x̃) ≤ τ satisfies f(x̃) ≥ L − τ(‖λ‖₁+‖μ‖₁), by
> Hölder's inequality and μ ≥ 0.

**L4.** `02:147` defines the tag [L] only to say that "no displayed result
carries" it. Rewrite: delete [L] and add: "No displayed result rests on a
hypothesis about the accuracy of a library function."

**L5.** `03-results.tex:25` says "We chose our first 11 instances … and the
other 32 from the remaining 146". The reader cannot see that 9 of the first
11 are among the 155. Rewrite: "We chose our first 11 instances, 9 of them
open by our rule, from a partial width census before the rule was fixed; we
chose the other 32 from the remaining 146 instances open by our rule." Check
the "9 of 11" against S3.4.

**L6.** `04-split.tex:385` says "The coefficients of the squared variables lie
in [−0.8156, 0], above −1, so each infimum over ℝ² is a minimum over an
explicit box". It does not say why −1 is the threshold. Rewrite: "Since
(a²)^{b²+1} ≥ a² for |a| ≥ 1, each pair Lagrangian grows at least like
(1+q)t² with multiplier coefficient q ≥ −0.8156 > −1; so each infimum over ℝ²
is a minimum over an explicit box (Lemma S1.x)."

**L7.** `04:407`. The link between nonconvex pump costs and cellwise slopes is
left implicit. Rewrite: "Because pump costs depend nonconvexly on the tank
levels, an affine split can leave the stage minimizers of consecutive periods
at different level vectors, which weakens the bound. For `waterno2_06` we
therefore use slopes that depend on the cell of the separator."

**L8.** `04:420` says "All five use identities of the decimal data", without
saying five what. Rewrite: "All five points use identities of the decimal
data, such as 0.7³ = 0.343, …".

**L9.** `05-other.tex:9` says "classes A′ to E of `tab:closures`". The classes
are defined only in a caption on a sideways table, and class A is not
mentioned. Rewrite: "They fall into five classes, shown in the column 'cl.'
of Table 2: a comparison theorem along a chain (Section 5.1), Lagrangians
over a few dense rows (5.2), global duality and convexity (5.3), an identity
(5.4), and branch and bound with enclosures that keep cancellation (5.5). The
split certificates of Section 4 form the sixth class."

**L10.** `05:349` uses "1,644,110 closed regions and 208,223 final open boxes".
The reader asks how a bound can be valid with open boxes; "closed" and "open"
also clash with T8. Rewrite: "1,644,110 pruned regions and 208,223 unsplit
leaf boxes, each with a proved lower bound of at least L*".

**L11.** `05:34–40` and `:56`. The text promises "six finite checks" but labels
only (C1)–(C5), and the sixth ("and c_H ≤ 2") has no label. The theorem then
says "(C1) to (C5) and c_H ≤ 2 hold". Rewrite: label all six (K1)–(K6), with
(K6) c_H ≤ 2, and write "Then (K1)–(K6) hold". This also removes the clash
with contributions C1–C9.

**L12.** `06-points.tex:17` says "In (B) and (C), except for the exact
rational points of `catmix`, certificate data define the point". But `catmix`
is listed under (B) at `:14`, so the reader cannot tell which construction it
belongs to. Rewrite: "In triangular definitions and interval existence
proofs, certificate data define the point: seeds and a recursion, a box and a
square system, or a bracket and a sign change. For `catmix` the recursion
gives exact rationals."

**L13.** `07-audit.tex:24`. Class (ii) mixes a proof ("proven valid") with
evidence ("repair"). Rewrite: "(ii) proved valid, if a rigorous lower bound on
v* is at least the bound; (ii′) repaired, if the exactly feasible point found
does not lie below the bound (evidence, not proof); (iii) undecided." Use the
same names in `tab:audit-classes`.

**L14.** `07:17` and `:26`. "Pair" means both a (bound, point) pair (158) and
an (instance, solver) pair (131). Rewrite: "158 flagged (bound, point) pairs
on 46 instances, involving 56 points and 131 per-solver bounds"; then "The 131
bounds split into …".

**L15.** `07:99–100` announces "with two exceptions", but the next sentence
mixes `ghg_3veh` with "nine instances". Rewrite: "… with two exceptions.
First, after both of its bounds, `ghg_3veh` rewrote three products of
constants as rounded decimals (relative change at most 1.84·10⁻¹⁵); the
refutation also holds on the old text. Second, nine instances were added days
before their 2014 bounds, and no copy predates the bounds."

**L16.** `07:119` says "16 of these instances by LINDO", which is ambiguous.
Rewrite: "With `rocket`, 22 per-solver bounds on 18 instances are proved
invalid; 16 of them are LINDO's, one on each of 16 instances."

**L17.** `08-solvers.tex:27` says "Because BARON's incumbents lie below the
exact optima, these run times do not measure the strength of its relaxation"
and leaves out the step that links the two. Rewrite: "BARON's incumbents lie
below the exact optima, so it closed its gap partly from the primal side; its
run times therefore do not show how fast its relaxation alone reaches the
optimum." `09:43` can then cite this sentence instead of restating it.

**L18.** `00-abstract.tex:8` says "leaving gaps of at most 1.68% to 10.82%",
which garbles the range. Rewrite: "leaving relative gaps of at most 10.82%
(1.68% for the smallest instance)".

**L19.** `00:10` says "we enclose their optimal values within 2.42·10⁻⁸",
without saying that the width is absolute. Rewrite: "within an absolute width
of at most 2.42·10⁻⁸".

**L20.** The Figure 1 caption (`03-results.tex:42`) says "The listed and
one-hour dual bounds of `hvycrash` are −2.185·10⁸" without saying why. Rewrite:
"… are −2.185·10⁸ and lie off the scale."

---

## 7. Repetition (R)

Each item keeps the statement once, where its proof or evidence is, and
replaces the other copies with a pointer.

**R1.** C1 (`01:78–80`) and §3.4 (`03:85–96`) credit prior results almost
word for word (Gurobi/lnts50, SCIP 8.1/eg_int_s, Octeract, MINOTAUR/QPLIB_8585,
ANTIGONE, the hvycrash SIF value, McDonald–Floudas). They also group the
instances differently: C1 calls lnts100–400 "partial results", while §3.4
counts them among the seven same-model floating-point results. Rewrite C1's
three sentences as: "For seven of them, floating-point closures or near-closures
of the same model were reported, and eight others have results for copies or
related models, values without proof or possible results in unread sources;
Section 3.4 credits each by name." Keep the "to our knowledge" qualifier.
This saves about 8 lines.

**R2.** The KAN results are stated in C4 (`01:97–101`), §3.3 (`03:75–80`),
§5.5 (`05:359–395`), §6 (`06:8`) and §8.1 (`08:35–37`). Rewrite §3.3 as: "The
six KAN instances of our set minimize trained Kolmogorov–Arnold networks
(Karia et al.). Their stored models have no exactly feasible point
(Proposition 5.x); Table 4 encloses the optimal values of two related models,
𝓡_P and 𝓡 (Section 5.5). No KAN instance is closed."

**R3.** The waterno2 and ann results appear in C3 (`01:90–94`), §3.3
(`03:67–73`) and §4.5 (`04:417–419`). In §3.3 keep only what is new there:
the description of the networks and "none of our one-hour runs returned a
finite one". Replace the factors, the p4 origin and the `ann_cumene_exp`
sentence with pointers.

**R4.** BARON's tolerance-level closure on camshape100/200 is stated in eight
places: `00:14`, `01:125`, `02:130`, `03:55`, `05:79`, `08:14–27`, `09:43` and
`11:41`. Keep C7, Proposition 8.1 with `08:25`, and the recommendation at
`11:41`. Delete `03:55`. At `02:130` keep the definition and "we credit such
results by name (Section 3.4)", without the BARON example. At `09:43` cite
`08:27` (L17).

**R5.** What does not transfer to reading (c) is stated in Remark 2.3(2)
(`02:50–52`), `04:420`, §6.3 (`06:84–86`), App. A.4 (`A:81–83`) and §11.2
(`11:60`). Replace `06:84–86` with "Remark 2.3 and Appendix A.4 state which
points stay feasible under binary64 data." At `04:420` keep only the clause
on the SCIP trigger.

**R6.** Where mpmath enters the primal claims is stated at `02:169–170`, at
`06:80–82` and in the last column of `tab:trust`. Keep §6.3. At `02:169`
mention only the dual side.

**R7.** The eg trust statement appears at `02:155–156`, in Theorem 5.x
(`05:319`), at `05:331` and at `11:53–54`. Delete `05:331`, since the theorem
states the hypotheses. Shorten `02:155–156` to one sentence: "The `eg`
certificates also need a padding lemma and an audited run; Theorem 5.x states
their trust base." Keep §11.2.

**R8.** "Classical / what is new" is repeated. `01:86–87` and `06:19` are
verbatim ("What is new is the points themselves and their re-proofs by
separately written …"). `01:158–160` and `04:122–126` cite the same mechanism
set (Krotov, Lincoln, Geoffrion, Karuppiah, Khajavirad, Cao, Bienstock).
Delete `06:19`. In §1.4 keep the mechanism families with one citation each
and leave the result-by-result mapping to §4.1, or the reverse.

**R9.** The selection caveat ("not a solve rate", "tractability") appears at
`01:53`, `03:25–26` and `11:63`. Keep §3.1. In §1.2 and §11.2 keep a short
clause with a pointer.

**R10.** The unread sources (Huang 2011, Ghaddar 2015, the 2022 paper,
McDonald–Floudas) are listed at `01:92`, `03:96,99`, `11:64` and `11:70`. Keep
§3.4 and §11.2. In C3 write: "three possibly relevant sources could not be
read (Section S3.x), and we claim no priority for decomposition by periods."

**R11.** The branching counts appear at `01:57–58`, `09:28` and `09:51`. Keep
§9.1. At `09:51` write "Afterwards, branching was low-dimensional or absent
in most closures (Section 9.1)".

**R12.** The regeneration of waterno2_18/24 appears at `02:181`, `04:418` and
`10:35–38`. Keep §10. Delete the parenthetical at `02:181`, and at `04:418`
keep a one-clause pointer.

**R13.** Lesson 2 (`01:60`) repeats C8 (`01:129`). Delete lesson 2 and
renumber, or cut C8 to the sentence on the extended-value form plus the
classical attribution.

**R14.** That the listed duals of lnts50 and camshape100 were "already close"
is said at `01:42`, `01:161`, `03:20–21` and `05:78–79`. Keep `03:20–21`
(selection) and `05:78` (camshape gaps). At `01:161` delete the example
clause.

**R15.** The refutation principle is restated at `07:6` and `08:8–9` after
Lemma 2.4 and Proposition 2.5. Delete `08:8–9` and keep `08:10`.

**R16.** C2 (`01:85`) and §6.2 (`06:70`) give the same "13 closures …
2.4·10⁻²⁰ to 7.9·10⁻¹²". At `06:70` keep the sources of the earlier points
and cite Table 5 for the violations.

**R17.** The weaker or partial second implementation of six families is listed
verbatim at `02:179` and `11:56`. At `11:56` write: "For six families the
second implementation certifies a weaker bound or covers part of the domain
(Section 2.6)."

**R18.** `eniplac`/`stockcycle` "0.083 and 0.31" appears at `07:131–132` and
`11:29`. At `11:29` drop the numbers and keep the pointer.

**R19.** The eg comparison "44 to 151 times looser … 0.1 to 0.003" appears at
`05:316` and `11:44`. At `11:44` drop the numbers: "range-sum bounds were much
looser than Taylor models that keep the signed moments (Section 5.5)".

**R20.** "Nothing … is formally verified" appears at `02:186` and `11:51`.
Keep one, preferably §11.2.

**R21.** Three closing sentences restate their section: `04:126` (restates
`01:160`), `05:80` (restates the C1 qualifier) and `07:134` (restates `07:6`
and `01:152`). Delete them.

---

## 8. Long sentences (S)

These are prose sentences of about 38 words or more (script count) that a
referee would want split. Certificate boxes and table cells are left out
except S38. The rewrites keep every qualifier.

- **S1.** `01:16` (43 words): "… or that at least three solvers claim
  infeasibility (Vigerske 2026b). No formula for the gap is documented."
- **S2.** `01:48` (51): "We take as the model of an instance its stored OSIL
  file and read every decimal string in it as the rational number it denotes
  (Section 2.1). A point is feasible only if it satisfies every row, bound and
  integrality requirement exactly. Exact mixed-integer programming treats
  rational input data in the same way (Cook et al. 2011; Eifler and Gleixner
  2023)."
- **S3.** `01:79–80` (40 and about 60): delete under R1. If they are kept,
  split each at its semicolon.
- **S4.** `01:84` (51): "Every primal value we report bounds the objective at
  a point that satisfies every row, bound and integrality requirement exactly.
  It is the upper end of a rigorous enclosure (the lower end for the
  maximization instance `pricing050`). For the KAN instances the point belongs
  to the model without the partition-of-unity rows (Section 6)."
- **S5.** `01:92` (43): see R10.
- **S6.** `01:118` (45): "The public CAMINO benchmark data record best bounds
  for Gurobi 13.0.0 on `eg_disc2_s`, `eg_disc_s` and `eg_int_s`. They exceed
  the objective values of exactly feasible points by at least 4.3%, 7.4% and
  80% (Ghezzi et al. 2026). The data record no termination status, and the
  cause is unknown."
- **S7.** `01:125` (43): "BARON made two optimality claims, on `camshape100`
  and `camshape200`. Its dual bounds are valid and lie within 1.23·10⁻⁷ and
  4.80·10⁻⁷, relative, of the exact optima, a tolerance-level closure by one
  solver. The values it returned lie at least 5.25·10⁻⁷ and 2.05·10⁻⁶ below
  the optima."
- **S8.** `01:129` (48): "Fifteen closures share one certificate pattern. The
  objective is split along the stage structure of the model with Lagrange
  multipliers, a discrete calibration, or chord minorants of concave value
  functions. The stage problems, over derived enclosures of unbounded states,
  are then small enough to be minimized rigorously."
- **S9.** `01:135` (44): "A public archive (DOI) contains the models with their
  SHA-256 hashes, the certificate data and the exact point definitions. It
  also holds the checking programs, the separately written re-implementations,
  a claim register that maps every reported number to its artifact, and replay
  commands in three tiers of effort (Sections 10 and S7)."
- **S10.** `01:150` (42): end the sentence after "Nowak and Vigerske (2008)
  report a wrong BARON root bound on `bayes2_10`", then begin "Vigerske and
  Gleixner (2017) discard runs …; Montanher et al. and Bestuzheva et al. count
  …".
- **S11.** `01:159` (75): split into three sentences:
  1. "This holds for Lagrangian decomposition and its use in nonconvex global
     optimization (…), for Krotov- and Mangasarian-type sufficiency and
     relaxed dynamic programming (…), and for LP formulations of bounded
     treewidth (…)."
  2. "It holds for discrete Sturm comparison (…), the Gibbs tangent-plane test
     (…), hidden convexity (…) and SDP relaxations of optimal power flow
     (…)."
  3. "It holds for Taylor models, affine arithmetic and safe per-box LP bounds
     (…), for interval existence tests (…) and for rational PSD certificates
     (…)."
- **S12.** `01:162` (47): "Our search for prior results covered the 43
  instance names, their source models and copies, and the literature cited
  above, up to 2026-10-04. It is a bounded search, not a proof of priority;
  Section S3 describes it and lists the sources we could not read."
- **S13.** `02:19` (47, definition item iv): end the item after "defined at x
  in the sense of (iii)", then add: "That is, no denominator vanishes, every
  `ln` argument is positive, every `sqrt` argument is nonnegative, and every
  `power` node falls under a case of (iii)."
- **S14.** `02:37` (43): "Reading the decimals exactly is a choice. MINLPLib's
  primary format is the GAMS scalar format (…), the OSIL schema types every
  numeric attribute as `xs:double` (footnote), and solvers work with binary64
  data."
- **S15.** `02:47` (42): "(1) As far as we checked, readings (a) and (b) agree
  for every instance of this paper except the four `catmix` instances. Their
  OSIL files print binary64 products such as 0.045000000000000005 in place of
  9/200, and Proposition S1.x transports our `catmix` dual bounds to reading
  (a)."
- **S16.** `02:58` (44): "The best listed dual of an instance is the best
  single-solver dual bound on its MINLPLib page. An instance is listed as open
  if its page has no solved mark S (Section 1.1). All 43 instances are listed
  as open; Section 3.1 gives our stricter selection rule."
- **S17.** `02:94` (49 with math): see L3.
- **S18.** `02:135` (51): "Dual bounds are rounded toward the infeasible side
  (down for minimization), so that each display is itself a valid dual bound.
  Primal values are rounded toward the feasible side. Gaps and other proved
  upper bounds are rounded up, and 'at least' margins and improvement factors
  down; no bound is rounded to nearest."
- **S19.** `02:143–147` (arithmetic tags, about 70) and `02:158–164` (trust
  base, about 75): set each as a short itemized list. The style guide allows
  lists for assumptions.
- **S20.** `02:165` (45): "The evidence level of a result is P for a
  pen-and-paper proof and C for a computer-assisted proof whose stored finite
  certificate is checked by exact or outward-rounded replay. It is S (R if T2
  is adopted) if the check needs a deterministic rerun of a search whose tree
  is not stored."
- **S21.** `02:177` (45): "Named shared components are the exception. These
  are mpmath where Table 1 lists it, and one rigorous exponential and interval
  core used by both KAN bounding codes. A third is one OSIL reader used by
  several decoders; a separately written reader reproduced its output exactly
  for `ann_cumene_tanh` and the KAN instances."
- **S22.** `02:179` (61): see L2.
- **S23.** `02:185` (73): "Four observations reduce this risk without removing
  it. The exactly compared GAMS and OSIL forms agree except for the `catmix`
  coefficients. MINLPLib's listed points have small residuals under our
  readers, which a misread coefficient that matters at those points would
  destroy. SCIP, with its own OSIL reader, accepts binary64 roundings of our
  points at tight tolerances, such as 10⁻¹² for `chain` (floating-point
  evidence only). Finally, the archive lets others replay every certificate
  (Section 10)."
- **S24.** `03:18` (51): "Of the 294, 155 are open by our selection rule, which
  is stricter than MINLPLib's. An instance is open by this rule if the best
  listed dual and the best value of a listed point with violation at most
  10⁻⁸ differ by more than 10⁻⁴, relative, or if there is no such point or no
  finite listed dual."
- **S25.** `04:324` (44): "Let G_H(v) = ½(v√(H²+v²) + H² asinh(v/H)) and
  c_H = 2G_H(1/(2N)). For the split φ_k(z,v) = G_H(v) − vz − k c_H, a
  closed-form inequality makes every interior stage residual nonnegative, with
  equality exactly on discrete catenaries (Lemma S1.x)."
- **S26.** `04:326` (47): "Here the height multiplier is the cumulative length,
  which varies with the configuration like the tension of a real chain. A fixed
  multiplier on the length row, which is effectively reverse convex, does
  worse: about 4.77 against an optimum of about 5.07, in a floating-point grid
  estimate."
- **S27.** `05:99` (43): "Both minimize the Gibbs free energy of three
  components over three phases, with amounts n_ip ∈ [10⁻⁷, b_i] and mass
  balances Σ_p n_ip = b_i. The objective is f(n) = Σ_p G_p(n_·p), where each
  G_p is a UNIQUAC phase function (an ideal vapour for the third phase of
  `ex6_2_5`) made of linear terms and terms (ℓ·n_p) ln(m·n_p)."
- **S28.** `05:197` (43): end the sentence after "bounds its cost". Then: "The
  shifts are needed because the eigenvalues of A(w) come in pairs
  (Proposition S1.x); they cost less than 4.4·10⁻⁷."
- **S29.** `05:319` (Theorem 5.x, 47 in its first sentence): "Assume
  Hypothesis H0, the correctness of the model reader, the enclosure code, the
  auditor, the exact arithmetic and the coverage checker, and the faithful
  execution and retention of the recorded run (Theorem S5.x). Read the
  decimal data as exact rationals. Then …". H0 already contains
  round-to-nearest-even and gradual underflow, so do not restate them.
- **S30.** `05:326` (45): "Lemma S5.x proves that the paddings cover all
  rounding errors under H0, provided every exponential and integer power used
  has relative error at most 10⁻¹⁴. The lemma covers every box inside the
  outward-enlarged root boxes of these searches; for arguments below −708, an
  exponential value in [0, 2⁻¹⁰²⁰] suffices."
- **S31.** `05:361` (45): "Each edge function contains a cubic B-spline. The
  encoding selects the knot interval of each edge argument by binaries and
  big-M rows and builds the basis by Cox–de Boor rows that are bilinear in
  binaries and arguments. It adds per edge three partition-of-unity rows
  Σ_m B_{e,m,p} = 1, p = 1, 2, 3."
- **S32.** `05:371` (50): "For every admissible k, exact computation over ℚ
  shows that they have no common zero in I_k. Either one of them is a nonzero
  constant or has no root there (Sturm sequence), or they have no common
  complex root (nonzero pairwise resultant, or constant greatest common
  divisor of the nonzero residuals)."
- **S33.** `05:377` (58): "Let 𝓡_P be the OSIL model without the
  partition-of-unity rows. Let 𝓡 be the network relaxation over the inputs.
  Its points are pairs (u,k) of an input u in the box of the model and a knot
  choice k that put every edge argument in its interval and every hidden value
  in its box, and its objective is F(u,k)."
- **S34.** `06:7` (47): see R5 and R8. Rewrite: "Every primal value U in this
  paper therefore bounds the objective at a point that we prove satisfies
  every row, bound and integrality requirement of the stored model exactly,
  under reading (b) (U is a lower bound for `pricing050`)."
- **S35.** `07:38–39` (46 and 45): "If s arises from b by finitely many
  roundings (to nearest or directed) or truncations to integer multiples of
  powers of ten, then |b − d(s)| < (10/9) u(s). H holds if at most one step
  changes the value, or if the last step that changes it rounds to nearest. H
  also holds if |d(s)| ≤ 6·10⁷ and the site handles numbers as follows: it
  rounds a binary64 copy of b to nearest at ten significant digits, stores
  the result in binary64, and displays it rounded to nearest at eight
  decimals. Almost all displayed values are consistent with this rule
  (Section S4.x)."
- **S36.** `07:113–114` (44 and 46). For `:113`: "So every listed dual bound of
  these instances is valid. The best listed primal values lie below v* by at
  least 1.41·10⁻⁵, 1.98·10⁻³, 2.92·10⁻⁴ and 6.86·10⁻⁶ (1.36·10⁻⁶ relative for
  `emfl050_3_3`). No exactly feasible point attains them; they are tolerance
  artifacts (category A)." For `:114`: end the sentence after "MINLPLib's gap
  tolerance", then: "The mark is consistent with the listed primal value and
  is defined with tolerance-feasible points, so we do not call it wrong."
- **S37.** `07:130`, `08:85`, `08:92`, `08:125` and `08:132` (48 to 62):
  - `07:130`: "On the 15 class (i) instances and on `rocket`, `emfl`,
    `spring` and `lop97icx`, neither the dual bound in the instance list nor
    the `=bestdual=` entry of the `.solu` file exceeds the lower end of a
    proved objective enclosure by more than display rounding. Section S4.x
    infers the rules behind these two aggregates from the data."
  - `08:85`: "In each, the first step that removes the witness is the same.
    On a row x³ − y = 0 with x fixed at fl(0.7) and y at fl(0.343), reverse
    propagation in the default nonlinear handler intersects the activity with
    [0,0]. It uses the exact routine `SCIPintervalIntersect`, not its
    ε-tolerant variant, and declares the node infeasible."
  - `08:92`: "A syntactic scan of the 1,632 OSIL files of the MINLPLib
    snapshot looks for rows y = x² or y = x³ whose bounds agree in decimal but
    not in binary64. It finds them only in nine `waterno2` instances. By
    Lemma 8.x, only the cube rows of the 0.7 stations, one per period, can
    trigger the traced cutoff (Section S6.x)."
  - `08:125`: "We ran BARON 26.5.27, Gurobi 13.0.2 and SCIP 10.0.3, in the
    versions bundled with GAMS 54.3.1, on the unmodified MINLPLib GAMS files
    of all 43 instances. Each run used one thread, a limit of 3600 s (CPU time
    for BARON, wall time for the others), requested absolute and relative gaps
    of 10⁻⁹, no option file and a memory cap of 8192 MiB, on a shared machine
    (Section S6.x)."
  - `08:132`: "On the primal side, 35 returned objective values lie beyond a
    certified bound by more than their printing precision: 30 for OSIL models
    and 5 for 𝓡. None of these points is exactly feasible. The 15 that we
    evaluated at 50 digits have largest violations between about 10⁻¹⁰ and
    10⁻⁶ (Table S…)."
- **S38.** Appendix A and one certificate box:
  - `A:25` (70): split into one sentence per instance (`lukvle10`, `pindyck`,
    `etamac`).
  - `A:38` (52): "In type O, d(σ) is enclosed in an interval. The interval is
    built by mpmath from σ (at 53 or 64 bits, or at 30 to 60 digits), or lies
    between the two binary64 neighbours of fl(d(σ)), or is an mpmath interval
    quotient of the numerator and denominator of d(σ), or is a dyadic floor
    and ceiling."
  - `A:47` (55): "Finally, we tested the O-type string conversions directly on
    all 164,791 distinct numeric strings of the 46 OSIL files involved: the
    43 stored models and `rocket100`, `rocket200` and `rocket400` from the
    audit. Each conversion, and the mpmath interval of the shortest binary64
    round-trip string, contains d(σ); the quotient and dyadic conversions are
    outward by construction."
  - `A:88` (51): end the first sentence after "auxiliary variables".
  - `A:94` (55): "Their existence certificates succeed again when every datum
    that is not a binary64 number is replaced by its binary64 value. The upper
    ends of the objective enclosures change by at most 2.13·10⁻¹⁰ in absolute
    terms and 2.8·10⁻¹² relative, and every margin still exceeds 1.11 display
    units of the listed bound (computed, one implementation; Section S4.x)."
  - `A:101` (51): end the first sentence after "by a factor of 4 in one
    coefficient", and give dtoc5 and optcdeg2 one sentence each.
  - `05:257` (certificate box, 62): give `etamac` and `pindyck` separate
    \certitem lines.

---

## 9. Other style-guide points (H)

**H1.** These openings announce the section: `A-semantics.tex:7` ("This
appendix gives the details behind …"), `G-proofs-split.tex:10` ("This appendix
proves …") and `09-interpretation.tex:15` ("this section interprets both
facts"). Rewrite:

- `A:7`: "Definition 2.1 and Remark 2.3 rest on the following details of the
  OSIL files and of our readers."
- `G:10`: "We prove the validity results of Section 4.1 in the form that the
  certificates use: …".
- `09:15`: "… and the certificates of Sections 4 and 5 did. We interpret both
  facts below."

**H2.** `06-points.tex:13–16` uses inline italic labels "(A) *Explicit exact
points* … (D) *Strictly interior points*" as pseudo-headings inside one prose
paragraph. Rewrite: a four-item description list headed by the words
("Explicit exact points", "Triangular definitions", "Interval existence
proofs", "Strictly interior points"), without letters (see T1).

**H3.** `G-proofs-split.tex:13` holds a TODO that prints in the PDF (separate
check of the extended-value proofs; register PT-06). Resolve it, or move it to
`integration-notes`, before submission.

**H4.** `10-reproducibility.tex:68` says "Several scripts write logs or
certificates when imported or run, and some overwrite stored evidence …". In
the main text this reads as a defect of the artifact, and a referee will ask
why it was not fixed. Rewrite: fix the scripts before archiving if possible,
move the details to S7, and keep in §10: "Every command runs in a disposable
copy of the archive (Section S7.x)."

**H5.** `04-split.tex:334` (chain certificate box) says "the other became so
after a one-line fix of its pruning test". This is development history.
Rewrite: "two separately written codes certify the same four values; both are
outward-rounded throughout (Section S1.4 records a correction to the
second)."

**H6.** `03-results.tex:27` says "No separate review checked the census or the
selection code". This is review-round language, which the style guide keeps
out of the main text. Rewrite: "The census and selection code were not read
by a second party; three separately written programs reproduce every count."

**H7.** `05-other.tex:136` (certificate box) says "S, Tier 2, 258 s and 77 s;
C, Tier 1, 28 s", which does not say which value belongs to which instance.
Rewrite: "`ex6_2_5`, `ex6_2_7`: level S, Tier 2, 258 s and 77 s;
`pricing050`: level C, Tier 1, 28 s."

**H8.** `10-reproducibility.tex:44` says "some certificate boxes quote other
runs of the same or an equivalent check". This is vague, and a reader cannot
tell which boxes. Rewrite: name them ("the boxes of `optcdeg2`, …"), or quote
the claim-register run in every box (integration-notes-r1 §8 item 7).

---

## 10. Count

| group | items |
|---|---:|
| B overclaims and qualifier drift | 8 |
| T terminology and notation | 20 |
| J jargon, internal names, forward references | 25 |
| L unclear logic | 20 |
| R repetition | 21 |
| S long sentences | 38 |
| H other style-guide points | 8 |
| **total** | **140** |
