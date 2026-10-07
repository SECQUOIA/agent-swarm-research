# Implementation facts for "Certified support cuts for shared nonlinear expressions and quadratic blocks"

Fact check of the implementation claims in Report B
(`research-20261003-convexification/document/implementation.tex`) and Report A
(`research-20261002-convexification/document/integration.tex`) against the code,
dated 2026-10-03. Abbreviations: `B/` = `research-20261003-convexification/`,
`A/` = `research-20261002-convexification/`, `uenv/` =
`code/univariate_envelopes/uenv/`. All line numbers refer to the live files.
Section 4 records where the frozen campaign sources differ.

## 1. Targeted checks actually run

All commands ran from `/workspace/minlp-notes`. These are local targeted
checks only. No project-wide suite was run and no CI status was inspected.

| # | Command | Result |
|---|---|---|
| 1 | `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONPATH=research-20261003-convexification:research-20261003-convexification/solver code/minlp_solver_lab/.venv/bin/python -m pytest -q research-20261003-convexification/solver/test_*.py research-20261003-convexification/theory/test_*.py research-20261003-convexification/experiments/test_*.py` | **186 passed** in 2.53 s, exit 0 |
| 2 | `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 code/minlp_solver_lab/.venv/bin/python -m pytest -q research-20261002-convexification/theory/test_*.py` | **30 passed** in 0.25 s, exit 0 |
| 3 (extra) | `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONPATH=research-20261002-convexification:research-20261002-convexification/solver code/minlp_solver_lab/.venv/bin/python -m pytest -q -p no:cacheprovider research-20261002-convexification/solver/test_*.py` | **104 passed, 6 subtests passed** in 1.40 s, exit 0 |

The PYTHONPATH values for commands 1 and 2 match the task's specification. The
only additions were single-thread environment variables (and an outer
`timeout`). Command 3 was an extra targeted check of the Report A solver code
whose claims are reviewed here; its PYTHONPATH follows `A/VERIFICATION.md`.
These runs refreshed Python bytecode caches (`__pycache__`) under the two
report folders. No source, data, or document file there changed.

Additional read-only probes (scripts in `/tmp/implfacts/`, outside the
repository):

- An enumeration-budget, rounding-export, and fallback probe for
  `B/theory/quadratic_polytope.py`, `B/solver/row_certificate.py`, and
  `B/solver/support.py`. Its results are quoted in Section 2.
- Scans of `B/experiments/campaign-v2/records.jsonl`,
  `B/experiments/repair-discovery-v1/records.jsonl`, and
  `A/experiments/campaign-v1/records.jsonl` for the configurations used, cut
  methods, statuses, and callback times. Results are quoted in Sections 4 and 6.

Python 3.13.11, SymPy 1.14.0, python-flint 0.9.0, SciPy 1.18.1 (HiGHS),
NumPy 2.5.3, PySCIPOpt 6.2.1, SCIP 10.0.2 (from each campaign's
`environment.json` and the `scip_version` field of its records).

## 2. Claim-by-claim check

Status key: **OK** = code matches the text. **Clarify** = the text is
true, but a paper version needs the stated precision. **Mismatch** = the
text and code disagree, or the text overstates.

### 2.1 Report B `implementation.tex`

| Claim (tex lines) | Code | Status |
|---|---|---|
| Binary64 leaves are exact rationals. The builder assembles the native expression, compares it symbolically with the source (`expand(source - native) == 0`, no tolerance), and otherwise builds a generic DAG with separate constant children, then rechecks. A remaining difference raises `source_model_mismatch` (12-27). | `B/solver/model.py:53-57, 60-82, 309-329`; `A/solver/model_binding.py:115-173`; generic DAG `B/solver/model.py:237-262` | OK |
| "Ranged constraint sides and objective sense and constants are part of the same check" (26-27). | The objective constant is part of the checked expression (`model.py:265-270, 311`). Row sides are passed to `ExprCons` unchanged (`model.py:385-391`). Polynomial rows with a nonzero constant are forced onto the generic DAG so `ExprCons` cannot shift the sides in binary64 (`model.py:321-326`). The objective sense is mapped directly (`model.py:374-384`). No runtime step compares stored row sides or sense with the source. Coverage comes from tests (`B/reviews/test_model_review.py:281-289`, `B/solver/test_model.py:104-121`), and replay rechecks the objective sense through signed sides (`B/experiments/replay.py:144-147`). | **Mismatch (overstated)**: sides and sense are preserved by construction and tested, not symbolically checked at run time |
| The boundary is the submitted PySCIPOpt DAG; SCIP simplification, presolve, LP arithmetic, and tolerances are outside the claim (29-32). | `model.py:1-6`; metadata `binding_boundary` at `model.py:392` | OK |
| Exact affine bound propagation from original affine rows (no nonlinear tree or quadratic entries) with integer rounding, per-step provenance (row, side, variable, old/new bound), replay, a valid prefix on budget stop, and outward binary64 export (34-61). | `B/solver/bounds.py:74-75, 124-165, 179-226` (budgets `max_passes=8`, `max_steps=10000`, line 179), replay `229-315`, outward rounding `48-59`. The solver keeps the declared bounds (`model.py:302-306`). An exact contradiction refuses the model as `affine_infeasible` (`model.py:298-299`). | OK |
| Proportional original affine rows prove affine domain arguments, e.g. `x-y=1` for `log(x-y)` (63-66). | `model.py:104-135`, used at `model.py:164` | OK |
| Domain traversal visits every source node before simplification; one-sided intervals are retained (68-71). | `model.py:177-219` (children visited at 182), extended product `model.py:85-89` | OK |
| Exact existential witnesses: `d!=0`: `du=1`, `u` free. `d>0`: `du=1`, `u>=0`. `d>=0`: `d>=0`. Witnesses may be unbounded. The argument is compiled and checked. Sharing only for the same argument and requirement (72-88). | `model.py:333-371`: sharing key `(kind, srepr(arg))` at 337-338; argument check 340-342; equation check 356-360; `u` bounds 350-351. Replay re-derives the expected guards: `B/reviews/model_binding_audit.py:76-104`. | OK |
| Variable powers: `b^e = exp(e log b)` only after positivity of `b` is proved, otherwise `unsupported_variable_power_domain`; no indiscriminate guard; fixed exponents must be exact binary64 (97-105). | `model.py:78-80, 199-203, 168-169, 248-257`; rational exponent required at `model.py:204-205`. The native first attempt raises `NotImplementedError` for variable exponents (`uenv/osil.py:226-229`); this is caught at `model.py:316` and leads to the generic DAG. | OK |
| Discovery groups complete nonlinear remainders of original row sides; exact affine terms are kept for elimination; overlapping remainders form larger groups up to the block size; a remainder with unsupported variables is declined whole; affine sides on the chosen variables supply domain rows (116-124). | `B/solver/integration.py:125-158` (split), `161-184` (signed sides), `187-272` (discover). A side is admissible only with 1 to 4 variables, all with finite proved bounds (`199-202`); a nonpolynomial remainder only if univariate (`204-207`); a polynomial remainder only with total degree at most 8 (`208-210`). Groups are each side's own variable set plus one greedy overlapping union per side (`214-223`), ordered largest first (`226`). | OK. The degree-8 cap is not stated in `implementation.tex` (it is in `B/implementation/integration.md:69-70`). |
| Lazy discovery: a model solved in presolve pays no discovery cost (126-127). | Discovery runs in the first `sepaexeclp` call (`integration.py:431-442`); test `B/solver/test_integration.py:125` | OK |
| A sample LP proposes the normal and nonnegative side multipliers; exact support is computed for the actual direction; its minimizer feeds a bounded exchange; samples and LP output establish no bound (127-132). | LP `integration.py:316-336` (HiGHS, intercept free, linear coordinates in [-1,1], multipliers in [0,1], 0.05 s, one thread); certification `466-471`; exchange `472-484` | OK. **Clarify**: before any LP, each block first tries one unit direction per signed side, i.e. the support of a single original row (`integration.py:403-407`). These count against the 24 support calls and run once per block per run (`seen`, 461-463). `implementation.tex` omits this step (`B/implementation/integration.md:95` has it). |
| "Exact polytope vertices and their centroid seed proposals on thin affine domains" (132-135). | `integration.py:297-307` adds exact vertices and their centroid for **every** quadratic block whose subset count is at most `max_faces`, not only for thin domains | **Clarify (imprecise)** |
| General quadratic blocks up to dimension 4 under a complete-subset budget: 5,000 subsets in the standalone wrapper, 2,000 in the callback; "an unmet limit yields no cut from that calculation" (137-143). | `B/solver/support.py:35-38, 65`; `integration.py:42, 46, 69, 470`; the budget is checked before enumeration (`B/theory/quadratic_polytope.py:110-116, 190-191`). On refusal, `support.py:71-72, 93-104` **falls back** to the v1 kernels and records `polytope_skipped`. | **Clarify**: no partial enumeration becomes a bound, but a cut can still come from the v1 star, Bernstein, or Arb kernel. Probe: a 4-variable center-leaf star with 8 rows needs 2,517 subsets and is certified by `quadratic_star`. Adding a leaf-leaf row gives `unsupported`. |
| The subset count is N = sum_{k<=d} C(m,k). | `quadratic_polytope.py:101-107` with **m = (affine rows) + 2d**, because the box sides count as rows | **Clarify** for C-POLY. Derived limits (probe): at 2,000 subsets, d=4 allows at most 7 signed affine domain sides (1,941 subsets), d=3 allows 16 (1,794), d=2 allows 58. At 5,000 subsets, d=4 allows 10 and d=3 allows 25. An equality row counts as two sides. With the 16-side cap, d=4 needs 12,951 subsets. |
| Higher-degree polynomial and elementary bounds remain sound; partial-domain features that cannot be covered are declined (143-148). | `A/solver/certified.py:342-374`: Bernstein only for 1 or 2 variables with at most 1,024 tensor coefficients (344-345); elementary path univariate only (347-348); Arb domain failures leave the cell unresolved, which yields `incomplete` (470-480) | OK. **Clarify**: discovery admits 3- and 4-variable polynomial sides of degree 3 to 8, which no kernel certifies. They end as `unsupported` (a certification failure, no cut). |
| Modes `baseline`, `all`, `auto` share one builder; `all` means all admitted blocks within caps; the complete separation API is separate (150-160). | `integration.py:547-549, 589-594`; `separate_graph` is never called from `integration.py` | OK. `control` is an alias of `baseline` (`integration.py:547`). |
| Frozen `auto` rule: admit quadratic blocks containing a signed quadratic not proved convex, and either a non-axis affine domain row or at least two distinct nonlinear source rows (162-164). | `integration.py:251-265`: "not proved convex" means SymPy `hessian(...).is_positive_semidefinite is not True` (261); a non-axis row has more than one nonzero coefficient (264); distinct rows are counted by `row_index`, so both sides of one ranged row count once (265) | OK |
| Two support failures deactivate a block for the remaining callbacks (164-166). | `integration.py:450, 485-488` | OK, in `auto` only. A failure means `certify_support` returned no cut (incomplete, empty, or unsupported). Insufficient violation and rounding rejections are not failures. |
| Limits: 32 blocks, six nonlinear sides and 16 affine domain sides per block, three root callbacks, 12 total cuts, four per callback, 24 support calls, three LP exchange attempts per block and callback (166-169). | `Config` at `integration.py:40-60`. Enforced at: blocks 268-270; sides 233; affine sides 249; root and calls 423 (`getDepth()!=0`) with separator `freq=0` at 594; total cuts and support calls in `_expired` 387-392; per callback 448, 460; exchanges 408 | OK. **Clarify**: 12 cuts and 24 support calls are totals per run. Blocks and sides are taken in a fixed order (largest groups first; source-row order) and truncated. |
| Callback work gets min(1 s, 5% of the requested total budget), checked between operations; nonpreemptive overrun possible (169-173). | `integration.py:387-392, 590-591` | OK. **Clarify**: this is one cumulative allowance for all callbacks of a run. The worker passes the soft budget minus its preparation time (`B/experiments/worker.py:67`), so the allowance is about 1 s for 30-s runs, at most 0.5 s for 10-s runs, and at most 0.25 s for 5-s root runs. |
| Final violation / max{1, sum_j abs(c_hat_j)} must exceed 1e-5 (`all`) or 5e-4 (`auto`) (173-175). | `integration.py:56-57, 458, 503-507` (binary64 evaluation at the LP point, after rounding) | OK. **Clarify**: two further work filters exist. The proposal LP needs a scaled objective below -1e-5 in both modes (330). For non-quadratic blocks, the support call has the unnormalized target `activity + threshold` (468). |
| The corrected discovery checks the deadline between source rows, additive terms, and group steps; on expiry it discards discovery and records `discovery_incomplete` and `budget_exhausted` (176-180). | `integration.py:31-37, 125-136, 161-166, 187-250, 431-440`; later callbacks return `DIDNOTRUN` (423) | OK for the live and repair sources. **Absent in the campaign-v2 source** (Section 4). |
| Terms become polynomials over their own symbols; nonrational and unconvertible terms stay in the nonlinear remainder (181-184). | `integration.py:143-151` (catches `CoercionFailed`, `RecursionError`) | OK (live and repair). The frozen campaign-v2 code used all global symbols and did not catch `CoercionFailed` (not a `PolynomialError` subclass in SymPy 1.14) or `RecursionError`. |
| Accepted-cut sequence: support for the actual direction, exact elimination, merging of repeated coefficients, bound correction, inspection of the stored row, global root cut (187-193). | `integration.py:467-534`; merging at `B/solver/row_certificate.py:124-137`; the violation test at `integration.py:503-507` sits between rounding and row creation | OK |
| Domain rows and rounding bounds are original global implications; no incumbent cutoff or local presolve bound (191-193). | Support box and rounding bounds are `built.bounds` (outward-rounded proved bounds, `model.py:300-301`; `integration.py:374-378`); rows use `local=False` (510) | OK |
| Conservative rounding: both finite bounds are required wherever the rounding error is nonzero, although the proposition needs only the bound in the error's direction (194-199). | `row_certificate.py:216-221`. Probe: error sign -1 on `x` with bounds (None, 1.0) is rejected, and with (0.0, 1.0) accepted. The objective epigraph has an exact coefficient `lambda*sign` and needs no bounds (`B/solver/test_row_certificate.py:91`). | OK |
| No feature-equality reformulation differs across modes (201-205). | `model.py` is mode-independent; `integration.py` only adds the separator | OK |
| A record binds the serialized instance, signed source sides, variables, nonlinear expressions, proved bounds, support domain, direction, support certificate, elimination, rounding, and actual row; fresh replay derives all of these from the archived model (207-215). | `integration.py:526-534`; replay `B/experiments/replay.py:192-293` (also archived as `B/reviews/replay-final.py`, same SHA-256) | OK |
| Replay shares exact primitives with generation and is independent of the LP and search (217-224). | `replay.py` imports `solver.support.replay_support`, `solver.row_certificate`, `solver.bounds`, and `build_model` (via `model_binding_audit.py:74`). It reimplements affine splitting and signed-side reconstruction independently (`replay.py:96-157`). | OK |
| Actual-row binding: columns, coefficients, constant, sides, scope, source-to-transformed mapping (`implementation.tex` 190-191; `B/implementation/integration.md:58-62`). | `integration.py:339-363`: exact rational equality of columns and coefficients, `lhs - constant == rhs`, finite `abs(lhs) <` SCIP infinity, upper side at infinity, not local, no two source variables mapped to one column | OK. **Clarify**: Report B does not mark variables as do-not-aggregate, so rows touching a substituted or aggregated variable are rejected (8 `row_binding_rejections` in campaign-v2, 16 in the repair cohort). The audit inspects the row object before `addCut`; later SCIP handling of the row is outside the check. |
| Replay checks recorded row bounds against the infinity sentinel (`B/implementation/integration.md:158-159`). | `replay.py:288-292` checks only the upper side (`rhs >= scip_infinity`), **not** `abs(lhs) < scip_infinity` | **Clarify**: the lower side was checked by a separate audit, `B/reviews/campaign-guard-audit.json` (all 123 campaign-v2 cuts pass; maximum `abs(rhs)` over SCIP infinity is 8.5e-19; largest `abs(rhs)` is 85). |

### 2.2 Report A `integration.tex`

| Claim (tex lines) | Code | Status |
|---|---|---|
| `certify_support` and `replay_support` take SymPy features with an ordered symbol tuple. `support-cut-v1` binds the typed expression tree, box, rows, hexadecimal coefficients, method, precision, proof, rational bound, and downward-rounded rhs (5-21). | `A/solver/certified.py:86-102, 114-140, 487-497, 506-590` | OK |
| Polynomial path: rational algebra with integer powers up to the cap. Elementary path: univariate, with +, *, rational powers, exp, log, sin, cos, sinh, cosh, tanh, arctan, abs, pi, e via Arb (22-31). | `certified.py:81-83, 105-111, 143-156, 223-283` | OK |
| Rational powers need a nonnegative base (positive for negative exponents); no odd-root extension; negative integer powers need a denominator interval excluding zero (27-30). | `certified.py:209-220, 254-268` | OK |
| Bernstein fallback: 1 or 2 variables, at most 1,024 tensor coefficients. Star oracle for higher-dimensional quadratics. Kernel powers up to 32. Discovery degree caps 8 (one variable) and 4 (pair) (33-40). | `certified.py:344-345, 390-399, 111, 154`; `A/solver/integration.py:44-45, 190-194` | OK. The star path also requires every row to involve the center and at most one other variable (`certified.py:397`). |
| Row exclusion only by an exact lower activity above the rhs; all-excluded proves emptiness; replay rebuilds dyadic children and recomputes leaves; limits return `incomplete`, unsupported input returns `unsupported` (42-52). | `certified.py:313-318, 456-491, 552-587, 498-503` | OK |
| The importer checks every source domain on the declared box only and refuses NaN, reversed, or sentinel-reaching bounds (64-72). | `A/solver/model_binding.py:176-299`; `A/solver/integration.py:513-530` | OK |
| A whole-row exact check runs in all four modes; constants are folded only if exactly binary64; `source_model_mismatch` carries no bound (74-87). | `A/solver/integration.py:538-552, 812-826`; `model_binding.py:86-112` | OK |
| Auxiliary definitions are checked; a failed atom is declined; a failed rewritten row reverts to the original row (89-96). | `A/solver/integration.py:558-569, 602-612` | OK |
| Discovery: atoms of one or two variables identified by source tree, quadratic row terms, pairs from atoms or affine rows, stars with 2-4 leaves, caps 256 atoms, 64 blocks, 8 coordinates (100-129). | `A/solver/integration.py:179-212, 233-237, 241-252, 257-274, 283, 304-306` | OK |
| Auxiliaries are enforced natively; control/all/auto share the reformulation (110-118). | `A/solver/integration.py:570-571, 586-591` (variables also marked do-not-aggregate in these three modes) | OK |
| Global root cuts with an actual-row audit (131-147). | `A/solver/integration.py:475-505, 749-762` | OK |
| Direction LP and samples: 65-point grid in 1D, 13x13 in 2D, 128 Halton points plus corners for stars, exact seeds (151-160). | `A/solver/integration.py:46-47, 313-378, 381-427` | OK |
| `auto` requires shared univariate structure, a pair with a retained affine row, or a recognized star; threshold 5e-4; stops after two failures; screen only for source-polynomial features (162-172). | `A/solver/integration.py:294-297, 579-580, 714-716, 726-742, 458-462` | OK. **Clarify**: "shared univariate structure" also covers a single atom with at least two nonlinear operations (composite). The screen evaluates the sample weights from the previous direction LP's row duals at the current query (`396-409`, `730-734`). |
| At most three exchange rounds (174-181). | `A/solver/integration.py:60, 656-696` | OK |
| Limits: five root callbacks, 24 cuts, six per callback, 128 cells, depth 16, budget min(2 s, 15% of the integration budget) (189-196). | `A/solver/integration.py:48-56, 837-839` | OK. **Clarify**: in campaign-v1 (6-s soft budget) the 15% term (about 0.9 s) was binding, not the 2-s cap; it was about 0.3 s for the 2-s root runs. |

### 2.3 Theory and separation kernels named in the contribution list

| Contribution | Code | Status |
|---|---|---|
| C-SUP / Prop. `prop:round`: the exported binary64 coefficients are certified exactly, and the rhs is rounded down. | `certified.py:129-132, 47-56, 492-497`; `support.py:81-92` | OK |
| C-BERN: exact Bernstein bound, complete subdivision cover, Arb enclosure, chord correction `min{p(a),p(b)} - max{0,M}(b-a)^2/8`. | `certified.py:159-180, 452-486, 223-283, 363-373` | OK. **Clarify**: the chord correction is used only on the univariate elementary (Arb) path, not on the Bernstein polynomial path. A missing or singular second derivative disables it. |
| C-SCREEN: exact convex-combination screen. | `A/solver/screening.py:90-115, 123-134, 176-239` | OK. Used only by Report A `auto`; Report B does not use it. |
| C-AGG / Prop. `prop:elimination-round`: exact elimination, then bound-corrected binary64 export. | `row_certificate.py:144-246` | OK (more conservative than the proposition; see 2.1). |
| C-POLY: bordered stationary systems of active subsets, singular and empty cases, replay by full re-enumeration. | `B/theory/quadratic_polytope.py:164-171, 174-225, 228-240, 119-138` | OK. m includes the 2d box sides. |
| C-STAR: center-leaf rows, any curvature sign, any number of leaves, rational center partition. | `A/theory/quadratic_star.py:19-47, 75-87, 97-116, 119-153, 166-230` | OK. In practice the Report A discovery proposes 2-4 leaves, and Report B blocks have at most 4 variables. |
| C-SEP: L1 distance, cone coordinates, R, normal grid `ceil(2R/(eps-delta))`, Lipschitz domain net, four statuses. | `B/solver/separation.py:248-250, 334-357, 162-210, 294-421`; replay `424-510` | OK. Defaults: `epsilon=1/100`, `max_directions=256`, `max_samples=20000`, `proposal_rounds=8`. No wall-clock limit, and no cap on vertex or face enumeration (`314`, `365`), as `separation.tex:159-163` states. |

## 3. Mismatches and wording changes the paper needs

1. **Row sides and objective sense** (`implementation.tex:26-27`). Do not say
   they are part of the symbolic check. Say: expression values, including
   constants, are checked symbolically with no tolerance. Row sides are
   submitted unchanged, and constants are kept inside the expression so the
   constraint constructor cannot round them into the sides. Tests and replay
   check sides and sense.
2. **Enumeration-budget fallback.** If the exact polytope enumeration exceeds
   its subset budget, the wrapper falls back to the inherited star, Bernstein,
   or Arb kernels. It never uses a partial enumeration. State the subset count
   with m = r + 2d. Under the callback's 2,000-subset budget, exact polytope
   support covers d = 4 only with at most 7 signed affine domain sides.
3. **Vertex seeds** are added for every quadratic block within the budget, not
   only for thin domains.
4. **The time allowance** is cumulative per run and is computed from the soft
   budget remaining after worker preparation. In Report A the binding term was
   15%, not 2 s.
5. **Single-row directions** come first and consume support calls. List them
   in the algorithm description.
6. **The campaign-v2 code is not the described code** for discovery
   deadlines, sparse splitting, `CoercionFailed`/`RecursionError` handling,
   the infinity-sentinel rejections, and exchange-evaluation failures
   (Section 4). The paper must say that the prospective campaign measured the
   frozen code. In that code, 47 of 184 cut-mode runs overran the separator
   allowance by more than 0.05 s, 36 by more than 0.5 s, and 17 by more than
   2 s. The maximum overrun was 19.4 s (`btest14`, `all`, 30-s budget). In 46
   of these runs, discovery time alone exceeded the allowance. Report B's
   evidence section says only "Discovery on a large case also overran its
   allowance"; the paper should give these counts. They match the repair
   rule: 23 overrun groups plus 2 crash groups make the 25 repair groups. In
   the repair cohort the maximum overrun was 0.03 s.
7. **Infinity sentinel.** Replay checks only the upper side; the lower side
   was covered by the separate guard audit. Name the checker that covers it.
8. **Degree caps.** Discovery admits polynomial sides up to total degree 8 in
   up to four variables. Certification supports quadratics in d <= 4 (polytope
   or star), Bernstein in 1 or 2 variables (at most 1,024 tensor coefficients,
   per-variable degree at most 32), and univariate elementary functions. Other
   admitted sides end as `unsupported`.
9. **Report A `auto`** eligibility includes composite single atoms. Its screen
   uses the weights from the previous LP.
10. **C-BERN wording.** The chord correction belongs to the elementary path
    only.
11. **C-SCREEN** was exercised only in Report A. **C-STAR fallback** produced
    no Report B campaign cut. Methods of recorded cuts: campaign-v2 has 91
    `quadratic_polytope`, 30 `arb`, and 2 `bernstein`. The repair cohort has 34
    `quadratic_polytope` and 8 `arb`. Report A campaign-v1 has 460
    `bernstein`, 450 `quadratic_polygon`, 125 `quadratic_star`, and 47 `arb`
    (1,082 total). No Report B cut carries `polytope_skipped`.

No mismatch was found in the listed limits (32 / 6 / 16 / 3 / 12 / 4 / 24 / 3),
the thresholds 1e-5 and 5e-4, the `auto` rule, the conservative two-bound
rounding rule, the domain witnesses, or the variable-power rule.

## 4. Source provenance of the measured code

| File | campaign-v2 snapshot | repair-discovery-v1 snapshot and live |
|---|---|---|
| `B/solver/integration.py` | `5620d3f26473e56e0f0f0b086412508caa416bc190e207d85ea6c815db73e1be` | `128fe10b13d22874aa6f76d86ed2a11f73076ddb747967cc7e468225c3203210` |
| `B/solver/support.py` | `c260fb29...` (same) | same |
| `B/solver/row_certificate.py` | `6917a78d...` (same) | same |
| `B/solver/model.py` | `e4b13e50...` (same) | same |
| `B/solver/bounds.py` | `51136605...` (same) | same |
| `B/solver/separation.py` | `8869c195...` (same) | same |
| `B/theory/quadratic_polytope.py` | `4fffd2f5...` (same) | same |
| `A/solver/certified.py`, `model_binding.py`, `A/theory/quadratic_star.py`, `quadratic_polygon.py` | same as live (`876bee20...`, `334efac5...`, `669aefec...`, `7172e3c9...`) | same |
| Offline replay checker `B/experiments/replay.py` = `B/reviews/replay-final.py` | `10115390a428ca2eb7131d5ebf4a094260170ebe3146e491ad73b85526c4c146` | same |

Report A's campaign-v1 snapshot matches the live Report A sources
(`A/solver/integration.py` `6a972944...`, `screening.py` `2a98eee1...`).

The frozen campaign-v2 `integration.py` differs from the live file only in:

- no discovery deadline;
- polynomial conversion over all global symbols, without catching
  `CoercionFailed` or `RecursionError` (this caused the four `worker_error`
  records on `chp_partload` and `waterno2_06`);
- no rejection of a converted rhs, or a stored row lhs, at SCIP's infinity
  sentinel;
- no catch for a failed heuristic evaluation of an exchange sample.

The `Config` values and the `auto` rule are identical. The single configuration
recorded in all 282 campaign-v2 records and all 75 repair records equals the
defaults in Section 6.

## 5. Paper-ready architecture description

### 5.1 Implementation section (prose)

The prototype is a Python layer over SCIP 10.0.2 through PySCIPOpt 6.2.1. It
does not change SCIP's constraint handlers, branching, or propagation. It adds
one separator that submits global root cuts. It has five components with
separate responsibilities.

1. **Source import and binding** (`model.py`, `bounds.py`, `model_binding.py`).
   The OSiL reader parses each numeric token to a binary64 number, and every
   such number is then read as its exact rational value. The source grammar
   is sums, products, negation, division, squares, fixed rational powers,
   variable powers, `exp`, `log`, `sqrt`, `sin`, `cos`, and `abs`. The
   importer builds one native model, used unchanged by every mode. For each
   original row and the objective, it compares the exact source expression
   with its reading of the submitted PySCIPOpt expression DAG, by symbolic
   subtraction and expansion with no tolerance. If ordinary assembly rounds a
   coefficient product or would move a constant into a row side, it submits a
   generic DAG with separate constant children and checks again. Any remaining
   difference is a structured refusal.

   Exact interval propagation over the original affine rows, with binary and
   integer rounding, yields bounds that hold at every original feasible point.
   Each deduction records its row, side, variable, and old and new bounds. The
   bounds are exported outward to binary64. They are used only as proof
   premises; the solver keeps the declared bounds.

   A traversal of every source node, done before any simplification, proves
   each partial-function domain from these bounds and from proportional
   affine rows. Domains it cannot prove are kept by exact existential
   constraints: `du=1` for `d!=0`, `du=1` with `u>=0` for `d>0`, and `d>=0`.
   A variable power `b^e` becomes `exp(e log b)`, but only after `b>0` is
   proved; otherwise the model is refused. All modes share these constraints
   and the objective epigraph.

2. **Discovery** (`integration.py:discover`). Discovery runs at the first root
   separation callback, so a model solved in presolve pays nothing. Each
   finite side of an original row (and the objective epigraph side) is written
   exactly as `h_r(x) + d_r^T v <= b_r`, where `h_r` is the complete nonlinear
   remainder. A side is admissible if `h_r` has 1 to 4 variables, all with
   finite proved bounds, and is univariate or a polynomial of total degree at
   most 8. A block is either one side's variable set or a greedy union of
   overlapping sides of at most four variables. It carries up to six such
   sides and up to 16 original affine sides supported on its variables, which
   serve as domain rows. Discovery checks its time allowance between rows,
   additive terms, and group steps. On expiry it discards its partial result
   and the separator stops.

3. **Direction search** (`integration.py:propose_direction`, `RowSeparator`).
   For each block the separator first tries the support of each single
   source side. It then solves up to three HiGHS LPs over a finite sample of
   the block graph:

   - free normals for the coordinates, scaled into [-1,1];
   - nonnegative side multipliers in [0,1];
   - a free intercept.

   Each exact support minimizer is added to the sample before the next LP.
   Samples, their numerical row filtering, and the LP choose directions only.

4. **Exact support and export** (`support.py`, `certified.py`,
   `quadratic_polytope.py`, `quadratic_star.py`, `row_certificate.py`).
   For the actual binary64 direction `(a, lambda)`, the support kernel
   certifies `a^T x + sum_r lambda_r h_r(x) >= beta` on the block box and
   domain rows. Quadratic blocks with d <= 4 use exact enumeration of
   bordered stationary systems, under a 2,000-subset budget in the callback.
   Beyond the budget, the inherited kernels apply: the exact center-leaf star
   oracle, exact Bernstein subdivision in one or two variables, or Arb ball
   enclosures for univariate elementary functions. A kernel either returns a
   whole-domain certificate or no cut.

   The row module then eliminates the source sides exactly, which gives
   `C^T v >= R` with `C = a - sum_r lambda_r d_r` and
   `R = beta - sum_r lambda_r b_r`. It rounds `C` to binary64 and adds the
   exact correction `sum_i min(e_i L_i, e_i U_i)` for the rounding errors
   `e`. It requires both proved bounds for every coordinate with a nonzero
   error, and rounds the rhs downward.

   A cut is offered only if its violation at the LP point, divided by
   `max{1, sum_j |c_hat_j|}`, exceeds 1e-5 (`all`) or 5e-4 (`auto`). Before
   submission, the separator reads SCIP's stored row back. It requires exact
   agreement of columns (through the original-to-transformed variable map),
   coefficients, constant, lower side, infinite upper side, and global scope.
   Otherwise it releases the row.

5. **Replay** (`experiments/replay.py`). Replay runs in a fresh process
   against the archived source snapshot. It verifies the source-file hashes,
   the pinned OSiL file, and the serialized binary64 model. It replays the
   bound certificate and rebuilds the native model metadata and domain
   constraints. It then reconstructs every signed source side from the
   original rows with its own affine splitter. For each cut it re-runs the
   exact support check on the source-derived features, box, and domain rows
   with the recorded binary64 direction, and recomputes elimination and
   rounding from these trusted inputs. Finally it compares the recorded
   stored SCIP row with the exported certificate. Fourteen tampering controls
   check that replay rejects altered inputs.

**What is trusted.**

- Python's `fractions` arithmetic.
- SymPy expansion and rational polynomial conversion.
- python-flint/Arb ball arithmetic.
- The OSiL reader's mapping from decimal tokens to binary64.
- PySCIPOpt's accessors for submitted expressions and stored rows.
- The shared exact kernels, which replay re-executes. This is re-execution,
  not an independent or formally verified checker.

**What is not trusted** and carries no proof obligation: HiGHS, NumPy
sampling, floating-point filtering, and all work-selection heuristics.

**What is outside the claim**: SCIP presolve and simplification, LP and
feasibility tolerances, SCIP's later handling of a submitted row, the
numerical primal and dual bounds, and the decimal meaning of OSiL tokens.

Report A uses the same certificate kernels and import binding with a
different integration. It defines an auxiliary `w = f(x)` for each admitted
atom of one or two variables. These auxiliaries are enforced natively and
protected from aggregation in the `control`, `all`, and `auto` modes. Its
cuts are in original plus auxiliary variables, so no elimination step is
needed. Its `auto` mode may skip a block when the exact convex-combination
screen bounds the possible scaled violation by 5e-4.

### 5.2 Appendix: exact limits used in the experiments

| Setting | Report A campaign-v1 (316 runs) | Report B campaign-v2 (282 runs) and repair cohort (75 runs) |
|---|---|---|
| Source | `A/solver/integration.py` `6a972944...` | campaign-v2 `5620d3f2...`; repair `128fe10b...` |
| Modes | baseline, control, all, auto (+ 10 `cache_samples=False` and 2 `merge_stars=False` ablations) | baseline, all, auto |
| Soft budget per run | 6 s full; 2 s with node limit 1 (root) | 30 s full; 10 s synthetic mechanisms; 5 s with node limit 1 (root) |
| Hard process limit | 20 s | 45 s / 20 s / 15 s by phase |
| SCIP | 1 thread, `limits/gap=1e-4`, seed shift 0 (seed 1 in repeats) | same |
| Threads | `OMP/OPENBLAS/MKL/NUMEXPR/BLIS/VECLIB=1`, one worker at a time | same |
| Separator allowance (cumulative per run) | min(2 s, 0.15 x budget): about 0.9 s full, 0.3 s root | min(1 s, 0.05 x budget): about 1 s full, 0.5 s mechanisms, 0.25 s root |
| Root callbacks | 5 | 3 |
| Total cuts / per callback | 24 / 6 | 12 / 4 |
| Support calls per run | not capped separately | 24 |
| LP exchange rounds | 3 per block search | 3 per block per callback (after single-side directions) |
| Discovery caps | 256 atoms, 64 blocks, 8 coordinates per block, degree 8 (1 variable) / 4 (pair), stars with 2-4 leaves | 32 blocks, at most 4 variables, 6 nonlinear sides, 16 affine domain sides, polynomial degree at most 8, nonpolynomial only if univariate |
| Exact quadratic oracle | 2D polygon (any number of rows); star (d >= 3, center-leaf rows) | d <= 4 polytope enumeration, at most 2,000 subsets; then v1 kernels |
| Subdivision kernels | 128 cells, depth 16, 128-bit Arb precision, Bernstein in 1-2 variables with at most 1,024 coefficients, powers at most 32 | same |
| Sampling | 65-point 1D grid, 13x13 2D grid, 128 Halton points + corners for d >= 3; HiGHS 0.1 s | 33-point 1D grid, 7x7 2D grid, 3^d for d = 3, 4, plus exact vertices and centroid; HiGHS 0.05 s |
| Violation threshold (scaled) | 1e-5 all, 5e-4 auto | 1e-5 all, 5e-4 auto (divided by max{1, sum abs(c_hat)}) |
| `auto` admission | univariate block with at least 2 atoms or a composite atom; pair with a retained affine row; star; stop after 2 failures; exact screen | quadratic block with a side not proved convex and (non-axis domain row or at least 2 source rows); stop after 2 failures |
| Exported cut type | global, root, removable, `forcecut=True` | same |
| Recorded cuts / replayed | 1,082 / 1,082 (8 missing logs) | 123 / 123 (4 missing logs); repair 42 / 42 |
| Tampering controls rejected | 12 / 12 | 14 / 14 in each campaign |
| Admission refusals | 36 `source_model_mismatch` records | none (the 4 `worker_error` records were discovery crashes after successful import) |

## 6. Experiment-record facts used above

These come from read-only scans of the archived JSONL records.

- **campaign-v2.** 282 records (94 per mode). Statuses: 106 optimal, 74
  gaplimit, 31 timelimit, 67 nodelimit, 4 `worker_error`. One configuration.
  123 cuts with largest `abs(rhs)` 85. Separator totals over cut-mode runs:
  418 support calls, 70 certification failures, 597 `auto` selection skips,
  8 row-binding rejections, and 0 row-rounding rejections. Three admitted
  runs (one model, three modes) carried two domain guards; all others had
  none.
- **repair-discovery-v1.** 75 records. Statuses: 15 optimal, 12 gaplimit, 21
  timelimit, 27 nodelimit. 42 cuts. Six runs reported
  `discovery_incomplete`. No callback overran its allowance by more than
  0.03 s.
- **Report A campaign-v1.** 316 records. Statuses: 162 optimal, 42 gaplimit,
  12 timelimit, 56 nodelimit, 36 `source_model_mismatch`, 8 `worker_error`.
  1,082 cuts. No callback time above 2.05 s.
