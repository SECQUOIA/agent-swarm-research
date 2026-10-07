# Dossier: small models (family key `small`)

Instances: hvycrash, ex6_2_7, ex6_2_5, etamac, pricing050, pindyck.

Prepared 2026-10-04 for the Mathematical Programming Computation paper. This
version replaces an earlier dossier of the same date (kept as
`small-checks/superseded-small-dossier-v1.md`); Section 8.1 lists the
corrections to that version, including one wrong gap figure.

Conventions.
- `R/` means `/workspace/minlp-notes/research-20260929/`.
- The authoritative bounds, displays and gaps are the rows of
  `R/open-instances-summary.md` for these six instances (closed-instance
  table). Older notes, including `R/open-instances-wave2/small/report.md`
  Section 1, contain weaker or unsafe displays.
- A dual bound is valid for every exactly feasible point of the stored OSIL
  model (decimal coefficients read as exact rationals, `ln` natural, `a^y` =
  exp(y ln a) for a > 0, a row with a division by zero is not satisfied).
- Checks run for this version are in
  `paper-open-minlplib/development/dossiers/small-checks/r2/` (scripts and
  logs). They use copies in `/tmp/smallchk/` of the OSIL files and saved logs,
  and a new OSIL reader (`osil.py`, ElementTree) that shares no code with the
  project's `osilx.py`. Nothing under `R/` or `literature/` was modified, and
  no saved certificate was regenerated; one new certificate computation (the
  third Gibbs implementation, Section 8, C1; 4.5 CPU-minutes) was run.

Status words:
- **proved**: a complete pen-and-paper proof;
- **computer-assisted**: a proof whose finite part is a computation in
  outward-rounded interval or exact rational arithmetic, with the trusted
  components stated;
- **independently implemented**: the finite part was redone by separate code;
- **numerical**: floating-point or high-precision evidence without an
  enclosure.

## 0. Overview

| instance | sense; variables/rows | mechanism | status of the dual bound |
|---|---|---|---|
| hvycrash | min; 201/150 equalities | the rows force the objective to a constant; explicit feasible point | proved (identity and analytic existence proof); the existence part was also checked in interval arithmetic by three codes |
| ex6_2_7 | min; 9/3 | Lagrangian over the 3 mass balances; Gibbs tangent-plane minimization on the composition simplex | computer-assisted. The displayed value comes from the verifier's code and is confirmed (with a slightly tighter value) by a third implementation written for this dossier (Section 8, C1); the authors' code certifies a weaker value |
| ex6_2_5 | min; 9/3 | same; the ideal vapour phase has a closed form | as for ex6_2_7; the third implementation certifies a gap ≤ 2.7e-19 |
| etamac | min; 97/70 | convex relaxation (production equalities to ≤ with a concave majorant), Lagrangian tangent plane at one point | computer-assisted; two implementations (displayed value from the verifier's) |
| pricing050 | max; 50/5 | Lagrangian over the 5 rows; 50 certified 1-D minimizations | computer-assisted; four implementations agree (authors, verifier, earlier dossier, this dossier) |
| pindyck | min; 116/96 | the reduced objective −J(p) is proved 0.001-strongly convex on a polytope G that contains the feasible prices; tangent-plane (or strong-concavity) bound at the KKT point | computer-assisted (exact-rational LP weak duality, Taylor or affine models, exact or interval LDLᵀ test); two implementations |

None of these certificates uses the eg_* assumptions A1/A2. The common trust
base is mpmath's interval arithmetic (`iv`: arithmetic, exp, log, cos, sqrt,
and decimal-to-interval conversion), Python `Fraction`, and, for the
verifier's Gibbs and etamac certificates, sympy differentiation and the
verifier's sympy-to-`iv` compiler (`ivgen.py`; not used by the third Gibbs
implementation). The authors' Gibbs and pindyck codes
additionally rely on IEEE round-to-nearest numpy arithmetic with explicit
error padding (Section 6).

## 1. Instances and models

### 1.1 hvycrash

**Source.** CUTE problem HVYCRASH (SIF file by Ph. L. Toint, 1994) at
N = 50, which the SIF file calls the "original value"; MINLPLib added it on
2017-02-06 from Yurttan's AMPL translation ("CUTE model hvycrash";
references Ivashkevich 1976; Tyatushkin, Zholudev and Erinchek 1992). The SIF
header calls the problem "freely inspired by" a heavy-spacecraft landing
problem; because no package found a feasible point of the original
formulation, the SIF version drops a final-state constraint and sets EPS = 0,
and calls the result "badly scaled degenerate". No physical claim is made.

**Size and sense.** 201 continuous variables, 150 equality rows, minimize.

**Variables (OSIL names, k = 1..50).**
- θ_k = x_k ∈ [0, 6.2831854]; θ_0 = x101 ∈ [0, 6.2831854];
- c_k = x_{50+k} ∈ [0.08, 0.417];
- r_k = x_{101+k} free; s_k = x_{202−k} free; s_0 := 0 (eliminated).

**Model.** Let h = 4.37e-3, D(c) = 0.486237c² + 0.0162079 (> 0) and
A(c) = c/(0.3c² + 0.01). For k = 1..50 the rows e_{3k−2}, e_{3k−1}, e_{3k}
are

- (acc_k) s_{k−1} − s_k + h cos θ_k / (D(c_k) r_k²) = 0;
- (alg_k) −1/r_k − cos θ_k / (D(c_k) r_k³) = 0;
- (dyn_k) 0.1 θ_{k−1} − 0.1 θ_k + h A(c_k)/r_k² − h cos θ_k / (D(c_k) r_k⁴) = 0;

and the problem is min s_50 (= x152).

This form was matched against the OSIL by three codes: the authors'
`hvycrash.py` and the verifier's `v_hvycrash.py` (exact string templates),
and this dossier's `hvy_check.py` (own reader; sympy identities in exact
rationals, including the signs of the linear parts).

**Structure that matters.** alg_k fixes the accumulator increment of acc_k
exactly. Termwise relaxations see free r_k inside divisions and cannot bound
the increments; SCIP's listed bound is −2.185e8.

**Provenance.**
- The decoded SIF problem at N = 50 equals the MINLPLib model: bounds were
  compared by code, rows at 20 random points × 150 rows in 50 digits
  (maximum difference 2.1e-48; literature track, round-2 reviewer). The SIF XX
  cards that fix θ_0 and θ_N at 0 are overridden by a later bound loop, so
  in the decoded problem every θ lies in [0, 2π].
- The GAMS World PrincetonLib file is a different variant (bounds shifted by
  0.005, one extra fixed variable); not used.

### 1.2 ex6_2_7 and ex6_2_5 (Gibbs free-energy minimization)

**Source.** Floudas et al., *Handbook of Test Problems in Local and Global
Optimization* (1999), Chapter 6, Test Problems 7 and 5, via GLOBALLib
(MINLPLib, added 2001-07-31). The MINLPLib pages cite McDonald and Floudas
(1997, GLOPEQ).
- ex6_2_7: ethylene glycol – lauryl alcohol – nitromethane; three liquid
  phases, UNIQUAC; T = 295 K; feed b = (0.4, 0.1, 0.5), T := Σ_i b_i = 1.
- ex6_2_5: sec-butyl alcohol – di-sec-butyl ether – water; two UNIQUAC
  liquid phases and an ideal vapour; P = 1.16996 atm; feed
  b = (40.30707, 5.14979, 54.54314), T = 100 exactly.

**Size and sense.** 9 variables n_{ip} (component i, phase p), bounds
n_{ip} ∈ [1e-7, b_i], 3 linear equality rows Σ_p n_{ip} = b_i. Minimize.

**Model.** f(n) = Σ_{p=1}^{3} G_p(n_{·p}). Each G_p is a sum of *atoms* of
two kinds, all in the amounts n_p = (n_{1p}, n_{2p}, n_{3p}) of one phase:
- linear atoms α·n_p;
- log atoms (ℓ·n_p) ln(m·n_p), with linear forms ℓ, m, where m has
  nonnegative coefficients and m·n_p > 0 on the positive orthant.

This is the expanded GAMS-Convert form of UNIQUAC (combinatorial and residual
terms; e.g. 26 terms per phase in ex6_2_7). After exact merging of atoms with
the same logarithm argument, each ex6_2_7 phase has one linear atom and 8 log
atoms, among them y_i ln y_i with coefficients 1 + O(5e-14) (this dossier,
`gibbs_cert.py`). The ex6_2_5 vapour phase is the ideal-gas function
G_3(n) = Σ_i n_i (ln(n_i/Σ_k n_k) + 0.156969560191053); the constant is ln P.

**Structure that matters.**
- No term mixes phases, so f is separable by phase and the only coupling is
  the 3 linear mass balances.
- Each G_p is homogeneous of degree 1 up to an exact residual (Lemma G1):
  exactly in ex6_2_5, up to 5e-14 on component 3 in ex6_2_7.
- ex6_2_7 has three identical phase functions; ex6_2_5 has two identical
  liquids. This symmetry and the dilute phases (y_i down to about 6e-7) make
  ordinary spatial branch and bound slow.

**Provenance.** The MINLPLib GAMS file equals the GLOBALLib scalar file.
The literature track re-implemented the objective from the handbook GAMS
source; it agrees with MINLPLib to ≤ 4.1e-14 (ex6_2_7) and ≤ 9.4e-14
(ex6_2_5) relative at 200 random points. The constants are rounded to about
15 digits. In ex6_2_7 the rounding leaves the non-homogeneous residual
8.73945638067505 + 1.868 − 10.607456380675 = 5e-14 on component 3.

### 1.3 etamac

**Source.** GAMS Model Library model etamac (SEQ=80), "Eta-Macro Energy
Model for the USA", after Manne's ETA-MACRO (1977); MINLPLib added it
2001-07-31. The MINLPLib GAMS text equals the GLOBALLib text. Not compared
with Manne's report (not obtained).

**Size and sense.** 97 variables, 70 rows (60 linear equalities, 9 nonlinear
equalities, 1 linear inequality). Minimize.

**Model.** Periods t = 1..9; g = 4.91287681, δ = 0.8153726976.
- Objective: minimize f = −Σ_t β_t ln C_t, with β_t > 0
  (β_1 = 0.8153726976, …, β_8 = 0.19536615155532, terminal weight
  β_9 = 3.98240565033479).
- Linear rows (OSIL row names in brackets):
  - KN_t = g I_{t−1}, t = 2..9 [e1–e8];
  - L_1 = LN_1 + 2.038431744 [e17], L_t = δL_{t−1} + LN_t [e18–e25];
  - E_1 = EN_1 + 40.76863488 [e26], E_t = δE_{t−1} + EN_t [e27–e34];
  - K_t = δK_{t−1} + KN_t [e35–e42]; Y_t = δY_{t−1} + YN_t [e44–e51];
  - 1000 EC_t = cL_t L_t + cE_t E_t, cL_t, cE_t > 0 [e52–e60];
  - Y_t = C_t + I_t + EC_t [e61–e69];
  - 0.07 K_9 ≤ I_9 [e70].
- Production rows:
  - YN_t = Φ_t := (a_t KN_t^{−p1} + b LN_t^{−p2} EN_t^{−p3})^{−q},
    t = 2..9 [e9–e16];
  - Y_1 = 3.4653339648 + (b LN_1^{−p2} EN_1^{−p3} + c0)^{−q} [e43];
  - p1 = .342222222222222, p2 = .427777777777778, p3 = .794444444444445,
    q = .818181818181818, b = .306708090151268, c0 = .612508399277048,
    a_t ∈ [0.330, 0.821].
- Bounds: K_1 = 12.32657617084 fixed; EC_t free; every other variable has a
  positive lower bound and no upper bound.
- Labels K, KN, Y, YN, C, I, EC are capital, new capital, output, new output,
  consumption, investment, energy cost; L, E, LN, EN are the reviewers'
  labels for the two priced inputs of the second nest and their new vintages.

**Structure that matters.** f is convex, all rows but production are linear,
and Φ_t is a CES function. If Φ_t were concave, relaxing the production
equalities to "≤" would give a convex program (hidden convexity).

**Provenance at the decimal level.** The exponents are 15-digit roundings of
0.28·11/9, 0.35·11/9, 0.65·11/9 and 9/11 (differences −2.2e-16, 2.2e-16,
5.6e-16, −1.8e-16). Consequently p1 q = 0.27999999999999975 and the degree
of the LN–EN Cobb–Douglas aggregate is s = (p2 + p3) q = 1 +
207070707070707/5·10^29 = 1 + 4.14e-16, not 1 (exact rationals;
`etamac_point.log`). So Φ_t is **not** exactly concave in the stored model;
the certificate handles this (Lemma E2).

### 1.4 pricing050

**Source.** Continuous version of the marketing pricing model of Davarnia and
van Hoeve (2021, Math. Program.) with n = 50; contributed to MINLPLib on
2024-03-25 by M. Kiaghadi. There is strong but not conclusive evidence that
it is their n = 50 instance #2: the integer version (x ∈ {0, …, 10}) has
MILP optimum 1825.0, the value reported for #2 (one floating-point HiGHS
solve, literature track).

**Size and sense.** 50 variables x ∈ [0, 10]^50, 5 nonlinear "≤" rows with
249 univariate terms. Maximize.

**Model.** maximize −Σ_j c_j x_j subject to
Σ_j a_ij x_j exp(g_ij x_j^{p_ij}) ≤ r_i, i ∈ {e2, …, e6}, where
- c_j ∈ {0, 1, …, 20} (46 positive);
- a_ij < 0 (one decimal), p_ij ∈ {1, 2, 3} (78, 94, 77 terms);
- g_ij = −.1, −1.0000000000000002e-2, −1.0000000000000002e-3 for
  p = 1, 2, 3 (the binary64 values of 0.1, 0.1², 0.1³ printed in full);
- r = (−500, −651, −615, −788, −984); row e5 has no x21 term.

In minimization form: minimize c·x subject to
Σ_j |a_ij| x_j e^{−|g_ij| x_j^{p_ij}} ≥ |r_i| (price-weighted demand
thresholds).

**Structure that matters.** Every term depends on one variable and the
objective is linear, so the Lagrangian of the 5 rows separates into 50
one-dimensional functions.

### 1.5 pindyck

**Source.** GAMS Model Library model pindyck (SEQ=28), "Optimal Pricing and
Extraction for OPEC", after Pindyck (1978); MINLPLib added it 2001-07-31.
The MINLPLib GAMS text equals the GLOBALLib scalar file. Not compared with
Pindyck's paper.

**Size and sense.** 116 variables, 96 equality rows. Minimize.

**Model.** For t = 1..16:
- prices p_t ≥ 0;
- total demand td_t = 0.87 td_{t−1} − 0.13 p_t + c_t, td_0 = 18, with
  exogenous c_t increasing from 3.3 to 3.87553375330505 (15-digit decimals);
- fringe supply s_t = 0.75 s_{t−1} + 1.02^{−k cs_t}(1.1 + 0.1 p_t),
  k = 0.142857142857143, s_0 = 6.5;
- cumulative supply cs_t = cs_{t−1} + s_t, cs_0 = 0;
- OPEC sales d_t = td_t − s_t;
- reserves R_t = R_{t−1} − d_t, R_0 = 500;
- profit π_t = (p_t − 250/R_t) d_t (free variables x101..x116).

The objective is min −Σ_t δ_t π_t with δ_t the 15-digit decimals of
1.05^{−(t−1)}. All variables except π_t are ≥ 0. Write
K = 0.142857142857143·ln 1.02 (the decimal, not 1/7).

**Structure that matters.** Given p, every other variable is determined: the
supply equation reads s − a − b e^{−Ks} = 0 with a = 0.75 s_{t−1} and
b = (1.1 + 0.1 p_t) e^{−K cs_{t−1}} > 0, whose left side is strictly
increasing in s. So the problem is max J(p) := Σ_t δ_t d_t(p)(p_t −
250/R_t(p)) over F := {p ≥ 0 : d_t(p) ≥ 0 ∀t}. J looks strongly concave
(sampled largest Hessian eigenvalue between −0.1195 and −0.1111), but F is
not known to be convex and entrywise interval Hessians over a price box lose
the correlation between entries.

**Provenance.** COCONUT's GAMS translation drops the factor 1/7 in the
exponent; its "best" value −1612.18 belongs to that different model.

### 1.6 OSIL against GAMS

The unmodified MINLPLib `.gms` files (copies in
`R/publication/solver-runs/gms/`) and the OSIL files agree at 5 random points
per instance: all rows to ≤ 3.5e-51 relative, objective rows exactly
(50 digits; earlier dossier's `gms_vs_osil.py`, rerun on copies for this
version with identical output). This is numerical evidence, not an algebraic
identity proof. The OSIL/GAMS coefficient differences known for catmix,
methanol50 and lop97icx do not occur here. The status refresh found the
model files unchanged since the 2014–2017 copies (pricing050: since 2024).

## 2. Listed MINLPLib status

All six instances are open on MINLPLib: no solved mark, and `minlplib.solu`
lists `=best=`, not `=opt=`. The instance pages were fetched 2026-09-29/30;
the 2026-10-02 refresh found them unchanged.

| instance | listed primal (point, solver, infeasibility) | best listed single-solver dual (solver, date) | `.solu` `=bestdual=` |
|---|---|---|---|
| hvycrash | −0.2185 (p3, COUENNE, 1e-12); p1, p2 = −0.21413 | −218500000 (SCIP, 2022-02-15) | none |
| ex6_2_7 | −0.16084762 (p1, CONOPT 2014, 6e-17) | −1.06726714 (BARON, 2017-09-13) | −1.354737094 |
| ex6_2_5 | −70.75207783 (p1, CONOPT 2014, 7e-15) | −111.4201713 (BARON, 2017-09-13) | −364.1162233 |
| etamac | −15.29467564 (p1, CONOPT 2014, 1e-10) | −15.40567054 (SCIP, 2025-07-31) | −16.3990195 |
| pricing050 (max) | −1813.829078 (p1, KNITRO, 2024, 7e-10) | −1534.3281 (SCIP, 2025-07-31; an upper bound) | −1153.003281 |
| pindyck | −1170.486285 (p1, CONOPT 2014, 6e-14) | −1437.941134 (SCIP, 2018-05-23) | −1889.888367 |

Sources: `R/open-instances-scout/fetched.csv`;
`R/reviews/wave2-small-verification/pages/`;
`R/publication/minlplib-status/data/tables.md` (Table B);
`R/publication/literature/small/report.md`, Section 2. The paper uses the
instance-page single-solver values; the `.solu` values are weaker for all
six. Note that the *latest dated* entries can differ from the best ones
(e.g. pindyck: GUROBI −1722.94 on 2025-07-31; ex6_2_5: GUROBI −123.19).

## 3. The certificates

### 3.1 hvycrash: the objective is constant on the feasible set (proved)

**Idea.** Row alg_k says exactly that the quantity added to the accumulator
in acc_k equals −h. Hence s_50 = −50h on the whole feasible set. A feasible
point is built backwards from θ_50, and a short induction keeps all angles
in [2.6, 3].

**Theorem 1.**
(a) Every feasible point of hvycrash has objective s_50 = −0.2185 = −437/2000.
(b) The feasible set is nonempty.
Hence the optimal value is exactly −0.2185, and every feasible point is
optimal.

*Proof of (a).* At a feasible point every row is defined, so r_k ≠ 0.
Multiplying alg_k by −r_k gives

  cos θ_k / (D(c_k) r_k²) = −1.   (∗)

Then acc_k reads s_k = s_{k−1} − h, and with s_0 = 0, s_50 = −50h. ∎

*Proof of (b).* By (∗), h cos θ_k/(D r_k⁴) = −h/r_k², so dyn_k becomes
θ_k − θ_{k−1} = 10h(A(c_k) + 1)/r_k², and (∗) gives
1/r_k² = D(c_k)/(−cos θ_k). Define:
- c_k = 0.08 for all k; then A(0.08) = 1000/149, D(0.08) =
  24149771/1250000000, and
  κ := 10h(A(0.08) + 1)D(0.08) = 81381972927/12500000000000 = 0.0065105578…;
- θ_50 = 3 and θ_{k−1} = θ_k − κ/(−cos θ_k), k = 50, …, 1;
- r_k = (−cos θ_k / D(0.08))^{1/2}, s_k = −kh.

Whenever every cos θ_k < 0, these definitions satisfy alg_k (by the choice
of r_k), acc_k (by (∗) and s_k = −kh) and dyn_k (since
θ_k − θ_{k−1} = κ/(−cos θ_k) = 10h(A + 1)D/(−cos θ_k)) exactly.

Claim: θ_k ∈ [2.6, 3] for k = 50, …, 0. Downward induction: suppose
θ_50, …, θ_k ∈ [2.6, 3]. Since 3 < 223/71 < π, these angles lie in
[2.6, 3] ⊂ (π/2, π), where cos is decreasing, so
−cos θ_j ≥ −cos 2.6 > 0.85 for j ≥ k. Hence
θ_{k−1} = 3 − Σ_{j=k}^{50} κ/(−cos θ_j) ≥ 3 − 50κ/0.85 = 3 − 0.38297… > 2.6,
and θ_{k−1} < θ_k ≤ 3. So all θ_k ∈ [2.6, 3] ⊂ [0, 6.2831854], all
cos θ_k < 0, all r_k are real and nonzero, and c_k = 0.08 is within bounds. ∎

The facts used are exact: cos 2.6 ∈ [−0.85688896, −0.85688155] by
alternating Taylor partial sums through x¹⁴ and x¹² (the terms decrease from
the second on); 50κ/0.85 < 0.4; 223/71 < π (Archimedes). This dossier's
`hvy_check.py` also evaluates all 150 OSIL rows of this point on 60-digit
interval enclosures (|row| ≤ 1.9e-60, enclosure width) and all bounds;
θ_0 = 2.6565078758566084090…, max cos θ_k = −0.8846. The authors' interval
run builds the same point; the verifier proved a different one (c_k = 0.417,
θ_50 = 4.2; θ_k ∈ [2.1653, 4.2], r_k ∈ [2.21, 3.15]) in 60-digit intervals.

**Remarks.**
- On the feasible set cos θ_k < 0 for k ≥ 1 and θ_k is strictly increasing
  in k.
- Nothing is computed numerically in the proof; the paper should present
  hvycrash as an exact observation, not a computational result.

### 3.2 ex6_2_7 and ex6_2_5: mass-balance Lagrangian and tangent-plane test (computer-assisted)

**Idea.** Price each component with a "chemical potential" λ_i. Because of
the mass balances, f(n) = λ·b + Σ_p [G_p(n_p) − λ·n_p], and each bracket
depends on one phase only. By (near-)homogeneity, each bracket is the phase
amount t_p times the tangent-plane distance D_p(y) = G_p(y) − λ·y at the
phase composition y. If λ are the equilibrium chemical potentials, D_p ≥ 0
on the simplex with zeros at the equilibrium phase compositions (the
classical tangent-plane criterion). A rigorous 2-D minimization of D_p over
the simplex closes the instance; the bound needs no knowledge of the phase
split.

**Lemma G1 (scaling; exact).** For t > 0 and n > 0,
G_p(tn) = t G_p(n) + t ln t ⟨r_p, n⟩, where r_p = Σ ℓ over the log atoms
(ℓ·n) ln(m·n) of G_p.

*Proof.* Linear atoms are homogeneous; (ℓ·tn) ln(m·tn) = t(ℓ·n) ln(m·n) +
t ln t (ℓ·n). ∎

For the stored decimals (exact rationals): r_p = (0, 0, 1/20000000000000)
for each phase of ex6_2_7, and r_p = 0 for every phase of ex6_2_5. Three
independent derivations agree: the authors' rule-based tree analysis, the
verifier's sympy identity check (`gibbs_sym.py`), and this dossier's own atom
decomposition (`gibbs_check.py`, `gibbs_cert.py`).

**Lemma G2 (ideal phase).** For G(y) = Σ_i y_i (ln y_i + c) on the simplex
and any λ: G(y) − λ·y ≥ −ln Σ_i e^{λ_i − c}.

*Proof.* With π_i = e^{λ_i − c}/Z, Z = Σ_i e^{λ_i − c}:
G(y) − λ·y = Σ_i y_i ln(y_i/π_i) − ln Z ≥ −ln Z (Gibbs' inequality). ∎

**Theorem G (dual bound).** Let T = Σ_i b_i, ε = 1e-7/T and
Δ_ε = {y ∈ R³ : y_i ≥ ε, Σ y_i = 1}. Let λ ∈ R³ be arbitrary, let
m_p ≤ inf_{y ∈ Δ_ε} [G_p(y) − λ·y] for p = 1, 2, 3, and suppose r_p ≥ 0
componentwise. Then every feasible n satisfies

  f(n) ≥ λ·b + Σ_p [ min(0, T·m_p) − max_i r_{p,i}/e ].

*Proof.*
1. Σ_p n_p = b gives f(n) = λ·b + Σ_p [G_p(n_p) − λ·n_p].
2. Fix p; let t = Σ_i n_{ip} and y = n_p/t. Since 0 < n_{ip} ≤ b_i (the
   lower bounds are 1e-7 and the other phases are nonnegative), t ∈ (0, T]
   and y_i ≥ 1e-7/t ≥ ε, so y ∈ Δ_ε.
3. Lemma G1: G_p(n_p) − λ·n_p = t[G_p(y) − λ·y] + t ln t ⟨r_p, y⟩.
4. t[G_p(y) − λ·y] ≥ t m_p ≥ min(0, T m_p).
5. ⟨r_p, y⟩ ∈ [0, max_i r_{p,i}] and t ln t ≥ −1/e, so
   t ln t ⟨r_p, y⟩ ≥ −max_i r_{p,i}/e. ∎

The variable upper bounds are not used, and the bound is valid for every λ.

**What is computed.**

*Multipliers.* λ is a decimal vector, the chemical potentials of the
equilibrium found by a tangent-plane LP on a simplex grid and a 60-digit
Newton solve of the 12-equation KKT system (verifier), rounded to 20 digits:
- ex6_2_7: λ = (−0.23993666802341555716, −0.54068374800661316808,
  −0.021609146907096643708), λ·b = −0.160847615463575861526 (exact);
- ex6_2_5: λ = (−0.92114611232187116319, −2.2777893037791928146,
  −0.40139310690864392314), λ·b = −70.7520778334477055803539469 (exact).
The authors' λ (multistart SLSQP + 50-digit Newton) agree to all 11 printed
digits.

*Tangent-plane minima m_p (verifier, `R/reviews/wave2-small-verification/gibbs_bb.py`).*
- Domain: coordinates (y1, y2) ∈ [ymin, 1 − 2ymin]², y1 + y2 ≤ 1 − ymin,
  y3 = 1 − y1 − y2 enclosed per box and clipped to [ymin, 1], with
  ymin = 9.9e-8 (ex6_2_7) and 9.9e-10 (ex6_2_5), slightly below ε. A box is
  discarded only by the exact test y1lo + y2lo > 1 − ymin.
- Per box, the best of three rigorous lower bounds: the natural interval
  extension; the mean-value form at a feasible centre; a second-order form
  using the end-point matrices of the interval Hessian (exact 2×2 quadratic
  minimum D(c) − ½gᵀQ⁻¹g when both end-point matrices are positive definite,
  otherwise a separable box bound).
- Fathoming rule: lower bound ≥ −τ. Arithmetic: mpmath `iv`, 53-bit boxes,
  40-digit centre values; G and its derivatives are sympy derivatives of the
  OSIL trees, compiled to `iv` by `ivgen.py`.
- Results: ex6_2_7, τ = 6e-15, 42,111 boxes (one phase function, used for all
  three identical phases); ex6_2_5 liquid, τ = 1e-17, 131,111 boxes; ex6_2_5
  vapour by Lemma G2: m_3 = 6.978e-22 > 0, so its term is 0.

*Assembly* (checked in exact rationals in this dossier, `gibbs_check.log`):
- ex6_2_7: bound = λ·b − 3·T·6e-15 − 3·(5e-14)/e
  ≥ **−0.16084761546364904344…** (λ·b − 7.32e-14; the r_p term alone is
  5.52e-14);
- ex6_2_5: bound = λ·b − 2·100·1e-17 = **−70.7520778334477075803539469**
  (exactly).

*Second implementation (authors, `R/open-instances-wave2/small/gibbs.py`).*
numpy intervals widened by one ulp per operation and a self-written rigorous
logarithm (`ia.ilog`; no libm log), different coordinates and splitting, and
τ = 1e-11. It certifies the weaker bounds −0.16084761549352554 (ex6_2_7)
and −70.752077836333563 (ex6_2_5). The 2026-10-02 regeneration gave
different but valid values (−0.16084761549338836 and −70.752077836338371)
because a float multistart picks a different dependent coordinate.

*Third implementation (this dossier, `gibbs_cert.py`).* Own reader, exact
atom merging, closed-form derivatives, convexity windows around the local
minimisers and an exclusion branch and bound; no sympy. It certifies
m ≥ −4.1878e-15 (ex6_2_7) and m ≥ −1.3797e-21 (ex6_2_5 liquids), hence the
duals ≥ −0.16084761546364361 and ≥ −70.75207783344770558063 (rounded down;
Section 8, C1).

**Trusted.** mpmath `iv` (arithmetic, log, decimal conversion), sympy
differentiation and `ivgen.py`, the parser `osilx.py`.

**No duality gap.** The primal points below lie 2.5e-14 (ex6_2_7) and
1.3e-20 (ex6_2_5) below λ·b, so the Lagrangian bound is tight up to τ and
the r_p artefact. (For ex6_2_7, λ·b itself is not a valid bound: the stored
model is not exactly homogeneous.)

### 3.3 etamac: concave majorant and Lagrangian tangent plane (computer-assisted)

**Idea.** The objective is convex, the coupling rows are linear, and the CES
production functions are concave up to a 4e-16 degree excess caused by the
file's decimals. Replace each production equality by "YN ≤ Φ̃", where Φ̃ is
a concave majorant of Φ on a box that contains all feasible points. The
result R is a convex relaxation. At a KKT point of R the Lagrangian is a
convex function whose tangent plane, minimized over the box, bounds f.

**Lemma E1 (box).** Every etamac-feasible point lies in a box
B = Π_j [lo_j, hi_j]: lo_j are the OSIL lower bounds (EC_t: (cL_t L_lb +
cE_t E_lb)/1000), and the upper ends follow from etamac's own rows:
- Y_1 ≤ 3.4653339648 + c0^{−q} (the bracket in e43 is ≥ c0 and x ↦ x^{−q}
  is decreasing);
- I_t ≤ Y_t − C_lb − EC_lb,t; KN_{t+1} = g I_t;
- YN_{t+1} ≤ a_{t+1}^{−q} KN_{t+1}^{p1 q} (drop the positive LN–EN term);
- Y_{t+1} = δ Y_t + YN_{t+1};
- C, EC, L, E, LN, EN, K from the linear rows.

Each step uses one row and earlier bounds, all evaluated in outward-rounded
`iv`. Largest upper end 2062.83 (E_9); Y_9 ≤ 26.73; Y_1 ≤ 4.959.

**Lemma E2 (concave majorant).** Let r = 1/q, s = (p2 + p3)q,
w = LN^{p2/(p2+p3)} EN^{p3/(p2+p3)}, W ≥ max_B w and κ ≥ max(1, W^{s−1}).
Define
  Φ̃_t = (a_t KN^{−p1} + b κ^{−r} LN^{−p2/s} EN^{−p3/s})^{−q},
and Φ̃_1 likewise with c0 in place of the KN term. Then
(a) Φ̃_t is concave and nondecreasing on the positive orthant;
(b) Φ_t ≤ Φ̃_t on B.

*Proof.* M(u, v) = (a u^{−r} + b v^{−r})^{−1/r} (a, b > 0, r > 0) is a
positive multiple of a weighted power mean with exponent −r < 1, hence
concave and nondecreasing in (u, v) on the positive orthant. With
u = KN^{p1 q}: Φ_t = M(u, w^s) and Φ̃_t = M(u, κw), because u^{−r} =
KN^{−p1}, (w^s)^{−r} = LN^{−p2}EN^{−p3} and (κw)^{−r} =
κ^{−r}LN^{−p2/s}EN^{−p3/s}. u is concave (0 < p1 q < 1) and w is concave
(Cobb–Douglas, exponents summing to 1); a concave nondecreasing function of
concave arguments is concave: (a). Since s > 1 and 0 < w ≤ W,
w^s = w·w^{s−1} ≤ κw, and M is nondecreasing in v: (b). For Φ_1 the u-term
is the constant c0. ∎

Numbers: s − 1 = 4.14e-16 > 0, so the majorant is needed.
- Verifier: W = 1015.6000321087411 (max over t of LN_ub^α EN_ub^{1−α}),
  W^{s−1} ≤ 1 + 2.8672e-15, κ = 1.000000000000004.
- Authors: W = 2022.06 (max(LN_ub, EN_ub)); W^{s−1} − 1 = 3.152e-15 (the
  authors' log prints 3.11e-15 because of a 15-digit print; the certificate
  used the 40-digit interval end, Section 8.3).

**Relaxation R.** Replace YN_t = Φ_t by YN_t ≤ Φ̃_t (t = 2..9) and e43 by
Y_1 ≤ 3.4653339648 + Φ̃_1. By Lemmas E1 and E2(b), every etamac-feasible
point is in B and feasible for R.

**Theorem E.** Let h(x) = 0 collect the 60 linear equalities, g̃(x) ≤ 0 the
9 relaxed rows and g_70(x) ≤ 0 the terminal row. For any ν ∈ R^60, any
μ ∈ R^10 with μ ≥ 0 and any x̂ ∈ B, with l = f + ν·h + μ·(g̃, g_70), every
feasible x satisfies

  f(x) ≥ l(x̂) + Σ_j min_{ξ ∈ [lo_j, hi_j]} ∂_j l(x̂)(ξ − x̂_j).

*Proof.* A feasible x is in B and in R, so h(x) = 0, g̃(x) ≤ 0, g_70(x) ≤ 0
and, with μ ≥ 0, f(x) ≥ l(x). l is convex and differentiable on the positive
region that contains B (f convex, h linear, g̃ convex by E2(a), μ ≥ 0), so
l(x) ≥ l(x̂) + ∇l(x̂)·(x − x̂); minimize the right side coordinatewise over B. ∎

**What is computed (verifier, `v_etamac.py`).**
- Structure: all 70 rows, 97 bounds and the objective matched to templates
  built from an explicit role map.
- x̂, ν, μ: SLSQP on R, then a 50-digit Newton solve of R's KKT system
  (residual 2.7e-48), rounded to 30 digits. Multipliers are positive
  (min μ = 0.277935, μ_70 = 0.362913), and every free variable is ≥ 0.047
  above its lower bound.
- l(x̂) and ∇l(x̂) in `iv` (40 digits) from sympy expressions with exact
  rational data. Largest free-variable gradient 4.9e-31; ∂l/∂K_1 = 0.00496
  multiplies a zero-width range.
- Result: f ≥ **−15.2946756433680921685** (lower end
  −15.29467564336809216848701…, rounded down).

The authors' `etamac.py` used the KKT point of the unrelaxed model; its
gradient is 1.1e-16 and its bound is weaker: −15.294675643368096.

**Trusted.** mpmath `iv` (exp, log), sympy and `ivgen.py`, `osilx.py`.

**Tightness.** The remaining gap (2.6e-15) is essentially the price of κ,
not numerical error: the relaxation's optimum lies about 2.6e-15 below
etamac's.

### 3.4 pricing050: Lagrangian over five rows (computer-assisted)

**Idea.** Dualize the five rows. The Lagrangian separates into 50 univariate
functions on [0, 10], whose minima are certified by 1-D interval methods. With
the optimal multipliers there is no duality gap.

**Theorem P.** For any μ ∈ R^5 with μ ≥ 0, every feasible x satisfies

  −c·x ≤ μ·r − Σ_j min_{ξ ∈ [0,10]} F_j(ξ),
  F_j(ξ) = c_j ξ + Σ_i μ_i a_ij ξ exp(g_ij ξ^{p_ij}).

*Proof.* For feasible x, row_i(x) ≤ r_i and μ ≥ 0, so
c·x ≥ c·x + Σ_i μ_i(row_i(x) − r_i) = Σ_j F_j(x_j) − μ·r
≥ Σ_j min F_j − μ·r. ∎

**What is computed.**
- μ_e5 = 3.0489011208166370021, μ_e6 = 2.1677509642745686136, others 0
  (authors: Kelley cutting planes + 50-digit Newton; verifier: Nelder–Mead +
  50-digit refinement; same digits). μ·r = −4535.6010320496854734372 exactly.
- Σ_j min F_j, certified:
  1. authors: natural/mean-value interval B&B (16,960 boxes; weaker final
     value −1813.8290784519704);
  2. verifier: monotonicity partition in `iv` (F′ > 0, F′ < 0, F″ < 0, or
     F″ > 0 on width < 1e-7 with an exact quadratic bound; 2,406 pieces):
     Σ min F_j ≥ −2721.771953597712415687255 (25 digits printed);
  3. earlier dossier: natural/mean-value B&B with its own parser:
     ≥ −2721.77195359771241568725405598…;
  4. this dossier (`pricing_check.py`, own parser, different method): a
     50-digit stationary point per j, a window where F″ > 0 is proved
     (F ≥ F(x̂) − F′(x̂)²/(2F″_lo)) or where F′ has a fixed sign at an end
     point, and a 1-D exclusion B&B elsewhere (247 boxes, 3 s):
     ≥ −2721.77195359771241568725405377….
- **Upper bound** (max form): ≤ −1813.82907845197305774994594… (implementations
  3 and 4 agree to 2e-27). The summary display −1813.8290784519730577 is
  5.0e-17 above it, so it is valid.

**Trusted.** mpmath `iv` (exp), `Fraction`.

### 3.5 pindyck: strong concavity on a polytope (computer-assisted)

**Idea.** Every state is a function of the 16 prices, so the problem is
max J(p) over F. The proof (i) encloses F in a polytope G by LP bounds with
exact weak-duality certificates, (ii) writes the Hessian as an explicit
function Ψ of 112 per-period quantities θ, ∇²J(p) = Ψ(θ(p)), (iii) encloses
θ(G) in a box Θ, and (iv) proves Ψ ⪯ −μI on Θ (μ = 0.001) with first-order
Taylor (affine) models and a small branch and bound. Then J is μ-strongly
concave on the convex set G ⊇ F, and the stationary point p* is a global
maximizer up to its tiny gradient.

**Lemma P1 (reduction).** For p ≥ 0 the recursions have a unique solution.
Every OSIL-feasible point has prices in F and objective −J(p). F drops the
sign constraints on td, s, cs and R, so it contains the projection of the
feasible set (correct direction for a bound).

**Lemma P2 (polytope).** Let α_t = td_t(0), CSH_t ≥ sup_{p∈F} cs_t(p) and
e_lo,t ≤ exp(−K·CSH_t). Define, for j ≤ t,
W_tj = 0.13·0.87^{t−j} + 0.1·0.75^{t−j} e_lo,j and
γ_t = α_t − 6.5·0.75^t − 1.1 Σ_{j≤t} 0.75^{t−j} e_lo,j, and
G = {p ≥ 0 : W̲p ≤ γ̄} with W rounded down and γ rounded up. Then F ⊆ G.

*Proof.* For p ∈ F, e^{−K cs_t} ≥ e_lo,t, so by induction
s_t ≥ ℓ_t(p) := 6.5·0.75^t + Σ_{j≤t} 0.75^{t−j}(1.1 + 0.1p_j)e_lo,j; then
d_t ≥ 0 gives td_t(p) ≥ ℓ_t(p), i.e. (Wp)_t ≤ γ_t. Rounding is safe because
p ≥ 0. ∎

CSH_t comes from six rounds of LPs in (p, s) that contain every
(p, s(p)), p ∈ F (supply relaxed with e_t ∈ [e(CSH_t), e(CSL_t)], s_t ≤ td_t,
p_t ≤ α_t/0.13, s_t ≤ α_t). Every LP value is certified by weak duality in
exact `Fraction` arithmetic with finite variable bounds; HiGHS only proposes
multipliers. Result CSH_16 = 169.273; on G, p_t ≤ γ_t/W_tt ∈ [57.41, 126.15];
p* is interior to G with smallest slack 6.4376 (exact).

**Lemma P3 (state ranges over G).** LPs in (p, s, e, z), with W p ≤ γ, the
exact supply equation s_t = 0.75 s_{t−1} + 1.1e_t + 0.1z_t, five verified
tangent lines below and one verified secant above e^{−K cs_t} on the current
cs range, McCormick inequalities for z_t = p_t e_t, and finite valid bounds
(s_t ≤ 0.75 s_{t−1} + 1.1 + 0.1 p̄_t since e ≤ 1 on G), give, after seven
rounds and exact weak-duality certificates, cs_16 ∈ [71.1, 158.8],
R_16 ∈ [192.5, 500.9] (all R_t ≥ 192.5 > 0) and d_16 ∈ [−3.16, 23.48] (d may
be negative on G). Interval arithmetic then gives a box Θ ⊇ θ(G).

**Lemma P4 (Hessian map).** With E_t = e^{−K cs_{t−1}}, β_t =
(1.1 + 0.1p_t)E_t, φ_t = e^{−K s_t}, u_t = p_t − 250/R_t,
θ_t = (β_t, E_t, φ_t, d_t, u_t, R_t^{−2}, R_t^{−3}), ι_t = 1/(1 + Kβ_tφ_t),
κ_t = φ_t ι_t and G_t = ∇cs_{t−1}, one has ∇²J(p) = Ψ(θ(p)), where

```
∇b   = 0.1 E_t e_t − K β_t G_t
∇²b  = β_t (K² G_t G_tᵀ − K ∇²cs_{t−1}) − 0.1 K E_t (e_t G_tᵀ + G_t e_tᵀ)
∇s_t = 0.75 ι_t ∇s_{t−1} + κ_t ∇b
∇²s_t = 0.75 ι_t ∇²s_{t−1} + κ_t ∇²b − K κ_t (∇b ∇s_tᵀ + ∇s_t ∇bᵀ) + K² β_t κ_t ∇s_t ∇s_tᵀ
∇cs_t = ∇cs_{t−1} + ∇s_t,  ∇²cs_t = ∇²cs_{t−1} + ∇²s_t
∇d_t = ∇td_t − ∇s_t, ∇²d_t = −∇²s_t;  ∇R_t = ∇R_{t−1} − ∇d_t, ∇²R_t = ∇²R_{t−1} − ∇²d_t
∇q_t = e_t + 250 R_t⁻² ∇R_t,  ∇²q_t = 250 (R_t⁻² ∇²R_t − 2 R_t⁻³ ∇R_t ∇R_tᵀ)
∇²J  = Σ_t δ_t (u_t ∇²d_t + d_t ∇²q_t + ∇d_t ∇q_tᵀ + ∇q_t ∇d_tᵀ)
```

with ∇td_t = −0.13 Σ_{k≤t} 0.87^{t−k} e_k (exact). (The extension note writes
the ∇²b cross term as 0.1(e_t∇Eᵀ + ∇E e_tᵀ) with ∇E = −K E_t G_t, which is
the same.)

*Proof.* Implicit differentiation of s = a + b e^{−Ks} (twice) and the
product rule. Evidence: two independent derivations (author, reviewer); a
symbolic check of the implicit step (earlier dossier); agreement with
50-digit finite-difference Hessians at 12 points of G to 1.7e-16 (review)
and with a separate float Hessian at p* to 1.1e-16 (author).

**Lemma P5 (matrix test).** Suppose that for all θ in a box Θ′,
Ψ(θ) = C + Σ_k ε_k A_k + E with ε ∈ [−1, 1]^K, |E| ≤ R_m entrywise, and that
X_k ⪰ ±A_k, ρ̄ ≥ ρ(R_m) and −C − Σ_k X_k − (ρ̄ + μ)I ≻ 0. Then Ψ(θ) ⪯ −μI on
Θ′.

*Proof.* For |ε_k| ≤ 1, X_k − ε_kA_k = ½(1 + ε_k)(X_k − A_k) +
½(1 − ε_k)(X_k + A_k) ⪰ 0; λ_max(E) ≤ ρ(|E|) ≤ ρ(R_m) by Perron–Frobenius
monotonicity; hence Ψ ⪯ C + Σ_k X_k + ρ̄I ≺ −μI. ∎

In the computation X_k = V|Λ|Vᵀ + e_k I with a float eigendecomposition
A_k ≈ VΛVᵀ and e_k ≥ ‖A_k − VΛVᵀ‖_∞ (then X_k ∓ A_k = V(|Λ| ∓ Λ)Vᵀ +
e_kI ∓ (A_k − VΛVᵀ) ⪰ 0 exactly for any real V); ρ̄ by a Collatz–Wielandt
quotient; positive definiteness by LDLᵀ without pivoting (interval-valued in
the author's code, exact rational in the review). The Taylor model of Ψ over
Θ′ comes from the affine (first-order Taylor) arithmetic of `tm1.py` (author;
float coefficients with γ_n rounding allowances) or the review's affine
arithmetic with interval coefficients and `nextafter` rounding.

**Theorem 5 (strong concavity; computer-assisted).** ∇²J(p) ⪯ −10⁻³ I for
every p ∈ G.

*Proof.* Lemma P5 holds with μ = 0.001 on every leaf of a partition of Θ
(author: 9 leaves after splitting u_16 once, u_15 twice, β_13 three times,
β_12 twice; review: 6 leaves on the hull of both parties' boxes; coverage of
both partitions checked exactly). With θ(G) ⊆ Θ and Lemma P4 the claim
follows. J is C² on a neighbourhood of G because R_t ≥ 192 and
1.1 + 0.1p_t > 0 there, and s_t(p) is smooth by the implicit function theorem
(1 + Kbe^{−Ks} > 0). ∎

**Theorem 6 (dual bound).** Let p* be the 17-digit price vector in
`R/open-instances-wave2/small/logs/pindyck_primal.txt` and g = ∇J(p*). Every
feasible point of pindyck has objective

  ≥ −J(p*) − ‖g‖²/(2μ) ≥ **−1170.486285436088562087577425069306**
  (rounded down; this dossier).

The summary's weaker bound −J(p*) − Σ_t |g_t| max(p*_t, p̄_t − p*_t)
≥ −1170.4862854360886163931058729 (review, rounded down) displayed as
**−1170.4862854360886163932** also holds.

*Proof.* For p ∈ F ⊆ G the segment [p*, p] lies in G (convex), so by
Taylor's formula with integral remainder and Theorem 5,
J(p) ≤ J(p*) + g·(p − p*) − (μ/2)‖p − p*‖². The right side is at most
J(p*) + ‖g‖²/(2μ) (complete the square), and also at most
J(p*) + Σ_t |g_t| max(p*_t, p̄_t − p*_t) (drop the quadratic term and use
0 ≤ p_t ≤ p̄_t on G). Enclosures from the review's saved exact end points
(`R/reviews/pindyck-review-checks/logs/primal_enclosure.txt`):
J(p*) = 1170.4862854360885620875774250692880254… (width 1.4e-46),
‖g‖₂² ≤ 3.3989e-32, so ‖g‖²/(2μ) ≤ 1.6995e-29 (`pindyck_sc.log`). ∎

**Corollary (uniqueness).** The maximizer of J over F exists, is unique, and
lies within ‖·‖₂ distance 2‖g‖₂/μ ≤ 3.7e-13 of p*. (F is compact and J
continuous; J(p) ≥ J(p*) forces (μ/2)‖p − p*‖² ≤ ‖g‖‖p − p*‖; the ball lies
in F because p* is interior to F (min d_t = 5.44, p* > 0), and J is strictly
concave there.)

**Trusted.** Author: IEEE round-to-nearest numpy arithmetic with γ_n
allowances (a hand-checked padding analysis), mpmath `iv`, `Fraction`; LAPACK
and HiGHS only propose (eigenvectors, Perron vector, LP duals). Review: only
mpmath `iv` (exp, log) and `Fraction`, since its affine arithmetic is
outward-rounded and its matrix test is exact.

## 4. Exactly feasible primal points

| instance | point | how feasibility is proved | objective |
|---|---|---|---|
| hvycrash | c_k = 0.08, θ_50 = 3, backward recursion (Section 3.1); real point with irrational coordinates | analytic (Theorem 1(b)); also interval runs of the authors (same point), the verifier (c_k = 0.417, θ_50 = 4.2) and this dossier (own reader) | exactly −0.2185 |
| ex6_2_7 | rational: phases 1, 2 = 20-digit decimals of the KKT amounts; phase 3 = b − (phases 1 + 2) exactly; listed in `R/reviews/wave2-small-verification/logs/ex6_2_7_bound.json` | rows exact in `Fraction`, bounds exact; objective in `iv` (verifier; rechecked with own reader here) | −0.16084761546360086152447… |
| ex6_2_5 | same construction; `ex6_2_5_bound.json` | same | −70.75207783344770558036712… |
| etamac (verifier) | I_1..I_8, LN_t, EN_t = 25-digit decimals of the KKT point of R; all other variables by the exact recursion of the 70 rows; I_9 := 0.07 K_9 (e70 active). **The decimals were not saved**; `v_etamac.py` regenerates them deterministically (reproduction 2026-10-02 matched every printed digit) | rows hold as real identities; bound margins ≥ 0.047 in `iv` | ∈ [−15.29467564336808959198292336128453574383340, +4e-45] |
| etamac (this dossier) | same construction from the authors' **saved** 17-digit decisions in `R/open-instances-wave2/small/logs/etamac_primal.txt` | rows hold by construction; all 70 row enclosures contain their right sides (width ≤ 6.6e-37); bound margins ≥ 0.047 (`etamac_point.log`) | ∈ [−15.29467564336808959198292336128724888685…, +4e-45] |
| pricing050 (authors) | saved 17-digit KKT point, `R/open-instances-wave2/small/logs/pricing050_primal.txt` (x11 raised by 1.27e-15) | `iv` row slacks ≥ 3.4958e-15 (e5), 3.9173e-15 (e6); bounds exact (this dossier and the earlier one) | exactly −1813.8290784519730769 (rational) |
| pricing050 (verifier) | KKT minimizers rounded to 25 digits; **not saved** (`v_pricing050.py` regenerates them) | `iv` row slack ≥ 1.1e-18 | −1813.8290784519730578 (20 digits) |
| pindyck | p* = 17-digit prices in `pindyck_primal.txt`; states by the exact recursion | each s_t by a verified interval inclusion (author: fixed-point TX ⊆ X; review: interval Newton); min d_t = 5.437, min R_t = 350.3, min td_t = 13.99 | −1170.486285436088562087577425069288025… |

Notes.
- The stored decimal vectors of the hvycrash and pindyck points are not
  exactly feasible (row violations 3.9e-62 and 8.3e-28); the exactly
  feasible points are the recursion-defined real points.
- The wave-2 etamac "primal" (17 digits, row violation 6.0e-14) is not
  exactly feasible; the recursion points above replace it.

## 5. Numbers table

Gap cells are rounded upward. For the maximization instance the dual is an
upper bound and the primal display is rounded down.

| instance | listed dual | our dual (safe display; summary) | our primal (safe display; summary) | gap (summary) | relative | sources |
|---|---|---|---|---|---|---|
| hvycrash | −2.185e8 | −0.2185 (exact) | −0.2185 (attained) | 0 | 0 | Theorem 1; summary row |
| ex6_2_7 | −1.06726714 | −0.16084761546364905 | −0.16084761546360086 | ≤ 4.9e-14 (exact 4.8182e-14) | 3.1e-13 | `R/reviews/wave2-small-verification/logs/ex6_2_7_bound.json`; `R/reviews/closing-confirm-r2-checks/logs/ex6_2_5_lower_end.log` (ex6_2_7 end); `R/publication/integration/gap-values.json` |
| ex6_2_5 | −111.4201713 | −70.75207783344770759 | −70.752077833447705 | ≤ 2.1e-15 (2.0000e-15 against the certified end) | 3.0e-17 | `ex6_2_5_bound.json`; closing-confirm r2/r3 |
| etamac | −15.40567054 | −15.294675643368093 | summary: "exactly feasible point"; proposed −15.29467564336808959 | ≤ 2.6e-15 (exact 2.5760e-15) | 1.7e-16 | `R/reviews/wave2-small-verification/logs/etamac.json`; `etamac_point.log` |
| pricing050 (max) | −1534.3281 | −1813.8290784519730577 (upper) | −1813.8290784519731 | ≤ 4.23e-14 (subtraction of displays) | 2.4e-17 | `logs/pricing050.json`; `pricing_check.log` |
| pindyck | −1437.941134 | −1170.4862854360886163932 | −1170.486285436088562 | ≤ 5.44e-14 (exact 5.4306e-14) | 4.7e-17 | `R/reviews/pindyck-review-checks/logs/final_bound.log`, `primal_check.txt` |

**Available tighter statements (no new search; Section 8):**
- pindyck: dual −1170.486285436088562087577425069306, primal
  −1170.486285436088562087577425069288, gap ≤ 1.8e-29 (relative 1.6e-32)
  by strong concavity.
- pricing050: against the *saved* authors' point the gap is ≤ 1.92e-14
  (exact 1.9150e-14); against the verifier's unsaved point it is 1.04e-17.
- ex6_2_7: dual −0.16084761546364361, gap ≤ 4.3e-14 (third implementation,
  Section 8, C1).
- ex6_2_5: dual −70.75207783344770558063, primal −70.75207783344770558036
  (rounded up), gap ≤ 2.7e-19 (relative 3.8e-21; C1).

**Display checks** (exact rationals, this dossier): every summary dual display
lies on the valid side of its certified value; every summary primal display
lies on the valid side of its objective enclosure.

**Disagreements found** (none affects validity):
1. `R/publication/reproduction/README.md` (ex6_2_5 row) and the authors' log
   give the primal as "−70.752077833447706". This nearest rounding lies
   4.2e-16 *below* the exactly feasible point's objective, so it is not a
   safe primal display for a minimization. The summary's
   −70.752077833447705 is safe. Likewise the string "−70.75207783344770758"
   (the verifier's printed dual) lies 3.5e-19 above the certified end; the
   summary already uses −…759.
2. `R/open-instances-wave2/small/report.md`, Section 1, keeps the authors'
   weaker certificates and an etamac "gap 6.6e-15" against a point with row
   violation 6e-14; its Section 11 and the summary supersede these.
3. The pricing050 gap appears as ≤ 4.23e-14 (summary), "gap 1.0e-17"
   (literature report; the verifier's unsaved point) and 2.7e-12 (wave-2
   report). All are upper bounds under their own references, but the paper
   should use one (Section 9).
4. The earlier version of this dossier stated "gap ≤ 2.0e-17 against the
   saved point" for pricing050. That is wrong by a factor 1000: its own log
   prints 1.915e-14 (Section 8.1).

## 6. Verification record

| review (date) | what it checked | verdict |
|---|---|---|
| wave-2 small verification, `R/reviews/wave2-small-verification/verification-report.md` (2026-09-30), independent verifier with own code (shares only the parser `osilx.py` with the authors) | **hvycrash**: templates for all rows/bounds; identity; own feasible point in 60-digit intervals; MINLPLib points; tolerance remark by hand. **Gibbs**: symbolic scaling identity (sympy, exact); own multipliers (grid LP + 60-digit Newton); own mpmath 2-D B&B with different arithmetic, coordinates, splitting and bounding rules; closed-form vapour; own rational primal points; sanity and negative controls (τ = 1e-17 fails for ex6_2_7, as predicted by the floor D ≈ −4.2e-15; a 1e-3 perturbation of λ_1 fails). **etamac**: templates; exact exponents; own box from etamac's rows; own W; KKT of R itself; own bound; own exactly feasible point. **pricing050**: templates; own multipliers; own monotonicity-partition minima; own exactly feasible point. Status pages; brief novelty search | **verified** for all five; bounds equal to or tighter than the authors'. Not checked: the authors' B&B code itself |
| pindyck review, `R/reviews/pindyck-review.md` (2026-09-30), adversarial, independent rebuild | own OSIL reader; reduction; primal enclosure (interval Newton); own derivation of Ψ and 12-point finite-difference check; own exact-LP ranges; proof that the author's G contains F; own affine arithmetic with interval coefficients; exact rational matrix test; own 6-leaf B&B; author's 9 leaves re-verified; exact coverage; final bound in exact rationals; line-by-line code review | **verified**; five issues (gap rounding 5.43 → 5.44e-14; an overclaim about entrywise Hessians; mpmath truncation wording; uniqueness argument; log overwrite), all applied in text except the log side effect |
| closing confirmations, `R/reviews/closing-confirm-r2.md`, `-r3.md` (2026-09-30) | direction of every displayed bound; ex6_2_5 display corrected to −…759 (end −70.7520778334477075803539469); etamac and pricing050 directions | resolved |
| literature reviews r1–r3, `R/publication/reviews/lit-small-review-r{1,2,3}.md` | provenance and prior results; r1 major (SIF bound cards; fixed); r2 added Kosolap 2019; r3 added Cuesta et al. 2026 | latest **issues**, no blocker or major issue; minor fixes checked by the parent |
| integration review r1, `R/publication/reviews/integration-review-r1.md` | recomputed every gap cell exactly; noted that the saved pricing050 digits cannot reproduce 1.04e-17 | confirmed |
| reproduction (2026-10-02), `R/publication/reproduction/commands.json`, `small/logs/` | reran all author and reviewer scripts (A01–A30, exit 0) in a clean worktree under a file-open guard; smoke checks reproduced saved outputs exactly | matched, except the expected float nondeterminism of the authors' `gibbs.py` (different but valid bounds) |
| this dossier (2026-10-04), `small-checks/r2/` | own reader; hvycrash structure/identities in sympy and analytic existence proof; exact Gibbs assembly and display checks; third Gibbs implementation; etamac exponents and an exactly feasible point from saved decimals; fourth pricing050 implementation and saved-point check; pindyck strong-concavity bound from saved enclosures; GAMS vs OSIL rerun | Appendix A; no validity problem found |

**Remaining assumptions** (same for all six).
- mpmath `iv` is correct: outward rounding of arithmetic, exp, log, cos, sqrt
  and of decimal conversion.
- Python `Fraction` is exact.
- Gibbs and etamac (displayed values): sympy differentiation and `ivgen.py`
  reproduce the OSIL expressions (mitigated: the authors' code and this
  dossier's third Gibbs implementation avoid sympy).
- Authors' (non-displayed) Gibbs and pindyck bounds: numpy elementwise
  operations are IEEE round-to-nearest and the hand-checked padding analysis
  is right.
- pindyck Hessian map Ψ: a hand derivation, checked as in Lemma P4 (no
  computer-algebra proof of the full recursion).

No A1/A2-type sampling assumption is used. The OSIL semantics in the
Conventions are standard.

**Runtimes** (recorded; `R/publication/READINESS.md` and
`R/publication/reproduction/commands.json`): hvycrash 0.17 s; ex6_2_7
authors 167 s, verifier 77 s (one process; 50 s on 6 processes
originally); ex6_2_5 authors 801 s, verifier 258 s (one process); etamac
authors 27 s, verifier 22 s; pricing050 authors 8 s, verifier 28 s; pindyck
author 19 s, review concavity B&B 322 s.

## 7. Relation to prior work

Main source: `R/publication/literature/small/report.md` (latest review r3:
issues, no blocker). Slugs refer to `literature/papers/`.

### hvycrash
- The CUTE SIF file (slugs bongartz1995-cute-constrained-and-unconstrained-testing,
  gould2015-cutest-a-constrained-and-unconstrained) records "SOLTN −0.21850"
  without N or proof, present at least since the 2013 repository version;
  presumably for N = 50. The paper should credit it.
- No source found states the identity or gives an exactly feasible point.
- Published values that cannot be objective values of feasible points:
  COCONUT Fbest −0.0481 and its OQNLP point −0.1573199996
  (shcherbina2003-benchmarking-global-optimization-and-constraint;
  coconut2026-globallib-gams-coconut-and-minlplib); Smith (2011) −1.905155235
  (smith2011-improved-placement-of-local-solver); the SIF's SOLTN(100),
  SOLTN(500), SOLTN(1000) ≈ 1e-8; Omheni (2014) local-solver values at
  N = 1000 (omheni2014-methodes-primales-duales-regularisees-pour).
- Local solvers struggled (gomes2007-a-sequential-quadratic-programming-algorithm,
  buchanan2008-techniques-for-solving-nonlinear-programming,
  andretta2008-topicos-em-otimizacao-com-restricoes; Prudente 2012 not read,
  prudente2012-inviabilidade-em-metodos-de-lagrangiano).
- New observation (Section 8, item C4): tolerance-feasible points can drop
  stages, which explains several of these values.

### ex6_2_7 and ex6_2_5
- Handbook (floudas1999-handbook-of-test-problems-in) and McDonald–Floudas
  (mcdonald1994-decomposition-based-and-branch-and,
  mcdonald1995-global-optimization-for-the-phase,
  mcdonald1997-glopeq-a-new-computational-tool; GOP and αBB-type ε-global
  methods, floudas1990-a-global-optimization-algorithm-gop,
  adjiman1998-a-global-optimization-method-bb) very likely report the optimal
  phase splits in floating point. **None of these was read** (paywalled);
  the readable McDonald–Floudas NRTL paper
  (mcdonald1995-global-optimization-for-the-phase-2) concerns a different
  activity model. Indirect evidence: the handbook GAMS start points lie
  within 4.3e-4 and 3.0e-5 of our optima, objectives 8.2e-7 and 1.0e-10
  above them.
- Rigorous interval solvers did not close them
  (ninin2010-optimisation-globale-basee-sur-l,
  ninin2015-a-reliable-affine-relaxation-method,
  trombettoni2011-inner-regions-and-interval-linearizations: "not solved by
  any solver, including Baron"); MAiNGO did not close ex6_2_7 in 8 h
  (najman2021-linearization-of-mccormick-relaxations-and); Gurobi, BARON and
  COUENNE did not close either in 600 s (Cuesta et al. 2026,
  arXiv:2510.14122v3; no slug — the slug cuesta2025-global-optimization-of-mixed-integer
  is a different paper).
- bertsimas2025-towards-a-practical-global-optimization labels BARON's runs
  "GOpt" after 1502 s with a 1500 s limit and an undefined 0.1% gap; not a
  certificate.
- Kosolap (2019) reports −70.9586 for ex6_2_5, 0.2065 below our certified
  lower bound (kosolap2019-global-optimization-of-the-general).
- Method precedents: tangent-plane criterion (baker1982-gibbs-energy-analysis-of-phase,
  michelsen1982-the-isothermal-flash-problem-part); Lagrangian-dual reading
  of Gibbs minimization (Mitsos and Barton 2007, not read, no slug);
  interval tangent-plane stability tests
  (tessier2000-reliable-phase-stability-analysis-for and later Stadtherr
  group work).

### etamac
- Only local values: MINOS −15.2947 (COCONUT), CONOPT p1.
- Root-node studies did not solve it: tawarmalani2005-a-polyhedral-branch-and-cut
  (problem 8), gleixner2017-three-enhancements-for-optimization-based (root
  tables only); Müller, Serrano and Gleixner (2020) only statistics (no slug).
- Concavity of CES and log utility is standard economics; no global
  certificate for etamac was found.

### pricing050
- Model and generator: davarnia2021-outer-approximation-for-integer-nonlinear
  (Davarnia and van Hoeve, integer version).
- davarnia2021-strong-relaxations-for-continuous-nonlinear, Table 1 (read in
  the preprint), n = 50 instance #2: UB 1813.3, decision-diagram bound
  1663.7, solver bounds 1037.4–1437.6 (min form). 1813.3 lies 0.53 below our
  certified minimum 1813.829078…; if the data agree this value is not
  attainable. The instance identity rests on the MILP evidence; formula (9)
  is printed without the 1/10 price scaling.
- pricing050 is not in the test set of davarnia2026-a-graphical-framework-for-global.

### pindyck
- SCIP studies did not solve it: Müller, Serrano and Gleixner (2020): root
  bound −2239.98, 1800 s time-outs; root-node tables in
  tawarmalani2005-a-polyhedral-branch-and-cut (problem 28) and
  gleixner2017-three-enhancements-for-optimization-based.
- COCONUT's −1612.1783 belongs to a translation that lost the 1/7 factor
  (recursion at its prices: 1612.17830322903 with factor 1; J = 1057.218 and
  d < 0 with the correct factor).
- Mechanism: interval-Hessian concavity tests are classical (αBB,
  adjiman1998-a-global-optimization-method-bb; Taylor forms,
  neumaier2003-taylor-formsuse-and-limits). Our variant expresses the Hessian
  through per-period intermediate quantities, uses affine forms, and proves
  concavity on a polytope instead of a box. Exact LP bounds by weak duality
  follow neumaier2004-safe-bounds-in-linear-and. General setting:
  neumaier2004-complete-search-in-continuous-global.

### General
The mechanisms are classical: weak Lagrangian duality, tangent planes,
convexity and concavity certificates, interval arithmetic
(hansen2004-global-optimization-using-interval-analysis,
kearfott1996-rigorous-global-search-continuous-problems). The contribution is
rigorous certificates for the stored models, and the observation that these
instances stayed open because the structure that closes them (an identity,
phase separability with homogeneity, hidden convexity, separability,
concavity on a polytope) is invisible to termwise relaxations.

## 8. Critical examination

I re-derived every proof in Section 3 and recomputed the key numbers where
this was cheap (Appendix A). **Nothing found invalidates a claimed bound,
primal point or summary gap.** The items below are improvements, gaps in
evidence, and documentation errors, each with a resolution.

### 8.1 Corrections to the earlier version of this dossier

- **Wrong pricing050 gap.** The earlier version said "gap ≤ 2.0e-17 against
  the saved point" (Sections 5, 8 E5, 9 and Appendix A). Its own log
  (`small-checks/pricing_check.log`) prints 0.0000000000000191500…, i.e.
  1.915e-14. Exact recomputation: UB ≤ −1813.82907845197305774994594623,
  saved point −1813.8290784519730769, difference 1.9150054e-14. The correct
  statement is "gap ≤ 1.92e-14 against the saved authors' point". A paper
  that had used 2.0e-17 would have overstated the closure by a factor 1000.
- Its relative pricing gap "1.1e-20" was derived from the wrong figure.
- Its etamac κ discussion and other items are retained where correct.

### 8.2 Improvements that need no new search

**C2. pindyck: gap 5.44e-14 → 1.7e-29.** The certificate proves μ-strong
concavity (μ = 0.001) on G, but the final bound drops the quadratic term
and uses the linear term over the whole price box. Completing the square
gives J(p) ≤ J(p*) + ‖g‖²/(2μ) for every p ∈ F (Theorem 6). The extension's
own uniqueness argument already uses this inequality. With the review's saved
exact enclosures, ‖g‖²/(2μ) ≤ 1.6995e-29, so the dual can be displayed as
−1170.486285436088562087577425069306 and the gap is ≤ 1.8e-29 (relative
1.6e-32). Cost: none (`pindyck_sc.py`, < 1 s, exact rationals). Suggested
action: update the summary row (dual, primal display to 30 decimals, gap),
or keep the conservative row and mention the sharper figure in the text.

**C3. pricing050 gap.** The summary's ≤ 4.23e-14 subtracts two displays.
- Against the saved authors' point (exactly feasible, objective
  −1813.8290784519730769), the gap is ≤ 1.92e-14 (`pricing_check.log`).
- The verifier's 25-digit point gives 1.04e-17, but it was never saved.
  Regenerating it costs about 28 s (`v_pricing050.py` on a copy, with its
  output redirected) plus saving the 50 decimals; then the gap can be stated
  as ≤ 1.1e-17.
- Either keep 4.23e-14 (honest, conservative), or use 1.92e-14 with this
  dossier's check, or regenerate and save the verifier's point.

**C1. ex6_2_7/ex6_2_5: a third, independent tangent-plane certificate
(done for this dossier).** `gibbs_cert.py` differs from both earlier codes in
the parser, the expression handling, the bounding scheme and the arithmetic
organisation:
- own OSIL reader; each phase objective is decomposed by pattern matching
  into linear atoms and log atoms (ℓ·y) ln(m·y), and atoms with the same
  logarithm argument are merged exactly. Merging removes the large cancelling
  coefficients of the GAMS-Convert form (for example the four n_1 ln n_1
  pieces of ex6_2_7, 0.2407 + 11.24 + 2.248 − 12.7287, combine to
  1 − 2.1e-14). No sympy is used. The decomposition equals the OSIL tree at
  5 random points to < 1e-50;
- closed-form gradient and Hessian of the two atom types, checked against
  60-digit central differences to the truncation level of the differences
  (`gibbs_deriv_check.log`);
- local minimisers ŷ of D by 50-digit Newton from a grid and edge seeds
  (a proposal only: a missed minimiser with D ≤ 0 would make the exclusion
  step fail, not pass);
- around each ŷ a window W (half-widths 1e-3, except 5.1e-4 and 1.5e-7 in
  dilute coordinates) on which the reduced Hessian has λ_min ≥ ℓ, ℓ between
  1.04 and 16.1. This is proved on 8×8 sub-boxes with the exact monotonicity
  of λ_min of a symmetric 2×2 matrix in its diagonal entries and |off-
  diagonal|. On W, D ≥ D(ŷ) − ‖∇D(ŷ)‖²/(2ℓ), with ‖∇D(ŷ)‖ ≈ 1e-49;
- outside the windows an interval branch and bound (natural extension and
  mean-value form, 53-bit `iv`) proves D ≥ 0 (smallest fathomed lower bound
  7.3e-11 for ex6_2_7 and 3.1e-12 for ex6_2_5);
- assembly with Theorem G in `iv`; vapour of ex6_2_5 by Lemma G2.

| | ex6_2_7 | ex6_2_5 (liquid phases) |
|---|---|---|
| local minima D(ŷ) | 7.213e-15, 7.095e-15, −4.188e-15 | −1.24e-22, −1.38e-21 |
| certified m | ≥ −4.1878239e-15 | ≥ −1.3797006e-21 |
| exclusion boxes, time (one core) | 53,057; 63 s | 153,745; 198 s |
| dual bound | ≥ −0.1608476154636436069140 | ≥ −70.75207783344770558062989 |
| safe display (rounded down) | −0.16084761546364361 | −70.75207783344770558063 |
| gap to the rational primal point | 4.2745e-14 (≤ 4.3e-14) | 2.628e-19 (≤ 2.7e-19) |

The ex6_2_7 minimum −4.188e-15 is the floor the verifier predicted from the
r_p residual, so no λ certifies much below it. Both summary duals
(−0.16084761546364905 and −70.75207783344770759) are weaker than the new
values. They are therefore now supported by two independent implementations
at tight tolerance. The ex6_2_5 gap could be shown as ≤ 2.7e-19 (relative
3.8e-21) with the 20-decimal displays above. Trust: mpmath `iv` and
`Fraction` only; neither sympy nor `osilx.py` is used. Cost: 4.5 minutes on
one core, plus about two hours of coding.

### 8.3 Gaps in evidence, with resolutions

**E1. Before this dossier, the displayed Gibbs and etamac values rested on
one implementation.** The tight ex6_2_7/ex6_2_5 duals came from the
verifier's `gibbs_bb.py` (τ = 6e-15, 1e-17); the authors' independent code
certifies only τ = 1e-11 (gaps 3.0e-11 and 2.9e-9), and the verifier never
reviewed the authors' B&B code. For Gibbs this is now resolved by C1. The
etamac display −15.294675643368093 is still above the authors' bound
−15.294675643368096, so it rests on the verifier's `v_etamac.py` alone.
Resolution for etamac: (a) state the provenance in the paper, or display the
authors' weaker bound (gap ≤ 6.5e-15, exact 6.408e-15 against the exactly
feasible point); (b) an independent rebuild of the KKT point of R and the
tangent-plane bound with this dossier's reader and closed-form derivatives
would take about two hours of coding and under a minute to run. I read the
verifier's `gibbs_bb.py`, `gibbs_bound.py`, `ivgen.py` and `v_etamac.py`
line by line for this dossier and found no validity error: domain coverage
(root grid and exact discard test), clipping of y3, the hull used in the
mean-value and second-order forms, the endpoint argument for the interval
off-diagonal Hessian entry, the use of one phase-type bound for three
symmetric phases (backed by `gibbs_sym.py`'s identity check), the box
derivation from etamac's own rows, κ, and μ > 0 are all sound.

**E2. Saved artefacts.** The etamac and pricing050 points that give the
smallest gaps were not saved by the verifier. The etamac gap no longer
depends on this: this dossier defines an exactly feasible point from the
authors' saved decisions (gap 2.5765e-15 ≤ 2.6e-15, same cell). For
pricing050 see C3. Resolution for the data release: save the 25-digit
decisions of both verifier points (cost: two script runs on copies, < 1 min).

**E3. Common-mode parser.** The authors and the wave-2 verifier both used
`osilx.py`. Risk is low (both match expression trees by exact string
comparison), and it is now mitigated: this dossier's own ElementTree reader
reproduces the hvycrash structure, the Gibbs objectives (atom decomposition
equals tree evaluation to < 1e-50 at random points), the etamac rows (exact
point), the pricing050 structure and rows, and all six GAMS files agree with
the OSIL files numerically.

**E4. pindyck Hessian map.** Ψ is a hand derivation, and the concavity
proof is about Ψ. Evidence: two independent derivations, a symbolic check of
the implicit step, and finite-difference agreement to 1.7e-16 at 12 points
of G, including LP vertices where d < 0. A full computer-algebra proof of the
recursion for T = 2 or 3 periods (implicit s) would take under an hour and
seconds to run; I do not regard its absence as a gap in the proof, because
every step is the product rule or the implicit-function formula, both
checked.

**E5. Model provenance at the 1e-14 level.** The certificates hold for the
stored decimals, not for the source models: ex6_2_7 has the r_p residual
5e-14 (its bound term 5.5e-14 exceeds the final gap) and differs from the
handbook by up to 4.1e-14 relative; etamac has s − 1 = 4.14e-16; pricing050
has g = −1.0000000000000002e-2/e-3; pindyck uses k = 0.142857142857143 and
15-digit δ_t and c_t. The enclosures need not contain the optima of the
exactly specified source models. Resolution: wording (Section 9).

**E6. Unsafe secondary displays** (Section 5, item 1): do not copy
"−70.752077833447706" or "−70.75207783344770758".

**E7. Cosmetic log error.** The authors' etamac log prints "kappa − 1 ≤
3.11e-15"; mp.dps was 15 at that line. The true W^{s−1} − 1 for W = 2022.06
is 3.152e-15 (`etamac_point.log`); the certificate used the 40-digit interval
end and report.md says ≤ 3.2e-15. No effect on validity.

**E8. hvycrash proof status.** The authors and the verifier proved existence
with 50–60-digit intervals. Theorem 1(b) is analytic, and every number in it
was checked exactly (`hvy_check.log`). When writing the proof, note that an
upper bound on cos 2.6 needs an alternating partial sum that ends with a
*positive* term.

**E9. Hypotheses that could be weakened or are unused.**
- Gibbs: the upper bounds n ≤ b are not used; any λ works.
- etamac: the box is derived from etamac's rows, so it does not depend on the
  relaxation; μ ≥ 0 is checked on the decimal strings.
- pindyck: interiority of p* in G is not needed for the bound (only p* ∈ G);
  it is needed for the uniqueness corollary.

### 8.4 New observation for hvycrash (C4)

With any positive row tolerance τ, alg_k and acc_k can be satisfied
approximately by sending r_k → ∞: then alg_k = O(1/r_k), the k-th accumulator
increment tends to 0, and dyn_k forces θ_{k−1} ≈ θ_k. So tolerance-feasible
objective values cluster at −0.2185 + j·h, j = 0..50 (h = 0.00437), and range
up to about 0. Checks against published values:
- MINLPLib p1, p2: −0.21413 = −0.2185 + 1·h (r_50 = 2.5e7 and 1.6e9);
- COCONUT OQNLP point: −0.1573199996 = −0.2185 + 14h − 4e-10; its record
  lists "infeas = 14";
- COCONUT Fbest −0.0481 ≈ −0.2185 + 39h = −0.04807 (to the printed digits);
- the SIF's SOLTN(N) ≈ 1e-8 for N ≥ 100 is consistent with nearly all stages
  dropped.

Conversely, values below −0.2185 need |r_k| < 7.86 and are limited to
−0.2185(1 + 7.86τ) − 50τ, so Smith's −1.905 needs τ ≈ 0.03. This is
arithmetic on published numbers, not a reconstruction of those points
(except MINLPLib p1/p2, whose r_50 values were evaluated).

## 9. What the paper may claim and must not claim

**General.**
- May: "Each bound holds for every exactly feasible point of the stored
  MINLPLib (OSIL) model; the proofs are computer-assisted with
  outward-rounded interval and exact rational arithmetic, assuming correct
  mpmath interval primitives (hvycrash: pen and paper)."
- Must not: transfer the numbers to the source models (handbook, GAMS Model
  Library, CUTE, Davarnia–van Hoeve data) at the 1e-14 level; call
  tolerance-level points optimal; rank solvers.

**hvycrash.**
- May: "The objective of hvycrash is constant, equal to −0.2185, on the
  feasible set; a short proof and an explicit feasible point give the exact
  optimal value. The value −0.21850 is already recorded, without proof, in
  the CUTE SIF file. To the best of our knowledge the identity has not been
  stated before."
- May: the tolerance-artifact explanation (Section 8.4), labelled as such.
- Must not: claim discovery of the value or a computational result; give a
  physical interpretation.

**ex6_2_7 and ex6_2_5.**
- May: "We certify the MINLPLib models ex6_2_7 and ex6_2_5 to absolute gaps
  ≤ 4.9e-14 and ≤ 2.1e-15 against exactly feasible rational points. The
  optimal phase splits were very likely reported earlier as ε-global
  floating-point solutions (McDonald and Floudas), which we could not
  consult. To the best of our knowledge no rigorous certificate has been
  published. The Lagrangian tangent-plane argument is classical."
- Must: describe the evidence accurately: two independent implementations
  certify the displayed values (verifier; this dossier's C1), and the
  authors' code certifies weaker values (τ = 1e-11). If the C1 values are
  adopted, ex6_2_5 can be stated with gap ≤ 2.7e-19 and ex6_2_7 with
  ≤ 4.3e-14; C1 has not yet been reviewed by a second person.
- Must not: claim the first solution; cite BARON's "GOpt" label as a proof.

**etamac.**
- May: "closed to ≤ 2.6e-15 against an exactly feasible point. With the
  stored 15-digit exponents the CES aggregate has degree 1 + 4.14e-16 and is
  not exactly concave; a concave majorant restores a convex relaxation. The
  local optimum value was known; to the best of our knowledge no global
  certificate was published."
- Must not: say "the CES is concave" without the qualification; claim results
  for Manne's model.

**pricing050.**
- May: "upper bound −1813.8290784519730577; exactly feasible point with
  objective −1813.8290784519730769; gap ≤ 1.92e-14 (summary: ≤ 4.23e-14).
  Independent implementations agree." Use 1.1e-17 only after saving the
  verifier's point (C3).
- May: "A published primal value 1813.3 (min form) for what is very likely
  the same instance lies below our certified minimum; if the data agree, no
  feasible point attains it."
- Must not: state the instance identity as fact; cite "2.0e-17" (wrong).

**pindyck.**
- May: "The reduced objective is proved 0.001-strongly concave on a polytope
  containing the feasible price set; hence the KKT point is globally optimal
  up to 1.7e-29 (or, conservatively, 5.44e-14), and the maximizer is unique
  and within 3.7e-13 of it. To the best of our knowledge no global
  certificate was published; SCIP studies reported the instance unsolved."
- Must not: say J is concave on the price box or on F "because F is convex"
  (F is not known to be convex); quote COCONUT's −1612.18 as a value of this
  model.

**Umbrella sentence (label as interpretation).** "These six instances were
open not because their search spaces are hard, but because an exact identity
(hvycrash), phase separability with homogeneity (ex6_2_*), hidden convexity
(etamac), separability (pricing050) or concavity on a polytope (pindyck) is
invisible to termwise relaxations."

## 10. Candidate figures and tables

1. **Table (main text):** instance, sense, size, structure, mechanism,
   status class (Section 0).
2. **Table (main text):** listed dual/primal, our dual/primal, absolute and
   relative gap (Section 5), with a footnote for the tighter pindyck and
   pricing050 figures.
3. **Figure:** ex6_2_7 tangent-plane distance D(y) = G(y) − λ·y on the
   ternary simplex (log colour scale for D ≥ 0), marking the three phase
   compositions (0.0278, 0.0021, 0.9702), (0.6928, 0.0040, 0.3032),
   (0.2790, 0.4919, 0.2291), with the certified local minima 7.2e-15,
   −4.19e-15, 7.1e-15. Float evaluation suffices for the picture.
4. **Figure:** pindyck: sampled λ_max(∇²J) over G (−0.1195 to −0.1111)
   against the certified −0.001; optionally a 2-D slice of G and F through
   p*. Data: `R/reviews/pindyck-review-checks/logs/hess_check.log` and the
   extension's samples.
5. **Figure (small):** hvycrash tolerance artefacts: objective values
   −0.2185 + jh with published values marked (Section 8.4).
6. **Table (appendix):** decimal artefacts of the stored models (r_p = 5e-14;
   s − 1 = 4.14e-16; g = −1.0000000000000002e-2/e-3; k = 0.142857142857143)
   and their effect.
7. **Table (appendix):** published values shown unattainable or belonging to
   other models (hvycrash: COCONUT −0.0481, OQNLP −0.15732, Smith −1.905,
   SIF SOLTN(N ≥ 100); ex6_2_5: Kosolap −70.9586; pricing050: Davarnia 1813.3
   (conditional); pindyck: COCONUT −1612.18 (other model)).
8. **Table (appendix):** one-hour solver campaign rows for the six instances
   (`R/publication/solver-runs/results_table.md`): no closures; BARON cannot
   handle cos (hvycrash); SCIP memory stops on ex6_2_5, ex6_2_7, pindyck.
   Final duals (BARON, GUROBI, SCIP; "—" = no finite dual): hvycrash —,
   −2.1413e9, −2.185e8; etamac −16.51, —, −15.51; ex6_2_5 −157.3, −128.3,
   −592.1; ex6_2_7 −1.409, −1.584, −1.422; pindyck −3067, −1829, −1625;
   pricing050 (max, upper) −1055.0, −1418.1, −1514.5. SCIP's values concern
   slightly tightened log/power argument bounds.
9. **Table (appendix):** trust base and runtime per certificate (Section 6).

## Appendix A. Checks run for this dossier

Run on copies in `/tmp/smallchk/` (OSIL files from the MINLPLib cache, saved
logs copied from `R/`), single-threaded, at most two processes. Scripts and
logs are saved in
`/workspace/minlp-notes/paper-open-minlplib/development/dossiers/small-checks/r2/`.
No project-wide checks were run and no CI was inspected.

| script | what it does | result |
|---|---|---|
| `osil.py` | independent OSIL reader (ElementTree, exact decimal strings, `mult`/`incr` expansion) and evaluator | used by all checks |
| `hvy_check.py` | all 150 rows matched to the model in sympy (exact rationals, signs included); identities acc = s_{k−1} − s_k − h − h r·alg and dyn = 0.1(θ_{k−1} − θ_k) + h(A + 1)/r² + h·alg/r verified for all 50 stages; analytic point numbers (κ, cos 2.6 bracket, 50κ/0.85 < 0.4); 60-digit interval check of the point | objective −437/2000; κ = 81381972927/12500000000000; cos 2.6 ∈ [−0.8568890, −0.8568816]; max \|row\| ≤ 1.9e-60; θ ∈ [2.6565, 3]; objective enclosure contains −0.2185 (width 4e-62) |
| `gibbs_check.py` | own parse, phase separability, identical phases, r_p by sympy; exact assembly of both bounds from the verifier's saved τ and λ; primal rows exact and objective enclosure; display directions | ex6_2_7 bound ≥ −0.160847615463649043442…, gap 4.81819e-14; ex6_2_5 bound ≥ −70.75207783344770758035395, gap 1.99999e-15; vapour minimum 6.978e-22; summary displays valid; "−…758" and "−70.752077833447706" not valid |
| `gibbs_cert.py` | third tangent-plane implementation (Section 8, C1) | ex6_2_7: 3 minimisers, m ≥ −4.1878239e-15, 53,057 boxes, 63 s, dual ≥ −0.1608476154636436069140; ex6_2_5: 2 liquid minimisers, m ≥ −1.3797006e-21, 153,745 boxes, 198 s, dual ≥ −70.75207783344770558062989 |
| `gibbs_deriv_check.py` | closed-form gradient/Hessian of `gibbs_cert.py` against 60-digit central differences at 5 points per instance | max relative difference 4.6e-13 at (0.0567, 6e-7) (finite-difference truncation), ≤ 2e-15 elsewhere |
| `etamac_point.py` | exponent facts (exact); W^{s−1} for three W; exactly feasible point from the authors' saved decisions; row and bound checks; display checks | s − 1 = 4.1414e-16; W^{s−1} − 1 ≤ 2.8672e-15 (W = 1015.6), 3.1524e-15 (2022.06), 3.1607e-15 (2062.83); all rows consistent, margins ≥ 0.04735; objective −15.2946756433680895919829233612872…; gap 2.5765e-15 |
| `pricing_check.py` | own parse and structure; window + exclusion certificate of all 50 minima (247 boxes, 3 s); saved authors' point in `iv` | Σ min F_j ≥ −2721.77195359771241568725405377; UB ≤ −1813.82907845197305774994594623; display margin 5.0e-17; saved point feasible (slacks 3.4958e-15, 3.9173e-15), objective −1813.8290784519730769, gap 1.91501e-14 |
| `pindyck_sc.py` | strong-concavity bound from the review's saved exact enclosures | ‖g‖² ≤ 3.39889e-32; bound −1170.48628543608856208757742506930502…; gap ≤ 1.69945e-29 |
| `gmscheck/` (earlier dossier's `gms_vs_osil.py` on copies) | GAMS vs OSIL at 5 random points | identical output to the earlier run: rows ≤ 3.51e-51 relative, objectives exact |
