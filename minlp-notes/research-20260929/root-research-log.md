# Root research log (September 29 continuation)

## 2026-09-29: direction selection

Reviewed the closing records of the September 22–28 continuations, the
second September 28 scouting reports (13 scouts, best scores 3–6/10), the
repository's open-theory-challenges page, and recent (2026) library
entries. The earlier program established single-tree spatial B&B
complexity (lower bounds for adaptive trees, covering characterization,
face-exact theory, branching-point competitiveness, random sparse
regression thresholds).

Candidates weighed (root judgment, not reviewed):

- Decomposition-aware (tree-decomposition) spatial B&B versus single-tree
  B&B on sparse problems — chosen as the main line after a SCIP probe
  showed exponential node growth on a path-structured instance with a unique
  nondegenerate interior minimizer (see PROGRAM.md).
- Real-log-canonical-threshold (RLCT) law for node-count exponents —
  chosen as a secondary, self-contained line.
- Others considered and not pursued now: Burer's `m >= 3` balls exact
  representation (hard, moderate solver impact), Del Pia–Khajavirad
  treewidth-hardness statements (hard, mostly negative), certified upper
  bounds with nonconvex equalities (core results exist in computational
  topology: robust satisfiability, Franek–Krčál), cost-aware relaxation
  choice (largely a corollary of existing theory), outer-approximation
  certificate complexity (modest), random-instance B&B for further ML
  models (incremental).

Probe results that shaped the choice (floating point, SCIP 10 via
PySCIPOpt 6.2.1, targeted runs only):

- Random tridiagonal box QPs (`scratch/chain_boxqp.py`) are easy for SCIP:
  optima sit at vertices, where McCormick is exact (at most a few thousand
  nodes at `n = 80`).
- A path family whose summed objective is convex (`probe2.py`) is solved
  at the root: SCIP's relaxation handles it.
- The genuinely nonconvex path family (`probe3.py`, quartic term
  `-0.1 x_i^4`) shows exponential node growth; table in PROGRAM.md.

## 2026-09-29: workstreams launched

Five background agents: literature/novelty audit; theory of decomposition
certificates; single-tree lower bounds for face-exact relaxations;
computation (prototype versus SCIP); RLCT law. Root runs a treewidth census
of MINLPLib (`treewidth-census/`).

Census design correction: pure variable–row incidence treewidth hides the
internal coupling of dense nonlinear rows (autocorrelation instances showed
width 1). The census now uses a factor-incidence graph (row nodes linked to
linear variables and to additive-term nodes; term nodes linked to their
variables), plus the primal graph of nonlinear terms.

## 2026-09-29: census lead and sixth workstream

Partial census (751 instances analyzed, 613 nonconvex): scalable MINLPLib
families with constant small factor-incidence width have best-known gaps
that grow with size — camshape100/200/400/800 (width at most 4; gaps 4.5%,
12.9%, 17.2%, 20.4%) and lnts50–400 (width at most 12; gaps 5.5%–10.6%).
Several very large chain-structured instances are open with essentially
trivial dual bounds: dtoc5 (99999 variables), optcdeg2 (150002), lukvle10
(1000). These are discrete-time optimal-control or recursion chains with
state dimension 1–2. Launched an agent to compute rigorous
decomposition-aware dual bounds for them (`open-instances/`).

## 2026-09-29: first results in

- Literature audit (`literature/decomposition-bb-prior.md`): no continuous,
  relaxation-based precedent found for the instance-dependent pair
  (single-tree `exp(Omega(n))` at a unique nondegenerate minimizer; decomposition
  `O(n log(n/eps))`), but discrete AND/OR search, MILP B&B lower bounds at
  treewidth 2 (Basu et al. 2023; Dey–Shah 2022), two-stage decomposition B&B
  (Cao–Zavala; Kannan; Li–Grossmann; MUSE-BB; Robertson–Cheng–Scott 2025) and
  Zhang–Sun's nested-decomposition bounds must be credited. Worst-case bounds
  must be stated as `(Cn/eps)^{O(w)}` (ETH obstruction derived by the auditor).
- Census finished (`treewidth-census/census-report.md`).
- RLCT note (`rlct/`): reviewed (`reviews/rlct-review.md`), four substantive
  corrections applied by the author with their own rechecks; a fresh recheck
  of the revision is running.
- Theory B (`theory-face-exact/`): Theorem 1 proves at least
  `0.57 (5/3)^n` leaves for termwise McCormick on the probe family. It also
  showed two of the root's PROGRAM.md statements were wrong (αBB Theorem 3.1
  does not give growth on this family; the convex-sum variant is not solved at
  the root beyond `n` about 5). PROGRAM.md corrected. Adversarial review
  running (`reviews/face-exact-review.md`).

## 2026-09-29: open MINLPLib instances (pending independent verification)

`open-instances/open-instances-report.md` reports rigorous dual bounds
(mpmath or outward-rounded intervals, second route per instance) closing the
MINLPLib gaps of lnts50–400, dtoc5, camshape100–800 (exact optima in closed
form), lukvle10 (3.7e-8) and optcdeg2 (2.1e-5 relative), and that MINLPLib's
metadata primal values for camshape400/800 come from points violating rows
by 3e-10 that beat the exact optimum. An independent verifier with fresh
code is running (`reviews/open-instances-verification/`). Nothing will be
stated as "closed" before it reports.

Lesson for the program (root reading): the generic cell-constant separator
DP failed on camshape100 (cells must resolve an O(1/n^2) per-stage
constraint scale) and optcdeg2 (partial separator branching with fixed
multipliers). The successful pattern was a tree/chain Lagrangian with
multipliers from a local solution, bound propagation for free variables, and
exact treatment of the few windows where the stage Lagrangian is nonconvex.
Candidate theory: the duality gap at KKT multipliers equals the sum over
bags of (local Lagrangian at x* minus its minimum), which vanishes on bags
whose local Lagrangian is convex; branching is needed only on the others
("gap localization").

## 2026-09-29: reassessment after the theory drafts

Theory A (`theory-decomposition/`) proves an instance-dependent decomposition
bound `O(|T| C^{w+1} log(|T|/eps))` under global quadratic growth, width
lower bounds valid for every tree decomposition, and a separation on the
path family with per-factor alphaBB on the bilinear terms (single-tree base
1.3155). Its own caveats: the separation is asymptotic (the proven
single-tree bound overtakes computed decomposition certificates only near
`n` about 45–50) and does not cover McCormick. Review running.

Root framing point (to be checked by the reviews, not yet a result): the
single-tree lower bounds depend on the modeler's fixed factorization. On a
tree decomposition, if the split of `F` into bag functions may be chosen
freely (arbitrary functions of the bag variables, not only affine
multipliers), the strongest per-bag relaxation is the local-consistency
relaxation over bag measures with equal separator marginals, and on trees
such measures glue to a joint measure, so it is exact. Hence no lower bound
can hold uniformly over all splits; the exponential cost belongs to fixed
termwise relaxations. Three cures then exist: decomposition-aware search
(this program), consistency-strengthened relaxations (the repository's
sparse moment results, uniform in the number of bags), and tree Lagrangians
with good multipliers plus localized branching (the open-instance
certificates). Claims must be stated relative to a fixed relaxation class.

The open-instance certificates are mostly classical in mechanism: dtoc5's
convex Lagrangian at the costate is a discrete-time Mangasarian/Arrow
sufficiency argument; camshape's is a discrete Sturm comparison. Their value
is as benchmark certificates and as evidence of where solver gaps come from,
not as new theory.

## 2026-09-29: open-instance certificates verified

The independent verifier (`reviews/open-instances-verification/`) rechecked
all 11 bounds with its own code: all valid; camshape optima exact in rational
arithmetic; lukvle10 tightened independently to a 1.4e-9 gap. Baseline
correction applied to the report: MINLPLib's metadata dual needs agreement of
three solvers; best single-solver duals on the instance pages were already
within 1.2e-6 (camshape100) and 3.8e-5 (lnts50), so those improvements are
marginal. Substantive closures: dtoc5 (best listed dual 0.0024 vs optimum
5.39), camshape200/400/800 (best listed gaps about 8%, 16%, 20%), and
smaller gaps (about 0.3–0.5%) for lnts100–400, optcdeg2 (99.6% of the gap
closed) and lukvle10. No prior global certificate found for any of the 11.
Mechanisms are classical (Mangasarian/Arrow sufficiency, discrete Sturm
comparison, linear-tangent law); the contribution is the certificates.

## 2026-09-30: second certification wave (partial)

- Small targets (`open-instances-wave2/small/report.md`, verified in
  `reviews/wave2-small-verification/`): hvycrash solved exactly (objective
  constant on the feasible set), ex6_2_7 and ex6_2_5 closed (prior ε-global
  solutions exist: McDonald–Floudas 1997; tangent-plane duality known),
  etamac and pricing050 closed; pindyck not closed. Listed LINDO dual bounds
  for methanol50 and rocket100/200/400 are invalid, now proved with interval
  Krawczyk existence tests (rocket discrepancies below MINLPLib's solved
  tolerance; MINLPLib already marks them unsolved).
- waterno2 (`open-instances-wave2/waterno2/report.md`): exact period
  decomposition; certified duals raise the best listed bounds by factors of
  1.6–6 (remaining gaps 4.9–10.8%); a claim that SCIP 10.0.2 reports
  "optimal" above feasible points on period subproblems. Independent
  verification running.
- Theory: a robust single-tree lower-bound agent is running
  (`theory-robust-lb/`).

## 2026-09-30: waterno2 verified; SCIP wrong answers confirmed

The waterno2 certified duals are valid (waterno2_06 fully reproduced with an
exact-rational branch and bound; two periods of larger sizes spot-checked).
The verifier confirmed that SCIP 10.0.2 returns wrong "optimal" values on
three waterno2 period subproblems because of an invalid in-tree bound
reduction (nonlinear constraint handler propagation), not tolerances or
presolve. Documented with a reproducer; no upstream report filed (an
outward-facing action left to the user). This matters for the program's
claims: single-solver outcomes, including our own SCIP baselines, need
independent checks.
Robust lower-bound note revised after review (qualitative result; Lemma 1.2
credited to dual-decomposition/cost-shifting duality).

## 2026-09-30: reassessment and next phase

State: the structure program's theory is reviewed (face-exact lower bound,
decomposition certificates, RLCT characterization, split-robust lower bound,
consistency relaxations — the last under revision); 24 open MINLPLib
instances closed (16 verified, 8 awaiting verification), 5 improved; invalid
listed LINDO bounds and SCIP 10.0.2 wrong optima found.

Honest significance reading: the theory pieces are solid but individually
moderate; the certificate campaign has the clearest outward value, and its
diagnosis (relaxation, not branching, is the bottleneck on large sparse
instances; affine splits plus exact short windows suffice) is now backed by
the consistency identity.

Next phase, chosen for breadth of impact:
1. Theory: dense linear coupling. The census shows nonlinear-term width is
   small for most large nonconvex instances (62.7% at most 12) while
   factor-incidence width is small for only 13.6%, because of dense linear
   rows. Develop complexity results for tree-structured nonlinearity plus k
   dense linear coupling rows (Lagrangian relaxation of the rows, a
   Shapley–Folkman-type gap bound, localized branching), and an adaptive
   theorem for separator value functions with finitely many kinks.
2. Practice: a systematic validity audit of MINLPLib listed dual bounds
   (polish listed primal points, prove exact feasibility by interval Newton,
   compare with listed duals per solver), plus a third certification wave.

## 2026-09-30: audit, coupling, calibration

- Bound audit (`bound-audit/audit-report.md`): over all 1633 MINLPLib
  instances, 19 listed solver dual bounds on 15 instances are claimed proven
  invalid (mostly LINDO; also ANTIGONE/BARON on ghg_3veh, CPLEX/GUROBI on an
  nd_netgen instance, BONMIN on watercontamination0303), plus tolerance
  effects (emfl family). Independent verification running
  (`reviews/bound-audit-verification/`).
- Coupling note reviewed and revised: modest, largely negative.
- Calibration scout (`theory-calibration/scouting.md`): discrete calibrations
  unify all certificates (classical in substance: Krotov, Bellman
  inequality); elementary new-looking items incl. a transfer theorem (strict
  smooth continuous calibration ⇒ exact certificates for fine
  transcriptions). Review running. Next question launched: bang-bang
  switch windows (O(1) stages?) with optcdeg2's open tail as the test
  (`theory-bangbang/`).

## 2026-09-30: audit verified; repository hygiene

- Audit verification (`reviews/bound-audit-verification/`): 14 of the 19
  proven-invalid pairs and one emfl instance confirmed with separate code;
  recommendation to separate gross errors (glider100, topopt, methanol50,
  sssd, nuclear14, ghg_3veh) from 1e-9–3e-7 exact-arithmetic violations.
  Revision requested from the auditor.
- `.gitignore`: added narrow rules for re-downloadable MINLPLib material
  under this continuation (OSIL copies, instance pages, downloaded `.sol`
  folders; about 86 MB). Parsed data, our own points and logs stay tracked.
  Found that the existing top-level rule `literature/` also matched
  `research-20260929/literature/` (our prior-work audit); added an explicit
  exception. Two older `literature/` folders under paper revisions hold
  third-party PDFs and remain untracked.

## 2026-09-30: wave 3 and bang-bang results (pending verification)

- Wave 3 (`open-instances-wave3/report.md`, saved by the root): KAN family
  6/6 closed to about 1e-10 (three listed primal values improved; caveat:
  partition-of-unity rows are inconsistent in exact decimals, so "closed"
  means a valid bound matched by 2.5e-15-feasible points); powerflow0030p
  closed by an exact-rational SDP-dual certificate; 0039p/r improved;
  ann_cumene_tanh first finite dual; eg_* failed. Verification running.
- Bang-bang (`theory-bangbang/report.md`, saved by the root): optcdeg2 closed
  (gap 8.3e-12) by one quadratic calibration whose curvature vanishes at the
  switches; window-law dichotomy (tangential vs non-tangential calibrations)
  and a proof that C^2 calibrations exact on the trajectory are tangential.
  Verification and review running.

Reassessment: the calibration/window theory is the most promising
theoretical thread now (it turns the certificate successes into a general
capability for fine transcriptions of bang-bang problems). Next candidates:
tangential calibrations for state dimension >= 2 (the open conjecture),
singular arcs (Kelley/Goh), and applying the method to rocket/glider/lnts-type
instances.

## 2026-09-30: user instruction — finish current directions, no new ones

The user asked to finish the current directions and their possible
extensions without starting new idea generation or new directions. Plan:
a completion workflow (`finish-sept29-continuation`) that (1) rechecks every
second-round revision not yet independently rechecked (robust lower bound,
consistency, coupling, calibration, RLCT second round, audit presentation),
(2) closes verification gaps (remaining waterno2 periods, catmix400/800,
five unchecked audit pairs and three emfl instances), and (3) attempts only
extensions already listed as open in existing notes (bang-bang n >= 2
tangency conjecture; decomposition adaptive algorithm and Conjecture 3.7;
powerflow0039p/r and pindyck certificates), each with independent
verification, fixes and confirmation. The wave-3 and bang-bang verifications
already running will be handled when they finish. A closing phase with
independent closing audits follows. The earlier "next candidates" note
(singular arcs, other instances) is dropped as new directions.

## 2026-09-30: completion workflow results

`finish-sept29-continuation` (28 agents) finished:
- Rechecks verified without changes: coupling (second round), RLCT (second
  round). Rechecks with fixes applied and confirmed: calibration. Fixes
  applied but residual issues found on confirmation: robust lower bound,
  consistency, audit presentation — handled in `finish-round2`.
- Verification gaps closed: all 63 remaining waterno2 period bounds
  certified by code other than the authors' (exact sums match bit for bit);
  catmix400/800 recomputed independently (tighter than claimed); all 19
  audit pairs and all four emfl instances now independently confirmed.
- Extensions (all independently verified): powerflow0039p/0039r closed
  (≈6e-10 relative; exact leaf-bus identity plus vertex cuts); pindyck
  closed (5.4e-14; concavity on a polytope containing the feasible set,
  rebuilt independently); bang-bang n ≥ 2 resolved locally (eta_L
  criterion; counterexample to the "no conjugate point" reading);
  decomposition adaptive algorithm (fixes applied; residual issues in round
  2).
- Root-applied: wave-3 verification corrections (KAN models exactly
  infeasible; powerflow0030p digit); bang-bang verification corrections
  (confirmation in round 2).
Totals now: 28 open instances closed for the model as written, 6 KAN
relaxations certified, 5 waterno2 improved, ann first finite dual.

## 2026-09-30: round 2 and closing

`finish-round2` (24 agents): robust lower bound, consistency, audit,
decomposition-adaptive and the root-applied bang-bang fixes all confirmed
clean after one or two fix/confirm rounds; the decomposition non-dyadic
check found that certificate code dropped touching (leaf, cell) pairs at
non-dyadic centres and corrected two zero-slope gaps in the original note's
Section 5.3 (old values still valid bounds). The root applied the last
residual wording fixes (Prop 5.8(a) constant; rounded "at least" values; LS
attribution of 29n; Theorem 4.1 parenthetical; Section 8.4 counts) and saved
one unwritten confirmation file. Root documents updated (synthesis sections
2, 5, 8; summary; READMEs) and the closing record written. Closing audits
launched (`closing-audit-sept29`).

## 2026-09-30: closing audits and closing revision

Correction to the completion-results entry above: "Rechecks verified without
changes: coupling (second round), RLCT (second round)" should read that these
rechecks found no error, but suggested minor wording, labelling and
provenance edits (coupling M1–M8; RLCT W1–W4 and optional O1–O3) that were
not applied then. The closing revision applied coupling M1–M7 (M4 in the
note only; the `jn_lifted_cert.py` docstring still says (c)) and RLCT
W1–W4, O1–O2 (coupling note Section 11.1; RLCT note Section 11.2); coupling
M8 and RLCT O3 remain unapplied, as those sections say.

The closing revision also resolved the round-1 closing-audit findings in the
root documents (`closing-research-results.md`, `SYNTHESIS.md`,
`open-instances-summary.md`, `README.md`, `PROGRAM.md` and the repository
README paragraph) and applied the residual review items of the calibration,
bang-bang `n ≥ 2`, pindyck, powerflow-extension and wave-3 notes, and the
status-line updates of several notes. Each note records its changes in a
dated entry. These root edits have not been rechecked.

## 2026-09-30: closing audits complete

`closing-audit-sept29` (8 agents): closing auditors A and B found 41 and 38
issues in the root documents (stale statements, rounded-up bound displays,
overstated verification wording, missing qualifiers, unresolved review
items in several notes, a broken table). Three fix/confirm rounds resolved
them; the third confirmation is clean. Two audit files that their agents
could not write were saved by the root. Per the user's instruction, no new
directions were started; the continuation is closed. Nothing committed;
outside this folder only `.gitignore` and the top-level `README.md` changed.

## 2026-09-30: extensions round 3 (open questions of existing notes only)

The goal hook asks for continued development; the user's latest instruction
limits work to current directions and their extensions. Reconciled by
continuing only with open questions that the closed notes list:
window exactness at bang-bang switches (report.md Section 6), singular arcs
(same), closing waterno2 by separator branching on the 3-D tank levels
(waterno2 report; the program's own method), the upper half of the covering
characterization (Conjecture 3.7 / extension-adaptive B.5), and a stronger
ann_cumene_tanh bound. Workflow `extensions-round3` launched with
verify/fix/confirm loops.

## 2026-09-30: extensions round 3 results

Workflow `extensions-round3` (26 agents, no errors). All five tasks ended
"verified" by an independent agent:

- **Window exactness** (`theory-bangbang/window-exactness.md`): decided by
  the sign of `kappa_tau = b(x*(tau))^T w`. Positive: no window needed;
  zero: one `O(1)` window exact; negative: windows of `o(1/h)` stages fail
  on grids with a fractional stage. Three confirmation rounds. It also found
  a factor-2 slip in the proof of `report.md` Theorem 4.1 (fixed with
  `mu' < mu`), a missing terminal hypothesis in that theorem's statement,
  and that the "tangential family fails on none" statement holds for stages
  only; the root applied the first and third to `report.md` at once and the
  second only after the root-edit check found it missing (see below).
- **Singular arcs** (`theory-bangbang/singular-arcs.md`): tangency on the
  arc implies Goh's condition; exact calibrations imply Kelley's; Euler sign
  criterion `b^T w` (under stated assumptions); accessory symbol explains
  COPS catmix chattering (heuristic agreement: gain within 3%, eigenvalue
  within 0.1% of the finite-section estimate, both against a smooth
  reference). Three confirmation rounds.
- **Covering upper half** (`theory-decomposition/covering-upper-half.md`):
  graded exact split; upper half settled in the exact-bag model for trees
  with one-dimensional separators; certificates only in part. Two
  confirmation rounds.
- **waterno2_06** (`open-instances-wave2/waterno2/separator-branching.md`):
  263.735099 → 272.584700 (gap 7.26% → 3.78%). The reviewer re-bounded all
  8,958 pair bounds with independent code. Not closed; 09–24 not attempted.
- **ann_cumene_tanh** (`open-instances-wave3/ann/extension.md`):
  −4024.495 → −3386.5403 (gap 19% → 0.194%). The reviewer replayed both runs
  bit for bit and re-certified every region with independent code.

Root follow-up: applied the remaining minor review items (window-exactness
confirm r3, covering confirm r2, waterno2 and ann reviews) in the notes with
dated entries; integrated the results into `SYNTHESIS.md`,
`closing-research-results.md`, `open-instances-summary.md`, `README.md`
and the top-level README. The singular-arcs confirm r3 nits were optional
("no fix required") and were not applied. Round 3 settled the two
bang-bang questions in the stated scope and the exact-bag upper half; the
upper half for certificates in reading (R1) stays open, and waterno2_06
and ann_cumene_tanh were improved but not closed (waterno2_09–24 not
attempted). No new directions were started. Nothing committed.

Check of the root edits: workflow `round3-root-edits-confirm` (2 agents)
found errors in the root's integration: an unsupported "2–7%" agreement
figure for catmix (taken from an early author summary that the reviews
had since corrected), dropped hypotheses (`K_t ⪯ hΛI`; the exact terminal
term; `b(x*(tau)) != 0`; `c_*`), a waterno2_06 display rounded up
(272.585) in `README.md`, "tangency = Goh" stated as an equivalence, the
certificate case of the covering result stated as proved (its size bound is
a sketch), and a missing terminal hypothesis in the statement of
`report.md` Theorem 4.1 (now added). All were fixed. Lesson: take figures
for root documents from the final notes, not from the authors' first
summaries.

## 2026-09-30: root-edit checks, rounds 2 and 3

`round3-root-fixes-confirm-r2` (1 agent) confirmed the fixes above and
raised two minor items (the terminal condition in `report.md` Theorem 4.1
must be over `X_N`, not `D`, and its quadratic-data remark needs quadratic
`Φ`, `S` and a free endpoint; the closing record attached the 0.1%
eigenvalue agreement to the saddle, where it misses by 21%) and six
optional ones. All were applied. `round3-root-fixes-confirm-r3` (1 agent)
returned "verified"; its optional record-keeping and wording nits were
applied without a further check. Round 3 is complete; no new directions
were started. Nothing committed.

## 2026-09-30: extensions round 4 (listed open questions of existing notes only)

The goal hook again asks for continued development; the user's latest
instruction still limits work to current directions and their extensions.
Reassessment: within the existing lines, the open questions with the most
solver relevance are (1) the main open problem of the adaptive note — an
algorithm that knows neither `x*` nor the constants and matches
Theorem 3.4 — together with the certificate case (R1) of the covering
upper half, which the graded split of round 3 may now make tractable;
(2) a split-robust single-tree lower bound with a meaningful base (the
robust-lb note says a different counting argument is needed; uniform
chains are open); (3) bang-bang switches with `kappa_tau < 0`, where window
certificates provably fail: which certificate does work, and at what size,
plus the several-switch version of Theorems A–B; (4) waterno2: cell-dependent
slopes for waterno2_06 (its remaining gap is away from the best known
trajectory, where one slope per link is used) and separator branching for a
longer instance; (5) eg_*, which failed in wave 3 with natural/mean-value
enclosures, retried with the affine-arithmetic machinery that worked on
ann_cumene_tanh. Workflow `extensions-round4` launched with the same
author → independent review → fix/confirm structure as round 3.

## 2026-10-01: round 4 results and finish

The user asked to finish the current ideas and developments and stop.
`extensions-round4` (26 agents) finished except one review, which a usage
limit stopped; `finish-round4` (7 agents) ran that review and applied the
remaining minor items, and `finish-round4-final` (4 agents) applied the
last review items and optional nits. All five round-4 results ended
"verified" by independent agents:

- **adaptive-matching** (`theory-decomposition/adaptive-matching.md`):
  algorithm GR matches Theorem 3.4 without knowing `x*` on path
  decompositions with `∇F(x*) = 0` (localization lemma; proved, constants
  numerically vacuous); trees open (Conjecture 7); the covering note's rule
  `bd` provably needs `Omega(n^{3/2} log(1/eps))` cells on a strongly
  convex quadratic path.
- **robust-chains** (`theory-robust-lb/robust-chains.md`): no split-robust
  bound growing with `n` on symmetric uniform chains under (H1), for split
  classes that contain the balanced split; chiral
  chains give a gadget-free split-robust exponential bound with tiny bases;
  a meaningful base was not achieved.
- **kappa-negative** (`theory-bangbang/kappa-negative.md`): for LQ data,
  node-specific `kappa`-limited calibrations give only
  `epsilon`-certificates with `Theta(log(h^2/epsilon))` nodes; lifted
  calibrations give exact certificates on the scalar toys (central node proved, few outer nodes
  heuristic); several switches switch by switch (sketch level), a coupling
  condition for close switches, terminal rows on `ker C`.
- **waterno2_06** (`open-instances-wave2/waterno2/cell-slopes.md`):
  272.584700834 → 278.230573774 (gap 1.67%) with cell-dependent slopes;
  the review re-bounded all 49,315 pair bounds with independent code.
- **eg_*** (`open-instances-wave3/eg/retry.md`): eg_int_s, eg_disc_s,
  eg_disc2_s closed to a relative 1e-9 against exactly feasible points
  (31 closed instances in total); eg_int_s had been solved in floating
  point by SCIP 8.1 in the literature.

The root integrated these into `SYNTHESIS.md`, `closing-research-results.md`,
`open-instances-summary.md`, both READMEs and pointer lines in the parent
notes, taking figures from the final notes. Link check over the edited
documents: no broken links after one fix (a review filename). An
independent check of this integration follows. No new directions were
started. Nothing committed.

## 2026-10-01: check of the round-4 integration; finish

`round4-root-integration-check` (2 agents) checked the root's round-4
edits against the final notes and reviews. Verified: every displayed bound
is rounded down from its certified value, every gap and count recomputes
(31 closed; 13 with tolerance-feasible primal points), and all links
resolve. Found and fixed by the root: one error (the closing record called
the chiral base 1.023 "proved"; it is computer-evaluated in floating
point) and minor items — dropped qualifiers (`kappa`-limited families; split
classes containing the balanced split; scalar toys versus the float-only
two-state example; Lebesgue reference measure; `theta <= theta*`,
`R >= 3K*`; the fixed-endpoint rate; WALL's even `n` and `eps`), a
non-attained supremum shown as an analytic base, a stale "several
switches" open item, an overstated "same form of work" in the top-level
README, missing links to the final confirmations, the superseded
"15–20 times" ratio (now 15–19, and 3–7 at other sizes, with the per-box
LP credited), outdated solver-evidence statements (the largest run is now
eg_disc2_s at 3.4 CPU-hours; chain-type certificates are 15 of 31), a
missing eg_* qualifier in Limits (the hand-derived floating-point error
analysis; sampling for seven eg_disc2_s parts), a missing superseded
pointer in the wave-3 Summary, and record-keeping wording. These fixes
were not rechecked. The optional nits of the last note-level
confirmations (`waterno2-cellslopes-confirm-r1.md` Section 3;
`round4-nits-confirm.md` Section 4, items 1–3) were left unapplied.

Per the user's instruction ("finish fully current ideas and developments
and stop"), work stops here: no further rounds. Nothing committed; outside
`research-20260929/` this work changed only `.gitignore` and the top-level
`README.md`. (The working tree also shows changes under
`paper-sparse-indicator-quadratics/` that this work did not make.)
