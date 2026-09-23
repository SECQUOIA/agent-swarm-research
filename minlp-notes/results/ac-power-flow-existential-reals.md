# AC power flow feasibility is complete for the existential theory of the reals

Date: 2026-09-05. Status: independently audited (three audit notes);
all requested corrections applied. See the status line at the end.

This applies the technique of the [pooling `∃R`-completeness
theorem](pooling-existential-theory-of-reals.md) to power networks. The
core statement is about the resistive power-flow model, in which bus
powers are voltages times linear currents; the AC statement follows because
zero reactive injections force equal phase angles across purely resistive
lines under the stated bounds on real angle differences.

**Theorem 1 (resistive power flow).** RPF is `∃R`-complete, where RPF is:
given a graph with conductances `g_ij ∈ Q_{>0}`, voltage bounds
`0 < V_i^L ≤ V_i^U`, and injection bounds `P_i^L ≤ P_i^U`, decide whether
there are voltages `V` with

```
V_i^L ≤ V_i ≤ V_i^U   and   P_i^L ≤ V_i · sum_{j ~ i} g_ij (V_i - V_j) ≤ P_i^U   for all buses i.
```

Hardness holds with maximum degree three, conductances in `{1, 2}`, voltage
bounds from `{[1/2,2], [1,1], [1,4]}`, and injection bounds from a fixed
finite set of rational intervals.

**Theorem 2 (AC power flow).** ACPF is `∃R`-complete, where ACPF is: given
a network of lines with series admittance `g_ij + j b_ij`, shunt
susceptances, bus voltage-magnitude bounds, real and reactive injection
bounds, and angle-difference limits `|θ_i - θ_j| ≤ θ_ij^max` with rational
`cos θ_ij^max ≥ 0` (so `θ_ij^max ≤ π/2`), decide whether bus voltage
magnitudes `V_i > 0` and **real** phase angles `θ_i ∈ R` satisfying the
polar AC power-flow equations exist within all bounds. Hardness holds
already for networks whose lines are purely resistive (`b_ij = 0`, no
shunts), with reactive injection bounds `[0,0]` at every bus, maximum
degree three, angle limits `π/2`, and the data of Theorem 1.

The angle limits are constraints on real angle differences, as in the
polar formulation used by MATPOWER-style models. They are not the same as
constraints on principal differences of complex voltages: on an `n`-cycle
with `n ≥ 4`, unit voltages `V_k = exp(2πjk/n)` have zero reactive
injection at every bus and principal differences `2π/n ≤ π/2`, yet no real
angles with all differences at most `π/2` exist, and the real injections
`P_k = 2g(1 - cos 2π/n) > 0` are not those of any equal-angle profile (in
an equal-angle profile a bus of minimum voltage has injection
`V_min sum_l g (V_min - V_l) ≤ 0`). Lemma 4 below therefore needs the
real-angle semantics; Section 1 shows that this semantics is still
decidable in `∃R`. The same hardness statement holds for the rectangular
formulation if bus angles are bounded relative to a reference bus,
`|θ_i - θ_ref| ≤ π/4`, which is the polynomial constraint
`e_i ≥ |f_i|` after rotating the reference to angle `0`.

**Corollary 3.** Unless `NP = ∃R`, neither RPF nor ACPF is in `NP`; both
lie in `∃R ⊆ PSPACE`. Rational instances can require solutions of
arbitrarily high algebraic degree (as in Corollary 3 of the pooling
theorem, via the same bijection argument).

Bienstock and Verma (2019, Section 1.3) proved strong NP-hardness of a
lossless AC feasibility system and remarked that membership in `NP` is
"unlikely" to have a straightforward proof because of irrational solutions.
Theorem 2 makes this precise for the general AC model: membership in `NP`
would collapse `∃R` to `NP`. It does not cover their specific lossless
model with fixed unit magnitudes, whose variables are angles only.

## 1. Membership in ∃R

RPF is a system of polynomial inequalities of degree two in the voltages,
so RPF is in `∃R`.

For ACPF write `V_i = e_i + j f_i`. The AC equations in rectangular
coordinates are polynomial of degree two in `(e,f)`, magnitude bounds are
`V_i^{L2} ≤ e_i^2 + f_i^2 ≤ V_i^{U2}`, and a limit `|δ_ij| ≤ θ^max_ij` on
the **principal** angle difference `δ_ij ∈ (-π,π]` of `V_i conj(V_j)` with
`c_ij := cos θ^max_ij ≥ 0` rational is the polynomial condition
`e_i e_j + f_i f_j ≥ 0` and `(e_i e_j + f_i f_j)^2 ≥ c_ij^2 (e_i^2+f_i^2)(e_j^2+f_j^2)`.
What remains is the real-angle semantics: real angles `θ` with
`|θ_i - θ_j| ≤ θ^max_ij ≤ π/2` on every line exist for given complex
voltages if and only if every principal difference satisfies
`|δ_ij| ≤ θ^max_ij` **and** the principal differences sum to zero around
every fundamental cycle of a spanning forest (`|E| - |N| + c` cycles for
`c` components). Indeed, real angles within the limits have
`θ_i - θ_j ≡ δ_ij (mod 2π)` with both numbers in `[-π/2, π/2]`, hence
`θ_i - θ_j = δ_ij`, and cycle sums of `δ` telescope to zero; conversely,
summing `δ` along the forest defines `θ` with `θ_i - θ_j = δ_ij` on tree
lines, and a zero fundamental-cycle sum gives the same identity on each
non-tree line. Since the problem quantifies over `V_i > 0`, the sentence
includes `e_i^2 + f_i^2 > 0`.

The cycle condition is polynomial. Orient each line `(i,j)` and let it
contribute `δ_ij ∈ [-π/2, π/2]`, the argument of the short arc from `V_j`
to `V_i`. For a continuous argument running from `a` to `b` the signed
number of crossings of the positive real axis, counted with the half-open
convention "the arc crosses when it enters the closed upper half-plane
from the open lower half-plane" (counterclockwise, `+1`) or leaves it
(clockwise, `-1`), equals `⌊b/2π⌋ - ⌊a/2π⌋`, which telescopes around a
closed curve to its winding number. For a short arc this count is
determined polynomially: it is `+1` if and only if `f_j < 0 ≤ f_i` and
`e_i + e_j > 0`, and `-1` if and only if `f_i < 0 ≤ f_j` and
`e_i + e_j > 0`; here a short arc whose endpoints lie on opposite sides
of the real axis meets exactly one of the two axis points, it passes
angle `0` exactly when both endpoints are within `π/2` of angle `0`,
which forces `e_i + e_j > 0` (equality would need both endpoints at
`±π/2`, an arc of length `π`), and it passes angle `π` exactly when
`e_i + e_j ≤ 0`. Introduce a real variable `k_ij` with
`k_ij (k_ij - 1)(k_ij + 1) = 0` and the Boolean combination of polynomial
inequalities stating that `k_ij = 1`, `-1`, `0` in the three cases.
Reversing an arc negates its count under this convention, so the cycle
sum `sum ε_ij k_ij`, with `ε_ij = +1` when the cycle traverses `(i,j)`
from `j` to `i` and `-1` otherwise, is the winding number. Requiring it to
vanish for each fundamental cycle is a polynomial-size existential
sentence. Hence ACPF with real angles is in `∃R`. The rectangular variant
with bus-angle boxes needs only the linear constraints `e_i ≥ f_i` and
`e_i ≥ -f_i`.

## 2. From AC to resistive networks

**Lemma 4.** Let all lines be purely resistive (`b_ij = 0`, no shunts), all
angle limits satisfy `θ^max_ij ≤ π/2`, and all reactive injection bounds be
`[0,0]`. Then a voltage profile `(V_i, θ_i)` is ACPF-feasible if and only if
`θ_i = θ_j` on every line and the magnitudes `V_i` are RPF-feasible for the
same conductances and bounds.

*Proof.* With `b_ij = 0` and no shunts, the standard line-flow expressions
(`S_ij = V_i conj((V_i - V_j) g_ij)`) are
`P_ij = g_ij (V_i^2 - V_i V_j cos θ_ij)` and `Q_ij = -g_ij V_i V_j sin θ_ij`,
where `θ_ij = θ_i - θ_j` is the real angle difference. Suppose the profile
is feasible. Zero reactive injection at every bus means
`sum_j g_ij V_i V_j sin θ_ij = 0` for all `i`. Multiply the equation of bus
`i` by the real number `θ_i` and sum over `i`; each line `{i,j}` contributes
`g_ij V_i V_j (θ_i sin θ_ij + θ_j sin θ_ji) = g_ij V_i V_j θ_ij sin θ_ij`, so

```
sum_{lines} g_ij V_i V_j θ_ij sin θ_ij = 0.
```

Every term is nonnegative because `V > 0`, `g > 0`, and `t sin t ≥ 0` for
real `|t| ≤ π/2`, with equality only at `t = 0`. Hence `θ_ij = 0` on every
line, and then `P_ij = g_ij V_i (V_i - V_j)`, so the magnitudes are
RPF-feasible. Conversely an RPF-feasible `V` with all angles equal has
`Q_ij = 0` and the same `P_ij`, so it is ACPF-feasible. ∎

Lemma 4 is the `ω = 0` case of the uniqueness of "cohesive" solutions of
the coupled oscillator equations `sum_j a_ij sin(θ_i - θ_j) = ω_i` with
`a_ij = g_ij V_i V_j > 0` (Dörfler, Chertkov, Bullo 2013, supplementary
Lemma 2, stated for `|θ_i - θ_j| ≤ γ < π/2` and proved there by a
one-to-one property); the proof above is self-contained and includes the
limit `π/2`. The statement fails without the real-angle limits, as the
`n`-cycle example above shows. Lavaei and Low
(2012, Appendix B, Case 2) use the same "resistive lines, zero reactive
power" reduction with unit magnitudes but without angle limits, where it is
not valid on cycles. Therefore ACPF restricted to the stated class is the
same decision problem as RPF, and Theorem 2 follows from Theorem 1 and
Section 1.

## 3. Reduction from ETR-INV to RPF

Start from an ETR-INV instance (Abrahamsen, Adamaszek, Miltzow 2018,
Definition 5; `∃R`-complete by their Theorem 7), with `x = 1` replaced by
`x·x = 1`, so that all equations are inversions `x·y = 1` (`x = y` allowed)
and additions `x + y = z` (repeated summands allowed). Variables are
promised to lie in `[1/2, 2]`; this range is imposed directly by voltage
bounds below.

Bus kinds:

- **Value buses** carry a value in `[1/2,2]`: voltage bounds `[1/2, 2]`,
  free injection bounds `[-L_i, L_i]` (defined below).
- **Pinned buses** have voltage bounds `[1,1]` and a fixed injection
  (bounds `[P,P]`). With neighbours `a_1,…,a_k` and conductances `g_k`, the
  injection constraint of a pinned bus reads `sum_k g_k (1 - V_{a_k}) = P`,
  a linear equation in the neighbours' voltages.
- **Inversion buses** `I` have voltage bounds `[1/2,2]`, fixed injection
  `-1`, and exactly two neighbours with conductance `1`.
- **Auxiliary buses** `W` have voltage bounds `[1,4]` and free injection.

**Complements and copies.** A pinned bus `C` with fixed injection `-1/2`
and exactly two neighbours `a, b` (conductance `1`) enforces
`(1 - V_a) + (1 - V_b) = -1/2`, that is, `V_a + V_b = 5/2`. Since
`v ↦ 5/2 - v` maps `[1/2,2]` onto itself, chaining
`X_v — C — X̄_v — C' — X'_v — …` produces, for each variable `v`, a path
of value buses alternately carrying `v` and `5/2 - v`; each bus of the path
has at most two path neighbours and one further gadget neighbour. For each
gadget occurrence, the next path bus of the required kind (`v` or
`5/2 - v`) with a free gadget slot is used, extending the path when
necessary (the script always extends from the end of the path, which may
create a few more buses than strictly needed; both allocations are
valid). In a feasible profile, the values along the path are determined
by `V_{X_v}` through the complement equations.

**Addition `x + y = z`.** A pinned bus `A` with fixed injection `1/2` and
three neighbours of conductance `1`: a `v = x` bus, a `v = y` bus, and a
`5/2 - z` bus. Its constraint is `(1 - x) + (1 - y) + (1 - (5/2 - z)) = 1/2`,
i.e. `z = x + y`. For `x + x = y` the two `x`-neighbours are two distinct
path buses of `x`.

**Inversion `x·y = 1`.** An inversion bus `I`, an auxiliary bus `W`, a pinned
bus `C_I` (injection `-1/2`) with neighbours `I` and a `5/2 - x` bus, and a
pinned bus `D` (injection `-5/2`) with neighbours `W` (conductance `1`), a
`5/2 - x` bus (conductance `2`), and a `5/2 - y` bus (conductance `1`).
The lines of `I` are `(I,W)` and `(I,C_I)`, both of conductance `1`. For `x = y` the `5/2 - x` buses at `C_I` and `D`
are three distinct path buses.

In a feasible profile: `C_I` gives `V_I + (5/2 - x) = 5/2`, so `V_I = x`.
The injection constraint of `I` is `x[(x - V_W) + (x - 1)] = -1`, i.e.
`V_W = 2x - 1 + 1/x` (note `x ≥ 1/2 > 0`). The constraint of `D` is
`(1 - V_W) + 2(1 - (5/2 - x)) + (1 - (5/2 - y)) = -5/2`, i.e.
`y = V_W - 2x + 1 = 1/x`. Hence `x·y = 1`. Conversely, given `x, y ∈ [1/2,2]`
with `xy = 1`, set `V_I = x` and `V_W = 2x - 1 + 1/x`; then
`V_W ∈ [2√2 - 1, 7/2] ⊂ [1, 4]` (the function `2x - 1 + 1/x` on `[1/2,2]`
has minimum `2√2 - 1` at `x = 1/√2` and maximum `7/2` at `x = 2`), and both
pinned constraints hold. When `x = y` the two `5/2 - x` buses at `D` and
`C_I` are distinct path buses of the same variable.

**Free injection bounds.** Every value bus and auxiliary bus has at most
three neighbours, all voltages lie in `[1/2, 4]`, and conductances are at
most `2`, so `|V_i sum_j g_ij (V_i - V_j)| ≤ 4 · 3 · 2 · (7/2) = 84`. Set
`L_i := 85` for all free buses (the script uses the sharper
`V_i^U · sum_j g_ij · 7/2 + 1`). These bounds never bind at the intended
profile, and impose nothing else in the converse direction.

**Lemma 5.** The ETR-INV instance has a solution in `[1/2,2]^n` if and only
if the constructed RPF instance is feasible.

*Proof.* (⇐) Let `V` be feasible. Set `x_v := V_{X_v} ∈ [1/2,2]`. The
complement equations propagate `x_v` and `5/2 - x_v` along the path of `v`
(each pinned path bus has exactly the two path neighbours). The addition
and inversion computations above then give `x + y = z` and `x·y = 1` for
every equation. (⇒) Given a solution, assign the path buses their values,
`V_I = x`, `V_W = 2x - 1 + 1/x`, and all pinned buses `1`. Every pinned and
inversion constraint holds by the computations above, all voltages are
within bounds, and every free injection lies within `[-L_i, L_i]`. ∎

**Size and data.** Each variable path has `O(number of occurrences)` buses;
each equation adds `O(1)` buses and lines. Conductances lie in `{1,2}`,
voltage bounds in `{[1/2,2],[1,1],[1,4]}`, fixed injections in
`{-1/2, 1/2, -5/2, -1}`, free injection bounds `[-85, 85]` (or the sharper
per-bus values), and every bus has degree at most three (path buses: two
path lines and one gadget line; pinned buses: two or three lines; `I`: two;
`W`: two). Together with Section 1 this proves Theorem 1. ∎

## 4. Remarks

1. The model of Theorem 1 is the power-flow model of DC networks with
   constant-power injections, as in Gan and Low (2014) (not the linearized
   "DC approximation" of AC networks), and also the gas or water analogue
   in which a node's power is its potential times its net linear (laminar)
   flow. The theorem says that deciding the existence of an operating point
   under power bounds is `∃R`-complete already for this model. Hardness
   needs voltage bounds on non-source buses together with injection
   bounds: with fixed source voltages and loads only, Jeeninga, De Persis,
   and van der Schaft (arXiv:2010.01076) decide feasibility by a linear
   matrix inequality.
2. Lemma 4 uses real angle limits `≤ π/2` only to make `t sin t ≥ 0` with
   equality only at zero; any real-angle limit `θ^max < π` works in the
   lemma, while the `∃R` membership argument of Section 1 as written uses
   `θ^max ≤ π/2`. Without angle limits, or with limits on principal
   differences only, the reduction is not claimed, and the `n`-cycle
   example shows that Lemma 4 then fails.
3. Theorem 2 does not resolve the `NP`-membership question for the
   lossless fixed-magnitude system of Bienstock and Verma (2019), in which
   only angles vary; the resistive class used here is the opposite regime.
   NP-hardness of AC-OPF for resistive networks without reactive loads is
   due to Lavaei and Low (2012); the new statement is `∃R`-completeness.
4. On trees the reduction does not apply: value copies require paths and
   gadgets link different variables' paths, creating cycles. Lehmann,
   Grastien, and Van Hentenryck (2016) proved (weak) NP-hardness of AC
   feasibility on trees; the exact complexity class of the tree case is
   not settled here.
5. Instances of Theorem 1 have a constant number of distinct data values;
   in this sense the hardness is "strong", in analogy with strong
   NP-hardness.
6. Corollary 3's algebraic-degree statement refers to the RPF voltages,
   which are the AC magnitudes; all bus voltages of the constructed
   instance are rational functions (`v`, `5/2 - v`, `1`, `2x - 1 + 1/x`)
   of the ETR-INV solution, so the bijection argument of the pooling
   theorem applies.

## 5. Verification record

`code/power_flow_existential_reals/dc_resistive_build_and_check.py`
implements the reduction (paths of complements, addition and inversion
gadgets, degree-derived free injection bounds) and decides RPF feasibility
of each constructed instance with Gurobi 13 as a nonconvex QCQP. Eight
ETR-INV systems (six satisfiable, including `1/√2`, the golden ratio, and
boundary values `1/2` and `2`; two unsatisfiable) all received the
correct verdict, with recovered values matching the algebraic solutions to
six digits and maximum degree three. On instances with at most 25 buses
the script also solves the rectangular AC model of the bus-angle-box
variant (resistive lines, `Q_i = 0`, magnitude bounds, `e_i ≥ |f_i|`) as a
feasibility problem and then maximizes `sum_i f_i^2` under a time limit.
In the final run all four such instances (15, 19, 23, and 25 buses) were
AC-feasible with a solver-reported upper bound below `10^-6` on
`sum_i f_i^2`. This is numerical consistency with Lemma 4; a positive
tolerance bound does not prove that all angles are exactly zero. Exact
equal-angle behavior follows from Lemma 4. Both auditors reproduced the RPF verdicts independently and one
verified the intended profiles in exact arithmetic. The saved exact check
`code/power_flow_existential_reals/check_winding_count_exact.py` tests
the polynomial crossing rule at axis and quarter-turn boundaries, with
unequal voltage magnitudes, and checks cycle winding independently. Their
4- and 5-cycle counterexamples to the principal-angle version of Lemma 4 were checked
with the same script's models.

## Sources

- M. Abrahamsen, A. Adamaszek, T. Miltzow, *The Art Gallery Problem is
  ∃R-complete*, STOC 2018; J. ACM 69(1) 2022, Definition 5 and Theorem 7
  (local: `literature/papers/abrahamsen2022-the-art-gallery-problem-is`).
- D. Bienstock, A. Verma, *Strong NP-hardness of AC power flows feasibility*,
  Oper. Res. Lett. 47 (2019) 494–501, Section 1.3
  (local: `literature/papers/bienstock2019-strong-np-hardness-of-ac`).
- K. Lehmann, A. Grastien, P. Van Hentenryck, *AC-feasibility on tree
  networks is NP-hard*, IEEE Trans. Power Syst. 31 (2016) 798–801
  (arXiv:1410.8253).
- J. Lavaei, S. H. Low, *Zero duality gap in optimal power flow problem*,
  IEEE Trans. Power Syst. 27 (2012) 92–107, Appendix B, Case 2.
- L. Gan, S. H. Low, *Optimal power flow in direct current networks*, IEEE
  Trans. Power Syst. 29 (2014) 2892–2904.
- F. Dörfler, M. Chertkov, F. Bullo, *Synchronization in complex oscillator
  networks and smart grids*, PNAS 110 (2013) 2005–2010 (arXiv:1208.0045).
- M. Jeeninga, C. De Persis, A. J. van der Schaft, arXiv:2010.01076
  (DC power flow with constant-power loads; feasibility by a linear
  matrix inequality in the loads-only case).
- M. Abrahamsen, T. Miltzow, *Dynamic Toolbox for ETRINV*, arXiv:1912.08674
  (local: `literature/papers/abrahamsen2019-dynamic-toolbox-for-etrinv`),
  used through Corollary 3 of the pooling theorem.
- Novelty audit: `notes/power-flow-existential-reals-novelty.md`.
- M. Schaefer, J. Cardinal, T. Miltzow, *The Existential Theory of the Reals
  as a Complexity Class: A Compendium*, arXiv:2407.18006
  (local: `literature/papers/schaefer2024-the-existential-theory-of-the`).
- The pooling theorem and its sources:
  `results/pooling-existential-theory-of-reals.md`.

## Status

Draft by the root agent, 2026-09-05. Independent audits
`notes/review-power-flow-existential-reals-A.md` (FAIL as first written:
the angle-limit semantics of Theorem 2 was inconsistent between the
rectangular encoding and Lemma 4, with explicit `n`-cycle counterexamples)
and `notes/review-power-flow-existential-reals-B.md` (same blocking
finding; Theorem 1 verified in exact arithmetic). Fix applied: Theorem 2
now uses real angles, Section 1 proves `∃R` membership of that semantics
by a winding-number crossing count, and the rectangular bus-angle-box
variant is stated separately. The follow-up audit
`notes/review-power-flow-existential-reals-C.md` of the corrected
Theorem 2 and Section 1 returned PASS WITH CORRECTIONS (clarifications
only: attribution wording, the minimum-voltage justification, sign
convention and lift argument in the crossing count, spanning-forest
count), and the final part of audit B concurs; all applied. Theorem 1,
the reduction, and Lemma 5 passed both original audits, one in exact
arithmetic. Novelty audit: new as a
statement about power flow; the resistive model, the zero-reactive
reduction idea, and the oscillator uniqueness argument are credited.
