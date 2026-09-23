# Review: certified lower bounds for convex MINLP (2026-09-12)
**Historical review.** The six corrections described here did not establish soundness of the complete executable. The September 13 audit reproduced an empty-SOL attack against the accepting checker and found additional arithmetic and model-semantics issues. Current repairs and independent reviews are linked in [the repair and replay record](certified-minlp-repair-and-replay.md).

Reviewed: `notes/certified-bounds-20260912-method.md`;
`code/minlp_solver_lab/certify/{convexity,safecut,driver,run_all}.py` as in
the working copy at HEAD `696fad1` (this includes the half-line rule for
one-sided bounds that was added to `safecut.py` / `driver.py` while the
review was in progress; see "Half-line rule" below); the VIPR 1.1
specification and `viprchk.cpp` in `/home/sgusev/build-scip/vipr`.
The OA engine (`lbesh/`) is treated as untrusted, except where the checker
itself imports it (see S2).

Verdict: the overall design (convexity witness + safe rational cuts + exact
MILP + VIPR) is sound in principle and the safe-cut inequality and its
interval implementation are correct for valid inputs. The current
implementation, however, has six blocking defects: two convexity rules are
unsound, the checker does not verify one hypothesis of the lemma (`z` in the
box), the checker never ties the VIPR file to the master LP, the checker's
viprchk acceptance test is wrong, and the `drop_solutions` fallback in
`run_all` is unsound under VIPR semantics. Each is reproduced below; the
first three were demonstrated end to end (a "certified" bound of 2 for a
problem whose optimum is 0).

Adversarial tests were added under `code/minlp_solver_lab/certify/tests/`
(`test_review_convexity.py`, `test_review_safecut.py`; run with
`uv run --with pytest python -m pytest -q certify/tests` from
`code/minlp_solver_lab`; pytest is not in the project environment). 30 pass
and 6 fail on the current code; each failing test documents one of B1-B3
or S5 and should pass after the fixes.

## Blocking

### B1. Checker does not verify `z ∈ B` (lemma hypothesis) — invalid bound certified end to end

`check_certificate` / `_verify_given_cut` (driver.py:420-461) accept any
linearization point `z` from `lemma.json`; nothing checks `L_j ≤ z_j ≤ U_j`.
The supporting-hyperplane inequality `phi(x) ≥ phi(z) + d^T(x−z)` needs
convexity on a convex set containing both `z` and `B`; the rule set only
certifies convexity on the box (e.g. `x**3` for `x ≥ 0`).

Reproduction (artifacts in `code/minlp_solver_lab/certify/tests/review_artifacts/`:
`cube_instance.py`, `cube_lemma.json`, `cube_master.lp`; copy them to a
directory as `cube.py`, `lemma.json`, `master.lp` and run `check_certificate`,
then SCIP exact / viprcomp / viprchk on `master.lp`):

```python
# cube.py
m.x = Var(bounds=(0, 10)); m.y = Var(bounds=(0, 1000))
m.c1 = Constraint(expr=m.x**3 - m.y <= 0); m.obj = Objective(expr=m.y)   # optimum 0
```

lemma: row `c1_ub`, `z = {x: -1.0, y: 0.0}`, `a = {x: 3, y: -1}`, `b = 2`.
At `z`, `d = (3·(−1)² − 3, −1 + 1) = (0, 0)`, so `_verify_given_cut` returns
`b_safe = phi(z) = 2` and accepts `b = 2`. The regenerated LP contains
`cut1: + 3 x - 1 y <= -2` (i.e. `y ≥ 3x + 2`), is byte-identical, SCIP exact
reports dual bound 2, `viprchk` prints "Successfully verified optimal value
range [2, 2]", and `check_certificate` returns `ok = True`. The true
optimum is 0 (`x = y = 0`).

Fix: in `_verify_given_cut`, for every variable of the row require
`lb ≤ z_j ≤ ub` (rational comparison with the checker's box; a variable with
a `None` bound on one side is only constrained on the other side) and
reject the lemma otherwise. The producer should clip `z` to the rational
box before writing it (any `z ∈ B` is admissible, and float LP points may
lie a few ulps outside the box because the model bounds are rounded
outward at driver.py:228-237). Test:
`test_review_safecut.py::test_linearization_point_outside_box_is_rejected`.

### B2. Perspective rule (`_perspective`, convexity.py:544-567) is unsound

The rule replaces every `e / t` node in `g` by `e` and certifies the result
`f`, claiming `t·g = t·f(x/t)`. That identity requires that `t` occurs in
`g` *only* as the denominator of those divisions and that every other
variable occurs *only* inside their numerators. Neither is checked.
Counterexamples (all with `t ∈ [0.5, 1.5]`, `x ∈ [−1, 1]`; verified by
midpoint tests on a grid):

| expression | certify() | truth |
|---|---|---|
| `t * ((x/t)**2 + exp(-t))` = `x²/t + t·e^{−t}` | convex | not convex (`t e^{−t}` is concave for `t < 2`) |
| `t * (exp(x/t) + x)` = `t·e^{x/t} + t·x` | convex | not convex (bilinear term) |
| `t * (x/t + t)` = `x + t²` | affine | convex, not affine |

The first two would let a non-convex row be treated as convex; the third
would let a nonlinear row be classified "affine" by `certify_constraint`.

Fix: after building `f`, require (i) that no variable of `t` occurs in `f`
(`identify_variables(f)` disjoint from `identify_variables(t)`), and (ii)
that every variable occurrence in `g` is inside the numerator of a
division by `t` — walk `g` treating each matched division as a leaf and
reject if any other variable node is reached. Also replace string equality
`_same` by structural equality on the linear representation of `t` (or
restrict `t` to a single variable). Tests: `test_perspective_*`.

### B3. `negative const / positive convex → concave` (convexity.py:230-231) is unsound

`k/g` with `k < 0` is `−|k|·(1/g)`; `1/g` is convex when `g` is positive
*concave* (convex decreasing outer function), not when `g` is convex. So the
rule must require `cb.curv in (AFFINE, CONCAVE)` for both signs of `k`.
Counterexample: `-1/(exp(x)+exp(-x))` on `x ∈ [−1, 1]` is certified
`concave` ("negative const / positive convex"); it is `−sech(x)`, which is
convex near 0. A constraint `-1/(exp(x)+exp(-x)) >= -0.9` (a feasible,
non-convex set) would be accepted as a concave row and cut with tangents of
a non-concave function. Test: `test_negative_const_over_positive_convex`.

### B4. `run_all.drop_solutions` is unsound under VIPR semantics

VIPR allows a derivation with reason `{ sol }`: `OBJ ≤ r` is accepted iff
`r ≥ bestObjectiveValue` (minus 1 for integral objectives), where
`bestObjectiveValue` is the best objective of the *verified* solutions in
the SOL section (viprchk.cpp:1079-1100). SCIP uses this to encode the
cutoff bound; the batch certificate contains three such derivations
(`grep -c "{ sol }" master_complete.vipr` → 3). With the SOL section
present this is sound for the lower bound: the proof shows
`{feasible, OBJ ≤ r} ⊆ {OBJ ≥ lb}`, and the verified solution forces
`lb ≤ r`. With the SOL section removed (`SOL 0`), `bestObjectiveValue` is a
default-constructed `mpq_class` = 0, so *any* `OBJ ≤ r` with `r ≥ 0` is
accepted without justification, and an absurdity derived from it dominates
any bound.

Reproduction (`certify/tests/review_artifacts/bogus2.vipr`): problem `min x, x ≥ 1`
(optimum 1), `RTP range 1000000 inf`, `SOL 0`, derivations
`D0 L 0 OBJ {sol}`, `D1: 0 ≥ 1 {lin 2 0 1 1 -1}`, `D2 G 1000000 OBJ {lin 1 2 1}`.
`viprchk` prints "Successfully verified optimal value range [1000000, inf)".

`run_all.run_instance` falls back to exactly this (drops SOL, sets the
RTP upper end to `inf`) whenever the with-SOL check fails, and then reports
the result as certified. Fix: do not drop the SOL section; treat a failed
with-SOL `viprchk` as a failed certificate. If a SOL-free mode is wanted,
the checker must parse the DER section and require, for every `{ sol }`
derivation `OBJ ≤ r`, that `r ≥ lb` (`r + 1 ≥ lb` suffices when viprchk
establishes objective integrality) — simplest is to reject any `{ sol }`
reason when the SOL section is empty.

### B5. The VIPR file's problem is never compared with the master (docstring claims otherwise)

driver.py:16-20 says the checker performs "a check that the VIPR problem
section matches the LP"; `check_certificate` only runs `viprchk` on
`certdir/master.vipr` (driver.py:407-413). Consequently:

- Replacing `master.vipr` in the batch directory by `bogus2.vipr` (problem
  `min x, x ≥ 1`) gives `check_certificate(..., viprchk=...)["ok"] == True`.
- The certified value (`RTP` lower end / viprchk's verified range) is not
  read by the checker at all; `run_all` takes it from viprchk's stdout for
  the file it ran, and calls `check_certificate(inst, outdir)` *without*
  `viprchk`, after renaming `master.vipr` to `master_verified_raw.vipr`. So
  the "independent checker" never looks at any VIPR file in the pipeline.
- The link LP → VIPR relies on SCIP having read `master.lp` and written
  the same problem; that is exactly what the certificate should make
  unnecessary.

Fix (prototype in `certify/tests/review_artifacts/vipr_compare.py`, ~80
lines, run on batch, on the
`cube` attack, and on the bogus file): parse `VAR` (strip SCIP's `t_`
prefix), `INT`, `OBJ`, `CON`; build the multiset of
`(sense, rhs, sorted (var, coef))` triples from the VIPR `CON` section and
from the regenerated rational data (linear rows split into `G`/`L`/`E`,
cuts as `L −b`, finite bounds as singleton `G`/`L`, `objconst` as `G 1`/`L 1`),
and require multiset equality (extra VIPR constraints would make the VIPR
problem more constrained and are as dangerous as missing ones); require
equal variable sets, integer sets, objective vector and sense `min`. For
the batch artifact all 234 constraints match exactly (SCIP writes rows first
and bound constraints after them, contrary to the spec's ordering rule, so
do not rely on `b` in `CON m b`). Then read `RTP range lb ub` and report
`lb` as the certified value; the checker should run `viprchk` on the
completed file it just compared (`master_complete.vipr`, after
`canonicalize_fractions`), and `run_all` should pass `viprchk` to it.

### B6. `check_certificate` accepts a failed viprchk run

driver.py:412 accepts if `"success" in out.stdout.lower()`. viprchk prints
"Successfully checked solution for feasibility." *before* the DER section
is checked. `certify/tests/review_artifacts/badder.vipr` (valid SOL, bogus derivation
`D0 G 5 OBJ {lin 1 0 1}` for `min x, x ≥ 1`) prints that line, then
"Failed to derive constraint D0 / Verification failed."; the checker reports
`('viprchk', '', 'OK')` and `ok = True`. Fix: accept only
`"Successfully verified optimal value range"` (as `run_all` does) and parse
the range; also check the exit status.

## Should fix

### S1. The "as read" semantics is not what is implemented

The note certifies "every numeric coefficient … the exact rational value of
the double". The pipeline instead certifies the problem *after* floating
point folding in three places, and the checker inherits all three:

1. `generate_standard_repn(compute_values=True)` accumulates coefficients in
   floats: `0.1*x + 0.2*x` gives `0.30000000000000004`, which differs from
   the exact `0.1_d + 0.2_d` by `2^-55`; products with fixed variables or
   mutable parameters (`0.1*f*x`, `f` fixed to 0.3) are float products.
   Curvature consequence:
   `0.1*x*x + 0.2*x*x - 0.30000000000000004*x*x + x` is certified
   `affine` (Q = 0 after folding) although its exact as-read `x²`
   coefficient is `−2^-55` (concave).
2. `sympyify_expression` (used by `SafeCutter` for `g` and its gradient)
   auto-folds `Float` coefficients at 53 bits (`exp(0.1*x + 0.2*x)` →
   `exp(0.3*x)`), and applies identities such as `sqrt(x)**2 → x`,
   `exp(log(x)) → x` (value-preserving on the domain, but the enclosed
   function is no longer the Pyomo expression).
3. `lbesh.structure._classify_constraint` computes the row constant
   `const - ub` / `lb - const` and negated coefficients in floats; the
   checker then treats `Fraction(row.const)` as exact. When rounding goes
   the wrong way (e.g. `const = -1e-20, ub = 1` gives `-1.0` instead of
   `-1 - 1e-20`) the intercept `b` is too large by that amount, so the cut
   is invalid for the as-read row by ~1 ulp.

Effects are ~1e-16 relative, but the certificate's claim is exact, so the
gap should be closed or the claim weakened. Recommended: define the
certified object as the Pyomo expression tree after Python-level constant
evaluation (that is unavoidable: `2*0.1` is 0.2_d before Pyomo sees it)
and make everything after that exact: (a) a small exact linear walker (or
`compute_values=False` plus rational evaluation of coefficient expressions)
for rows, objective and the `g + l^T x + c` split; (b) build the sympy
expression with `sympy.Rational(Fraction(float))` constants and
`evaluate=False`, or evaluate the *Pyomo* expression directly with an
interval walker instead of going through sympy; (c) exact rational row
constants. If this is not done, state in the method note that the certified
problem is the float-folded one and quantify the perturbation.

### S2. The checker's trusted base includes `lbesh`

`check_certificate` imports `lbesh.structure._classify_constraint`, `NLRow`
and `lbesh.nlfunc.NLFunction` (which lambdifies through numpy and evaluates
the expression on construction) to obtain the `g + l^T x + c` split and the
variable order of every nonlinear row. This is deterministic re-derivation
from the instance, so a corrupted *lemma file* cannot exploit it, but the
lbesh code is now part of the checker's TCB, contrary to the stated
threat model. Inline the split into `certify/` (it is ten lines with
`generate_standard_repn`, or the exact walker from S1) and drop the lbesh
import from the checker.

### S3. Interval precision claim is false; `mpf_to_frac_down` is not a downward conversion

`mpmath.workdps(60)` changes `mp.prec` only; `iv.prec` stays at 53 bits
(verified: inside the `with`, `mp.prec == 203`, `iv.prec == 53`). All
interval arithmetic in `safecut.py` therefore runs at double precision. It
is still rigorous (outward rounding), so no cut is invalid because of this,
but the method note's "60 digits" is wrong and the lemma slack is
correspondingly larger. Separately, `mpf_to_frac_down` calls
`mpmath.mp.mpf(x)`, which re-rounds to `mp.prec` *to nearest*; it is exact
today only because the endpoints are 53-bit numbers and `mp.prec ≥ 53`. In
`safe_cut` the call is outside the `workdps` block. If someone "fixes" the
precision by setting `iv.prec = 203`, the producer's `b` would be rounded
to nearest at 53 bits (verified: the endpoint changes by ~1.9e-17 in the
test), which can exceed the true bound. Fix: set `iv.prec` explicitly and
convert endpoints exactly from `x._mpi_[0]` (a `(sign, man, exp, bc)`
tuple) without going through `mp.mpf`; delete the unused `_frac_lower`
and `enclosure_from_sympy`.

### S4. Floating range helpers are not rigorous and do feed sign decisions

The note claims "only the rational bounds decide positivity". Not so:
`positive`/`nonneg` of a *sum* uses `lo` values that may come from
`_exp_range`, `_log_range`, `_rpow` (e.g. `1/(exp(x) - 1)`,
`log(x**p - K)`, `sqrt(K - x**p)`). The margins (`1e-12` relative) cover
double rounding for `exp`/`log` and small exponents, but `_rpow` is not an
enclosure for large exponents: for `x = 1 + 2^-60`, `p = 10^7`,
`_rpow(x, p, "up") = 1 + 1e-12` while `x^p = 1 + 8.67e-12`. A wrong `hi`
propagates to a wrong `lo` of `K - x**p`, which can make
`1/(K - x**p)` "positive const / positive concave → convex" on a box that
contains a pole. Also `float(x)` and `math.exp` overflow raise
`OverflowError` (crash, not unsoundness). Fix: compute these ranges with
`mpmath.iv` (rigorous) or with exact rational bounds (`x^(p/q)` bounds via
integer root bounds), and make the method note's statement accurate.

### S5. Monomial rule picks the wrong variable when a zero exponent precedes a unit one

`_monomial_cert` (convexity.py:508-516): `exps` is filtered to drop zero
exponents but `vars_` is not, so `y/y*x` (`x ∈ [−5, 5]`, `y ∈ [1, 2]`) returns
"linear monomial" with the *range of `y`* (`[1, 2]`). A wrong positive
range can then license domain-dependent rules (`log`, `1/·`, negative
powers) on `x`. Filter `vars_` together with `exps`. Test:
`test_monomial_zero_exponent_variable_order`.

### S6. The checker never reports or compares the certified value

Related to B5: `check_certificate` returns `ok` but no bound. It should
return the `RTP` lower end (as a `Fraction`) after the VIPR problem
comparison and `viprchk` succeed, and `run_all` should record *that* value
as `certified_lb` (with `sense` applied) rather than the value parsed from
its own viprchk run.

## Minor

- `rational_bounds` (driver.py:96) raises `TypeError` for a linear row with
  a zero coefficient and a one-sided-unbounded variable (`0 * None`).
- Fixed variables inside a nonlinear row become free sympy symbols in
  `sympyify_expression`, but `NLFunction.vars` excludes them
  (`include_fixed=False`), so `iv_eval` raises `KeyError`; the producer
  silently drops the cut, the checker crashes. Substitute fixed values
  before conversion (consistent with `_var_cert`).
- `iv_eval` treats a `Float` exponent that is integral (`x**2.0`, as written
  in several MINLPLib files) as a fractional power and refuses negative
  bases; handle `q.denominator == 1` as an integer power.
- Completeness gaps (not soundness): `x**2/y` through a
  `DivisionExpression` never reaches `_monomial` (returns `unknown`);
  `_pow_cert` returns `convex` rather than `affine` for `p == 1` of an
  affine base; the Lundell–Westerlund rule requires all variables positive
  even for even exponents (`x**2/y` with `x ∈ [−1, 1]`).
- `certify_constraint` classifies an `AFFINE` certificate as "affine" even
  when the body is nonlinear (only reachable through B2 today); after the
  B2 fix, add an assertion that affine-certified rows are linear in
  `generate_standard_repn`.
- `check_certificate` contains dead code (`sc._round = lambda ...`), and
  `_verify_given_cut` duplicates `SafeCutter.safe_cut` almost line for
  line; factor the bound computation into one function taking rational
  slopes, used by both producer and checker.
- `write_lp`: a cut whose rounded slopes are all zero produces `cut: <= r`
  with no terms; an objective without variables produces `obj:` with no
  terms. Both should be rejected explicitly rather than left to SCIP's
  parser. Cut names (`cutN`) and row names (`name_lb`) can collide with
  instance constraint names; harmless once B5 compares coefficient vectors.
- `canonicalize_fractions` rewrites every `p/q` token in the VIPR file,
  including inside names if any contained a slash; restrict it to the
  numeric fields.
- Multiple active objectives are silently reduced to `objs[0]`; refuse.
- Constraints on GDP `Disjunct` blocks are *not* collected by
  `component_data_objects(..., descend_into=True)` (checked); dropping them
  is a relaxation and therefore safe, but instances with disjunctions or
  logical constraints should be refused explicitly because the producer
  (`lbesh.extract`) does use them.

## Half-line rule (added during the review)

`_verify_given_cut` now handles coordinates with one finite bound: with
only `L_j` it requires the enclosure `d_j.a ≥ 0` and subtracts
`d_j (z_j − L_j)`; with only `U_j` it requires `d_j.b ≤ 0` and subtracts
`d_j (z_j − U_j)`. These are the exact one-sided minimizations of
`d_j (x_j − z_j)` and the enclosure endpoints are used on the safe side, so
the rule is sound *provided* `z_j` lies on the bounded side of the
half-line. Without B1 it is worse than before: for `z_j < L_j` the shift
`d_j (z_j − L_j)` is negative and *raises* the bound. The producer-side
slope adjustment (`_round_dir`) is not trusted and needs no review beyond
noting that its float `log10` only picks the decimal scale; the rounding
direction is enforced by exact rational comparisons. Brute-force test:
`test_review_safecut.py::test_half_line_rule_one_sided_bounds` (passes).

## Verified as correct

- `is_psd` (symmetric rational elimination with zero-pivot row check):
  correct PSD test; the row check after a zero pivot is equivalent to the
  column check because the trailing block stays symmetric.
- `_sqrt_quadratic` (homogenized PSD ⇒ `sqrt(q)` is a Euclidean norm of an
  affine map): correct.
- `_pow_cert` cases (even integer powers of affine/nonneg-convex/nonpos-
  concave bases; `p ≥ 1` on nonneg convex; `0 < p < 1` on nonneg concave;
  `p < 0` on positive concave), `k ** g` cases, `exp`/`log`/`sqrt`/`abs`
  compositions, `_linear_fractional` (derivation and both signs), the
  Lundell–Westerlund monomial conditions as coded, and `_add`/`_scale`/`_neg`
  range propagation: sound (tested on grids).
- Safe-cut inequality: sign conventions, `max(d(z−L), d(z−U))` enclosure via
  `[max(t1.a, t2.a), max(t1.b, t2.b)]`, `lower.a = phi.a − worst.b`, the
  exact-zero requirement for unbounded coordinates, exact rational
  `_iv_from_frac` (verified to enclose for >53-bit rationals), `iv_eval`
  rules (integer powers of intervals containing zero are correct; sqrt of a
  negative base, log of a nonpositive base and division by an interval
  containing zero either raise or yield infinite endpoints that
  `mpf_to_frac_down` rejects). Brute-force grid tests with corner, interior
  and unbounded cases pass (`test_review_safecut.py`).
- `rational_bounds`: propagation formulas and integer rounding are correct
  and sound (they only use the linear rows, which every feasible point
  satisfies).
- LP regeneration is byte-identical for the batch artifact, `fstr` prints
  exact decimals, and the batch VIPR `CON` section equals the regenerated
  master as a multiset (234 constraints, 47 variables, 24 integers).

## Suggested order of fixes

1. B1 (z in box), B3, B2 — small local changes; rerun the new tests.
2. B6 and B5 — strict viprchk acceptance, VIPR problem comparison, return
   the certified value; make `run_all` call the checker with `viprchk` on
   the completed file.
3. B4 — remove `drop_solutions`.
4. S3 (precision/conversion), S5, then S1/S2 (exact row extraction without
   lbesh), and update the method note (precision claim, range-helper claim,
   as-read semantics).
