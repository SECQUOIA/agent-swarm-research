# Dossier: powerflow0030p, powerflow0039p, powerflow0039r

Family key: `powerflow`. Written 2026-10-04 for the MPC paper; this version replaces a
first-pass dossier written earlier the same day (its errors are listed in §8.4). `R/` means
`research-20260929/`. My check scripts and logs are in
`paper-open-minlplib/development/dossiers/checks/powerflow/r2/` (README.txt lists inputs,
patches and commands). The first-pass checks remain in `checks/powerflow/`. All checks ran in
`/tmp` on copies; nothing in `R/` or `literature/` was imported, executed or edited.

**Bottom line.**

- All three dual bounds are rigorous and independently verified. Each proof uses weak
  Lagrangian duality for a quadratic relaxation, exact rational evaluation, and an exact proof
  that a matrix is positive semidefinite. No floating-point error analysis enters any dual bound.
- powerflow0039p/r also need an exact identity at one leaf generator bus, vertex-plane cuts from
  it, and a covering of a three-dimensional box by 6 or 9 leaf boxes.
- Exactly feasible points exist for all three models (interval Newton/Krawczyk proofs,
  independently re-proved). The optimal values are enclosed to relative widths of at most
  2.1e-9, 6.4e-10 and 6.7e-10.
- I found nothing that invalidates a claimed number. I reproduced every cited dual exactly with
  my own Lagrangian code and a different exact PD test (integer Bareiss/Sylvester).
- New in this pass:
  - The 0030p relaxation is now rebuilt by an OSIL reader that shares no code with the
    author's. Before, the author and the wave-3 verifier both used `osilx`.
  - The 0039p certificate also holds without the angle-difference rows and with ε = 0.
  - Two documentation errors are corrected: an unsafe 0039r display (it exceeds the
    certificate by 6.0e-12) and stale "no exactly feasible point" sentences.
  - Several errors of the first-pass dossier are corrected (§8.4).

---

## 1. Instances and models

### 1.1 Source and physical meaning

- These are AC optimal power flow (ACOPF) problems. They minimize the generation cost of a
  steady-state AC transmission network, in per unit on a 100 MVA base, subject to:
  - the AC power-flow equations;
  - bus voltage limits;
  - generator active and reactive limits;
  - apparent-power (thermal) line limits.
- MINLPLib cites Hijazi, Coffrin and Van Hentenryck, "Convex Quadratic Relaxations of Nonlinear
  Programs in Power Systems" (Optimization Online 2013-09). The published version is MPC
  9(3):321–367 (2017). KB slugs: `hijazi2014-convex-quadratic-relaxations-of-nonlinear` and
  `hijazi2017-convex-quadratic-relaxations-for-mixed`. MINLPLib added the instances on
  18 Aug 2014.
- **powerflow0030p.** MATPOWER `case30`: 30 buses, 41 branches, 6 generators. The network
  data are from Alsac–Stott and the generator data from Ferrero et al. Polar formulation.
- **powerflow0039p / powerflow0039r.** MATPOWER `case39` ("New England"): 39 buses,
  46 branches, 10 generators. Polar (p) and rectangular (r) formulations.

### 1.2 Sizes and data (OSIL; my own run of `pf_model.decode` on a /tmp copy, cross-checked by the reviewer's independent reader)

| | 0030p | 0039p | 0039r |
|---|---|---|---|
| type, sense | NLP, min | NLP, min | QCQP, min |
| variables / rows | 236 / 555 | 282 / 657 | 282 / 473 |
| buses / branches / generators | 30 / 41 / 6 | 39 / 46 / 10 | 39 / 46 / 10 |
| flow rows (4 per branch) | 164 | 184 | 184 |
| thermal rows (2 per branch) | 82 | 92 | 92 |
| balance rows | 60 (4 single-variable) | 78 | 78 |
| angle-difference rows | 164 (±0.26 rad) | 184 (±0.26 rad) | none |
| voltage limits | [0.95, 1.05] on 25 buses, [0.95, 1.10] on 5 | [0.94, 1.06] | 0.94² ≤ e²+f² ≤ 1.06² |
| Σ_k v̄_k² | 33.6125 | 43.8204 | 43.8204 |
| reference row | θ_ref = 0 (e496) | θ_ref = 0 (e580) | f_ref = 0 (e396) |
| objective | Σ_g (c2_g P_g² + c1_g P_g), c0 = 0 | Σ_g (100 P_g² + 30 P_g) + 2 | same as 0039p |

- All OSIL variables are continuous and free; every bound is written as a row. Single-variable
  rows become boxes on the flow and generator variables (16 boxes in 0030p, 20 in 0039).
- In 0030p, four flow variables are fixed by single-variable balance rows at one-branch buses:
  x48 = 0, x100 = −0.035, x130 = 0, x182 = −0.023.
- 0030p cost coefficients (OSIL): c1 = (200, 175, 300, 100, 300, 325) and
  c2 = (200, 175, 250, 625, 250, 83.4).
- OSIL SHA-256 (equal to the cache and to the 2026-10-02 refresh): 0030p `5c4b386b…`,
  0039p `0a27073f…`, 0039r `d8ba3132…`.

### 1.3 The model in clean notation

**Variables.**

- Bus voltages: (v_k, θ_k) in the polar form, (e_k, f_k) in the rectangular form.
- For each branch (k, m): the oriented flows P_km, Q_km, P_mk, Q_mk.
- For each generator g: the outputs P_g, Q_g.
- The flows and generator outputs together form the vector y.

**Polar model.** Write θ_km = θ_k − θ_m. The branch π-model has series admittance g_km + i·b_km
and total charging b^c_km. MINLPLib has no taps, no phase shifters and no bus shunts.

```
min   f(y) = c0 + Σ_g ( c1_g P_g + c2_g P_g² )
s.t.  P_km = g_km v_k² − v_k v_m ( g_km cos θ_km + b_km sin θ_km )                 (flow)
      Q_km = −(b_km + b^c_km/2) v_k² − v_k v_m ( g_km sin θ_km − b_km cos θ_km )   (flow)
      Σ_m P_km = Σ_{g at k} P_g − Pd_k ,   Σ_m Q_km = Σ_{g at k} Q_g − Qd_k        (balance)
      P_km² + Q_km² ≤ s̄_km²   (both ends)                                         (thermal)
      v̲_k ≤ v_k ≤ v̄_k ,  P_g ∈ [P̲_g, P̄_g] ,  Q_g ∈ [Q̲_g, Q̄_g]                     (boxes)
      −0.26 ≤ θ_k − θ_m ≤ 0.26  (both orientations of each branch),  θ_ref = 0
```

- Every coefficient is the OSIL decimal, read as an exact rational.
- Each OSIL flow row is written as y + expr(v, θ) = 0. Example: e65 of 0039p is
  `−55.2486187845304·x30·x2·sin(x253 − x225) + x103 = 0`.

**Rectangular model (0039r).**

- Each flow is a quadratic form in the bus coordinates (e, f).
- The voltage rows read v̲² ≤ e² + f² ≤ v̄².
- There are no angle rows; instead there is a reference row f_ref = 0.
- The stored sign convention is f = −v sin θ (network literature report §3.2). Hence, in the
  notation below, the leaf line has P_{L→N} = −b·w^I in 0039r and +b·w^I in 0039p.

### 1.4 Structure that matters

- **Quadratic in rectangular coordinates.** Let x = (e_1, f_1, …, e_n, f_n). For all real v
  and θ, with e = v cos θ and f = v sin θ:
  - v_k² = W_kk := e_k² + f_k²;
  - v_k v_m cos θ_km = w^R_km := e_k e_m + f_k f_m;
  - v_k v_m sin θ_km = w^I_km := f_k e_m − e_k f_m.

  So every flow row reads y_r = xᵀQ_r x with Q_r rational. The objective depends only on y.
  The Shor (SDP) relaxation and the Lagrangian dual therefore apply directly.
- **Rotation invariance.** Rotating every (e_k, f_k) by the same angle leaves every row of the
  relaxation unchanged (§3.6). This is why the exact proofs sometimes need a tiny shift ε.
- **Leaf generator bus (0039 only).** MATPOWER bus 30 has internal index L = 29 (0-based, as
  in all `R/` notes). It is joined only to MATPOWER bus 2 (index N = 1).
  - The branch is the step-up transformer 2–30. In MATPOWER it has r = 0, x = 0.0181, no
    charging and tap 1.025; MINLPLib drops the tap.
  - In the model the branch is a pure series susceptance
    b = 69060773480663/1250000000000 = 55.2486187845304, which is 1/0.0181 rounded to 15
    significant digits.
  - Bus 30 has no load and one generator: Pg = x263 ∈ [0, 10.4] and Qg = x273 ∈ [1.4, 4]
    (MATPOWER gen 30: Pmax 1040 MW, Qmin 140 MVAr, Qmax 400 MVAr).
  - At the optimum, v₃₀ = 1.06 (its upper bound) and Qg = 1.4 (its lower bound).
  - The plain SDP relaxes exactly this branch (§3.1).
  - Buses 30–38 of case39 are all leaf generator buses, each joined by one transformer. The
    branches 2–30, 6–31, 10–32 and 22–35 have r = 0. Only bus 30 needed cuts; the other
    leaves were not treated.

### 1.5 Model provenance: what the instances are not

- **0030p is not MATPOWER case30.**
  - The two bus shunts (Bs = 0.19 MVAr at bus 5 and 0.04 MVAr at bus 24) are missing; their
    values occur nowhere in the file (network literature report §3.1, exact check
    `checks/powerflow_loads_shunts.py`).
  - case30 *with* shunts has a floating-point local solution 576.8923368, which lies *below* our
    bound. **Our bound does not apply to case30.**
- **0039p/r are not MATPOWER case39.**
  - For 11 of the 12 tapped branches, the tap ratio is dropped; the twelfth has τ = 1. All other
    checked data match: costs, limits, thermal limits, line charging and loads.
  - The stored model's optimum is 41869.05; tapped case39's is 41864.18.
  - The leaf transformer 2–30 is one of the dropped-tap branches. With a tap, the leaf
    identity of Lemma 4 would change.
- **Angle limit.** MINLPLib uses ±0.26 rad; the source report uses π/12 ≈ 0.2618. The rows are
  not binding at the optimum (reviewer's floating-point OPF runs).
- **0030p vs 0030r.** The rectangular twin powerflow0030r has the same data up to coefficient
  rounding in the 15th–16th significant digit, and it has no angle rows. Bounds cannot be
  transported between the two files without a perturbation argument.
- **OSIL vs GAMS: identical for all three.** Unlike catmix, methanol and lop97icx, where the
  files differ in the last digits, no rounding difference exists here. Two checks support this:
  - the status refresh compared GAMS-Convert output with the OSIL at 50-digit random points
    (`publication/minlplib-status`, `history_final.log`: "rows_numerically_different 0");
  - an exact term-by-term comparison (first-pass dossier script, which I reran:
    `r2/gms_vs_osil.log`) found 555/555, 657/657 and 473/473 rows identical, objectives
    identical, and maximum coefficient difference 0.

  The bounds therefore also hold for the GAMS models. This statement rests on dossier-level
  scripts plus the refresh's numerical evidence, not on a review.

## 2. Listed status (MINLPLib, fetched 2026-09-29, unchanged at the 2026-10-02 refresh)

All three are **not solved** on MINLPLib: the "S" column is empty. MINLPLib marks an instance
solved only when at least 3 solvers claim global optimality within relative gap 1e-6.

| instance | listed primal (point p1) | best single-solver dual on page | other page duals | listing dual ("≥ 3 solvers") |
|---|---|---|---|---|
| powerflow0030p | 576.8934135 | **572.8395847** (GUROBI, 07 Aug 2025) | 0 (COUENNE 2014, LINDO 2014, SCIP 2022) | 0. |
| powerflow0039p | 41869.05151 | **41818.27916** (GUROBI, 07 Aug 2025) | 3504.985115 (LINDO), 107.4444007 (SCIP), 2 (COUENNE) | 107.4444 |
| powerflow0039r | 41869.05151 | **41804.88153** (GUROBI, 07 Aug 2025) | 41793.39807 (SCIP), 41265.7074 (BARON), 29022.62958 (ANTIGONE), 27103.82841 (COUENNE), 27035.50382 (LINDO) | 41265.7074 |

- The twin powerflow0030r (not a target) lists ANTIGONE's dual 576.8934129 against the primal
  576.8934135, so it is closed in floating point.
- The page shows p1 "infeasibilities" of 6e-15, 9e-14 and 8e-12. Our 50-digit absolute row
  violations of p1 are 2.13e-13 (e133), 1.18e-12 (e178) and 7.91e-12 (e110). The page's
  measure is not documented; quote ours and name the measure.
- Sources: `R/open-instances-scout/fetched.json`,
  `R/publication/minlplib-status/pages/site/instances.html` and `data/tables.md`.

## 3. The certificate

### 3.1 Idea in plain words

- **Relax.** Write the problem in rectangular voltage coordinates. Every constraint becomes a
  quadratic equation or inequality in (x, y), and the cost depends only on y.
- **Weak duality.** Multiply each constraint by a multiplier of the right sign and add it to
  the cost. The sum is a lower bound on the cost at every feasible point. It splits into three
  parts:
  - a constant;
  - a separable quadratic in the flow and generator variables, minimized in closed form over
    their boxes;
  - a quadratic form xᵀAx in the voltage coordinates. If A + εI is positive semidefinite,
    this form is at least −ε·Σ_k v̄_k² on the relaxation.
- **Checking is exact.** An SDP solver supplies multipliers. The bound is then computed in
  exact rational arithmetic, and A + εI ⪰ 0 is proved exactly. A poor solver answer can only
  weaken the bound; it cannot make it invalid.
- **0030p.** This alone closes the gap; the SDP relaxation is essentially exact.
- **0039p/r.** The SDP leaves a relative gap of about 3e-5, and almost all of it sits on one
  line.
  - At leaf bus 30, the two line equations and Lagrange's identity
    |V_N|²|V_L|² = |V_N V̄_L|² fix |V_2|² exactly as a convex function F of
    (Pg, Qg, |V_30|²).
  - The SDP keeps only the inequality |V_2|² ≥ F (a 2×2 minor). So it can raise v₂ above the
    value that the generator's forced reactive output Qg ≥ 1.4 allows.
  - Planes through vertices of a box bound the convex F from *above* on that box.
  - Branching on the three coordinates closes the gap after 11 nodes (0039p) and 17 nodes
    (0039r).

### 3.2 The relaxation R

**Rows.** For each kept row r, write h_r(x, y) = Σ_y ℓ_{r,y} y + Σ_y q_{r,y} y² + xᵀQ_r x,
with Q_r rational and symmetric. The row reads lb_r ≤ h_r ≤ ub_r, an equality if
lb_r = ub_r. R consists of:

- **(F′)** y_r = xᵀQ_r x for every flow row: the identities of §1.4 for polar models, the rows
  verbatim for 0039r;
- **(B), (T)** the linear balance rows and the thermal rows P² + Q² ≤ s̄², unchanged;
- **(Y)** y ∈ Y, the box formed by all single-variable rows on y;
- **(V′)** v̲_k² ≤ e_k² + f_k² ≤ v̄_k²;
- **(A′)** polar only, and used only by the stored 0039p certificate: for each branch pair,
  w^I ≤ t⁺w^R and w^I ≥ t⁻w^R, with rationals t⁺ ≥ tan(0.26) and t⁻ ≤ tan(−0.26).

The reference row is dropped.

**Lemma 1 (R is a relaxation).** Let (v, θ, y) be exactly feasible for a polar OSIL model, and
put e_k = v_k cos θ_k, f_k = v_k sin θ_k. Then (x, y) ∈ R with the same objective. For 0039r,
every exactly feasible (e, f, y) lies in R.

*Proof.*

1. The identities of §1.4 hold for all real (v, θ). So every OSIL flow expression equals
   xᵀQ_r x with the same rational coefficients, and (F′) holds.
2. v̲_k ≥ 0, so v̲_k ≤ v_k ≤ v̄_k implies v̲_k² ≤ v_k² = e_k² + f_k² ≤ v̄_k². This is (V′).
3. Let δ = θ_p − θ_q ∈ [−0.26, 0.26] ⊂ (−π/2, π/2). Then w^R = v_p v_q cos δ ≥ 0 and
   w^I = w^R tan δ. Since tan is increasing, t⁻w^R ≤ tan(−0.26)·w^R ≤ w^I ≤ tan(0.26)·w^R ≤ t⁺w^R.
   This is (A′).
4. Rows (B), (T) and (Y) are unchanged. Dropping a row only enlarges the set. The objective
   depends only on y.

∎

**Computer-checked inputs.**

- The polar conversion was checked three ways:
  - symbolically with sympy (wave-3 verifier; 164 rows of 0030p, 184 of 0039p);
  - term by term with an independent reader, plus 60-digit evaluation (0039 review; largest
    difference 1.6e-58);
  - for 0030p, by my run of the 0039 reviewer's independent reader and row builder
    (`r2/cmp_rows_0030p.log`). It gives all 332 non-angle rows identical to `pf_model`, the
    y boxes, the y list, Σv̄² = 33.6125 and the objective identical, and 60-digit agreement of
    native and converted rows to 2.0e-59.
- The rationals t± come from `pf_model.tan_bounds`: a 40-digit mpmath value ± 1e-35, which is
  not interval arithmetic. Their validity was checked twice:
  - with 300-bit mpmath intervals (0039 review; 0030p in my run of the same code; margin
    1.0e-35);
  - with exact alternating-series bounds (first-pass dossier, `checks/powerflow/tan_check.log`).

  (A′) is needed only by the stored 0039p certificate, and §3.5 removes even that need.

### 3.3 Lagrangian certificate

**Multipliers.**

- λ_r ∈ ℝ on each equality row.
- μ⁺_r ≥ 0 (only if ub_r is finite) and μ⁻_r ≥ 0 (only if lb_r is finite) on each inequality
  row.

Put w_r = λ_r or w_r = μ⁺_r − μ⁻_r, and define

```
c(w)  = c0 − Σ_eq λ_r lb_r − Σ_ineq μ⁺_r ub_r + Σ_ineq μ⁻_r lb_r
κ_y   = c1_y + Σ_r w_r ℓ_{r,y} ,     σ_y = c2_y + Σ_r w_r q_{r,y}
A(w)  = Σ_r w_r Q_r          (2n × 2n, symmetric rational)
V̄²    = Σ_k v̄_k²
```

**Proposition 2 (weak duality with an eigenvalue shift).** Assume:

- σ_y ≥ 0 for every y;
- every y without a box has σ_y > 0 or κ_y = 0;
- A(w) + εI ⪰ 0 for some rational ε ≥ 0.

Then every (x, y) ∈ R satisfies f(y) ≥ β(w, ε), where

```
β(w,ε) = c(w) + Σ_{y boxed} min_{t∈[l_y,u_y]} (σ_y t² + κ_y t) + Σ_{y unboxed, σ_y>0} ( −κ_y²/(4σ_y) ) − ε V̄² .
```

*Proof.*

1. At a point of R: λ_r(h_r − lb_r) = 0, μ⁺_r(h_r − ub_r) ≤ 0 and μ⁻_r(lb_r − h_r) ≤ 0. Add all
   of them to f(y):
   f(y) ≥ f(y) + Σ(…) = c(w) + Σ_y (σ_y y² + κ_y y) + xᵀA(w)x.
2. Each y-term is at least its minimum over the box of y, or over ℝ if y is unboxed. On a box
   the minimum is at clamp(−κ/(2σ), l, u) if σ > 0, and at an endpoint if σ = 0. Unboxed, it
   is −κ²/(4σ) if σ > 0, and 0 if σ = κ = 0.
3. xᵀAx = xᵀ(A + εI)x − ε‖x‖² ≥ −ε Σ_k (e_k² + f_k²) ≥ −εV̄², by (V′).

∎

Remarks.

- β depends only on (w, ε). How the multipliers were found does not matter.
  - Stored binary64 multipliers are dyadic rationals and convert exactly.
  - Negative parts of inequality multipliers are clipped to 0, which keeps validity.
- **Shor dual.** The same β is a lower bound on the Shor relaxation of R. Take (W, y) feasible
  with W ⪰ 0 and h_r linear in W. Then f(y) ≥ c + Σ(σy² + κy) + ⟨A, W⟩ and
  ⟨A + εI, W⟩ ≥ 0. Also tr W ≤ V̄², because (V′) holds for W. Hence f(y) ≥ β.
- **Exact PSD test (Lemma 3).** Let M be a symmetric rational matrix, and process the indices
  one at a time:
  - if the pivot d > 0, take the Schur complement;
  - if d < 0, M is not PSD;
  - if d = 0 and its row is nonzero, M is not PSD;
  - if d = 0 and its row is zero, delete the index.

  M ⪰ 0 if and only if no index fails. Proof: congruence M = L·diag(d, M′)·Lᵀ; and if
  M ⪰ 0 with M_kk = 0, then the 2×2 minors force row k to vanish.

  I used a second exact test: integer Bareiss elimination on the scaled matrix, with
  Sylvester's criterion (M ≻ 0 if and only if all leading principal minors are > 0). Both are
  exact in ℚ.

### 3.4 Theorem A (powerflow0030p)

**Theorem A.** Every exactly feasible point of the OSIL model powerflow0030p has objective at
least

β_A = 576.89341229880046984915963178… ≥ **576.8934122988004**.

*Proof.* Apply Lemma 1 and Proposition 2 with the following data:

- **Rows.** R without (A′): 332 rows (164 flow, 82 thermal, 56 linear balance, 30 voltage),
  plus 16 y boxes.
- **Multipliers.** The stored multipliers
  `R/open-instances-wave3/logs/powerflow0030p.sdpcert.json` (SHA-256 `63cf1e21…`).
- **Shift.** ε = 0.

The hypotheses are checked exactly:

- σ_y ≥ 0 for all 176 y;
- every unboxed y with σ_y = 0 has κ_y = 0, so no multiplier adjustment is needed;
- A ≻ 0: exact LDLᵀ gives 60 positive pivots, the smallest 9.865e-8 (wave-3 verifier). All 60
  leading minors are positive by Bareiss (my run).

The value β is 576.8934122988004698491596317863177375… (verifier at 40 digits; my run is
identical to the stored `bound_exact` as a rational). The display 576.8934122988004 truncates
it. ∎

### 3.5 Theorem B (powerflow0039p and powerflow0039r)

**Leaf data.** Fix L = 29 (MATPOWER bus 30), N = 1 (MATPOWER bus 2) and
b = 69060773480663/1250000000000.

- OSIL variables:
  - 0039p: v_L = x30, θ_L = x253, v_N = x2, θ_N = x225;
  - 0039r: (e_L, f_L) = (x214, x253), (e_N, f_N) = (x186, x225);
  - both: Pg = x263, Qg = x273.
- The rows touching bus 30 are:
  - the four flow rows of branch 2–30 (e64, e65, e156, e157);
  - its voltage rows;
  - the balance rows x103 − x263 = 0 and x195 − x273 = 0 (0039p e581/e591; 0039r e397/e407);
  - in 0039p only, its angle rows.
- Define W_NN = e_N² + f_N², W_LL = e_L² + f_L², w^R = e_N e_L + f_N f_L and
  w^I = e_N f_L − f_N e_L.
- The flow rows give P_{L→N} = s·b·w^I (s = +1 for 0039p, −1 for 0039r) and
  Q_{L→N} = b(W_LL − w^R).

**Lemma 4 (leaf identity).** At every point of R,

W_NN = F(Pg, Qg, W_LL) := W_LL − 2Qg/b + (Qg² + Pg²)/(b² W_LL).

*Proof.*

1. The flow rows and the two balance rows give Pg = s·b·w^I and Qg = b(W_LL − w^R).
2. Lagrange's identity holds for all reals:
   (e_N² + f_N²)(e_L² + f_L²) = (e_N e_L + f_N f_L)² + (e_N f_L − f_N e_L)².
   Hence W_NN·W_LL = (W_LL − Qg/b)² + Pg²/b².
3. By (V′), W_LL ≥ 0.94² > 0. Divide by W_LL and expand.

∎

The Shor relaxation keeps only W_NN W_LL ≥ |W_NL|², that is, W_NN ≥ F.

**Lemma 5 (vertex planes).** F is convex on ℝ × ℝ × (0, ∞). Let
B = [p₁,p₂] × [q₁,q₂] × [s₁,s₂] with s₁ > 0, and let H be affine with H ≥ F at the 8 vertices of
B. Then H ≥ F on B.

*Proof.*

1. (p² + q²)/s is the perspective of p² + q², hence convex on s > 0; the rest of F is affine.
   (Hessian check: the diagonal is (2/s, 2/s, 2(p² + q²)/s³), the 2×2 principal minors are
   4/s², 4q²/s⁴ and 4p²/s⁴, and the determinant is 0.)
2. Each z ∈ B is a convex combination Σλ_j z_j of the vertices, so
   F(z) ≤ Σλ_j F(z_j) ≤ Σλ_j H(z_j) = H(z).

∎

**Theorem B.** Let B₀ = [0, 52/5] × [7/5, 4] × [2209/2500, 2809/2500] in the coordinates
(Pg, Qg, W_LL). Let B₁, …, B_m be the stored leaf boxes of the tight runs: m = 6 for 0039p and
m = 9 for 0039r.

- For each i, let ℋ_i be the set of affine H that pass through four vertices of B_i and satisfy
  H ≥ F at all eight. Each leaf has 4 such planes.
- Let R_i be R with three changes:
  - Pg and Qg are boxed to B_i;
  - the row s₁ ≤ W_LL ≤ s₂ is added;
  - one row W_NN − αPg − βQg − γW_LL ≤ δ is added for each H = αp + βq + γs + δ in ℋ_i.

Assume the following, all checked by computer in exact arithmetic:

- (a) B₁ ∪ … ∪ B_m = B₀;
- (b) every H ∈ ℋ_i satisfies H ≥ F at the 8 vertices of B_i;
- (c) Proposition 2 holds for R_i with the leaf's stored multipliers and some ε_i, giving β_i.

Then every exactly feasible point of the OSIL model has objective at least min_i β_i. The
minimum is ≥ **41869.05148485014** for 0039p and ≥ **41869.05148327243** for 0039r.

*Proof.*

1. By Lemma 1, a feasible point gives (x, y) ∈ R.
2. Rows (Y) and (V′) put (Pg, Qg, W_LL) in B₀. By (a), it lies in some B_i.
3. By Lemmas 4 and 5 and (b), W_NN = F ≤ H for all H ∈ ℋ_i. So (x, y) ∈ R_i.
4. Proposition 2 on R_i gives f ≥ β_i ≥ min_i β_i.

∎

**Certificate data.**

- Leaf boxes and multipliers:
  `R/open-instances-wave3/powerflow/ext/logs/powerflow0039p.bb3t.json` (SHA-256 `8af24081…`)
  and `powerflow0039r.bb3t.json` (`09e1a62a…`).
- The B&B code stores max(parent bound, own certificate) per node. The theorem uses only each
  leaf's *own* certificate. Every leaf stores its own multipliers, and every check recomputes
  them.
- The stored exact minimum over leaves:
  - 0039p: 41869.0514848501403285788486… ≥ 41869051484850140/10¹²;
  - 0039r: 41869.0514832724339667485968… ≥ 41869051483272433/10¹².
- Shifts used:
  - 0039p decisive leaf: ε = 10⁻⁸ (the float λ_min(A) is −1.09e-9; the cost is
    10⁻⁸ × 43.82 = 4.4e-7);
  - 0039r decisive leaf: ε = 10⁻⁹ (λ_min ≈ −6.1e-10; cost 4.4e-8);
  - all other 0039r leaves: ε = 0.
- Decisive leaves (exact):
  - 0039p: [3024409/450773, 449605480/66644851] × [7/5, 83/50] × [2749/2500, 2809/2500],
    approximately [6.70938, 6.74629] × [1.4, 1.66] × [1.0996, 1.1236];
  - 0039r: [1327418/197845, 5938456/884431] × [7/5, 713/500] × [2803/2500, 2809/2500],
    approximately [6.70938, 6.71444] × [1.4, 1.426] × [1.1212, 1.1236].

**Angle-free variant of 0039p** (two dossier-level implementations; not yet independently
reviewed).

- Set every angle-row multiplier of the six 0039p leaves to 0. This is the same as using R
  without (A′); the largest stored angle multiplier was 2.3e-7.
- Then A ≻ 0 with ε = 0 on every leaf (`r2/leaves_0039p_noangle.log`; first-pass
  `checks/powerflow/drop_angle.log`).
- The angle rows have lb = 0 and no y terms, so c, σ and κ are unchanged. The new minimum is
  therefore the old c + inner sum without the shift: 41869.05148528834432858 =
  41869.05148485014032858 + 10⁻⁸ × 43.8204.
- So Theorem B for 0039p also holds for R without (A′) and with ε = 0. With this variant, all
  three theorems use only flow, balance, thermal and voltage rows and the y boxes, and no
  trigonometric bound enters any dual proof.

### 3.6 Why an eigenvalue shift appears

**Proposition 6.** Let J = blockdiag(J₂, …, J₂) with J₂ = [[0, −1], [1, 0]]. Then every Q_r of R
and of R_i commutes with J, so A(w) commutes with J for every w. Hence:

- every eigenvalue of A(w) has even multiplicity;
- if the relaxation is tight at a rank-one optimum W* = x*x*ᵀ and the multipliers are exactly
  optimal, then A(w*)x* = A(w*)Jx* = 0.

*Proof.*

1. The 2×2 blocks of every row matrix commute with J₂:
   - W_kk contributes the block I₂;
   - w^R_km contributes the off-diagonal blocks ½I₂;
   - w^I_km contributes ½J₂ at (k, m) and −½J₂ at (m, k);
   - the voltage, angle, cut and VBL rows combine these blocks.
2. If Au = λu, then A(Ju) = λ(Ju) and uᵀJu = 0. So each eigenspace is J-invariant, and J acts
   on it as a complex structure; its dimension is even.
3. If A ⪰ 0 and ⟨A, x*x*ᵀ⟩ = 0, then Ax* = 0, and AJx* = JAx* = 0.

∎

Floating-point multipliers split the double zero eigenvalue into a pair of size about ±1e-9.
The 0030p float eigenvalues are 4.00126e-9 and 4.00143e-9, a pair; then ε = 0 works. At tight
0039 leaves the pair can be slightly negative, and ε = 10⁻⁹ to 10⁻⁸ is needed.

### 3.7 What the computation checks, in what arithmetic, and what must be trusted

**Checks.**

- (i) Parse the OSIL decimals as exact rationals and build the rows of R and R_i.
- (ii) Convert the stored binary64 multipliers to exact rationals, and form c, κ, σ, A and the
  y-minima exactly.
- (iii) Prove A + εI ⪰ 0 exactly: by LDLᵀ (Lemma 3), by integer Bareiss/Sylvester, or by
  Cholesky followed by an exact residual and a Gershgorin bound.
- (iv) For 0039, also check exactly:
  - every plane passes through 4 vertices and satisfies H ≥ F at all 8;
  - the leaves cover B₀;
  - the leaf structure: the four flow forms, b > 0, and the zero-constant two-variable balance
    rows (asserted in `leafcut.leaf_info`).

All arithmetic is exact Python `int`/`Fraction`. Floating point only *generates* multipliers.

**Trust base and the evidence for each part.**

- **(T1) OSIL parsing.**
  - Readers: `osilx` (author and wave-3 verifier); `own_osil.py` (0039 review, and for 0030p
    my run of it); `osil_read.py` (primal review).
  - Supporting evidence: the GAMS files are identical to the OSIL (§1.5), and SCIP's own reader
    accepts the exact points.
- **(T2) Row construction.** Three independent builders agree: `pf_model`, the wave-3
  verifier's `pfv.py`, and the 0039 reviewer's `own_relax.py`.
- **(T3) Exact integer arithmetic in CPython.**
- **(T4) PSD proofs.** Four procedures agree:
  - author `verify_exact` (pivoted exact LDLᵀ);
  - wave-3 verifier (exact LDLᵀ);
  - 0039 reviewer (60-digit Cholesky, exact residual, Gershgorin);
  - this dossier (integer Bareiss/Sylvester; the first pass used natural-order LDLᵀ).
- **(T5) Planes and coverage.** Author `verify_bb3` (volume plus disjointness), reviewer
  `verify_leaves` (grid cells and Cramer's-rule planes), and this dossier (`r2/cover.py`, grid
  cells plus volume; own vertex check in `mycheck.py`).
- **(T6, stored 0039p certificate only) Validity of t±.** Checked with mpmath iv at 300 bits and
  with exact series bounds. The angle-free variant removes (T6).

**Not to cite as proof.** The author's `pf_cert.interval_cholesky` bounds floating-point
summation error by hand (`j·1.2e-16·Σ|·|` padding). That is an unreviewed A1-type argument.
Every cited number is reproduced or exceeded by exact methods, so the paper should cite only
those.

### 3.8 A rigorous corollary for 0030p

By the Shor-dual remark after Proposition 2,
β_A ≤ val(Shor(R)) ≤ val(R) ≤ OPT ≤ f(x*). So the Shor relaxation of 0030p is tight to at most
1.1716e-6 absolute (2.03e-9 relative). This holds both with and without the angle rows,
because β_A uses R without them.

For 0039, only val(Shor(R)) ≥ 41867.7797031 is rigorous: the verifier's accurately solved,
exactly certified root. The plain-SDP gap of about 1.27 (3.0e-5 relative) is numerical. It
rests on Clarabel's primal value 41867.779703029 for 0039r; no rigorous *upper* bound on
val(Shor) was computed.

## 4. Exactly feasible primal points

Source: `R/publication/primal/powerflow/report.md`; points in `points/*.json`.

| file | SHA-256 |
|---|---|
| 0030p | `4b063599…` |
| 0039p | `acef65da…` |
| 0039r | `e851cfb4…` |

**Construction (numerical, not part of the proof).**

1. Start from p1.
2. Fix variables at active single-variable bounds to exact rationals:
   - 0030p: x29 = 21/20;
   - 0039p: x30–x36 and x38 = 53/50; Pg x264, x266, x267, x269, x270 at their upper bounds;
     x273 = 7/5;
   - 0039r: the same six generator bounds.
3. Fix the remaining degrees of freedom, chosen by column-pivoted QR, at p1's decimals. In 0039
   these are x263, x265, x268, x271 and x282.
4. Form a square system S:
   - all equality rows that do not fix a single variable;
   - the active multi-variable inequality rows, taken as equalities: e208 and e211 in 0030p;
     e307–e313 and e315 (e² + f² = 1.06²) in 0039r; none in 0039p.
5. Run Newton's method at 70 digits until the residual is about 1e-68.

Sizes: 222/14, 262/20 and 270/12 free/fixed variables. Jacobian condition numbers: 1.0e4,
2.0e4 and 5.0e4.

**Theorem C.** For each instance there is a point x* with these properties:

- its fixed coordinates equal the stored rationals;
- its free coordinates lie within r = 10⁻⁴⁵ of the stored 60-digit centre c;
- it satisfies every OSIL row exactly (the models have no variable bounds or integrality);
- its objective lies in the enclosure of §5.

*Proof (Krawczyk).*

1. Let X = [c − r, c + r]. Let F(x) = 0 be S with the fixed values substituted. Let C be a
   float64 approximate inverse of the Jacobian. Let J(X) be an interval enclosure of the
   Jacobian over X, from forward-mode interval differentiation of the OSIL expression trees.
2. The computation shows two facts:
   - K(X) := c − C F(c) + (I − C J(X))(X − c) ⊂ int X, with max |K − c|/r = 1.930e-12,
     2.859e-12 and 5.376e-12;
   - ‖I − C J(X)‖_∞ ≤ 1.930e-12, 2.855e-12 and 5.376e-12.
3. For x ∈ X, the mean-value form gives F(x) = F(c) + Ā(x − c) with Ā ∈ J(X), entrywise. Hence
   g(x) = x − C F(x) ∈ K(X) ⊂ X. By Brouwer, g has a fixed point x*, so C F(x*) = 0.
4. ‖I − CĀ‖ < 1, so CĀ and hence C are nonsingular. So F(x*) = 0. The same contraction gives
   uniqueness in X.
5. Every other row is checked in one of two ways:
   - as an interval enclosure over X strictly inside its bounds; the smallest margins are
     4.30e-4 (e215), 1.08e-3 (e346) and 2.29e-3 (e306);
   - exactly in rationals, when all its variables are fixed.

   Counts (in S / exact / interval): 222/23/310, 262/39/356 and 270/23/180. The reviewer
   counts 0030p as 25/308, because it checks two quadratic rows with only fixed variables
   exactly; both are valid.
6. The objective is enclosed over X.

∎

**Citations and assumptions.**

- Cite Krawczyk, Computing 4 (1969) 187–201, and Moore, SIAM J. Numer. Anal. 14 (1977)
  611–615, for existence. Uniqueness and nonsingularity follow from the explicit norm bound.
- The author's computation uses mpmath 1.3.0 `iv`: outward rounding of +, −, ×, /, sin, cos
  and decimal conversion.
- The independent reviewer re-proved all three points without mpmath, `osilx` or author code.
  It used its own dyadic outward-rounded intervals at 2⁻³²⁰ (sin and cos by Taylor series with
  a Lagrange remainder), its own reader and its own preconditioner, and agrees to every printed
  digit.
- Either implementation alone is a full proof.
- SCIP 10 `checkSol` at feastol 1e-9 accepts the double-rounded centres (evidence only).

**Comparisons and leaf data.**

- The exact points' objectives exceed obj(p1) by 2.873e-12, 4.643e-12 and 1.826e-10.
- **Leaf data at the 0039 points (my run, `r2/leaves_*.log`, `r2/pointeval_0039r.log`).**
  - 0039p: Pg = 41964029348667/6250000000000 ≈ 6.71424469578672, Qg = 7/5, v_L = 53/50.
  - 0039r: Pg = 167856117394623/25000000000000 ≈ 6.71424469578492, Qg = 7/5, and W_LL = 1.1236
    exactly (an active row of S). The 60-digit centre exceeds 1.1236 by 9.2e-60.
  - The identity residual W_NN − F at the centres is −8.4e-60 (0039p) and −1.6e-59 (0039r).
  - Each point lies in its run's decisive leaf. The plane slacks H − W_NN at the point are
    4.5e-8 (twice) and 4.6e-7 (twice) for 0039p, and 2.7e-10 (twice) and 4.1e-8 (twice) for
    0039r.

## 5. Numbers table

| | powerflow0030p | powerflow0039p | powerflow0039r |
|---|---|---|---|
| best listed dual | 572.8395847 (GUROBI) | 41818.27916 (GUROBI) | 41804.88153 (GUROBI) |
| listed primal (p1) | 576.8934135 | 41869.05151 | 41869.05151 |
| plain SDP, stored rigorous root (wave 3) | 576.8934122988004… (final) | 41867.77607197097 | 41867.68744320833 |
| plain SDP, accurate re-solve, rigorous (verifier) | — | 41867.77970311977 (ε = 1e-9) | 41867.77970316397 (ε = 0) |
| **our dual (safe display)** | **576.8934122988004** | **41869.05148485014** | **41869.05148327243** |
| exact stored certificate | 576.89341229880046984915963… | 41869.05148485014032857884… | 41869.05148327243396674859… |
| strongest recomputation (not cited) | same | 41869.05148528834 (angle-free, ε = 0) | 41869.05148328967 (reviewer, tight ε) |
| exact primal enclosure | [576.8934134703742598676683, …684] | [41869.0515113202038027683844, …845] | [41869.0515113209830932768581, …582] |
| **primal (safe display)** | **576.8934134704** | **41869.0515113203** | **41869.0515113210** |
| absolute gap (enclosure upper end − display dual) | ≤ 1.171573860e-6 | ≤ 2.6470063803e-5 | ≤ 2.8048553094e-5 |
| **relative gap (summary)** | **≤ 2.1e-9** (2.03083e-9) | **≤ 6.4e-10** (6.32211e-10) | **≤ 6.7e-10** (6.69912e-10) |
| improvement over best listed dual | 4.054 | 50.77 | 64.17 |
| B&B nodes / leaves / time | root only; replay < 1 s | 11 / 6 / 309 s | 17 / 9 / 423 s |

**Sources.**

- Listed values: the summary and `R/open-instances-scout/fetched.json`.
- Duals:
  - the summary;
  - `open-instances-wave3/logs/powerflow0030p.sdpcert.json` (`bound_exact`);
  - `ext/logs/*.bb3t.json` (`LB_exact`);
  - `reviews/wave3-verification/powerflow/root*.log` and `sdp*_root_tight.log`;
  - `reviews/powerflow0039-review.md`;
  - my `r2/root.log`, `r2/leaves_*.log` and `r2/gaps.log`.
- Primal: `publication/primal/powerflow/report.md` and `logs/certify.*.log`.
- Gaps: `publication/integration/gap-values.json`, recomputed exactly in `r2/gaps.log`.
- Times:
  - extension report: 309 s and 423 s;
  - pinned-stack regeneration: 316.23 s and 463.46 s, with identical final bounds
    (`publication/reproduction/network/logs/pf.bb3.*.log`);
  - 0030p is an exact replay of the stored multipliers (my run: 0.4 s).

**Checks of the displays.**

- Every summary display is safe:
  - each dual display is ≤ its exact certificate (by 7.0e-14, 3.3e-13 and 4.0e-12);
  - each primal display is ≥ its enclosure;
  - each gap cell is ≥ the exact gap;
  - each dual is < the lower end of its enclosure.
- **Disagreement (minor).** The extension report (Summary table and §3 table), its tight-run
  log FINAL line, the reproduction log FINAL line and the 0039 review's "stored LB" column show
  **41869.05148327244** for 0039r. That value is above the exact stored certificate
  41869.0514832724339667… by **6.03e-12**.
  - It is still a true lower bound, because the reviewer's recomputation with a tighter shift
    gives 41869.05148328967.
  - The paper must use the summary's **41869.05148327243** or the rational
    41869051483272433/10¹².

## 6. Verification record

| check | by | what was checked | verdict / numbers |
|---|---|---|---|
| wave-3 verification, powerflow part (`R/reviews/wave3-verification/verification-report.md` §2; `powerflow/pfv.py`, `run_root.py`, `sdp_node.py`, `test_cut.py`) | independent subagent | own R from OSIL (via `osilx`); 164/184 flow rows symbolically (sympy); 332 multipliers aligned and sign-checked; exact LDLᵀ; exact L = `bound_exact`; p1 | 0030p **verified** (display corrected to …004). 0039 roots verified. Accurate roots 41867.7797031/…032. The wave-3 pf_bb2 results are superseded (0039p's 41868.26524 cannot be reproduced). |
| `R/reviews/powerflow0039-review.md` (+ `powerflow0039-review-checks/`) | independent reviewer | own reader and own R compared exactly with `pf_model` (0039p/r, including the 92 angle rows and a 300-bit tan check); leaf structure from OSIL; planes re-enumerated (Cramer) and checked exactly; coverage by grid cells (12/16/16/45); every leaf of all four runs re-evaluated exactly (Cholesky + exact residual + Gershgorin); p1; tight fixed-leaf diagnostic | **verified**. Own minima 41869.051485240394 (0039p) and 41869.05148328967 (0039r); both cited rationals hold. Three minor items, applied 2026-09-30. |
| author re-checks `ext/verify_bb3.py`, `verify_exact.py` (rerun by the reviewer) | author | partition by volume and disjointness; exact pivoted LDLᵀ for every leaf | reproduce or exceed the stored bounds (by ≤ 4.4e-8) |
| primal review r1 (`R/publication/reviews/primal-powerflow-review-r1.md`) | independent reviewer | own reader, own dyadic intervals, own Krawczyk and preconditioner; every row; enclosures; gaps; 5 negative controls; SCIP fixed-point check | **verified**; six minor issues, all addressed in the report |
| `R/reviews/closing-confirm-r2.md` F1 | independent | outward rounding of the summary dual displays | all three valid |
| integration (`publication/integration/gap-values.json`) | parent | exact gap cells | 2.1e-9 / 6.4e-10 / 6.7e-10 confirmed |
| reproduction package (`publication/reproduction/report.md`) | package author; review r1 (issues, no blocker) | pinned-stack regeneration of `pf_bb3` (identical final bounds); 0030p replay (576.893412298800469849…) | a fresh 0030p re-solve gives only 576.8905424271796; the certificate is the stored multipliers |
| network literature review r2 (`publication/reviews/lit-network-review-r2.md`) | independent | provenance (shunts, taps, angle rows, twin rounding), prior results | **verified** |
| first-pass dossier (`checks/powerflow/`) | dossier author, unreviewed | GAMS = OSIL exactly; natural-order exact LDLᵀ of roots and leaves; angle-free 0039p; exact tan bounds; coverage; gaps | consistent; see §8.4 for its text errors |
| **this dossier** (`checks/powerflow/r2/`) | dossier author, unreviewed | own Lagrangian + integer Bareiss for the 0030p root and all 15 tight leaves; angle-free 0039p; own vertex check; coverage; Lagrangian at the exact points; 0030p R rebuilt by the reviewer's independent reader; GAMS = OSIL rerun; exact gaps | all consistent (§8.2) |

**Remaining assumptions.**

- **Dual bounds.** Correct code for (T1)–(T5) of §3.7, plus (T6) for the stored 0039p
  certificate only. Several independent implementations agree on each item. No A1/A2-type
  floating-point assumption remains.
- **Primal points.** Correctness of one outward-rounding interval implementation: mpmath `iv`
  for the author, or the reviewer's dyadic code. The two agree, and each alone suffices.

## 7. Relation to prior work

Sources: network literature report `R/publication/literature/network/report.md` §3 and §8
(review r2 **verified**); its saved sources in `…/network/sources/`; KB slugs in
`literature/papers/`.

**Status of these instances.**

- **0030p: partly known.**
  - The twin 0030r is closed in floating point on MINLPLib (ANTIGONE 576.8934129 against
    576.8934135). The files differ by rounding, so no rigorous transfer exists.
  - MATPOWER case30 *with* shunts, a close relative, has a floating-point SDP gap of 0.00%:
    NESTA Table 1 (`coffrin2014-nesta-network-enabled-scalable-tools`), Bingane et al. 2018
    Table I (`bingane2019-tight-and-cheap-conic-relaxations`), and Hijazi et al. June 2014
    Table 3 (`hijazi2014-convex-quadratic-relaxations-of-nonlinear`).
  - Lavaei–Low 2012 (`lavaei2012-zero-duality-gap-in-optimal`) observe a numerically zero
    duality gap for an "IEEE 30-bus" file, probably with different data.
  - Ours is the first rigorous certificate found for this MINLPLib model, and the first bound
    that closes the gap of the polar instance as listed.
- **0039p/r: new as far as found.**
  - Ghaddar, Mareček and Mevissen 2016 (`ghaddar2016-optimal-power-flow-as-a`, Table 4) solved
    *tapped* case39 globally in floating point, with second-order moment bound 41864.18 equal to
    the local value.
  - Published floating-point SDP gaps for tapped case39 are 0.00% (NESTA), 0.01% (Bingane),
    0.005% (Lavaei–Low SDP in Ghaddar et al.) and −0.06% in Hijazi et al. 2014. The last is a
    non-valid bound, as those authors say; it is a good illustration of why rigorous bounds
    matter.
  - No source treats the tap-free model or the value 41869.05.
  - Floating-point runs at the time limit that do not close the gap: SCIP Opt. Suite 8.0
    report, Müller–Serrano–Gleixner 2020, and Göß 2026. Göß prints a 0039p value at an
    unexplained scale (4.0e2); do not use it.

**Certified SDP bounds: the mechanism is known; do not claim it as new.**

- Oustry, D'Ambrosio, Liberti and Ruiz, PSCC 2022 / EPSR 212:108278
  (`oustry2022-certified-and-accurate-sdp-bounds`; KB status "unread", but the network report
  read it).
  - They treat any rational dual vector as a lower bound. Each eigenvalue term is bounded
    rigorously by min_i D_ii + λ_LB(A − UDUᴴ), where λ_LB is a Gershgorin bound and UDUᴴ is a
    rational approximate eigendecomposition. The trace bound ρ_k = Σ_b V̄_b² plays the role of
    our V̄². Their bounds are for PGLib cases (different models).
  - Our differences: a single dense 2n × 2n block, an exact LDLᵀ or Sylvester proof, and exact
    y-minima. The 0039 reviewer's Cholesky + Gershgorin check is essentially their device.
- Jansson, Chaykin and Keil 2007 (`jansson2007-rigorous-error-bounds-for-the`, Theorem 3.2) and
  VSDP (`jansson2006-vsdp-verified-semidefinite-programming`, `harter2012-vsdp-a-matlab-toolbox-for`)
  give rigorous SDP lower bounds from approximate dual solutions, with eigenvalue upper bounds
  on the primal block. Our −εV̄² term is that device.
- The LP analogue is Neumaier and Shcherbina 2004 (`neumaier2004-safe-bounds-in-linear-and`).

**Global ACOPF and spatial branching.**

- Gopalakrishnan et al. 2012 (`gopalakrishnan2012-global-optimization-of-optimal-power`): B&B
  with SDP or Lagrangian bounds.
- Chen, Atamtürk and Oren (`chen2016-a-spatial-branch-and-cut`; BCOL 15.04; Math. Prog. 2017):
  spatial branch-and-cut with linear inequalities from the convex hull of rank-one 2×2 Hermitian
  matrices with box bounds on W_ii, W_jj, Re W_ij and Im W_ij.
- Our leaf cut is close to these. It is the concave envelope, over a box, of the rank-one
  relation W_NN = |W_NL|²/W_LL. The box is in (Im W_NL, W_LL − Re W_NL, W_LL), an affine image
  of their coordinates, and it comes from the generator P and Q bounds.
- Not in the KB and not read: Kocuk–Dey–Sun, "Inexactness of SDP relaxation and valid
  inequalities for OPF" (IEEE TPS 2016), "Matrix minor reformulation and SOCP-based spatial
  branch-and-cut" (MPC 2018), and Coffrin–Hijazi–Van Hentenryck 2017 (SDP strengthening).
- So treat the cut as a simple, problem-specific use of known ideas. The new content is the
  observation that one lossless leaf branch with a binding reactive lower bound carries the
  whole SDP defect, and that an exact identity there closes it.

**Context for the defect.**

- Lavaei–Low 2012 note that zero-resistance transformers break their sufficient exactness
  condition; they add 1e-5 resistance. Our defect sits on such a branch (r = 0), at a generator
  whose Qmin = 140 MVAr and whose voltage upper bound are both active.
- That is consistent with, but not explained by, the literature on SDP inexactness
  (`molzahn2019-a-survey-of-relaxations-and` §4; `kocuk2016-strong-socp-relaxations-for-the`).

**Solver campaign** (`R/publication/solver-runs/results_table.md`; 1 h, one thread; no
closure).

- BARON cannot read sin/cos in the polar models.
- SCIP ended with duals 0 (0030p) and 2 (0039p, the objective constant).
- On 0039p, GUROBI returned a point with objective 41869.0502370 and row violation 6.81e-7.
  That is *below* our rigorous dual by 1.25e-3: a tolerance-feasible point beats a bound that
  is valid for exactly feasible points.

## 8. Critical examination

### 8.1 Re-derivation

I re-derived Lemma 1, Proposition 2, Lemma 3, Lemmas 4–5, Theorem B's covering argument,
Proposition 6 and the Krawczyk argument. I also read the code that produces the numbers:
`pf_model.decode`, `pf_cert.certify`, `leafcut.leaf_info/planes3/cut_rows3`,
`pf_bb3.node_model/run`, `verify_exact` and the reviewers' row builders. I found no logical
error. Points I checked specifically:

- The orientation of w^I is consistent between `pf_model`
  (sin θ_pq v_p v_q = f_p e_q − e_p f_q) and `leafcut`. In 0039p, P_{L→N} = +b w^I, which
  matches GAMS row e65: x103 = b·v30·v2·sin(θ30 − θ2).
- The Lagrangian constant treats the lower and upper sides correctly. Clipping negative
  multiplier parts keeps validity.
- The y-minima are correct for boxed y, unboxed y with σ > 0, and σ = κ = 0. No flow multiplier
  was adjusted in any certificate.
- The −εV̄² term uses only (V′), which belongs to R and to every R_i. The node row
  s₁ ≤ W_LL ≤ s₂ is tighter but is not needed.
- The cut rows are quadratic in x and linear in y, so Proposition 2 applies to them.
- The leaf boxes are closed. Covering needs only the union; overlaps would be harmless.
- A child shares the split value with its sibling, and the coverage check confirms that the
  leaves cover B₀.
- The max(parent, own) inheritance in `pf_bb3` is not used: no final leaf lacks its own
  multipliers.
- For 0039r, the exact point lies on the face W_LL = 1.1236 of its closed leaf. That is
  harmless, because boxes are closed.
- Upper bounds UB enter `pf_bb3` only as a stopping rule; they have no effect on validity.

### 8.2 Cheap checks run in this pass (`checks/powerflow/r2/`; single-threaded, in /tmp)

| check | command (from /tmp/pfd2) | result |
|---|---|---|
| 0030p root, own Lagrangian + integer Bareiss | `python3 mycheck.py root` | PD with ε = 0 (60 leading minors > 0); β equals the stored `bound_exact` as a rational: 576.8934122988004698492… At the exact point x*: L(x*) − β = 1.506e-7 and f(x*) − L(x*) = 1.021e-6; sum 1.17157e-6 = gap. |
| 0039p tight leaves | `python3 -u mycheck.py leaves powerflow0039p bb3t` | all 6 leaves certified, ε ∈ {1e-10, 1e-9, 1e-8}; minimum 41869.05148485014032858 (= stored; differences ≤ 3.9e-8 above stored, or ~1e-23 from ε as exact decimal vs binary64); floor·10¹² = 41869051484850140. At x*: L − β = 5.231e-7, f − L = 2.595e-5. |
| 0039r tight leaves | `python3 -u mycheck.py leaves powerflow0039r bb3t` and `pointeval.py` | all 9 leaves certified (ε = 1e-9 on the decisive leaf, 0 elsewhere); minimum 41869.05148327243396675 (= stored); floor·10¹² = 41869051483272433. At x*: L − β = 6.234e-7, f − L = 2.743e-5. |
| angle-free 0039p | `python3 -u mycheck.py leaves powerflow0039p bb3t noangle` | all 6 leaves PD with ε = 0; minimum 41869.05148528834432858 |
| plane validity | inside `mycheck.py` | 4 planes per leaf; H ≥ F exactly at all 8 vertices for all 60 planes |
| coverage | `python3 cover.py` | 16 and 45 grid cells, each in exactly one leaf; volume sums exact |
| 0030p R by an independent reader | `(cd rev; python3 cmp_rows.py powerflow0030p)` | 332/332 non-angle rows, boxes, y list, Σv̄² = 33.6125 and objective identical to `pf_model`; polar rows agree with native OSIL to 2.0e-59 at 60 digits; 41 angle pairs valid (margin 1.0e-35) |
| GAMS vs OSIL (first-pass script, rerun) | `(cd gv; python3 gms_vs_osil.py …)` | 0 differing rows in all three; objectives identical |
| gaps and displays | `python3 gaps.py` | §5 numbers; 0039r display 41869.05148327244 exceeds the certificate by 6.03e-12 |
| MATPOWER cross-check | text inspection of `network/sources/matpower_case39.m` | branch 2–30: r = 0, x = 0.0181, b = 0, tap 1.025; gen 30: Qmin 140, Qmax 400, Pmax 1040; buses 30–38 are leaves |

Wall time: about 8 minutes of single-core CPU in total. These checks use `pf_model` copies for
row order, so they are not independent of row construction; the reviews cover that, and the
0030p rebuild above now does too.

### 8.3 Issues and proposed resolutions

None of these invalidates a claimed result.

1. **(minor) Unsafe 0039r display.**
   - 41869.05148327244 appears in `extension-report.md` (Summary and §3 tables), the bb3t and
     reproduction FINAL log lines, and the 0039 review table. It exceeds the stored exact
     certificate by 6.03e-12.
   - It is still a valid bound, through the reviewer's stronger recomputation
     (41869.05148328967).
   - *Resolution:* the paper cites 41869.05148327243 or 41869051483272433/10¹² only. No
     computation is needed. Optionally, note this in the next `R/` integration round.
2. **(minor) Stale primal statements.**
   - `R/SYNTHESIS.md` (lines ~486–489) and `R/closing-research-results.md` (lines ~209–213)
     still say that for lnts, dtoc5, lukvle10, chain and powerflow "no exactly feasible point
     was constructed".
   - The summary and `publication/primal/*` supersede both.
   - *Resolution:* do not propagate these sentences. The integration owner should fix the two
     files; `R/` is not edited here.
3. **(minor; removable assumption) The stored 0039p certificate uses the angle rows (A′) and
   ε = 10⁻⁸.**
   - So it needs the tan-bound step (T6). That step was checked with mpmath iv (reviewer) and
     with exact series bounds (first-pass dossier).
   - Two dossier implementations show that zeroing the angle multipliers gives a stronger,
     ε-free certificate (41869.05148528834).
   - *Resolution:* state Theorem B for R without (A′), so that Lemma 1 has no angle part for any
     instance. Before citing it, run one independent replay: for example, the reviewer's
     `verify_leaves.py` or the author's `verify_exact.py` with angle multipliers set to 0, in a
     /tmp copy. Cost: 1–3 CPU-minutes. Keep the cited value 41869.05148485014 either way.
4. **(minor; resolved here) 0030p relaxation previously had a single OSIL reader.**
   - The author and the wave-3 verifier both used `osilx`; the 0039 review's independent reader
     was never run on 0030p.
   - My run of that reader (`r2/cmp_rows_0030p.log`) reproduces all rows exactly. The exact
     GAMS = OSIL comparison also confirms the parse against an independent text.
   - *Resolution:* cite these; if desired, have the next reviewer rerun the two scripts
     (seconds).
5. **(minor) Interval-Cholesky code is not a proof.**
   - `pf_cert.interval_cholesky` uses hand-coded float error padding.
   - *Resolution:* the paper cites only the exact PSD proofs. Every cited bound is reproduced
     or exceeded by them.
6. **(minor) Reproducibility of 0030p.**
   - A fresh SDP solve on the pinned stack gives 576.8905424271796, below the cited bound. The
     certificate is the stored multiplier file.
   - *Resolution:* the artifact ships `*.sdpcert.json` and `*.bb3t.json` with SHA-256 values,
     and the text describes verification as *replay*.
   - Optional: re-solve the 0030p dual SDP at Clarabel tolerance 1e-10 (about 5–20 s) and replay
     exactly (under 1 s). This would make the certificate regenerable; it is not needed for
     validity.
7. **(minor) Scope and provenance.**
   - The models are not MATPOWER case30/case39: shunts and taps are dropped, and the angle
     limit is 0.26. The bounds do not transfer to MATPOWER or to 0030r.
   - *Resolution:* write "for the MINLPLib models as distributed". Cite the shunt/tap evidence
     and the 576.8923368 counterexample to transfer.
8. **(minor) Bus numbering.**
   - `R/` notes use the 0-based "bus 29", "line 1–29"; the wave-3 summary also says "leaf
     bus 30".
   - *Resolution:* the paper uses MATPOWER numbers (bus 30, bus 2, branch 2–30) and gives the
     OSIL variable names once.
9. **(minor) Numerical statements that must stay out of theorems.**
   - They are:
     - "the rest of the network is exact" (fixed-leaf SDP at tolerance 1e-10: 41869.05150, angle
       rows dropped; diagnostic);
     - "only line 1–29 had a 2×2 defect above 1e-6";
     - the eigenvalue statements;
     - the plain-SDP gap of 0039 (§3.8);
     - the explanation of the pf_bb2 stall;
     - the GAMS CONOPT/IPOPT local solves.
   - *Resolution:* label them as diagnostics. The 0030p Shor tightness (§3.8) is rigorous and
     may be stated.
   - To make the 0039 plain-SDP gap rigorous, one would need a rigorous upper bound on
     val(Shor(R)): a rigorously feasible primal (W, y) near 41867.7797. That needs a VSDP-type
     primal certificate with the equalities handled (for example by an exact projection onto the
     affine constraints plus a PD margin). Estimated work: half a day of coding and seconds of
     compute. It is not needed for any claim.
10. **(minor) Positioning of the leaf cut.**
    - Rank-one 2×2 convex-hull cuts with box bounds (Chen–Atamtürk–Oren, in the KB) and
      minor-based cuts are prior art for the same object.
    - *Resolution:* present the cut as an exact identity plus its concave envelope. Cite
      Chen–Atamtürk–Oren and do not claim novelty of the cut. Reading Kocuk–Dey–Sun 2016/2018
      and Coffrin et al. 2017 (1–2 hours, no computation) would let the paper say precisely how
      the cut relates to them.
11. **(minor) MINLPLib "solved".** The S mark needs 3 solvers. *Resolution:* never say "solved
    on MINLPLib"; say "closed to a relative gap of …, certified".
12. **(minor) KB metadata errors** (`literature/`, not edited here).
    - `oustry2022-certified-and-accurate-sdp-bounds` lists "Oustry, David" and "Ruiz,
      Christian"; the paper says Antoine Oustry and Manuel Ruiz. The bib author field uses ";"
      instead of "and".
    - `josz2015-certified-moment-relaxation-for-ac` carries the title "Certified moment
      relaxation…". Its full text (arXiv 1311.6370) is "Application of the Moment–SOS Approach to
      Global Optimization of the OPF Problem" (IEEE TPS 30(1), 2015).
    - *Resolution:* take bibliographic data from the network report's bibliography (§10) and fix
      the KB in a literature pass.

**Assumptions that could be removed.** Only (T6), by item 3. The ε shifts are rigorous and
cost at most 4.4e-7. They could be removed only with new multipliers, which is not worth doing.
No missing proof step was found.

### 8.4 Corrections to the first-pass dossier (same path, earlier today)

- It said that the 0039r display 41869.05148327244 exceeds the certificate "by 6e-15". The
  correct value is **6.03e-12** (`r2/gaps.log`).
- It said that Oustry et al. is "not in `literature/papers`" and that Chen–Atamtürk–Oren is not
  in the local KB. Both are present (`oustry2022-certified-and-accurate-sdp-bounds`,
  `chen2016-a-spatial-branch-and-cut`). So are VSDP/Jansson, Hijazi 2014/2017, Bingane, NESTA
  and Neumaier–Shcherbina.
- It listed the second independent OSIL reader as covering all three instances. For the 0030p
  dual it did not until this pass (item 4).
- Its other numbers agree with my recomputations.

## 9. What the paper may and must not claim

**May claim** (suggested wording):

- "For the MINLPLib models powerflow0030p, powerflow0039p and powerflow0039r as distributed (the
  OSIL and GAMS files define identical expressions), every exactly feasible point has objective
  at least 576.8934122988004, 41869.05148485014 and 41869.05148327243, respectively. Each model
  has an exactly feasible point with objective at most 576.8934134704, 41869.0515113203 and
  41869.0515113210. The optimal values are therefore enclosed to relative widths of at most
  2.1e-9, 6.4e-10 and 6.7e-10."
- "The lower bounds follow from weak Lagrangian duality for a quadratic relaxation. They are
  evaluated in exact rational arithmetic from stored multipliers, with an exact
  positive-semidefiniteness certificate. For the 39-bus instances we add an exact identity at a
  leaf generator bus, concave-envelope cuts derived from it, and a branch and bound over three
  coordinates (6 and 9 leaves). No floating-point error analysis enters the dual bounds."
- "All bounds and points were re-verified with independently written code, including
  independent OSIL readers."
- "To the best of our knowledge, these are the first rigorous bounds that close these three
  MINLPLib instances." Add the precedents:
  - for 0030p: its rectangular twin powerflow0030r had been closed in floating point by
    ANTIGONE, and MATPOWER case30 with shunts has a numerically exact SDP relaxation;
  - for 0039p/r: MATPOWER case39 with transformer taps was solved globally in floating point by
    Ghaddar, Mareček and Mevissen (2016).
- "For powerflow0030p the Shor relaxation is provably tight to 2.1e-9 relative."
- "For powerflow0039p/r, branching on the three coordinates of a single leaf branch suffices to
  close the gap." This is an observation supported by the certificate; do not state it as a
  property of the SDP.
- "Certified SDP lower bounds for ACOPF follow the approach of Jansson et al. and Oustry et
  al.; our contribution here is their exact application to these models and the leaf identity."

**Must not claim:**

- that the bounds apply to MATPOWER case30 or case39, or to powerflow0030r through 0030p;
- exact optimality or a zero gap;
- that the instances are now "solved on MINLPLib";
- novelty of certified SDP bounds for ACOPF in general, or novelty of rank-one/envelope cuts;
- that the 0039 plain-SDP gap (3e-5) is proved;
- that "the rest of the network is exact" or that only branch 2–30 is defective, as proved
  facts;
- that a fresh numerical solve reproduces the 0030p certificate;
- the display 41869.05148327244, or any p1-based gap as a rigorous gap;
- "previously unsolved globally" without the floating-point precedents above;
- that solvers fail on these instances in general (the campaign covers one budget and one
  setting);
- the wave-3 0039 values 41868.26524 and 41867.77921 (superseded; the first is not
  reproducible).

## 10. Candidate figures and tables

1. **Table: instances and provenance.**
   - Sizes (§1.2).
   - Differences from MATPOWER (shunts, taps, angle limit 0.26).
   - GAMS = OSIL.
   - Listed duals and S status (§2).
2. **Table: numbers** (§5): listed dual, plain-SDP root, final dual, exact primal enclosure and
   gap. Placing the plain-SDP root next to the final bound shows where the leaf B&B matters.
3. **Figure: the leaf mechanism.**
   - Panel (a): schematic of bus 2, transformer 2–30 and generator bus 30, with
     Pg ∈ [0, 10.4], Qg ≥ 1.4 and v₃₀ ≤ 1.06 marked as binding.
   - Panel (b): along Pg at Qg = 1.4 and W_LL = 1.1236, the true W_NN = F, the SDP region
     W_NN ≥ F, and the vertex-plane upper bound on the root interval [0, 10.4] and on the
     decisive leaf. The root envelope error is (Pg − 0)(10.4 − Pg)/(b²W_LL) ≈ 7.2e-3 at
     Pg = 6.714, against a defect of 5.1e-3.
4. **Figure: leaf partitions.**
   - 0039p (6 leaves) and 0039r (9 leaves), projected on (Pg, W_LL), with the Qg splits
     annotated.
   - Colour by β_i − min β on a log scale, and mark the exact point.
5. **Figure: B&B progress** (from `ext/logs/*.bb3t.log`). Plot the certified lower bound
   against nodes, with the exact primal enclosure as a horizontal line.
   - 0039p: root 41867.77970; node 3 41869.04903; nodes 5–9 41869.05055; node 11
     41869.05148.
   - 0039r: root 41867.77970; node 3 41869.04903; node 5 41869.04986; nodes 7–9 41869.05098;
     node 11 41869.05124; nodes 13–15 41869.05124; node 17 41869.05148.
6. **Table: verification matrix** (§6).
   - Rows: OSIL reading, R, multipliers and Lagrangian, PSD, planes, coverage, primal.
   - Columns: the author and each independent check, with method and arithmetic.
7. *(optional)* **Box: the certificate recipe.** Display the formula for β(w, ε) with Lemma 3,
   as a template for certified Lagrangian bounds on other MINLPLib QCQPs.
