# Scout report: discrete convex analysis as a source of exact MINLP classes

Area: `discrete-convexity-minlp`. Date: 2026-09-28. Scratch files, scripts and
downloaded sources: `research-20260928b/scouting/discrete-convexity-minlp/`.
Everything below marked "new" is first-pass work by this scout. It has not been
reviewed, and the novelty search was cut short (see Section 1.7).

## Summary

The question "when is the integer value function `v(x) = inf_y F(x,y)` of a
convex MINLP discretely convex?" is older than it looks. Takamatsu, Hara and
Murota (2004) settled the L-natural (L♮) case, and Moriguchi, Hara and Murota
(2007) settled the integral-polyhedral M-natural (M♮) case. Both appeared in
short, rarely cited Japanese control-journal notes. The main findings of this
scout are:

1. **New, proved (first pass).** A C² convex function is "directed discrete
   midpoint convex in continuous variables" (R-DDM, Tamura–Tsurumi 2021) if and
   only if its Hessian is diagonally dominant with nonnegative diagonal (DD⁺)
   everywhere. DD⁺ is preserved under Schur complements. Therefore R-DDM is closed
   under continuous partial minimization. In the smooth case with strong convexity
   in `y`, this closure is fully proved. A sketch extends it to nonsmooth
   objectives and to UTVPI constraints `z_i ± z_j ≤ c`.
   Consequence: in every convex MINLP of this class, the integer value function
   is DDM-convex. So ℓ∞-neighbourhood local search (LD-SDA with `N∞`) is exact.
   If the NLP-relaxation minimizer is unique, or the domain is bounded, an
   optimum lies within ℓ∞-distance `n` of it, and
   steepest descent from the rounded relaxation point needs at most `n+1`
   neighbourhood searches. For convex MIQPs with an unconstrained continuous
   part, the integer value function is DDM-convex exactly when the Schur
   complement is DD⁺, a condition that can be checked in polynomial time.
2. **New counterexample (exactly verified).** An M♮-convex set in `Z^4` has a
   3-scaling that is not integrally convex. Consequently, the restriction to `Z^4`
   of a polyhedral continuous M♮-convex function with fractional data can fail
   integral convexity. As a consequence, a four-integer-variable network MINLP
   with continuous flows, fractional arc capacities and integer supplies/demands
   has an `N∞`-local minimum that is not global, although its continuous
   relaxation is M♮. A capacity version (max-flow value as a function of four
   integer arc capacities) also fails integral convexity. The integrality
   assumption of Moriguchi–Hara–Murota (2007) is therefore needed even for
   local-equals-global, not only for M♮-convexity.
3. **New criterion (derived, numerically cross-checked).** A quadratic form
   `x^T Q x` is integrally convex on `Z^n` if and only if
   `d^T Q d ≥ min_{s∈{±1}^O} s^T Q_OO s` for every `d ∈ {0,±1,±2}^n` with some
   `|d_i| = 2`, where `O = {i : |d_i| = 1}`. This puts recognition in `Π2^p`.
   Each test contains a ±1 quadratic minimization, which is max-cut-type and
   NP-hard in general.
4. **Numerical evidence.** In random value functions from mixed 2-separable
   objectives with UTVPI constraints, 0 of 120 instances violated DDM or integral
   convexity, as the theorem predicts. Adding one generic jointly convex coupling
   term made 73 of 120 instances fail integral convexity, and 12 had false local
   minima.

Recommendation score: **4/10**. The direction is feasible and clean, but its
originality is only moderate and its solver impact is narrow (Section 5).

## 1. Frontier map

### 1.1 Classes and what "local = global" buys

Notation: `N∞(x) = x + {−1,0,1}^n`; DD⁺ means `q_ii ≥ Σ_{j≠i}|q_ij|`.

| Class (on `Z^n`) | Local optimality certificate | Cost of one local check | Proximity `B(n,α)` for scaling | Closed under integer projection | Closed under scaling |
|---|---|---|---|---|---|
| separable convex | ±unit vectors | `2n` evaluations | `n(α−1)` | yes | yes |
| L♮ | `x ± 1_S`, all `S` | 2 submodular minimizations (polynomial) | `n(α−1)` | yes | yes |
| M♮ | `x ± e_i`, `x − e_i + e_j` | `O(n²)` evaluations | `n(α−1)` | yes | **no** |
| DDM (Tamura–Tsurumi) | `N∞` | `3^n` evaluations; NP-hard in general | `n(α−1)` | yes | yes |
| globally/locally d.m.c. | ℓ∞-distance-2 neighbourhood | exponential | `n(α−1)` | yes | yes |
| integrally convex (IC) | `N∞` | `3^n` evaluations; NP-hard in general | `β_n(α−1)`, `β_n ≤ (n+1)!/2^{n−1}` | yes | **no** |

Sources: Murota–Tamura IC survey (arXiv 2211.10912, Thms 4.5–4.7, bounds 4.8–4.10,
Sec. 4.4); Murota operations survey (arXiv 1907.09161, Tables 5–6, Prop. 4.10);
Tamura–Tsurumi DDM (arXiv 2001.11676, Thms 6.1, 7.3, 8.2, 8.3, Prop. 6.5, Remark 8.2).
Every function on `{0,1}^n` is IC and DDM, so minimizing over `N∞` is NP-hard for
variable `n` (TT Remark 8.2). Even 2-separable convex minimization contains
max-cut: take `ψ(x_i+x_j)` with `ψ(t) = w|t−1|`, plus the indicator of
`[0,1]` on each variable. For IC, the best known
scaling-proximity bound is superexponential, and the known lower bound is
`(n−2)²(α−1)/4` (2211.10912 p.30).

Inclusions: L♮ ⊊ DDM ⊊ IC and M♮ ⊊ IC. DDM is independent of M♮. Separable,
2-separable (`Σφ_i(x_i) + Σφ_ij(x_i−x_j) + Σψ_ij(x_i+x_j)`) and DD⁺ quadratics are
DDM. For quadratic forms, `x^TQx` is DDM iff `Q` is DD⁺ (TT Thm 5.2), and L♮ iff
`Q` is DD⁺ with nonpositive off-diagonal entries. `Q` DD⁺ implies IC
(Favati–Tardella). The converse holds for `n ≤ 2` (2211.10912 Ex. 3.5) but fails for
`n ≥ 3`: the M♮ form `(x1+x2+x3)²` is IC but not DD⁺.

### 1.2 Mixed-integer ("hybrid") value functions: the key prior work

- **Takamatsu, Hara, Murota (2004)**, ISCIE Trans. 17:409–411; English
  translation at `kzmurota.fpark.tmu.ac.jp/paper/THM04hybridLenglish.pdf`.
  They define `f: Z^n × R^m → R∪{+∞}` to be hybrid L♮ if `f(x, Ay+b)` is
  continuous L♮ for some nonsingular `A`. Prop. 2 shows that
  `h(x) = inf_y f(x,y)` is discrete L♮. Thm 1 gives the optimality criterion
  `0 ∈ ∂_y f` together with `h(x*) ≤ h(x* ± 1_S)`, which can be checked by
  submodular function minimization. For a quadratic, the Schur complement
  `L_d − L_h L_c^{-1} L_h^T` must satisfy the L♮ sign and dominance conditions.
  Example 2: `f` need not be hybrid L♮ for `h` to be L♮. Motivation: MIQP in
  hybrid model predictive control.
- **Moriguchi, Hara, Murota (2007)**, ISCIE Trans. 20:84–86; translation at
  `.../MHM07hybridMenglish.pdf`. This is the hybrid M♮ analogue. Prop. 4 shows
  that `h` is discrete M♮ only for *integral polyhedral* hybrid M♮ `f`.
  Discussion 3 notes that restricting a continuous M♮ function to `Z^n` does
  not preserve M♮-convexity. Prop. 2 notes that scalings of M♮ functions are
  "hybrid M♮ with `m = 0`" but need not be M♮.
- **Tamura–Tsurumi (2021)**, JJIAM; arXiv 2001.11676. They define R-DDM
  functions: `F: R^n → R∪{+∞}` convex with every `F(·/α)|Z^n` DDM. Continuous
  2-separable functions are R-DDM (Sec. 9). Proximity: for an R-DDM `F` with a
  unique minimizer `x̄`, some integer minimizer lies within ℓ∞-distance `n`
  (Thms 9.1–9.3). Remark 9.2: the convex extension of a DDM function need not be
  R-DDM. The paper has **no Hessian characterization and no continuous
  partial-minimization result**. Projection (Prop. 6.5) is over integer
  variables only.
- **Moriguchi–Murota (2019)**, DAM 255; arXiv 1710.04077. Integral convexity
  and discrete midpoint convexity are preserved under *integer* projection.
  Convolution with a separable convex function preserves integral convexity.
  Only the abstract was checked.
- **Murota (2021)**, network induction, OMS; arXiv 2001.03018, Tables 1–2.
  Integral convexity, L♮ and discrete midpoint convexity are **not** closed
  under aggregation or network induction. M♮ is closed under both, but with *integer*
  flows.
- Continuous-relaxation proximity for L♮ (Moriguchi–Tsuchimura 2009, PJO 5) and
  for M-convex/laminar functions (Moriguchi–Shioura–Tsuchimura 2011, SIOPT 21).
  These are known from search snippets and reference lists only; the full text
  was not accessible (SIAM returned 403). Their exact bounds are unverified here.

### 1.3 MINLP-side context (local literature)

- LD-SDA (Ovalle et al. 2025). The paper recalls that `N∞` i-local implies
  global for IC objectives and that `N2` s-local implies global for separable
  ones. It states that process models are generally neither
  [[ovalle2025-logic-based-discrete-steepest-descent]] p.8. Its future work
  explicitly asks how convex GDP relates to integrally convex problems
  [[ovalle2025-logic-based-discrete-steepest-descent]] p.26.
- Repository negative result (notes/research-20260912b-log.md): joint
  convexity is not enough. The reduced function
  `v(k) = (2k1−k2)² + |k|²/100` has a strict `N∞`-local minimum at `(1,2)` that
  is not global.
- Yu–Küçükyavuz (2025) give complete epigraph hulls for L♮ functions on
  boxes and for one mixed extension `max_i{h_i(x)−y_i}`
  [[yu2025-convexification-of-classes-of-mixed]] p.1-4, p.24-35. That work
  concerns hulls, not value functions of general convex MINLPs.
- Hochbaum–Shanthikumar proximity `nΔ` between integer and continuous optima
  for separable convex objectives over `Ax ≥ b`
  [[hochbaum1990-convex-separable-optimization-is-not]] p.9-12. Related work:
  n-fold/Graver methods for separable convex objectives
  [[hemmecke2013-n-fold-integer-programming-in]] p.9-10, and low-dimensional
  proximity [[weismantel2023-minimizing-a-low-dimensional-convex]] p.13-14.
- Discrete Shapley–Folkman bounds for IC sets
  [[murota2024-shapley-folkman-type-theorem-for]] p.5-6.

### 1.4 Recent arXiv (2024–2026) checked

- Kimura, Makino, Yamada, Yoshizumi, arXiv 2608.24078 (Sep 2026; abstract
  read). A set `S ⊆ Z^n` is UTVPI-representable iff it is closed under
  directed-midpoint and median operations, iff it is IC and 2-decomposable. This
  is relevant to Q1(c) below: which convex sets are R-DDM domains.
- Ligthart, arXiv 2606.30330 (2026; abstract and introduction read). Value
  functions `b ↦ min{f(x) : Ax=b, x∈Z^n_{≥0}}` with separable convex `f` are
  convex-extensible on cosets `r + MZ^m`, which yields FPT algorithms. This is
  convex-extensibility, which is weaker than integral convexity. It concerns
  right-hand-side value functions of IPs, not the projection of continuous
  variables.
- Murota–Tamura, arXiv 2211.10912 (IC survey, 2023), and arXiv 2305.15125
  (Shapley–Folkman, 2025).
- Semantic Scholar citation chase of arXiv 2001.11676 found 10 citing works.
  None concerns continuous projection, Hessians or MINLP value functions.

### 1.5 Operations-management use (not re-verified)

L♮-convexity is standard in inventory theory (Zipkin 2008; Chen 2017 survey;
Chen–Li 2021 POMS survey), and M♮-convexity appears in Chen–Li 2021 (OR
69:1396–1408). According to its abstract, Chen–Li 2021 gives a
necessary-and-sufficient C² characterization of M♮ functions and
parametric-preservation results. Only abstracts and search snippets were seen.
I did not verify whether these papers treat mixed integer/continuous
projections.

### 1.6 Sources examined

| Source | What was checked |
|---|---|
| `SCOUT-BRIEF.md` | Brief. |
| `notes/research-20260912b-log.md`, `-closeout.md` | Repository LD-SDA counterexample. |
| `literature/topics/bernal-minlp-gdp-review-2026-09-10.md` | LD-SDA summary. |
| `notes/candidate-directions-2026-09-05.md` | Item 3 (mixed separable proximity); item 11 (IC and SDDiP). |
| [[ovalle2025-logic-based-discrete-steepest-descent]] | p.8 (i-local/IC), p.26 (future work). |
| [[yu2025-convexification-of-classes-of-mixed]], [[hochbaum1990-convex-separable-optimization-is-not]], [[hemmecke2013-n-fold-integer-programming-in]], [[weismantel2023-minimizing-a-low-dimensional-convex]], [[murota2024-shapley-folkman-type-theorem-for]] | Paper notes and locators (above). |
| arXiv 2211.10912 | Full text: definitions, Thms 3.1–3.3, 4.5–4.7, Ex. 3.5–3.6, scaling algorithm. |
| arXiv 2001.11676 | Full text: Secs 2, 5–9 (definitions, quadratic characterization, projection, proximity, algorithms, R-DDM). |
| arXiv 1907.09161 | Tables 5–6, Prop. 4.10, scaling Examples 3.4–3.6. |
| arXiv 2001.03018 | Introduction, Tables 1–2. |
| arXiv 1710.04077 | Abstract. |
| arXiv 2608.24078, 2606.30330 | Abstract and introduction. |
| arXiv 2111.07240, 2108.10502, 1708.04579, 2212.03598 | Downloaded; grepped only. |
| THM04 and MHM07 English translations | Full text (3 pages each). |
| Murota publication list; `250924ISMzib=web.pdf` (ZIB workshop, Sep 2025) | Titles 2020–2026; overview slides. |
| SIOPT 10.1137/080736156 (Moriguchi–Shioura–Tsuchimura) | Not accessible (403). |
| Murota–Shioura 2005, "Substitutes and complements in network flows viewed as discrete convexity" (Disc. Opt. 2) | Title only. Gale–Politof (1981) is cited from memory. |

### 1.7 Search limitation

The shared web-search budget ran out early in this scout's session, after 8
searches. Novelty checks after that point relied on direct fetches of known
URLs, one citation chase, and Murota's publication list. **An unsuccessful search
does not establish novelty.** The most likely places for overlooked prior work
are (i) the 2010–2025 inventory and OM literature on mixed discrete/continuous
L♮ or M♮ decisions, (ii) Japanese-language DCA notes (ISCIE, RIMS Kôkyûroku),
and (iii) Murota's 2024 Japanese book 『離散凸解析——理論の拡大と応用』.

## 2. Open questions

**Q1 (hybrid DDM and IC value functions; best, partly attacked in Section 3).**
Let `F: R^n × R^m → R∪{+∞}` be closed convex, and let
`v(x) = inf_y F(x,y)` for `x ∈ Z^n`.
- (a) Prove in full generality that if `F(x, Aw+b)` is R-DDM for some
  nonsingular `A`, then `v` is R-DDM (so `v|Z^n` is DDM). This includes
  nonsmooth and extended-valued `F`.
- (b) Characterize R-DDM for nonsmooth convex functions: are they exactly the
  convex functions whose distributional Hessian is DD⁺-valued?
- (c) Are R-DDM convex sets exactly the UTVPI polyhedra? (Compare arXiv
  2608.24078.)
- (d) Is there a class that contains both R-DDM and integral polyhedral M♮
  functions, is closed under continuous partial minimization, and restricts to
  IC functions? Mixtures matter in applications: network flows (M-type) plus
  difference constraints (L-type).

Evidence that these are open: THM04 covers L♮ only and MHM07 covers integral
polyhedral M♮ only. Tamura–Tsurumi treat R-DDM without a Hessian criterion and
project over integer variables only. Moriguchi–Murota 2019 project over integer
variables only. The citation chase found nothing further. Solver significance:
exactness certificates and iteration bounds for LD-SDA-type `N∞` search, and a
proximity box of radius `n` around the NLP relaxation.

**Q2 (continuous-flow network MINLPs).** Consider convex network flow problems
with continuous flows and integer supplies or integer capacities.
- (a) Is `v|Z^n` IC when `n ≤ 3`?
- (b) Is it IC when all data (capacities, cost breakpoints) are half-integral,
  i.e. for 2-scalings of M♮ functions?
- (c) For capacity value functions with integer capacities on `|K| ≥ 3` arcs,
  are they IC when every fixed datum (other capacities, cost breakpoints) is
  integral? Which topologies make them DDM or L♮ up to sign changes?

Known: pairs of arcs are substitutes or complements (Gale–Politof 1981;
Murota–Shioura 2005). Proposition 6 settles the general question negatively for
`n = 4` with data in thirds. This holds for supply value functions (with a false
local minimum) and for capacity value functions (IC fails, Prop. 6(b)). The open
cases are therefore small `n`, the scale factor `α = 2`, integral fixed data
with nonlinear costs, and structured topologies.

The mechanism in Proposition 6 needs three "odd" coordinates and one coordinate
at distance 2, so `n = 4` is the smallest dimension where it works. A slice
argument suggests that `n = 3` may always be IC: 2D g-polymatroid slices through
integer endpoints cannot avoid every corner. This is unproved.

Evidence from the computations:
- 0 IC violations in 420 random or structured capacity and supply value
  functions (`n ≤ 4`), in 460 scaled M♮ instances (E6), and in 9000 random
  scaled M♮ sets with `n = 3, 4` (E9), while DDM, L♮ and M♮ fail often.
- Random fractional transportation sets with `n = 5` fail IC in 3 of 109 cases
  (E7), consistent with Proposition 6. That includes
the series–parallel network `SP4`, where the substitute/complement signs are
unbalanced. Solver significance: capacity expansion and network loading with
convex congestion or transport costs are among the most common convex MINLPs.
A structural answer would decide when local search over capacity or production
levels is exact.

**Q3 (recognition complexity).**
- (a) Is it coNP-hard (or `Π2^p`-complete) to decide whether `x^TQx` is
  integrally convex? Proposition 5 below places the problem in `Π2^p`.
- (b) Is it coNP-hard to decide whether the value function of a convex MIQP with
  linear constraints on the continuous variables is DDM, given that it is
  piecewise quadratic with one Schur complement per active set?

Evidence: the Murota–Tamura survey states only that DD⁺ is sufficient, and
necessary when `n ≤ 2`. I found no complexity statement. Solver significance: it
separates cheaply checkable exactness certificates (DD⁺ Schur complement) from
certificates that cannot be checked.

(Known open problem, not pursued: whether IC functions admit a polynomial
scaling-proximity bound. Moriguchi–Murota–Tamura–Tardella prove a
superexponential upper bound and a quadratic lower bound.)

## 3. Best question (Q1): attack plan and first-pass mathematics

### 3.1 Results

Let `μ(p,q)` denote the directed discrete midpoint of Tamura–Tsurumi: round
`(p+q)/2` toward `p` coordinatewise. DDM means
`f(p)+f(q) ≥ f(μ(p,q)) + f(μ(q,p))`.

**Lemma 1 (pair structure).** Let `d = q − p`, `a_i = sgn(d_i)⌊|d_i|/2⌋`, and
`b = d − a`. Then `μ(p,q) = p+a` and `μ(q,p) = p+b`. Moreover `a_i b_i ≥ 0`, and
`(a_i + σa_j)(b_i + σb_j) ≥ 0` for all `i ≠ j` and `σ = ±1`.
*Proof.* The formulas follow from the definition. For the product, note that
`(σa_j, σb_j)` is the pair for `σd_j`, because truncated halving is odd. Write
`A = a_i + a_j` and `E = e_i + e_j`, where `e_k = b_k − a_k ∈ {0, sgn d_k}`. The
product is `A(A+E)`. It is negative only if `|A| = 1` and `E = −2A`. But
`E = ±2` forces both `d`'s to be odd with the same sign, and then `A` has that
sign. ∎ (Exhaustively checked for `|d| ≤ 60`: `lemma_checks.py`, L0/L1.)

**Lemma 2.** If `H` is DD⁺, then `a^T H b ≥ 0` for every pair from Lemma 1.
*Proof.* Decompose
`H = Σ r_i e_ie_i^T + Σ_{i<j}[h_ij^+ (e_i+e_j)(e_i+e_j)^T + h_ij^− (e_i−e_j)(e_i−e_j)^T]`
with `r_i = h_ii − Σ_{j≠i}|h_ij| ≥ 0`, and apply Lemma 1 to each term. ∎

**Theorem 1 (Hessian criterion, new).** A C² convex `F: R^N → R` is R-DDM iff
`∇²F(z)` is DD⁺ for every `z`.
*Proof.* (⇐) For `p, q ∈ Z^N`,
`F(p)+F(q)−F(μ(p,q))−F(μ(q,p)) = ∫₀¹∫₀¹ aᵀ∇²F(p+sa+tb) b ds dt ≥ 0`
by Lemma 2. `F(·/α)` has Hessian `α⁻²∇²F(·/α)`, which is again DD⁺.
(⇒) Suppose row `i` of `H = ∇²F(z₀)` is not dominant. Take
`d = 2e_i + Σ_{j≠i} σ_j e_j` with `σ_j = −sgn h_ij`. Then `a = e_i` and
`aᵀHb = h_ii − Σ_{j≠i}|h_ij| < 0`. At `p = round(αz₀)`, the DDM inequality for
`F(·/α)` has left side `α⁻²(aᵀHb + o(1)) < 0` for large `α`. ∎
This generalizes TT Thm 5.2 (constant Hessian) and the classical Hessian
characterization of continuous L♮.

**Lemma 3 (Schur complement).** If `H` is DD⁺ and `H_yy ≻ 0`, then `H/H_yy` is
DD⁺. Eliminating a pivot `k` changes the row slack `r_i` to
`r_i + |h_ik| r_k/h_kk ≥ r_i`. ∎ (Exact rational check, random `n ≤ 6`:
`lemma_checks.py` L3.)

**Theorem 2 (continuous partial minimization, new).**
- (a) *Smooth.* Let `F ∈ C²`, `∇²F` DD⁺ everywhere, `∇²_yy F ≻ 0`, and assume
  `min_y F(x,y)` is attained for each `x`. Then `v(x) = min_y F(x,y)` is C² with
  `∇²v = ∇²F/∇²_yy F`, the Schur complement, by the implicit function theorem.
  So `v` is R-DDM by Theorem 1 and Lemma 3. **Proof complete.**
- (b) *Nonsmooth, finite-valued (sketch).* Let `F` be finite convex R-DDM, and
  let the `y`-level sets be bounded locally uniformly in `x`. Then `v` is R-DDM.
  1. R-DDM is invariant under real translations: for rational shifts, combine
     integer translation invariance (TT Prop. 2.4) with scaling invariance
     (TT Thm 6.1), then pass to real shifts by continuity.
  2. So `F_ε = F*ρ_ε + ε|z|²` is C∞, strongly convex and R-DDM, hence DD⁺ by
     Theorem 1.
  3. Apply (a), then let `ε → 0`. DDM inequalities survive pointwise limits.
- (c) *UTVPI constraints (sketch).* Let `P = {z : z_i ± z_j ≤ c_ij, l ≤ z ≤ u}`
  with `y` bounded, and add 2-separable penalties
  `k·max(0, z_i ± z_j − c)²` (R-DDM by TT Sec. 9). The penalized value
  functions increase to `v_P` as `k → ∞`; points with `v_P = +∞` diverge. The
  DDM inequalities survive the limit, so `dom v_P ∩ Z^n` is a DDM set.
- (d) Reparametrizing `y = Aw + c` (with `A` nonsingular) does not change `v`, so
  it suffices that `F(x, Aw + c)` is R-DDM.

**Corollary 3 (MINLP consequences).** Consider
`min{F(x,y) : (x,y) ∈ P, x ∈ Z^n}` with `F`, `P` as in Theorem 2. Then:
1. `x*` is optimal iff `v(x*) ≤ v(x*+d)` for all `d ∈ {−1,0,1}^n` (TT Cor. 3.3).
   So LD-SDA with `N∞` and exact convex subproblem solves is exact.
2. Steepest descent over `N∞` uses exactly `L+1` neighbourhood minimizations,
   where `L` is the ℓ∞-distance to the nearest minimizer (TT Thm 8.2).
3. If the NLP relaxation has a unique minimizer `x_R` in its `x`-part, some
   integer optimum satisfies `‖x*−x_R‖∞ ≤ n` (TT Thm 9.2; Thm 9.3 covers bounded
   domains). Starting from `round(x_R)` therefore takes at most `n+1`
   neighbourhood minimizations, i.e. at most `(n+1)·3^n` convex NLP solves.
   Caveat: TT's §9 proofs use continuity of the R-DDM function. For constrained
   `v` this must be checked on its (closed, polyhedral) domain; that belongs to
   the step-1 write-up in Section 3.3.
4. Suppose one fixed sign change of the variables makes every Hessian
   off-diagonal entry nonpositive at every point, and turns every constraint
   into a difference or bound constraint. Then `F` is continuous L♮ (hybrid L♮)
   and `v` is L♮ (THM04). Each neighbourhood minimization reduces to two
   submodular minimizations, giving polynomially many NLP solves.
5. If the pattern is unbalanced, there is no polynomial algorithm in `n` unless
   P = NP, by the max-cut reduction in Section 1.1.

**Theorem 4 (unconstrained MIQP criterion).** Let `F = zᵀQz + cᵀz` with
`Q_yy ≻ 0` and no constraints on `y`, and let `S = Q/Q_yy`. Then:
- `v|Z^n` is DDM iff `S` is DD⁺ (TT Thm 5.2 applied to `v`).
- `v|Z^n` is L♮ iff, in addition, `s_ij ≤ 0` (THM04).
- `v|Z^n` is IC iff `S` satisfies Proposition 5; for `n ≤ 2` this is again DD⁺.
Joint DD⁺ of `Q` is sufficient but not necessary.

**Proposition 5 (IC of quadratic forms, new).** For symmetric `Q`, `xᵀQx` is IC
on `Z^n` iff `dᵀQd ≥ min_{s∈{±1}^O} sᵀQ_OO s` for all `d ∈ {0,±1,±2}^n` with
`‖d‖∞ = 2`, where `O = {i : |d_i| = 1}`.
*Proof.*
1. By Murota–Tamura Thm 3.1, it suffices to test pairs at ℓ∞-distance 2.
2. The identity `f(z+x) = f(x) + 2zᵀQx + f(z)` and invariance of integral
   convexity under adding affine functions reduce every pair to `(0,d)`.
3. Coordinate sign changes allow `d ≥ 0`.
4. At `m = d/2`, the local convex extension minimizes `E[(e+w)ᵀQ(e+w)]` over
   distributions on `w ∈ {0,1}^O` with `E w = ½·1`, where `e = 1_{d_i=2}`.
   Reflecting `w ↦ 1−w` preserves this objective, so symmetric distributions
   suffice. This yields
   `f̃(m) = eᵀQe + eᵀQ1_O + ¼ min_s sᵀQ_OO s + ¼·1ᵀQ_OO 1`.
5. Comparing with `½dᵀQd` gives the stated inequality. ∎

The criterion agreed with an LP-based test in all 85 random cases (`n = 3, 4`;
45 IC, of which 22 are not DD). Script: `quad_ic_criterion.py`.

**Proposition 6 (counterexample, new as far as found).** Let
`S = {Σ_{i≤3} [c_i(e_i−e_4) + k_i e_i] : c_i ∈ {0,1,2}, k_i ∈ {0,1}} ⊆ Z^4`.
- `S` is M♮-convex: it is a Minkowski sum of M♮ segments. Checks: 160 points,
  0 exchange violations, 0 IC violations.
- Its 3-scaling is `T = {y : 3y ∈ S} = Z^4 ∩ ⅓·conv S = {0, (1,1,1,−2)}`. This is
  not IC: no point of `T` lies in `N((0+y)/2)`.
- Network reading: sources `s1, s2, s3`; sinks `t1` (coordinate 4) and `t2`
  (the dropped coordinate); arcs `s_i→t1` with capacity 2/3 and `s_i→t2` with
  capacity 1/3; continuous flows; integer supplies and demands.
- Minimizing `−(z1+z2+z3)` gives a feasible `N∞`-local minimum at `z = 0` that
  is not global; the optimum is −3 at `(1,1,1,−2)`.
- **(b) Capacity version.** Add a super source `S` with integer capacities `u_i`
  on `S→s_i` and a super sink `T` with integer capacity `u_4` on `t1→T`
  (`t2→T` uncapacitated), and let `v(u) = −(max flow)`. Then
  `v(0,0,0,0) = 0` and `v(1,1,1,2) = −3`. The local convex extension at the
  midpoint `(½,½,½,1)` is `−4/3 > −3/2`, attained by
  `½[v(1,1,0,1) + v(0,0,1,1)] = ½(−5/3 − 1)`. So a capacity value function with
  continuous flows can fail integral convexity. Verified by hand and by LP
  (`e8_scaled_mnat_counterexample.py`, part b).

So restrictions of polyhedral continuous M♮ functions, and scalings of M♮ sets,
can fail integral convexity. The integrality hypothesis in MHM07 is needed even
for local-equals-global. Script: `e8_scaled_mnat_counterexample.py`. The survey
examples show only that scaled M♮ sets can fail to be M♮ (Ex. 3.4, which is
still IC) and that IC sets can fail IC under scaling (Ex. 3.6, not M♮).

### 3.2 Computations

Values were computed with cvxpy/Clarabel (tolerance `1e-10`), and discrete
convexity was tested with tolerance `1e-6`, using `dcheck.py`. Integral
convexity is tested with Murota–Tamura Thm 3.2 and exact local-extension LPs. A
violation found on a box is also a violation for the underlying function,
because restriction to a box preserves each class.

| Experiment | Instances | DDM viol. | IC viol. | other |
|---|---|---|---|---|
| E1 mixed 2-separable, `n=2`, `m∈{1,2,3}` continuous, ± UTVPI constraints | 80 | 0 | 0 | 0 false local minima. L♮ fails in 59, so the class is strictly larger than L♮. `v(x/2)` also DDM. |
| E1 same, `n=3` | 40 | 0 | 0 | 0 false local minima |
| E2 control: E1 plus one generic coupling `(a·z)²`, `n=2` | 80 | 41 | 41 | 7 false `N∞`-local minima |
| E2 control, `n=3` | 40 | 36 | 32 | 5 false `N∞`-local minima |
| E3 capacity value functions, random digraphs, `n=2` | 75 | 0 | 0 | always L♮ after sign changes (substitutes/complements) |
| E3 same, `n=3` | 75 | 2 | 0 | not L♮ after any sign change in 3 |
| E4 supply value functions (continuous flows, fractional capacities), `n=2` | 75 | 0 | 0 | 0 M♮ violations |
| E4 same, `n=3` | 75 | 65 | 0 | M♮ fails in 53 |
| E6 scaled M♮ sets and functions (generator networks), `n=3`; counts are over (instance, `α`) pairs, `α∈{2,3}` | 300 | 92 | 0 | scaled M♮ fails in 45 pairs |
| E6 same, `n=4` | 160 | 50 | 0 | scaled M♮ fails in 33 pairs |
| E8 structured `n=4` (Proposition 6) | 1 | – | 1 | false local minimum |
| E5 three parallel capacitated arcs (`P3`, M♮ type), `n=3` | 24 | 0 | 0 | 0 M♮ violations |
| E5 series(parallel(a,b), parallel(c,d)) with elastic demand (`SP4`), `n=4` | 24 | 22 | 0 | never L♮ after any sign change (unbalanced signs); M♮ fails in all |
| E5 Wheatstone bridge, capacities on 2 or 3 arcs (`WB2`, `WB3`, `WB3b`) | 72 | 0 | 0 | not L♮ after any sign change in 7 (including `n=2`: substitute/complement sign changes across the domain) |
| E8(b) capacity version of Proposition 6, `n=4` | 1 | – | 1 | – |
| E7 integer points of random bipartite transportation polytopes, capacities in thirds; M-form (`n ≤ 5`) | 74 | – | 1 | – |
| E7 same, M♮ form (one sink dropped, `n ≤ 5`) | 109 | – | 3 | first violation has `n = 5` |
| E9 random scaled M♮ sets, `n=3`, `α=2` and `α=3` (3000 each) | 6000 | – | 0 | – |
| E9 same, `n=4`, `α=2` and `α=3` (1500 each) | 3000 | – | 0 | random generators never hit the Proposition 6 pattern |

Random value-function experiments with `n ≤ 4` (E3–E6, E9) never produced the
Proposition 6 structure; random `n = 5` transportation sets did, in 3 of 109
cases. Random search in small dimensions would therefore have suggested a false
general conjecture. The counterexample came from analysing why a pairing
argument (conformal subflows of the difference of two optimal flows) fails.

### 3.3 Attack plan for the remaining steps

1. Write Theorem 2(b)–(d) rigorously. Handle extended-valued `F`, level
   boundedness, and continuity of `v` on its domain; TT Thm 9.1 uses continuity.
   Expected effort: 2–4 days. Low risk.
2. Q1(b)–(c): prove "R-DDM ⇔ DD⁺-valued Hessian measure", and determine whether
   R-DDM domains are exactly the UTVPI polyhedra. Moderate risk: the UTVPI
   characterization of arXiv 2608.24078 is for integer sets and needs a
   continuous analogue.
3. Q2(a)–(b): run an exhaustive search over g-polymatroids for `n = 3` and
   `α = 2`. Then try to prove integral convexity for `n = 3`. A proof would
   choose conformal subflows of the difference of two optimal flows; the
   pairing argument fails in the Proposition 6 geometry, so a multi-point
   decomposition is needed. Risk is moderate to high.
4. Q3(a): reduce max-cut to IC recognition. One approach adds a coordinate
   whose cross terms tilt the ±1 quadratic, while keeping `Q` PSD and every
   other test vector `d` satisfied. Risk is moderate.
5. Applications. Identify PSE, hybrid MPC and inventory models with DD⁺ or
   sign-balanced structure after eliminating the continuous variables, and test
   LD-SDA with certificates against Pyomo.GDP instances. The repository already
   has the GDP/LD-SDA context.

Difficulty and risk: Theorem 2 and the counterexample are low risk but also low
depth; the key idea is an elementary integration identity plus a classical
Schur complement fact. The real difficulty is Q1(d) and Q2, a class that mixes
M-type and L-type structure; it may not exist in useful generality.

## 4. Significance

**Proved (first pass, unreviewed).**
- Theorems 1, 2(a), 4 and Propositions 5–6. Theorem 2(b)–(c) are sketches.
- Consequences for any convex MINLP whose objective is R-DDM up to a linear
  change of the continuous variables (C² with DD⁺ Hessian, or continuous
  2-separable) and whose constraints are UTVPI:
  - exact `N∞` local-optimality certificate (LD-SDA is exact);
  - at most `n+1` neighbourhood searches from the rounded NLP relaxation;
  - an integer optimum within ℓ∞-distance `n` of the relaxation.
- For convex MIQPs without constraints on `y`, a polynomial test (Schur
  complement DD⁺) decides whether this certificate applies.
- Negative: continuous M♮ structure of the relaxation does not give
  local-equals-global once data are fractional (Proposition 6, supply version).
  The capacity version loses integral convexity (Prop. 6(b)). Joint convexity
  alone does not give local-equals-global either (repository example).

**Plausible.**
- A DCA structure detector in MINLP presolve, analogous to convexity
  detection, could recognize balanced-sign DD⁺ or L♮ integer projections and
  switch to steepest descent with submodular-minimization neighbourhood search.
  That would give a polynomial number of NLP solves on those classes.
- For small numbers of ordered external variables (typically at most 7 in
  PSE), `N∞` search with a certificate is practical: at most `8·3^7` NLP solves.

**Speculative.**
- How often real process or supply-chain models satisfy these structural
  conditions is unknown. The LD-SDA benchmark models are mostly nonconvex, and
  the LD-SDA paper's CSTR case shows `N2` search failing there.
- For network-flow (M-type) MINLPs, the counterexample suggests that
  integrality of data (capacities, cost breakpoints), not continuous convexity,
  is the operative condition. That may limit practical coverage.

**What would still be needed for practical value:** automatic structure
recognition, handling of nonconvex subproblems (Corollary 3 assumes exact
subproblem solves), and evidence on realistic instances that the classes occur.

## 5. Recommendation

This area has a clean, feasible core. First, R-DDM convexity (DD⁺ Hessians) is
closed under continuous partial minimization and UTVPI constraints. That gives
exact local-search certificates, `n+1` iteration bounds and an
`n`-proximity box for a recognizable class of convex MINLPs; it answers
positively, for a subclass, the question in LD-SDA's future-work statement.
Second, a small verified counterexample shows that continuous M♮ structure with
fractional data can destroy the local certificate. Both are good material for a short
note. However, the L♮ and integral-M♮ cases date to 2004/2007. The new
mathematics is elementary (an integration identity plus Schur complements). The
class is narrow, and its unbalanced part has NP-hard neighbourhoods. The harder
questions (Q1(d), Q2) could be significant but carry real risk of a negative or
unstructured answer. **Score: 4/10** (significance 4, feasibility 8, originality
4). Pursue only as a short note or as a side result to support the
repository's LD-SDA/GDP work, not as the main direction.

## Appendix: reproduction

All scripts live in `research-20260928b/scouting/discrete-convexity-minlp/`.

- `python3 sanity_checks.py`: checker validation on known functions.
- `python3 lemma_checks.py`: Lemmas 1–3, exact arithmetic.
- `python3 e1_projection.py 1 40`: E1/E2, about 23 minutes; output in `e1_out.txt`.
- `python3 e3_network.py 7 25`: E3/E4; output in `e3_out.txt`.
- `python3 e6_scaled_mnat.py 3`: E6; output in `e6_out.txt`.
- `python3 e8_scaled_mnat_counterexample.py`: Proposition 6, exact.
- `python3 quad_ic_criterion.py`: Proposition 5 cross-check.
- `e5_structured_networks.py`, `e5b_wheatstone.py`, `e7_transport_sets.py`, `e9_scaled_search.py 9`: see Section 3.2; outputs in `e5_out.txt`, `e5b_out.txt`, `e7_out.txt`, `e9_out.txt`. The E5 run was stopped after `SP4`; its Wheatstone cases were rerun in `e5b_wheatstone.py`.

Downloaded sources are in `src/` (PDF and pdftotext output). Only targeted
scripts were run; no project-wide checks were run.
