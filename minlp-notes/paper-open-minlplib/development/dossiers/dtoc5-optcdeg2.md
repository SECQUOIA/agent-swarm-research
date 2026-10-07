# Dossier: dtoc5 and optcdeg2 (calibration certificates for transcribed optimal-control QCQPs)

Family key: `dtoc5-optcdeg2`. Written 2026-10-04 for the MPC paper. `R/` means
`research-20260929/`. Checks run for this dossier are in
`paper-open-minlplib/development/dossiers/checks/dtoc5-optcdeg2/` (scripts, logs, README).
Nothing under `R/` or `literature/` was edited; no scientific script was run in the main tree.

**Bottom line.** Both results stand. I found nothing that invalidates a claimed bound,
primal point or gap. I re-derived both proofs and re-checked the numbers. Three of my
checks strengthen the record:

1. **dtoc5.** I computed a new dual certificate in exact rational arithmetic, with no
   floating point and no mpmath. It uses multipliers read from the committed exactly
   feasible point and takes 2.6 s. It brackets the optimum to **7.3e-43**:
   f* ∈ [5.38967211918114046742396649913627186883131268,
   5.38967211918114046742396649913627186883131341]. It also fixes a provenance gap:
   the summary's displayed dual, 5.38967211918114, lies *above* the author's stored
   certificate (5.3896721191811325). That display currently rests on the verifier's
   multipliers, which were regenerated and never saved.
2. **optcdeg2.** I re-ran unmodified copies of the reviewer's exact-rational pipeline
   (state enclosure plus calibration bound). Its outputs are bit-identical to the saved
   ones: LB = 293.87607509587509237940… I also proved an exactly feasible point
   **without mpmath**, using integer interval arithmetic. Its objective lies in
   293.876075095875093277214211424708015934099559491 ± 5e-64, which agrees with the
   reviewer's mpmath result.
3. Both GAMS files match the stated models exactly, checked as exact text. Their hashes
   match the MINLPLib files recorded in the status refresh.

---

## 1. Instances and models

### 1.1 dtoc5

**Source and meaning.** This is a discrete-time optimal control problem: problem 5 of
Coleman and Liao (Comput. Optim. Appl. 4 (1995) 47–66). It has a scalar state y, a
scalar control u, and Euler-discretized dynamics ẏ = y² − u. The cost is a quadratic
regulator on the state and control.

- Provenance chain: MINLPLib dtoc5 ← QPLIB_8585 (donor Gould) ← CUTEst DTOC5 ←
  Coleman–Liao problem 5.
- The MINLPLib `.gms` is textually identical to QPLIB_8585.gms
  (`R/publication/literature/control/checks/qplib_dtoc5_optcdeg2_identity.log`).
- It was added to MINLPLib on 18 Aug 2018. Type QCQP, nonconvex, all variables
  continuous.

**Model (OSIL = .gms; exact decimals).** Let T = 49 999 and h = 2e-5 = 1/50 000.

- Variables: u_t = x_{t+2} for t = 0..T−1, and y_t = x_{50001+t} for t = 0..T.
  That is 99 999 variables; the `.gms` adds `objvar`, for 100 000.
- y_0 = 1 is fixed. All other variables are free.

$$
\min\; h\sum_{t=0}^{T-1}\left(u_t^2+y_t^2\right)\quad\text{s.t.}\quad
-h\,u_t + y_t - y_{t+1} + 4h\,y_t^2 = 0,\qquad t=0,\dots,T-1 .
$$

- y_T does not appear in the objective. y_0² contributes the constant h.
- OSIL coefficients: 2e-5 (objective; u in the rows) and 8e-5 = 4h (y_t² in the rows).
- Structure that matters: each u_t appears linearly in exactly one row, with nonzero
  coefficient −h, so the rows can be eliminated. The problem is a chain in y with
  one-dimensional separators. No variable has finite bounds. This is what defeats
  termwise relaxations: listed solver bounds are of order 1e-3, against an optimum of
  5.39.
- A spot check of the optimizer: û_t ∈ [−2e-26, 8.0572], ŷ ∈ [0.3924, 1], ŷ_T = 0.7304.
  The control vanishes at the end because y_T is free and does not enter the cost.

**Provenance issue (factor 4).**

- Coleman–Liao, DTOC5.SIF and Benson's AMPL file all use the row y_{t+1} = y_t + h(y_t² − u_t).
- QPLIB/MINLPLib use 4h·y_t² (QPLIB Hessian entry 0.00016 = 4h under the ½xᵀQx convention).
- The objective agrees with the sources.
- Floating-point confirmation (`R/publication/literature/control/checks/dtoc5_coef_check.log`):
  - the h variant reproduces Coleman–Liao Table 3;
  - the 4h variant at N = 50 000 gives 5.389672119181 (the MINLPLib value);
  - the h variant at N = 50 000 gives about 1.53515.
- Where the factor 4 entered is undetermined.
- **Our certificate concerns the MINLPLib/QPLIB variant only.** The CUTEst/Coleman–Liao
  values belong to a different model.
- PrincetonLib (2006) has a smaller dtoc5 (9 999 variables); it is a different model,
  not a predecessor (`R/publication/minlplib-status/data/tables.md`).

**OSIL vs GAMS.**

- The status refresh lists dtoc5 among the 64 instances whose OSIL and `.gms` define
  the same model.
- I checked the `.gms` text exactly (`checks/dtoc5-optcdeg2/dtoc5_checks.py`, part A):
  every row is `8e-5*sqr(y_t) + y_t - 2E-5*u_t - y_{t+1} =E= 0`, every objective
  coefficient is 2e-5 on exactly {u_0..u_{T−1}, y_0..y_{T−1}}, and the only bound
  statement is `x50001.fx = 1`.
- OSIL attribute census: 99 998 `coef="2e-5"` objective terms, 49 999 `coef="8e-5"`,
  49 999 linear `-2e-5`; only x50001 has bounds [1, 1].
- Hashes: `.gms` sha256 4fc80f6b…, OSIL ac7b2d94…. Both match
  `R/publication/minlplib-status/data/part_a.json`.

### 1.2 optcdeg2

**Source and meaning.** Optimal control of a forced oscillator with a quadratic velocity
term, over horizon 20 (N = 50 000 Euler steps, h = 4e-4).

- Continuous model: ẏ = v, v̇ = u − 0.02y − 0.2v².
- Cost: ½∫y² dt.
- Data: |u| ≤ 0.2, v ≥ −1, y(0) = 10, v(0) = v(T) = 0.
- Provenance chain: MINLPLib optcdeg2 ← QPLIB_8803 (Gould) ← CUTEst OPTCDEG2 ←
  Murtagh–Saunders (1982) Ex. 5.11 (per OPTCNTRL.SIF). Murtagh–Saunders itself was not read.
- Added 18 Aug 2018. Type QCQP, nonconvex.
- The `.gms` is identical to QPLIB_8803.gms up to the solve statement. QPLIB adds one
  redundant "Positive Variables" line for two variables that both files fix at 0.

Remark for the text: −0.2v² is not a symmetric damping. It decelerates only when v > 0
and accelerates the motion when v < 0. On the optimal trajectory v ∈ [−0.8315, 0.198]
and is mostly negative. Call it a "quadratic velocity term" or quote CUTEst's
"damping" with care.

**Model (OSIL = .gms; exact decimals).** Let N = 50 000, h = 4e-4 = 1/2500,
a = 8e-6 = 0.02h, b = 8e-5 = 0.2h and w = 2e-4 = h/2.

- Variables:
  - u_t = x_{2+t} for t ≤ N−2, and u_{N−1} = x50002;
  - y_t = x_{50003+t} for t = 0..N;
  - v_t = x_{100004+t} for t = 0..N−1, and v_N = x50001.
  - In total 150 002 variables and 100 000 rows.

$$
\min\; \tfrac h2\sum_{t=0}^{N} y_t^2\quad\text{s.t.}\quad
y_{t+1}=y_t+h v_t,\qquad v_{t+1}=v_t+h u_t-a y_t-b v_t^2\quad(t=0..N-1),
$$

with u_t ∈ [−1/5, 1/5], v_t ≥ −1 (1 ≤ t ≤ N−1), y_0 = 10, v_0 = v_N = 0, and y_1..y_N
free. The OSIL bound strings are `-.2`/`.2`, so the control bounds are exactly ±1/5.

- Structure that matters:
  - The state (y_t, v_t) is the two-dimensional separator.
  - The objective is convex. The only nonconvexity is the v_t² term in the velocity rows.
  - y is unbounded.
  - The optimal control is bang-bang: −1/5 for t < 3091, +1/5 for 3092 ≤ t < 47290 and
    −1/5 for t > 47290, with fractional controls at stages 3091 and 47290.
  - The switch times are 3091h ≈ 1.2364 and 47290h ≈ 18.916.
- Spot check of the trajectory: y_N ≈ −0.964; min y ≈ −1.161; min v = −0.8315 at
  t ≈ 26 559 (so the bound v ≥ −1 is inactive); max v ≈ 0.198.

**Provenance issue (factor 4).**

- CUTEst OPTCDEG2.SIF, Benson's AMPL file and OPTCNTRL.SIF use the damping coefficient
  0.05; MINLPLib/QPLIB use 0.2.
- IPOPT confirmation (`checks/optcdeg2_coef_check.log` in the control literature report):
  - damping 0.05 reproduces the SIF SOLTN values;
  - damping 0.2 at T = 50 000 gives 293.8762;
  - damping 0.05 at T = 50 000 gives 227.044.
- The certificate concerns the MINLPLib/QPLIB variant only.
- PrincetonLib's optcdeg2 (1 202 variables) is a different model.

**OSIL vs GAMS.** My exact text check (`optcdeg2_gms_check.py`) confirms:

- every Y-row and V-row;
- the objective 2e-4·Σ_{t=0}^{N} y_t²;
- u ∈ [−0.2, 0.2] on all 50 000 controls;
- v_1..v_{N−1} ≥ −1;
- y_0 = 10 and v_0 = v_N = 0;
- no sign declarations.

The OSIL census agrees (one `mult="2"` element for −4e-4). Hashes: `.gms` 42171d55…,
OSIL 6a9bcd91…, matching the status refresh. The reviewer's OSIL reader
(`R/reviews/bangbang-verification/v_model.py`) independently found the same layout.

---

## 2. Listed MINLPLib status (fetched 2026-09-29; unchanged at the 2026-10-02 refresh)

Source: `R/publication/minlplib-status/data/part_a.json`. Both instances are listed as
open (`solved: false`).

| instance | listing (3-solver metadata) dual / primal | per-solver duals on the page | listed points |
|---|---|---|---|
| dtoc5 | 0.0006 / 5.3897 | **BARON 0.00243096** (15 Feb 2022, best); COUENNE 0.00237817 (16 May 2020); SCIP 0.00062719 (31 Jul 2025); GUROBI −175.1969035 (07 Aug 2025) | p1 5.38967212 (infeas. 6e-17) |
| optcdeg2 | 4.3996 / 293.8761 | **GUROBI 292.41713458** (11 Apr 2023, best); SCIP 264.4199628 (16 May 2020); BARON 4.39955186 (15 Feb 2022); COUENNE 0.41999966 (16 May 2020) | p1 293.8760751 (infeas. 2e-15); p2 292.4171346 (infeas. **1e-6**, "other", added 11 Apr 2023) |

GUROBI's optcdeg2 dual equals the objective of p2. The first-wave verifier found that p2
violates 46 687 rows by more than 1e-8, with a maximum of 9.97e-7. The bound is
therefore a valid but weak dual bound. The matching "optimal" value is a
tolerance-level artifact under exact feasibility.

---

## 3. The certificates

Both certificates are instances of one scheme: a discrete verification function, which
Krotov calls a sufficient-condition function and the project notes call a calibration.

- Given functions S_t on the state space and any sets that contain the states of every
  feasible point, define the stage residual ρ_t = L_t + S_{t+1}∘f_t − S_t.
- The telescoping identity then gives
  f(x) = S_0(x_0) + Σ_t ρ_t(x_t,u_t) + (Φ − S_N)(x_N) along every feasible trajectory.
- Bounding each term below by its infimum gives a lower bound on f*.
- Affine S_t gives exactly the Lagrangian dual function with the dynamics rows
  dualized (`R/theory-calibration/scouting.md`, Theorem 3.1).
- **dtoc5 uses an affine S, the Lagrangian. optcdeg2 needs a quadratic S.**

### 3.1 dtoc5: zero Lagrangian duality gap at the costate

**Idea in plain words.** Dualize every row with its discrete costate. For dtoc5 the
Lagrangian is then a sum of one-variable convex quadratics: the costate makes the
nonconvex term 4h·y² harmless because the multipliers are ≤ 0. So the Lagrangian's
minimum equals the objective at the KKT point. This is the classical sufficiency
argument for a KKT point whose Lagrangian is convex at its multipliers: Mangasarian's
condition in discrete time, or the QCQP condition "KKT plus a positive semidefinite
Hessian of the Lagrangian implies global optimality". No variable bounds and no
branching are needed.

**Proposition 1 (dtoc5 dual function).** Let λ ∈ ℝ^T satisfy λ_{T−1} = 0 and
λ_t < 1/4 for t = 1..T−1. Define

$$
d(\lambda)= h(1-4\lambda_0)-\lambda_0-\frac h4\sum_{t=0}^{T-1}\lambda_t^2-\sum_{t=1}^{T-1}\frac{(\lambda_{t-1}-\lambda_t)^2}{4h(1-4\lambda_t)} .
$$

Then every exactly feasible point x satisfies

$$
f(x)=d(\lambda)+h\sum_{t=0}^{T-1}\Big(u_t+\frac{\lambda_t}{2}\Big)^2+h\sum_{t=1}^{T-1}(1-4\lambda_t)\big(y_t-\hat y_t(\lambda)\big)^2\ \ge\ d(\lambda),
\qquad \hat y_t(\lambda)=\frac{\lambda_t-\lambda_{t-1}}{2h(1-4\lambda_t)} .
$$

*Proof.* Write the rows as c_t(x) = y_{t+1} − y_t − 4h y_t² + h u_t = 0. For feasible x,
f(x) = f(x) + Σ_t λ_t c_t(x). Collect terms by variable:

- u_t: h u_t² + h λ_t u_t = h(u_t + λ_t/2)² − hλ_t²/4.
- y_t, 1 ≤ t ≤ T−1: h y_t² − λ_t y_t − 4hλ_t y_t² + λ_{t−1} y_t
  = h(1−4λ_t) y_t² + (λ_{t−1} − λ_t) y_t. Completing the square gives
  h(1−4λ_t)(y_t − ŷ_t)² − (λ_{t−1}−λ_t)²/(4h(1−4λ_t)).
- y_0 = 1: h − λ_0 − 4hλ_0 = h(1−4λ_0) − λ_0.
- y_T: λ_{T−1} y_T = 0.

Summing gives the identity. The two sums are nonnegative because 1 − 4λ_t > 0. □

**Theorem 1 (dtoc5 bracket).** Let x̂ be the committed point
`R/publication/primal/dtoc5-lukvle10/points/dtoc5_point.txt.gz` (sha256 6e963788…):
exact decimals; ŷ rounded to 30 decimals; û from the rows. Set λ̂_t = −2û_t for
t ≤ T−2 and λ̂_{T−1} = 0. Then:

- λ̂_t ≤ 0 < 1/4 for all t. (û_{T−1} = −1.96e-26 is not used.)
- x̂ is exactly feasible.
- With the exact objective value of x̂,

$$
5.38967211918114046742396649913627186883131268\;\le\; d(\hat\lambda)\;\le\; f^*\;\le\; f(\hat x)=5.389672119181140467423966499136271868831313409\ldots
$$

  so f(x̂) − d(λ̂) ≤ 7.21e-43.

*What the computation checks* (`checks/dtoc5-optcdeg2/dtoc5_checks.py`, 2.6 s, Python
`Fraction` and `int` only):

1. It reads the decimal strings as exact rationals.
2. It checks all 49 999 rows exactly and y_0 = 1.
3. It recomputes f(x̂) exactly and confirms that it equals the stored rational in
   `.../logs/dtoc5_check_objective_exact.txt`.
4. It asserts λ̂_t < 1/4 exactly.
5. It evaluates d(λ̂). The polynomial part is exact. Each of the 49 998 division terms
   is rounded **up** to the grid 2^-256 before subtraction, so the result is a rigorous
   lower bound.

*What must be trusted:* Python's rational and integer arithmetic, and the model
transcription. The model was checked by four OSIL readers that agree (author, first
verifier, primal reviewer, primal author) and by my exact `.gms` text check.

*Status:* this certificate is new in this dossier and has **not yet been independently
reviewed** (see issue DO-1).

**Corollary (attainment and localization; proof given here).**

- **Attainment.** f* is attained. On a level set {f ≤ c}, the variables u and
  y_0..y_{T−1} are bounded, and y_T = y_{T−1} + 4h y_{T−1}² − h u_{T−1} is then bounded
  too. The feasible set is closed, so the level set is compact.
- **Localization.** By Proposition 1, every feasible x with f(x) ≤ f(x̂) satisfies
  Σ_t (u_t + λ̂_t/2)² + Σ_{t≥1} (1−4λ̂_t)(y_t − ŷ_t(λ̂))² ≤ 7.21e-43/h = 3.7e-38.
  Since 1 − 4λ̂_t ≥ 1, every global minimizer has each u_t and each y_t (t ≤ T−1)
  within 1.9e-19 of the explicit values −λ̂_t/2 and ŷ_t(λ̂).
- **Conclusion.** The optimal set is nonempty and has diameter below 4e-19 in these
  coordinates. Proving uniqueness would require an exact KKT pair, for example an
  interval Newton proof on the tridiagonal reduced system. It is not needed for any claim.

**Earlier certificates of the same form** (all valid; the summary display depends on the
second one):

- Author (`R/open-instances/dtoc5_bound.py` → `logs/dtoc5_bound.json`): λ = −2u from a
  double-precision Newton solve, evaluated in mpmath iv (30 digits):
  **5.3896721191811325**.
- First verifier (`R/reviews/open-instances-verification/v_dtoc5.py` →
  `logs/dtoc5_verify.json`): own Newton solve plus three 40-digit Newton steps, λ rounded
  to doubles, evaluated in mpmath iv: [5.3896721191811404674239647238640027, …8610945].
  The multipliers were not saved, so reproducing this value means regenerating them.

### 3.2 optcdeg2: one quadratic calibration whose curvature vanishes at both switches

**Why affine fails.** The control enters linearly and b = e_v, so the costate switching
function is σ = p_v. On the two u = −1/5 arcs, p_v > 0: p_v(1) = 124.09 on the head,
and p_v ≈ 0.595 on the tail end. The affine residual then contains the term −b·p_v·v²
from S_{t+1}(v − bv² + …), which is **concave** in v. So the affine (Lagrangian)
calibration is not minimized at the trajectory on whole arcs.

- This is a failure of the stage-wise Mangasarian condition, not a switch effect.
- In floating-point screening, the affine calibration loses 0.6258 in total: 0.6197 on
  the head and 0.0060 on the tail.
- The best affine-plus-window bound of the first wave (exact head block via a
  monotonicity certificate) reached 293.8699938542, a gap of 6.1e-3.

**Idea.** Add a curvature term only in v:

$$
S_t(y,v)=p^y_t\,y+p^v_t\,v+\tfrac{q_t}{2}\,(v-\bar v_t)^2 ,
$$

- (p^y, p^v) are the discrete costates of a refined KKT point, and v̄ is its velocity.
- On each u = −1/5 arc, q_t is chosen so that the v-curvature of ρ_t at the trajectory
  equals a positive margin 2κh. This requires
  ρ_vv = −0.4h·p^v_{t+1} + q_{t+1}(1 − 0.4h v̄_t)² − q_t = 2κh.
- Head: q_{3091} = 0 and, backward,
  q_t = q_{t+1}(1 − 0.4h v̄_t)² − 0.4h p^v_{t+1} − 2κ_H h with κ_H = 1, giving
  q_0 = −34.10.
- Middle arc: q ≡ 0, because the affine residual is already convex there (p^v < 0).
- Tail: q_{47291} = 0 and, forward,
  q_{t+1} = (q_t + 0.4h p^v_{t+1} + 2κ_T h)/(1 − 0.4h v̄_t)² with κ_T = 0.05, giving
  q_N = 0.286.

Two facts make this possible.

1. **Fixed endpoints free the curvature at both ends.** The endpoints v_0 = 0 and
   v_N = 0 are fixed, so the curvature of S_0 and S_N in v never enters the bound. The
   schedules can therefore start from q = 0 at each switch and run outward.
2. **Zero curvature keeps the switching stages exact.** q = 0 at both switches means the
   state gradient of the switching function, ∝ (0, q_{t+1}), vanishes there. This
   "tangency" keeps the fractional switching stages exact.

The bang-bang note's Proposition 3.1 explains why exact C² calibrations must be
tangential at a regular switch. That is interpretation; validity does not depend on it.

**Lemma 2 (calibration bound; Krotov-type).** Let S_1, …, S_N be arbitrary real
functions on ℝ², and let V_t ⊂ ℝ (1 ≤ t ≤ N−1) contain v_t for every exactly feasible
point. Put U = [−1/5, 1/5] and

$$
\rho_t(y,v,u)=w y^2+S_{t+1}\big(y+hv,\;v+hu-ay-bv^2\big)-S_t(y,v).
$$

Then every exactly feasible point satisfies f(x) ≥ m_0 + Σ_{t=1}^{N−1} m_t + m_N, where

- m_0 = min_{u∈U} [100w + S_1(10, hu − 10a)];
- m_t = inf {ρ_t(y,v,u) : y ∈ ℝ, v ∈ V_t, u ∈ U};
- m_N = inf_{y∈ℝ} [w y² − S_N(y, 0)].

*Proof.* For a feasible point, (y_{t+1}, v_{t+1}) is exactly the image of
(y_t, v_t, u_t) under the dynamics. The S terms therefore telescope:

f(x) = [w y_0² + S_1(y_1, v_1)] + Σ_{t=1}^{N−1} ρ_t(y_t, v_t, u_t) + [w y_N² − S_N(y_N, v_N)].

Here y_0 = 10, v_0 = 0, and hence (y_1, v_1) = (10, hu_0 − 10a); also u_t ∈ U,
v_t ∈ V_t, y_t ∈ ℝ and v_N = 0. Each bracket is at least its infimum. □

**Lemma 3 (state enclosure).** Define intervals by one forward and one backward pass:

- Forward: Y_{t+1} = Y_t + hV_t and V_{t+1} = g(V_t) + hU − aY_t, where
  g(v) = v − bv². Intersect with [−1, ∞) for 1 ≤ t+1 ≤ N−1, and check that 0 ∈ V_N.
- Backward: Y_t ∩ (Y_{t+1} − hV_t) and V_t ∩ g^{-1}(V_{t+1} − hU + aY_t).
- Every step is rounded outward.

These intervals contain the states of every feasible point.

*Proof.* Induction over t; each recurrence holds exactly at a feasible point.

- g is increasing on v < 1/(2b) = 6250. The forward upper bounds are below 1.22
  (asserted < 6000), so g maps intervals to intervals through their endpoints.
- The relevant preimage is the increasing branch.
- Outward rounding preserves containment. □

The reviewer's implementation (`R/reviews/bangbang-verification/v_states.py`) works as
follows:

- It computes each step exactly in rationals and rounds outward to the dyadic grid 2^-110.
- It encloses g^{-1} by one exact Newton step, which lands below the root because g is
  concave, followed by exact corrections.
- It rounds the final bounds outward to doubles.
- Result: V_t ⊂ [−1, 1.2134], maximum width 2.089.

**Lemma 4 (exact stage minimization).** Fix t and the data, and write
P0 = (p^y_t, p^v_t, q_t, c_t) and P1 = (p^y_{t+1}, p^v_{t+1}, q_{t+1}, c_{t+1}), with
c = v̄. Let e = g(v) + hu − c_{t+1} and

- A2 = w + q_{t+1}a²/2;
- B0 = p^y_{t+1} − p^y_t − a p^v_{t+1};
- K2 = q_{t+1}w/(2A2);
- K1' = p^v_{t+1} + B0 q_{t+1} a/(2A2);
- K0 = −B0²/(4A2);
- F(v) = (h p^y_{t+1} − p^v_t) v + p^v_{t+1} c_{t+1} + K0 − (q_t/2)(v − c_t)².

If A2 > 0, then min_{y∈ℝ} ρ_t = G(v, e) := F(v) + K2 e² + K1' e. The control enters
only through e ∈ [e_−(v), e_+(v)] = g(v) − c_{t+1} + h·[−1/5, 1/5]. Hence

m_t = min( min_{V_t} G(v, e_−(v)), min_{V_t} G(v, e_+(v)), [K2 > 0] min_{R*} G*(v) ),

where G* = F − K1'²/(4K2) and R* is any interval containing
{v ∈ V_t : e_−(v) ≤ −K1'/(2K2) ≤ e_+(v)}.

*Proof (re-derived for this dossier).* With y' = y + hv and v' − c_{t+1} = e − ay,

ρ_t = A2 y² + (B0 − q_{t+1} a e) y + [h p^y_{t+1} v + p^v_{t+1}(e + c_{t+1}) + (q_{t+1}/2)e² − p^v_t v − (q_t/2)(v − c_t)²].

Minimizing over y subtracts (B0 − q_{t+1} a e)²/(4A2). The e² coefficient becomes
q_{t+1}/2 − q_{t+1}²a²/(4A2) = q_{t+1}w/(2A2) = K2, and the e coefficient becomes K1'.

For fixed v, the map u ↦ e is affine and increasing. A quadratic in e attains its
minimum over an interval at an endpoint, or at the vertex when K2 > 0. Over any
superset of R*, G* is still ≤ min_e G, so the third term remains a valid lower bound. □

Each piece is a univariate polynomial of degree ≤ 4 on an interval. The reviewer's code
(`v_qcal_exact.py`) minimizes it rigorously, as follows:

- It evaluates G at both endpoints.
- It isolates the distinct real roots of G' with an exact Sturm sequence.
- It brackets each sign change from − to + exactly, using floating-point roots only as seeds.
- On a bracket [l, r] around a root of G' it uses G ≥ min(G(l), G(r)) − M2(r−l)², with
  M2 ≥ max|G''|. This is valid because |G'| ≤ M2|x − x_0| on the bracket.
- Even-multiplicity roots and local maxima cannot be interior minima and are skipped.

The code also checks the y-elimination exactly against the definition of ρ_t, at three
(v, u) points in each of about 110 stages.

**Theorem 2 (optcdeg2 lower bound; computer-assisted, exact rational arithmetic).** Take
the calibration data (p^y, p^v, q, c) as the float64 arrays in
`R/theory-bangbang/logs/optcdeg2_qcal_data.npz` (sha256 08311d33…), read as exact
rationals. Take V_t from Lemma 3 as computed by `v_states.py`. Then every exactly
feasible point of optcdeg2 satisfies

$$ f(x)\ \ge\ 293.87607509587509237940\ldots\ (\text{exact value } B=\textstyle\sum_t \lfloor m_t\rfloor_{2^{-200}},\ \text{truncated}). $$

Components:

- m_0 = 1014.9964727128661…
- m_N = −p^y_N²/(2h) = −1.8598627153335e-4. Here c_N = 0, so the q_N term vanishes.

*What the computation checks.*

1. A2 > 0 at every stage (the minimum A2 is 1.99999e-4).
2. The exact y-reduction; spot checks against the definition at about 110 stages.
3. The exact u case split. The interior-u piece is never active.
4. Rigorous minimization of 11 596 quartics: 7 785 seeded brackets, no fallback
   bisections, no even-multiplicity roots, largest bracket slack 9.5e-29.
5. Each stage minimum is floored to the grid 2^-200 and the floors are summed as
   integers (loss 1.6e-56).

Arithmetic: Python `Fraction` and `int`. Floating point is used only for seeds and
initial guesses, and every use is followed by an exact check. Run time 16–18 s.

*What must be trusted:* Python's rational arithmetic; correctness of `v_states.py` and
`v_qcal_exact.py` (reviewed line by line for this dossier, see Section 8); and the model
reading.

*Cross-validation by a second method.* The author's certificate
(`R/theory-bangbang/optcdeg2_qcal_certify.py` → `logs/optcdeg2_qcal_certify.json`) is a
separate implementation:

- It uses outward-rounded IEEE interval arithmetic (`ivnp`).
- It covers each stage with 162 geometric cells and bisects cells below −1e-16.
- Its domain is the stored first-wave V_t widened by one ulp.
- It gives **293.8760750958728**, a valid bound of its own.

The reviewer found that the stored V_t are rounded to nearest, cutting off up to
0.4999 ulp, but that after one-ulp widening they contain the rigorous V_t at all 50 001
stages. Every author per-stage bound is ≤ the exact stage minimum (maximum difference
−3.7e-19). Note that "bad_cells_final: 1" in the author's log is not a failure: one
stage kept a cell bound below −1e-16 after 12 refinement rounds, and that lower bound
is what enters the sum.

---

## 4. Exactly feasible primal points

**dtoc5.** The point is stored as exact decimals in
`R/publication/primal/dtoc5-lukvle10/points/dtoc5_point.txt.gz`. It was constructed as
follows:

1. Start from the double-precision Newton solution.
2. Apply three 50-digit Newton steps on the reduced problem in y; the maximum gradient
   falls to 4.3e-46.
3. Round y_1..y_T to 30 decimals and set y_0 = 1.
4. Compute u_t = 50 000(y_t − y_{t+1}) + 4y_t² in exact rational arithmetic, which
   gives terminating decimals with at most 60 digits.

Every row holds exactly by construction. Checks:

- The author's generic exact checker (`check_exact_point.py`) and a cross-check with the
  first verifier's reader (`dtoc5_crosscheck.py`) both report 0 failures.
- Negative test: changing x500 by 1e-60 breaks only row e500.
- The independent primal review r1 (own reader `osil_rev.py`, Fractions) verified all of this.
- Integration recomputed the objective exactly.
- My `dtoc5_checks.py` re-checks all rows and the objective exactly.

The objective is the exact rational in `logs/dtoc5_check_objective_exact.txt`:
5.389672119181140467423966499136271868831313409846661118…

**optcdeg2.**

- Controls: −1/5 for t < 3091; the stored double u_3091 = 1506828432880435/2^55 ≈ 0.041823;
  +1/5 for 3092 ≤ t < 47290; u_47290 free; −1/5 for t > 47290.
- For each value of u_47290, the states are defined by the rows, so every row holds exactly.
- v_N is a polynomial, hence continuous, function of u_47290.
- If v_N(α) < 0 < v_N(β) rigorously, the intermediate value theorem gives u* ∈ [α, β]
  with v_N = 0.
- That point is exactly feasible if, over the whole bracket, v_t ≥ −1 for 1 ≤ t ≤ N−1
  and the bracket lies in U.
- Its objective lies in the interval enclosure of J over the bracket.

Two proofs:

- **Reviewer** (`R/reviews/bangbang-verification/v_primal.py` → `logs/primal_check.json`):
  - mpmath iv at 200 bits, bracket u* ± 1e-40;
  - v_N = ∓3.8e-44 at the bracket ends;
  - min v = −0.8315;
  - J ≤ **293.8760750958750932772142114247080159…**, enclosure width 4.7e-44.
  - Assumes mpmath iv rounds outward correctly.
- **This dossier, without mpmath** (`checks/dtoc5-optcdeg2/optcdeg2_primal_int.py`, 1.5 s):
  - intervals on integers scaled by 2^320 with explicit floor and ceil;
  - bracket u* ± 1e-60;
  - v_N = ∓3.8e-64 at the ends;
  - v_t ≥ −0.83155 over the bracket;
  - J ∈ [293.876075095875093277214211424708015934099559491, +4.8e-64];
  - negative test: a bracket lying above the root shows no sign change.
  - It trusts only Python integers. The two proofs agree to 2.4e-44, which is the
    difference in bracket width.

So f* ≤ 293.87607509587509327722 (20 decimals, rounded up). The summary displays
≤ 293.87607509587509328.

Points that are **not** exactly feasible:

- The author's float KKT point, 293.87607509588105, violates rows by 8.9e-16. It is
  6.0e-12 *above* the rigorous upper bound, because repairing the rows lowers the value.
- The first-wave point 293.876075095886 has a 1.1e-17 bound violation (double 0.2 > .2).
- MINLPLib p1, 293.876075102017, has row violations of 1.25e-14.

---

## 5. Numbers table

| instance | best listed dual | our dual (safe display) | primal (safe display) | gap (rounded up) | sources |
|---|---|---|---|---|---|
| dtoc5 | 0.00243096 (BARON) | **5.38967211918114** (summary); exact-rational dossier certificate 5.38967211918114046742396649913627186883131268 (not yet reviewed) | **5.389672119181141** (exact objective 5.3896721191811404674239664991362718688313134…) | **≤ 4.7e-16** (summary; display-limited, exact 4.6742e-16); ≤ 1.776e-24 against the verifier's dual; **≤ 7.3e-43** against the dossier certificate | listed: `R/publication/minlplib-status/data/part_a.json`; dual: `R/reviews/open-instances-verification/logs/dtoc5_verify.json`, `checks/dtoc5-optcdeg2/dtoc5_checks.log`; primal: `R/publication/primal/dtoc5-lukvle10/logs/dtoc5_check_objective_exact.txt`; gap: `R/publication/integration/gap-values.json`, `R/publication/primal/dtoc5-lukvle10/logs/gaps.json` |
| optcdeg2 | 292.41713458 (GUROBI) | **293.87607509587509** (exact certificate value 293.87607509587509237940…, truncated); author interval certificate 293.8760750958728 | **≤ 293.87607509587509328** (enclosure upper end 293.876075095875093277214211…) | **≤ 9e-16** (exact 8.978142e-16; 3.1e-18 relative) | listed: `part_a.json`; dual: `R/reviews/bangbang-verification/logs/qcal_exact.json` (`bound_str` 29387607509587509237940), rerun `checks/dtoc5-optcdeg2/rerun_reviewer_qcal_exact.json`; primal: `R/reviews/bangbang-verification/logs/primal_check.json`, `checks/dtoc5-optcdeg2/optcdeg2_primal_int.log`; gap: `gap-values.json` |

Agreement check:

- Every summary display is on the safe side of the exact value it summarizes.
- The gap cells match `gap-values.json`: dtoc5 4.6742e-16 → 4.7e-16; optcdeg2
  8.978e-16 → 9e-16.
- **One disagreement of provenance, not of value:** the dtoc5 dual display
  5.38967211918114 is *larger* than the author's stored certificate 5.3896721191811325.
  It rests on the verifier's computation, or now on the dossier certificate (DO-1).

Context for the paper (one-hour runs, one thread; `R/publication/solver-runs/results_table.md`):

- dtoc5 final duals:
  - BARON 0.000273134 (BARON warns that globality is not guaranteed);
  - GUROBI −781.515624;
  - SCIP 0.000019999.
- optcdeg2 final duals:
  - BARON 2.31984 (same warning);
  - GUROBI 166.817;
  - SCIP 200.134.
- Returned primal values *below* the certified optimum, which are tolerance artifacts:
  - dtoc5: BARON 5.38966972922 and GUROBI 5.38967197982;
  - optcdeg2: BARON 293.876075034.
- These rows belong to the first, overloaded batch, which passed the measurement rule.

---

## 6. Verification record

| item | reviewer and method | verdict | remaining assumptions |
|---|---|---|---|
| dtoc5 dual (argument, value) | First verifier, `R/reviews/open-instances-verification/` (2026-09-29): own OSIL reader (`osilx.py`, exact strings); re-derived Lagrangian; own Newton plus 40-digit mpmath Newton; d(λ) in mpmath iv | **verified**; 5.38967211918114046 | mpmath iv; multipliers regenerated, not saved |
| dtoc5 dual (exact) | This dossier: exact-rational evaluation from the committed point | consistent with the verifier (difference 1.8e-24) | Python `Fraction`; **not independently reviewed** |
| dtoc5 exact primal | Primal track plus independent review r1 (`R/publication/reviews/primal-dtoc5-lukvle10-review-r1.md`), own reader, Fractions; integration re-evaluation | **verified** (minor issues addressed) | Python `Fraction` |
| optcdeg2 model | `v_model.py` (own ElementTree reader, exact decimals); my `.gms` text check | structure verified | — |
| optcdeg2 V_t | `v_states.py` (exact, 2^-110 grid); re-run by me: identical array | **verified**; author's stored V_t valid only with the one-ulp widening | Python `Fraction` |
| optcdeg2 bound | `v_qcal_exact.py` (exact Sturm-based); re-run by me: identical `bound_str`; author's `ivnp` certificate as a second method | **verified** (bang-bang verification, Part A) | Python `Fraction`; one exact implementation, cross-checked by the interval implementation |
| optcdeg2 primal | `v_primal.py` (mpmath iv, 200 bits); my integer-interval proof | **verified**; agree to 2.4e-44 | mpmath iv (reviewer only); Python `int` (mine) |
| telescoping consistency | `diag_stage_losses.py`: at a 2^-300-accurate feasible trajectory the identity holds to 5e-85; every stage loss ≥ 0; the losses sum to UB − LB = 8.978e-16, almost all at stage 3091 (p^v_{3092} = 7.6e-12) | consistent | — |
| bang-bang theory (Props 1.2, 1.3, 3.1, 3.2; Thms 2.3, 4.1) | Bang-bang verification Part B plus three confirmation rounds (`R/reviews/bangbang-root-fixes-confirm*.md`) and root edits | proved under stated hypotheses; Thm 4.1's B = f* is conditional on window exactness and an exact terminal term | not used by the certificate |
| displays and gaps | Integration (`R/publication/integration/`) | exact gap fractions recorded | — |

---

## 7. Relation to prior work

Instances (from `R/publication/literature/control/report.md`; reviewed, latest verdict verified):

- **dtoc5.**
  - *MINOTAUR 0.4.1*, Mittelmann's QPLIB benchmark (17 May 2026): reports "Optimal
    solution found", value 5.3897, in 1005 s, on QPLIB_8585, which is textually
    identical to MINLPLib dtoc5. The log says default lower and upper bounds were
    assumed for 99 983 and 99 997 variables, so this is a floating-point claim on an
    artificially bounded box. Its value agrees with ours.
  - *Waki, Kim, Kojima and Muramatsu (2006)*, SIAM J. Optim. 17:218–242 (slug
    `waki2006-sums-of-squares-and-semidefinite`), problem (39), p. 30, Table 12: the
    sparse order-1 SDP relaxation (Shor/Lagrangian level) of the **h variant** is
    numerically tight for M = 600–1000. It is the same phenomenon, zero relaxation gap,
    on the source model. Cite it as prior global work on the source model.
  - Coleman–Liao Table 3 and Smith (2011) report local values only.
  - The DTOC5.SIF SOLUTION lines are tolerance artifacts.
  - QPLIB (`furini2018-qplib-a-library-of-quadratic`) gives only the value 5.38967212.
- **optcdeg2.**
  - *MINOTAUR 0.2.1* was listed as solving QPLIB_8803 in 1641 s (Mittelmann, 3 Dec 2021).
    The log and value are unavailable, and no later table lists it as solved.
  - MINOTAUR 0.4.1 (2026) stops with "Detected infeasibility", which is false, since an
    exactly feasible point exists.
  - GUROBI's 292.417 (MINLPLib, 2023) is a tolerance artifact.
  - BARON's 2026 incumbent 293.876075074557 lies 2.1e-8 below the certified optimum.
  - COPT's bound is 283.41.
- Searches cannot establish novelty. The literature verdict for both instances is
  "partly known (floating point); first rigorous certificate as far as found".

Mechanisms:

- **Discrete verification functions:** Krotov, Doklady AN SSSR 172(1) (1967), and
  *Global Methods in Optimal Control Theory* (1996). Related: Bellman inequalities and
  the LP approach to dynamic programming; Lincoln–Rantzer relaxed dynamic programming
  (slugs `rantzer2005-on-approximate-dynamic-programming-in`,
  `rantzer2006-relaxed-dynamic-programming-in-switching`); Wang–O'Donoghue–Boyd (2015),
  quadratic value-function lower bounds from LMIs. The affine case is the Lagrangian
  dual (`R/theory-calibration/scouting.md`, Theorem 3.1).
- **dtoc5 mechanism:** sufficiency of a KKT point whose Lagrangian is convex at its
  multipliers.
  - Mangasarian (SIAM J. Control 4, 1966), in discrete-time form (Sydsæter et al.,
    *Further Mathematics for Economic Analysis*, Ch. 12).
  - Tamminen, ESAIM COCV 25 (2019) A20: strong Lagrange duality for discrete-time control.
  - For QCQPs: the global optimality condition "KKT plus ∇²L(λ) ⪰ 0", for example
    Jeyakumar–Rubinov–Wu, Math. Program. 110 (2007) 521–541. That paper is **not** in
    `literature/`; verify the reference before citing it.
  - "Arrow-type" (Arrow–Kurz 1970) is not needed for dtoc5. It describes lnts.
- **optcdeg2 mechanism:**
  - quadratic verification functions via Riccati equations: Maurer–Pickenhain,
    JOTA 86 (1995) 649–667;
  - bang-bang second-order conditions with Riccati solutions that jump at switches:
    Osmolovskii–Lempio, Set-Valued Anal. 10 (2002); Maurer–Osmolovskii, Control
    Cybern. 32 (2003).
  - The bang-bang verification showed that tangency (β = Pb − w = 0) is exactly the
    no-jump case q_k = 0 of the Osmolovskii–Maurer jump condition.
  - The pointwise Leitmann–Stalford condition (JOTA 8, 1971) is the property that fails
    for affine calibrations on the u = −0.2 arcs.
  - Bibliographic data for these were checked against Crossref and mathdoc; only parts
    of Maurer–Osmolovskii were read.
- **Rigorous-bound framing:** Neumaier–Shcherbina (`neumaier2004-safe-bounds-in-linear-and`)
  and Neumaier (`neumaier2004-complete-search-in-continuous-global`).
- **Global dynamic optimization:** branch-and-bound with ODE bounding (Chachuat–Singer–Barton,
  `chachuat2005-global-mixed-integer-dynamic-optimization`;
  `singer2006-bounding-the-solutions-of-parameter`) treats continuous-time models. No
  prior rigorous certificate for these transcriptions was found.

---

## 8. Critical examination

### 8.1 What I re-derived

- **dtoc5.**
  - The Lagrangian, the dual function, the hypotheses (λ_{T−1} = 0; λ_t < 1/4 for
    t ≥ 1; no condition on λ_0, because y_0 is fixed), and the completed-square identity
    of Proposition 1.
  - The identity also yields the localization corollary.
  - The objective covers u_0..u_{T−1} and y_0..y_{T−1}, not y_T. I confirmed this in the
    `.gms` and in the OSIL census.
- **optcdeg2.**
  - The telescoping bound (Lemma 2), including the stage-0 and terminal terms and the
    exact coordinates (y_1, v_1) = (10, hu − 10a).
  - The reduced residual G(v, e) (Lemma 4). I derived A2, B0, K2, K1', K0 and F by hand,
    and they match the code term by term.
  - The u case split, the validity of using a superset of R*, the Sturm and bracket
    logic, the M2 slack bound, and the handling of degrees ≤ 2.
  - The state enclosure: branch choice for g^{-1}, the direction of the Newton step
    (below the root because g is concave), and outward rounding.
  - The curvature recursions: the stated q-schedule makes ρ_vv = 2κh at the trajectory.
    This is design only; validity does not depend on it.
  - The data checks: q_{3091} = 0, q ≡ 0 for 3091 ≤ t ≤ 47291, q nonzero from 47292,
    c = v̄, c_N = 0, p^v_{3092} = 7.6e-12, p^v_N = 0.5952523741, p^y_N = −3.857e-4.

### 8.2 Cheap checks run (one core each; all in `/tmp/dossier-dtoc5-optcdeg2`)

| command | result |
|---|---|
| `python3 dtoc5_checks.py` (2.6 s) | `.gms` model exact; all rows of x̂ exact; f(x̂) equals the stored rational; exact dual ≥ 5.38967211918114046742396649913627186883131268…; gap 7.205e-43 |
| `python3 optcdeg2_gms_check.py` | `.gms` rows, objective and bounds exact; 150 002 variables |
| copy of `v_states.py` (4.7 s) | V_t identical to the stored `vt_reviewer.npy` |
| copy of `v_qcal_exact.py` (16.2 s) | `bound_str` 29387607509587509237940 (identical); stage-0, terminal and statistics identical |
| `python3 optcdeg2_primal_int.py` (1.5 s) | exactly feasible point without mpmath; J = 293.876075095875093277214211424708015934099559491 (+4.8e-64); negative test passes |
| `sha256sum` | `.gms` and OSIL hashes match `part_a.json`; npz 08311d33… |

### 8.3 Issues and resolutions

**DO-1 (major for reproducibility; not invalidating).**

- *Problem.* The summary's dtoc5 dual display 5.38967211918114 exceeds the author's
  stored certificate 5.3896721191811325. It is supported only by the first verifier's
  mpmath computation. That computation used multipliers obtained by a fresh Newton
  solve, and they were not saved, so the displayed number can be regenerated but not
  replayed. The reproduction README lists the author command, whose output is below the
  display, and the reviewer command, which regenerates the multipliers.
- *Resolution, done here:* the exact-rational certificate of Theorem 1. Its multipliers
  are read from the committed exact point, so it replays in 2.6 s, and it closes the gap
  to 7.3e-43.
- *To adopt it:*
  1. Copy `checks/dtoc5-optcdeg2/dtoc5_checks.py` into the paper's reproduction material.
  2. Have it reviewed independently. This is cheap: under 1 hour of reviewer time and
     seconds of compute.
  3. Optionally widen the displays, for example dual 5.389672119181140467423966 and
     primal 5.389672119181140467423967.

**DO-2 (minor).**

- *Problem.* The optcdeg2 upper bound relied on mpmath iv.
- *Resolution, done here:* the integer-interval proof (Section 4), 1.5 s, which agrees
  to 2.4e-44. Include it as the primary or a second proof.

**DO-3 (minor).**

- *Problem.* The optcdeg2 exact value depends on the committed data npz
  (sha256 08311d33…) and on the reviewer's V_t. The reproduction README's chain
  `optcdeg2_refine_primal.py → … → optcdeg2_qcal_certify.py` regenerates the npz with
  floating-point code. A regenerated npz may differ in its last bits and give a slightly
  different (still valid) bound.
- *Resolution:* describe the exact replay as "`v_states.py` + `v_qcal_exact.py` on the
  committed npz", and state the hash. Regeneration is optional.

**DO-4 (minor).**

- *Problem.* There is only one exact implementation of the optcdeg2 stage minimization.
- *Mitigations already present:*
  - an independent method (the author's interval cells) gives a valid bound
    293.8760750958728 with every per-stage bound ≤ the exact minimum;
  - the telescoping diagnostic shows every stage loss ≥ 0 at an exactly feasible
    trajectory, with the sum equal to UB − LB;
  - I reviewed the code and reproduced its output.
- *Optional further check:* a second exact implementation with a different univariate
  method, for example interval Newton on rational intervals or isolation of
  critical-point resultants. About half a day of agent time; under 1 minute of compute.

**DO-5 (minor; superseded numbers).** Older documents carry superseded values. The paper
must use the summary and exact numbers.

- Open-instances report (5.3896721191811325, gap 8e-15; optcdeg2 293.86999385,
  gap 6.1e-3).
- Bang-bang report Summary ("certified lower bound 293.8760750958728", gap 2.3e-12).
- First-wave head-block certificate (293.8699938542 at m = 3080, 293.8700386118 at m = 3090).

**DO-6 (minor; wording of the mechanism).**

- "Mangasarian/Arrow-type" for dtoc5 should read **Mangasarian-type**: joint convexity
  of the Lagrangian, equivalently of the Hamiltonian, at the KKT multipliers; or "zero
  Lagrangian duality gap at the discrete costate".
- For optcdeg2, do not use the Mangasarian label: that condition fails there. Use
  "quadratic Krotov-type verification function".
- Sign convention: the multiplier on y_{t+1} − y_t − 4hy_t² + hu_t = 0 is λ_t = −2u_t,
  and the calibration slope is p_{t+1} = −λ_t.

**DO-7 (minor; model statements).** Some older notes give imprecise model data. The
paper should state:

- v ≥ −1 for 1 ≤ t ≤ N−1 only;
- control bounds exactly ±1/5;
- the variable layout, including v_N = x50001 and u_{N−1} = x50002;
- that the dtoc5 objective omits y_T.

**DO-8 (minor; theory scope).**

- Not needed for the certificate: the window law (Theorem 2.3), tangency
  (Proposition 3.1), the transfer theorem (Theorem 4.1) and the singular-coefficient
  Riccati inequality.
- Float-only evidence: the bang-bang note's Sections 5.7 (window-law screening on the
  optcdeg2 family) and 5.8 (margin sensitivity).
- Conditional result: Theorem 4.1's conclusion B = f* assumes window exactness and an
  exact terminal term.
- If the paper includes this theory, give it its own section with hypotheses, and label
  the screenings "floating-point".

**DO-9 (minor; citations).** Before citing, verify bibliographic details for
Jeyakumar–Rubinov–Wu (2007), Krotov (1967/1996), Mangasarian (1966), Arrow–Kurz (1970)
and Leitmann–Stalford (1971). None is in `literature/`; Leitmann–Stalford and
Maurer–Pickenhain were checked only as metadata. Waki et al. is in the knowledge base;
its problem (39) and Table 12 locations were confirmed in `fulltext.md`.

**DO-10 (minor; interpretation).** "The difficulty for solvers is unbounded variables
and termwise relaxations" is an interpretation.

- dtoc5 evidence: the Lagrangian or Shor relaxation is tight. Waki et al. found the
  same on the h variant.
- Strictly, the Shor SDP value equals sup_λ d(λ) only under SDP strong duality. Here we
  only need d(λ̂) ≤ Shor ≤ f*, which holds without it. So "the order-1 SDP relaxation
  is tight for dtoc5" **is** proved by Theorem 1, up to 7.3e-43.

**DO-11 (minor; optional sharpening).** The 9e-16 optcdeg2 gap comes almost entirely
from stage 3091, where p^v_{3092} = 7.6e-12 ≠ 0. It could be reduced by polishing the
KKT data in high precision so that p^v_{3092} → 0, then re-running the exact check.
Cost: under 1 minute of compute and about 1–2 hours of agent work. It is not needed;
the relative gap is already 3.1e-18.

**Nothing found would invalidate a claimed result.**

---

## 9. What the paper may and must not claim

**May claim** (suggested wording):

- "For the MINLPLib instance dtoc5 (identical to QPLIB_8585), every exactly feasible
  point has objective at least 5.38967211918114, and an exactly feasible rational point
  with objective below 5.389672119181141 exists."
  - With DO-1 adopted after review: "the optimal value lies in an interval of width
    7.3e-43 around 5.3896721191811404674239664991362718688313".
- "The bound is a Lagrangian dual bound with the discrete costates as multipliers. The
  Lagrangian is convex at these multipliers, so the duality gap is zero up to rounding
  of the data, and no variable bounds or branching are needed."
- "For optcdeg2 (identical to QPLIB_8803 up to a redundant declaration), every exactly
  feasible point has objective at least 293.87607509587509237940; an exactly feasible
  point with objective at most 293.87607509587509327722 exists; the optimum is
  bracketed within 9.0e-16 (3.1e-18 relative)."
- "The optcdeg2 certificate is a single quadratic verification function in the
  velocity, with curvature zero on the middle arc and at both switching stages. It is
  checked in exact rational arithmetic in under 20 seconds."
- "MINLPLib's GUROBI dual 292.41713458 equals the value of point p2, which violates
  constraints by up to 1e-6. Under exact feasibility the optimum is 1.459 higher."
- "To the best of our knowledge, these are the first rigorous optimality certificates
  for these two MINLPLib models. A floating-point global closure of dtoc5 under assumed
  default variable bounds (MINOTAUR, 2026) and an unverifiable 2021 solved listing for
  optcdeg2 exist."
- "The mechanisms are classical: Lagrangian (Mangasarian-type) sufficiency, and
  Krotov-type verification functions with Riccati-type curvature."

**Must not claim:**

- that the CUTEst DTOC5/OPTCDEG2, Coleman–Liao or Murtagh–Saunders problems are
  certified (different coefficients, by a factor of 4);
- that MINOTAUR's dtoc5 result is wrong (its value agrees);
- unconditional priority ("first ever", "previously unsolved globally");
- uniqueness of the dtoc5 minimizer (only localization within 4e-19 is proved);
- that the window law, the O(1)-stage switch windows or the margin necessity are
  *proved* for optcdeg2 (they are floating-point screenings or general theorems with
  hypotheses);
- that MINLPLib p1 or the author's float KKT points are exactly feasible;
- that the 1.459 difference means GUROBI's *bound* is invalid (the bound is valid; the
  matching "optimal" point is tolerance-feasible only);
- performance rankings from the one-hour runs.

---

## 10. Candidate figures and tables

1. **Table: numbers** (Section 5): listed dual, our dual, primal and gap for both
   instances, plus the one-hour solver duals.
2. **Figure: optcdeg2 trajectory and certificate data** (cheap; saved arrays only). Show
   y_t, v_t and u_t against time with switches at 1.2364 and 18.916; p^v_t, whose sign
   gives the bang-bang law; and q_t, which is zero on the middle arc and at both
   switches, with q_0 = −34.10 and q_N = 0.286. Data: the npz.
3. **Figure: dtoc5 trajectory and convexity margin.** Show ŷ_t, û_t and 1 − 4λ̂_t ≥ 1.
   Data: the exact point file.
4. **Table: optcdeg2 certificate progression.**

   | method | bound | gap |
   |---|---|---|
   | affine Lagrangian | 293.2500703 | 0.626 |
   | affine + exact monotone head block | 293.8699938542 | 6.1e-3 |
   | quadratic calibration, IEEE intervals | 293.8760750958728 | 2.3e-12 |
   | same calibration, exact | 293.87607509587509238 | 9.0e-16 |

5. **Optional (theory section, labelled floating point): margin sensitivity.**

   | (κ_H, κ_T) | total loss |
   |---|---|
   | (0, 0) | 1.07e-4 |
   | (0.02, 0.002) | 1.85e-5 |
   | (0.1, 0.01) | 1.4e-7 |
   | (1, 0.05) | 1.2e-13 |

   Also the family-window screening (families A–D, N = 6250…100 000).

6. **Optional: per-stage loss plot** along the exactly feasible trajectory: all losses
   below 1e-24 except stage 3091 (9e-16). This needs the reviewer's diagnostic to output
   all stages (about 4 min of compute), or uses the saved partial log.
