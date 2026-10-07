# Cluster `cutrecourse`: conditional recourse, star counterexample, cut residual oracle

Scope: `extensions.tex`, subsections "Why a global grid correction cannot simply be made local",
"The precise conditional-recourse interface" and "An exact cut oracle for a large nonconvex
residual" (including the finite-noise count and the exact core mode), plus the mixed
submodular residual paragraph. The self-contained statements and proofs are in
`cutrecourse-proofs.tex` (same directory).

## 1. Verdict

**Sound with fixes.** Every mathematical claim in the cluster survived a line-by-line
re-derivation and exact finite checks. No claim is false. The fixes are about hidden
hypotheses, notation, self-containment, and prior-work positioning. Two of them matter for the
paper's narrative:

1. The m = 32 star refutes a bag-local budget only when the budget may depend on (p, L).
   Its growth constant degrades as m grows, so it does not address budgets depending on
   (p, κ), which is the parameterization of the main theorem. The companion's
   positive-definite star family closes this gap. I generalized both families to every
   dyadic mesh (Proposition `prop:cr-star`).
2. The cut oracle is classical for a fixed core point. The paper must credit the classical
   reduction (DR-submodular box QP to minimum cut) and position the construction against
   Del Pia–Khajavirad Section 4, which uses the same binary/continuous split.

Development results (Section 5) add four things: a sharper form of the interface (only error
*oscillation* matters); a star family on which the paper's global correction is optimal
among constant corrections up to a factor (1−h)^{-1}; a deterministic count and an exact
f(k,κ)·poly(I) algorithm under core growth; and an exact polynomial algorithm for one core
coordinate with sign-consistent couplings.

## 2. What was verified, and how

All checks use `fractions.Fraction` (exact arithmetic) and are under `checks/`. Each run took
a few seconds. Commands actually run, from `paper-decomposition-aware/process/w1/checks/`:

| Command | Result |
|---|---|
| `python3 cutrecourse_star.py` | passed: m=32 values `0, 23/32, 31/16`; corners `23/32, 27/32, 31/16, 31/16`; identity `V_h−V = m dist(x/4,G)^2` on 65 points; brute-force separability cross-check; family (A) for h = 1/2…1/16 with corner formula `(1−h)(mh²/4−h−ε)`; family (B) for h = 1/4 (d = 8, 9, 16, 64, 1000; needed = d/16 − 3/8) and h = 1/8, 1/16 |
| `python3 cutrecourse_cut.py` | passed: 150 random instances (k ≤ 2, r ≤ 5, random orientations, rational boxes, integer residuals): cut identity for every label, exact Edmonds–Karp = brute-force endpoint minimum, flow certificate (capacity, conservation, value = cut), endpoint lemma against residual grids and integer domains |
| `python3 cutrecourse_count.py` | passed: discrete-law bound (300 random intervals); exact expectation **over all noise atoms** of near-optimal tuples (≤ H_k) and queries (≤ 2^k + 8^k J H_k) for k = 1 (M = 16, J = 4, σ ∈ {1/2, 4}) and k = 2 (M = 8, J = 3); worst ratios 0.14 (queries) and 0.33 (near tuples); incumbent gap ≤ e_j at every level and atom; growth count; flat example retains 1, 4, 10, 22, 46, 94, 190, 382 cells at levels 0–7 |
| `python3 cutrecourse_exact.py` | passed: 200 random instances: T_0 F integral for every label with both `T_0 = Λ_cΛ_e²` and `T_0 = S_0³`; den(label optimum) ≤ D_0 and den(F*) ≤ D_0 (the ratio reached 1, so the bound can be tight); example where S_0² fails for lcm-based S_0 |
| `python3 cutrecourse_submod.py` | passed: fixture `0, 13/16, 13/16, 0` (single greedy base gives −13/16, the equal mixture gives 0); 40 random mixed instances: endpoint reduction, all submodular inequalities, base-polytope membership of all greedy vectors, and Edmonds' min–max attained exactly by a mixture of ≤ |D|+1 greedy vectors (exact vertex enumeration) |
| `python3 cutrecourse_monotone.py` | passed: least minimizers nested and ≤ r+1 distinct for sign-consistent couplings (150 trials); nestedness fails in 58/150 mixed-sign trials |
| `python3 cutrecourse_k1exact.py` | passed: k = 1 sign-consistent recursion equals brute force on 200 instances; flow-call count ≤ 2r+1 (attained) |
| `pdflatex` on a temporary wrapper in `/tmp` | the fragment compiles; only undefined citations (expected) and five overfull boxes under 6 pt |

These are targeted finite checks. They support the proofs but do not replace them. No
project-wide verification or CI inspection was performed.

### Specific questions

**(a) Star counterexample (m = 32, ε = 1/16, G = {0, 1/2, 1}).** Confirmed exactly:
V(x) = −x² + (15/16)x, unique optimizer (1, 1/4, …), value −1/16; conditional grid values
0, 23/32, 31/16; U_G = 0; bag cell [1/2,1]×[0,1/2] is the only cell containing (1, 1/4), with
corner min-marginals 23/32, 27/32, 31/16, 31/16; the bag-local budget 1/8 rejects it, and the
global budget 33/16 keeps it; V_h − V = m dist(x/4, G)². The same threshold applies to the
paper's *coordinate-interval* test on x (its endpoint min-marginals are V_h(1/2), V_h(1)), so
the example is relevant to the actual filtering rule, not only to bag cells.

**(b) Interface theorem and constants.** Correct: retained optimizer cells, U ≤ F* + e + η,
and every retained cell has a corner with W_B ≤ F* + 2(e + η). Hidden hypothesis: the
current level's cells must cover an optimizer's bag projection (true by induction in a
refinement scheme). Lemma `lem:cr-cell` gives the sharper per-cell budget, with zero
contribution from integer unit intervals.

**(c) Signed endpoint/min-cut identity, integer residuals, box stability, flow certificate.**
All correct. Signs: ω_ij = c_ij o_i o_j (u_i−l_i)(u_j−l_j) ≤ 0; ρ_i = μ_i + ½Σ ω_ij; arcs
i→t: max(ρ_i, 0), s→i: max(−ρ_i, 0), pair arcs r_ij = −ω_ij/2; identity
F = φ_0 + Σ min(0, ρ_i) + cap(S_y). Inward rounding is exactly what makes the endpoint lemma
valid for integer residuals. A fixed coordinate (d_i = 0) is harmless. Bit complexity: after
scaling capacities by a common denominator, augmenting-path flows stay integral and bounded.

**(d) Core search and the expected query bound.** Correct, including the following points.
- Discrete uniform law: P(γ ∈ I) ≤ ℓ/(2σ) + 1/M, since atoms are 2σ/(M−1) apart.
- Independence: the event "W(v) ≤ F*_γ + 2e_j" depends on γ through F*_γ. Comparing with
  neighbours removes this dependence, so the event is contained in a product event with
  deterministic intervals I_i(v), which depend only on V_0.
- Interval length: Lh + 4e_j/h = Lh(1 + k/2), from coordinate semiconcavity of V_0.
- Boundary coordinates contribute a factor of at most 1, with two such values per
  coordinate.
- Counting: each retained cell has a 2e_j-near-optimal corner, a grid point touches at most
  2^k cells, and each retained cell has 2^k children with 2^k corners each.
- Minor: M ≥ 2^{J−1} already suffices for queries through level J; the text's M ≥ 2^J is
  harmless.

**(e) Exact core mode.** Correct.
- T_0 = S_0³ is needed because a monomial coefficient times two residual endpoints carries
  up to three denominators (a_j x_j², c_ij x_i x_j in the constant term). If S_0 is a least
  common denominator (or the product of *distinct* denominators), the cube is necessary;
  example: ½·x_i x_j at x_i = x_j = ½ gives 1/8 with lcm 2. If S_0 is the product with
  multiplicity, S_0² would already suffice. The sharper natural choice is T_0 = Λ_cΛ_e².
- The smallest-face argument makes the 3^k face enumeration complete even for singular or
  indefinite core Hessians.
- The rational separation is correct: F* ≤ Φ(z_U) ≤ U and U − LB < 1/D_0², and both values
  have reduced denominators ≤ D_0.
- The warning against inserting this depth into the noise count is correct and in fact
  understated: for a fixed noise scale the atom denominators grow with M, so D_0 ≥ T_0 grows
  at least like M³ and M ≥ 2^{J(D_0)} generally cannot hold.

**(f) Mixed submodular oracle.** Correct.
- Submodularity of g after partial minimization follows from the lattice argument applied
  to minimizing completions. PSD is *not* needed for submodularity, only for exact
  polynomial computability of g(S).
- Greedy vectors lie in B(h), and a mixture gives a valid lower bound. Edmonds' min–max
  supplies an exact mixture of ≤ m+1 vectors.
- The GLS oracle-LP construction is consistent. I checked Theorem 6.4.9 and Lemma 6.5.15 in
  the local GLS text, the LP duality, the greedy separation, and the Lovász-extension
  recovery of a minimizing prefix.
- The fixture needs a two-vector mixture.
- Small wording errors: "at most |R|+1 greedy base vectors" should be |D|+1 (or |D|); the
  text says "The full constructive certificate proof remains in the companion note", which
  the paper cannot rely on (now supplied in Proposition `prop:cr-greedy`).

## 3. Issues and fixes

| # | Severity | Location | Issue | Fix (verified) |
|---|---|---|---|---|
| 1 | major | extensions.tex, star subsection | The m=32 family has growth constant g ≤ ε/(1+mh²/4) → 0, so it refutes only (p,L)-dependent local budgets, not (p,κ)-dependent ones, which are the relevant ones for the paper | Include family (B) (positive definite star, κ < 11, needed correction ≥ dh(1/2−h) + 2h² − 1/2 = Ω(√m h)); Proposition `prop:cr-star`(B), checked exactly |
| 2 | major | cut-oracle subsection, prior work | The fixed-core cut oracle is classical (Hammer; Picard–Ratliff; Kolmogorov–Zabih; DR-submodular box QP is polynomial, as recorded by Burer–Natarajan–Willemsen with Staib–Jegelka and Padberg). Del Pia–Khajavirad Section 4 (Thm 4, Cor. 3) uses the same split of nonpositive-diagonal (binary) variables and proves polynomial classes with few positive-diagonal variables. Neither is discussed | Remark `rem:cr-cut-prior`. Claim only the box-stable certified oracle and its composition with core search. Note that DPK's binary-part condition is treewidth/interface size, ours is signs, and our guarantees are additive, deterministic under core growth, or smoothed |
| 3 | major | mixed paragraph; exact-mode paragraph | The paper text defers proofs to companions ("remains in the companion note", "existing base-selected closure and fallback construction") | Mixed oracle: Propositions `prop:cr-submod`, `prop:cr-greedy` give complete proofs (classical existence/computation cited). The exact smoothed closure/fallback theorem is outside this cluster: either include its proof elsewhere in the paper or drop the sentence |
| 4 | minor | interface subsection | "Interpolation at an optimizer gives U ≤ OPT + e + η" silently assumes the current cells cover an optimizer's bag projection | State the hypothesis (Theorem `thm:cr-filter`(b)) and note it holds by induction |
| 5 | minor | interface subsection | Budget e_B = \|B\|Lh²/8 is stated without the integer-unit-interval refinement and without saying which points it bounds | Lemma `lem:cr-cell` (bounds every feasible x with x_B in the cell; integer unit intervals contribute 0) |
| 6 | minor | cut subsection | α_i undefined; symbols h_i, p_i, K, s, t clash with mesh h, bag size p, grid size K, width s | Define α_i; rename to μ_i, ω_ij, ρ_i, φ_0, orientation o_i, source/sink 𝗌/𝗍 |
| 7 | minor | finite-noise count | M ≥ max{2, 2^J} is stronger than needed | M ≥ 2^{J−1} suffices; state either |
| 8 | minor | exact mode | T_0 = S_0³ is valid but its reason is not stated; "could be circular" understates the problem | Explain the three denominators; offer T_0 = Λ_cΛ_e²; state that M ≥ 2^{J(D_0)} generally cannot hold |
| 9 | minor | mixed paragraph | "at most \|R\|+1 greedy base vectors" | \|D\|+1 |
| 10 | minor | smoothed count | Its meaning is not stated: it bounds work on the *perturbed* instance; as an approximation device for the unperturbed problem it is worse than deterministic grids ((k²L/δ)^k vs (kL/δ)^{k/2}) | Remark `rem:cr-smoothed`; contrast with the flat example (deterministic count exponential in J) |
| 11 | minor | main.tex notation | \OPT is defined as f^* in main.tex; the shared notation asks for F^* | Change the macro or adjust the fragment |

No critical issues.

## 4. Classical vs new, and placement

| Result (label in fragment) | Classical / new | Closest prior work | Recommendation |
|---|---|---|---|
| Conditional value inherits curvature; bag-cell interpolation (`lem:cr-semiconcave`, `lem:cr-cell`) | Elementary; partial minimization preserving semiconcavity is standard | Same argument as the paper's grid interpolation lemma | **main**, short |
| Conditional-recourse filter (`thm:cr-filter`) | New formulation in this context; the mechanism is branch-and-bound on a variable subset with exact inner solves | Branch-and-bound on complicating variables, e.g. generalized Benders / GOP-type methods (recalled, not checked); semiconcave interpolation bounds as in the paper | **main** |
| Oscillation form (`prop:cr-osc`) | New, small | — | **main** (as a short proposition next to the open question) or remark |
| Star families (`prop:cr-star`, `ex:cr-star32`) | New as stated; formalizes accumulation of per-variable discretization error | Bienstock–Muñoz error scaling with total coefficient size is consistent with it | **main** (structural limit). On family (A), the paper's global correction is optimal among constant corrections up to (1−h)^{-1}, which supports the main design |
| Endpoint lemma, signed cut representation, certified oracle (`lem:cr-endpoint`, `prop:cr-cut`, `thm:cr-oracle`) | Classical ingredients | Hammer 1965; Picard–Ratliff 1975; Kolmogorov–Zabih 2004; DR-submodular box QP (BNW 2026 introduction, Table 1); DPK 2026 Section 4 | **main**, compact, with explicit credit |
| Core search correctness and certificate (`thm:cr-search`) | Composition is new; the mechanism is the paper's corrected-grid idea with exact recourse | — | **main** |
| Deterministic count under core growth (`prop:cr-growth`) | New (my development); parallels the main theorem's (p,κ) story | — | **main** |
| Flat example (`ex:cr-flat`) | Elementary | — | **remark** |
| Smoothed query count (`thm:cr-smoothed`) | New composition; the confinement argument resembles isolation/winner-gap lemmas | Beier–Vöcking 2004, Röglin–Vöcking 2007 (local copies checked) | **appendix**, with Remark `rem:cr-smoothed` |
| One core coordinate, consistent signs (`prop:cr-k1`) | New observation (my development); the nestedness is Topkis monotonicity, and parametric min cut is classical (Gallo–Grigoriadis–Tarjan, recalled) | — | **appendix** or remark |
| Uniform height and exact output (`lem:cr-height`, `thm:cr-exact`) | Standard rational-height and separation arguments; the uniform-over-labels bound is the useful point | Vavasis 1990; the paper's own height lemma | Statement in **main** (one paragraph), proof in **appendix**. The f(k,κ)·poly(I) exact claim under core growth is new (my development) |
| Mixed concave–convex residuals (`prop:cr-submod`, `prop:cr-greedy`) | Classical ingredients and precedents | Topkis 1978 (partial minimization); Edmonds 1970; GLS 1988 (Thm 6.4.9, Lemma 6.5.15 checked locally); IFF 2001; Kozlov–Tarasov–Khachiyan 1980; Bunton–Tabuada 2022 and Gómez–Han 2025 (cited by the companion; not checked locally) | **appendix**, or a remark in the main text with the proof in the appendix |
| Implemented exact mode, checker, code paths | Implementation | — | **drop** from the theorem text (evidence sections only) |

Is the smoothed count meaningful? It is a legitimate smoothed-analysis statement, with three
points in its favour:
- the expected work is linear in the accuracy bits J and exponential only in k;
- the residual size enters only polynomially;
- without perturbation the count can be exponential in J (flat example: 2^{jk/2} retained
  cells).

Its limitations:
- it bounds work on the perturbed instance only;
- the base H_k ≈ ((1+k/2)L/(2σ))^k is polynomial in L/σ only for fixed k;
- it is not an approximation scheme for the unperturbed problem.

Now that the deterministic count under core growth is available, the smoothed count is
secondary for the paper's story. Hence the appendix recommendation.

Citation keys used in the fragment but missing from `references.bib`:
- Topkis1978 (title and venue confirmed via Bach's bibliography in the local knowledge base);
- BeierVocking2004, RoglinVocking2007 (local copies exist);
- Hammer1965, PicardRatliff1975, Edmonds1970 (recalled, **not checked locally**; verify
  bibliographic details before use).

I also cite Gallo–Grigoriadis–Tarjan (SIAM J. Comput. 1989) in this report only; the fragment's
k = 1 proof is self-contained and does not need it.

## 5. Open questions and development

### (g) A general local-error interface for sparse messages — **sharpened**

1. **Exactly which property is needed.** Proposition `prop:cr-osc`: for filtering
   (optimizer cells kept; every retained cell has a corner with W_B ≤ F* + 2e + 2η), it
   suffices that W_B − ℓ has *oscillation* ≤ η over the compared corners. Its absolute size,
   valid lower bounds and feasible completions do not matter. A common shift, for example
   message normalization, is harmless. Valid lower bounds and completions are needed only to
   certify the final gap (Theorem `thm:cr-filter`(c)). So the sparse-message question is
   exactly: compute conditional values at bag corners with error oscillation O(pLh²),
   without refining all outside coordinates.
2. **Cleaner impossibility for grid min-marginals.** Proposition `prop:cr-star`:
   - (A) For a uniform grid of mesh h, a constant correction must satisfy
     c ≥ (1−h)(m − 4/h − 4ε/h²)·Lh²/8 on a star with L = 2, p = 2. On this family the
     paper's global correction (m+1)Lh²/8 is optimal among constant corrections up to
     (1−h)^{-1} as m → ∞.
   - (B) Even with p = 2 and κ < 11, c ≥ dh(1/2 − h) + 2h² − 1/2 with m = d² leaves, so no
     correction of the form c(p, κ, h) is sound.
   - Both bounds also apply to the paper's coordinate-interval test.
3. **The interface is computable for fixed p; the question is about parameters.** For a
   bag value v, the conditioned outside problem has the same curvature and a tree
   decomposition of width ≤ p. The corrected-grid lower bound on a uniform outside grid of
   mesh h' = h·sqrt(p/(n−|B|)) gives (∗) with η = e. It costs O(p(N+|A|)K'^p) with
   K' ≈ (s/h)·sqrt(n/p) per query (main-text Lemma round with bag coordinates fixed). This is
   polynomial for fixed p but costs h^{-p} per query. That destroys the accuracy-polynomial
   counts, which is why the open question is meaningful. (Observation; not put in the
   fragment.)
4. **Still open.**
   - A realization of the oscillation interface with per-query cost f(p,κ)·poly(n, log 1/h)
     for general bounded-treewidth quadratics. The obstacle: conditional problems at
     non-optimal bag values need not inherit growth, so the main theorem cannot be applied
     recursively.
   - At bounded κ, the true dimension exponent of the necessary correction. Family (B)
     gives Ω(√n·h) at fixed h, versus O(n·h²) sufficient. Star families with bounded L and
     PD Hessian seem limited to √m by Cauchy–Schwarz on the leaf shifts; other topologies
     were not explored.

### Further developments (outside the listed questions)

- **Deterministic count under core growth** (Proposition `prop:cr-growth`): queries
  ≤ 2^k + 8^k J (1 + sqrt(kκ))^k, where only V(v) − F* ≥ g‖v − v*‖² is needed (implied by
  point growth of F; the residual may have ties). The algorithm never uses g.
- **Exact output in f(k,κ)·poly(I)** under core growth (Theorem `thm:cr-exact`). This
  combines the count with the uniform height bound and rational separation. It mirrors the
  paper's exact quadratic theorem with the residual dimension and treewidth only in the
  polynomial factor, so the residual may be dense and nonconvex.
- **k = 1 with sign-consistent core couplings** (Proposition `prop:cr-k1`): least minimizers
  are nested (Topkis), so V is a lower envelope of ≤ r+1 quadratics. A recursion over least
  minimizers finds them with ≤ 2r+1 cuts, giving an exact deterministic polynomial algorithm
  with no perturbation. Open: k = 1 with mixed-sign couplings. Nestedness fails (58/150
  random trials), and parametric min cut with non-monotone parameters can have
  superpolynomially many breakpoints (Carstensen 1983, recalled, not checked). I do not know
  whether this case is polynomial. Also open: k ≥ 2 with consistent signs, where the number
  of pieces of the parametric envelope is not obviously polynomial.

### What failed or was not attempted

- I did not find a bounded-κ family needing Θ(n·h²). The natural star constructions give
  only √n.
- I did not attempt a general sparse realization of the oscillation interface beyond the
  observations above.
- I did not re-verify the companion's exact smoothed closure/fallback theorem; it is outside
  this cluster and was used only as context.
