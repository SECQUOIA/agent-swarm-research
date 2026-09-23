# Review A: `results/ac-power-flow-existential-reals.md`

Reviewer: independent referee (power systems modelling, computational
complexity). Date: 2026-09-05. Scope: Theorem 1 (RPF `∃R`-complete),
Theorem 2 (ACPF `∃R`-complete on purely resistive lines with zero reactive
injections), Lemma 4, Lemma 5, Corollary 3, Remarks 1–5, and the script
`code/power_flow_existential_reals/dc_resistive_build_and_check.py`.
Background read: `results/pooling-existential-theory-of-reals.md`
Sections 2, 3 and 5; Abrahamsen–Adamaszek–Miltzow Definition 5 and
Theorem 7; Bienstock–Verma 2019 Sections 1 and 1.3; the arXiv abstract of
Lehmann–Grastien–Van Hentenryck (1410.8253).

Summary: Theorem 1 and its reduction (Lemma 5) are correct; every
algebraic identity, range, degree and bound claim checks out, and the script
matches the text. Theorem 2 has one blocking gap: the draft uses two
inequivalent meanings of the angle limit `|θ_i − θ_j| ≤ π/2`. Section 1
encodes it in rectangular coordinates as `e_i e_j + f_i f_j ≥ 0`
(principal value of the angle difference, per line), while the proof of
Lemma 4 needs real angle variables `θ_i` whose actual differences are in
`[−π/2, π/2]` on every line. On graphs with cycles these are different
constraints, and under the rectangular semantics Lemma 4 is false (explicit
counterexample below, verified with the draft's own `solve_ac` model). The
fix is clear: define ACPF with real polar angle variables (the MATPOWER
polar convention) and supply an `∃R`-membership encoding for that semantics.

## Findings

### 1. BLOCKING — Angle-limit semantics: Section 1, Lemma 4 and the code disagree, and Lemma 4 fails under the rectangular semantics

Location: Theorem 2 statement ("angle-difference limits `|θ_i − θ_j| ≤
θ_ij^max`", "complex bus voltages"), Section 1 (encoding `e_i e_j + f_i f_j
≥ 0`), Lemma 4 proof (multiplication of bus equations by `θ_i`), Section 5
and `solve_ac` (same rectangular constraint).

The problem. For complex voltages the argument difference is defined modulo
`2π`. Section 1 fixes the meaning per line: `Re(V_i conj V_j) ≥ 0`, i.e. the
principal value `δ_ij ∈ [−π/2, π/2]`. Lemma 4's proof multiplies the reactive
balance at bus `i` by a real number `θ_i` and sums; the identity

```
sum_i θ_i sum_j g_ij V_i V_j sin(θ_i − θ_j) = sum_lines g_ij V_i V_j θ_ij sin θ_ij
```

is correct (antisymmetry checked: line `{i,j}` contributes
`g V_i V_j (θ_i sin θ_ij + θ_j sin θ_ji) = g V_i V_j (θ_i − θ_j) sin θ_ij`),
but it needs a single real vector `θ` such that, on every line, the *real*
difference `θ_i − θ_j` lies in `[−π/2, π/2]` (so that `t sin t ≥ 0` applies to
`t = θ_i − θ_j` itself, not to `t + 2πk`). Given only the per-line principal
values `δ_ij`, such a lift exists if and only if the oriented sum of `δ_ij`
around every cycle is `0` rather than a nonzero multiple of `2π`. The
rectangular constraint does not enforce this.

Counterexample (rectangular semantics). Take an `n`-cycle (`n ≥ 4`) with
`g = 1` on every line, `V_k = exp(2πjk/n)`. Then on every line
`Re(V_k conj V_{k±1}) = cos(2π/n) ≥ 0` (equal to `0` for `n = 4`, `0.309` for
`n = 5`), the reactive line flows `Q_{k,k+1} = −sin(−2π/n)` and
`Q_{k,k−1} = −sin(2π/n)` cancel so `Q_k = 0` at every bus, and
`P_k = 2(1 − cos(2π/n)) > 0`. With magnitude bounds `[1,1]`, reactive bounds
`[0,0]` and real bounds `[P_k, P_k]` this is ACPF-feasible in the rectangular
model but RPF-infeasible (with `V ≡ 1` RPF forces `P ≡ 0`). I ran it through
the draft's own `solve_dc`/`solve_ac`:

```
n=4: P_i=2.000000; RPF feasible=False; rectangular ACPF (Q=0, cos>=0) feasible=True
n=5: P_i=1.381966; RPF feasible=False; rectangular ACPF (Q=0, cos>=0) feasible=True
```

So under the semantics of Section 1 and of the code, Lemma 4 ("ACPF-feasible
iff angles equal and magnitudes RPF-feasible") is false in general, and the
sentence "ACPF restricted to the stated class is the same decision problem as
RPF" is unproved. The `n = 5` example also shows that no constant
`θ^max ∈ (0, π/2]` rescues the rectangular reading: cycles of length
`> 2π/θ^max` can wind, and the reduction's networks contain cycles of
unbounded length (each variable path is a long chain closed by gadgets).
Whether the constructed instances admit winding solutions is not addressed
by the proof; the spread check in Section 5 is numerical evidence on small
instances only (and see Finding 10).

Fix (recommended). Define ACPF with real polar variables: magnitudes
`V_i > 0` and angles `θ_i ∈ R`, with the angle limits as linear constraints
`|θ_i − θ_j| ≤ θ_ij^max` on these reals (this is the MATPOWER/OPF polar
convention with unbounded `Va`). Then Lemma 4 and its proof are correct as
written, including the converse (all `θ_i = 0` gives `Q_ij = 0` and
`P_ij = g V_i (V_i − V_j)`), and Remark 2's `θ^max < π` is exactly the
boundary (`t sin t > 0` for `0 < |t| < π`; with `θ^max = π` a single line with
`V_i = V_j = 1`, `θ_ij = π` has `Q = 0`, `P_i = P_j = 2`, not RPF-feasible).
Section 1 must then encode the real-lift condition, which the rectangular
inequality alone does not. One polynomial-size encoding: since every line
difference is at most `π/2` in absolute value, angles can be taken in
`[−nπ/2, nπ/2]`; write `θ_i = (π/2) q_i + ρ_i` with an integer
`q_i ∈ [−n, n]` (encoded by `O(log n)` Boolean variables `b(b−1) = 0`) and
`ρ_i ∈ [0, π/2)` represented by a point `(c_i, s_i)` with
`c_i^2 + s_i^2 = 1`, `c_i > 0`, `s_i ≥ 0`. The line condition
`|θ_i − θ_j| ≤ π/2` is then: `q_i = q_j`; or `q_i = q_j + 1` and
`s_i ≤ s_j`; or `q_j = q_i + 1` and `s_j ≤ s_i` (comparisons and `±1` on
binary-encoded integers are polynomial-size polynomial systems). The
rectangular voltage is `V_i = |V_i| · j^{q_i} · (c_i + j s_i)`, where
`j^{q_i}` is fixed by the two low bits of `q_i`; the power equations stay
degree-two polynomials in `(|V_i|, c_i, s_i)` times the bit selectors. For
general rational `cos θ^max` the same encoding works with the quadrant
comparison replaced by the squared cosine test of Section 1. Alternatively,
if the authors prefer the rectangular semantics, Theorem 2 needs a new
argument that the constructed instances have no winding solutions; I do not
see one, and I would not accept the theorem on the strength of the spread
check.

Also state in Theorem 2 that the limits apply to *every* line (Lemma 4
uses that).

### 2. MAJOR — Remark 2 and the "rational `cos θ^max`" remark are semantics-dependent

Location: Section 1 last sentence; Remark 2.

Under the polar-real semantics of the fix in Finding 1 both are right:
`t sin t ≥ 0` with equality only at `0` holds on `|t| ≤ θ^max` for any
`θ^max < π`, and `e_i e_j + f_i f_j ≥ cos θ^max · |V_i||V_j|` for
`0 ≤ cos θ^max ∈ Q` is `e_i e_j + f_i f_j ≥ 0` together with
`(e_i e_j + f_i f_j)^2 ≥ cos^2 θ^max (e_i^2 + f_i^2)(e_j^2 + f_j^2)` — but only
as the *per-line principal-value* constraint. Under the rectangular
semantics, Remark 2's "any limit `θ^max < π` works" is false already for a
triangle (`V_k = exp(2πjk/3)`, `δ = 2π/3 < π`, `Q ≡ 0`). After fixing
Finding 1, rewrite Remark 2 to say that `θ^max < π` suffices for Lemma 4
under real angle variables, and that the `∃R` encoding of Section 1 is the
principal-value constraint plus the lift condition. Note also that for
`θ^max ∈ (π/2, π)` the cosine is negative and the squaring step needs the
two-case form (`LHS ≥ 0`, or `LHS < 0` and `LHS^2 ≤ cos^2 θ^max · …`).

### 3. MINOR — Input representation of angle limits

Location: Theorem 2 statement, Section 1.

`θ_ij^max ≤ π/2` is in general irrational, so it cannot be part of a rational
input. Say that limits are given by rational `cos θ_ij^max ∈ [0, 1]`
(or by the flag `θ^max = π/2`); the hardness instances use `π/2` on every
line, which has `cos = 0`.

### 4. MINOR — Lemma 4 bookkeeping

Location: Lemma 4 and the parenthetical after its proof.

- Line-flow expressions: with series admittance `y = g + jb`, `b = 0`, no
  shunts, `S_ij = V_i conj(y (V_i − V_j)) = g(|V_i|^2 − V_i conj V_j)`, so
  `P_ij = g(V_i^2 − V_i V_j cos θ_ij)`, `Q_ij = −g V_i V_j sin θ_ij` with
  `θ_ij = θ_i − θ_j`. Correct and consistent with the standard
  `Q_ij = −V_i^2 b − V_i V_j (g sin θ_ij − b cos θ_ij)` at `b = 0`. The code's
  `Q = −g (f_i e_j − e_i f_j)` equals `−g Im(V_i conj V_j)`, also correct.
- Connectivity is not needed: the identity is a sum over lines and the
  conclusion `θ_ij = 0` is per line. The remark "the argument applies
  componentwise" is superfluous; the natural statement is "angles are
  constant on each connected component". Delete or reword.
- The lemma silently uses that angle limits are present on every line
  (see Finding 1).

### 5. MINOR — Repeated variables in gadgets: say explicitly that the buses are distinct

Location: "Addition" and "Inversion" paragraphs; Lemma 5.

For `x + x = y` the text says "a `v = x` bus, a `v = y` bus"; it should say
that when `x = y` these are two distinct path buses of `x` (the slot rule
"next path bus of the required kind with a free gadget slot" implies this,
and `take` in the script guarantees it, but the reader has to infer it).
For inversion with `x = y` the text says "the two `5/2 − x` buses at `D` and
`C_I` are distinct"; in fact three distinct `5/2 − x` buses are used (`C_I`'s,
`D`'s `g = 2` neighbour, and `D`'s `g = 1` neighbour), and the last two must
be distinct because the graph is simple. The script does this (three
separate `take(·, 'bar')` calls). Degenerate additions such as
`x + y = x` or `x + x = x` use distinct `x` and `5/2 − x` buses and correctly
become infeasible (they force `y = 0` or `x = 0`, outside `[1/2, 2]`);
checked with `build`.

### 6. MINOR — Corollary 3 for ACPF: say what "solution" means

Location: Corollary 3.

The bijection argument is valid for RPF: in a feasible profile every bus
voltage is a fixed rational function of `x = (V_{X_v})_v` (`v`, `5/2 − v`,
`1`, `x`, `2x − 1 + 1/x`), and conversely `x` is read off the buses `X_v`, so
feasible profiles correspond bijectively to `V(Ψ)`; with `V(Ψ) = {x*}`,
`x* ∈ Q(α)^n`, the unique profile has values in `Q(α)` and bus `X_π` carries
`(α − b)/a`. Add this sentence (the pooling text has its analogue). For ACPF
the degree statement should refer to the voltage *magnitudes*: the
rectangular coordinates depend on the free reference angle per component
and can be made transcendental or algebraic at will.

### 7. MINOR — Remark 4: characterise the Lehmann et al. result

Location: Remark 4.

Lehmann–Grastien–Van Hentenryck (IEEE TPWRS 31(1), 2016; arXiv:1410.8253)
prove NP-hardness of AC-feasibility on trees; Bienstock–Verma (Section 1,
footnote 1) describe it as weak NP-hardness whose "reduction encodes some
irrational quantities". Saying "NP-hard (weakly, by a numeric reduction)"
would make the contrast with Theorem 2's strong, constant-data hardness on
general graphs (Remark 5) explicit and accurate.

### 8. MINOR — Comparison with Bienstock–Verma

Location: introduction after Corollary 3; Remark 3.

The quotation is accurate: Section 1.3 says "A straightforward proof of such
a fact, if true, is unlikely, for the reason that in a feasible solution very
likely the `f_ij` (and possibly even some of the `θ_i`) would be irrational
values." Their system is lossless (reactances `x_ij`, unit magnitudes,
angle variables, flow limits, `θ_ij^max < π/2`); Remark 3's description is
correct. Two nuances worth one sentence: (i) their strong NP-hardness is
"number of bits polynomially bounded", whereas Theorem 1 has a constant
number of distinct data values (stronger); (ii) Theorem 2 concerns a
different regime (resistive, zero `Q`), so it neither implies nor is
implied by their result — the draft says this, fine.

### 9. REMARK — Remark 1 wording

"gas or water analogue in which a node's power is its potential times its
net linear flow": real gas and water networks have nonlinear potential–flow
laws (Weymouth, Hazen–Williams). Say "a linear (laminar) potential-flow
network".

### 10. REMARK — Script observations (`dc_resistive_build_and_check.py`)

- Text–code match: conductances `{1,2}` (`D`'s `x̄` line is `2`, all others
  `1`); bounds `[1/2,2]`, `[1,1]`, `[1,4]`; fixed injections `C: −1/2`,
  `A: +1/2`, `I: −1`, `D: −5/2`; `take`/`extend` implement the slot rule; the
  free bound `VU · Σg · 7/2 + 1` is valid (max `|V_i − V_j| = 7/2`) and
  sharper than 85. I verified with exact rational arithmetic on seven small
  instances that the intended profile (`V_I = x`, `V_W = 2x − 1 + 1/x`,
  pinned `1`, path values `v`/`5/2 − v`) satisfies every bound with
  equality-free slack on free buses, that every `C`/`C_I` bus has exactly two
  neighbours, `A` and `D` three, `I` and `W` two, every path bus at most two
  path neighbours and at most one gadget neighbour, and max degree 3.
  `V_W` ranges over `[2√2 − 1, 7/2]` on `[1/2, 2]` (critical point
  `x = 1/√2`; endpoints `2` and `7/2`) as claimed.
- `solve_ac` implements the rectangular semantics
  (`e_i e_j + f_i f_j ≥ 0`), so the spread check tests exactly the reading
  under which Lemma 4 is unavailable (Finding 1). A certified spread bound of
  `0` is evidence that the tested instances have no winding solutions; it is
  not a proof for all instances. The message "the zero-angle claim is proved
  analytically" printed when the bound is not certified is misleading under
  this semantics and should be reworded.
- The spread objective `Σ f_i^2` with `f_ref = 0` certifies equal angles
  only on the component of `ref`; the constructed instances are connected
  when every variable occurs in some equation, but the script does not
  check this.
- Run of the script (`~/miniconda3/envs/minlp-notes/bin/python
  dc_resistive_build_and_check.py`, this review): it did not complete. Case 1
  (`x*x=1`): DC feasible, AC feasible, spread bound certified `3.7e-10`.
  Case 2 (`x+x=y, x*y=1`): DC feasible with `x = 0.707107`, AC feasible,
  spread bound *not* certified (upper bound `54.3` after the 300 s limit).
  Case 3 (infeasible instance): DC infeasible as expected, then the AC
  feasibility solve hit the 120 s limit (Gurobi status 9) and the
  `assert m.Status in (OPTIMAL, INFEASIBLE)` in `solve_ac` aborted the
  script with exit code 1; cases 4–8 were never run. I re-ran all eight cases
  with `ac=False`: every DC verdict matches the expectation (feasible cases
  return `x = 1`; `x = 1/√2, y = √2`; `x = 1/2, y = 1`; `x = 1/2, y = 1, z = 2`;
  golden ratio `x = 0.618034, z = 1.618034`; fan-out `u = 1/2, y_i = 2`; the two
  infeasible cases are infeasible), each in well under a second, with the
  bus/line counts and `maxdeg = 3` as reported. So the Theorem 1 evidence is
  complete; the AC evidence (Section 5's "certify that only zero-angle
  solutions exist") is available for one instance only. Section 5 and the
  status line must not claim more than this, and the script should report
  `TIME_LIMIT` outcomes instead of asserting (see also Finding 12).

### 11. REMARK — Items checked and found correct (no action)

- ETR-INV as used matches Abrahamsen et al. Definition 5 (range
  `[1/2, 2]`); replacing `x = 1` by `x·x = 1` is sound in that range.
- Membership of RPF in `∃R`: degree-two polynomial system, polynomial size.
- Pinned-bus constraint `Σ_k g_k (1 − V_{a_k}) = P` with the draft's
  injection convention `P_i = V_i Σ g (V_i − V_j)` (generation positive);
  complement `V_a + V_b = 5/2` and `v ↦ 5/2 − v` maps `[1/2,2]` onto itself;
  addition `(1−x)+(1−y)+(1−(5/2−z)) = 1/2 ⟺ z = x + y`; inversion
  `V_I = x`, `x(2x − 1 − V_W) = −1 ⟺ V_W = 2x − 1 + 1/x` (needs `x ≠ 0`,
  given), `D`: `−V_W + 2x + y − 7/2 = −5/2 ⟺ y = V_W − 2x + 1 = 1/x`.
- Lemma 5 both directions: (⇐) every complement bus has exactly two lines,
  so the path values are forced from `V_{X_v}`, which lies in `[1/2, 2]` by
  its bounds; every ETR-INV variable has a bus `X_v`. (⇒) as verified above.
- Free injection bound `4 · 3 · 2 · 7/2 = 84 < 85` is valid and never
  binds at the intended profile.
- Size: `O(occurrences)` buses per variable path, `O(1)` per equation.
- Corollary 3's `NP`/`PSPACE` statement; Remark 5 ("constant number of
  distinct data values").

### 12. MAJOR — Verification record: the script aborts and the AC spread check is largely uncertified

Location: Section 5; `solve_ac` and `run_case` in the script.

As run here (details in Finding 10), the script aborts on the third case
because an AC feasibility solve times out and `solve_ac` asserts on the
status; the 300 s spread solve on case 2 ends with an upper bound of `54.3`,
so only the trivial instance `x*x = 1` has a certified zero-angle bound. The
draft's Section 5 says the script "certif[ies] that only zero-angle solutions
exist" on "the same instances"; the status line must record exactly what
was certified. Fixes: return and print the status on `TIME_LIMIT` rather
than asserting; run the DC checks for all cases before any AC solve (or make
the AC part optional) so a slow AC solve cannot suppress the Theorem 1
evidence; and, after Finding 1 is resolved, state which semantics the
spread check tests.

## Verdict

FAIL as written, because of Finding 1: Theorem 2's proof (Lemma 4) is
valid only for real polar angle variables, while the draft's problem
definition, `∃R`-membership encoding, and verification code use the
per-line principal-value constraint, under which Lemma 4 is false (explicit
cycle counterexample). Theorem 1, Lemma 5, the gadget algebra, the degree and
data claims, and the script's implementation of the reduction all pass.
With the semantics fixed to real angles, the membership paragraph rewritten
as sketched in Finding 1, and the minor edits above, I would expect PASS
WITH CORRECTIONS on re-review.
