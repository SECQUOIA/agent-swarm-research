# Wave 3: KAN family, powerflow0030p/0039p/0039r, ann_cumene_tanh and eg_*

Date: 2026-09-30. Status: computational results with the proofs given below;
independently verified with corrections
([verification](../reviews/wave3-verification/verification-report.md));
corrections applied by the root in Section 9. All runs were
single-threaded (`OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=RAYON_NUM_THREADS=1`)
and time-limited.

*Provenance note (root).* The agent that produced these results could not
write this file because its tool environment blocked report writes; the
root saved the agent's report text verbatim on 2026-09-30.

A **dual bound** here is a number L with L ≤ f(x) for every exactly
feasible x of the OSIL model. Listed values come from
`open-instances-scout/fetched.csv`. OSIL files are read with the
decimal-preserving `reviews/open-instances-verification/osilx.py`; objective
and row constants are read, and every certificate asserts them. Points are
evaluated at 50–60 digits with `open-instances-wave2/small/ev.py`; `tanh` was
added to its function table for the ANN.

## Summary

- **KAN (6/6: optimum of the relaxation certified; the OSIL models are
  exactly infeasible).** The verifier proved, with exact Sturm-count and
  resultant certificates, that none of the six KAN models has an exactly
  feasible point (the partition-of-unity rows are inconsistent in exact
  decimals). The claim below is therefore about the relaxation R (the
  intended network problem): its optimum is certified to about 1e-10 and
  matched by points violating only the partition rows (by at most 2.5e-15).
  The bound is not a rigorous bound for tolerance-feasible points in general.
  Each instance is a 3- or 5-input network whose edges
  are SiLU plus a cubic B-spline; the binaries only pick the knot interval.
  Once the inputs and interval binaries are fixed, every other variable is
  determined. The exact C² network was bounded over the inputs with a
  rigorous branch and bound, plus an explicit error term Δ ≤ 1.4e-10
  covering decimal rounding in the model. Final gaps are 7e-11 to 1.1e-10
  (9e-11 relative for kan_r5_h1_n3); the largest run took 925 s. The listed
  primal values of three instances are not optimal:
  - kan_r5_h1_n3: −262.8642259 (listed −262.3058993)
  - kan_r5_h1_n5: 0.2725832540 (listed 0.2726545)
  - kan_r5_h1_n8: 0.0693278606 (listed 0.3606213)
- **powerflow.** A Lagrangian/SDP dual with an exact rational evaluation and
  a PSD proof by interval Cholesky.
  - 0030p: 576.8934122988 against 576.8934134704, a gap of 2e-9 relative
    (listed dual 572.84).
  - 0039p: 41868.26524 (listed dual 41818.28); 0039r: 41867.77921 (listed
    41804.88). Remaining gaps 0.79 and 1.27 (1.9e-5 and 3.0e-5 relative):
    the SDP rank defect sits at leaf bus 30, and the branch and bound
    stalled. *Superseded:* the extension
    ([`powerflow/extension-report.md`](powerflow/extension-report.md))
    closes 0039p and 0039r (gaps 6.3e-10 and 6.7e-10 relative to p1's
    value); verified in
    [`../reviews/powerflow0039-review.md`](../reviews/powerflow0039-review.md).
- **ann_cumene_tanh.** First finite dual bound, −4024.49, against a primal
  of −3379.98239407 (gap 19%). The instance has no listed dual.
- **eg_\*.** No improvement: bounds after 600 s and 1800 s are 2.43 on
  eg_int_s (SCIP's is 6.326) and −0.056 on eg_disc2_s (SHOT's is 0). The
  Gaussian-sum enclosures are too loose; eg_disc_s was assessed but not run.
  *Superseded (root, 2026-10-01):* the round-4 retry
  ([`eg/retry.md`](eg/retry.md)) closes all three to a relative 1e-9
  against exactly feasible points; verified in
  [`../reviews/eg-retry-review.md`](../reviews/eg-retry-review.md). The
  table below and Section 6 describe the wave-3 attempt.

## 1. Results

| instance | listed primal | best listed dual | rigorous dual | primal (max violation) | gap | mechanism |
|---|---|---|---|---|---|---|
| kan_r3_h1_n4 | 0.00278124 | 0.0003908 (GUROBI) | **0.0027812371525814** | 0.0027812372214418 (2.5e-15) | 6.9e-11 | reduced-space B&B |
| kan_r3_h1_n5 | −0.01104268 | −0.01302849 (GUROBI) | **−0.011042679521782** | −0.011042679414487 (1.8e-16) | 1.1e-10 | same |
| kan_r3_h1_n9 | 0.01296366 | 0.0081425 (GUROBI) | **0.012963659963475** | 0.012963660053039 (1.0e-15) | 9.0e-11 | same |
| kan_r5_h1_n3 | −262.3058993 | −789.740197 (GUROBI) | **−262.86422590922** | **−262.86422588507** (3.3e-16) | 2.4e-8 (9e-11 rel.) | same |
| kan_r5_h1_n5 | 0.27265451 | 0.26787523 (GUROBI) | **0.27258325385485** | **0.27258325395662** (2.0e-16) | 1.0e-10 | same |
| kan_r5_h1_n8 | 0.36062128 | −45.00462396 (GUROBI) | **0.069327860510525** | **0.069327860606191** (5.8e-16) | 9.6e-11 | same |
| powerflow0030p | 576.8934135 | 572.8395847 (GUROBI) | **576.8934122988004** (corrected from ...005, 4e-14 too high) | p1: 576.89341347037 (2.1e-13) | 1.2e-6 (2.0e-9 rel.) | Lagrangian/SDP; the SDP relaxation is tight |
| powerflow0039p | 41869.05151 | 41818.27916 (GUROBI) | **41868.26524** | p1: 41869.0515113202 (1.2e-12) | 0.786 (1.9e-5 rel.) | SDP, then spatial B&B with envelope cuts; not closed |
| powerflow0039r | 41869.05151 | 41804.88153 (GUROBI) | **41867.77921** | p1: 41869.0515113208 (7.9e-12) | 1.272 (3.0e-5 rel.) | same; not closed |
| ann_cumene_tanh | −3379.982394 | none | **−4024.4949777** | −3379.9823940717715 (4.6e-27) | 644.5 (19%) | reduced-space B&B with a Lagrangian bound; weak |
| eg_int_s | 6.45310316 | 6.32629896 (SCIP) | 2.4266 (600 s) | 6.4531031593 (strictly feasible) | worse than listed | failed |
| eg_disc2_s | 5.64210058 | 0 (SHOT) | −0.0559 (1800 s) | 5.6421005800 | worse than listed | failed |

- The KAN primal points are the agent's own 60-digit points; the violation
  column is for the 30-digit rounding written to `sol/<name>.wave3.sol`.
- For KAN, all violation remaining after the 60-digit construction is in the
  partition-of-unity rows (Section 2.4); the other rows hold to about 1e-61.
- For powerflow the listed primal points are MINLPLib p1, evaluated at 50
  digits.
- powerflow0030r (not a target; already closed by ANTIGONE) was also
  certified: 576.8934126255.

## 2. KAN family

### 2.1 Exact structure (`kan/kan_model.py`)

The decoder classifies every row by pattern and asserts that every row and
every variable is used.

- **Network.** Each instance is a KAN [d, n, 1]: d = 3 inputs (r3) or 5
  inputs (r5); n = 4, 5, 9 or 3, 5, 8 hidden neurons. Every edge is
  φ(z) = w_s·S(z) + w_b·silu(z), with S = Σ_m c_m B_m a cubic B-spline; r3
  edges have 18 knot intervals, r5 edges 12.
- **Objective.** obj = A·y + B with y = β0 + Σ_j ψ_j(h_j) and
  h_j = β_j + Σ_i φ_ij(u_i); r3: A = 970.2192, B = 981.2777; r5:
  A = 1439.6299, B = 1975.9560.
- **How the binaries enter.** Each edge has its own one-hot binaries b_k,
  one per knot interval. Big-M rows force z ∈ [lo_k, hi_k] when b_k = 1:
  `c_k b_k − z ≤ M1` and `d_k b_k + z ≤ M2`; the first interval's lower row
  and the last interval's upper row carry no binary.
- **Spline encoding.** Bilinear rows implement Cox–de Boor: order-1 bases
  are B = b_j(α + βz) + b_{j+1}(γ + δz); orders 2 and 3 use products B·z. A
  spline-sum row, the SiLU row `s = z/(1+exp(−z))`, and an edge row
  e = w_s S + w_b s follow. Partition rows Σ_m B_{m,p} = 1 are present for
  p = 1, 2, 3.
- **Linear rows.** Exact copy rows give each edge its own argument variable.
  Scaling rows, e.g. x777 = 1.1796·x776 + 0.0039 with x777 ∈ [−2.048, 2.048],
  encode the Rosenbrock input domain. Neuron-sum rows, the output row and
  the objective row complete the model.
- **Pre-activation bounds are active constraints.** The layer-2 argument
  copies of h_j carry the output grid range as bounds, e.g.
  h_2 ∈ [0.703, 1.735] for kan_r5_h1_n3, much narrower than the hidden
  variable's own bounds.
- **Inputs plus interval binaries determine the point.** `kan_check.full_point`
  propagates rows generically (an equality with one unknown that appears
  linearly determines it; when an edge argument becomes known, its binary is
  set). This determines all variables for every instance.
- **Knot ambiguity.** The big-M intervals of neighbouring knots overlap or
  leave gaps of at most about 6e-16, so near a knot the binary choice is
  ambiguous; the bounds below cover every admissible choice.

### 2.2 The relaxation, and the ideal network as a proxy

R drops the partition rows, the B ≥ 0 bounds, and all intermediate-variable
bounds except the input class (the intersection of the bounds of u_i, its
copies and its scaled copy) and the hidden class (h_j ∈ [L_j, U_j] from h_j
and its layer-2 copy). Dropping constraints gives a relaxation, so
min over R ≤ min over the exactly feasible set.

In R, obj = A(β0 + Σ_j [w_s S_j,k(h_j) + w_b σ(h_j)]) + B, where h_j uses the
model's piece polynomials S_k (the exact rational polynomials obtained by
propagating the recursion rows with b = e_k). Define:

- S̃ = the exact C² cubic B-spline on the decoded knots
  (t_0 = −M1, t_k = lo_{k+1}, t_K = M2), with the model's coefficients c_m;
  bases are matched to model variables by support;
- ε_e = max over admissible k and z ∈ [lo_k, hi_k] ∩ box of
  |S_k(z) − S̃(z)|, computed exactly with Taylor-shift bounds in Fractions;
- η_j = Σ_i |w_s,ij| ε_ij, δ_j = |w_s,j| ε_j (layer 2), and
  Lip_j ≥ max |ψ̃_j'| on [L_j − η_j, U_j + η_j] (4000-cell interval
  subdivision).

Then for every point of R, |h_j − h̃_j| ≤ η_j and obj ≥ f̃(u) − Δ with
Δ = |A| Σ_j (δ_j + Lip_j η_j), and h̃_j ∈ [L_j − η_j, U_j + η_j]. Δ ranges from
1.65e-11 to 1.38e-10. **The certified dual bound is min f̃ over R̃ minus Δ.**

### 2.3 Branch and bound over the inputs (`kan/kan_bb.py`, `bbcore.py`, `kan/kan_iv.py`)

**Interval arithmetic.** `ia.NI` (one-ulp outward rounding). exp is built
from + − × ÷ only: a table of exp(j·ln2/64) computed with mpmath, a degree-8
Taylor polynomial, and a remainder bound; no libm result is trusted. SiLU
ranges use monotonicity and a certified bracket of its minimum
(−0.278464542761074). Piece polynomials use centred Taylor ranges.

**Lower bounds per box** (maximum of four valid bounds):
1. the natural enclosure, with h intersected with its box;
2. the mean-value form;
3. an affine-split second-order form:
   ψ_j(h) ≥ ψ_j(h_c) + ψ_j'(h_c)s + M_j s²/2, with M_j s²/2 minorized on its
   range by a tangent (if M_j > 0) or a secant, and
   s_j = Σ_i(φ_ij(u_i) − φ_ij(c_i)); the bound separates into 1-D
   quadratics per input, minimized exactly (unit test against brute force:
   no violations);
4. a third-order form: the exact Hessian H_c at the centre plus the Hessian
   variation R over the box, f ≥ f(c) + g·d + dᵀH_c d/2 − rᵀRr/2. Positive
   definiteness of H_c is proved by Gershgorin on VᵀH_cV (a congruence with
   float eigenvectors preserves inertia); the convex QP is bounded by
   q(y) + ∇q(y)·(d − y), evaluated in intervals.

**Why the third-order form was needed.** kan_r5_h1_n3 stalled with forms
1–3, which fathomed about 35% of boxes of radius ρ/(4√5) at distance ρ from
the optimum; with form 4 they fathom 100%. A soundness test over 1,200 boxes
found 0 violations.

**Other details.** A monotonicity test on fully feasible boxes; candidate
points are box centres whose h lies strictly in its box; depth-first search;
a box is discarded when lb ≥ UB − 1e-10·max(1, |UB|).

### 2.4 Checks and caveats

- **Primal points.** `run_kan.py` rebuilds the full OSIL point from u by
  generic propagation at 60 digits, rounds to 30 digits, and re-evaluates
  every row and bound with ev.py: 0 bound violations, and h_j inside the true
  box in all six cases.
- **Random enclosure test.** `kan_check.py random` compares the OSIL objective
  at 40 random inputs per instance with the B&B enclosures widened by Δ. All
  held; the largest |OSIL − f̃| was 1.2e-11, below Δ.
- **Exact feasibility is degenerate.** On each knot interval the partition
  rows are polynomial identities only up to decimal rounding (for edge x776
  of kan_r5_h1_n3 the level-2 sum is 1 − 6.2e-17·z). Exactly feasible inputs
  therefore form a finite set; the verifier proved it is **empty** for all six
instances (exact Sturm-count and resultant certificates). The dual bounds are for R,
  which contains every exactly feasible point and the intended network
  problem. The primal points violate only these rows, by at most 2.5e-15;
  MINLPLib's points violate other rows by up to 9e-11 (corrected: not the
  partition rows). *Root note:* "closed"
  for the KAN instances therefore means a valid bound for the model as
  written, matched to within 1e-10 by points that are feasible up to
  2.5e-15; the exactly feasible set may be empty.
- **Solver bounds.** BARON, LINDO and XPRESS list −10.80477537 on
  kan_r5_h1_n5, close to the trivial bound
  A(β0 + Σ_j min_{[L_j,U_j]} ψ_j) + B = −10.812 that treats the hidden
  neurons as independent within their boxes.
- **Literature.** Karia, Lastrucci and Schweidtmann (arXiv 2503.02807)
  report SCIP runs, e.g. a Rosenbrock-5D KAN at 0.27 with dual 0.19 at the
  7200 s limit. Their architectures differ from these instances; no global
  certificates for them were found.

## 3. powerflow0030p, 0039p, 0039r (`powerflow/`)

### 3.1 Structure and relaxation R (`pf_model.py`)

- **Model.** AC OPF. All OSIL variables are free; bounds are written as
  rows. There are 164 or 184 flow definitions, nodal balances, line limits
  P² + Q² ≤ s², voltage-magnitude rows, ±0.26 rad angle-difference rows
  (polar models only) and a quadratic generation cost.
- **Mapping.** A polar-feasible point maps to e = v cos θ, f = v sin θ. Flow
  rows become exact quadratic identities in (e, f). The bus mapping v↔θ is
  recovered from the flow terms and asserted.
- **Replaced rows.** Voltage rows lo ≤ v ≤ hi become lo² ≤ e² + f² ≤ hi². An
  angle row a ≤ θ_p − θ_q ≤ b becomes w_I ≤ t_b·w_R and w_I ≥ t_a·w_R, with
  rational t_b ≥ tan b and t_a ≤ tan a. The reference-angle row is dropped.
  Rectangular models are taken row by row; the f_ref = 0 row is dropped.

Every change is a valid consequence or a relaxation.

### 3.2 Certificate (`pf_sdp.py`, `pf_cert.py`)

For any multipliers w (free on equalities, a difference of nonnegative parts
on inequalities),

obj ≥ L = const(w) + Σ_y (σ_y y² + κ_y y) + xᵀA(w)x.

- The y terms are minimized in closed form over their boxes; flows with
  σ_y > 0 contribute −κ²/(4σ). If σ_y = 0, the flow row's multiplier is
  adjusted exactly so that κ_y = 0.
- A(w) is formed exactly in rationals. Interval Cholesky of A + εI proves
  xᵀAx ≥ −ε Σ vmax²; ε = 0 succeeded in every case.
- Multipliers come from the dual SDP solved with cvxpy and Clarabel
  (chordal decomposition off: it hangs on the 39-bus case). Inaccurate solves
  only weaken the bound; they never make it invalid.
- Sanity check (`pf_check.py`): at MINLPLib p1, bound ≤ L(p1) ≤ obj(p1) in all
  three cases.

### 3.3 Results

- **0030p.** Rigorous bound 576.8934122988 with the angle rows dropped (zero
  multipliers); the SDP relaxation is tight to 1.2e-6 absolute.
- **0039p and 0039r.** The plain SDP gives 41867.776 and 41867.687 (the
  latter from an inaccurate solve). The complex SDP matrix has eigenvalues
  42.05, 5.1e-3 and 3e-7; the defect is almost entirely on bus index 29
  (0-based), a leaf generator bus reached only through line 1–29, where
  W₂₉,₂₉ sits at 1.06² but |W₁,₂₉| is too small.
- **Spatial branch and bound (`pf_bb2.py`).** Branching on the angle of W_pq
  on lines (children cover the parent exactly, sharing one rational split
  direction) and on voltage magnitudes; an envelope cut at each node,
  c·w_R + s·w_I ≥ κ·P(W_pp, W_qq), with κ ≤ |u| cos h′ (mpmath, rounded down)
  and P an affine function below √(ab) at the four corners of the node's
  magnitude box (valid because √(ab) is concave). 0039p rises from 41867.776
  to **41868.26524** after 31 nodes (1272 s); 0039r from 41867.689 to
  **41867.77921** after 61 nodes. Both stalled. On 0039p the lowest node's
  SDP solution is rank-one to 1e-8 on lines, but the extracted point
  violates the balance rows by about 1e-4. A better branching rule or
  QC-type cuts on edge 1–29 with v₂₉ splits would be the next step.
- **Local solves.** GAMS CONOPT and IPOPT on 0039p from p1, from the default
  start, and from the SDP-extracted point all return 41869.05151.
- **Failed attempt.** `pf_bb.py` (angles only, no cuts): +0.0045 after 13
  nodes.

## 4. ann_cumene_tanh (`ann/`)

*Follow-up (root, 2026-09-30):* a later extension raised the dual bound
from −4024.4949777 to −3386.5402291369187 (gap 0.194%), independently
re-certified; see [`ann/extension.md`](ann/extension.md). This section
describes the wave-3 bound.

- **Structure.** Five inputs x723–x727 with boxes. Forward propagation
  determines 784 of 794 variables (stage 1: 200 tanh neurons, 33 outputs;
  stage 2: 50 tanh neurons, 8 outputs). The ten remaining variables (x754,
  x756, x787–x793, objvar) appear only in bilinear rows e749, e750 and
  e782–e790; every feasible point satisfies x746·x78k = RHS(e78k),
  x766·x792 = x760·x763 − x765·x772, and x766·x793 = x766 − x766·x792 (e788
  multiplied by x766).
- **Relaxation.** Substituting these identities gives obj = f(u) on a
  relaxation R that drops the solvability of the product rows and
  e749/e750; R keeps 70 training-domain bounds in [−1, 1], x772 ≥ 0.999, and
  all other finite bounds. At the inputs of p1, forward propagation
  reproduces p1 to within 2e-12.
- **Branch and bound (`ann_fast.py`).** Level-wise midpoint-radius sparse
  products with a γ_n error bound; natural enclosure, mean-value form, and the
  mean-value form of the Lagrangian f − 58.51(x647 + 1) − 20891.4(x772 − 0.999)
  (KKT multipliers from NNLS on the active constraints); pruning with both
  enclosures of the constrained variables. Best-first for 3600 s: 2.37M
  boxes, 40.07% of the volume closed at the end of the run (39.7% at
  3399 s), **certified bound −4024.49**.
- **Why it is weak.** The Lagrangian minimum over the box is −3386.8 < UB at a
  point with x647 = −1.18, so some regions must be proved infeasible; the
  Lagrangian Hessian at the optimum is indefinite (eigenvalue −44), so the
  third-order bound never applies; first-order enclosures overestimate by a
  factor of 4–10 on boxes 2–5% wide.
- **Primal.** `ann_point.py` builds the full point: −3379.98239407177, row
  violation 1e-59 (4.6e-27 after 30-digit rounding), no bound violations;
  slightly better than p1.

## 5. eg_disc_s, eg_disc2_s, eg_int_s (`eg/`)

*Follow-up (root, 2026-10-01):* a later retry closed all three instances to
a relative 1e-9 against exactly feasible points, independently verified;
see [`eg/retry.md`](eg/retry.md). This section describes the failed wave-3
attempt.

- **Structure (`eg_model.py`).** Seven decision variables, 3–4 integer (the
  scale 0.1 on integers is exact); 24 objective rows objvar ≥ c_k + g_k(x),
  and 4 side rows. Each g_k is a sum of 97 terms a·exp(Σ_i γ_i(μ_i + s_i x_i)²)
  plus linear terms: a minimax over GP-like surrogates.
- **Methods.** Integers relaxed and split at integers; exact exponent ranges;
  rigorous exp; natural and mean-value enclosures; max over rows. A
  second-order-plus-LP variant (`eg_bb2.py`) improved bounds only about 2×
  at 20 ms per box.
- **Results.** Below the listed bounds: eg_int_s 2.43 after 600 s (SCIP
  6.33); eg_disc2_s −0.056 after 1800 s (SHOT 0).
- **Why it failed.** The functions are rugged (F from 6.8 to 26.7, γ up to
  46, enclosure widths about 0.7 at half-width 0.01).
- **Side finding.** The listed eg_int_s point sits exactly on row e26's
  bound; polished, its value is 6.4531031593.

## 6. Mechanisms

| instance | mechanism |
|---|---|
| KAN (all six) | reduced-space B&B over the inputs, with an ideal-network perturbation bound and affine-split/third-order bounds |
| powerflow0030p | Lagrangian/affine split (SDP dual; the relaxation is tight) |
| powerflow0039p, 0039r | the same, plus spatial branching; stalled on a localized rank defect |
| ann_cumene_tanh | reduced-space B&B with a Lagrangian bound; weak |
| eg_* | reduced-space B&B; failed |

## 7. Commands run (targeted only; no project-wide checks, no CI)

- `kan/run_kan.py <name> 1e-10 <T>` for all six (`run_queue.sh` covers the
  r3 reruns and r5_n5/r5_n8); `kan/kan_check.py <name> random` for all six;
  `kan/kan_summary.py`.
- `powerflow/pf_cert.py` on 0030p, 0030r, 0039p, 0039r; `pf_check.py` on
  0030p, 0039p, 0039r; `pf_bb.py` on 0039p (13 nodes; stopped);
  `pf_bb2.py` on 0039p (final 31 nodes) and 0039r (61 nodes), stopped after
  stalling; GAMS CONOPT/IPOPT local solves (`powerflow/gms/local.sh`, log
  `logs/powerflow0039p.gams_local.log`; downloaded `.gms` files deleted).
- `ann/ann_fast.py 1e-9 3600 best`; an earlier depth-first run of 2197 s;
  `test_h3.py`; `ann_point.py`.
- `eg/eg_bb.py eg_int_s 1e-9 600`; `eg/eg_run.py eg_disc2_s 1800`.

## 8. Files

Under `research-20260929/open-instances-wave3/`: shared `bbcore.py`,
`qpbound.py`; `kan/` (model, interval code, B&B, checks, runner, summary);
`powerflow/` (`pf_model.py`, `pf_sdp.py`, `pf_cert.py`, `pf_check.py`,
`pf_bb.py`, `pf_bb2.py`, `gms/local.sh`); `ann/` (`ann_model.py`,
`ann_bb.py`, `ann_fast.py`, `ann_h3.py`, `test_h3.py`, `ann_point.py`);
`eg/` (`eg_model.py`, `eg_bb.py`, `eg_bb2.py`, `eg_run.py`); `logs/`
(results, SDP multipliers, B&B logs, model dumps); `sol/` (MINLPLib points
and the agent's primal points `*.wave3.sol`).

Sources: [arXiv 2503.02807](https://arxiv.org/html/2503.02807v1),
[MINLPLib](https://www.minlplib.org).

## 9. Revision after verification (root, 2026-09-30)

An independent verifier checked the KAN, powerflow and ann results with its
own code ([report](../reviews/wave3-verification/verification-report.md)):

1. **KAN.** Structure and the relaxation R verified; the Δ logic checked but
   not recomputed (an independent bound that needs no Δ confirms the dual
   bounds); the
   verifier's own branch and bound on the model's pieces reproduces all six
   bounds (e.g. kan_r3_h1_n4 ≥ 0.0027812371879, kan_r5_h1_n8 ≥
   0.0693278605795, both above the claimed values) and found the new optima
   independently. **Correction:** the exactly feasible set of each KAN OSIL
   model is empty (proved), so "closed" is restated as "optimum of the
   relaxation R certified to about 1e-10". Knot gaps reach 1.5e-15 rather
   than 6e-16 (no effect). MINLPLib's points violate non-partition rows by
   up to 9e-11.
2. **powerflow0030p** verified (exact Lagrangian evaluation; exact LDLᵀ PSD
   proof); the printed bound is corrected to 576.8934122988004.
3. **powerflow0039p/0039r:** root bounds and the branch-and-bound argument are
   valid; the 0039r final bound holds, but an accurately solved root SDP
   (41867.7797) already beats it; the 0039p final bound 41868.26524 could not
   be reproduced because node multipliers were not stored. The extension
   (`powerflow/extension-report.md`) closes 0039p and 0039r; verified in
   `../reviews/powerflow0039-review.md`.
4. **ann_cumene_tanh:** the relaxation is verified; the bound −4024.49 is
   verified per box with caveats (the 3600 s run was not repeated).
5. **Status:** MINLPLib values match; all ten instances were open; no prior
   certificates found (brief search).

*Root edits (2026-09-30, closing revision).* Verifier correction 6 is now
applied in Section 4 (40.07% of the volume closed at the end of the run).
Item 1 above now says that the Δ logic was checked but not recomputed, as
the verifier wrote. Item 3 and the Summary's powerflow bullet point to the
extension that closes 0039p and 0039r and to its review. No bound changed.
