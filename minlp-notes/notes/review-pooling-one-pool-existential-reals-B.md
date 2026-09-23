# Review B: one pool with bypass arcs is ∃R-complete

Target: `results/pooling-one-pool-bypass-existential-reals.md` (draft of
2026-09-05). Reviewer: independent referee (global optimization and
complexity). Method: the construction was reconstructed by hand from the
text alone for one instance; the code was run and read only afterwards.

Verdict: **PASS WITH CORRECTIONS** (no blocking or major mathematical
errors; corrections are notation, cross-references, and one comparison
claim that must be scoped).

## 1. Hand reconstruction

Instance: variables `x, y`; equations `x·y = 1` and `x + x = y`.

**Normalization (Section 2).** `x + x = y` has a repeated summand, so it
becomes `x·u = 1`, `u·x' = 1`, `x + x' = y` with fresh `u, x'`. Normalized
instance: `V = {x, y, u, x'}`, equations

- E1 `x·y = 1` (inversion), E2 `x·u = 1` (inversion),
- E3 `u·x' = 1` (inversion, roles: "x" = `u`, "y" = `x'`),
- E4 `x + x' = y` (addition, summands distinct); `m = 4`.

Within `[1/2,2]`, E2 and E3 give `u = 1/x`, `x' = 1/u = x`, so the
normalized instance is equivalent to the original.

**Auxiliaries.** E1: `j_1, j_2`; E2: `j_3, j_4`; E3: `j_5, j_6`; E4: `j_7`.
Range rule: every variable is an `x` or `y` of some inversion (`x` in
E1, E2; `y` in E1; `u` in E2, E3; `x'` in E3), so no range auxiliary.
Total 7 auxiliaries. `n_s = 4 + 7 = 11`, `B = 44`.

**Sources** (capacity, forced?, arcs):

| source | cap | forced | arcs |
|---|---|---|---|
| `s_x, s_y, s_u, s_x'` | 2 | no | `(s_v, p)` |
| `a_1 … a_7` | 2 | yes | `(a_j, p)`, `(a_j, t_j)` |
| `f` (filler) | 44 | no | `(f, p)`; quality 0 in every attribute |

**Pool** `p`: forced, capacity 44, in-degree 12, out-degree 8.

**Attributes** (12): `A_{s_x}, A_{s_y}, A_{s_u}, A_{s_x'}` (quality 1 at
the named source only), `A_{a_1} … A_{a_7}` (quality 1 at `a_j` only),
`A_{x+x'}` (quality 1 at `s_x` and `s_x'`, 0 elsewhere, including at every
`a_j` and at `f`).

**Terminals** (capacity, forced?, incoming arcs, pins with `κ`):

| terminal | cap | forced | in-arcs | pins (`ℓ = u = κ`) |
|---|---|---|---|---|
| `t_1` | 2 | yes | `(p,t_1)`, `(a_1,t_1)` | `A_{s_x}: 1/88` |
| `t_2` | 2 | yes | `(p,t_2)`, `(a_2,t_2)` | `A_{a_1}: 1/88`, `A_{s_y}: 1/88` |
| `t_3` | 2 | yes | `(p,t_3)`, `(a_3,t_3)` | `A_{s_x}: 1/88` |
| `t_4` | 2 | yes | `(p,t_4)`, `(a_4,t_4)` | `A_{a_3}: 1/88`, `A_{s_u}: 1/88` |
| `t_5` | 2 | yes | `(p,t_5)`, `(a_5,t_5)` | `A_{s_u}: 1/88` |
| `t_6` | 2 | yes | `(p,t_6)`, `(a_6,t_6)` | `A_{a_5}: 1/88`, `A_{s_x'}: 1/88` |
| `t_7` | 2 | yes | `(p,t_7)`, `(a_7,t_7)` | `A_{s_y}: 1/44`, `A_{x+x'}: 1/44` |
| `t_0` | 44 | no | `(p,t_0)` | none |

All unpinned bounds (all attributes at `t_0`; the other 10 or 11
attributes at each `t_j`) are `ℓ = 0`, `u = 1`, as the Pins bullet states.

**Costs** (minus the number of forced groups: arcs leaving `a_j`, arcs
leaving `p`, arcs entering `t_j`): `(s_v,p)`: 0; `(f,p)`: 0; `(a_j,p)`: −1;
`(a_j,t_j)`: −2; `(p,t_j)`: −2; `(p,t_0)`: −1. All in `{0,−1,−2}`.

**Threshold** `ζ = 44 + 7·2 + 7·2 = 72 = B + 4·7`. Profit
`= Σ_j [x_{a_j p} + 2x_{a_j t_j} + 2x_{p t_j}] + x_{p t_0}
 = Σ_j out(a_j) + Σ_j in(t_j) + X_p`, the sum of forced-group totals, so
the general theorem's Lemma 4 applies unchanged (bypass arcs simply sit in
two groups).

## 2. (a) Intended flow for `x = 1/√2`, `y = √2`

Then `u = √2`, `x' = 1/√2`, and E4 holds (`1/√2 + 1/√2 = √2`).

- `X_x = X_x' = 1/√2`, `X_y = X_u = √2`.
- `τ_1 = x_y = √2`, `τ_2 = 1/x_y = 1/√2` (E1); `τ_3 = √2`, `τ_4 = 1/√2`
  (E2); `τ_5 = x_{x'} = 1/√2`, `τ_6 = √2` (E3); `τ_7 = 2/x_y = √2` (E4).
- `x_{p t_j} = τ_j`, `x_{a_j t_j} = 2 − τ_j ∈ {2−√2, 2−1/√2} > 0`.
- `Σ_v X_v = 3√2`, `Σ_j τ_j = 11/√2`; `X_f = 44 − 17/√2 ≈ 31.98`,
  `x_{p t_0} = 44 − 11/√2 ≈ 36.22`; both in `[0, 44]`.

Capacities: `s_v ≤ √2 < 2`; `a_j`: `τ_j + 2 − τ_j = 2`; `t_j`: 2; `t_0`:
36.22 ≤ 44; pool inflow `3√2 + 11/√2 + X_f = 44 =` outflow
`11/√2 + x_{p t_0}`. Conservation holds. `X = 44 > 0`, so
`w^A = Σ_s q_s^A X_s / 44` is unique: `w^{A_{s_x}} = w^{A_{s_x'}} = 1/(44√2)`,
`w^{A_{s_y}} = w^{A_{s_u}} = √2/44`, `w^{A_{a_j}} = τ_j/44`,
`w^{A_{x+x'}} = √2/44`.

Pins (mass `= w^A τ_j + q_{a_j}^A (2 − τ_j)` must equal `2κ`; the second
term is 0 for every pinned attribute):

| pin | mass | `2κ` |
|---|---|---|
| `t_1, A_{s_x}` | `(1/(44√2))·√2 = 1/44` | `1/44` |
| `t_2, A_{a_1}` | `(√2/44)(1/√2) = 1/44` | `1/44` |
| `t_2, A_{s_y}` | `(√2/44)(1/√2) = 1/44` | `1/44` |
| `t_3, A_{s_x}` | `1/44` | `1/44` |
| `t_4, A_{a_3}` | `(√2/44)(1/√2) = 1/44` | `1/44` |
| `t_4, A_{s_u}` | `1/44` | `1/44` |
| `t_5, A_{s_u}` | `(√2/44)(1/√2) = 1/44` | `1/44` |
| `t_6, A_{a_5}` | `((1/√2)/44)·√2 = 1/44` | `1/44` |
| `t_6, A_{s_x'}` | `(1/(44√2))·√2 = 1/44` | `1/44` |
| `t_7, A_{s_y}` | `(√2/44)·√2 = 2/44` | `2/44` |
| `t_7, A_{x+x'}` | `(√2/44)·√2 = 2/44` | `2/44` |

Unpinned bounds: at `t_j` the own attribute `A_{a_j}` has mass
`τ_j²/44 + (2 − τ_j) ≤ τ_j + 2 − τ_j = 2 = I_{t_j}` (since `τ_j ≤ 44`),
and `≥ 0`; every other attribute has mass `w^A τ_j ∈ [0, τ_j] ⊆ [0, 2]`.
At `t_0` the mass is `w^A x_{p t_0} ∈ [0, x_{p t_0}]`. All forced nodes are
saturated, so profit `= 72 = ζ`. Everything checks.

## 3. (b) Proof from scratch that profit `≥ ζ` forces the solution

Let `x` be feasible with profit `≥ 72`. Profit
`= Σ_j out(a_j) + Σ_j in(t_j) + X_p ≤ 14 + 14 + 44 = 72`, so every term is
tight: `out(a_j) = in(t_j) = 2` for all `j` and `X_p = 44`.

Since `X = 44 > 0`, the quality vector is unique, `w^A = Σ_s q_s^A X_s/44`.
For each `j`: `out(a_j) = 2` with exactly two arcs gives
`x_{a_j t_j} = 2 − τ_j`; `in(t_j) = 2` with exactly two incoming arcs gives
`x_{p t_j} = 2 − x_{a_j t_j} = τ_j`. A pin `(t_j, A, κ)` with
`q_{a_j}^A = 0` (true for every pin: variable attributes are supported on
`s_v`, `A_{a_i}` on `a_i` with `i ≠ j`, `A_{x+x'}` on `s_x, s_x'`) reads
`2κ ≤ w^A τ_j ≤ 2κ`, i.e. `w^A τ_j = 2κ`. Hence:

- `κ = 1/88` on `A_{s_v}`: `X_v τ_j = 1`; on `A_{a_i}`: `τ_i τ_j = 1`;
- `κ = 1/44` on `A_{s_v}`: `X_v τ_j = 2`; on `A_{x+x'}`: `(X_x + X_x') τ_7 = 2`.

E1: `X_x τ_1 = 1`, `τ_1 τ_2 = 1`, `X_y τ_2 = 1`. All four are positive,
`τ_1 = 1/X_x`, `τ_2 = X_x`, `X_y = 1/τ_2 = 1/X_x`, so `X_x X_y = 1`. Capacity
`τ_2 ≤ 2` gives `X_x ≤ 2`; `τ_1 ≤ 2` gives `X_x ≥ 1/2`; hence
`X_x, X_y ∈ [1/2,2]`.
E2: likewise `X_u = 1/X_x`. E3: `X_x' = 1/X_u = X_x`.
E4: `X_y τ_7 = 2` and `(X_x + X_x') τ_7 = 2` with `τ_7 > 0`, so
`X_y = X_x + X_x' = 2 X_x`.

Therefore `x_{s_x p} · x_{s_y p} = 1`, `2 x_{s_x p} = x_{s_y p}`, both in
`[1/2, 2]` (so `X_x = 1/√2`, `X_y = √2`). The text's Lemmas 3–4 follow
exactly this route and are correct.

Answers to the specific questions:

- Unpinned bounds at pinned terminals and at the slack terminal: specified
  ("All unpinned bounds are vacuous, `ℓ = 0`, `u = 1`"; slack terminal
  "with vacuous bounds"). They really are vacuous for every feasible flow,
  because `w^A ∈ [0,1]` whenever `X > 0` and qualities are in `{0,1}`.
- Which attribute `A_{a_{j_1}}` refers to: well defined (the attribute of
  the auxiliary source `a_{j_1}`, one per source). But the variable
  attributes are written `A_x, A_y, A_z, A_v` in the pin list and
  `A_{s_v}` in Lemma 3; only `A_s` for a source `s` is defined. See F1.
- Ordering of `j_1, j_2`: determined by the written order `x·y = 1`
  (`j_1` is pinned to the first variable). Because the equation is
  symmetric the text should say that either order works; it does not. See
  F5.
- Filler qualities: specified ("quality 0 in every attribute").
- Auxiliary sources' qualities in `A_{x+y}`: specified by "0 elsewhere".

## 4. (c) Theorem statement and Corollary 2

- Exactly one pool: yes.
- Source qualities in `{0,1}`: yes; filler and auxiliaries are 0 in every
  attribute except `A_{a_j}` at `a_j`.
- Source out-degree ≤ 2: `s_v` 1, `f` 1, `a_j` 2. Terminal in-degree ≤ 2:
  `t_j` 2, `t_0` 1.
- Capacities: sources 2 except `f` (`B`); terminals 2 except `t_0` (`B`);
  pool `B`. Flow lower bounds zero. Costs in `{0,−1,−2}` (see Section 1).
- Lower and upper bounds: only equal pins `ℓ = u = κ` and vacuous
  `[0,1]`. The upper-bounds-only conversion (negated attribute
  `q' = 1 − q`, `u' = 1 − ℓ`) still works with bypass arcs: at a terminal
  the negated mass is `I_t − mass`, so `I_t − mass ≤ (1 − ℓ) I_t` iff
  `mass ≥ ℓ I_t`. The cross-reference to "Remark 3 of the general theorem"
  is stale (F2).
- Membership in `∃R`: the system of the general theorem's Section 3 gains
  linear bypass terms only; degree stays two. Fine.
- Size and numbers: `O(n+m)` nodes/arcs/attributes; numbers
  `2, B, 1/(2B), 1/B, 0, 1` and `ζ`. Correct.
- Corollary 2: follows from Theorem 1 as in the general theorem's
  Corollary 2. Correct; it could add "and it lies in `∃R ⊆ PSPACE`".
- Remark 3 (transfer of the algebraic-degree corollary): every
  threshold-feasible flow is determined by `(X_v)` alone
  (`τ` values are `1/X_x`, `X_x`, `2/X_z`, `1/X_v`; `X_f` and `x_{p t_0}`
  are `B` minus sums), and `(X_v)` solves the normalized instance, whose
  solutions project bijectively onto those of the original. So the
  bijection claim holds. Note the general theorem's Corollary 3 was revised
  to "irrational α"; the transferred statement inherits that hypothesis.

## 5. (d) Comparison claims

**Haugland (2016), Theorem 2** (`fulltext.md`, p. 7): "If `|P| = 1`, the
Pooling Problem can be solved in terms of `min{(|T|+1)^{|K|}, 2^{|T|}}`
compact linear programs." The proof for the `2^{|T|}` bound: since all
terminals receive flow only from the pool, `x` is feasible iff for every
`t`, `x_{pt} = 0` or `w^k ≤ u_t^k` for all `k`; for a fixed set `T⁺` of
terminals with positive flow, the conditions
`Σ_s q_s^k x_{sp} ≤ u_t^k Σ_s x_{sp}` are linear in `x`. Guessing `T⁺` and
solving one LP (with the cost threshold as a row) is a polynomial-time
verifiable certificate, so the decision problem is in NP. Lower bounds are
covered by Haugland's negation convention (p. 4), and strong NP-hardness
with one pool is his Theorem 1 (Alfaki–Haugland), whose construction uses
lower and upper bounds and one attribute per vertex. The claim "one-pool
without bypasses is NP-complete" is correct. Two nits: the "one per subset
of terminals receiving pool flow" description fits only the `2^{|T|}`
option (the `(|T|+1)^{|K|}` option comes from Alfaki–Haugland Proposition
2 and enumerates something else); and Haugland's model (Section 2.1) has
no source–terminal arcs at all, so "without bypass arcs" is the whole of
his setting, not a restriction of it (F6).

**Linear-fiber lemma** (`results/fixed-parameter-linear-fibers-np-membership.md`,
"Pooling consequence"): for fixed numbers `p` of pools and `k` of quality
coordinates, with rational data and finite flow bounds, the decision
problem is in NP "including arbitrary direct input-output arcs and lower
flow bounds". With `p = 1` this is exactly the claim "with a fixed number
of attributes (with or without bypasses) … NP membership". The one-pool
instances have finite node capacities, so the bounded-fiber hypothesis
holds. Correct. (Counting convention: a lower-and-upper bounded attribute
is one coordinate there; after doubling it is two; both fixed.)

**Boland, Kalinowski, Rigterink (2017)** (`fulltext.md`, abstract, Section
1, Theorem 1): "the pooling problem with one pool and a bounded number of
inputs can be solved in polynomial time". Their model explicitly excludes
input-to-output arcs ("We do not consider input-to-output arcs since …
we can add an auxiliary pool", Section 1) and has upper quality bounds
only. Their algorithm, like Haugland's, relies on outputs receiving flow
only from the pool (the LP(J′) family). So the polynomial-time claim is
established only **without bypasses**. In the result text this clause is
attached to the bullet that begins "with a fixed number of attributes
(with or without bypasses)", and a reader will carry the parenthetical
over to Boland. With bypasses and a bounded number of sources, only NP
membership follows (pool quality lies in a fixed-dimensional simplex, so
the linear-fiber lemma applies); a polynomial algorithm is not claimed by
anyone. Scope the sentence (F3).

The concluding sentence "bypass arcs together with an unbounded attribute
count are exactly what lifts the one-pool problem from NP to ∃R" is
justified by the first two items alone.

## 6. Code run and discrepancies

`~/miniconda3/envs/minlp-notes/bin/python one_pool_build_and_check.py`
(Gurobi 13, academic license) ran to completion and printed `ALL OK`.
For the audited instance it reports `sources=12 attrs=12 terms=8 B=44
zeta=72` (12 sources includes the filler; 8 terminals includes the
slack), `best = 71.999999985`, `bound = 72.0`, `x = 0.707107`,
`y = 1.414214`. This matches the hand reconstruction of Section 1 exactly
(11 non-filler sources, 12 attributes, 7 pinned terminals, `B = 44`,
`ζ = 72`). Five satisfiable cases reached `ζ` within `2e-8`; the three
unsatisfiable cases stopped at `50.5`, `122.25`, `71.0` against thresholds
`52`, `124`, `72`, with proven bounds within `1e-3`.

Code versus text:

- The script does not construct arc costs. It maximizes the sum of
  forced-group totals `Σ out(a_j) + X_p + Σ in(t_j)`, which equals the
  profit by the forcing lemma (verified in Section 1 above). Equivalent,
  but the verification record should say that costs are not materialized
  (the general theorem's script claims to build costs and `ζ` literally;
  this one does not).
- The script bounds `w ∈ [0,1]` as variable bounds; the text leaves `w`
  arbitrary when `X = 0`. Harmless: when `X = 0` all `x_{pt} = 0`.
- Addition attributes are keyed by the ordered pair `(x, y)`, so two
  additions `x + y = z` and `x + y = z'` share one attribute while
  `y + x = z'` gets another. The text says one attribute per addition.
  Both are correct; the difference is immaterial.
- The script accepts only `add` and `inv` constraints; the text's
  normalization step `x = 1 → x·x = 1` must be done by the caller.
- The range rule, the repeated-summand normalization, `B = 4 n_s`,
  `κ ∈ {1/(2B), 1/B}`, capacities, pins, and vacuous `[0,1]` bounds match
  the text.

## 7. Findings

1. **MINOR** (Section 2, pins; Section 3 first paragraph after Lemma 3).
   The pin list writes `A_x`, `A_y`, `A_z`, `A_v` for the attribute of
   variable `v`, but only `A_s` for a source `s` is defined, and Lemma 3
   writes `A_{s_v}`. Fix: define `A_v := A_{s_v}` once, or write
   `A_{s_x}`, `A_{s_y}`, `A_{s_z}` throughout.

2. **MINOR** (Theorem 1, second bullet; Remark 4). "Remark 3 of the general
   theorem" no longer exists; the general theorem now calls it "Section 6,
   item 1". Fix the two cross-references, and add the one-line argument
   that the negation trick survives bypass arcs (the negated mass at a
   terminal is `I_t − mass`, so `≤ (1 − ℓ) I_t` iff `mass ≥ ℓ I_t`).

3. **MINOR** (introduction, second comparison bullet). Boland, Kalinowski,
   Rigterink (2017) work in a model without input-to-output arcs
   (their Section 1) and with upper bounds only; their LP(J′) enumeration
   needs every output to be fed by the pool alone. Rewrite so that "with
   or without bypasses" attaches only to the linear-fiber lemma, e.g.
   "…and, without bypasses, with a fixed number of sources Boland et al.
   (2017) give a polynomial algorithm."

4. **MINOR** (Section 1, Model). The source and terminal capacity
   constraints are not written; with bypass arcs they must read
   `Σ_p x_{sp} + Σ_t x_{st} ≤ b_s` and `I_t ≤ b_t`. Lemma 3(2) relies on
   the source constraint counting the bypass arc. Fix: display the three
   capacity constraints.

5. **REMARK** (Section 2, inversion pins). The equation `x·y = 1` is
   symmetric but the gadget is not (`j_1` is pinned to the first-named
   variable). Say that the roles are fixed by an arbitrary ordering of the
   two variables; either choice is correct, as Lemma 4 shows.

6. **REMARK** (introduction, first comparison bullet). Haugland's Theorem
   2 gives `2^{|T|}` LPs "one per subset of terminals receiving pool
   flow"; the `(|T|+1)^{|K|}` alternative is a different enumeration
   (Alfaki–Haugland Proposition 2). Either drop the `min{…}` or describe
   only the `2^{|T|}` branch, which is the one that yields the NP
   certificate.

7. **REMARK** (Section 2, normalization). The text does not say why the
   repeated-summand rule is needed (the attribute `A_{x+x}` would need
   quality 2 at `s_x`). One sentence would help. A simpler alternative
   avoids the rule entirely: for `x + x = y` use one auxiliary `j` with
   pins `(t_j, A_{s_y}, 1/B)` and `(t_j, A_{s_x}, 1/(2B))`, giving
   `X_y τ_j = 2`, `X_x τ_j = 1`, hence `X_y = 2X_x`, with
   `τ_j = 1/X_x ∈ [1/2,2]`. This removes two variables and two inversions
   per repeated-summand addition and needs no addition attribute. Optional.

8. **REMARK** (Section 5, verification record). State that the script
   maximizes the forced-group sum rather than building the arc costs
   (equivalent by the forcing lemma), and that `x = 1` equations are not
   accepted by the script. See Section 6 above for the other, immaterial,
   code–text differences.

9. **REMARK** (Corollary 2). Add "it is in `∃R ⊆ PSPACE`" for symmetry
   with the general theorem's Corollary 2.

No BLOCKING or MAJOR finding. The reduction, Lemmas 3–5, the theorem's
restrictions, and the two NP-membership comparisons that support the
"exactly what lifts" sentence are correct as reconstructed and verified
by hand on the instance `x·y = 1`, `x + x = y`, and the script agrees with
the hand construction.

## Verdict

**PASS WITH CORRECTIONS**: apply findings 1–4 (notation, stale
cross-references, scoping of the Boland claim, explicit capacity
constraints); findings 5–9 are optional improvements.
