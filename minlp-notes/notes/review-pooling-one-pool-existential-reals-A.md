# Referee report A: `results/pooling-one-pool-bypass-existential-reals.md`

Date: 2026-09-05. Reviewer: independent adversarial audit. Scope: the full
draft; Sections 1–4.1 of `results/pooling-existential-theory-of-reals.md`
(forcing lemma, ETR-INV, membership); Haugland (2016) Section 2.1 and
Theorem 2 with proof (local fulltext); Alfaki–Haugland (2013) Section 2
(local fulltext, arc set); Boland–Kalinowski–Rigterink (2017) Sections 1–3
and Theorem 1 (local fulltext); Abrahamsen–Adamaszek–Miltzow Definition 5;
`results/fixed-parameter-linear-fibers-np-membership.md` (statement); and
`code/pooling_existential_reals/one_pool_build_and_check.py`, which I ran.

Method: I re-derived every identity in Lemmas 3–5, enumerated the arcs at
every node kind, recomputed the arc costs from the forcing rule with bypass
arcs present, checked every case split in Lemma 4 (variables occurring only
as `z`, only in additions, in no equation, and additions with a repeated
or coincident name), and compared the script to the text item by item.

The mathematics is correct. All findings are citation precision, wording,
or redundancy; none affects Theorem 1 or Corollary 2.

## Findings

### 1. MINOR — Section 1 does not write the capacity constraints, which now include bypass arcs

Location: Section 1, "A flow `x ≥ 0` satisfies the source, pool, and
terminal capacity constraints".

The forcing lemma (general theorem, Lemma 4) rests on `out(s) ≤ b_s` and
`in(t) ≤ b_t` where `out(s)` and `in(t)` now include the bypass arc
`(a_j,t_j)`. Lemma 3(2) uses exactly this (`X_{a_j} + x_{a_j t_j} = 2` and
`x_{pt_j} + x_{a_j t_j} = 2`). The terminal inflow `I_t` is defined with the
direct flows, but the source constraint is never displayed.

Fix: display `x_{sp} + sum_t x_{st} ≤ b_s`, `X ≤ b_p`, `I_t ≤ b_t`, and
state that with these the forcing lemma's proof is unchanged. Otherwise the
model matches Alfaki–Haugland (2013, Section 2: `A ⊆ (S×I) ∪ (S×T) ∪ (I×T)`)
and the terminal constraint with direct arcs is correctly stated (mass
`w^k x_{pt} + sum_s q_s^k x_{st}`, inflow `I_t = x_{pt} + sum_s x_{st}`).
The zero-throughput convention is stated and is harmless with bypasses,
since `w` then multiplies `x_{pt} = 0` only.

### 2. MINOR — Attribution of lower bounds to Haugland's Section 2.1

Location: Section 1, first sentence.

Haugland (2016) Section 2.1 defines only upper bounds `u_t^k`; the lower
bounds `ℓ_t^k` appear in his Section 4 (network `D^min`, Lemmas 6–9,
Theorem 4) and in his summary of the Alfaki–Haugland one-pool reduction.
The draft's model is "Haugland Section 2.1 + direct arcs + lower bounds".

Fix: say so, e.g. "Haugland's model (2016, Section 2.1) with the lower
quality bounds he uses in Section 4 and with source–terminal arcs, i.e. the
standard pooling problem of Alfaki and Haugland (2013) with lower bounds."
(The same imprecision exists in the general theorem file and is presumably
covered by its audit.)

### 3. REMARK — Arc costs: the draft is right; an explicit inventory would prevent a natural misreading

Location: Section 2, "Costs and threshold", and Theorem 1's bullet
"arc costs lie in `{0,-1,-2}`".

With the general theorem's groups (arcs leaving a forced source, arcs
*leaving* the forced pool, arcs entering a forced terminal), the costs are:

| arc | groups | cost |
|---|---|---|
| `(s_v,p)`, `(f,p)` | none | `0` |
| `(a_j,p)` | forced source | `-1` |
| `(a_j,t_j)` | forced source, forced terminal | `-2` |
| `(p,t_j)` | forced pool, forced terminal | `-2` |
| `(p,t_0)` | forced pool | `-1` |

So all three values `0,-1,-2` occur, and
`-sum_a c_a x_a = sum_j out(a_j) + X + sum_j in(t_j) ≤ 2·#aux + B + 2·#aux = ζ`,
matching `ζ = B + 4·(number of auxiliaries)`. Note the pool group contains
only the pool's outgoing arcs, so throughput is counted once. The referee
brief I was given listed `(a_j,p)` at `-2` and `(s_v,p)`, `(f,p)` at `-1`;
that would put pool-entering arcs in the pool group too, count `X` twice,
and require `ζ = 2B + 4·#aux`. The draft does not do this and is
consistent; the script maximizes the group totals directly (pool counted
once via `Y`) and reports `ζ = 20 = 12 + 4·2` for `x·x = 1`, as the text
predicts. Suggest adding the table above to Section 2.

### 4. MINOR — Intro bullet on Haugland Theorem 2: two imprecisions

Location: introduction, first comparison bullet.

(a) "one per subset of terminals receiving pool flow" describes the
`2^{|T|}` family only; the `(|T|+1)^{|K|}` family is a different
enumeration (Alfaki–Haugland 2013, Proposition 2, cited by Haugland). The
NP certificate is the subset `T^+`, and this is correct: for fixed `T^+`
the constraints are `x_{pt} = 0` (`t ∉ T^+`) and
`ℓ_t^k sum_s x_{sp} ≤ sum_s q_s^k x_{sp} ≤ u_t^k sum_s x_{sp}` (`t ∈ T^+`),
all linear.

(b) Haugland's Theorem 2 is stated for his upper-bound-only model. The
draft's model has lower bounds; the certificate argument extends verbatim
(the lower bound is the linear row just displayed), but the text should say
this rather than attribute it to the theorem. Also, NP-hardness of one pool
without bypasses (needed for "NP-complete") is Alfaki–Haugland (2013,
Section 3, reduction from MIVS with one pool), not Haugland's Theorem 2;
cite it.

Fix: "Without bypass arcs, for each subset `T^+` of terminals receiving
pool flow the feasible set is a polytope described by linear constraints
(Haugland 2016, proof of Theorem 2; the same holds with lower bounds), so
`T^+` is an NP certificate; with hardness from Alfaki and Haugland (2013),
the one-pool problem without bypasses is NP-complete."

### 5. MINOR — Boland–Kalinowski–Rigterink's model has no bypass arcs; the sentence lets "(with or without bypasses)" be read as covering it

Location: introduction, second comparison bullet.

Boland et al. (2017), Section 1: "We do not consider input-to-output arcs
since for every such arc `(i,j)`, we can add an auxiliary pool"; their
Section 3 fixes `A_I = {(v_i,ℓ)}`, `A_J = {(ℓ,w_j)}`, and only upper bounds
`µ_jk`. The auxiliary-pool replacement breaks the one-pool restriction, so
their Theorem 1 ("one pool and `m` inputs, polynomial time for every fixed
`m`") is for the no-bypass model. "Bounded number of inputs" = bounded
number of sources, as the draft says.

The linear-fiber lemma is used correctly: with one pool and fixed `|K|`
the parameters are the `|K|` pool qualities, for fixed `w` every constraint
(blending `w^k X = sum_s q_s^k x_{sp}`, terminal rows with the bypass terms,
capacities, threshold) is linear in `x`, and the capacities bound every
fiber; so NP membership holds with or without bypasses.

Fix: split the bullet: "with a fixed number of attributes, with or without
bypasses, the linear-fiber lemma gives NP membership; without bypasses and
with a fixed number of sources, Boland, Kalinowski, and Rigterink (2017,
Theorem 1) give a polynomial algorithm."

### 6. REMARK — Lemma 4: one redundant step

Location: Lemma 4, "`τ_{j_1} ≤ 2` gives `X_y ≤ 2`".

`X_y ≤ 2` already holds by the capacity of `s_y` (single arc). The step is
harmless. Everything else in Lemma 4 checks: positivity of all four
quantities from the products `= 1`; `τ_{j_2} = 1/X_y`, `τ_{j_1} = X_y`,
`X_x X_y = 1`; `X_y ≥ 1/2` from `τ_{j_2} ≤ 2`; the `x = y` case
`τ_{j_1} = τ_{j_2} = 1/X_x`, `X_x^2 = 1`; additions with `τ_j > 0` forced
by `X_z τ_j = 2`; and the range case split is exhaustive (a variable is
either an `x`/`y` of an inversion, hence bounded through it, or it gets a
range pin, which covers variables occurring only as `z`, only as
summands, or nowhere).

### 7. REMARK — Lemma 5: two bounds are stated more elaborately than needed

Location: Lemma 5, "`2/x_z ∈ [1,4]` would exceed `2` only if …" and
"`w^A ≤ (sum of at most two inflows …)/B ≤ 4/B ≤ 1`".

(a) `x_z = x_x + x_y ≥ 1` directly gives `τ_j = 2/x_z ∈ [1,2]`.
(b) `w^A` is a convex combination of qualities in `{0,1}` whenever `X > 0`,
so `w^A ∈ [0,1]` without any counting; the `4/B` bound is true but
irrelevant. The rest of Lemma 5 checks: all `τ ∈ [1/2,2]`,
`x_{a_j t_j} = 2 - τ_j ≥ 0`, `X_f, x_{pt_0} ∈ [B/2, B]` (with `n_s`
correctly excluding the filler, `sum_v X_v + sum_j τ_j ≤ 2n_s = B/2`),
pool inflow and outflow both `B`, every pinned mass equal to `κ·2`,
unpinned masses in `[0, I_t]` (including `A_{a_j}` at `t_j`, whose mass is
`τ_j^2/B + 2 - τ_j ≤ 2`), and profit `= ζ` by the group identity.

### 8. REMARK — Lemma 3: arc inventories and `q_{a_j}^A = 0` verified

Location: Lemma 3.

Each `a_j` has exactly the arcs `(a_j,p)`, `(a_j,t_j)`; no other source has
an arc into `t_j` (variable and filler sources have a single arc into `p`;
`a_i` bypasses only `t_i`), so `t_j` has exactly `(p,t_j)`, `(a_j,t_j)`.
Pins at `t_j` are on `A_{s_v}`, on `A_{a_{j_1}}` at `t_{j_2}` with
`j_1 ≠ j_2`, or on `A_{x+y}` (supported on variable sources); no pin is
ever on `A_{a_j}` at `t_j`. Hence `q_{a_j}^A = 0` for every pinned
attribute and the mass identity reduces to `w^A X_{a_j} = 2κ` with
`I_{t_j} = 2`. Correct as written.

### 9. REMARK — Normalization and name coincidences

Location: Section 2, first paragraph.

`x = 1 ↔ x·x = 1` and `x + x = y ↔ {x·u = 1, u·x' = 1, x + x' = y}` are
equivalent within `[1/2,2]` (`u = 1/x`, `x' = x`, both in range). Definition
5 also allows `x + y = z` with `z ∈ {x, y}`; the gadget handles it without
comment (the pins force `X_y τ_j = 0`, so `X_y = 0`, contradicting the
range bound in Lemma 4; Lemma 5 is vacuous since such an equation has no
solution in `[1/2,2]`). One sentence would make the case explicit.

### 10. REMARK — Script versus text

Location: Section 5 and `one_pool_build_and_check.py`.

Run output: `ALL OK`, five satisfiable and three unsatisfiable cases as the
text says, values `x = 0.707107`, `x = 0.618034` etc. Checked against the
text: variable sources capacity `2` unforced with a single arc; auxiliaries
capacity `2` forced with `(a,p)` and the bypass; pinned terminals capacity
`2` forced; filler capacity `B` with zero quality (absent from every
attribute dict); slack capacity `B`; `n_s = len(sources)` taken before the
filler is appended; `B = 4n_s`; `κ = 1/(2B)` for inversion and range pins,
`1/B` for addition pins; pins `(t_1,A_x)`, `(t_2,A_{a_1})`, `(t_2,A_y)`
and `(t,A_z)`, `(t,A_{x+y})`; range pins for variables not an `x`/`y` of
any inversion; objective = sum of forced group totals with the pool counted
once; `ζ` = sum of forced capacities. Hand check: `x·x = 1` gives
`n_s = 3`, `B = 12`, `ζ = 12 + 8 = 20`; `x + x = y, x·y = 1` gives 4
variables (with `u`, `x'`), 7 auxiliaries, `n_s = 11`, `B = 44`,
`ζ = 44 + 28 = 72`. All match the printed values.

Two small differences, neither affecting the check: the script has no
`x = 1` constraint kind (tests enter `x·x = 1` directly), so "implements
this construction" should say the `x = 1` step is done by hand; and the
script bounds `w ∈ [0,1]` as variable bounds, which is without loss of
generality (convex combination of `{0,1}` qualities when `X > 0`, and `w`
multiplies zero when `X = 0`).

### 11. REMARK — Doubling attributes with bypass arcs (Theorem 1 bullet 2, Remark 4)

With complement attribute `Ā` (`q̄_s = 1 - q_s`), the mass at a terminal is
`(1 - w^A) x_{pt} + sum_s (1 - q_s^A) x_{st} = I_t - mass^A`, so the lower
bound `ℓ I_t ≤ mass^A` becomes `mass^Ā ≤ (1 - ℓ) I_t`; the argument in
Remark 3 of the general theorem goes through with the direct-arc terms.
Qualities stay in `{0,1}`. Only the description "filler of quality `0` in
every attribute" stops being literally true after doubling; Theorem 1 does
not rely on it.

## Verdict

**PASS WITH CORRECTIONS** (all MINOR). The reduction, Lemmas 3–5, the
forcing accounting with bypass arcs, the size bound, and the script agree
with each other and with the cited sources. The corrections are: display
the capacity constraints (Finding 1), attribute the lower bounds and the
one-pool NP-hardness correctly (Findings 2, 4), and state that the
Boland–Kalinowski–Rigterink result is for the no-bypass model (Finding 5).
This report verified the forcing lemma with bypass arcs directly; the
membership argument, Remark 3 (doubling), and Corollary 3 (used in Remark 3
of the draft) are inherited from the general theorem and are covered by its
separate audit.
