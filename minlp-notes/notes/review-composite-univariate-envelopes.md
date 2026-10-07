# Review: composite univariate envelopes (note and code)

Date: 2026-09-21. Reviewer: independent agent. Scope:
`results/composite-univariate-envelopes.md` (all sections except the
placeholder "Computational evidence") and `code/univariate_envelopes/`.
No existing file was modified. All checks were targeted; no project-wide
suite was run and CI was not inspected.

## Verdict

No soundness bug was found that changes a reported optimal value or bound.
Propositions 1–3 are correct as mathematical statements, and the arithmetic of
Example 4 is exact. A randomized stress test (440 random expressions, 5 760
cut checks and about 8 600 direct `_inner` checks against dense sampling)
found no line that exceeds `g` by more than `4e-15` relative. On 26 small
applicable MINLPLib instances the hybrid and native modes agree with each other and with
`instancedata.csv` within solver tolerances, and none of the 237 existing
sweep records has a dual bound beyond the reference primal bound or a primal
value beyond the reference dual bound at `1e-4` relative.

The note should not be published as is, for three reasons:

1. The local/global cut flag has a latent validity bug (finding 1). It has a
   function-level reproducer. I could not trigger it through SCIP on the test
   instances, but the fix is one line.
2. The curvature certificate does not check that `g` is defined on the
   interval (finding 2). Today this ends in an exception or a hang, not in a
   wrong cut, but the note states a stronger guarantee than the code gives.
3. The wording "exact", "certified" and "rigorous" is stronger than what the
   code guarantees (finding 9).

The remaining findings are tolerance-level effects, robustness problems and
wording.

## Findings

### 1. Global cuts can be computed on local bounds (should-fix; latent soundness bug)

Evidence. `scip_plugin.py::_cut` computes the cut on the local interval
`[l, u]` and sets
`is_local = l > lbGlobal + 1e-9 or u < ubGlobal - 1e-9`. The slack is
absolute. When `is_local` is false the cut is still computed on `[l, u]`, not
on the global interval. Two consequences:

- A variable whose global domain is of order `1e-9` to `1e-8` gets every node
  cut flagged global. Reproducer (function level):
  `f = Univariate(-(1e9*X)**2, 0, 1e-9)`, node interval `[0, 5e-10]`:
  `is_local` is `False`; `f.under(0, 5e-10, 2.5e-10)` gives a line with value
  `-0.5` at `x = 1e-9`, where `g = -1`. The cut removes the feasible point
  `(1e-9, -1)` by `0.5`.
- With a normal scale the error is `1e-9` times the slope difference. For
  `g = 1/x` on the global interval `[1e-4, 1]` and local lower bound
  `1e-4 + 5e-10`, `is_local` is `False` and `f.over(l, u, l)` gives
  `9999.950005` at `x = 1e-4`, where `g = 10000`. The cut-off is `0.05`, or
  `5e-6` relative, above SCIP's feasibility tolerance.

SCIP rarely accepts bound changes this small, which is why the sweeps do not
show it. It is still a wrong flag.

Correction. When the interval is not flagged local, compute the cut on the
global interval:
`if not is_local: l, u = max(lbGlobal, f.lo), min(ubGlobal, f.hi)`.
Alternatively set `is_local = (l > lbGlobal or u < ubGlobal)` with no slack.

### 2. The curvature certificate does not certify that `g` is defined or `C^2` (should-fix)

Evidence. `certify_pieces` looks only at the ball enclosure of the symbolic
second derivative. Sympy's derivative can have a larger domain than `g`:

- `certify_pieces(log(X), -2, -1)` returns one piece labelled `concave`,
  because `g'' = -1/X**2` is finite and negative there. The same holds for
  `X*log(X)` on `[-2, -1]`. `Univariate(...).range` then raises
  `ValueError: math domain error`. `build_scip` catches it and keeps the
  subtree native, so no wrong cut results. `add_univariate` in standalone mode
  does not catch it.
- Sympy simplification changes the domain before certification:
  `sqrt(X)**2 + exp(X)` becomes `X + exp(X)` and is certified convex on
  `[-1, 1]`. In hybrid mode this is harmless, because the relaxation is over a
  superset and the native constraint guards feasibility. In standalone mode
  the handler would accept points where the original `g` is undefined.
- Poles and domain boundaries inside the interval are rejected correctly:
  `1/(X-1)` on `[0, 2]` and `[0, 3]`, `1/(X**2-2)` on `[0, 3]`, `tan(X)` on
  `[0, 3]`, `log(X)` on `[0, 1]`, `log(X**2)` on `[-1, 1]`, `exp(-1/X)` on
  `[0, 1]` all raise `ValueError: cannot enclose expression`. `log(X)` on
  `[-1, 1]` raises an uncaught `TypeError: Cannot convert complex to float`
  from `range_enclosure` (`float(at)` on a complex value).
- python-flint comparisons behave as required: `arb(0,1) >= 0` and
  `arb(0,1) <= 0` are both `False`; NaN balls are not finite. `_ball(a, b)`
  is a true enclosure because of the two `union` calls (20 000 random
  intervals, 0 failures). The merge logic is correct: the stack pops the left
  half first, so pieces arrive left to right and adjacent.

I did not find a discontinuous or undefined `g` that yields certified pieces
and a wrong cut. The protection is accidental: it comes from the later float
evaluation raising an exception.

Correction. In `certify_pieces`, require a finite ball enclosure of `g`
itself (not only of `g''`) on every piece before it is labelled convex or
concave. State in the note that the certificate covers the sympy-simplified
expression.

### 3. Certification can hang (should-fix; robustness)

Evidence. `certify_pieces` treats every `ValueError` from `ball_eval` as
"undecided" and bisects down to width `1e-7 (U-L)` with no cap on the number
of pieces. Reproducers that do not finish in 20 s (they would create about
`1e7` pieces):

- `certify_pieces(X**2*log(X), -1, -0.5)` (`g''` contains `log`, NaN
  everywhere);
- `certify_pieces(Abs(X)**3, -1, 1)` (`g''` contains `sign`, for which
  `ball_eval` raises "unsupported function"; the same error class is used for
  an unsupported operator and for a failed evaluation).

Ill-conditioned expanded polynomials degrade in the same direction:
`expand((X-100)**4 - (X-100)**2)` on `[98.5, 101.5]` gives 983 pieces, and
`expand((X-30)**6 - (X-30)**2)` on `[29, 31]` did not finish in 110 s.
The OSiL path excludes `abs`, so the first kind needs a variable whose
presolved interval lies in the undefined region. During this review I also
saw a sweep process (`ann_cumene_exp`, hybrid, `--tl 120`) with 47 CPU
minutes; I did not investigate the cause. `eg_int_s` in hybrid mode did not
finish building in 150 s; the traceback shows the time is spent in sympy
`diff` for several hundred candidates.

Correction. Raise a distinct exception for unsupported functions; cap the
number of pieces (for example 2 000) and reject the function beyond it; apply
a build time budget.

### 4. The function domain comes from a separate presolve and is not imposed on `x` (should-fix; tolerance level)

Evidence. `presolved_bounds` sets `misc/allowstrongdualreds` and
`misc/allowweakdualreds` to `False` before `presolve()`. Both parameters
exist in SCIP 10 (default `True`). Three probes showed no optimality-based
tightening: a linear objective whose trivial all-lower-bound solution is
optimal; a separable problem with independent components; an integer problem
with a linear objective. Bounds stayed at the declared or
feasibility-implied values (`x <= 1.904` from `x^4 - x^2 <= 5.25`, which is
valid and loose). I could not prove that no SCIP plugin ignores the two
flags; I only tested.

The hybrid model keeps the declared bounds on `x`, while cuts, the bounds of
`w` and propagation use `[f.lo, f.hi]`. `_propagate` returns `CUTOFF` when
the local interval of `x` lies outside `[f.lo, f.hi]` by any amount, and
cuts are valid only on `[f.lo, f.hi]`. SCIP's presolve bounds are not rounded
outwards. A point with `x` outside the domain by `1e-9`, which SCIP accepts
as feasible for the native constraint, can therefore be cut off. In exact
arithmetic nothing feasible is lost.

Correction. Widen a presolved bound that is tighter than the declared one by
a small relative margin (for example `1e-7 max(1, |bound|)`, clipped to the
declared bound) before building `Univariate`, or add the domain as explicit
bounds on `x` in the hybrid model so that the model is self-consistent.

### 5. Proposition 1 holds for the code, up to floating point (minor)

Proof check, branch by branch, for `[l, u]` inside `[f.lo, f.hi]`:

- Concave piece: a concave function on the clipped piece has its minimum at
  an endpoint. Correct.
- Convex piece: if `da < 0 < db`, the bound
  `phi(x0) - |phi'(x0)| (b - a)` is valid for any `x0` in `[a, b]`, so it
  does not depend on Brent's accuracy. Otherwise the minimum of a convex
  `phi` is at the endpoint where the derivative sign says so, and the code
  takes the smaller endpoint value, which is not larger. If the float signs
  of `da`, `db` are wrong by rounding, the error is at most
  `|phi'| (b - a)` with `|phi'|` at rounding level.
- Unknown piece: `min (g - s x) >= glo - max(s a, s b)` for either sign of
  `s`. For `sign = -1` the code builds pieces with `glo = -ghi`,
  `ghi = -glo` and swapped labels. Correct. `glo` refers to the unclipped
  piece, which is weaker but valid.
- `_dg_safe` with `±1e300` only influences the slope bracket and the branch
  choice on convex pieces. A piece with a finite `g''` enclosure has a finite
  `g'`, so the value is not used where validity depends on it.
- `u - l <= 1e-12` branch: returns slope 0 and
  `min(g(l), g(u)) - 1e-11`. This is exact only if `g` is monotone on the
  interval. The safety shift is absolute here, while it is relative
  elsewhere. For `|g| >= 1e5` the float error of `g` exceeds `1e-11`.
- `range()` is `h(0)` for `g` and `-g` with the rigorous unknown-piece
  bounds, shifted outwards. It is a valid outer enclosure.
- `under`/`over` do not check `[l, u]` against `[f.lo, f.hi]`. A caller that
  passes a wider interval gets a line that ignores the uncovered part. The
  plugin clips correctly; an `assert` would make the contract explicit.

The safety shift is relative to `|h|`, not to the condition number of the
float evaluation of `g`. I tried to break this with expanded shifted
polynomials and exact rational comparison
(`expand((X-c)**4 - (X-c)**2)`, `c` in `{3, 10, 40, 100}`). No violation
occurred, because the ball enclosures degrade first and the affected region
turns into unknown pieces with rigorous bounds (the computed lower range for
`c = 100` is `-3.02` against the true `-0.25`: weak but valid). I have no
reproducer, so this stays minor.

Correction. Use a relative shift in the tiny-interval branch. Add the
interval assertion. Say in the note that Proposition 1 is a statement in
exact arithmetic, given correct piece labels and `[l, u]` inside `[L, U]`.

### 6. Singular endpoints work only at `0` (minor; note wording)

Evidence. `certify_pieces(X**0.6, 0, 1)`, `sqrt(X)` and `X**1.5` on `[0, 1]`
succeed with an unknown piece `[0, 6e-8]`. A shifted singular endpoint fails:
`Univariate((X+4.5)**0.6, -4.5, -2.8)` raises `cannot enclose expression on
[-4.5, -4.4999999]`; 80 of the random stress cases with a singular endpoint
at `-4.5` were rejected this way. The cause is in `range_enclosure`:
`lo = end + (other - end) * 2**(-k-1)` rounds to `end` after about 28 steps,
and the piece `[end, hi]` contains the singular point. The result is safe
(the function is rejected), but the note's "singular endpoints such as
`x^0.6` at `0`" describes the only case that works.

The start value `arb(float(at))` is a rounded point, not an enclosure of
`g(end)`, and continuity on the sliver is assumed. The note states the
continuity assumption correctly. The sliver length `2^-60` is relative to the
unknown piece, not to `[L, U]`.

Correction. Stop the dyadic loop when `lo == end` and take the union with the
endpoint value, or describe the restriction in the note.

### 7. Standalone enforcement fallback is not exact (minor; standalone mode only)

Evidence. When every violated constraint has
`u - l <= 1e-9 max(1, |l|, |u|)`, `_enforce` fixes `x` to the LP or pseudo
solution value and lets propagation pin `w`. What is lost: every point with
`x` in `[l, u]` other than that value. Because a violation above the
feasibility tolerance survived on such an interval, `g` varies by more than
`1e-6 max(1, |g|)` across it (a steep region), or cuts were not allowed
(`consenfops`, or the 12-cuts-per-node limit). The objective can then change
by that variation, and a constraint that needs another `x` inside the
interval makes the node infeasible. This matches usual solver practice but
is not rigorous. The note does not mention it.

Correction. State it under "Limitations".

### 8. Hybrid mode: feasibility is guarded by the native constraint (no bug)

`conscheck` returns `FEASIBLE` in hybrid mode. Every solution, including the
one from `_try_completion` (`trySol` with `completely=False`, all checks on),
is still checked by SCIP's nonlinear handler on `w == g(x)`, so no solution
that violates the native constraint is accepted. The hybrid model has the
native feasible set and objective: `w` is defined by a native equality, its
bounds are `range(f.lo, f.hi)`, and the objective reformulation with `objvar`
is the same in both modes. The only way the handler removes a native-feasible
point is finding 4 (tolerance level) or finding 1.

Propagation. Tightening `w` to `range(l, u)` and trimming `x` where the range
misses `[wl, wu]` are valid. The `1e-9 max(1, |w|)` slack is on the safe side
(fewer cut-offs, less trimming). `wl`, `wu` are read before `w` is tightened,
which is weaker but valid. Points that SCIP accepts with a violation between
`1e-9` and `1e-6` can be trimmed; exact feasible points cannot.

`_initial_cuts` uses global bounds and is valid wherever it is called.
Locks are set in both directions for both variables.

### 9. Wording overclaims (should-fix; note)

- Title and summary: "Exact certified envelopes". What is certified is the
  sign of the symbolic `g''` on pieces. Cut coefficients come from float
  evaluation with a fixed shift, the slope search stops at a tolerance,
  slopes are capped, and unknown pieces make the result an outer
  approximation. The note admits this in one sentence ("not a verified
  numerical code"); the title, the summary ("propagate with the exact range",
  "separate the exact ... envelopes") and "The exact range of `g` is
  `[h(0), -h_{-g}(0)]`" do not. Suggested wording: "envelopes that are exact
  up to certified slivers and floating-point safety margins"; "range"
  instead of "exact range" unless Proposition 2's hypothesis is repeated.
- "Let `g` be ... `C^2` on `[L, U]`" is an assumption the code does not
  verify (finding 2). Say so, or fix the code.
- "Unknown intervals appear only around inflection points and at singular
  endpoints": they also appear wherever the ball enclosure of `g''` is too
  wide to decide (finding 3: 983 pieces for a shifted quartic).
- Detection: "a polynomial written as separate monomials is recovered" holds
  only for monomials inside the `<nl>` tree. MINLPLib OSiL files store
  quadratic and linear parts of some rows separately
  (`st_e19`, `hs62`, `ex4_1_8` have `quadraticCoefficients`); the reader does
  not merge those into the univariate function. In `st_e19` the objective
  polynomial is complete inside `<nl>`, but constraint row 1 has
  `-x1^2` (variable index 0) in the quadratic section.
- "140 of the 744 MINLPLib instances": the scan confirms 140 of 744, but 38
  of 1 632 files were not parsed (31 unsupported operators such as `erf`,
  `signpower`, `tanh`, `log10`, `min`; 7 too large), and only 115 remain
  applicable after the bound and certification filters. Give all three
  numbers.
- "local when the node interval is smaller than the global one": see
  finding 1.
- Proposition 3: the statement with `min(m, n)` largest `rho_i` is the
  Udell–Boyd form. As far as I remember, Aubin–Ekeland give a bound with
  `m + 1` terms; I could not check either text. Attribute the stated form to
  Udell–Boyd and cite Aubin–Ekeland as the origin. Add the hypotheses:
  `g_i` lower semicontinuous on compact intervals, feasible problem, and `m`
  counts linear rows only, not the box.
- Literature: the claim is qualified ("to our knowledge", "an unsuccessful
  search does not establish novelty"), which is appropriate. "certified" in
  the claim needs the restriction above. I could not verify
  arXiv:2604.03871, the SCIP 10.1 Lennard-Jones handler, or the Gurobi 13
  deprecation statement.

### 10. Example 4 and Propositions 2–3 (no error)

`g = x^4 - x^2` on `[-1, 1]`: the secant of `-x^2` is `-1`; the term-wise
relaxation is `min sum (x_i^4 - 1)` with value `-n` at `x = 0`. The minimum of
`g` is `-1/4` at `x = ±1/sqrt(2)`; for even `n` balanced pairs give `-n/4`.
The term-wise gap is `3n/4`. The envelope equals `-1/4` on
`[-1/sqrt(2), 1/sqrt(2)]` and `g` outside, so the envelope relaxation has
value `-n/4` at `x = 0`, which is exact for even `n`. `rho = g(0) + 1/4 =
1/4`, so Proposition 3 gives `1/4` for `m = 1`. The code reproduces the
envelope: `under(-1, 1, x)` gives `-0.25 - 1.25e-11` for `x` in
`{0, 0.3, -0.7}` and the tangent value at `0.9`. For odd `n` the relaxation
is not exact; the note's "for even `n`" covers this, and the sentence "so the
envelope relaxation is exact here" should repeat the qualifier.

Proposition 2 is the standard biconjugate statement and is correct: if
`x*` lies in the convex hull of `argmin phi_s`, the line `s x + h(s)` touches
`g` on both sides of `x*`.

### 11. OSiL reader (no error found; small gaps)

Native mode against `instancedata.csv` (30 s, gap `1e-4`): `ex4_1_1`,
`ex4_1_2`, `ex4_1_3`, `ex4_1_6`, `ex4_1_7`, `ex8_1_1`, `ex8_1_2`, `nvs01`,
`nvs08`, `st_e19`, `st_e04`, `hs62`, `ex1226`, `ex4_1_9`, `ex14_1_9`,
`mathopt5_{1,3,5,7}`, `mathopt6`, `trig`, `ex6_1_4`, `inscribedsquare01`
(max) match the reference primal bound within solver tolerances;
`ex6_2_10`, `ex6_2_12`, `ex6_2_14`, `ex8_5_5`, `eg_int_s` hit the time limit
with consistent bounds. `st_e36` found no solution in 30 s in native mode
(120 000 nodes). The file parses as expected (degree-10 equality), so I
attribute this to SCIP, but I did not verify the reader on it.

Checked by reading: default `lb = 0`, `ub = INF` (`1` for binaries);
objective constant (`ex4_1_1` has `constant=".1"`); `maxOrMin`; `qTerm` as
`coef * x_i * x_j` for both `i == j` and `i != j`, which is the OSiL
convention; `minus`, `negate`, `variable coef`, `mult`/`incr`; non-integer
`power` exponents are passed as floats to SCIP and as sympy `Float` to the
certifier. No MINLPLib file uses semicontinuous types. Gaps: instances
without an objective (`camcns`, `gancns`, `korcns`) would call
`setObjective` with a float; variable types other than `C`, `B`, `I` are
silently read as continuous.

`collapse`: grouping same-variable summands only reorders a sum, so it is an
identity. `abs` is excluded both at the top-level test and in the grouping.
`nonlinear_ops` counts a `times` node once regardless of the number of
variable factors, and counts `power` with exponent 1 as nonlinear; neither
affects validity.

### 12. Hybrid against native on applicable instances (no disagreement)

26 applicable instances, 30 s, gap `1e-4` (`eg_int_s` was also started, but its
hybrid build did not finish in 150 s; see finding 3). In no case is the hybrid dual bound above the
reference primal bound beyond `1e-8` relative, and no hybrid primal value is
better than the reference dual bound beyond solver tolerance. Two cases
looked suspicious and were resolved:

- `inscribedsquare01` (max): native reports `0.9900770`, hybrid proves
  `0.9900754` as optimal. Restricting all variables to the native solution
  `± 1e-4` and solving to gap 0 gives `0.99007480` (native) and `0.99007478`
  (hybrid). The native value is a feasibility-tolerance artefact of the eight
  equalities; the reference primal bound is `0.990074741`.
- `ex6_1_4`: native `-0.2945467` and hybrid `-0.2945491` are both better than
  the reference primal `-0.2945413` by about `2e-5` relative. Both modes
  show it, so it is a tolerance effect of the instance, not of the handler.

Performance observations for the experiment record: `mathopt6` takes 25 s in
hybrid mode against 0.1 s native (37 nodes, 121 cuts). `root_dual` is `1e+20`
for hybrid runs that finish in one node (`ex4_1_1`, `ex4_1_2`, `ex4_1_7`,
`ex8_1_2`, `ex1226`), so root-gap tables must not use that field for them.

## Commands run

All from `code/univariate_envelopes`, with `PYTHONPATH=$PWD` and the prefix
`uv run --project /workspace/minlp-notes/code/minlp_solver_lab python`
(abbreviated `PY`). Helper scripts were written to `/tmp/rev/` only. At most
two processes ran at a time.

- `PY /tmp/rev/t1b.py`: python-flint comparison semantics, `_ball` enclosure
  test (20 000 intervals), and `certify_pieces` on the singular cases of
  finding 2, 3 and 6, each with a 20 s alarm.
- `PY /tmp/rev/stress.py 1 40 80` and `PY /tmp/rev/stress2.py 7 400 500`:
  random expressions from polynomials, `exp`, `log`, `sin`, `cos`, fractional
  powers and quotients; random intervals (widths `1e-3` to `6`), random
  subintervals including widths `1e-11` to `1e-4`; `under`/`over` at four
  points per subinterval, `_inner` for random slopes and both signs, and
  `range`; each compared with 4 001 samples plus piece endpoints. Result:
  0 violations above `1e-9` relative; worst excess `3.6e-15`.
- `PY /tmp/rev/cancel.py c` for `c` in `3 10 40 100`: exact rational check of
  under-cuts for expanded shifted quartics. Result: excess 0.
- `PY /tmp/rev/presol.py`: three probes of `presolved_bounds` and the two
  parameter names.
- `PY run_minlplib.py /tmp/minlplib/minlplib/osil/<name>.osil <mode> --tl 30`
  for `mode` in `native`, `hybrid` and the instances listed in findings 11
  and 12 (one stream per mode).
- `PY /tmp/rev/cmp.py inscribedsquare01 1e-7` and `... 1e-4`: native and
  hybrid restricted to a box around the native solution, gap 0.
- `PY /tmp/rev/eg.py eg_int_s`: timing of `presolved_bounds` and the hybrid
  build with a traceback after 80 s.
- `PY /tmp/rev/loc.py`: the two function-level reproducers of finding 1.
- `PY -m pytest -q -p no:cacheprovider test_envelope.py`: 1 passed.
- A read-only pass over `results/minlplib_v1.jsonl` and
  `results/minlplib_v2.jsonl` (237 records with a reference) comparing dual
  and primal values with `instancedata.csv` at `1e-4` relative: no hit.
- A read-only recount of `results/scan.json`: 1 632 files, 1 594 parsed, 744
  with general nonlinear rows, 140 with composites.

## Not checked

- `test_plugin.py`, `run_quartic.py`, `sweep_separable.py` and standalone
  mode under SCIP were read but not run (machine load). Finding 7 is from
  reading the code.
- Finding 1 was not reproduced through SCIP, only at function level.
- Whether some SCIP presolver or propagator ignores the two dual-reduction
  flags; only three probes were run. Symmetry handling was not probed.
- Behaviour across SCIP restarts (cached transformed variables in
  `cons.data`).
- The cited literature, including the exact form of the Aubin–Ekeland bound
  and Udell–Boyd Theorem 1. No web access was used.
- The "Computational evidence" section (placeholder) and the experiment
  record.
- Large instances, and the cause of the long-running `ann_cumene_exp` sweep
  process.
