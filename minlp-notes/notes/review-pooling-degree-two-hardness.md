# Referee review: one-quality pooling with degree-two pools is strongly NP-hard

Date: 2026-09-04. Reviewed file:
[results/pooling-one-quality-degree-two-hardness.md](../results/pooling-one-quality-degree-two-hardness.md).
Model checked against Boland, Kalinowski, Rigterink (2017), Section 1 and
Section 4 (P-formulation, Table 2, open problems 2 and 3). Source hardness
checked against the author PDF of Asahiro, Jansson, Miyano, Ono, Zenmyo
(2011), extracted with `pdftotext`.

## Verdict: PASS WITH CORRECTIONS

Theorems 1 and 2 are correct, and they answer open problems 2 and 3 of Boland
et al. as stated. Lemma 1 is correct in both directions. The source hardness
is cited accurately. The reduction is polynomial with all instance numbers in
`{-2,…,2}`, so strong NP-hardness follows with no gap. I could not construct a
counterexample; an independent exhaustive check (described at the end)
agrees with the claim on every instance tried, including the variants that
the remarks add.

The corrections concern the remarks and one sentence of the problem
statement: remark 5 is true but its stated justification is false (input
capacities do not give `t ≤ w_e`), the compactness sentence is false as
written, and two literature claims need qualification or a fixed citation.
None of these affects the theorems.

## Checks performed

### 1. Lemma 1 and the source hardness

Asahiro et al. define `S-MMO` on a simple, undirected graph with positive
integer weights, weighted outdegree = sum of weights of outgoing edges
(Section 1). Section 5 reduces At-most-3-SAT(2L) to `{1,k}-MMO`; Lemma 1
there states `OPT(G_φ) ≤ k` if `φ` is satisfiable and `OPT(G_φ) ≥ k+1`
otherwise; Theorem 6 states `{1,k}-MMO` is strongly NP-hard for every fixed
`k ≥ 2`. Footnote 3 replaces the special 2-cycle by a 3-cycle for `k=2`
precisely to keep `G_φ` simple. So "simple graph, weights in `{1,2}`,
threshold 2, outdegree" is exactly what the result file uses. Reversing all
arcs turns outdegree into indegree, and the uniform threshold `2` is the
special case `T ≡ 2` of the per-vertex capacities of CO. Correct.

Lemma 1 (subdivision), forward direction: `m_e` receives exactly
`w_e = T_{m_e}`, endpoints unchanged. Converse: both halves into `m_e` is
impossible since `2w_e > w_e`; one half into `m_e` forces the other half
into the far endpoint and the orientation is copied; neither half into `m_e`
gives both endpoints load `w_e` in `H'`, and orienting `e` into `u` charges
`u` the same `w_e` it already carries and charges `v` nothing. In every
case each original vertex's in-load in `H` is at most its in-load in `H'`.
Correct. All numbers stay in `{1,2}` (originals keep `T=2`, midpoints get
`T=w_e`). Subdividing also removes parallel edges, so the "simple" claim would
hold even if the source graph were a multigraph; loops are excluded by the
CO definition. No issue.

### 2. Theorems 1 and 2

Cost accounting: `x_a - 2y_u - y_w = x_a - y_u - t` using `y_u + y_w = t`
from (1). Correct.

`x_a ≥ y_u`: if `y_u > 0` then `t > 0`, so `p_{ℓ_e} = x_b/t ∈ [0,1]` by (6)
and `λ ∈ {0,1}`. Constraint (7) at `u` with `μ_u = 0` is a sum of terms
`p·y`; pools with positive throughput contribute `p ≥ 0`, pools with zero
throughput contribute `y = 0` by (1) regardless of their free `p`. A sum of
nonnegative terms bounded by `0` has every term zero, so `p_{ℓ_e} = 0`,
`x_b = 0`, `x_a = t ≥ y_u`. This is exactly why the aggregate form of (7)
cannot be exploited: `μ_u = 0` sits at the bottom of the quality range, so
no pool with `p` strictly between `0` and `1` can send anything to a strict
output, and lax outputs (`μ_w = 1`) impose no constraint at all. The free
`p` of an idle pool is harmless because (6) reads `0 = p·0` and the pool's
out-arcs carry zero flow in (7). Correct.

Lower bound `cost_e ≥ -t ≥ -w_e` uses `t ≤ C_{ℓ_e} = w_e`. Equality
analysis and orientation extraction: correct. Capacity identification: in
Theorem 1 the in-load of vertex `v` under the extracted orientation is the
sum of `w_e` over edges oriented into `v`, and each such edge contributes
`y_{ev} = w_e` to output `v`, so in-load equals inflow `≤ C_v = T_v`. In
Theorem 2 the same holds with outflow of input `v`. Correct. Converse
directions satisfy (1), (2), (6), (7) and every input/pool/output capacity;
I checked each constraint. Correct.

Theorem 2: the sentence "constraint (7) at `A_e` reads `p y_A ≤ 0`, so
`p = 0`" silently uses `p ≥ 0`, which follows from (6) with `t > 0`. Half a
sentence should be added (issue 6).

Threshold and attainment: for the decision problem no attainment argument is
needed. The proof shows every feasible point has cost `≥ K`, and a feasible
point of cost exactly `K` exists iff an orientation exists, which is a
complete answer to "is there a feasible point of cost `≤ K`". The sentence
"the feasible set is compact" is false as written because `p_ℓ` is free for
idle pools (issue 2); the minimum is still attained because any feasible
point can be relabelled with `p ∈ [0,1]` without changing flows.

### 3. Degree claims versus the open problems

Theorem 1: inputs out-degree 1, pools in/out 2, outputs in-degree
`deg_H(v)` (unbounded). Theorem 2: outputs in-degree 1, pools 2/2, inputs
out-degree `deg_H(v)`. Verified from the arc lists. Boland et al. phrase
problem 2 as "one quality and in-degrees at most two" and problem 3 as "one
quality and out-degrees at most two". Inputs have no incoming arcs and
outputs no outgoing arcs, so "all in-degrees at most two" is exactly "pools
and outputs" (their Table 2, row 13) and "all out-degrees at most two" is
exactly "inputs and pools" (row 12). Theorem 2 has all in-degrees `≤ 2` and
Theorem 1 has all out-degrees `≤ 2`. The match is exact. Remark 4 correctly
records that bounding all four degrees at once is not covered.

### 4. Corollaries and remarks

Remark 1 (PARTITION): with two vertices, parallel edges of weights `s_i`,
`T_u = T_w = B = Σ s_i / 2`, an orientation is feasible iff the edges
oriented into `u` sum to exactly `B`. Theorems 1 and 2 never use simplicity,
and the CO definition admits multigraphs, so this is valid. It is weak
hardness because the pooling numbers are the `s_i`. Two overclaims to fix
(issue 4): the statement "remains open" about strong hardness with `|J|=2`
and bounded input out-degree cannot be verified without Haugland (2016),
whose row 11 (`min{|I|,|J|}=2`, `|K|=1`, pool degrees `≤ 6`, strongly
NP-hard) is already close; and the pooling side of row 10 (`|I|=|J|=2`,
`|K|=1`, bin packing with two bins) very likely already has pools of degree
`(2,2)`, so the only new content of the corollary is the private-input
(resp. private-output) structure. Say so.

Remark 2: fine, but "is a linear program" is a stronger claim than row 14's
"P" and is attributed to a paper the project has not read (issue 7, minor).

Remark 3: the Dey–Gupte package in the project is a slide-style exposition
in which the fixed-pool-out-degree question is item 2 under "Open Problems"
(fulltext line 1875), not "Question 1". The numbering in the published
article was not checked (issue 5).

Remark 5 (dropping pool capacities): the conclusion is true but the reason
given is wrong (issue 1). With `C_{a_e} = C_{b_e} = w_e` and no pool
capacity, `t = x_a + x_b ≤ 2w_e`, not `w_e`, so the proof's line
`cost_e ≥ -t ≥ -w_e` fails. The bound survives by a case split:
if `y_u > 0` then `x_b = 0` (as before) and `t = x_a ≤ w_e`, so
`cost_e ≥ -t ≥ -w_e`; if `y_u = 0` then `cost_e = x_a - t = -x_b ≥ -w_e`.
Equality in the second case forces `x_b = w_e` but leaves `x_a ∈ [0,w_e]`
free with `y_w = w_e + x_a ≥ w_e`, so the orientation extraction still
works (inflow to `w` only increases) but cost-`K` points are no longer
unique or necessarily integral, which contradicts the first sentence of the
same remark for this variant. Theorem 2 without pool capacities is
symmetric: `t = y_A + y_B ≤ 2w_e`; if `y_A > 0` then `x_w = 0` and
`cost_e = -y_A ≥ -w_e` by `C_{A_e} = w_e`; if `y_A = 0` then `t = y_B ≤ w_e`
and `cost_e = -x_w ≥ -w_e`. Both variants were confirmed numerically.

### 5. Strong NP-hardness

The pooling instance has `2|E|` or `|V|` inputs, `|E|` pools, `4|E|` arcs,
costs in `{-2,-1,0,1}`, capacities and qualities in `{0,1,2}`, and threshold
`K = -Σ w_e` with `|K| ≤ 2|E|`. Every number is bounded by a polynomial in
the instance size, the reduction is polynomial, and the source decision
problem is NP-hard. This is the standard route to strong NP-hardness. No
gap. (The source problem's hardness is for its decision version via
Asahiro's Lemma 1 and the NP-hardness of At-most-3-SAT(2L), which is what
is needed.)

### 6. Counterexample search

Script: `/tmp/review_check.py` (written independently of
`verify_reduction.py`; not committed). Differences from the repository
script: pool quality `p` bounded in `[-5,5]` rather than `[λ_min, λ_max]`, to
exercise the free-`p` case; exhaustive generation of bipartite multigraphs
with `|U|,|W| ≤ 2`, up to three edges (parallel edges allowed), weights in
`{1,2}`, capacities in `{0,1,2,3}`, of which 250 were solved (127
yes-instances); each instance solved for both theorems with and without
pool capacities; the four PARTITION instances `s ∈ {(1,2,3), (3,3,2,2,2),
(1,1,3), (2,2,2,5)}` with and without pool capacities; and a sanity check
that a deliberately broken variant (`μ = 0.5` at strict outputs) is caught,
which it was on 40 of 60 instances. Gurobi `NonConvex=2`, `MIPGap=0`,
tolerances `1e-9`. Result: `min cost ≥ K` always, and `min cost = K` iff a
feasible orientation exists, on every instance and variant. No
counterexample.

## Issues

| # | Severity | Location | Issue |
| --- | --- | --- | --- |
| 1 | Moderate | Remark 5 | Justification "since `t ≤ w_e` is all that is used" is false: input (resp. output) capacities alone give `t ≤ 2w_e`. Conclusion true by a different argument (above); the integrality sentence of the same remark fails for the capacity-free variant. |
| 2 | Minor | Problem statement, "The feasible set is compact" | False: `p_ℓ` is free for idle pools, so the feasible set in `(x,y,p)` is unbounded. Attainment holds after restricting `p ∈ [0,1]` WLOG, and the decision reduction does not need attainment at all. |
| 3 | Minor | Verification section and `code/pooling_degree_two/verify_output.txt` | The committed output file contains only the last two trials and summary of one 40-trial run; the text claims seeds 0 (60 trials) and 1 (40 trials). Regenerate the full logs or state what is stored. |
| 4 | Minor | Remark 1 | "remains open" and the novelty of `|J|=2` with pool degrees `(2,2)` are claims about Haugland (2016), which the project could not read. Table 2 rows 9–11 already give `|J|=2`, one quality, strongly NP-hard (row 11 with pool degrees `≤ 6`), and row 10 probably already uses `(2,2)` pools. Qualify. |
| 5 | Minor | Remark 3 and Sources | "Dey and Gupte (2015, Question 1)": in the project's copy (slides) it is item 2 under "Open Problems". Verify the numbering in the journal article or cite by wording. |
| 6 | Minor | Theorem 2 proof | "`p y_A ≤ 0`, so `p = 0`" needs `p ≥ 0`, which follows from (6) with `t > 0`; add it. |
| 7 | Minor | Summary and Remark 2 | "removed by linear programming"/"is a linear program" is attributed to Haugland's Proposition 3 without the text. Row 14 of Boland et al. says only "P". Either give the two-line argument (in-degree-one pools have fixed quality; out-degree-one pools can be merged into their output's constraint) or soften to "polynomially solvable". |
| 8 | Trivial | Header | Date `2026-09-05` is one day ahead of the review date; check. |

## Recommended text changes

1. Replace, in the problem statement,
   "The feasible set is compact and the objective continuous, so the minimum
   is attained. Note that `p_ℓ` is a free variable when the pool carries no
   flow; this is harmless below."
   with
   "`p_ℓ` is a free variable when pool `ℓ` carries no flow, but such a pool
   has zero outflow by (1), so its `p_ℓ` enters no other constraint and can
   be set to any value in `[min λ, max λ]` without changing flows or cost.
   Restricting `p` to that box therefore loses nothing, makes the feasible
   set compact, and shows the minimum is attained. The decision reduction
   below does not use attainment: it shows every feasible point has cost at
   least `K` and exhibits a cost-`K` point exactly when the orientation
   exists."

2. Replace remark 5 with:
   "**No numerical subtlety.** The reduction is exact at the threshold `K`;
   in the constructions above every cost-`K` point is integral, and the
   argument uses only the sign structure of the data. The pool capacities
   can be dropped, leaving only `C_{a_e}=C_{b_e}=w_e` (Theorem 1) or
   `C_{A_e}=C_{B_e}=w_e` (Theorem 2), at the price of a different bound:
   the throughput can then reach `2w_e`, but in Theorem 1 `y_u>0` still
   forces `x_b=0` and hence `t=x_a≤w_e`, while `y_u=0` gives
   `cost_e=-x_b≥-w_e`; in Theorem 2 `y_A>0` forces `x_w=0` and
   `cost_e=-y_A≥-w_e`, while `y_A=0` gives `t=y_B≤w_e` and
   `cost_e=-x_w≥-w_e`. Equality still forces the orientation pattern, though
   cost-`K` points are then not unique (an edge oriented into `w` may carry
   any `x_a∈[0,w_e]` alongside `x_b=w_e`)."

3. In remark 1, replace
   "Whether `|J|=2` with input out-degree at most two, or `|I|=2` with
   output in-degree at most two, is strongly NP-hard remains open; the
   present construction needs many vertices on both sides."
   with
   "Row 9 of the Boland et al. table already gives strong NP-hardness for
   `|J|=2` with one quality, and row 11 adds pool degrees at most six; the
   degree structure of those reductions, and of the bin-packing reduction of
   row 10 (`|I|=|J|=2`), was not available to this project, so the only
   content of this corollary that we can claim as new is the private-input
   (resp. private-output) structure. We do not know whether `|J|=2` with
   input out-degree at most two, or `|I|=2` with output in-degree at most
   two, is strongly NP-hard; the present construction needs many vertices on
   both sides."

4. In the Theorem 2 proof, replace
   "constraint (7) at `A_e` reads `p_{ℓ_e} y_A ≤ 0`, so `p_{ℓ_e}=0`"
   with
   "constraint (7) at `A_e` reads `p_{ℓ_e} y_A ≤ 0`, and `p_{ℓ_e}=x_w/t≥0`
   by (6), so `p_{ℓ_e}=0`".

5. In remark 3 and the Sources entry, replace "Question 1" with the item's
   wording ("the complexity status for a fixed value of the out-degree of the
   pool nodes", listed under Open Problems) unless the numbering is confirmed
   in the Operations Research article.

6. In the summary and remark 2, replace "can be removed by linear
   programming (Haugland's Proposition 3, row 14 of the Boland et al.
   table)" with "make the problem polynomially solvable (row 14 of the
   Boland et al. table, attributed there to Haugland's Proposition 3; the
   full text was not checked)", or add the two-line LP argument.

7. In the verification section, either commit the full logs for seeds 0 and
   1 or change the sentence to describe what `verify_output.txt` contains.
   Optionally add: an exhaustive referee check over all bipartite
   multigraphs with `|U|,|W|≤2`, at most three edges, weights in `{1,2}`,
   capacities in `{0,…,3}` (250 instances), with pool capacities present and
   dropped, and with `p` free, found no discrepancy.

8. Change "Independent proof review: pending" to record this review.
