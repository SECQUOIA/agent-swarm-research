# Review B: `results/ac-power-flow-existential-reals.md`

Date: 2026-09-05. Independent referee audit. Method: the reduction was
reconstructed from the text alone, the example `x + x = y`, `x·y = 1` was
checked in exact arithmetic with sympy, Lemma 4 was re-derived from the
rectangular branch-flow equations, the literature claims were checked
against local full texts and arXiv abstracts, and the script was run
last. Supporting scripts (not committed): `/tmp/audit/check.py`
(instance reconstruction, forcing, Lemma 4 derivation, cycle
counterexamples) and `/tmp/audit/winding.py` (crossing-count test).

The result file was revised while this audit was in progress. Part I
audits the version I was given (Theorem 2 with line angle limits only,
rectangular membership encoding). Part II audits the corrected version at
commit `668d071` (real-angle Theorem 2, winding-number membership proof,
bus-angle-box variant, new credits), which already incorporates the
blocking finding of Part I.

## Summary

Theorem 1 (RPF) is correct: the reconstruction, the intended profile, the
forcing argument, the degree and data restrictions, and the ∃R membership
all check out, and the example instance has exactly one feasible profile.
Theorem 2 as first written had a gap (Part I, Finding 1): Lemma 4 is false
for the principal-angle semantics used by the membership encoding. The
corrected version fixes this correctly: the real-angle semantics makes
Lemma 4 valid, and the new winding-number membership argument is sound
(verified in 97,455 random cycle tests with windings `0, ±1`). Remaining
items are minor: a wrong count in the verification record, a path
allocation rule that differs between text and code, an inexact title in
the sources, and two new literature credits that could not be verified.

# Part I. Audit of the version as first written

## (a) Reconstruction of the RPF instance for `x + x = y`, `x·y = 1`

Reading Section 3 literally. Free bound `L = 85` (text); the sharper
per-bus bound `V^U · sum g · 7/2 + 1` is listed in the last column.

Gadget slots needed: addition `x + x = y` needs two distinct `x` buses and
one `5/2 - y` bus; inversion `x·y = 1` needs one `5/2 - x` bus (at `C_I`),
one `5/2 - x` bus (at `D`, conductance 2), and one `5/2 - y` bus (at `D`).
Each path bus has one gadget slot, so the `x` path needs two `x`-kind and
two `x̄`-kind buses, and the `y` path needs two `ȳ`-kind buses (its
`y`-kind buses `X_y`, `X'_y` are unused).

| bus | kind | V bounds | P bounds | neighbours (g) | degree | sharp L |
|---|---|---|---|---|---|---|
| `X_x` | value | [1/2,2] | [-85,85] | `C_x1`(1), `A`(1) | 2 | 15 |
| `X̄_x` | value | [1/2,2] | [-85,85] | `C_x1`(1), `C_x2`(1), `C_I`(1) | 3 | 22 |
| `X'_x` | value | [1/2,2] | [-85,85] | `C_x2`(1), `C_x3`(1), `A`(1) | 3 | 22 |
| `X̄'_x` | value | [1/2,2] | [-85,85] | `C_x3`(1), `D`(2) | 2 | 22 |
| `C_x1`,`C_x2`,`C_x3` | pinned | [1,1] | [-1/2,-1/2] | two path buses (1,1) | 2 | – |
| `X_y` | value | [1/2,2] | [-85,85] | `C_y1`(1) | 1 | 8 |
| `X̄_y` | value | [1/2,2] | [-85,85] | `C_y1`(1), `C_y2`(1), `A`(1) | 3 | 22 |
| `X'_y` | value | [1/2,2] | [-85,85] | `C_y2`(1), `C_y3`(1) | 2 | 15 |
| `X̄'_y` | value | [1/2,2] | [-85,85] | `C_y3`(1), `D`(1) | 2 | 15 |
| `C_y1`,`C_y2`,`C_y3` | pinned | [1,1] | [-1/2,-1/2] | two path buses (1,1) | 2 | – |
| `A` | pinned | [1,1] | [1/2,1/2] | `X_x`(1), `X'_x`(1), `X̄_y`(1) | 3 | – |
| `C_I` | pinned | [1,1] | [-1/2,-1/2] | `I`(1), `X̄_x`(1) | 2 | – |
| `I` | inversion | [1/2,2] | [-1,-1] | `W`(1), `C_I`(1) | 2 | – |
| `W` | auxiliary | [1,4] | [-85,85] | `I`(1), `D`(1) | 2 | 29 |
| `D` | pinned | [1,1] | [-5/2,-5/2] | `W`(1), `X̄'_x`(2), `X̄'_y`(1) | 3 | – |

Totals: 19 buses, 21 lines, maximum degree 3, conductances in `{1,2}`,
voltage bounds in `{[1/2,2],[1,1],[1,4]}`, fixed injections in
`{-1/2, 1/2, -5/2, -1}`.

Intended profile (`x = 1/√2`, `y = √2`): path buses carry `x`, `5/2 - x`,
`y`, `5/2 - y`; pinned buses `1`; `V_I = 1/√2`; `V_W = 2√2 - 1 ≈ 1.828`.
Exact check: every voltage and injection bound holds (fixed injections
exactly; free injections between `1 - √2` and `17 - 19√2/2 ≈ 3.56`, far
inside `[-85, 85]` and inside the sharp per-bus bounds).

Forcing (symbolic): with `sx := V_{X_x}`, `sy := V_{X_y}` as parameters and
pinned voltages `1`, the complement equations plus `C_I` and `I` determine
every other voltage uniquely (`V_{X̄_x} = 5/2 - sx`, `V_{X'_x} = sx`,
`V_I = sx`, `V_W = 2 sx - 1 + 1/sx`, ...). The constraint of `A` then
reduces to `sy - 2 sx = 0` and that of `D` to `sy - 1/sx = 0`. Hence every
feasible profile has `V_{X_y} = 2 V_{X_x}` and `V_{X_x} V_{X_y} = 1`, and
the instance has exactly one feasible profile, the intended one.

Also checked: `2x - 1 + 1/x` on `[1/2, 2]` has minimum `2√2 - 1` at
`x = 1/√2` and maximum `7/2` at `x = 2`, so `V_W ∈ [1, 4]` in the (⇒)
direction.

Ambiguities in the text (none affects correctness):

- Addition with `x = y`: the two summand neighbours of `A` must be distinct
  path buses; the first version did not say so (the corrected version
  does).
- Path allocation: the path starts with `X_v`, so a variable whose
  occurrences are all of complement kind gets an unused `X_v` of degree 1
  (here `X_y`), and a variable in no equation is an isolated bus (degree
  0, injection 0). Both are allowed by the RPF definition but should be
  stated, or such variables dropped (they are unconstrained in
  `[1/2, 2]`).
- The `[1/2, 2]` range is enforced directly by the voltage bounds of every
  value bus, whether or not the variable appears in an inversion. The
  phrase "Variables are promised to lie in `[1/2, 2]`" is misleading: in
  ETR-INV (Definition 5) the range is part of the question, not a promise.
- The (⇐) direction divides by `V_I = x ≥ 1/2 > 0`; fine.

## (b) Lemma 4 re-derivation and the angle-limit issue

From `S_ij = V_i conj((V_i - V_j) g_ij)` with `V_i = |V_i| e^{jθ_i}`:
`P_ij = g (V_i^2 - V_i V_j cos θ_ij)`, `Q_ij = -g V_i V_j sin θ_ij`
(confirmed symbolically). The identity
`sum_i θ_i sum_j g_ij V_i V_j sin θ_ij = sum_lines g_ij V_i V_j θ_ij sin θ_ij`
is correct, and the conclusion needs `t sin t > 0` for `0 < |t| < π`.

The argument requires real numbers `θ_i` whose line differences are the
quantities bounded by the angle limit. The first version's ACPF definition
did not say what `|θ_i - θ_j| ≤ θ^max` means, and Section 1 encoded it on
the principal difference (`e_i e_j + f_i f_j ≥ 0`). Under that semantics
Lemma 4 is false (unit voltages, unit conductances, sympy-checked): the
4-cycle with angles `0, π/2, π, 3π/2` has `Q_i = 0` at every bus, every
principal difference is `π/2`, and `e_i e_j + f_i f_j = 0 ≥ 0` on every
line, yet the angles differ (`P_i = 2` at every bus, not the injections of
any equal-angle profile). The 6-cycle with spacing `π/3` does the same
with `θ^max = π/3`; the k-cycle with spacing `2π/k` with any
`θ^max ≥ 2π/k`; the triangle with spacing `2π/3` refutes "any
`θ^max < π` works" for the principal semantics. Under real-valued angles
these examples disappear (lifting along a path gives real difference
`2π - 2π/k ≥ π` on the closing line), Lemma 4 is correct, but the first
version's Section 1 then did not prove membership, since rectangular
coordinates lose the winding information.

Is an angle limit needed at all? Yes: without any limit the triangle is a
counterexample under both semantics.

Fixes proposed at the time: (1) real-angle semantics plus a membership
argument, or bus-angle bounds relative to a reference (`e_i ≥ 0`, or
`e_i ≥ |f_i|`), under which real lifts in `[-π/2, π/2]` make each real
line difference equal its principal value; (2) an instance-dependent
`θ^max < 2π/N`. The corrected version adopts (1) in both forms.

## (c) Membership and Corollary 3 (first version)

RPF membership is correct. ACPF membership was correct for the principal
semantics only (see (b)). Corollary 3's first sentence is standard. The
degree remark transfers from the pooling theorem because the reduction is
a bijection between `V(Ψ)` and feasible RPF profiles with all voltages
rational functions of the solution; it depends on Abrahamsen–Miltzow 2019
(Theorem 1), which should be cited, and for ACPF uniqueness holds only up
to the global rotation.

## (d) Restriction lists versus the construction

Degrees: value bus ≤ 3; complement pinned bus 2; `A` 3; `C_I` 2; `D` 3;
`I` 2; `W` 2. Conductance `2` occurs only on the `D — (5/2 - x)` line.
Voltage bounds `{[1/2,2],[1,1],[1,4]}`; fixed injections
`{-1/2, 1/2, -5/2, -1}`; free bounds `[-85, 85]` or the sharp per-bus
values, finitely many (`V^U ∈ {2,4}`, `sum g ∈ {0,...,4}`). The bound
`|V_i sum_j g_ij (V_i - V_j)| ≤ 84` holds at the intended profile. All
restriction lists of Theorems 1 and 2 match the construction.

## (e) Literature claims (first version)

- Bienstock–Verma (2019), local full text, Section 1.3: "A straightforward
  proof of such a fact [NP membership], if true, is unlikely, for the
  reason that in a feasible solution very likely the `f_ij` (and possibly
  even some of the `θ_i`) would be irrational values." Paraphrase
  accurate; their model is the lossless flow/angle system (1), correctly
  excluded from Theorem 2. They also conjecture an `ε`-approximate version
  is in NP.
- Lehmann et al. (2016): cited by Bienstock–Verma as ref. [9] with matching
  bibliographic data and described as "weak NP-hardness ... on trees";
  arXiv:1410.8253 abstract confirms title and authors. Full text not
  local; the weak/strong distinction was not verified from the paper.
- ETR-INV Definition 5 / Theorem 7 (Abrahamsen et al., local): match.
- Schaefer et al. compendium: no power-flow entry.

## Part I findings (all addressed or superseded in Part II)

1. BLOCKING (Theorem 2) — angle-limit semantics inconsistent between
   Section 1 and Lemma 4; 4-cycle counterexample. Fixed in `668d071`.
2. MAJOR — Remark 2's "any `θ^max < π`" false for principal semantics.
   Fixed (now stated for real angles).
3. MINOR — how `θ^max` enters the rational input. Fixed (rational
   `cos θ^max ≥ 0`).
4. MINOR — distinct summand buses for `x + x = y`. Fixed.
5. MINOR — unused `X_v` / variables in no equation; "promised" wording.
   Still open (see Part II, Finding 4).
6. MINOR — Corollary 3 degree claim: precise statement, Abrahamsen–Miltzow
   citation, reference angle for ACPF. Partly addressed (Remark 6);
   Abrahamsen–Miltzow 2019 still not in the sources.
7. MINOR — Section 5 should say which AC model the script certifies.
   Fixed (bus-angle-box variant named).
8. REMARK — "weak" NP-hardness for trees. Fixed.
9. REMARK — bus types in power-system terms. Open, cosmetic.
10. REMARK — Bienstock–Verma's approximate-NP conjecture. Open, cosmetic.

# Part II. Audit of the corrected version (commit `668d071`)

## Theorem 2 and Section 1 (real-angle semantics, winding numbers)

- Definition: real angles `θ_i ∈ R`, limits on real differences with
  rational `cos θ^max ≥ 0`. Consistent with Lemma 4, whose proof is now
  valid as written (Part I (b)). The `n`-cycle paragraph after Theorem 2
  is correct (`n ≥ 4`, principal differences `2π/n ≤ π/2`, real
  injections `2(1 - cos 2π/n) ≠ 0`).
- Reduction to principal differences plus a cycle condition: correct. If
  real angles within limits exist, `θ_i - θ_j ∈ [-π/2, π/2]` is the
  principal difference, so the principal differences are cocycle-exact and
  sum to `0` on every cycle. Conversely, the sum of principal differences
  around a cycle is `2π` times an integer; vanishing on the fundamental
  cycles of a spanning tree implies vanishing on all cycles (the sum is
  `Z`-linear on the cycle space, which the fundamental cycles generate),
  and summing `δ` along the tree gives real angles with
  `θ_i - θ_j = δ_ij` on every line.
- Crossing-count criterion: for an oriented line with `|δ_ij| ≤ π/2`, the
  short arc from `V_j` to `V_i` crosses the positive real axis
  counterclockwise iff `f_j < 0 ≤ f_i` and `e_i + e_j > 0`, clockwise iff
  `f_i < 0 ≤ f_j` and `e_i + e_j > 0`. Checked by hand: an arc of length
  `≤ π/2` from below the axis to on-or-above it passes through angle `0`
  or `π`; through `0` both endpoints lie within `π/2` of `0` and not both
  at `±π/2` (their difference would be `π`), so `e_i + e_j > 0`; through
  `π` both `e ≤ 0`. The half-open convention handles endpoints on the axis
  (touch-and-return gives `+1 - 1`). Signed crossings of a closed curve
  count its winding number about the origin, which is `(sum δ)/2π`.
  Numerical test (`/tmp/audit/winding.py`): 97,455 random cycles of
  length 3–9 with all `|δ| ≤ π/2`, random magnitudes in `[0.5, 4]`, 30%
  with a voltage snapped exactly onto an axis, windings `0` (93,769),
  `+1` (1,881), `-1` (1,805): zero mismatches; the `4,5,6,8`-cycles with
  spacing `2π/n` give crossing count `1`, as they should.
- Encoding size: one variable `k_ij` with `k(k-1)(k+1) = 0` and a Boolean
  combination of strict/non-strict polynomial inequalities per line, one
  linear equation per fundamental cycle. ETR allows Boolean combinations
  and strict inequalities, so this is a polynomial-size ETR sentence.
  Conclusion: ACPF with real angles is in ∃R. Correct.
- Bus-angle-box variant (`|θ_i - θ_ref| ≤ π/4`, `e_i ≥ |f_i|` after
  rotating the reference to `0`): with real lifts in `[-π/4, π/4]` every
  real line difference lies in `[-π/2, π/2]` and equals the principal one,
  so Lemma 4 applies; rotation to the reference is without loss of
  generality. Correct, and it is what the script tests.
- Remark 2 (any real-angle `θ^max < π` works in Lemma 4; Section 1 as
  written needs `≤ π/2`): correct and appropriately cautious. For
  `π/2 < θ^max < π` the crossing criterion `e_i + e_j > 0` no longer
  separates arcs through `0` from arcs through `π`, so the caveat is
  needed.

## Corollary 3, Remark 6

Consistent with Part I (c). The bijection argument is valid for RPF; for
ACPF with real angles the solution set is the RPF profile times the global
angle shift, so "exactly one" should be read up to that shift (or with a
reference angle fixed). Abrahamsen–Miltzow 2019 (Theorem 1), on which the
degree statement rests, is still not listed in the sources.

## New literature credits

- Jeeninga, De Persis, van der Schaft, arXiv:2010.01076: exists; the
  abstract states "a necessary and sufficient LMI condition for the
  feasibility of a vector of power demands under small perturbation". The
  actual title is "DC power grids with constant-power loads — Part I: A
  full characterization of power flow feasibility, long-term voltage
  stability and their correspondence", not "DC power flow feasibility with
  constant power loads" as listed.
- Dörfler, Chertkov, Bullo, arXiv:1208.0045: exists (PNAS). The
  attribution "uniqueness of cohesive solutions with `ω = 0`" is
  consistent with that paper's synchronization condition, but the abstract
  does not state it and the full text is not local; not verified.
- Lavaei and Low (2012, Appendix B, Case 2): not local; the claims that
  they prove NP-hardness of AC-OPF for resistive networks without reactive
  loads and that their zero-reactive reduction is "not valid on cycles"
  were not verified. The second is a criticism of a published proof and
  deserves a precise quotation before it stays in the result.
- Gan and Low (2014): not local; bibliographic data plausible, not
  verified.

## (f) Code run and text/code discrepancies

`dc_resistive_build_and_check.py` (run twice; the first background run
was killed by the harness before Gurobi produced output, the second ran
detached): `ALL OK`, exit 0, wall time 25 s (not 10–20 min). Eight cases,
all with `maxdeg = 3`, all DC verdicts as expected, recovered values
`1/√2, √2`, `0.618034/1.618034`, boundary `1/2` and `2`. AC checks (bus-
angle-box model, instances with ≤ 25 buses): four instances feasible with
certified spread bounds `1.08e-9`, `2.03e-9`, `5.04e-7`, `7.76e-7`.

Discrepancies:

1. Section 5 says "five satisfiable ... three unsatisfiable". The script
   has six satisfiable cases (`x·x=1`, `1/√2`, `x=1/2`, `z=2`, `golden`,
   `fan-out`) and two unsatisfiable. Wrong count.
2. Path allocation. The text says "the next path bus of the required kind
   with a free gadget slot is used, extending the path when necessary";
   the code (`take`) only ever uses the current end of the chain and never
   revisits an earlier bus with a free slot. For the example this gives
   23 buses / 25 lines in the code versus 19 / 21 under the literal
   reading (which would reuse `X̄_x`'s free slot for `C_I`). Both are valid
   instances; the text should describe the code's rule ("extend from the
   end; earlier free slots are not reused") or say either works. For
   `x·x = 1` both readings give 15 buses / 16 lines, matching the script.
3. The AC check is skipped for instances above 25 buses, which includes
   both unsatisfiable cases (34 and 35 buses), so "infeasible RPF ⇒
   infeasible ACPF" is not exercised numerically at all. Worth one
   sentence.
4. Two of the four certified spread bounds (`5.0e-7`, `7.8e-7`) are within
   a factor of two of the script's own `1e-6` threshold; they are
   tolerance-level artefacts of the nonconvex solve, not evidence of
   nonzero angles, but the text's "below `10^-6`" reads as tighter than it
   is. Say "at the solver's feasibility tolerance".
5. Free injection bounds, DC model, gadget data, and voltage bounds in the
   code match the text exactly (`L = V^U · sum g · 7/2 + 1`; pinned `[1,1]`
   with `-1/2, 1/2, -5/2`; `I` `[1/2,2]` with `-1`; `W` `[1,4]`;
   conductance 2 only on the `D — x̄` line).

## Part II findings

1. **MINOR** — Section 5: "five satisfiable ... three unsatisfiable" should
   be "six ... two".
2. **MINOR** — Section 3, path rule versus code `take`: state the rule the
   code implements (extend from the chain end; no reuse of earlier free
   slots), or note that any allocation respecting one slot per bus works.
3. **MINOR** — Sources: correct the Jeeninga et al. title; add
   Abrahamsen–Miltzow 2019 (Theorem 1) for Corollary 3.
4. **MINOR** — Section 3: replace "promised to lie in `[1/2, 2]`" with
   "the question asks for a solution in `[1/2, 2]^n`"; say what happens to
   an unused `X_v` (degree 1) and to a variable in no equation (isolated
   bus, or drop it).
5. **MINOR** — Section 2 and Remark 3: the Lavaei–Low attributions
   (NP-hardness for resistive networks; "not valid on cycles") are
   unverified here and the second is a claim of an error in a published
   proof; quote the passage or soften to "appears to".
6. **MINOR** — Corollary 3 / Remark 6: for ACPF say "unique up to the
   global angle shift" or fix a reference angle.
7. **REMARK** — Section 5: mention that the AC check covers only feasible
   instances (≤ 25 buses) and that the certified spread bounds are at
   tolerance level.
8. **REMARK** — Dörfler–Chertkov–Bullo credit not verified against the
   full text (abstract-level only).

## Verdict

- Version as first written: **FAIL** for Theorem 2 (Lemma 4 false under
  the membership semantics), PASS WITH CORRECTIONS for Theorem 1.
- Corrected version `668d071`: **PASS WITH CORRECTIONS.** Theorem 1, the
  reduction, Lemma 5, the real-angle Lemma 4, the winding-number
  membership proof, and the bus-angle-box variant are correct; the script
  reproduces the claimed verdicts. The remaining corrections are the minor
  items above (count in Section 5, path rule, citations, unverified
  Lavaei–Low attribution).
