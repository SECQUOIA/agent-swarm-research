# Dossier: exactly feasible primal points across all result families

Family key: `primal-points`. Revised 2026-10-04 (second pass; supersedes the first-pass text of the same
date). Paths are relative to `research-20260929/` (written R/) unless they start with `paper-open-minlplib/`.
Numbers come from R/open-instances-summary.md (authoritative) and from the saved point files and logs named
in each row. My own checks are in `paper-open-minlplib/development/dossiers/primal-points-checks/` (scripts
and `logs/`). They ran on copies under /tmp and imported no research script from the tree.

## 0. Main points

- **All 31 closed instances have a primal side that is a point proved to satisfy every row, bound and
  integrality requirement of the stored OSIL model exactly**, with the file's decimal data read as exact
  rationals (Section 1.1). For 13 of them (lnts50/100/200/400, dtoc5, lukvle10, chain50/100/200/400,
  powerflow0030p/0039p/0039r) the original closure used points that violate rows by 2.4e-20 to 7.9e-12. The
  publication tracks R/publication/primal/ built exactly feasible points for these 13. Five independent r1
  reviews verified them. The same tracks supplied exact points for waterno2_06–24 and ann_cumene_tanh, and
  points of the relaxation R for the six KAN instances.
- **Five constructions suffice:**
  - (A) explicit exact points with rational or quadratic-field coordinates;
  - (B) triangular forward definitions, where each row is solved for one new variable;
  - (C) interval existence proofs: a Krawczyk test on a reduced or active-set square system, or a 1-D
    intermediate-value bracket;
  - (D) strictly interior points for inequality-only models;
  - plus an exact-identity witness (hvycrash).

  The point's objective is then enclosed rigorously. The gap is the upper end of that enclosure minus the
  certified dual, computed exactly and rounded upward.
- **Trust base.** Every interval existence proof for the 13 instances and for the water/ANN/KAN points was
  redone by an independent implementation that uses only Python integer and rational arithmetic, with
  explicit series remainder bounds. So "mpmath iv is correct" is *not* needed for these claims. This pass
  adds two items:
  - mpmath-free re-proofs of the eg_* primal points (Section 8.2; previously only 50/60-digit point
    evaluations, or the certifier's interval path under A1/A2);
  - mpmath-free re-proofs of the ex6_2_* objective enclosures.

  Five primal claims still rest on a single mpmath-iv implementation: hvycrash, etamac, pricing050, pindyck
  and optcdeg2.
- **The data semantics must be stated as part of the model definition (major, not invalidating).**
  - Every primal and dual proof reads each decimal string of the OSIL file as the exact rational it denotes.
  - The OSiL 2.0 schema types bounds, coefficients, constants and `number` values as `xs:double`, which I
    checked in the schema files (Section 8.2). Solvers read binary64.
  - Under a binary64 reading, the dtoc5, chain, powerflow, water, ANN, KAN, catmix and eg points are not
    exactly feasible.
  - The lnts and lukvle10 primal points are feasible under both readings.
- **A defect in the first-pass dossier check is corrected; no claimed result is invalidated.**
  - The first-pass `eg_iv_check.py` negated `Decimal` intervals with Python's unary minus. That operation
    rounds to nearest at 28 digits, so its "outward-rounded proof" was not valid as written.
  - I fixed it and added an independent library-free dyadic-interval proof. Both confirm the eg points,
    with margins of at least 5.57e-20.
  - I recomputed every gap and display direction for the 13 instances and the water/ANN/KAN points exactly
    and found no disagreement with the summary.
  - New finding for the artifact list: MINLPLib's listed lnts50 p1 has objective 0.55466876489565, which
    is 4.25e-11 *below* the certified dual. It is a tolerance artifact (Section 9).

## 1. Instances and models

### 1.1 What "exactly feasible" means (model definition for the paper)

The model is the OSIL file cached at `~/.cache/minlplib/minlplib/osil/<name>.osil`. The 2026-10-02 status
refresh found it byte-identical to the live file (R/publication/minlplib-status/data/part_a.json). SHA-256
prefixes of the 13: lnts50 3d8234b3, lnts100 284bddc3, lnts200 c2dde9ef, lnts400 96eb4456, dtoc5 ac7b2d94,
lukvle10 1eb1236d, chain50 f6b2b409, chain100 45cb3020, chain200 634acc62, chain400 7cd93486,
powerflow0030p 5c4b386b, powerflow0039p 0a27073f, powerflow0039r d8ba3132.

**Definition (proposed for the paper).**
- Read every numeric string of the OSIL file as the rational number it denotes in decimal. This covers
  variable and row bounds, linear and quadratic coefficients, `coef` attributes, `number` nodes, and
  objective and row `constant` attributes.
- Apply the OSiL defaults: variable bounds [0, +∞), type continuous, row bounds (−∞, +∞), `coef` 1,
  `constant` 0.
- Read `sqrt` as the nonnegative root and `power(a, b)` with a > 0 as exp(b ln a).
- This gives a real-number model min{f(x) : x ∈ F}.
- A point x is *exactly feasible* if x ∈ F, with every row, every bound and every integrality
  requirement holding with no tolerance.
- A number L is a *valid dual bound* if L ≤ f(x) for every exactly feasible x.

Three readings of "the MINLPLib model" are possible, and they differ at the 1e-16 relative level:
- (a) the .gms text with exact decimals;
- (b) the OSIL text with exact decimals, which **all our certificates use**;
- (c) binary64 data, which is what solvers see and what the OSiL schema's `xs:double` typing implies.

For the 13 instances, (a) and (b) agree by 60-digit evaluation (status report; evidence, not an
algebraic proof). For catmix, (a) ≠ (b): MINLPLib's OSIL prints binary64 products such as
0.045000000000000005 for 9/200. The claims are for (b). Section 8, PP-1 gives consequences and wording.

### 1.2 The 13 formerly tolerance-only closures

All 13 are continuous NLP or QCQP minimization models without integer variables. Sizes are counted from
the OSIL files.

**lnts50/100/200/400 (NLP; 5N+6 variables, 4N equality rows: 256/200, 506/400, 1006/800, 2006/1600).**
- *Source.* GAMS `lnts`, which is COPS 2.0 problem 9, the linear tangent steering problem. A particle with
  thrust acceleration of magnitude 100 in direction θ(t) must reach height 5 with horizontal speed 45 and
  vertical speed 0 in minimum time. The trapezoidal rule with N steps of length h discretizes the problem.
- *Variables.* θ_0..θ_N ∈ [−1.5707963267949, 1.5707963267949], then px, py, vx, vy (N+1 each), then
  h ≥ 0.
- *Fixed values.* px_0 = py_0 = vx_0 = vy_0 = vy_N = 0, py_N = 5, vx_N = 45; all other states are free.
- *Objective.* min N·h.
- *Rows* (i = 0..N−1):

      px_{i+1} − px_i − (h/2)(vx_i + vx_{i+1}) = 0,   py_{i+1} − py_i − (h/2)(vy_i + vy_{i+1}) = 0,
      vx_{i+1} − vx_i − 50h(cos θ_i + cos θ_{i+1}) = 0, vy_{i+1} − vy_i − 50h(sin θ_i + sin θ_{i+1}) = 0.

- *Data.* Every constant is binary64-exact except ±1.5707963267949.

**dtoc5 (QCQP; 99,999 variables, 49,999 equality rows).**
- *Source.* QPLIB_8585 (an identical file), from CUTEst DTOC5 (Coleman–Liao problem 5), with T = 49,999
  and h = 1/50000.
- *Variables.* u_t = x_{t+2} (t < T) and y_t = x_{50001+t} (t ≤ T). All are free except y_0 = 1.
- *Model.*

      min h (Σ_{t<T} u_t² + Σ_{t<T} y_t²)   s.t.   −h u_t + y_t − y_{t+1} + 4h y_t² = 0   (t = 0..T−1).

- *Data.* The OSIL coefficients are the strings 2e-5 and 8e-5, read as 1/50000 and 1/12500; neither is
  binary64-exact.
- *Provenance.* CUTEst has h·y_t²; MINLPLib has 4h·y_t² (control literature report). The claims are for
  MINLPLib's model.

**lukvle10 (NLP; 1000 free variables, 998 equality rows).**
- *Source.* CUTEst LUKVLE10, Lukšan–Vlček problem 5.10, with N = 1000.
- *Model* (0-based indices):

      min Σ_{i=0}^{499} [ (x_{2i}²)^{x_{2i+1}²+1} + (x_{2i+1}²)^{x_{2i}²+1} ]
      s.t. −x_j + 3x_{j+1} − 2x_{j+2} − 2x_{j+1}² = −1   (j = 0..997).

- *Data.* All constants are integers. The objective is written with OSiL `power` nodes over `square`
  bases.

**chain50/100/200/400 (NLP; 2N+2 variables, N+1 equality rows).**
- *Source.* GAMS `chain`, which is COPS 2.0 problem 3: a hanging chain of length 4 between heights 1 and 3.
- *Variables.* x_0..x_N (height) and u_0..u_N (slope). All are free except x_0 = 1 and x_N = 3.
- *Model.* With η = 1/(2N), weights w_0 = w_N = 1 and w_i = 2 otherwise, and s_i = √(1+u_i²) (OSiL
  `sqrt` nodes):

      min η Σ_{i<N}(s_i x_i + s_{i+1} x_{i+1})
      s.t. x_{i+1} − x_i − η(u_i + u_{i+1}) = 0 (i < N),   η Σ_{i<N}(s_i + s_{i+1}) = 4.

- *Data.* η is written 1e-2, 5e-3, 2.5e-3 and 1.25e-3; none is binary64-exact.

**powerflow0030p/0039p/0039r (AC optimal power flow).**
- *Source.* Hijazi–Coffrin–Van Hentenryck models. 0030p is MATPOWER case30 without its two bus shunts, in
  polar form. 0039p and 0039r are MATPOWER case39 with transformer taps dropped, in polar and rectangular
  form (network literature report).
- *Variables.* All are free; every bound is written as a row. There are no integers.
- *Rows.* Flow definitions, nodal balances, line limits P² + Q² ≤ s², voltage-magnitude rows, ±0.26 rad
  angle-difference rows (polar models) and single-variable bound rows.
- *Objective.* A quadratic generation cost; 0039p and 0039r carry an objective `constant="2"`, which both
  readers apply.

| instance | type | variables | rows (equalities) | non-binary64-exact distinct strings |
|---|---|---|---|---|
| powerflow0030p | NLP | 236 | 555 (225) | 172 |
| powerflow0039p | NLP | 282 | 657 (263) | 245 |
| powerflow0039r | QCQP | 282 | 473 (263) | 264 |

*Provenance.* MINLPLib's 0030p and 0030r differ by coefficient rounding, so no rigorous statement
transfers between them without a perturbation argument.

### 1.3 Other families: structure used by the point construction

| family | structure exploited by the exact point | provenance caveat relevant to the point |
|---|---|---|
| camshape100–800 | rows linear in u = 1/r; the min-plus envelope E is feasible and optimal | QPLIB copies have rounded constants |
| optcdeg2 | given the controls, the states follow by forward simulation; one control is left free to make v_N = 0 | CUTEst damping coefficient differs by a factor of 4 |
| hvycrash | alg_k gives r_k = √(−cos θ_k/D_k); dyn_k is linear in θ_{k−1}; the objective is constant on the feasible set | none for the point |
| ex6_2_5 / ex6_2_7 | the only rows are linear mass balances; phase 2 is defined as b − (other phases) | none |
| etamac | the linear and CES rows define the states from (I_t, LN_t, EN_t) | scaled source models differ |
| pricing050 (max) | inequality rows only | none |
| pindyck | prices p determine all states; each fringe-supply row has a unique root s_t | COCONUT's model is a mistranslation |
| catmix100–800 | given the controls, the trapezoid rows are linear in the states | OSIL constants are binary64 products (≤ 1.78e-16 relative from .gms); claims are for OSIL |
| eg_int_s / eg_disc_s / eg_disc2_s | 28 inequality rows (24 minimax rows with Gaussian-kernel exp terms, 4 side rows); 3 integers | none for the point |
| waterno2_06–24 | with the binaries fixed, rows are polynomials of degree ≤ 3; each running station's speed is a root of a quadratic | Huang's extended models differ |
| ann_cumene_tanh | a feedforward network; every equality row defines one variable | none for the point |
| KAN r3/r5 | as ANN, plus B-spline one-hot and big-M rows; the partition-of-unity rows are exactly inconsistent | claims concern the relaxation R only |

## 2. Listed status of the 13

Source: MINLPLib pages fetched 2026-09-29, unchanged at the 2026-10-02 refresh (part_a.json); re-read for
this pass (`logs/listed_display_check.log`). **None of the 13 is marked solved.** The listed primal values
are page displays with 7–10 significant digits, rounded to nearest.

| instance | best listed dual (solver) | listed best primal display (point, MINLPLib infeas.) | display − our safe dual |
|---|---|---|---|
| lnts50 | 0.55464755 (GUROBI) | 0.55466876 (p1, 9e-10) | −4.94e-9 |
| lnts100 | 0.55299042 (GUROBI) | 0.5545954 (p1, 8e-15) | −1.17e-9 |
| lnts200 | 0.55219867 (GUROBI) | 0.55457702 (p1, 9e-14) | +3.90e-9 |
| lnts400 | 0.55204395 (GUROBI) | 0.55457241 (p1, 3e-10) | −3.70e-9 |
| dtoc5 | 0.00243096 (BARON) | 5.38967212 (p1, 6e-17) | +8.19e-10 |
| lukvle10 | 351.223393 (SCIP) | 352.2380254 (p5, 9e-16) | −5.08e-9 |
| chain50 | 0.17451499 (ANTIGONE) | 5.07226149 (p1, 2e-16) | −3.98e-9 |
| chain100 | 0.09367008 (ANTIGONE) | 5.06978461 (p1, 4e-16) | −7.39e-10 |
| chain200 | 0.08256615 (ANTIGONE) | 5.06891734 (p1, 4e-16) | −1.79e-9 |
| chain400 | 0.09563835 (ANTIGONE) | 5.0686217 (p1, 9e-16) | +5.40e-9 |
| powerflow0030p | 572.8395847 (GUROBI) | 576.8934135 (p1, 6e-15) | +1.20e-6 |
| powerflow0039p | 41818.27916 (GUROBI) | 41869.05151 (p1, 9e-14) | +2.51e-5 |
| powerflow0039r | 41804.88153 (GUROBI) | 41869.05151 (p1, 8e-12) | +2.67e-5 |

**Caution.** Several displays lie *below* our certified duals only because of display rounding. Such a
display is not evidence of infeasibility. Only an evaluated objective below a certified dual is evidence.
For the four lnts p1 points, I evaluated N·h exactly (`logs/lnts_p1_check.log`):

| point | f(p1) | f(p1) − certified dual N·h2 |
|---|---|---|
| lnts50 p1 | 0.55466876489565 | **−4.25e-11 (tolerance artifact)** |
| lnts100 p1 | 0.5545954011684 | +2.0e-12 |
| lnts200 p1 | 0.5545770161058 | +3.3e-12 |
| lnts400 p1 | 0.5545724137156 | +1.5e-11 |

The lnts50 file is R/open-instances/minlplib_sol/lnts50.p1.sol. The other three were fetched from
minlplib.org/sol on 2026-10-04; their hashes are in the log.

The earlier closures used these tolerance-feasible primal points:

| instances | earlier primal point | maximum row violation (source) |
|---|---|---|
| lnts50–400 | own tangent-law/KKT vectors | 4.6e-15–6.9e-15 (open-instances report); 5.3e-15–1.3e-14 for the same vectors in the verifier's evaluation |
| dtoc5 | double-precision Newton point | 2.4e-20 (open-instances report) |
| lukvle10 | MINLPLib p5 | 3.48e-15 (dtoc5-lukvle10 report and review) |
| chain50–400 | wave-2 double points | ≤ 3.6e-16 (COPS report) |
| powerflow0030p/0039p/0039r | MINLPLib p1 | 2.1e-13 / 1.2e-12 / 7.9e-12 (powerflow report and review) |

## 3. The certificates: how exact feasibility is proved

### 3.0 The idea in plain words

A floating-point point that "satisfies" a nonlinear equality does so only up to rounding. Its objective
value is not a valid upper bound on the optimum, and it can even lie below a true lower bound. Rounding the
point to rationals does not help, because rounded rationals rarely satisfy nonlinear equalities exactly.

We instead *define* a point mathematically so that most rows hold by construction:
- solve each row for one variable (B);
- keep exact rational or algebraic numbers (A);
- or prove that a small square system has exactly one root in a tiny box (C).

We then check every remaining row and bound, either exactly or by outward-rounded enclosures with a
nonnegative margin. The point need not be written out in decimals; it suffices to prove that it exists
and to enclose its objective tightly. The gap is the upper end of that enclosure minus the certified dual.

### 3.1 Objective enclosure and gap

**Lemma 0.** Let x* be exactly feasible for min{f(x) : x ∈ F}, let x* ∈ X, and let [f̲, f̄] ⊇ f(X). Let L be
a valid dual bound and v* the optimal value. Then L ≤ v* ≤ f(x*) ≤ f̄. Hence f̄ − L, computed in exact
rational arithmetic and rounded upward, bounds both v* − L and f(x*) − v*.

For maximization (pricing050), exchange the directions: primal displays round down, dual displays round
up. All dual displays used are truncations or outward roundings of certified values, so each display is
itself a valid bound. Relative gaps divide by the denominator stated per row of the summary.

### 3.2 Method A: explicit exact points

**Proposition A.** Suppose each coordinate of x lies in a field where equality and sign are decidable:
- Q; or
- Q(√D) with D > 0 a rational non-square. The sign of p + q√D is the common sign when p and q have the
  same sign or one is zero. Otherwise it is sign(p) if p² > q²D, and sign(q) if p² < q²D.

Suppose also that each row uses only field operations and `sqrt`, and that each `sqrt` is evaluated by
exhibiting s in the field with s ≥ 0 and s² = argument. Then exact evaluation decides feasibility, and
the objective is an exact field element.

*Proof.* Field arithmetic is exact. The sign rule follows from p + q√D = (p² − q²D)/(p − q√D) when p and q
have opposite signs. The nonnegative square root is unique. ∎

**Uses.**
- dtoc5: rational coordinates.
- chain: coordinates in Q(√R).
- camshape: rational envelope point.
- catmix: rational controls, with the states the exact solution of the linear trapezoid rows.
- ex6_2_*: rational point and linear rows. The objective's ln terms are enclosed separately.
- waterno2: each coordinate is rational or lies in one field Q(w_k). Here w_k is the unique root of
  A w² + B w + C in a rational isolating interval (lo, hi) of width 2e-45, and the quadratic changes sign
  on (lo, hi). The checkers write w_k = (−B + s√d)/(2A), with d = B² − 4AC not a square and the sign s
  fixed from (lo, hi). No row mixes two fields; the reviewer confirmed this with an evaluator over
  Q(√D_1, …, √D_m).

**dtoc5 construction** (R/publication/primal/dtoc5-lukvle10/report.md).
1. Take y from the double-precision Newton solution and polish it with three 50-digit Newton steps; the
   maximum gradient fell 2.9e-11 → 4.8e-26 → 4.3e-46.
2. Round y_1..y_T to 30 decimals and set y_0 = 1.
3. *Define* u_t := 50000(y_t − y_{t+1}) + 4y_t², which is row t solved for u_t. Each u_t is a decimal
   with at most 60 places.

Every row then holds identically. The objective is an exact rational with a 124-digit denominator,
5.38967211918114046742396649913627186883….

**Proposition A.1 (chain reduction).** Let x_0 = 1 and define x_1..x_N by the linear rows. Then
x_N = 1 + η Σ_i w_i u_i, so x_N = 3 ⇔ Σ_i w_i u_i = 4N, and the length row holds ⇔ Σ_i w_i s_i = 8N.

For t_i > 0, put u_i = (t_i − 1/t_i)/2. Then s_i = (t_i + 1/t_i)/2 = √(1+u_i²) exactly, and the two
conditions become

    Σ_i w_i t_i = 12N   and   Σ_i w_i / t_i = 4N.

Fix t_i for i ∉ {a, b} at rationals, with a = 1 and b = N−1 (the smallest and largest t at the start
point) and t rounded to 20 decimals. Put α = (12N − Σ' w t)/2 and β = (4N − Σ' w/t)/2. Then
t_a + t_b = α and t_a t_b = α/β, so t_a and t_b are the roots of T² − αT + α/β. They lie in Q(√R), where
R = num·den of α² − 4α/β; R has 1,928, 3,755, 7,323 and 14,507 digits for N = 50, 100, 200 and 400.

*Proof.*
- Summing the linear rows gives x_N − x_0 = η Σ_{i<N}(u_i + u_{i+1}) = η Σ w_i u_i. Since 1/η = 2N,
  x_N = 3 ⇔ Σ w u = 4N.
- The length row reads η Σ w s = 4, that is, Σ w s = 8N.
- With t = u + s and 1/t = s − u (because s² − u² = 1): Σ w t = 12N and Σ w/t = 8N − 4N = 4N.
- Conversely, every t > 0 gives u ∈ R and s = (t + 1/t)/2 > 0 with s² = 1 + u².
- Both roots are positive because α > 0, α/β > 0 and the discriminant is positive; the build and both
  checkers verify this. ∎

The swapped root order is also exactly feasible, with objective 6.326 (chain review). The generator
therefore records "smaller root at a".

### 3.3 Method B: triangular forward definitions

**Proposition B.** Order the variables so that a seed set S gets exact values. For each non-seed x_k,
choose a distinct equality row r_k(x) = a_k(x_{<k})·x_k + b_k(x_{<k}) − β_k. Here x_k does not occur in
a_k, in b_k or in any nonlinear subterm. Suppose an outward-rounded enclosure of a_k, computed from the
enclosures of earlier variables, excludes 0. Then:
- x_k := (β_k − b_k)/a_k defines a unique real point x* satisfying every r_k exactly;
- the computed enclosures contain x*.

If every other row, bound and integrality requirement is then verified (exactly, or over enclosures with
nonnegative margin), x* is exactly feasible.

*Proof.* Induction on k. The definition is valid because a_k(x*_{<k}) lies in an enclosure that excludes
0. The row then holds by algebra, and inclusion isotonicity keeps x*_k in its computed enclosure. ∎

**Uses.**
- lukvle10: seeds x_0 and x_1; a_k = −2 is constant; x* is rational.
- ann_cumene_tanh: 5 rational inputs and 789 defining rows. These are tanh rows, plus bilinear rows
  divided by x753, x746 or x766, whose enclosures exclude 0.
- KAN points of R: the inputs are the exact binary64 wave-3 inputs. The binaries are chosen so that the
  big-M rows hold over the whole enclosure of each edge argument. The partition rows are never used.
- hvycrash: backward definitions r_k = √(−cos θ_k/D_k), with cos θ_k ≤ −0.490 proved by intervals, and
  θ_{k−1} from dyn_k.
- etamac (verifier's point): I_t, LN_t and EN_t fixed at 25-digit decimals; all other variables defined
  by the linear and CES rows.
- pindyck: each implicit row s_t = 0.75 s_{t−1} + 1.02^(−κ cs_t)(1.1 + 0.1 p_t) has its unique root
  isolated by a 1-D interval Newton inclusion N(X) ⊂ int X (an instance of Theorem C with n = 1).

### 3.4 Method C: interval existence proofs

**Theorem C (Krawczyk test with uniqueness).** Assumptions:
- X ⊂ R^n is a box with componentwise width W > 0, and y ∈ X;
- F is C¹ on an open set containing X;
- 𝐀 is an interval matrix with F′(x) ∈ 𝐀 for all x ∈ X;
- 𝐟 is an interval vector with F(y) ∈ 𝐟;
- C ∈ R^{n×n} is any real matrix (in practice a binary64 approximate inverse, used as exact rationals).

Let 𝐁 ⊇ {I − CA : A ∈ 𝐀} and let K be any interval vector with

    K ⊇ y − C𝐟 + 𝐁 (X − y),

for example the result of evaluating this expression in outward-rounded interval arithmetic. If
K ⊆ int X, then:
- (a) C and every A ∈ 𝐀 are nonsingular;
- (b) F has exactly one zero x* in X, and x* ∈ K.

*Proof.*
1. *Mean value form.* For x ∈ X, apply the mean value theorem to each component F_i on the segment [y, x]
   ⊆ X. This gives F(x) − F(y) = M_x (x − y), where row i of M_x is ∇F_i(ξ_i) for some ξ_i ∈ X. Hence
   M_x ∈ 𝐀.
2. *Existence.* Let g(x) = x − CF(x). Then g(x) = y − CF(y) + (I − CM_x)(x − y). Each entry lies in
   the corresponding entry of y − C𝐟 + 𝐁(X − y), so g(x) ∈ K ⊆ X. The continuous map g sends the convex
   compact set X into itself. By Brouwer's theorem there is x* = g(x*), so CF(x*) = 0 and x* ∈ K.
3. *Nonsingularity.* Write |𝐁_ij| = max{|b| : b ∈ 𝐁_ij}. The interval 𝐁_ij·(X_j − y_j) contains
   b·(X_j − y_j) for some b with |b| = |𝐁_ij|. That set has width |𝐁_ij| W_j, because X_j − y_j is an
   interval of width W_j containing 0. Interval sums add widths, and outward rounding only enlarges
   intervals. Hence width(K_i) ≥ Σ_j |𝐁_ij| W_j. Since K ⊆ int X, width(K_i) < W_i, so |𝐁| W < W
   componentwise.

   Let D = diag(W). Then q := ‖D⁻¹|𝐁|D‖_∞ = max_i (|𝐁|W)_i / W_i < 1. For A ∈ 𝐀, |I − CA| ≤ |𝐁|
   entrywise, so ‖D⁻¹(I − CA)D‖_∞ ≤ q < 1. Hence CA = I − (I − CA) is nonsingular (Neumann series), and
   so are C and A.
4. *Zero and uniqueness.* By step 3, CF(x*) = 0 implies F(x*) = 0. If also F(z) = 0 with z ∈ X, then
   0 = M(z − x*) with M ∈ 𝐀 from step 1 (componentwise mean values on [x*, z] ⊆ X). M is nonsingular, so
   z = x*. ∎

This is the classical Krawczyk (1969) / Moore (1977) existence test, with the standard strict-inclusion
uniqueness argument (Neumaier 1990, Ch. 5). Because the proof above is self-contained, the paper need not
cite a theorem number that the reviewers could not check (powerflow r1 review, issue 6). The statement
allows y ≠ mid X and outward-rounded boxes X′ that contain the exact decimal box. If the computed K
satisfies K ⊆ int X_dec ⊆ X′, then the unique zero in X′ lies in X_dec.

**C1: reduced-system Krawczyk (lnts).**
- *Reduction.* For fixed rational controls θ_1..θ_{N−1} and any z = (θ_0, θ_N, h), the rows determine all
  free states uniquely by

      v_{i+1} = v_i + 50h(f(θ_i) + f(θ_{i+1})),   p_{i+1} = p_i + h(v_i + v_{i+1})/2,

  starting from 0, for (v, f) = (vx, cos), (vy, sin). Each row has coefficient 1 on its "next" state, so
  all 4N rows hold identically. The three remaining fixed values hold if and only if
  F(z) := (vx_N(z) − 45, vy_N(z), py_N(z) − 5) = 0; px_N is free.
- *Independent derivation.* The reviewer re-derived this elimination generically from the OSIL: it solves
  197, 397, 797 and 1597 rows and leaves exactly 3.
- *Test.* Theorem C is applied to F on the stored box:
  - centre: an exact 75-digit decimal;
  - radius 1e-50 for θ_0 and θ_N and 1e-52 for h;
  - Jacobian: forward-mode differentiation of the recursion;
  - C: the inverse of the midpoint Jacobian.
- *Bounds.* |θ| ≤ 0.9523 and h > 0 hold on the box.
- *The point.* x* consists of the rational controls, z*, and the recursion states.

**C2: active-set square system (powerflow).** Starting from MINLPLib's p1:
1. Determine the active set with a slack cutoff of 1e-9. The separation is clean:
   - active slacks are at most 6.8e-13;
   - the next inactive slacks are 4.3e-4 (0030p, e215), 1.08e-3 (0039p, e346) and 2.3e-3 (0039r, e306).
2. Fix as exact rationals:
   - variables of single-variable equality rows;
   - variables at active single-variable bound rows (0030p: x29 = 21/20; 0039p: x30–x36 and x38 = 53/50,
     five Pg at their upper bounds and Qg x273 = 7/5; 0039r: the same six generator bounds);
   - the remaining degrees of freedom, chosen by column-pivoted QR and kept at p1's decimals.

   Free/fixed counts are 222/14, 262/20 and 270/12.
3. Form the square system S from the non-fixing equality rows plus the active multi-variable inequality
   rows taken as equalities (e208 and e211 in 0030p; e307–e313 and e315 in 0039r; none in 0039p). S has
   222, 262 and 270 rows.
4. Apply Theorem C to S on a box of radius 1e-45 around a 60-digit centre. The test passes with
   max|K − c|/r = 1.930e-12, 2.859e-12 and 5.376e-12 (reviewer), and with ‖I − C𝐉(X)‖_∞ ≤ 1.930e-12,
   2.855e-12 and 5.376e-12.

Every OSIL row is then covered in one of three ways:
- it is in S, with its side inside the row bounds;
- all its variables are fixed, and it is checked exactly;
- it is enclosed over X strictly inside its bounds. The smallest margins are 4.30e-4 (e215), 1.08e-3
  (e346) and 2.29e-3 (e306).

This is the "approximate active set plus Krawczyk on a square subsystem" scheme (Section 7), applied once
at a known near-optimal point.

**C3: one-dimensional bracket (optcdeg2; verifier).**
- The controls are set to exactly ±1/5, u_3091 to the stored double, and u_47290 is left free in
  [u* − 1e-40, u* + 1e-40].
- Forward simulation in 200-bit mpmath intervals gives v_N(a) = −3.8e-44 < 0 < v_N(b) = +3.8e-44.
- All state and control bounds hold over the whole bracket.
- v_N is a continuous function of u_47290, so by the intermediate value theorem some u_47290 in the
  bracket gives v_N = 0. Hence f* ≤ 293.87607509587509328.

### 3.5 Method D: strictly interior points (inequality-only rows)

If every row is an inequality, a rational point is exactly feasible when its outward-rounded row
enclosures lie on the feasible side (margin ≥ 0 for non-strict rows) and its bounds and integrality hold
exactly.
- pricing050: KKT minimizers rounded to 25 digits; the verifier found row slack ≥ 1.1e-18. The objective
  is linear and therefore exact.
- eg_*:
  - the decision variables are the exact decimals of the binary64 search point, and the integers are
    exact;
  - objvar is a 20-digit decimal above the maximum of the 24 minimax requirements;
  - only eg_int_s needed a push into the interior of a nearly active side row (e26 margin 1.49e-11);
  - this pass re-proved all three points with two interval implementations (Section 8.2).

### 3.6 What the computation checks, in what arithmetic, and what must be trusted

| instances | claim checked | author arithmetic | independent re-proof (reviewer or this dossier) |
|---|---|---|---|
| dtoc5 | every row, bound and objective, exactly | Fraction; two OSIL readers (own and osilx.py) | reviewer: own reader, Fraction; dossier: third reader (`dtoc5_check.py`, re-run here) |
| chain50–400 | every row and bound exactly in Q(√R); objective enclosed with isqrt | Fraction + isqrt (separate build and verify scripts) | reviewer: own reader, Q(√D) with rational D; dossier: chain50/100 (`chain_check.py`, re-run here) |
| lnts50–400 | Krawczyk on F; bounds and objective over the box | mpmath iv at 110 digits; crosscheck.py (verifier's reader, closed-form Jacobian) | reviewer: mpmath iv at 120 digits **and** `verify_no_mpmath.py` (dyadic integers at 2^-430, alternating-series sin/cos remainders) |
| lukvle10 | recursion enclosure; objective via exp/log | mpmath iv at 750 digits; second author implementation in integer fixed point with Taylor/atanh remainders | reviewer: integer fixed-point coordinates (2^-3400); objective by integer-only ln/exp (`objective_noniv_lukvle10.py`) |
| powerflow ×3 | Krawczyk on S; all rows; objective | mpmath iv at 80 digits; osilx.py reader (SHA-256 4bcdc1d8…) | reviewer: `dyiv.py` (dyadic 2^-320, Taylor sin/cos with Lagrange remainder), own reader; numpy only for the preconditioner C, which need not be exact |
| waterno2 ×5 | every row and bound exactly in Q(w_k) | Fraction; second exact checker (Q(√d) pairs) | reviewer: multi-quadratic field Q(√D_1, …, √D_m), exact |
| ann_cumene_tanh, KAN ×6 | forward definitions; all other rows and bounds by enclosure | mpmath iv at 60 digits | reviewer: `rint.py` (rationals rounded outward to 320 bits; exp by Taylor with Lagrange remainder) |
| eg ×3 | 28 inequality rows, bounds and integrality | 50-digit point evaluation (verify_primal.py) and the certifier's interval path (under A1/A2) | reviewer: 60-digit point evaluation (not interval); **dossier: `eg_dyadic_check.py` (library-free dyadic intervals, own exp bounds) and corrected `eg_iv_check.py` (Python decimal, directed rounding)** |
| ex6_2_5 / ex6_2_7 | rows exact; objective (ln terms) enclosed | authors' tolerance point (not exact) | verifier: exact rational point, objective in mpmath iv; **dossier: `ex62_check.py` (Fraction intervals, atanh series)** |
| camshape ×4 | envelope exact; objective = bound | Fraction | verifier: own exact rational code |
| catmix100/200/400/800 | exact simulation of rational controls (states solve the linear trapezoid rows) | authors: 60-digit interval simulation of their controls (reproduction/cops/logs/a_catmix_primal_*.log) | verifier: exact rational simulation of the 100/200 author points (`v_catmix_model_all.log`, "exact J") and of the 800 DP-policy point (policy_exact.py); dossier first pass: catmix400 author point exactly (`catmix400_author_exact.log`) |
| optcdeg2, hvycrash, etamac, pricing050, pindyck | IVT bracket / backward definitions / forward definitions / interior point / interval Newton | authors' points numerical only | verifier only, mpmath iv (single implementation); hvycrash has two different points from two implementations |

**Trust base, stated precisely.**
- (T1) Python integer and `fractions.Fraction` arithmetic and `math.isqrt` are correct.
- (T2) At least one of the two independent implementations per instance is correct. Their agreement, and
  negative controls in every track, are evidence. "Independent" means separately written code and
  readers. The authors and reviewers are AI agents, so a shared misreading of OSiL semantics is the main
  common-mode risk. SCIP's OSiL reader mitigates it: SCIP accepted the chain points at feastol 1e-13/1e-12
  and the powerflow points at 1e-9 (floating point, evidence only). So do the small residuals of
  MINLPLib's listed points under our readers.
- (T3) The OSIL file is read with the semantics of Section 1.1. Each family has at least two readers.
- (T4) Classical theorems: the mean value theorem, Brouwer's fixed-point theorem, the Neumann series, the
  intermediate value theorem, the alternating-series and Lagrange remainder bounds, and the
  Lindemann–Weierstrass theorem (Proposition L only).

**Not needed** for the 13 instances, water, ANN, KAN, eg_* and ex6_2_*: mpmath iv, libm, numpy. Needed
as a single implementation: mpmath iv for hvycrash, etamac, pricing050, pindyck and optcdeg2. The eg dual
side keeps A1/A2; that belongs to the eg dossier.

### 3.7 Obstructions to rational points

**Proposition L (lnts has no algebraic point).** In every exactly feasible point of lnts<N>, at least one of
θ_0, …, θ_N, h is transcendental. In particular, no exactly feasible point has all coordinates rational.

*Proof.*
1. Suppose all θ_j and h are algebraic. If h = 0, the recursion gives vx_N = 0 ≠ 45, so h ≠ 0.
2. The vx recursion gives vx_N = 100h Σ_j w_j cos θ_j with w = (½, 1, …, 1, ½). So
   Σ_j w_j cos θ_j = q := 45/(100h), an algebraic number.
3. Group the indices by a = |θ_j| and let c_a = Σ_{|θ_j|=a} w_j > 0. Since cos a = (e^{ia} + e^{−ia})/2,

       (c_0 − q)·e^0 + Σ_{a>0} (c_a/2)(e^{ia} + e^{−ia}) = 0.

4. The exponents 0 and ±ia (a > 0) are distinct algebraic numbers. By the Lindemann–Weierstrass theorem
   (Baker's form: e^{β_1}, …, e^{β_m} are linearly independent over the algebraic numbers for distinct
   algebraic β_k), every coefficient vanishes. Since c_a > 0, no a > 0 occurs, so every θ_j = 0.
5. Then vy ≡ 0 and py ≡ 0, which contradicts py_N = 5. ∎

This strengthens the rational version (lnts report; primal-lnts review r1, item 8) and explains why lnts
needs an interval existence proof.

**lukvle10.** Row j gives x_{j+2} = (1 − x_j + 3x_{j+1} − 2x_{j+1}²)/2. With rational seeds, the
denominator of each new coordinate is generically 2·den(x_{j+1})², so its size doubles at each of the 998
steps. The point is rational but cannot be written out.

The linearization at the fixed point −1/√2 has characteristic polynomial λ² − ((3 + 2√2)/2)λ + ½, with
roots 2.731 and 0.183. Seed errors therefore grow by about 2.73^999 ≈ 1e436:
- with 15-digit seeds, |x| exceeds 10 at index 40;
- seeds with 50–420 correct decimals give exactly feasible points with objectives 352.89–353.00;
- 440 decimals give 352.2380254064956;
- the stored point uses 640 decimals.

The author's seed-sensitivity log records these values, and the reviewer reproduced them.

**chain.** Linear independence over Q of square roots of distinct squarefree integers, together with the
positive weights, forces every s_i, and hence every t_i, to be rational in any rational point. With three
free indices of equal weight, the conditions reduce to the plane cubic family
(t_a + t_b + t_c)(1/t_a + 1/t_b + 1/t_c) = const. Hence 2–3 free indices give no rational parametrization.
Whether a rational point exists near the optimum is **not settled**. The report's "genus-1 curve" remark
is plausible but unproved and must not be stated as a result. The quadratic-field point is exact, so this
does not affect any claim.

## 4. The exactly feasible points of the 13 instances

| instance | definition of the point (stored data, under R/publication/primal/) | method | objective of the point |
|---|---|---|---|
| lnts50–400 | θ_1..θ_{N−1} exact 40-digit decimals; z* = the unique zero of F in the stored box; states from the recursion (`lnts/points/lnts<N>_point.json`). The middle control is a stored rational of about 1e-112, inherited from Newton noise. | C1 | enclosed with width < 3e-109 (valid two-step); stored as 25-digit outward decimals |
| dtoc5 | all 99,999 values as exact decimals (`dtoc5-lukvle10/points/dtoc5_point.txt.gz`) | A | exact rational (`logs/dtoc5_check_objective_exact.txt`) |
| lukvle10 | seeds x_0, x_1 = KKT values rounded to 640 decimals (`points/lukvle10_seed.txt`); the rest from the rows; box of radius ≤ 5e-61 (`points/lukvle10_box.txt.gz`) | B | enclosure width 6.1e-58 (box), 2.0e-264 (tight) |
| chain50–400 | generator: a = 1, b = N−1, 20-decimal t_i, root choice, R (`chain/points/chainN_generator.json`); box of radius 1e-40 (`chainN_box.json`) | A | exact element of Q(√R); 40-decimal enclosure |
| powerflow ×3 | fixed variables as rationals; square system S as (row, side) pairs; 60-digit centre; radius 1e-45 (`powerflow/points/<name>.json`) | C2 | enclosure at 22 decimals, width 2.3e-42 to 2.8e-42 |

**Relation to the earlier tolerance points.**
- lnts: the new points agree with the earlier vectors to 3.25e-15–3.54e-15 in every coordinate.
- dtoc5: the objective agrees with the double point to 17 digits.
- lukvle10: x* agrees with the numerical KKT vector to about 205 digits (5.8e-206). Its objective lies
  5.14e-13 *below* the objective evaluated at p5's stored coordinates (352.23802540649613695).
- chain: the points are within 2.3e-16 (x) and 4.0e-15 (u) of the wave-2 points.
- powerflow: the free variables moved by at most 1.4e-14, 2.5e-13 and 7.8e-12; the objectives rose by
  2.87e-12, 4.64e-12 and 1.83e-10 over obj(p1).

**Stored decimals are not points.** For lnts, lukvle10, powerflow, ANN and KAN, the point is defined
implicitly. The `*.approx40.sol` files and the box centres are approximations that are not exactly
feasible. The dtoc5 decimal file is the point itself. The chain and water points need field elements.

## 5. Numbers tables

### 5.1 The 13 instances

All displays come from R/open-instances-summary.md. Gaps are absolute and rounded upward; powerflow
relative gaps divide by the dual. I recomputed every cell exactly from the saved files
(`logs/gaps_check_v2.log`) and found **no disagreement** with the summary.

| instance | listed dual | our dual (safe display; certified source) | primal display; objective enclosure (source) | gap (upward) |
|---|---|---|---|---|
| lnts50 | 0.55464755 | 0.5546687649381 (verifier N·h₂ ≥ 0.5546687649381242; reviews/open-instances-verification) | 0.5546687649387; [0.5546687649386788986220922, …923] (lnts/points/lnts50_point.json) | ≤ 5.79e-13 (≤ 5.55e-13 vs N·h₂) |
| lnts100 | 0.55299042 | 0.5545954011663 (≥ 0.5545954011663565) | 0.5545954011670; [0.5545954011669111610017828, …829] | ≤ 6.12e-13 (≤ 5.55e-13) |
| lnts200 | 0.55219867 | 0.5545770161025 (≥ 0.5545770161025290) | 0.5545770161031; [0.5545770161030836720556252, …253] | ≤ 5.84e-13 (≤ 5.55e-13) |
| lnts400 | 0.55204395 | 0.5545724137001 (≥ 0.5545724137001325) | 0.5545724137007; [0.5545724137006871088173911, …912] | ≤ 5.88e-13 (≤ 5.55e-13) |
| dtoc5 | 0.00243096 | 5.38967211918114 (verifier lower end 5.38967211918114046742396472386…; reviews/open-instances-verification/logs/dtoc5_verify.json) | 5.389672119181141; exact rational in [5.3896721191811404674239664991362718688313, …8314] | ≤ 4.7e-16 (4.675e-16; 1.776e-24 vs verifier end) |
| lukvle10 | 351.223393 | 352.2380254050784 | 352.2380254064961; [352.2380254064956226308712710293664647979978, …979] (dtoc5-lukvle10/logs/lukvle10_enclose.json) | ≤ 1.5e-9 (1.418e-9; rel. 4.024e-12) |
| chain50 | 0.17451499 | 5.0722614939828627 (truncation of the certified double 5.07226149398286274561…; open-instances-wave2/cops/logs/chain50_bound.json) | [5.0722614939828723164454381769845467731843, …844] (chain/points/chain50_box.json) | 9.62e-15 (9.58e-15 vs double) |
| chain100 | 0.09367008 | 5.0697846107387505 | [5.0697846107387605574911913664186759056713, …714] | 1.01e-14 (1.003e-14 vs double) |
| chain200 | 0.08256615 | 5.0689173417931616 | [5.0689173417931710001847965010674364416891, …892] | 9.41e-15 (9.34e-15 vs double) |
| chain400 | 0.09563835 | 5.068621694604009 | [5.0686216946040190143614896914450892607014, …015] | 1.01e-14 (9.78e-15 vs double) |
| powerflow0030p | 572.8395847 | 576.8934122988004 | 576.8934134704; [576.8934134703742598676683, …684] (powerflow/logs/certify.powerflow0030p.log) | abs. 1.171573860e-6; ≤ 2.1e-9 rel. (2.031e-9) |
| powerflow0039p | 41818.27916 | 41869.05148485014 | 41869.0515113203; [41869.0515113202038027683844, …845] | abs. 2.6470063803e-5; ≤ 6.4e-10 rel. (6.323e-10) |
| powerflow0039r | 41804.88153 | 41869.05148327243 | 41869.0515113210; [41869.0515113209830932768581, …582] | abs. 2.8048553094e-5; ≤ 6.7e-10 rel. (6.699e-10) |

**Notes on the table.**
- The summary's chain row reads "5.06862 … 5.07226" and "≤ 1.01e-14". The paper should show the four
  safe individual duals above.
- Do not use 5.072261493982863 or 5.068917341793162: these shortest-repr strings lie 2.54e-16 and
  3.32e-16 *above* the certified doubles.
- Old primal displays that were not upper bounds and are now corrected in the summary:
  - lnts100: 0.5545954011669;
  - dtoc5: 5.38967211918114;
  - powerflow0039p and 0039r: 41869.0515113202 and 41869.0515113208.

### 5.2 Water, ANN and KAN (my recomputation agrees with the summary)

| instance | primal display | objective of the exact point | dual used (exact) | gap (upward) |
|---|---|---|---|---|
| waterno2_06 | 282.888038 | 282888037386904807969455615812871/10^30 | 39157472136693483/140737488355328 | ≤ 1.68% (1.67396%) |
| waterno2_09 | 914.012 | 914.011975237085991… | cert_09 `certified_bound_exact` | ≤ 10.82% (10.81153%) |
| waterno2_12 | 2233.821346 | 2233.821345608215233… | cert_12 | ≤ 6.90% (6.89396%) |
| waterno2_18 | 5023.983 | 5023.982760460661871… | cert_18 | ≤ 4.87% (4.86685%) |
| waterno2_24 | 6963.795181 | 6963.795180156419512… | cert_24 | ≤ 5.90% (5.89469%) |
| ann_cumene_tanh | −3379.9823940 | [−3379.982394071771548095722619880929, …928] | −3386.5402291369187 (binary64) | ≤ 0.195% of \|primal\| (0.19402%); 0.194% of \|dual\|; absolute 6.55784 |
| KAN (points of R) | — | stored outward enclosures of width ≤ 1e-42 (point JSONs; the reviewer's own enclosures are about 1e-89 wide) | `dual_bound` of R | 6.89e-11, 1.08e-10, 8.96e-11 (r3 n4/n5/n9); 2.42e-8, 1.02e-10, 9.57e-11 (r5 n3/n5/n8). Summary displays: ≤ 6.9e-11, ≤ 1.08e-10, ≤ 9e-11, ≤ 2.42e-8, ≤ 1.02e-10, ≤ 9.6e-11 |

### 5.3 Other closed families (primal side)

| instance | primal value used | how proved |
|---|---|---|
| camshape100–800 | exact optimum, attained (gap 0) | exact rational envelope |
| optcdeg2 | ≤ 293.87607509587509328 | IVT bracket (C3) |
| hvycrash | −0.2185 exactly | objective constant on the feasible set, plus an explicit feasible witness |
| ex6_2_7 | −0.16084761546360086 (point objective in [−0.1608476154636008615244708, …707], `logs/ex62_check.log`) | exact rational point (verifier); display 1.52e-18 above the enclosure |
| ex6_2_5 | −70.752077833447705 (point objective in [−70.7520778334477055803671221, …220]) | as above; display 5.80e-16 above the enclosure |
| etamac | [−15.29467564336808959198, same + 4e-45] | forward definitions (verifier) |
| pricing050 (max) | −1813.8290784519731 (display; point −1813.8290784519730578) | interior point (verifier) |
| pindyck | ≤ −1170.486285436088562 | interval Newton per s_t (verifier) |
| catmix100/200/400 | −0.0480694320309595635… / −0.0480591455801143916… / −0.048056547756611554855… | exact simulation of the author controls |
| catmix800 | −0.0480559013312308003… | verifier's DP-policy point, exact |
| eg_int_s / eg_disc_s / eg_disc2_s | objvar 6.4531031593842274088 / 5.7605396164535106058 / 5.6421005799711067563; displays …275 / …107 / …068 | interior points; interval-proved in this pass |

## 6. Verification record

| track | author checks | independent review | verdict and residual points |
|---|---|---|---|
| primal-lnts | lnts_primal.py; crosscheck.py (verifier reader, closed-form Jacobian); jacobian_check.py (numerical); mutation_test.py (3 mutations rejected) | R/publication/reviews/primal-lnts-review-r1.md: own generic elimination; Krawczyk in mpmath iv at 120 digits **and** in mpmath-free integer arithmetic; byte-identical rerun of the author construction; 4 mutations rejected | **verified**, 5 minor issues. The invalid second Krawczyk step (centre outside Z) was corrected; the one-step enclosure already gives all displayed digits. |
| primal-dtoc5-lukvle10 | check_exact_point.py and dtoc5_crosscheck.py (two readers); lukvle10_enclose.py (mpmath iv); lukvle10_crosscheck.py (integer fixed point) | primal-dtoc5-lukvle10-review-r1.md: own reader; dtoc5 exactly; lukvle10 by integer fixed point, plus mpmath-iv and integer-only objective routes | **verified**, 4 minor issues. The unconditional "KKT ⇒ remaining gap is on the dual side" overclaim was removed. |
| primal-chain | build_points.py; separate verify_points.py (own Q(√R)); SCIP checkSol at 1e-13 | primal-chain-review-r1.md: own reader and Q(√D) arithmetic; 7 negative controls | **verified**, 4 minor issues: display locations, which L the gaps use, u-distance rounding, wording |
| primal-powerflow | construct.py (numerical); certify.py (mpmath iv); scip_check.py; 4 negative tests | primal-powerflow-review-r1.md: own reader, own dyadic intervals, own preconditioner; 5 negative controls; OSIL byte-identical to the live site | **verified**, 6 minor issues, including the uniqueness citation (now Theorem C) and the osilx.py dependency (hash recorded) |
| primal-water-ann-kan | water_exact.py; check_water_point.py (second exact checker); nn_exact.py; 60-digit cross-checks | primal-water-ann-kan-review-r1.md: own reader, multi-quadratic field, rational intervals; 7 negative controls; parser validated on listed points | **verified**, 5 minor issues: rounding statements, old-point bound violations, the x650 zero margin |
| minor-fixes | — | minor-fixes-review-r1.md: **issues**, including major display problems (lnts100 and dtoc5 primal displays below the point objective; a water rounding statement); r2: **issues**, one major outside this family | All primal-display corrections are applied in the summary; I re-verified their directions. |
| integration | gap-values.json; objectives.log (dtoc5 and five water objectives recomputed) | integration-review r1/r2: **issues**, 0 blockers; all gap cells confirmed | Primal-related fixes applied. No later independent round. |
| this dossier (two passes) | — | my checks (Section 8.2) | consistent with all of the above. The first-pass eg interval script was defective and is now fixed; the eg points are now interval-proved twice. |

**Remaining assumptions** for this family:
- T1–T4 (Section 3.6);
- the decimal reading of the data (Section 1.1; PP-1);
- for hvycrash, etamac, pricing050, pindyck and optcdeg2: correctness of mpmath iv.

Dual-side assumptions (A1/A2 for eg_*, mpmath iv where used) belong to the dual dossiers.

## 7. Relation to prior work

- **Rigorous upper bounds need verified feasible points.**
  - Neumaier's survey (`neumaier2004-complete-search-in-continuous-global`, "Certification of upper
    bounds") states that an objective value is a valid upper bound only at a feasible point. Near
    equality constraints, this requires an interval-Newton existence proof in a small box around an
    approximate point, with the existence tests modified when there are fewer equalities than variables.
  - The same survey credits Kahan (1968) with interval existence proofs and Krawczyk (1969) with the
    operator.
  - Methods C1 and C2 are instances of this classical approach.
- **Feasibility verification with active sets.**
  - Füllner, Kirst, Otto and Rebennack (2024, `fullner2024-feasibility-verification-and-upper-bound`)
    treat possibly active inequalities as equalities ("approximate active index sets").
  - They compare against Krawczyk on square systems ("KRAW") and against a narrow-box variant ("NARR",
    local solve plus Krawczyk) that follows Kearfott (1998) and Domes–Neumaier (2015). They also compare
    against a Miranda-based test (`fullner2021-convergent-upper-bounds-in-global`).
  - Our powerflow construction (cutoff 1e-9, QR-chosen fixed variables, Krawczyk on S) is NARR-type
    verification applied once at a known near-optimal point.
  - Kearfott (1998, 2014) and Domes–Neumaier (2015) are cited via Füllner et al.; they are not in the
    local knowledge base and were not read.
- **Exact feasibility in MIP.**
  - Exact rational MIP solvers check feasibility and optimality in rational arithmetic
    (`cook2011-an-exact-rational-mixed-integer`, `eifler2023-a-computational-status-update-for`,
    `borst2024-certified-constraint-propagation-and-dual`).
  - Hoen and Gleixner (`hoen2025-analyzing-the-numerical-correctness-of`) post-process floating-point MIP
    solutions: they round the integers and compute rational continuous values that satisfy all
    constraints exactly. They find that floating-point solvers sometimes accept slightly infeasible
    solutions.
  - For MINLP, rational points generally do not exist (Proposition L), so methods B and C are needed in
    addition to exact arithmetic.
- **Prior primal values for these instances** (literature reports).
  - lnts and chain: COPS gives local values only.
  - dtoc5: MINOTAUR's floating-point closure on QPLIB_8585 matches our value; its variable bounds are
    assumed defaults.
  - lukvle10: the CUTEst SIF value `*LO SOLTN 3.52237E+02` lies 1.0e-3 below our certified dual
    352.2380254050784 as displayed. Any value that 6-digit display can stand for is at least 5e-4 below
    the dual, so it is not the value of an exactly feasible point. Its origin (consistent with a
    1e-6-feasible local point) is inferred.
  - powerflow: there is a floating-point closure of 0030p via its rectangular twin, and the Ghaddar et al.
    (2016) moment relaxation solves a *different* (tapped) case39.
  - None of these sources gives an exactly verified feasible point. The literature reports did not search
    specifically for verified-feasibility results on these instances, so novelty must be stated "as far
    as found".

## 8. Critical examination

### 8.1 Re-derivations

- **Chain reduction (Proposition A.1).** Re-derived; correct. The swapped root order gives a second
  exactly feasible point, so the root choice is part of the point's definition.
- **lnts block elimination.** Correct.
  - Every row has coefficient 1 on its "next" state, px_N is free, and F collects exactly the three
    remaining fixed values.
  - The rational-point impossibility argument is correct, and I strengthened it to Proposition L.
- **Theorem C.** I rewrote the proof for an arbitrary y ∈ X (not only the centre) and for computed boxes
  that contain the exact decimal box.
  - Nonsingularity now follows from a weighted ∞-norm bound obtained from the widths. No Perron–Frobenius
    argument is needed.
  - The lnts and powerflow computations satisfy its hypotheses.
  - The lnts second Krawczyk step needed y ∈ the step-1 box; the corrected code ensures this, and the
    one-step enclosure already gives the 25-digit displays.
- **lukvle10.**
  - Each row is affine in x_{j+2} with constant coefficient −2, so Proposition B applies with no division
    risk.
  - The `power` bases are x_k² with min|x_k| = 0.26003, so all bases are at least 0.0676 > 0 and the
    exp/log reading is unambiguous.
  - The saddle eigenvalues 2.731 and 0.183 follow from the linearization at −1/√2.
- **Forward definitions (ANN, KAN, hvycrash, etamac).** The argument is Proposition B.
  - The safeguard against a wrong symbolic solve is the reviewer's independent re-derivation of every
    defining row from the OSIL. These rows equal the author's `defined_by` entries.
  - Re-evaluating the defining rows over the enclosures (which contain 0) is consistent with this but is
    not by itself a proof.
- **Gaps and display directions.** Lemma 0, recomputed exactly (Section 5).
- **Data reading of the dual side** (both sides of a gap must refer to the same model). For chain and
  dtoc5, where the gaps are 1e-14 and 5e-16:
  - `open-instances-wave2/cops/chain_bound.py` converts η with `iv.mpf(<decimal string>)` and asserts
    Fraction(η) = 1/(2N);
  - the dtoc5 verifier uses h = `iv.mpf(1)/50000`.

  Both duals are therefore valid for reading (b). I did not check the other dual codes; the family
  dossiers should confirm them.

### 8.2 Cheap checks run in this pass

All checks ran on copies under /tmp. Scripts and logs are in
`paper-open-minlplib/development/dossiers/primal-points-checks/`.

| check | command | result |
|---|---|---|
| eg_* feasibility, library-free | `python3 eg_dyadic_check.py eg_int_s eg_disc_s eg_disc2_s` | Own OSiL reader. Intervals are integers × 2^-256 with floor/ceil rounding. exp is bounded by the alternating Taylor series of exp(−y), y ≤ 2^-8, then outward squaring, in fixed point at 2^-352; tested on 304 arguments against a 120-digit reference. **All 28 rows of each instance hold** with enclosure widths ≤ 1e-73; bounds and integrality are exact. objvar − (upper bound on the least feasible objvar) ≥ 5.5744e-20, 7.8003e-20, 7.4919e-20. Smallest side-row margins: 1.49e-11 (eg_int_s e26), 0.140 (eg_disc_s e25), 0.123 (eg_disc2_s e25). Run time 19 s + 37 s. |
| eg negative controls | modified copies of the eg_int_s .sol (`logs/eg_dyadic_negative_controls.log`) | Rejected: objvar − 1e-19 (e12 fails by 4.43e-20); x3 = 1 + 1e-30 (ub); i5 = 1.5 (integrality); x1 + 1e-9 (e26). The unchanged point passes. |
| eg_* feasibility, second implementation | corrected `eg_iv_check.py` (Python `decimal` at 60 digits, directed rounding; exp correctly rounded by libmpdec, widened by one ulp) | Same margins; enclosure widths 2.5e-57 to 1.1e-56. The first-pass version used unary minus on `Decimal`, which rounds to nearest at 28 digits. Its enclosures had collapsed to 28-digit points (width 0E-27), so it was **not** an outward-rounded proof. The rounding error (≤ 5e-28) was far below the margins, so the conclusion was right but unproved. Fixed with `copy_negate()`. |
| ex6_2_* primal, mpmath-free | `python3 ex62_check.py ex6_2_7 …`, `… ex6_2_5 …` (Fraction intervals; ln via atanh series with remainder, ln2 = 2 atanh(1/3); outward rounding to 2^-400) | The 3 rows hold exactly and the bounds hold exactly. f ∈ [−0.1608476154636008615244708, −0.1608476154636008615244707] and [−70.7520778334477055803671221, …220]. The summary displays are above the upper ends by 1.52e-18 and 5.80e-16. |
| gaps and displays | `python3 gaps_check_v2.py` | Every primal display of the 13 and the water/ANN/KAN rows is at least the enclosure upper end (min problems). Every dual display is at most the certified value. Every gap cell equals the summary after upward rounding. The water duals are the exact rationals from certB_verify.json and cert_TT_w1_impl.json. |
| dtoc5, third exact check (re-run) | `python3 dtoc5_check.py` | 99,999 variables, 2 finite bounds, 49,999 rows, 0 violated; the objective equals the stored rational. 2.8 s. |
| chain50/100, third exact check (re-run) | `python3 chain_check.py 50 100` | All 51/101 rows exact; bounds exact; the objective is inside the stored 40-decimal enclosure. The printed "width 0.0e+00" is float underflow of a width below 1e-300. 1.5 s. |
| listed lnts points | `python3 lnts_p1_check.py` | lnts50 p1: N·h = 0.55466876489565, **4.25e-11 below the certified dual**, so it is not exactly feasible. lnts100/200/400 p1 lie 2.0e-12 / 3.3e-12 / 1.5e-11 above it. |
| listed displays | `python3 listed_display_check.py` | 7 of the 13 bold listed primal displays lie below our safe duals by 7e-10 to 5e-9, only through display rounding (Section 2). |
| OSiL schema | curl of OSiL.xsd, OSgL.xsd, OSnL.xsd (2.0) from optimizationservices.org; grep (`logs/osil_schema_types.log`, hashes recorded) | var `lb`/`ub`, con `lb`/`ub`/`constant`, obj `constant`, `coef`, the linear `value` vector elements (`DoubleVectorEl`) and `number/@value` are all `xs:double`. |
| `constant` attributes | grep over the 32 relevant OSIL files | Only objective constants occur: powerflow0039p/r `constant="2"` and catmix `constant="-1"`. Both readers of each family apply them. |
| data semantics (re-run) | `python3 binexact.py …`, `python3 dtoc5_bin64.py` | Non-binary64-exact constants: lnts only ±1.5707963267949; lukvle10 none; dtoc5 {2e-5, 8e-5}; chain {η}; powerflow ≥ 172/245/264 distinct strings. Rebuilding dtoc5's u from the same y with binary64 coefficients raises the objective by 4.37e-17, about 9% of the 4.7e-16 gap. |
| catmix400 author point (first pass) | copy of the reviewer's `policy_exact.py` on `open-instances-wave2/cops/logs/catmix400_u.npy` | floor(J·10^30) = −48056547756611554855186829087, matching the 60-digit interval simulation. Removes the mpmath dependence of the catmix400 primal in the summary gap (≤ 6.81e-11). |

### 8.3 Issues and proposed resolutions

**PP-1 (major; hidden modelling convention, not invalidating). The data semantics are implicit, and the
OSiL schema says `xs:double`.**
- *The reading used.* Every proof, primal and dual, reads the decimal strings as exact rationals
  (reading (b)). The summary and READINESS never state this.
- *The schema's reading.* OSiL 2.0 types all numeric data as `xs:double`, whose value space is binary64.
  Solvers and GAMS also use binary64 data.
- *MINLPLib's own strings.* The OSIL strings are sometimes shortest-repr strings of binary64 products
  (catmix). So reading (b) differs from both the .gms intent (a) and binary64 (c).
- *Consequences under reading (c).*
  - The dtoc5, chain, powerflow, water, ANN, KAN, catmix and eg points are not exactly feasible.
    Equalities are off by about 1e-17 relative. For eg and pricing, the inequalities may still hold
    thanks to their margins, but that was not checked.
  - The 1e-16–1e-14 gaps are not established for (c). For dtoc5, the analogous binary64-data point costs
    4.37e-17 more.
  - The KAN statement "the OSIL models have no exactly feasible point" is also proved only for (b).
- *Reading-independent claims.* The lnts and lukvle10 primal points are feasible under (b) and (c): all
  their data are binary64-exact, and the lnts angle bounds were checked against both readings with margin
  (|θ| ≤ 0.9523 < 1.5707).
- *Resolution.* State Section 1.1 as the model definition in the paper, with a footnote on `xs:double`
  and on the catmix strings. Say that results for binary64 data are not claimed, except that the lnts and
  lukvle10 primal points are reading-independent.
- *Optional computation.*
  - Primal points for binary64 data: seconds each for dtoc5 and chain (same constructions with dyadic
    coefficients); about an hour of scripting for powerflow (rerun certify with binary64 data).
  - Dual certificates under (c): owned by the dual dossiers; not estimated here.

**PP-2 (minor; resolved here). The eg_* "exactly feasible" primal points lacked an independent
outward-rounded proof, and the first-pass dossier check was defective.**
- *Before this pass.* The author's `verify_primal.py` and the reviewer's `check_primal.py` evaluated at
  50/60 digits without intervals. The certifier's interval path carries A1/A2. The first-pass
  `eg_iv_check.py` collapsed enclosures through 28-digit `Decimal` negation.
- *Now.* `eg_dyadic_check.py` (library-free) and the corrected `eg_iv_check.py` both prove all three
  points, with margins of at least 5.57e-20. Seven negative controls behave as expected.
- *Resolution.* Cite `eg_dyadic_check.py` in the reproduction package. Cost: 1 minute.

**PP-3 (minor). The trust base is stated more weakly than the evidence supports in some places; a few
claims stay single-implementation.**
- *Understated.* READINESS and the summary say that ANN feasibility (and the KAN, powerflow and lnts
  enclosures) "assume mpmath iv". The reviews re-proved all of them without mpmath (Section 3.6).
- *Single-implementation (mpmath iv, verifier only).* hvycrash, etamac, pricing050, pindyck, optcdeg2.
- *Not replayable.* The verifier's pricing050 point coordinates are not saved: `logs/pricing050.json`
  holds only the objective. Replay requires regeneration (`v_pricing050.py`, 27.7 s).
- *Resolution.* In the paper, state the trust base per instance as in Section 3.6.
- *Optional work.*
  - Save the pricing050 point vector. Cost: rerun v_pricing050.py in a copy, under 1 minute.
  - Re-prove the five single-implementation primal claims with the dyadic arithmetic used here. Cost:
    about 1–2 hours of scripting each for hvycrash, etamac and pindyck; under an hour for optcdeg2 (one
    50,000-step forward simulation over a 1-D bracket) and for pricing050. Run times are seconds to
    minutes.

**PP-4 (minor). Outdated statements in synthesis documents** (owners must update; the paper must take
numbers and status only from the summary).
- R/SYNTHESIS.md (lines 485–489) and R/closing-research-results.md (lines 210–213 and 383–384) still say
  the 13 closures are measured against tolerance-feasible points and that "no exactly feasible point was
  constructed".
- R/SYNTHESIS.md line 435 says the KAN relaxations are certified "to about 1e-10". The summary's largest
  KAN gap is 2.42e-8 (kan_r5_h1_n3).
- R/SYNTHESIS.md uses the nearest-rounded 1.67% and 0.194%.
- R/publication/reproduction/README.md has three stale items:
  - line 146 says the primal studies "do not replace the summary's original primal values";
  - lines 340–341 show the powerflow primals 41869.0515113202 and 41869.0515113208, both below the
    exact-point objectives;
  - line 361 gives the ANN primal as −3379.9824, a nearest rounding that lies below −3379.98239407…,
    so it is not an upper bound.

**PP-5 (minor; new). The tolerance-artifact list needs one addition and one caution.**
- *Add lnts50 p1.* Its exact objective N·h = 0.55466876489565 is 4.25e-11 below the certified dual. The
  verifier's row violation is 9.1e-10; MINLPLib lists 9e-10.
- *Caution.* Seven listed *displays* of the 13 (lnts50/100/400, lukvle10, chain50/100/200) lie below our
  duals only through 7–10-digit display rounding. Do not call them artifacts. Base every artifact claim
  on an evaluated objective, as in the table of Section 9.

**PP-6 (minor). Inconsistent violation figures for the earlier lnts vectors.** The open-instances report
gives 4.6e-15–6.9e-15. The verifier measured 5.3e-15–1.3e-14 for the same author vectors and 4.7e-15–6.7e-15
for its own point. *Resolution:* quote "≤ 1.3e-14" or the range by evaluator. The 2.4e-20–7.9e-12 range for
the 13 is unaffected.

**PP-7 (minor; resolved here). The existence and uniqueness proof was not self-contained.** Theorem C and
its proof supply it, including the case of a non-centred y and of outward-rounded boxes.

**PP-8 (minor). Implicitly defined points.**
- The paper must define each point by its certificate data: seeds and recursion, box and square system,
  or generator and field.
- It must say that no finite decimal vector for lnts, lukvle10, powerflow, ANN or KAN is claimed to be
  exactly feasible; in particular, the `.approx40.sol` files and box centres are not.
- Submitting these points to MINLPLib as .sol files would again give tolerance-feasible vectors.

**PP-9 (minor). Side remarks about rational points.** Drop the chain "genus-1" remark or label it
unproved, and use Proposition L for lnts.

**PP-10 (minor). The quantitative camshape explanation needs care.**
- The open-instances report quotes per-row Chebyshev weights of about 76 (n = 100) to 600 (n = 800).
- The multiplier-mass bound (Section 9) uses their *sum*. The observed ratios deficit/violation are about
  2.7e4 (camshape400 p2) and 1.1e5 (camshape800 p2). These are compatible only with a total mass of that
  order, not with the maximum weight.
- *Resolution:* state the lemma qualitatively ("deficits up to the multiplier mass times the
  tolerance"). Computing the camshape multiplier mass exactly is cheap (the certificate data exist) but
  was not done.

**PP-11 (minor; optional, dual side).** The lnts gaps of about 5.6e-13 come from the verifier's dual
margin h₂ = h(1 − 1e-12); the primal enclosures are narrower than 3e-109. The dual dossier owns any rerun.

**Nothing found invalidates a claimed result.**
- Every primal claim of the 13, water, ANN, KAN, eg_* and ex6_2_* is reproduced by at least two
  independent implementations, one of them free of mpmath. dtoc5, chain50 and chain100 have three.
- The defect found (PP-2) was in a check, not in a result, and the corrected checks confirm the result.

## 9. What the paper may claim and must not claim

**May claim** (suggested wording):
- "For each of the 31 closed instances, the reported primal value is the objective value of a point that
  we prove satisfies every constraint, variable bound and integrality requirement of the MINLPLib OSIL
  model exactly, or an upward rounding of a rigorous enclosure of that value. Here the file's decimal
  data are read as exact rationals."
- "For 13 of these instances (lnts50–400, dtoc5, lukvle10, chain50–400, powerflow0030p/0039p/0039r),
  earlier closures were measured against points that violate rows by 2.4e-20 to 7.9e-12. The exactly
  feasible points are new in this work. To the best of our knowledge, based on our literature search,
  no exactly verified feasible points had been published for these models."
- "Every interval-based existence proof for these 13 instances, the five waterno2 instances,
  ann_cumene_tanh, the KAN relaxations and the eg_* instances was reproduced by an independent
  implementation that uses only integer and rational arithmetic with explicit remainder bounds."
- "No exactly feasible point of lnts<N> has all of θ_0, …, θ_N, h algebraic" (Proposition L).
- "Several listed or published primal values are tolerance artifacts: they lie below a certified lower
  bound and are attained only within a feasibility tolerance," with the list below.
- For lukvle10: "x* agrees with a numerically computed KKT point to about 205 digits; if that KKT point
  is a global minimizer, the remaining gap of at most 1.5e-9 lies on the dual side."

**Must not claim:**
- that any finite decimal vector (box centres, `.approx40.sol`, MINLPLib .sol) for lnts, lukvle10,
  powerflow, ANN or KAN is exactly feasible;
- exact feasibility for binary64 data, the .gms/.nl renderings, QPLIB copies or the source models
  (CUTEst, COPS, MATPOWER), except the reading-independence of the lnts and lukvle10 points;
- that the exact points are optimal; only camshape and hvycrash have attained, proved optima;
- that the KAN points are feasible for the OSIL models; they are points of R only;
- that mpmath iv is part of the trust base for the 13, water, ANN, KAN, eg_* or ex6_2_* primal claims.
  Conversely, the paper must not claim mpmath-free proofs for hvycrash, etamac, pricing050, pindyck or
  optcdeg2;
- the existence or nonexistence of a rational chain point;
- that a MINLPLib page display below our dual is itself evidence of infeasibility;
- an unqualified priority claim.

**Tolerance artifacts and related effects (evidence-backed list for the paper):**

| value | source | relation to the certificate | violation | evidence |
|---|---|---|---|---|
| lnts50 p1 (0.55466876489565) | MINLPLib point | 4.25e-11 below the certified dual | 9.1e-10 (verifier; listed 9e-10) | `logs/lnts_p1_check.log` (exact N·h); open-instances verification |
| camshape400 / camshape800 p2 | MINLPLib points | 8.2e-6 / 3.3e-5 below the exact optimum | 3.0e-10 | open-instances report §5.5; verified |
| camshape200 / camshape400 p1 | MINLPLib points | 1.14e-12 / 9e-12 below the optimum | about 2e-14 | verifier's exact evaluation |
| BARON camshape100 / camshape200 (campaign) | "optimal" claims | 5.26e-7 / 2.05e-6 below | about 1.0e-10 | solver-runs point_checks.log (50-digit evaluation, not interval) |
| SCIP camshape100 (campaign) | incumbent | 1.5e-7 below | 7.7e-10 | same |
| hvycrash p1 / p2 | MINLPLib points | value −0.21413 is impossible for a feasible point (objective ≡ −0.2185) | 4.05e-8 / 6.3e-10 | wave-2 small report §3 |
| etamac p1 | MINLPLib point | 9.5e-11 below the dual | 1.33e-10 | same, §5 |
| pricing050 p1 (max) | MINLPLib point | 2.1e-9 above the upper bound | 7.3e-10 | same, §6 |
| eg_int_s old GAMS World point | archive | 2.3e-10 below the dual | 6.37e-9 at e12 (interval-proved) | small literature report §9 |
| lukvle10 SOLTN 3.52237E+02 | CUTEst SIF | 1.0e-3 below the dual as displayed; at least 5e-4 below for any value the 6-digit display can stand for | unknown (origin inferred) | control literature report |
| optcdeg2 Gurobi 292.417 "optimum" | MINLPLib listed dual = p2 | far below the certified bound | p2 up to 1e-6 | open-instances report |
| kan_r3_h1_n4/n5 SCIP zero-gap optima | published | below the certified minimum of R | about 1e-6 (output scale about 970) | network literature report |
| kan_r5_h1_n5 ConvexHull primal 0.2725188 | published (source paper's SCIP run) | below the certified minimum of R (0.27258325); the exact network at that input gives 0.2729243 | tolerance-level (not quantified) | network literature report, item 6 |
| emfl050_3_3 (solved), emfl100_5_5 (solved), emfl050_5_5, emfl100_3_3 | MINLPLib listed primal | ≥ 1.42e-5 / 6.87e-6 below the exact optimum; e.g. listed 18.91165289 vs ≥ 18.9136329529, and 18.13236088 vs ≥ 18.1326531194 | 4e-11 to 8e-10 and more | bound-audit §1 |

*The opposite direction (not artifacts, same lesson).*
- optcdeg2's author point (row violation 8.9e-16) is 6.0e-12 *above* the rigorous upper bound.
- MINLPLib's lukvle10 p5 coordinates evaluate 5.14e-13 above the exactly feasible x*.
- Tolerance-feasible values are therefore unreliable in both directions.

**Explanatory lemma (proved; suitable for a remark).** Let L = inf_{x∈X} f(x) + λᵀh(x) + μᵀg(x), with
μ ≥ 0, be a Lagrangian lower bound for min{f : h = 0, g ≤ 0, x ∈ X}. Then every x̃ ∈ X with |h_i(x̃)| ≤ τ
and g_j(x̃) ≤ τ satisfies f(x̃) ≥ L − τ(‖λ‖₁ + ‖μ‖₁).

*Proof.* f(x̃) ≥ L − λᵀh(x̃) − μᵀg(x̃) ≥ L − τ‖λ‖₁ − τ‖μ‖₁. ∎

So a tolerance-feasible point can undercut an aggregation (Lagrangian or comparison) certificate by at
most the multiplier mass times the tolerance, provided it stays in X. Chains with large total multiplier
mass amplify violations most: camshape, and hvycrash with the verified bound −0.2185(1 + 7.86τ) − 50τ.

## 10. Candidate figures and tables

1. **Table (main text): the 13 formerly tolerance-only closures.** Columns: instance, size, earlier primal
   violation, construction method (A / B / C1 / C2), point data, arithmetic and independent re-proof,
   objective enclosure width, gap (Section 5.1 numbers).
2. **Table (appendix): primal points across all 31 closed, 6 improved and 6 KAN-R instances.** Columns:
   - method;
   - whether a rational point exists: yes / provably no (lnts) / unknown (chain) / exists but cannot be
     written out (lukvle10);
   - trust base: T1–T4 only, or mpmath iv single implementation.
3. **Figure: decision diagram of the construction.**
   - inequality-only → D;
   - triangular after fixing seeds → B;
   - rows polynomial with quadratics solvable in one symbol → A (field);
   - otherwise, reduce by exact elimination and apply C1, or fix the active set and apply C2;
   - one missing scalar condition → C3.
4. **Figure: lukvle10 seed sensitivity.** Objective of the exactly feasible seed-defined point against the
   number of correct seed decimals: 15 → divergence at index 40; 50–420 → 352.89–353.00; 440 →
   352.2380254064956; ≥ 460 → the KKT value. Data: dtoc5-lukvle10/logs/lukvle10_seed_sensitivity.json and
   the reviewer's seed_sens log.
5. **Figure: tolerance deficits.** Log–log scatter of the deficit below the certified bound against the
   point's maximum violation, for the artifact table, with reference lines τ·M for a few multiplier
   masses M.
6. **Box: model definition and trust base.** The three readings (a)/(b)/(c), T1–T4, and what is not
   assumed.
