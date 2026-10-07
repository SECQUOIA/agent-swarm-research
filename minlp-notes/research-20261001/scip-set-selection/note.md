# Does a better choice of quadratic-free set make SCIP's intersection cuts pay off?

Stream `scip-set-selection`, research-20261001 (program:
[`../PROGRAM.md`](../PROGRAM.md)). Work began 2026-10-01 and continued
2026-10-02; analysis of the completed logs was finished on 2026-10-03.
A first author agent wrote the SCIP patch, the validation
scripts, ran the screening and the root benchmark, and was stopped by an
account usage limit at about 04:30 UTC on 2026-10-02 before writing a note.
This continuation re-checked that work, ran the remaining experiments and
wrote this note. The repository was swept into commits made outside this
program; this program makes no commits. **Final status (2026-10-04): reviewed in three rounds; r2 major timing issue
addressed by withdrawing the claims; independent [round 3](reviews/review-r3.md)
verified the r2 revision (N1 and N2); not refereed.** Its optional O1–O3
wording fixes are now applied and have not been re-reviewed. Review means a check by another
research agent, not journal peer review. Reviews:
[`round 1`](reviews/review-r1.md), [`round 2`](reviews/review-r2.md) and
[`round 3`](reviews/review-r3.md).

Code: [`code/`](code/). Raw outputs: [`logs/`](logs/). Patch:
[`patch/scip-10.0.3-setrule.patch`](patch/scip-10.0.3-setrule.patch).
Earlier notes cited: the sfree note
[`../../research-20260928b/sfree/optimal-intersection-cuts.md`](../../research-20260928b/sfree/optimal-intersection-cuts.md),
its reviews `../../research-20260928b/reviews/sfree-review.md` and
`sfree-recheck.md`, and the sibling stream
[`../scip-rule-fidelity/note.md`](../scip-rule-fidelity/note.md).

## Summary

**No-go for these two set-selection rules as a reason to enable SCIP's
quadratic intersection cuts, or as a clear improvement when the cuts are
enabled.** This is a recommendation from numerical evidence on the tested
SCIP 10.0.3 build, not a theorem about the best possible choice of `λ`.

At the root (Section 6), enabling cuts with SCIP's point rule raises mean
root gap closed by 0.10–0.11 over three seeds, with about 25% more root CPU
time. Searching `λ` to maximize the corner bound instead lowers mean RGC
by 0.007–0.010; searching for efficacy gives changes between −0.004 and
+0.003, with no consistent improvement. Across the 60 full-solve instances
and two seeds, the original patched `scip` / `corner` / `eff` solve
75 / 76 / 76 pairs: no clear improvement from searching. All three capture
added rows, which changes tree search even under the point rule.
Rule-vs-rule comparisons share that capture; `corner`/`eff` vs stock-off
comparisons include its effect.

The **stock point-rule rerun** (Section 7.4) solves 77 / 120,
against 75 / 120 off, with CPU shifted geometric means 15.962 vs 17.709 s.
Its extra pairs are `ex5_4_2`, seed 1 (off's LP numerical failure), and
`gabriel01`, seed 2. Excluding the failure leaves 76 vs 75 solved and
16.361 vs 17.277 s. On the 73 pairs solved by all five settings, stock has
CPU shifted geometric mean 1.926 s vs 2.148 s off and node shifted
geometric means 614.0 vs 616.8. Cross-batch timing is not comparable:
the rerun shows neither that enabling SCIP's own rule helps full solves
nor that it hurts them. The extra `gabriel01` completion is sensitive to
batch speed: its 256.83 s solve would take approximately 395 s at the
archived batch's speed, beyond the 300 s limit. The cleaner within-batch
timing comparison about enabling in this grid is the patched point
rule / off shifted CPU ratio of 1.103 on 68 pairs solved by off where stock and
patched point rules have matching node/LP signatures. It shows about 10%
CPU cost on that subset; it does not answer the full-solve enabling question.
Sections 7.1–7.2 also report a within-batch common-solved ratio of 1.0999
(p = 0.046), which includes capture-changed paths and points in the same direction.

The patched point rule solves 75 vs stock's 77, with CPU shifted geometric
means 17.979 vs 15.962 s. The CPU gap reflects batch speed: on 69 solved
pairs with matching node/LP signatures, patched/stock is 1.1544, whereas
the reviewer's same-load runs agree within ±3%. The differences attributable
to row capture are search-path differences: stock completes both `blend852`
seeds while patched times out, patched completes `tln7`, seed 1 while stock
times out, and five of the 74 pairs solved by both have changed final node/LP
signatures. These outcomes have different paths; their CPU timings also
include the batch-speed effect. The root statistics match wherever available (117
pairs with both first-LP and root dual values), supporting the root results.

Section 8 gives two reasons the single-cut theory does not predict this
result. In 82% of scanned root corners the floored corner criterion is
attained at a zero-cost ray, where it optimizes a surrogate rather than a
positive single-cut bound. Even on the mostly nondegenerate instances,
the corner rule lowers mean RGC by 0.018 (p = 0.008). The idea that it
favours directions the next LP does not use remains an untested heuristic
explanation; degeneracy alone does not explain the loss.

**Proved:** the sets accepted by the free-`λ` rules are S-free in exact
arithmetic (Section 2), and hence their mathematical intersection cuts are
valid. **Numerical evidence:** the dumped-corner checks support the C
formulas; the root and full-solve comparisons support the recommendation
above. The debug-solution runs are not a clean validity certificate
(Section 9): five runs report 73 intersection-row violations, all on
`st_glmp_fp2`, because the supplied solution omits SCIP's nonlinear
objective helper. Re-evaluating those rows with the correct helper value
leaves zero violations; all helper coefficients are positive and all reports
precede any incumbent. The supplied point has objective 7.6275 and is
not optimal (7.3445454180). The nine local secant-row reports are false
alarms: their node domains exclude the supplied `x2 = 5.65`.
No available debug, original or stock full-solve final dual bound
excludes the MINLPLib reference at the stated tolerance, but other debug
diagnostics remain unresolved. The `kall_congruentcircles_c52` discrepancy
is closed by SCIP's primal check: maximum constraint violation
9.51357·10^-7 is below 10^-6. The exact-arithmetic proof does not certify all floating-point
cuts or returned primal solutions.

**Not known:** whether a better search, another criterion or a larger set
family would help; whether longer solves, additional seeds (ordinary
seed-0 full solves are absent), strengthened full solves or a build with
Ipopt and PaPILO would change the result. Shared-machine load (12–200 in
the original runs; 5.319–125.853 in the stock rerun) can
distort CPU time through cache and memory contention as well as affect
which runs finish at the CPU limit. The timing rankings are
therefore provisional. An interleaved same-batch comparison of stock off
and stock scip on a quiet machine would answer the enabling question;
it is recommended, not run here. It would not by itself change the measured
root-bound and degeneracy results. Independent [round 3](reviews/review-r3.md)
verified this revision; the later optional O1–O3 wording edits are not re-reviewed.

---

## 1. Question and setting

SCIP 10.0.3 separates intersection cuts for nonconvex quadratic constraints
in `nlhdlr_quadratic.c` (Chmiela, Muñoz, Serrano, Math. Program. 197, 2023).
For each cut it uses one maximal quadratic-free set from the Muñoz–Serrano
family written in eigen-coordinates,
`C_λ = {s : φ_λ(ŷ(s)) ≤ λ^T x̂(s)}`, with the *point rule*
`λ = x̂(s̄)/‖x̂(s̄)‖`, where `s̄` is the LP solution. These cuts are off by
default (`nlhdlr/quadratic/useintersectioncuts = FALSE`,
`usestrengthening = FALSE`).

The sfree note showed that for a single cut the point rule can be
arbitrarily bad inside its own family (Proposition 6), that letting `λ`
vary reaches every maximal set in signatures `(n, 1)` and `(1, m)` under the
Lorentz orbit (Theorem 8), and that on McCormick LP corners a better set
closes more of the single-constraint gap after re-solving the LP (Section
9.2), while over several rounds the evidence was mixed (Section 9.3).

**Go/no-go question.** Inside SCIP 10.0.3, does a better choice of `λ`
make the quadratic intersection cuts worth enabling, or clearly better when
they are enabled?

## 2. Rules: design and justification

All set-selection rules keep SCIP's family `{C_λ : ‖λ‖ = 1}` in SCIP's
eigen-coordinates and select `λ` within it. The patched cut-on settings also
keep added cut rows alive for statistics; this changes tree search even
with rule 0 (Section 3). SCIP's `λ` is always evaluated first and kept unless a
rule improves its criterion by a relative margin of `10^-4`. Every rule
falls back to SCIP's `λ` if the cut computation for the chosen `λ` fails.

- **Rule 0 (`scip`)**: SCIP's point rule and cut formulas, with the patch's
  clocks and row capture. `stock-scip` in Section 7.4 is the unpatched rule.
- **Rule 1 (`corner`)**: maximize the single-cut corner bound
  `z_λ(w) = min_j w_j α_j(C_λ)` over unit `λ`, where `α_j` is the step
  length of ray `j` and `w_j` the reduced cost (dual value for slack rays)
  of the nonbasic variable of ray `j`, floored at `10^-6 max_j w_j`.
- **Rule 2 (`eff`)**: maximize the Euclidean efficacy of the cut in the
  space of LP columns. The cut is `Σ_j s_j/α_j ≥ 1` in the nonbasic
  variables `s_j` (violation 1 at `s̄`); its efficacy is `1/‖a(λ)‖`, where
  `a(λ) = Σ_j u_j/α_j(λ)` and `u_j` is the structural column vector of
  nonbasic `j` (a signed unit vector for a column, the signed row for a
  slack).

*Search.* When `dim λ = 2` (one positive eigenvalue plus the extra
coordinate of Cases 2 and 4, or two positive eigenvalues in Cases 1 and 3),
the search evaluates a grid of 24 angles on the half circle centred at
SCIP's `λ` and refines the best grid interval by golden-section search, up
to 48 evaluations per cut (`nlhdlr/quadratic/setrulemaxevals`). When
`dim λ > 2` it runs a projected subgradient ascent on the sphere (rule 1:
the minimum-norm element of the convex hull of the gradients of the nearly
active rays; rule 2: the gradient of `1/‖a‖`), with a line search along a
great circle. One evaluation costs `O(N)` closed-form step lengths (SCIP's
own root finder `computeIntersectionPoint`), plus `O(nnz)` for rule 2. When
`dim λ = 1` there is nothing to choose.

*Why these rules.*

1. Theorem 1 of the sfree note: for strictly positive reduced costs, the
   bound of one intersection cut from an S-free set `C` is
   `z_C(w) = min_j w_j α_j(C)`, and the best value over all S-free sets is
   the corner bound `z_K(w)`. Rule 1 is this criterion restricted to SCIP's
   family. Proposition 6 shows the restriction to the point rule loses up to
   a factor that tends to 0 inside the same family, so a free `λ` can only
   help the single-cut bound.
2. Theorem 8: with `λ` free, the orbit of the Muñoz–Serrano set under the
   automorphisms of the form reaches every maximal set in signatures
   `(n, 1)` and `(1, m)`. The patch does not search over transformations,
   only over `λ` in SCIP's fixed coordinates, so it searches a subfamily of
   the orbit. The offline test in Section 4.4 measures what is lost.
3. Theorems 4, 5 and 11: the corner minimizer uses at most `ρ(q)` rays
   (`ρ = 2` for bilinear terms) and `z_K` is computable cheaply; this is
   used here only in the validation (Section 4.1), to check `z_λ ≤ z_K` and
   to measure how close the searched `λ` gets to `z_K`.
4. Sections 8 and 9.2–9.3: the best-orbit set (bisection over 2×2 LMIs,
   candidate (iii) of the task) attains the **stored** `z_K` on all 120
   McCormick LP corners. Some stored values are wrong (Section 4.4 and
   `multiround/note.md`, Section 1.3), so this is not a verified claim
   about all true corner bounds. Its multi-round performance fell behind SCIP's rule on the
   larger instances, and the objective-parallel corner-optimal cut is much
   worse after re-solving the LP. This motivates the efficacy criterion
   (rule 2) as a second candidate: it rewards cuts that are deep in the
   structural space rather than along the objective.
5. Candidate (iii), the best orbit set by LMI bisection, was not implemented
   in SCIP. Each cut would need a sequence of small SDPs, and SCIP has no
   SDP solver in its quadratic handler. The offline test (Section 4.4)
   shows that the free-`λ` search inside SCIP's family already attains
   the stored `z_K` on 102 of 120 McCormick corners (the orbit on 120 of
   120; see the caveat on the stored `z_K` there), and
   that after re-solving the LP it is within 0.004 (4×4) and 0.017 (6×8) of
   the orbit set on average. An LP-gain criterion (re-solve the LP for each
   candidate) was not implemented because it costs one LP per evaluation.

*Validity of every rule.* Each `C_λ` with `s̄` in its interior is S-free,
so every rule produces valid cuts. Proof, for the four Chmiela cases (with
`q(s) = ‖x̂(s)‖² − ‖ŷ(s)‖²` in SCIP's coordinates, `S = {q ≤ 0}`):

- Cases 1–3 (no linear term outside the range of `Q`): SCIP writes
  `S = {‖x̂‖ ≤ ‖ŷ‖}` with `x̂ = x` or `(x, √κ)` and `ŷ = y` or `(y, √−κ)`.
  If `s ∈ int C_λ`, then `‖ŷ(s)‖ < λ^T x̂(s) ≤ ‖x̂(s)‖` (Cauchy–Schwarz,
  `‖λ‖ = 1`), so `q(s) > 0` and `s ∉ S`.
- Case 4 (a linear term `w` outside the range): SCIP uses
  `x̂ = (x, (w + κ + r)/(2√r))`, `ŷ = (y, (w + κ − r)/(2√r))`,
  `r = √(1 + κ²)`, so `‖x̂‖² − ‖ŷ‖² = q` and `x̂_last − ŷ_last = √r`. Then
  `S ⊆ S_≤0 = {‖x̂‖ ≤ ‖ŷ‖, a^T x̂ + d^T ŷ ≤ 0}` with `a = −e_last`,
  `d = e_last` (scaled), and SCIP's set is
  `C_λ = {max{β^T ŷ : ‖β‖ ≤ 1, β_last ≤ λ_last} ≤ λ^T x̂}`; the two pieces
  of SCIP's restriction to a ray are the two cases of this maximum
  (Muñoz–Serrano 2022, Remark 7). For `(x̂, ŷ) ∈ S_≤0` and `θ ≥ 0`, the
  proof of Muñoz–Serrano's Proposition 3 gives
  `λ^T(x̂ + aθ) ≤ ‖x̂ + aθ‖ ≤ ‖ŷ − dθ‖` (it uses only `‖λ‖ = 1`,
  `‖a‖ ≤ ‖d‖` and the two defining inequalities), so
  `inf_θ≥0 ‖ŷ − dθ‖ − λ^T a θ ≥ λ^T x̂`. If `λ ≠ −e_last` (equivalently
  `λ ≠ a/‖a‖`), the maximization over `{‖β‖ ≤ 1, β_last ≤ λ_last}` has a
  Slater point (`β = −t e_last` with `max(0, −λ_last) < t < 1`, which
  exists when `λ_last > −1`), so by
  strong duality the maximum equals that infimum and is `≥ λ^T x̂`: no point
  of `S` lies in `int C_λ`. Muñoz–Serrano state the proposition only for
  the point rule; the argument does not use the choice of `λ`. The sfree
  note (Section 8.1, family (B)) already treats every `λ` as admissible
  for bilinear terms. The excluded `λ = −e_last` is never accepted: the
  code accepts `λ` only if `‖ŷ(s̄)‖ < λ^T x̂(s̄)` (the upper bound `‖ŷ‖`
  for `φ_λ` gives `s̄ ∈ int C_λ`), and for `λ = −e_last` this would need
  `‖ŷ(s̄)‖ < −x̂_last(s̄)`, which is impossible because
  `‖ŷ‖ ≥ |ŷ_last| = |x̂_last − √r| ≥ √r − x̂_last > −x̂_last`.

**Status:** proved (the argument above, which restates Muñoz–Serrano's
proof for a general unit `λ`).

## 3. Implementation

Patch [`patch/scip-10.0.3-setrule.patch`](patch/scip-10.0.3-setrule.patch)
(1553 lines, only `scip/src/scip/nlhdlr_quadratic.c`; applies with
`patch -p1` to a fresh SCIP 10.0.3 suite tree, checked in Section 10). The
file `patch/nlhdlr_quadratic_setrule.patch` is the same diff with other
header timestamps.

New parameters (defaults use SCIP's point rule, with instrumentation):

| Parameter | Default | Meaning |
|---|---|---|
| `nlhdlr/quadratic/setrule` | 0 | 0 = SCIP's point rule, 1 = corner bound, 2 = efficacy |
| `nlhdlr/quadratic/setrulemaxevals` | 48 | evaluations of `λ` per cut |
| `nlhdlr/quadratic/dumpfile` | "" | append the corner data of every root cut as JSON (validation only) |

Code structure. `computeRestrictionToRay` gains an argument `lambda`
(NULL = SCIP's code path). With a `lambda`, it calls
`computeRestrictionToRayLambda`, which splits the restriction into a
`λ`-independent part per ray (computed once per cut) and a cheap
`λ`-dependent part (`buildLambdaCoefs`). `selectLambda` runs the search
in `generateIntercut` before the cut is computed; the cut itself and the
optional strengthening (`usestrengthening`) then use the chosen `λ` through
the same functions. Two SCIP features that depend on the apex of SCIP's set
are switched off when a different `λ` is used: monoidal strengthening
(`usemonoidal`, default on, applies in Case 2 with integer nonbasic
variables) and the minimal representation (`useminrep`, Case 2). In the
root benchmark SCIP's rule applied monoidal strengthening 608 times on 17
instances, rule 1 207 times on 16 instances.

Statistics. The table `nlhdlr_quadratic` gains a line `Quadratic SetSel`
with the number of searches, changed `λ`, fallbacks, evaluations, the mean
gain of the criterion on changed cuts, the time in `generateIntercut` and
in the search, and three counts obtained by capturing every added cut row:
cuts that were in at least one solved LP (`Applied`), cuts with a nonzero
dual value in some LP (`Active`), and root cuts that were in at least one
LP (`RootAppl`). The `Fallback` counter mixes two events: SCIP's own `λ`
fails the numerical checks before any search (then SCIP also aborts the
cut; in the root benchmark these are about as frequent as SCIP's
`AbrtBadRay` count), and the cut for a chosen `λ` fails so SCIP's `λ` is
used instead.

**Row capture changes tree search.** `SCIPcaptureRow` keeps each added row
alive until `nlhdlrExitQuadratic`. In SCIP 10.0.3, a dropped row is unlinked
from its columns only when `SCIProwFree` calls `rowUnlink`, so captured
rows remain linked after leaving the LP or cut pool. With cuts on, seed 0
and a 2000-node limit on `tln7`, the patched point rule gives dual bound
13.9974022605189, primal bound 17.1 and 5939 dual LPs / 27844 iterations;
stock SCIP gives 14.1602941176471, 16.1 and 5550 / 25644. The reviewer
repeated both paths and restored stock identity by removing only the capture
block. The separate stock relink here reproduces both paths
([`logs/check_stock_r1.log`](logs/check_stock_r1.log)). Rule-vs-rule
comparisons are among patched binaries with the same capture. Full-solve
comparisons of `corner` or `eff` with stock `off` include this capture effect.
Future full-solve instrumentation should count rows without keeping them
alive, for example by reading `SCIProwGetNLPsAfterCreation` in a row-deletion
event before release, or by disabling the applied-cut counters.

Build (no PaPILO, no Ipopt, LAPACK from the system; see Section 10 for the
exact commands). Without Ipopt, SCIP has no NLP solver: the NLP-based
primal heuristics do not run and the minor intersection cuts
(`sepa_interminor`) are not available. So the absolute times are not those
of a standard SCIP build; the comparisons between rules are on equal terms.
The unpatched binary used in Section 7.4 has the same build configuration.
With cuts off it matches two completed archived full solves (`nvs17`,
`st_glmp_fp2`, seed 1) and the `ex5_4_2`, seed-1 failure in LP 3040 at node
3643. Cut-on root runs match on all five newly checked instances
(`blend029`, `ex8_3_2`, `kall_circlespolygons_c1p11`, `st_e31`, `tln7`),
apart from timing. The review checked 13 root instances with the same result;
these checks support the root comparisons, not general tree-search identity.

## 4. Validation

### 4.1 Step lengths and S-freeness on dumped corners

With `nlhdlr/quadratic/dumpfile` set, the patched SCIP writes, for every
root cut, the quadratic data, SCIP's eigendecomposition, the LP point, the
rays, the reduced costs, SCIP's `λ`, the chosen `λ`, the step lengths the C
code computed for both, and the step lengths of the final cut
(`code/run_dumps.sh`: 12 instances, rules 1 and 2, root only;
`logs/dumps/*.jsonl.gz`). `code/check_dump.py` then, independently of the C
code:

1. rebuilds `q` from the dumped quadratic data and checks SCIP's
   decomposition `q = ‖x‖² − ‖y‖² (+ w) + κ` at random points;
2. evaluates `C_λ` from its definition (Muñoz–Serrano; for Case 4 the
   maximum over the cap `{‖β‖ ≤ 1, β_last ≤ λ_last}`, written out
   independently) and computes every step length by bisection on the
   membership function;
3. compares these with the C step lengths (search evaluation for SCIP's `λ`,
   for the chosen `λ`, and the final cut);
4. samples 30 directions × 4 points inside `C_λ` per corner and 12 points
   along every ray before its step, and counts points with `q < 0` (points
   of `int S` inside the set);
5. for corners with `ρ(q) ≤ 2` and at most 80 rays, or `ρ(q) ≤ 4` and at
   most 20 rays, computes `z_K` with the sfree code
   (`research-20260928b/sfree/code/core.py: corner_bound`, support
   enumeration up to `ρ(q)` rays, Theorem 4) and checks `z_λ ≤ z_K`
   (Theorem 1(2)); the reduced costs are floored at `10^-6 max_j w_j` as in
   rule 1.

Result (`logs/dumps/checks_summary.md`, from
`code/summarize_checks.py`), 1254 corners:

- decomposition error at most `9·10^-12` (relative);
- no sampled point of `int S` inside any `C_λ` and none along any ray
  (S-freeness, numerically, for both SCIP's and the chosen `λ`);
- C and reference step lengths agree to `10^-6` relative or better, with
  two kinds of exceptions: steps of order `10^5`–`10^11` in
  `crudeoil_pooling_ct2` (relative differences up to `10^-2`, but cut
  coefficients of order `10^-11`), and rays in `ex8_3_2` where SCIP's root
  finder returns a *shorter* step (conservative, Section 4.3);
- 21 C steps are longer than the reference step, all by at most
  `3.1·10^-7` relative, and `q` is still positive at every such C point
  (`code/overshoot_diag.py`), so no cut cuts off a point of `S` there;
- `z_λ ≤ z_K` on all 399 corners where `z_K` was computed and valid;
- the criterion value reported by the C search equals the Python value at
  the chosen `λ` (no mismatch).

**Status:** numerical evidence that the C restriction for a free `λ`
matches the definition of `C_λ` and that the sets are S-free; the
S-freeness itself is proved in Section 2.

### 4.2 A robustness problem in the sfree code (correction to earlier code)

Nine of the 408 `z_K` values computed with `core.corner_bound` were
spurious: the returned minimizer had `q = q(s̄) > 0`. In `ex5_2_5` the
returned "bound" was `3.05·10^-5 = 2^-15` on a two-ray face where `q` is
constant along one ray (both coefficients of `q` along the ray are below
`10^-15`) and the reduced costs are tiny (floored at `1.8·10^-5`). The
function `two_ray` maximizes `u₊(θ)` and returns `1/u₊` without checking
that the corresponding point is feasible, so rounding noise in the
quadratic coefficients, scaled by `1/w²`, produced a finite value. The
check now verifies the returned point and discards such values
(`zk_spurious` in the summary). This is a second instance of the
flaw that the sibling stream `scip-rule-fidelity` found independently
(its Section 7.1: antiparallel ray pairs make `a(θ)` and `bb(θ)` rounding
noise; 10 stored `z_K` values of the sfree note's Section 9.2 are wrong,
with corrected numbers given there). Here the trigger is a ray along which
`q` is constant, combined with tiny floored weights.

A second, smaller correction concerns the scout's reimplementation of
Chmiela's Case-4 set (`research-20260928b/sfree/code/scout_sfree.py:
ms_set`). It divides `x` and `y` by `√r`, `r = √(1 + κ²)`, which is not a
scaling of `q` when `κ ≠ 0`; sampling finds points of `int S` inside its
set (1460 of 25943 interior samples on 108 random corners of
`w − xy + c`, `c ∈ {±0.3, ±1, ±3}`; SCIP's own Case-4 formula: 0;
`code/check_scout_case4.py`, `logs/check_scout_case4.log`). The sfree
note's bilinear experiments use `q = ±(w − xy)` with constant 0
(`core.bilinear_quadratic`), so `κ = 0`, `r = 1`, and they are not affected.
I did not audit every scout script for Case-4 corners with `κ ≠ 0`.

### 4.3 SCIP's own root finder can halve a step (observation)

In `ex8_3_2` the final cut computed by SCIP's unchanged code path has step
`49.999999` on rays whose exact step is `99.99999991` (4 rays in each rule's
dump; 8 of 83057 final-cut rays across all dumps are shorter than 0.9 times
the exact step). The cause is in `computeRoot` of SCIP 10.0.3: when the
interval solution gives `φ > 10^-10` at the root, `doBinarySearch` bisects
`[0, root]` and stops at the first midpoint with `φ ≤ 0` and
`|φ| ≤ feastol`; when `φ` is small in absolute terms along the ray (here
`q(s̄) = 0.058`), the first midpoint already qualifies. The cut stays valid
but is weaker on those rays. It affects all rules equally (they all use
`computeIntersectionPoint`) and is rare in these dumps.

### 4.4 How good is the search, and how much does the family lose?

*Inside SCIP* (`code/search_optimality.py`: for rule-1 corners with
`dim λ = 2`, a scan of 720 angles on the full circle with golden-section
refinement, using the reference step lengths):

| dump | corners | C search within `10^-4` of the family optimum | mean ratio C / optimum (min) | SCIP's `λ` within `10^-4` | mean ratio SCIP / optimum |
|---|---|---|---|---|---|
| blend029 | 39 | 39 | 1.000 (0.99998) | 1 | 0.852 |
| crudeoil_pooling_ct2 | 27 | 16 | 0.858 (0.378) | 5 | 0.725 |
| ex8_3_2 | 11 | 5 | 0.894 (0.580) | 4 | 0.894 |
| st_e31 | 7 | 7 | 1.000 (0.999999) | 0 | 0.927 |
| waterund08 | 2 | 2 | 1.000 (0.99999999997) | 0 | 0.998 |
| kall_circlespolygons_c1p11 | 40 | 1 | 0.844 (0.402) | 1 | 0.844 |
| tln7 | 0 | — | — | — | — |

These are all seven archived `logs/dumps/search_opt_*.out` outputs.
`tln7` has no `dim λ = 2` corners; its script crashed while taking the
minimum of an empty array, so it has no search-optimality estimate.
On all six completed outputs the best angle was never outside the half
circle that the C search covers. The grid of 24 points misses narrow peaks
of the nonsmooth criterion on some corners. On `ex8_3_2` the mean ratios
are 0.8944348579 for the C search and 0.8939184782 for SCIP's `λ`:
both round to 0.894, so the average gain is only 0.0005163797.

*Offline, on the McCormick corners of the sfree note* (Section 9.2
generator, same seeds; `code/offline_constlambda.py`, run by the first
author agent; `logs/offline_constlambda_11.log`,
`logs/offline_constlambda_12_big.log`). Fractions of the single-constraint
gap:

| rule | 4×4, n = 47: corner / after LP re-solve | 6×8, n = 73: corner / after LP re-solve | reaches `z_K` |
|---|---|---|---|
| SCIP's `λ` | 0.700 / 0.895 | 0.591 / 0.870 | 4 / 47, 10 / 73 |
| free `λ`, max corner bound (`lamK`) | 0.753 / 0.924 | 0.640 / 0.890 | 41 / 47, 61 / 73 |
| free `λ`, max efficacy (`lamE`) | 0.706 / 0.905 | 0.597 / 0.877 | – |
| best orbit set (sfree note) | 0.755 / 0.929 | 0.648 / 0.907 | 47 / 47, 73 / 73 |

So inside SCIP's own family a free `λ` recovers most of the single-cut gain
of the orbit search on these corners (after re-solving: +0.029 / +0.020
against the orbit's +0.034 / +0.037 over SCIP's set). This is the evidence
behind not implementing the LMI-bisection rule. The scout's Case-4 problem
of Section 4.2 does not apply (`κ = 0`). Caveat: the "corner" columns and
the "reaches `z_K`" counts are measured against `core.corner_bound`, which
the sibling stream `scip-rule-fidelity` (its Section 7.1) showed to be wrong
on 10 of these 120 corners (antiparallel ray pairs in `two_ray`; corrected
means for SCIP's set 0.724 / 0.616 and for the orbit set 0.783 / 0.675).
The LP re-solve columns do not use `z_K` and are not affected; the
offline script was not rerun with a corrected `z_K`.

## 5. Benchmark design

*Candidates* (`code/candidates.py`, `logs/candidates.txt`): the 489
MINLPLib instances (OSiL files of the local cache) whose problem type
contains a quadratic part, that are not convex, not pure binary QPs, and
have at most 2000 variables and 4000 constraints (`sources/instancedata.csv`,
downloaded 2026-10-01).

*Screening* (`logs/screen/`, `logs/screen.json`): SCIP's rule, root node
only (`limits/nodes = 1`), 60 s CPU. The quadratic handler detected at
least one expression on 412 instances, generated at least one intersection
cut on 368, and on 347 at least one generated root cut entered an LP. These
347 form the root test set (`logs/testset_root.txt`). An earlier screening
with the first build (no LAPACK) generated no cut at all and was discarded,
as was its binary.

*Full-solve test set* (`code/select_fullset.py`, `logs/testset_full.txt`):
a random sample (seed 20261001) of 60 of the 260 root-test-set instances
that were not solved at the root and whose screening root took less than
30 s. The selection uses only SCIP's rule.

*Settings* (`code/run_bench.py`): `off` (SCIP default: no intersection
cuts), `scip` (cuts on, SCIP's rule), `corner` (rule 1), `eff` (rule 2), and
the same three with `usestrengthening = TRUE` (`scipS`, `cornerS`,
`effS`). All other parameters are SCIP defaults, including
`ncutslimitroot = 20` cuts per expression at the root and 2 per expression
at other nodes. Times are user CPU seconds (`timing/clocktype = 1`), because the
machine was shared (load average between 12 and 200 during the runs). Each
run writes one log with the full statistics; the parser is
`code/parse_logs.py`.

*Measures.* Root gap closed
`RGC = (db − z_LP1)/(z_ref − z_LP1)` (signs flipped for maximization),
with `db` the root "Final Dual Bound", `z_LP1` the first LP value of the
same run and `z_ref` the MINLPLib value (`=opt=` or `=best=`,
`sources/minlplib.solu`, downloaded 2026-10-01). Only instances whose root
finished in every compared setting without hitting the time limit are
compared (the "complete" instances), and only if `|z_ref − z_LP1| >
10^-6 max(1, |z_ref|)`. Paired differences are tested with the two-sided
Wilcoxon signed-rank test (zero differences dropped). For full solves:
solved count, shifted geometric means of CPU time (shift 1 s, unsolved runs
counted at the time limit) and of nodes (shift 100), per seed and over all
instance–seed pairs, and the same on the pairs solved by every setting.
All uncorrected p-values in Sections 6–8, including the 50% degeneracy
split in Section 8.2, are exploratory; no multiplicity adjustment was made.

## 6. Root results

Commands: `run_bench.py ../logs/root ../logs/testset_root.txt
off,scip,corner,eff,scipS,cornerS,effS 0 root 120 12` (2429 runs,
2026-10-02 00:29–01:26 local time) and `run_bench.py ../logs/rootseeds
../logs/testset_rootseeds.txt off,scip,corner,eff 1,2 root 120 10` (2440
runs, 19:11–19:37), on the 305 instances whose seed-0 root finished in all
seven settings (`code/select_rootseeds.py`). Analysis:
`code/root_analysis.py root.json rootseeds.json > logs/root_analysis.md`.
All runs ended with return code 0 and no error message.

**Validity screen.** No root dual bound exceeds the MINLPLib optimum by more
than `10^-6 max(1, |z_ref|)`, except one run: `tricp`, rule 2, seed 2, root
bound `1.7·10^-5` against the optimum 0 (objective values up to `6·10^7`).
Rerunning that exact run with the debug-solution build (MINLPLib solution
loaded, `logs/debugsol_tricp_eff_s2.log`) reproduces the bound, generates
160 intersection cuts (59 added, 13 in a root LP) and reports no row that
cuts off the solution (SCIP's check uses the absolute LP feasibility
tolerance). I read this as tolerance-level slack, not an invalid cut.

**Seed 0, all seven settings** (251 complete instances with a defined RGC):

| setting | mean RGC | median RGC | sgm root CPU s (shift 1) | cuts generated | cuts in a root LP | search time (s, total) | intersection-cut time (s, total) |
|---|---|---|---|---|---|---|---|
| off | 0.333 | 0.200 | 0.97 | 0 | 0 | 0 | 0 |
| scip | 0.447 | 0.409 | 1.20 | 95181 | 13113 | 0 | 167.6 |
| corner | 0.439 | 0.415 | 1.26 | 95657 | 12826 | 40.8 | 202.8 |
| eff | 0.448 | 0.417 | 1.23 | 95131 | 13216 | 43.9 | 205.1 |
| scipS | 0.453 | 0.417 | 1.52 | 91307 | 13168 | 0 | 665.7 |
| cornerS | 0.446 | 0.417 | 1.68 | 94886 | 13923 | 39.0 | 909.1 |
| effS | 0.453 | 0.422 | 1.60 | 91870 | 13439 | 42.7 | 845.8 |

Paired differences of RGC (X minus Y; "better"/"worse" by more than 0.01):

| X vs Y | seed | n | mean | X better | X worse | Wilcoxon p |
|---|---|---|---|---|---|---|
| scip vs off | 0 / 1 / 2 | 251 / 250 / 248 | +0.114 / +0.104 / +0.106 | 110 / 109 / 103 | 16 / 15 / 21 | 5e-17 / 4e-18 / 1e-15 |
| corner vs scip | 0 / 1 / 2 | 251 / 250 / 248 | −0.008 / −0.007 / −0.010 | 30 / 27 / 29 | 41 / 40 / 44 | 0.071 / 0.062 / 0.011 |
| eff vs scip | 0 / 1 / 2 | 251 / 250 / 248 | +0.001 / +0.003 / −0.004 | 33 / 31 / 27 | 33 / 30 / 39 | 0.996 / 0.43 / 0.11 |
| eff vs corner | 0 / 1 / 2 | 251 / 250 / 248 | +0.009 / +0.011 / +0.005 | 45 / 51 / 44 | 31 / 24 / 30 | 0.054 / 0.002 / 0.062 |
| scipS vs scip | 0 | 251 | +0.006 | 26 | 18 | 0.083 |
| cornerS vs scipS | 0 | 251 | −0.008 | 29 | 44 | 0.026 |
| effS vs scipS | 0 | 251 | −0.000 | 35 | 32 | 0.57 |

Seed noise (same setting, two permutation seeds, complete instances): the
RGC changes by more than 0.01 on 34–42 of about 266 instances with cuts off
and on 60–72 of about 250 with cuts on (mean absolute change 0.009 off,
0.013–0.024 on).

Findings (numerical evidence, on this test set and build):

1. Enabling the cuts with SCIP's rule raises the root bound: mean RGC
   +0.10 to +0.11, better on about 105 of 250 instances and worse on about
   17, consistently over three seeds. The median gain is small (+0.002 to
   +0.003): most of the mean comes from a minority of instances. The root
   costs about 25% more CPU time (shifted geometric mean 1.20 s against
   0.97 s).
2. **Rule 1 (corner bound) is slightly worse than SCIP's rule at the root**,
   in all three seeds (mean −0.007 to −0.010; worse on 40–44 instances,
   better on 27–30; p = 0.011 to 0.071). The per-instance differences are
   of the same size as the seed noise, so single instances say little; the
   sign is consistent.
3. **Rule 2 (efficacy) is indistinguishable from SCIP's rule** (mean
   between −0.004 and +0.003, p ≥ 0.1 in every seed) and slightly better
   than rule 1.
4. Strengthening (`usestrengthening`) adds little (+0.006, p = 0.08) and
   costs about 25% more root time; with it, rule 1 is again slightly worse
   than SCIP's rule (p = 0.026) and rule 2 equal. I therefore left the
   strengthened variants out of the full solves.
5. The search costs 40–50 s over the about 95000 cuts of the 251 instances
   (0.426 / 0.461 ms per **generated** cut, rule 1 / rule 2) and
   raises the time spent in intersection-cut generation by about 20–30%.
   Separately, over all seed-0 root logs, the rules change `λ` on
   173928 / 228135 searches (76.2%, rule 1) and 184473 / 233699
   (78.9%, rule 2). The median per-instance mean criterion gains are
   1.428× and 1.044× over the 267 instances with a change for each rule;
   these shares and medians are not restricted to the 251 RGC comparisons.
   On the same 251 instances, 40.77 / 43.87 s divided by 80350 / 79785
   searches gives 0.507 / 0.550 ms per search. The review's approximate
   0.18 ms divides this subset's time by all-root search counts and mixes
   populations; it is not a per-search cost for either population.

## 7. Full solves

The completed benchmark has 480 runs: four settings × 60 instances × seeds
1 and 2, at a 300 CPU-second limit. The archived launch command is
`run_bench.py ../logs/full ../logs/testset_full.txt off,scip,corner,eff 1,2
full 300 10`: ten concurrent SCIP processes, with `OMP_NUM_THREADS=1`
in each process, default sequential SCIP solving, a 6000 MB memory limit,
and a per-process wall timeout of 720 s. The full logs confirm the CPU
clock, limit and permutation seeds. The initial closeout only read logs;
the subsequent review revision adds the separate
120-run stock benchmark in Section 7.4. Analysis of the original benchmark:
[`code/full_analysis.py`](code/full_analysis.py),
[`logs/full_analysis.md`](logs/full_analysis.md), and unrounded records and
summaries in [`logs/full_analysis.json`](logs/full_analysis.json).

In Sections 7.1–7.3, `scip`, `corner` and `eff` all use the patched binary
and capture added rows. `off` has no rows to capture and is stock-equivalent
on the checked instances. Thus the original cut-on vs off comparisons
combine cuts and capture; they are not stock-SCIP comparisons. Rule-vs-rule
comparisons share the capture. Section 7.4 reports the stock rerun,
the cross-batch timing confound and the search-path differences from the
patched point rule.

### 7.1 Solved counts and shifted geometric means

An unsuccessful run, including an error, counts at 300 s in the CPU shifted
geometric mean.
The node shifted geometric mean uses the first number on SCIP's `Solving Nodes`
line (the node count of the last run after a restart), including truncated
search on time-limited runs. One error has no final node count; the node means
therefore use the same 59 pairs in seed 1 and 119 pairs overall for every
setting. They are measures of work performed before termination, not
estimates of nodes needed to solve the unsolved instances. On the subset
solved by every setting, all observations are complete. The shifts are
1 s for CPU time and 100 for nodes, as specified in Section 5.

| seed | setting | solved / runs | CPU sgm (s) | nodes sgm | all-settings-solved pairs | CPU sgm on those pairs (s) | nodes sgm on those pairs |
|---|---|---|---|---|---|---|---|
| 1 | off | 37 / 60 | 18.490 | 4739.2 | 36 | 2.170 | 617.6 |
| 1 | scip | 38 / 60 | 18.028 | 4609.9 | 36 | 2.537 | 624.7 |
| 1 | corner | 38 / 60 | 17.814 | 4563.0 | 36 | 2.554 | 627.6 |
| 1 | eff | 38 / 60 | 17.071 | 4280.1 | 36 | 2.366 | 572.3 |
| 2 | off | 38 / 60 | 16.959 | 4447.1 | 37 | 2.127 | 616.0 |
| 2 | scip | 37 / 60 | 17.930 | 4315.9 | 37 | 2.391 | 616.0 |
| 2 | corner | 38 / 60 | 16.815 | 3890.1 | 37 | 2.117 | 515.4 |
| 2 | eff | 38 / 60 | 17.260 | 3868.8 | 37 | 2.319 | 530.6 |
| 1 + 2 | off | 75 / 120 | 17.709 | 4589.6 | 73 | 2.148 | 616.8 |
| 1 + 2 | scip | 75 / 120 | 17.979 | 4459.3 | 73 | 2.462 | 620.3 |
| 1 + 2 | corner | 76 / 120 | 17.308 | 4210.6 | 73 | 2.325 | 568.4 |
| 1 + 2 | eff | 76 / 120 | 17.166 | 4067.6 | 73 | 2.342 | 550.8 |

Thus the searches solve one more instance–seed pair than either baseline,
and improve the all-pair CPU sgm by only 0.40–0.54 s against `off` and
0.67–0.81 s against `scip`. On the common solved subset, enabling cuts
increases CPU sgm: 2.148 s off, 2.462 s with SCIP's rule, and 2.325–2.342 s
with search. The searches use fewer nodes there, but that does not establish
a CPU improvement over cuts off.

### 7.2 Paired comparisons and seed variability

The ratios below are geometric means of `(X + shift)/(Y + shift)` over
the same pairs, so a ratio below 1 favours X. They are not ratios of the
shifted geometric means after subtracting the shift. CPU tests use paired
log ratios. For pooled tests, the two seed differences are first averaged
within an instance; 120 pairs are not treated as 120 independent instances.
On the common solved subset, 73 pairs represent 37 instances (36 with both
seeds). Wilcoxon tests are two-sided, drop zero differences, and are
exploratory, without correction for the multiple comparisons. The report
also gives comparisons on subsets solved by each pair of settings.

| X vs Y | all-pair CPU shifted ratio | Wilcoxon p (60 instance averages) | common-solved CPU shifted ratio | CPU p (37 instance averages) | common-solved node shifted ratio | nodes p (37 instance averages) |
|---|---|---|---|---|---|---|
| scip vs off | 1.0144 | 0.0402 | 1.0999 | 0.0460 | 1.0048 | 0.109 |
| corner vs off | 0.9786 | 0.376 | 1.0563 | 0.235 | 0.9325 | 0.968 |
| eff vs off | 0.9710 | 0.971 | 1.0618 | 0.815 | 0.9080 | 0.681 |
| corner vs scip | 0.9646 | 0.266 | 0.9604 | 0.288 | 0.9280 | 0.0941 |
| eff vs scip | 0.9571 | 0.579 | 0.9653 | 0.667 | 0.9036 | 0.132 |
| eff vs corner | 0.9922 | 0.944 | 1.0051 | 0.827 | 0.9737 | 0.966 |

No per-seed CPU comparison is significant at 0.05. The isolated node
signal for `eff` versus `scip` in seed 1 (common solved subset: ratio
0.9277, p = 0.0200) does not repeat in seed 2 (0.8808, p = 0.290) and
does not establish a general advantage. Exact paired solved-count tests
within each seed give p = 1 for every nonempty discordant comparison;
the counts differ by at most one. These small samples do not establish
equivalence either.

Same-setting variability between seeds is substantial relative to the
small between-rule changes. Among instances solved in both seeds:

| setting | instances | seed-2 / seed-1 CPU shifted ratio | CPU differs by a factor > 1.1 | seed-2 / seed-1 node shifted ratio | nodes differ by a factor > 1.1 |
|---|---|---|---|---|---|
| off | 37 | 0.9823 | 14 | 0.9516 | 19 |
| scip | 37 | 0.9901 | 14 | 1.0188 | 18 |
| corner | 38 | 0.9174 | 16 | 0.8853 | 19 |
| eff | 38 | 1.0166 | 16 | 0.9625 | 19 |

For example, `corner` versus `scip` on the common solved subset has CPU
ratios 1.0047 in seed 1 and 0.9192 in seed 2. `off` solves one instance
only in seed 2, `scip` one only in seed 1, and the solved sets of each
search rule are the same in both seeds. Seed effects here are mixed with
differences in machine load and cannot be isolated as pure randomization
effects.

### 7.3 Errors, reference values and limits

There are 302 reported optimal completions, 177 time limits, and one
failure: `ex5_4_2.off.s1`, return code 255, unresolved numerical trouble
in LP 3040 at node 3643. It has no final statistics and is counted as
unsolved, at 300 s. Every other full run returns 0 and has no error
message. Excluding that pair from all settings changes the solved counts
to 75 / 74 / 75 / 75 and CPU sgms to 17.277 / 18.443 / 17.751 / 17.603 s
(`off` / `scip` / `corner` / `eff`). The small search advantage over `off`
in the headline mean disappears: it depends on penalizing this baseline
failure. The searches' only additional solved pair over `off` is exactly
`ex5_4_2`, seed 1. Against `scip`, both searches solve `blend852` in both
seeds where `scip` times out, but fail on `tln7`, seed 1, where `scip`
succeeds. The advantage over `scip` remains small.

No final dual bound excludes the MINLPLib feasible reference by more than
`10^-6 max(1, |z_ref|)`, with objective sense accounted for. One reported
optimum fails the corresponding two-sided check against an `=opt=` value:
`kall_congruentcircles_c52.eff.s2` returns 1.5371086884193 against
1.537110798, a difference of −2.1095807·10^-6 (relative 1.3724·10^-6).
This is a small value discrepancy, not evidence of an invalid dual bound;
no optimum discrepancy exceeds `10^-4 max(1, |z_ref|)`. The review rerun
reproduces exactly 3830 nodes and objective 1.5371086884193. SCIP's
`checksol` accepts the solution in the original problem: maximum constraint
violation 9.51357·10^-7 < 10^-6, LP-row violation 1.34291·10^-8 and bound
violation 9.73643·10^-10
([`reviews/r1-logs/kall_c52.eff.s2.log`](reviews/r1-logs/kall_c52.eff.s2.log)).
This closes the discrepancy as tolerance-level infeasibility accepted by
SCIP, not an intersection-cut validity problem. Excluding both seeds of this instance
gives counts 73 / 73 / 74 / 74 and CPU sgms 18.372 / 18.597 / 17.963 /
17.670 s, leaving the qualitative comparison unchanged. Debug-solution
diagnostics are reported separately in Section 9.

**Status: numerical evidence on this test set and build.** Neither search
rule clearly improves full solves, and neither makes a convincing case
for enabling the cuts on this patched build. The original patched point
rule solves as many pairs as off; that observation does not answer the
stock-SCIP question. This is not a proof that set selection cannot help:
the sample is 60 instances selected through SCIP's screening rule, the
limit is short, there are only two full-solve seeds, and the build omits
Ipopt and PaPILO. Ordinary full solves with seed 0 are absent from the
archived benchmark; the seed-0 debug-solution runs use different heuristics,
symmetry settings, a different build and a 30 s limit, so cannot fill that
gap. Strengthened variants have no full-solve comparison.

CPU timing under shared load 12–200 still changes with cache and memory
contention; CPU clocking removes scheduling delays, not those effects.
Consequently the few-percent timing rankings, and CPU-limit completions,
are sensitive to uncontrolled load. The 300 debug-solution runs started
at 20:10 on October 2, during the full benchmark (19:37 to 21:35 by the
archived log modification times),
and added load. Jobs were ordered by instance, keeping
its settings close together in time, which mitigates within-batch load
differences. Median wall/CPU ratios for full runs
above 5 CPU s were 1.221 / 1.205 / 1.213 / 1.205 for
`off` / `scip` / `corner` / `eff`; these measure scheduling delay, not CPU
inflation, and do not establish comparable CPU speed (Section 7.4).
A quiet-machine rerun with matched
settings and seeds would be needed before claiming a timing advantage or
changing the recommendation on timing grounds. It was not run here. The
root-bound and degeneracy findings in Sections 6 and 8 already give no
support for these selection rules independently of such a rerun.

### 7.4 Stock point-rule rerun after review

The stock binary is
`/workspace/local-home/build-scip/selection/revision-r1-stock/scip-stock`. It replaces
only the benchmark executable's patched quadratic-handler object with the
pristine SCIP 10.0.3 object, using the benchmark compile and link commands.
Recompiling the patched handler with those flags gives a byte-identical
benchmark object; LAPACK and the other linked libraries match
([`logs/build_stock_r1.log`](logs/build_stock_r1.log)). Existing builds
were left untouched. The off/root checks and `tln7` tree divergence are
reported in Section 3.

The rerun uses the same 60-instance list, seeds 1 and 2, 300 CPU-second
limit, CPU clock type 1, 6000 MB memory limit and cut settings as
`logs/full/`, with at most eight solver processes and `OMP_NUM_THREADS=1`.
[`code/run_stock_r1.py`](code/run_stock_r1.py) reuses `run_bench.command`,
wraps each solver in GNU `timeout`, writes a separate partial log, and
atomically renames completed logs in [`logs/full_stock/`](logs/full_stock/).
It records load every 30 seconds and each completion in
[`logs/full_stock/driver.jsonl`](logs/full_stock/driver.jsonl).

The complete grid has **120 valid runs: 77 optimal, 43 CPU time limits,
all return code 0 and no errors**. The first pass finished at
2026-10-04 03:20:59 UTC with 112 valid runs and eight wall timeouts.
Only those eight were retried, with an 1800-second wall guard; all retries
returned 0. The original attempts remain in `logs/full_stock/attempts/`
and are excluded from the measures below. The final driver finished at
03:28:45 UTC. The complete work ran on October 3, 22:36–23:28 local time.

Shared-machine one-minute load ranged from 5.31884765625 to
125.85302734375, with nearly 10 GiB of swap observed during the early
spike. SCIP's CPU clock type 1 counts user CPU (`tms_utime` in `clock.c`),
so kernel time and swap stalls can exhaust a wall guard before that limit.
The stock runs above 5 CPU s have median wall/CPU ratio
1.2046666667, close to the archived settings' approximately 1.2. This does
not establish comparable CPU speed: wall/CPU measures scheduling delay,
while cache and memory contention can inflate user CPU time on the same path.
Resource observations and concurrent process snapshots are in
[`logs/stock_resource_observations_r1.md`](logs/stock_resource_observations_r1.md)
and [`logs/stock_load_processes_r1.txt`](logs/stock_load_processes_r1.txt).

Analysis: [`code/stock_analysis_r1.py`](code/stock_analysis_r1.py),
[`logs/stock_analysis_r1.md`](logs/stock_analysis_r1.md) and unrounded
[`logs/stock_analysis_r1.json`](logs/stock_analysis_r1.json).
CPU shifted geometric means penalize every unsuccessful run at 300 s,
with shift 1 s.
Node shifted geometric means use the first number on SCIP's `Solving Nodes`
line (the node count of the last run after a restart), shift 100 and the
same 59 / 60 / 119 pairs in seed 1 / seed 2 / pooled, because off's
numerical failure lacks statistics.
The common-solved subset uses all five settings, including `corner` and
`eff`, and remains 36 / 37 / 73 pairs. Its observations are complete;
all-pair nodes include truncated work and do not estimate solution effort.
Using total nodes over restarts changes the displayed node shifted geometric
means in Sections 7.1 and 7.4 by at most 0.5 at table precision (for example,
off seed 1: 4739.2 → 4739.4); the tables retain the last-run definition.

| seed | setting | solved / runs | CPU sgm (s) | nodes sgm | common-solved pairs | CPU sgm there (s) | nodes sgm there |
|---|---|---|---|---|---|---|---|
| 1 | off | 37 / 60 | 18.490 | 4739.2 | 36 | 2.170 | 617.6 |
| 1 | stock-scip | 38 / 60 | 16.066 | 5444.3 | 36 | 1.992 | 623.5 |
| 1 | patched-scip | 38 / 60 | 18.028 | 4609.9 | 36 | 2.537 | 624.7 |
| 2 | off | 38 / 60 | 16.959 | 4447.1 | 37 | 2.127 | 616.0 |
| 2 | stock-scip | 39 / 60 | 15.858 | 5057.4 | 37 | 1.864 | 604.8 |
| 2 | patched-scip | 37 / 60 | 17.930 | 4315.9 | 37 | 2.391 | 616.0 |
| 1 + 2 | off | 75 / 120 | 17.709 | 4589.6 | 73 | 2.148 | 616.8 |
| 1 + 2 | stock-scip | 77 / 120 | 15.962 | 5245.7 | 73 | 1.926 | 614.0 |
| 1 + 2 | patched-scip | 75 / 120 | 17.979 | 4459.3 | 73 | 2.462 | 620.3 |

Pooled paired ratios, defined as in Section 7.2. All CPU ratios in this
table compare different batches and cannot measure the effect of cuts or
capture. Tests average seed log ratios within an instance; p-values are
exploratory and uncorrected and do not remove the batch confound.

| X vs Y | all-pair CPU shifted ratio | CPU p (60 instances) | common-solved CPU shifted ratio | CPU p (37 instances) | common-solved node shifted ratio | node p |
|---|---|---|---|---|---|---|
| stock-scip vs off | 0.9066 | 0.003315 | 0.9296 | 0.007924 | 0.9960 | 0.1207 |
| patched-scip vs stock-scip | 1.1189 | 1.666e-7 | 1.1832 | 2.355e-7 | 1.0088 | — |

The node test for patched vs stock is not reported because fewer than ten
instance-averaged differences are nonzero, as in the original analysis's
test policy. Pair-solved subsets are also in the report: stock vs off has
75 pairs, CPU ratio 0.9236 (p = 0.005131) and node ratio 1.0034
(p = 0.09022); patched vs stock has 74 pairs, CPU ratio 1.1807
(p = 2.355e-7) and node ratio 1.0087.

**Stock point rule vs off: cross-batch outcomes.** Stock alone
solves `ex5_4_2`, seed 1 (off's LP numerical failure), and `gabriel01`,
seed 2; off solves no pair that stock fails to solve. Excluding the failure
from both leaves 76 / 119 vs 75 / 119 solved, CPU shifted geometric means
16.361 vs 17.277 s and CPU shifted ratio 0.9499 (p = 0.003473).
The `gabriel01`, seed-2 completion at 256.83 CPU s and 97603 nodes is
sensitive to batch speed. Stock and patched share their first 103 display
rows through node 6600 except for the time and memory columns (memory
differs from the first row); this prefix takes 29.0 vs 44.6 CPU s. Applying
that observed speed ratio to stock's solve gives
`256.83 × 44.6 / 29.0 ≈ 395 s`, beyond the archived 300 s limit. This is
an estimate from the shared prefix, not a replay of the complete stock path.
After setting aside off's numerical failure and this load-sensitive
completion, no solved-count difference attributable to cuts remains.
Cross-batch timing is not comparable. The stock rerun shows neither that
enabling SCIP's own rule helps full solves nor that it hurts them.

**Batch speed and the within-batch timing evidence.** On 69 pairs solved
by both point rules with matching final node and primal/dual LP counts,
the patched/stock shifted CPU ratio is 1.1544. Splitting by stock CPU time:

| stock CPU time | pairs | patched/stock shifted CPU ratio |
|---|---|---|
| < 1 s | 41 | 1.0398 |
| 1–10 s | 19 | 1.3033 |
| ≥ 10 s | 9 | 1.4384 |

The reviewer ran four seed-1 instances under the same load, with four
concurrent processes per instance: `{patched, stock} × {off, scip}`.
All 16 runs reproduce the archived node counts. Patched/stock CPU ratios
are 0.996–1.022 with cuts on and 0.97–0.99 with cuts off, within ±3%.
These checks show no measurable capture cost on these matching paths.
The archived batch is slower even with cuts off, where no rows are captured:

| instance | archived off CPU (s) | same-load stock off CPU (s) | archived/same-load ratio |
|---|---|---|---|
| kall_diffcircles_5b | 5.61 | 3.96 | 1.42 |
| nvs24 | 10.87 | 7.44 | 1.46 |
| crudeoil_pooling_ct2 | 26.34 | 19.03 | 1.38 |
| pointpack08 | 52.49 | 32.98 | 1.59 |

On the 68 matching stock/patched-path pairs that off also solves, the
cross-batch stock/off shifted CPU ratio is 0.9535 (0.954 rounded), but
the within-batch patched/off ratio is 1.1029 (1.103 rounded). This is the
cleaner within-batch timing comparison about enabling in this grid: cuts cost
about 10% CPU on this selected solved subset. The matching paths are
those of stock and patched with cuts on; off need not follow the same path.
The ratio includes the patched instrumentation, whose CPU cost is not
measurable in the four same-load checks. It does not establish an effect
on full solves across the whole test set or on paths changed by capture.
The common-solved comparison in Sections 7.1–7.2 also runs within the
archived batch (ratio 1.0999, p = 0.046), but includes capture-changed paths;
both comparisons point in the same direction.
The cross-batch apparent 5% saving and the 12–18% patched/stock CPU gap
reflect batch speed, not a demonstrated benefit of cuts or CPU cost of
row capture.

Evidence: [`reviews/r2-logs/batch_effect.log`](reviews/r2-logs/batch_effect.log),
[`same-load runs`](reviews/r2-logs/sameload/),
[`same-load summary`](reviews/r2-logs/sameload_summary.log) and
[`path prefixes`](reviews/r2-logs/path_prefix.log). The independent
raw-log recheck for this revision is [`logs/audit_revision_r2.log`](logs/audit_revision_r2.log).

**Patched point rule vs stock: search-path differences from row capture.**
Stock alone solves `blend852` in both seeds (172.64 / 172.68 CPU s,
84509 / 96144 nodes) and `gabriel01`, seed 2. Patched alone solves
`tln7`, seed 1 (283.04 CPU s, 308290 nodes); stock times out there at
584309 nodes. The total count is two fewer solved pairs with the patch,
but it includes the load-sensitive `gabriel01` completion. Only the two
`blend852` outcomes and the one `tln7` outcome are attributed to changed
search paths; their CPU times also include batch speed.
Five of the 74 pairs solved by both have different final node/LP
signatures: `blend531`, seed 2; `carton9`, both seeds; and
`edgecross14-039`, both seeds. Overall signatures differ on 51 / 120
pairs, but that count includes time-limited work affected by load and is
not a count of divergences caused purely by capture. First-LP and root
dual values have no differences; both values are available on 117 pairs.
No stock final dual bound excludes the MINLPLib reference; the stock
reference-value audit reports no flags at the Section 7.3 tolerance.

The no-go recommendation for the two new rules remains: the root results
and the comparisons among patched rules show no clear gain from either
search. The stock rerun does not answer whether enabling the existing
point rule helps full solves. `corner` / `eff` still solve 76 / 120
with CPU shifted geometric means 17.308 / 17.166 s, but their comparisons
with stock-off or stock-scip retain the capture confound and cannot isolate
set selection.

**Limits and recommended follow-up.** Stock-scip has no row capture, but
its comparison with archived off does not control batch speed. The
`corner`/`eff` comparisons with stock-off still mix set selection and capture.
Run stock off and stock scip interleaved in the same batch on a quiet
machine, with matched instances, seeds and limits, to answer the enabling
question. With cuts off either binary is equivalent on the checked paths;
using stock for both settings avoids capture. This is a recommended
follow-up; no new benchmark was run in this revision.
No capture-free full solve of `corner` or `eff` was run;
their tree-search ranking without this instrumentation remains untested.
Root identity is checked on a finite sample, not proved
for every instance. No quiet-machine timing comparison is available.

## 8. What the single-cut criterion sees at SCIP's root

The rules change `λ` on most cuts and raise their own criterion (rule 1:
median gain 1.05–1.65 on the dumps where it changed `λ`; mean `z_λ/z_K`
from 0.74 to 0.85 on `blend029`), yet the root bound does not improve. Two
observations explain part of this.

### 8.1 SCIP's root corners are mostly dual degenerate

Theorem 1 of the sfree note equates the best single-cut bound with `z_K(w)`
only for strictly positive reduced costs `w`; Proposition 2 there shows the
equality can fail otherwise. At SCIP's root LPs, after the first rounds of
cuts, many reduced costs are zero. In the rule-1 dumps
(`code/degeneracy.py`, `logs/dumps/degeneracy.md`, SCIP's `λ`):

| dump | corners | mean share of rays with zero reduced cost | corners with every ray at zero cost | corners whose criterion `min_j w̃_j α_j` is attained at a zero-cost ray |
|---|---|---|---|---|
| blend029 | 182 | 0.07 | 0 | 158 |
| crudeoil_pooling_ct2 | 944 | 0.41 | 0 | 754 |
| ex5_2_5 | 136 | 0.80 | 0 | 136 |
| ex8_3_2 | 428 | 0.99 | 129 | 428 |
| kall_circlespolygons_c1p11 | 331 | 1.00 | 331 | 331 |
| nvs17 | 80 | 0.00 | 0 | 0 |
| pointpack08 | 555 | 0.36 | 0 | 457 |
| qp3 | 20 | 0.02 | 0 | 5 |
| st_e31 | 56 | 0.97 | 0 | 56 |
| st_qpk3 | 20 | 0.00 | 0 | 0 |
| tln7 | 107 | 0.54 | 0 | 107 |
| waterund08 | 268 | 0.45 | 1 | 267 |
| total | 3127 | | 461 | 2699 |

(`w̃` = reduced costs floored at `10^-6 max_j w_j`; "zero" means
`w_j ≤ 10^-9 max_j w_j`.) A per-instance scan of all 305 root instances
(`code/degeneracy_scan.py`, SCIP's rule, seed 0, root only; dumps deleted
after summarizing; `logs/degeneracy_root.jsonl`) gives the same picture:
over 109389 root corners, 82% have the criterion attained at a zero-cost
ray and 9% have every reduced cost zero (per instance: median share of
zero-cost rays 0.11, median share of corners with the criterion at a
zero-cost ray 0.72).

For such a corner the true single-cut bound `min_j w_j α_j` of SCIP's set
is 0, and so is that of every set that a zero-cost ray leaves at a finite
step: the point `x̄ + α_j r_j` of a zero-cost ray `j` satisfies the cut
with equality and has the LP value of `x̄`, so one cut alone does not raise
the corner bound. Rule 1 then maximizes a surrogate set by the floor
(roughly, the shortest step among the zero-cost rays). Theorem 1 does not
identify this surrogate with a positive bound. Lengthening zero-cost steps
can still be a first step toward one: every zero-cost ray must have an
infinite step for a positive single-cut bound. When every reduced cost is
zero, the floor is `10^-15`; for shortest steps below about `10^3`, the
criterion is below `10^-12` and the absolute acceptance threshold can
prevent a change. The exact test is
`critbest > crit0·(1 + 10^-4) + 10^-12`. On the fully degenerate
`kall_circlespolygons_c1p11` dumps it keeps SCIP's `λ`; a full-circle scan finds
`λ` up to 2.5 times better in the floored criterion (mean ratio 0.844 for
SCIP's `λ`, which is also the C choice). This acceptance behaviour was not
designed; it acts as the "keep SCIP's rule" fallback in the fully
degenerate cases observed here. The sibling
[`scip-rule-fidelity` note](../scip-rule-fidelity/note.md) reports 73% of
sampled MINLPLib corners with `z_K = 0`. Its test of whether a zero-cost
face meets `S` differs from this scan's floored-criterion
minimizer at a zero-cost ray (81.6%, rounded to 82%); the samples also differ.

### 8.2 Where the criterion is meaningful, maximizing it hurts

If degeneracy were the whole story, rule 1 should help where the corners
are nondegenerate. It does the opposite (`code/degeneracy_vs_root.py`,
`logs/degeneracy_vs_root.md`; RGC differences averaged over seeds 0, 1, 2;
248 instances with complete roots in all three seeds):

| instances | n | mean D(corner, scip) | corner better / worse by > 0.01 | Wilcoxon p | mean D(eff, scip) | eff better / worse | Wilcoxon p |
|---|---|---|---|---|---|---|---|
| criterion at a zero-cost ray in < 50% of corners (mostly nondegenerate) | 97 | −0.018 | 13 / 26 | 0.008 | −0.003 | 16 / 21 | 0.36 |
| criterion at a zero-cost ray in ≥ 50% of corners | 151 | −0.002 | 9 / 20 | 0.086 | +0.002 | 11 / 12 | 0.46 |
| all | 248 | −0.009 | 22 / 46 | 0.002 | +0.000 | 27 / 33 | 0.85 |

Spearman correlations over the 248 instances: the share of corners with
the criterion at a zero-cost ray correlates with D(corner, scip) at
`ρ = +0.145` (p = 0.022), with D(eff, scip) at `+0.031` (p = 0.62), and
with the gain of SCIP's cuts over no cuts, D(scip, off), at `ρ = −0.509`
(p = `9·10^-18`).

So (numerical evidence on this test set):

1. Averaged over three seeds, rule 1 is worse than SCIP's rule at the root
   (mean −0.009, worse on 46 and better on 22 instances, p = 0.002).
2. The loss is concentrated on the instances where the corner criterion is
   mostly set by positive reduced costs, i.e. where rule 1 does what
   Theorem 1 suggests (−0.018, p = 0.008). On the degenerate instances it
   mostly optimizes the floor surrogate or keeps SCIP's `λ`, and the effect
   is small.
3. Intersection cuts in general help less on degenerate instances
   (`ρ = −0.51` with the gain over no cuts).

The single-cut corner bound is therefore a poor guide for SCIP's
multi-round root separation even when it is well defined. This matches the
sfree note's Sections 9.2–9.3: the objective-parallel corner-optimal cut is
worse after re-solving the LP than tilted cuts, and choosing the
bound-optimal set in every round fell behind SCIP's rule over 10 rounds on
the 6×8 instances. A plausible mechanism, not tested here, is that the
criterion favours sets that are long in the cheap directions of the current
objective and short elsewhere, which cuts deep where the next LP will not
go. A degeneracy-aware variant (rule 1 only when SCIP's criterion is set
by a positive reduced cost) was written but not built or run: by item 2 it
would act mainly on the instances where rule 1 loses.

## 9. Debug-solution checks and their limits

[`code/debugsol_analysis.py`](code/debugsol_analysis.py) audits the
completed runs, counts explicit row-violation messages, checks final and
root dual bounds against the MINLPLib values, and re-evaluates the reported
intersection rows described below. Results and per-run diagnostics:
[`logs/debugsol_analysis.md`](logs/debugsol_analysis.md) and
[`logs/debugsol_analysis.json`](logs/debugsol_analysis.json). It does not
use the parser's broad `debugsol_violation` flag as a row count: that flag
also matches other debugging diagnostics in the same log.

### 9.1 The 300 runs with symmetry disabled

`logs/debugsol/` contains the complete grid of five settings
(`scip`, `corner`, `eff`, `cornerS`, `effS`) × 60 instances × seed 0,
plus six runner logs, which are not solver runs. Each solver run has a
30 CPU-second limit, the debug-solution build, primal heuristics switched
off, and `misc/usesymmetry = 0`. There are 170 reported optimal
completions, 129 time limits, and one LP numerical failure
(`ex5_4_2.eff.s0`, return code 255, unresolved numerical trouble in
LP 4218 at node 6384); the other 299 return 0.

The answer to "did any run report a cut cutting off the known solution?"
is **yes in the raw diagnostics**: five runs report intersection rows,
and the same five report other rows. All are `st_glmp_fp2`:

| setting | intersection-row messages | other-row messages | final / root dual bounds excluding the MINLPLib reference (runs) |
|---|---|---|---|
| scip | 17 | 3 | 0 / 0 |
| corner | 19 | 2 | 0 / 0 |
| eff | 9 | 1 | 0 / 0 |
| cornerS | 19 | 2 | 0 / 0 |
| effS | 9 | 1 | 0 / 0 |
| total | 73 | 9 | 0 / 0 |

Counts are diagnostic messages, including repeated messages, not a claim
that every printed row is distinct. Across all 300 runs, zero of 299
available final dual bounds and zero of 286 available root dual bounds
exclude the MINLPLib feasible reference at `10^-6 max(1, |z_ref|)`. The failed run has
no final statistics. There are 45 runs with at least one `ERROR`
diagnostic; a return code of 0 does not mean the checker found no problem.

**Objective mapping problem, established from logs and reader code.**
The solution files use the name `objvar`. SCIP's OSiL reader instead
creates `nlobjvar` for the nonlinear part of the objective and
`objconstvar` for a nonzero objective constant. `debug.c` ignores names
not in the problem, assigns zero to missing original variables, and
computes its reference objective from the supplied linear objective
coefficients. An unknown-variable warning appears in 215 of 300 runs;
such a warning alone does not prove the point is wrong, since a redundant
`objvar` can be ignored harmlessly on a purely linear objective.

On `st_glmp_fp2`, the objective is `x3*x4`; the provided solution has
`x3 = 5.65`, `x4 = 1.35`, so `nlobjvar` must be 7.6275. The log instead
shows `<t_nlobjvar>[0]` in every reported intersection row. The supplied
point is therefore infeasible in SCIP's extended model even though its
original-variable coordinates are those of the MINLPLib solution. Using
the printed row coefficient to replace 0 by 7.6275, **all 73 reported
intersection rows satisfy that solution**. Their smallest slack is
0.0175438188008, well above the logged LP feasibility tolerance 10^-6.
The supplied point is feasible in the original OSiL constraints but is
not optimal: its objective is 7.6275, while `.solu` reports
7.3445454180. All 73 rows have a **positive** helper coefficient and were
reported before any incumbent existed. Thus every feasible helper value
`≥ x3*x4` at this point also satisfies these rows. The objective-helper
correction is right and hides no invalid cut among the reported rows.
This is an offline re-evaluation, not a certificate for all generated rows.
The nine `overestimate_pow` messages are local secants for `x2²` at nodes
with `x2` near 6.45. In the point-rule logs the secant domains are approximately
[6.4508, 6.4553] and [6.4539, 6.4544]. Across all five settings there
are five distinct printed secants, with domains contained in
[6.3413, 6.4806], as recovered from their coefficients
([`logs/audit_revision_r1.json`](logs/audit_revision_r1.json)). All exclude the supplied
`x2 = 5.65`. These checker false alarms are resolved; the preceding
local-bound implication errors arise from the infeasible debug point.

The checker also prints 114699 global objective-bound warnings in 25
runs: all five settings on each of `ex5_2_5`, `gasprod_sarawak01`,
`nvs17`, `nvs24`, and `st_glmp_fp2`. Its loaded objective is wrong on
all five instances. Direct evaluation of the OSiL objective at the supplied
solution gives these missing contributions:

| instance | loaded linear objective part | missing quadratic part / constant | actual supplied-solution objective |
|---|---|---|---|
| ex5_2_5 | −8699.9999995406 | 5199.9999993339 / 0 | −3500.0000002067 |
| gasprod_sarawak01 | −45620.39190921 | 0 / 14104.987000025 | −31515.404909186 |
| nvs17 | −2220.4 | 1120 / 0 | −1100.4 |
| nvs24 | −2036.2 | 1003 / 0 | −1033.2 |
| st_glmp_fp2 | 0 | 7.6275 / 0 | 7.6275 |

These warning objectives differ from both the correctly evaluated supplied
solutions and, where the supplied solution is not optimal, the `.solu`
optimum. They cannot be counted as invalid original-objective dual bounds.
The final and root statistics are checked against `.solu` separately.
Additional variable-bound, local-bound, implication and node-cutoff
diagnostics, including on `carton9`, `genpooling_lee2`, `ndcc16persp`,
`pooling_foulds5pq`, `pooling_rt2pq` and `qp3`, are listed in the report.
Their causes were not all resolved; they are not evidence specific to the
new `λ` rules, since several also occur with SCIP's point rule.

Three reported optima on `kall_congruentcircles_c52` fail the two-sided
10^-6 check: `scip` returns 1.53710899052844, and `corner` and `cornerS`
return 1.53710865152757, against 1.537110798. These are small downward
discrepancies (1.81–2.15·10^-6 absolute), as in Section 7, without a dual
bound that excludes the reference. The Section 7.3 primal check closes
this effect as tolerance-level infeasibility; its presence with SCIP's own
rule also argues against an error specific to the new rules.

### 9.2 The earlier symmetry-enabled attempt

`logs/debugsol_withsym/` contains 43 solver logs, not 120 completed runs:
22 `corner`, 21 `eff`, all seed 0 with a 30 s limit. Of these, 41 have
return code 0, the same `ex5_4_2.eff.s0` has return code 255, and
`kall_congruentcircles_c52.corner.s0` was interrupted by a termination
signal and has no runner return-code footer. The runner log says
`jobs 120`, but contains no completion marker. This is an incomplete
attempt, not another complete validation sample.

No intersection-row violation is reported. Two `eff` runs report 23
other-row messages: 16 `underestimate_prod` messages on `ex5_2_5` and
7 `SSTcut` messages on `ex8_3_9`; the latter are symmetry-related rows.
There are global objective-bound warnings in four runs (34487 messages)
on `ex5_2_5` and `gasprod_sarawak01`, and zero of 42 available final
or 40 available root dual bounds exclude the MINLPLib reference.
Ten runs have an `ERROR` diagnostic. Symmetry-breaking may exclude a particular supplied solution
while preserving an equivalent solution, so this attempt cannot certify
validity against that one point.

**Status: numerical evidence, with an incomplete validity check.** There
is no confirmed intersection-row exclusion after correcting the 73
reported rows' objective helper, but the archived experiment cannot support
the claim "300 clean debug-solution runs". A clean whole-run check would
need solution values mapped into the OSiL extended model, including objective
helpers and constants, followed by investigation of residual diagnostics.
The checker can also stop checking once an incumbent reaches its loaded
reference objective. No debug-solution rerun was made in this revision.

## Revision after review round 1

The no-go recommendation for these two selection rules remains. This
revision corrects the major fairness claim and adds a matched stock binary
and 120 completed full solves (Section 7.4). The proof and original
root/rule-vs-rule tables remain unchanged.

- **M1:** Sections 2, 3, 7 and the Summary now explain row capture, the
  reproducible tree divergence, and which comparisons include its effect.
  The relink and off/root checks passed. Stock solves 77 pairs vs 75 off
  and 75 with the patched point rule, with CPU shifted geometric means
  15.962 / 17.709 / 17.979 s. These cross-batch timings do not establish
  an enabling benefit; the round-2 revision below corrects their
  interpretation. Section 7.4 adds explicit limits and Section 3 recommends
  counting rows without extending their lifetime.
- **m1–m2:** The helper correction is verified for all 73 rows, including
  positive helper coefficients and reports before any incumbent. The
  supplied `st_glmp_fp2` point is explicitly non-optimal. The nine local
  secant false alarms and `kall_congruentcircles_c52` primal discrepancy
  are closed with the review evidence and raw-log rechecks.
- **m3–m4:** The median-gain range is 1.05–1.65. Section 4.4 reports all
  seven search outputs, including the empty `tln7` crash and the negligible
  mean improvement on `ex8_3_2`.
- **m5–m7:** Timing limits include concurrent debug runs, instance-ordered
  jobs and observed wall/CPU ratios. Search shares and gains identify the
  267-instance population; costs distinguish generated cuts from searches.
  The requested 0.18 ms per search was corrected to 0.507 / 0.550 ms:
  raw logs show that the review's estimate mixed populations.
  The best-orbit claim identifies the stored corner-bound caveat.
- **Optional comments:** Section 8.1 qualifies the floored criterion and
  acceptance threshold, all uncorrected p-values are exploratory, and the
  82% degeneracy scan is distinguished from the sibling's 73% result.

[`code/audit_revision_r1.py`](code/audit_revision_r1.py) verifies the changed
archived-log numbers, reads and inventories all 65 review code/log artifacts,
and records the results in [`logs/audit_revision_r1.log`](logs/audit_revision_r1.log)
and [`logs/audit_revision_r1.json`](logs/audit_revision_r1.json).
Round 2 confirmed the build, retries and numbers, but found the timing
interpretation issue corrected below. This program makes
no commits; pre-existing repository changes were left alone.

## Revision after review round 2

This revision addresses N1 and N2 in
[`reviews/review-r2.md`](reviews/review-r2.md). The no-go for `corner` and
`eff` remains: it rests on the root results and within-batch rule-vs-rule
comparisons. The proof, root results and Sections 7.1/7.4 table numbers
remain unchanged. Round 2 confirmed m1–m7, including 0.507 / 0.550 ms per
search. Independent [round 3](reviews/review-r3.md), verdict **verified**,
confirmed the N1/N2 fixes in this revision. Its optional O1–O3 wording
edits were applied afterward and have not been re-reviewed.

- **N1:** The Summary, Section 7.4 and the round-1 M1 entry now state
  that the stock rerun establishes neither help nor harm from enabling
  SCIP's own rule for full solves. The archived batch was slower:
  patched/stock is 1.1544 over 69 matching solved paths and 1.3033 / 1.4384
  in the two ranges above 1 s; the 16 same-load runs agree within ±3%.
  The within-batch ratio 1.103 on 68 eligible pairs is the cleaner timing
  comparison about enabling in this grid, with its subset and capture
  limits stated. The `gabriel01`, seed-2 completion depends on batch speed;
  its shared-prefix estimate is approximately 395 s at archived speed.
  Only the `blend852`/`tln7` path outcomes and five of 74 changed solved
  node/LP signatures are attributed to row capture. Stock off vs stock scip
  interleaved on a quiet machine is recommended, not run.
- **N2:** Sections 7.1 and 7.4 name the node count as the first number
  on `Solving Nodes`, the count of the last run after a restart. Total
  nodes change the displayed shifted geometric means by at most 0.5;
  the existing definition and numbers are retained. The Summary now names
  both CPU and node shifted geometric means.

- **Round-3 optional wording:** O1 cross-references the within-batch
  common-solved ratio 1.0999 (p = 0.046) in Sections 7.1–7.2; O2 makes
  clear in Section 7.3 that matching wall/CPU ratios do not establish
  comparable CPU speed; O3 states that the shared `gabriel01` display
  prefix differs in the time and memory columns. The evidence and numbers
  are unchanged.

[`code/audit_revision_r2.py`](code/audit_revision_r2.py) reads and inventories
all round-2 code/log artifacts, independently parses the 600 full logs
and 16 reviewer same-load logs, and checks both node definitions and the
new timing statements. Results: [`logs/audit_revision_r2.log`](logs/audit_revision_r2.log)
and [`logs/audit_revision_r2.json`](logs/audit_revision_r2.json). It launches
no solver. Review files were left unchanged; no benchmark, commit or git
state change was made.

## 10. Reproducibility: build and run commands

*Sources.* SCIP Optimization Suite 10.0.3 tarball
`/workspace/local-home/build-scip/scipoptsuite-10.0.3.tgz` (sha256
`b6af618adc62c2f945a531f28eaf65f152a201913fa261000a5b711d5968aa85`);
MINLPLib OSiL files from `~/.cache/minlplib/minlplib/osil`;
`sources/minlplib.solu` (https://www.minlplib.org/minlplib.solu, accessed
2026-10-01, sha256 `df6732aa…bbac34`), `sources/instancedata.csv`
(https://www.minlplib.org/instancedata.csv, accessed 2026-10-01, sha256
`0ec2cb1e…dc8283`), solution files `sources/sol/*.p1.sol`
(https://www.minlplib.org/sol/INST.p1.sol, accessed 2026-10-02); see
`sources/MANIFEST.md`.

*Build* (as done in `/workspace/local-home/build-scip/selection/`; the build
directory used for every benchmark is `build-lapack`):

```
cd /workspace/local-home/build-scip/selection
tar xzf ../scipoptsuite-10.0.3.tgz
cd scipoptsuite-10.0.3 && patch -p1 < /workspace/minlp-notes/research-20261001/scip-set-selection/patch/scip-10.0.3-setrule.patch && cd ..
mkdir -p lapack && cd lapack
ln -sf /usr/lib/x86_64-linux-gnu/liblapack.so.3 liblapack.so
ln -sf /usr/lib/x86_64-linux-gnu/libblas.so.3 libblas.so
ln -sf /usr/lib/x86_64-linux-gnu/libgfortran.so.5 libgfortran.so.5
ln -sf /usr/lib/x86_64-linux-gnu/libquadmath.so.0 libquadmath.so.0
cd .. && mkdir -p build-lapack && cd build-lapack
L=/workspace/local-home/build-scip/selection/lapack
CC=/workspace/local-home/miniconda3/envs/scipbuild/bin/gcc CXX=/workspace/local-home/miniconda3/envs/scipbuild/bin/g++ \
cmake ../scipoptsuite-10.0.3 -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH=/workspace/local-home/miniconda3/envs/scipbuild \
  -DLPS=spx -DIPOPT=OFF -DPAPILO=OFF -DZIMPL=OFF -DGCG=OFF -DUG=OFF -DAUTOBUILD=OFF -DLAPACK=ON \
  "-DLAPACK_LIBRARIES=$L/liblapack.so;$L/libblas.so" "-DBLAS_LIBRARIES=$L/libblas.so" \
  "-DCMAKE_EXE_LINKER_FLAGS=-Wl,-rpath-link,$L" "-DCMAKE_SHARED_LINKER_FLAGS=-Wl,-rpath-link,$L"
make -j10 scip
```

The debug-solution build (`build-debugsol`) uses the same command with
`-DDEBUGSOL=ON`. Check that the binary links LAPACK
(`ldd bin/scip | grep lapack`) and that the statistics table
`nlhdlr_quadratic` (`set table nlhdlr_quadratic active TRUE`) shows a
nonzero `GenCuts` count; without LAPACK and Ipopt no cut is generated.

*Runs* (from `code/`; every runner skips finished logs, so it can be
restarted):

```
python3 candidates.py > ../logs/candidates.txt
python3 run_bench.py ../logs/screen ../logs/candidates.txt scip 0 root 60 12
python3 parse_logs.py ../logs/screen ../logs/screen.json        # testset_root.txt = runs with RootAppl > 0
python3 run_bench.py ../logs/root ../logs/testset_root.txt off,scip,corner,eff,scipS,cornerS,effS 0 root 120 12
python3 select_rootseeds.py
python3 run_bench.py ../logs/rootseeds ../logs/testset_rootseeds.txt off,scip,corner,eff 1,2 root 120 10
python3 select_fullset.py
python3 run_bench.py ../logs/full ../logs/testset_full.txt off,scip,corner,eff 1,2 full 300 10
python3 parse_logs.py ../logs/root ../logs/root.json   # likewise rootseeds
python3 root_analysis.py ../logs/root.json ../logs/rootseeds.json > ../logs/root_analysis.md
```

A timing rerun can reuse `run_bench.py` unchanged (it sets
`timing/clocktype = 1`, a 6000 MB memory limit, and
`randomization/permutationseed` for seeds > 0); for dedicated timing, run
matched comparisons with no other load and no more than four concurrent
processes. This is a
recommendation, not a benchmark run made during the closeout.

*Debug-solution runs.* `code/run_debugsol.py` documents the command form
`python3 run_debugsol.py OUTDIR INSTLIST SETTINGS TIMELIMIT NPROC`.
The archived run headers establish five settings, seed 0, a 30 s CPU limit,
heuristics off, and symmetry off for the complete sample. The six chunk
runner logs record 55 + 50 + 35 + 40 + 60 + 60 = 300 jobs. The temporary
chunk instance lists and exact chunk launch commands were not retained,
so their concurrency cannot be recovered from these artifacts. The earlier
symmetry-enabled runner declares 120 jobs but only 43 solver logs remain.
The current runner has since been changed to turn symmetry off; it does
not reproduce that earlier attempt unchanged.

*Completed-log closeout, 2026-10-03.* The following commands were actually
run from `/workspace/minlp-notes/research-20261001/scip-set-selection/`.
Each analysis ran as one foreground process; no SCIP benchmark was started.
Both commands exited 0. They parse raw logs directly and write their JSON
companions as well as the redirected Markdown reports.

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout 120s python3 code/full_analysis.py > logs/full_analysis.md
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout 120s python3 code/debugsol_analysis.py > logs/debugsol_analysis.md
```

The targeted check below also exited 0; its output is
[`logs/closeout_checks.log`](logs/closeout_checks.log). It independently
counts optimal statuses in the raw full logs and checks the CPU aggregation,
debug diagnostic counts, corrected row activities, seed inventory, section
numbering and review status. These are local checks; CI was not inspected.

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout 30s python3 - <<'PY' > logs/closeout_checks.log
import ast, json, math, re
from collections import Counter
from pathlib import Path
for name in ('full_analysis.py', 'debugsol_analysis.py'):
    ast.parse((Path('code') / name).read_text())
full = json.loads(Path('logs/full_analysis.json').read_text())
debug = json.loads(Path('logs/debugsol_analysis.json').read_text())
raw = []
for path in Path('logs/full').glob('*.log'):
    text = path.read_text()
    setting = path.name.rsplit('.', 3)[1]
    raw.append((setting, 'SCIP Status        : problem is solved [optimal solution found]' in text))
assert Counter(s for s, ok in raw if ok) == {'off': 75, 'scip': 75, 'corner': 76, 'eff': 76}
for row in full['tables']:
    if row['scope'] != 'all pairs':
        continue
    rs = [r for r in full['records'] if r['setting'] == row['setting']]
    values = [r['time'] if 'optimal solution found' in (r['status'] or '') else 300 for r in rs]
    independent = math.exp(math.fsum(math.log(v + 1) for v in values) / len(values)) - 1
    assert math.isclose(independent, row['time'], rel_tol=1e-12)
rs = debug['groups']['debugsol']['records']
assert sum(r['diagnostic_counts'].get('intersection_row', 0) for r in rs) == 73
assert sum(r['diagnostic_counts'].get('other_row', 0) for r in rs) == 9
assert sum(bool(r['diagnostic_counts']) for r in rs) == 45
assert sum(r['diagnostic_counts'].get('global_objective_bound', 0) for r in rs) == 114699
assert sum(len(r['corrected_rows']) for r in rs) == 73
assert all(c['violation'] < -0.0175 for r in rs for c in r['corrected_rows'])
assert debug['seed0_inventory']['ordinary_full_logs'] == []
note = Path('note.md').read_text()
prose = re.sub(r'```.*?```', '', note, flags=re.S)
assert re.findall(r'^## (\d+)\.', prose, re.M) == [str(i) for i in range(1, 11)]
assert '(DRAFT:' not in prose and '(Being filled in.)' not in prose
assert 'has not been\nreviewed' in prose
print('PASS: syntax, independent raw solved counts, CPU means, diagnostic counts, corrected row activities, seed-0 inventory, note numbering and review status.')
for d, g in debug['groups'].items():
    print(d, 'available final bounds', sum(r['dual'] is not None for r in g['records']), 'available root bounds', sum(r['rootdual'] is not None for r in g['records']))
PY
```

Process checks used `pgrep -af '[s]cip-set-selection'` (no matches, exit 1)
and `ps -C claude -o pid,lstart,comm` (exit 0). All remaining Claude
processes began on October 3, after the October 2 owner referred to by
`STREAM_OWNER_LOCK.txt`; no stream runner or solver process was present.
That stale lock file was removed. The separate lock directory outside this
stream was left untouched. No background process was started in the
closeout, and the final scoped process check found none.

*Review revision, 2026-10-03 (local date).* Commands below use paths relative
to this stream. The initial launches used the equivalent repository-root
prefix `research-20261001/scip-set-selection/`; final analyses and checks
ran from this stream. No CI was inspected and no project-wide verification
was run:

```bash
OMP_NUM_THREADS=1 timeout 120s python3 code/build_stock_r1.py > logs/build_stock_r1.log 2>&1
OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout --kill-after=10s 1200s python3 code/check_stock_r1.py > logs/check_stock_r1.log 2>&1
OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout --signal=TERM --kill-after=20s 10800s python3 code/run_stock_r1.py > logs/full_stock_driver.log 2>&1
OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout --signal=TERM --kill-after=20s 10800s python3 code/run_stock_r1.py 1800 > logs/full_stock_retry_driver.log 2>&1
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout 120s python3 code/audit_revision_r1.py > logs/audit_revision_r1.log 2>&1
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout 120s python3 reviews/r1-code/recompute.py > logs/recompute_revision_r1.md
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout 120s python3 code/stock_analysis_r1.py > logs/stock_analysis_r1.md 2>&1
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout 120s python3 code/check_revision_r1.py > logs/check_revision_r1.log 2>&1
# From the repository root:
git diff --check -- research-20261001/scip-set-selection
# Process checks (exit 1 means no matches):
pgrep -af scip
pgrep -af '[r]un_stock_r1.py|[c]heck_stock_r1.py'
```

Build, final identity checks, audit and independent table recomputation
exited 0. The final independent check also exited 0, verifying 600 raw
records, CPU/node aggregates, paired ratios and instance-averaged tests;
the scoped whitespace check exited 0. Its first attempt omitted the legal
parenthesized restart suffix on a SCIP node-count line; that parser was
corrected before the successful check. Two preliminary off probes
(`qp3`, `ex5_2_5`) were stopped after
their archived runs were found to be time-limited; load-sensitive stopping
nodes are unsuitable for an identity check. Their incomplete logs remain
in `logs/stock_checks_r1/aborted-probes/`. All those probe processes were
terminated. The final identity checks use two completed solves and the
reproduced numerical failure. The first stock driver exited 0 with
112 valid results and eight wall timeouts. The retry skips all 112 completed
logs, retained the eight failed attempts, completed eight valid runs and
exited 0. All 120 final solver runs returned 0. The first stock-analysis
attempt failed while formatting an absent node-test p-value; the formatter
was fixed to print a dash and the rerun exited 0. Final independent checks
and process cleanup are recorded in `logs/check_revision_r1.log` and
`logs/process_check_revision_r1.log`. No background experiment process
remains after this work. The historical closeout command above asserted
the then-unreviewed status; use the targeted checks below for the current status.

*Revision after round 2, 2026-10-04.* The following targeted commands ran
from this stream in the foreground. Both final Python checks exited 0.
The audit reads all 39 round-2 code/log artifacts, checks the new evidence
against raw logs, and records their hashes. The existing checker independently
rechecks the unchanged numbers, paired ratios and tests. No benchmark was
started and no CI checks or logs were inspected.

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout 60s python3 code/audit_revision_r2.py --check-note > logs/audit_revision_r2.log 2>&1
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout 60s python3 code/check_revision_r1.py > logs/check_revision_r2.log 2>&1
# From the repository root:
OMP_NUM_THREADS=1 timeout 30s git diff --check -- research-20261001/scip-set-selection
OMP_NUM_THREADS=1 timeout 30s pgrep -af '[r]un_stock_r1.py|[c]heck_stock_r1.py|[r]un_bench.py|[s]cip-stock|build-lapack/bin/[s]cip'
```

The scoped whitespace check exited 0; the process check exited 1 (no
matching runner or solver). No background process was started. Results:
[`logs/audit_revision_r2.log`](logs/audit_revision_r2.log) and
[`logs/check_revision_r2.log`](logs/check_revision_r2.log).
The initial evidence-only audit exited 1 because it tested the review's
0.5 node-mean change as an unrounded bound. A targeted raw-log probe
(`OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 timeout 30s python3 -`,
exit 0) found a maximum change of 0.5952801059670492 for corner seed 2.
At the tables' precision that is 3890.1 → 3890.6, a displayed change of 0.5.
The audit and wording were corrected to distinguish these precisions;
the corrected evidence-only audit and final note check exited 0.
