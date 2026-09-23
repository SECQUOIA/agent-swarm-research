# Referee report: Theorem 1′ (bounded data and degrees) in `results/pooling-existential-theory-of-reals.md`

Date: 2026-09-05. Scope: Section 6, item 5 only (the chain construction
replacing fan-out), read against Sections 4.2–4.8 and the script
`code/pooling_existential_reals/bounded_build_and_check.py`. Theorem 1 itself
is covered by `notes/review-pooling-existential-reals-1.md` and `-2.md` and
is taken as given here. The result file was not edited.

## Method

1. Re-derived the chain algebra (qualities, emitted values, diluent and
   slack margins) from Lemma 5 and the quality flip of Section 4.3.
2. Enumerated the in- and out-arcs of every node kind in the chain variant.
3. Read `build_bounded`, `Chain.take`, `Chain.advance`, the final
   range-enforcement loop, and `check_degrees_and_data`; ran the script
   (`~/miniconda3/envs/minlp-notes/bin/python bounded_build_and_check.py`,
   Gurobi 13, academic license; output recorded below).
4. Wrote an independent script (`/tmp/bounded_audit/structural.py`, not
   committed) that (a) asserts the structural claims on the instances built by
   `build_bounded` for 300 random ETR-INV systems (1–6 variables, 0–12
   equations) and (b) for seven satisfiable systems with rational solutions,
   including "no equations", "a variable used in no equation", and a variable
   with eight summand occurrences, propagates the intended flow from the
   variable values by the local rules of Sections 4.2–4.7 and checks every
   capacity, conservation, and quality constraint and `profit = ζ` exactly in
   rational arithmetic. All checks passed. A second random test (2000
   systems) measured chain lengths against occurrence counts.

## Verification of the chain

**Qualities along the chain.** `P_v` has quality-`1` inflow `v` from `s_v`
and quality `v/B`. Its link emission carries `1/v` (Lemma 5), the flip
delivers `1/v` at quality `1` into `R_v`, so `R_v` has quality `1/(vB)`.
The link emission from `R_v` carries `1/(1/v) = v`, flipped into
`P_v^{(2)}`, which therefore has quality `v/B` again. By induction the chain
alternates `v/B`, `1/(vB)`, `v/B`, …, and the complement chain alternates
`(5/2 − v)/B`, `1/((5/2 − v)B)`, … . The induction is sound because every
chain pool is fed only by the previous chain pool's link emission (gadget
arcs leave chain pools; they never enter them), so no circularity arises in
the (⇐) direction of Lemma 6.

**Lemma 5 hypotheses.** Every chain pool is forced with capacity `B`, has
exactly two in-arcs (its diluent, and one quality-`1` arc: from `s_v` for
`P_v`, `P̄_v`; from the flip source `s_3` otherwise), and one slack out-arc.
This is exactly the hypothesis of Lemma 5, so its proof applies verbatim.
The (⇐) direction also gives `a > 0` at each pool (`v > 0` at `P_v`,
`5/2 − v > 0` at `P̄_v`).

**Diluent and slack margins with `B = 7`.** The four quality-`1` inflow
values `v`, `1/v`, `5/2 − v`, `1/(5/2 − v)` all lie in `[1/2, 2]` when
`v ∈ [1/2, 2]`, so `B − a ≥ 5 ≥ 0` in the intended flow (diluent capacity
`7` respected). A chain pool has at most one link arc and at most one gadget
arc, each carrying at most `2` (`1/a ≤ 2`, `y ≤ 2`, `5/2 − z ≤ 2`), so the
slack arc carries `≥ 7 − 4 = 3 > 0` and at most `7`. Confirmed exactly by
the propagated flows (asserted: every non-slack arc from a forced pool
`≤ 2`, every slack arc `≥ 3`).

**Serving gadgets.** `Chain.take(kind)` loops `advance()` while the current
pool has the wrong kind or already has a gadget arc (`used ≥ 1`). Since the
kinds alternate (`P ↔ R`, `Pb ↔ Rb`) and a fresh pool has `used = 0`, the
loop terminates after at most two advances (wrong kind: 1; right kind but
used: 2). Each `advance` spends the current pool's single link emission and
moves to the new pool, so a pool never receives a second link arc, and
`used ≤ 1` ensures at most one gadget arc: at most two non-slack arcs per
forced pool, i.e. `M ≤ 2`. Inversion: `take(y,'Rb')` (emission of `5/2 − y`
at quality `0` into `p_c`) and `take(x,'P')` (arc `(P_x^{(k)}, t)`); addition:
`take(x,'R')`, `take(y,'R')` (emissions of `x`, `y` into `p_+`) and
`take(z,'Rb')` (arc `(R̄_z^{(k)}, t)`). Repeated variables (`x = y` in an
addition, `x = y` in an inversion) are handled: two `take` calls on the same
chain yield two distinct pools; inversion uses the two different chains of
`x`. The gadget analyses of 4.5 and 4.6 use only the qualities `x/B` and
`1/((5/2 − z)B)` and the emitted values `5/2 − y`, `x`, `y`, which the chain
pools reproduce. `P̄`-type pools are never used by a gadget (only `P`, `R`,
`R̄` kinds are taken), matching Theorem 1 where `P̄_v` has one emission.

**Range enforcement.** The (⇐) argument of 4.4 needs one emission from
`P_v` (gives `v > 0` and `1/v ≤ 2`, i.e. `v ≥ 1/2`) and one from `P̄_v`
(gives `5/2 − v > 0` and `1/(5/2 − v) ≤ 2`, i.e. `v ≤ 2`). In the code, a
chain's current kind is `P`/`Pb` only if it has never been advanced or has
been advanced an even number of times; in either case the final loop
advances it, and if the kind is `R`/`Rb` the chain has been advanced at
least once. In all cases `P_v` and `P̄_v` end up with a link emission. The
"unused variable" and "no equations" cases confirm this: every `P_v` and
`Pbar_v` has an emission terminal out-arc, and the exact flow check passes.
(The link emission from `R_v` would also give `v ≤ 2`, so a single chain
advanced twice suffices; the text's argument via `P̄_v` is correct as is.)

**Degrees and data.** Enumeration of node kinds in the chain variant:

| node | in | out |
|---|---|---|
| `s_v` (5/2, q=1, forced) | – | 2 |
| diluent (7, q=0) | – | 1 |
| relay source `s'`, flip source `s_3` (2, forced) | – | 2 |
| chain pool (7, forced) | 2 | ≤ 3 (slack, link, gadget) |
| relay pool `p'`, flip pools `p_2`, `p_3` (2) | 1 | 1 |
| `p_c` (5/2) | 1 | 1 |
| `p_+` (4) | 2 | 1 |
| emission terminal (2, `1/14`, forced), flip terminal (2, `[0,1]`, forced) | 2 | – |
| inversion/addition terminal (5/2, `2/35`, forced) | 2 | – |
| slack terminal (7, `[0,1]`) | 1 | – |

Hence in-degree `≤ 2`, out-degree `≤ 3` (attained only at chain pools with
both a link and a gadget arc), capacities `{2, 5/2, 4, 7}` (`4` only when an
addition is present, `5/2` always), bounds `{0, 1, 1/14, 2/35}`, qualities
`{0, 1}`, costs `{0, −1, −2}`: diluent arcs `0`; `(s_v,·)`, `(s',p')`,
`(s_3,p_3)`, `(s',p_2)`, `(s_3, chain pool)`, `(p',t)`, `(p_c,t)`, `(p_+,t)`,
`(Q, slack)` `−1`; `(Q, t)` with `t` forced `−2`. Nothing reaches `−3`. The
script's printout agrees on every case (`max_out 3`, `max_in 2`, the four
data sets). The random structural test asserts the same properties on 300
instances.

**Size.** Each equation triggers at most three `take` calls, each at most
two advances; the final loop adds at most one advance per chain. So the
number of advances is at most `6m + 2n`, and each advance creates 10 nodes
and 11 arcs (emission: 3 nodes; flip: 4; new pool with diluent and slack:
3). Exactly, `|nodes| = 7n + 10·(advances) + 5·#inv + 8·#add`, verified as
an identity on all random instances. A chain of `v` has length at most
`2·(occurrences of v in that chain's role) + 3`; the random test found the
maximum excess `length − 2·occ = 2`. Hence the instance has `O(n + m)`
nodes and arcs, with `ζ = O(n + m)`.

**Script output** (verbatim verdict lines):

```
case x*x=1: |S|=10 |P|=12 |T|=10 |A|=32 zeta=53                       best=53.000000 bound=53.000000 True/True
case x+x=y, x*y=1: |S|=39 |P|=49 |T|=39 |A|=128 zeta=200              best=200.000000 bound=200.000000 True/True  x=0.707107 y=1.414214
case x+y=z, x*y=1, z*z=1 (infeasible): zeta=223                       best=222.445503 bound=222.467414 False/False
case x+x=y, y+y=z (z=2): zeta=441/2                                   best=220.500000 bound=220.500000 True/True  x=0.5 y=1 z=2
case golden: zeta=253                                                 best=253.000000 bound=253.000000 True/True  x=0.618034 z=1.618034
case fan-out (u+u=w, w*w=1, u*y_i=1, i=1..3): zeta=419                best=419.000000 bound=419.000000 True/True  u=0.5 w=1 y_i=2
case fan-out infeasible: zeta=753/2                                   best=375.899999 bound=375.937324 False/False
data (every case): max_out 3, max_in 2, caps {2,5/2,(4),7}, bounds {0,2/35,1/14,1}, quals {0,1}, costs {-2,-1,0}
ALL OK
```

All Gurobi statuses were OPTIMAL (the script asserts this), so the two
"no" verdicts are certified with margins `0.53` and `0.56` below `ζ`.

## Findings

No BLOCKING or MAJOR findings. The chain construction is correct and the
code implements it as described.

1. **MINOR — "`M = 2` and `B = 7` for every instance" (Section 6, item 5).**
   `M` as defined in Section 4 is the maximum number of non-slack terminal
   arcs at a forced pool; in the chain variant it is at most `2` and can be
   `1` (an instance with no equations, or one whose gadgets never share a
   pool with a link arc). Since Section 4 sets `B := 2M + 3`, an instance
   with `M = 1` would formally get `B = 5`, contradicting the stated
   capacity set. Fix: write "each forced pool has at most two non-slack
   arcs, so `M ≤ 2`; fix `B := 7` for every instance (all arguments use only
   `B ≥ 2M + 3` and `B > 5/2`)". The code already hardcodes `B = 7`.

2. **MINOR — "all numerical data from a fixed finite set" (same item).**
   The threshold `ζ` is the sum of forced capacities and grows linearly
   with the instance; it is not from a fixed set. The preceding clause
   already says so, but the "that is" sentence overstates. Fix: "all data
   except the threshold from a fixed finite set, the threshold being a
   half-integer of magnitude `O(n + m)`", and optionally note that by
   Remark 2 (throughput lower bounds equal to the forced capacities, no
   objective) every number in the instance then lies in the finite set.

3. **MINOR — chain pools' diluent and slack are implicit.** The text says
   the flip feeds "the next forced pool" and later mentions "one diluent
   inflow", but never states that each chain pool `P_v^{(k)}`, `R_v^{(k)}`
   gets its own diluent source and slack terminal (the code does this in
   `forced_pool`). Fix: "…feeding the next forced pool, of capacity `B`, with
   its own diluent source and slack terminal".

4. **MINOR — "a fan-out instance in which one variable occurs in five
   equations".** In that instance (`u + u = w`, `w·w = 1`, `u·y_i = 1`,
   `i = 1,2,3`) the variable `u` has five occurrences in four of the five
   equations. Fix: "one variable has five occurrences (two of them in one
   addition)", or "occurs in four of its five equations".

5. **MINOR — the `O(n + m)` size claim is asserted without the count.**
   Fix: add one sentence, e.g. "each gadget occurrence advances its chains
   at most twice per required pool, so there are at most `6m + 2n`
   links, each of constant size".

6. **MINOR — code: the final range-enforcement loop.** The loop variable
   `want` is unused, and the condition `ch.kind in ('P','Pb')` advances a
   chain that is already at `P_v^{(k)}`, `k ≥ 2`, where `P_v` has already
   emitted; this adds a harmless extra link. Simplest fix consistent with
   the text: record whether a chain has ever been advanced and advance only
   if not (or keep the condition and drop `want`). Correctness is
   unaffected either way; the text's "advanced at least once" holds after
   the loop in all cases.

7. **MINOR — code: `check_degrees_and_data` reports but does not assert.**
   `run_case` prints the data set and degrees; the "ALL OK" verdict depends
   only on the Gurobi feasibility outcomes. Fix: assert
   `info['max_in'] ≤ 2`, `info['max_out'] ≤ 3`, and the four set
   inclusions in `run_case`, so the printed claim is machine-checked rather
   than eyeballed.

8. **REMARK — status sentence.** "The chain argument has not been separately
   audited" should be replaced by a pointer to this note once the
   corrections above are applied.

9. **REMARK — `P̄`-type pools are never used by gadgets.** Only kinds `P`,
   `R`, `R̄` are requested, so the complement chain's `P̄` pools serve solely
   as inverters between consecutive `R̄` pools. This is consistent with
   Theorem 1 (where `P̄_v` has exactly one emission) and needs no change;
   it is noted because it explains why a `P̄` pool always has out-degree
   `≤ 2`.

## Verdict on Theorem 1′

**PASS WITH CORRECTIONS** (all minor, wording and code hygiene). The chain
construction produces pools with the claimed alternating qualities, every
chain pool satisfies the hypothesis of Lemma 5 exactly, at most two
non-slack arcs leave any forced pool so `B = 7` gives diluent margin `≥ 5`
and slack margin `≥ 3`, every gadget occurrence can be served with at most
two advances per requested pool, the range `[1/2, 2]` is enforced for every
variable including unused ones, the data lie in `{2, 5/2, 4, 7}`,
`{0, 1, 1/14, 2/35}`, `{0, 1}`, `{0, −1, −2}` with in-degree `≤ 2` and
out-degree `≤ 3`, and the size is `O(n + m)`. The script's chain logic
matches the text, and its seven Gurobi verdicts and printed data sets
match the claims.
