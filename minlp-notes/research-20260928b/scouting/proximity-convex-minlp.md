# Scout report: proximity for convex and structured MINLP (`proximity-convex-minlp`)

Date: 2026-09-28. Scratch code and outputs: `research-20260928b/scouting/proximity-convex-minlp/`.

## Summary

The proximity theory for nonlinear integer programs is thin. It consists of results for separable convex objectives, a few Hessian-dependent bounds for convex quadratics, and results for discrete-convex function classes. The brief's central question is how the Hessian should enter a Cook–Gerards–Schrijver–Tardos (CGST) or Steinitz-type bound. This report gives a partial answer.

- **Steinitz regime (standard form, dimension-free).** The right invariant is combinatorial. An integral rank-`k` non-separable part `W^T Λ W` acts exactly like `k` extra equality rows. The upper bound follows by lifting to a separable problem. The matching lower bound follows by penalty simulation. Conditioning does not matter. Bounded Hessian entries or subdeterminants alone cannot give dimension-free bounds; a Hessian with entries at most 5 already has proximity `(2^n-1)/2`.
- **Cook regime (inequality form).** The exact unconstrained invariant is `ρ∞(Q)`, the `ℓ∞` radius of the `Q`-norm Voronoi cell of `Z^n`. The natural conjecture `prox ≤ C(n)·Δ(A)·ρ∞(Q)` is **false**. Using simultaneous Diophantine approximation, we found a 3-variable family with `Δ(A) = 1` in which the ratio grows like `R^{1/12}`. We confirmed it numerically. The corrected conjecture uses Voronoi radii of the face sublattices `ker(A_S) ∩ Z^n`.
- The best open question is this corrected, sublattice-aware Cook theorem for convex quadratic integer programming (IP). The report gives a proof strategy (an exchange lemma that reduces proximity to a lattice-point problem) and names the main technical obstacle. It is interesting theory, but its solver impact is indirect. Score: **4/10**.

## 1. Frontier map

Notation: `P = {x : Ax ≤ b}` with `A` integral. `Δ(A)` is the largest absolute subdeterminant, and `Δ` alone means the largest absolute entry in standard-form statements. `x*` is a continuous optimum and `z*` an integer optimum. `φ` is the number of fractional entries of `x*`.

### 1.1 Linear and mixed-integer linear (baseline)

| Result | Form and assumptions | Bound |
|---|---|---|
| Cook–Gerards–Schrijver–Tardos 1986 | `max c^T x`, `Ax ≤ b`, any linear-programming (LP) optimum `x*`, pure integer | `‖x*−z*‖∞ ≤ n·Δ_{n−1}(A)`, independent of `b, c` |
| Celaya–Kuhlmann–Paat–Weismantel (arXiv:2111.01782, 2211.14941; MOR 2024) | as above, `b` integral, `x*` a vertex, `n ≥ 2` | `< (4n+2)/9 · Δ_{n−1}(A)`. Whether CGST is tight for integral `b` is open. Paat–Weismantel–Weltge conjecture an `n`-free bound. |
| Paat–Weismantel–Weltge (arXiv:1801.08751; MP 2020) | mixed-integer, `Ax ≤ b` | bound in terms of `Δ` and the number of integer variables only; conjecture: `Δ` only |
| Eisenbrand–Weismantel (arXiv:1707.00481; TALG 2019) | standard form `Ax=b, 0≤x≤u`, `‖A‖∞ ≤ Δ`, optimal vertex | `‖x*−z*‖1 ≤ m(2mΔ+1)^m`, dimension-free |
| Lee–Paat–Stallknecht–Xu (arXiv:2001.04659, 2105.08160) | standard form | sparsity-based improvements; bound polynomial in determinants and `m` for box-constrained IPs |
| Aliev–Averkov–Jones–Oertel (arXiv:2606.13579, June 2026) | standard form, `b` integral, rank `m` | Euclidean proximity `≤ √det(AA^T) − 1`, asymptotically tight |
| Oertel–Paat–Weismantel (arXiv:1907.07960) | parametric in `b` | typical proximity is much smaller than worst case |
| Berndt–Jansen–Lassota (arXiv:2010.09255) | configuration-type ILPs, nonnegative `A`, integral `b` | lower bound `Δ^{Θ(d)}`: the CGST/EW-type exponent is tight |
| Oertel–Paat–Weismantel colorful Steinitz (arXiv:2201.05874) | block-structured | proximity for block IPs |

### 1.2 Separable convex objectives

| Result | Assumptions | Bound |
|---|---|---|
| Hochbaum–Shanthikumar 1990 (local `hochbaum1990-convex-separable-optimization-is-not`) | separable convex `Σ f_i(x_i)`, `Ax ≤ b`, pure integer; also proximity between scaled grids | `‖x*−z*‖∞ ≤ nΔ(A)`; proximity-scaling algorithm |
| Granot–Skorin-Kapov 1990 (MP 47) | separable convex quadratic; the abstract also claims validity for nonseparable mixed-integer quadratic programs | `nΔ(A)`. **Not verified:** the paper is paywalled, and we could not check which matrix's subdeterminants govern the nonseparable version. The most likely invariant is `Δ` of `A` stacked with a factor of the Hessian. |
| Werman–Magagnosc 1991 (MP 51) | convex (Del Pia–Ma describe it as separable) | `nΔ`. Paywalled; not verified. |
| Hemmecke–Köppe–Weismantel (arXiv:1207.1149) | separable convex, block-structured, Graver-based | `‖·‖∞ ≤ n·(max Graver ‖·‖∞)` |
| Hunkenschröder thesis Prop. 2.24 (quoted in Hunkenschröder–Pokutta–Weismantel, HPW) | separable convex, `Ax=b, l≤x≤u` | `‖x*−z*‖1 ≤ φ·γ(A)`, with `γ(A) ≤ (2m‖A‖∞+1)^m` |
| Brand–Koutecký–Lassota–Ordyniak (arXiv:2111.08048; ESA 2024) | separable convex, **mixed** integer, standard form | Lemma 5: proximity ≤ mixed Graver *weight* `wt^X_p(E)`. Open (their §8): can the weight be bounded by the mixed Graver norm? Separable-convex mixed n-fold and 2-stage problems are harder than their linear counterparts. |
| Hunkenschröder–Koutecký–Levin–… (arXiv:2505.22212, 2025) | separable convex, small treedepth | near-optimal algorithms via scaling, proximity and sensitivity |
| Ligthart (arXiv:2606.30330, June 2026) | separable convex value functions | periodic convexity (Graver-based) |

### 1.3 Non-separable and nonlinear objectives

| Result | Assumptions | Bound or statement |
|---|---|---|
| Baldick 1995 (DAM 61) | non-separable integer quadratics | Linear transformation to a separable frame, followed by Hochbaum–Shanthikumar. A "slight generalization" of ILP with a non-separable nonlinear objective and totally unimodular (TU) constraints is NP-hard. Abstract only. |
| Sun–Li 2001 (ORL) | convex quadratic, also convex and mixed-integer convex | distance bound in terms of the Hessian condition number (search snippet; paywalled, not verified) |
| Sankaranarayanan 2024 (SSRN 4827001, quoted in local `sankaranarayanan2024-…`) | unconstrained, `Q ≻ 0` | `π(Q) ≤ (φ_n/4)·√κ(Q)`, with `φ_n` the flatness constant; holds for all integer minimizers |
| Hunkenschröder–Pokutta–Weismantel (local `weismantel2023-…`; SIOPT) | `g(Wx)` over `{0,1}^n`, `W ∈ Z^{m×n}` | separable `g`: `δ ≤ 2m(2m‖W‖∞+1)^m` via lifting; sharp `g`: bound in `L, μ, θ`. For general convex `g`, proximity can be very large. |
| Dadush–Léonard–Rohwedder–Verschae (local `verschae2023-…`; arXiv:2303.02474) | `g(Wx)+c^Tx`, boxes, arbitrary `g` | avoid proximity entirely (guess `Wx*`) |
| Del Pia–Ma (arXiv:2006.01718; MP 2022) | separable concave quadratic IP, `Ax ≤ b` | no exact proximity; `ε`-approximate proximity `nΔ(10Δ/ε+1)^k`, with lower bounds |
| Del Pia 2019 (local `pia2019-…`) | separable concave IQP | approximation via subdeterminants |
| Murota–Tamura 2004; Moriguchi–Shioura–Tsuchimura 2011 (SIOPT 21) | L♮- and M-convex functions (discrete convexity) | Scaling proximity. Real-vs-integer proximity for M-convex functions; we recall the bound as `n−1` but checked only the abstract. |
| Moriguchi–Murota–Tamura–Tardella (arXiv:1703.10705; MP 2019), Murota–Tamura survey (arXiv:2211.10912) | integrally convex (includes diagonally dominant quadratics) | proximity holds with a superexponential bound in `n`; scaling fails for `n ≥ 3` |

### 1.4 Nonlinear constraints

- **Kocuk–Morán, arXiv:2501.00638.** Version 1 (Dec 2024) was titled "Proximity results in convex mixed-integer programming". We read it in full (`src/kocuk-moran-v1.txt`).
  - For recession cones and single Lorentz cones it gives bounds in terms of the data and a covering radius.
  - Its Proposition 6 for ellipsoids bounds the distance to the nearest *feasible* integer point, not to an *optimal* one.
  - Examples 5–7 show that proximity and the integrality gap depend on the right-hand side, with growth `~√N`. This holds for a ball plus a halfspace and for two balls; after scaling, the data are integral.
  - Version 2 (April 2026, local `ramirez2026-…`) is retitled "On the integrality gap…". Its §7 explicitly says no proximity analysis was carried out and names mixed-integer second-order cone programs (MISOCPs) as future work. The status of the v1 proximity claims is therefore unclear.

### 1.5 Solver use

- Proximity drives proximity-scaling for convex separable flows and resource allocation (Hochbaum; Moriguchi–Shioura–Tsuchimura).
- It also drives Steinitz dynamic-programming and parameterized algorithms (Eisenbrand–Weismantel, Jansen–Rohwedder, block-structured IPs).
- In general-purpose mixed-integer quadratic programming (MIQP) and MINLP solvers, a priori proximity bounds are not used for domain reduction; they are far too large. What solvers do use is the incumbent ellipsoid `‖z−x*‖²_Q ≤ 2(f(z_inc)−f(x*))`. It is used in convex QIP branch-and-bound, `ℓ0`-regression safe screening, and GNSS LAMBDA-style search after decorrelation.

### 1.6 Sources examined and what was checked

- **Local literature.** Read the proximity statements and examples:
  - `hochbaum1990-convex-separable-optimization-is-not`, `pia2019-subdeterminants-and-concave-integer-quadratic`;
  - `weismantel2023-minimizing-a-low-dimensional-convex` (Theorems 4.1 and 4.4, and Prop. 2.24 as quoted);
  - `verschae2023-optimizing-low-dimensional-functions-over`;
  - `ramirez2026-on-the-integrality-gap-of` (the v2 disclaimer);
  - `sankaranarayanan2024-proximity-based-approximation-algorithms-for` (Definition 5, Proposition 2, Lemma 5).

  `cslovjecsek2021-…` and `koppe2012-…` were identified but not read in depth. `notes/candidate-directions-2026-09-05.md` (row 3, mixed-integer separable proximity) was proposed but never pursued.
- **Downloaded full texts** (`src/*.txt`): Kocuk–Morán v1; Del Pia–Ma 2006.01718 (introduction and Theorem 1); CKPW 2211.14941 (introduction and Theorems 1–2); CKPW 2111.01782 (not read in detail); Brand et al. 2111.08048 (Lemma 5, Theorems 2–6, §8); Oertel–Paat–Weismantel 2201.05874 (abstract); Hochbaum 2007 survey (§3.2 proximity theorem).
- **Abstracts only** (arXiv API, Semantic Scholar, publisher pages): 1707.00481, 1803.04744, 1801.08751, 2001.04659, 2105.08160, 1907.07960, 1907.07886, 2010.09255, 2606.13579, 2606.30330, 2505.22212, 1207.1149, 1703.10705, 2211.10912, 2412.15940, ESA 2024 (LIPIcs 308:32), Baldick 1995, Moriguchi–Shioura–Tsuchimura 2011.
- **Titles and search snippets only:** Granot–Skorin-Kapov 1990, Werman–Magagnosc 1991, Sun–Li 2001.
- **Keyword searches** (web search, then the arXiv API after the web-search quota ran out): proximity together with quadratic, separable convex, Steinitz, mixed-integer convex, integrally convex, and the author names Paat and Oertel. None turned up a Cook-type theorem whose Hessian invariant is lattice-geometric (a Voronoi or covering radius), and none turned up a treatment of the sublattice effect in §3.3. **An unsuccessful search does not establish novelty.**

## 2. Open questions

**OQ1 (best): which Hessian invariant governs Cook-type proximity for convex quadratic IP?**

For `min ½x^TQx + c^Tx`, `Ax ≤ b`, `x ∈ Z^n`, define

    ρ_A(Q) = max over S ⊆ rows of ρ∞(Q; ker(A_S) ∩ Z^n)

(with `S = ∅` giving `Z^n`). Here `ρ∞(Q; L)` is the `ℓ∞` radius of the `Q`-Voronoi cell of the lattice `L`, taken within `span L`.

Conjecture C1\*: `prox ≤ C(n)·Δ(A)^{O(1)}·max(1, ρ_A(Q))`, independent of `b`, `c` and the conditioning of `Q`. The weak form asks only for `prox ≤ F(n, Δ(A), ρ_A(Q))`.

- **Why it is open.** Known bounds use a different invariant: `√κ(Q)` (Sun–Li; Sankaranarayanan; §3.2), a factor subdeterminant (Granot–Skorin-Kapov, Baldick, lifting), or sharpness parameters (HPW). Each can be exponentially loose relative to `ρ_A` (§3.4).
- **Why the refinement is needed.** The global-Voronoi form C1 is false (§3.3).
- **What is established.** C1\* holds for `Q = 0` (CGST), for diagonal `Q` (Hochbaum–Shanthikumar, where `ρ = ½`), for `A = ∅` (exactly), and for lattice-separable `Q` in a weaker polynomial form (§3.2).

**OQ2: Steinitz regime with real low-rank Hessians.**

For standard form with `Q = Diag(d) + W^T H W`, where `W ∈ Z^{k×n}` and `H ≻ 0` is `k×k` and **not** diagonal or integral, what is the tight dependence on `H`?

- Known: HPW's sharpness bound for the cube (condition-number type).
- Lower bound: already for `n = k = 2` with no constraints, proximity is at least of order `√κ(H)` (§3.4). The conjectured answer is `φ·(O((m+k)Δ))^{O(m+k)}·max(1, ρ∞(H; lattice))`.
- If `H` is integral, the question reduces to the diagonal case (§3.1).

**OQ3: curved constraints (MISOCP).**

For `P ∩ {‖G x − p‖ ≤ R}` with integral `A` and `G`, is optimal-to-optimal proximity `Θ(√R)` up to factors in `n`, `Δ(A)` and `G`?

- A single ball with integral data and a linear objective already gives `Θ(√R)` (§3.4, E3).
- Kocuk–Morán's examples give `√N` for a ball plus a halfspace and for two balls. Their v2 dropped proximity entirely.
- The open part is a general upper bound once polyhedral constraints are present. The obstruction here is lattice points near curved boundaries (convex hulls of lattice points in a disk have edges of length `≈ R^{1/3}` to `R^{1/2}`).

**OQ4: mixed-integer convex problems with many continuous variables.**

- Is proximity for separable convex MINLP bounded by a function of `(n_I, Δ(A))`, independent of `n_C`? This is the convex analogue of Paat–Weismantel–Weltge. We believe it follows by combining their Olson-type argument with the conformal exchange, but we did not check this.
- When the continuous variables are coupled through a non-separable Hessian, projecting them out yields a pure-integer problem whose Hessian is the Schur complement. OQ4 then reduces to OQ1 applied to that Schur complement.
- Brand et al.'s question — can the mixed Graver weight be bounded by the mixed Graver norm — is the standard-form counterpart.

Considered and not pursued: proximity to the perspective relaxation in indicator QPs (support-recovery and screening type). It overlaps the repository's indicator-quadratic work.

## 3. First-pass mathematics

All computations are exact (fractions and exhaustive enumeration over regions proven to contain every optimum) unless marked as floating point.

### 3.1 Steinitz regime: an integral rank-`k` part costs exactly `k` rows

**Proposition S (upper bound; folklore, following HPW Theorem 4.1).** Let `Q = Diag(d) + W^TΛW`, with `d ≥ 0`, `Λ ≻ 0` diagonal (any scale) and `W ∈ Z^{k×n}`. Consider `Ax = b`, `l ≤ x ≤ u`, `x ∈ Z^n`.

1. All continuous optima share `Qx`. So `x*_i` is fixed wherever `d_i > 0`, and `y* = Wx*` is fixed.
2. Choose a vertex of `{Ax=b, Wx=y*, bounds, x_i = x*_i for d_i > 0}` that is optimal for `c`. It has at most `m+k` fractional entries among the coordinates with `d_i = 0`.
3. The lifted problem, with matrix `[A 0; W −I]` and objective separable in `(x, y)`, satisfies Hunkenschröder's Prop. 2.24. This gives

       ‖(x̂,y*) − (z,Wz)‖1 ≤ φ̂·(2(m+k)Δ′+1)^{m+k},  Δ′ = max(‖A‖∞, ‖W‖∞, 1),

   where `φ̂ ≤ #{i : d_i>0, x*_i ∉ Z} + m + 2k`. The bound does not depend on `d` or `Λ`.

**Proposition S′ (matching lower bound by penalty simulation).** Take an ILP with rows `[A; W]`, integral `β`, a bounded box, and unique LP optimum `x̄`. Its integer optima coincide with those of `min c^Tx + M‖Wx−β‖²` over `Ax=b` for `M` large. The continuous optima `x*_M → x̄`. So every ILP proximity lower bound with `m+k` rows (e.g. Berndt–Jansen–Lassota `Δ^{Θ(d)}`) transfers to an MIQP with `m` rows and Hessian `M·W^TW`.

**Obstruction.** Bounded Hessian entries cannot replace factor rank. For `D = I − 2S` (lower bidiagonal) and `Q = D^TD`, every `|Q_ij| ≤ 5`, yet the unconstrained proximity is exactly `ρ∞(Q) = (2^n−1)/2` (E2 below). So no bound of the form `φ·F(m, Δ, ‖Q‖∞)` exists.

### 3.2 Cook regime: established facts

- **(U) Exact unconstrained invariant.** For `Q ≻ 0`, `sup_c min_{z* optimal} ‖z*−x*‖∞ = ρ∞(Q)`, the `ℓ∞` radius of the `Q`-Voronoi cell of `Z^n`. Two general bounds:
  - `ρ∞(Q) ≤ ½·(tr Q · max_i (Q^{-1})_ii)^{1/2}`, which for integral `Q` is `≤ ½(nΔ_1(Q)Δ_{n−1}(Q)/det Q)^{1/2}`.
  - `‖z*−x*‖2 ≤ ½(tr Q/λ_min)^{1/2} ≤ ½√(nκ)` for **all** integer minimizers. This improves Sankaranarayanan's `(φ_n/4)√κ` by a factor of order at least `√n`. The proof uses the nearest-plane covering-radius bound.

  The bidiagonal family attains the upper bound within `O(√n)`. For example, at `n = 12`, `ρ = 2047.5` against the bound `8848`.
- **(L) Linearization lemma (all optima).** Let `g = ∇f(x*)` and let `z′` be any integer optimum of `min{g^Tx : x ∈ P ∩ Z^n}`. Then every integer optimum `z` satisfies `‖z−x*‖_Q ≤ ‖z′−x*‖_Q`. The proof is one line:

      ½‖z−x*‖²_Q = f(z) − f(x*) − g^T(z−x*) ≤ ½‖z′−x*‖²_Q + g^T(z′−z).

  With CGST this gives `‖z−x*‖_Q ≤ n^{3/2}Δ(A)λ_max^{1/2}`, and hence `‖z−x*‖2 ≤ n^{3/2}Δ(A)√κ`. Checked exactly on 152 integer optima from random 3-variable instances; no violations (`check_linearization.py`).
- **(E) Exchange lemma** (reformulates proximity as geometry of numbers). Let `Q ≻ 0` and let `z` be the integer optimum closest to `x*` in `Q`-norm, with `h = z−x*`. Then **no** integer `g ≠ 0` satisfies both
  - `Ag ⊑ Ah` (for every row, `A_jg` has the sign of `A_jh` and `|A_jg| ≤ |A_jh|`), and
  - `g^TQ(h−g) ≥ 0` (`g` lies in the Thales ellipsoid with diameter `[0,h]`).

  Proof: `f(z−g) + f(x*+g) = f(z) + f(x*) − g^TQ(h−g)`, and `‖h−g‖²_Q < ‖h‖²_Q`. Hence `prox ≤ T(A,Q) := sup{‖h‖∞ : no such g}`. With `A = ∅` this reduces exactly to Voronoi: `T(∅,Q) = 2ρ∞(Q)`.
- **(LS) Lattice-separable Hessians** (essentially Baldick's 1995 transformation combined with Hochbaum–Shanthikumar). If `Q = U^TDU` with `U` unimodular and `D ⪰ 0` diagonal, then `prox ≤ n‖U^{-1}‖_{∞→∞}·Δ(AU^{-1})` for every `D`, including arbitrarily ill-conditioned ones. Here `ρ∞(Q) = ½‖U^{-1}‖_{∞→∞}`. By Cauchy–Binet, `Δ(AU^{-1}) ≤ 2^nΔ(A)·max_k Δ_k(U^{-1})`, so `prox ≤ C(n)Δ(A)·ρ^{O(n)}`.

### 3.3 The global Voronoi conjecture is false; the sublattice version survives

Take `Q = R·ww^T + I` on `Z^3` with `w = (1, −α, −β)`, and let the constraint rows be `±e_3`, i.e. `x_3 = 0`, so `Δ(A) = 1`. The constrained problem is exactly the unconstrained 2-D problem with the `2×2` block `Q_SS`, so `prox ≥ ρ∞(Q_SS)`.

- In the plane, bad approximability of `α` (e.g. `√2`) forces `λ_1(Q_SS) ≳ R^{1/4}`. The Voronoi cell contains a `Q`-ball of that radius, stretched along the cheap direction, so `ρ∞(Q_SS) ≳ R^{1/4}`.
- In `Z^3`, a linear form in three variables admits better approximations. By Schmidt's subspace theorem, or by the norm argument for a cubic-field basis, `λ_1 ≳ R^{1/6−ε}`. Minkowski's second theorem then gives `λ_3 ≲ R^{1/6+2ε}`, so `ρ∞(Q) ≤ μ ≲ R^{1/6+2ε}`.
- Therefore `prox/(Δ(A)·ρ∞(Q)) ≳ R^{1/12−ε} → ∞`.

Numerical confirmation (`sublattice_gap.py`, floating point). The 3-D value is an LP upper bound, which is valid for any subset of bisector constraints. The 2-D value was checked from below by brute force for `R = 10^4, 10^6, 10^8` (`verify_gap.py`).

| `R` | `ρ∞(Q,Z³)` (cubic pair) | `ρ∞(Q_SS,Z²)` | ratio | ratio for `(√2,√3)` |
|---|---|---|---|---|
| 1e2 | 2.00 | 2.36 | 1.18 | 1.06 |
| 1e4 | 3.96 | 6.93 | 1.75 | 1.72 |
| 1e6 | 8.05 | 19.74 | 2.45 | 2.43 |
| 1e8 | 18.23 | 60.57 | 3.32 | 3.48 |
| 1e10 | 40.23 | 198.47 | 4.93 | 5.23 |

The mechanism: conformality forces exchanges to stay in face lattices `ker(A_S) ∩ Z^n`. Such a lattice can be much worse for Diophantine approximation than `Z^n`. This is why C1\* uses `ρ_A`. In two dimensions every proper face lattice is 1-dimensional with `ρ ≤ Δ/2`, so C1\* coincides with C1 there.

Random and adversarial searches found no counterexample to C1\*, but they are weak evidence:

- 2-D random search, 129 instances: maximum `prox/(Δ·max(½,ρ))` = 0.53.
- 2-D hill-climbing over `(b, c)`, 23 runs with `Q = M ww^T + εI`: maximum 0.90.
- 3-D random search with ill-conditioned lattice-separable `Q`, 439 instances: maximum 0.45.
- 3-D "lexicographic" search, 49 instances: maximum 0.38.

### 3.4 Obstruction families (verified exactly by `examples.py`)

- **E1: separable convex quadratic over a TU matrix with integral data.** Network with arcs `s→v`, `k` parallel arcs `v→t` with cost `(x−½)²`, and `s→t` with cost `x²/k²`; supply `k`. The integer optimum is unique and satisfies `‖z*−x*‖∞ = k²/(2(k+1))` with `n = k+2`. This happens because the integer restriction of the parallel-arc costs is flat.
  - Consequence: for separable convex objectives, the factor `n` in Hochbaum–Shanthikumar and Granot–Skorin-Kapov is necessary even for TU matrices with integral `b`, and `ℓ∞` proximity cannot be dimension-free. This contrasts with the linear case, where proximity over TU is 0 and an `n`-free bound is conjectured for integral `b`.
  - Rounding the NLP relaxation (RENS-style) excludes the optimum.
  - We believe this is consistent with the Moriguchi–Shioura–Tsuchimura tightness discussion but did not verify it.
- **E2: Hessian entries ≤ 5, exponential proximity.** `Q = (I−2S)^T(I−2S)` with `t_i = 2/5` gives `prox = 0.4(2^n−1)`; the supremum over `c` is `(2^n−1)/2`.
- **E3: one ball, integral data.** For `x_1²+x_2² ≤ N²+N` with objective `max x_1 + εx_2`, the integer optimum is `(N, ⌊√N⌋)`, and the proximity is about `0.75√N` (48.2 at `N = 4096`). The upper bound `‖z*−x̂‖ ≤ (2√n R)^{1/2}` holds for all optima of a linear objective over a ball of radius `R`. Proof: a cap of depth `√n` contains a lattice point.
- **Conditioning lower bound for OQ2** (`kappa_family.py`, `verify_kappa.py`). Take `Q = R·ww^T + I` with `w = (1, −1/(2K))` and `K ≈ 0.45√R`. Then `κ ≈ R` and `ρ∞(Q) ≈ 0.25√κ` (computed up to `R = 10^9`; brute-force confirmed at `R = 10^4, 10^6`). This matches the upper bound `½√(tr Q/λ_min)` within a factor of about 2, so `√κ` is the tight conditioning rate in 2-D. With a badly approximable slope (`w = (1, −√2)`), `ρ∞` grows only like `R^{1/4}`. Conditioning alone therefore neither determines proximity nor can be dropped without lattice structure.

### 3.5 Attack plan for OQ1 (weak C1\*)

1. Use the exchange lemma (E) to reduce proximity to a lattice-point problem. Done.
2. Decompose `h = Σλ_t g_t` into CGST cone generators with `‖g_t‖∞ ≤ Δ(A)`. Work in coefficient space with Gram matrix `G = Γ^TQΓ`. Any nonzero integer `u ∈ [0,λ]` with `u^TG(λ−u) ≥ 0` gives an exchange ("box–Thales problem").
3. **Fat coordinates** (`λ_t` large): take the `G`-nearest lattice point to the centre `λ/2`. If it is nonzero and lies in the box, the exchange succeeds. This happens once `λ_t ≥ 2ρ∞(G_FF)`.
4. **Face lattices:** `span{g_t : t ∈ T} ∩ Z^n` is a finite-index sublattice of a face lattice `ker(A_S) ∩ Z^n`, with index at most `Δ^n`. So coordinate-sublattice Voronoi radii in `G` are bounded by `poly(Δ^n)·ρ_A(Q)`.
5. **Main obstacle: drift of the conditional centre.** Fixing the thin coordinates `u_R` shifts the target by `G_FF^{-1}G_FR λ_R/2`. This shift can be large when the fat and thin generators are strongly correlated in the `Q`-norm (a cheap fat generator paired with an expensive thin one at an obtuse `Q`-angle).
   - Possible fixes: choose the Carathéodory or Hilbert-basis decomposition to minimize drift; induct on faces with re-centring; or bound the drift by `ρ_A` through a transference argument.
6. **Targets.**
   - A complete proof for `n = 2`. The remaining case is the thin-cone configuration above.
   - A computer-assisted extremal search in `n = 3` over face-lattice–adversarial families, like the one in §3.3.
   - The weak form for general `n`, with `C(n) = Δ^{O(n)}`.

**Difficulty and risk.**
- The 2-D proof looks feasible, roughly 1–2 weeks.
- The general weak form is moderately hard; we put success at about 40% over 1–3 months.
- The tight form `C(n)Δρ_A` is unlikely to be reached soon.
- Risk: C1\* could also fail through slabs of width between 1 and `Δ`, or through cone rather than subspace restrictions. A corrected invariant ("conic Voronoi radii") would be less clean.
- Novelty risk: the Granot–Skorin-Kapov nonseparable section and Sun–Li 2001 were not accessible. We expect them to contain factor- and κ-based bounds, not a lattice-geometric invariant, but this is unconfirmed.

## 4. Significance

**Proved here** (elementary, some folklore-level):
- The Steinitz-regime equivalence (S and S′).
- The obstruction families E1–E3 and the `√κ` example.
- The linearization lemma for all optima, with the improved unconstrained constant.
- The lattice-separable bound (LS).
- The refutation of the global-Voronoi conjecture, together with its Diophantine mechanism.

These settle the brief's "right invariant" question in the Steinitz regime for integral structure, and show which invariants fail in the Cook regime.

**Plausible, if OQ1 is solved:**
- The first Cook-type theorem in which the Hessian enters only through lattice closest-vector geometry of the face lattices. It would unify CGST (`Q = 0`), Hochbaum–Shanthikumar/Granot–Skorin-Kapov (diagonal `Q`) and the closest vector problem (CVP, `A = ∅`), and it would be conditioning-free.
- It would give provable guarantees for "decorrelate, then round or locally search" heuristics in constrained MIQP (LAMBDA-style preprocessing with linear constraints). It would also explain why ill-conditioned but lattice-aligned Hessians are benign for rounding.

**Speculative:**
- Lattice-reduced branching directions guided by Voronoi-relevant vectors of face lattices.
- Proximity-based domain reduction for small structured subproblems.

**Needed for practical value.** The bounds are exponential in `n`, and `ρ_A` is CVP-hard to compute exactly. Solver use would need either structure (lattice-separable Hessians, low `n` per node) or cheap upper bounds (from LLL). Generic MIQP domain reduction will not benefit directly. The incumbent ellipsoid already captures the a-posteriori version.

## 5. Recommendation

- **Should the area get a full campaign?** Not as the main line; this area does not have the highest potential.
- **What stands out.** The sublattice-aware Cook theorem for convex quadratic IP (OQ1) is the most original item: a precise conjecture (C1\*), a clean reduction to lattice points (exchange lemma), a refuted naive version with a Diophantine mechanism, and exact obstruction families.
- **Why it ranks below the main line.**
  - The Steinitz-regime question in the brief is essentially answered by lifting and penalty simulation. That makes it folklore-level, not a paper.
  - The MISOCP question is classical lattice-point geometry.
  - OQ1's solver impact is indirect: bounds are exponential in `n`, and the invariant is CVP-hard.
- **Recommended next step.** A bounded follow-up (about two weeks): prove C1\* for `n = 2`, run a face-lattice-adversarial search for `n = 3`, and retrieve the Granot–Skorin-Kapov, Sun–Li and Baldick full texts to confirm novelty.

**Score: 4/10** (significance moderate-low for solvers, moderate for theory; feasibility moderate; originality moderate-high, pending the paywalled 1990–2001 papers).

## Verification record (targeted scratch checks only; no project-wide checks, no CI inspection)

Run from `research-20260928b/scouting/proximity-convex-minlp/`:

- `python3 examples.py` → `examples_output.txt` (E1, E2, E3 exact)
- `python3 search_c1.py 1 2 200` → `c1_n2_seed1.txt`
- `python3 search_c1.py s 3 250` for s = 1..4 → `c1_n3_seed*.txt`
- `python3 search_lex.py 1 60 30` → `lex_seed1.txt`
- `python3 search2d.py s 15 50` for s = 1..3 → `s2d_seed*.txt`
- `python3 sublattice_gap.py [sqrt]` → `sublattice_gap_output.txt`, `sublattice_gap_sqrt_output.txt`
- `python3 verify_gap.py` → `verify_gap_output.txt`
- `python3 check_linearization.py 7` → `check_linearization_output.txt`
- `python3 kappa_family.py` → `kappa_family_output.txt`
- `python3 verify_kappa.py` → `verify_kappa_output.txt`

The claims in §3.1–3.4 are backed by proofs sketched above plus these finite checks. The finite checks do not verify universal statements. The Diophantine asymptotics in §3.3 rely on standard results that were not formalized here.
