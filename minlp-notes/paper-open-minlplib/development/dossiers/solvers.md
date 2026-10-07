# Dossier: solver behaviour (family key `solvers`)

**Scope.** This family covers five results:

- the one-hour BARON 26.5.27 / GUROBI 13.0.2 / SCIP 10.0.3 campaign on the 43 paper
  instances;
- the two BARON optimality claims (camshape100/200) that are inconsistent with our
  exact optima;
- the SCIP wrong-optimal-value defect on waterno2 subproblems, whose traced
  mechanism is reverse propagation with a binary64 residual;
- published claims that our certificates contradict: CAMINO's Gurobi 13.0.0
  bounds, SCIP 9.0.1's KAN optima, MINOTAUR and ANTIGONE on QPLIB copies, and
  MINOTAUR's optcdeg2 infeasibility claim;
- tolerance artifacts in solver and library points.

The listed-bound audit (19 invalid MINLPLib duals, emfl, LINDO rocket/methanol50)
belongs to the `audit` dossier. It is cited here only where it touches solver
behaviour.

**Paths.**

- `R/` = `research-20260929/`
- `P/` = `R/publication/`
- `C/` = `paper-open-minlplib/development/dossiers/solvers-checks/`

The checks written for this revision are in `C/r2/`, with a README. The earlier
draft's checks are in `C/` itself.

**Status words.**

- **proved**: exact rational arithmetic, or outward-rounded arithmetic, with the
  stated trust base.
- **verified**: an independent reviewer re-derived it with its own code.
- **assumption-qualified**: the proof holds only under the named assumptions.
- **numerical**: solver output or floating-point evidence only.

**Revision note.** This file replaces an earlier draft written the same day. I
treated that draft as an unreviewed input:

- I re-implemented its two new computations independently (exact camshape-type
  bounds on QPLIB copies; worst-case tolerance deficits). Both reproduce to all
  printed digits.
- I re-derived its propositions.
- New in this revision: a MINLPLib-wide scan for the SCIP data trigger; the
  finding that QPLIB's own best values for QPLIB_2703 and QPLIB_3177 lie below
  rigorous bounds; exact evaluation of five campaign savepoints; the
  MINLPLib-convention framing of the BARON claims; BARON and Gurobi
  patch-release context.

---

## 0. Summary for the paper author

1. **Campaign (numerical; independently reviewed; recounted here).**
   - 129 kept outcomes (43 instances × 3 solvers); 126 pass the measurement rule;
     3 SCIP runs stopped at the 8192 MiB memory cap.
   - Zero closures consistent with our certificates.
   - All 109 finite final duals are weaker than our certificates. The smallest
     margin is 5.2581469e-7 (BARON, camshape100). Six of the 109 are BARON values
     that BARON itself disclaims ("Globality is therefore not guaranteed").
   - My own recount from `results_table.csv` reproduces every headline number.
2. **Two kinds of disagreement must be kept apart.**
   - **(A) Tolerance artifact.** The reported value lies below the exact optimum,
     the reported dual is still valid, and the point is feasible only within a
     tolerance.
   - **(B) Invalid bound.** A reported dual bound, or an infeasibility claim,
     contradicts an exactly feasible point.
   - Only SCIP on waterno2 subproblems, CAMINO's recorded Gurobi bounds and
     MINOTAUR's optcdeg2 infeasibility claim are category B.
3. **BARON camshape100/200 (proved, category A).**
   - BARON's dual bounds are valid, and lie within 1.23e-7 and 4.80e-7 (relative)
     of the exact optima.
   - Its returned points are not exactly feasible: they violate rows and the r₁
     upper bound by about 1e-10.
   - Their deficits are 87% of the rigorous worst case that 1e-10 violations allow
     (Proposition 5).
   - At MINLPLib's 1e-6 relative gap, BARON thus closes both instances in 0.45 s
     and 23 s (as one solver; MINLPLib's S mark needs three). The paper must say
     this next to "zero closures" (issue S1).
4. **SCIP defect (refutation proved; mechanism traced in 15 instrumented runs).**
   - Eight exactly feasible rational witnesses refute SCIP's "optimal" values:
     waterno2_06 periods 0, 4 and 5; one cell-pair subproblem; four small models.
   - SCIP's own feasibility check accepts every witness. The wrong claims are
     therefore inconsistent with SCIP's own tolerance semantics, not only with
     exact decimal semantics.
   - For the 15-variable reproducer fm336, the claims are wrong in every reading
     of the data (Proposition 9).
   - New: a scan of all 1632 MINLPLib OSIL files finds the trigger pattern only in
     the nine waterno2 instances. The pattern is an equality y = x² or y = x³
     whose decimal bounds agree at a bound but disagree after binary64 rounding.
5. **Published claims.**
   - **CAMINO.** The best bounds recorded for Gurobi 13.0.0 exceed the objectives
     of interval-verified feasible points by 4.3%, 7.5% and 81%. These are invalid
     recorded bounds (assumption-qualified). The cause is unknown.
   - **KAN.** SCIP 9.0.1's published optima for kan_r3_h1_n4/n5 lie 1.70e-3 and
     2.03e-3 below the certified minimum of the network relaxation R (category A).
   - **QPLIB camshape copies.** Direct exact bounds on the copies, computed
     independently twice, now prove the following:
     - MINOTAUR's "Optimal" −4.2774 on QPLIB_3177 is not attained by any exactly
       feasible point (margin ≥ 3.16e-3).
     - ANTIGONE's "Global minimum" −4.284302 on QPLIB_2738 is not attained either
       (margin ≥ 1.55e-4).
     - QPLIB's own best values for QPLIB_2703 and QPLIB_3177 lie 8.15e-6 and
       3.27e-5 below rigorous bounds for those instances.
   - **MINOTAUR optcdeg2.** MINOTAUR's "Detected infeasibility" on QPLIB_8803 is
     false, assuming the `.nl` file encodes the MINLPLib model.
6. **Nothing found invalidates a claimed result of this family.** The issues are
   framing (S1, S2), stale or wrong supporting sentences (S5–S7), version context
   (S8), assumptions to state (S9–S11), process (S12, S13) and optional checks
   (S14, S15, S18). See Section 8.

---

## 1. Instances and models

### 1.1 Campaign instances

The campaign ran the unmodified MINLPLib GAMS files (`P/solver-runs/gms/`; 29 NLP
and 14 MINLP solve statements; hashes in `gms_manifest.*`). Our certificates
concern the OSIL files.

| group | instances | what the certificate covers |
|---|---|---|
| closed (31) | lnts50/100/200/400, dtoc5, camshape100/200/400/800, lukvle10, optcdeg2, hvycrash, ex6_2_7, ex6_2_5, etamac, pricing050 (max), chain50/100/200/400, catmix100/200/400/800, powerflow0030p/0039p/0039r, pindyck, eg_int_s, eg_disc_s, eg_disc2_s | OSIL model, exactly feasible points |
| improved (6) | waterno2_06/09/12/18/24, ann_cumene_tanh | OSIL model |
| KAN (6) | kan_r3_h1_n4/n5/n9, kan_r5_h1_n3/n5/n8 | network relaxation R only; the OSIL models are exactly infeasible (proved in wave 3) |

**Versions and settings.**

- GAMS 54.3.1 (61154be4).
- BARON 26.5.27 (built 2026-05-27).
- GUROBI 13.0.2 (v13.0.2rc1).
- SCIP 10.0.3 (d409edf9f6), with CPLEX 22.1.2.0 as LP solver, Ipopt 3.14.19,
  CONOPT 4.39.1 and PaPILO 3.0.1.
- Every job used `reslim=3600 threads=1 optcr=1e-9 optca=1e-9` and no option
  files.
- BARON's limit is CPU time; GUROBI and SCIP use wall time.

**Model points that affect comparisons.**

- **GAMS vs OSIL.** Review r1 checked all 43 pairs for identical names, types,
  bounds and senses, and for numerical agreement of functions at random points.
  This is strong evidence of equivalence, not an algebraic proof. The status
  report found that the OSIL coefficients of catmix100–800 (and of methanol50 and
  lop97icx) differ from the `.gms` text by at most 2.4e-16 relative per
  coefficient (`P/minlplib-status/report.md`). No comparison below is sensitive
  to this.
- **SCIP tightened models.** SCIP raised log/pow argument lower bounds to 1e-9 on
  ex6_2_5, ex6_2_7, etamac, hvycrash, lukvle10 and pindyck. Its six finite duals
  there bound a slightly tightened model.
- **BARON disclaimers.** BARON prints "User did not provide appropriate variable
  bounds … Globality is therefore not guaranteed" on catmix100/200/400/800, dtoc5
  and optcdeg2.
- **KAN.** Comparisons concern R. R drops the partition-of-unity rows, the B ≥ 0
  bounds and most intermediate bounds. The certified dual is min f̃ over R̃ minus
  Δ, where Δ ≤ 1.38e-10 covers decimal rounding (`R/open-instances-wave3/report.md`
  §2.2).

### 1.2 camshape (MINLPLib camshape-n; COPS 2.0 problem 4)

I identified the data from the `.gms` files (C/r2 `cambd.py` asserts the
structure). Let θ = 2π/(5(n+1)), c = 2 cos θ, α = 1.5 θ. The constants are
written as 15-significant-digit decimals, for example c = 1.99984519984971 and
α = 0.0186629266549889 for n = 100. The model is:

    minimize   f(r) = −(π/n) Σ_{j=1..n} r_j            (objective row with objvar)
    subject to 1 ≤ r_j ≤ 2,   r_1 ≤ 1/(c−1),   r_n ≥ 2 − α
               (C_j)  c r_{j−1} r_{j+1} − r_j (r_{j−1} + r_{j+1}) ≤ 0,   j = 1..n,
                      with r_0 = 1 and r_{n+1} = 2 substituted
               c r_n² − 4 r_n ≤ 0
               r_{j+1} − r_j = d_j,   |d_j| ≤ α (j = 2..n−1),   d_1 free.

The QPLIB copies (QPLIB_2738/2480/2703/3177, donor R. Misener) are the same
models with constants rounded to 8–10 significant digits (for example
c = 1.9998452 for n = 100) and with different variable numbering. My parser
checks that all n−1 convexity rows C_1..C_{n−1} share one coefficient c, that
every slope pair exists, and that the bounds have the shape above.

### 1.3 SCIP subproblem models (`P/scip-bug/`)

**Pump-station structure (waterno2).** Each pump has a binary b, a speed s, a
square q = s² and a cube p = s³:

    s ∈ [L, 1],   s − (1 − L) b ≤ L,     q ∈ [L², 1],  q − s² = 0,
    p ∈ [L³, 1],  p − s³ = 0.

The values L ∈ {0.6, 0.7, 0.8, 0.85} occur in every waterno2 period. L² and L³
are written as exact decimals (0.49, 0.343, 0.614125, …). If b = 0, the speed row
and the bound force s = L, and then the equalities force p = L³ = lb(p). Example
from `models/p4.cip`:

- `x546 ∈ [0.7, 1]`
- `e472_up: x546 − 0.3 b48 ≤ 0.7`
- `x995 ∈ [0.343, 1]`
- `e1222: x995 = x546³`

**The models.**

- **p0, p4, p5.** Single-period Lagrangian subproblems of waterno2_06: 166
  variables (9 binary), 203 rows (138 linear, 65 nonlinear). The objective is the
  wave-2 Lagrangian with multipliers `R/open-instances-wave2/waterno2/logs/scip_repro_mult.json`.
  The reviewer proved each row an exact copy of the same-named OSIL row
  (`P/reviews/scip-bug-r1/rv_osil_crosscheck.log`).
- **pair2236.** Period 3 of waterno2_06 restricted to one entry/exit cell pair
  (cert2 record 2236). Seventeen variable bounds form the cell box; the objective
  uses that record's multipliers.
- **tiny2** (3 variables, 2 rows): min 0.2 b − 2.4 s + p subject to p = s³,
  s − 0.3 b ≤ 0.7, b ∈ {0,1}, s ∈ [0.7, 1], p ∈ [0.343, 1].
- **fm336** (15 variables, 12 rows; the main reproducer). Pumps i = 0, 1, 2 with
  (L₀, L₁, L₂) = (0.7, 0.85, 0.6):

      min  5w₀ + 0.2b₁ + w₁ + 0.1b₂ + 2w₂
      s.t. p₀ = s₀³,  p₂ = s₂³,  p₁ = 0.614125 (fixed by its bounds; no cube row)
           s₀ − 0.3b₀ ≤ 0.7,   s₁ − 0.15b₁ ≤ 0.85,   s₂ − 0.4b₂ ≤ 0.6
           q₀ − 3s₀ − 0.3b₀ ≤ −2.1,  q₁ − 2s₁ − 0.3b₁ ≤ −1.7,  q₂ − 3s₂ − 0.3b₂ ≤ −1.8
           wᵢ − pᵢ − bᵢ ≥ −1 (i = 0, 1, 2),   q₀ + q₁ + q₂ ≥ 0.5
           s₀ ∈ [0.7,1], s₁ ∈ [0.85,1], s₂ ∈ [0.6,1], p₀ ∈ [0.343,1], p₂ ∈ [0.216,1],
           q₀, q₁ ∈ [0,1], q₂ ∈ [0,0.5], wᵢ ∈ [0,1], bᵢ ∈ {0,1}.

- **pumps_default** (20 variables, 12 rows) and **fm318** (10 variables, 8 rows;
  wrong on master only) have the same structure.

### 1.4 Models behind the published claims

| claim | model the solver ran | relation to our certified model |
|---|---|---|
| CAMINO Gurobi 13.0.0, eg_* | MINLPLib `.mod` files via the AMPL Python interface (`benchmark/using_amplpy.py`) | Header "GAMS Convert at 01/12/18". Feasibility was proved directly on the `.mod` rows. CAMINO's local copy is assumed equal to the current file. |
| SCIP 9.0.1, KAN (Karia–Lastrucci–Schweidtmann 2025) | Pyomo "Default" formulation via ASL | Variable, constraint and integer counts equal MINLPLib's. The input order was confirmed by the reviewer's permutation test. Identity up to coefficient printing is inferred, not proved. |
| ANTIGONE 1.1, QPLIB_2738 | `QPLIB_2738.gms.gz` under GAMS 52.3.0, `OptFile 1` (contents unknown) | Our bound uses the saved `QPLIB_2738.gms`. GAMS reports 201 rows, 200 columns and 697 nonzeros, which matches. |
| MINOTAUR 0.4.1, QPLIB_3177 / 8803 / 8585 | `cnonconvex/QPLIB_*.nl` | The `.nl` files were not obtained. Our bounds use the `.gms` copies. Equality of `.nl` and `.gms` is an assumption. QPLIB_8803/8585 `.gms` are textually identical to MINLPLib optcdeg2/dtoc5, except for the solve statement and one redundant declaration (`P/literature/control/checks/qplib_dtoc5_optcdeg2_identity.log`). |

---

## 2. Listed status (MINLPLib, fetched 2026-09-29, unchanged at the 2026-10-02 refresh)

None of the 43 campaign instances is marked solved. MINLPLib's S mark requires
that at least three solvers claim global optimality within a 1e-6 relative gap
for the best known feasible point (`vigerske2026-minlplib-documentation-database-snapshot-2026`).
The values below come from `P/solver-runs/references.csv`, which matches the
summary and `R/bound-audit/pages.json`.

| instance | best listed dual (solver) | best listed primal (point, infeasibility) | our certificate (safe display) |
|---|---|---|---|
| camshape100 | −4.28415233 (ANTIGONE) | −4.28414712 (p1, 9e-16) | −4.28414712174675 (exact optimum, rounded down) |
| camshape200 | −4.63229055 (ANTIGONE) | −4.27850023 (p1, 1e-15) | −4.27850023299273 (exact optimum, rounded down) |
| camshape400 | −4.97265746 (ANTIGONE) | −4.27569663 (p2, 3e-10; tolerance artifact) | −4.27568847892555 |
| camshape800 | −5.12584096 (GUROBI) | −4.27430687 (p2, 3e-10; tolerance artifact) | −4.27427414195420 |
| optcdeg2 | 292.41713458 (GUROBI) | 293.8760751 (p1, 2e-15) | 293.87607509587509 (rounded down) |
| eg_int_s / eg_disc_s / eg_disc2_s | 6.32629896 (SCIP) / 3.36596129 (SCIP) / 0 (SHOT) | 6.45310316 / 5.76053962 / 5.64210058 | 6.4531031529331155 / 5.760539610694994 / 5.642100574331458 (A1/A2) |
| kan_r3_h1_n4 / n5 | 0.0003908 / −0.01302849 (GUROBI) | 0.00278124 / −0.01104268 | min R ≥ 0.0027812371525814 / ≥ −0.011042679521782 |
| waterno2_06 / 09 / 12 / 18 / 24 | 165.1902989 (SCIP) / 273.8958303 (SCIP) / 479.5051427 (GUROBI) / 770.7361733 (SCIP) / 1095.126488 (SCIP) | 282.8880374 / 922.5952898 / 2263.358374 / 5269.638815 / 7332.721691 | 278.230573 / 824.834692 / 2089.754565 / 4790.820715 / 6576.151388 |

Also relevant to the scope of the SCIP defect (Observation 12):

- waterno2_01 and waterno2_02 are marked solved. Several solvers agree, for
  example on 02: SCIP 39.57142193, COUENNE 39.5714215, ANTIGONE 39.57141794,
  primal 39.57142193.
- waterno2_03 and waterno2_04 are not marked solved, but their SCIP duals
  (115.0045167 and 145.4397918) equal their listed primals. The other solvers'
  duals are slightly lower (pages.json).

---

## 3. Results as propositions, with proofs

### 3.0 Semantics and a basic lemma

A model M has decimal data, read as exact rationals.

- A point is **exactly feasible** if it satisfies every row, bound and
  integrality condition exactly.
- A point is **ε-feasible** if every row and every bound is violated by at most
  ε in the row's written scaling.
- v*(M) is the infimum of the objective over exactly feasible points
  (minimization).
- A dual bound d is **valid** if d ≤ v*(M).
- A solver's **optimality claim** is GAMS model and solver status 1/1, or
  "bound = objective" when the run stops before its limit.

**Lemma 1 (certificate-implied infeasibility).** Let d be a valid lower bound for
M. A point x̂ with f(x̂) < d is not exactly feasible for M.

*Proof.* Otherwise d ≤ v*(M) ≤ f(x̂). ∎

Lemma 1 turns "a returned point is infeasible" into a proof whenever f(x̂) is
evaluated accurately. Row residuals are then only supporting evidence.

### 3.1 The campaign (numerical facts; Proposition 1)

**Proposition 1 (measured facts).** In the final campaign (driver PID 898862,
2026-10-03T00:56Z to 13:33:28Z):

| solver | measurement-valid | finite final duals | returned primals | raw optimality claims | accepted closures | capability failures | other failures | memory stops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BARON | 43 | 35 (6 disclaimed) | 35 | 2 | 0 | 8 (sin/cos: lnts50/100/200/400, powerflow0030p/0039p; cos: hvycrash; tanh: ann_cumene_tanh) | 0 | 0 |
| GUROBI | 43 | 36 | 40 | 0 | 0 | 0 | 1 (lukvle10, error 10024: POW needs a constant argument) | 0 |
| SCIP | 40 | 38 | 30 | 0 | 0 | 1 (tanh) | 0 | 3 (ex6_2_5, ex6_2_7, pindyck) |

Further facts:

- Of the 109 finite duals, 91 compare with OSIL certificates and 18 with R.
- Every finite dual is weaker than its certificate. The smallest margin is
  5.2581469e-7 (BARON camshape100), then 2.05270746e-6 (BARON camshape200), then
  2.19e-5 (GUROBI lnts50).
- No dual exceeds a reference primal.
- Five duals improve the listed best dual:
  - BARON on camshape100/200/400;
  - GUROBI on lnts200 (0.552265826638 vs 0.55219867);
  - SCIP on waterno2_18 (891.934497970 vs 770.7361733).
- Ten runs were admitted in an overloaded first batch: dtoc5, optcdeg2 and
  waterno2_24 for all three solvers, plus kan_r3_h1_n9/BARON. Load reached up to
  50.95 on 36 threads, and MemAvailable fell to 1.06 GB. Their CPU/wall ratios,
  0.9561–0.9811, are the ten lowest of 117 long runs.
- All four BARON wall-time overruns (3706.37–3728.4 s, BARON CPU 3600.01–3601.65 s)
  fall in that first batch.

*Evidence.* Raw logs, traces and `run.json` files under
`P/solver-runs/runs/`. Independent review r1 re-extracted all 129 rows with its
own code (`P/reviews/solver-analysis-r1/`). My recount (`C/r2/recount.py`,
`recount.log`; `margins.py`, `margins.log`) agrees on every number above. This
is solver output, not proof. ∎

### 3.2 A discrete comparison bound for camshape-type models (proved)

**Lemma 2 (discrete comparison).** Let c ∈ ℚ and n ≥ 2. Define U₀ = 1, U₁ = c and
U_{m+1} = c U_m − U_{m−1}, so that U_m = U_m(c/2) is the Chebyshev polynomial of
the second kind. Assume U_m ≥ 0 for 0 ≤ m ≤ n−1.

Let u₀, …, u_n be real numbers with e_j := u_{j−1} − c u_j + u_{j+1} ≥ −δ for
j = 1, …, n−1, where δ ≥ 0. Let S₀ = u₀, S₁ ≤ u₁ and S_{j+1} = c S_j − S_{j−1}.
Then

    u_j ≥ S_j − δ W_j  for 0 ≤ j ≤ n,   where W₀ = W₁ = 0 and W_j = Σ_{m=0}^{j−2} U_m.

*Proof.* Put z_j = u_j − S_j. Then z₀ = 0, z₁ ≥ 0 and
z_{j+1} = c z_j − z_{j−1} + e_j. By induction on j ≥ 1,

    z_j = U_{j−1} z₁ + Σ_{k=1}^{j−1} U_{j−1−k} e_k.

The case j = 1 is trivial. For the inductive step, use c U_{j−1−k} − U_{j−2−k} = U_{j−k}
for k ≤ j−2, c U₀ = U₁ for k = j−1, and the new term U₀ e_j. Since U_m ≥ 0,
z₁ ≥ 0 and e_k ≥ −δ, we get z_j ≥ −δ Σ_{k=1}^{j−1} U_{j−1−k} = −δ W_j. ∎

**Proposition 3 (exact lower bound; proved, computer-assisted).** Consider a
model with:

- radii r₁, …, r_n and bounds lb_j ≥ 1, ub_j;
- rows C₁: c r₂ − r₁ r₂ − r₁ ≤ 0 and C_j: c r_{j−1} r_{j+1} − r_j r_{j−1} − r_j r_{j+1} ≤ 0
  for 2 ≤ j ≤ n−1;
- slope rows r_{j+1} − r_j = d_j with d_j ∈ [−α_j, α_j] (α_j = ∞ allowed);
- objective f = κ − Σ_j w_j r_j with every w_j > 0;
- any other rows.

Assume U_m(c) ≥ 0 for m ≤ n−1. Define:

- S₀ = 1, S₁ = 1/ub₁ and S_{j+1} = c S_j − S_{j−1};
- B_j = min(ub_j, 1/S_j) if S_j > 0, and B_j = ub_j otherwise;
- E_j, the result of a forward pass E_j ← min(E_j, E_{j−1} + α_{j−1}) and a
  backward pass E_j ← min(E_j, E_{j+1} + α_j), started from E = B.

Then every exactly feasible point satisfies r_j ≤ E_j, and hence
f ≥ κ − Σ_j w_j E_j.

*Proof.*

1. Put u_j = 1/r_j > 0 and u₀ = 1. Dividing C₁ by r₁r₂ > 0 gives
   u₀ − c u₁ + u₂ ≥ 0. Dividing C_j by r_{j−1} r_j r_{j+1} > 0 gives
   u_{j−1} − c u_j + u_{j+1} ≥ 0.
2. Also u₁ ≥ 1/ub₁ = S₁. Lemma 2 with δ = 0 gives u_j ≥ S_j, so r_j ≤ 1/S_j
   whenever S_j > 0. Together with r_j ≤ ub_j, this gives r_j ≤ B_j.
3. The slope rows give |r_{j+1} − r_j| ≤ α_j, so r_j ≤ B_k + Σ_{i between j and k} α_i
   for every k.
4. Each update in the two passes replaces E_j by a minimum of valid upper bounds
   on r_j, so r_j ≤ E_j.
5. Since w_j > 0, f ≥ κ − Σ w_j E_j. Rows not used only strengthen the true
   optimum.

In the computation, 1/S_j is rounded up to a 1e-40 grid; an upper bound stays an
upper bound. Everything else is exact rational arithmetic. ∎

*Computation* (`C/r2/cambd.py` with my own GAMS-subset parser `gparse.py`;
log `cambd.log`; 3.2 s in total). The script:

- parses every equation into an exact polynomial and asserts complete
  tokenization;
- identifies the objective, slope and convexity rows by their monomial
  structure;
- asserts one common c, U_m ≥ 0 and lb_j ≥ 1;
- returns the bound.

Displays below are floor values, so each is itself a valid bound.

| model | n | c | lower bound (safe display) | comparison |
|---|---|---|---|---|
| MINLPLib camshape100 | 100 | 1.99984519984971 | −4.284147121746744 | equals the certified exact optimum −4.2841471217467438034… |
| QPLIB_2738 | 100 | 1.9998452 | **−4.284146267804612** | QPLIB's point gives −4.284146267804670 (5.8e-14 above) |
| MINLPLib camshape200 | 200 | 1.99996091355262 | −4.278500232992723 | equals the certified optimum |
| QPLIB_2480 | 200 | 1.999960914 | **−4.278490409673679** | QPLIB's point lies 1.5e-12 above |
| MINLPLib camshape400 | 400 | 1.99999017956722 | −4.275688478925544 | equals the certified optimum |
| QPLIB_2703 | 400 | 1.99999018 | **−4.275650712512653** | QPLIB's point lies 8.15e-6 **below** (Proposition 15) |
| MINLPLib camshape800 | 800 | 1.99999753875636 | −4.274274141954195 | equals the certified optimum |
| QPLIB_3177 | 800 | 1.999997539 | **−4.274187151471744** | QPLIB's point lies 3.27e-5 **below** |

**Two independent implementations agree.** The earlier draft's `C/cambound.py`
and my `C/r2/cambd.py` agree on all eight values to every printed digit. They
share no code: the earlier one uses regex-based monomial extraction, mine a
recursive-descent parser.

For the MINLPLib models, the bound equals the exact optimum because the camshape
family proves the envelope point exactly feasible. For the copies, attainment is
not claimed. Proposition 3 gives only a lower bound, which is all that the
refutations need.

### 3.3 BARON's camshape100/200 optimality claims (proved; category A)

**Proposition 4.** On MINLPLib camshape100 and camshape200, BARON 26.5.27 (GAMS
54.3.1, optca = optcr = 1e-9, one thread) reports "Normal completion" with model
status 1. It reports Solution = Best possible = −4.28414764756144 (camshape100,
3 iterations, 0.45 s) and −4.27850228570019 (camshape200, 23.22 s). Then:

- (i) both reported duals are valid;
- (ii) both returned points are not exactly feasible;
- (iii) the claimed optimal values lie 5.2581469e-7 and 2.05270746e-6 below the
  exact optima, that is, 1.23e-7 and 4.80e-7 relative. This exceeds the
  requested 1e-9 gaps but is within MINLPLib's 1e-6 relative gap.

*Proof.*

- By Proposition 3, v*₁₀₀ ≥ −4.2841471217467438034… and
  v*₂₀₀ ≥ −4.2785002329927222918…. Equality holds by the camshape family's
  exactly feasible envelope points, but only the inequality is needed here.
- (i) The reported duals are below these values.
- (ii) I evaluated the returned points exactly from the binary64 levels in the
  GDX savepoints (`C/r2/ev.py`, `ev.log`). The objective at the radii is
  −4.28414764756144 and −4.27850228570019, below the bound. Lemma 1 applies.
- (iii) Subtract. ∎

The same exact evaluation finds the following residuals. They are evidence, not
part of the proof:

- camshape100: maximum row violation 9.9950e-11 (e100) and maximum bound
  violation 9.9966e-11, on the upper bound of r₁ = x1;
- camshape200: maximum row violation 9.9975e-11 (e200) and maximum bound
  violation 9.9979e-11 (x1).

These match `P/solver-runs/point_checks.log` and the reviewer's own check.

### 3.4 How large can a tolerance artifact be? (camshape; proved)

**Proposition 5 (worst-case tolerance deficit).** For a camshape-type model as
in Proposition 3 with every lb_j ≥ 1, and for 0 ≤ ε < 1, let 𝓕_ε be the set of
ε-feasible points. Then every x ∈ 𝓕_ε satisfies f(x) ≥ v_ε, where v_ε is the
bound of Proposition 3 recomputed with these changes:

- δ = ε/(1−ε)³;
- ub_j replaced by ub_j + ε, and S₁ = 1/(ub₁ + ε);
- α_j replaced by α_j + 2ε;
- B_j = min(ub_j + ε, 1/(S_j − δ W_j)) when S_j − δ W_j > 0.

Write D(ε) = v₀ − v_ε. For the MINLPLib models v₀ = v*, so every ε-feasible
point lies at most D(ε) below the exact optimum. This assumes that the
objective is evaluated from the radii; if the objective row itself is violated
by ε, add ε.

*Proof.*

1. For x ∈ 𝓕_ε, every radius satisfies r_j ≥ 1 − ε > 0.
2. A convexity row violated by at most ε gives, after division by
   r_{j−1} r_j r_{j+1} ≥ (1−ε)³, e_j ≥ −ε/(1−ε)³ = −δ. Row C₁ is divided by
   r₁r₂ ≥ (1−ε)² and gives a smaller residual.
3. u₁ ≥ 1/(ub₁ + ε).
4. Each slope variable satisfies |d_j| ≤ α_j + ε, and each slope equation holds
   within ε, so |r_{j+1} − r_j| ≤ α_j + 2ε.
5. Lemma 2 now gives u_j ≥ S_j − δ W_j. Steps 2–5 of the proof of Proposition 3
   then go through with the relaxed data. ∎

*Computation* (`C/r2/tol.py`, `tol.log`, 18 s; it reproduces the earlier
draft's `C/tolbound.log` exactly):

| model | ε | D(ε) | D/ε | observed deficit of a real point with max violation ≤ ε | observed / D |
|---|---|---|---|---|---|
| camshape100 | 1e-10 | 6.0447e-7 | 6.0e3 | BARON claim 5.2581e-7 | 0.870 |
| camshape100 | 7.72e-10 | 4.6665e-6 | 6.0e3 | SCIP campaign point 1.5191e-7 | 0.033 |
| camshape100 | 1e-8 | 6.0449e-5 | 6.0e3 | earlier exploratory SCIP incumbent 5.3e-5 (unchecked) | 0.877 |
| camshape200 | 1e-10 | 2.3551e-6 | 2.4e4 | BARON claim 2.0527e-6 | 0.872 |
| camshape400 | 1e-10 | 9.3475e-6 | 9.3e4 | BARON point 8.1545e-6 | 0.872 |
| camshape400 | 3e-10 | 2.8043e-5 | 9.3e4 | MINLPLib p2 8.15e-6 | 0.291 |
| camshape800 | 3e-10 | 1.1255e-4 | 3.8e5 | MINLPLib p2 3.27e-5 | 0.291 |
| camshape800 | 3.32e-7 | 0.11123 | 3.4e5 | BARON point 9.3656e-2 | 0.842 |
| camshape800 | 9.75e-7 | 0.27232 | 2.8e5 | GUROBI point 2.3284e-2 | 0.086 |
| QPLIB_2738 | 1e-8 / 2.6e-8 / 1e-6 | 6.0449e-5 / 1.5717e-4 / 5.9635e-3 | 6.0e3 | ANTIGONE deficit ≥ 1.5523e-4 | needs ε > 1e-8 |
| QPLIB_3177 | 1e-9 / 1e-8 / 1e-6 | 3.7443e-4 / 3.7296e-3 / 0.27756 | 3.7e5 | MINOTAUR deficit ≥ 3.1628e-3 | needs ε > 1e-9 |

For small ε, D(ε) ≈ 0.59 n² ε. The largest per-row weight is
U_max = 76.1, 151.8, 303.2 and 605.9 for n = 100, 200, 400 and 800. The total
weight Σ U_m is 4.35e3, 1.75e4, 6.99e4 and 2.80e5.

**Consequences.**

- The BARON deficits are about 87% of the worst case for 1e-10 violations. They
  are fully explained by tolerance, and this does not suggest a bounding error.
- Because D is increasing in ε, any point of QPLIB_2738 whose objective reaches
  ANTIGONE's value violates some row or bound by more than 1e-8. Any point of
  QPLIB_3177 that reaches MINOTAUR's value violates one by more than 1e-9. Both
  values are therefore consistent with 1e-6-tolerance points, and neither alone
  proves a bounding error.

### 3.5 The SCIP defect

**Proposition 6 (refutation; proved).** For each model M and witness x* below,
x* is exactly feasible for M with the decimal data read as exact rationals, and
f(x*) is strictly below every wrong "optimal" claim listed.

| model | witness | exact f(x*) | smallest wrong claim (version) | largest wrong claim | excess range |
|---|---|---|---|---|---|
| p0 | `witness/p0.json` | 168.108652029808 | 169.950250085232 (GAMS/SCIP) | 169.950685 | 1.84 |
| p4 | `witness/p4.json` | −6.730643699816… | −6.72988938834578 (bin 10.0.2/10.0.3, seed 3) | −4.646232 (wheel) | 7.5e-4 to 2.08 |
| p5 | `witness/p5.json` | −232.172853003462 | −231.905843299873 (master) | −228.343114 (GAMS) | 0.267 to 3.83 |
| pair2236 | `witness/pair2236.json` | 55.689908409449 | 56.4920384487893 (master) | 65.124528 (bins) | 0.802 to 9.43 |
| tiny2 (heur./sepa. off) | b = 0, s = 7/10, p = 343/1000 | −1337/1000 | −1.23108446311479 | same | 0.106 |
| pumps_default | `minimal/pumps_default_witness.json` | 153/250 | 1.19799998144798 | 1.19800 | 0.586 |
| fm336 | `min/fm336_v1010.witness.json` | 187/270 | 0.814125 (master) | 1.50521312595154 | 0.122 to 0.813 |
| fm318 (master only) | `min/fm318_master.witness.json` | 729/500 | 2.0 | 2.0 | 0.542 |

*Proof.* Exact evaluation of every row, bound and integrality condition. Eight
code bases agree:

- the track's four checkers (`exact_check.py`, `spec_check.py`, `indep_check.py`,
  and `gams_check.py`, which reads the `.gms` files);
- the reviewer's `rv_cip_exact.py` and `rv_gms_exact.py`;
- the earlier draft's `C/mycheck.py`;
- my `C/r2/cipchk.py` (`cipchk.log`).

My mutation tests are all rejected: x546 + 1e-30, x995 − 1e-30 and b6 = 1/2 in
p4. ∎

**Proposition 7 (exact optima of the small reproducers; proved by hand).**

(a) The optimal value of fm336 is exactly 187/270 = 0.69259….

*Proof.* Every objective term is nonnegative.

- If b₁ = 1, the cost is at least 0.2 + w₁ ≥ 0.2 + p₁ = 0.814125.
- If b₀ = 1, then w₀ ≥ p₀ = s₀³ ≥ 0.343, so the cost is at least 1.715.
- Otherwise b₀ = b₁ = 0. The speed rows and bounds force s₀ = 0.7 and s₁ = 0.85.
  The flow rows then give q₀ ≤ 0 and q₁ ≤ 0, and the demand row forces q₂ ≥ 0.5.
  - If b₂ = 0, then s₂ = 0.6 and q₂ ≤ 0, which is infeasible.
  - So b₂ = 1. Then q₂ ≤ 3s₂ − 1.5 forces s₂ ≥ 2/3, and
    w₂ ≥ p₂ = s₂³ ≥ 8/27. The cost is at least 0.1 + 16/27 = 187/270.

The witness attains this value. ∎

(b) The optimal value of tiny2 is exactly −1.337.

*Proof.*

- If b = 0, then s = 0.7 and p = 0.343, which gives −1.337.
- If b = 1, the minimum over s ∈ [0.7, 1] of 0.2 − 2.4 s + s³ is attained at
  s = √0.8 and equals 0.2 − 1.6√0.8 = −1.2310835056…. This exceeds −1.337 because
  0.8 < (1.537/1.6)² = 0.92280…. ∎

**Lemma 8 (binary64 residuals; proved by exact computation).** Let fl be
round-to-nearest conversion to binary64. Recomputed here in rational arithmetic:

| L | fl(L)³ − fl(L³) | fl(L)² − fl(L²) | exact decimal L³ is the written value |
|---|---|---|---|
| 0.6 | −2.1538e-17 | −1.3323e-17 | yes (0.216) |
| 0.7 | −9.2371e-17 | −5.3291e-17 | yes (0.343) |
| 0.8 | +7.4607e-17 | +5.7732e-17 | yes (0.512) |
| 0.85 | −8.0103e-17 | −6.8834e-17 | yes (0.614125) |

The tightest binary64 enclosure of fl(0.7)³ is
[0.3429999999999999, 0.34299999999999997]. Its upper end lies 5.5511e-17 below
fl(0.343) = 0.34300000000000003. SCIP's traced activity for s³ − p with both
variables fixed is [−1.6653e-16, −5.5511e-17], which is exactly this enclosure
minus fl(0.343).

**Proposition 9 (what "wrong" means; proved except where marked).**

(a) **Exact decimal model.** v*(M) ≤ f(x*) < claim (Proposition 6). Each claim
therefore overstates the optimum. SCIP's dual bound, which equals the claim up to
SCIP's gap limit, is invalid by more than 1e-4. Here 1e-4 is the scan's
threshold; the actual margins are at least 7.5e-4.

(b) **SCIP's own tolerance semantics.** SCIP 10.0.2 `checkSol` (default
tolerances) accepts all eight witnesses (`P/scip-bug/logs/checksol_witness.log`;
`P/reviews/scip-bug-r1/rv_wheel.log`). SCIP 10.0.2, 10.0.3, 10.1.0 and master
also accept the fm336 witness when it is read from a `.sol` file, and then report
0.692592587925926 as optimal. The witnesses violate the binary64-rounded rows by
at most 2.9e-15, far below 1e-6. Every refuted claim therefore exceeds the value
of a point that SCIP itself counts as feasible. The output is self-inconsistent,
independent of any choice of data semantics. (Acceptance is numerical evidence,
but the 2.9e-15 bound on the residual is exact.)

(c) **Binary64 data with zero tolerance** (fm336 only).

- By Lemma 8, b₀ = 0 forces s₀ = fl(0.7) and p₀ = fl(0.7)³ < fl(0.343) = lb(p₀),
  which is infeasible. In the same way b₂ = 0 is infeasible.
- So every feasible point has b₀ = b₂ = 1 and costs at least
  5·fl(0.343) + fl(0.1) + 2·fl(0.216) = 2.247 (to the printed digits).
- SCIP's returned point has b₀ = 0, so it is infeasible in this reading, and the
  claimed value is not the optimum.

Hence the fm336 claims are wrong in every reading. For contrast, tiny2's wrong
claim −1.23108446311479 lies 9.6e-7 below the zero-tolerance binary64 optimum
0.2 − 1.6√0.8, so tiny2 alone does not show an error under that reading. The
paper should lead with fm336 and with (b). ∎

**Observation 10 (mechanism; numerical evidence from instrumented runs).**

- **Instrumented runs.** All 15 instrumented wrong runs are listed in the 14 rows
  of `P/scip-bug/report.md` §5.3; one row combines p5 seeds 0 and 2. The builds
  are a 10.0.2 debug-solution build and a master a01de2c debug-solution build. In
  every one of these runs, the first loss of the witness follows the same event:
  the `default` nonlinear handler's reverse propagation declares a node infeasible
  on x³ − y, with x fixed at fl(0.7), y fixed at fl(0.343), propagation bounds
  [0, 0] and activity [−1.6653e-16, −5.5511e-17]. I spot-checked five traces
  (`mdbg_fm336_s0`, `dbgsol_fm336_v1010`, `mdbg_p4_s0`, `dbgsol_expr_p0_seed2`,
  `mdbg_pair2236_s14`); all show this `SCIPBUG REVCUT` line before the first
  cut-off or invalid-bound message.
- **The steps, from the tiny2 trace** (`logs/tiny2_debugprop.log`):
  1. Linear propagation fixes s = fl(0.7).
  2. In round 0, p's bound is still relaxed by about 1e-9 under the default
     `constraints/nonlinear/varboundrelax = r`. The activity contains 0. The
     propagation bounds become [0, 0], and p is fixed to fl(0.343) "within
     tolerance".
  3. In round 1 both variables are fixed. Mode `r` relaxes fixed domains by
     min(ε·max(1,|b|), 0.001·(ub − lb)) = 0. `reversepropSum` calls
     `SCIPintervalPropagateWeightedSum`, which intersects exactly
     (`SCIPintervalIntersect`, intervalarith.c about line 4793 on master) rather
     than with `SCIPintervalIntersectEps`. The intersection is empty, the node is
     declared infeasible, and b ≥ 1 becomes global.
- **What this shows.** The same 5.5e-17 discrepancy is accepted in one round and
  fatal in the next.
- **Supporting experiments.** `varboundrelax = b` (relax all bounds, including
  fixed ones) gives 0 wrong runs out of 122, against 78/122 under default
  settings on the same cases. The settings `varboundrelax = a` or `n`, nonlinear
  `propfreq = −1`, `maxproprounds = 0` and `propagating/maxrounds = 0` each
  remove the error on fm336.
- **Limits.**
  - Why `n` works is an untested hypothesis.
  - pair2236 seed 11 is uninstrumented; its first loss involves b35 at the 0.85
    station.
  - The two small-excess p4 claims are untraced.
  - The wheel, official-binary and GAMS wrong runs are linked to the mechanism
    only by the `varboundrelax = b` experiment. That is evidence, not proof.

**Proposition 11 (optimum enclosures of the waterno2 subproblems; assumes the
wave-2 rbb certifier, which was independently verified in
`R/reviews/waterno2-verification/`).** `R/open-instances-wave2/waterno2/logs/scip_unreliable_rbb.log`
certifies φ ≥ 168.107652, ≥ −6.731984 and ≥ −232.173990 for periods 0, 4 and 5.
These runs use the same multipliers as p0, p4 and p5.
`P/reviews/scip-bug-r1/` confirmed that cert2 record 5539 certifies ≥ 55.0942345372475
with the same multipliers and box as pair2236.

| model | optimum lies in | width |
|---|---|---|
| p0 | [168.107652, 168.108652029808] | 1.0e-3 |
| p4 | [−6.731984, −6.730643699816] | 1.34e-3 |
| p5 | [−232.173990, −232.172853003462] | 1.14e-3 |
| pair2236 | [55.0942345372475, 55.689908409449] | 0.60 |

The low pair2236 claims 55.689773 and 55.689858 lie inside this interval and are
**not refuted**. The scip-bug report says "the first author states" the p0–p5
enclosures and did not re-verify them. The rbb log above is the direct source.

**Observation 12 (scope of the data trigger in MINLPLib; new; exact for the
syntactic class).** `C/r2/pattern_scan.py` read all 1632 cached OSIL files (read
only; 128 s on one core; `pattern_scan.log`). It looks for equality rows
y − x^k = 0, with k ∈ {2, 3}, written as a single power, square, product or
quadratic term plus one linear term, with zero right-hand side. It then checks
whether lb(y) = lb(x)^k or ub(y) = ub(x)^k holds exactly in decimal while the
binary64 residual has the infeasible sign (fl(lb x)^k < fl(lb y), or
fl(ub x)^k > fl(ub y)).

- Twelve instances contain decimal-consistent rows of this form.
- In three of them (kall_ellipsoids_tc02b/tc03c/tc05a), every such row is also
  binary64-consistent.
- Only the nine waterno2 instances (01, 02, 03, 04, 06, 09, 12, 18, 24) contain
  binary64-inconsistent rows: 12 per period, at L = 0.6, 0.7 and 0.85 (lower
  bounds) and 0.8 (upper bound), for both squares and cubes.
- The scan is syntactic. It misses scaled forms (y = a x^k), bounds implied by
  rows, and other functions. It does not test whether SCIP's search reaches the
  fixed state.
- Relevance: the listed SCIP duals that close or nearly close waterno2_01–04
  (Section 2) are exposed to the defect in principle. No point contradicts them, and they
  were not examined.

### 3.6 CAMINO's recorded Gurobi 13.0.0 bounds (category B; assumption-qualified)

**Proposition 13.** The CAMINO-benchmark data (commit 66a134daf8,
`results/26_03_10_results/noncvx_gurobi.csv`; saved copy
`P/literature/small/sources/eg/camino_benchmark/`) record the following
"obj" and "dual_obj" values:

| instance | obj = dual_obj | time / per-instance limit |
|---|---|---|
| eg_disc2_s | 5.88669499573929 | 2.15 s / 32.63 s |
| eg_disc_s | 6.191829847658548 | 0.99 s / 19.24 s |
| eg_int_s | 11.65415903480683 | 70.80 s / 212.66 s |

Points proved feasible for the same `.mod` models have objectives
5.6421005799711067563, 5.7605396164535106058 and 6.4531031593842274088. So each
recorded bound exceeds the optimum by at least 0.2445944, 0.4312902 and 5.2010558,
that is, 4.34%, 7.49% and 80.6% of the point values. These are recomputed here
from the saved values (`C/r2/claims.log`). The recorded bounds are invalid, and
so is the optimality claim that "bound = objective" implies.

*Proof.* `P/literature/small/checks/eg_camino_gurobi.py` (log
`checks/logs/eg_camino_gurobi.log`) evaluates every row, bound and integrality
condition of each `.mod` model at the recorded point in mpmath `iv` (200 bits).
All 28 rows hold on the enclosure, with smallest proved slacks 7.5e-20, 7.8e-20
and 5.6e-20. Then v* ≤ f(x̂) < the recorded bound. ∎

**Trust base and assumptions.**

1. mpmath `iv`, including `exp`, rounds outward.
2. The `.mod` parser is correct; its row and variable counts match the header.
3. CAMINO's local `.mod` files equal the current MINLPLib files.
4. `dual_obj` is AMPL's `obj.bestbound` (`using_amplpy.py` lines 105 and 136,
   options `bestbound=1 feastol=1e-8 mipgap=1e-2 threads=1`). On 59 other early
   stops it is a genuine bound different from the objective.

The CSV records no termination status. The cause is unknown.

*Context only, not an explanation.*

- Gurobi's fixed-issue list for 13.0.2 includes "Fixed numerical issue in MINLP
  presolve that could lead to wrong answers" and "Fixed bug in MINLP presolve that
  could lead to wrong answers" (`optimization2026-fixed-issues-in-gurobi-optimizer`).
- Our GUROBI 13.0.2 runs through GAMS (a different interface and time limits)
  reached the time limit on all three instances with valid duals −6.37450863475,
  −2.86089160167 and −1.90678635916. Its eg_int_s point exceeded Gurobi's own
  tolerance (maximum violation 5.9580e-5).

### 3.7 SCIP 9.0.1 "optimal" KAN values (category A; for R)

**Proposition 14.** Karia, Lastrucci and Schweidtmann (2025; Zenodo 14961066,
"Default" logs) report "optimal solution found", gap 0, at
1.08116412047821e-3 (kan_r3_h1_n4) and −1.30809958982354e-2 (kan_r3_h1_n5).
These values lie 1.7000730e-3 and 2.0383163e-3 below the certified minima of R
(≥ 0.0027812371525814 and ≥ −0.011042679521782). No point of R attains them. In
particular, no input of the exact network attains them, and no exactly feasible
OSIL point exists.

*Proof.* R's certified bounds (wave-3 verification) apply to every point of R.
Subtract. ∎

**Evidence for the cause** (numerical):

- 60-digit forward evaluations at SCIP's reported inputs give 0.0028684784 and
  −0.0108512435. These lie above the claims and above min R. The reviewer's
  independent OSIL reader and permutation test agree.
- With the inputs fixed at SCIP 9's point, SCIP 10.0 returns "optimal"
  0.002695929010542 and −0.011320291171415, with maximum row violations 9.34e-7
  and 9.99e-7 (`P/reviews/lit-network-r1/kan_scip_fixed.log`).
- The objective is A·y + B with A ≈ 970.2 (r3), so violations of 1e-6 move it by
  about 1e-3.

SCIP's own duals (equal to the claims) are valid for R. These are tolerance
artifacts, not invalid bounds. Assumption: the published Default models equal
MINLPLib's up to coefficient printing.

### 3.8 QPLIB copies and MINOTAUR/ANTIGONE claims

**Proposition 15 (proved, computer-assisted; not yet independently reviewed).**
By Proposition 3 applied to the saved QPLIB `.gms` copies:

1. **MINOTAUR 0.4.1 on QPLIB_3177** (`P/literature/control/sources/mittelmann_cnconv/logs/QPLIB_3177.mnt`)
   reports "Optimal solution found" with best value −4.2774, one node, a
   remaining-node bound of +∞ and 2.89 s. Even the top of the printed value's
   rounding interval, −4.27735, lies at least 3.162849e-3 below the rigorous bound
   −4.274187151471744. No exactly feasible point of the copy attains the claim.
2. **ANTIGONE 1.1 on QPLIB_2738** (`QPLIB_2738.ant`, lines 206–209) reports
   "Termination Status : Global minimum" with best feasible = best possible =
   −4.284302 (printed to 7 digits) and relative gap 1e-9. It lies at least
   1.552322e-4 below the bound −4.284146267804612.
3. **SCIP 9.2.1's primal −4.33023953971002 on QPLIB_2703** lies 5.458883e-2 below
   that copy's bound.
4. **QPLIB's own best values.** `qplib.solu` lists `=best=` −4.275658867 for
   QPLIB_2703 and −4.274219874 for QPLIB_3177. The `.sol` objvar values are
   −4.275658866817820 and −4.274219874014470. These lie 8.154305e-6 and
   3.272254e-5 below the rigorous bounds. So QPLIB's reference points for these
   two instances are not exactly feasible (Lemma 1); their reported violation in
   the QPLIB model is 3.0e-10. For QPLIB_2738 and QPLIB_2480, QPLIB's points lie
   5.8e-14 and 1.5e-12 above the bounds, which is consistent. *New in this
   dossier.*
5. **Rounding shifts the optimum.** The copies' bounds exceed the MINLPLib optima
   by at least 8.5394e-7, 9.8233e-6, 3.7766e-5 and 8.6990e-5 (n = 100 … 800). So
   rounding the constants at about the 1e-10 level raises the optimum by **at
   least** these amounts. The MINLPLib optimizers are not feasible for the copies.

*Proof.* Proposition 3 and subtraction (`C/r2/claims.log`). ∎

**Assumptions.**

- MINOTAUR read `QPLIB_3177.nl`, which was not obtained; its equality with the
  `.gms` copy is assumed.
- ANTIGONE read `QPLIB_2738.gms.gz`.

**Interpretation.** Each claimed value lies below the exact optimum of the model
the solver ran, while the solver's own dual, equal to its value, remains valid.
These are category A claims. By Proposition 5 they are consistent with points of
violation above 1e-8 (ANTIGONE) and above 1e-9 (MINOTAUR). ANTIGONE's log
reports a CONOPT input-point aggregate infeasibility of 8.7007237331e-6.

MINOTAUR's closure pattern is unusual: one node, and a node bound of +∞ after an
incumbent is found. The same version ends at the 10800 s limit with gaps of
5.9–20.8% on the three smaller copies. That contrast suggests a pruning error,
but it is not a proof.

**Proposition 16 (MINOTAUR's optcdeg2 infeasibility claim is false;
assumption-qualified).** MINOTAUR 0.4.1 reports "status of presolve: Detected
infeasibility" on QPLIB_8803 after 119 s (`QPLIB_8803.mnt`). QPLIB_8803.gms
equals MINLPLib optcdeg2 except for the solve statement and one redundant
declaration. optcdeg2 has a rigorously feasible point with objective
≤ 293.87607509587509328 (bang-bang verification). So the claim is false, provided
that the `.nl` file encodes the same model. ∎

- optcdeg2 has 150003 variables, of which about 100000 have no upper bound.
- In dtoc5, MINOTAUR's QuadHandler warns that it assumed default bounds, but that
  warning appears after presolve. The optcdeg2 run stopped in presolve and
  printed no such warning.
- Whether default bounds could matter is not established. State this as an
  assumption.

**Remark (no contradiction).** MINOTAUR's "Optimal" 5.3897 on QPLIB_8585 (dtoc5)
agrees with our 5.38967211918114. It assumed default bounds for 99983/99997
variables, so it concerns a bounded restriction.

### 3.9 Trust base, by result

| result | what must be trusted |
|---|---|
| Propositions 3–5, 15 | Python `fractions`; my GAMS-subset parser (complete-tokenization asserts; two independent implementations agree); saved `.gms` files equal the solvers' inputs (MINOTAUR: `.nl` assumed equal) |
| Proposition 4 (ii) | GDX levels via `gdxdump dFormat=hexponential` (exact binary64) |
| Propositions 6, 7, 9 | `fractions` (eight code bases); for 9(b), SCIP's acceptance is SCIP output |
| Lemma 8, Proposition 9(c) | Python `float()` is correctly rounded decimal-to-binary64 conversion (IEEE 754) |
| Observation 10 | SCIP debug builds and a local diagnostic patch; read as evidence only |
| Proposition 11 | wave-2 rbb certifier (independently verified) |
| Proposition 13 | mpmath `iv` outward rounding; `.mod` parser; CAMINO `.mod` = MINLPLib `.mod`; meaning of `obj.bestbound` |
| Proposition 14 | KAN R certificate (wave-3 verification; Δ logic checked, not recomputed); model identity |
| Proposition 16 | optcdeg2 point existence (bang-bang verification); `.nl` = `.gms` |

---

## 4. Exactly feasible points used by this family

| use | point | how proved | objective |
|---|---|---|---|
| SCIP refutations | 8 rational witnesses (Proposition 6) | exact rational evaluation in eight code bases; mutation tests | exact rationals (Proposition 6 table) |
| fm336 optimum | b = (0,0,1), s = (7/10, 17/20, 2/3), p = (343/1000, 4913/8000, 8/27), q = (0,0,1/2), w = (0,0,8/27) | hand proof plus checkers | 187/270 |
| tiny2 optimum | b = 0, s = 7/10, p = 343/1000 | hand proof plus checkers | −1337/1000 |
| CAMINO refutation | `R/open-instances-wave3/eg/retry/sol/eg_*.retry.sol` | mpmath `iv` on the `.mod` rows; the eg family proves the OSIL points exactly feasible | 5.6421005799711067563 / 5.7605396164535106058 / 6.4531031593842274088 |
| BARON and QPLIB claims (camshape) | not needed: Proposition 3 alone refutes values below the bound | — | — |
| MINOTAUR optcdeg2 | optcdeg2 family point | rigorous existence (bang-bang verification) | ≤ 293.87607509587509328 |

No new primal point was constructed for this dossier.

---

## 5. Numbers tables

### 5.1 Contradicted optimality, bound or infeasibility claims

Margins are rounded down, so each is a valid lower bound on the true margin.

| # | claim (solver, source) | claimed value | rigorous comparison (safe display) | margin | category | status | sources |
|---|---|---|---|---|---|---|---|
| 1 | BARON 26.5.27 camshape100, status 1/1 | −4.28414764756144 | v* ≥ −4.28414712174675 | ≥ 5.258e-7 | A | proved | `P/solver-runs/runs/camshape100__BARON/gams.log`; `C/r2/ev.log` |
| 2 | BARON 26.5.27 camshape200, status 1/1 | −4.27850228570019 | v* ≥ −4.27850023299273 | ≥ 2.052e-6 | A | proved | `.../camshape200__BARON/gams.log` |
| 3 | SCIP 10.0.2–master, p0/p4/p5/pair2236 (default settings; seed-dependent) | e.g. 169.9502…, −6.72989…, −231.9058…, 56.4920… / 65.12… | exact witnesses | ≥ 1.84 / 7.5e-4 / 0.267 / 0.802 | B | proved | `P/scip-bug/report.md`; `logs/scan_summary.csv` |
| 4 | SCIP all tested versions, fm336 (default) | 1.50521312595154 (10.x); 0.814125 (master, 8/10 seeds) | v* = 187/270 | ≥ 0.1215 | B | proved | `P/scip-bug/logs/fm_scan.log` |
| 5 | Gurobi 13.0.0 (CAMINO), eg_disc2_s / eg_disc_s / eg_int_s | 5.88669499573929 / 6.191829847658548 / 11.65415903480683 | feasible points 5.64210057997… / 5.76053961645… / 6.45310315938… | ≥ 0.2445 / 0.4312 / 5.2010 | B | assumption-qualified (assumptions 1–4) | `P/literature/small/report.md` §9.2, §10.1, §11.1 |
| 6 | MINOTAUR 0.4.1, QPLIB_8803 (optcdeg2) | "Detected infeasibility" | feasible point exists | — | B | proved, given `.nl` = `.gms` | `P/literature/control/report.md`; `QPLIB_8803.mnt` |
| 7 | MINOTAUR 0.4.1, QPLIB_3177 | −4.2774 "Optimal" | copy bound ≥ −4.274187151471744 | ≥ 3.162e-3 | A (suspicious closure) | proved (new; two implementations; needs review) | `C/r2/cambd.log`, `claims.log` |
| 8 | ANTIGONE 1.1, QPLIB_2738 | −4.284302 "Global minimum" | copy bound ≥ −4.284146267804612 | ≥ 1.552e-4 | A | proved (as row 7) | same; `QPLIB_2738.ant` |
| 9 | SCIP 9.0.1 (Karia et al.), kan_r3_h1_n4 / n5, Default | 1.08116412047821e-3 / −1.30809958982354e-2 | min R ≥ 0.0027812371525814 / ≥ −0.011042679521782 | ≥ 1.700e-3 / 2.038e-3 | A | proved for R; identity assumed | `P/literature/network/report.md` §4.2–4.3 |
| 10 | GUROBI on MINLPLib optcdeg2 (dual 292.41713458 and point p2, infeasibility 1e-6, added 2023-04-11) | 292.417 "optimal" | v* ≥ 293.87607509587509 | ≥ 1.4589 (0.50%) | A (dual valid) | proved | `P/literature/control/report.md` (optcdeg2) |

### 5.2 Campaign headline numbers

Sources: `P/solver-runs/report.md` and `results_table.csv`. Reproduced by review
r1 and by my recount (`C/r2/recount.log`).

| quantity | value |
|---|---|
| kept outcomes / measurement-valid / memory stops | 129 / 126 / 3 |
| finite final duals (BARON / GUROBI / SCIP) | 109 (35 / 36 / 38); 6 BARON disclaimed, leaving 103 (29 / 36 / 38) |
| compared with OSIL certificates / with R | 91 / 18 |
| smallest certificate − dual margin | 5.2581469e-7 (BARON camshape100; 1.23e-7 relative) |
| accepted closures | 0 / 0 / 0 |
| raw optimality claims | 2 (BARON camshape100/200) |
| listed-dual improvements | 5 |
| returned-primal / log-incumbent forbidden-side flags | 36 / 38, on 39 pairs (30 returned flags beyond printing for OSIL; 5 for R only; 1 within printing) |
| savepoints checked at 50 digits | 18, all with positive violations (numerical) |

### 5.3 Strongest campaign dual per instance against our certificate

Sorted by relative margin. Margins are descriptive comparisons of floating-point
solver output; C is the reference certificate from `references.csv`. Source:
`C/r2/margins.py`, `margins.log`.

| instance | C | strongest D | solver | C − D (sense-adjusted) | relative | note |
|---|---|---|---|---|---|---|
| camshape100 | −4.28414712174675 | −4.28414764756 | BARON | 5.26e-7 | 1.23e-7 | optimality claim |
| camshape200 | −4.27850023299273 | −4.27850228570 | BARON | 2.05e-6 | 4.80e-7 | optimality claim |
| lnts50 | 0.5546687649381 | 0.554646860480 | GUROBI | 2.19e-5 | 3.95e-5 | |
| powerflow0039p | 41869.05148485014 | 41765.7115905 | GUROBI | 103 | 2.47e-3 | |
| powerflow0039r | 41869.05148327243 | 41745.9299435 | SCIP | 123 | 2.94e-3 | |
| lnts200 / lnts100 / lnts400 | 0.5545770161025 / 0.5545954011663 / 0.5545724137001 | 0.552265826638 / 0.551893222965 / 0.550885686672 | GUROBI | 2.3e-3 / 2.7e-3 / 3.7e-3 | 4.2e-3 / 4.9e-3 / 6.7e-3 | |
| powerflow0030p | 576.8934122988004 | 569.890824735 | GUROBI | 7.00 | 1.21e-2 | |
| lukvle10 | 352.2380254050784 | 347.646742306 | SCIP | 4.59 | 1.30e-2 | SCIP tightened model |
| etamac | −15.294675643368093 | −15.5138681230 | SCIP | 0.219 | 1.43e-2 | SCIP tightened model |
| camshape400 | −4.27568847892555 | −4.62237809041 | BARON | 0.347 | 8.1e-2 | |
| eg_int_s | 6.4531031529331155 | 5.43888535430 | SCIP | 1.01 | 0.157 | |
| pricing050 (max) | −1813.8290784519730577 | −1514.52108768 | SCIP | 299 | 0.165 | |
| camshape800 | −4.27427414195420 | −5.14464335341 | BARON | 0.870 | 0.204 | |
| optcdeg2 | 293.87607509587509 | 200.133567480 | SCIP | 93.7 | 0.319 | |
| pindyck | −1170.4862854360886… | −1625.39840602 | SCIP | 455 | 0.389 | memory stop; tightened |
| waterno2_06 / 09 / 12 / 18 / 24 | Section 5.4 | | | | 0.49 / 0.73 / 0.78 / 0.81 / 0.84 | |
| eg_disc_s | 5.760539610694994 | 2.71549916578 | SCIP | 3.05 | 0.529 | |
| ex6_2_5 | −70.75207783344770759 | −128.325187347 | GUROBI | 57.6 | 0.814 | |
| dtoc5 | 5.38967211918114 | 0.000273134009568 | BARON | 5.39 | 1.00 | BARON disclaims globality |
| eg_disc2_s | 5.642100574331458 | −2.83013002499 | SCIP | 8.47 | 1.50 | |
| ex6_2_7, chain50–400, catmix100–800, kan_*, hvycrash | | | | | 3.1 to 1e9 | catmix: BARON values only, all disclaimed |
| ann_cumene_tanh | −3386.5403 | none finite | — | — | — | BARON and SCIP reject tanh |

### 5.4 waterno2 and ANN: certificate, strongest campaign dual and exact primal

The campaign report's reference column predates the exact primal track. Use the
exact values, which `P/primal/water-ann-kan/report.md` gives exactly and which
are rounded up here.

| instance | certificate | strongest campaign dual (solver) | campaign reference primal (stale; tolerance-feasible) | exactly feasible primal (rounded up) |
|---|---:|---:|---:|---:|
| waterno2_06 | 278.230573 | 142.831148612344 (GUROBI) | 282.8880374 | 282.8880374 (exact 282.888037386904807…) |
| waterno2_09 | 824.834692 | 220.683687371791 (GUROBI) | 914.011970350 | 914.011975238 |
| waterno2_12 | 2089.754565 | 454.55506441964 (GUROBI) | 2233.821335282 | 2233.821345609 |
| waterno2_18 | 4790.820715 | 891.934497969825 (SCIP) | 5023.982735143 | 5023.982760461 |
| waterno2_24 | 6576.151388 | 1074.43904635414 (SCIP) | 6963.795154460 | 6963.795180157 |
| ann_cumene_tanh | −3386.5403 | no finite bound | −3379.9823940717715481 | −3379.982394071771548 (enclosure; mpmath iv) |

### 5.5 Tolerance artifacts: points below exact optima

These are category A, primal-only, or claims without a dual.

| point | deficit below certificate | max violation | proof of non-feasibility | source |
|---|---|---|---|---|
| BARON camshape400 (campaign) | 8.15450068e-6 | 1.0e-10 (e400) | Lemma 1 | `point_checks.log` |
| BARON camshape800 | 9.365569719715e-2 | 3.3143e-7 (e2) | Lemma 1 (exact evaluation in `C/r2/ev.log`) | same |
| GUROBI camshape800 | 2.328447110410e-2 | 9.75e-7 (e58) | Lemma 1 | same |
| SCIP camshape100 | 1.519102e-7 | 7.717e-10 (e63) | Lemma 1 (`C/r2/ev.log`) | same |
| GUROBI powerflow0039p | 1.24788354e-3 | 6.81e-7 (e73) | Lemma 1 | same |
| GUROBI chain50 | 2.01996813e-7 | 6.69e-8 (e52) | Lemma 1 | same |
| BARON / SCIP pricing050 (max) | 1.0463230577e-6 / 4.500930577e-7 | 3.41e-7 / 1.22e-7 | Lemma 1 | same |
| BARON / GUROBI etamac | 3.34037807e-7 / 2.85107407e-7 | 6.80e-7 / 9.93e-7 | Lemma 1 | same |
| BARON pindyck | 4.368613836068e-7 | 3.49e-7 | Lemma 1 | same |
| SCIP kan_r3_h1_n4 / GUROBI kan_r5_h1_n3 (R) | 1.76772953844896e-3 / 1.3090062917e-2 | 9.62e-7 / 8.17e-7 | Lemma 1 for R | same |
| MINLPLib camshape400 p2 / camshape800 p2 | 8.15e-6 / 3.27e-5 | 3.0e-10 | Lemma 1 | `R/reviews/open-instances-verification/verification-report.md` |
| QPLIB `=best=` QPLIB_2703 / QPLIB_3177 | 8.154305e-6 / 3.272254e-5 below copy bounds | 3.0e-10 (QPLIB model) | Proposition 15 (new) | `C/r2/claims.log` |
| SCIP 9.2.1 QPLIB_2703 primal (Mittelmann) | 5.458883e-2 below copy bound | — | Proposition 15 | same |
| Karia et al. ConvexHull primal, kan_r5_h1_n5 | 6.45e-5 below min R | — | for R | network report §4.6 |
| S-B-MIQP (CAMINO), eg_disc2_s | 2.2e-7 below certified dual | — | Lemma 1, under A1/A2 | small report §11.1 |
| Kosolap (2019), ex6_2_5 | 0.2065 below certified dual | — | Lemma 1 | small report §12 |
| BARON optcdeg2 incumbent (Mittelmann 2026) 293.876075074557 | 2.1e-8 | — | Lemma 1 | control report |
| CUTEst LUKVLE10 SOLTN 352.237; LANCELOT/COPS lnts values; hvycrash p1/p2 | various | — | in their families | control and small reports |

**A positive counterpart, not flagged in the campaign report.** SCIP 10.0.3's
returned camshape800 point has objective −4.27427414195107, which is 3.1e-12
**above** the exact optimum. Its maximum row violation is 1.4e-14 (objective row)
and its maximum bound violation 2.4e-16 (`C/r2/ev.log`). SCIP found the
camshape800 optimum to about 12 digits on the primal side, while its dual bound
was −5.20.

### 5.6 Disagreements between documents found while compiling these tables

- **Summary line 314.** "because the chain amplifies violations up to about
  600-fold" is wrong as an explanation. 600 is the largest per-row weight
  U_max ≈ 1/sin θ for n = 800, the factor the verification report attached to the
  p1 deficits. The p2 deficits quoted in the same sentence imply 2.7e4 (n = 400)
  and 1.1e5 (n = 800) per unit of violation, and the worst case is about
  0.59 n² (Proposition 5). See issue S5.
- **Campaign references.** `P/solver-runs/references.csv` labels 13 references
  "numerical" (chain, dtoc5, lnts, lukvle10, powerflow) and uses
  tolerance-feasible water primals. Exactly feasible enclosures now exist. The
  report's "Remaining limits" sentence ("exact feasibility of the numerical
  reference primals … unresolved") is stale. See issue S6.
- **Dangling reference.** `P/solver-runs/report.md` (lines 402 and 513) and
  `README.md` cite `report.prev.md`, which was removed on 2026-10-04. See S7.
- **Network report.** `P/literature/network/report.md` gives "≤ 4.90%" for the
  waterno2_18 gap; the summary's "≤ 4.87%" is the checked display. Both are valid
  upper bounds.
- **Older SCIP scope.** `R/SYNTHESIS.md` (line 417) and
  `R/closing-research-results.md` (line 232) still describe the finding as "SCIP
  10.0.2 … (an invalid in-tree bound reduction; not reported upstream)". The
  publication track extends it to 10.0.3, 10.1.0 and master. Use
  `P/scip-bug/report.md`.

---

## 6. Verification record

| item | independent review | what was checked | verdict | remaining assumptions or limits |
|---|---|---|---|---|
| campaign setup | `P/reviews/solver-campaign-review-r1.md` | driver, accounting, admission, settings, model hashes | issues (2 major: lost optcdeg2/SCIP run; 0.72 CPU share), addressed by the final relaunch | the round-2 driver review (`solver-campaign-r2/`) stopped at a reading-state placeholder with no findings or verdict |
| campaign analysis | `P/reviews/solver-analysis-review-r1.md` (own extraction, comparison and point-check code) | all 129 rows from raw logs; validity rule; counts; references and listed values; 9 of 15 savepoints at 60 digits | **issues**: 2 major (six BARON disclaimers; overloaded first batch), 4 minor; all fixed by the author and checked by the parent orchestrator (Claude) | no second independent round after the fixes; GAMS ≡ OSIL is numerical only; shared machine |
| SCIP defect | `P/reviews/scip-bug-review-r1.md` (own CIP and GMS exact checkers; OSIL cross-check; own runs on all versions; toggles; trace and source reading; issue search) | witnesses; models equal OSIL rows; binary64 residuals; scan counts; traces; source pointers; fm336/tiny2 exact optima | **verified**, 7 minor issues, all addressed; later minor-fixes review r2 found one major overstatement (report line 173), fixed in round 3 with the reviewer's text | mechanism established for 15 instrumented runs; seed 11 untraced; `n` unexplained; upstream report drafted, **not filed** |
| CAMINO / Gurobi | lit-small reviews r1–r3 (r2 raised the CAMINO finding; r3: issues, no blocker or major) | data hashes; early-stop scan; interval feasibility | latest verdict: issues (minor), addressed; parent checked | assumptions 1–4 of Proposition 13 |
| KAN / SCIP 9.0.1 | lit-network reviews r1–r2 (own OSIL reader, permutation test, SCIP 10 fixed-input runs) | values at SCIP's points; model counts | **verified** (r2, 9 minor) | model identity; KAN R certificate |
| MINOTAUR/ANTIGONE on QPLIB | lit-control reviews r1–r2 | logs; QPLIB identity and rounding; values | **verified** (r2, 7 minor) | at that stage the copies were "strong evidence, not proof" |
| this dossier's new computations (Propositions 3 for copies, 5, 15; Observation 12) | none; two implementations by dossier authors (the earlier draft and this revision, both Claude) | — | own checks, not an independent review | needs an independent reviewer before the paper upgrades the QPLIB wording |

---

## 7. Relation to prior work

- **Wrong global claims by complete solvers.** Neumaier, Shcherbina, Huyer and
  Vinkó (2005; `neumaier2005-a-comparison-of-complete-global`) tabulate
  "wrongly claimed global/claimed global" per solver. They judge against best
  known points accepted by `solcheck` at a 1e-5 tolerance; in one BARON
  reliability table the entry is 19/209 ≈ 9%. Their reference is
  tolerance-based. Ours uses exact certificates, which separates tolerance
  artifacts (A) from invalid bounds (B). Several famous-looking "wrong optima"
  here are of type A.
- **Floating-point correctness in MIP, and certified reasoning.**
  - `neumaier2004-safe-bounds-in-linear-and`: wrong LP and MILP answers caused by
    rounding; safe bounds.
  - `hoen2025-analyzing-the-numerical-correctness-of`: retrospective exact checks
    of MIP branch-and-bound decisions.
  - Exact rational MIP: `eifler2023-a-computational-status-update-for` and
    `cook2011-an-exact-rational-mixed-integer`.
  - Certified constraint propagation with directed rounding:
    `borst2024-certified-constraint-propagation-and-dual`, for linear constraints
    in an exact MIP solver.
  - Proof logging: `doornmalen2023-a-proof-system-for-certifying` and
    `wood2026-satisfiability-modulo-theories-for-verifying`.
  - None treats nonlinear reverse propagation in a floating-point MINLP solver.
    The SCIP defect is an inconsistency between ε-tolerant acceptance and exact
    interval intersection.
- **Interval forward/backward propagation (FBBT).**
  `schichl2005-interval-analysis-on-directed-acyclic`,
  `vu2009-interval-propagation-and-search-on`,
  `domes2010-constraint-propagation-on-quadratic-constraints` (rigorously
  rounded propagation), and `vigerske2017-scip-global-optimization-of-mixed`
  (SCIP's expression-graph propagation). SCIP 10 context:
  `hojny2025-the-scip-optimization-suite-10`.
- **SCIP issue tracker.** On 2026-10-02 the track found no matching report. #162
  (multilinear; symmetry-related) and #190 (presolve with 1e-6 coefficients) are
  related but apparently have different causes. #22 (SOCP wrongly infeasible,
  SCIP 8) is the same kind of error with no common cause shown.
- **Gurobi.** `optimization2026-nonlinear-constraints-gurobi-optimizer-13`
  documents that small violations in a disaggregated reformulation can produce
  much larger violations in the original function. This is the same kind of
  amplification as our camshape and KAN artifacts. It also documents that static
  piecewise-linear approximation is used only when FuncNonlinear = 0, and is
  deprecated in 13.0. `optimization2026-fixed-issues-in-gurobi-optimizer` lists
  the 13.0.x MINLP-presolve wrong-answer fixes. Neither explains the CAMINO
  values.
- **BARON.** `firm2026-baron-release-notes-26-5`: the 2026.5.28 entry reads "Serious
  fix in initialization that led to BARON ignoring variable bounds, although
  rarely affecting problems." Our runs used 26.5.27 (issue S8). Our BARON points
  show bound violations of at most about 1e-10, so there is no sign of ignored
  bounds.
- **Benchmark practice.**
  - MINLPLib: `bussieck2003-minlpliba-collection-of-test-models`,
    `vigerske2026-minlplib-a-library-of-mixed`, and the S-mark rule in
    `vigerske2026-minlplib-documentation-database-snapshot-2026`.
  - PAVER 2.0 and its Examiner, which checks returned points:
    `bussieck2014-paver-2-0-an-open`.
  - QPLIB: `furini2018-qplib-a-library-of-quadratic`.
  - Mittelmann's QPLIB logs are saved under
    `P/literature/control/sources/mittelmann_cnconv/`.
- **Instance-specific sources** are in the three literature reports:
  - CAMINO: `ghezzi2024-camino-a-mixed-integer-nonlinear`, data
    `ghezzi2026-camino-benchmark-results-for-nonconvex`; read as
    arXiv:2404.11786v2. The MPC version and its correction were not read.
  - KAN: `karia2025-kolmogorov-arnold-networks-kans-as`,
    `karia2025-karia-et-al-zenodo-default`.
  - ANTIGONE: `misener2014-antigone-algorithms-for-continuous-integer`.
  - eg_int_s floating-point closure by SCIP 8.1:
    `go2026-parabolic-approximation-relaxation-for-minlp`, plus the publisher
    correction `go2026-publisher-correction-parabolic-approximation-relaxation`,
    which is unread.
  - Octeract on camshape100: Bestuzheva et al., arXiv:2301.00587, App. B.

---

## 8. Critical examination

### 8.1 What I re-derived and re-ran

All runs used copies in `/tmp/solv2/`, one process at a time. No solver was run,
nothing under `R/` or `literature/` was edited or executed in place, and nothing
was committed.

1. **Campaign counts** (`recount.py`, `margins.py`). These reproduce: 129 rows on
   43 instances; finite duals 35/36/38 = 109 (91 OSIL + 18 R); 126 valid; 2
   claims; 6 BARON warnings; 6 SCIP tightened rows; 10 first-batch rows;
   minimum margin 5.2581469e-7; no dual at or beyond a certificate; no dual
   beyond a reference primal; 5 listed-dual improvements, with the values given
   above. **All agree.**
2. **SCIP witnesses** (`cipchk.py`, my own CIP parser). 8/8 are exactly feasible
   with the same exact objectives; the mutation tests are rejected. **Agree.**
3. **Lemma 8 and the tiny2 trace intervals**, recomputed. **Agree.** The fm336
   binary64 bound 2.247 and tiny2's 9.6e-7 coincidence are new here.
4. **fm336 and tiny2 optima** re-proved by hand. **Agree** with the reviewer.
5. **Comparison lemma and Propositions 3 and 5**, re-derived. Implemented
   independently of the earlier draft (`gparse.py`, `cambd.py`, `tol.py`).
   - The four MINLPLib optima are reproduced to all printed digits.
   - The QPLIB copy bounds and D(ε) agree with the earlier draft to all printed
     digits.
6. **Savepoints** (`ev.py`): exact objectives and residuals of BARON
   camshape100/200/800 and SCIP camshape100/800 from the binary64 GDX levels.
   They agree with `point_checks.log`. The SCIP camshape800 observation is new.
7. **Pattern scan** over 1632 OSIL files (`pattern_scan.py`, 128 s).
   Observation 12 is new.
8. **Margins.** CAMINO, KAN, MINOTAUR, ANTIGONE, QPLIB `=best=`, BARON relative
   and GUROBI optcdeg2 margins were recomputed in `fractions` (`claims.log`).
9. **Read-only checks.** CAMINO CSV rows and `using_amplpy.py` options; the
   MINOTAUR/ANTIGONE logs and their input files; BARON's camshape100 log and
   trace; `scan_summary.csv` per version; the rbb log for Proposition 11;
   `checksol_witness.log`; the MINLPLib S-mark definition; the waterno2 listed
   bounds in `pages.json`; Gurobi 13.0.x and BARON 26.5 release notes.

### 8.2 Issues and proposed resolutions

**S1 (major; framing and novelty; no new computation).** "Zero closures" and
"BARON's claims contradict the proved optimum intervals" are true only under
exact semantics.

- Under the community convention, BARON 26.5.27 effectively closes camshape100
  (0.45 s) and camshape200 (23 s). Its duals are **valid** and within 1.23e-7 and
  4.80e-7 relative of the exact optima, well inside MINLPLib's 1e-6 relative
  gap. Only the claimed *value* (= the dual) lies below v*. The returned points
  are 1e-10-feasible, with 87% of the rigorous worst-case deficit.
- For camshape200 this is a large improvement over the listed −4.63229055
  (8.3% gap).
- The control literature row for camshape200 ("partly known: an unverifiable
  floating-point claim", Octeract on the rounded copy) therefore understates
  current floating-point solvability. Our own campaign shows a current solver
  closing it to tolerance in 23 s.

*Resolution.*

- Present the two BARON runs as category-A tolerance-level closures with valid
  duals, and credit them.
- Keep "no certificate-consistent closure" only as an exact-semantics statement.
- Update the camshape100/200 prior-work wording: "already solved globally in
  floating point (Octeract; BARON 26.5.27 in our campaign); the exact optimum is
  new".

**S2 (minor; SCIP semantics wording).** The summary says that reverse propagation
"cuts off a feasible point". This invites the reply that under binary64 data the
witnesses are infeasible.

*Resolution.*

- Say "a point that is feasible for the model as written (exact decimal data) and
  that SCIP's own feasibility check accepts".
- Lead with Proposition 9(b): the claims exceed the value of a point that SCIP
  itself accepts.
- Use fm336 as the example that is wrong in every reading.
- Note that tiny2's claim matches the zero-tolerance binary64 optimum within
  9.6e-7.

**S3 (minor; improvement that needs review).** Propositions 3 (copies), 5 and 15
upgrade the QPLIB statements from "strong evidence" to proofs:

- MINOTAUR camshape800 and ANTIGONE camshape100;
- SCIP 9.2.1's QPLIB_2703 incumbent;
- the new QPLIB `=best=` finding.

The two implementations share an author and a model of the math.

*Resolution.*

- An independent reviewer re-derives Lemma 2 and the ε-relaxation, and audits
  `cambd.py` and `gparse.py` or writes a third implementation. Cost: about 1 hour
  of review and under 20 s of computation.
- State MINOTAUR's `.nl` input as an assumption. Optionally fetch QPLIB_3177.nl
  from QPLIB and compare its constants (minutes, network access).
- Until then, use "contradicted for the MINLPLib model; for the rounded QPLIB
  copy, a direct bound computed by us".

**S4 (minor; new finding that the paper may report).** QPLIB's best values for
QPLIB_2703 (−4.275658867) and QPLIB_3177 (−4.274219874) lie 8.15e-6 and 3.27e-5
below rigorous bounds of those instances. They mirror MINLPLib's camshape400/800
p2 tolerance artifacts.

*Resolution.* Report with S3's review. Consider notifying the QPLIB maintainers;
that is a user decision.

**S5 (minor; wrong explanatory sentence in the authoritative summary).** "The
chain amplifies violations up to about 600-fold" (summary, line 314) does not
explain 8e-6 and 3e-5 deficits from 3e-10 violations. Those imply
2.7e4–1.1e5-fold amplification.

*Resolution.* Replace with: "each row violation enters with a Chebyshev weight
of up to about 600 (n = 800), and these weights add up along the chain, so
violations of 3e-10 can move the objective by up to 2.8e-5 (n = 400) or 1.1e-4
(n = 800) (Proposition 5)."

**S6 (minor; stale campaign references).** See Section 5.6. No comparison
changes, because all flags compare with certificates.

*Resolution.*

- Use the summary's exactly feasible primal displays in the paper's tables
  (Section 5.4).
- Optionally regenerate `references.*` in a disposable copy (seconds, no solver).
- Delete or update the "Remaining limits" sentence.

**S7 (minor; dangling path).** `report.prev.md` is cited but deleted.

*Resolution.* Cite the git commit that contains it (it was a byte-identical
backup of the HEAD report), or delete the references.

**S8 (minor; versions).**

- BARON 26.5.28 (fix: "BARON ignoring variable bounds" in initialization) and
  Gurobi 13.0.3 (further wrong-answer fixes) were released before the campaign.
- The campaign used the versions bundled with GAMS 54.3.1.
- No BARON point checked shows a bound violation above about 1e-10, so nothing
  indicates that the 26.5.27 issue affected these runs.

*Resolution.*

- Write "BARON 26.5.27 and GUROBI 13.0.2 as bundled with GAMS 54.3.1" and do not
  call them the latest versions.
- Optionally rerun the two camshape BARON runs with 26.5.28. Cost: under one
  minute of solver time, if the user authorizes a solver run and the version is
  available.

**S9 (minor; assumption to state).** The MINOTAUR optcdeg2 refutation assumes
that `QPLIB_8803.nl` encodes the MINLPLib model, and that presolve imposed no
default bounds that cut off all feasible points.

*Resolution.* State both. Optionally evaluate the optcdeg2 point's largest
absolute coordinate against MINOTAUR's documented defaults (minutes, if the
default values can be confirmed from source).

**S10 (minor; CAMINO wording).**

*Resolution.*

- Use "the best bound recorded for Gurobi 13.0.0 in the public CAMINO data is
  invalid", not "Gurobi has a bug".
- Keep assumptions 1–4 and "the termination status is not recorded".
- Mention the 13.0.x MINLP-presolve fixes only as context.
- Do not attribute the error to Gurobi rather than to the AMPL interface or the
  pipeline.

**S11 (minor; KAN wording).**

*Resolution.*

- Say "below the certified minimum of the network relaxation R of the same
  networks", and say that the solver's duals are valid (category A).
- State that model identity rests on counts plus the reviewer's input-order
  permutation test.

**S12 (minor; process).** After the author's fixes there was no second
independent solver-analysis review, and the campaign's round-2 driver review
never finished. The parent's checks are not independent.

*Resolution.* A short independent check of the final CSV, table and flags. About
1–2 hours, no solver.

**S13 (minor; process; user decision).** The upstream SCIP report is drafted and
not filed. Other parties have not been told either:

- MINLPLib (waterno2 exposure; QPLIB/MINLPLib tolerance points);
- Mittelmann/MINOTAUR (optcdeg2 infeasibility; camshape800 root closure);
- the CAMINO authors;
- BARON (optional).

*Resolution.* If the user agrees, file before submission so the paper can cite
the issue. Never write "reported" otherwise.

**S14 (minor; mechanism scope).** Traces cover only the 15 instrumented runs.

*Resolution.*

- Keep the report's scope.
- Optional: a source-level experiment on master (ε-tolerant intersection in
  `SCIPintervalPropagateWeightedSum`, or ε-relaxation of fixed domains in mode
  `r`), then rerun the 122-case scan. That would make the cause a tested one.
  Cost: a few hours of build and scan on 2 cores. This is the developers' job
  once the report is filed.

**S15 (minor; optional computation).** The low pair2236 claims (55.689773,
55.689858) are neither refuted nor confirmed.

*Resolution.* One rbb run on the pair box with target 55.6898 would decide
whether the optimum exceeds them. Typical pair runs took at most 28 s; cost:
minutes. Not needed for any claim.

**S16 (minor; evidential weight of flags).** Four primal flags have margins of
3.3e-12 or less. Lemma 1 needs an accurately evaluated objective, and 30 flags
rest on printed solver objectives without a checked vector.

*Resolution.* In the paper:

- count as proved only flags whose vector was evaluated exactly or at 50 digits,
  or whose printed margin exceeds the printing uncertainty;
- call the rest "certificate-inconsistent as printed".

**S17 (minor; framing).** The certificate-versus-solver comparison sets
instance-specific, human-designed certificates against general-purpose one-hour
runs.

*Resolution.*

- Present the campaign as a status check of current solvers on these stored
  models, not a method race.
- Disclose certificate effort (Readiness timing table).
- Keep "no speed ranking".

**S18 (minor; scope of the SCIP exposure; resolved here by computation).** The
summary says that whether listed SCIP bounds on instances with this data pattern
are affected was not examined. Observation 12 bounds the syntactic exposure to
the nine waterno2 instances. Listed SCIP duals that close or nearly close waterno2_01–04
are the only listed bounds in that set that could matter.

*Resolution.* Add one sentence with the scan's caveats. Optional: run SCIP 10.1.0
on waterno2_03 and waterno2_04 with `varboundrelax = b` and compare with the
default run (about 2 × 1 h of solver time; a user decision). The result would be
evidence, not proof.

**S19 (minor; footnote).** The campaign solved the `.gms` files; certificates are
for OSIL. Equivalence is numerical. The OSIL coefficients of catmix differ from
the `.gms` text by at most 2.4e-16 relative.

*Resolution.* Add a footnote. The smallest affected margin, BARON's catmix100
primal flag of 1.48e-9, is far above that level.

**S20 (minor; outdated cross-document statements).** Two kinds of outdated
statements remain (Section 5.6):

- `R/SYNTHESIS.md` line 417 and `R/closing-research-results.md` line 232
  describe the SCIP finding as "SCIP 10.0.2 … not reported upstream". The
  publication track covers 10.0.2, 10.0.3, 10.1.0 and master.
- The network literature report shows "≤ 4.90%" for waterno2_18, while the
  summary shows "≤ 4.87%".

*Resolution.* The paper should cite `P/scip-bug/report.md` and the summary's
displays. These files lie under `R/` and are not edited here.

### 8.3 Does anything invalidate a claimed result?

**No.**

- Every number in this family that I could recompute agrees.
- The new computations strengthen the QPLIB claims and quantify the BARON,
  ANTIGONE and MINOTAUR claims as tolerance artifacts.
- The most consequential correction is S1. It changes how the paper must
  describe BARON's camshape results and the prior status of camshape200. It
  changes no certificate.

---

## 9. What the paper may claim, and must not claim

**May claim (suggested wording).**

- "We ran BARON 26.5.27, GUROBI 13.0.2 and SCIP 10.0.3 (as bundled with GAMS
  54.3.1), each for one hour on one thread with gap requests of 1e-9, on all 43
  models. Of the 109 finite final dual bounds, every one is weaker than our
  certified bound. The closest are BARON's bounds on camshape100 and camshape200,
  within 1.2e-7 and 4.8e-7 (relative) of the exact optima."
- "BARON reported optimality on camshape100 and camshape200. Its dual bounds are
  valid and close the gap to within MINLPLib's 1e-6 tolerance. Under exact
  feasibility, however, the reported optimal values are 5.3e-7 and 2.1e-6 below
  the exact optima, and the returned points violate constraints by about 1e-10.
  Such points can lie up to 6.0e-7 and 2.4e-6 below the optimum (Proposition 5)."
- "SCIP 10.0.2, 10.0.3, 10.1.0 and the development version of 2 October 2026
  report wrong optimal values on single-period and cell-pair subproblems of
  waterno2_06, depending on the random seed. The errors reach 3.8 on periods and
  9.4 (about 17%) on a cell pair. Exactly feasible rational points refute every
  such claim, and SCIP's own feasibility check accepts these points. The same
  happens through PySCIPOpt and GAMS. A 15-variable model reproduces the error
  with default settings in every version and interface tested, and its claims are
  wrong under every reading of the data. In instrumented runs, nonlinear reverse
  propagation declares a node infeasible because fl(0.7)³ < fl(0.343) in binary64,
  although 0.7³ = 0.343 in decimal."
- "Among all MINLPLib instances, rows y = x² or y = x³ whose decimal bounds agree
  at a bound but disagree in binary64 occur only in the nine waterno2 instances
  (syntactic scan)."
- "To the best of our knowledge this defect had not been reported (SCIP issue
  tracker, searched 2 October 2026)." Add "we reported it" only if that becomes
  true.
- "In the public CAMINO benchmark data, the best bounds recorded for Gurobi 13.0.0
  on eg_disc2_s, eg_disc_s and eg_int_s exceed the objective values of points we
  prove feasible for the same `.mod` models, by 4.3%, 7.5% and 81%. The data do
  not record the termination status, and the cause is unknown."
- "The SCIP 9.0.1 optimal values published for kan_r3_h1_n4 and kan_r3_h1_n5 lie
  below the certified minimum of the network relaxation of the same networks.
  They are artifacts of the feasibility tolerance, amplified by an output scale
  of about 970."
- After S3's review: "No exactly feasible point of the rounded QPLIB copies
  attains MINOTAUR's camshape800 optimum (−4.2774) or ANTIGONE's camshape100
  global minimum (−4.284302); rigorous bounds for the copies are
  −4.274187151471744 and −4.284146267804612. QPLIB's own best values for
  QPLIB_2703 and QPLIB_3177 also lie below rigorous bounds, by 8.2e-6 and
  3.3e-5." Before the review, say "contradicted for the MINLPLib model; for the
  copies by a direct bound we computed".
- "MINOTAUR 0.4.1's infeasibility report for QPLIB_8803 (textually identical to
  MINLPLib optcdeg2) is false, assuming the `.nl` file encodes the same model."
- "Rounding camshape's constants at the 1e-10 level, as in QPLIB, raises the
  optimum by at least 8.5e-7 (n = 100) to 8.7e-5 (n = 800)."

**Must not claim.**

- That BARON, Gurobi, MINOTAUR or ANTIGONE have bugs. Only the SCIP finding has
  a traced mechanism, and even that is observed in instrumented runs.
- That BARON's camshape results are wrong "within BARON's tolerances", or that
  BARON failed on camshape100/200 (S1).
- That the SCIP mechanism explains every wrong SCIP run, or that any
  MINLPLib-listed SCIP bound is wrong. The listed waterno2 SCIP bounds are
  either far below our certificates or uncontradicted.
- That SCIP "cuts off feasible points" without saying feasible in what sense
  (S2).
- That Gurobi caused the CAMINO values, or that Gurobi "terminated optimal".
- Any speed ranking or isolated-core timing, or that the instances "remain open
  for solvers" beyond these runs, settings and budget. Disclose the ten
  first-batch runs and the three memory stops.
- That the 50-digit residuals are interval proofs, or that unchecked flagged
  points are proved infeasible beyond Lemma 1 with accurate objectives.
- That the KAN OSIL models have feasible points or optima.
- "Upstream report filed" or "confirmed by developers", unless true.
- That the campaign used the latest BARON or Gurobi patch release.

---

## 10. Candidate figures and tables

1. **Table (main text): campaign summary per solver** (Proposition 1). Add
   footnotes on BARON disclaimers, SCIP tightened models, memory stops, the first
   batch, and the GAMS/OSIL distinction.
2. **Figure: certificate − strongest solver dual, relative, per instance** (log
   scale, 42 instances, Section 5.3 data). Use separate markers for "no finite
   bound", "BARON-disclaimed only" and "SCIP tightened model". It shows the range
   from 1.2e-7 (camshape100) to 1e9 (hvycrash) at a glance.
3. **Figure: tolerance artifacts on camshape.** A log–log plot of objective
   deficit against maximum violation for the campaign points, MINLPLib p2,
   QPLIB `=best=` 2703/3177 and the exploratory SCIP incumbent. Overlay the
   rigorous curves D_n(ε) for n = 100 … 800 (Proposition 5). The BARON points sit
   at 87% of the curve.
4. **Table: contradicted claims** (Section 5.1), split into category A (tolerance
   artifacts with valid duals) and category B (invalid bounds or infeasibility
   claims).
5. **Box: the SCIP defect.** The fm336 model, the three propagation steps of
   tiny2 with binary64 intervals, and Lemma 8's residual table. Add
   Proposition 9's three readings in one line each.
6. **Table: SCIP wrong runs by version and model** (`P/scip-bug/report.md` §3.2)
   and the `varboundrelax = b` experiment (78/122 → 0/122).
7. **Small table: QPLIB copy bounds against MINLPLib optima** (Proposition 3
   table), showing the shift of at least 8.5e-7 to 8.7e-5 caused by 1e-10 data
   rounding.

---

## Appendix: commands run for this dossier

From `/tmp/solv2/` copies, one process at a time:

- `cp P/solver-runs/{results_table.csv,references.csv,results.csv} camp/`
  - `python3 recount.py > recount.log`
  - `python3 margins.py > margins.log`
- `cp` of the eight CIP models and JSON witnesses from `P/scip-bug/` to `scip/`
  - `python3 cipchk.py > cipchk.log` (8/8 feasible; 3/3 mutations rejected)
- `cp P/solver-runs/gms/camshape*.gms P/literature/control/sources/qplib/camshape_copies/QPLIB_*.gms cam/`
  - `python3 cambd.py <8 files> > cambd.log` (3.2 s)
  - `python3 tol.py > tol.log` (18 s)
  - an inline `fractions` script → `claims.log`
- `cp` of five savepoints (`m_p.gdx` of camshape100/200/800 BARON and camshape100/800 SCIP) from `P/solver-runs/runs/` to `gdx/`
  - `python3 ev.py <model> <gdx> <cert>` → `ev.log` (uses `gdxdump dFormat=hexponential`)
- Inline `python3` (`fractions`, `math.nextafter`): Lemma 8, the tiny2 intervals,
  the fm336 binary64 bound and tiny2's binary64 optimum.
- `python3 scan2.py > scan2.log` over `~/.cache/minlplib/minlplib/osil/*.osil`
  (read only; 128 s). A first version missed quadratic-coefficient rows and was
  extended. Its first invocation unintentionally scanned all files rather than
  one (111 s); no harm.
- Read-only inspection with `cat`, `sed`, `grep`, `head`: logs, reports,
  reviews, CSV and literature files named above.

Input hashes (sha256, first 16 hex digits):

- camshape100/200/400/800.gms: 7f9ef5412da5bb12 / fbf6546260555d96 /
  650e42f387a8544f / 807666900ba72dcb
- QPLIB_2738/2480/2703/3177.gms: b30f282782e78cb9 / 2ca3dde537e2c367 /
  0ac46c15b8c8847a / 4d0e595fdd62b995

Scripts and logs are saved in `C/r2/`. Its README gives the copy-then-run
procedure. The earlier draft's checks remain in `C/`.
