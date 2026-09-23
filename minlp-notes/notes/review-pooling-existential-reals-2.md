# Referee report 2: `results/pooling-existential-theory-of-reals.md`

Date: 2026-09-05. Scope: independent audit of the reduction ETR-INV → POOL,
the membership argument, the corollaries, the theorem statement, and
`code/pooling_existential_reals/build_and_check.py`. The draft was not
edited. Note on versions: the draft was revised on disk while this audit was
in progress (uncommitted working-tree changes to `M`, the cost set, the
in-degree bound, Corollary 3, and Remark 2). Findings below refer to the
revised text; items that the revision already resolved are listed at the end
so the record shows they were independently found. Audit scripts are in
`/tmp/etr_audit/` (not committed).

## Method

1. Reconstructed the instance for `x + x = y`, `x·y = 1` from Sections
   4.1–4.7 alone, before reading the code; encoded that reconstruction with
   the text's parameters (diluent and slack capacity `B`; all four pools
   `P_v, P̄_v, R_v, R̄_v` for both variables); checked it exactly with sympy
   and numerically with Gurobi.
2. Traced Lemmas 4–6 by hand, including the requested boundary cases.
3. Ran the repository script and compared it with the text.
4. Checked the cited statements in Abrahamsen–Miltzow (`/tmp/etrinv.txt`),
   Abrahamsen–Adamaszek–Miltzow (arXiv 1704.06969, text extracted from the
   PDF), and Haugland 2016 (local `fulltext.md`, Section 2.1).

## A. Reconstruction of the tiny instance

Equations: addition with summands `x, x` and sum `y`; inversion `x·y = 1`.
Non-slack terminal arcs per forced pool: `P_x`: 2 (feed of `R_x`, inversion
arc `(P_x, t_inv)`); `P̄_x`: 1; `R_x`: 2 (both summands); `R̄_x`: 0; `P_y`: 1;
`P̄_y`: 1; `R_y`: 0; `R̄_y`: 2 (inversion emission, addition arc
`(R̄_y, t_add)`). So `M = 2`, `B = 7`.

Nodes and data (capacity; quality or bounds; F = forced):

- Sources: `s_x, s_y` (5/2, q=1, F); 8 diluents (7, q=0); 7 relay sources
  (2, q=0, F), one per emission (feeds of `R_x, R̄_x, R_y, R̄_y`; inversion
  emission from `R̄_y`; two addition emissions from `R_x`); 4 flip sources
  (2, q=1, F) for the four feeding emissions.
- Pools: `P_x, P̄_x, R_x, R̄_x, P_y, P̄_y, R_y, R̄_y` (7, F); 7 relay pools
  (2); 4 + 4 flip pools `p_2`, `p_3` (2); `p_c` (5/2); `p_+` (4).
- Terminals: 7 emission terminals (2, `ℓ=u=1/14`, F); 4 flip terminals
  (2, `[0,1]`, F); `t_inv`, `t_add` (5/2, `ℓ=u=2/35`, F); 8 slack terminals
  (7, `[0,1]`).
- `ζ = 5 + 14 + 8 + 56 + 14 + 8 + 5 = 110`. Costs occurring: 0, −1, −2.
  Totals: 21 sources, 25 pools, 21 terminals, 68 arcs.

(i) With `x = 1/√2`, `y = √2`, the intended flow (Lemma 5 values, flip
values, `x_{P_x t_inv} = y`, `x_{p_c t_inv} = 5/2 − y`, `x_{p_+ t_add} = 2x`,
`x_{R̄_y t_add} = 5/2 − 2x`, diluents `7 − a`, slacks `7 − Σ`) is exactly
feasible, every forced node is saturated, and the profit is exactly 110.
Verified symbolically on all 68 arcs and all node and quality constraints.

(ii) Saturation forces the equations. `s_x` saturated: `x_{s_x P̄_x} = 5/2 − x`.
Emission from `P_x`: `x·x_{P_x t} = 1` with `x_{P_x t} ≤ 2`, so `x ≥ 1/2`; the
flip delivers `1/x` at quality 1 into `R_x`. Both emissions from `R_x` deliver
`x`. `t_add` saturated: `x_{R̄_y t_add} = 5/2 − 2x`; its quality constraint
with `w_{R̄_y} = 1/((5/2 − y)·7)` gives `2x = y`. `t_inv` saturated:
`x_{P_x t_inv} = y`; its quality constraint gives `x·y = 1`. Gurobi on the
same instance: maximum profit 110.0000000; minimum and maximum of
`x_{s_x P_x}` subject to profit ≥ 110 − 1e−7 are both 0.70710678, and of
`x_{s_y P_y}` both 1.4142135. Every arc value is determined by `(x, y)` in
this trace, so the threshold-feasible flow is unique.

Answers to the specific ambiguity questions: the list of emissions is
implicit but recoverable from 4.4–4.6; the addition arc `(R̄_z, t)` needs no
relay (`p_+` plays the relay-pool role, as the text says); the inversion arc
`(P_x, t)` likewise uses `p_c` as its relay pool and is now (revised line
124–127) counted in `M`; emissions from `P_v` deliver quality 0 and only the
feeds of `R_v`, `R̄_v` are flipped to quality 1; `M = 2`, `B = 7` for this
instance in both the text and the code.

## Findings against the revised draft

1. **MINOR — Corollary 3 proof, `a ≠ 0` (lines 25, 325–326).** The linear
   extension of Abrahamsen–Miltzow (Definition 5, `/tmp/etrinv.txt` lines
   192–197) only says `x ↦ a·π(x) + b` is a bijection `V(Ψ) → V(Φ_α)`; when
   both sets are single points this holds for `a = 0`, `b = α` as well, so
   `a ≠ 0` does not follow from the cited statement when `α ∈ Q`. For
   irrational `α`, `a ≠ 0` is forced (`b` is rational). Fix: either state
   Corollary 3 for irrational `α` (the rational case is trivial anyway), or
   add "if `a = 0` then `α = b ∈ Q`, and any arc works".

2. **MINOR — Corollary 3 proof, "correspond bijectively" (line 330).**
   The bijection needs that every arc value of a saturated flow is
   determined by `(v)_v`. This is true (Sections 4.2–4.6 fix every arc of
   each gadget; diluent and slack arcs are fixed by the forced throughput
   `B`), and it is what makes "exactly one threshold-feasible flow" (line
   24) valid, but Lemma 6's proof only derives the values it needs. Add one
   sentence: "in a saturated flow all arc values are determined by the
   values `x_{s_v P_v}` (each section fixes every arc of its gadget, and
   diluent and slack arcs are fixed by the throughput `B`)".

3. **MINOR — Section 7 (lines 402–403) says the script "implements the
   reduction literally"; it does not.** Differences (none changes the
   numerical conclusions):
   - Diluent sources and slack terminals have capacity `BIG = 1000`, not `B`
     (code lines 98, 106, 148–150, 157–158, 163–164).
   - `R_v`, `R̄_v` are created only when a gadget uses them (code lines 153,
     159), contrary to the revised Section 4.7 (lines 279–281). Otherwise
     the range-enforcing emission is terminated in an unforced
     pool–terminal pair `pv → tv` of capacity 2 (code lines 194–202), a
     structure absent from the text. For `x + x = y, x·y = 1` the code's
     instance has 6 forced pools and `ζ = 88`; the text's has 8 and
     `ζ = 110`. Both pin `x` to `1/√2` (verified).
   - Code lines 168–173 are a dead loop; `diluent_pool` (line 104) is
     unused. `w` is bounded to `[0,1]` (line 215), harmless here.
   Either align the code with the text or say in Section 7 that the script
   uses large diluent/slack capacities and omits unused inverse pools.
   Run result: `ALL OK`; satisfiable optima equal `ζ` to within 3e−8;
   unsatisfiable optima are below `ζ` by 0.55 and 0.17, with Gurobi upper
   bounds 140.4588 and 144.8361 confirming gaps ≥ 0.54 and ≥ 0.16, so the
   "at least 0.15" claim is supported. The code counts `M` correctly
   (inversions add to `need[x]['P']`), matching the revised definition.

4. **MINOR — numbering (lines 13, 347).** "Remark 3" collides with
   Corollary 3. Renumber (e.g. Remark 7).

5. **REMARK — Lemma 4 consequence (line 159).** "profit at least `ζ` iff it
   is feasible and every forced node is saturated" mixes two conditions:
   for any flow satisfying capacity and conservation, profit ≥ `ζ` is
   equivalent to saturation; quality feasibility is a separate requirement
   of POOL. Reword.

6. **REMARK — Section 6 item 3 (line 366).** The existence of an
   `ε`-feasible, `ε`-optimal flow with polynomially many bits is asserted
   without proof. Plausible, but mark it as an aside.

7. **REMARK — model fidelity (Section 1).** Haugland 2016, Section 2.1
   (`fulltext.md` lines 61–79) matches the draft: `A ⊆ (S×P) ∪ (P×T)`,
   node capacities, quality matrix free at zero-throughput pools, terminal
   constraint proportional to inflow, lower bounds explicitly admitted.
   Two points worth a sentence: Haugland writes feasibility "for any
   quality matrix `w` of `x`"; since `w` is free only where it multiplies
   zero flow, "for any" and "for some" coincide, which justifies the
   draft's "for some". And Haugland's model has no source–terminal arcs at
   all (removed WLOG), so that restriction in Theorem 1 is automatic in his
   model and only informative for others.

8. **REMARK — citations.** AAM 2018 (arXiv 1704.06969): Definition 5
   defines ETR-INV with forms `x = 1`, `x + y = z`, `x·y = 1`; Theorem 7
   states ∃R-completeness. Both verified. Abrahamsen–Miltzow's ETR-INV
   (Definition 19) has no `x = 1` form, so the normalized form of Section 2
   is exactly their problem and Corollary 3 needs no normalization.
   Journal-version numbering not checked.

## Checks that passed

- **Lemma 4 (B).** An arc has one tail (source or pool) and one head (pool
  or terminal), so it lies in at most two forced groups. Forced source →
  forced pool: −1 (the pool's group is its outgoing arcs). Forced pool →
  forced terminal: −2. Forced pool → slack terminal: −1. The group-sum
  identity and "equality iff all tight" hold in every case.
- **Lemma 5 boundary cases (C).** Emitted value 2 (`a = 1/2`): relay pool
  throughput 0, its quality arbitrary but multiplied by `x_{p't} = 0`; relay
  source sends 0 to `p'` and 2 on the delivering arc. `a = 2`: emitted 1/2,
  relay 3/2. Flip with delivered value 2: `p_3` has throughput 0; harmless
  since `t_2` is vacuous (qualities in `{0,1}` make `[0,1]` vacuous). The
  step `a·x_{Qt} = 1 ⇒ a > 0` uses `x_{Qt} ≥ 0`. Inversion with `x = y`:
  `x_{P_x t} = x`, giving `x² = 1`. Addition with `z = 2`: `x_{R̄_z t} = 1/2`,
  `w_{R̄_z} = 2/B`, product `1/B`. `x + y > 4` is impossible; `x + y > 5/2`
  would force `x_{R̄_z t} < 0`, so no saturated flow, consistent with
  `z ≤ 2`.
- **Range enforcement (D).** `R_v`, `R̄_v` and their feeding emissions exist
  for every variable regardless of occurrence (revised 4.7). Feed of `R_v`:
  `v > 0`, `1/v ≤ 2`; feed of `R̄_v`: `5/2 − v > 0`, `1/(5/2 − v) ≤ 2`. Lemma
  5's hypothesis (one quality-1 arc plus one diluent) holds at all four
  pool types.
- **Membership and corollaries (E).** Section 3: degree-2 system, `w` free
  at zero throughput, denominators cleared. Corollary 2 correct. Revised
  Corollary 3: `V(Φ_α) = {α}` is compact; rational equivalence puts `x*` in
  `Q(α)^n` (= `Q[α]^n`); the (⇒) flow values are rational functions of
  `x*`; the (⇐) map reads off coordinates; "only irrational optimal
  solutions" follows because the optimum equals `ζ` (attained; upper bound
  by Lemma 4). Apart from Findings 1–2 the proof is sound.
- **Theorem statement (F).** Revised list is accurate: in-degree of every
  pool ≤ 2 (forced pools and `p_+`: 2; others: 1); costs `{0,−1,−2}`;
  capacities `{2, 5/2, 4, B}` with `B ≤ 4m + 5`; qualities `{0,1}`; no
  source–terminal arcs. Not stated but delivered: every terminal has
  in-degree ≤ 2, every source has out-degree ≤ 2, every non-forced pool has
  out-degree 1; only forced pools have unbounded out-degree
  (`1 +` number of non-slack terminal arcs `≤ M + 1`). Consider adding the
  terminal and source degree bounds to Theorem 1.
- **Size (4.9).** `M ≤ max(2m, m + 1) ≤ 2m + 1` is right; `R_v` reaches
  `2m` when every addition is `v + v = z_i`.
- **Remark 3 (negated attribute).** Correct, including the zero-throughput
  case.

## Findings already resolved by the concurrent revision

Recorded because this audit found them independently before the revision
appeared; each was verified against the previous text.

- Definition of `M` undercounted the inversion arcs `(P_x, t)`. Witness:
  variables `x, y, w, y1, y2, y3`, equations `x + x = y`, `y + y = w`,
  `x·y_i = 1` (unique solution `x = 1/2, y = 1, w = 2, y_i = 2`); `P_x` must
  carry `2 + 2 + 2 + 2 = 8`, but the old `M = 2` gave `B = 7`. Gurobi with
  `B` forced to 7: optimum 264.4298 (bound 264.4366) < ζ = 264.5, a
  yes-instance mapped to a no-instance; with the code's `M = 4`, `B = 11`,
  the threshold is reached. The revised definition (lines 124–130) fixes
  this and matches the code.
- `M ≤ m + 2`, `B ≤ 2m + 7` were false (now `2m + 1`, `4m + 5`).
- "in-degree at most three" (now two); cost set `{0,−1,−2,−3}` (now
  `{0,−1,−2}`).
- "arbitrarily high algebraic degree" was not implied by the cited
  Corollary 2 alone; the revision now argues via Theorem 1's linear
  extension (subject to Findings 1–2).
- Remark 2 needed node-throughput lower bounds, not arc lower bounds (now
  stated).

## Verdict

**PASS WITH CORRECTIONS.** The reduction is correct and the revised
statement matches what the construction delivers. Remaining corrections are
small: the `a ≠ 0` justification and the explicit uniqueness sentence in
Corollary 3 (Findings 1–2), the description of the script in Section 7
(Finding 3), and the Remark numbering (Finding 4).
