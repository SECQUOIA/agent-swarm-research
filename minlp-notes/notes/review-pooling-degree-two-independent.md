# Independent verification: one-quality pooling with degree-two pools

Date: 2026-09-05. Reviewer: independent agent (second review). Subject:
[results/pooling-one-quality-degree-two-hardness.md](../results/pooling-one-quality-degree-two-hardness.md),
Theorems 1 and 2. The result file was edited by its author while this review
was in progress (a first referee's corrections were applied); the comparison
below is against the version whose section headers were at lines 32, 66, 108,
170, 205, 255, 275.

## Verdict

**PASS.** Both theorems are correct, and the proofs in the result file are
complete. My own proofs, written before reading the author's Theorem 1 proof,
coincide with the author's in every step. The Asahiro et al. hardness result
is transported correctly (checked against the author PDF of the JOCO 2011
paper). The bipartite subdivision lemma is correct in both directions. A
brute-force checker (Gurobi global solve, an independent exact disjunctive-LP
solve, and orientation enumeration) found no discrepancy. I list a few
presentation issues and one possible strengthening; none affects the claims.

Process note: I read the model, the problem statement, the source-problem
section, and the two construction bullet lists, then wrote my proofs. The
Theorem 2 proof in the result file directly follows its construction bullets
without a separating heading, so I saw it before writing my own Theorem 2
proof; my Theorem 1 proof was written blind and is the more independent one.
Theorem 2 is the mirror image of Theorem 1, so this leak is minor.

## Model used

P-formulation of Boland, Kalinowski, Rigterink (2017), pp. 2-3 of the PDF,
with one quality: (1) pool flow conservation; (2)-(4) capacities at inputs,
pools, outputs; (5) arc capacities (not used); (6) pool blending
`sum_{a in A^in_l} lambda_a x_a = p_l sum_{a in A^in_l} x_a`; (7) output
blending `sum_{a in A^in_j} p_a y_a <= mu_j sum_{a in A^in_j} y_a`; objective
`min sum c_a x_a + sum c_a y_a` with costs of either sign. Open problem 2 asks
about one quality with `|A^in_l|, |A^in_j| <= 2`; open problem 3 about one
quality with `|A^out_i|, |A^out_l| <= 2` (Section 4, p. 8; in-/out-degree
classes as in Table 2 rows 12-13).

## My proof of Theorem 1 (inputs out-degree 1, pools (2,2))

Notation per edge `e={u,w}`, `u` strict (`mu_u=0`), `w` lax (`mu_w=1`):
`x_a, x_b >= 0` intakes from the clean (`lambda=0`, cost 1) and dirty
(`lambda=1`, cost 0) inputs, `t = x_a + x_b <= w_e`, outflows `y_u` (cost -2)
and `y_w` (cost -1) with `y_u + y_w = t` by (1). Then
`cost_e = x_a - 2y_u - y_w = x_a - y_u - t`.

Lower bound. I claim `x_a >= y_u` at every feasible point. If `y_u = 0` this
is trivial. If `y_u > 0`, then `t > 0`, so (6) gives `p_e = x_b/t in [0,1]`.
At the strict output `u`, (7) reads `sum_{e' ~ u} p_{e'} y_{e'u} <= 0`. Each
term is nonnegative: pools with positive throughput have `p in [0,1]`, and
pools with zero throughput have zero outflow by (1), so their (free) `p`
multiplies zero. Hence every term vanishes, in particular `p_e y_u = 0`, so
`p_e = 0`, so `x_b = 0`, so `x_a = t >= y_u`. Therefore
`cost_e >= -t >= -w_e`, and the total cost is at least `K = -sum_e w_e`.

Equality analysis. Cost `K` forces `t = w_e` and `x_a = y_u` for every `e`.
If `y_u > 0`: `x_b = 0`, so `x_a = y_u = t = w_e`, `y_w = 0`. If `y_u = 0`:
`x_a = 0`, so `x_b = w_e = y_w`. So each pool sends all `w_e` units to
exactly one endpoint. Orient `e` into that endpoint. The in-load of `v` is
the total inflow of output `v`, at most `C_v = T_v` by (4). This is a
feasible CO orientation.

Converse. Given a feasible orientation, route `a_e -> l_e -> u` at value
`w_e` if `e` is oriented into `u` (pool quality 0, cost `w_e - 2w_e = -w_e`),
else `b_e -> l_e -> w` at value `w_e` (quality 1, cost `-w_e`). Input and
pool capacities `w_e` hold; output capacities hold because inflow at `v`
equals in-load `<= T_v`; (6) holds by construction; (7) at `u` has all
incoming qualities 0; (7) at `w` has `mu_w = 1 >= p`. Cost is exactly `K`.

Hence `min cost <= K` iff `min cost = K` iff CO feasible. All numbers are in
`{-2,...,2}` except `K`, which is bounded by `2|E|`, so this is a
pseudo-polynomial (indeed polynomial-magnitude) reduction and the restricted
pooling decision problem is strongly NP-hard.

## My proof of Theorem 2 (outputs in-degree 1, pools (2,2))

Per edge: intakes `x_u` (from strict input `u`, `lambda=0`, cost 1), `x_w`
(from lax input `w`, `lambda=1`, cost 0), `t = x_u + x_w <= w_e`; outflows
`y_A` to strict output `A_e` (`mu=0`, cost -2), `y_B` to lax output `B_e`
(`mu=1`, cost -1). `cost_e = x_u - y_A - t`. If `y_A > 0` then `t > 0`,
`p = x_w/t >= 0`, and (7) at `A_e` (in-degree one) is `p y_A <= 0`, so
`p = 0`, `x_w = 0`, `x_u = t >= y_A`. Otherwise `x_u >= 0 = y_A`. So
`cost_e >= -w_e`; equality forces `t = w_e`, `x_u = y_A`, hence either
`(x_u, x_w, y_A, y_B) = (w_e, 0, w_e, 0)` (orient into `u`) or
`(0, w_e, 0, w_e)` (orient into `w`). The in-load of `v` is the outflow of
input `v`, at most `T_v` by (2). Converse as in Theorem 1 with paths
`u -> l_e -> A_e` or `w -> l_e -> B_e`. Same threshold, same conclusion.

## Checks on the specific concerns

1. **Pools with zero throughput.** `p_l` is unconstrained by (6) when
   `t = 0`, but (1) then gives zero outflow, so `p_l` multiplies zero in every
   (7). The proofs use this explicitly. Restricting `p` to `[0,1]` is without
   loss, as the result file now states; the decision argument does not need
   attainment anyway.
2. **Aggregate output blending / compensation.** At a strict output
   `mu = 0`, (7) is a sum of nonnegative terms bounded by zero, so it
   decomposes into per-arc conditions `p_e y_{e,u} = 0`; no clean pool can
   compensate a dirty one because no pool has quality below 0. At lax outputs
   `mu = 1 = max lambda`, (7) is automatic. This is exactly why the
   construction uses the extreme values `mu in {0,1}` with `lambda in {0,1}`;
   with an intermediate `mu` the reduction would fail. Correctly handled.
3. **Exact attainment of the threshold.** Every feasible point has cost
   `>= K`; the orientation-induced flows cost exactly `K`. So yes-instances
   have optimum exactly `K`. For no-instances the checker measured the
   smallest optimum minus `K` (reported below); it is bounded away from zero,
   so the reduction is not sensitive to solver tolerance either.
4. **Subdivision lemma.** Both directions hold. Forward: orient
   `u -> m_e -> v`; `m_e` receives exactly `T_{m_e} = w_e`. Backward: at most
   one half-edge enters `m_e`; if one does, the other continues to the far
   endpoint and the original edge is oriented there; if none does, both
   endpoints receive `w_e` in `H'`, so orienting `e` either way charges one of
   them at most what it already carried. In-loads in `H` are bounded by
   in-loads in `H'`. Brute-force confirmed on all multigraphs with up to 3
   vertices and 3 edges (see below). Note the lemma needs `w_e >= 1` (so
   `2w_e > T_{m_e}`); the CO definition requires this.
5. **Transport of Asahiro et al. (JOCO 22 (2011) 78-96).** Verified in the
   author PDF (`www.df.lth.se/~jj/Publications/mmoutdegr10_JOCO_2011.pdf`):
   MMO input is a simple undirected graph with positive integer weights, and
   the objective is the maximum weighted outdegree. Section 5 reduces
   At-most-3-SAT(2L) to `{1,k}`-MMO; Lemma 1 states (i) satisfiable implies
   `OPT(G_phi) <= k`, (ii) unsatisfiable implies `OPT(G_phi) >= k+1`. So the
   decision question "orientation with weighted outdegree `<= k` at every
   vertex" is NP-complete on simple graphs with weights in `{1,k}`; for
   `k = 2` footnote 3 replaces the 2-cycle special gadget by a 3-cycle to keep
   the graph simple. Theorem 6 states strong NP-hardness of `{1,k}`-MMO for
   fixed `k >= 2`. Reversing all arcs turns weighted outdegree into weighted
   in-load, so CO with `T = 2` and `w in {1,2}` is NP-complete. The result
   file's description matches the paper. (Asahiro et al. take the
   NP-hardness of At-most-3-SAT(2L) from Garey-Johnson [LO1]; this is
   standard and not re-verified here.)
6. **Degree claims.** Bipartiteness plus looplessness guarantee `u != w`, so
   each pool has two distinct out-arcs; each edge gets its own pool, so
   parallel edges in `H` do not create parallel arcs. Output in-degree in
   Theorem 1 (input out-degree in Theorem 2) equals `deg_H(v)`, which is
   unbounded in the Asahiro gadget (the special-gadget vertices collect one
   edge per short clause).
7. **Strong NP-hardness bookkeeping.** All instance numbers are in
   `{-2,...,2}` and `K = -sum w_e` has magnitude at most `2|E|`, so the
   numbers are polynomially bounded; NP-hardness of this restricted decision
   problem is strong NP-hardness. The theorem statements' data ranges (costs
   `{-2,-1,0,1}`, capacities `{1,2}`, qualities and bounds `{0,1}`) match the
   constructions given `T in {1,2}` after subdivision.

## Discrepancies and remarks

None of these affects correctness.

- **Constraint numbering.** The result file's "(2)" bundles the paper's
  (2), (3), (4); the proofs cite "(2)" for output capacities (paper's (4)) and
  input capacities (paper's (2)). Internally consistent; a reader with the
  paper open may stumble. Cosmetic.
- **Corollary 1 (two outputs / two inputs).** Correct: a 2-vertex multigraph
  with parallel edges of weights `s_i`, `T_u = T_w = B = sum s_i / 2` is
  PARTITION. The result file rightly labels this weak NP-hardness only.
- **Corollary 2 (tightness).** The LP argument for pools with in-degree one
  or out-degree one (all pools) is right: in-degree one fixes `p_l = lambda`;
  out-degree one lets `p_l y_{l j} = sum lambda_a x_a` be substituted into
  (7), which becomes linear. This reproduces Boland et al. row 14.
- **Remark 5 (dropping pool capacities).** Re-derived and correct for both
  theorems; the lower bound then uses the input capacities (Theorem 1) or
  output capacities (Theorem 2) instead of the pool capacity. In Theorem 2
  the non-uniqueness at cost `K` is `y_B in [0,w_e]` alongside `y_A = w_e`,
  `x_u = t`; the file only spells out the Theorem 1 case. Cosmetic.
- **Possible strengthening (not a discrepancy).** The unbounded degree in
  Theorems 1-2 comes only from Asahiro's special gadget. If that gadget is
  replaced by enough vertex-disjoint 3-cycles of weight-2 edges, each cycle
  vertex receiving at most one clause edge, Lemma 1 of Asahiro et al. goes
  through unchanged for `k = 2` (with weighted outdegree `<= 2`, every
  3-cycle vertex already has outdegree exactly 2, so every clause-cycle edge
  points into the cycle; a clause vertex of degree 3 then needs an in-edge
  from a literal vertex, which must be true). The resulting graph has maximum
  degree 3, and subdivision keeps original-vertex degrees. Then Theorem 1
  holds with outputs of in-degree at most 3, and Theorem 2 with inputs of
  out-degree at most 3. I checked this only by hand; if the author wants to
  record it, it deserves its own brute-force check. It would sharpen Remark 4:
  the only open degree pattern is all four bounds simultaneously `<= 2`.
- **Result file drift.** The file changed during this review (line numbers
  and a new Verification section). The verification section cites this note
  before it existed; that is now consistent.

## Checker

Script: `/workspace/minlp-notes/code/pooling_degree_two/independent_check.py`
(written from scratch; `verify_reduction.py` was not consulted). Log:
`/workspace/minlp-notes/code/pooling_degree_two/independent_check_output.txt`.

Method. Enumerate every bipartite CO instance with `|U|, |W| <= 2`, edge
multisets of size 1-3 (size 1-2 when `|U| = |W| = 2`), weights in `{1,2}`,
capacities in `{0,1,2,3}`. For each instance: (a) decide CO by enumerating all
orientations; (b) build the Theorem 1 and Theorem 2 pooling instances exactly
from the construction bullets; (c) solve each with Gurobi 13 `NonConvex=2`,
`MIPGap=0`, `p` free in `[-10,10]`, tight feasibility tolerances; (d) solve
each again with an independent exact method: for every pool branch on
"no flow to `mu=0` outputs" or "no intake with `lambda>0`" and solve the
resulting LP with HiGHS (via `scipy.optimize.linprog`), taking the best of
the `2^|L|` branches; (e) assert `|Gurobi - LP| <= 1e-5`, `opt >= K - 1e-6`,
and `opt <= K + 1e-6` iff CO feasible. Separately, brute-force the
subdivision lemma on all loopless multigraphs with 2-3 vertices, 1-3 edges,
weights `{1,2}`, capacities `{0,...,3}`.

Results (run 2026-09-05, exit code 0):

- 18,656 bipartite CO instances (11,359 feasible, 7,297 infeasible), each
  tested under both constructions: 0 failures. Gurobi and the disjunctive-LP
  solver agreed on every instance, the optimum was never below `K`, and it
  equalled `K` exactly when an orientation existed.
- Smallest `opt - K` over infeasible instances: `1.0` (to solver precision).
  So on no-instances the optimum misses the threshold by at least one unit
  in this range, consistent with integrality of the branch LPs; the
  reduction is robust to numerical tolerance.
- Subdivision lemma: 7,264 general (non-bipartite, multi-edge) CO instances,
  0 failures.
- An earlier run with capacities up to 4 and three edges on `|U|=|W|=2` was
  stopped for time after 11,000 instances, also with 0 failures.
