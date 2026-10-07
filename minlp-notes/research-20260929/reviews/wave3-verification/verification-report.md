# Wave 3 verification: KAN family, powerflow0030p/0039p/0039r, ann_cumene_tanh

Date: 2026-09-30. Scope: the claims in
`research-20260929/open-instances-wave3/report.md` (Sections 1–4; `eg_*` was
not in scope). The verifier did not produce those results. Every check below
uses the verifier's own code in this directory. The authors' code was read to
learn file formats, and it was run as a black box only where a check says so.
Instances were read from `~/.cache/minlplib/minlplib/osil/` with the
decimal-preserving reader `reviews/open-instances-verification/osilx.py`. All
runs were single-threaded (`OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1`) and ran
under `timeout`. Only targeted checks were run: no project-wide verification,
no CI.

Two subagents did parts of the work under the same rules: powerflow (item 2)
and ann_cumene_tanh plus the MINLPLib and literature check (items 3–4). Their
code and logs are in `powerflow/` and `ann/`.

The powerflow extension `open-instances-wave3/powerflow/extension-report.md`
(it claims to close 0039p and 0039r) appeared while this review ran. It was
not reviewed.

## Verdicts at a glance

| item | verdict | key numbers (verifier) |
|---|---|---|
| 1a KAN structure | verified | own exact decoder; every row and variable classified for all 6 instances |
| 1b relaxation R and Δ | R verified; Δ logic sound but not recomputed | an independent bound that needs no Δ confirms the resulting dual bounds |
| 1c own rigorous lower bounds | verified for all six (table in 1c) | e.g. kan_r5_h1_n8 ≥ 0.069327860579524 (claimed 0.069327860510525), with the verifier's own UB 0.069327860619524 |
| 1d primal points | verified | all six `*.wave3.sol` points reproduce the claimed objective values at 60 digits |
| 1e exact feasibility | **the claim understates the issue**: the exactly feasible set is proved **empty** for all six | exact certificates in `logs/kan_infeas_cert.log` |
| 2 powerflow0030p | verified, with a 4e-14 rounding caveat | exact L = 576.89341229880046985… = `bound_exact` |
| 2 powerflow0039p / 0039r | root bounds verified; the B&B argument is sound; 0039r final bound confirmed; 0039p final bound not reproduced | accurate root SDP gives 41867.7797032 for both, which is already above the 0039r claim |
| 3 ann_cumene_tanh | relaxation verified; bound verified with caveats (full run not repeated) | per-box spot checks consistent; points verified |
| 4 MINLPLib status / novelty | verified (brief search) | listed values match; no prior certificates found |

## 1. KAN family

### 1a. Structure: verified

`kan_decode.py` parses each OSIL file and derives the network in exact
rational arithmetic without pattern-specific assumptions. It asserts that every
row is classified. For kan_r3_h1_n4 the 1478 rows split into 800 recursion,
spline-sum and edge rows; 576 big-M; 48 partition; 16 one-hot; 16 SiLU;
13 copy; 5 sum; 3 scaling; 1 objective.

- **Network.** Every instance is a KAN [d, n, 1] with d = 3 (r3) or 5 (r5),
  and each edge is P_k(z) + w_b·silu(z). The pieces come from 18 (r3) or 12 (r5)
  knot intervals per edge. The objective is A·y + B with A = 970.2191877107767
  and B = 981.2776620620748 (r3), or A = 1439.6298856740555 and
  B = 1975.955959593862 (r5). All match the report.
- **Binaries select knot intervals.** Each edge has its own one-hot binaries. With
  b = e_k the big-M rows give z ∈ I_k. Propagating the equality rows with
  b = e_k solves each row for a single unknown that enters linearly with a
  constant coefficient, so the value of every variable is forced. The result
  is an exact cubic P_k per piece plus w_b·silu. Inputs plus binaries therefore
  determine the whole point, as claimed.
- **Pre-activation bounds.** The hidden class box is the intersection of the
  bounds of h_j and of its layer-2 copy. It equals [t_3, t_15] of the layer-2
  grid and narrows the hidden variable's own box. Example: kan_r5_h1_n3, h_2 ∈
  [0.7032, 1.7346] against its own [0.6661, 1.7346]. That neuron is narrowed
  only at the lower end; others are narrowed more. The input boxes (including
  the scaled Rosenbrock variable) and the hidden boxes are identical to the
  authors' decoder in exact arithmetic (checked for r3_n4 and r5_n8).
- **Knot ambiguity.** Among admissible pieces, gaps reach 1.5e-15 (kan_r5_h1_n3)
  and overlaps 7e-16. The report says "at most about 6e-16", which is slightly
  low for gaps; this changes nothing. Value jumps |P_{k+1} − P_k| at knots are
  at most 4.2e-15.
- **Bounds that R drops**, per instance: the lower bounds 0 on every basis and
  spline variable (768 for r3_n4); the edge-output bounds; the output-sum
  bound; and the SiLU lower bound −0.278464596867598. That SiLU bound lies below
  the true minimum −0.27846454276…, so it is inactive.

### 1b. Relaxation R and perturbation bound Δ

- **R is a valid relaxation.** It drops rows and bounds only. The rows it keeps
  force obj = A(β0 + Σ_j ψ_j(h_j)) + B with h_j = β_j + Σ_i φ_ij(u_i), where each
  edge uses any piece k whose admissible interval contains its argument. The
  verifier's decoder derives the same R independently.
- **The Δ argument is correct in logic.**
  - |h_j − h̃_j| ≤ η_j = Σ_i |w_s| ε_ij.
  - |ψ_{j,k}(h_j) − ψ̃_j(h̃_j)| ≤ δ_j + Lip_j η_j, with Lip_j taken on
    [L_j − η_j, U_j + η_j].
  - The hidden bounds of R̃ are enlarged by η_j. `kan_bb.py` lines 189–207
    implement this.
- **What was not recomputed.** The verifier did not recompute ε, η, δ or Lip.
  Instead the verifier's branch and bound (1c) works directly with the model's
  pieces P_k. It takes the hull over every admissible piece, and an explicit
  |P_k − P_k0| penalty where arguments cross knots. So it needs no ideal spline
  and no Δ, and it confirms the claimed bounds independently.
- **Is the bound valid "for the OSIL model as written"?** Yes, but trivially
  (see 1e). The substantive statement is that it is valid for R.
- **Wording nit.** The report says R contains "the intended network problem".
  Strictly, R contains the network with the model's decimal pieces, which
  differs from the ideal-spline network by at most Δ (1.7e-11 to 1.4e-10 in
  the objective).

### 1c. Independent rigorous lower bounds: verified

`kan_bnb.py` is the verifier's own interval branch and bound over the inputs.
It is vectorized with numpy.

- **Rounding.** IEEE doubles are rounded outward by one ulp (nextafter) after
  every operation. exp is numpy's, widened by a relative 2^-50. numpy's exp was
  measured at 0.58 ulp maximum error on 2·10^5 points against mpmath
  (`kan_bnb.py --check-exp`), so the widening leaves a 7× margin. This accuracy
  is an empirical assumption, not a proof.
- **Bounds per box.** The maximum of three, each valid for every admissible
  choice of pieces:
  - LB1: the natural enclosure. It takes the hull over admissible pieces, uses
    Taylor ranges of the cubic pieces, and intersects them with mean-value forms.
  - LB2: a second-order form. ψ_j is expanded around ĥ_j = h_j(c) with
    reference pieces. Per neuron it takes the larger of two valid versions: an
    interval slope, or ψ_j'(ĥ_j) plus min(ψ_j'', 0)·ρ_j²/2, which costs
    nothing where ψ_j is convex. The linear part then splits into 1-D quadratic
    bounds per input. Where arguments cross knots, the bound adds explicit
    penalties |P_k − P_k0|, computed exactly from the knot-difference
    polynomials.
  - LB3: a third-order form: V(c) + g·s + ½sᵀH_m s − g_r·r − ½rᵀRad·r − penalties,
    where Rad bounds |H(ξ) − H_m| over the box. This bound is applied only when
    H_m is positive definite, which is proved per box by an exact rational
    LDLᵀ; ½gᵀH_m⁻¹g is then computed exactly.
- **Incumbent.** A multistart local search from 20 random points (not the
  authors' points), then evaluated rigorously at a point that is certified
  R-feasible.
- **Final bound.** min(UB − tol, min over open boxes), with
  tol = 4e-11·max(1, |UB|).
- **Soundness tests.** `kan_soundness.py` samples 90–150 boxes per instance on
  scales 1e-6 to 1. The samples include boxes that straddle knots and points
  exactly at knot endpoints, and LB3 is forced on. It evaluates R at 50 digits
  for every admissible combination of pieces. There were 0 violations on
  r3_n4, r3_n9, r5_n3, r5_n5 and r5_n8 (`logs/kan_soundness_v2.log`). The
  smallest margin was 1.2e-10.

Final code, `kan_bnb.py <name> 4e-11 1800 1024` (logs `logs/<name>.bnb_v2.log`
and `.json`):

| instance | verifier lower bound (valid for R) | verifier UB (rigorous, R-feasible point) | claimed dual bound | claim ≤ verifier LB? | boxes / time |
|---|---|---|---|---|---|
| kan_r3_h1_n4 | 0.0027812371878504 | 0.0027812372278504 | 0.0027812371525814 | yes | 26,353 / 9 s |
| kan_r3_h1_n5 | −0.011042679449684 | −0.011042679409684 | −0.011042679521782 | yes | 22,297 / 6 s |
| kan_r3_h1_n9 | 0.012963660028294 | 0.012963660068294 | 0.012963659963475 | yes | 42,635 / 14 s |
| kan_r5_h1_n3 | −262.86422589412710 | −262.86422588361250 | −262.86422590922 | yes | 1,648,095 / 266 s |
| kan_r5_h1_n5 | 0.27258325392338 | 0.27258325396338 | 0.27258325385485 | yes | 709,939 / 147 s |
| kan_r5_h1_n8 | 0.069327860579524 | 0.069327860619524 | 0.069327860510525 | yes | 615,347 / 219 s |

- **All six claimed dual bounds are confirmed as valid for R.** Each is lower
  than the verifier's independent bound.
- **The verifier's gap brackets the authors' primal values.** The UB − LB gap
  is 4e-11 (1.05e-8 absolute for r5_n3, which is 4e-11 relative). Each of
  the authors' 60-digit primal values lies inside [verifier LB, verifier UB].
  So the optimal value of R is certified to within about 1e-10 relative, as
  claimed.
- **Independent confirmation of the new optima.** Without the authors' points,
  the verifier's own multistart found:
  - 0.06932786062 on kan_r5_h1_n8 (listed 0.36062128);
  - 0.27258325396 on kan_r5_h1_n5 (listed 0.27265451).

  On kan_r5_h1_n3 and kan_r3_h1_n9 the multistart found only −229.89 and
  0.036; the branch and bound itself then found −262.8642258836 and
  0.0129636601.
- **Earlier revisions**, sound but slower (logs `*_v1*` and
  `kan_r5_h1_n8.bnb_secondorder_only.*`):
  - With LB1–2 only, kan_r5_h1_n8 stopped at 2000 s with 10.0M boxes and a
    lower bound of 0.0693247203. That alone proves the listed primal 0.3606 is
    far from optimal.
  - Without the convex variant of LB2, kan_r5_h1_n3 finished in 1508 s
    (9.2M boxes) with the same bound. kan_r5_h1_n5 reached only 0.2725832039
    by its 1700 s limit.
  - The r3 runs agree with the final code. r3_n4 and r3_n5 gave identical
    bounds; r3_n9 differs by 6e-12 because it found a different incumbent.

  `kan_bnb_v1.py` is the revision without the convex LB2 variant.

### 1d. Primal points: verified

`kan_primal.py` evaluates every OSIL row and bound at 60 digits
(`logs/kan_primal.log`).

| instance | objective of `*.wave3.sol` (60 digits) | max violation, partition rows | max violation, other rows | bound / integrality violation |
|---|---|---|---|---|
| kan_r3_h1_n4 | 0.0027812372214418141291 | 2.49e-15 | 3.9e-27 | 0 / 0 |
| kan_r3_h1_n5 | −0.011042679414487295306 | 1.79e-16 | 3.5e-28 | 0 / 0 |
| kan_r3_h1_n9 | 0.012963660053039328497 | 1.0e-15 | 1.3e-27 | 0 / 0 |
| kan_r5_h1_n3 | −262.86422588506524044 | 3.32e-16 | 6.5e-27 | 0 / 0 |
| kan_r5_h1_n5 | 0.27258325395662269731 | 2.0e-16 | 6.6e-27 | 0 / 0 |
| kan_r5_h1_n8 | 0.069327860606191085327 | 5.81e-16 | 6.3e-27 | 0 / 0 |

- **Agreement.** The objective values and partition-row violations match the
  report exactly. The decoder's partition residual polynomials reproduce the
  actual row values at each point to 1e-30. The reduced network value V(u)
  equals objvar to 1e-28. The hidden margins to [L_j, U_j] are at least 0.19,
  so no pre-activation bound is active at any of the optima.
- **MINLPLib's points** (p1/p2/p3) violate partition rows by only about 1e-15.
  Their larger violations, 2.3e-13 to 9.0e-11, are in other rows, for example
  the objective row e1114 of kan_r3_h1_n4 and row e195 of kan_r5_h1_n5. The
  report attributes the 1e-12 to 9e-11 range to partition rows; that
  attribution is inaccurate.

### 1e. Exact feasibility: every KAN OSIL model is infeasible in exact arithmetic

The report's caveat ("possibly empty") can be sharpened: the set is empty,
with a certificate. Consider the partition rows Σ_m B_{m,p}(z) = 1 of one
edge. Once the edge's interval k is fixed, each row is a polynomial identity
in z, and with decimal coefficients the residual is a nonzero polynomial of
magnitude about 1e-15. Two scripts show that for some edges no z in the box
satisfies all of these rows.

- `kan_infeas_cert.py` checks every admissible piece k of an edge. For each piece it gives either
  - one partition row whose residual has no real root in I_k ∩ box (exact Sturm
    count over QQ), or
  - two partition rows whose residuals have a nonzero resultant.
- The certificate uses a single edge, so it holds whatever pieces the other
  edges choose, including at overlap points.
- An independent gcd-and-root-isolation analysis (`kan_struct.py`) gives the
  same edge counts.

| instance | layer-1 edges with a complete infeasibility certificate |
|---|---|
| kan_r3_h1_n4 | 4 of 12 (all edges of the second input, x1076; e.g. piece 5 by resultant(e197, e198) ≠ 0, piece 14 by e198 root-free) |
| kan_r3_h1_n5 | 5 of 15 |
| kan_r3_h1_n9 | 9 of 27 |
| kan_r5_h1_n3 | 15 of 15 |
| kan_r5_h1_n5 | 25 of 25 |
| kan_r5_h1_n8 | 40 of 40 |

**Consequence.** In exact arithmetic each of the six OSIL models has an empty
feasible set, so its optimal value is +∞. Every number is then a valid dual
bound, and "closed" means nothing for the exact OSIL problem.

**Recommended wording.** Report the result as a statement about R:

- **For R.** min over R ∈ [L, U]. Here R is the OSIL model without the
  partition-of-unity rows and without the bounds on basis, spline, edge-output
  and output variables. L is the certified bound and U is the value at an
  R-feasible point. This gap is what was closed to about 1e-10.
- **For the OSIL model.** It is exactly infeasible, which is certified. Points
  feasible within 2.5e-15, violating only partition rows, reach U.

MINLPLib judges feasibility with tolerances, so U is a legitimate new primal
value there. L is not a rigorous bound for tolerance-feasible points, though:
at tolerance 1e-6, relaxed recursion rows could lower the objective by roughly
A·1e-6. Calling these instances "closed" is justified only in the R sense
above, and the R qualification should be stated explicitly.

**Not checked for KAN:**
- the authors' ε, η and Lip numbers;
- the authors' `kan_iv` exp construction and third-order form.

Both are superseded by the independent bounds for all six instances. The
verifier's own exp enclosure relies on numpy's measured accuracy (see 1c).

## 2. powerflow (subagent; code in `powerflow/`)

### powerflow0030p: verified

**Relaxation (`pfv.py`, `run_root.py`).** All 555 rows are accounted for.

- All 164 flow rows turn into exact quadratic identities in (e, f). This was
  checked symbolically with sympy and a generic trig expansion.
- The voltage rows become 0.95² ≤ e² + f² ≤ hi², which is valid because lo ≥ 0.
- The angle rows (164) and the reference row are dropped.
- The single-variable rows become boxes on 16 variables.

**Multipliers.** The 332 stored multipliers align row by row; this was
asserted. Every inequality part is ≥ 0 and sits on the correct side. No flow
multiplier needed adjusting.

**Certificate.**
- Exact rational LDLᵀ of A(w) gives 60 positive pivots (the smallest 9.9e-8).
- L = 576.89341229880046985…, equal to `bound_exact` exactly.
- **Caveat:** the printed decimal 576.8934122988005 is the nearest double and
  lies 4.3e-14 above the exact L. The strictly valid decimal is
  576.8934122988004.

**p1 point.** obj(p1) = 576.89341347037138687, with a max row violation of
2.1e-13. The gap is 1.17e-6 (2.0e-9 relative), and L ≤ Lagrangian(p1) ≤ obj(p1).

### powerflow0039p and powerflow0039r: partly verified

**Root bounds: verified.** Exact L equals `bound_exact`:

| instance | exact root bound | pivots | note |
|---|---|---|---|
| 0039p | 41867.77607197097637… | 78 positive | printed …098 is 4e-13 high |
| 0039r | 41867.68744320833597… | 78 positive | |

All 184 flow identities were checked for 0039p.

**B&B argument (`pf_bb2.py`): sound.**
- **Covering.** Children cover the parent with complementary half-planes or
  magnitude intervals.
- **Envelope cut.** For rank-one W, c·w_R + s·w_I = |u||W|cos(φ−φ_u)
  ≥ κ√(W_pp W_qq) ≥ κP. This needs κ ≤ |u|cos h′ and κ ≥ 0, and P ≤ √(ab) on
  the box, which holds because √(ab) is concave.
- **Test of the cuts.** An exact random test found 0 violations over 400 nodes
  and 49,891 rank-one points (smallest slack 3.9e-19), and it detects a 1e-6
  inflation of κ.
- **Minor.** κ is rounded down by a (1 − 1e-25) margin at 40 digits, which is
  not interval arithmetic but far exceeds the numerical error.

**0039r final bound 41867.77921: verified.** An accurately solved Shor SDP
(Clarabel, tolerance 1e-11), certified exactly, gives a root bound of
41867.7797032. That is already above the claim, so the reported 0039r "B&B
gain" only makes up for their inaccurate root solve.

**0039p final bound 41868.26524: not reproduced.** Multipliers for each node
were not stored. The logged value is the minimum over the open heap plus the
closed nodes, as it should be. The accurate root bound is 41867.7797031
(needed eps = 1e-9), so the true B&B gain on 0039p is about 0.486, not 0.489.

**p1 points.**

| instance | obj(p1) | max row violation |
|---|---|---|
| 0039p | 41869.051511320199159 | 1.2e-12 |
| 0039r | 41869.051511320800473 | 7.9e-12 |

**Not checked:**
- the authors' interval-Cholesky code (replaced by exact LDLᵀ);
- the angle-row tan margins in polar nodes;
- powerflow0030r;
- the GAMS local solves;
- the new extension report.

## 3. ann_cumene_tanh (subagent; code in `ann/`)

### Relaxation: verified

**Structure.** Forward propagation from x723–x727 fixes 779 variables through
529 linear and 250 tanh rows. The ten remaining variables appear only in e749,
e750, e782–e788 and e790. The three claimed identities hold on the parsed
coefficients.

**Substitution.** Row e790 contains exactly the products x746·x78k, x766·x792
and x766·x793. Each is replaced by the right-hand side of an equality row, so
no division is involved. That matters because x746 ∈ [−194, 262] and
x766 ∈ [−18.1, 30.9] can be zero.

**Validity.** Dropping e749/e750 is valid: their extra variables x754 and x756
are free and appear nowhere else. Dropping the solvability of the product rows
only enlarges R. R keeps exactly the OSIL bounds of the determined variables
(722 finite bounds) and x772 ≥ 0.999. So min over R ≤ the OSIL optimum.

### Bound −4024.4949777: verified with caveats

**Per-box checks.** The subagent built its own interval evaluator (mpmath
intervals; tanh enclosed via iv.exp and monotonicity) with three bounds:
natural, mean-value, and mean-value of the Lagrangian.

- On 13 named boxes and 1200 small boxes, the authors' per-box bound never
  exceeded the verifier's, and never exceeded the best feasible value in the box.
- No box was wrongly declared infeasible.
- The authors' tanh enclosure held at 24,013 test points.

**Lagrangian signs are correct.** Both multipliers are ≥ 0, and the constraints
x647 ≥ −1 and x772 ≥ 0.999 belong to R.

**Final value.** It is the minimum over fathomed boxes, open boxes and the
incumbent. A 160 s rerun of their script reproduced their iteration-50 line
exactly.

**Caveats.**
- The full 3600 s run was not repeated.
- The report's "39.7% of the volume closed" is the value at 3399 s; the log's
  last line shows 40.07%.

### Points: verified

| point | objective (50 digits) | max row violation |
|---|---|---|
| p1 | −3379.982394023530105 | 8.2e-12 |
| wave3 | −3379.9823940717715481 | 4.6e-27 |

Neither point violates any bound.

## 4. MINLPLib status and novelty (brief)

- **Listed values.** The MINLPLib pages of all ten target instances agree with
  `open-instances-scout/fetched.csv` and the report's table. For example:
  - kan_r5_h1_n8: 0.36062128 / −45.00462396 (GUROBI);
  - powerflow0030p: 576.8934135 / 572.8395847.

  All ten are listed as open, and ann_cumene_tanh has no dual bound.
- **Prior certificates.** None were found.
  - The KAN instances come from arXiv 2503.02807 (SCIP runs, no global
    certificates); no follow-up was found.
  - Müller et al. (arXiv 1912.00356) list only best-known values for
    powerflow0030p and 0039p.
  - Lavaei–Low report a zero duality gap for IEEE 30-bus. That is consistent
    with the tight 0030p SDP, although the instance data may differ.

## Corrections suggested for the wave-3 report

1. **KAN 2.4.** Replace "possibly empty" with "empty, certified". Report
   "closed" as a statement about R (see 1e).
2. **KAN 2.4.** MINLPLib's points violate the partition rows by about 1e-15;
   their 1e-12 to 9e-11 violations are in other rows.
3. **KAN 2.1.** The knot gaps reach 1.5e-15, not 6e-16.
4. **powerflow.** Print the certified decimals rounded down: 576.8934122988004
   for 0030p, and 41867.77607197097 for the 0039p root.
5. **powerflow0039r.** The final bound is below an accurately solved root SDP
   (41867.7797). The 0039p final value is not reproducible from the stored
   data.
6. **ann.** The closed volume is 40.07% at the end of the run.

## Commands run (targeted; this directory unless noted)

KAN (verifier):
- `python3 dump.py kan_r3_h1_n4` (output `logs/kan_r3_h1_n4.dump.txt`)
- `python3 kan_decode.py <name>` for r3_n4, r5_n3 and r5_n8
- `python3 kan_struct.py <name> v` for all six (log: `logs/kan_struct.log`)
- `python3 kan_infeas_detail.py kan_r3_h1_n4 x1076`
- `python3 kan_infeas_cert.py <name>` for all six (`logs/kan_infeas_cert.log`)
- `python3 kan_primal.py <name> <sol>` for the wave3 and MINLPLib points of all
  six (`logs/kan_primal.log`)
- `python3 kan_bnb.py --check-exp`
- `python3 kan_soundness.py <name> <nbox> <u>` for r3_n4, r3_n9, r5_n3, r5_n5
  and r5_n8 (`logs/kan_soundness_v2.log`)
- `python3 kan_bnb.py <name> 4e-11 1800 1024` for all six
  (`logs/<name>.bnb_v2.log/.json`), plus the earlier-revision runs in
  `logs/*_v1*` and `logs/kan_r5_h1_n8.bnb_secondorder_only.*`
- `python3 kan_local.py kan_r5_h1_n8 <u> …`, a diagnostic only. It certifies a
  local convexity box of half-width 1e-5 to 5e-5 and shows λ_min(H) ≈ 1: the
  optimum lies in an ill-conditioned valley.
- one inline comparison of input and hidden boxes against the authors'
  `kan_model.decode` (bytecode writing off)

Powerflow and ANN subagents: see their directories. In short:
- powerflow: `run_root.py powerflow{0030p,0039p,0039r}`,
  `sdp_node.py powerflow0039r root|kids`, `sdp_node.py powerflow0039p root`,
  `test_cut.py`;
- ann: `annv.py structure|points|boxes|boxes2`, `authors_boxes.py`, and a 160 s
  rerun of `ann_fast.py`.

## Files

- `kan_decode.py`, `kan_struct.py`, `kan_infeas_detail.py`,
  `kan_infeas_cert.py`, `kan_primal.py`, `kan_bnb.py` (final),
  `kan_bnb_v1.py` (earlier revision), `kan_soundness.py`, `kan_local.py`,
  `dump.py`
- `logs/`
- `powerflow/`
- `ann/`

Nothing under `open-instances-wave3/` was edited. The `__pycache__` folders
there date from 07:58. They coincide with the concurrent powerflow extension
work in the same directory and were left in place.
