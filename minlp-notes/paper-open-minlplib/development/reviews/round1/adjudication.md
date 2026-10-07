# Round-1 adjudication: consolidated change list

Date: 2026-10-04. Paper: `paper-open-minlplib` (main: Sections 1–11,
Appendices A and B; supplement: S1–S8). Inputs: the ten round-1 reviews in
this folder (`sol-math-main.md`, `sol-math-supp1.md`, `sol-math-supp2.md`,
`sol-numbers.md`, `sol-literature.md`, `sol-referee.md`, `opus-referee.md`,
`opus-math-main.md`, `opus-claims.md`, `opus-writing.md`), the follow-up
results (`kan-guard/report.md`, `eg-dyadic/`, the reruns reported in
`sol-numbers.md`), the lead-author decisions LD-1 to LD-7, and the
development records (`development/outline.md` §8, `style-guide.md`,
`terminology.md`, `decision-register.md`, `open-items.md`, the dossiers and
`research-20260929/` reports).

Source references use the review file stem and its item number, for example
`opus-writing 5` or `opus-referee M4`. Line numbers refer to the sources as
reviewed on 2026-10-04.

## 0. How to use this file

- Each item has an id (`Gk-nn`), its sources, a severity (blocker, major,
  minor; the highest among its sources), a decision (accept,
  accept-modified, reject) with a one-line reason, the change, and the files.
  Sub-points that are rejected inside an accepted item are marked
  "rejected part". All full rejections are also listed in Section 9.
- Where a reviewer gave replacement text, it is quoted here, with any
  modification already applied. "As given" means: use the quoted text.
- Editors work in parallel on their own files. Shared files have one owner:
  every generated table and `data/numbers.json` belong to G7 (edit the
  generators, never the generated `.tex`); `figures/make_fig_headline.py`
  belongs to G2. A group that needs a generator change names it in its item,
  and G7 makes it.
- Rules that apply to every group:
  1. Do not edit `research-20260929/` or `literature/`. Do not commit.
  2. Never run a scientific script in place; copy it and its inputs to
     `/tmp`. Use at most two CPU cores, with `OMP_NUM_THREADS=1
     OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`.
  3. Certified numbers change only where a review proved a display unsafe
     (items G4-04, G7-05, G7-07, G4-03/G7-09). Each changed display is
     checked exactly (`fractions.Fraction`) against its source in `/tmp`, and
     the check is recorded in the item's log or in `data/check.log`.
  4. Every theorem statement and every qualifier of a claim stays, in the
     main text or with a cross-reference to its single full statement.
     Length cuts remove repetition, not conditions.
  5. Agent-work vocabulary (from LD-1): write "a separate agent session" for
     work that the supplement now calls a "second party", "different party"
     or "separate review"; never write "independent" without the §2.6
     definition; reserve "by hand" for `\evid{hand}` (a proof written out
     without computation), not for how certificates were constructed.
  6. One home per repeated statement (`opus-writing 52`, `opus-referee M1`,
     `sol-referee 5`): the full statement appears once, elsewhere a clause
     with `\cref`. Homes: semantics and readings §2.1; status words and
     separately written code §2.6; eg trust base Theorem 5.14 (its
     hypotheses stay in the theorem) with §2.5 giving one sentence; KAN
     tolerance disclaimer §5.5; BARON tolerance-level closures §8.1; SCIP
     defect §8.2 (Box 2); prior status and every priority credit §3.4;
     "not a solve rate" §3.1; the 13 earlier-violating closures §6.2;
     the waterno2 priority waiver §3.4 (one phrase: "period decomposition").
- Order of work: G1–G6 text edits and G7 generator edits in parallel; G2/G3
  remove main-text certificate boxes only after G5/G6 have merged them into
  the supplement (G5/G6 take the box text from `git show
  HEAD:paper-open-minlplib/sections/04-split.tex` and `05-other.tex`); G7
  rebuilds and validates the claim register last (G7-15), after every other
  edit; then `make`, the checks of `development/build.md`, and the float
  check of G7-03.

## 1. Lead-author decisions

| id | decision | implemented by |
|---|---|---|
| LD-1 | AI-use disclosure: (a) define "separately written implementation" truthfully in §2.6 and state the common-mode risk and mitigations; (b) AI-use statement in the declarations, marked [authors to confirm wording]; funding, competing interests, licence and `\archiveDOI` stay marked placeholders. | G1-01, G1-02, G1-06, G4-01, G5-02, G6-02, G7-12, G7-15 |
| LD-2 | Length: Sections 1–11 to about 38 pages (now 45.8); supplement body to about 100 pages (now about 130). Remove repetition; keep every theorem statement and qualifier; full proofs stay in the supplement or Appendix B. | page budget (Section 2); G1-09, G2-09, G2-15, G3-02, G3-13, G4-09, G5-01, G5-14, G6-01, G6-12, G7-18 |
| LD-3 | Fix the clipped Table 2 and Table S42 and any other cropped float. | G7-01, G7-02, G7-03 |
| LD-4 | Figure 1 and §8: separate original-model comparisons from KAN relaxation comparisons, tightened-domain SCIP values and BARON values without a globality guarantee. | G2-01, G4-05, G7-06 |
| LD-5 | §9 is an interpretation, not lessons or tested findings; reframe the §1 lessons. | G1-06, G4-06, G4-08 |
| LD-6 | Apply all accepted findings; reject only with a stated reason. | this file; Section 9 lists the rejections |
| LD-7 | Rebuild and validate `artifact/claims.json` after all edits; the reproduction text must describe the artifact accurately. | G7-12, G7-15 |

## 2. Page budget (LD-2)

Pages are measured in the build of 2026-10-04 19:57 (`build/main.pdf`, 62
pages; `build/supplement.pdf`, 138 pages).

| part | now | target | group |
|---|---:|---:|---|
| §1 Introduction | 5.5 | 4.0 | G1 |
| §2 Semantics and verification | 6.0 | 5.0 | G1 |
| §3 Results | 4.0 | 3.25 | G2 |
| §4 Split certificates | 8.0 | 6.75 | G2 |
| §5 Other classes | 8.0 | 6.5 | G3 |
| §6 Points | 2.0 | 1.75 | G3 |
| §7 Audit | 4.0 | 3.25 | G3 |
| §8 Solvers | 3.0 | 2.75 | G4 |
| §9 Interpretation | 3.0 | 1.5 | G4 |
| §10 Reproducibility | 1.0 | 1.0 | G4 |
| §11 Conclusion and declarations | 2.8 | 2.25 | G4 |
| **Sections 1–11** | **45.8** | **38.0** | |
| Appendix A (outside the target) | 3.5 | 3.0 | G1 |
| Appendix B (outside the target) | 4.5 | ≤ 4.5 | G2 |

| supplement part | now | target | group |
|---|---:|---:|---|
| S1.1 lnts, lukvle10 | 8 | 6 | G5 |
| S1.2 dtoc5, optcdeg2 | 8 | 6 | G5 |
| S1.3 camshape | 6 | 5 | G5 |
| S1.4 chain, catmix | 10 | 7.5 | G5 |
| S1.5 small instances | 10 | 7.5 | G5 |
| S1.6 powerflow | 7 | 5.5 | G6 |
| S1.7 eg | 8 | 6 | G6 |
| S1.8 waterno2 | 7 | 5.5 | G6 |
| S1.9 ann, KAN | 8 | 6.5 | G6 |
| S5 eg rounding (F) | 8 | 5.5 | G6 |
| S2 points (C) | 8 | 6 | G7 |
| S3 literature (D) | 7 | 5.5 | G7 |
| S4 audit (E) | 13 | 10.5 | G7 |
| S6 solvers (H) | 13 | 10 | G7 |
| S7 reproduction (I) | 6 | 5 | G7 |
| S8 displays (J) | 3 | 2 | G7 |
| **Supplement body** | **130** | **100** | |

Group targets: G1 9.0 main pages (+ Appendix A 3.0); G2 10.0 (+ Appendix B
≤ 4.5); G3 11.5; G4 7.5; G5 32 supplement pages; G6 29; G7 39.

The largest single savings, already assigned: the twelve main-text
certificate boxes move to the supplement (about 2 pages; G2-09, G3-02, merged
by G5-01, G6-01), the contribution list is regrouped (about 1.5 pages;
G1-07), Table 7 is dropped and §9 halved (about 1.5 pages; G4-06), Table 1
becomes compact (about 0.5 page; G7-04), the selection funnel moves to S3.4
(about 0.3 page; G2-03).

---

## 3. G1 front: `00-abstract`, `01-introduction`, `02-semantics`, `A-semantics`

### G1-01 Provenance of the implementations (§2.6)
- Sources: LD-1(a); opus-claims 1, 10; opus-referee M3; opus-writing 2; sol-referee 10.
- Severity: blocker. Decision: accept-modified. Reason: the development
  records show that all implementations and reviews are AI-agent work
  (`decision-register.md` G-09, O-3; `dossiers/primal-points.md:471`;
  `dossiers/camshape.critique.md:3`; `research-20260929/README.md:6`), while
  the text reads as independent human work. The records also show that the
  second sessions could read the first code and sometimes did
  (`research-20260929/reviews/wave3-verification/verification-report.md`:
  "read to learn file formats";
  `research-20260929/reviews/wave2-small-verification/verification-report.md`: read
  "only after my own numbers existed"; ann: read in full), and that one OSIL
  reader is shared in several families (`dossiers/small.md:787`,
  `dossiers/waterno2.md:879,1065`,
  `research-20260929/reviews/cops-verification/verification-report.md`: "The
  authors' `osilx.py` is byte-identical"; `dossiers/powerflow.md:24`). The
  definition must not claim more independence than this. The model of each
  session is not recorded consistently (some reviews say "Codex review
  sub-agent", others "Claude agent"), so the text must not claim cross-model
  diversity as a mitigation.
- Change: replace `sections/02-semantics.tex:191–196` and `:206–211` by the
  following (keep `:197–200` after the second paragraph, adjusted by G1-02):

  > The certificates, their checking programs, the separately written
  > re-implementations and the code and proof readings that the supplement
  > reports were produced with AI coding agents (Anthropic Claude and OpenAI
  > GPT models) directed by the authors; the project records do not identify
  > the model of every session. No person outside the authors has checked
  > the code or the proofs. [authors to confirm wording, and to state which
  > proofs or codes the authors read themselves.]
  >
  > The *first implementation* of a certificate is the code that produced it
  > (the supplement's *authors' code*). A *second implementation* (the
  > *verifier's code*) was written later, in a separate agent session that
  > received the statement to be checked, the model files and the stored
  > inputs, and wrote its own code. We call it *separately written*: it
  > neither imports nor runs the first implementation in its checking
  > computation (some second sessions ran or imported first code for side
  > comparisons, which the records name and no certificate uses). This is
  > weaker than independent development. The sessions
  > shared one file system, so a second session could read the first code;
  > the verification records state where it did, for example to learn file
  > formats or to compare parameters after its own results existed, and the
  > session that wrote the second bounding code for `ann_cumene_tanh` read
  > the first in full (`\cref{app:annkan-ann-verif}`). Three components are
  > shared by both implementations: mpmath where `\cref{tab:trust}` lists it;
  > one rigorous exponential and interval core used by both KAN bounding
  > paths; and one OSIL reader, used by both implementations in several
  > families [list the families from the verification records: at least
  > `chain`, `catmix`, the small instances, `waterno2`, `ann_cumene_tanh` and
  > KAN], whose output separately written readers reproduced exactly for
  > [`waterno2`, `ann_cumene_tanh` and the KAN instances]. Apart from these
  > exceptions, every computer-assisted dual certificate has at least two
  > separately written implementations, which need not certify the same
  > value (`\cref{tab:trust}`).
  >
  > Agent sessions directed by the same authors and given the same written
  > statements can share a misreading of the model or of the statement;
  > separately written code reduces this common-mode risk less than code
  > from independent teams would. The following reduce it without removing
  > it. Every check uses exact or outward-rounded arithmetic, so it does not
  > inherit rounding errors from the computation that proposed the
  > certificate. Separately written readers reproduce the shared OSIL reader
  > where stated, and the exactly compared GAMS and OSIL forms agree except
  > for the `catmix` coefficients. MINLPLib's listed points have small
  > residuals under our readers, which a misread coefficient that matters at
  > those points would destroy. SCIP, with its own OSIL reader, accepts
  > binary64 roundings of our points at tight tolerances, such as
  > $10^{-12}$ for `chain` (floating-point evidence only). The point checks
  > and many dual checks include negative controls. Finally, the archive
  > stores certificates, inputs and logs, so that others can replay every
  > check (`\cref{sec:repro}`).

  Before inserting the bracketed family lists, the editor checks them against
  the verification reports named above and against the "readers" column of
  Table 1 (G7-04); if a family's reader sharing cannot be confirmed, leave it
  out of the list rather than guess. Side uses of first code are recorded in
  `research-20260929/reviews/waterno2-recheck.md` (first code imported for
  one objective comparison) and `reviews/wave3-verification/verification-report.md`
  (first code run "as a black box only where a check says so"); if any
  displayed value rests on such a run, name that family as an exception.
- Files: `sections/02-semantics.tex`.

### G1-02 Status words (§2.6)
- Sources: opus-writing 1; opus-claims 4 (paper side); sol-referee 10.
- Severity: major. Decision: accept. Reason: the three status words overlap
  and are used inconsistently (`A-semantics.tex:99–100`, `07-audit.tex:59`).
- Change: replace `02-semantics.tex:204` by, as given:

  > We use three words for the status of a statement. It is *proved* if a
  > pen-and-paper argument, or a computer-assisted proof at one of the
  > evidence levels of `\cref{sec:semantics-trust}`, establishes it. It is
  > *verified by a separately written implementation* if, in addition, a
  > second implementation reproduced its computer-assisted part. It is
  > *computed* if a single implementation produced it and we do not present
  > it as proved; we label such statements with this word and do not use
  > them as premises. Interpretation, like numerical evidence, never
  > supports a claim.

  Then: `07-audit.tex:59` becomes "proved by one implementation" (G3-09);
  `A-semantics.tex:99–100` keeps "computed, one implementation" and "we do
  not claim it". G7-12/G7-15 print the status per register row.
- Files: `sections/02-semantics.tex`.

### G1-03 Abstract
- Sources: LD-2; opus-referee M2 (a)–(d); opus-writing 9; sol-referee 4, 8, 12.
- Severity: major. Decision: accept-modified. Reason: the abstract must say
  that for seven closures the gain is mainly rigor, state the size breakdown
  of the 22 refutations, qualify `ann_cumene_tanh`, and replace "closed no
  instance under exact feasibility" (true almost by construction) by the
  informative comparison. Modifications to opus-referee M2: the margins are
  proved lower bounds on the excess, so "eleven by less than the gap
  tolerance" becomes "eleven proved margins are below $10^{-6}$ relative";
  the text is cut to 250 words.
- Change: replace `00-abstract.tex:4–15` by (250 words; keep ≤ 250 in the
  source count; if a later edit adds words, shorten the device list last):

  > MINLPLib lists tolerance-feasible points and solver-reported dual bounds
  > and marks an instance solved when three solvers claim global optimality;
  > none of these records is a proof. We study 43 nonconvex instances
  > without this mark, reading stored decimals as rationals and requiring
  > exact feasibility. For 31 instances we prove a dual bound and exhibit an
  > exactly feasible point within a relative gap of at most $3.1\cdot10^{-9}$;
  > for nine we characterize the optimal value exactly, and for seven,
  > floating-point closures or near-closures had been reported. For five
  > pump-scheduling instances we raise the best listed dual bounds 1.68- to
  > 6.21-fold, leaving gaps of at most 10.82%; for `ann_cumene_tanh`, whose
  > exp variant has floating-point closures, we prove a bound with gap
  > 0.195%. The six Kolmogorov–Arnold network instances in our set have no
  > exactly feasible point; without their partition-of-unity rows we enclose
  > their optima within $2.42\cdot10^{-8}$. The certificates combine
  > classical devices (Lagrangian and SDP duality, calibrations, Sturm
  > comparison, hidden convexity, Taylor models) with exact or
  > outward-rounded arithmetic; apart from named exceptions, separately
  > written code rechecks them, sometimes only for a weaker bound or part of
  > the domain. Of the 11,086 per-solver dual bounds MINLPLib lists, we prove
  > 22 invalid under a stated hypothesis on page displays; four of the
  > proved margins exceed 1%, eleven are below $10^{-6}$, relative. We report
  > a seed-dependent SCIP 10 error giving wrong optimal values on `waterno2`
  > subproblems. No dual bound from one-hour BARON, Gurobi and SCIP runs
  > reached ours; BARON reached tolerance-level closures on two instances.
  > Code, certificates and points are archived.

  The abstract mentions no AI use; the disclosure is in §2.6 and the
  declarations (LD-1). Rejected part: opus-referee M2's suggestion to move
  `ann_cumene_tanh` out of the abstract (the qualifying clause suffices).
- Files: `sections/00-abstract.tex`.

### G1-04 Opening paragraph of §1
- Sources: opus-writing 10; opus-referee m3.
- Severity: minor. Decision: accept opus-writing 10; reject opus-referee m3
  (removing the numbers). Reason: sol-referee praises the numerical opening;
  repetition is removed from the contribution list instead (G1-07).
- Change: replace `01-introduction.tex:7–8` by, as given:

  > For 31 of them we prove a dual bound and exhibit an exactly feasible
  > point within a relative gap of at most `\sci{3.1}{-9}`; for nine of these
  > we characterize the optimal value exactly. For six more we raise the
  > best listed dual bound or, where none is listed, prove one. We apply the
  > same standard to the library's records and to solver output. Under a
  > stated hypothesis on how MINLPLib's pages display numbers, we prove 22
  > of its listed per-solver dual bounds invalid, and we report a
  > seed-dependent error in SCIP~10 that returns wrong optimal values on
  > subproblems of `waterno2_06`.
- Files: `sections/01-introduction.tex`.

### G1-05 Wording of §1.1
- Sources: opus-referee m4, m5; opus-writing 11, 12, 13, 14, 15; sol-referee 12.
- Severity: minor. Decision: accept (m5 merged with sol-referee 12).
- Change:
  - `:13` "MINLPLib, the reference against which MINLP solvers and methods
    are measured," → "MINLPLib, a standard benchmark library for MINLP
    solvers and methods,".
  - `:19` "It is a consensus label, not a check." → "The solved mark is
    thus a consensus label, not a check."
  - `:22` "These records are nevertheless used as facts." → "These records,
    and solver claims of the same kind, nevertheless serve as reference
    values." (sol-referee: "used as facts" is broader than the cited uses.)
  - `:26` → "If a listed point is feasible only within a tolerance, or a
    reported bound is invalid, every such use inherits the error."
  - Box 1, `:40` → "so the gap between the listed bounds compares a valid
    but weak dual bound with a value below the optimum."
  - `:43–45` → as given in opus-writing 15: "Even where the listed dual and
    primal values nearly agree, the listed point need not be exactly
    feasible. For `lnts50` the best listed dual bound lies within
    `\sci{3.9}{-5}`, relative, of the optimum, yet the best listed point,
    p1, violates rows by up to `\sci{9.1}{-10}`, and its objective lies at
    least `\sci{4.30}{-11}` below the exact optimal value
    (`\cref{thm:lnts-opt}`)."
- Files: `sections/01-introduction.tex`.

### G1-06 §1.2: approach and observations instead of lessons
- Sources: LD-5; opus-referee M4 (lesson 1), m1, m2, m7; opus-claims 1 ("by hand"), 5, 6; opus-writing 4 (lesson 2), 16.
- Severity: major. Decision: accept-modified. Reason: lesson 1 holds by
  construction and is presented as a finding; lesson 2 calls `catmix` a
  split, which §4.1 denies; lesson 3 attributes amplification to equality
  chains without evidence; the SCIP trigger is stated beyond the traced
  runs. LD-5 asks to present the interpretation as such.
- Change:
  - Title: `\subsection{Approach and main observations}`.
  - `:53` → "A closure (a certified relative gap of at most $10^{-6}$,
    MINLPLib's tolerance; `\cref{def:sem-certificate}`) then needs two
    certificates: …".
  - `:54` → "We built each dual bound individually for each instance, from
    the structure of the model, and evaluated it in exact rational or
    outward-rounded arithmetic."
  - `:55` → append "(`\cref{sec:semantics-protocol}` states how these
    implementations were produced and what 'separately written' means)".
  - `:58` → "Three observations stand out; we return to them in
    `\cref{sec:conclusion}`."
  - Item 1 (opus-referee M4, adapted): "Once a bound fitted to the structure
    of the model was in place, little search remained: branching was absent
    in 12 closures and at most three-dimensional in 15 more; the `pindyck`
    certificate splits one box into 9, and the three `eg` certificates
    branch on their 7 original variables. Why general-purpose solvers did
    not find such bounds we do not test; `\cref{sec:interpretation}` offers
    an interpretation."
  - Item 2 (opus-referee m1): "Fifteen closures exploit the stage structure
    of the model: eleven split the objective along the stages
    (`\cref{lem:split-bound}`), and the four `catmix` certificates bound the
    value functions of a backward dynamic program
    (`\cref{lem:split-minorant}`); in both, every stage problem is small
    enough to be minimized rigorously (`\cref{sec:split}`)."
  - Item 3 (opus-claims 5, 6): "Exact feasibility changes the verdict on
    benchmark data and solver output. Some listed dual bounds are invalid.
    Some listed and published optimal values hold only within tolerances,
    and along long chains of coupled rows a tolerance can lower the
    objective by far more than its own size: for `camshape` we prove a
    deficit bound of about $0.6\,n^2\varepsilon$, and explicit
    tolerance-feasible points reach about 87% of it (numerical evidence).
    SCIP~10 returns wrong optimal values on some subproblems; in the 15
    wrong runs that we traced, a binary64 residual of decimal data triggered
    the error (`\cref{sec:audit,sec:solvers}`)."
- Files: `sections/01-introduction.tex`.

### G1-07 §1.3: four contribution groups instead of C1–C9
- Sources: LD-2; sol-referee 4, 5, 8; opus-referee M1.1, M2 (C3, C7), M6 (C5), m17; opus-claims 7, 13 (`:81`), 18, 19, 20; opus-writing 17, 18, 19, 20.
- Severity: major. Decision: accept-modified. Reason: nine contributions
  repeat the abstract and §3; the referees ask for three or four groups with
  the counts once. C8 moves out (its content is §4's opening and §9).
  Modification: four groups, not five; every qualifier listed below stays.
- Change: replace `:72–148` by four `description` items of at most 9 lines
  each (target −1.5 pages). Required content and wording:
  - **C1 (certificates under exact semantics).** 31 closures, "28 continuous
    and three mixed-integer, from 14 instance families" (checked:
    `numbers.json` has integer variables only in the three `eg` closures;
    §9 counts 14 families); gap ≤ `\sci{3.1}{-9}`; nine exact optima,
    attained; the search-scoped priority sentence of `:80`; "For seven of
    them, floating-point closures or near-closures of the same model, or for
    `dtoc5` of a copy under assumed variable bounds, were reported;
    `\cref{sec:results-prior}` credits these and the other earlier results
    by name" (opus-claims 13). Primal side (opus-referee m17, as given):
    "Every primal value is the upper end of a rigorous enclosure (the lower
    end for `pricing050`) at a point proved exactly feasible; for 13
    closures the floating-point points that first indicated a closure
    violate rows by `\sci{2.4}{-20}` to `\sci{7.91}{-12}`, and we replace
    them using classical existence tests (`\cref{sec:points}`)." waterno2
    with factors 1.68–6.21, gaps, and "we claim no priority for period
    decomposition"; `ann_cumene_tanh` with the clause that the bound applies
    to `ann_cumene_exp`, which SCIP and LINDO closed in floating point, and
    that our rigorous bound is weaker than their values; KAN: exact
    infeasibility of the six stored models, the enclosure of $\RP$ with
    widths `\sci{2.42}{-8}` and `\sci{1.08}{-10}`, "they say nothing about
    points that satisfy the OSIL rows only within a tolerance". Trust: one
    sentence pointing to `\cref{tab:trust}`.
  - **C2 (audit of listed dual bounds).** Screen of 11,086 bounds against
    2,816 points; settled only by proved existence; 22 bounds on 18
    instances invalid under `\cref{hyp:audit-display}`: 19 on 15 from the
    screen, each proved again by a second implementation, and three LINDO
    bounds on `rocket100`–`rocket400` outside it. Add (opus-referee M6):
    "Every class (i) margin is at least $1.115\,\dunit{s}$, so these 19
    refutations need only that the display arises from the reported number
    by decimal roundings or truncations; of all 22 refutations, only
    `rocket100` (1.06 units) needs Hypothesis~H itself." Margin breakdown:
    four above 1% of $|\dval{s}|$, seven between `\sci{1.2}{-5}` and
    `\sci{7.4}{-5}`, eleven below $10^{-6}$; no refutation contradicts a
    solved mark; emfl sentence; the search-scoped "first systematic screen
    … that settles conflicts by proving that an exactly feasible point
    exists" with the Vigerske/Nowak/Vigerske–Gleixner credits; "We attribute
    no cause to the invalid bounds."
  - **C3 (solver and published claims).** SCIP: "SCIP 10.0.2, 10.0.3, 10.1.0
    and a development snapshot" (opus-writing 18); "Exactly feasible
    rational witnesses, which SCIP 10.0.2's feasibility check accepts"
    (opus-claims 19); mechanism (opus-writing 19, scoped by opus-claims 5):
    "In the 15 instrumented wrong runs, reverse propagation declares
    infeasible a node that contains a witness: on a row $x^3-y=0$ with $x$
    fixed at $0.7$ and $y$ at $0.343$, the binary64 values satisfy
    $\fl(0.7)^3<\fl(0.343)$, although $0.7^3=0.343$ exactly
    (`\cref{lem:scip-cube}`)"; dated tracker search. CAMINO with its two
    assumptions (G4-04) and "invalid as recorded; the cause is unknown".
    MINOTAUR (opus-claims 20): "MINOTAUR~0.4.1's infeasibility report for
    QPLIB\_8803 is invalid as recorded (cause unknown), assuming that its
    `.nl` file encodes the MINLPLib model `optcdeg2`." One-hour comparison
    (sol-referee 4, opus-referee M2 C7, adapted):

    > We ran BARON 26.5.27, Gurobi 13.0.2 and SCIP 10.0.3 on all 43 instances
    > (one thread, 3600 s, requested gaps $10^{-9}$). All finite final dual
    > bounds are weaker than our certified bounds; 79 of the 109 compare with
    > a certified bound for the same model and carry a globality guarantee
    > (`\cref{sec:solvers-campaign}`). Five improve the best listed dual.
    > Only BARON's runs on `camshape100` and `camshape200` ended within
    > $10^{-6}$: their dual bounds are valid and lie within `\sci{4.80}{-7}`,
    > relative, of the exact optima, but the returned points are not
    > exactly feasible (tolerance-level closures, `\cref{sec:semantics-categories}`).
    > The comparison checks the status of current solvers on the stored
    > models; it does not rank them.

    The count 79 comes from G7-06 (generated and checked); until then it is
    a computed value (79 = 23 BARON + 30 Gurobi + 26 SCIP, from
    `research-20260929/publication/solver-runs/results.csv` flags
    `globality_warning` and `scip_argument_bounds_tightened`, KAN rows
    excluded; 6 + 6 + 18 make up the 109). Catalogue of unattainable values:
    one clause.
  - **C4 (reproducibility).** As C9, with opus-claims 18: "a number file
    with the exact source of every displayed number, a claim register that
    maps each result to its checkers and inputs, …". Keep `\archiveDOI` as
    the marked placeholder (LD-1(b)).
  - Drop C8; §4's opening (G2-07) carries the staged-class summary, and the
    window/enclosure pointers go to §4.1.
  - opus-writing 17 ("The constructions are classical"; "What is new are the
    points themselves and their second proofs by separately written code")
    and opus-claims 7 ("for all but `etamac` and `pricing050`") apply if the
    C2-style sentence survives; with the m17 merge above it is replaced.
- Files: `sections/01-introduction.tex`.

### G1-08 §1.4: prior work and what is classical
- Sources: sol-literature 1, 2, 3, 4, 5, 6; opus-referee M2 (rigorous solvers), m6; opus-writing 21; sol-referee 8; new KB sources (`literature/topics/paper-open-minlplib-L1-benchmarks-verified-go-2026-10.md` §6).
- Severity: minor. Decision: accept; rejected part: opus-referee M2's option
  to run a rigorous interval solver (Section 9, R-13).
- Change:
  - `:157` → "The benchmark records inspected in our search do not supply
    independently checkable nonlinear dual-bound certificates."
  - After `:159` add: "Their computational construction and verification
    solve the auxiliary optimization problems with Gurobi; here we require
    exact or outward-rounded verification on the stored nonconvex models."
  - `:153` locator → `\citep[slide 23, PDF p.~38]{vigerske2014-towards-minlplib-2-0}`;
    `:23` → `\citep[§3.3, author manuscript p.~23]{bestuzheva2025-...}`.
  - `:163` → `\citep[Berthold's contribution, §3.6]{bonami2018-designing-and-implementing-algorithms-for}`.
  - After `:166` add two sentences (sol-literature 3; opus-referee M2):
    "Current interval solvers such as IbexOpt combine reliable affine and
    Taylor relaxations and certify LP-derived lower bounds by interval
    post-processing `\citep{araya2025-hybridizing-two-linear-relaxation-techniques}`;
    when they search for points they relax equality rows by a tolerance. We
    did not run such a solver: its bounds would need the same exact
    existence proofs for points that our certificates supply."
  - After `:167` add one compact sentence (sol-literature 4): "Recent work
    certifies propagation and dual proof analysis in an exact MIP solver
    `\citep{borst2024-certified-constraint-propagation-and-dual}`, builds
    VIPR certificates from black-box floating-point ILP solvers
    `\citep{szeider2026-vipr-certificate-construction-from-black}` and
    analyses the numerical correctness of branch-and-bound decisions
    `\citep{hoen2025-analyzing-the-numerical-correctness-of}`; these
    certify linear MIP results, whereas our obligations are nonlinear and
    sometimes transcendental." Optional, same sentence budget: "Xpress
    Global withholds a global-optimality claim when it imposes artificial
    bounds `\citep{belotti2025-solving-minlps-to-global-optimality}`, and
    Sudermann-Merx pairs a solver-reported $\varepsilon$-global bound with
    exactly recovered coordinates `\citep{merx2026-from-computational-certification-to-exact}`;
    in both the global bound remains solver output." (Hoen and Gleixner
    have two authors; write "Hoen and Gleixner" where named.)
  - `:170–174` → opus-referee m6, as given: "Every mechanism in our
    certificates is classical: Lagrangian decomposition [cites], Krotov- and
    Mangasarian-type sufficiency [cites], discrete Sturm comparison [cite],
    the Gibbs tangent-plane test [cites], hidden convexity [cite], SDP
    relaxations of optimal power flow [cites], Taylor models and affine
    arithmetic [cites], interval existence tests [cites] and rational PSD
    certificates [cite]. What is new are the instance-specific
    constructions, their exact or outward-rounded evaluation on the stored
    models, and what they show about benchmark data and solver claims."
    Keep every current citation key. sol-referee 8: add one sentence naming
    the distinctive constructions: "the exact `camshape` envelope, the
    scalar `lnts` characterization and the curved `optcdeg2` split are
    examples."
- Files: `sections/01-introduction.tex`; bibliography entries in G7-14.

### G1-09 §1.5 Organization
- Sources: LD-2. Severity: minor. Decision: accept.
- Change: two sentences; drop the enumeration of supplement sections (the
  supplement has a table of contents).
- Files: `sections/01-introduction.tex`.

### G1-10 §2 opening and §2.1
- Sources: opus-writing 22, 23, 24, 8; opus-math-main 1 (lines 44, 53); opus-referee M7.3.
- Severity: minor. Decision: accept.
- Change:
  - `:5` → opus-writing 22, as given: "Under this semantics a dual bound must
    hold for every exactly feasible point, and a primal value must come from
    a point proved to satisfy every row exactly; a listed or reported value
    that fails either test is a tolerance artifact or an invalid claim
    (`\cref{sec:semantics-categories}`)."
  - `:35` → "The smallest $\varepsilon$ for which a point is
    $\varepsilon$-feasible, its largest violation, is the measure that
    MINLPLib records for listed points."
  - `:44` → opus-math-main 1 with opus-writing 24: "*Unless a statement
    names another reading, every claim in this paper concerns \reading{b}*,
    following exact MILP solvers, which treat input data as rational numbers
    and floating-point data as approximations of them [cites]. The
    exceptions are the transfer of the `catmix` bounds to \reading{a}
    (`\cref{prop:catmix-transport}`), the statements about \reading{c} in
    `\cref{rem:sem-readings}`(2) and `\cref{app:semantics-binary64}`, and
    the statements about binary64 data of small derived models in
    `\cref{sec:solvers-invalid}`."
  - Remark 2.3(1) → "Readings (a) and (b) define the same model for every
    instance of this paper except the four `catmix` instances; the
    comparison is exact for 21 instances and numerical evidence for the
    others (`\cref{app:semantics-gams}`)." Drop the clause from `:51`.
  - Remark 2.3(2), `:53–54` → "For \reading{c} we claim only the following:
    `lukvle10` (integer data) is the same model; our `lnts` points stay
    exactly feasible (only inactive angle bounds change); and our points of
    `dtoc5`, `chain`, `powerflow` and `waterno2` are not feasible
    (`\cref{app:semantics-binary64}`)." G1-16 supplies the proofs.
  - Listed data, after `:60` (opus-writing 8; opus-referee M7.3): "MINLPLib's
    instance list also gives one dual bound per instance, formed from the
    per-solver bounds by trusting a bound only if other solvers confirm it
    `\citep{vigerske2014-minlplib-2}`; we call it the *dual bound in the
    instance list*. It can be weaker than the best listed dual." Elsewhere
    in the main text use only "best listed dual" except §7.5 and §11.
- Files: `sections/02-semantics.tex`.

### G1-11 §2.2
- Sources: opus-math-main 8; opus-writing 25; opus-claims 17.
- Severity: minor. Decision: accept.
- Change: `:78` add "(the lower end for maximization)". `:98` → "For a
  Lagrangian-type certificate, a point that satisfies the kept constraints
  and violates the dualized rows by at most $\tau$ can lie below $\Lcert$
  only by an amount that the multipliers control." `:99` "where $X$ holds
  the constraints" → "where $X$ is the set defined by the constraints that
  the certificate keeps". `:101` → "The sum $\|\lambda\|_1+\|\mu\|_1$ can
  grow with the length of a chain of coupled rows."
- Files: `sections/02-semantics.tex`.

### G1-12 §2.3
- Sources: opus-writing 26, 27. Severity: minor. Decision: accept.
- Change: `:133` → "Category~A covers values on both sides of the optimum.
  The listed points p2 of `camshape400` and `camshape800` lie below the
  optimal value; the listed points p1 and p2 of `hvycrash` have the value
  $-0.21413$, above the value $-0.2185$ of every exactly feasible point."
  `:137` → "A solver run reaches a *tolerance-level closure* if it reports a
  valid dual bound and, at a point feasible within its tolerances, a value
  within its optimality tolerance of that bound; we credit such results by
  name (`\cref{sec:results-prior}`)." Move this sentence after the closure
  discussion of §2.2 (after `:79`).
- Files: `sections/02-semantics.tex`.

### G1-13 §2.4 Display rules
- Sources: sol-referee 12; opus-math-main 2; opus-writing 28; LD-2.
- Severity: minor. Decision: accept. Reason: "Every printed number remains
  true as printed" is a slogan; `\dunit` is defined twice with different
  meanings (they differ for strings with trailing zeros); the §7.2
  definition is the one Lemma S4.1 needs.
- Change: `:141` → "Certified displays are rounded in a direction that
  preserves the bound." Delete `:148` (the `\dunit` definition); §7.2 keeps
  its definition (`07-audit.tex:30`), and `A-semantics.tex:99` writes
  `\dunit{s}` (G1-16). Shorten the subsection to at most 6 lines.
- Files: `sections/02-semantics.tex`.

### G1-14 §2.5 Arithmetic, trust base and evidence levels
- Sources: opus-referee m8, m9, M7.2; opus-claims 3 (definition), 9; opus-math-main 4; sol-referee 2, 12; opus-writing 3 (`:183`).
- Severity: major. Decision: accept-modified (opus-referee m8 and
  opus-claims 9 merged).
- Change:
  - `:158` → "No proof of record assumes an accuracy bound for the elementary
    functions of NumPy, the C mathematical library or Intel SVML; mpmath's
    interval functions are trusted where `\cref{tab:trust}` shows \arith{I},
    and the second audit checker additionally assumes an accurate 90-digit
    mpmath exponential (`\cref{app:audit}`)."
  - H0, `:163` (opus-math-main 4): replace "In particular" by "and, in
    addition, the conversion of a rational number (Python `Fraction`) or of
    a decimal string to binary64 is correctly rounded (true of CPython's
    `float`), `nextafter` returns …".
  - `:169–177`: replace the T-* list by one sentence naming the trusted
    components in words (integer and rational arithmetic, H0, mpmath
    interval arithmetic for named primitives, the OSIL reading of
    Definition 2.1, the named checking programs, classical theorems); the
    labels T-int … T-thm are defined in S7 only (G7-12).
  - Evidence levels, `:178–180`: "`\evid{hand}`, a proof written out in
    full, without computation; `\evid{stored}`, a computer-assisted proof
    whose stored finite certificate is checked by exact or outward-rounded
    replay; `\evid{rerun}`, a computer-assisted proof whose check reruns a
    search or the numerical computation that produced its data, because
    these are not stored. For `eg` the leaf partition is stored and checked
    for coverage; only the per-leaf certificates are recomputed." (opus-referee
    m9; sol-referee 2 needs `rerun` to cover the regenerated `catmix`,
    `emfl` and `topopt` data.)
  - `:181` (sol-referee 12) → "Numerical evidence, such as floating-point
    solves, high-precision evaluation or random sampling, is never used to
    establish a bound, an enclosure or exact feasibility; we label it as
    evidence where we report it."
  - `:183` (opus-writing 3): "reading the code showed" → "inspection of the
    code showed".
  - `:166–167` (eg): keep one sentence and point to `\cref{thm:eg-trust}`
    (repetition rule).
- Files: `sections/02-semantics.tex`.

### G1-15 §2.6: replay and tiers
- Sources: opus-math-main 12; opus-referee M7.2; LD-2.
- Severity: minor. Decision: accept-modified. Reason: the tiers are defined
  by cost but assigned inconsistently (`ex6_2_5` 258 s in Tier 2,
  `pindyck` 322 s in Tier 1, `catmix` 20–46 min in Tier 3).
- Change: keep the replay/regeneration definition (`:202`); delete the tier
  sentence (`:203`) here; §10 defines the tiers by recorded wall time per
  instance: Tier 1 under 10 minutes, Tier 2 under one hour, Tier 3 longer
  (G4-07 reassigns).
- Files: `sections/02-semantics.tex`.

### G1-16 Appendix A
- Sources: opus-math-main 1 (A.4 proofs), 10, 11; opus-writing 3 (`A:43`, `A:48`), 28 (`A:99`), 51; LD-2.
- Severity: minor. Decision: accept-modified.
- Change:
  - A.4 "Points", `:84`: replace "because they satisfy equality rows whose
    coefficients change" by one-line proofs (opus-math-main 1):
    - `dtoc5`: "$\fl(8\cdot10^{-5})=4\fl(2\cdot10^{-5})$, because scaling by
      a power of two commutes with rounding, so under \reading{c} row~0 has
      the residual $(\fl(h)-h)(u_0-4y_0^2)\ne0$, since
      $\fl(2\cdot10^{-5})\ne2\cdot10^{-5}$ and $u_0\ne4$."
    - `chain`: "$\eta=1/(2N)$ is not dyadic; the dynamics rows under
      \reading{c} leave the residuals $(\eta-\fl(\eta))(u_i+u_{i+1})$, which
      cannot all vanish because $\sum_i\eta(u_i+u_{i+1})=x_N-x_0=2$."
    - `powerflow0039p`, `powerflow0039r`: "the branch 2–30 flow row has the
      residual $(b-\fl(b))\,w$ with $w\ne0$, because $P_g\ne0$."
    Before inserting, the editor verifies each statement exactly in `/tmp`
    on copies of the stored point and OSIL file (Fraction; check the
    coefficient strings, the sign convention and $u_0$). The reviewer's
    `powerflow` argument does not cover `powerflow0030p`; give an analogous
    row for it after the same exact check, or write "(computed)" for that
    instance.
  - `:43` → "Exact, outward and rounded data readings make the certificate
    valid for the decimal data of \reading{b}; a binary64 data reading does
    so only for the data that the code actually uses, which we checked case
    by case." `:48` → "Inspecting the codes also found a latent error: …".
    Rejected part of opus-writing 3: the global rename to "data entry"
    (R-15).
  - `:46` (opus-math-main 10): the second `ann_cumene_tanh` code uses a
    *rounded* reading (checked: `research-20260929/reviews/ann-extension-review-checks/annx.py`
    uses correctly rounded doubles, covered by its slack); keep "rounded"
    here, and G6-04 aligns B9.
  - `:80` → "which changes the value of no string in `lukvle10`, of two
    strings in each `lnts` and `chain` file, and of up to 3,332 strings
    (`eg_disc2_s`) elsewhere."
  - `:99` → `\dunit{s}`.
  - Table A9 (`tab:sem-gams`): keep `chain` in the "evaluation" row
    (opus-math-main 11; G5-09 weakens B4).
  - Trim A.1–A.3 by about 0.5 page where they restate §2.1 and Remark 2.3.
- Files: `sections/A-semantics.tex`.

---

## 4. G2 results and split: `03-results`, `04-split`, `G-proofs-split`, `figures/make_fig_headline.py`

### G2-01 Figure 1
- Sources: LD-4; sol-referee 4, 11; opus-referee m13.
- Severity: major. Decision: accept-modified. Rejected part: opus-referee
  m13's removal of the hollow-triangle variant (LD-4 requires a distinct
  marker for tightened SCIP models; R-08).
- Change in `figures/make_fig_headline.py` (data from `data/numbers.json`;
  ask G7 for any missing field, see G7-06):
  - Panel (a): the 37 instances with exactly feasible points (31 closures,
    five `waterno2`, `ann_cumene_tanh`). Every comparison in this panel is
    against the same stored model. Markers: certified dual (filled square);
    attained exact optimum in a separate column labelled "exact optimum",
    drawn left of a visible axis break and not as a tick "0" on the log
    axis (sol-referee 11); best listed dual (open circle); best one-hour
    dual with a globality guarantee on the unmodified model (filled
    triangle); SCIP bound on a model with tightened argument bounds (open
    triangle, plotted at its value); BARON value without a globality
    guarantee (cross, plotted at its value, not only at the flag column);
    no finite bound (arrowhead at the right edge).
  - Panel (b): the six KAN instances, titled "Different models: certified
    lower bound for $\Rnet$; listed and one-hour bounds for the stored
    models (descriptive)".
  - Optional (opus-referee m13): cap the axis at $10^{-20}$ with a break
    mark for `dtoc5` and `pindyck` and their exponents annotated; do not
    move a plotted value without the annotation.
  - Legend at most six entries; caption at most five lines, stating that
    only filled triangles are same-model comparisons with a globality
    guarantee. Run the script as `development/build.md` prescribes.
- Files: `figures/make_fig_headline.py`, `figures/fig-headline.pdf`, caption in `sections/03-results.tex`.

### G2-02 §3 opening
- Sources: opus-writing 6. Severity: major. Decision: accept.
- Change: insert after the `\section` line, as given (adapted to the new
  panels): "`\Cref{tab:closures,tab:unclosed,tab:kan}` and
  `\cref{fig:results-headline}` summarize the results: 31 closures, nine of
  them attained exact optima (`\cref{tab:closures}`); improved dual bounds
  without closure for the five `waterno2` instances and
  `ann_cumene_tanh` (`\cref{tab:unclosed}`); and enclosures for two
  relaxations of the six KAN instances, whose stored models have no exactly
  feasible point (`\cref{tab:kan}`). We first explain how we chose the 43
  instances." Move the definitions of class and prior status from the
  Table 2 caption into §3.2/§3.4 text (G7-01 shortens the caption).
- Files: `sections/03-results.tex`.

### G2-03 §3.1 Selection
- Sources: opus-referee m18, M7.3; opus-writing 29; opus-claims 1 (`03:54`).
- Severity: minor. Decision: accept-modified.
- Change: replace `:40–54` by opus-referee m18's three sentences, kept with
  the `camshape100`/`lnts50` sentence: "We chose the 43 instances from the
  155 nonconvex instances that are open by a selection rule stricter than
  MINLPLib's (`\cref{app:literature-funnel}` gives the rule and the funnel),
  in two rounds, by judged tractability; two closures, `camshape100` and
  `lnts50`, were not open by that rule, because their best listed duals were
  already within `\sci{1.22}{-6}` and `\sci{3.9}{-5}`, relative, of the best
  listed points and of our proved optima; for them what is new is the exact
  optimal value, its proof and an exactly feasible point. The 29 closures
  among the 155 are therefore not a solve rate. Three separately written
  programs reproduce every count of the funnel; no separate review session
  read the census or the selection code." The funnel counts move to S3.4
  (G7-11). This removes the main-text use of the instance-list dual.
- Files: `sections/03-results.tex`.

### G2-04 §3.2 The 31 closures
- Sources: opus-claims 3 (count); sol-referee 8, 11.
- Severity: minor. Decision: accept.
- Change: `:60` → "For the 14 closures at evidence level `\evid{rerun}`
  (`\cref{tab:trust}`), no search tree or stage data are stored" (10 + the
  four `catmix` instances, G2-09/G7-04). Add "28 of the 31 are continuous;
  the three `eg` instances are mixed-integer." Define the class and
  prior-status codes here in one short paragraph (from the Table 2
  caption). Gap cells of exact optima read "exact optimum" (G7-01).
- Files: `sections/03-results.tex`.

### G2-05 §3.3 KAN statement
- Sources: opus-claims 14. Severity: minor. Decision: accept.
- Change: `:72` → "No KAN instance is closed: the stored models have optimal
  value $+\infty$ (no exactly feasible point), and our bounds do not concern
  their tolerance-feasible points."
- Files: `sections/03-results.tex`.

### G2-06 §3.4 Prior status
- Sources: opus-claims 13; opus-writing 52; sol-referee 8.
- Severity: minor. Decision: accept-modified. Reason: `camshape200` is
  "listed solve" for a listing on a rounded copy, while `camshape800` is
  "none" despite a listed solve of its rounded copy; both listings concern a
  different model. Both become *related model* (checked:
  `numbers.json` `prior` notes; `D-literature.tex:116–127`). The partition
  changes from 7 + 8 + 16 to 7 + 9 + 15.
- Change: `:83` "Eight closures" → "Nine closures"; move the `camshape200`
  sentence to the related-model credits and add one for `camshape800`
  ("MINOTAUR is listed as solving `QPLIB_3177`, a rounded copy of
  `camshape800`; its value is not attainable on the copy
  (`\cref{prop:qplib-copies}`)"); `:90` "The other 16" → "The other 15".
  `:91` is the single home of the waterno2 priority waiver ("period
  decomposition"); §1 keeps a clause. G7-06 changes `numbers.json`; G7-11
  changes S3; G1-07 says "these and the other earlier results".
- Files: `sections/03-results.tex`.

### G2-07 §4 opening
- Sources: opus-writing 4; opus-referee m1; opus-writing 31.
- Severity: major. Decision: accept. Reason: the opening ascribes the split
  mechanism to `catmix`, which `:70` denies (outline §8 item 8).
- Change: replace `:8–10` by, as given: "Fifteen of the 31 closures form the
  staged class of `\cref{tab:closures}`: `lnts50`–`lnts400`, `dtoc5`,
  `optcdeg2`, `lukvle10`, `chain50`–`chain400` and `catmix100`–`catmix800`;
  the `waterno2` bounds use the same idea. We cut the model along its
  stages, add to each stage a function of the variables that it shares with
  the next stage, and subtract the same function from the next stage, so
  that these terms cancel at every feasible point. If each stage problem can
  be minimized rigorously, the sum of the stage minima is a dual bound. The
  `catmix` certificates use a variant: they bound the value functions of the
  stage recursion from below, and their validity rests on concavity of the
  true value functions (`\cref{lem:split-minorant}`)." Add one sentence
  from the former C8: "Two of the six instance families involved,
  `lukvle10` and `chain`, add a window of stages that is minimized exactly
  (`\cref{prop:split-window}`), and several use derived enclosures of
  unbounded states (`\cref{rem:split-enclosures}`)."
- Files: `sections/04-split.tex`.

### G2-08 §4.1 Path model and validity
- Sources: sol-math-main 1; opus-math-main 3, 13 (rename), notation remark; sol-referee 9 (part); opus-referee m10; opus-writing 30, 31, 32, 33.
- Severity: minor. Decision: accept; opus-referee m10 accept-modified (label,
  do not move; R-06).
- Change:
  - `:59` (sol-math-main 1), as given: "For nonempty control sets $U_i$ and
    maps $g_i\colon Y_{i-1}\times U_i\to Y_i$, consider the dynamics
    $y_i=g_i(y_{i-1},u_i)$ with $y_i\in Y_i$ and $u_i\in U_i$. For a
    terminal cost $\Phi\colon Y_n\to\R$, let $V_n=\Phi$ and …".
  - `:24–25` (opus-writing 30): "The costs $F_t$ take the value $+\infty$
    where an expression of the model is undefined; this encodes the domain
    rule of `\cref{def:sem-model}`(iv)."
  - After `:36` (opus-writing 31): "We also call bag~$t$ the $t$-th stage;
    its *stage problem* is the minimization of $F^\varphi_t$ over $K'_t$,
    with value the *stage infimum*."
  - `:38` (opus-writing 32): "The *split form* is the set of functions
    allowed for the $\varphi_t$: affine, quadratic, cellwise affine, and so
    on." Use "split form" throughout (§4.3 title "Richer split forms";
    `tab:staged` header via G7-06; `terminology.md` via G7-17).
  - Lemma 4.1(d): rename $h_k$ to $\psi_k$ (opus-math-main notation remark,
    nearest clash only); `:51` (opus-writing 33): "With the copy rows
    $\pi^R_tz_t-\pi^L_{t+1}z_{t+1}$ as the $\psi_k$ and
    $Y=K'_1\times\dots\times K'_N$, the bound in (d) is $B(\varphi;K')$ for
    an affine split (`\cref{prop:split-affine}`)."
  - `:85` (opus-math-main 3; sol-referee 9), as given: "By part (c), exact
    affine slopes are the copy-row multipliers of a minimizer at which every
    bag is interior; when the dynamics rows stay in the bags, part (c) does
    not apply, and the analogous computation after eliminating them yields
    the discrete costates (`\cref{app:splitproofs-affine}`). So the affine
    certificates below take their slopes from a local KKT point; validity
    never depends on this choice."
  - opus-referee m10: mark Proposition 4.3(c) and the last sentence of
    Proposition 4.5 ("SP is the largest value …") as explanatory: one
    sentence after each, "No certificate uses part (c)" / "No certificate
    uses this maximality statement." The proofs stay in Appendix B.
  - `:122–125`: keep the attributions in one sentence with all citations;
    drop "None of these devices is new" (stated once in §1.4).
- Files: `sections/04-split.tex`.

### G2-09 Main-text certificate boxes of §4
- Sources: LD-2; opus-referee M1.3, m11; opus-claims 3, 8; sol-math-main 4; opus-math-main 12.
- Severity: major. Decision: accept-modified. Reason: the boxes repeat
  Table 1 and Table 8 (opus-referee M1, m11) and cost about 1.3 pages in
  §4; the style guide requires certificate boxes, and the supplement keeps
  them. Modification: the box content is not deleted but merged into the
  supplement family sections (G5-01, G6-01); the main text keeps one
  sentence per theorem with every qualifier.
- Change: delete the seven `certbox` environments in `04-split.tex`
  (`:165, :214, :251, :278, :302, :337, :370`) after G5/G6 confirm the merge.
  After each theorem add one sentence of the form "Certificate (`\cref{…}`
  in the supplement): arithmetic \arith{…}; displayed bound from …; second
  implementation …; level …; Tier …". Required qualifiers:
  - `lnts`: two separately written integer-only codes; `\evid{hand}+\evid{stored}`; Tier 1.
  - `dtoc5`: two separately written exact codes, both give the displays; `\evid{hand}+\evid{stored}`; Tier 1.
  - `optcdeg2`: one exact code; a separately written interval code certifies 293.8760750958728; `\evid{stored}`; Tier 1.
  - `chain`: two separately written codes certify the same four values; `\evid{rerun}`; Tier 1.
  - `catmix` (sol-math-main 4; opus-claims 3, 8): "the displayed bounds come
    from one code; a separately written code certifies bounds lower by at
    most `\sci{3.7}{-10}` and, on identical test inputs for $N=100$, agrees
    with the first per stage within `\sci{9.44}{-15}`; `\evid{rerun}`, since
    the per-stage chord values are not stored; Tier 2 (20 to 46 min per
    instance)." Primal: `\evid{stored}` (exact rational state evaluation).
  - `lukvle10`: one code; a separately written one certifies
    352.238025369202; both use mpmath's interval exp and log; `\evid{rerun}`; Tier 1 (300 s).
  - `waterno2`: two separately written branch-and-bound codes, either of
    which yields every value; `\evid{rerun}`; Tier 3 for the searches.
  Tiers follow the rule of G4-07.
- Files: `sections/04-split.tex`.

### G2-10 §4.2 lnts support bound
- Sources: opus-math-main 13. Severity: minor. Decision: accept.
- Change: `:162` → "At a fixed step $h$ the objective is the constant $Nh$;
  dropping it, combining these identities with multipliers $(\mu,\nu)$ and
  applying the Cauchy–Schwarz inequality to each control gives a support
  bound; this is `\cref{lem:split-bound}`(d) in its infeasibility form
  (`\cref{prop:lnts-support}`)."
- Files: `sections/04-split.tex`.

### G2-11 §4.3 optcdeg2 motivation and chain outline
- Sources: opus-writing 5, 34, 32 (title). Severity: major. Decision: accept.
- Change:
  - Title `\subsection{Richer split forms}`.
  - `:234` → "At our exactly feasible point the control is …"; `:236` →
    "There the stage residual of the costate-affine split is not minimized
    at this point, and a floating-point evaluation with refined costates
    puts its bound about 0.6258 below the optimal value."
  - Replace `:269–274` by opus-writing 5, as given: "The linear rows express
    the heights and slopes through the heights $z_1,\dots,z_N$ of a polyline
    over a fixed horizontal mesh; its two end pieces depend only on the end
    values $z_1$ and $z_N$ (`\cref{lem:chain-polyline}`). Summation by parts
    then writes the objective with the cumulative length $v$ of the polyline
    as a second state, started at a free value $V$. For a parameter $H>0$
    let $G_H(v)=\frac12\bigl(v\sqrt{H^2+v^2}+H^2\operatorname{asinh}(v/H)\bigr)$
    and $c_H=2G_H(1/(2N))$. For the split $\varphi_k(z,v)=G_H(v)-vz-k\,c_H$,
    a closed-form inequality makes every interior stage residual
    nonnegative, with equality exactly on discrete catenaries
    (`\cref{lem:chain-calibration}`). So the objective is at least an
    explicit function $B_N(z_1,z_N;V,H)$ of the end values, for all $V$ and
    all $H>0$ (`\cref{prop:chain-endvalue}`). In this split the multiplier
    of each height difference is the cumulative length, which varies with
    the configuration as the tension of a real chain does. A fixed
    multiplier on the length row, a reverse-convex equality, does worse:
    about 4.77 against an optimum of about 5.07, in a floating-point grid
    estimate."
- Files: `sections/04-split.tex`.

### G2-12 §4.4 lukvle10 gap sentence
- Sources: sol-math-main 3; sol-math-supp1 3.
- Severity: minor. Decision: accept. Reason: the exact recomputation in
  sol-math-supp1 3 shows the summed tolerances and the gap differ by about
  `3.47e-16`; equality is not proved.
- Change: `:335` → "The certified gap is at most `\sci{1.42}{-9}` and is
  dominated by the summed branch-and-bound tolerances; global optimality of
  the exactly feasible point is not proved." (G5-05 for B1.)
- Files: `sections/04-split.tex`.

### G2-13 §4.5 waterno2
- Sources: opus-claims 5; opus-writing 31. Severity: major. Decision: accept.
  Reason: the trigger was traced in 15 runs only; one wrong run is not
  linked to the mechanism (`08-solvers.tex:90`; outline §8 item 6).
- Change: title `\subsection{Large stages: \inst{waterno2}}`. `:368` →
  "All five points use identities of the decimal data such as
  $0.7^3=0.343$; in the 15 wrong SCIP runs that we traced, the binary64
  residual of this cube identity triggered the error
  (`\cref{sec:solvers-invalid}`)." Cut `:357` to one sentence (arc weights
  from 49,315 rigorous pair bounds through an exact linear correction; the
  exact shortest path); keep Theorem 4.13 unchanged.
- Files: `sections/04-split.tex`.

### G2-14 Appendix B
- Sources: sol-math-main 1, open item 1; opus-math-main 3, 13; sol-referee 9.
- Severity: minor. Decision: accept. Both math reviews found the
  extended-value proofs correct; no proof changes.
- Change:
  - B.4, `G-proofs-split.tex:197–202` → "When $K_t$ contains equality rows
    such as discretized dynamics, its interior is empty and (c) does not
    apply. After these rows are eliminated, the same computation at a
    minimizer whose reduced stage problems are interior gives the discrete
    costate equations, as in the Lagrange form of Krotov's conditions
    [cite]. This is explanatory; no certificate uses it."
  - `:339` → "At a fixed step $h$ the objective is the constant $Nh$;
    dropping it, `\cref{prop:lnts-support}` is `\cref{lem:split-bound}`(d)
    in its infeasibility form: the $\psi_k$ are the three identities …, and
    the Lagrangian separates into one term per control."
  - Rename $h_k$ → $\psi_k$ as in G2-08.
  - Remove the first-paragraph pointer to the open check if any remains
    (open item 1 is resolved; G7-17).
- Files: `sections/G-proofs-split.tex`.

### G2-15 Length and repetition in §3–§4
- Sources: LD-2; opus-referee M1.4; opus-writing 52; sol-referee 5.
- Severity: major. Decision: accept-modified (M1.4's "statement plus 3–5
  lines" applied where the supplement has the full proof; the `lnts`,
  `dtoc5` and `camshape` worked examples stay complete).
- Change: target §3 3.25 pages and §4 6.75 pages. In addition to G2-03,
  G2-09, G2-13: shorten the `optcdeg2` proof outline (`:246–249`) to three
  sentences; cut the `catmix` outline (`:297–300`) to three sentences;
  remove every repeated priority or BARON statement (rule 6).
- Files: `sections/03-results.tex`, `sections/04-split.tex`.

---

## 5. G3 other, points, audit: `05-other`, `06-points`, `07-audit`

### G3-01 §5 opening
- Sources: opus-writing 7. Severity: major. Decision: accept (count checked:
  4 + 3 + 5 + 1 + 3 = 16).
- Change: replace `:8–10` by, as given: "The other 16 closures fall into
  five certificate classes (`\cref{tab:closures}`): *comparison* for
  `camshape`, a discrete Sturm comparison along the chain of curvature rows
  (`\cref{sec:other-camshape}`); *dense rows* for `ex6_2_5`, `ex6_2_7` and
  `pricing050`, Lagrangian duality over a few coupling rows
  (`\cref{sec:other-dense}`); *convexity* for the three `powerflow`
  instances, `etamac` and `pindyck`, SDP duality, hidden convexity and
  concavity on a polytope (`\cref{sec:other-convex}`); *identity* for
  `hvycrash`, whose rows force the objective value
  (`\cref{sec:other-hvycrash}`); and *reduced space* for the three `eg`
  instances, branch and bound over seven inputs with enclosures that keep
  cancellation (`\cref{sec:other-bb}`). The reduced-space method also
  bounds `ann_cumene_tanh` and the KAN relaxations
  (`\cref{tab:unclosed,tab:kan}`)."
- Files: `sections/05-other.tex`.

### G3-02 Main-text certificate boxes of §5
- Sources: as G2-09; opus-claims 15.
- Severity: major. Decision: accept-modified (as G2-09).
- Change: delete the five boxes (`:68, :132, :193, :242, :280`) after G5/G6
  merged them; one sentence each with the qualifiers:
  - `camshape`: "three separately written codes (two exact, one with
    directed rounding) agree on $v_n$ to all printed digits" (opus-claims
    15); `\evid{hand}+\evid{stored}`; Tier 1.
  - `ex6_2_5`, `ex6_2_7`: displayed bounds from one code; a separately
    written code confirms slightly stronger ones; `\evid{rerun}`; Tier 1
    (258 s and 77 s). `pricing050`: two codes reproduce the bound; one code
    checks the point; `\evid{stored}`; Tier 1.
  - `powerflow`: the first and the separately written exact replays
    reproduce or exceed every bound; `\evid{stored}`; Tier 1.
  - `etamac`: displayed bound from one code, the weaker
    $-15.294675643368096$ from a separately written one; primal by one
    code. `pindyck`: concavity by two separately written codes; displayed
    bound from one code's enclosures, a slightly weaker one from the
    other's; primal by two codes; `\evid{stored}`; Tier 1.
  - `hvycrash`: proof by hand; "two codes checked the first witness and a
    third code a second witness" (opus-claims 16); `\evid{hand}`.
- Files: `sections/05-other.tex`.

### G3-03 §5.1 camshape
- Sources: sol-math-main 2; opus-writing 35 (`:86`), 52 (`:79`); sol-referee 11 (Figure S4).
- Severity: minor. Decision: accept; sol-referee 11's promotion of Figure S4
  rejected (R-09), replaced by a pointer.
- Change:
  - Proposition 5.4, `:82` (sol-math-main 2), as given: "For $0\le\varepsilon<1$
    there is an explicit bound $D_n(\varepsilon)$, rational when
    $\varepsilon$ is rational (`\cref{app:camshape-deficit}`), such that …".
    Reason checked: as $\varepsilon\to1^-$ the bound becomes
    $c_0[n\varepsilon+\dots]$, irrational for irrational $\varepsilon$.
  - `:86`, as given: "The proof applies the identity of
    `\cref{lem:camshape-sturm}` to a point with violations at most
    $\varepsilon$; the row violations enter with the weights $U_m$ (up to
    605.9 for $n=800$), and the bounds and slopes are relaxed by
    $\varepsilon$." Add "(`\cref{fig:camshape-deficit}`)" after "about 87%
    of it".
  - `:79`: one clause with `\cref{prop:baron-camshape}` (BARON home is §8.1).
- Files: `sections/05-other.tex`.

### G3-04 §5.3 powerflow, etamac
- Sources: opus-math-main 6; opus-writing 35 (`:148, :204, :213`).
- Severity: minor. Decision: accept. Reason: Remark S1.55 shows that no
  shift is needed for `powerflow0039p` with angle-row multipliers set to
  zero; paired eigenvalues explain negative pairs, not a necessity.
- Change:
  - `:188–189`, as given: "`\Cref{prop:pf-duality}` applies verbatim to
    these leaf relaxations. Because the eigenvalues of $A(w)$ come in pairs
    (`\cref{prop:pf-double}`), rounding near-optimal multipliers can create
    a negative pair. The stored `powerflow0039r` certificate absorbs one,
    about $-6.07\cdot10^{-10}$, with $\varepsilon=10^{-9}$. The stored
    `powerflow0039p` certificate uses $\varepsilon=10^{-8}$ and tiny
    angle-row multipliers; with those set to zero, it needs no shift
    (`\cref{rem:pf-anglefree}`). All shifts cost less than $4.4\cdot10^{-7}$."
    The editor checks the two shift values against B6 before inserting.
  - `:148` → "Let $\mathcal Q$ be the set of $(x,y)$ that satisfy these
    identities, …". `:204` → name the added term (from the OSIL row of
    period 1). `:213` → "an upper bound $W$ on that degree-one aggregate
    over $\mathcal B$".
- Files: `sections/05-other.tex`.

### G3-05 §5.4 hvycrash
- Sources: opus-claims 16. Severity: minor. Decision: accept (checked:
  `B5-small.tex:44` says two codes evaluated the first witness and the
  verifier's code proved a second).
- Change: one count everywhere: "two codes checked the first witness and a
  third code a second witness" (here, in the certificate sentence of G3-02,
  and in `06-points.tex:83`, G3-07).
- Files: `sections/05-other.tex`.

### G3-06 §5.5 reduced space
- Sources: opus-writing 36, 37; opus-math-main 5; opus-claims 11; sol-math-supp2 1 with `kan-guard/report.md`; opus-referee M2(c).
- Severity: major. Decision: accept.
- Change:
  - Title `\subsection{Reduced-space branch and bound with enclosures that keep cancellation}`.
  - `:297`, split as given: "Enclosures that bound each term separately
    fail there, because of cancellation (`eg`) or the depth of the networks
    (`ann_cumene_tanh`, KAN). The certificates therefore use enclosures that
    keep cancellation, and per-box linear programs whose values are
    recomputed by weak duality, so the LP solver is not trusted [cites]."
  - `:324`: "The authors' search" → "The first implementation's search";
    "the part of `eg_disc2_s` that contains the optimum" → "the part of
    `eg_disc2_s` with $x_7\in[24,27]$, the last under a side condition on
    its LP multipliers (`\cref{tab:eg-matrix}`)" (outline §8 item 5: no
    exact optimum for `eg`).
  - `:331` (opus-math-main 5; count checked 2·722 + 1): "… where
    $\Omega\subset\mathcal U$ is cut out by the two-sided bounds of 722
    determined variables and the purity row (1,445 one-sided inequalities)."
  - `:342`: "the second does not import the first, but the session that
    wrote it read it in full".
  - `:383–384` (opus-claims 11; sol-math-supp2 1; kan-guard): "The reported
    $L$ is the weaker of the two bounds, so it is valid if either code is
    correct, given their shared OSIL reader, rigorous exponential and
    interval core; path~(II) assumes, without a check, that no NaN bound
    occurred. A later replay of path~(I), with a guarded quadratic bound
    routine, reproduced all six searches and their bounds bit for bit
    (`\cref{app:annkan-kan-enclosure}`)." (Replaces "A separate rerun … not
    for those in five.") Outline §8 item 4 forbids saying that the *review*
    reran the r5 searches; this sentence reports the guarded replay, which
    did.
  - KAN tolerance disclaimer: `:388` is its home; §1 and §3 keep a clause.
  - opus-referee M2(c): the `ann_cumene_exp` qualifier stays at `:335`.
- Files: `sections/05-other.tex`.

### G3-07 §6 Exactly feasible points
- Sources: opus-writing 38; opus-math-main 9; sol-referee 9 (Theorem 6.1); opus-claims 16 (`06:83`); sol-literature 4 (`06:46`); opus-writing 52.
- Severity: minor. Decision: accept.
- Change:
  - Theorem 6.1, `:27` → "Let $X\subset\R^m$ be a closed box with finite,
    positive widths, and let $y\in X$." (Compactness is used in the proof.)
  - Title `:69` → `\subsection{Closures whose earlier points were feasible only within a tolerance}`;
    `:74` → "no point proved exactly feasible had been published". This
    subsection is the home of the list of the 13 closures.
  - `:73` (opus-math-main 9): "For `lnts`, $\Uprim$ comes from the
    attaining point of `\cref{thm:lnts-opt}`, enclosed in \arith{E} with
    width below `\sci{1.11}{-91}`; the Krawczyk points are a second,
    strictly suboptimal witness (`\cref{rem:lnts-stored}`)." G7-05 splits
    the table row.
  - `:46`: name "Hoen and Gleixner" (two authors).
  - `:83`: "the two computer checks" → "two codes checked the first witness
    and a third code a second witness".
- Files: `sections/06-points.tex`.

### G3-08 §7 opening and the class rule
- Sources: opus-writing 39, 40, 42; opus-referee M6.
- Severity: major. Decision: accept-modified. Reason: three thresholds and a
  mixed class (ii) obscure the hypothesis. Checked: every class (i) margin
  is at least $1.1158\,\dunit{s}$ and every (i-r) margin is below
  $0.44\,\dunit{s}$ (sol-numbers, opus-math-main), so no class changes.
- Change:
  - `:7`, adapted from opus-writing 39: "We screened every per-solver dual
    bound on MINLPLib's instance pages against the listed points, and we
    settled a conflict only by proving that an exactly feasible point
    exists. Under a stated hypothesis on how the pages display numbers, we
    prove 22 listed bounds on 18 instances invalid; none of them contradicts
    a solved mark. We state everything for minimization."
  - `:20–24`: (i) *invalid*, if the margin is at least $\dunit{s}$; (i-r)
    *invalid as displayed*, if the margin is positive but below
    $\dunit{s}$; (ii) *proved valid*, if a rigorous lower bound on $\vstar$
    is at least the bound; (ii′) *not refuted after repair*, if the exactly
    feasible point found does not lie below the bound (evidence, not
    proof); (iii) *undecided*. Add: "The screen used a slack of half a
    unit; since no margin lies between $0.44\,\dunit{s}$ and
    $1.115\,\dunit{s}$, both rules give the same classes
    (`\cref{app:audit-screen}`)."
  - `:55–56` → opus-referee M6, as given: "Every class (i) margin is at
    least $1.115\,\dunit{s}>\tfrac{10}{9}\dunit{s}$, so the 19 class (i)
    refutations need only that the display arises from the reported number
    by decimal roundings or truncations (`\cref{lem:audit-display}`(a)); of
    all 22 refutations, only `rocket100` (1.06 units) needs Hypothesis~H
    itself."
  - G7-08 makes the same change in S4.1 and in `tab:audit-classes`.
- Files: `sections/07-audit.tex`.

### G3-09 §7.2 Hypothesis H and the GAMS form
- Sources: opus-writing 41, 1 (`07:59`); opus-math-main 2; opus-claims 2 (GAMS form).
- Severity: minor. Decision: accept-modified. Reason for keeping the GAMS
  statement: the condition of register AU-03 is met; sol-numbers reran the
  exact GAMS/OSIL comparison from a clean copy (23 identical models, the
  `methanol50` exception, three negative controls).
- Change:
  - `:36–38`, as given: "`\Cref{lem:audit-display}` shows when Hypothesis~H
    holds. If $s$ arises from $b$ by finitely many roundings (to nearest or
    directed) or truncations to integer multiples of powers of ten, then
    $|b-\dval{s}|<\tfrac{10}{9}\dunit{s}$; Hypothesis~H itself holds if at
    most one of these operations changes the value, or if the last one that
    changes it rounds to nearest."
  - `:59` → "An exact symbolic comparison, proved by one implementation and
    rerun from a clean copy by a separate agent session, found the two forms
    identical for 14 of the 15 class (i) instances, and the refutation on
    `methanol50` holds for both forms (`\cref{app:audit-history}`)."
  - `:30`: this is the single definition of $\dunit{s}$ (G1-13).
- Files: `sections/07-audit.tex`.

### G3-10 §7.3 Existence certificates: trust
- Sources: opus-claims 9. Severity: minor. Decision: accept.
- Change: `:71` → "These assume IEEE binary64 arithmetic for matrix
  products and, for `glider100` and `ghg_3veh`, mpmath's interval
  exponential in the audit implementation; the second checker also assumes
  an accurate 90-digit mpmath exponential (`\cref{app:audit-existence}`)."
- Files: `sections/07-audit.tex`.

### G3-11 §7.4 Results
- Sources: opus-writing 43, 44; opus-claims 2 (rocket); sol-referee 11 (Table 6 caption, done by G7-06).
- Severity: minor. Decision: accept; opus-claims 2 accept-modified (keep
  22/18; the required rerun is done, R-14).
- Change:
  - `:82`: end the sentence at "below the common relative gap tolerance
    $10^{-4}$" (no suggested cause).
  - `:92–94`, as given: "Archived copies show the models unchanged since
    before the refuted and (i-r) bounds, with two exceptions
    (`\cref{app:audit-history}`). After both of its bounds, `ghg_3veh`
    rewrote three products of constants as rounded decimals (relative
    change $\le1.84\cdot10^{-15}$), and the refutation also holds on the old
    text. Nine instances added days before their 2014 bounds have no older
    copy."
  - `:109`: "two implementations agree; a clean-copy rerun of the second
    proof reproduced all three brackets (`\cref{app:audit-rocket}`)".
- Files: `sections/07-audit.tex`.

### G3-12 §7.5
- Sources: opus-writing 8. Severity: minor. Decision: accept.
- Change: `:123`: cut the relative clause "which it forms by trusting …"
  (now defined in §2.1, G1-10).
- Files: `sections/07-audit.tex`.

### G3-13 Length and repetition in §5–§7
- Sources: LD-2; opus-referee M1.4; opus-writing 52.
- Severity: major. Decision: accept-modified (as G2-15).
- Change: targets §5 6.5, §6 1.75, §7 3.25 pages. Shorten the Gibbs,
  pricing, etamac, pindyck, eg and ann proof sketches to their reduction and
  validity idea (each ≤ 6 lines; the supplement has the proofs); cut the
  sampled-box comparison of `:307` to one clause (keep "numerical
  evidence"); in §6 drop the description sentences that repeat Table S-points;
  in §7 drop numbers repeated from C2 except where a proposition needs them.
- Files: `sections/05-other.tex`, `sections/06-points.tex`, `sections/07-audit.tex`.

---

## 6. G4 solvers and end: `08-solvers`, `09-interpretation`, `10-reproducibility`, `11-conclusion`

### G4-01 Statements and declarations: AI use
- Sources: LD-1(b); opus-referee B2, M3.2; opus-claims 1.
- Severity: blocker. Decision: accept-modified. Rejected part: opus-referee
  B2's request to fill authors, licence, competing interests and funding now
  (LD-1(b) keeps them as marked placeholders; R-12).
- Change: add to `11-conclusion.tex` (Statements and declarations), as
  given by the lead author:

  > \paragraph{Use of AI tools.}
  > AI coding and writing assistants (Anthropic Claude and OpenAI GPT
  > models) were used, under the authors' direction, to implement and
  > re-implement the certificate computations, to check them, to search the
  > literature and to draft the manuscript. The authors take full
  > responsibility for the content. \TODO{authors to confirm wording}

  Keep `\TODO` for licence, competing interests and funding, and
  `\archiveDOI`. Delete the source comment "No AI-use statement (revision
  decision 8)" (`:66–67`). G7-17 updates `development/labels.md:48`.
- Files: `sections/11-conclusion.tex`.

### G4-02 §8 opening
- Sources: opus-writing 45. Severity: minor. Decision: accept-modified (the
  last sentence follows G4-05).
- Change: append to `:7`: "Many reported values are tolerance artifacts
  (`\cref{sec:solvers-tolerance}`). Three are invalid claims, and only one
  of these, the SCIP~10 error, we trace to a defect
  (`\cref{sec:solvers-invalid}`). In one-hour runs, every final dual bound
  stayed below our certified bounds, and only BARON's two optimality claims
  ended within $10^{-6}$ (`\cref{sec:solvers-campaign}`)." Optional lead-in
  before Proposition 8.1 as given in opus-writing 45.
- Files: `sections/08-solvers.tex`.

### G4-03 §8.1 QPLIB copies and the KAN values
- Sources: opus-math-main 7; sol-referee 7 (KAN assumption placement).
- Severity: minor. Decision: accept-modified. Reason: the margins
  $3.162\cdot10^{-3}$ and $1.552\cdot10^{-4}$ hold only for round-to-nearest
  displays; Mittelmann's display rule is not documented. Checked: under the
  weaker assumption $|b-\dval{s}|<\dunit{s}$ the thresholds are $-4.2773$
  and $-4.284301$, and with the copies' exact optima $\ge-4.2741871514717434$
  and $\ge-4.2841462678046117$ the margins exceed
  $3.1128\cdot10^{-3}$ and $1.5473\cdot10^{-4}$.
- Change: `:28` → "… the margins are at least `\sci{3.11}{-3}` and
  `\sci{1.54}{-4}` for any value within one unit of the last displayed
  digit; reaching them needs row or bound violations above … ". For the
  violation thresholds `8e-9` and `2.5e-8`: either G7-09 recomputes them
  exactly for the new thresholds (copy of the S6 check in `/tmp`), or write
  "if the values are rounded to nearest, reaching them needs violations
  above `\sci{8}{-9}` and `\sci{2.5}{-8}`". Part (b) holds under both
  assumptions (deficit bounds $-4.2771731888>-4.2773$ and
  $-4.2842973949>-4.284301$). `:32–33` (sol-referee 7): put the assumption
  into the sentence: "If the published models equal MINLPLib's up to the
  printing of coefficients, the zero-gap SCIP~9.0.1 optima … lie at least
  …". BARON tolerance-level closures: this subsection is their home.
- Files: `sections/08-solvers.tex`.

### G4-04 §8.2 invalid claims
- Sources: sol-numbers 2; sol-referee 7 (Proposition 8.6); opus-claims 20; opus-writing 46.
- Severity: minor. Decision: accept.
- Change:
  - Proposition 8.2, `:54`: "at most `\sci{2.9}{-15}`" → "at most
    `\sci{2.93}{-15}`". Checked by sol-numbers: exact maximum
    $32122061/10995116277760000000000=2.9215\ldots\cdot10^{-15}$; the editor
    repeats the division exactly and logs it.
  - Proposition 8.3 (opus-writing 46): title "The reproducers in three
    senses"; in (b) "(1) decimal data read exactly, zero tolerance
    (\reading{b}): …; (2) SCIP's own tolerances: …; (3) binary64 data, zero
    tolerance (\reading{c}): …"; `:70` "only in senses (1) and (2)".
  - Proposition 8.6 (sol-referee 7): begin the statement with "Assume that
    CAMINO's model files equal the current MINLPLib files and that the
    recorded bound is AMPL's `bestbound`." Delete the assumption sentence at
    `:109`; keep the status and run-time sentence and "invalid as recorded;
    the cause is unknown".
  - Proposition 8.7 (opus-claims 20): "If the `.nl` file encodes the GAMS
    copy, the report is invalid as recorded (cause unknown)."
  - Shorten the scan paragraph `:91–94` by one sentence.
- Files: `sections/08-solvers.tex`.

### G4-05 §8.3 One-hour comparison
- Sources: LD-4; sol-referee 4; opus-referee M2(a); opus-writing 47.
- Severity: major. Decision: accept-modified. Reason: "all 109 … weaker"
  mixes 79 same-model comparisons with a globality guarantee, 6 BARON values
  without a guarantee, 6 SCIP bounds on tightened models and 18 KAN
  comparisons with a different model; "no run closed" must say what was
  required. Checked in `results.csv`: only the BARON runs on `camshape100`
  and `camshape200` end with a relative gap at most $10^{-6}$.
- Change: replace `:131–136` by:

  > Of the 129 runs (`\cref{tab:solvers}`), only BARON's on `camshape100`
  > and `camshape200` ended with a relative gap of at most $10^{-6}$. Their
  > dual bounds are valid and, paired with our exactly feasible points,
  > would meet the closure threshold; but the points BARON returned are not
  > exactly feasible (`\cref{prop:baron-camshape}`), so no run closes an
  > instance under exact feasibility. Of the 109 finite final dual bounds
  > (35 from BARON, 36 from Gurobi, 38 from SCIP), 79 refer to the stored
  > model, carry a globality guarantee and use no tightened bounds; all 79
  > are weaker than our certified bounds (`\cref{tab:campaign-runs}`). So
  > are the other 30: six BARON values that BARON disclaims, six SCIP
  > bounds on models with tightened argument bounds, and 18 values on the
  > KAN instances, which we compare with the bound for $\Rnet$ only
  > descriptively. Five final dual bounds improve the best listed dual:
  > BARON's on `camshape100`, `camshape200` and `camshape400`, Gurobi's on
  > `lnts200` and SCIP's on `waterno2_18`.

  Keep the primal-side sentences (`:134–136`). The counts come from G7-06.
- Files: `sections/08-solvers.tex`.

### G4-06 §9: an interpretation, shortened
- Sources: LD-5; opus-referee M4, m14; sol-referee 11, 12; opus-writing 3 (§9), 20 (`09:24`), 48.
- Severity: major. Decision: accept opus-referee M4 option (b); reject option
  (a), a new solver experiment (R-02).
- Change (target 1.5 pages):
  - Title `\section{What the certificates exploit: an interpretation}`.
  - Opening: keep `:15–18` and insert after `:15` (opus-writing 48): "Our
    interpretation, which we did not test by experiment, is that termwise
    relaxations cannot see the structure that each certificate uses: free
    states along long chains of nonconvex equalities, hidden convexity or
    monotonicity, and cancellation among many terms."
  - Drop Table 7 (`tab:structure`; G7-06 stops generating it) and
    `:22–24`'s reference to it; keep the branching census `:28–31` as a
    paragraph of facts; write "instance families" (`:24`).
  - §9.2: keep the run evidence in at most 8 lines; keep the
    counter-evidence (`camshape100` SCIP, ex6_2/pricing/eg without free
    variables, powerflow formulation).
  - §9.3: rename `\subsection{Interpretation}`; delete `:50–51` (restates
    lesson 1); `:52` "In our reading" → "In our interpretation"; `:41` "do
    not fit a simple explanation"; `:64` "The same interpretation applies,
    with less force, …"; `:65` "which we interpret as too large for tight
    stage bounds". State the causal conjectures once; keep the "We do not
    claim …" sentence `:62`.
- Files: `sections/09-interpretation.tex`.

### G4-07 §10 Reproducibility
- Sources: sol-referee 2; opus-math-main 12; opus-referee m15; opus-writing 37, 49; sol-numbers 5; opus-claims 18, 3.
- Severity: major. Decision: accept. Reason (sol-referee 2, checked): the
  `topopt` certificate does not store its basis (`E-audit.tex:325`,
  register AU-05), so `:40` "the archived certificates replay exactly" is
  false for `topopt`; the display uses the archived result, and regeneration
  proves a different valid point.
- Change:
  - `:23` "the authors' checkers" → "the first implementations".
  - `:25` (sol-numbers 5) → "The script that writes our tables checks the
    certified bound, primal, gap and margin displays that it generates
    against their exact values in rational arithmetic; hand-written tables
    are checked separately (`\cref{app:displays}`)."
  - `:26` (opus-claims 18): "maps each result to its checkers, …".
  - `:39–40` → "Regeneration gives other multipliers and a weaker bound for
    `powerflow0030p`, whose archived certificate replays exactly and gives
    the displayed value. The `topopt-cantilever_60x40_50` existence
    certificate of the audit does not store its basis, so it is regenerated,
    not replayed: with one BLAS thread pivoted QR picks another basis and
    proves another exactly feasible point, which also satisfies its row of
    `\cref{tab:audit-pairs}` (`\cref{app:audit-existence}`)."
  - Tiers (opus-math-main 12): define once here: "Recorded wall time per
    instance (for a result split into parts, the sum over its parts):
    Tier~1 under 10 minutes, Tier~2 under one hour, Tier~3 longer."
    Reassign Table 8 by the recorded times: `ex6_2_5`, `ex6_2_7`,
    `lukvle10`, `powerflow0039p`/`r` from the stored leaves and `chain` →
    Tier 1; `catmix` (20–46 min each) and the KAN $\RP$ bounds (up to
    18 min per model) → Tier 2; `pindyck` stays Tier 1; `eg_int_s` and
    `eg_disc_s` by their recorded per-instance totals; `waterno2`, `ann`,
    the `eg_disc2_s` search and the audited `eg` re-certification → Tier 3. G7-12 aligns the register; G5/G6
    align the supplement boxes.
  - `:46` → "They show the order of magnitude to expect and support no
    speed comparison."
- Files: `sections/10-reproducibility.tex`.

### G4-08 §11 Recommendations, limitations and conclusion
- Sources: opus-writing 50, 38 (`11:23`), 3 (`11:74`); opus-referee M4 (recommendation), M5 (limitations), m16; opus-claims 1 (`11:61`), 22; LD-5.
- Severity: major. Decision: accept-modified. opus-referee m16 needs no
  paper change (authors' action; R-11).
- Change:
  - Title `\section{Recommendations, limitations and conclusion}`.
  - Benchmark bullet `:88` → "*Mark listed points as proved exactly
    feasible or as feasible only within a tolerance, …*".
  - Solver bullet "Exploit stage structure": begin "*As an untested
    proposal, exploit stage structure* (for circumstantial evidence see
    `\cref{sec:interpretation-evidence}`): …".
  - Merge the six benchmark bullets into at most four and the four solver
    bullets into three (LD-2), without dropping a cited fact.
  - Limitations `:119`: replace by one sentence pointing to §2.6 ("All
    implementations come from agent sessions directed by the authors;
    `\cref{sec:semantics-protocol}` states the resulting common-mode
    risk."). Add (opus-claims 22, updated to the round-1 results): "The
    extended-value proofs of Appendix B and the `eg` primal check were
    rechecked by separate agent sessions; no human reviewer outside the
    authors has checked any proof." Add (opus-referee M5): "Replay was run
    on one machine; the search trees of the `\evid{rerun}` certificates are
    not stored." `:126` (opus-claims 1): "The certificates were built
    individually, one instance or family at a time".
  - `:138–141` (LD-5) → "We return to the three observations of
    `\cref{sec:intro}`. First, once a bound fitted to the structure of the
    model was in place, little search remained; why general-purpose solvers
    did not find such bounds we have only interpreted
    (`\cref{sec:interpretation}`). Second, fifteen closures exploit the
    stage structure, eleven through splits and four through value-function
    minorants. Third, exact feasibility changed the verdict on listed
    bounds, listed points and solver claims often enough that benchmark
    values should carry their data semantics, their provenance and, where
    possible, a certificate that others can check."
- Files: `sections/11-conclusion.tex`.

### G4-09 Length and repetition in §8–§11
- Sources: LD-2. Severity: major. Decision: accept.
- Change: targets §8 2.75, §9 1.5, §10 1.0, §11 2.25 pages. §8.1 QPLIB
  paragraph to three sentences (details in S6); §11 limitation paragraphs to
  cross-references where §2 or §7.5 states the limit.
- Files: `sections/08-solvers.tex` to `sections/11-conclusion.tex`.

---

## 7. G5 supplement certificates I: `B0`–`B5`

### G5-01 One certificate box per result in S1.1–S1.5
- Sources: LD-2; opus-referee M1.3, m11; `development/integration-notes-r1.md` §"How the verification records describe who checked" item 3.
- Severity: major. Decision: accept.
- Change: move the main-text boxes for `lnts`, `dtoc5`, `optcdeg2`,
  `chain`, `catmix`, `lukvle10` (from `HEAD:04-split.tex`) and `camshape`,
  `ex6_2_5`/`ex6_2_7`/`pricing050`, `etamac`/`pindyck`, `hvycrash` (from
  `HEAD:05-other.tex`) into their family sections, merged with the existing
  detail boxes (`B2:90, :302`, `B1:325`) and replacing the verification-record
  tables or prose, so that each result has exactly one six-field box
  (`terminology.md` §6). Apply the qualifiers listed in G2-09 and G3-02, the
  `catmix` level of G5-10 and the tiers of G4-07.
- Files: `sections/B1-lnts-lukvle10.tex` to `sections/B5-small.tex`.

### G5-02 Uniform description of who checked
- Sources: LD-1; opus-claims 1 (`B3:292`, `B4:497`, `B5:184`).
- Severity: major. Decision: accept (one statement in §2.6, none repeated
  per family).
- Change: delete "none is peer review" (`B3:292`, `B4:497`); `B5:184` "a
  separate review" → "a separate agent session"; "the verifier" stays as
  the name of the second implementation's author session, defined in §2.6.
- Files: `sections/B3-camshape.tex`, `sections/B4-chain-catmix.tex`, `sections/B5-small.tex`.

### G5-03 Gibbs second-order bound
- Sources: sol-math-supp1 1. Severity: major. Decision: accept. Reason
  (checked by the reviewer's counterexample): the ordinary componentwise
  endpoint matrices do not give a valid bound; the implementation
  (`research-20260929/reviews/wave2-small-verification/gibbs_bb.py:115–129`)
  uses the lower diagonal ends in both matrices, which is valid.
- Change: at `B5-small.tex:148–150` define
  $a=\underline{H}_{11}$, $e=\underline{H}_{22}$,
  $Q^-=\begin{pmatrix}a&\underline{H}_{12}\\\underline{H}_{12}&e\end{pmatrix}$,
  $Q^+=\begin{pmatrix}a&\overline{H}_{12}\\\overline{H}_{12}&e\end{pmatrix}$,
  and state with proof: "For every displacement $z$ and every admissible
  symmetric Hessian $H$, $z^\top Hz\ge\min(z^\top Q^-z,z^\top Q^+z)$: the
  diagonal terms are bounded below independently, and the off-diagonal term
  is linear in $H_{12}$, so it is minimal at an endpoint. When $Q^-$ and
  $Q^+$ are positive definite, the smaller of their unconstrained quadratic
  minima is a valid lower bound on the box." Replace "minimizes the
  resulting quadratics exactly" by "evaluates their closed-form minima in
  outward-rounded mpmath interval arithmetic, with interval enclosures of
  the centre value and gradient".
- Files: `sections/B5-small.tex`.

### G5-04 lnts negative controls
- Sources: sol-math-supp1 2. Severity: minor. Decision: accept (checked by the
  reviewer in `development/reviews/code/sol-lnts-review/verify.py:291–299`).
- Change: `B1:89` → "Shifting the final bracket by $\pm10^{-55}$ fails the
  sign test; changing one acceleration coefficient by $10^{-40}$ fails the
  model-structure assertion."
- Files: `sections/B1-lnts-lukvle10.tex`.

### G5-05 lukvle10 gap
- Sources: sol-math-supp1 3; sol-math-main 3. Severity: minor. Decision: accept.
- Change: `B1:314–315` → "The certified gap, at most `\sci{1.42}{-9}`, is
  dominated by the summed branch-and-bound tolerances (they agree to about
  $3.5\cdot10^{-16}$); global optimality of the exactly feasible point is
  not proved."
- Files: `sections/B1-lnts-lukvle10.tex`.

### G5-06 etamac margin
- Sources: sol-math-supp1 4. Severity: minor. Decision: accept.
- Change: `B5:308` → "Every nonfixed variable satisfies its finite bounds
  with margin at least 0.047; $K_1$ equals its fixed value exactly."
- Files: `sections/B5-small.tex`.

### G5-07 lnts novelty statement
- Sources: opus-claims 21. Severity: minor. Decision: accept.
- Change: `B1:136` → "To our knowledge, within the search of
  `\cref{app:literature}`, the attaining discrete control, the scalar
  equation $g(\nu)=0$ and the rigorous enclosure are new."
- Files: `sections/B1-lnts-lukvle10.tex`.

### G5-08 Remark S1.2 (lnts Krawczyk points)
- Sources: opus-math-main 9. Severity: minor. Decision: accept-modified.
  Reason (checked): `dossiers/primal-points.md:530` gives the Krawczyk point
  enclosures as narrower than `3e-109` at 110 digits; an enclosure that
  narrow cannot contain the `1.11e-91`-wide enclosure of $\vstar$.
- Change: `B1:124` → "Their objective enclosures (110-digit interval
  arithmetic, width below $3\cdot10^{-109}$) and 60-digit enclosures of $h$
  show that their objective values exceed $\vstar$ by less than
  $2\cdot10^{-58}$." Drop "contain the rational enclosure of $\vstar$";
  keep "This overlap …" only if the source shows an overlap, else write
  "This closeness is a consistency check between two separate existence
  proofs; it does not make these points optimal." Verify both widths in the
  dossier logs before writing.
- Files: `sections/B1-lnts-lukvle10.tex`.

### G5-09 chain GAMS and OSIL forms
- Sources: opus-math-main 11. Severity: minor. Decision: accept. Reason
  (checked): no exact `chain` comparison is recorded
  (`research-20260929/publication/minlplib-status/report.md`; Table A9 lists
  `chain` under evaluation).
- Change: `B4:23` → "The `.gms` files agree with the OSIL files in the step
  ($0.5\,h$ with $h=1/N$), the length $4$ and the end values $1$ and $3$,
  and their rows agree at sample points (`\cref{tab:sem-gams}`)."
- Files: `sections/B4-chain-catmix.tex`.

### G5-10 catmix evidence level and scope
- Sources: sol-math-main 4; opus-claims 3, 8; sol-referee 2.
- Severity: major. Decision: accept (the supplement already says that the
  per-stage values are not stored, `B4:412`).
- Change: the `catmix` box (G5-01): "Evidence level: `\evid{rerun}` for the
  dual (the minorant computation; per-stage values not stored),
  `\evid{stored}` for the primal (exact rational state evaluation)";
  "Replay: Tier~2; 20.2 to 46.1 min per instance". `B4:411`: keep the scope
  of the per-stage agreement ("on identical test inputs for $N=100$, all 99
  stages on a 324-ray grid and 40 stages on a $2^{-21}$-band grid").
- Files: `sections/B4-chain-catmix.tex`.

### G5-11 camshape deficit construction
- Sources: sol-math-main 2. Severity: minor. Decision: accept.
- Change: `B3:206–208`: "an explicit bound $D_n(\varepsilon)$, rational
  when $\varepsilon$ is rational" (same wording as Proposition 5.4).
- Files: `sections/B3-camshape.tex`.

### G5-12 hvycrash witness count
- Sources: opus-claims 16. Severity: minor. Decision: accept.
- Change: in the merged `hvycrash` box: "two codes checked the first
  witness and a third code a second witness"; `B5:44` keeps its wording.
- Files: `sections/B5-small.tex`.

### G5-13 Terms in S1.0–S1.5
- Sources: opus-writing 32; opus-math-main 12. Severity: minor. Decision: accept.
- Change: "split class" → "split form" in `B0-families.tex` and B1–B4 text
  (the `tab:staged` header is G7-06); tiers in boxes per G4-07.
- Files: `sections/B0-families.tex` to `sections/B5-small.tex`.

### G5-14 Length of S1.1–S1.5
- Sources: LD-2; sol-referee 5; opus-referee M1. Severity: major. Decision: accept.
- Change: targets S1.1 6, S1.2 6, S1.3 5, S1.4 7.5, S1.5 7.5 pages. Remove
  restatements of models, listed status and certificate summaries that §4,
  §5 or S3 already give (cross-reference instead); move superseded-display
  notes to S8 or the artifact README; replace verification-record tables by
  the merged boxes (G5-01). Keep every proof, lemma and computation
  description.
- Files: `sections/B0-families.tex` to `sections/B5-small.tex`.

---

## 8a. G6 supplement certificates II: `B6`–`B9`, `F`

### G6-01 One certificate box per result in S1.6–S1.9
- Sources: LD-2; opus-referee M1.3. Severity: major. Decision: accept.
- Change: move the main-text `powerflow` box (from `HEAD:05-other.tex:193`)
  into S1.6 as its single box, replacing its verification-record table;
  check that the existing `waterno2` (`B8:306`), `ann` and KAN (`B9:161,
  :332`) and `eg` (`F:423`) boxes carry the qualifiers of G2-09/G3-02 and
  the tiers of G4-07.
- Files: `sections/B6-powerflow.tex`, `sections/B8-waterno2.tex`, `sections/B9-ann-kan.tex`, `sections/F-eg-rounding.tex`.

### G6-02 Uniform description of who checked
- Sources: LD-1; opus-claims 1 (`B8:219`, `B9:67, :258, :316, :323`, `F:420`).
- Severity: major. Decision: accept.
- Change: "second party", "different party" → "a separate agent session";
  `B9:258` "path~(I) was written later by a different party" → "path~(I)
  was written later, in a separate agent session"; `B9:316`, `F:420` "A
  separate review" → "A separate agent session"; `B9:323` "Neither code was
  read line by line by a third party" → "Neither code was read line by line
  by another session".
- Files: `sections/B8-waterno2.tex`, `sections/B9-ann-kan.tex`, `sections/F-eg-rounding.tex`.

### G6-03 KAN path (I): guarded replay
- Sources: sol-math-supp2 1; `kan-guard/report.md`; opus-claims 11.
- Severity: major. Decision: accept. Reason: the subnormal counterexample to
  `minquad` is real; the guarded routine is proved in
  `kan-guard/minquad-proof.md`, passed 72,240 exact comparisons, and the six
  complete replays reproduce every archived bound with zero guard triggers.
- Change:
  - Insert after the paragraph "Rerun with a rigorous exponential"
    (`B9:300–306`) the paragraph of `kan-guard/report.md` §"Exact
    replacement text for the paper", verbatim (it begins "Path~(I) was
    subsequently replayed with a guarded quadratic lower-bound routine").
  - `B9:304`: replace "it did not rerun the `r5` searches" by "the guarded
    replay below reran all six".
  - Table `tab:kan-rerun` caption: add "The guarded replay (below) gives the
    same $\Lcert_{\mathrm{ver}}$ bit for bit."; values unchanged.
  - KAN box (`B9:332`) "Replay": add "guarded path~(I): 23\,s to 20\,min
    wall per model (six concurrent processes)"; "Inputs/Implementations":
    name the guarded source (SHA-256 prefix `e5783a24`) and the logs in
    `development/reviews/round1/kan-guard/logs/` (G7-15 adds them to the
    register).
  - Keep the path (II) NaN sentence (`B9:285`); Table 1's KAN cell says
    "path (II) assumes no NaN" (G7-04).
- Files: `sections/B9-ann-kan.tex`.

### G6-04 ann second code data reading
- Sources: opus-math-main 10. Severity: minor. Decision: accept (checked:
  `annx.py` uses correctly rounded doubles covered by its slack).
- Change: `B9:137` "which are enclosed outward" → "which it uses as
  correctly rounded binary64 values, a rounding that the slack covers".
- Files: `sections/B9-ann-kan.tex`.

### G6-05 eg weight padding: second-order terms
- Sources: sol-math-supp2 2. Severity: minor. Decision: accept. Reason
  (checked by the reviewer's exact rational proof in
  `eg-dyadic/math-probes.log`): $\delta E<10^{-6}$ does not make the
  second-order terms below $10^{-27}$, but the affine bound used holds.
- Change: delete the $10^{-27}$ assertion at `F:257`; derive "for
  $0\le d\le10^{-6}$,
  $\exp(d)/((1-u)^2(1-\epsilon))-1\le1.000001\,d+\epsilon+2.01\,u$ with
  $u=2^{-53}$, $\epsilon=10^{-14}$", by bounding $(e^d-1)/d$ with the
  positive Taylor series and its tail, and the reciprocal denominator
  separately; keep the padding constants as computed from their exact
  binary64 values.
- Files: `sections/F-eg-rounding.tex`.

### G6-06 eg search points: trust statement
- Sources: sol-math-supp2 3. Severity: minor. Decision: accept.
- Change: `B7:349` "Under H0 alone" → "Under `\cref{hyp:fp-ieee}` and the
  correctness of the interval-mode implementation and its reader".
- Files: `sections/B7-eg.tex`.

### G6-07 eg primal check: review status and self-test
- Sources: sol-math-supp2 4 and its eg primal resolution; `open-items.md` item 2.
- Severity: minor. Decision: accept-modified. Reason: the separate agent
  session reran the dyadic check, read it in full and found the three points
  exactly feasible (logs in `eg-dyadic/`); the built-in self-test cannot
  fail at $1234/7$ (`or (t > 100)` bypass), but the proof does not use it.
  Modification: do not edit the archived checker (its recorded run is the
  evidence); describe the test status and cite the separate test.
- Change: `B7:345`: "The check was rerun and read in full by a separate
  agent session, which confirmed the three points (`eg-dyadic/primal-rerun.log`).
  Its built-in self-test skips the reciprocity assertion for arguments
  above 100; a separate test (`eg-dyadic/exp_test.py`, log
  `exp-test.log`) checks enclosures and reciprocity at 452 arguments,
  including both signs of $1234/7$. The tests support, and do not replace,
  the alternating-series proof." G7-10 makes the same change in S2.
- Files: `sections/B7-eg.tex`.

### G6-08 powerflow shift statements
- Sources: opus-math-main 6. Severity: minor. Decision: accept.
- Change: make `B6:223` and Remark S1.55 (`B6:276–284`) agree with the new
  §5.3 text (G3-04): shifts are a choice of the stored certificates, not a
  necessity; give the two stored $\varepsilon$ values.
- Files: `sections/B6-powerflow.tex`.

### G6-09 waterno2 shared components
- Sources: opus-claims 9, 10. Severity: minor. Decision: accept.
- Change: `B8:288` "exactly rounded summation (`\cref{hyp:fp-ieee}`)" →
  "Python's correctly rounded `math.fsum` (a further checking-program
  assumption, not part of H0)"; `B8:50, :286`: state that both branch-and-bound
  codes share the OSIL reader and that V$_{\mathrm{ex}}$ and
  V$_{\mathrm{fl}}$ share the builder, relaxation and node bound, in the
  words of §2.6 (G1-01). G7-04 lists `fsum` in Table 1's waterno2 row.
- Files: `sections/B8-waterno2.tex`.

### G6-10 Recent interval relaxations in S1.9
- Sources: sol-literature 3. Severity: minor. Decision: accept.
- Change: `B9:116`, after the Ninin et al. credit: "Recent interval solvers
  combine such affine relaxations with Taylor-based ones
  `\citep{araya2025-hybridizing-two-linear-relaxation-techniques}`."
- Files: `sections/B9-ann-kan.tex`.

### G6-11 eg evidence level
- Sources: opus-referee m9. Severity: minor. Decision: accept.
- Change: in S1.7 and S5 state once: "the leaf partition is stored and its
  coverage is checked exactly; only the per-leaf certificates are
  recomputed" (consistent with G1-14).
- Files: `sections/B7-eg.tex`, `sections/F-eg-rounding.tex`.

### G6-12 Length of S1.6–S1.9 and S5
- Sources: LD-2. Severity: major. Decision: accept.
- Change: targets S1.6 5.5, S1.7 6, S1.8 5.5, S1.9 6.5, S5 5.5 pages.
  Condense run, leaf and partition tables to the columns that a proof uses;
  move rerun histories that do not support a current claim to the artifact
  README; cross-reference model statements given in §5.
- Files: `sections/B6-powerflow.tex` to `sections/B9-ann-kan.tex`, `sections/F-eg-rounding.tex`.

---

## 8b. G7 supplement other: `C`, `D`, `E`, `H`, `I`, `J`; generators; `references.bib`

### G7-01 Table 2 (`tab:closures`)
- Sources: LD-3; sol-referee 3, 11; opus-referee B1.
- Severity: blocker. Decision: accept. Reason (checked by rendering page 13):
  the caption start and the three `eg` rows lie outside the page.
- Change in `data/make_tables.py`: drop the columns $n$ ($n_{\mathrm{int}}$)/$m$
  (move them to `tab:sem-hashes` in S7) and "arith." (Table 1 has it); keep
  instance, best listed dual (solver), $L$, $U$, $\Delta$, $\delta$, class,
  prior status. Caption at most four lines; the class and prior-status
  definitions move to §3 (G2-02, G2-04). For attained exact optima print
  "exact optimum" in the $\Delta$ and $\delta$ cells instead of "$0$" with a
  footnote (sol-referee 11; `02-semantics.tex:82`). Apply the prior-status
  change of G2-06. If the table still does not fit one sideways page, split
  it into "attained exact optima and staged closures" and "other closures".
- Files: `data/make_tables.py`, `tables/tab-closures.tex` (generated), `sections/I-reproduction.tex` (`tab:sem-hashes`).

### G7-02 Table S42 (`tab:claims`)
- Sources: LD-3; sol-referee 3, 6; opus-claims 12.
- Severity: blocker. Decision: accept. Reasons: the caption and the final
  row are clipped (checked by rendering page 116); the `optcdeg2` KKT row is
  not an unattainable value (a value above $U$ is attainable by some other
  point or not, and a single comparison does not show a tolerance cause);
  "tolerance artifact" is used as a cause where no tolerance cause is known.
- Change in `data/make_tables.py` (`claims_table` in `numbers.json`):
  remove the row "authors' float KKT point, optcdeg2"; caption: "Reported
  values that no exactly feasible point attains (category~A; 'tolerance
  artifact' names the category, not a diagnosed cause)"; qualifier column
  of the `lukvle10` SIF SOLTN row and of Kosolap's `ex6_2_5` row: "cause
  unknown; violation not reported". Make the table fit (split it or set it
  as a `longtable` with repeated headers; drop a column if needed).
  `H-solvers.tex:83–88` (G7-09) keeps one sentence on the KKT point as
  evidence about that numerical candidate. The row is register entry
  `reported-39` of `artifact/claims.json`, so the register drops to 65
  entries (27 rows and 38 reported values); G7-12 updates the counts after
  the rebuild.
- Files: `data/make_tables.py`, `data/numbers.json`, `tables/tab-claims.tex` (generated).

### G7-03 All other floats
- Sources: LD-3. Severity: major. Decision: accept. Reason: LaTeX gives no
  warning for clipped sideways tables, and `pdftotext` does not reliably
  extract rotated captions (checked: no Overfull or float warnings in the
  logs; captions of Tables 1, 2, 7, S1, S41, S42 missing from the raw text).
- Change: after the final build, render every page with a sideways table or
  longtable (main: Tables 1 and 2; supplement: S1, S39, S41, S42, S46, the
  longtables) at 40 dpi and inspect them; add this check to
  `development/build.md` together with a `pdftotext` check that all 31
  closure names occur in the main PDF. Fix any clipping in the generator.
- Files: `development/build.md`; generators as needed.

### G7-04 Table 1 (`tab:trust`)
- Sources: opus-referee M1.2; opus-claims 3, 4, 9, 11; sol-referee 10; `kan-guard/report.md`.
- Severity: major. Decision: accept-modified (Table 1 stays in the main text
  as the one compact dependency summary, because the main-text certificate
  boxes move to the supplement).
- Change in `data/make_tables.py` (`trust_table`): caption at most five
  lines; columns: family; dual arithmetic and trusted primitives; displayed
  dual certified by / second implementation; status (G1-02: *proved*,
  *verified by a separately written implementation*, or *proved; a second
  implementation certifies a weaker bound / part of the domain*; ann:
  "two codes; the second's author session read the first"); level; primal
  construction. Move the "reading" detail and "mpmath-free" column to S7
  (`tab:sem-hashes` or a short S7 table) or abbreviate them. Rows:
  `catmix` level `rerun` (sol-math-main 4; opus-claims 3); KAN: "reported
  $L$ is the weaker of two paths; path (II) assumes no NaN; path (I)
  replayed with guarded quadratic bounds" (opus-claims 11; kan-guard);
  `waterno2`: add "`math.fsum` (correctly rounded)" (opus-claims 9);
  `chain`/`camshape` "to all printed digits" (opus-claims 15).
- Files: `data/make_tables.py`, `tables/tab-trust.tex` (generated).

### G7-05 Points table (`tab:points`)
- Sources: sol-numbers 4; opus-math-main 9.
- Severity: major (unsafe display). Decision: accept. Reason (checked by the
  reviewer from the stored proof boxes): the `powerflow0039` widths are
  about `2.8208e-42`, above the printed cap `2.8e-42`.
- Change in `POINTS13` (`make_tables.py:1204`): "$\le2.8\cdot10^{-42}$" →
  "$\le2.83\cdot10^{-42}$", with an exact `check()` against the three
  widths; split the `lnts` row: attaining point "\arith{E}", width
  "$<1.11\cdot10^{-91}$" (it gives $U$); Krawczyk points "\arith{I}, 110
  digits", width "$<3\cdot10^{-109}$" (second witness).
- Files: `data/make_tables.py`, `tables/tab-points.tex` (generated).

### G7-06 Other generator and number-file changes
- Sources: LD-4, LD-5; opus-writing 32; opus-referee m12; sol-referee 4, 11; opus-math-main 7; opus-claims 2, 13; sol-numbers 5.
- Severity: major. Decision: accept.
- Change:
  - Stop generating and inputting `tab-structure` (G4-06).
  - `tab:staged` header "split class" → "split form" (opus-writing 32).
  - `tab:unclosed` footnote a (opus-referee m12): "(one slope per separator
    on a 113–162-cell partition, $\delta\le3.78\%$)" in place of "separator
    branching"; check the cell range against `B8:263`.
  - `tab:audit-pairs` caption opening (sol-referee 11): "Listed bounds
    refuted under Hypothesis H: the 19 listed per-solver dual bounds on 15
    instances …".
  - `claims_table` QPLIB rows (opus-math-main 7): margins
    "$\ge3.11\cdot10^{-3}$" and "$\ge1.54\cdot10^{-4}$", each with an exact
    check against the copies' exact optima and the thresholds $-4.2773$,
    $-4.284301$.
  - `numbers.json` `headline.audit` (opus-claims 2): add the totals with
    `rocket` (22 bounds, 18 instances, 16 LINDO) next to the class (i)
    counts, so that the abstract's 22 is generated and checked.
  - `campaign.totals` (sol-referee 4): add
    `same_model_guaranteed_finite_duals = 79` (per solver 23/30/26),
    computed from `results.csv` flags and checked to sum with 6 + 6 + 18 to
    109; add `runs_within_1e-6 = 2`. If `figures/make_fig_headline.py`
    needs per-instance BARON-disclaimed and tightened-SCIP values, add them
    to `headline_figure` (G2-01).
  - `instances.camshape200.prior.code` and `camshape800.prior.code` →
    "related model" (G2-06).
  - `make_tables.py` docstring (sol-numbers 5): "Every certified bound,
    primal, gap and margin display that this script generates is checked …;
    hand-written tables are checked separately."
  - Regenerate all tables in `/tmp`-free mode as `development/build.md`
    prescribes; confirm `data/check.log` reports zero failures.
- Files: `data/make_tables.py`, `data/make_campaign_table.py`, `data/make_points_table.py`, `data/numbers.json`, `tables/*.tex` (generated).

### G7-07 S4: unsafe hand-written displays
- Sources: sol-numbers 1, 3. Severity: major. Decision: accept. Reason
  (rechecked for this adjudication from
  `research-20260929/reviews/bound-audit-verification/logs/kraw_*.json`,
  field `obj_hi`, with `Fraction`): the printed upper ends lie below the
  exact upper ends by `1.450e-11`, `4.061e-14` and `3.345e-15`.
- Change: `tab:audit-second` (`E-audit.tex:292, :294, :300`):
  `glider100` $-983842.2577881224\to-983842.2577881223$;
  `methanol50` $0.0079302187992\to0.0079302187993$;
  `nuclear14` $-1.12968744117116\to-1.12968744117115$.
  `E-audit.tex:565`: "at most $2.38\cdot10^{-16}$" → "at most
  $2.39\cdot10^{-16}$" (exact maximum $1/4196280000000000$). Log the exact
  checks (a short `/tmp` script and its output, kept in
  `development/reviews/round1/`).
- Files: `sections/E-audit.tex`.

### G7-08 S4: classes, reruns, emfl and topopt
- Sources: opus-referee M6; opus-writing 40; opus-claims 2; sol-referee 2.
- Severity: major. Decision: accept.
- Change:
  - S4.1 and `tab:audit-classes`: the class rule of G3-08, with the
    half-unit note.
  - `app:audit-rocket` and `app:audit-history`: record that on 2026-10-04 a
    separate agent session reran the second `rocket` proofs from copies
    (every inclusion test passed; brackets
    $[-1.0128320069151,-1.0128320069130]$,
    $[-1.0128356770698,-1.0128356770677]$,
    $[-1.0128365294843,-1.0128365294821]$; pinned counts 76/64, 151/127,
    315/254) and the exact GAMS/OSIL comparison (23 identical models, the
    `methanol50` exception, three negative controls). Source: `sol-numbers.md`.
  - `emfl` box (`E:478`): "Evidence level: `\evid{hand}`
    (`\cref{lem:audit-socp}`) + `\evid{rerun}`: the rational dual vectors
    are not stored; a rerun solves the cone programs again and checks the
    new vectors exactly, and may give slightly different, equally valid
    endpoints."
  - `topopt` (`E:325`): keep "regenerated rather than replayed"; make
    `I:322` and §10 (G4-07) say the same.
- Files: `sections/E-audit.tex`.

### G7-09 S6 solvers
- Sources: sol-referee 6; opus-math-main 7; opus-claims 20.
- Severity: minor. Decision: accept.
- Change: `H:83–88`: describe `tab:claims` without the KKT row; keep one
  sentence: "Our floating-point KKT point of `optcdeg2` violates rows by up
  to `\sci{8.9}{-16}` and its objective lies at least `\sci{5.95}{-12}`
  above $\Uprim$; this says nothing about attainability or about the
  direction of tolerance effects in general." Proposition S6.1
  (`H:110`): margins and assumption as G4-03, with the exact recomputation
  of the violation thresholds or the round-to-nearest qualifier. MINOTAUR
  wording as G4-04 wherever S6 calls the report "false".
- Files: `sections/H-solvers.tex`.

### G7-10 S2 points
- Sources: opus-math-main 9; sol-math-supp2 4 and eg primal resolution.
- Severity: minor. Decision: accept-modified (as G6-07).
- Change: `C:156–162`: "$\Uprim$ from the attaining point ([E], width below
  `\sci{1.11}{-91}`); the Krawczyk points are enclosed at 110 digits
  (width below `\sci{3}{-109}`)". `C:269`: the eg dyadic check text of
  G6-07.
- Files: `sections/C-points.tex`.

### G7-11 S3 literature
- Sources: sol-literature 1, 5; opus-claims 13, 21, 23; opus-referee m18; opus-writing 29.
- Severity: minor. Decision: accept.
- Change: `D:171` → "In the search described in this supplement, we found
  no source treating this exact tap-free stored model." `D:229`: version
  locators as G1-08. `D:116–127`: prior status of `camshape200`,
  `camshape800` → related model (G2-06). `D:59` (opus-claims 21): drop "and
  a rigorous enclosure of the optimal value of $\RP$" or add "($\RP$ is our
  own construction)". S3.4 receives the funnel from §3.1 (G2-03), with the
  graphs named (opus-writing 29: "of the factor-incidence graph or of the
  nonlinear-primal graph of the model") and the definition before its first
  use. opus-claims 23: list in S3.1 the sources read for the audit-novelty
  search (the paragraph "Benchmark checks and solver reliability" partly
  does this).
- Files: `sections/D-literature.tex`.

### G7-12 S7 reproduction guide and register
- Sources: LD-1, LD-7; sol-numbers 5; sol-referee 1, 2, 13; opus-claims 1 (`I:318`), 3, 4; opus-math-main 12; opus-referee M5, M7.2.
- Severity: major. Decision: accept-modified (R-03 for the archive
  restructuring).
- Change:
  - Opening paragraph: one sentence pointing to §2.6 for how the
    implementations were produced (LD-1; opus-referee M3.3).
  - Define the trust labels T-int … T-thm here (moved from §2.5).
  - `:23`: describe the archive layout accurately ("it keeps the layout of
    our working tree; `$R` and `$P` …") and add a per-family table or list
    of replay entry points with tier and expected output (opus-referee M5,
    without renaming directories).
  - `:45` (sol-numbers 5): "It checks the certified bound, primal, gap and
    derived margin displays that it generates against their exact values in
    rational arithmetic; hand-written tables and fixed metadata require
    separate checks."
  - `:51`: replace the historical "all valid" sentence by the counts and
    result of the final validation of G7-15 (claims, SHA-256 references,
    files).
  - `:56` (sol-referee 13): remove the instruction to edit the absolute path
    of `gibbs_cert.py` after G7-16.
  - `tab:repro-register`: add the status column (G1-02; opus-claims 4);
    `catmix` "Tier 2; rerun"; tiers per G4-07; KAN rows name the guarded
    path (I) and its logs.
  - `:318` "A separate review reran" → "A separate agent session reran";
    add the guarded six-model replay.
  - `:322` (sol-referee 2): topopt and emfl as in G7-08.
  - `tab:sem-hashes`: add $n$ ($n_{\mathrm{int}}$)/$m$ (from G7-01).
  - Move long command tables to the artifact README (LD-2).
- Files: `sections/I-reproduction.tex`.

### G7-13 S8 display record
- Sources: LD-2; opus-math-main 7. Severity: minor. Decision: accept.
- Change: shrink to 2 pages (keep the unsafe-string table; move narrative
  history to the artifact README); QPLIB row: safe displays
  `\sci{3.11}{-3}`, `\sci{1.54}{-4}` under the stated assumption.
- Files: `sections/J-displays.tex`.

### G7-14 references.bib
- Sources: sol-literature 3, 4, 6; KB sources for G1-08.
- Severity: minor. Decision: accept-modified. Reason: the BibTeX proposed in
  sol-literature 3 gives issue 2; the KB record and the lead author give
  JOGO 91(3):437–456 (`literature/papers/araya2025-hybridizing-two-linear-relaxation-techniques/paper.md`).
- Change: add `araya2025-hybridizing-two-linear-relaxation-techniques`
  (JOGO 91(3):437–456, 2025, doi 10.1007/s10898-024-01449-2);
  `borst2024-certified-constraint-propagation-and-dual` (arXiv:2403.13567;
  use the KB slug as key); `szeider2026-vipr-certificate-construction-from-black`
  (CP 2026, LIPIcs 379, 52:1–52:14, doi 10.4230/LIPIcs.CP.2026.52); if G1-08
  uses them, `belotti2025-solving-minlps-to-global-optimality`
  (Optimization, 2025, doi 10.1080/02331934.2025.2595437) and
  `merx2026-from-computational-certification-to-exact` (arXiv:2603.11107;
  author Nathan Sudermann-Merx). `bonami2018-…`: keep the `author` field
  for plainnat and add `note = {Edited report; see Berthold's contribution, §3.6, p.~71}`.
  Check that every new key resolves in both documents.
- Files: `references.bib`.

### G7-15 Artifact: claim builder, README, index rebuild and validation
- Sources: LD-7; sol-referee 1, 13; opus-claims 4; opus-referee M5 (ii); LD-1.
- Severity: major. Decision: accept-modified (DOI and licence stay marked
  placeholders, LD-1(b)).
- Change:
  - `artifact/build_claims.py:179` (opus-claims 4, checked): the rule tests
    the obsolete macros `\evid{P}`/`\evid{S}`, so a rebuild would label
    every entry "computed". Read an explicit status per register row (G7-12
    column) instead; map: proved / verified by a separately written
    implementation / proved with a weaker second check / floating-point
    output (campaign). Rejected part of opus-claims 4: labelling `optcdeg2`,
    `lukvle10`, `catmix`, `etamac`, `pindyck`, `eg_disc2_s` "computed" (R-07).
  - Include in the relevant entries the guarded KAN source and logs
    (`development/reviews/round1/kan-guard/`), the eg dyadic test and logs
    (`development/reviews/round1/eg-dyadic/`), and the round-1 rerun logs
    that the text cites.
  - `artifact/README.md`: delete the paragraph addressed to
    "paper-editing agents" and the obsolete statement about S7.1
    (`:172–174`); ANN entry (`:155`): "verification about 1.2 h wall on two
    processes (2.0 CPU-hours)"; add one sentence on provenance pointing to
    §2.6 (LD-1); state that the built PDFs are included in the release;
    keep the DOI and licence as marked placeholders; describe the KAN
    guarded replay and the eg dyadic test.
  - After every other group has finished: copy `build_claims.py` and
    `check_claims.py` to `/tmp`, rebuild `artifact/claims.json`, run the
    validator, and require "OK" with zero errors; store the output in
    `artifact/logs/`; run `run_short_checks.py` from `/tmp` if any path it
    uses changed. Then update the counts in S7 (G7-12) and rebuild once
    more if S7 changed (the validator hashes S7).
- Files: `artifact/build_claims.py`, `artifact/README.md`, `artifact/claims.json`, `artifact/logs/`.

### G7-16 Gibbs checker path
- Sources: sol-referee 13. Severity: minor. Decision: accept.
- Change: in `development/dossiers/small-checks/r2/gibbs_cert.py` replace the
  absolute-path constant by `os.environ['MINLP_REPO_ROOT']`-relative paths
  (no numerical change); record the edit in `artifact/path-edits.json`;
  run the script once from a `/tmp` copy to confirm unchanged output.
- Files: `development/dossiers/small-checks/r2/gibbs_cert.py`, `artifact/path-edits.json`.

### G7-17 Development records
- Sources: opus-claims 23; LD-1; open items 1–4; opus-writing 32.
- Severity: minor. Decision: accept.
- Change: `development/open-items.md`: item 1 resolved (sol-math-main,
  opus-math-main: Appendix B proofs correct); item 2 resolved
  (sol-math-supp2, `eg-dyadic/`); item 3 resolved (sol-numbers reruns);
  item 4: claim index rebuilt (G7-15), README updated, audit-priority
  sentence exists with its search scope (opus-claims 23).
  `development/labels.md:48`: the declarations contain an AI-use statement.
  `development/terminology.md`: status words (G1-02), audit classes
  (i)/(i-r)/(ii)/(ii′)/(iii), "split form", certificate boxes only in the
  supplement with a one-sentence certificate note in the main text, tier
  rule, prior status of the camshape copies.
- Files: `development/open-items.md`, `development/labels.md`, `development/terminology.md`.

### G7-18 Length of S2, S3, S4, S6, S7, S8
- Sources: LD-2; sol-referee 5. Severity: major. Decision: accept.
- Change: targets S2 6, S3 5.5, S4 10.5, S6 10, S7 5, S8 2 pages. Remove
  per-instance repetitions of main-text tables; move command lists and
  historical notes to the artifact README; keep every proof and every
  certificate box.
- Files: `sections/C-points.tex`, `sections/D-literature.tex`, `sections/E-audit.tex`, `sections/H-solvers.tex`, `sections/I-reproduction.tex`, `sections/J-displays.tex`.

---

## 9. Rejections (full or partial), with reasons

| id | source | rejected | reason |
|---|---|---|---|
| R-01 | opus-referee M1.7 | splitting the audit and solver findings into a separate paper | the lead author keeps one paper; sol-referee judges a split unnecessary if the text is consolidated (LD-2 does this) |
| R-02 | opus-referee M4 option (a) | a new 14-CPU-hour solver experiment with derived enclosures | LD-5 frames §9 as an untested interpretation; a new campaign is outside this revision and its two-core limit |
| R-03 | opus-referee M5 (i), (iii), (iv) | renaming archive directories per family; storing leaf partitions of rerun certificates; a second-machine replay | the archive mirrors `research-20260929/`, which must not be edited; storing partitions needs new computations; no second machine is available. The limits are stated instead (G4-08, G7-12) |
| R-04 | opus-referee M7.1 | a half-page glossary in the main text | conflicts with the 38-page target; the taxonomies are reduced instead (T-* labels to S7, tiers in §10 only, instance-list dual defined once) |
| R-05 | opus-referee M1.5 | moving Appendix B.1–B.5 and A.2–A.5 to the supplement | the appendices are outside the 38-page target, both math reviews verified Appendix B, and the supplement must shrink by 30 pages |
| R-06 | opus-referee m10 | moving the proofs of Proposition 4.3(c) and of the maximality part of 4.5 | same reason as R-05; the statements are marked explanatory instead (G2-08) |
| R-07 | opus-claims 4 (mapping) | labelling single-implementation computer proofs "computed" | under the §2.6 definitions (G1-02) these are proved; their second implementation certifies a weaker bound, which the status column says |
| R-08 | opus-referee m13 | dropping the hollow-triangle marker | LD-4 requires distinct markers for tightened SCIP models |
| R-09 | sol-referee 11 | promoting a compact Figure S4 to the main text | length target; §5.1 and §8.1 point to Figure S4 |
| R-10 | opus-referee m3 | removing the result numbers from the first paragraph | sol-referee values the numerical opening; repetition is cut in the contribution list (G1-07) |
| R-11 | opus-referee m16 | filing the SCIP issue and writing to the MINLPLib maintainer | an author action, not a text change; the dated "to our knowledge" sentence stays true until then |
| R-12 | opus-referee B2; sol-referee 1 (placeholders) | filling authors, licence, competing interests, funding and the DOI now | LD-1(b): these stay marked placeholders for the authors |
| R-13 | opus-referee M2 | running a rigorous interval solver | outside this revision; the text states why such bounds would still need exact existence proofs (G1-08) |
| R-14 | opus-claims 2 | reducing the headline to 19 bounds on 15 instances | the condition (reviewer rerun of the rocket proofs and the GAMS/OSIL comparison) is met by sol-numbers; the reruns are recorded (G3-11, G7-08) |
| R-15 | opus-writing 3 (option) | renaming the code-level notion to "data entry" everywhere | churn across boxes, tables and generators; the required uses of "reading" are fixed and "data reading" is kept as the defined term |
| R-16 | opus-referee M7.4 | replacing "fp near-closure" by the gap in Table 2 | Table 2 must get narrower (LD-3); §3.4 gives the gaps |
| R-17 | opus-claims 18 (part) | writing "archived" only after the DOI exists | LD-1(b) keeps `\archiveDOI` as a placeholder to be filled before submission; the archive is deposited before submission |
| R-18 | opus-referee M2 (ann) | removing `ann_cumene_tanh` from the abstract | the qualifying clause about the exp variant suffices (G1-03) |

---

## 10. Coverage index (review item → adjudication id)

- **sol-math-main:** 1 → G2-08, G2-14; 2 → G3-03, G5-11; 3 → G2-12, G5-05; 4 → G2-09, G5-10, G7-04; open item 1 → G2-14, G4-08, G7-17.
- **sol-math-supp1:** 1 → G5-03; 2 → G5-04; 3 → G2-12, G5-05; 4 → G5-06.
- **sol-math-supp2:** 1 → G3-06, G6-03, G7-04, G7-15; 2 → G6-05; 3 → G6-06; 4 → G6-07, G7-10; eg primal resolution → G6-07, G7-10, G7-17.
- **sol-numbers:** 1 → G7-07; 2 → G4-04; 3 → G7-07; 4 → G7-05; 5 → G4-07, G7-06, G7-12; open item 3 reruns → G3-09, G3-11, G7-08, G7-17.
- **sol-literature:** 1 → G1-08, G7-11; 2 → G1-08; 3 → G1-08, G6-10, G7-14; 4 → G1-08, G3-07, G7-14; 5 → G1-08, G7-11; 6 → G1-08, G7-14.
- **sol-referee:** 1 → G7-15, R-12; 2 → G1-14, G4-07, G5-10, G7-08, G7-12; 3 → G7-01, G7-02; 4 → G1-03, G1-07, G2-01, G4-05, G7-06; 5 → Section 2, G2-15, G3-13, G5-14, G7-18, R-01; 6 → G7-02, G7-09; 7 → G4-03, G4-04; 8 → G1-03, G1-07, G1-08, G2-04, G2-06; 9 → G2-08, G2-14, G3-07; 10 → G1-01, G1-02, G7-04; 11 → G2-01, G2-04, G3-03, G4-06, G7-01, G7-06, R-09; 12 → G1-03, G1-05, G1-13, G1-14, G4-06; 13 → G7-12, G7-15, G7-16.
- **opus-referee:** B1 → G7-01, G7-03; B2 → G4-01, R-12; M1.1 → G1-07; M1.2 → G1-14, G7-04; M1.3 → G2-09, G3-02, G5-01, G6-01; M1.4 → G2-15, G3-13; M1.5 → R-05; M1.6 → G4-06; M1.7 → R-01; M2 (a) → G1-03, G4-05; (b) → G1-03, G1-07; (c) → G1-03, G3-06, R-18; (d) → G1-03; C7 → G1-07; rigorous solvers → G1-08, R-13; M3 → G1-01, G4-01, G7-12; M4 → G1-06, G4-06, G4-08, R-02; M5 → G4-08, G7-12, G7-15, R-03; M6 → G1-07, G3-08, G7-08; M7 → G1-10, G1-14, G1-15, G2-03, R-04, R-16; m1 → G1-06, G2-07; m2 → G1-06; m3 → G1-04, R-10; m4 → G1-05; m5 → G1-05; m6 → G1-08; m7 → G1-06; m8 → G1-14; m9 → G1-14, G6-11; m10 → G2-08, R-06; m11 → G2-09, G3-02; m12 → G7-06; m13 → G2-01, R-08; m14 → G4-06; m15 → G4-07; m16 → G4-08, R-11; m17 → G1-07; m18 → G2-03, G7-11.
- **opus-math-main:** 1 → G1-10, G1-16; 2 → G1-13, G3-09; 3 → G2-08, G2-14; 4 → G1-14; 5 → G3-06; 6 → G3-04, G6-08; 7 → G4-03, G7-06, G7-09, G7-13; 8 → G1-11; 9 → G3-07, G5-08, G7-05, G7-10; 10 → G1-16, G6-04; 11 → G1-16, G5-09; 12 → G1-15, G2-09, G4-07, G5-13, G7-12; 13 → G2-10, G2-14; notation remark → G2-08.
- **opus-claims:** 1 → G1-01, G1-06, G2-03, G4-01, G4-08, G5-02, G6-02, G7-12; 2 → G3-09, G3-11, G7-06, G7-08, R-14; 3 → G1-14, G2-04, G2-09, G4-07, G5-10, G7-04, G7-12; 4 → G1-02, G7-04, G7-12, G7-15, R-07; 5 → G1-06, G1-07, G2-13; 6 → G1-06; 7 → G1-07; 8 → G2-09, G5-10; 9 → G1-14, G3-10, G6-09, G7-04; 10 → G1-01, G6-09; 11 → G3-06, G6-03, G7-04; 12 → G7-02; 13 → G1-07, G2-06, G7-06, G7-11; 14 → G2-05; 15 → G3-02, G7-04; 16 → G3-02, G3-05, G3-07, G5-12; 17 → G1-11; 18 → G1-07, G4-07, R-17; 19 → G1-07; 20 → G1-07, G4-04, G7-09; 21 → G5-07, G7-11; 22 → G4-08; 23 → G7-11, G7-17.
- **opus-writing:** 1 → G1-02, G3-09; 2 → G1-01; 3 → G1-14, G1-16, G4-06, G4-08, R-15; 4 → G1-06, G2-07; 5 → G2-11; 6 → G2-02; 7 → G3-01; 8 → G1-10, G3-12; 9 → G1-03; 10 → G1-04; 11 → G1-05; 12 → G1-05; 13 → G1-05; 14 → G1-05; 15 → G1-05; 16 → G1-06; 17 → G1-07; 18 → G1-07; 19 → G1-07; 20 → G1-07, G4-06; 21 → G1-08; 22 → G1-10; 23 → G1-10; 24 → G1-10; 25 → G1-11; 26 → G1-12; 27 → G1-12; 28 → G1-13, G1-16; 29 → G7-11; 30 → G2-08; 31 → G2-07, G2-08, G2-13; 32 → G2-08, G2-11, G5-13, G7-06; 33 → G2-08; 34 → G2-11; 35 → G3-03, G3-04; 36 → G3-06; 37 → G3-06, G4-07; 38 → G3-07, G4-08; 39 → G3-08; 40 → G3-08, G7-08; 41 → G3-09; 42 → G3-08; 43 → G3-11; 44 → G3-11; 45 → G4-02; 46 → G4-04; 47 → G4-05; 48 → G4-06; 49 → G4-07; 50 → G4-08; 51 → G1-16; 52 → Section 0 rule 6, G2-06, G2-15, G3-03, G3-07, G3-13.
- **Follow-up results:** `kan-guard/report.md` → G3-06, G6-03, G7-04, G7-15; `eg-dyadic/` → G6-05, G6-07, G7-10, G7-15; rocket and GAMS/OSIL reruns (sol-numbers) → G3-09, G3-11, G7-08.

## 11. Counts

| group | items | blocker | major | minor | accept | accept-modified |
|---|---:|---:|---:|---:|---:|---:|
| G1 front | 16 | 1 | 5 | 10 | 9 | 7 |
| G2 results and split | 15 | 0 | 7 | 8 | 10 | 5 |
| G3 other, points, audit | 13 | 0 | 5 | 8 | 9 | 4 |
| G4 solvers and end | 9 | 1 | 5 | 3 | 4 | 5 |
| G5 supplement certificates I | 14 | 0 | 5 | 9 | 13 | 1 |
| G6 supplement certificates II | 12 | 0 | 4 | 8 | 11 | 1 |
| G7 supplement other, generators, bib, artifact | 18 | 2 | 9 | 7 | 13 | 5 |
| **total** | **97** | **4** | **40** | **53** | **69** | **28** |

Rejections: 18 (Section 9), all partial or full rejections of single review
points; every review item maps to at least one change or rejection
(Section 10).
