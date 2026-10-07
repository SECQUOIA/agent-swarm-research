# Dossier: camshape100/200/400/800 — exact optima by a discrete Sturm comparison

Family key: `camshape`. Written 2026-10-04 for the MPC paper. `R/` means
`research-20260929/`, `P/` means `R/publication/`. The checks run for this
dossier are in `checks/camshape/` (scripts, logs, README). They were run on
copies under `/tmp/camshape_dossier_o5/`, never in the main tree, on one core.
This dossier has not been independently reviewed.

**Bottom line.**

- For each n ∈ {100, 200, 400, 800}, the optimal value of the MINLPLib model
  camshape<n> (decimal constants read as exact rationals) is a rational number
  v_n, attained by an explicit rational point (the "envelope" E). The optimal
  solution is unique, and E is the componentwise greatest feasible radius vector.
- The proof is a discrete Sturm comparison in u = 1/r (positivity of a
  Chebyshev Green's function), a min-plus envelope for the slope rows, and a
  feasibility argument for E. The only computer-assisted part is a finite
  exact-rational check of a few inequalities (C1–C5 below). No floating point,
  no interval arithmetic and no branching are needed.
- Three independent implementations agree on all four values to all printed
  digits: the author's mpmath interval code (16 digits), the verifier's exact
  `Fraction` code (20 digits) and this dossier's exact `Fraction` code (30
  digits).
- Nothing found here invalidates a claimed result. The issues are wording
  ("proved analytically", "600-fold"), unsafe displays in older notes, a proof
  sketch that should be replaced by the lemma given below, and several
  statements in the literature report that can now be made exact
  (QPLIB-copy optima, the COPS model, the MINOTAUR refutation).

---

## 1. Instances and models

### 1.1 Source and meaning

- COPS 2.0 problem 4 (Dolan and Moré 2000/2001, after Anitescu and Serban
  1998): maximize the valve-opening area for one rotation of a convex cam,
  with bounds on the radius and on the curvature. The cam is circular with
  radius r_min = 1 over 6π/5 of its circumference. The design variables r_i
  are the radii at n equally spaced angles θ_i = iΔθ over an arc of 2π/5,
  Δθ = 2π/(5(n+1)). The arc is closed by r_0 = r_min = 1 and r_{n+1} = r_max = 2.
  Sources: `P/literature/control/sources/cops2_html/camshape.txt`;
  [[dolan2001-benchmarking-optimization-software-with-cops]];
  [[library2026-cops-and-gams-source-models]].
- The COPS convexity row "area(r_{i−1}, r_{i+1}) ≤ area(r_{i−1}, r_i) +
  area(r_i, r_{i+1})" (triangle areas with the origin) is
  2cos(Δθ) r_{i−1} r_{i+1} ≤ r_i (r_{i−1} + r_{i+1}). In polar coordinates it says
  that the point (r_i, θ_i) lies on or outside the chord through its two
  neighbors. With u = 1/r it is the linear row u_{i−1} + u_{i+1} ≥ 2cos(Δθ) u_i,
  the discrete form of u'' + u ≥ 0 (convexity of a curve in polar coordinates).
- MINLPLib camshape<n> is the GAMS model library model `camshape` (SEQ=232)
  translated to scalar form, n = 100, 200, 400, 800, objective negated to a
  minimization. GAMS encodes the COPS end rows as bounds and as two edge rows.
  GAMS bounds `rdiff(i)` only for i ≥ 2, so the COPS curvature row on the pair
  (r_1, r_2) is **omitted** (d_1 is free). MINLPLib camshape is therefore a
  one-row relaxation of the COPS discretization, with constants printed to 15
  significant digits (`P/literature/control/sources/gamslib/camshape.gms`).
- QPLIB_2738, 2480, 2703, 3177 (LCQ, donor Ruth Misener) are the same four
  models with constants rounded to 8–10 digits and a different variable order
  ([[furini2018-qplib-a-library-of-quadratic]],
  [[cache2026-qplib-pages-and-rounded-camshape]]).

### 1.2 The model (OSIL = MINLPLib .gms, exactly)

Variables r = (r_1, …, r_n) (OSIL x1…xn) and d = (d_1, …, d_{n−1})
(x_{n+1}…x_{2n−1}); all continuous. The OSIL/GAMS row names are given in
brackets, e.g. for n = 100: G_1 = e100, G_n = e101, H = e102, D_1 = e103.

    (P_n)  minimize   f(r,d) = −c₀ Σ_{j=1}^{n} r_j
           subject to
           G_1 [e<n>]:      −r_1 + c r_2 − r_1 r_2 ≤ 0
           G_j [e<j>]:      −r_{j−1} r_j + c r_{j−1} r_{j+1} − r_j r_{j+1} ≤ 0,   2 ≤ j ≤ n−1
           G_n [e<n+1>]:    c₂ r_{n−1} − 2 r_n − r_{n−1} r_n ≤ 0
           H   [e<n+2>]:    c r_n² − 4 r_n ≤ 0
           D_i [e<n+2+i>]:  r_i − r_{i+1} + d_i = 0,                        1 ≤ i ≤ n−1
           1 ≤ r_1 ≤ ū,   1 ≤ r_j ≤ 2 (2 ≤ j ≤ n−1),   ℓ ≤ r_n ≤ 2,
           d_1 free,   −α ≤ d_i ≤ α (2 ≤ i ≤ n−1).

G_1 is the convexity row at i = 1 with r_0 = 1; G_n is the row at i = n with
r_{n+1} = 2; H is the row at i = n+1 with r_{n+2} = r_n. The bound ū is the
COPS convexity row at i = 0 (r_{−1} = r_0 = 1), and ℓ is the COPS curvature
row at i = n.

Constants (exact decimals from the OSIL; the MINLPLib .gms text has the same
decimals, checked exactly by `check_gms.py`):

| n | c₀ (= π/n) | c (= 2cos Δθ) | c₂ (= 4cos Δθ) | ū (= 1/(2cos Δθ − 1)) | ℓ (= 2 − 1.5Δθ) | α (= 1.5Δθ) |
|---|---|---|---|---|---|---|
| 100 | 3.14159265358979e-2 | 1.99984519984971 | 3.99969039969942 | 1.00015482411709 | 1.98133707334501 | 1.86629266549889e-2 |
| 200 | 1.5707963267949e-2 | 1.99996091355262 | 3.99992182710524 | 1.00003908797519 | 1.99062211148182 | 9.37788851817849e-3 |
| 400 | 7.85398163397448e-3 | 1.99999017956722 | 3.99998035913443 | 1.00000982052922 | 1.99529936261308 | 4.7006373869174e-3 |
| 800 | 3.92699081698724e-3 | 1.99999753875636 | 3.99999507751272 | 1.0000024612497 | 1.99764674707596 | 2.3532529240373e-3 |

- c₂ = 2c exactly except n = 400, where c₂ − 2c = −1e-14 (rounding). The
  coefficient of r_n² in H equals c. The objective has no constant.
- Every decimal is within 5.1e-15 of the exact COPS constant
  (`cops_consts.py`, mpmath interval arithmetic). In each file ū is the
  convexity bound 1/(2cosΔθ − 1), which is tighter than the curvature bound
  1 + 1.5Δθ.

Sizes and type (MINLPLib): QCP, nonconvex, continuous.

| n | variables | constraints | quadratic rows | linear equalities |
|---|---|---|---|---|
| 100 | 199 | 200 | 101 | 99 |
| 200 | 399 | 400 | 201 | 199 |
| 400 | 799 | 800 | 401 | 399 |
| 800 | 1599 | 1600 | 801 | 799 |

### 1.3 The structure that matters

- **Chain.** Every row couples at most three consecutive radii. The primal
  graph is a path of bags {r_{j−1}, r_j, r_{j+1}}.
- **Hidden linearity.** All r ≥ 1 > 0. Dividing G_1 by r_1 r_2 and G_j by
  r_{j−1} r_j r_{j+1} gives, for u_j = 1/r_j and the constant u_0 = 1,

      e_j(u) := u_{j−1} − c u_j + u_{j+1} ≥ 0,   1 ≤ j ≤ n−1.

  These rows are linear in u. They are a second-order difference inequality
  with 0 < c < 2: discrete polar convexity. The objective −c₀ Σ 1/u_j is
  increasing in each u_j, so the problem asks for the smallest u.
- **Slope rows** |r_{j+1} − r_j| ≤ α for 2 ≤ j ≤ n−1 (from D_j and the d_j
  bounds) are linear in r. The pair (1, 2) is unconstrained.
- **Why solvers struggle (our reading, not tested).** Termwise relaxations of
  the bilinear rows with c ≈ 2 (reverse-convex rows) are weak, and the weakness
  accumulates along the chain; listed best gaps grow from 1.2e-6 (n = 100) to
  19.9% (n = 800).
- **A negative result.** The project's generic separator-cell dynamic program
  did not reach useful accuracy on camshape100: dual −4.451 with 5.9e7 cells
  per stage (461 s), still 0.167 below the optimum. The convexity rows act at
  the per-stage scale (2 − c)u ≈ 1.5e-4, which cells must resolve
  (`R/open-instances/open-instances-report.md` §8.1; numerical, not
  independently checked).
- **Ill-conditioning.** The Green's function weights reach 76.1, 151.8, 303.2
  and 605.9 (n = 100…800), and their sums 4.35e3 … 2.80e5. Row violations of
  size ε can lower the objective by up to about 0.6 n² ε (Section 8, I-3).

### 1.4 Model-provenance issues

- MINLPLib omits the COPS curvature row |r_2 − r_1| ≤ αΔθ. It is slack at the
  optimum: |E_2 − E_1| = 3.10e-4, 7.82e-5, 1.96e-5, 4.92e-6 against
  α = 1.87e-2, 9.38e-3, 4.70e-3, 2.35e-3. This is now an **exact** check
  (`check_exact.py`), not the floating-point check of the literature report.
- OSIL vs GAMS: identical constants and rows for all four sizes (exact check,
  `check_gms.py`). There is no OSIL/GAMS coefficient issue for this family
  (unlike catmix).
- QPLIB copies differ by rounding at about 1e-10 relative. The rounding moves
  the exact optimum by 8.5e-7 to 8.7e-5 (Section 8, I-5).
- MINLPLib model history: the OSIL and GAMS files are unchanged since at least
  2014 (statistics snapshots) and identical to GLOBALLib text
  (`P/minlplib-status/data/tables.md`, Table B).

---

## 2. Listed status (MINLPLib pages fetched 2026-09-29; unchanged on 2026-10-02)

No instance has a solved mark. Source: `R/bound-audit/pages.json`,
`P/minlplib-status/report.md`.

| instance | best listed dual (solver, date) | other listed duals | metadata dual (≥ 3 solvers) | listed primal (point, page infeasibility, date) | starting gap vs best listed dual |
|---|---|---|---|---|---|
| camshape100 | −4.28415233 (ANTIGONE, 15 Feb 2022) | GUROBI −4.39132248, LINDO −4.47499355, SCIP −4.51386847, BARON −4.58132553, COUENNE −4.79690014, SHOT −6.25177425 | −4.474993552 | −4.28414712 (p1, 9e-16, 15 Aug 2014) | 1.216e-6 relative (5.2e-6 absolute) |
| camshape200 | −4.63229055 (ANTIGONE, 13 Sep 2017) | GUROBI −4.79046586, SCIP −4.83186659, LINDO −4.86514453, BARON −4.97559754, COUENNE −5.06045236, SHOT −6.26747796 | −4.831866586 | −4.27850023 (p1, 1e-15, 15 Aug 2014) | 8.27% |
| camshape400 | −4.97265746 (ANTIGONE, 13 Sep 2017) | GUROBI −4.99975168, LINDO −5.01318561, SCIP −5.04679597, BARON −5.17608573, COUENNE −5.18463969 | −5.013185607 | −4.27569663 (p2, 3e-10, 22 May 2018); p1 −4.27568848 (2e-15) | 16.30% |
| camshape800 | −5.12584096 (GUROBI, 31 Jul 2025) | LINDO −5.14217333, ANTIGONE −5.14437494, SCIP −5.19335593, COUENNE −5.27240816, BARON −5.27650359 | −5.144374942 | −4.27430687 (p2, 3e-10, 22 May 2018); p1 −4.27427414 (4e-10) | 19.92% |

Relative gaps are (listed primal − best dual)/|listed primal|. Against the
exact optimum they are 1.2157e-6, 8.27%, 16.30%, 19.92%. Under the scout's
1e-4 rule camshape100 was not "open"; it is open only in the sense of having
no solved mark (see the pattern-theory dossier, item 3).

The listed primal values of camshape400/800 (points p2) lie **below** the exact
optima, by 8.15e-6 and 3.27e-5. Our dual bound is therefore above MINLPLib's
listed primal for these two instances. This is a feasibility-tolerance effect,
not a contradiction (Section 4.3).

---

## 3. The certificate

### 3.1 Idea in plain words

After the substitution u = 1/r, the convexity rows say that u is "discretely
convex in polar coordinates": u_{j−1} − c u_j + u_{j+1} ≥ 0. Among all such
sequences that start at u_0 = 1 with u_1 ≥ 1/ū, the smallest one is the
solution S of the equality recurrence. In the cam picture, S is a straight
line: no convex arc that starts on the base circle can leave the extension of
the base circle's last chord. The comparison u ≥ S holds because the Green's
function of the recurrence (Chebyshev values U_m(c/2)) is nonnegative on the
whole index range. This is the discrete Sturm comparison; its validity
condition is disconjugacy of the recurrence.

So r_j ≤ R_j := 1/S_j. Adding the bounds r ≤ 2 and the slope rows gives a
componentwise bound r ≤ E, where E is the min-plus envelope of min(R, 2) with
slope α. Because the objective is increasing in every r_j, −c₀ Σ E_j is a dual
bound. The envelope is itself feasible: it follows the straight line until
the line becomes steeper than the curvature limit, then rises with the maximal
slope α, then stays at r = 2. So the bound is attained, and it is the exact
optimum.

### 3.2 Definitions

Fix n and the constants of Section 1.2. Define, all in exact rationals:

- U_0 = 1, U_1 = c, U_{m+1} = c U_m − U_{m−1} (so U_m = U_m(c/2), Chebyshev
  polynomials of the second kind);
- S_0 = 1, S_1 = 1/ū, S_{j+1} = c S_j − S_{j−1} (1 ≤ j ≤ n−1);
- R_j = 1/S_j if S_j > 0, R_j = +∞ otherwise; b_1 = ū, b_j = 2 (j ≥ 2);
  B_j = min(R_j, b_j);
- E_1 = B_1, and E_j = min_{2 ≤ k ≤ n} (B_k + α|j − k|) for 2 ≤ j ≤ n
  (equivalently: a forward pass F_j = min(B_j, F_{j−1} + α) and a backward pass
  E_j = min(F_j, E_{j+1} + α) over j ≥ 2);
- d^E_i = E_{i+1} − E_i (1 ≤ i ≤ n−1), and v_n = −c₀ Σ_{j=1}^n E_j.

Since R_1 = 1/S_1 = ū = b_1, E_1 = ū.

**Finite checks** (exact rational arithmetic; all pass for n = 100, 200, 400, 800):

- (C1) U_m ≥ 0 for 0 ≤ m ≤ n−1. (min U_m = 1, max 76.1/151.8/303.2/605.9.)
  Analytic alternative: c < 2 and c/2 > cos(π/n) imply arccos(c/2) < π/n, so
  U_m = sin((m+1)φ)/sin φ > 0 with φ = arccos(c/2). The inequality
  c/2 > 1 − x²/2 + x⁴/24 ≥ cos(π/n), x = (333/106)/n < π/n, is a rational check
  (`check_exact.py`, `analytic_cheb_test`).
- (C2) 0 < S_j ≤ 1 for 1 ≤ j ≤ n. (S is strictly decreasing; min S_j = 0.31493,
  0.31199, 0.31051, 0.30976.)
- (C3) E_{n−1} = E_n = 2.
- (C4) ū ≤ 1 + α.
- (C5) c₀ > 0, 1 ≤ ū ≤ 2, 0 < c < 2, c₂ ≤ 4, 0 < ℓ ≤ 2.

### 3.3 Statement

**Theorem 1 (camshape optima).** Let n ∈ {100, 200, 400, 800} and read the
decimal constants of MINLPLib camshape<n> as exact rationals.

(a) Every feasible (r, d) of (P_n) satisfies r_j ≤ E_j for all j. Hence
f(r, d) ≥ v_n.

(b) (E, d^E) is feasible for (P_n).

(c) v_n is the optimal value. The optimal solution is unique and equals
(E, d^E). E is the greatest element (componentwise) of the set of feasible
radius vectors, so (E, d^E) also maximizes every componentwise nondecreasing
function of r over the feasible set.

(d) The values are

| n | v_n (first 25 decimals of the exact rational) | safe lower display (floor, 14 decimals) | safe upper display (ceil, 14 decimals) |
|---|---|---|---|
| 100 | −4.2841471217467438034410071… | −4.28414712174675 | −4.28414712174674 |
| 200 | −4.2785002329927222918988259… | −4.27850023299273 | −4.27850023299272 |
| 400 | −4.2756884789255432151508246… | −4.27568847892555 | −4.27568847892554 |
| 800 | −4.2742741419541941011244678… | −4.27427414195420 | −4.27427414195419 |

Parts (a) and (b) hold for any constants that satisfy (C1)–(C5); the theorem
uses the stored constants only through these checks and the value in (d).

### 3.4 Proof

**Lemma 1 (Green's function; discrete Sturm comparison).** Let 1 ≤ N ≤ n,
u_0, …, u_N real numbers with u_0 = 1 and u_1 ≥ S_1, and put
e_j = u_{j−1} − c u_j + u_{j+1} for 1 ≤ j ≤ N−1. Then for 1 ≤ j ≤ N

    u_j − S_j = U_{j−1} (u_1 − S_1) + Σ_{k=1}^{j−1} U_{j−1−k} e_k.

If (C1) holds and e_k ≥ 0 for all k, then u_j ≥ S_j for 1 ≤ j ≤ N.

*Proof.* Let z_j = u_j − S_j. Then z_0 = 0 and z_{j+1} = c z_j − z_{j−1} + e_j,
because S satisfies the recurrence with zero right-hand side. The formula
holds for j = 1 (U_0 = 1, empty sum) and j = 2 (z_2 = c z_1 + e_1 =
U_1 z_1 + U_0 e_1). If it holds for j−1 and j, then

    z_{j+1} = (c U_{j−1} − U_{j−2}) z_1 + Σ_{k≤j−2} (c U_{j−1−k} − U_{j−2−k}) e_k + c U_0 e_{j−1} + e_j
            = U_j z_1 + Σ_{k≤j−2} U_{j−k} e_k + U_1 e_{j−1} + U_0 e_j,

which is the formula for j+1. All indices of U that occur are at most
N−1 ≤ n−1. With U ≥ 0, z_1 ≥ 0 and e ≥ 0 every term is nonnegative. ∎

LP reading: u_j ≥ S_j is the value of the LP "minimize u_j subject to
e_k(u) ≥ 0, u_1 ≥ S_1"; the weights U_{j−1−k} and U_{j−1} are its dual
multipliers, and (C1) is dual feasibility (disconjugacy of the recurrence on
[0, n], in the sense of Hartman 1978). See `R/theory-calibration/scouting.md`,
item 7.

**Lemma 2 (min-plus envelope).** If r_j ≤ B_j for all j and
|r_{j+1} − r_j| ≤ α for 2 ≤ j ≤ n−1, then r ≤ E.

*Proof.* r_1 ≤ B_1 = E_1. For j, k ≥ 2 all pairs between j and k are
slope-constrained, so r_j ≤ r_k + α|j − k| ≤ B_k + α|j − k|. Take the minimum
over k. ∎

**Proof of (a).** Let (r, d) be feasible. The lower bounds give r_j ≥ 1 for j < n and r_n ≥ ℓ > 0.
Put u_j = 1/r_j and u_0 = 1. Dividing G_1 by r_1 r_2 > 0 and G_j by
r_{j−1} r_j r_{j+1} > 0 gives e_j(u) ≥ 0 for 1 ≤ j ≤ n−1, and r_1 ≤ ū gives
u_1 ≥ S_1. Lemma 1 (with N = n) and (C1) give u_j ≥ S_j, so r_j ≤ R_j
whenever S_j > 0; with r_j ≤ b_j this is r_j ≤ B_j. For 2 ≤ j ≤ n−1, D_j and
|d_j| ≤ α give |r_{j+1} − r_j| ≤ α. Lemma 2 gives r ≤ E, and since c₀ > 0,
f = −c₀ Σ r_j ≥ −c₀ Σ E_j = v_n. ∎

The proof uses only G_1, …, G_{n−1}, the upper bounds, positivity, and the
slope rows for j ≥ 2. G_n, H, D_1, ℓ and the exact value of c₂ are not used.

**Lemma 3 (the envelope is feasible).** Under (C1)–(C5), (E, d^E) is feasible.

*Proof.* (i) *Bounds on r.* By (C2), R_k ≥ 1 where finite, and b_k ≥ 1, so
B_k ≥ 1 and E_j ≥ min_k B_k ≥ 1. Also E_j ≤ B_j ≤ b_j, E_1 = ū, and
E_n = 2 ≥ ℓ by (C3), (C5).

(ii) *D rows and slopes.* D_i holds by definition of d^E. On {2, …, n} each
function j ↦ B_k + α|j − k| is α-Lipschitz, so their minimum E is too; hence
|d^E_i| ≤ α for i ≥ 2. d_1 is free.

(iii) *H.* With E_n = 2: c·4 − 8 < 0 because c < 2.

(iv) *G_n.* With E_n = 2: G_n = (c₂ − 2) E_{n−1} − 4 ≤ max(c₂ − 2, 0)·2 − 4 ≤ 0
because c₂ ≤ 4 and E_{n−1} ≤ 2.

(v) *G_1, …, G_{n−1}.* Since E > 0 these rows are equivalent to e_j(w) ≥ 0
for w = 1/E, w_0 = 1. Note E ≤ R, hence w_k ≥ S_k for all k (trivially if
S_k ≤ 0; w_0 = S_0).

- Case A, E_j = R_j (contact). Then w_j = S_j and
  e_j(w) ≥ S_{j−1} − c S_j + S_{j+1} = 0.
- Case B, E_j < R_j. Then j ≥ 2 (E_1 = R_1). We show E_{j−1} + E_{j+1} ≤ 2E_j.
  - B1: E_j = B_j = 2 < R_j. All E_k ≤ 2 (E_1 = ū ≤ 2), so the sum is ≤ 4 = 2E_j.
  - B2: E_j < B_j. Then E_j = B_k + α|j − k| for some k ≥ 2, k ≠ j.
    If k < j, then 2 ≤ k ≤ j−1, so E_{j−1} ≤ B_k + α(j−1−k) = E_j − α, and
    E_{j+1} ≤ E_j + α by (ii). If k > j, then E_{j+1} ≤ B_k + α(k−j−1) = E_j − α,
    and E_{j−1} ≤ E_j + α: by (ii) if j ≥ 3, and for j = 2 because
    E_1 = ū ≤ 1 + α ≤ E_2 + α by (C4) and (i).

  By the AM–HM inequality, w_{j−1} + w_{j+1} ≥ 4/(E_{j−1} + E_{j+1}) ≥ 2/E_j =
  2w_j ≥ c w_j, so e_j(w) ≥ (2 − c) w_j ≥ 0. ∎

**Proof of (b)–(d).** (b) is Lemma 3. By (a) and (b), v_n is attained, so it
is the optimal value. If (r, d) is feasible with f(r, d) = v_n, then
Σ r_j = Σ E_j and r ≤ E, so r = E, and the D rows give d = d^E. E is feasible
and dominates every feasible r, so it is the greatest element. (d) is the
exact rational −c₀ Σ E_j, printed with outward rounding. ∎

### 3.5 What the computation checks, and what must be trusted

- **Computed:** (C1)–(C5) and the rational number v_n, from the decimal
  strings of the OSIL file, with Python `fractions.Fraction` (arbitrary
  precision integers). O(n) rational operations; the denominators are long
  (v_100 has a 28,165-digit denominator), so no rounding is involved at any
  step. Displays are produced by exact floor/ceil of v_n.
- **Also checked, though implied by Lemma 3:** every OSIL row and bound at
  (E, d^E), evaluated generically from the parsed sparse data (not from the
  template): zero violations; 63/127/255/512 convexity rows active.
- **Must be trusted:** Python integer arithmetic, and the OSIL parsers together
  with the structure assertions (that the file is the model of Section 1.2).
  Three parsers written independently (author `osil_eval.load`; verifier
  `osilx.py` keeping decimal strings; this dossier's `xml.etree` reader) give
  the same constants. No mpmath, no floating point and no interval arithmetic
  are needed for Theorem 1. (The author's original computation used mpmath
  interval arithmetic at 0.4n + 60 digits; the published values rest on the
  exact computations.)
- **Run time:** the verifier's batch takes 8.0 s for all four sizes
  (`P/reproduction/README.md`); this dossier's slower generic version took
  6 min 9 s, mostly for n = 800.

### 3.6 Structure of the optimum (exact, `check_exact.py`)

| n | contact phase E_j = R_j | maximal-slope phase | E_j = 2 | active convexity rows | slack of e_m (u-form) | S_min |
|---|---|---|---|---|---|---|
| 100 | j = 1…64 | 65…94 (30) | 95…100 (6) | G_1…G_63 | 1.04e-4 | 0.31493 |
| 200 | 1…128 | 129…187 (59) | 188…200 (13) | G_1…G_127 | 2.19e-5 | 0.31199 |
| 400 | 1…256 | 257…374 (118) | 375…400 (26) | G_1…G_255 | 3.29e-6 | 0.31051 |
| 800 | 1…513 | 514…749 (236) | 750…800 (51) | G_1…G_512 | 5.10e-6 | 0.30976 |

Exactly: E_j = R_j for j ≤ m, and E_j = min(R_m + α(j − m), 2) for j ≥ m, with
m = max{k : R_k − R_{k−1} ≤ α}; R is increasing with increasing increments.
At E, G_n has slack 8 − 2c₂ and H has slack 8 − 4c (both 6.19e-4 for n = 100). The contact
angle mΔθ is 0.796–0.805 rad and the first angle at r = 2 is 1.175–1.182 rad.
For comparison (numerical remark, not a claim): the continuous problem with
the same structure (line r = sec φ until its slope reaches 1.5, then slope 1.5,
then r = 2) gives area A* = 4.2728604777…, and −v_n − A* ≈ 1.13/n for all four n.

---

## 4. Exactly feasible primal points

### 4.1 Construction

The primal point is the envelope itself: r = E, d_i = E_{i+1} − E_i. It is
defined by the recurrences of Section 3.2, so every coordinate is a rational
number computed exactly. No repair, rounding or interval existence argument
is needed. Exact feasibility follows from Lemma 3 and was checked directly:

- by the verifier (`R/reviews/open-instances-verification/v_camshape.py`,
  `logs/camshape_verify.json`): every row, bound and slope constraint holds
  exactly; 63/127/255/512 convexity rows active; objective equals the bound;
- by this dossier (`check_exact.py`): the same, with a generic evaluation of
  all 2n OSIL rows and all bounds.

### 4.2 Objective enclosure

The objective at (E, d^E) is exactly v_n (gap exactly 0). Its decimal
enclosure is [floor, ceil] at 14 decimals in Theorem 1(d); the verifier's
400-bit enclosure has width about 1e-118.

A binary64 rounding of E is not exactly feasible (row violations 2.8e-16 to
4.8e-16 in the author's float envelope). This does not matter: the exact
point is the witness.

### 4.3 The MINLPLib points (exact evaluation, three independent codes agree)

| point | objective | max violation (row) | objective − v_n |
|---|---|---|---|
| camshape100 p1 | −4.284147121746719 | 1.95e-14 (e44) | +2.43e-14 |
| camshape200 p1 | −4.278500232993864 | 1.84e-14 (e6) | −1.14e-12 |
| camshape400 p1 | −4.275688478934241 | 2.53e-14 (e221) | −8.70e-12 |
| camshape400 p2 (listed) | −4.275696633420248 | 3.00e-10 (e400 = G_1) | **−8.154e-6** |
| camshape800 p1 | −4.274274141954209 | 3.91e-10 (e1562, a D row) | −1.52e-14 |
| camshape800 p2 (listed) | −4.274306866226310 | 3.00e-10 (e800 = G_1) | **−3.272e-5** |

The worst-case deficit for points with violations ≤ 3e-10 is
D_400(3e-10) = 2.804e-5 and D_800(3e-10) = 1.125e-4 (Section 8, I-3), so the
p2 deficits are about 29% of what that tolerance permits.

---

## 5. Numbers table

All displays are outward-rounded. "Listed" values come from
`R/bound-audit/pages.json` (MINLPLib pages fetched 2026-09-29, unchanged
2026-10-02).

| instance | best listed dual | our dual (safe display) | primal | gap | sources |
|---|---|---|---|---|---|
| camshape100 | −4.28415233 (ANTIGONE) | −4.28414712174675 | exact optimum attained; ≤ −4.28414712174674 | 0 (exact) | dual and point: `R/reviews/open-instances-verification/logs/camshape_verify.json` ("bound": −4.2841471217467438034); this dossier `checks/camshape/check_exact.log` (30 digits); summary row |
| camshape200 | −4.63229055 (ANTIGONE) | −4.27850023299273 | ≤ −4.27850023299272 | 0 | same files (−4.2785002329927222919) |
| camshape400 | −4.97265746 (ANTIGONE) | −4.27568847892555 | ≤ −4.27568847892554 | 0 | same files (−4.2756884789255432152) |
| camshape800 | −5.12584096 (GUROBI) | −4.27427414195420 | ≤ −4.27427414195419 | 0 | same files (−4.2742741419541941011) |

- The summary's displays (`R/open-instances-summary.md`, closed table) are
  exactly the floor of v_n at 14 decimals for all four n (checked).
  `P/integration/gap-values.json` records gap 0 for all four. **No
  disagreement with the summary.**
- **Unsafe displays in older notes (do not copy into the paper):**
  `R/open-instances/open-instances-report.md` Section 1 gives "our verified
  dual bound" −4.28414712174674, −4.27850023299272, −4.27568847892554,
  −4.27427414195419; these are ceilings, i.e. above v_n by 3.8e-15, 2.3e-15,
  3.2e-15, 4.1e-15. Its Section 5.4 values −4.278500232992722,
  −4.275688478925543 and −4.274274141954194 are also above v_n (by 2.9e-16,
  2.2e-16, 1.0e-16); only the n = 100 value −4.284147121746744 is below.
  Because v_n is attained, these numbers are correct approximations of the
  optimum, but as dual-bound displays they are invalid.
- Starting gaps and improvements: the best listed dual moves up by 5.2e-6,
  0.354, 0.697 and 0.852 (n = 100…800).

---

## 6. Verification record

| check | by | what it checked | verdict |
|---|---|---|---|
| Original computation (`R/open-instances/camshape_bound.py`, `camshape_model.py`) | author | structure assertions on the OSIL; U, S, R, E in mpmath intervals at 0.4n + 60 digits from the decimal constants (`repr(float(s))`, valid because every constant has ≤ 15 significant digits); upper ends only in the envelope; envelope evaluated as a primal point in 50-digit arithmetic (violations ≤ 4.8e-16, from float storage) | bound valid; "exact optimum" claimed |
| Independent recheck in the same report (`verify_independent.py`) | author | closed form of S, LP relaxation with HiGHS, SLSQP | agree to about 1e-12 (floating point; evidence only) |
| `R/reviews/open-instances-verification/verification-report.md` §5, `v_camshape.py` | independent verifier (did not run or import the authors' code; read `camshape_bound.py` only to confirm the pair (1,2) exclusion) | own OSIL reader keeping decimal strings; every row checked by string equality against the template; U, S, E in `Fraction`; E exactly feasible (every row, bound, slope); objective = bound; MINLPLib p1/p2 evaluated exactly | **verified (exact), stronger than claimed**: the bounds are exact optima |
| `P/reviews/lit-control-review-r1.md`, `-r2.md` | independent literature reviewers | provenance, QPLIB copies (exact rational comparison of all rows and bounds), solver logs, novelty labels | verified; minor issues fixed |
| `paper-open-minlplib/development/dossiers/solvers.md`, Propositions 2, 3, 12 | solvers-dossier author (own checks; flagged as needing review) | BARON claims vs v_n; worst-case tolerance deficit D_n(ε); comparison bounds for the four QPLIB copies | author-checked only |
| This dossier, `checks/camshape/` | dossier author (not independent of the dossier) | third exact implementation from the OSIL (own XML reader, generic row evaluation); C1–C5 and Lemma 3 case split row by row; the omitted COPS row; GAMS = OSIL; QPLIB copies (bounds, exact feasibility of their envelopes, their reference points); D_n(ε); robust enclosures | all agree with the verifier to 20 digits; reproduces Propositions 3 and 12 of the solvers dossier; new results in Section 8 need review |

**Status of each claim.**

| claim | status |
|---|---|
| v_n is the optimal value of MINLPLib camshape<n>, attained, unique optimizer E | proved (Theorem 1: analytic proof plus exact rational checks C1–C5); verified by independent code (verifier, `Fraction`) and re-verified by this dossier |
| summary displays are valid (floor at 14 decimals) | proved by exact comparison (this dossier) |
| MINLPLib p2 points lie 8.154e-6 / 3.272e-5 below v_n, violations 3.0e-10 | proved by exact evaluation of the decimal `.sol` values (verifier; this dossier) |
| MINLPLib .gms = OSIL for camshape | proved by exact parse of both files (this dossier only) |
| omitted COPS row is slack at E | proved, exact (this dossier only; previously floating point) |
| worst-case tolerance deficits D_n(ε) | proved, exact rational with upward rounding (solvers dossier Prop. 3 and this dossier; same project, no independent review) |
| exact optima of the QPLIB copies; QPLIB reference points 2703/3177 below them | proved, exact (this dossier only; needs review) |
| MINOTAUR's QPLIB_3177 value not attainable exactly | proved for the .gms model (solvers dossier Prop. 12; this dossier); for the .nl it read: assumption-qualified (same rows and bounds as the .gms) |
| optimum of the exact-constant COPS discretization within ±5.9e-11 … ±3.6e-9 of v_n | assumption-qualified (mpmath interval arithmetic for the constant distances); otherwise exact |
| BARON camshape100/200 returned points are not exactly feasible | proved from objective values below v_n, given the 50-digit objective evaluation (solvers dossier Prop. 2); row residuals ≈ 1e-10 are numerical evidence |
| SCIP exploratory camshape100 incumbent 5.3e-5 below v_n | numerical, not independently checked |
| cell-DP failure on camshape100 | numerical, not independently checked |
| continuous limit A* = 4.27286…, −v_n − A* ≈ 1.13/n | numerical remark only |

**Remaining assumptions for Theorem 1:** none beyond correct integer
arithmetic and correct parsing. A1/A2 (eg family) and mpmath correctness do
not enter. mpmath interval arithmetic enters only the optional COPS-constant
statement (Section 8, I-7) and the author's original (superseded) computation.

---

## 7. Relation to prior work

### 7.1 These instances

- **COPS** ([[dolan2001-benchmarking-optimization-software-with-cops]],
  [[dolan2004-benchmarking-optimization-software-with-cops]]): local solvers
  only, no global claim. COPS 2.0 Table 4.2 (LOQO) gives 4.28414, 4.27850,
  4.27568, 4.27427, agreeing with −v_n to the printed digits; LANCELOT values
  4.30178 … 4.85693 at violations 3–5e-6 exceed the exact optima by 0.018 to
  0.58 (early evidence of the ill-conditioning). COPS 3.0 Table 3.2 gives
  4.27427 for n = 800 for all five solvers.
- **camshape100 was already solved globally in floating point.** Octeract
  4.5.1 solved it in 19.40 s at 1e-6 relative/absolute gap and 1e-6
  feasibility tolerance ([[bestuzheva2025-global-optimization-of-mixed-integer]],
  App. B.1; arXiv:2301.00587v1 pp. 36–37; also 19.42 s at 1e-4 gap, App. B.2).
  BARON, Lindo and SCIP did not solve it in 2 h there. Octeract (2021–2024)
  and ANTIGONE (2021–2026) are listed as solving QPLIB_2738 in Mittelmann's
  QPLIB benchmark ([[mittelmann2026-continuous-non-convex-qplib-benchmark]]);
  ANTIGONE's 2026 "Global minimum" −4.284302 lies 1.557e-4 below the exact
  optimum of QPLIB_2738 (and 1.549e-4 below v_100). MINLPLib's own ANTIGONE
  bound was within 1.216e-6 relative.
- **camshape200:** Octeract 4.5.1 is listed as solving QPLIB_2480 in 6853 s
  (Mittelmann, 7 Jan 2023 only); value and log unavailable. ANTIGONE 2026 timed
  out at −4.601964 on the copy.
- **camshape400:** never listed as solved. SCIP 9.2.1's primal −4.33023953971002
  on QPLIB_2703 is 5.46e-2 below that copy's exact optimum.
- **camshape800:** MINOTAUR (0.2.1–0.4.1, 2021–2026) is listed as solving
  QPLIB_3177; the 2026 log (read from `QPLIB_3177.nl`) reports "Optimal
  solution found", −4.2774, one node, remaining-node bound +∞. This value is at
  least 3.16e-3 below the exact optimum of the QPLIB_3177 .gms model
  (Section 8, I-6). On the smaller copies the same version stops at the 3 h
  limit with gaps of 5.9–20.8%.
- **Other bounds** (all weak): SCIP 7/8 gaps 6–22% (SCIP 8.0 suite report,
  [[bestuzheva2021-the-scip-optimization-suite-8]]); Mattick–Mutschler 2023
  ([[mattick2023-reinforcement-learning-for-node-selection]]) 7–23% after 45 s;
  surrogate duality (Müller et al., arXiv:1912.00356v1, Table 4, PDF p. 40)
  −4.908 for camshape100 (the journal version
  [[muller2022-on-generalized-surrogate-duality-in]] in the knowledge base has
  no camshape entries);
  Mittelmann's MINLP benchmark (26 Feb 2026): BARON, SHOT, LINDO, SCIP exceed
  7200 s on camshape100 ([[mittelmann2026-mixed-integer-nonlinear-programming-benchmark]]).
- **Our own one-hour campaign** (`P/solver-runs/results_table.md`): BARON
  26.5.27 reports optimality on camshape100 (0.45 s) and camshape200 (23.2 s)
  at −4.28414764756 and −4.27850228570. Both duals are valid and lie
  1.23e-7 and 4.80e-7 (relative) below v_n; both incumbents are not exactly
  feasible. All other runs end at the time limit with final duals 5.4% to
  21.7% below v_n (relative), e.g. SCIP 10.0.3 dual −5.20341 on camshape800. So current
  solvers close n = 100, 200 at tolerance level, not n = 400, 800.

### 7.2 The mechanism

- Discrete Sturm comparison / disconjugacy: the sign of the Green's function
  of a second-order difference operator is equivalent to disconjugacy
  ([[hartman1978-difference-equations-disconjugacy-principal-solutions]],
  unread in the knowledge base; [[bohner1996-linear-hamiltonian-difference-systems-disconjugacy]],
  read, for the discrete Jacobi/Reid framework). The paper only needs the
  elementary Chebyshev identity of Lemma 1, which it proves.
- The polar-convexity identity (convexity ⇔ u'' + u ≥ 0 for u = 1/r) is
  classical; the discretization is exactly the COPS triangle-area row.
- The min-plus envelope is the standard greatest Lipschitz minorant on a path.
- Contribution claimed: the certificates and their exactness for these
  instances, not the mechanism (consistent with
  `R/open-instances-summary.md`, "What the pattern shows").

---

## 8. Critical examination

I re-derived the proof (Section 3.4 is my own write-up) and recomputed every
number exactly. Nothing below invalidates a claimed result.

**I-1 (minor, proof completeness).** The original report argues feasibility
of E in one sentence ("the convexity rows hold at the kinks because u only
bends upward there"). That sketch is incomplete: it does not cover the rows
inside the maximal-slope phase or the j = 2 edge (d_1 free). Rigor currently
rests on the verifier's exact row-by-row check, which is a complete proof for
these four files. *Resolution (supplied):* Lemma 3 proves feasibility for any
constants satisfying (C1)–(C5); `check_exact.py` confirms its case split row
by row (case A rows 64/128/256/513, case B rows 35/71/143/286, concavity and
e_j ≥ (2 − c)w_j asserted in every case-B row). Put Lemma 3 in the paper and
cite the exact row check as a second, independent confirmation.

**I-2 (minor, wording).** The summary says the camshape zero gaps are "an
attained exact optimum proved analytically". The proof is analytic up to the
finite exact-rational checks (C1)–(C5) and the evaluation of v_n.
*Resolution:* "proved (comparison theorem with exact rational checks)".

**I-3 (minor, wording; also solvers dossier I3).** The summary explains the
p2 deficits "because the chain amplifies violations up to about 600-fold".
600 is the largest single Green's-function weight (605.9 for n = 800). The
objective deficit per unit of maximum violation is much larger: 8.15e-6/3e-10
≈ 2.7e4 (n = 400) and 3.27e-5/3e-10 ≈ 1.1e5 (n = 800). *Check run:*
`tol_check.py` re-derives the worst-case deficit D_n(ε) over points that
violate every row and bound by at most ε (objective row exact): with
δ = ε/(1−ε)³, u_j ≥ S′_j − δ W_j (W_j = Σ_{m≤j−2} U_m, S′ started from
1/(ū+ε)), radius bounds 2 + ε, slopes α + 2ε, upward rounding to a 2^-200 grid.
Results: D_100(1e-10) = 6.0447e-7, D_100(1e-8) = 6.0449e-5,
D_200(1e-10) = 2.3551e-6, D_400(1e-10) = 9.3475e-6, D_400(3e-10) = 2.8043e-5,
D_800(3e-10) = 1.1255e-4; D_n(ε)/(n²ε) = 0.604, 0.589, 0.584, 0.586. These
agree with Proposition 3 of the solvers dossier to all printed digits.
*Resolution:* "row violations of size ε can lower the objective by up to
about 0.6 n² ε (2.8e-5 for n = 400 and 1.1e-4 for n = 800 at ε = 3e-10)".

**I-4 (minor, displays).** The older report's camshape "verified dual"
displays are ceilings (Section 5). *Resolution:* use only the summary's floor
displays or Theorem 1(d). No computation needed.

**I-5 (improvement; resolves an open question in the literature report).**
The literature report and its r2 review state that whether the QPLIB
rounding moves the optimum "was not determined"/"is not established". It is
now determined exactly. `check_gms.py` parses the QPLIB .gms copies with an
own exact parser, asserts the same structure, and finds that each copy's
envelope is exactly feasible in that copy (zero row and bound violations;
63/127/255/512 active rows). So the copies' exact optima are

| copy | c | exact optimum (floor, 16 decimals) | minus v_n |
|---|---|---|---|
| QPLIB_2738 (n = 100) | 1.9998452 | −4.2841462678046117 | +8.539e-7 |
| QPLIB_2480 (n = 200) | 1.999960914 | −4.2784904096736786 | +9.823e-6 |
| QPLIB_2703 (n = 400) | 1.99999018 | −4.2756507125126530 | +3.777e-5 |
| QPLIB_3177 (n = 800) | 1.999997539 | −4.2741871514717434 | +8.699e-5 |

(These agree with Proposition 12 of the solvers dossier, which gave the bounds
only.) All four copies round c up, which tightens every convexity row
(monotonicity, I-6). The other constants move both ways (ū is rounded down in
2738/3177 and up in 2480/2703; α down in 2738/2480/3177 and up in 2703); the
net effect raises the optimum in all four. Consequences:

- The MINLPLib optimizers are not feasible for the copies. QPLIB's reference
  points for 2738 and 2480 are near-optimal (objective 6.0e-14 below and
  1.5e-12 above the copy optimum; violations about 2e-14), but **QPLIB's
  reference points for 2703 and 3177 are tolerance artifacts**:
  violations 3.0e-10 (row G_1) and objectives 8.154e-6 and 3.272e-5 below the
  copies' exact optima (`eval_qplib_points.py`). The literature report's
  sentence "Each is at or above our MINLPLib optima, which is consistent with
  our certificates" is true but should add this copy-level fact.
- The literature report cites "BARON's QPLIB_2738 incumbent is within 1.9e-8
  of our MINLPLib camshape100 optimum" as evidence of insensitivity. That
  incumbent (−4.28414710266608) lies 8.35e-7 **below** the exact optimum of
  QPLIB_2738, so it is a tolerance artifact on the copy and its closeness to
  v_100 is a coincidence. Drop this argument; the exact copy optima replace it.

*Resolution:* report the copy optima as new results after an independent
review of `check_gms.py` (cost: under 1 h of review; about 10 min of compute).

**I-6 (improvement; upgrades the camshape800 refutation).** MINOTAUR read
`QPLIB_3177.nl`, not the .gms text. The .nl constants are presumably binary64
transcriptions of the same decimals. A monotonicity argument removes this
gap except for model structure:

*Proposition (robust enclosure).* For u > 0 the rows e_j(u) ≥ 0 tighten as c
increases, r_1 ≤ ū and |d_j| ≤ α tighten as ū and α decrease, and −c₀ Σ r
decreases as c₀ increases. Hence every model with the structure of
Section 1.2 (in particular positive lower bounds 1 and ℓ) and constants
c ≥ c⁻, ū ≤ ū⁺, α ≤ α⁺, c₀ ≤ c₀⁺ has optimal value
≥ −c₀⁺ Σ E(c⁻, ū⁺, α⁺) (Theorem 1(a) at the corner; needs C1 at c⁻), and every
model with c ≤ c⁺, ū ≥ ū⁻, α ≥ α⁻, c₀ ≥ c₀⁻, c₂ ≤ 4, c_H ≤ 2, ℓ ≤ 2 contains
the corner envelope E(c⁺, ū⁻, α⁻) (checked exactly; its last two entries are
2), so its optimum is ≤ −c₀⁻ Σ E(c⁺, ū⁻, α⁻).

`robust.py` with perturbation η = 1e-14 in each of c, ū, α, c₀ gives

| model | enclosure of the optimum for all constants within 1e-14 | half-width |
|---|---|---|
| camshape100 | [−4.2841471218055516, −4.2841471216879360] | 5.9e-11 |
| camshape200 | [−4.2785002332195158, −4.2785002327659288] | 2.3e-10 |
| camshape400 | [−4.2756884798207931, −4.2756884780302933] | 9.0e-10 |
| camshape800 | [−4.2742741455363412, −4.2742741383720470] | 3.6e-9 |
| QPLIB_2738 | [−4.2841462678634194, −4.2841462677458038] | 5.9e-11 |
| QPLIB_3177 | [−4.2741871550536714, −4.2741871478898154] | 3.6e-9 |

Binary64 conversion changes each constant by at most 4.4e-16, well inside
η. So any binary64 transcription of QPLIB_3177 with the same rows has
optimum ≥ −4.2741871550536714, at least 3.16e-3 above the upper end
−4.27735 of MINOTAUR's printed −4.2774. *Remaining assumption:* the .nl file
has the same rows and bounds as the .gms file (not inspected; the .nl is not
in the source cache). *Resolution:* state the refutation as proved for the
QPLIB_3177 .gms model and for every binary64 transcription with the same
structure; fetch `QPLIB_3177.nl` to remove the structural assumption (network
fetch plus a 2-minute exact run). Also state the semantics: under MINOTAUR's
own feasibility tolerance a value near −4.2774 can be tolerance-feasible
(D_800(ε) ≈ 3.75e5 ε, and COPT reports −4.277371 at violation 2.98e-8), so
"false" means "not attainable by any exactly feasible point"; the root
closure with remaining-node bound +∞ is separate, circumstantial evidence of
a solver defect.

**I-7 (improvement; the COPS model).** The literature report says
"camshape = COPS 2.0 optimum rests on a floating-point slack check".
`cops_consts.py` shows (mpmath intervals) that every decimal constant is
within 5.1e-15 of its exact COPS value (θ = 2π/(5(n+1)) exactly). The COPS
discretization is the MINLPLib model with exact constants plus the row
|r_2 − r_1| ≤ αθ. `omitted_row_hi.py` checks exactly that the "upper" corner
envelope satisfies that row (|E_2 − E_1| ≤ 3.1e-4 ≪ α). So the robust
enclosures of I-6 also enclose the optimum of the exact-constant COPS 2.0
discretization (e.g. COPS camshape100 optimum ∈ [−4.2841471218055516,
−4.2841471216879360], i.e. area 4.28414712175 ± 6e-11), under the assumption
that mpmath interval arithmetic is correct. This replaces the floating-point
statement. Optional for the paper.

**I-8 (minor, precision of a remark).** The report's "nθ/π = 0.396 to 0.3995"
uses the nominal Δθ. The relevant angle is φ = arccos(c/2) for the decimal c;
positivity is checked exactly (C1) or by the rational test c/2 > cos(π/n).
No issue; state (C1) in the paper rather than the nominal angle.

**I-9 (minor, novelty framing).** The summary's literature row for camshape200
says "Partly known; exact optimum new as far as found". Our own campaign shows
BARON 26.5.27 reaching a valid dual within 4.8e-7 relative in 23 s, and
Octeract was listed as solving the rounded copy in 2023. The paper must not
present camshape200 as beyond current solvers at tolerance level. Same for
camshape100 (Octeract; BARON in 0.45 s). The large gaps on MINLPLib's pages
for n = 200 are stale relative to current BARON, though not for n = 400/800
(BARON's dual −4.622/−5.145 after 1 h).

**I-10 (minor, statement strength).** Uniqueness of the optimizer and the
greatest-element property are not stated in any project document; they follow
in one line from (a) and (b). *Resolution:* include in Theorem 1.

**I-11 (check of other claims).** Confirmed exactly: the p2 deficits
(8.154e-6, 3.272e-5) and violations (3.0e-10, row G_1); the p1 deviations
(+2.4e-14, −1.14e-12, −8.70e-12, −1.52e-14); c₂ − 2c = −1e-14 for n = 400; the
active-row counts; S_min; "MINLPLib's listed bounds were within 1.3e-6
relative" (1.216e-6). The summary's verification label "verified (rational)"
is correct.

**I-12 (scope).** Theorem 1 is about exact feasibility of the stored decimal
model. Tolerance-feasible points can be better by up to D_n(ε). The paper
must state this whenever it compares v_n with MINLPLib's listed primal values
or with solver incumbents.

---

## 9. What the paper may and must not claim

**May claim (suggested wording):**

- "For n = 100, 200, 400, 800, the MINLPLib instance camshape<n>, with its
  decimal constants read exactly, has the optimal value v_n given in Table X.
  The optimum is attained at an explicit rational point, which is the unique
  optimal solution. The proof is a discrete Sturm comparison for u = 1/r plus
  a min-plus envelope for the slope rows; the only computation is an exact
  rational evaluation of O(n) recurrences."
- "To the best of our knowledge, these are the first proofs of global
  optimality for camshape200, camshape400 and camshape800, and the first exact
  optimum for camshape100, which had been solved globally in floating point
  (Octeract, 1e-6 tolerances)."
- "MINLPLib's listed primal values for camshape400 and camshape800 (points p2)
  violate the convexity rows by 3.0e-10 and lie 8.15e-6 and 3.27e-5 below the
  exact optima. Our dual bounds are therefore above these listed values; the
  listed values are attainable only within a feasibility tolerance."
- "Row violations of size ε can lower the objective by up to about 0.6 n² ε
  (rigorous bound D_n(ε))."
- After review of I-5/I-6: "The QPLIB copies (rounded constants) have exact
  optima higher by 8.5e-7 to 8.7e-5. MINOTAUR's reported optimum −4.2774 for
  QPLIB_3177 is not attainable by any exactly feasible point of that model or
  of any binary64 transcription with the same rows; ANTIGONE's 'global
  minimum' −4.284302 on QPLIB_2738 lies 1.56e-4 below that copy's optimum."
- "The optimum is insensitive to the 15-digit rounding of the constants:
  perturbing them by 1e-14 moves it by at most 5.9e-11 (n = 100) to
  3.6e-9 (n = 800)." (I-6/I-7; mpmath iv needed only for the COPS
  statement.)

**Must not claim:**

- that the mechanism is new (Sturm comparison, disconjugacy, Green's
  functions and min-plus envelopes are classical);
- that camshape100 or camshape200 are beyond current global solvers at
  tolerance level (Octeract solved camshape100; BARON 26.5.27 reaches valid
  duals within 1.2e-7 and 4.8e-7 relative in 0.45 s and 23 s);
- that BARON, ANTIGONE, MINOTAUR, SCIP or MINLPLib made "errors" in the
  camshape values without the exact-feasibility qualifier; BARON's and
  ANTIGONE's duals are valid, and their optimality claims fail only under
  exact feasibility (call them tolerance artifacts);
- that the camshape800 MINOTAUR claim is refuted for the .nl model without
  the structural assumption of I-6 (until the .nl is checked);
- that v_n is the optimum of the COPS model or of the QPLIB copies (they are
  different models; use the separate enclosures and copy optima);
- "gap 0" without saying that it means an attained exact optimum, not a
  subtraction of displays;
- the old unsafe displays of Section 5, or "600-fold" amplification;
- the continuous-limit value A* (numerical remark only).

---

## 10. Candidate figures and tables

1. **Figure (cam profile).** The optimal radii E_j against the angle jΔθ for
   n = 100 and 800, with the comparison line R_j = 1/S_j, the cap r = 2, and the
   three phases marked (contact, maximal slope, r = 2). Optionally a polar
   inset showing the cam with the base circle and the straight-line segment.
   Data: `check_exact.py` (E, R are returned by `main`).
2. **Table (main results).** Per n: listed best dual (solver), listed primal
   (point, infeasibility), v_n floor/ceil displays, phase lengths
   (64/30/6 …), active rows, S_min, max U_m. Sections 2, 3.3, 3.6.
3. **Table (tolerance artifacts).** Point, model, max violation, deficit
   against the exact optimum, worst case D_n(ε), ratio: MINLPLib p2
   (400/800), BARON (100/200/400/800), GUROBI 800, SCIP 100, QPLIB reference
   points 2703/3177, ANTIGONE 2738, MINOTAUR 3177. Data: Section 4.3, I-3,
   I-5, solvers dossier Proposition 3, `P/solver-runs/point_checks.log`.
4. **Figure (sensitivity).** D_n(ε) against ε on log–log axes for the four
   n, with observed (ε, deficit) points; shows the ≈ 0.6 n² ε scaling.
5. **Small table (QPLIB copies).** Copy optimum, shift from v_n, reference
   point deficit (I-5).
6. **Proof box.** Lemma 1 (Green's function) and the two-case feasibility
   argument (Lemma 3) fit in half a page.

---

## Appendix: checks run for this dossier

All in `/tmp/camshape_dossier_o5/` (copies of the inputs; sha256 prefixes in
`checks/camshape/input_sha256.txt`), `OMP_NUM_THREADS=1`, one core each, at
most two processes at a time. Scripts and logs are copied to
`checks/camshape/`.

| command | result | time |
|---|---|---|
| `python3 check_exact.py 100 200 400 800` | C1–C5 pass; v_n to 30 digits equal to the verifier's 20; summary displays are exact floors; E exactly feasible in a generic evaluation of every OSIL row and bound; Lemma 3 case split confirmed; omitted COPS row slack; p1/p2 evaluated | 6 min 9 s |
| `python3 check_gms.py camshape{100,200,400,800}.gms QPLIB_{2738,2480,2703,3177}.gms` | own GAMS parser; MINLPLib .gms constants = OSIL constants; same optima; QPLIB copies: bounds and exactly feasible envelopes | about 10 min |
| `python3 eval_qplib_points.py QPLIB_*.gms:QPLIB_*.sol` | QPLIB reference points: 2738/2480 near-optimal; 2703/3177 violate G_1 by 3.0e-10 and lie 8.154e-6/3.272e-5 below the copy optima | about 5 min |
| `python3 tol_check.py 100:1e-10 100:1e-8 200:1e-10 400:1e-10 400:3e-10` and `800:3e-10` | D_n(ε) values of I-3 | about 6 min |
| `python3 cops_consts.py` | decimals within 5.1e-15 of exact COPS constants (mpmath iv, 60 digits) | seconds |
| `python3 omitted_row_hi.py 100 200 400 800` | omitted row holds at the perturbed corner envelope | about 3 min |
| `python3 robust.py camshape100.osil:1e-14 QPLIB_2738.gms:1e-14 camshape200.osil:1e-14 camshape400.osil:1e-14 camshape800.osil:1e-14 QPLIB_3177.gms:1e-14` | robust enclosures of I-6 | about 17 min |

No project-wide checks were run; no CI was inspected. These are targeted
dossier checks by the dossier author, not an independent review.
