# Referee report 1: `results/pooling-existential-theory-of-reals.md`

Date: 2026-09-05. Reviewer: independent audit (adversarial). Scope: the full
draft, Haugland (2016) Section 2.1 (local fulltext), Abrahamsen–Adamaszek–
Miltzow Definition 5 / Theorem 7, Abrahamsen–Miltzow (toolbox) Definition 19,
Theorem 1, Corollary 2, Definitions 4–5, and the script
`code/pooling_existential_reals/build_and_check.py`, which I ran.

Summary of the audit method: I re-derived every algebraic identity in
Sections 4.2–4.8, enumerated the in/out arcs of every node kind (listed in
Finding 12), checked both directions of Lemma 6 against that enumeration, and
built a concrete instance to test the one place where the text and the code
differ in a way that matters (Finding 1).

## Findings

### 1. MAJOR — `M` as defined in the text undercounts the outflow of `P_x`; the (⇒) direction of Lemma 6 fails on concrete instances

Location: Section 4 ("Let `M` be the largest number of emission terminals
(defined in 4.3) attached to any single forced pool"), Section 4.5, Section
4.7 ("at most `M` emission arcs each carrying at most 2 ... `B - 2M = 3`").

The inversion gadget (4.5) adds the arc `(P_x, t)` to a terminal `t` of
capacity `5/2` that is *not* an emission terminal in the sense of 4.3
(different capacity and bounds). Section 4.6 explicitly declares that the
analogous arc `(R̄_z, t)` "is counted as an emission of `R̄_z` for the purpose
of defining `M`"; Section 4.5 contains no such sentence. Under the literal
definition, `M` ignores all inversion arcs leaving `P_x`, each of which
carries `y ≤ 2`, so the slack bound `B - 2M ≥ 3` in 4.7 is false and the
saturating assignment of the (⇒) direction can violate the capacity of `P_x`.

Concrete counterexample (verified numerically). `Φ`: `u + u = w`, `w·w = 1`,
`u·y_1 = 1`, `u·y_2 = 1`, `u·y_3 = 1`. Its unique solution in `[1/2,2]^5` is
`u = 1/2, w = 1, y_i = 2`. With the text's definition, `M = 2` (attained at
`R_u` and `R̄_w`), so `B = 7`. In any saturated flow `P_u` must send
`1/u + y_1 + y_2 + y_3 = 8 > 7 = B`. Building the instance with `B = 7`
(`build(V, C, B=7)`) and solving to optimality gives profit `213.8889 < ζ =
214` (Gurobi status OPTIMAL, bound `213.8889`), i.e. the reduction as written
answers NO on a YES instance. With the script's own count (`M = 4`, `B = 11`)
the optimum is `ζ = 274` with the correct values. The script is right; the
text is wrong.

Proposed fix: define `M` as the maximum, over forced pools `Q`, of the number
of arcs from `Q` to terminals other than its slack terminal (equivalently:
emission terminals, inversion terminals, and addition terminals). Add to 4.5
the sentence already present in 4.6. Then every such arc carries at most `2`
(`1/a ≤ 2`, `y ≤ 2`, `5/2 - z ≤ 2`) and 4.7 goes through unchanged.

### 2. MINOR — The bound `M ≤ m + 2` is false

Location: Section 4 (`M ≤ m + 2`), Section 4.9 (`B ≤ 2m + 7`).

`R_v` receives one emission per *summand slot* equal to `v`. For
`x + x = y_1, x + x = y_2, x + x = y_3` (`m = 3`) the pool `R_x` has six
emissions, exceeding `m + 2 = 5`. Correct counts, with `M` defined as in
Finding 1: `P_v ≤ m + 1`, `P̄_v = 1`, `R_v ≤ 2m`, `R̄_v ≤ m`; hence
`M ≤ max(m + 1, 2m) ≤ 2m + 1` and `B ≤ 4m + 5`. Only the size claims are
affected; polynomial boundedness survives.

Proposed fix: replace `M ≤ m + 2` by `M ≤ 2m + 1` and `B ≤ 2m + 7` by
`B ≤ 4m + 5`.

### 3. MINOR — Arc costs never reach `-3`

Location: Theorem 1 (bullet "arc costs lie in `{0,-1,-2,-3}`"), Section 4.1
("Thus `c_a ∈ {0,-1,-2,-3}`"), Section 4.9.

The three forced groups are arcs *leaving* a forced source, arcs *leaving* a
forced pool, and arcs *entering* a forced terminal. An arc `(s,p)` can lie
only in the first group; an arc `(p,t)` only in the last two. So
`c_a ∈ {0,-1,-2}`; the "thus" is a non sequitur. The claim as stated is not
false (a superset), but the theorem should state the tight set. The script's
`cost()` agrees with the group definition and also never produces `-3`.

Proposed fix: write `{0,-1,-2}` in all three places.

### 4. MINOR — Corollary 3's "arbitrarily high algebraic degree" is not proved by the argument given

Location: Corollary 3 statement ("In particular ... of arbitrarily high
algebraic degree") and Section 5.

What the proof establishes is exactly the displayed statement: every
threshold-feasible flow generates a field containing `α`. That does not imply
that any *individual* flow value has degree `≥ deg α` (e.g. `√2` and `√3`
generate a degree-4 field while each has degree 2). The phrase "optimal
solutions of arbitrarily high algebraic degree" reads as a statement about
individual values.

The stronger statement is nevertheless true, but needs the part of the
toolbox paper's Theorem 1 that the draft does not cite: `V(Ψ)` is a *linear
extension* of `V = {x : p(x) = 0, a ≤ x ≤ b} = {α}` (toolbox Definition 5).
For a one-point `V ⊆ R` this means there are rationals `a' ≠ 0, b'` and a
variable `x_j` of `Ψ` with `a' x_j + b' = α` in the unique solution; hence the
flow value `x_{s_{x_j} P_{x_j}} = x_j` has algebraic degree exactly `deg α` in
every threshold-feasible flow (there is exactly one, since `V(Ψ)` is a single
point and the flow is determined by the variables).

Proposed fix: either delete "of arbitrarily high algebraic degree", or add the
linear-extension argument above and cite toolbox Theorem 1 and Definition 5
in addition to Corollary 2. Also, the (⇒) list of flow values in Section 5
omits the slack flows (`B` minus a *sum* of several such values) and
`5/2 - x - y`; all still lie in `Q(α)`, so this is a wording gap only.

### 5. MINOR — Remark 2's claim about "formulations with flow lower bounds" needs qualification

Location: Section 6, item 2, last sentence.

Saturation of a forced source `s_v` is the constraint `x_{s_v P_v} +
x_{s_v P̄_v} = 5/2`; it cannot be expressed by *arc* lower bounds (each arc
individually can be anywhere in `[0, 5/2]`). It can be expressed by a node
throughput lower bound (`out(s_v) ≥ 5/2`, and likewise `X_Q ≥ B`, `in(t) ≥ 2`).
So the pure-feasibility statement holds for models with node lower bounds,
not for arbitrary "formulations with flow lower bounds".

Proposed fix: say "node throughput lower bounds".

### 6. MINOR — In-degree claim is weaker than what the construction gives

Location: Theorem 1 (bullet "every pool has in-degree at most three"),
Section 4.9.

Enumerating the pools (Finding 12): `P_v, P̄_v, R_v, R̄_v` have in-degree 2
(one quality-1 arc, one diluent), relay pools `p'`, `p_2`, `p_3`, `p_c` have
in-degree 1, and `p_+` has in-degree 2. No pool has in-degree 3. The
parenthetical in 4.9 already says this, so the "at most three" is
inconsistent with its own justification. In-degree 2 matches Haugland's
bounded-in-degree NP-hardness (his Section 5.2) and is a strictly stronger
statement for free.

Proposed fix: state "in-degree at most two".

### 7. MINOR — Text/code discrepancies (the code is a faithful *variant*, not the literal construction)

Location: Section 7 ("implements the reduction literally").

- Diluent sources and slack terminals: text capacity `B`; code capacity
  `BIG = 1000`. Harmless for feasibility (unforced nodes, larger caps), but
  it means the script does not test the claim "capacities lie in
  `{2, 5/2, 4, B}`".
- Inverse pools: text creates `R_v` and `R̄_v` for *every* variable
  (Section 4.4, reaffirmed in 4.7); code creates `R_v` only if `v` occurs as a
  summand and `R̄_v` only if `v` occurs as `y` in an inversion or as `z` in an
  addition. When neither exists, the code enforces the range by a plain
  emission from `P_v`/`P̄_v` whose relay source delivers into a fresh
  unforced pool `pv` (cap 2) and unforced vacuous terminal `tv` (cap 2). This
  variant is valid (Lemma 5 gives `1/a ≤ 2` from the emission terminal's
  capacity regardless of where the delivered flow goes), but it is not what
  the text describes.
- Dead code: the loop in `build()` under the comment "range enforcement: at
  least one emission ..." only executes `pass`; the actual range enforcement
  is the final loop. Cosmetic.
- `w` variables are bounded to `[0,1]` in the model; the text leaves them in
  `R`. Equivalent here (qualities in `{0,1}`; free `w` only multiply zero
  flow), but worth a comment.
- Quality flip, emission bounds `1/(2B)`, gadget bounds `2/(5B)`, capacities
  `2, 5/2, 4`, `ζ`, and the cost rule match the text exactly.
- The `M` count in the code (`need[x]['P'] += 1` per inversion) is the
  corrected count of Finding 1, not the text's.

Proposed fix: either align the code with the text (caps `B`, always create
`R_v, R̄_v`) or change Section 7 to say the script implements the reduction
"up to two harmless variants" and list them.

### 8. REMARK — Feasibility quantifier: "for some `w`" versus Haugland's "for any `w`"

Location: Section 1.

Haugland defines `x` feasible if the terminal inequality holds "for any
quality matrix `w` of `x`"; the draft says "for some quality vector `w`". The
two are equivalent because `w_p` is free only when `X_p = 0`, in which case
every `x_{pt} = 0`; the draft's own convention paragraph says this. Section 3
(membership) is correct under either reading. Suggest one clause noting the
equivalence, since the ∃R membership system existentially quantifies `w`.

### 9. REMARK — Counting of quality parameters

Location: Theorem 1, bullet 1.

Haugland (Section 2.2) states that a parameter with both bounds "has to be
counted twice" when the number of quality parameters is an issue. The
theorem's bullet 2 and Remark 3 already give the two-attribute upper-bound
form, so the statement is faithful; but bullet 1 ("one quality attribute")
should say "one attribute with lower and upper bounds (two in Haugland's
counting)" to avoid overclaiming against his Section 4 single-parameter
result, which uses upper bounds only. The open question flagged in Remark 3
is the right one.

### 10. REMARK — Items verified correct (no action)

- Model (Section 1) versus Haugland 2.1: arc set `A ⊆ (S×P) ∪ (P×T)`, node
  capacities `b ∈ Q_+`, costs `c ∈ Q^A`, quality matrix definition with
  arbitrary value at zero throughput, terminal inequality proportional to
  inflow, decision version with rational `ζ`, and lower bounds as admitted in
  his Section 2.2: all faithful. Profit `≥ ζ` is his cost `≤ -ζ`.
- Section 2: AAM Definition 5 and Theorem 7 quoted correctly. Replacing
  `x = 1` by `x·x = 1` is sound in `[1/2,2]` (`x > 0`). The resulting form is
  exactly toolbox Definition 19, so Corollary 3 applies the reduction to a
  `Ψ` that needs no further normalization.
- Section 3: the system is degree 2, polynomial size, and equivalent to
  feasibility (Finding 8).
- Lemma 4: profit equals the sum of forced group totals; each is bounded by
  the node capacity; equality iff all tight. Correct.
- Lemma 5: `w_Q = a/B`; `w_{p'} x_{p't} = 0` in both throughput cases;
  `a x_{Qt} = 1` gives `a > 0`, `x_{Qt} = 1/a ≤ 2`; relay pool single-in
  single-out; relay source saturated with two arcs. Converse values
  `2 - 1/a ∈ [0, 3/2]`. Correct.
- Quality flip: `t_2` forced at 2, `p_2`, `p_3` single-in single-out, `s_3`
  forced with two arcs; delivered value preserved; `t_2` vacuous so pool
  qualities `0` and `1` are immaterial. Correct.
- Inverse pools: `w_{R_v} = 1/(vB)`, emissions from `R_v` carry `v`; range
  `1/v ≤ 2`, `1/(5/2 - v) ≤ 2` with `5/2 - v > 0` gives `[1/2, 2]`; diluent
  `B - 1/v ≥ B - 2 ≥ 0`. Correct.
- Inversion gadget: `x_{p_c t} = 5/2 - y`, `x_{P_x t} = y`, mass
  `(2/(5B))(5/2) = 1/B`, `p_c` term vanishes, so `xy = 1`. Case `x = y`
  fine. Converse fine (`5/2 - y ≤ 5/2`).
- Addition gadget: `w_{p_+} = 0` (throughput `x + y ≥ 1 > 0`, only quality-0
  inflow), `x_{R̄_z t} = 5/2 - x - y` from saturation and `= 5/2 - z` from
  mass, so `x + y = z`. Converse: `x + y = z ≤ 2 ≤ 4`, `5/2 - z ∈ [1/2,2]`.
  Correct.
- Slack bookkeeping is correct once `M` is corrected (Finding 1):
  `B - 2M = 3 > 0` and slack `≤ B`.
- Corollary 2: correct.
- Remark 3 (negated attribute): `w'_p = 1 - w_p` at positive throughput uses
  `sum_s x_{sp} = X_p`; zero-throughput pools contribute nothing. Correct.
- Concrete example `x + x = y, x·y = 1` has unique solution `1/√2, √2`.

### 11. REMARK — Hidden-assumption checklist (all confirmed against the construction text)

- Saturated flow could route through an arc in an unintended way: no. Every
  node's arcs are listed in Finding 12; there are no arcs beyond those the
  gadgets create, and no node is shared between gadgets except the forced
  pools `P_v, P̄_v, R_v, R̄_v` (by design) and the variable source `s_v`.
- Multiple inflows to a relay pool: none; `p'`, `p_2`, `p_3`, `p_c` have one
  inflow each; `p_+` has exactly the two intended.
- Zero-throughput pools: `p'` (when `a = 1/2`) and `p_3` (when `v = 1/2`) can
  have zero throughput; both cases are handled (`x_{p't} = 0`; `t_2`
  vacuous). No forced pool can have zero throughput.
- Quality of `p_+` nonzero: impossible; only quality-0 inflows and positive
  throughput.
- Emission terminal receiving flow from elsewhere: no; exactly `(Q,t)` and
  `(p',t)`.
- `v` outside `[0, 5/2]`: impossible, `s_v` saturated at `5/2` with two
  nonnegative arcs; then `[1/2,2]` is forced by the two feeding emissions,
  which exist for every variable (Section 4.4).
- Order of deductions in (⇐): `w_{R̄_y}` requires `a = 5/2 - y > 0`, which
  Lemma 5 at `P̄_y` supplies as a conclusion (`a x = 1`). No circularity.
- The (⇒) assignment saturates every forced node: `s_v` (`v + 5/2 - v`),
  `P_v`-type pools (`B` by definition of the slack), emission terminals and
  relay sources (`2`), `t_2`, `s_3` (`2`), gadget terminals (`5/2`). Checked.

### 12. REMARK — Node/arc inventory implied by the construction

For the record (every item below is specified in the text):

| node | kind | in-arcs | out-arcs |
|---|---|---|---|
| `s_v` | forced source, q=1, cap 5/2 | – | `P_v`, `P̄_v` |
| `P_v`, `P̄_v`, `R_v`, `R̄_v` | forced pool, cap `B` | one quality-1 arc, one diluent | slack + emission/gadget terminals |
| diluent | unforced source, q=0, cap `B` | – | one pool |
| slack | unforced terminal, cap `B`, vacuous | one pool | – |
| `t` (emission) | forced terminal, cap 2, `ℓ=u=1/(2B)` | `Q`, `p'` | – |
| `p'` | unforced pool, cap 2 | `s'` | `t` |
| `s'` | forced source, q=0, cap 2 | – | `p'`, one delivery arc |
| `p_2` | unforced pool, cap 2 | `s'` | `t_2` |
| `t_2` | forced terminal, cap 2, vacuous | `p_2`, `p_3` | – |
| `p_3` | unforced pool, cap 2 | `s_3` | `t_2` |
| `s_3` | forced source, q=1, cap 2 | – | `p_3`, `R_v` or `R̄_v` |
| `p_c` | unforced pool, cap 5/2 | `s'` | `t_inv` |
| `t_inv` | forced terminal, cap 5/2, `ℓ=u=2/(5B)` | `p_c`, `P_x` | – |
| `p_+` | unforced pool, cap 4 | `s'_x`, `s'_y` | `t_add` |
| `t_add` | forced terminal, cap 5/2, `ℓ=u=2/(5B)` | `p_+`, `R̄_z` | – |

### 13. Script run

Command: `cd code/pooling_existential_reals && python build_and_check.py`
(Gurobi 13.0.3). Result: `ALL OK`, exit 0. All seven cases finished with
status 2 (OPTIMAL), so the unsat verdicts are certified by the dual bound and
not merely by the incumbent: gaps `ζ - bound` are `0.552` and `0.164`, both
above the `0.15` stated in Section 7. Satisfiable cases recover
`1/√2 ≈ 0.707107`, `(√5-1)/2 ≈ 0.618034`, and the boundary values `1/2`,
`1`, `2` to six digits. One robustness note: the pass/fail test in
`run_case` uses the incumbent only; if a run ever hit the 60 s time limit on
an unsat case the check would "pass" without certification. Suggest also
asserting `status == OPTIMAL` (or `bound < ζ - tol`).

## Verdict

**PASS WITH CORRECTIONS.** The reduction is sound and the script confirms it,
but the text of the proof is wrong in one place that changes yes/no answers:

1. (Finding 1, MAJOR) Redefine `M` to count the inversion arcs `(P_x, t)` (or
   simply: all arcs from a forced pool to non-slack terminals). The script
   already does this; the text does not, and a concrete instance shows the
   text's `B` is too small.
2. (Finding 2) Correct `M ≤ m + 2` to `M ≤ 2m + 1`, `B ≤ 4m + 5`.
3. (Finding 3) Costs are in `{0,-1,-2}`.
4. (Finding 4) Either drop "of arbitrarily high algebraic degree" or add the
   linear-extension argument.
5. (Finding 5) "node throughput lower bounds" in Remark 2.
6. (Finding 6) In-degree at most two.
7. (Finding 7) State that the script differs from the text in diluent/slack
   capacities and in creating `R_v, R̄_v` only when used, or align the code.

Findings 8–9 are optional wording improvements.
