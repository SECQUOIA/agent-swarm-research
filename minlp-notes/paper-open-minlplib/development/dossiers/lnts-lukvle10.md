# Dossier: lnts50/100/200/400 and lukvle10

Family key: `lnts-lukvle10`. Written 2026-10-04 for the MPC paper. R below means
`research-20260929/`. All numbers are copied from the cited files or recomputed
by the commands in Appendix A. "Verified" means rechecked by an independent
reviewer with separate code; "dossier check" means checked by the author of this
dossier with new code (not yet independently reviewed).

## 0. Main findings

1. **Both certificates are sound.** I re-derived every proof step and found no
   error that affects a claimed bound, primal point or gap.
2. **lnts can be strengthened from "gap ≤ 5.79e-13" to "exact optimum,
   attained".** The existing dual argument, evaluated at the exact dual
   multipliers instead of at a shifted step `h2 = h*(1 − 1e-12)`, proves that
   the optimum equals `N·h*`, where `h*` is defined by one scalar equation
   (Theorem 3 below). It is attained by the discrete linear-tangent control. A
   dossier check that uses only Python integers and fractions encloses each
   optimum in an interval narrower than 5e-61 (Section 8.1). This needs one
   independent review (seconds of CPU) before the paper uses it.
3. **lukvle10 stays at a gap of ≤ 1.42e-9 (4.03e-12 relative).** The dual side
   relies on mpmath interval `exp`/`log` in both independent certificates. The
   KKT point's global optimality is not proved. A cheap refinement (local
   convexity plus Krawczyk on each 2-D problem) would probably shrink the gap to
   about 1e-25 (Section 8.2, item L9).
4. **Display problems to avoid in the paper.**
   - The verification report's lukvle10 value 352.2380254050785 is rounded to
     nearest and lies 4.4e-14 above the certified lower end. Use 352.2380254050784.
   - The summary's lukvle10 primal 352.2380254064961 is MINLPLib p5's displayed
     value, not the exact point's value. It is a valid upper bound, but the
     exact point gives 352.2380254064957.
   - Our lnts50 dual lies 4.2e-11 *above* the objective of MINLPLib's listed
     point p1 (0.55466876489565, row violation 9.1e-10). The paper must explain
     this as camshape400/800 are explained: p1 is only tolerance-feasible.

## 1. Instances and models

### 1.1 lnts50, lnts100, lnts200, lnts400 (linear tangent steering)

**Source and meaning.** GAMS Model Library `lnts` (SEQ=237), the GAMS translation
of COPS 2.0 problem 9, "particle steering" (Dolan–Moré 2000; COPS 3.0, 2004). A
particle starts at rest at the origin. A thrust of constant magnitude `a = 100`
acts in a steerable direction `θ(t)`. The particle must reach height 5 with
horizontal speed 45 and vertical speed 0 in minimum time. The continuous problem
is the classical linear-tangent steering problem (Bryson–Ho 1975, pp. 59–62;
boundary data from Betts et al. 1993). The MINLPLib instances use the trapezoidal
rule with `N` intervals of length `h`. MINLPLib added them on 2001-07-31 from
GLOBALLib (R/publication/literature/control/report.md, lines 247–253).

**Model** (as asserted from the OSIL by exact string comparison in
R/reviews/open-instances-verification/v_lnts.py `check_structure`). Variables, in
OSIL order: `θ_0..θ_N`, `px_0..px_N`, `py_0..py_N`, `vx_0..vx_N`, `vy_0..vy_N`,
`h` (index 5N+5). All are continuous.

    min  N·h
    s.t. for i = 0..N−1:
      px_{i+1} − px_i − (h/2)(vx_i + vx_{i+1}) = 0
      py_{i+1} − py_i − (h/2)(vy_i + vy_{i+1}) = 0
      vx_{i+1} − vx_i − (h/2)(100 cos θ_i + 100 cos θ_{i+1}) = 0
      vy_{i+1} − vy_i − (h/2)(100 sin θ_i + 100 sin θ_{i+1}) = 0
      px_0 = py_0 = vx_0 = vy_0 = 0,  py_N = 5,  vx_N = 45,  vy_N = 0
      −1.5707963267949 ≤ θ_j ≤ 1.5707963267949,  h ≥ 0,  all other states free.

The OSIL writes the velocity rows as `v_{i+1} − v_i + (100 f(θ_i) + 100 f(θ_{i+1}))·(−.5)·h`.
Several fixed values come from `ub="0"` with the default `lb = 0`.

| instance | variables | rows | sense | integer vars |
|---|---|---|---|---|
| lnts50 | 256 | 200 | min | 0 |
| lnts100 | 506 | 400 | min | 0 |
| lnts200 | 1006 | 800 | min | 0 |
| lnts400 | 2006 | 1600 | min | 0 |

**Structure that matters.**
- For fixed `h` the recursion is linear in the states, and the states are
  determined uniquely by `(θ, h)`. Summing it gives three aggregate terminal
  equations (Lemma 1). The certificate needs only these.
- The global variable `h` appears in every stage. The objective is monotone in
  `h`, so `h` needs no branching.
- `px` plays no role: `px_N` is free.
- The control bounds are inactive. The bound 1.5707963267949 exceeds π/2 by
  3.4e-15; the optimal controls satisfy `|θ_j| ≤ 0.9524`.

**Provenance issues.** None that affect the certificate. The literature track
found the MINLPLib model equal to COPS 2.0 #9 for `nh = N` (same sizes and
values). The MINLPLib status refresh found the OSIL and GMS files unchanged (OSIL
dated 2019-06-25), the GLOBALLib 2001 versions and the MINLPLib.jl copy
semantically equal, and all statistics snapshots since 2014-12-09 equal
(R/publication/minlplib-status/data/tables.md, Table B2 rows lnts50–400). Older
translations with negative objective values (Smith 2011 thesis: lnts50 −339.2)
are different models and are not comparable.

### 1.2 lukvle10

**Source and meaning.** Lukšan–Vlček (1999, TR V-767), problem 5.10, "generalized
Brown function with Broyden tridiagonal constraints", via CUTEr/CUTEst
`LUKVLE10` with `n = 1000`. It is an artificial test problem with no physical
meaning. MINLPLib added it on 2017-02-06. LUKVLE10.SIF (Gould 2001, default
`N = 10000`) is the same model (R/publication/literature/control/report.md, lines
390–395).

**Model** (asserted in v_lukvle10_prep.py `check_structure`): 1000 free continuous
variables `x_0..x_999`, 998 equality rows, minimization.

    min  f(x) = Σ_{i=0}^{499} F(x_{2i}, x_{2i+1}),   F(a,b) = (a²)^(b²+1) + (b²)^(a²+1)
    s.t. c_j(x) := 1 − x_j + 3x_{j+1} − 2x_{j+2} − 2x_{j+1}² = 0,   j = 0..997.

The OSIL writes the objective terms as `power(square(x_a), square(x_b) + 1)` and the
rows as `−x_j + 3x_{j+1} − 2x_{j+2} − 2x_{j+1}² = −1`. GAMS writes `sqr(a)**b`.
The base is a square, so the real power is defined (as `exp(e·log a)` for
`a > 0` and as 0 for `a = 0`, since `e ≥ 1`).

**Structure that matters.**
- Row `j` is linear in `x_{j+2}` with coefficient −2. It defines `x_{j+2}` from
  `(x_j, x_{j+1})` through the planar map
  `(u, v) ↦ (v, Φ(u, v))`, `Φ(u,v) = (1 − u + 3v − 2v²)/2`.
  The feasible set is therefore a 2-parameter family indexed by `(x_0, x_1)`.
- The map has Jacobian determinant 1/2 and fixed points `±1/√2`. `+1/√2` is an
  attracting focus (|eigenvalue| = √0.5). `−1/√2` is a saddle with eigenvalues
  2.731 and 0.183 (checked by the verifier).
- The best known point (MINLPLib p5) stays on the saddle `x_k ≈ −1/√2` for
  `k ≈ 40..960`, with cheap transients at both ends. Each saddle pair costs
  `F(−1/√2, −1/√2) = 2^{−1/2} ≈ 0.70711`; p5 saves 1.315 against 500 × 0.70711.
- Separator between consecutive pairs: `(x_{2i}, x_{2i+1})`, dimension 2.
- The objective grows super-exponentially for `|x| > 1`, and forward simulation
  amplifies seed errors by about `2.73^998 ≈ 1e436`.

**Provenance issues.** None. The MINLPLib model equals LV 5.10 and LUKVLE10.SIF
for `n = 1000`. The status refresh found the MINLPLib.jl copy (2017-11-23) and
the 2024 Internet Archive captures of the GMS and OSIL files equal to the current
files, and all statistics snapshots since 2017-11-14 equal (Table B2 row
lukvle10). MINLPLib lists p5's infeasibility as 9e-16, while our absolute
maximum row residual of p5 is 3.48e-15. The difference is unexplained and
irrelevant, because our gap uses an exactly feasible point.

## 2. Listed status (MINLPLib pages fetched 2026-09-29, unchanged at the 2026-10-02 refresh)

Source: R/publication/minlplib-status/data/part_a.json (`page.duals`, `page.points`)
and R/open-instances-summary.md. No instance is marked solved.

| instance | best listed dual (solver, date) | other listed duals | metadata dual (≥3 solvers) | listed primal (point, infeasibility) | starting gap vs best dual |
|---|---|---|---|---|---|
| lnts50 | 0.55464755 (GUROBI, 2025-07-31) | SCIP 0.53788851, COUENNE 0.52583155, LINDO 0.50634188 | 0.5258 | 0.55466876 (p1, 9e-10) | 3.8e-5 rel. |
| lnts100 | 0.55299042 (GUROBI, 2025-08-07) | COUENNE 0.52413508, SCIP 0.5089748, LINDO 0.5022977 | 0.509 | 0.5545954 (p1, 8e-15) | 0.29% |
| lnts200 | 0.55219867 (GUROBI, 2025-07-31) | COUENNE 0.52355554, SCIP 0.50543034, LINDO 0.50017634 | 0.5054 | 0.55457702 (p1, 9e-14) | 0.43% |
| lnts400 | 0.55204395 (GUROBI, 2025-08-07) | COUENNE 0.52310285, SCIP 0.50155307, LINDO 0.45 | 0.5016 | 0.55457241 (p1, 3e-10) | 0.46% |
| lukvle10 | 351.223393 (SCIP, 2025-07-31) | LINDO 2.11236694, BARON 0.05080583, COUENNE 0.00006665, ANTIGONE 0 | 0.0508 | 352.2380254 (p5, 9e-16) | 0.29% (1.01 abs.) |

MINLPLib p1 for lnts50 evaluates to 0.55466876489565 with row violation 9.1e-10
(R/reviews/open-instances-verification/logs/lnts_verify.json). This is 4.2e-11
*below* our certified dual display 0.5546687649381 (and 4.3e-11 below the optimum
of Theorem 3), so p1 is a tolerance artifact.

## 3. The certificates

### 3.1 lnts: aggregate Lagrangian, linear-tangent law, monotonicity in h

**Idea in plain words.** For a fixed step `h` the dynamics are linear, so the
end state is a weighted sum of `cos θ_j` and `sin θ_j`. Feasibility then reduces
to three equations in the controls. Combine them with multipliers `(1, μ, ν)`.
Each control then appears in a separate term `w cos θ + b sin θ`, whose maximum
over `θ` is `√(w² + b²)`. This bounds a decreasing function of `h` from above
and hence bounds `h` from below. At the right multipliers the maximizing
controls are feasible, so the bound is the optimum. The maximizers satisfy
`tan θ_j = μ + ν c_j / w_j`, a discrete linear-tangent law.

**Notation.** `a = 100`. Trapezoid weights `w_0 = w_N = 1/2`, `w_j = 1`
otherwise. `c_j = Σ_k w_k W_{kj}` with `W_{kj} = ([j ≤ k−1] + [1 ≤ j ≤ k])/2`.
In closed form (dossier check, exact Fractions, all four N):

    c_0 = N/2 − 1/4,   c_j = N − j  (1 ≤ j ≤ N−1),   c_N = 1/4,
    and the reflection identity c_{N−j} = N w_j − c_j.

`A(h) = 45/(a h) = 9/(20h)`, `B(h) = 5/(a h²) = 1/(20h²)`.

**Lemma 1 (exact elimination).** For any `θ ∈ R^{N+1}` and `h`, let the states be
generated by the recursion from zero initial states. Then

    vx_N = a h Σ_j w_j cos θ_j,   vy_N = a h Σ_j w_j sin θ_j,   py_N = a h² Σ_j c_j sin θ_j.

Hence `(θ, h, states)` is feasible iff the states come from the recursion, `θ`
satisfies its bounds, `h > 0`, and

    (E1) Σ w_j cos θ_j = A(h),   (E2) Σ w_j sin θ_j = 0,   (E3) Σ c_j sin θ_j = B(h).

The OSIL allows `h = 0`, but `h = 0` gives `vx_N = 0 ≠ 45`.

*Proof.* `vy_k = (ah/2) Σ_{i<k} (sin θ_i + sin θ_{i+1}) = a h Σ_j W_{kj} sin θ_j`,
and similarly for `vx`. Then `py_N = (h/2) Σ_{i<N} (vy_i + vy_{i+1}) = h Σ_k w_k vy_k`.
Substituting gives the third identity. The rows are linear in the "next" state
with coefficient 1, so the states are uniquely determined, and `px_N` is free.
The identities are linear in the values `cos θ_j`, `sin θ_j`; they were checked
in exact rational arithmetic with arbitrary rational stand-ins (verifier and
dossier check). □

**Proposition 2 (dual bound).** Let `μ ∈ R`, `ν ≥ 0`, and

    S(μ,ν) = Σ_j √( w_j² + (μ w_j + ν c_j)² ).

Every feasible point satisfies `A(h) + ν B(h) ≤ S(μ,ν)`. Consequently, if
`A(h2) + ν B(h2) > S(μ,ν)` for some `h2 > 0`, then every feasible point has
`h > h2` and `N·h2` is a valid dual bound.

*Proof.* By (E1)–(E3), `A(h) + νB(h) = Σ_j [w_j cos θ_j + (μ w_j + ν c_j) sin θ_j]`.
Each term is at most `√(w_j² + (μ w_j + ν c_j)²)` (Cauchy–Schwarz), which gives
the first claim. `A + νB` is strictly decreasing on `(0, ∞)` because `ν ≥ 0`. So
`h ≤ h2` would give `A(h) + νB(h) ≥ A(h2) + νB(h2) > S`, a contradiction. □

Proposition 2 is the certificate of R/open-instances/open-instances-report.md
§3.3. It uses no control bounds and no `px` row. The verified computations
evaluate `S − νB(h2) − A(h2) < 0` at `h2 = h*(1 − ε)`, `ε = 1e-10` (authors) and
`ε = 1e-12` (verifier). The authors use binary64 `μ`, `ν`, `h2` in 60-digit
`mpmath.iv`; the verifier converts its 60-digit Newton values to 50-digit `iv`
intervals, so the check covers the exact 60-digit numbers. The verifier's interval upper ends of
`S − νB(h2) − A(h2)` are −8.64e-11, −1.73e-10, −3.45e-10 and −6.91e-10 at
`ε = 1e-12` for N = 50, 100, 200, 400.
The certified bound is `N·h2`, where `h2` is a 60-digit binary number.

**Theorem 3 (exact optimum; new in this dossier, needs independent review).** Let
`r_j = c_j/w_j − N/2`, that is, `r_0 = (N−1)/2`, `r_j = N/2 − j` for
`1 ≤ j ≤ N−1`, and `r_N = −(N−1)/2`. For `ν ≥ 0` define

    C(ν) = Σ_j w_j (1 + ν² r_j²)^{−1/2},
    D(ν) = Σ_j c_j ν r_j (1 + ν² r_j²)^{−1/2},
    g(ν) = D(ν) − (20/81) C(ν)².

If `ν* > 0` and `g(ν*) = 0`, then the optimal value of lntsN is `N·h*` with
`h* = 9/(20 C(ν*))`. It is attained at `θ*_j = arctan(ν* r_j)`, `h = h*`, with
the states from the recursion. For N ∈ {50, 100, 200, 400} such a `ν*` exists,
and the optimal values lie in these intervals:

| N | ν* (numerical) | optimal value N·h* enclosed in |
|---|---|---|
| 50 | 0.05640028332758032986088817… | [0.5546687649386788986220922339726517468015, …016] |
| 100 | 0.02817764593774146276705563… | [0.5545954011669111610017828739043968162226, …227] |
| 200 | 0.01408601756576152360926878… | [0.5545770161030836720556252926039795506005, …006] |
| 400 | 0.00704265847933977081026324… | [0.5545724137006871088173911331507631508456, …457] |

*Proof.*
1. *Feasibility.* Put `t_j = ν* r_j`, so `cos θ*_j = (1+t_j²)^{−1/2}` and
   `sin θ*_j = t_j (1+t_j²)^{−1/2}`. Since `|θ*_j| < π/2 < 1.5707963267949`, the
   bounds hold. The reflection identity gives `r_{N−j} = −r_j`, and
   `w_{N−j} = w_j`, so `Σ w_j sin θ*_j = 0` (E2). By definition
   `Σ w_j cos θ*_j = C(ν*) = 9/(20 h*) = A(h*)` (E1). Also
   `Σ c_j sin θ*_j = D(ν*) = (20/81) C(ν*)² = (20/81)·(81/(400 h*²)) = B(h*)`
   (E3). By Lemma 1 the point is feasible, with objective `N h*`.
2. *Optimality.* Apply Proposition 2 with `ν = ν*` and `μ* = −ν* N/2`. Then
   `μ* w_j + ν* c_j = w_j t_j`, so
   `S(μ*, ν*) = Σ w_j √(1+t_j²) = Σ [w_j cos θ*_j + w_j t_j sin θ*_j]`.
   By (E1)–(E3) at the point, this equals `A(h*) + ν* B(h*)`. Since `A + ν*B` is
   strictly decreasing, every feasible point has `h ≥ h*`.
3. *Enclosure.* `g` is continuous. The dossier check shows
   `g(ν_lo) < 0 < g(ν_hi)` for rationals `ν_lo < ν_hi` at distance 2e-62. By the
   intermediate value theorem a root `ν* ∈ (ν_lo, ν_hi)` exists. Each term of
   `C` is nonincreasing in `ν ≥ 0`, so `C(ν_hi) ≤ C(ν*) ≤ C(ν_lo)` and
   `N h* ∈ [9N/(20 C(ν_lo)), 9N/(20 C(ν_hi))]`. The table uses outward enclosures
   of `C(ν_lo)` and `C(ν_hi)`. □

Remarks.
- Uniqueness of `ν*` is not needed. Every positive root gives the same `N h*`.
- The choice `μ* = −ν* N/2` reflects the time-reversal symmetry
  `θ_j ↦ −θ_{N−j}`, which maps the feasible set to itself (by the reflection
  identity). The verifier's Newton multipliers satisfy it to all
  printed digits (e.g. N = 50: μ = −1.4100070831895082, ν·N/2 = 1.4100070831895082).
  The middle control is exactly 0. This explains the tiny middle control (about
  1e-112) in the stored primal points.
- `tan θ*_j = ν*(N/2 − j)` for interior `j`, with half-step corrections at both
  ends. This is the discrete linear-tangent law. The pair `(μ*, ν*)` is the
  discrete costate.
- Theorem 3 makes the margin `ε` unnecessary. The verified bounds `N·h2` are
  Proposition 2 at `h2 < h*`.

**What the computation checks, and what must be trusted.**
- *Verified certificate (Proposition 2):* mpmath 1.3.0 `iv` (50 digits) for
  `+ − × ÷ √` and conversions; correct reading of the OSIL (two independent
  readers agree).
- *Theorem 3 (dossier check):* the sign of `g` at two rationals and an enclosure of
  `C` at the same rationals. Arithmetic uses Python integers and `Fraction` only:
  `√q` for rational `q = p/r` is enclosed by `[m, m+1]/(r·2^600)` with
  `m = isqrt(p r 2^1200)`. mpmath only finds the numerical root. Trusted: Python
  integer arithmetic, and the model structure (asserted twice from the OSIL by
  the verifier and the primal reviewer).

### 3.2 lukvle10: partial chain Lagrangian plus 2-D interval branch and bound on an end window

**Idea in plain words.** Move all rows except the last four into the objective
with multipliers taken from the best local solution. The Lagrangian then splits
into independent 2-variable problems, one per objective pair, so its minimum is
a sum of 2-D global minima. At the right multipliers these minima reproduce the
local solution almost exactly, except at the end of the chain. There the
trajectory leaves the saddle, and the pair Lagrangians are nonconvex with
minimizers away from the local solution. Keeping the last four rows exactly
makes the last three pairs one block, a function of its 2-D entry state only. A
coercivity bound reduces each 2-D problem to a box, and interval
branch-and-bound bounds the minimum on the box.

**Theorem 4 (partial Lagrangian bound).** Let `m = 994` and `λ ∈ R^m`. Put
`λ_j = 0` for `j ∉ [0, m)` and, for `k = 0..995`,

    β_k = −λ_k + 3λ_{k−1} − 2λ_{k−2},     q_k = −2λ_{k−1}.

Define, for `a, b ∈ R`,

    ℓ_i(a,b) = F(a,b) + β_{2i} a + q_{2i} a² + β_{2i+1} b + q_{2i+1} b²,   i = 0..496,
    τ(a,b)   = F(a,b) + F(P(a,b)) + F(P²(a,b)) + β_994 a + q_994 a² + β_995 b,
    P(a,b)   = (u, Φ(b, u)),  u = Φ(a, b),   Φ(u,v) = (1 − u + 3v − 2v²)/2.

Here `β_994 = 3λ_993 − 2λ_992`, `q_994 = −2λ_993`, `β_995 = −2λ_993`,
`q_995 = 0`. Then every feasible `x` satisfies

    f(x) ≥ Σ_{j<m} λ_j + Σ_{i=0}^{496} inf ℓ_i + inf τ.

*Proof.* For feasible `x`, `c_j(x) = 0`, so `f(x) = f(x) + Σ_{j<m} λ_j c_j(x)`.
Row `j` contributes `λ_j − λ_j x_j + 3λ_j x_{j+1} − 2λ_j x_{j+2} − 2λ_j x_{j+1}²`.
Collecting by variable gives the coefficients `β_k`, `q_k`. Dualized rows reach
only up to `x_995`. The kept rows 994–997 give `(x_996, x_997) = P(x_994, x_995)`
and `(x_998, x_999) = P²(x_994, x_995)`. So `f(x) = Σλ_j + Σ_i ℓ_i(x_{2i}, x_{2i+1}) + τ(x_994, x_995)`.
Bound each term below by its infimum. □

**Lemma 5 (reduction to a box).** Let `φ(t) = t²` if `|t| ≥ 1` and 0 otherwise.
1. `F(a, b) ≥ φ(a) + φ(b)`. (For `|a| ≥ 1`, `a² ≥ 1` and the exponent
   `b² + 1 ≥ 1`, so `(a²)^{b²+1} ≥ a²`. Otherwise the term is ≥ 0.)
2. With `ψ(t) = φ(t) + q t² + β t`: `ℓ(a,b) ≥ ψ_a(a) + ψ_b(b)`. Also
   `τ(a,b) ≥ ψ_994(a) + ψ_995(b)`, because `F ≥ 0` lets us drop `F∘P` and `F∘P²`.
3. If `q > −1`, then `ψ(t) ≥ (1+q)t² − |β||t|` for `|t| ≥ 1`, and `ψ(t) ≥ −|q| − |β|`
   for `|t| < 1`. Hence `min ψ ≥ min(−|q| − |β|, −β²/(4(1+q))) =: m_ψ`.
4. Let `U ≥ ℓ(a0, b0)` for some point. If `R_a ≥ max(1, |β_a|/(2(1+q_a)))` and
   `(1+q_a)R_a² − |β_a| R_a + m_{ψ_b} > U`, then `ℓ(a, b) > U` whenever `|a| ≥ R_a`.
   The same holds with `a` and `b` exchanged. So `inf_{R²} ℓ` equals the minimum
   over `[−R_a, R_a] × [−R_b, R_b]`. The minimum is attained, by continuity and
   coercivity.

*Proof of 4.* For `|t| ≥ R ≥ |β|/(2(1+q))`, `(1+q)t² − |β||t|` is nondecreasing
in `|t|`. □

Hypotheses actually used: `q_k > −1`, i.e. `λ_j < 1/2`. The multipliers used lie
in `[0.2342, 0.4078]`, so `q ∈ [−0.8156, −0.4684]` (dossier check). The authors'
radius routine also assumes `q ≤ 0` (concave inner piece), which holds; the
verifier's routine uses the sign-free bound of item 3.

**Multipliers.** Any `λ` gives a valid bound. The verifier computed least-squares
KKT multipliers at MINLPLib p5 (residual 4.6e-14), in binary64. It replaced
`λ_30..λ_960` (spread 2.4e-14) by `λ_495 = 0.4077978179563417`. This makes 464
middle pair problems identical (`β = 0`, `q = −2λ̄`), leaving 33 other pair
problems and the tail: 34 pair groups plus `τ`. On the saddle, stationarity of
`ℓ` at `(−1/√2, −1/√2)` gives `λ̄ = (3 − ln 2)/(4√2) = 0.4077978179563422…`. The
binary64 value differs by 5.6e-16 (dossier remark; not used in the proof).

**Computer-assisted step** (verifier, R/reviews/open-instances-verification/v_lukvle10_bnb.py):
for each of the 35 problems, a best-first 2-D interval branch and bound on the
box of Lemma 5:
- *Arithmetic:* `mpmath.iv` with 64-bit mantissa and outward rounding.
  Multipliers enter as exact binary64 intervals.
- *Enclosure of F:* `base^e` with `base = a² ≥ 0` and `e = b² + 1 ≥ 1`. The
  range uses monotonicity: increasing in the base, and increasing in `e` if
  `base ≥ 1`, decreasing otherwise. The endpoint powers are
  `exp(e·log(base))` in intervals.
- *Box lower bound:* the maximum of the natural enclosure and the mean-value
  form `ℓ(c) + ∇ℓ(X)·(X − c)`. The interval gradient comes from forward-mode
  differentiation, through `P` and `P²` for `τ`. It is used only when no
  argument interval of `F` contains 0. `F` is C¹ on `R²` (exponent ≥ 2 in
  `|a|`), so the mean-value form is valid wherever the gradient formula is.
- *Incumbent:* the interval upper end of `ℓ` at box centres.
- *Pruning and stopping:* boxes with lower bound above the incumbent are
  discarded. The search stops when the incumbent minus the smallest open lower
  bound is at most 1e-12 (pairs) or 1e-9 (tail). The returned value is the
  smallest open lower bound. A box holding a minimizer has lower bound
  ≤ min ≤ incumbent, so it is never discarded.
- *Summation:* `Σλ_j` and the group lower bounds (logged to 20 digits, each
  reduced by 1e-18) are summed in intervals.

Results (R/reviews/open-instances-verification/logs/lukvle10_bnb.json):
- pair groups: 2,255–9,471 boxes each; largest `UB − LB` 1.0e-12;
- middle group: radius 3.0426, LB −0.10848885472697348, UB −0.1084888547261358;
- tail: box [−4.989, 4.989] × [−2.279, 2.279], 92,551 boxes (605 open),
  LB 1.1740123815542916, UB 1.1740123825517311;
- `Σλ = 405.03299763692109328`;
- certified lower end 352.23802540507845565 (64-bit `iv`, reproduced by the
  dossier check); safe display **352.2380254050784**.

Runtime: 300.35 s on one process (R/publication/reproduction/README.md).

**What must be trusted.** mpmath 1.3.0 `iv` (`+ − × ÷`, even integer power,
`exp`, `log`, conversions); the verifier's B&B code; the OSIL reading (two
independent readers). The authors' independent code (`R/open-instances/lukvle10_bound.py`,
30-digit `iv`, its own multipliers) certifies 352.238025369202, consistent with
the verifier's value. Both certificates share mpmath's `exp`/`log`. The B&B leaves
are not saved, so a re-check means rerunning the search.

## 4. Exactly feasible primal points

### lnts (R/publication/primal/lnts/report.md; points in `points/lnts<N>_point.json`)
- **Construction.** `θ_1..θ_{N−1}` are fixed to 40-digit decimal rationals, rounded
  from the tangent law. Given `(θ, h)`, the recursion defines all states and
  satisfies all 4N rows exactly. The three terminal conditions reduce to
  `F(z) = (vx_N − 45, vy_N, py_N − 5) = 0` in `z = (θ_0, θ_N, h)`. A Krawczyk
  test on a stored decimal box (radius 1e-50 for the angles, 1e-52 for `h`)
  proves a unique zero `z*`. The authors' test uses 110-digit mpmath `iv`.
- **Objective enclosures** (25 digits): [0.5546687649386788986220922, …923],
  [0.5545954011669111610017828, …829], [0.5545770161030836720556252, …253],
  [0.5545724137006871088173911, …912].
- **Review.** Independent review r1 reran Krawczyk with its own code, both in
  mpmath and mpmath-free (integers, `Fraction`, alternating-series bounds for
  sin and cos). It found one invalid second Krawczyk step (since corrected) and
  no effect on the 25-digit enclosures.
- **No rational feasible point exists** (Lindemann–Weierstrass argument in the
  primal report and r1). An existence proof is therefore necessary.
- **Alternative (dossier).** Theorem 3 gives an exactly feasible point that attains
  the optimum. Its feasibility is pure algebra once a root `ν*` exists, and the
  root exists by the intermediate value theorem. The dossier check finds the
  stored points' objectives within 7e-26 of the optimum, consistent with their
  rounded interior controls.

### lukvle10 (R/publication/primal/dtoc5-lukvle10/report.md)
- **Construction.** Seeds `x_0, x_1` are the KKT values rounded to 640 decimals
  (`points/lukvle10_seed.txt`). All other coordinates are defined by the rows,
  so `x*` is rational and satisfies all 998 rows exactly. Its exact rationals
  are too large to store, because the denominator at least squares at every
  step.
- **Enclosure.** Coordinates enclosed in mpmath `iv` at 750 digits (maximum radius
  8.0e-265); `min |x_k| = 0.26003`. The saved box has radius ≤ 5e-61.
- **Objective.** `f(x*) ∈ [352.2380254064956226308712710293664647979978, …979]`.
- **Second implementations.** The author wrote an integer-only fixed-point version
  (atanh-series log, halving-plus-Taylor exp). Independent review r1 used an
  integer-only route too (`check_lukvle10.py` at 3400 bits and
  `objective_noniv_lukvle10.py`). Both give the same enclosure, so the primal
  side does not depend on mpmath.
- **Seed sensitivity** (numerical illustration). p5's 15-digit seeds leave
  `|x| ≤ 10` at index 40. Seeds with 50–420 correct decimals give objectives
  352.89–353.00. About 440–460 decimals are needed to reach the KKT value.
- `x*` agrees with a numerical KKT point to about 205 digits (stationarity
  residual 1.4e-205). This is numerical evidence of local stationarity only.

## 5. Numbers table

Display conventions: duals rounded down, primals rounded up, gaps rounded up.

| instance | listed best dual | our dual (safe display) | our primal (safe display) | gap (rounded up) | sources |
|---|---|---|---|---|---|
| lnts50 | 0.55464755 | 0.5546687649381 | 0.5546687649387 | ≤ 5.79e-13 (1.05e-12 rel.) | dual: verifier `logs/lnts_verify.json` cert_1e-12 (N·h2 = 0.55466876493812422…); primal: `primal/lnts/points/lnts50_point.json` objective_enclosure; gap: `publication/integration/gap-values.json` |
| lnts100 | 0.55299042 | 0.5545954011663 | 0.5545954011670 | ≤ 6.12e-13 (1.11e-12 rel.) | same files |
| lnts200 | 0.55219867 | 0.5545770161025 | 0.5545770161031 | ≤ 5.84e-13 (1.06e-12 rel.) | same files |
| lnts400 | 0.55204395 | 0.5545724137001 | 0.5545724137007 | ≤ 5.88e-13 (1.06e-12 rel.) | same files |
| lukvle10 | 351.223393 | 352.2380254050784 | 352.2380254064961 (summary; p5 display) — exact point: 352.2380254064957 | ≤ 1.5e-9 (exact upper bound 1.4172e-9; 4.03e-12 rel.) | dual: verifier `logs/lukvle10_bnb.json`; primal: `primal/dtoc5-lukvle10/logs/lukvle10_enclose.json`; gap: `gap-values.json` |

Against the certified verifier values `N·h2` (rather than the 13-digit displays),
the lnts gaps are at most 5.55e-13. All displays agree with
R/open-instances-summary.md. Disagreements with other documents are recorded in
Section 8.4.

If Theorem 3 is adopted after review, the lnts rows become:

| instance | optimum (rounded down / up) | gap |
|---|---|---|
| lnts50 | 0.5546687649386788 / 0.5546687649386789 | 0 (attained; enclosure width 5.7e-62) |
| lnts100 | 0.5545954011669111 / 0.5545954011669112 | 0 (width 1.2e-61) |
| lnts200 | 0.5545770161030836 / 0.5545770161030837 | 0 (width 2.3e-61) |
| lnts400 | 0.5545724137006871 / 0.5545724137006872 | 0 (width 4.6e-61) |

Historical values that must not be quoted as bounds: the author's lnts values at
margin 1e-10 (e.g. 0.554668764883212; some were rounded to nearest above
`N·h2`), the verifier's 16-digit lnts100/lnts200 displays (rounded to nearest,
above `N·h2`), the author's lukvle10 bound 352.238025369202 with gap 3.7e-8
(valid but superseded), and 352.2380254050785 (above the certified end).

## 6. Verification record

| check | by | what was checked | verdict / result | remaining assumptions |
|---|---|---|---|---|
| lnts dual, author | `R/open-instances/lnts_bound.py` | Prop. 2 at ε = 1e-10 in mpmath `iv` (60 digits) | margins −8.6e-9 … −6.9e-8 | mpmath iv |
| lnts dual, independent | `R/reviews/open-instances-verification/v_lnts.py`, report §3 | own OSIL reader (decimal strings), exact-rational check of the summation identities, own Newton, Prop. 2 at ε = 1e-10 and 1e-12 in `iv` (50 digits) | verified | mpmath iv (`√`, rational ops) |
| lnts float recheck | author, `verify_independent.py` | cvxpy convex relaxation infeasible at h2(1−1e-5), feasible at h2(1+1e-5) | supporting only; not rechecked | floating point |
| lnts primal, author | `R/publication/primal/lnts/` | Krawczyk existence (110 digits), crosscheck with the verifier's reader and closed-form Jacobian, mutation tests | proved under mpmath-iv assumption | mpmath iv |
| lnts primal, independent r1 | `R/publication/reviews/primal-lnts-review-r1.md` | own generic elimination to a 3×3 system, own Krawczyk in mpmath and mpmath-free, all rows/bounds, gaps | verified; 5 minor issues, all resolved | Python integers, Taylor remainder bound |
| lnts exact optimum | this dossier, `checks/lnts-lukvle10/lnts_exact_opt.py` | Theorem 3: closed form of `c`, reflection identity, recursion identity, sign change of `g`, enclosure of `N h*`; negative test | passes for all four N | Python integers; **not independently reviewed** |
| lukvle10 dual, author | `R/open-instances/lukvle10_bound.py` | Theorem 4 + Lemma 5 + own B&B (30-digit iv, mpmath power) | 352.238025369202 | mpmath iv |
| lukvle10 dual, independent | `v_lukvle10_prep.py`, `v_lukvle10_bnb.py`, report §7 | own multipliers, own radii, own B&B with monotone power ranges, own forward-mode gradients | verified, 352.2380254050785 (nearest display) | mpmath iv `exp`/`log` (shared with the author) |
| lukvle10 float sanity | both | grid 1501² (author) and 1201² (verifier) plus local search on each problem | no sample below its LB (smallest margins 9.8e-12 and 8.4e-13) | evidence only |
| lukvle10 primal, author | `R/publication/primal/dtoc5-lukvle10/` | seed-defined exact point, mpmath and integer-only enclosures | proved | Python integers (second route) |
| lukvle10 primal, independent r1 | `R/publication/reviews/primal-dtoc5-lukvle10-review-r1.md` | own reader, own integer fixed-point enclosure, integer-only log/exp, gaps | verified; 4 minor issues, resolved | Python integers |
| displays and gaps | `R/publication/reviews/minor-fixes-review-r1.md`, `-r2.md`, `integration-review-r1.md`, `-r2.md` | exact recomputation of every gap cell and display direction | corrected lnts100 primal and lnts gap displays; all now valid | — |
| sum recomputation | this dossier, `lukvle10_sum.py` | exact sum of the verifier's logged LBs and `Σλ` | 352.2380254050784557… ≥ display | logged LBs |
| replay | `R/publication/reproduction/README.md` | reviewer commands rerun | 1.58 s (lnts, all four); 0.64 + 300.35 s (lukvle10) | — |

Not rechecked by anyone: the author's lukvle10 full-Lagrangian estimate 352.152
(floating point) and the cvxpy lnts recheck.

## 7. Relation to prior work

**lnts.**
- Local values: COPS 2.0 Table 9.2 gives MINOS values 0.554668, 0.554595, 0.554577
  and 0.554572 (agreeing with our optima to the printed digits). LANCELOT's
  lnts100/lnts400 values lie below our optima (tolerance artifacts); COPS 3.0 has
  0.554577 (nh=200) and 0.554572 (nh=400). R/publication/literature/control/report.md
  §"lnts50/100/200/400".
- Floating-point global results: Göß–Burlacu–Martin, JOGO 94 (2026) 951–996
  [[go2026-parabolic-approximation-relaxation-for-minlp]]. Their Table 17
  (p.42 of the extracted text, journal p. 992) reports that Gurobi solved the
  original lnts50 in 5811.5 s and lnts100–400 hit the 4 h limit. Their Table 11
  (p.22, journal p. 972) gives SCIP time-limit gaps of 0.0251–0.1033. Göß,
  arXiv:2603.16505v1, App. B Table 4 (p. 32; not in literature/, copy in
  R/publication/literature/control/sources/) prints PARA dual-bound gaps of
  0.00% (lnts50/100/200, i.e. below 0.005%) and 0.01% (lnts400). These are
  floating-point results with numerically validated under-estimators.
- MINLPLib GUROBI bounds (2025) are within 3.8e-5 relative (lnts50) and
  0.29–0.46% (lnts100–400).
- Our one-hour campaign (GAMS 54.3.1; R/publication/solver-runs/results_table.md):
  GUROBI duals 0.55464686, 0.55189322, 0.55226583, 0.55088569; SCIP duals
  0.5078–0.5451; BARON rejects sin/cos. GUROBI's returned lnts50 and lnts100
  points and SCIP's lnts100 point lie below the certified optimum
  (tolerance artifacts).
- Mechanism: the linear-tangent law is classical (Bryson–Ho 1975, cited, not
  read). Our use is a discrete Lagrangian sufficiency argument (an Arrow-type
  argument: the maximized Hamiltonian is affine in the state for fixed `h`; see
  R/theory-calibration/scouting.md lines 479–486 and R/theory-consistency/consistency-relaxations.md
  §5.1). The literature track found no rigorous certificate.

**lukvle10.**
- No prior global result found. LV TR V-767 gives no values. LUKVLE10.SIF lists
  `*LO SOLTN 3.52237E+02`, which is 1.0e-3 below our certified bound. It matches a
  1e-6-feasible IPOPT point (tolerance artifact; origin inferred, not documented).
  MINLPLib points p1–p5 (2017–2022) are local. Listed bounds come from SCIP
  (351.223), LINDO (2.11), BARON (0.051), COUENNE and ANTIGONE. The SCIP 8 suite
  report shows an infinite gap.
- Our campaign: BARON dual 0.0117 at the time limit, GUROBI rejects the model
  (error 10024, POW with two variable arguments), SCIP dual 347.65 for a slightly
  tightened model.
- Mechanisms: partial Lagrangian relaxation is standard. Interval B&B with
  natural and mean-value enclosures follows the Moore–Skelboe tradition
  [[neumaier2004-complete-search-in-continuous-global]] p.4, p.31. The Krawczyk
  operator used for the lnts primal points is described in the same survey
  (p.31). Neumaier–Shcherbina [[neumaier2004-safe-bounds-in-linear-and]] p.1
  motivate rigorous arithmetic.

## 8. Critical examination

### 8.1 lnts: re-derivation and the exact-optimum strengthening

- **L1. Proposition 2 is correct.** I re-derived it independently: the sign
  conditions (`ν ≥ 0`), monotonicity of `A + νB`, the exclusion of `h = 0`, and
  the fact that no `θ` bounds are used. Lemma 1's closed form of `c` and the
  identities hold in exact arithmetic (dossier check). The verifier's interval
  evaluation uses interval `μ, ν, h2` and therefore covers the exact 60-digit
  values. No issue.
- **L2. The margin is unnecessary (strengthening, Theorem 3).** At the exact
  multipliers, the maximizing controls are feasible, and Proposition 2 is tight.
  I proved this above and ran the computation (`lnts_exact_opt.py`, 0.6 s, one
  core). Results: sign change confirmed for all four N with `|g| ≈ 1e-58` at the
  bracket ends; optimum enclosures of width 5.6e-62 to 4.5e-61 (table in
  Section 3.1). Consistency: each stored exact primal point's objective
  enclosure lies above the lower end, at most 7e-26 above it (its interior
  controls are rounded). Every summary dual display lies below the optimum.
  Negative test: shifting the bracket by ±1e-55 makes the sign test fail
  (`lnts_negative_test.log`). **Proposed resolution:** adopt Theorem 3 as the
  lnts result. Ask an independent reviewer to recheck the proof and rerun or
  reimplement the 1-D sign check (seconds; the existing verifier scripts could
  be extended). This also removes the mpmath assumption from the lnts dual, and
  it gives a second, Krawczyk-free proof of an exactly feasible point.
- **L3. Tolerance artifact against MINLPLib.** MINLPLib p1 for lnts50 has
  objective 0.55466876489565 (h = 0.011093375297913 in `lnts50.p1.sol`), which is
  4.3e-11 below the optimum, and our dual display exceeds it by 4.2e-11. The
  summary does not mention this. For lnts100–400 only 7–8-digit page displays
  were saved, so the comparison is open. **Resolution:** state it in the paper
  like the camshape400/800 note. Optionally download the three p1 `.sol` files
  and read `N·h` (seconds; files are re-downloadable and git-ignored).
- **L4. Author float rounding.** `lnts_bound.py` reports `float(lower end)` with
  round-to-nearest. Its 1e-10-margin values can exceed `N·h2` by half an ulp
  (the minor-fixes review measured 2.96e-17 and 3.26e-17 for lnts200/400). These
  values are superseded; never quote them as bounds.

### 8.2 lukvle10: re-derivation

- **L5. Theorem 4 and Lemma 5 are correct.** I re-derived the coefficients,
  including the tail entries `β_994 = 3λ_993 − 2λ_992`, `q_994 = −2λ_993`,
  `β_995 = −2λ_993`, `q_995 = 0`, and checked that the verifier's code uses the
  same `λ` for the pair coefficients and for `Σλ` (both after replacement). This
  matters: a mismatch would invalidate the bound. Head pairs `i ≤ 496` use
  `(λ_{2i−2}, …, λ_{2i+1})`; the grouping key is these four numbers.
- **L6. Hidden hypotheses, now stated.**
  1. `q_k > −1` (holds: `q ∈ [−0.8156, −0.4684]`).
  2. The authors' radius routine evaluates the inner piece of `ψ` only at
     `t = ±1`. This assumes `q ≤ 0`, which holds because every `λ_j > 0`.
  3. The verifier's radius check rounds `max|β|` to binary64 by round-to-nearest.
     The "+1" safety term in `U + 1` absorbs this error (at most about 1e-15).
  4. The B&B's centre point lies in the box (binary midpoint), so the mean-value
     form is valid.

  None of these is a defect, but the paper should state hypotheses 1–2 and use
  the sign-free bound of Lemma 5(3). I also tested mpmath's interval power on
  bases containing 0 (used in the authors' code): `[0,0.25]^[1,1.5] = [0, 0.25]`,
  `[0,4]^[1,2] = [0,16]`, `[−0.5,0.5]^2 = [0, 0.25]`, all correct.
- **L7. Sum and display.** My exact recomputation from the logged LBs gives
  352.2380254050784557…, and a 64-bit `iv` replay of the verifier's summation
  gives the lower end 352.23802540507845565. The summary display
  352.2380254050784 is valid, with a 5.6e-14 margin. The verification report's
  "352.2380254050785" (`mpmath.nstr`, nearest) exceeds the lower end by 4.4e-14
  and is **not** a valid lower bound as displayed. **Resolution:** the paper uses
  352.2380254050784; mention it if the verification report is cited.
- **L8. The gap is entirely B&B tolerance.** Pair `UB − LB` sums to 4.197e-10 and
  the tail to 9.974e-10, total 1.417e-9, which equals the gap to `x*`. The sum of
  B&B upper ends plus `Σλ` is 352.23802540649562278, only 1.5e-19 above `f(x*)`.
  This is strong numerical evidence that, at these multipliers, the partial
  Lagrangian dual value equals `f(x*)` to about 1e-19. It is **not a proof** of
  zero duality gap or of global optimality of `x*`. The open-instances report
  §7.5 sentence "the partial Lagrangian has no duality gap at these
  multipliers" overstates this.
- **L9. Removing the KKT caveat (proposed computation).** For each of the 35
  problems:
  1. enclose the stationary point near the KKT pair by a Krawczyk test on
     `∇ℓ = 0` (2×2; for `τ` through `P`, `P²`);
  2. prove `∇²ℓ` positive definite on a small box `B_r` around it (radius about
     1e-4, interval Hessian);
  3. rerun the existing B&B on the big box minus `B_r` with target "lower bound
     > value at the stationary point". Near `∂B_r` the excess is about `κr²/2`,
     where `κ` is the smallest Hessian eigenvalue. For the middle pair problem
     the Hessian at the saddle pair has eigenvalues 2.35 and 2.57 (dossier,
     numerical), so the excess is about 1e-8 at `r = 1e-4`. The mean-value form
     then needs boxes of width about `r/2` near `∂B_r`, a much coarser search
     than the present 1e-12 run.

  The middle group has four symmetric minimizers (`β = 0`, `ℓ` even in each
  variable); treat them by symmetry. The result is `Σλ + Σ min ℓ_i + min τ`, the
  dual value itself, enclosed to about 1e-50. It differs from `f(x*)` only by the
  second-order effect of the multiplier perturbation (about `|δλ|²`, with
  `|δλ| ≤ 2.4e-14`), so the gap would probably fall to about 1e-25 and `x*` would
  be proved globally optimal to that accuracy. If some pair problem has a second
  global minimizer, step 3 fails visibly, and the existing 1.42e-9 bound stays
  valid. Cost: about one person-day to implement on top of `v_lukvle10_bnb.py`,
  under 15 CPU minutes on one core, plus an independent review. Optional; the
  paper can stand on the current gap.
- **L10. mpmath dependency of the dual.** Both independent certificates use
  mpmath `iv` `exp`/`log`, and the B&B leaves were not saved. **Proposed
  computation:** rerun the verifier's B&B, dumping each leaf (box and lower
  bound), then re-bound every leaf with the integer-only `exp`/`log` already
  written for the primal (author's `lukvle10_crosscheck.py` or reviewer r1's
  `objective_noniv_lukvle10.py`). About 3×10^5 leaves at about 2–4 ms each:
  roughly 15–30 CPU minutes plus the 5-minute rerun, on one core. This would
  remove the mpmath assumption. Otherwise state it explicitly in the paper
  (assumption: mpmath 1.3.0 `iv` encloses `exp`, `log`, and the arithmetic
  operations correctly).
- **L11. The 352.152 estimate** (all rows dualized) is a floating-point grid
  estimate that nobody rechecked. It motivates the end window. Label it as a
  floating-point estimate or drop the number.
- **L12. Why the window is 2-D and short.** There are no controls. The window's
  entry state `(x_994, x_995)` determines its interior through `P`. Three pairs
  were enough because the transient is short. A longer window would remain 2-D,
  but its enclosures would widen by about 2.73 per step. This is a structural
  explanation, not a gap.

### 8.3 Primal-side checks

- lnts primal points: proved twice, including mpmath-free, after the second-step
  fix. Theorem 3 gives a third, independent existence argument (IVT). No issue.
- lukvle10 primal point: proved with integer-only arithmetic by the author and by
  r1. The OSIL `power` semantics with positive base is the only modelling
  assumption; all `|x_k| ≥ 0.26`.

### 8.4 Inconsistencies between documents (all minor; no number in the summary is wrong)

| place | statement | problem | resolution |
|---|---|---|---|
| summary, lukvle10 row | primal 352.2380254064961 with "exact primal verified" | This is p5's displayed value. It is a valid upper bound but not the exact point's value (`f(x*)` ≤ 352.2380254064956226…). | Display 352.2380254064957 and gap ≤ 1.42e-9 in the paper. |
| verification-report §1, §7 | lukvle10 dual 352.2380254050785 | rounded to nearest, 4.4e-14 above the certified end | Use 352.2380254050784. |
| reproduction/README.md lines 95–98, 113 | lnts100 primal "0.5545954011669"; "the summary's 5.5e-13 gaps" | The first is below the exact point objective (summary now 0.5545954011670); the second is stale (now 5.79e-13 … 6.12e-13, or ≤ 5.55e-13 against `N·h2`). | Cite the summary and gap-values.json, not the README. |
| open-instances-report §1, §3.4, §7.5 | 1e-10-margin lnts duals; lukvle10 352.238025369202 and gap 3.7e-8; "no duality gap" | superseded or overstated | Use the summary; reword the duality-gap sentence (L8). |
| summary, lnts rows | no tolerance remark | our lnts50 dual exceeds MINLPLib p1's objective | Add a remark (L3). |

### 8.5 Does anything invalidate a claimed result?

No. I found no error in any proof, bound, primal point or gap. The issues are
display and wording issues, one unproved statement that the summary already
qualifies (lukvle10 KKT optimality), one dependency (mpmath for the lukvle10
dual), and one strengthening opportunity (lnts exact optimum).

## 9. What the paper may claim and must not claim

**May claim** (current evidence):
- "For lnts50, lnts100, lnts200 and lnts400 we prove dual bounds within
  5.79e-13, 6.12e-13, 5.84e-13 and 5.88e-13 (absolute) of exactly feasible
  points. The bounds are certified in interval arithmetic and were verified
  independently."
- After independent review of Theorem 3: "We determine the optimal value of
  lntsN exactly: it equals `N·h*`, where `h*` is defined by a scalar equation,
  and it is attained by the discrete linear-tangent control. We enclose it in an
  interval of width below 1e-60 using integer arithmetic only."
- "For lukvle10 we prove the lower bound 352.2380254050784 and exhibit an exactly
  feasible point with objective in [352.23802540649562263, 352.23802540649562264].
  The remaining gap is at most 1.42e-9 (4.03e-12 relative). The dual side assumes
  that mpmath's interval exp and log are correct."
- "To the best of our knowledge these are the first rigorous global certificates
  for these five instances. For lnts the optimal values were known to high
  accuracy from local solvers (COPS), and floating-point global solvers had
  essentially closed lnts50 (Gurobi, to its default tolerance; Göß–Burlacu–Martin
  2026) and printed gaps of 0.00–0.01% for lnts100–400 (Göß 2026). For lukvle10
  we found no prior global result; the CUTEst SOLTN value 352.237 lies 1.0e-3
  below our certified bound."
- "MINLPLib's lnts50 point p1 (objective 0.55466876489565, row violation
  9.1e-10) lies 4.2e-11 below our certified dual bound; it is feasible only
  within MINLPLib's tolerance." (After Theorem 3 is reviewed: "4.3e-11 below
  the optimum".)
- Mechanism wording: "a Lagrangian relaxation of the dynamics with the discrete
  costate as multipliers (for lnts, after exact elimination of the linear
  dynamics, three multipliers suffice), plus monotonicity in the global step
  `h`"; and for lukvle10, "a partial Lagrangian whose 497 two-variable
  subproblems and one 2-D end window are bounded by interval branch and bound".

**Must not claim:**
- that lukvle10 is solved exactly, that `x*` is globally optimal, or that the
  partial Lagrangian has zero duality gap (unless L9 is carried out);
- that the lnts optimum is in closed form. It is defined by a scalar equation
  (Theorem 3) or certified to 5.8e-13 (current);
- 352.2380254050785, 352.238025369202, the 1e-10-margin lnts values or the
  verifier's 16-digit lnts100/lnts200 displays as dual bounds;
- that the lukvle10 dual is independent of mpmath (only the primal is);
- new mechanisms: the linear-tangent law, Lagrangian relaxation and interval
  B&B are classical. The contribution is the rigorous certificates and the
  exact-feasibility treatment;
- a large improvement for lnts50. The listed GUROBI bound was already within
  3.8e-5 relative, so the improvement there is marginal;
- that MINLPLib's lnts50 primal is wrong: it is correct within MINLPLib's
  tolerance.

## 10. Candidate figures and tables

1. **Table (main text):** the numbers table of Section 5, with listed dual,
   certified dual, exact primal and gap. If Theorem 3 is adopted, add an
   "optimum" column.
2. **Figure: lnts optimal controls.** `θ*_j` against `t_j = j h*` for N = 50 and
   400, with `tan θ*` linear in `t` and the half-step end corrections; inset with
   the multipliers `μ* = −ν*N/2`. Data: Theorem 3, cheap to generate.
3. **Figure or small table: lnts optimum against N.** The optima decrease as
   `O(N^{−2})`: successive differences 7.34e-5, 1.84e-5, 4.60e-6 (ratios 3.990,
   3.995). Richardson extrapolation from N = 200, 400 gives 0.55457088. This
   illustrates that the discrete optima differ from the continuous one, so
   continuous theory cannot certify them.
4. **Figure: lukvle10 trajectory.** `x_k` for `x*`, k = 0..999, with the saddle
   level `−1/√2` and the end transients; mark the dualized region and the
   three-pair exact window `x_994..x_999`.
5. **Figure: lukvle10 window search.** The B&B leaf boxes over
   `(x_994, x_995)`, coloured by lower bound. This needs a rerun with leaf dump
   (5 CPU minutes; could be combined with L10).
6. **Table (appendix):** per-problem B&B statistics for lukvle10 (radii, boxes,
   LB, UB, tolerance), from `lukvle10_bnb.json`.
7. **Table (appendix):** verification matrix of Section 6.

## Appendix A. Commands run for this dossier

All runs used a scratch directory, one core, and inputs copied there.
Scripts and logs are saved in `paper-open-minlplib/development/dossiers/checks/lnts-lukvle10/`.

- `mkdir /tmp/dossier-lnts`; copied
  `R/reviews/open-instances-verification/logs/{lukvle10_bnb.json,lukvle10_lam_kkt.npy,lukvle10_prep.json,lnts_verify.json,lukvle10_x5.npy}`,
  `R/publication/primal/dtoc5-lukvle10/logs/{lukvle10_enclose.json,gaps.json,lukvle10_kkt.json}`,
  and `R/publication/primal/lnts/points/lnts{50,100,200,400}_point.json`.
- `OMP_NUM_THREADS=1 python3 lnts_exact_opt.py 50 100 200 400` → all four sign
  changes proved; enclosures in Section 3.1; 0.6 s (`lnts_exact_opt.log`, `.json`).
- Negative test (inline, saved as `lnts_negative_test.log`): bracket shift ±1e-55 → sign test fails for N = 50 and 400.
- `python3 lukvle10_sum.py` → exact sum 352.2380254050784557017…; display ...784 valid, ...785 not; tolerance accounting 4.197e-10 + 9.974e-10 (`lukvle10_sum.log`).
- Inline mpmath (64-bit `iv`) replay of the verifier's summation → lower end 352.23802540507845565.
- Inline mpmath tests of interval power on bases containing 0 (Section 8.2, L6).
- Inline mpmath: `λ̄` closed form, middle-pair value at the saddle
  (−0.1084888547261358344 with the binary64 `λ̄`, equal to the verifier's UB),
  numerical Hessian eigenvalues of the middle pair problem at the saddle pair
  (2.3487, 2.5734), and the lnts Richardson numbers.
- Read-only inspection of `R/open-instances/minlplib_sol/lnts50.p1.sol` (h = 0.011093375297913).

No project-wide checks, solver runs or long computations were run. Nothing under
R/ or literature/ was modified.
