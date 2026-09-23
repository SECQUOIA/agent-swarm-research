# Review C: corrected Theorem 2 and Section 1 of `results/ac-power-flow-existential-reals.md`

Reviewer: independent referee (power systems, computational complexity).
Date: 2026-09-05. Scope, as instructed: only the parts corrected after
Reviews A and B, namely the Theorem 2 statement and its explanatory
paragraph, Section 1 (membership in `∃R`), Lemma 4 with its proof and
attribution paragraph, and Remarks 2 and 6. Theorem 1, Lemma 5 and the
reduction were not re-audited (both earlier reviews passed them).

Sources consulted: Dörfler–Chertkov–Bullo, arXiv:1208.0045 (PNAS 2013),
main text and SI (Lemma 2 and Theorem 1 of the SI); Lavaei–Low 2012,
author copy at `https://smart.caltech.edu/papers/zeroduality.pdf`,
Appendix B; the pooling result's Corollary 3 and its proof
(`results/pooling-existential-theory-of-reals.md`); the checker script
`code/power_flow_existential_reals/dc_resistive_build_and_check.py`.

Summary: the blocking flaw of Reviews A and B is fixed. The real-angle
semantics is now stated explicitly, the membership proof for that
semantics is correct (I verified the crossing-count criterion exhaustively
on all boundary configurations and the winding-number bookkeeping on random
closed curves), Lemma 4 is correct under the real-angle semantics, the
`n`-cycle counterexample is correct, and the rectangular bus-angle-box
variant is sound. The findings below are clarifications and one
literature nuance; none affects the truth of Theorem 2.

## Findings

### 1. PASS — Existence of real angles iff principal limits and zero cycle sums (Section 1, item 1a)

Setting: complex voltages `V_i ≠ 0`, principal differences
`δ_ij ∈ (−π, π]` of `V_i conj(V_j)`, all `|δ_ij| ≤ θ^max_ij ≤ π/2`.

*Only if.* Real angles with `V_i = |V_i| e^{jθ_i}` and
`|θ_i − θ_j| ≤ θ^max_ij ≤ π/2` satisfy `θ_i − θ_j ≡ δ_ij (mod 2π)`; both
lie in `[−π/2, π/2] ⊂ (−π, π]` and differ by a multiple of `2π` of absolute
value at most `π`, hence are equal. Cycle sums of `δ` then telescope to `0`.
Correct. (The text's justification "because `|θ_i − θ_j| ≤ π/2 < π`" is
terse; the operative fact is that both numbers lie in `(−π, π]` and are
congruent mod `2π`.)

*If.* Fix a spanning tree `T` (per component), set `θ_r = arg V_r` at a
root and `θ_i = θ_{parent(i)} + δ_{i,parent(i)}` down the tree; by
induction `θ_i ≡ arg V_i (mod 2π)`, and on tree lines `θ_i − θ_j = δ_ij`
(note `δ_ji = −δ_ij` because `|δ| ≤ π/2 < π`). For a non-tree line
`(i,j)`, traverse its fundamental cycle `j → (tree path) → i → j`. The
tree path contributes `Σ (θ_v − θ_u) = θ_i − θ_j`; the line traversed from
`i` to `j` contributes `δ_ji = −δ_ij`. The cycle condition gives
`θ_i − θ_j − δ_ij = 0`, so `θ_i − θ_j = δ_ij`, and
`|θ_i − θ_j| = |δ_ij| ≤ θ^max_ij`. Sign bookkeeping is consistent: a line
traversed from `u` to `v` contributes `δ_vu = arg V_v − arg V_u`. Correct.

Note that the ETR sentence must impose the cycle condition only for the
fundamental cycles; all other cycle sums are then automatically zero
because every real difference equals `δ`. The text's count
`|E| − |N| + 1` assumes a connected graph; per component it is
`|E| − |N| + c`. Trivial (see Finding 8).

### 2. PASS — Crossing-count criterion, boundary cases, and winding number (item 1b)

Let the short arc run from angle `a` (argument of `V_j`) to `b = a + δ_ij`
(argument of `V_i`), `|δ_ij| ≤ π/2`. Define the arc's crossing count as
`⌊b/2π⌋ − ⌊a/2π⌋` for the continuous lift. This is the half-open
convention "count `+1` when the argument passes a multiple of `2π` from
strictly below to at-or-above, `−1` for the reverse", and it has two
properties the encoding needs:

- Around any closed curve of concatenated arcs the counts telescope to
  `⌊(a_0 + 2πw)/2π⌋ − ⌊a_0/2π⌋ = w`, the winding number, with no
  general-position assumption. So "sum of principal differences around the
  oriented cycle `= 2π ×` winding number `=` signed crossing count" holds
  exactly, including cycles that touch the positive real axis at buses.
- Reversing an arc negates the count, so the cycle sum is `Σ ± k_ij` with
  `+` when the cycle traverses the line from `j` to `i` (the direction of
  the arc defining `k_ij`) and `−` otherwise. This antisymmetry is exactly
  why the two criteria in the text are the mirror images
  `f_j < 0 ≤ f_i` and `f_i < 0 ≤ f_j`; a convention such as
  `f_i ≤ 0 < f_j` for the clockwise case would break it.

Equivalence with the text's criterion. If the count is `+1`, then
`a ∈ [2πm − π/2, 2πm)` and `b ∈ [2πm, 2πm + π/2]`, so `f_j < 0 ≤ f_i`,
`e_i, e_j ≥ 0`, and `e_i = e_j = 0` is impossible (the arc would have
length `π`), so `e_i + e_j > 0`. Conversely, if `f_j < 0 ≤ f_i`, the arc
goes from the open lower half-plane to the closed upper half-plane and
therefore meets the real axis exactly once (it cannot reach both angle `0`
and angle `π`, being shorter than `π`); through angle `0` both endpoints
have `cos ≥ 0` with not both zero, through angle `π` both have `cos ≤ 0`.
Hence `e_i + e_j > 0` selects the positive axis. The clockwise case is the
mirror image. The two cases are mutually exclusive (`f_j < 0 ≤ f_i` and
`f_i < 0 ≤ f_j` cannot both hold), so `k_ij` is uniquely determined in
`{−1, 0, 1}` for every configuration.

Boundary cases checked by hand and by machine:

- Endpoint of the arc on the positive axis (`f_i = 0`, `e_i > 0`) arriving
  from below: `+1` (correct, `2πm ∈ (a, b]`). Arriving from above: `0`.
- Start on the positive axis (`f_j = 0`) going down: `−1` via the
  clockwise criterion (`f_i < 0 ≤ f_j = 0`); going up: `0`.
- Endpoint on the negative axis: `e_i + e_j ≤ 0`, count `0`.
- Both endpoints on the axis: `δ = 0` (same ray) gives `0`; opposite rays
  would need `δ = π`, excluded.
- Arcs of length exactly `π/2` with an endpoint at `±j`: e.g.
  `V_j = −j, V_i = 1` gives `+1`; `V_j = −j, V_i = −1` gives `0`;
  `V_j = j, V_i = 1` gives `0` (arrives from above);
  `V_j = 1, V_i = j` gives `0`.

Machine check: for all pairs of angles on the grid of multiples of `π/4`
(several lifts each) plus 165,935 random and mixed configurations, the
text's criterion equals `⌊b/2π⌋ − ⌊a/2π⌋` with no mismatch; antisymmetry
under reversal holds on all tested pairs; on 2,000 random closed cycles of
3–8 short arcs (30 % of vertices at grid angles) the signed sum of `k`
equals the winding number every time.

The text's parenthetical "(a short arc through angle `0` has both endpoints
within `π/2` of angle `0`, hence `e_i + e_j > 0` ...)" is correct but skips
why the sum is strictly positive (not both endpoints at `±π/2`) and why an
arc with `f_j < 0 ≤ f_i` must pass through exactly one of the two axis
points. One sentence would close this; see Finding 8.

### 3. PASS — Encoding size (item 1c)

Variables: `2|N|` reals for `(e,f)` and `|E|` reals `k_ij`. Constraints:
`O(|N| + |E|)` polynomial (in)equalities of degree at most four (the
squared-cosine limit is degree four); per line one Boolean combination of
strict and non-strict inequalities in `e, f, k` of constant size; per
fundamental cycle one linear equation in `k` with `±1` coefficients and at
most `|N|` terms. Total size `O(|E| · |N|)`. Strict inequalities and
Boolean combinations (`∧, ∨, ¬`) are part of the standard definition of
ETR (Schaefer–Cardinal–Miltzow compendium), so this is a polynomial-size
existential sentence. Correct. The cubic `k(k − 1)(k + 1) = 0` is redundant
(the three exclusive cases already fix `k`) but harmless.

### 4. PASS — Rational-cosine encoding (item 1d)

For `c = cos θ^max ∈ [0, 1]` rational and `|V_i|, |V_j| > 0`:
`|δ_ij| ≤ arccos c` iff `cos δ_ij ≥ c` (cosine is decreasing on `[0, π]`)
iff `Re(V_i conj V_j) ≥ c |V_i||V_j|`. Since the right-hand side is
nonnegative, this holds iff `Re ≥ 0` and `Re^2 ≥ c^2 |V_i|^2 |V_j|^2`
(if `Re ≥ 0` and `Re^2 ≥ (cM)^2` with `cM ≥ 0` then `Re ≥ cM`; the converse
is immediate). Correct, and for `c = 0` it reduces to `e_ie_j + f_if_j ≥ 0`.

### 5. PASS — Lemma 4 under the real-angle semantics (item 2)

Line flows: `S_ij = V_i conj(g(V_i − V_j)) = g(|V_i|^2 − V_i conj V_j)`,
giving `P_ij = g(V_i^2 − V_iV_j cos θ_ij)`, `Q_ij = −g V_iV_j sin θ_ij`.
Correct. The summation identity: bus `i`'s reactive balance is
`Σ_j g_ij V_iV_j sin θ_ij = 0`; multiplying by `θ_i` and summing, line
`{i,j}` collects `g V_iV_j (θ_i sin θ_ij + θ_j sin θ_ji) = g V_iV_j θ_ij sin θ_ij`
by oddness of sine. Correct. For real `|t| ≤ π/2`, `t sin t ≥ 0` with
equality only at `t = 0`; with `g, V > 0` every term is nonnegative, so all
vanish and `θ_ij = 0` on every line. Then `P_ij = gV_i(V_i − V_j)`, so the
magnitudes are RPF-feasible; the converse is immediate (equal angles give
`Q_ij = 0`, the same `P_ij`, and satisfy any limit `θ^max ≥ 0`). Correct.
The proof uses only the real-angle hypothesis `|θ_ij| ≤ π/2`, which is what
the corrected Theorem 2 provides.

### 6. MINOR — Attribution paragraph after Lemma 4 (item 2)

*Dörfler–Chertkov–Bullo 2013.* Verified in the arXiv full text. The main
text's "Sync condition" asserts "a unique and stable solution `θ*` with
synchronized frequencies and cohesive phases `|θ*_i − θ*_j| ≤ γ < π/2`",
and the SI's Lemma 2, statement 3 reads "Uniqueness: This equilibrium
manifold is unique in `Δ̄_G(γ)`", with the proof: "The uniqueness statement
3) follows since the right-hand side of [2] is a one-to-one function for
`θ ∈ Δ̄_G(π/2)`, see [37, Corollary 1]." Two nuances:

- Their cohesive set has `γ < π/2` strictly, whereas Lemma 4 admits the
  closed limit `π/2`. The result's own proof covers the closed case, so
  nothing is lost, but the sentence "The argument is the uniqueness of
  cohesive solutions" slightly overstates: what coincides is the *fact*
  (for `ω = 0` the only cohesive solution is `θ ≡ const`); DCB prove it by
  citing a one-to-one property from their reference [37], not by the
  `Σ θ_ij sin θ_ij` summation.
- Suggested wording: "Lemma 4 is the `ω = 0` case of the uniqueness of
  cohesive solutions of `Σ_j a_ij sin(θ_i − θ_j) = ω_i` with
  `a_ij = g_ij V_iV_j > 0` (Dörfler, Chertkov, Bullo 2013, SI Lemma 2,
  stated for `|θ_i − θ_j| ≤ γ < π/2`); the proof above is self-contained
  and includes the limit `π/2`."

*Lavaei–Low 2012, Appendix B, Case 2.* Verified in the author copy. Case 2
is "obtained from Case 1 by including the extra assumption `Im{Y} = 0` and
changing the limits ... to `Q_k^min = Q_k^max = 0` for every `k ∈ G`"
(Case 1 has `G = N`, `V_k^min = V_k^max = 1`, infinite `P` limits and
`S^max = P^max = ΔV^max = ∞` on all lines, i.e. no angle limits). They then
write "With no loss of generality, suppose that the voltage angle at bus 1
is equal to 0. Then, the OPF problem can be written as
`min V*YV + Σ P_Dk` s.t. `V_k ∈ {−1, 1}`". The result's description ("same
reduction with unit magnitudes but without angle limits, where it is not
valid on cycles") is accurate and claims no more than the text supports:
the step from `Q_k = 0` on a resistive network with `|V_k| = 1` to
`V_k ∈ {−1, 1}` is exactly what the rotating `n`-cycle profile refutes
(already for `n = 3`, since `sin(2π/3) + sin(−2π/3) = 0`). The result does
not comment on whether Lavaei–Low's NP-hardness conclusion survives, which
is appropriate.

### 7. PASS — The `n`-cycle counterexample paragraph (item 3)

For `V_k = exp(2πjk/n)`, unit conductance `g`, neighbours `k ± 1`:
`Q_k = −g[sin(2π/n) + sin(−2π/n)] = 0` at every bus; principal differences
`2π/n ≤ π/2` iff `n ≥ 4`; the oriented cycle sum of principal differences
is `n · 2π/n = 2π ≠ 0`, so by the "only if" direction of Finding 1 no real
angles with all differences at most `π/2` exist. The real injections are
`P_k = 2g(1 − cos 2π/n) > 0` at every bus. The claim that these "are not
those of any equal-angle profile" is true in a stronger form than the
`|V| ≡ 1` comparison: in any equal-angle (RPF) profile with positive
magnitudes, a bus of minimum voltage has
`P = V_min Σ g(V_min − V_l) ≤ 0`, so no RPF profile has all injections
positive. The text states the claim without justification; add either the
one-line minimum-voltage argument or "with `|V| ≡ 1` an equal-angle
profile has `P ≡ 0`". Numerical confirmation is in Finding 10.

### 8. MINOR — Clarity items in Section 1 (fixes)

Suggested one-line additions, in order of usefulness:

1. State the sign convention explicitly: "the cycle sum is
   `Σ ε_ij k_ij` with `ε_ij = +1` if the cycle traverses line `(i,j)` from
   `j` to `i` and `−1` otherwise; reversing an arc negates its count under
   the half-open convention, so this is consistent."
2. Justify "winding number = signed crossing count" by the lift:
   "for the continuous argument `a → b` along an arc the count is
   `⌊b/2π⌋ − ⌊a/2π⌋`, which telescopes around a closed curve to the winding
   number; the criterion below computes this count."
3. In the parenthetical, add why `e_i + e_j > 0` is strict (both endpoints
   at `±π/2` would make the arc of length `π`) and why an arc with
   `f_j < 0 ≤ f_i` meets exactly one of the two axis points.
4. Say "fundamental cycles of a spanning forest, `|E| − |N| + c` in total"
   or restrict to connected networks.
5. If the input may have `V_i^L = 0`, add `e_i^2 + f_i^2 > 0` to the
   sentence (the theorem quantifies over `V_i > 0`, and the principal
   difference is undefined at `V_i = 0`). Strict inequalities are allowed
   in ETR, so this is free.

### 9. PASS — Rectangular variant with `e_i ≥ |f_i|` (item 4)

With the reference rotated to angle `0` (the AC equations and the box
constraint are rotation-invariant, so this loses nothing), `e_i ≥ |f_i|`
together with `|V_i| > 0` places every `V_i` in the closed sector
`|arg V_i| ≤ π/4`. Taking `θ_i := arg V_i ∈ [−π/4, π/4]` gives real
differences `|θ_i − θ_j| ≤ π/2`, and each real difference is congruent to
`δ_ij` mod `2π` with both in `(−π, π]`, hence equal. So real and principal
differences coincide, all per-line limits `≤ π/2` are satisfied
automatically, Lemma 4 applies verbatim, and the problem is a system of
polynomial constraints (in `∃R`). Hardness with the same instances: the
intended profile has all angles `0`, i.e. `f_i = 0 ≤ e_i = V_i`, and
conversely any feasible profile has `θ_ij = 0` by Lemma 4, hence
RPF-feasible. Correct.

REMARK: `e_i ≥ |f_i|` is the pair of *linear* inequalities `e_i ≥ f_i`,
`e_i ≥ −f_i`; the text's `e_i ≥ 0, e_i^2 ≥ f_i^2` is equivalent but
nonconvex. The script also uses the quadratic form (`m.addConstr(e[i] *
e[i] >= f[i] * f[i])`); the linear form would be both simpler and easier
for Gurobi. Not a correctness issue.

### 10. PASS — Code check of the `n`-cycle example against `solve_ac` (item 6)

Run with the current script (Gurobi 13, nonconvex QCQP): `n`-cycles for
`n = 4, 5, 6` with `g = 1`, `|V| = 1`, and `P` bounds
`2(1 − cos 2π/n) ± 10^{−6}` at every bus.

| `n` | RPF (`solve_dc`) | AC with bus-angle box (`solve_ac`) | principal-only model (box removed) |
|---|---|---|---|
| 4 | infeasible | infeasible | feasible, angles `0, 90, 180, −90` |
| 5 | infeasible | infeasible | feasible, angles `0, 72, 144, −144, −72` |
| 6 | infeasible | infeasible | feasible, angles `0, −60, −120, 180, 120, 60` |

So `solve_ac` now agrees with RPF where the old rectangular model did not.
A 4-cycle with wide bounds (`V ∈ [1/2, 2]`, `P ∈ [−10, 10]`) is RPF-feasible
and AC-feasible with certified angle-spread bound `0`, as Lemma 4 predicts.

### 11. PASS — Remark 2 (item 5)

"Any real-angle limit `θ^max < π` works in the lemma": for real
`0 < |t| < π`, `sin t` has the sign of `t`, so `t sin t > 0`; the lemma's
proof goes through unchanged. Correct. "The `∃R` membership argument of
Section 1 as written uses `θ^max ≤ π/2`": accurate as a description of the
text. The last sentence (without limits, or with principal limits only, the
reduction is not claimed and Lemma 4 fails) is correct by Finding 7.

REMARK (optional strengthening, not required): the crossing criterion in
fact holds for every arc of length `< π`, not only `≤ π/2`. For an arc
with `f_j < 0 ≤ f_i` passing angle `0`,
`e_i + e_j = 2 cos((a+b)/2) cos((b−a)/2)` with `|b − a| < π` and
`(a+b)/2 ∈ (−π/2, π/2)`, hence `> 0`; passing angle `π` the same identity
gives `< 0`. I confirmed this numerically on 129,087 configurations with
`|δ| ≤ 0.999π`. Together with the encoding of `cos δ ≥ c` for negative
rational `c` (`Re ≥ 0 ∨ Re^2 ≤ c^2 |V_i|^2|V_j|^2`) and the "only if"
direction for differences in `(−π, π)`, membership therefore extends to
any `θ^max < π` with rational cosine, matching the range of Lemma 4. The
result may keep the `π/2` statement; if it wants Theorem 2 for the full
range `θ^max < π`, this is the route.

### 12. PASS — Remark 6 and Corollary 3 for ACPF

Checked against the pooling Corollary 3 proof: the bijection argument
needs (i) every constructed variable to be a fixed rational function of
the ETR-INV solution and (ii) the solution to be readable from the
instance's solution. For RPF, (i) holds with the functions `v`, `5/2 − v`,
`1`, `2x − 1 + 1/x` and (ii) via `x_v = V_{X_v}`, so a single-point
`V(Ψ)` gives exactly one RPF profile, with values in `Q(α)` and the
designated bus carrying `(α − b)/a`. For ACPF, Lemma 4 makes feasible
profiles exactly the RPF profiles with a common (free) angle, so
"solution" must refer to the magnitudes; Remark 6 says so. Correct.

### 13. REMARK — Theorem 2 statement

The statement is now unambiguous: real angles, limits on real differences,
input `θ^max` given through a rational nonnegative cosine. Two small
points: (a) shunt *conductances* are not mentioned; they do not affect
anything and could be included for generality; (b) "Hardness holds ...
angle limits `π/2`" corresponds to `cos θ^max = 0`, which is rational, so
the hardness instances are within the input format. No change required.

## Verdict

**PASS WITH CORRECTIONS** for the corrected Theorem 2 and Section 1. The
mathematics is correct: the real-angle semantics is well defined, the
winding-number/crossing-count membership proof is right including all
boundary cases (verified exhaustively on the critical configurations and by
random closed-curve tests), Lemma 4 holds under this semantics, the
`n`-cycle counterexample is valid, and the rectangular bus-angle-box
variant is sound and `∃R`-complete with the same instances. The
corrections requested are clarifications only: the attribution sentence
for Dörfler–Chertkov–Bullo (Finding 6, their uniqueness is for `γ < π/2`
and is proved by citation, not by the summation argument), a one-line
justification for "not those of any equal-angle profile" (Finding 7), and
the sign-convention, lift, and strictness sentences in Section 1
(Finding 8). Optional: extend membership to all `θ^max < π` (Finding 11)
and use the linear form of `e_i ≥ |f_i|` in text and code (Finding 9).
