# Dossier: chain50–400 and catmix100–800 (family key `chain-catmix`)

Prepared 2026-10-04 for the Mathematical Programming Computation paper
(second pass; it replaces the first-pass draft of the same day). `R/` means
`research-20260929/`. Unless a statement is marked **(this dossier)**,
numbers come from the authoritative summary (`R/open-instances-summary.md`),
the integration gap file (`R/publication/integration/gap-values.json`) and
the exact display record
(`R/publication/reproduction/cops/logs/exact_display_checks.json`).

Checks made for this dossier are in
`paper-open-minlplib/development/dossiers/chain-catmix-checks/`. The
first-pass scripts and logs are at the top level; this pass's are in `r2/`
(Section 8.2). All of them ran on copies under `/tmp`, one thread at a time.

Status words:
- **proved**: a complete proof is given here. Proofs marked *new* have not yet had an independent read.
- **verified computation**: a computer-assisted step with directed rounding, implemented independently at least twice, with the stated trust base.
- **numerical**: floating-point evidence only.

## 0. At a glance

| | chain50/100/200/400 | catmix100/200/400/800 |
|---|---|---|
| source | COPS 2.0 problem 3, hanging chain (GAMS model library `chain`, SEQ=231) | COPS 2.0 problem 14, catalyst mixing (GAMS model library `catmix`, SEQ=242) |
| MINLPLib type | NLP, nonconvex; 2N+2 variables, N+1 equality rows | QCP (bilinear equality rows), nonconvex; 3N+3 variables, 2N rows |
| MINLPLib status | not solved; best page dual 0.0826–0.1745 (ANTIGONE); optimum ≈ 5.07 | not solved; best page dual −0.0666 to −1.489 (LINDO); optimum ≈ −0.048 |
| our optimum enclosure | width ≤ 1.01e-14 absolute (≤ 1.99e-15 relative) | width ≤ 1.85e-13 / 1.90e-11 / 6.81e-11 / 1.49e-10 absolute |
| dual mechanism | closed-form discrete catenary calibration (proved), which reduces the problem exactly to two end values; 2-D interval branch and bound over those | exact reduction to a 1-D projective state; DP lower bound by chord interpolation of the concave, homogeneous value functions; rigorous 1-D minimization per ray and stage |
| arithmetic of the computer-assisted step | mpmath `iv` (30 and 40 digits; uses sqrt and log) | IEEE binary64 plus one `nextafter` step outward per operation; only + − × ÷ |
| primal side | exactly feasible point with coordinates in Q(√R_N); objective enclosed to 40 decimals with integer arithmetic | binary64 controls and exact rational states; exact rational objective |
| status | lemma and reduction proved; window computation verified (two codes) | DP principle proved; computation verified (two codes). The strongest values come from one code, which agrees per stage with the second (Section 3.2) |

## 1. Instances and models

### 1.1 chain (hanging chain)

**Physical problem.** A chain of uniform density and length 4 hangs between
(0, 1) and (1, 3). Its shape x(t) minimizes the potential energy
∫₀¹ x√(1+x′²) dt subject to ∫₀¹ √(1+x′²) dt = 4. Source: Cesari 1983,
pp. 126–127, via COPS 2.0 §3 (problem suggested by Mittelmann). COPS writes
it as a control problem with u = x′ and discretizes the ODE and both
integrals with the trapezoidal rule on N intervals.

**Model (MINLPLib chainN, N = 50, 100, 200, 400).** Let h = 1/N and η = h/2.
All variables x_0..x_N, u_0..u_N are continuous.

    minimize    f(x,u) = η Σ_{i=0}^{N−1} ( x_i √(1+u_i²) + x_{i+1} √(1+u_{i+1}²) )
    subject to  x_{i+1} − x_i − η(u_i + u_{i+1}) = 0,        i = 0..N−1,
                η Σ_{i=0}^{N−1} ( √(1+u_i²) + √(1+u_{i+1}²) ) = 4,
                x_0 = 1,  x_N = 3;  all other variables free (no bounds).

- **Sizes.** 102/202/402/802 variables; 51/101/201/401 rows (N linear equalities plus one nonlinear equality).
- **OSIL facts.** η is the exact decimal 1e-2, 5e-3, 2.5e-3, 1.25e-3; the objective constant is 0. sha256 prefixes f6b2b409 (50), 45cb3020 (100), 634acc62 (200), 7cd93486 (400). The files were unchanged on minlplib.org at the 2026-10-02 refresh.
- **GAMS = OSIL.** The `.gms` and OSIL forms have identical coefficients (`R/publication/minlplib-status/report.md`: only catmix, methanol50 and lop97icx differ).
- **Same as COPS 2.0.** `chain.gms` is COPS 2.0 #3. COPS 3.0 §4 is an equivalent reformulation with auxiliary states (`R/publication/literature/control/report.md` §3; GAMS source text in `literature/papers/library2026-cops-and-gams-source-models`).

**Structure that matters.**
- **No bounds.** All interior variables are free, so spatial branch and bound starts from no box. The listed duals are 0.08–0.17 (ANTIGONE) and −33 to −862 for the other listed solvers. Our one-hour runs ended at −36 to −1673.
- **Polyline form.** The linear rows are an exact reparametrization of the chain as a polyline over a fixed horizontal mesh (Lemma C1). After it, only the two "end values" z_1, z_N couple the end pieces to the interior.
- **Reverse-convex length row.** A fixed-multiplier Lagrangian of the length row reaches at most about 4.77 against the optimum 5.07 (grid estimate, `R/open-instances-wave2/cops/report.md` §2, "What failed").

### 1.2 catmix (catalyst mixing)

**Physical problem.** The catalyst mixing problem of Gunn and Thomas, via
von Stryk's DIRCOL guide and COPS 2.0 §14. A tubular plug-flow reactor holds
two catalysts; u(t) ∈ [0, 1] is the fraction of catalyst 1 at position t.
Catalyst 1 drives A ⇌ B and catalyst 2 drives B → C:

    x₁′ = u(10x₂ − x₁),   x₂′ = u(x₁ − 10x₂) − (1 − u)x₂,   x(0) = (1, 0).

The goal is to maximize the yield 1 − x₁(1) − x₂(1) of C. The objective
−1 + x₁(1) + x₂(1) is minus the yield, about −0.048. The continuous problem
is bang–singular–bang (COPS 2.0 §14).

**Model (MINLPLib catmixN, N = 100, 200, 400, 800).** Let a = 1/(2N), b = 10a,
e₊ = 1 + a, e₋ = 1 − a, and c = c_N (Section 1.3). Define

    P(u) = [[1 + a u,  −b u], [−a u,  e₊ + c u]],   Q(u) = [[1 − a u,  b u], [a u,  e₋ − c u]].

All variables u_0..u_N ∈ [0, 1] and x_i = (x1_i, x2_i) ∈ ℝ² (i = 0..N) are
continuous:

    minimize    J = x1_N + x2_N − 1        (the −1 is the OSIL objective constant)
    subject to  P(u_{i+1}) x_{i+1} = Q(u_i) x_i,   i = 0..N−1    (2N bilinear equality rows),
                x1_0 = 1,  x2_0 = 0;  all other states free.

- **Sizes.** 303/603/1203/2403 variables; 200/400/800/1600 rows.
- **OSIL facts.** sha256 prefixes 9f5b5bae (100), 9194135d (200), 3dfc4d7f (400), 40b572a4 (800).
- **Exact row check (this dossier).** An xml.etree reading confirms the full quadratic-term pattern, all 400/800/1600/3200 linear coefficients (−1, 1, −(1−a), 1+a), the bounds and the objective constant −1, all in exact rationals (`r2/lin_check.log`, `r2/exact_catmix.log`).

**Structure that matters.**
- **States follow from controls.** det P(u) ≥ 1 + a > 0 on [0, 1], so the states are functions of the controls (Lemma M1).
- **Homogeneity and positivity.** The dynamics are linear and homogeneous in the state, and every stage map is entrywise nonnegative. So the value functions are concave and positively homogeneous on the positive quadrant, and the 2-D state reduces to a 1-D ray θ = y₂/(y₁ + y₂).
- **Q = 2I − P.** e₊ + e₋ = 2 exactly, so Q = 2I − P and M := QP⁻¹ = 2P⁻¹ − I.
- **Shape of the best points (numerical).** u = 1 for 14/28/55/109 steps; then a singular arc on which the best points alternate between about 0.454 and 0; then u = 0. That the discrete optimum itself chatters is not proved (`R/theory-bangbang/singular-arcs.md`: "observed, not proved").
- **Trivial bound.** J ≥ −1, because the states are nonnegative.

### 1.3 Model provenance: OSIL vs GAMS coefficient c (catmix only)

- **The difference.** `catmix.gms` gives the x2-row coefficient as c = 9a exactly; it comes from −(1−u)x₂ − 10ux₂. The MINLPLib OSIL stores binary64 products instead: c_100 = 4.5000000000000005e-2, c_200 = 2.2500000000000003e-2, c_400 = 1.1250000000000001e-2, c_800 = 5.625000000000001e-3. So c_N − 9a = 5e-18, 3e-18, 1e-18 and 1e-18, all **positive** (exact; `R/publication/minlplib-status/report.md`; confirmed by this dossier's own reader).
- **Where it occurs.** c appears in both c-terms of every x2-row (half the rows). All other coefficients and the objective agree exactly.
- **What is certified.** All certificates are for the OSIL values. **New in this dossier:** Proposition M8 shows that the OSIL lower bounds also hold for the exact-coefficient model (c = 9a) of the GAMS text, and it gives the exact primal shift.
- **COPS 2.0 and 3.0.** The GAMS text is COPS 2.0 #14 with smoothing α = 0; this rests on the GAMS header and the COPS description, since the COPS AMPL archive returned 404. COPS 3.0 catmix uses 3-stage collocation, a **different model** (printed value −4.80556e-2). None of our results transfer to it.

## 2. Listed status (MINLPLib)

The instance pages were fetched 2026-09-29 (site updated 2026-09-14) and were
unchanged at the 2026-10-02 refresh. **No instance has a "solved" mark.**
"Best listed dual" is the best single-solver bound on the instance page, as in
the summary. The `instances.html` listing has a different dual column
(−37.1026, −77.456, −145.8856, −286.8087 for chain; none for catmix); the
paper should say which column it quotes.

| instance | best listed dual (solver, date) | listed primal p1 (page; infeasibility) | `minlplib.solu` best | other page duals |
|---|---|---|---|---|
| chain50 | 0.17451499 (ANTIGONE, 15 Aug 2014) | 5.07226149 (2e-16) | 5.0722614940 | BARON −45.23, COUENNE −49.77, GUROBI −37.10, LINDO −32.77, SCIP −38.84 |
| chain100 | 0.09367008 (ANTIGONE, 16 Aug 2014) | 5.06978461 (4e-16) | 5.0697846110 | BARON −173.12, COUENNE −106.90, GUROBI −77.46, LINDO −72.90, SCIP −183.98 |
| chain200 | 0.08256615 (ANTIGONE, 08 Mar 2015) | 5.06891734 (4e-16) | 5.0689173420 | BARON −377.41, COUENNE −219.02, GUROBI −145.89, LINDO −114.85, SCIP −284.66 |
| chain400 | 0.09563835 (ANTIGONE, 15 Aug 2014) | 5.0686217 (9e-16) | 5.0686216950 | BARON −862.00, COUENNE −447.13, GUROBI −706.56, LINDO −282.62, SCIP −286.81 |
| catmix100 | −0.06655801 (LINDO, 16 May 2020) | −0.04806939 (6e-11) | −0.0480693911 | none |
| catmix200 | −0.07254639 (LINDO, 16 May 2020) | −0.04805912 (1e-10) | −0.0480591228 | none |
| catmix400 | −0.65810523 (LINDO, 07 Dec 2015) | −0.04805652 (5e-12) | −0.0480565180 | none |
| catmix800 | −1.48896963 (LINDO, 13 Sep 2017) | −0.04805584 (2e-14) | −0.0480558393 | none |

Sources: `R/bound-audit/pages.json`, `R/open-instances-scout/fetched.csv`,
`R/bound-audit/pages/minlplib.solu`. All p1 points were added 15 Aug 2014.

- **Listed duals.** All are valid and weak. LINDO's catmix800 value lies below the trivial bound −1.
- **Listed primals against our enclosures (this dossier; `r2/logs/gaps.log`).**
  - *chain.* `minlplib.solu` rounds to 10 decimals. The chain100/200/400 listed values lie above our certified optimum enclosure by at least 2.1e-10, 1.5e-10 and 3.4e-10 (after allowing ±5e-11 for rounding). chain50's value is consistent with the optimum. The page display of chain400, 5.0686217 (= 5.06862170), is **not** optimal to its printed digits: the optimum is 5.0686216946…, which prints as 5.06862169. The older statement "the listed primal values are optimal to their printed digits" (`R/open-instances-wave2/cops/report.md` §2) holds only for the chain50/100/200 page displays.
  - *catmix.* The listed values lie above our exact points by at least 4.08e-8, 2.27e-8, 2.97e-8 and 6.19e-8 (`solu` values, ±5e-11 allowed). Even reading the 8-decimal page displays as truncations, the improvement is at least 3.2e-8, 1.5e-8, 1.7e-8 and 5.1e-8.
- **MINLPLib's 1e-6 rule.** Combined with our duals, the listed points would satisfy MINLPLib's 1e-6 relative-gap convention, |p−d|/min(|p|,|d|), for all chain instances and for catmix100/200/400 (8.5e-7, 4.7e-7, 6.2e-7). They would not for catmix800 (1.29e-6). Our exact points close all eight far below that tolerance. The listed points are tolerance-feasible only (infeasibility 2e-16 to 1e-10).
- **One-hour solver campaign** (BARON 26.5.27, GUROBI 13.0.2, SCIP 10.0.3; `R/publication/solver-runs/results_table.md`). No solver closed any of the eight.
  - Final chain duals were −36 to −1673.
  - GUROBI and SCIP had no finite catmix dual. BARON's catmix duals (−1.18, −2.87, −8.41, −54.6) carry BARON's own "globality not guaranteed (inappropriate variable bounds)" warning.
  - Several returned primals lie below our certified duals, so they are only tolerance-feasible. Examples: BARON catmix100, −0.0480694335130 (1.48e-9 below our dual); BARON chain50, 5.07226148709; GUROBI chain50, 5.07226129199 (row violation 6.7e-8).

## 3. The certificates

### 3.1 chain: discrete catenary calibration and a 2-D end window

**Idea in plain words.** The linear rows say that the chain is a polyline
over a fixed horizontal mesh. Summation by parts turns the energy of the
interior pieces into end terms plus a sum of products: cumulative length ×
vertical rise. Each product is bounded by a closed-form inequality (Lemma C3).
The inequality depends only on the cumulative length before and after the
piece, and it holds with equality exactly on discrete catenaries. Summing
telescopes, so the interior chain is bounded below by an explicit function of
the two end values (z_1, z_N) and two free "field parameters" (V, H). For
fixed end values the best (V, H) give the exact minimum (Proposition C6). What
remains is a 2-D problem, which a small interval branch and bound settles.

Unlike a Lagrangian with fixed multipliers, the vertical "multiplier" here is
the cumulative length v_k. It depends on the configuration, as a tension does
in a real chain.

**Lemma C1 (polyline form).** Let (x, u) satisfy the N linear rows. Put
z_i = x_i − ηu_i (0 ≤ i ≤ N) and z_{N+1} = x_N + ηu_N. Then
z_{i+1} = x_i + ηu_i for 0 ≤ i ≤ N, so x_i = (z_i + z_{i+1})/2 and
u_i = (z_{i+1} − z_i)/h. The map (x, u) ↦ z is a bijection between solutions
of the linear rows and ℝ^{N+2}. With x_0 = 1 and x_N = 3 we get z_0 = 2 − z_1
and z_{N+1} = 6 − z_N. Put

- λ_0 = √(η² + (z_1 − 1)²),
- λ_N = √(η² + (3 − z_N)²),
- λ_k = √(h² + (z_{k+1} − z_k)²) for 1 ≤ k ≤ N−1.

Then the length row is equivalent to λ_0 + λ_N + Σ_{k=1}^{N−1} λ_k = 4, and

    f = λ_0 + 3λ_N + Σ_{k=1}^{N−1} λ_k (z_k + z_{k+1})/2.

*Proof.* Row i reads x_{i+1} − ηu_{i+1} = x_i + ηu_i; adding and subtracting
gives x_i and u_i. Put ℓ_i = √(h² + (z_{i+1} − z_i)²); then
η√(1 + u_i²) = ℓ_i/2. The trapezoidal sums weight index i by ω_0 = ω_N = 1
and ω_i = 2 otherwise. So the length row reads
ℓ_0/2 + Σ_{1}^{N−1} ℓ_i + ℓ_N/2 = 4, and
f = x_0ℓ_0/2 + Σ_{1}^{N−1} x_iℓ_i + x_Nℓ_N/2. Finally, ℓ_0/2 = λ_0 because
z_1 − z_0 = 2(z_1 − 1), and ℓ_N/2 = λ_N likewise. ∎

*Geometry.* A = (0, 1), Q_k = ((k − ½)h, z_k), B = (1, 3). Piece AQ_1 has
length λ_0, the interior piece Q_kQ_{k+1} has length λ_k, and piece Q_NB has
length λ_N. The trapezoidal rule puts the mass of the end pieces at the end
heights 1 and 3, and the mass of each interior piece at its midpoint height.
Checks: verifier (60 digits, < 1e-50); this dossier's independent xml.etree
reader (50 digits, ≤ 1.4e-48 at random z; `r2/logs/chain_osil_check.log`).

**Lemma C2 (summation by parts).** For any reals z_1..z_N, λ_1..λ_{N−1} and V,
put v_1 = V, v_{k+1} = v_k + λ_k and V_k = (v_k + v_{k+1})/2. Then

    Σ_{k=1}^{N−1} λ_k (z_k + z_{k+1})/2 = v_N z_N − v_1 z_1 − Σ_{k=1}^{N−1} V_k (z_{k+1} − z_k).

*Proof.* v_{k+1}z_{k+1} − v_kz_k = V_k(z_{k+1} − z_k) + (v_{k+1} − v_k)(z_k + z_{k+1})/2.
Sum over k. ∎

**Lemma C3 (discrete catenary calibration).** Let h > 0 and H > 0. Put
τ = asinh(h/(2H)), G_H(v) = ½(v√(H² + v²) + H² asinh(v/H)) (so
G_H′(v) = √(H² + v²)) and c_H = 2G_H(h/2). Then for all real a, b with
b − a ≥ h,

    |a + b|/2 · √((b − a)² − h²) ≤ G_H(b) − G_H(a) − c_H,

with equality if and only if asinh(b/H) − asinh(a/H) = 2τ.

*Proof.* Both sides are homogeneous of degree 2 in (a, b, h, H), so take
H = 1. Write a = sinh φ_a, b = sinh φ_b, S = (φ_a + φ_b)/2, D = (φ_b − φ_a)/2,
u = |sinh S| and X = sinh D cosh D. Since b − a ≥ h > 0, D > 0. Elementary
hyperbolic identities give:
- G(b) − G(a) = D + (1 + 2u²)X;
- c = τ + sinh τ cosh τ;
- (a + b)/2 = sinh S cosh D;
- ((b − a)² − h²)/4 = Y := (1 + u²)sinh²D − sinh²τ ≥ 0.

So the claim is

    R := D − τ − sinh τ cosh τ + (1 + 2u²)X − 2u cosh D √Y ≥ 0.

For p, q ≥ 0 and t > 0, 2√(pq) = pt + q/t − (√(pt) − √(q/t))². With
p = u²cosh²D, q = Y and t = tanh D this gives

    2u cosh D √Y = (1 + 2u²)X − sinh²τ coth D − (√(tanh D) u cosh D − √(Y coth D))².

Hence R ≥ φ(D) := D − τ − sinh τ cosh τ + sinh²τ coth D. Now φ(τ) = 0 and
φ′(D) = 1 − sinh²τ/sinh²D, which is negative for D < τ and positive for
D > τ. So φ ≥ 0, with equality only at D = τ. At D = τ, √Y = u sinh τ and the
square vanishes too. So equality holds exactly when D = τ, that is, when
asinh(b/H) − asinh(a/H) = 2τ. ∎

**Theorem C4 (chain lower bound).** Let N ≥ 2, let (x, u) be any exactly
feasible point of chainN, let z_1, z_N, λ_0, λ_N be as in Lemma C1, and put
L = 4 − λ_0 − λ_N. Then for every V ∈ ℝ and H > 0,

    f(x,u) ≥ B_N(z_1, z_N; V, H) := λ_0 + 3λ_N + (V + L) z_N − V z_1 − G_H(V + L) + G_H(V) + (N − 1) c_H.

V and H may be arbitrary functions of (z_1, z_N). No bound on the interior
heights is used.

*Proof.* By Lemma C1, L = Σ_{k=1}^{N−1} λ_k and λ_k ≥ h. Apply Lemma C2 with
this V; then v_N = V + L. Since |z_{k+1} − z_k| = √(λ_k² − h²),

    −V_k(z_{k+1} − z_k) ≥ −|v_k + v_{k+1}|/2 · √((v_{k+1} − v_k)² − h²) ≥ −(G_H(v_{k+1}) − G_H(v_k) − c_H),

by Lemma C3 with a = v_k and b = v_{k+1} (b − a = λ_k ≥ h). Summing over
k = 1..N−1 telescopes to −G_H(V + L) + G_H(V) + (N − 1)c_H. ∎

**Lemma C5 (end window).** Every feasible point satisfies (z_1, z_N) ∈ Ω_N,
the set of points with

    |z_1 − 1| ≤ 3 + η,   |z_N − 3| ≤ 3 + η,   L(z_1, z_N) ≥ √((1 − h)² + (z_N − z_1)²).

*Proof.* L ≥ (N − 1)h = 1 − h and λ_N ≥ η, so λ_0 ≤ 4 − η − (1 − h) = 3 + η,
and |z_1 − 1| ≤ λ_0. The bound on z_N follows in the same way. The interior
polyline runs from Q_1 to Q_N, a horizontal span of 1 − h, so its length L is
at least the chord. ∎

**Proposition C6 (the end-window reduction is exact; discrete Weierstrass
theorem). Proved, new in this dossier.** Let N ≥ 3. Suppose (z_1, z_N)
satisfies the chord condition strictly:
L > √((1 − h)² + (z_N − z_1)²), with L = 4 − λ_0 − λ_N.
1. There are H* > 0 and V* with
   - tanh φ_m = (z_N − z_1)/L,
   - 2H* sinh((N − 1)τ*) = √(L² − (z_N − z_1)²), where τ* = asinh(η/H*),
   - V* = H* sinh(φ_m − (N − 1)τ*).
2. The *discrete catenary* with slopes (z_{k+1} − z_k)/h = sinh(φ_m − (N − 1)τ* + (2k − 1)τ*), k = 1..N−1, starting at z_1, ends at z_N and has interior length L. Together with the end pieces it is a feasible point.
3. Its objective equals B_N(z_1, z_N; V*, H*). Hence
   max_{V,H} B_N(z_1, z_N; V, H) = min{ f : feasible, with these end values }.
4. This discrete catenary is the unique minimizer on that slice.

Consequently f*_N = inf over (z_1, z_N) ∈ Ω_N of max_{V,H} B_N. The
reduction to the end window loses nothing.

*Proof.* (1) The map g(H) = 2H sinh((N − 1) asinh(η/H)) is continuous on
(0, ∞), tends to 2(N − 1)η = 1 − h as H → ∞, and tends to +∞ as H → 0⁺ when
N ≥ 3 (it behaves like (2η)^{N−1}H^{2−N}). By the strict chord condition, the
target √(L² − (z_N − z_1)²) exceeds 1 − h, so the intermediate value theorem
gives H*. Also |z_N − z_1| < L, so φ_m exists.

(2) Put φ_1 = φ_m − (N − 1)τ, S_k = φ_1 + (2k − 1)τ and n = N − 1. Then
Σ_{k=1}^{n} sinh S_k = sinh φ_m sinh(nτ)/sinh τ and
Σ cosh S_k = cosh φ_m sinh(nτ)/sinh τ. Since h = 2H sinh τ, the rise is
h Σ sinh S_k = 2H sinh φ_m sinh(nτ) = z_N − z_1 and the length is
h Σ cosh S_k = 2H cosh φ_m sinh(nτ) = L, by the equations of (1). The end
pieces depend only on (z_1, z_N), so the length row holds.

(3) Put v_k = H sinh(φ_1 + 2(k − 1)τ). Then v_1 = V*,
v_{k+1} − v_k = 2H cosh S_k sinh τ = h cosh S_k = λ_k, and
asinh(v_{k+1}/H) − asinh(v_k/H) = 2τ, so Lemma C3 holds with equality. Also
V_k = H sinh S_k cosh τ has the sign of z_{k+1} − z_k = h sinh S_k, so the
first inequality in the proof of Theorem C4 is an equality too. Hence
f = B_N(z_1, z_N; V*, H*) ≤ max B_N. Theorem C4 gives
max B_N ≤ min over the slice ≤ f, so all three are equal.

(4) Equality forces D = τ and the sign condition for every k. These fix v_k
and then z_{k+1} − z_k, given (V, H) = (V*, H*). ∎

*Evidence.* This dossier's 40-digit test (`r2/logs/lemma_checks.log`) checks
the interior inequality of Theorem C4 on 3,000 random and catenary chains. The
minimum relative slack is −5.4e-40, which is rounding; equality to 1e-30 is
asserted on exact discrete catenaries. The closed-form (V*, H*) make ∂B/∂V
and ∂B/∂H vanish to 1e-41.

At the stored KKT end values, B_N equals the KKT objective in all 25 stored
digits (`chainN_bound.json`). It also equals the objective of the exact
feasible point (Section 4.1) to about 33 digits. So the ~1e-14 gaps are
entirely the chosen branch-and-bound target (KKT value − 1e-14), not slack in
the certificate.

**Computer-assisted step C7 (what is checked).** By Theorem C4 and
Lemma C5, f*_N ≥ inf over Ω_N of B_N(·; V(·), H(·)), for any choice of
multipliers. Each B&B certifies the following.

- **Cover.** A finite bisection tree of boxes covers the root box. The authors' root is [−2 − h, 4 + h] × [−h, 6 + h]; the verifier's is [1 − (3 + η) − 1e-9, 1 + 3 + η + 1e-9] × [3 − (3 + η) − 1e-9, 3 + 3 + η + 1e-9]. Both contain the box of Lemma C5.
- **Leaves.** Every leaf either is proved disjoint from Ω_N by an interval evaluation of L ≥ 0 and the chord condition, or carries binary64 constants (V_b, H_b > 0) with a rigorous lower bound of B_N(·; V_b, H_b) over the box that is ≥ L_N.
- **Leaf bound.** The larger of the natural interval extension and a first-order mean-value form around the box centre. The gradient formula matches symbolic differentiation, and the expansion point (a float midpoint) lies in the box.
- **What the result is.** L_N is the binary64 target (60-digit KKT value − 1e-14). Validity does not depend on how (V_b, H_b) are chosen; both codes solve the 1-D equation of Proposition C6 in floating point at the box centre. No unresolved leaves remain.

Arithmetic and trust:
- mpmath 1.3.0 `iv` with outward rounding for +, −, ×, ÷, integer powers, sqrt and log. asinh(x) = log(x + √(x² + 1)) for x ≥ 0, extended by oddness and monotonicity. Authors at 40 digits, verifier at 30 digits.
- Exact conversion of binary64 values to mpmath.
- The OSIL reading, checked by three readers: `osilx.py`, the primal track's and its reviewer's xml readers, and this dossier's xml.etree check.

Two codes:
- The authors' `R/open-instances-wave2/cops/chain_bound.py`: 11,121/15,329/21,057/27,843 boxes, 13/18/25/34 s.
- The verifier's independent `R/reviews/cops-verification/v_chain_bnb.py`: 36,689/52,955/75,385/104,945 boxes, 50/79/122/154 s.
- Both certify the same four doubles with 0 unresolved boxes. The clean-checkout reproduction (`R/publication/reproduction/cops/report.md`) reran both bit-identically.

The authors' pruning test squares one endpoint in plain mpf arithmetic (the
verifier's caveat). With a one-line rigorous fix
(`chain-catmix-checks/chain_bound_rigorous_pruning.patch`), the first pass
reproduced identical certificates for all four N: same box and infeasible-box
counts, 0 unresolved. This pass re-ran N = 50 and got the same result
(11,121 boxes, 61 infeasible, 0 unresolved; `r2/logs/chainfix_spot_chain50_bound.json`).

**Remark (calibration reading).** Put Φ_k(z, v) := v z − G_H(v) + k c_H on the
extended state (height, cumulative length). Then every interior stage
satisfies λ_k (z_k + z_{k+1})/2 ≥ Φ_{k+1}(z_{k+1}, v_{k+1}) − Φ_k(z_k, v_k).
So Φ is a Krotov verification function: a discrete Weierstrass field of
catenaries with vertical costate −v (`R/theory-calibration/scouting.md` §2.4
writes it with the opposite sign convention). The family of discrete
catenaries, slopes sinh(α + 2kτ), has two parameters (V, H). These are the
field parameters chosen per box.

### 3.2 catmix: rigorous DP lower bound on an exact 1-D projective reduction

**Idea in plain words.** For fixed controls, the states follow from the rows
by inverting 2×2 matrices, and each stage map is linear and entrywise
nonnegative. The optimal cost-to-go is therefore a minimum of linear functions
of the state. That makes it concave and positively homogeneous, so it is
determined by its values on the directions θ ∈ [0, 1]. We bound it below on a
grid of directions. Concavity guarantees that linear interpolation between the
grid values stays below the true function, with second-order error. Going
backward stage by stage, each grid value is a rigorous lower bound of a 1-D
minimization over u ∈ [0, 1] of a piecewise rational function.

**Lemma M1 (nonnegativity). Proved; short proof new in this dossier.** Let
0 < a ≤ 1/10, b = 10a and 9a ≤ c ≤ 1 − a; this covers the four OSIL values and
c = 9a. Then for all u ∈ [0, 1]:
- det P(u) ≥ 1 + a;
- adj P(u) ≥ 0 and Q(u) ≥ 0 entrywise.

Hence P(u)⁻¹ ≥ 0 and M(u) := Q(u)P(u)⁻¹ ≥ 0.

*Proof.* det P(u) − (1 + a) = u[a(1 + a) + c + acu − 10a²u], and for
u ∈ [0, 1] the bracket is at least a + a² + 9a − 10a² > 0. Next,
adj P(u) = [[1 + a + cu, 10au], [au, 1 + au]] ≥ 0. The entries of Q are
1 − au ≥ 1 − a, 10au, au and 1 − a − cu ≥ 1 − a − c ≥ 0. ∎

The verifier also checked the exact minima of all stage polynomials in
rational arithmetic for all four N (`R/reviews/cops-verification/` §2a;
`R/reviews/catmix-recheck.md`, check 2).

**Lemma M2 (reduction).** Fix u ∈ [0, 1]^{N+1}. The rows have a unique
solution x(u). Put y_i := Q(u_i)x_i for i = 0..N−1. Then:
- y_0 = (1 − au_0, au_0)ᵀ, y_i = M(u_i)y_{i−1} for 1 ≤ i ≤ N−1, and x_{i+1} = P(u_{i+1})⁻¹y_i;
- J(u) + 1 = 𝟙ᵀP(u_N)⁻¹y_{N−1};
- all y_i and x_i lie in K := ℝ²₊, so J ≥ −1.

*Proof.* Row i is P(u_{i+1})x_{i+1} = Q(u_i)x_i = y_i, and
y_{i+1} = Q(u_{i+1})x_{i+1}. Nonnegativity follows from Lemma M1. ∎

Each control enters exactly one factor: Q(u_0), M(u_1), …, M(u_{N−1}), and
P(u_N)⁻¹. That is what makes the DP over independent controls exact.

**Lemma M3 (value functions).** On K define
V_{N−1}(y) = min_{u∈[0,1]} 𝟙ᵀP(u)⁻¹y and V_{i−1}(y) = min_{u∈[0,1]} V_i(M(u)y)
for i = N−1, …, 1. Then:
- (i) J* + 1 = min_{u_0∈[0,1]} V_0(Q(u_0)x_0), with x_0 = (1, 0)ᵀ;
- (ii) each V_i is concave, positively homogeneous of degree 1, and nonnegative on K;
- (iii) each V_i is superadditive: V_i(y + y′) ≥ V_i(y) + V_i(y′).

*Proof.* Unrolling gives V_i(y) = min over (u_{i+1}, …, u_N) of κ(u)ᵀy, with
κ(u)ᵀ = 𝟙ᵀP(u_N)⁻¹M(u_{N−1})⋯M(u_{i+1}) ≥ 0. κ is continuous on a compact
set, so the minimum is attained. A pointwise minimum of linear functions with
nonnegative coefficients is concave, positively homogeneous and nonnegative on
K. Then V(y + y′) = 2V((y + y′)/2) ≥ V(y) + V(y′). Part (i) follows from
Lemma M2. ∎

**Lemma M4 (chord minorant).** Let 0 = θ_0 < ⋯ < θ_R = 1,
r_k = (1 − θ_k, θ_k)ᵀ and w_k ≤ V_i(r_k). For y ∈ K∖{0}, put
ρ(y) = y₁ + y₂ and θ(y) = y₂/ρ(y). If θ(y) ∈ [θ_k, θ_{k+1}], define

    W(y) = ρ(y)[w_k + σ_k(θ(y) − θ_k)],   σ_k = (w_{k+1} − w_k)/(θ_{k+1} − θ_k).

Equivalently, W(y) = α_k y₁ + β_k y₂ with α_k = w_k − σ_kθ_k and
β_k = w_k + σ_k(1 − θ_k). Then W ≤ V_i on K.

*Proof.* Write y = s r_k + t r_{k+1} with s = ρ(θ_{k+1} − θ)/Δθ ≥ 0 and
t = ρ(θ − θ_k)/Δθ ≥ 0; then W(y) = s w_k + t w_{k+1}. By Lemma M3(iii) and
homogeneity, V_i(y) ≥ sV_i(r_k) + tV_i(r_{k+1}) ≥ s w_k + t w_{k+1}. ∎

W need not be concave: validity uses concavity of the *true* V_i, not of W.
`R/theory-calibration/scouting.md` Proposition 2.3 gives the alternative
form, in which W itself is a calibration if it is concave.

**Theorem M5 (DP lower bound).** For each i = 0..N−1, let Θ^{(i)} be a grid
containing 0 and 1 and carrying numbers w^{(i)}_j. Let W^{(i)} be the chord
function of (Θ^{(i)}, max(w^{(i)}, 0)). Suppose that

    (T) w^{(N−1)}_j ≤ min_{u∈[0,1]} 𝟙ᵀP(u)⁻¹ r^{(N−1)}_j,
    (S) w^{(i−1)}_j ≤ min_{u∈[0,1]} W^{(i)}(M(u) r^{(i−1)}_j),   i = N−1, …, 1,
    (I) ω ≤ min_{u∈[0,1]} W^{(0)}(Q(u) x_0).

Then J* ≥ ω − 1.

*Proof.* By induction, w^{(i)}_j ≤ V_i(r^{(i)}_j); clipping at 0 keeps this,
since V_i ≥ 0. Lemma M4 gives W^{(i)} ≤ V_i on K. Since M(u)r ∈ K,
min_u W^{(i)}(M(u)r) ≤ min_u V_i(M(u)r) = V_{i−1}(r). Conclude with (I) and
Lemma M3(i). ∎

**Lemma M6 (losses add up across stages). Proved, new in this dossier;
explains tightness, not needed for validity.** For u ∈ [0, 1] and
9a ≤ c ≤ 1 − a, 𝟙ᵀM(u) ≤ 𝟙ᵀ entrywise, so ρ(M(u)y) ≤ ρ(y) on K.
Consequently:
- let δ_i ≥ 0 bound the slack of the computed minimization at stage i, that is, w^{(i−1)}_j ≥ min_u W^{(i)}(M(u)r_j) − δ_i, with the same meaning for the terminal and initial stages;
- let ε_i be the interpolation error of the exact V_i on the grid Θ^{(i)}: the supremum, over y ∈ K with ρ(y) = 1, of V_i(y) minus the chord interpolant of the exact values V_i(r_k).

Then J* − (ω − 1) ≤ Σ_i (δ_i + ε_i), summed over the N + 1 minimizations.

*Proof.* 𝟙ᵀQ = 𝟙ᵀP − (0, 2a − 2(b − c)u), so
𝟙ᵀM = 𝟙ᵀQP⁻¹ = 𝟙ᵀ − 2(a − (b − c)u)·e₂ᵀP⁻¹. Here e₂ᵀP⁻¹ ≥ 0 (Lemma M1),
and a − (b − c)u ≥ min(a, c − 9a) ≥ 0. Let E_i = max_k (V_i(r_k) − w^{(i)}_k);
clipping at 0 does not increase it. For unit y in cone k, write
y = s r_k + t r_{k+1} with s + t = 1. Then
V_i(y) − W^{(i)}(y) ≤ ε_i + (s + t)E_i = ε_i + E_i, and by homogeneity
V_i − W^{(i)} ≤ (ε_i + E_i)ρ on K. Let u′ minimize W^{(i)}(M(u)r) for a unit
ray r. Then
V_{i−1}(r) − w^{(i−1)}(r) ≤ V_i(M(u′)r) − W^{(i)}(M(u′)r) + δ_i ≤ ρ(M(u′)r)(ε_i + E_i) + δ_i ≤ ε_i + E_i + δ_i.
The terminal stage gives E_{N−1} ≤ δ_term (the terminal cost is linear, so
nothing is interpolated), and ρ(Q(u_0)x_0) = 1 at the initial stage. Summing
gives the claim. ∎

*Use.* The authors' stage routine stops a subinterval only when its lower
bound is within tol = 1e-14 of a float incumbent. Its logged per-stage loss
is ≤ 9.99e-15. By Lemma M6, the stage minimization accounts for at most
about 101 × 1e-14 ≈ 1.0e-12 of the authors' catmix100 gap of 7.92e-12, so
most of the gap is interpolation error from the grid. This contradicts the
verifier's suggestion of "a grid-independent loss in their stage
minimization" (`R/reviews/cops-verification/verification-report.md` §2c).
It agrees with the per-stage cross-check below (agreement within 9.4e-15 per
ray). This pass did not identify which part of the authors' grid causes the
loss: the band spacing there is 1e-6 throughout (`r2/logs/grid_diag.log`).
Lemma M6 is also consistent with the observed second-order convergence of
uniform grids. Where V_i is C² in θ, its chord error is O(Δθ²). At a kink of
V_i (a switch of the minimizing control) the error is O(Δθ), but only on one
cone.

**Computer-assisted step M7 (what is checked).** For each stage and output
ray r, f(u) = W(M(u)r) = W(Nm(u)r)/D(u), where Nm = Q adj P has quadratic
entries and D = det P ≥ 1 + a is quadratic. On cone k, f = p_k/D with
p_k = w_kρ(n) + σ_k g_k(n), where n(u) = Nm(u)r and
g_k(y) = (1 − θ_k)y₂ − θ_k y₁, all quadratic in u. The certificate of record
is the verifier's `R/reviews/cops-verification/v_catmix_dp.py`, used
unchanged by the recheck for N = 400/800. For every ray it:
1. covers [0, 1] by intervals cut at 0, 1 and the float preimages of cone boundaries, plus ±1e-9 slivers;
2. verifies on each interval a cone range [k_lo, k_hi] rigorously, from the signs of the quadratics g_{k_lo}(n(u)) ≥ 0 and g_{k_hi+1}(n(u)) ≤ 0, widening until verified;
3. bounds each (interval, cone) pair either crudely, by (min ρ / max D)·min(w_k, w_{k+1}) (valid because w ≥ 0), or by an exact Dinkelbach step: for a float t, a rigorous m ≤ min_I (p_k − tD) gives p_k/D ≥ t + m/D_min if m < 0 and ≥ t + m/D_max otherwise. Quadratic minima use the lower ends of the coefficient intervals (valid since u ≥ 0) and include the vertex whenever it may lie in the interval;
4. sets the new w to the minimum over all pairs.

The reported bound is the binary64 value dn(ω − 1). Floats decide only where
u is cut and which bound is used, never validity.

Arithmetic and trust:
- IEEE 754 binary64 with correctly rounded +, −, ×, ÷ in numpy, round-to-nearest, without flush-to-zero; values stay far from the subnormal range. Each result moves one ulp outward with `np.nextafter`.
- No libm function enters the rigorous path; `sqrt` is used only to place cuts.
- Stage-polynomial coefficients are exact rationals: sympy with P·adj P = det P·I asserted (verifier), and closed formulas (authors). They are enclosed by binary64 intervals.
- Grid rays are dyadic with ≤ 30 fractional bits, so 1 − θ and differences of θ are exact.
- OSIL reading by three readers: `osilx.py`, the recheck's regex cross-check, and this dossier's xml.etree reader.

Second implementation and cross-check:
- **Authors' code.** `R/open-instances-wave2/cops/catmix_bound.py` uses its own 1-D interval branch and bound per ray: mean-value and second-order Taylor bounds on chord pieces, and a Lipschitz bound across many cones. End to end it certifies the weaker bounds −0.048069432038882705, −0.04805914560067171 (safe display −0.048059145600671712), −0.048056547950296354 and −0.048055901841076894.
- **Per-stage cross-check (this dossier, first pass; `xcheck.py`, `logs/x{coarse,fine}100.log`).** Both stage routines ran on *identical* inputs (N = 100, same grid, same chord values): 99 stages on a 324-ray grid, and 40 stages on a grid with a 2^-21 band on [0.0703, 0.0710]. They agree per ray within 9.44e-15, and both stay below dense float minima (max(LB − dense) ≤ −3.9e-16). This pass re-ran the first 12 coarse stages and reproduced the log line for line (`r2/logs/xcheck_spot12.log`).

**Proposition M8 (monotonicity in c; transport to the exact-coefficient
model). Proved, new in this dossier.** Fix u ∈ [0, 1]^{N+1}, and let
9a ≤ c′ ≤ c ≤ 1 − a. Then J_{c′}(u) ≥ J_c(u). Hence J*_{9a} ≥ J*_{c_N} ≥ L_N:
every certified OSIL lower bound is also a lower bound for the GAMS-text
model, in which c = 9a.

*Proof.* P_{c′} = P_c − (c − c′)uE₂₂ and Q_{c′} = Q_c + (c − c′)uE₂₂, with
E₂₂ = e₂e₂ᵀ. By the resolvent identity,
P_{c′}⁻¹ − P_c⁻¹ = (c − c′)u·P_{c′}⁻¹E₂₂P_c⁻¹ ≥ 0, because both inverses are
nonnegative (Lemma M1). So P_{c′}⁻¹ ≥ P_c⁻¹ ≥ 0 and Q_{c′} ≥ Q_c ≥ 0, which
gives M_{c′} ≥ M_c ≥ 0 entrywise. Further, Q(u_0)x_0 = (1 − au_0, au_0)ᵀ does
not depend on c. By Lemma M2, J + 1 is a product of nonnegative factors, each
entrywise nondecreasing as c decreases. ∎

Under c = 9a, the exact objectives of our points are higher than under the
OSIL c by 1.18e-17 (100), 1.42e-17 (200), 9.47e-18 (400) and 1.89e-17 (800).
This was computed in exact rationals in both passes, with independent code
(`logs/catmix_exact.log`, `r2/logs/exact_catmix.log`). Gaps for the
exact-coefficient model are therefore ≤ 1.86e-13, 1.90e-11, 6.81e-11 and
1.49e-10.

**Grid design (heuristic; does not affect validity).**
- **Second-order convergence.** Uniform grids lose about 16-fold when the spacing is divided by 4. For N = 100, spacings 2^-9/2^-11/2^-13/2^-15 give gaps 3.2e-4/2.1e-5/1.28e-6/8.0e-8 (verifier).
- **Loss on the singular arc.** Almost all of the loss accumulates there. The recheck's empirical fit is gap ≈ n_arc·C·d², with C ≈ 1.2–1.8 at N = 400/800 and d the band spacing on the arc. This is a fit, not a law, and it does not carry over to N = 100.
- **Final designs.**
  - N = 100 (config B): base 2^-16, band [0.0697, 0.0715] at 2^-20, and a 601-ray window at 2^-25 around the primal θ-trajectory; 9,131 rays per stage.
  - N = 200 (config A): base 2^-15, band [0.0695, 0.0717] at 2^-19, and a 401-ray window at 2^-24.
  - N = 400/800: a 2^-21 core on [0.0703, 0.0710] and a 2^-19 shell on [0.0695, 0.0717] on the arc stages, with the 2^-24 window elsewhere; 2,629 and 2,647 rays per stage.

## 4. Exactly feasible primal points

### 4.1 chain: points in a real quadratic field (`R/publication/primal/chain/`)

**Proposition P1.** Let ω_0 = ω_N = 1 and ω_i = 2 otherwise. For t ∈ ℝ^{N+1}
with t > 0, put u_i = (t_i − t_i⁻¹)/2 and s_i = (t_i + t_i⁻¹)/2, and let x
follow from x_0 = 1 through the linear rows. This defines a feasible point of
chainN if and only if

    Σ ω_i t_i = 12N   and   Σ ω_i / t_i = 4N.

*Proof.* s_i > 0 and s_i² − u_i² = 1, so s_i = √(1 + u_i²) exactly. Next,
x_N = 1 + ηΣω_iu_i, so x_N = 3 ⇔ Σω_iu_i = 4N, and the length row ⇔
Σω_is_i = 8N. Add and subtract, using t = u + s and 1/t = s − u. ∎

**Construction.**
- Start from the saved wave-2 double point.
- Fix t_i for i ∉ {1, N−1} to 20 decimals; these are stored in `points/chainN_generator.json`.
- Solve t_1 + t_{N−1} = α and 1/t_1 + 1/t_{N−1} = β, with explicit rationals α and β. So t_1 and t_{N−1} are the roots of T² − αT + α/β, and t_1 is the smaller root.
- The discriminant n/d is a positive non-square rational, so every coordinate lies in Q(√R_N) with R_N = n·d. R_N has 1,928/3,755/7,323/14,507 digits.
- The exact point is within 2.3e-16 (x) and 4.0e-15 (u) of the double point.

**Checks.**
- Feasibility is checked in exact arithmetic in Q(√R_N), evaluating the OSIL expression trees: all rows and both fixed bounds hold exactly. A sqrt node is accepted only if the candidate root squares exactly to the argument and is nonnegative.
- The objective is enclosed with `math.isqrt`. The proof uses only Python integer and Fraction arithmetic.
- Independent review r1 re-checked everything with its own reader and its own Q(√D) arithmetic (`R/publication/reviews/primal-chain-review-r1.md`, verdict "verified").
- Evidence only: SCIP's checkSol (floating point) accepts the points, and negative controls are rejected.

| N | objective of the exact point (40-dp enclosure) |
|---|---|
| 50 | [5.0722614939828723164454381769845467731843, …731844] |
| 100 | [5.0697846107387605574911913664186759056713, …056714] |
| 200 | [5.0689173417931710001847965010674364416891, …416892] |
| 400 | [5.0686216946040190143614896914450892607014, …607015] |

These agree with the 60-digit KKT values in all 25 stored digits.

### 4.2 catmix: binary64 controls with exact rational states

**Proposition P2.** For any u ∈ [0, 1]^{N+1} with binary64 entries, (u, x(u))
is exactly feasible, because det P > 0 and the states are free. x(u) and J(u)
are rationals, computed exactly by the recursion of Lemma M2.

| N | point used for the gap | exact objective J (floor/ceil at 1e-30) | source |
|---|---|---|---|
| 100 | authors' controls `catmix100_u.npy` | [−0.048069432030959562924734533988, −…987] | verifier's exact simulation; this dossier (both passes) |
| 100 | (tighter, optional) verifier's Newton controls `catmix100_u_newton.npy` | [−0.048069432030979599106538896273, −…272] | this dossier. The verification report prints −0.048069432030979596104, the binary64 rounding, 3.0e-18 high; harmless for an upper bound |
| 200 | authors' `catmix200_u.npy` | [−0.048059145580114393563745030823, −…822] | verifier; this dossier |
| 400 | authors' `catmix400_u.npy` | [−0.048056547756611554855186829087, −…086] | before: a 60-digit mpmath `iv` enclosure only; **now exact** (this dossier) |
| 800 | recheck's DP-policy controls `catmix800_final_policy_u.npy` | [−0.048055901331230800339383491204, −…203] | `R/reviews/catmix-recheck-checks/logs/policy_exact_800.log`; this dossier |

Other exact values (this dossier):
- the authors' catmix800 `_snap` point: −0.0480559013308474668863…;
- the authors' catmix800 non-snap point: −0.0480559013293736689208…;
- the recheck's catmix400 policy point: −0.0480565477559440725822….

## 5. Numbers table

Dual displays are rounded toward −∞, primal displays toward +∞, and gaps
upward. Relative gaps divide by |dual|.

| instance | best listed dual | our dual: safe display (exact binary64 value begins) | primal upper display | gap ≤ (abs.) | rel. ≤ | sources |
|---|---|---|---|---|---|---|
| chain50 | 0.17451499 | 5.0722614939828627 (5.07226149398286274561…) | 5.0722614939828723165 | 9.62e-15 | 1.90e-15 | dual: `R/open-instances-wave2/cops/logs/chain50_bound.json` (bnb.bound), re-certified by `R/reviews/cops-verification/logs/chain50_bnb.log`; primal: `R/publication/primal/chain/points/chain50_box.json` and `logs/verify.log`; gap: `R/publication/integration/gap-values.json` |
| chain100 | 0.09367008 | 5.0697846107387505 (5.06978461073875052989…) | 5.0697846107387605575 | 1.01e-14 | 1.99e-15 | same, N = 100 |
| chain200 | 0.08256615 | 5.0689173417931616 (5.06891734179316166830…) | 5.0689173417931710002 | 9.41e-15 | 1.86e-15 | same, N = 200 |
| chain400 | 0.09563835 | 5.068621694604009 (5.06862169460400924236…) | 5.0686216946040190144 | 1.01e-14 | 1.98e-15 | same, N = 400 |
| catmix100 | −0.06655801 | −0.048069432031144562 (−0.04806943203114456136…) | −0.0480694320309595629 | 1.85e-13 | 3.85e-12 | dual: `R/reviews/cops-verification/logs/catmix100_cfgB.log`; primal: verifier's exact simulation; `exact_display_checks.json` |
| catmix200 | −0.07254639 | −0.048059145599072769 (−0.04805914559907276811…) | −0.0480591455801143935 | 1.90e-11 | 3.95e-10 | dual: `R/reviews/cops-verification/logs/catmix200_cfgA.log` |
| catmix400 | −0.65810523 | −0.048056547824671288 (−0.04805654782467128766…) | −0.0480565477566115548 | 6.81e-11 | 1.42e-9 | dual: `R/reviews/catmix-recheck-checks/logs/catmix400_final.log`; primal now exact (this dossier) |
| catmix800 | −1.48896963 | −0.048055901479675652 (−0.04805590147967565145…) | −0.0480559013312308003 | 1.49e-10 | 3.09e-9 | dual: `R/reviews/catmix-recheck-checks/logs/catmix800_final.log`; primal: `policy_exact_800.log` |

**Agreement with the summary.** The summary's displays ("5.06862 … 5.07226",
"−0.04806944 … −0.04805591", "≤ 1.01e-14",
"≤ 1.85e-13 / 1.90e-11 / 6.81e-11 / 1.49e-10") are valid and agree with this
table. The per-instance gaps above were recomputed exactly from the binary64
duals and the exact primal values (`r2/logs/gaps.log`). Four remarks:
1. The summary's catmix dual range is built from the *authors'* weaker duals, while its gaps use the stronger verifier/recheck duals of this table. The paper should show the per-instance duals that the gaps use.
2. The chain gaps use the displays shown, as `gap-values.json` does; that file rounds up to a unit of 1e-16 and prints 9.7e-15, 1.01e-14, 9.5e-15 and 1.01e-14. Against the exact doubles the gaps are 9.58e-15, 1.01e-14, 9.34e-15 and 9.78e-15. If the 17-digit truncation 5.0686216946040092 is shown for chain400, its gap is 9.82e-15.
3. The authors' end-to-end catmix bounds give gaps of 7.93e-12, 2.06e-11, 1.94e-10 and 5.11e-10 (the last against the `_snap` point).
4. Optional tightening: with the Newton point, the catmix100 gap is 1.65e-13 (1.6496e-13).

**Displays that are NOT valid bounds** (shortest-repr strings above their
certified doubles; `exact_display_checks.json`). The paper must not use:
- 5.072261493982863 (chain50) and 5.068917341793162 (chain200);
- −0.04806943203114456 (verifier, catmix100);
- −0.04805914560067171 (authors, catmix200);
- −0.04805590147967565 (recheck, catmix800).

**Computational cost** (shared 36-core machine, one thread; indicative only):

| | chain50/100/200/400 | catmix100 | catmix200 | catmix400 | catmix800 |
|---|---|---|---|---|---|
| certificate of record | authors: 11,121–27,843 boxes, 13–34 s; verifier: 36,689–104,945 boxes, 50–154 s | config B: 9,131 rays/stage, 2.0e9 pairs, 2,358 s (reproduction 46.0 min) | config A: 8.6e8 pairs, 1,170 s (20.2 min) | 2,629 rays/stage, 1.74e9 pairs, 2,578 s (45.2 min) | 2,647 rays/stage, 1.88e9 pairs, 2,595 s (46.1 min) |
| authors' weaker run | — | 1.6e8 interval evaluations, 21 min | 2.5e8, 32 min | 3.9e8, 47 min | 6.1e8, 70 min |

`R/publication/READINESS.md`'s runtime table gives 1049/1728/3001/4602 s for
catmix. These are the authors' runs, which produce the weaker bounds, not the
summary duals (issue CC-8).

## 6. Verification record

| review | scope | method | verdict |
|---|---|---|---|
| `R/reviews/cops-verification/verification-report.md` (2026-09-30) | chain: polyline form, identity, lemma, theorem, domain, all four B&Bs, primal vectors. catmix: transformation, M ≥ 0 with exact decimals, concavity and chord argument, reading of the authors' code, own DP for N = 100/200, primal | own code (`v_chain_*`, `v_catmix_*`); sympy plus a 200,000-case 50-digit test of the lemma (min slack +1.7e-31) and an adversarial search; own 2-D B&B; own DP with Dinkelbach per-ray bounds; shares the OSIL reader `osilx.py` | all verified (2c: "verified by reading, with caveats"); catmix100/200 duals tighter than claimed |
| `R/reviews/catmix-recheck.md` (2026-09-30) | catmix400/800 duals | unchanged copy of `v_catmix_dp.py`, own driver with grid-validity assertions, own regex OSIL cross-check, exact rational evaluation of the policy controls | confirmed; tighter by 1.26e-10 and 3.61e-10 |
| `R/publication/primal/chain/report.md`; `R/publication/reviews/primal-chain-review-r1.md` (2026-10-01/03) | exact chain points | separate build and check scripts; the reviewer's own xml reader and Q(√D) arithmetic | verified; minor display issues fixed |
| `R/publication/reproduction/cops/report.md` (2026-10-02) | all 52 commands, from a clean checkout | rerun; strace input audit | all outputs bit-identical; found the invalid displays |
| `R/publication/reviews/integration-review-r1.md` | gap cells | exact rational recomputation | confirmed |
| `R/publication/minlplib-status/report.md` (r1, r2) | status refresh; OSIL vs `.gms` | exact rational comparison | status unchanged; catmix c differs |
| `R/publication/literature/control/report.md` (r1, r2) | prior work | sources in `.../control/sources/` | "new as far as found" |
| **this dossier** (two passes) | re-derivation of all proofs; new Proposition C6, Lemma M1 proof, Lemma M6, Proposition M8; Section 8.2 checks | own scripts | no invalidating issue; the new statements await an independent read |

**Remaining assumptions.**
- *chain dual:* mpmath `iv` outward rounding (+, −, ×, ÷, powers, sqrt, log) at 30 and 40 digits, in both implementations; the OSIL interpretation (three readers agree).
- *chain primal:* none beyond Python integer and Fraction arithmetic and the OSiL conventions (default bounds; sqrt is the nonnegative root).
- *catmix dual:* IEEE 754 binary64 semantics of numpy and `nextafter`; exact sympy/Fraction coefficients; correctness of the per-ray code. The strongest values rest on `v_catmix_dp.stage` alone. The authors' code agrees with it per stage on identical inputs and certifies the weaker bounds end to end.
- *catmix primal:* none beyond exact Fraction arithmetic (catmix400 included as of this dossier).
- *transport to c = 9a:* Proposition M8 (proved here; not yet independently read).

## 7. Relation to prior work

Slugs refer to `literature/papers/<slug>/`. The prior-work verdicts come from
the verified control literature report (`R/publication/literature/control/report.md`).

- **COPS** (`dolan2001-benchmarking-optimization-software-with-cops`, `dolan2001-cops-2-problem-collection-source`, `dolan2004-benchmarking-optimization-software-with-cops`; GAMS sources in `library2026-cops-and-gams-source-models`). Local NLP values only; no global claims.
  - chain: LOQO/MINOS/SNOPT 5.07226, 5.06978, 5.06891, 5.06862, consistent with our enclosures. LANCELOT's chain400 value 5.06788 lies below our certified dual, a tolerance artifact.
  - catmix: LOQO −4.80694e-2, −4.80591e-2, −4.80565e-2, −4.80559e-2 (violations 1.2e-8 to 7e-8). COPS notes nonunique singular controls ("bang-singular-bang"), consistent with the chattering of our best points.
  - COPS 3.0 catmix uses collocation, a different model (−4.80556e-2).
- **MINLPLib and GLOBALLib** (`bussieck2003-minlpliba-collection-of-test-models`, `cache2026-minlplib-pages-for-43-target`, `coconut2026-globallib-gams-coconut-and-minlplib`).
  - The instances were added 31 Jul 2001; their p1 points date from 2014 and their duals from 2014–2020.
  - COCONUT records local values (modelstatus 2), e.g. chain50 5.0723 and catmix −0.0481. Neumaier et al. report aggregates only (`neumaier2005-a-comparison-of-complete-global`).
- **Global solvers on these instances.**
  - The ANTIGONE 1.0 test suite (Misener–Floudas 2013) lists catmix and chain without per-instance results; the ANTIGONE and GloMIQO papers (`misener2014-antigone-algorithms-for-continuous-integer`, `misener2013-glomiqo-global-mixed-integer-quadratic`) were not read for per-instance values.
  - The SCIP 8 suite report (`bestuzheva2021-the-scip-optimization-suite-8`) shows gap ∞ for chain50–400 and catmix100–800 under both expression frameworks. Mattick–Mutschler (`mattick2023-reinforcement-learning-for-node-selection`) also reports ∞ for catmix.
  - Müller et al.'s surrogate duals (`muller2022-on-generalized-surrogate-duality-in`) are negative for chain.
  - Smith 2011 (`smith2011-improved-placement-of-local-solver`; full text not in the library) gives catmix800 −0.048055605, worse than our points.
- **Hanging chain.**
  - Griva–Vanderbei (`griva2005-case-studies-in-optimization-catenary`) remark that "it is apparently not possible to make a convex model when parameterizing along x", which is exactly the COPS parameterization.
  - Gabrys–Sremac (`gabrys2025-a-convex-optimization-approach-to`) give a convex model of the *fixed-link-length* discrete chain with free 2-D joints. That is a different model, and they use no calibration.
  - The continuous catenary's Weierstrass sufficiency theory (Cesari 1983; `denzler1999-catenaria-verathe-true-catenary` for a variant) does not bound the discrete model. Proposition C6 is its discrete analogue for this transcription. It was not found stated in the verifier's or the calibration scouting's brief searches; this is a weak "not found", not a novelty proof.
- **Global dynamic optimization** (`chachuat2005-global-mixed-integer-dynamic-optimization`, `houska2015-stable-set-valued-integration-of`; Esposito–Floudas; occupation measures). These treat continuous-time problems; none was found applied to these discretizations.
- **Mechanisms.**
  - Both certificates are discrete verification functions in Krotov's sense (`krotov1967-sufficient-conditions-for-the-optimality`), that is, Bellman inequalities. Related: relaxed and approximate DP (`lincoln2006-relaxing-dynamic-programming`, `rantzer2005-on-approximate-dynamic-programming-in`).
  - Interval branch and bound and directed rounding are standard (`kearfott1996-rigorous-global-search-continuous-problems`, `hansen2004-global-optimization-using-interval-analysis`, `rump2010-verification-methods-rigorous-results-using`).
  - Piecewise-linear lower interpolation of concave, homogeneous value functions on a projective state is standard in spirit. Its use to certify a global optimum of a transcribed singular-arc problem was not found.

## 8. Critical examination

### 8.1 Re-derivation

I re-derived every step independently; Section 3 gives the proofs in my
form.

**chain.**
- Polyline form and end-piece weights: correct. The OSIL η decimals equal 1/(2N) exactly.
- Lemma C3: each identity, the AM–GM remainder and φ′ check out symbolically. Equality holds if and only if D = τ.
- Theorem C4 uses only λ_k ≥ h and the length row (to eliminate L), both of which hold for every feasible point. No box on interior heights is used. Multipliers may depend on the box.
- Lemma C5: valid necessary conditions; both root boxes contain the region.
- Both B&Bs:
  - the mean-value gradient formula agrees with symbolic differentiation;
  - B_N is C¹ on ℝ², because η > 0 keeps λ_0 and λ_N smooth;
  - the float midpoint lies in the box;
  - asinh is enclosed monotonically, including for intervals that contain 0;
  - the certified value is the binary64 target, not float(min leaf). In the verifier's code these coincide here (`exact_display_checks.log`: min leaf ≥ target for all four N).
- New: Proposition C6 shows the reduction is exact. This explains why both B&Bs reach any target slightly below the KKT value.

**catmix.**
- Row structure, P and Q, Q = 2I − P: correct, and confirmed exactly from the OSIL file.
- Nonnegativity: Lemma M1 gives a short proof for all four N and for c = 9a.
- Reduction: each control appears in exactly one factor.
- Concavity, homogeneity, chord minorant and induction: correct.
- Index bookkeeping in both codes: terminal → stages → initial uses u_N, u_{N−1}..u_1, u_0. Correct.
- `v_catmix_dp.py`: I re-read `qmin_lb`/`peval_lo` (lower coefficients valid for u ≥ 0; vertex test padded by 1e-12), `dinkelbach` (sign-dependent D_min/D_max), the crude bound (needs w ≥ 0, ensured by clipping), the cone-verification loop, the coverage of [0, 1] (0 and 1 are cut points of every ray), `fr_iv` (correct one-sided widening) and the final `dn(w0 − 1)`. No validity problem.
- `catmix_bound.py`: I re-read the candidate-cone filter (necessary conditions only), `mv_lb` (Taylor cases, monotone cases, f″ formula), the many-cone Lipschitz bound and the leaf logic (every subinterval ends as a leaf or the run raises). No validity problem.

### 8.2 Checks run for this dossier (targeted; copies under /tmp; one thread)

First pass (top level of `chain-catmix-checks/`):
1. `chain_checks.py`: sympy identities; gradient of B_N vs symbolic; a 20,000-case 50-digit lemma test (min slack/H² = +3.6e-30); B_N at the double points' ends equals the KKT value to 30 digits.
2. `chain_osil_check.py 50 100 200 400`: independent xml.etree reader; objective, length row and linear rows equal the piece form to ≤ 1.4e-48.
3. Authors' `chain_bound.py` with the rigorous pruning patch, N = 50..400: identical certificates, 0 unresolved.
4. `catmix_exact.py`: regex scan of the catmix OSIL constants; exact simulations under c_N and 9a.
5. `xcheck.py 100 coarse 99` and `xcheck.py 100 fine 40`: per-stage cross-check of the two catmix stage routines.

This pass (`chain-catmix-checks/r2/`, with logs in `r2/logs/`):
1. `python3 lemma_checks.py`: sympy re-check of Lemma C3 (identities, AM–GM remainder, φ(τ) = 0, φ′); 3,000-case 40-digit test of Theorem C4's interior inequality, including exact discrete catenaries (equality); stationarity of the Proposition C6 multipliers.
2. `python3 chain_osil_check.py 50 100 200 400` (rerun): same residuals as the first pass.
3. `python3 chain_bound.py 1e-14 50`, patched copy (spot rerun): 11,121 boxes, 61 infeasible, 0 unresolved, target 5.072261493982863.
4. `python3 exact_catmix.py 100 200 400 800`: a fresh xml.etree reader of the catmix OSIL (pattern, bounds, objective, exact constants) and exact Fraction simulation of all saved control vectors under c_N and 9a. All values agree with the first pass and the record; catmix400 is now exact.
5. `python3 lin_check.py 100 200 400 800`: all linear coefficients exact.
6. `python3 gaps.py`: exact gaps, safe displays, relative gaps and listed-primal comparisons from the logged binary64 duals and the exact primal values.
7. `python3 xcheck.py 100 coarse 12` (spot rerun): identical to the first-pass log.
8. `python3 grid_diag.py`: float diagnostic of the authors' catmix100 grids (band spacing 1e-6 at every stage; window spacing at the primal θ from 1.1e-7 to 3.5e-6).
9. A float sanity check of max_u column sums of M(u) for N = 100: 1.0000000000000002, which is rounding at 1. Lemma M6 proves ≤ 1.

### 8.3 Findings and proposed resolutions

**None of the findings invalidates a claimed bound, point or gap.**

- **CC-1 (resolved here; needs one independent read).** The caveat "OSIL coefficients differ from GAMS; no exact transport" can be dropped for catmix duals. Proposition M8 proves that the OSIL lower bounds hold for c = 9a, and the primal shifts are computed exactly. The exact-model gaps are ≤ 1.86e-13 (1.65e-13 with the Newton point), 1.90e-11, 6.81e-11 and 1.49e-10. Resolution: an independent reviewer reads Lemma M1 and Proposition M8 (about 15 minutes). The exact simulations already show J_{9a} − J_{c_N} > 0 for every saved point, as M8 predicts.
- **CC-2 (wording).** The strongest catmix duals (the summary's gap duals) were computed by one implementation, `v_catmix_dp.stage`; the recheck reused it unchanged. The authors' independent code certifies bounds lower by 7.7e-12, 1.6e-12, 1.26e-10 and 3.61e-10. Do not write "two independent implementations certify the stated bounds". Write instead: "computed by one implementation; a second, independent implementation agrees with it per stage within 1e-14 on identical inputs and certifies, end to end, bounds weaker by at most 3.7e-10." Optional: run the authors' `catmix_bound.py` on the recheck's final grids (about 1–1.5 h per instance, single thread, after adapting its grid input).
- **CC-3 (trust base, optional).** Both chain B&Bs use mpmath `iv` (sqrt, log). A third arithmetic, for example Arb via python-flint, could re-run the 2-D B&B. Cost: about 1–2 h of coding and under 5 min of run time for all four N (python-flint is not installed). This is not needed if mpmath `iv` is listed as a trusted component, as for the other families. The catmix dual needs no transcendental function; state this.
- **CC-4 (resolved).** The authors' chain pruning test squares one endpoint without directed rounding. The one-line patch reproduces identical certificates (spot-checked again in this pass). Either add the patch to the reproduction package, or cite the verifier's B&B, which was rigorous from the start, as the certificate of record.
- **CC-5 (resolved here).** The catmix400 gap relied on a 60-digit mpmath enclosure of the authors' point. That point's objective is now exact (Fraction arithmetic, 0.4 s), so no catmix number depends on mpmath.
- **CC-6 (corrects an older statement).** "The listed primal values are optimal to their printed digits" (`R/open-instances-wave2/cops/report.md` §2) is false for chain400: the page shows 5.0686217, but the optimum prints as 5.06862169. At the 10 decimals of `minlplib.solu`, the listed chain100/200/400 points are suboptimal by at least 2.1e-10, 1.5e-10 and 3.4e-10. Resolution: in the paper, say that our exact points improve the listed primal values of chain100/200/400 slightly (≥ 1.5e-10) and of catmix100–800 by ≥ 2.2e-8. No computation needed.
- **CC-7 (corrects two remarks in the verification report).**
  - "Gap ×1/16 per halving of the spacing" should read "per quartering": the spacings were 2^-9, 2^-11, …. This is second order.
  - The suggestion that the authors' extra catmix100 slack is "a grid-independent loss in their stage minimization" is contradicted by Lemma M6 and the logged per-stage loss ≤ 9.99e-15: at most about 1.0e-12 of the 7.92e-12 comes from stage minimization. The rest is grid interpolation, whose exact location in the authors' grid this pass did not identify.

  No result depends on either remark.
- **CC-8 (bookkeeping).** The READINESS runtime table quotes the authors' catmix runs (1049/1728/3001/4602 s), which produce the weaker bounds. The summary duals took 2,358/1,170/2,578/2,595 s in the original runs (46.0/20.2/45.2/46.1 min in the reproduction). Report both in the paper.
- **CC-9 (display consistency).** The summary's catmix dual cell (−0.04806944 … −0.04805591) comes from the authors' duals, while its gaps use the verifier/recheck duals. The paper should give per-instance safe displays of the duals actually used (Section 5). Never use the five shortest-repr strings listed there.
- **CC-10 (wording).**
  - "Exact DP" should read "rigorous DP lower bound on an exact 1-D projective reduction".
  - "The discrete optimum chatters" should read "our best feasible points chatter".
  - "Equality in the lemma along the optimal chain" is now proved for every slice (Proposition C6), but it is not a statement about the global optimum's location.
- **CC-11 (new statements need a read).** Proposition C6, the short proof of Lemma M1, Lemma M6 and Proposition M8 are new in this dossier. Each is elementary and short, and none is needed for the validity of the stated bounds except M8, and M8 only for the GAMS-model claim. Resolution: one independent read, about 30–45 minutes in total.
- **CC-12 (re-checkability, optional).** The per-stage chord values w are not saved, so checking catmix means re-running (about 45 min per instance). Saving (grid, w) per stage (about 17 MB for N = 800) would let others re-check stages independently and in parallel. Cost: one rerun per instance with an extra save, about 3.3 h total single-threaded.
- **CC-13 (novelty).** All eight instances are "new as far as found" (control literature report). Novelty of the chain lemma and of Proposition C6 rests only on brief searches, and the ANTIGONE 1.0/GloMIQO per-instance results were not seen. Use "to the best of our knowledge".

### 8.4 Verdict

The chain certificate has a complete proof (Lemmas C1–C3, C5, Theorem C4).
Its only computer-assisted part is a 2-D interval B&B, implemented twice
independently and reproduced bit for bit. Proposition C6 now shows that the
end-window reduction is exact. The catmix certificate has a complete proof of
the DP principle (Lemmas M1–M4, Theorem M5). Its computer-assisted part uses
only directed binary64 arithmetic for + − × ÷, and two implementations agree
per stage. Both primal sides are exact. The claimed enclosures stand.

## 9. What the paper may and must not claim

**May claim.**
- "For chain50, chain100, chain200 and chain400 we enclose the optimal value of the MINLPLib model in an interval of width at most 1.01e-14 (relative 2.0e-15). The lower end is proved by a closed-form discrete catenary calibration, which reduces the problem exactly to its two end values, and a two-dimensional interval branch and bound. The upper end is the exact objective of a feasible point with coordinates in a real quadratic field."
- "For catmix100–800 we enclose the optimal value of the MINLPLib model to within 1.85e-13, 1.90e-11, 6.81e-11 and 1.49e-10 (absolute). The lower bounds also hold for the exact-coefficient GAMS model (c = 9a)." Use the second sentence only after CC-1's read.
- "The catmix lower bound uses only outward-rounded binary64 addition, subtraction, multiplication and division; the chain lower bound uses mpmath interval arithmetic, including sqrt and log."
- "To the best of our knowledge, no global optimality certificate, rigorous or floating-point, had been published for these eight instances. MINLPLib lists none of them as solved; the best listed dual bounds are 0.08–0.17 for chain (optimum ≈ 5.07) and between −0.067 and −1.49 for catmix (optimum ≈ −0.048)."
- "Our exactly feasible catmix points improve on MINLPLib's best known values by at least 2.2e-8 (catmix200) and up to about 6.2e-8 (catmix800); for chain100–400 the improvement is at the 1e-10 level."
- "In one-hour runs, several primal values returned by BARON, GUROBI and SCIP lie below our certified lower bounds, so they are feasible only within tolerance."
- "For fixed end values, the discrete catenary is the unique global minimizer of the COPS chain's interior energy (a discrete Weierstrass theorem)." Use this only after CC-11's read.

**Must not claim.**
- Exact optimal values. We give enclosures; in this paper only camshape and hvycrash are exact.
- That the catmix discrete optimum chatters, or that the DP bound is "exact".
- That two independent implementations certify the stated, strongest catmix bounds (CC-2).
- Any result for COPS 3.0 catmix (a different discretization), for the continuous problems, or for the fixed-link-length discrete chain.
- Shortest-repr decimals as bounds (Section 5 list).
- That the chain bound needs no trusted component (mpmath `iv`), or that the catmix bound needs none (IEEE semantics, code correctness).
- That the listed chain primal values are optimal to their printed digits (CC-6).
- Unqualified priority ("first") without "to the best of our knowledge".

## 10. Candidate figures and tables

1. **Table (instances and status):** N, variables, rows, MINLPLib type, best listed dual (solver, date), listed primal, solved mark (Section 2).
2. **Table (results):** safe dual, primal upper display, absolute and relative gap, effort for the certificate of record and the second implementation (Section 5).
3. **Figure (chain field):** the optimal discrete chain for N = 50 with the end window marked. Inset: asinh(v_k/H) against k, a straight line of slope 2τ, which shows equality in Lemma C3 along the optimum. Data: saved primal vectors and multipliers; no new run.
4. **Figure (chain end window):** F(z_1, z_N) = max_{V,H} B_N over Ω_N (Proposition C6), with the B&B leaf boxes and the chord-infeasible region. Needs a 10–30 s rerun that dumps the leaves.
5. **Figure (catmix controls):** u_i against t_i for the best points at N = 100…800, showing bang, the chattering singular arc and bang (saved `.npy` files).
6. **Figure (catmix DP):** (a) gap against uniform grid spacing on log–log axes (slope 2; Section 3.2); (b) the θ-trajectory with the core and shell bands and the dependence bundle (`R/reviews/catmix-recheck-checks/logs/tree*.json`).
7. **Schematic:** the projective reduction y ↦ (ρ, θ) and the chord minorant under a concave V.
8. **Table (verification matrix):** each component, the codes that check it, the arithmetic and the trusted items (Section 6).
