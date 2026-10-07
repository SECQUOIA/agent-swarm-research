# Dossier: small models (family key `small`)

Instances: hvycrash, ex6_2_7, ex6_2_5, etamac, pricing050, pindyck.

Prepared 2026-10-04 for the MPC paper. `R/` means
`/workspace/minlp-notes/research-20260929/`. The authoritative
numbers are the rows of `R/open-instances-summary.md` for these instances
(table lines 40–44 and 50). Checks run for this dossier are in
`paper-open-minlplib/development/dossiers/small-checks/` (scripts, logs,
`run.sh`, which copies inputs to a fresh `/tmp` directory). Nothing under
`R/` or `literature/` was modified, and no long computation was rerun.

Status words used below:
- **proved**: a complete pen-and-paper proof;
- **computer-assisted**: a proof whose finite part is a computation in
  outward-rounded interval or exact rational arithmetic;
- **independently implemented**: the computation was redone by separate code;
- **numerical**: floating-point or high-precision evidence without enclosure.

## 0. Overview

| instance | sense; vars/rows | mechanism | status of the dual claim |
|---|---|---|---|
| hvycrash | min; 201/150 | the rows force a constant objective (exact identity); explicit feasible point | proved; this dossier gives a fully analytic existence proof (Section 3.1); two codes also verified it with intervals |
| ex6_2_7 | min; 9/3 | Lagrangian over the 3 mass balances; Gibbs tangent-plane test by 2-D interval branch and bound | computer-assisted; two implementations; the displayed tight value comes from the reviewer's implementation alone |
| ex6_2_5 | min; 9/3 | same, plus a closed form for the ideal vapour phase | same |
| etamac | min; 97/70 | convex relaxation (production equalities to ≤, with a concave majorant), then Lagrangian tangent plane at one point | computer-assisted; two implementations; displayed value from the reviewer's |
| pricing050 | max; 50/5 | Lagrangian over the 5 rows; 50 certified 1-D minimizations | computer-assisted; three implementations (the third in this dossier) |
| pindyck | min; 116/96 | reduced objective J(p) is 0.001-strongly concave on a polytope G that contains the feasible prices; tangent-plane bound at the KKT point | computer-assisted (exact-rational LP weak duality, Taylor models or affine forms, exact LDLᵀ test); two implementations |

None of these certificates uses the eg_* assumptions A1/A2. The common trust
base is mpmath's interval arithmetic (`iv`: arithmetic, exp, log, cos, sqrt,
and outward conversion), Python `Fraction`, and, for etamac and the Gibbs
instances, sympy's symbolic differentiation and expression compilation.
Section 6 lists the details.

## 1. Instances and models

### 1.1 hvycrash

**Source.** CUTE problem HVYCRASH (SIF file by Ph. Toint, 1994) at N = 50,
which the SIF file calls the "original value". It reached MINLPLib on
2017-02-06 through Yurttan's AMPL translation ("CUTE model hvycrash";
references Ivashkevich 1976 and Tyatushkin, Zholudev and Erinchek 1992).
According to its header, the SIF problem is "freely inspired by" a
heavy-spacecraft landing problem. Because no package found a feasible point
of the original formulation, the SIF problem drops a final-state constraint
and sets EPS = 0; the header calls the result "badly scaled degenerate". We
make no physical claim.

**Size.** 201 continuous variables, 150 equality rows, minimization, NLP.

**Variables (OSIL names).** For k = 1..50:
- θ_k = x_k ∈ [0, 6.2831854], and θ_0 = x101 ∈ [0, 6.2831854];
- c_k = x_{50+k} ∈ [0.08, 0.417];
- r_k = x_{101+k} and s_k = x_{202−k} are free.

The objective is s_50 = x152.

**Model.** Let h = 0.00437, E(c) = 0.01 + 0.3c², D(c) = 0.0162079 +
0.486237c² (= 1.62079·E(c)) and A(c) = c/E(c). Set s_0 := 0. For
k = 1..50 the rows are:

- (acc_k) h·cos θ_k /(D(c_k) r_k²) − s_k + s_{k−1} = 0;
- (alg_k) −1/r_k − cos θ_k /(D(c_k) r_k³) = 0;
- (dyn_k) h·A(c_k)/r_k² − h·cos θ_k /(D(c_k) r_k⁴) − 0.1θ_k + 0.1θ_{k−1} = 0.

The problem is min s_50.

**Structure.** alg_k forces cos θ_k /(D r_k²) = −1. This fixes every
accumulator increment. The difficulty for solvers is the free r_k inside the
divisions, which makes termwise relaxations unbounded.

**Provenance.**
- The literature track checked that the decoded SIF problem at N = 50 is the
  MINLPLib model:
  - bounds were compared by code;
  - rows were compared at 20 random points × 150 rows, with maximum
    difference 2.1e-48 (`R/publication/reviews/lit-small-r2/`).
- In the SIF BOUNDS section, the XX cards that fix θ_0 and θ_N at 0 have no
  effect. A later loop overrides them, because SIFDecode lets a later bound
  card overwrite an earlier one.
- The GAMS World PrincetonLib file is a different variant: its bounds are
  shifted by 0.005. By the identity below, its objective would be constant
  at −0.2135. Its feasibility was not checked.

### 1.2 ex6_2_7 and ex6_2_5 (Gibbs free-energy minimization)

**Source.** Floudas et al., *Handbook of Test Problems* (1999), Chapter 6,
Test Problems 7 and 5, through GLOBALLib (MINLPLib, 2001-07-31). The
MINLPLib pages cite McDonald and Floudas (1997, GLOPEQ).
- ex6_2_7: ethylene glycol, lauryl alcohol and nitromethane; three liquid
  phases (UNIQUAC); T = 295 K; feed b = (0.4, 0.1, 0.5).
- ex6_2_5: sec-butyl alcohol, di-sec-butyl ether and water; two UNIQUAC
  liquid phases and an ideal vapour; P = 1.16996 atm; feed
  b = (40.30707, 5.14979, 54.54314).

**Size.** 9 variables n_{p,i} (phase p, component i) in [1e-7, b_i] and 3
linear equality rows. Minimization, NLP.

**Model.** Minimize f(n) = Σ_p G_p(n_p) subject to Σ_p n_{p,i} = b_i for
i = 1, 2, 3.
- Each G_p is a finite sum of terms of three kinds, all involving only the
  amounts n_p of phase p:
  - α·n_i;
  - α·n_i ln n_i;
  - α·ℓ(n_p) ln m(n_p), where ℓ and m are linear forms with nonnegative
    coefficients and m > 0 on the positive orthant.
  
  This is the expanded GAMS-Convert form of the UNIQUAC combinatorial and
  residual terms.
- ex6_2_7: G_1 = G_2 = G_3, with 26 terms each.
- ex6_2_5: G_1 = G_2 (29 terms each), and the vapour phase is
  G_3(n) = Σ_i n_i (ln(n_i/Σ_k n_k) + 0.156969560191053). The constant is
  ln P.

**Structure.**
- No term mixes phases.
- The only coupling is the three linear mass balances.
- Each G_p is homogeneous of degree 1, exactly in ex6_2_5 and up to 5e-14 in
  ex6_2_7 (Lemma 2.1).

**Provenance.**
- The MINLPLib file equals the GLOBALLib scalar file.
- The literature track re-implemented the objective from the handbook's GAMS
  source. It agrees with the MINLPLib objective to ≤ 4.1e-14 (ex6_2_7) and
  ≤ 9.4e-14 (ex6_2_5) relative, at 200 random points.
- The constants are rounded to about 15 digits. In ex6_2_7 this rounding
  leaves a non-homogeneous residual on component 3:
  8.73945638067505 + 1.868 − 10.607456380675 = 5e-14 (checked in exact
  rationals; `small-checks/gibbs_assembly.log`).

### 1.3 etamac

**Source.** GAMS Model Library model etamac (SEQ=80), "Eta-Macro Energy Model
for the USA", after Manne's ETA-MACRO (1977). The MINLPLib file has the same
GAMS text as the GLOBALLib file (added 2001-07-31). It was not compared with
Manne's text, which was not obtained.

**Size.** 97 variables and 70 rows: 60 linear equalities, 9 nonlinear
production equalities and 1 linear inequality. Minimization, NLP.

**Model.** For t = 1..9, write g = 4.91287681 and δ = 0.8153726976.
- **Objective.** Minimize f = −Σ_t β_t ln C_t, with all β_t > 0
  (β_9 = 3.98240565033479 is the terminal weight).
- **Linear rows:**
  - KN_t = g·I_{t−1} (t = 2..9);
  - K_t = δK_{t−1} + KN_t, Y_t = δY_{t−1} + YN_t, L_t = δL_{t−1} + LN_t
    and E_t = δE_{t−1} + EN_t (t = 2..9);
  - L_1 = LN_1 + 2.038431744 and E_1 = EN_1 + 40.76863488;
  - 1000·EC_t = cL_t L_t + cE_t E_t, with cL_t, cE_t > 0;
  - Y_t = C_t + I_t + EC_t;
  - 0.07·K_9 ≤ I_9.
- **Production rows:**
  - YN_t = Φ_t := (a_t KN_t^{−p1} + b·LN_t^{−p2} EN_t^{−p3})^{−q} for t = 2..9;
  - Y_1 = 3.4653339648 + (b·LN_1^{−p2} EN_1^{−p3} + c0)^{−q}.
  
  The constants are p1 = .342222222222222, p2 = .427777777777778,
  p3 = .794444444444445, q = .818181818181818, b = .306708090151268,
  c0 = .612508399277048 and a_t ∈ (0.33, 0.83).
- **Bounds.** K_1 = 12.32657617084 is fixed. EC_t is free. Every other
  variable has a positive lower bound and no upper bound.
- **Labels.** K, KN, Y, YN, C, I and EC are capital, new capital, output, new
  output, consumption, investment and energy cost. L, E, LN and EN are the
  verification scripts' labels for the two priced inputs of the second CES
  nest and their new vintages. In ETA-MACRO these are presumably the two
  energy forms; we did not check this against Manne's text.

**Structure.**
- f is convex.
- Every row except production is linear.
- Φ_t is a CES function. Relaxing the production equalities to ≤ would give
  a convex program if Φ_t were concave ("hidden convexity").

**Provenance at the decimal level.**
- The decimals are evidently 0.28·11/9, 0.35·11/9, 0.65·11/9 and 9/11,
  rounded to 15 digits. So p1·q = 0.27999999999999975, and the degree of the
  LN–EN Cobb–Douglas aggregate is s = (p2 + p3)q = 1 + 4.14e-16 instead of 1
  (exact rational check, `small-checks/etamac_check.log`).
- Hence LN^{p2 q} EN^{p3 q} is **not** concave in the stored model. The
  scout's statement that the CES is concave is false at the 4e-16 level. The
  certificate handles this exactly (Lemma 3.2).

### 1.4 pricing050

**Source.**
- This is the continuous version of the marketing pricing model of Davarnia
  and van Hoeve (2021, Math. Program.) with n = 50. M. Kiaghadi contributed it
  to MINLPLib on 2024-03-25.
- There is strong, but not conclusive, evidence that it is their n = 50
  instance #2: the MILP optimum of the integer version is 1825.0, the value
  reported for #2. This rests on one floating-point HiGHS solve.

**Size.** 50 variables x ∈ [0, 10]^50 and 5 nonlinear ≤ rows with 249
univariate terms. Maximization, NLP.

**Model.** Maximize −Σ_j c_j x_j subject to
Σ_j a_ij x_j exp(g_ij x_j^{p_ij}) ≤ r_i for the rows i ∈ {e2, …, e6}.
- c_j ∈ {0, …, 20}. 46 are positive; x5, x10, x27 and x43 have zero cost.
- a_ij ∈ [−10, −0.1] (one decimal).
- p_ij ∈ {1, 2, 3}, with 78, 94 and 77 terms respectively.
- g_ij = −0.1, −1.0000000000000002e-2 and −1.0000000000000002e-3 for
  p = 1, 2, 3.
- r = (−500, −651, −615, −788, −984).
- Row e5 has no x21 term.

In minimization form: minimize the weighted price sum c·x subject to the
profit margins Σ_j |a_ij| x_j e^{−(x_j/10)^{p_ij}} ≥ |r_i|.

**Structure.** Every term depends on one variable and the objective is
linear, so the Lagrangian separates into 50 one-dimensional functions.

**Provenance.** The g values are the binary64 renderings of 0.1² and 0.1³.
The GAMS file has the same decimals. Certificates use these exact decimals.

### 1.5 pindyck

**Source.** GAMS Model Library model pindyck (SEQ=28), "Optimal Pricing and
Extraction for OPEC", after Pindyck (1978). The MINLPLib file has the same
GAMS text as the GLOBALLib scalar model (added 2001-07-31).

**Size.** 116 variables and 96 equality rows. Minimization, NLP.

**Model.** For t = 1..16:
- prices p_t ≥ 0;
- total demand: td_t = 0.87·td_{t−1} − 0.13·p_t + c_t, with td_0 = 18 and
  c_t = 3.3, 3.3345, …, 3.87553375330505;
- fringe supply: s_t = 0.75·s_{t−1} + 1.02^{−k·cs_t}·(1.1 + 0.1·p_t), with
  k = 0.142857142857143 and s_0 = 6.5;
- cumulative supply: cs_t = cs_{t−1} + s_t, with cs_0 = 0;
- OPEC demand: d_t = td_t − s_t ≥ 0;
- reserves: R_t = R_{t−1} − d_t, with R_0 = 500;
- profit: π_t = (p_t − 250/R_t)·d_t.

The objective is min −Σ_t δ_t π_t, where δ_t are 15-digit decimals of
1.05^{−(t−1)}. All variables except π_t are ≥ 0. Write K = k·ln 1.02, using
the decimal k, not 1/7.

**Meaning.** OPEC chooses prices. Total demand responds with a lag. Fringe
supply rises with price and falls with cumulative fringe output (depletion).
OPEC sells the residual demand d_t, and its unit cost 250/R_t rises as its
reserves R_t fall.

**Structure.**
- Given p, every other variable is determined. The supply equation
  s − a − b·e^{−Ks} = 0, with b = (1.1 + 0.1p_t)e^{−K cs_{t−1}} > 0, has a
  strictly increasing left side, so it has exactly one root.
- So the problem is: maximize J(p) = Σ_t δ_t d_t(p)(p_t − 250/R_t(p)) over
  F = {p ≥ 0 : d_t(p) ≥ 0 for all t}.

**Provenance.** COCONUT's GAMS translation loses the factor 1/7 in the
exponent, so it is a different model (Section 7).

### 1.6 OSIL against GAMS

For all six instances, the unmodified MINLPLib `.gms` files (copies in
`R/publication/solver-runs/gms/`, byte-identical to the literature track's
copies) were compared with the OSIL files. At 5 random points per instance,
in 50-digit evaluation, all rows and objective rows agree to ≤ 3.5e-51
relative (`small-checks/gms_vs_osil.log`). This is numerical evidence of
identity, not an algebraic proof.

The OSIL/GAMS coefficient differences found for catmix, methanol50 and
lop97icx do not occur here. The status refresh found the model files
unchanged since the 2014–2017 copies (pricing050: since 2024)
(`R/publication/minlplib-status/report.md`, Table B1).

## 2. Listed MINLPLib status

All six are open on MINLPLib: there is no solved mark, and `minlplib.solu`
has `=best=`, not `=opt=`. The pages were fetched on 2026-09-29/30; the
2026-10-02 refresh found them unchanged.

| instance | listed primal (point; infeasibility) | best listed single-solver dual (solver, date) | `.solu` `=bestdual=` |
|---|---|---|---|
| hvycrash | −0.2185 (p3, COUENNE; 1e-12); p1, p2 = −0.21413 | −218500000 (SCIP, 2022-02-15) | none |
| ex6_2_7 | −0.16084762 (p1, CONOPT 2014; 6e-17) | −1.06726714 (BARON, 2017-09-13) | −1.354737094 |
| ex6_2_5 | −70.75207783 (p1, CONOPT 2014; 7e-15) | −111.4201713 (BARON, 2017-09-13) | −364.1162233 |
| etamac | −15.29467564 (p1, CONOPT 2014; 1e-10) | −15.40567054 (SCIP, 2025-07-31) | −16.3990195 |
| pricing050 (max) | −1813.829078 (p1, KNITRO, contributed 2024; 7e-10) | −1534.3281 (SCIP, 2025-07-31; an upper bound) | −1153.003281 |
| pindyck | −1170.486285 (p1, CONOPT 2014; 6e-14) | −1437.941134 (SCIP, 2018-05-23) | −1889.888367 |

Sources:
- `R/open-instances-scout/fetched.csv`;
- `R/reviews/wave2-small-verification/pages/` (`instances.html`,
  `minlplib.solu`);
- `R/publication/minlplib-status/data/tables.md`;
- `R/publication/literature/small/report.md`, Section 2.

The paper uses the instance-page single-solver values. The `.solu`
`=bestdual=` values are weaker for all six.

## 3. The certificates

### 3.1 hvycrash: the objective is constant (proved)

**Idea.** Each "algebraic" row alg_k says exactly that the term added to the
accumulator in acc_k equals −h. So s_50 = −50h on the whole feasible set.
Feasibility is shown by building a point backwards from θ_50.

**Theorem 1.**
1. Every feasible point of hvycrash has objective s_50 = −0.2185 =
   −437/2000.
2. The feasible set is not empty.

Hence the optimal value is exactly −0.2185, it is attained, and every
feasible point is optimal.

*Proof of 1.* At a feasible point every row is defined, so r_k ≠ 0.
Multiplying alg_k by −r_k gives

  cos θ_k /(D(c_k) r_k²) = −1.   (∗)

Then acc_k reads s_k = s_{k−1} − h. With s_0 = 0, this gives
s_50 = −50h = −0.2185.

*Proof of 2* (new in this dossier; analytic). Under (∗),
cos θ_k /(D r_k⁴) = −1/r_k². So dyn_k becomes
θ_k − θ_{k−1} = 10h(A(c_k) + 1)/r_k², and by (∗),
1/r_k² = D(c_k)/(−cos θ_k). Define the point as follows:
- c_k = 0.08 for all k, and κ := 10h(A(0.08) + 1)D(0.08). Here
  A(0.08) = 1000/149 and D(0.08) = 0.0193198168, so
  κ = 0.0065105578… < 0.006511.
- θ_50 = 3, and θ_{k−1} = θ_k − κ/(−cos θ_k) for k = 50, …, 1.
- r_k = (−cos θ_k / D(0.08))^{1/2} and s_k = −kh.

Whenever cos θ_k < 0, these definitions make alg_k, dyn_k and acc_k hold
exactly.

We claim θ_k ∈ [2.6, 3] for all k, by downward induction. Suppose
θ_50, …, θ_k ∈ [2.6, 3]. Then:
- These angles lie in [2.6, 3] ⊂ (π/2, π), because 3 < 223/71 < π.
- cos is decreasing on [0, π], so −cos θ_j ≥ −cos 2.6 > 0.85 for j ≥ k.
- Hence θ_{k−1} = 3 − Σ_{j=k}^{50} κ/(−cos θ_j) ≥ 3 − 50κ/0.85 > 3 − 0.383
  > 2.6, and θ_{k−1} < θ_k ≤ 3.

So every θ_k lies in [2.6, 3] ⊂ [0, 6.2831854], every cos θ_k is negative,
so every r_k is real and nonzero, and c_k = 0.08 is within its bounds. ∎

The facts used are cos 2.6 = −0.85688875…, bracketed by alternating Taylor
partial sums, and π > 223/71 (`small-checks/hvy_analytic.log`). The
constructed point has θ_0 = 2.6565078758566084090…, the same as the author's
interval run (`R/open-instances-wave2/small/logs/hvycrash.log`). The
dossier's own OSIL evaluator confirms all 150 rows and all bounds on
60-digit interval enclosures of this point (`small-checks/own_osil_checks.log`).

**Remark (feasible-set structure).** On the feasible set, θ_k is strictly
increasing in k and cos θ_k < 0 for k ≥ 1.

**Remark (tolerance; explains the listed points).** Suppose every row holds
only within absolute tolerance τ. Then alg_k gives
cos θ_k /(D r_k²) = −1 − e_k r_k with |e_k| ≤ τ. An increment below −h
requires |cos θ_k /(D r_k²)| > 1, hence r_k² < 1/D ≤ 1/0.0162079, that is,
|r_k| < 7.86. So s_50 ≥ −0.2185(1 + 7.86τ) − 50τ. The opposite artifact
occurs in the listed points p1 and p2: there r_50 is 2.5e7 or 1.6e9, stage
50's increment is ≈ 0, and the objective is −0.2185 + h = −0.21413. The
listed SCIP bound −2.185e8 is valid but is 1e9 times the optimum; it is not
a tolerance effect.

### 3.2 ex6_2_7 and ex6_2_5: mass-balance Lagrangian and tangent-plane test (computer-assisted)

**Idea.** Price each component with a chemical potential λ_i. Because of the
mass balances, f(n) = λ·b + Σ_p [G_p(n_p) − λ·n_p], and each bracket depends
on one phase only. Homogeneity reduces each bracket to the "tangent-plane
distance" G_p(y) − λ·y on the composition simplex. If λ are the equilibrium
chemical potentials, this function is ≥ 0, with zeros at the equilibrium
phase compositions. A rigorous 2-D interval branch and bound proves
G_p(y) − λ·y ≥ −τ with τ tiny.

**Lemma 2.1 (scaling; exact).** For t > 0 and n > 0,
G_p(t n) = t·G_p(n) + t ln t·⟨r_p, n⟩, where:
- r_p = 0 for every phase of ex6_2_5;
- r_p = (0, 0, 5e-14) for every phase of ex6_2_7.

*Proof.* Under n ↦ tn:
- α n_i becomes t·α n_i;
- α n_i ln n_i becomes t·α n_i ln n_i + t ln t·α n_i;
- α ℓ(n) ln m(n) becomes t·α ℓ ln m + t ln t·α ℓ(n).

So r_p collects, for each component, the coefficients of the terms that
carry a logarithm. Summing them exactly from the OSIL decimals gives 0 for
components 1 and 2 of ex6_2_7. For example, for component 1:
10.4807341082197 + 2.248 − 12.7287341082197 = 0. For component 3 the sum is
8.73945638067505 + 1.868 − 10.607456380675 = 5e-14. For ex6_2_5 every sum
is 0. The independent reviewer also verified the identity
G_p(ty) − tG_p(y) − t ln t·R_p(y) ≡ 0 symbolically, with exact rationals
(`R/reviews/wave2-small-verification/gibbs_sym.py`). ∎

**Lemma 2.2 (ideal phase).** For G(y) = Σ_i y_i (ln y_i + c) on the simplex
and any λ: G(y) − λ·y ≥ −ln Σ_i exp(λ_i − c).

*Proof.* Let π_i = e^{λ_i − c}/Z with Z = Σ_i e^{λ_i − c}. Then
G(y) − λ·y = Σ_i y_i ln(y_i/π_i) − ln Z ≥ −ln Z, because the Kullback–Leibler
divergence is nonnegative. ∎

**Proposition 2.3 (dual bound).**

*Hypotheses.* Let T = Σ_i b_i, ε ≤ 1e-7/T and
Δ_ε = {y ∈ R³ : y_i ≥ ε, Σ_i y_i = 1}. Take any λ ∈ R³ and numbers
m_p ≤ inf over y ∈ Δ_ε of [G_p(y) − λ·y]. Assume r_p ≥ 0 componentwise.

*Conclusion.* Every feasible n satisfies

  f(n) ≥ λ·b + Σ_p [ min(0, T·m_p) − max_i r_{p,i}/e ].

*Proof.*
1. Because Σ_p n_p = b, f(n) = λ·b + Σ_p [G_p(n_p) − λ·n_p].
2. Fix p and set t = Σ_i n_{p,i}. Then t ∈ (0, T], since n_{p,i} ≤ b_i.
   Set y = n_p/t. Each y_i = n_{p,i}/t ≥ 1e-7/T ≥ ε, so y ∈ Δ_ε.
3. By Lemma 2.1, G_p(n_p) − λ·n_p = t[G_p(y) − λ·y] + t ln t·⟨r_p, y⟩.
4. The first term is ≥ t·m_p ≥ min(0, T·m_p).
5. ⟨r_p, y⟩ ∈ [0, max_i r_{p,i}] and t ln t ≥ −1/e, so the second term is
   ≥ −max_i r_{p,i}/e. If t ln t ≥ 0, the term is ≥ 0.

The upper bounds n ≤ b are not used. ∎

**What is computed.**

*Choice of λ.* λ is a decimal vector (20 digits) from a tangent-plane LP on
a simplex grid, refined by 60-digit Newton on the 12×12 KKT system. Any λ
gives a valid bound.
- ex6_2_7: λ = (−0.23993666802341555716, −0.54068374800661316808,
  −0.021609146907096643708).
- ex6_2_5: λ = (−0.92114611232187116319, −2.2777893037791928146,
  −0.40139310690864392314).

*Bounds m_p (reviewer's implementation, `gibbs_bb.py`).*
- The domain {(y1, y2) : y1, y2 ≥ ε, y1 + y2 ≤ 1 − ε} is covered by a grid of
  root boxes. A box is discarded only if the exact test
  y1_lo + y2_lo > 1 − ε shows it has no feasible point.
- y3 = 1 − y1 − y2 is enclosed per box and clipped to [ε, 1].
- Each box is fathomed when the best of three lower bounds is ≥ −τ:
  - the natural interval extension;
  - the mean-value form at a feasible centre;
  - an exact 2×2 quadratic bound D(c) − ½gᵀQ⁻¹g, using the end-point
    matrices of the interval Hessian when both are positive definite, and a
    separable bound otherwise.
- Box enclosures use 53-bit `iv`; centre values use 40 digits. G, ∇G and ∇²G
  are sympy derivatives of the OSIL trees compiled to `iv`.
- ε = 9.9e-8 (ex6_2_7) and 9.9e-10 (ex6_2_5) are slightly below 1e-7/T.

Results:
- ex6_2_7: τ = 6e-15, 42,111 boxes (one phase type).
- ex6_2_5 liquid: τ = 1e-17, 131,111 boxes.
- ex6_2_5 vapour: Lemma 2.2 gives m = 6.978e-22 > 0, so its contribution is
  0 (`small-checks/gibbs_assembly.log`).

*Assembly (rechecked exactly in this dossier).*
- ex6_2_7: λ·b = −0.160847615463575861526 (exact). The bound is
  λ·b − 3·6e-15 − 3·(5e-14)/e ≥ **−0.16084761546364904344…**.
  The bound lies 7.3e-14 below λ·b, and the R_p term accounts for 5.5e-14
  of this. That alone exceeds the final gap of 4.8e-14 (the primal point
  lies 2.5e-14 below λ·b). The R_p term is an artifact of the 15-digit
  constants.
- ex6_2_5: λ·b = −70.7520778334477055803539469 (exact). The bound is
  λ·b − 2·100·1e-17 = **−70.7520778334477075803539469**.

**Trusted.** mpmath `iv` (arithmetic, log, outward conversion), sympy
differentiation and the `ivgen` compiler, and the OSIL reader `osilx.py`.
The authors' separate implementation (`gibbs.py`) uses numpy intervals
widened by one ulp and a self-written rigorous log (`ia.ilog`). It certifies
τ = 1e-11, hence the weaker bounds −0.16084761549352554 and
−70.752077836333563.

### 3.3 etamac: concave majorant and Lagrangian tangent plane (computer-assisted)

**Idea.** The objective is convex, the coupling rows are linear, and the
production functions are (almost) concave. Relaxing YN = Φ to YN ≤ Φ̃, with
Φ̃ a concave majorant, gives a convex program R that contains the feasible
set. For a convex program, the Lagrangian at a KKT point is a global
underestimator; its tangent plane at a decimal point x̂, minimized over a
valid box, gives a rigorous bound.

**Lemma 3.1 (box).** Every feasible point lies in an explicit box
B = Π_j [lo_j, hi_j]. The lower ends are the OSIL lower bounds (for EC_t:
(cL_t L_lb + cE_t E_lb)/1000). The upper ends come from a forward interval
recursion:
- Y_1 ≤ 3.4653339648 + c0^{−q};
- I_t ≤ Y_t − C_lb − EC_lb, so KN_{t+1} = g·I_t is bounded;
- YN_t ≤ a_t^{−q} KN_t^{p1 q}, obtained by dropping the nonnegative LN–EN
  term;
- Y_{t+1} = δY_t + YN_{t+1};
- then bounds on C, EC, L, E, LN, EN and K from the linear rows.

*Proof.* Each step uses one row and existing bounds. The steps do not
depend on the relaxation. ∎

The largest upper end is E_9 ≤ 2062.83, and Y_9 ≤ 26.73.

**Lemma 3.2 (concave majorant).** Let r = 1/q, s = (p2 + p3)q,
α = p2/(p2 + p3) and w = LN^α EN^{1−α}. Choose W ≥ max over B of w and
κ ≥ max(1, W^{s−1}). Define

  Φ̃_t = (a_t KN^{−p1} + b·κ^{−r}·LN^{−p2/s} EN^{−p3/s})^{−q},

and define Φ̃_1 likewise, with c0 in place of the KN term. Then:
- (a) Φ̃_t is concave and nondecreasing on the positive orthant;
- (b) Φ_t ≤ Φ̃_t on B.

*Proof.*
1. Let M(u, v) = (a u^{−r} + b v^{−r})^{−1/r} with a, b > 0 and r > 0. This
   is a weighted power mean with exponent −r < 1, so it is concave and
   nondecreasing on the positive orthant.
2. We have Φ_t = M(KN^{p1 q}, w^s) and Φ̃_t = M(KN^{p1 q}, κw), because
   (KN^{p1 q})^{−r} = KN^{−p1}, (w^s)^{−r} = LN^{−p2} EN^{−p3} and
   (κw)^{−r} = κ^{−r} LN^{−p2/s} EN^{−p3/s}.
3. KN^{p1 q} is concave since 0 < p1 q < 1. w is concave as a Cobb–Douglas
   function with exponents summing to 1. A concave nondecreasing function of
   concave arguments is concave. This proves (a).
4. Since s > 1 and 0 < w ≤ W, w^s = w·w^{s−1} ≤ κw. M is nondecreasing in
   v. This proves (b).

For Φ_1 the KN term is the constant c0, and the same argument applies. ∎

**Numbers.**
- s − 1 = 4.14e-16 > 0, so v = w^s is not concave and the majorant is
  needed.
- Reviewer: W = 1015.6000321087411 (geometric-mean bound), so
  W^{s−1} ≤ 1.0000000000000028672, and κ = 1.000000000000004.
- Authors: W = max(LN_ub, EN_ub) = 2022.06, so κ ≈ 1 + 3.152e-15.

**Relaxation R.** Replace YN_t = Φ_t by YN_t ≤ Φ̃_t, and Y_1 = 3.465… + Φ_1
by Y_1 ≤ 3.465… + Φ̃_1. By Lemmas 3.1 and 3.2(b), every feasible point of
etamac lies in B and is feasible for R.

**Theorem 3.** Let h(x) = 0 be the 60 linear equations, g̃(x) ≤ 0 the 9
relaxed production rows, and g_70 ≤ 0 the terminal row. Take any ν ∈ R^60,
any μ ∈ R^10 with μ ≥ 0, and any x̂ ∈ B. Let l = f + ν·h + μ·(g̃, g_70).
Then every feasible x satisfies

  f(x) ≥ l(x̂) + Σ_j min over ξ ∈ [lo_j, hi_j] of ∂_j l(x̂)·(ξ − x̂_j).

*Proof.*
1. A feasible x lies in B and in R. So h(x) = 0, g̃(x) ≤ 0 and g_70(x) ≤ 0.
   With μ ≥ 0 this gives f(x) ≥ l(x).
2. l is convex and differentiable on the positive region that contains B:
   f is convex, h is linear, g̃ is convex by Lemma 3.2(a), and μ ≥ 0.
3. By convexity, l(x) ≥ l(x̂) + ∇l(x̂)·(x − x̂). Minimize the right side
   coordinatewise over B. ∎

**What is computed (reviewer, `v_etamac.py`).**
- x̂, ν and μ come from a 50-digit Newton solve of R's own KKT system
  (residual 2.7e-48) and are rounded to 30 digits. The multipliers are
  positive: min μ = 0.278 and μ_70 = 0.363.
- l(x̂) and ∇l(x̂) are enclosed in `iv` at 40 digits. The Lagrangian is built
  with sympy from the OSIL rows, which are matched against templates by exact
  string comparison.
- The largest gradient entry for a free variable is 4.9e-31. ∂l/∂K_1 = 0.00496
  multiplies a zero-width range.

Result: f ≥ **−15.2946756433680921685** (displayed −15.294675643368093).

The authors' `etamac.py` used the KKT point of the unrelaxed model, so its
gradient is 1.1e-16 and its bound is weaker: −15.294675643368096.

The remaining gap, 2.6e-15, is essentially the price of κ. It is not
numerical error.

**Trusted.** mpmath `iv` (exp, log), sympy differentiation and the `ivgen`
compiler, and `osilx.py`.

### 3.4 pricing050: Lagrangian over five rows (computer-assisted)

**Idea.** Dualize the five rows. The Lagrangian separates into 50 univariate
functions, whose minima over [0, 10] are certified by 1-D interval branch
and bound. With the optimal multipliers, the dual bound equals the optimum
up to rounding (no duality gap).

**Theorem 4.** For any μ ∈ R^5 with μ ≥ 0, every feasible x satisfies

  −c·x ≤ μ·r − Σ_j min over ξ ∈ [0, 10] of F_j(ξ),
  where F_j(ξ) = c_j ξ + Σ_i μ_i a_ij ξ exp(g_ij ξ^{p_ij}).

*Proof.* For feasible x, the row values are ≤ r_i and μ ≥ 0, so
c·x ≥ c·x + Σ_i μ_i (row_i(x) − r_i) = Σ_j F_j(x_j) − μ·r
≥ Σ_j min F_j − μ·r. ∎

**What is computed.**
- Multipliers: μ_e5 = 3.0489011208166370021, μ_e6 = 2.1677509642745686136,
  and 0 for the other rows. These came from Kelley cutting planes or
  Nelder–Mead, then 50-digit Newton.
- μ·r = −4535.6010320496854734372 (exact).
- Σ_j min F_j ≥ −2721.7719535977124156872540559800… (this dossier) and
  −2721.771953597712415687255 (reviewer, 25 digits).

Upper bound: max ≤ **−1813.8290784519730577499459…**. The display
−1813.8290784519730577 is 5.0e-17 above it, so it is valid.

Three implementations exist:
1. the authors' natural/mean-value branch and bound (16,960 boxes; weaker
   result −1813.8290784519704);
2. the reviewer's monotonicity partition (2,406 pieces);
3. this dossier's natural/mean-value branch and bound with incumbent
   fathoming (4,026 boxes, 0.7 s), with its own ElementTree OSIL reader
   (`small-checks/pricing_check.py`).

Implementations 2 and 3 agree to 1e-24.

**Trusted.** mpmath `iv` exp.

### 3.5 pindyck: concavity on a polytope (computer-assisted)

**Idea.** Every state is a function of the 16 prices, so we maximize J(p)
over F. Sampled Hessians are strongly negative definite: λ_max lies in
[−0.1195, −0.1111] at 3,000 points. But F is not known to be convex, and
entrywise interval Hessians over a price box lose too much correlation.

The certificate proceeds in four steps:
1. it encloses F in a polytope G, using LP bounds certified in exact
   rationals;
2. it writes ∇²J(p) = Ψ(θ(p)), an explicit function of 112 per-period
   quantities θ;
3. it encloses θ(G) in a box Θ;
4. it proves Ψ ⪯ −0.001·I on Θ with affine (first-order Taylor) forms and a
   9-leaf branch and bound.

Then J is strongly concave on the convex set G, and the tangent plane at
the interior stationary point p* bounds J on F.

**Lemma 5.1 (reduction).**
- For p ≥ 0 the recursions have a unique solution, because the supply
  equation has a unique root.
- Every OSIL-feasible point has prices in F and objective −J(p).
- F also drops the sign constraints on td, s, cs and R, so it contains the
  projection of the feasible set.

**Lemma 5.2 (polytope).** Let α_t = td_t(0). Let CSH_t ≥ sup over p ∈ F of
cs_t(p), and e_lo,t ≤ exp(−K·CSH_t). Define, for j ≤ t,
- W_tj = 0.13·0.87^{t−j} + 0.1·0.75^{t−j}·e_lo,j;
- γ_t = 0.87^t·18 + Σ_{j≤t} 0.87^{t−j} c_j − 0.75^t·6.5
  − 1.1·Σ_{j≤t} 0.75^{t−j}·e_lo,j;
- G = {p ≥ 0 : W̲p ≤ γ̄}, with W rounded down and γ rounded up.

Then F ⊆ G.

*Proof.* For p ∈ F we have p_t ≥ 0 and e^{−K cs_t} ≥ e_lo,t. By induction,
s_t ≥ ℓ_t(p) := 0.75^t·6.5 + Σ_{j≤t} 0.75^{t−j}(1.1 + 0.1p_j)·e_lo,j. Then
d_t ≥ 0 means td_t(p) ≥ s_t ≥ ℓ_t(p), which is (Wp)_t ≤ γ_t. Rounding is
safe because p ≥ 0. ∎

CSH_t comes from six rounds of LPs in (p, s). Each LP contains every point
(p, s(p)) with p ∈ F. Each LP value is certified by weak duality in exact
`Fraction` arithmetic with finite variable bounds; HiGHS only proposes the
duals (cf. neumaier2004-safe-bounds-in-linear-and). The result is
CSH_16 = 169.273. On G, p_t ≤ p̄_t := γ_t/W_tt, which ranges from 57.41
(t = 1) to 126.15 (t = 16). p* is interior to G, with smallest slack 6.4376
(exact).

**Lemma 5.3 (Hessian map).** Let θ_t = (β_t, E_t, φ_t, d_t, u_t, R_t^{−2},
R_t^{−3}), where E_t = e^{−K cs_{t−1}}, β_t = (1.1 + 0.1p_t)E_t,
φ_t = e^{−K s_t} and u_t = p_t − 250/R_t. Let ι_t = 1/(1 + Kβ_tφ_t),
κ_t = φ_tι_t and G_t = ∇cs_{t−1}. Then ∇²J(p) = Ψ(θ(p)), where Ψ is given
by the recursion

```
∇b   = 0.1 E_t e_t − K β_t G_t
∇²b  = β_t (K² G_t G_tᵀ − K ∇²cs_{t−1}) − 0.1 K E_t (e_t G_tᵀ + G_t e_tᵀ)
∇s_t = 0.75 ι_t ∇s_{t−1} + κ_t ∇b
∇²s_t = 0.75 ι_t ∇²s_{t−1} + κ_t ∇²b − K κ_t (∇b ∇s_tᵀ + ∇s_t ∇bᵀ) + K² β_t κ_t ∇s_t ∇s_tᵀ
∇d_t = ∇td_t − ∇s_t, ∇²d_t = −∇²s_t;  ∇R_t = ∇R_{t−1} − ∇d_t, ∇²R_t = ∇²R_{t−1} − ∇²d_t
∇q_t = e_t + 250 R_t⁻² ∇R_t,  ∇²q_t = 250 (R_t⁻² ∇²R_t − 2 R_t⁻³ ∇R_t ∇R_tᵀ)
∇²J  = Σ_t δ_t (u_t ∇²d_t + d_t ∇²q_t + ∇d_t ∇q_tᵀ + ∇q_t ∇d_tᵀ)
```

with ∇td_t = −0.13·Σ_{k≤t} 0.87^{t−k} e_k (exact).

*Proof.* This is implicit differentiation of s = a + b·e^{−Ks}, with
a = 0.75·s_{t−1}, plus the product rule. This dossier verified the
implicit second-order step symbolically (`small-checks/pindyck_hess_sym.log`).
The author and the reviewer derived the recursion independently. Numerical
checks agree to 1.7e-16 with 50-digit finite differences at 12 points of G
(review), and to 1.1e-16 at p* (author). ∎

**Lemma 5.4 (matrix test).** Suppose that for all θ in a box Θ′ there is
ε ∈ [−1, 1]^K with Ψ(θ) = C + Σ_k ε_k A_k + E, where |E| ≤ R_m entrywise.
Suppose also:
- X_k ⪰ 0 and X_k ⪰ ±A_k for each k;
- ρ̄ ≥ ρ(R_m);
- −C − Σ_k X_k − (ρ̄ + μ)I ≻ 0.

Then Ψ(θ) ⪯ −μI on Θ′.

*Proof.*
1. ε_k A_k ⪯ X_k, because X_k − ε_k A_k = (1 − |ε_k|)X_k + |ε_k|(X_k ∓ A_k)
   ⪰ 0.
2. λ_max(E) ≤ ρ(E) ≤ ρ(|E|) ≤ ρ(R_m) by Perron–Frobenius monotonicity.
3. Hence Ψ ⪯ C + Σ_k X_k + ρ̄I ≺ −μI. ∎

In the computation, X_k = V|Λ|Vᵀ + e_k I, where A_k ≈ VΛVᵀ is a float
eigendecomposition and e_k ≥ ‖A_k − VΛVᵀ‖_∞. ρ̄ is a Collatz–Wielandt upper
bound. Positive definiteness is shown by an LDLᵀ factorization without
pivoting: interval-valued in the author's code, exact rational in the
review.

**Theorem 5.** Every feasible point of pindyck has objective
≥ −1170.4862854360886163931058729 (review, rounded down). Hence the display
**−1170.4862854360886163932** is a valid lower bound.

*Proof.*
1. Step 3 bounds the states over G, not F, with LPs that use tangent lines
   below e^{−K cs} and secants above it, McCormick inequalities for
   z_t = p_t e_t, and exact weak-duality certificates. Results include
   cs_16 ∈ [71.1, 158.8], R_16 ∈ [192.5, 500.9] and d_16 ∈ [−3.16, 23.48];
   d_t may be negative on G.
2. Interval arithmetic on these ranges gives a box Θ ⊇ θ(G).
3. Lemma 5.4 holds with μ = 0.001 on every leaf of a partition of Θ:
   - author: 9 leaves, after splitting u_16 once, u_15 twice, β_13 three
     times and β_12 twice;
   - review: 6 leaves on the hull of both parties' boxes;
   - the review checked the coverage of both partitions exactly.
4. So ∇²J ⪯ −0.001·I on G. J is C² on a neighbourhood of G, because
   R_t ≥ 192 > 0 and 1.1 + 0.1p_t > 0 there.
5. For p ∈ F ⊆ G, the segment [p*, p] lies in the convex set G. Taylor's
   formula with integral remainder gives
   J(p) ≤ J(p*) + ∇J(p*)·(p − p*) − (μ/2)‖p − p*‖²
   ≤ J(p*) + Σ_t |∂_t J(p*)|·max(p*_t, p̄_t − p*_t).
6. At the decimal p*, interval evaluation gives:
   - J(p*) = 1170.486285436088562087577425069288… (width 1.4e-46);
   - max_t |∂_t J(p*)| ≤ 8.008e-17 and ‖∇J(p*)‖₂ ≤ 1.844e-16.

   Here each s_t is enclosed by a verified fixed-point or interval Newton
   inclusion. Evaluating step 5 in exact rationals gives the bound. ∎

The cheap consistency check
Σ_t |∂_t J| max(p*_t, p̄_t − p*_t) ≈ 5.4304e-14 agrees with the certified
5.430553e-14.

**Corollary 5.5 (uniqueness).** The maximizer of J over F exists, is unique,
and lies within ‖·‖₂ distance 2‖∇J(p*)‖₂/μ ≤ 3.7e-13 of p*.

*Proof.*
1. F is compact and J is continuous, so a maximizer exists.
2. Any p ∈ F with J(p) ≥ J(p*) satisfies (μ/2)‖p − p*‖² ≤ ‖∇J(p*)‖‖p − p*‖.
3. p* is interior to F (min d_t = 5.44 and p* > 0), so this small ball lies
   in F, where J is strictly concave. Two maximizers in the ball would make
   their midpoint strictly better. ∎

**Trusted.**
- Author (`pindyck_global.py`, `tm1.py`): IEEE round-to-nearest numpy
  arithmetic with γ_n error allowances (a hand-checked padding analysis),
  mpmath `iv`, and `Fraction`.
- Review: rebuilt the certificate with outward-rounded affine forms
  (interval coefficients, `nextafter`) and an exact rational matrix test. Its
  proof therefore rests only on mpmath `iv` (exp, log) and `Fraction`.

## 4. Exactly feasible primal points

| instance | point | how feasibility is proved | objective |
|---|---|---|---|
| hvycrash | c_k = 0.08, θ_50 = 3, backward recursion (Section 3.1); real point with irrational coordinates | analytic (Theorem 1). Also: authors' point (same construction) and reviewer's point (c_k = 0.417, θ_50 = 4.2; θ ∈ [2.1653, 4.2], r ∈ [2.21, 3.15], cos θ ≤ −0.490), both by 50–60-digit interval arithmetic | exactly −0.2185 |
| ex6_2_7 | rational: phases 1 and 2 = 20-digit decimals of the KKT amounts; phase 3 = b − (phases 1 + 2), exactly. Listed in `R/reviews/wave2-small-verification/logs/ex6_2_7_bound.json` | rows exact and bounds exact in `Fraction`; objective enclosed in `iv` | −0.16084761546360086152447… |
| ex6_2_5 | same construction; `ex6_2_5_bound.json` | same | −70.75207783344770558036712… |
| etamac | defined by the exact real recursion of all 70 rows from 25-digit decimals of I_1..I_8, LN_t and EN_t, with I_9 := 0.07 K_9 (e70 active) | every row holds as a real identity; bound margins ≥ 0.047 proved in `iv` | ∈ [−15.29467564336808959198292336…, same + 4e-45] |
| pricing050 | authors' saved 17-digit point, `R/open-instances-wave2/small/logs/pricing050_primal.txt` (x11 raised by 1.27e-15) | **checked in this dossier** with `iv`: row slacks ≥ 3.4958e-15 (e5) and 3.917e-15 (e6); bounds exact | exactly −1813.8290784519730769 (linear objective, rational point) |
| pricing050 (reviewer) | 25-digit KKT minimizers; **not saved** to a file | `iv` row slack ≥ 1.1e-18 | −1813.8290784519730578 (20 digits) |
| pindyck | p* = 17-digit prices in `R/open-instances-wave2/small/logs/pindyck_primal.txt`; states by the exact recursion | each s_t by verified interval inclusion; min d_t = 5.437, min R_t = 350.3, min td_t = 13.99 | −1170.486285436088562087577425069288… |

**Notes on stored vectors.**
- Stored decimal vectors of the hvycrash and pindyck points are not exactly
  feasible: they violate rows by 3.9e-62 and 8.3e-28. The exactly feasible
  points are the recursion-defined real points.
- The wave-2 etamac "primal" (row violation 6.0e-14) is superseded by the
  reviewer's recursion point.

## 5. Numbers table

Gap cells are rounded upward. For max, the dual is an upper bound and the
primal display is rounded down.

| instance | listed dual | our dual (safe display) | our primal (safe display) | gap (rounded up) | relative | sources |
|---|---|---|---|---|---|---|
| hvycrash | −2.185e8 | −0.2185 (exact) | −0.2185 (attained) | 0 | 0 | Theorem 1; summary l. 40 |
| ex6_2_7 | −1.06726714 | −0.16084761546364905 | −0.16084761546360086 | ≤ 4.9e-14 (exact ≤ 4.8182e-14) | 3.1e-13 | `R/reviews/wave2-small-verification/logs/ex6_2_7_bound.json`; `R/reviews/closing-confirm-r2-checks/logs/ex6_2_5_lower_end.log` (ex6_2_7 end −0.16084761546364904344…); `R/publication/integration/gap-values.json` |
| ex6_2_5 | −111.4201713 | −70.75207783344770759 | −70.752077833447705 | ≤ 2.1e-15 (exact ≤ 2.01e-15) | 3.0e-17 | `ex6_2_5_bound.json`; closing-confirm r2/r3 (lower end −70.7520778334477075803539469) |
| etamac | −15.40567054 | −15.294675643368093 | summary: "exactly feasible point"; proposed display −15.29467564336808959 | ≤ 2.6e-15 (exact 2.5760e-15) | 1.7e-16 | `R/reviews/wave2-small-verification/logs/etamac.json` |
| pricing050 (max) | −1534.3281 | −1813.8290784519730577 (upper) | −1813.8290784519731 | ≤ 4.23e-14 (summary; subtraction of displays). Rigorous alternative: ≤ 2.0e-17 (Section 8, E5) | 2.4e-17 (1.1e-20) | `logs/pricing050.json`; `small-checks/pricing_check.log` |
| pindyck | −1437.941134 | −1170.4862854360886163932 | −1170.486285436088562 | ≤ 5.44e-14 (exact 5.4306e-14) | 4.7e-17 | `R/reviews/pindyck-review-checks/logs/final_bound.log`, `primal_check.txt` |

All displays were checked against the certified values in exact rationals
(`small-checks/gibbs_assembly.log`, `etamac_check.log`, `pricing_check.log`).

**Disagreements found.** None affects validity.

1. `R/open-instances-wave2/small/report.md`, Section 1, still shows the
   authors' weaker certificates and an etamac "gap 6.6e-15" measured against a
   point that violates a row by 6e-14. Its Section 11 and the summary supersede
   these.
2. The ex6_2_5 primal string **"−70.752077833447706"** appears in the
   reproduction README table (`R/publication/reproduction/README.md`, l. 226)
   and in the authors' log. It is a nearest rounding and lies 4.2e-16
   *below* the point's true objective. It is therefore not a safe display for
   a minimization primal. The summary's −70.752077833447705 is safe.
3. pricing050 gap: the summary says ≤ 4.23e-14 (deliberately conservative).
   The literature report says "gap 1.0e-17" (the reviewer's point). The
   reviewer's log gives 1.041e-17. All are upper bounds under their own
   conventions, but the paper should use one.
4. The authors' etamac log prints "kappa − 1 ≤ 3.11e-15". This is a 53-bit
   display artifact: mp.dps was 15 at that line. The true value for
   W = 2022.06 is κ − 1 = 3.152e-15. The certificate used the 40-digit
   interval end, and report.md correctly says ≤ 3.2e-15. This is a cosmetic
   log error only.
5. Regenerating the authors' `gibbs.py ex6_2_7 1e-11` on 2026-10-02 gave a
   different but valid bound, −0.16084761549338836 (dependent coordinate 1;
   1,153,839 boxes), instead of −0.16084761549352554 (coordinate 2; 488,064
   boxes). The cause is a different float multistart result. This is
   recorded in `R/publication/reproduction/small/manifest.json`.

## 6. Verification record

| review (date) | what it checked | verdict |
|---|---|---|
| wave-2 small verification, `R/reviews/wave2-small-verification/verification-report.md` (2026-09-30), independent verifier, own code (shares only the parser `osilx.py` with the authors) | **hvycrash:** templates for all 150 rows and 201 variables; the identity; its own feasible point in 60-digit intervals; the MINLPLib points; the tolerance remark by hand. **Gibbs:** symbolic scaling identity (sympy, exact); own multipliers (grid LP + 60-digit Newton); own mpmath 2-D branch and bound with different bounding rules, arithmetic and splitting; closed-form vapour phase; own rational primal points; sanity and negative controls (τ = 1e-17 fails for ex6_2_7, as predicted by the R_p floor ≈ −4.2e-15; perturbing λ_1 by 1e-3 fails). **etamac:** templates; exact exponents; own box from etamac's rows; own W; KKT of R itself; own bound; own exactly feasible point. **pricing050:** templates; own multipliers; own monotonicity-partition minima; own exactly feasible point (not saved). Status pages and a brief novelty search | **verified** for all five; bounds equal or tighter than the authors' |
| pindyck review, `R/reviews/pindyck-review.md` (2026-09-30), adversarial | own OSIL reader; reduction; primal enclosure (interval Newton for each s_t); own derivation of Ψ and a 12-point finite-difference check; own exact-LP ranges; proof that the author's G contains F; own affine arithmetic with interval coefficients; exact rational matrix test; own 6-leaf branch and bound; author's 9 leaves rechecked; coverage proved exactly; final bound in exact rationals; line-by-line code review | **verified**; 5 issues (gap rounding 5.43 → 5.44e-14, an overclaim about entrywise Hessians, mpmath truncation wording, the uniqueness argument, the log overwrite), all applied in text except the log side effect |
| closing confirmations r1–r3, `R/reviews/closing-confirm-r{1,2,3}.md` | direction of every displayed bound; ex6_2_5 display corrected to −…759 (lower end −70.7520778334477075803539469); etamac and pricing050 display direction | resolved |
| literature reviews r1–r3, `R/publication/reviews/lit-small-review-r{1,2,3}.md` (checks in `lit-small-r{1,2,3}/`) | provenance and prior results; r1 major M1 (SIF bounds; fixed by a bound-card decoder); r2 added Kosolap; r3 added Cuesta et al. | r3 **issues**, no blocker or major issue; minor fixes checked by the parent |
| integration review r1, `R/publication/reviews/integration-review-r1.md` | recomputed every gap cell and count | confirmed |
| reproduction (2026-10-02), `R/publication/reproduction/small/` | reran the author and reviewer scripts in a clean checkout under a file-open guard | matched, except the expected nondeterminism of the authors' `gibbs.py` (Section 5, item 5); the reviewer's Gibbs branch and bound reproduced box counts and bounds exactly |
| this dossier (2026-10-04), `small-checks/` | analytic hvycrash existence proof; third pricing050 implementation with own parser; interval check of the authors' saved pricing050 point; exact Gibbs assembly; etamac constants; symbolic check of the pindyck implicit step; own-parser evaluation of all saved points; GAMS against OSIL | all passed (Appendix A) |

**Remaining assumptions.** These are the same for all six instances.
- mpmath `iv` is correct: outward rounding of arithmetic, exp, log, cos and
  sqrt, and of conversions.
- Python `Fraction` is exact.
- For etamac and the Gibbs instances: sympy differentiation and the
  `ivgen`/sympy-to-`iv` compilation reproduce the OSIL expressions.
- For the authors' (not displayed) bounds: numpy elementwise operations are
  IEEE round-to-nearest.

No A1/A2-type sampling assumption is used. The OSIL semantics are standard:
`ln` is the natural log, power(a, y) = exp(y·ln a), and decimals are exact
rationals.

**Runtimes** (from `R/publication/READINESS.md` and the reproduction logs):

| certificate | runtime |
|---|---|
| hvycrash | 0.17 s |
| ex6_2_7, authors' branch and bound | 167 s |
| ex6_2_7, reviewer's branch and bound | 73 s, single process |
| ex6_2_5, authors' | 801 s |
| ex6_2_5, reviewer's | 254 s |
| etamac | 22–27 s |
| pricing050 | 8–28 s; this dossier's version 0.7 s |
| pindyck, author's | 18.7 s |
| pindyck, review's concavity branch and bound | 322 s |

## 7. Relation to prior work

Main source: `R/publication/literature/small/report.md`. Slugs refer to
`literature/papers/`.

### hvycrash
- The CUTE SIF file gives SOLTN = −0.21850 without proof or N. This is
  presumably for N = 50, and has been present since at least the 2013
  repository version. The paper should credit it.
- No source states the constant-objective identity or gives an exactly
  feasible point.
- These published values cannot be objective values of feasible points:
  - COCONUT Fbest −0.0481;
  - Smith (2011): −1.905155235;
  - the SIF's SOLTN(100), SOLTN(500) and SOLTN(1000), each about 1e-8;
  - Omheni (2014) local-solver values at N = 1000.
- Local solvers struggled with the problem (Buchanan 2008; Andretta 2008;
  Gomes 2007).

### ex6_2_7 and ex6_2_5
- The handbook (Floudas et al. 1999) and McDonald and Floudas (1994, 1995,
  1997 GLOPEQ; GOP/αBB-type deterministic ε-global methods,
  floudas1990-a-global-optimization-algorithm-gop,
  adjiman1998-a-global-optimization-method-bb) very likely report the
  optimal phase splits in floating point. **These sources were not read.**
  Indirect evidence: the handbook GAMS start points lie within 4.3e-4 and
  3.0e-5 of our optima, with objectives 8.2e-7 and 1.0e-10 above them.
- The rigorous interval solvers did not close the instances:
  - Ninin 2010, Ninin–Messine–Hansen 2015 (IBBA), and Trombettoni et al. 2011
    ("not solved by any solver, including Baron");
  - MAiNGO did not close ex6_2_7 in 8 h (Najman et al. 2021);
  - Gurobi, BARON and COUENNE did not close either instance in 600 s
    (Cuesta et al. 2026).
- Bertsimas and Margaritis (2025) label BARON's result "GOpt" at 1502 s
  with a 1500 s limit. This is not a certificate.
- Kosolap (2019) reports −70.9586 for ex6_2_5, which is 0.2065 below our
  certified lower bound. It is not attainable.
- Method precedents:
  - the tangent-plane criterion (Baker, Pierce and Luks 1982; Michelsen
    1982);
  - the Lagrangian-dual reading of Gibbs minimization (Mitsos and Barton
    2007, not read);
  - interval tangent-plane stability tests (Stadtherr and coworkers;
    Tessier, Brennecke and Stadtherr 2000).

### etamac
- Only local values were found (MINOS in COCONUT; CONOPT p1).
- Root-node studies did not solve it: tawarmalani2005-a-polyhedral-branch-and-cut
  (problem (8)) and gleixner2017-three-enhancements-for-optimization-based
  (root tables only). Müller, Serrano and Gleixner (2020) give only
  statistics.
- The concavity of CES and log utility is standard economics. We found no
  global certificate for etamac.

### pricing050
- Davarnia and van Hoeve (2021) define the model and data generator.
- davarnia2021-strong-relaxations-for-continuous-nonlinear, Table 1, gives
  for n = 50, instance #2 (preprint): UB 1813.3, decision-diagram bound
  1663.7, and solver bounds 1037.4–1437.6 (min form). The UB 1813.3 lies 0.53
  below our certified minimum 1813.829078… This is a contradiction if the
  data agree; the instance identity rests on the MILP evidence.
- pricing050 is not in the test set of davarnia2026-a-graphical-framework-for-global.

### pindyck
- SCIP studies did not solve it: Müller, Serrano and Gleixner (2020) report a
  root bound of −2239.98 and 1800 s time-outs. Root-node studies:
  tawarmalani2005-a-polyhedral-branch-and-cut (problem (28)) and
  gleixner2017-three-enhancements-for-optimization-based.
- COCONUT's −1612.1783 belongs to a translation that lost the 1/7 factor. The
  recursion at its prices reproduces 1612.17830322903 with factor 1, and
  gives J = 1057.218 with d < 0 under the correct factor.
- Mechanism: interval-Hessian concavity tests are classical (αBB,
  adjiman1998-a-global-optimization-method-bb). Our variant expresses the
  Hessian through per-period intermediate quantities, uses affine or Taylor
  forms, and proves concavity on a polytope rather than a box. Exact LP
  bounds by weak duality follow neumaier2004-safe-bounds-in-linear-and. See
  also neumaier2004-complete-search-in-continuous-global for the general
  setting of rigorous complete search.

### General
The mechanisms are classical: weak Lagrangian duality, tangent planes,
convexity and concavity certificates, and interval arithmetic. The
contribution is the rigorous certificates for the stored models, and the
observation that these instances were open because of structure that
termwise relaxations do not see.

## 8. Critical examination

I re-derived every proof above. Where cheap, I recomputed the key numbers
(Appendix A). **Nothing found invalidates any claimed bound, primal point or
gap.** The items below are gaps in documentation or evidence, with concrete
resolutions.

**E1. hvycrash existence relied on interval arithmetic. Resolved here.**
The authors and the reviewer proved feasibility with 50–60-digit mpmath
intervals. Section 3.1 gives a short analytic proof (θ_k ∈ [2.6, 3] by
induction), so Theorem 1 is now fully pen-and-paper. The dossier also
checked all 150 OSIL rows at this point with its own parser. The paper
should use the analytic proof.

**E2. The tight Gibbs and etamac values rest on one implementation.**
- The displayed duals for ex6_2_7 and ex6_2_5 (gaps 4.9e-14 and 2.1e-15)
  come only from the reviewer's `gibbs_bb.py` (τ = 6e-15 and 1e-17). The
  2026-10-02 reproduction reran the same code. The authors' independent
  implementation certifies only τ = 1e-11, that is, gaps 3.0e-11 and 2.9e-9.
  It uses double-precision intervals and was never run at a smaller τ. For
  ex6_2_5, τ = 1e-17 is far below the double-precision rounding level of the
  tangent-plane values.
- Likewise, the etamac display −15.294675643368093 is above the authors'
  bound −15.294675643368096.

Resolution:
- (a) State provenance in the paper: "tight values from the reviewer's
  implementation; the authors' separate implementation certifies gaps
  ≤ 3.0e-11 and ≤ 2.9e-9 (ex6_2_*) and ≤ 6.5e-15 (etamac; exact 6.408e-15
  against the reviewer's exactly feasible point)".
- (b) Optional: write a third tangent-plane branch and bound, for example
  with python-flint/arb balls or a different bounding rule. Estimated cost:
  half a day of coding, and about 2–5 CPU-minutes (ex6_2_7, τ = 6e-15) plus
  10–30 CPU-minutes (ex6_2_5, τ = 1e-17) on 2 cores.
- (c) Optional for etamac: rebuild the KKT point and bound with an
  independent parser and AD tool. About 2 hours of coding; under 1 minute to
  run.

pricing050 no longer has this issue: the dossier's third implementation
agrees with the reviewer's to 1e-24.

**E3. Common-mode parser.** The authors and the wave-2 reviewer both parse
the OSIL with `osilx.py`. The risk is low, because both match expression
trees against templates by exact string comparison. It was mitigated here:
an independent ElementTree reader (`small-checks/osil_own.py`) reproduces
the objective and rows at the saved points of all six instances, and all
six OSIL files agree with the GAMS files. Still, the etamac Lagrangian and
the Gibbs branch-and-bound expressions reached the proofs only through
`osilx.py`. The optional rebuilds in E2 would remove this dependence.

**E4. Model provenance at the 1e-14 level.** The certificates hold for the
stored OSIL decimals, not for the source models:
- ex6_2_7: the 5e-14 non-cancellation R_p, and differences of up to
  4.1e-14 relative from the handbook;
- etamac: s − 1 = 4.14e-16;
- pricing050: g = −1.0000000000000002e-2 and −1.0000000000000002e-3;
- pindyck: k = 0.142857142857143, and 15-digit δ_t.

For ex6_2_7, the R_p contribution (5.5e-14) is larger than the stated gap.
So the enclosure need not contain the optimum of the exactly specified
handbook model. Resolution: wording only (Section 9).

**E5. pricing050 gap display and stored point.**
- The summary's ≤ 4.23e-14 is a valid but loose subtraction of displays.
- The reviewer's exactly feasible point gives 1.041e-17, but it was never
  saved.
- This dossier checked the authors' saved point
  (`logs/pricing050_primal.txt`) in interval arithmetic: slacks ≥ 3.49e-15,
  exact objective −1813.8290784519730769. Against the independently
  recomputed upper bound −1813.82907845197305774994…, the gap is
  ≤ 1.9150e-17.

Resolution: either keep ≤ 4.23e-14 and say it is conservative, or state
"gap ≤ 2.0e-17 against the saved point" and cite the dossier check. Do not
cite the 1.0e-17 figure unless the reviewer's point is regenerated and
saved (`v_pricing050.py` takes about 28 s).

**E6. etamac primal column.** The summary gives no number. Use
**−15.29467564336808959**, the upward rounding of the enclosure end
−15.2946756433680895919829…. The gap cell 2.6e-15 is unchanged.

**E7. Unsafe ex6_2_5 primal string in secondary documents** (Section 5,
item 2). Do not copy "−70.752077833447706". Use −70.752077833447705.

**E8. pindyck Hessian map.** Ψ is a hand derivation. Its correctness is
essential, because the concavity proof is about Ψ. Current evidence:
- two independent derivations;
- finite-difference agreement to 1.7e-16 at 12 points, including two LP
  vertices of G where d < 0;
- the dossier's symbolic check of the implicit second-order step.

Optional resolution: a full computer-algebra check of the recursion against
direct differentiation for T = 2 or 3 periods, with s defined implicitly.
Estimated cost: under 1 hour of coding, seconds to run. I do not regard this
as a gap in the proof. The other steps are product rules.

**E9. pindyck uniqueness.** The original "6.4e-13" radius used 4×8.01e-17
and lacked the interior-ball step. The review supplied both, giving radius
≤ 3.7e-13. Corollary 5.5 above is complete.

**E10. Gibbs hypotheses.** I checked that the proof needs only r_p ≥ 0,
t ≤ T and y_i ≥ 1e-7/T. The variable upper bounds are not used. The bound is
valid for any decimal λ. There is no hidden assumption.

**E11. etamac hypotheses.**
- The box is derived from etamac's own rows (reviewer), so it is not
  circular. The authors' box ("on R's feasible set") is also not circular:
  its YN bound drops the LN–EN term, which is valid for both Φ and Φ̃.
- Convexity needs μ ≥ 0. This is asserted on the decimal strings
  (min 0.278).
- Free EC is bounded in B through the rows, so no −∞ term arises.

**E12. Cosmetic log error** (etamac κ; Section 5, item 4), and the
nondeterministic regeneration of the authors' ex6_2_7 run (Section 5,
item 5). Neither affects validity. Mention the second if the paper
describes regeneration.

## 9. What the paper may claim, and what it must not claim

**General.**
- **May:** "Each bound holds for every exactly feasible point of the stored
  MINLPLib (OSIL) model; the proofs are computer-assisted with
  outward-rounded interval and exact rational arithmetic, assuming correct
  mpmath interval primitives."
- **Must not:** transfer the numbers to the source models (handbook, GAMS
  Model Library, CUTE, Davarnia–van Hoeve data) at the 1e-14 level.
- **Must not:** call tolerance-level points optimal, or claim solver
  performance rankings.

**hvycrash.**
- **May:** "The objective of hvycrash is constant, equal to −0.2185, on the
  feasible set; we give a short proof and an explicit feasible point, so
  the optimal value is exactly −0.2185. The value −0.21850 is already
  recorded, without proof, in the CUTE SIF file. To the best of our
  knowledge the identity has not been stated before."
- **Must not:** claim discovery of the value, a computational result, or any
  physical interpretation (the SIF problem is a "freely inspired",
  admittedly degenerate variant).

**ex6_2_7 and ex6_2_5.**
- **May:** "We certify the MINLPLib models ex6_2_7 and ex6_2_5 to absolute
  gaps ≤ 4.9e-14 and ≤ 2.1e-15 against exactly feasible rational points.
  The optimal phase splits were very likely reported earlier as ε-global
  floating-point solutions (McDonald and Floudas), which we could not
  consult. To the best of our knowledge, no rigorous certificate has been
  published. The Lagrangian tangent-plane argument is classical."
- **Must not:** claim the first solution. **Must not:** cite BARON's "GOpt"
  label (Bertsimas and Margaritis 2025) as a proof.

**etamac.**
- **May:** "closed to ≤ 2.6e-15. In the stored model the CES aggregate is
  not exactly concave, because the 15-digit exponents give degree
  1 + 4.14e-16; a concave majorant restores a convex relaxation. The local
  optimum value was known; to the best of our knowledge, no global
  certificate was published."
- **Must not:** say "the CES is concave" without that qualification, or
  claim results for Manne's original model.

**pricing050.**
- **May:** "upper bound −1813.8290784519730577; an exactly feasible point
  with objective −1813.8290784519730769; gap ≤ 4.23e-14 (or ≤ 2.0e-17, as in
  E5). Three independent implementations agree."
- **May:** "A published primal value of 1813.3 (min form) for what is very
  likely the same instance lies below our certified minimum; if the data
  agree, no feasible point attains it."
- **Must not:** state the instance identity as fact.

**pindyck.**
- **May:** "The reduced objective is proved 0.001-strongly concave on a
  polytope containing the feasible price set; hence the KKT point is
  globally optimal up to ≤ 5.44e-14, and the maximizer is unique and within
  3.7e-13 of it. To the best of our knowledge, no global certificate was
  published; SCIP studies reported the instance unsolved."
- **Must not:** say J is concave on the price box or on F "because F is
  convex" (F is not known to be convex).
- **Must not:** quote COCONUT's −1612.18 as a value of this model.

**Suggested umbrella sentence.** "These six instances were open not because
their search spaces are hard, but because an exact identity (hvycrash),
phase separability with homogeneity (ex6_2_*), hidden convexity (etamac),
separability (pricing050) or concavity on a polytope (pindyck) is invisible
to termwise relaxations." This is an interpretation and should be labelled
as such.

## 10. Candidate figures and tables

1. **Table (main text):** the instances, with sense, size, structure,
   mechanism and status class (Section 0).
2. **Table (main text):** listed dual and primal against our dual, primal
   and gap, with absolute and relative gaps (Section 5).
3. **Figure:** a ternary map of the tangent-plane distance D(y) = G(y) − λ·y
   for ex6_2_7. Use a log-scaled colour for D ≥ 0, mark the three phase
   compositions where D ≈ 0, and annotate the certified bound
   D ≥ −6e-15. Data: λ and G from the OSIL; float evaluation suffices for
   illustration.
4. **Figure:** pindyck. Show a histogram of sampled λ_max(∇²J) over G
   (−0.1195 to −0.1111) against the certified −0.001, possibly with a
   2-D slice of G and F through p*. Data: the review's
   `hess_check.log` and the extension's samples. This illustrates why the
   0.001 margin suffices despite the relaxation.
5. **Table (appendix):** decimal artifacts of the stored models
   (R_p = 5e-14; s − 1 = 4.14e-16; g = −1.0000000000000002e-2/e-3;
   k = 0.142857142857143), and their effect on each certificate.
6. **Table (appendix):** published values shown unattainable or belonging to
   other models:
   - hvycrash: COCONUT −0.0481, Smith −1.905, SIF SOLTN(N ≥ 100);
   - ex6_2_5: Kosolap −70.9586;
   - pricing050: Davarnia 1813.3 (conditional);
   - pindyck: COCONUT −1612.18 (a different model).
7. **Table (appendix):** the one-hour solver campaign rows for the six
   instances (`R/publication/solver-runs/results_table.md`). No closures.
   - BARON: cos unsupported on hvycrash.
   - SCIP: memory stops on ex6_2_5, ex6_2_7 and pindyck.
   - Final duals, in the order BARON, GUROBI, SCIP ("—" means no finite
     dual): hvycrash —, −2.1413e9 and −2.185e8; etamac −16.51, — and −15.51;
     ex6_2_5 −157.3, −128.3 and −592.1; ex6_2_7 −1.409, −1.584 and −1.422;
     pindyck −3067, −1829 and −1625; pricing050 (max, upper bounds) −1055.0,
     −1418.1 and −1514.5.
   - SCIP's values concern slightly tightened log/power argument bounds.
8. **Table (appendix):** the trust base and runtime of each certificate
   (Section 6).

## Appendix A. Checks run for this dossier

Run from a copy in `/tmp/smalldossier`, single-threaded. The scripts and
logs are saved in
`/workspace/minlp-notes/paper-open-minlplib/development/dossiers/small-checks/`;
`sh run.sh` repeats them in a fresh temporary directory in under 1 minute.

| script | result |
|---|---|
| `hvy_analytic.py` | κ(0.08) = 0.00651055783…; 50κ/0.85 = 0.38297 ≤ 0.4; cos 2.6 ∈ Taylor bracket ≤ −0.85; 3 < 223/71; θ_0 = 2.6565078758566084090 |
| `own_osil_checks.py` (own ElementTree parser `osil_own.py`) | hvycrash analytic point: all 150 rows hold on 60-digit enclosures (width 1.9e-60) and all bounds hold; objective −0.2185. Gibbs verifier points: rows exact (`Fraction`) and objectives −0.16084761546360086152447… and −70.75207783344770558036712…. etamac p1 objective −15.29467564346276. pindyck stored point −1170.48628543608856208757742507, residual 8.3e-28 |
| `pricing_check.py` | own parser and own 1-D branch and bound (4,026 boxes, 0.7 s): Σ min F_j ≥ −2721.77195359771241568725405598; UB ≤ −1813.82907845197305774994594; display margin 4.99e-17. Authors' saved point: `iv` slacks ≥ 3.4958e-15 and 3.917e-15; exact objective −1813.8290784519730769; gap ≤ 1.915e-17 |
| `gibbs_assembly.py` | exact λ·b; bound ends −0.16084761546364904344… and −70.75207783344770758035394690…; vapour m = 6.978e-22; R_3 = 1/20000000000000; both summary displays ≤ certified ends; gaps 4.8182e-14 and 2.0004e-15 |
| `etamac_check.py` | p1q = 0.27999999999999975; s − 1 = 4.1414e-16; W^{s−1} ≤ 1 + 2.8672e-15 (W = 1015.6), 1 + 3.1524e-15 (W = 2022.06), 1 + 3.1607e-15 (W = 2062.83), all ≤ κ = 1.000000000000004; display checks |
| `pindyck_hess_sym.py` | implicit first- and second-order formulas for s = a + b e^{−Ks} verified symbolically (differences 0) |
| `gms_vs_osil.py` | all six: GAMS and OSIL rows and objective rows agree to ≤ 3.5e-51 relative at 5 random points |

No project-wide checks were run. No CI was inspected. Nothing was
committed.
