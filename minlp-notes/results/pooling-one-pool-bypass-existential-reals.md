# One pool with bypass arcs and many attributes is already ∃R-complete

Date: 2026-09-05. Status: two independent proof audits passed with minor
corrections, all applied (see the status line at the end).

This sharpens the [general theorem](pooling-existential-theory-of-reals.md)
that the pooling problem is complete for the existential theory of the
reals. There, hardness used many pools and one quality attribute. Here the
network has a **single pool**, but source–terminal bypass arcs and an
unbounded number of quality attributes.

**Theorem 1.** The threshold decision version of the pooling problem with
bypass arcs (Section 1) is `∃R`-complete, and hardness holds under all of
the following restrictions:

- exactly one pool;
- every source quality lies in `{0,1}`; terminal quality bounds are lower
  and upper bounds (equivalently, only upper bounds after doubling the
  attribute set, as in Section 6, item 1, of the general theorem);
- every source has at most two outgoing arcs (one into the pool and at most
  one bypass); every terminal has in-degree at most two;
- every source capacity is `2` except one filler source, every terminal
  capacity is `2` except one slack terminal, and all flow lower bounds are
  zero; arc costs lie in `{0,-1,-2}`.

**Corollary 2.** Unless `NP = ∃R`, one-pool pooling with bypass arcs and an
unbounded number of quality attributes is not in `NP`; it is in
`∃R ⊆ PSPACE`.

This contrasts with two known tractable or `NP` cases of one-pool pooling:

- without bypass arcs, Haugland (2016, Theorem 2) solves one-pool instances
  with upper quality bounds by at most `2^{|T|}` compact linear programs,
  one per subset of terminals receiving pool flow (his other family uses
  `(|T|+1)^{|K|}` programs); lower bounds add linear rows to each program,
  so guessing that subset is an `NP` certificate. Together with the
  one-pool strong NP-hardness of Alfaki and Haugland (2013), the one-pool
  problem without bypasses is `NP`-complete;
- with a fixed number of attributes, with or without bypasses, the
  repository's [linear-fiber certificate lemma](fixed-parameter-linear-fibers-np-membership.md)
  gives `NP` membership; and without bypasses, with a fixed number of
  sources, Boland, Kalinowski, and Rigterink (2017) give a polynomial
  algorithm (their model excludes input–output arcs and uses upper bounds).

So bypass arcs together with an unbounded attribute count are exactly what
lifts the one-pool problem from `NP` to `∃R`-completeness.

## 1. Model

The model is Haugland's (2016, Section 2.1) with source–terminal arcs
added, which is the standard pooling problem of Alfaki and Haugland (2013),
and with the lower quality bounds that Haugland introduces in his
Section 4 (lower and upper bounds on the same attribute count as two
attributes in his convention). Sources `S`, one pool `p`, terminals `T`,
arcs `A ⊆ (S×{p}) ∪ ({p}×T) ∪ (S×T)`. Node capacities `b`, arc costs `c`, a
finite attribute set `K`, source qualities `q_s^k ∈ Q`, terminal bounds
`ℓ_t^k ≤ u_t^k`. A flow `x ≥ 0` satisfies

```
x_{sp} + sum_t x_{st} ≤ b_s        (s ∈ S)
X := sum_s x_{sp} = sum_t x_{pt} ≤ b_p
x_{pt} + sum_s x_{st} ≤ b_t        (t ∈ T),
```

where bypass arcs count toward both source and terminal capacities.
A quality vector `w ∈ R^K` satisfies `w^k X = sum_s q_s^k x_{sp}` for all
`k` (arbitrary when `X = 0`). The flow is feasible if for some such `w` and
all terminals `t` and attributes `k`,

```
ℓ_t^k I_t ≤ w^k x_{pt} + sum_s q_s^k x_{st} ≤ u_t^k I_t,   I_t := x_{pt} + sum_s x_{st}.
```

Profit is `-sum_a c_a x_a`; POOL-1 asks whether a feasible flow with profit
at least a rational `ζ` exists. Membership in `∃R` is exactly as in
Section 3 of the general theorem (a degree-two polynomial system).

## 2. The reduction

Start from an ETR-INV instance (Abrahamsen, Adamaszek, Miltzow 2018,
Definition 5), normalized as follows: replace `x = 1` by `x·x = 1`, and
replace each addition with a repeated summand `x + x = y` by
`x·u = 1`, `u·x' = 1`, `x + x' = y` with fresh variables `u, x'` (within
`[1/2,2]` these force `x' = x`). The result is an equivalent ETR-INV
instance whose equations are inversions `x·y = 1` (with `x = y` allowed)
and additions `x + y = z` with `x ≠ y`. Let its variables be `V`, and let
`m` be its number of equations.

The instance has one pool `p`, and the following nodes and arcs.

- **Variable sources.** For each `v ∈ V` a source `s_v` with capacity `2`,
  unforced, and the single arc `(s_v,p)`.
- **Auxiliary sources and pinned terminals.** For each auxiliary index `j`
  (created below) a forced source `a_j` of capacity `2` with the two arcs
  `(a_j,p)` and `(a_j,t_j)`, and a forced terminal `t_j` of capacity `2`
  with the two incoming arcs `(p,t_j)` and `(a_j,t_j)`.
- **Filler and slack.** A source `f` with capacity `B` and quality `0` in
  every attribute, unforced, with the single arc `(f,p)`; and an unforced
  terminal `t_0` of capacity `B` with vacuous bounds and the single arc
  `(p,t_0)`. Here `B := 4 n_s`, where `n_s` is the number of variable and
  auxiliary sources.
- **Pool.** `p` is forced with capacity `B`.
- **Attributes.** One attribute `A_s` for every variable or auxiliary source
  `s`, with `q_s^{A_s} = 1` and `q_{s'}^{A_s} = 0` for `s' ≠ s`; and one
  attribute `A_{x+y}` for every addition `x + y = z`, with quality `1` at
  `s_x` and at `s_y` and `0` elsewhere. All qualities are in `{0,1}`.
- **Pins.** A pin `(t_j, A, κ)` sets `ℓ_{t_j}^A = u_{t_j}^A = κ`. All
  unpinned bounds are vacuous, `ℓ = 0`, `u = 1`.

The auxiliaries and pins are created per equation:

Write `A_v := A_{s_v}` for the attribute of a variable source.

- Inversion `x·y = 1` (for `x = y` fix an arbitrary order of the two
  roles): two auxiliaries `j_1, j_2`; pins
  `(t_{j_1}, A_x, 1/(2B))`, `(t_{j_2}, A_{a_{j_1}}, 1/(2B))`,
  `(t_{j_2}, A_y, 1/(2B))`.
- Addition `x + y = z`: one auxiliary `j`; pins `(t_j, A_z, 1/B)` and
  `(t_j, A_{x+y}, 1/B)`. (Definition 5 allows `z ∈ {x,y}`; the gadget
  handles this case without change.)
- Range: for each variable `v` that is not `x` or `y` of any inversion, one
  auxiliary `j` with the pin `(t_j, A_v, 1/(2B))`.

Costs and threshold follow the forcing rule of the general theorem: every
arc has cost minus the number of forced groups containing it (arcs leaving
a forced source, arcs leaving the forced pool, arcs entering a forced
terminal), and `ζ` is the sum of the forced capacities, namely
`ζ = B + 4·(number of auxiliaries)`. Lemma 4 of the general theorem applies
verbatim: profit at least `ζ` holds iff every forced node is saturated.

## 3. Correctness

Throughout, write `X_s := x_{sp}` for the pool inflow from source `s`.

**Lemma 3 (saturated flows).** Let `x` be feasible with profit at least
`ζ`. Then:

1. `X = B`, so `w^A = sum_s q_s^A X_s / B` for every attribute `A`; in
   particular `w^{A_s} = X_s/B` and `w^{A_{x+y}} = (X_{s_x} + X_{s_y})/B`.
2. For each auxiliary `j`: `x_{a_j t_j} = 2 - X_{a_j}` and `x_{pt_j} = X_{a_j}`.
3. For each pin `(t_j, A, κ)` with `A ∈ {A_{s_v}, A_{a_i} (i ≠ j), A_{x+y}}`:
   `w^A X_{a_j} = 2κ`.

*Proof.* (1) The pool is saturated. (2) The source `a_j` is saturated with
exactly two arcs, so `x_{a_j t_j} = 2 - X_{a_j}`; the terminal `t_j` is
saturated with exactly two incoming arcs, so `x_{pt_j} = 2 - x_{a_j t_j} = X_{a_j}`.
(3) The pinned constraint at `t_j` reads `w^A x_{pt_j} + q_{a_j}^A x_{a_j t_j} = κ I_{t_j} = 2κ`.
For the listed attributes `q_{a_j}^A = 0`: the attribute `A_{s_v}` is
supported on `s_v`, `A_{a_i}` on `a_i ≠ a_j`, and `A_{x+y}` on variable
sources. Substituting (2) gives `w^A X_{a_j} = 2κ`. ∎

Set `X_v := X_{s_v}` for variables and `τ_j := X_{a_j}` for auxiliaries;
all lie in `[0,2]` by the source capacities. By Lemma 3(1),(3), a pin with
`κ = 1/(2B)` on `A_{s_v}` gives `X_v τ_j = 1`, a pin with `κ = 1/(2B)` on
`A_{a_i}` gives `τ_i τ_j = 1`, and a pin with `κ = 1/B` on `A_z` or
`A_{x+y}` gives `X_z τ_j = 2` or `(X_x + X_y) τ_j = 2`.

**Lemma 4.** In a saturated feasible flow, `(X_v)_{v∈V}` is a solution of the
normalized ETR-INV instance with every `X_v ∈ [1/2,2]`.

*Proof.* Inversion `x·y = 1` with auxiliaries `j_1, j_2`: the pins give
`X_x τ_{j_1} = 1`, `τ_{j_1} τ_{j_2} = 1`, `X_y τ_{j_2} = 1`. Hence all four
quantities are positive, `τ_{j_2} = 1/X_y`, `τ_{j_1} = X_y`, and
`X_x X_y = 1`. Also `τ_{j_2} ≤ 2` gives `X_y ≥ 1/2`, and `τ_{j_1} ≤ 2`
gives `X_y ≤ 2`; then `X_x = 1/X_y ∈ [1/2,2]`. When `x = y` the same three
equations give `X_x^2 = 1`, `X_x = 1`. Addition `x + y = z` with auxiliary
`j`: `X_z τ_j = 2 = (X_x + X_y) τ_j` with `τ_j > 0`, so `X_z = X_x + X_y`.
Range pins give `X_v τ_j = 1` with `τ_j ≤ 2`, so `X_v ≥ 1/2`; and
`X_v ≤ 2` always. Every variable is either an `x` or `y` of an inversion
(and then bounded through that inversion) or has a range pin, so all
`X_v ∈ [1/2,2]`. ∎

**Lemma 5.** If the normalized ETR-INV instance has a solution `(x_v)`, the
constructed instance has a feasible flow with profit `ζ`.

*Proof.* Set `X_v = x_v`; for an inversion `x·y = 1` set
`τ_{j_1} = x_y`, `τ_{j_2} = 1/x_y`; for an addition set `τ_j = 2/x_z`;
for a range pin set `τ_j = 1/x_v`. All of these lie in `[1/2,2]` because
`x_y, x_z, x_v ∈ [1/2,2]` and `2/x_z ∈ [1,4]` would exceed `2` only if
`x_z < 1`, which cannot happen since `x_z = x_x + x_y ≥ 1`. Set
`x_{a_j t_j} = 2 - τ_j ≥ 0`, `x_{pt_j} = τ_j`, filler inflow
`X_f = B - sum_v X_v - sum_j τ_j`, and slack outflow
`x_{pt_0} = B - sum_j τ_j`. Since there are `n_s` variable and auxiliary
sources with inflow at most `2` each, `sum_v X_v + sum_j τ_j ≤ 2 n_s = B/2`,
so `X_f ≥ B/2 ≥ 0` and `x_{pt_0} ≥ B/2 ≥ 0`, within the capacities `B`.
Every forced node is saturated: sources `a_j` at `2`, terminals `t_j` at
`2`, and the pool at `B` (inflow `B` by the choice of `X_f`, outflow
`sum_j τ_j + x_{pt_0} = B`). The pool quality is `w^A = sum_s q_s^A X_s/B`.
Pinned constraints hold by the computations preceding Lemma 4, read
backwards: for instance at `t_{j_1}` the mass of `A_x` is
`(x_x/B)·x_y = 1/B = 2·(1/(2B))`. Unpinned constraints are vacuous: masses
are nonnegative, and at `t_j` the mass of any attribute `A` is at most
`w^A x_{pt_j} + x_{a_j t_j} ≤ x_{pt_j} + x_{a_j t_j} = I_{t_j}` because
`w^A ≤ (sum of at most two inflows of size at most 2)/B ≤ 4/B ≤ 1` and
`q ≤ 1`; at the slack terminal only the pool arc enters and `w^A ≤ 1`. The
profit equals `ζ` by the forcing lemma. ∎

Lemmas 4 and 5, the normalization, and `∃R`-completeness of ETR-INV prove
Theorem 1; the size is `O(n + m)` nodes, arcs, and attributes, and all
numbers are `2`, `B = 4n_s`, `1/(2B)`, `1/B`, `0`, `1`. ∎

## 4. Remarks

1. The single pool has in-degree `n_s + 1` and out-degree equal to the
   number of pinned terminals plus one; this is unavoidable with one pool.
2. The number of attributes is `n_s + (number of additions)`; with a fixed
   number of attributes the problem is in `NP` by the linear-fiber lemma, so
   the attribute count cannot be bounded in Theorem 1 unless `NP = ∃R`.
3. Corollary 3 of the general theorem (algebraic degree) transfers: the
   correspondence between saturated flows and ETR-INV solutions is again a
   bijection given by rational functions, with `X_v = x_v` directly.
4. The auxiliary terminals use both a lower and an upper bound on the pinned
   attribute; doubling the attribute set converts these to upper bounds
   only, as in Section 6, item 1, of the general theorem. The argument is
   unchanged by bypass arcs: with `q'_s = 1 - q_s` the complementary mass
   at a terminal is `I_t` minus the original mass, so an upper bound
   `1 - ℓ` on it is the original lower bound `ℓ`.

## 5. Verification record

`code/pooling_existential_reals/one_pool_build_and_check.py` implements
this construction (including the repeated-summand normalization; equations
`x = 1` must be supplied as `x·x = 1`) and solves the resulting one-pool
instances with Gurobi 13 as nonconvex QCQPs. Instead of arc costs it
maximizes the sum of forced-group totals, which equals the profit of
Section 2 by the forcing lemma. Eight
ETR-INV systems were checked: five satisfiable ones (`x·x = 1`;
`x + x = y, x·y = 1` with `x = 1/√2`; `x + x = y, y·y = 1` with `x = 1/2`;
`x + x = y, y + y = z` with `z = 2`; `x + y = z, x·z = 1, y·y = 1` with the
golden ratio) reached the threshold with variable values matching the
algebraic solution to six digits, and three unsatisfiable systems stayed
strictly below it. This is a sanity check of the gadgets, not part of the
proof.

## Sources

- M. Abrahamsen, A. Adamaszek, T. Miltzow, *The Art Gallery Problem is
  ∃R-complete*, STOC 2018; J. ACM 69(1) 2022, Definition 5 and Theorem 7
  (local: `literature/papers/abrahamsen2022-the-art-gallery-problem-is`).
- D. Haugland, *The computational complexity of the pooling problem*,
  J. Global Optim. 64 (2016), Theorem 2
  (local: `literature/papers/haugland2016-the-computational-complexity-of-the`).
- M. Alfaki, D. Haugland, *Strong formulations for the pooling problem*,
  J. Global Optim. 56 (2013).
- N. Boland, T. Kalinowski, F. Rigterink, *A polynomially solvable case of
  the pooling problem*, J. Global Optim. 67 (2017).
- The general theorem and its sources:
  `results/pooling-existential-theory-of-reals.md`.

## Status

Draft by the root agent, 2026-09-05. Numerical gadget checks passed.
Independent proof audits: `notes/review-pooling-one-pool-existential-reals-A.md`
and `notes/review-pooling-one-pool-existential-reals-B.md`, both PASS WITH
CORRECTIONS (citation precision for Haugland's lower bounds and Theorem 2,
Boland et al.'s model scope, explicit capacity constraints with bypasses,
notation `A_v`); all applied.
