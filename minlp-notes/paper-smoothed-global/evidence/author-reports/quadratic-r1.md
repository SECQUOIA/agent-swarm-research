# Author report, round 1: counting and quadratic chapters

Author: Opus (principal mathematical author for these files). Date: 2026-10-05.

Files owned and written:

- `sections/03-counting.tex` (Section `sec:count`)
- `sections/04-quadratic.tex` (Section `sec:qp`)
- `appendices/A-finite-noise.tex` (Appendix `app:count`)
- `appendices/B-quadratic.tex` (Appendix `app:qp`)
- this report

No other file was edited. No experiment was rerun, no literature search was
made, nothing was committed, and no work was delegated.

## 1. Source development to manuscript label map

Paths are relative to `research-20261002/new-direction/` unless stated.

| Source (section) | Manuscript labels | Notes |
| --- | --- | --- |
| `smoothed-semiconcave-cells.md` §1 (counting lemma) | `def:count:curv`, `lem:count:interval`, `def:count:local-event`, `thm:count:local` | Stated with general interval concentration (density, grid, Kolmogorov) and a conditional form. |
| same, §2 (nested meshes) | `def:count:mesh`, `cor:count:levels` | Generalized to per-coordinate curvatures and mesh scales with balance constant `c_bal`; gives `1+2k` (isotropic) and `1+8k` (anisotropic) from one proof. Grid law with per-coordinate `sigma_i` (used by the integer author). |
| same, §3 (cell algorithm, certificate, accuracy) | `lem:count:rounding`, `def:count:search`, `thm:count:cells`, `cor:count:approx` | Search admits optional exact closure steps, so the approximate and exact searches share one theorem. |
| same, §4 (finite noise for prescribed accuracy) and its review (atom example) | `cor:count:levels` (grid case), `cor:count:approx`, `ex:count:atom` | |
| same, §5 (convex QP recourse, fixed box, square completion) | `lem:qp:aux`(a),(d), `thm:qp:aligned` | |
| `proximal-growth-tail.md` §§1–7 | `def:count:growth`, `thm:count:growth-tail` (proof in App. A) | Generalized from continuous to lower semicontinuous `f` (needed for reduced objectives on graph domains). Uniform-volume alternative proof (§6) omitted as duplicate. Product sharpness omitted; scalar sharpness kept. |
| same, §8 (finite QP grid, slice lemma `8(F+1)^2`) | `lem:qp:growth-sections` | Extended to mixed polytopes (`F = Z 2^r`) and Gaussian-like laws. |
| same, §9; `expected-smoothed-qp.md` | `thm:qp:two`, `rem:qp:moments` | Part (b) (Gaussian-like law) from Sol's two-inertia supplement §5. |
| `negative-inertia-qp.md` (dependency of the k≤2 theorem) | `thm:qp:conditioned` (proof in App. B) | Projected-growth variant omitted (not needed). |
| `polynomial-finite-noise-tails.md` §§2–3 | `lem:count:finite-tails`(a)–(c), `thm:count:renegar` | Generalized to auxiliary variables (`m≥0`, noise on `x` only) for graph domains, and to Kolmogorov laws. |
| same, §4 | `lem:count:finite-tails`(d) | Uses `lem:sp:bezout` (sparse author, App. C) for the nonsingular-root count. |
| same, §5 | `lem:count:rare-fallback`(b) | Stated with a free allocation parameter `rho` (`P <= 3 rho`). Part (a) is the accounting principle. |
| `polynomial-exact-fallback.md` §§1–6 | `def:count:semialg`, `thm:count:fallback` (proof in App. A) | Stated for explicit compact mixed semialgebraic domains (covers boxes, polytopes, graph constraints), as the sparse audit requires. Output: root representations of the coordinates of the lexicographically least minimizer and of the value. |
| `polynomial-exact-fallback-construction.md` | not reproduced | Constructive box-only alternative; the general QE proof supersedes it for the needed domains. |
| `spectral-normalization.md` (one-sided `beta`) and frame bound from `smoothed-ambient-cell-closure.md` §6 | `lem:qp:normalize` (proof App. B) | |
| `smoothed-exact-cell-closure.md` | `lem:qp:face`, `lem:qp:pieces`, `def:qp:closure-search`, `lem:qp:tube`, `lem:qp:tube-prob`(a), `thm:qp:aligned`, `ex:qp:atom` | Kernel condition removed (see §2). Aligned theorem now for an arbitrary rational factor `T` (Theta uses `max|T_il|`). |
| `smoothed-ambient-cell-closure.md` | `lem:qp:volume`, `lem:qp:uniform-count`, `lem:qp:sections`, `lem:qp:tube` (ambient form), `lem:qp:tube-prob`(b), `thm:qp:uniform` | |
| `ambient-local-count-barrier.md` §1 | `prop:qp:fiber-sharp` (proof App. B) | |
| same, §§2–6 | `prop:qp:ambient-barrier` (statement) | Proof is the boundaries author's `thm:lim:ambient` / `app:lim:ambient` (more general family). My duplicate proof was removed. |
| `smoothed-gaussian-cell-closure.md` | `def:count:laws`, `lem:count:transfer`, `lem:count:gauss-sampler` (construction App. A), `lem:qp:gauss-count`, `thm:qp:gauss`, `lem:qp:tube-prob`(c), budget loop (C) in `app:qp:main` | |
| `smoothed-miqp-cell-closure.md`, `integer-label-isolation.md` | `prop:qp:primitives`(b), `lem:qp:gap`, `lem:qp:isolation`, `lem:qp:sections` (`R^2` count), `thm:qp:uniform` with `n_z>=1`, `ex:qp:corner-labels` | Gap constant simplified (§2 item 8). |
| `smoothed-gaussian-miqp.md` | `thm:qp:gauss` with `n_z>=1` | One theorem now covers QP (`n_z=0`) and MIQP. |
| `smoothed-mixed-separable-closure.md` | `def:qp:sep`, `lem:qp:scalar`, separable-piece paragraph, `thm:qp:sep` | Irrational-breakpoint example kept in text. |
| `anisotropic-gaussian-separable-closure.md` | `lem:qp:aniso`, `thm:qp:sep-gauss` | Derived as a specialization of the unified proof. |
| Sol `prewrite-lowrank-sol.md` | `lem:qp:aux`(c), kernel-condition removal everywhere, common-lemma order | Independently verified (§2 item 1). |
| Sol `prewrite-two-inertia-sol.md` | `thm:qp:conditioned`, `thm:qp:two`(b), `rem:qp:moments` | |

## 2. Mathematical repairs, consolidations, and new developments

1. **Kernel condition removed** (Sol's consolidation, independently verified).
   For every attaining witness `x_a` of `W_zeta(a)`, the quadratic
   `F(x_a)+zeta'x_a+(a'-Tx_a)'Lambda(a'-Tx_a)/2` is a global upper model of
   `W_zeta` touching at `a`; minimizing it gives
   `g' Lambda^{-1} g <= 2(V(a)-V*)` with `g=Lambda(a-Tx_a)+xi`
   (`lem:qp:aux`(c)). This needs no differentiability and holds at integer
   ties, flat faces, and knots. The extraction (`lem:qp:pieces`), the
   algebraic gradient identity, the tube lemma, and the section counts never
   use `ker P ⊆ ker T`; overlapping region formulas are used only through
   equal **values** (`lem:qp:sections` states this explicitly). The intrinsic
   normalization satisfies the condition anyway, so nothing is lost.
2. **Growth tail for lower semicontinuous `f`.** Every step (attained maxima,
   closed good set, regular points) works for lsc `f`; needed because a
   reduced objective `min_y F(x,y)` over a compact graph domain is only lsc.
   The trace step was rewritten to avoid symmetry of `DP`: monotonicity gives
   PSD symmetric parts, and `det DP=0` gives a vector with `DQ v=v`, so
   `tr DQ >= 1`.
3. **Finite tails with auxiliary variables and Kolmogorov laws**
   (`lem:count:finite-tails`): the two-block formula with `n+m` variables per
   block characterizes point growth of the reduced objective; the format
   bound is `((2s+1)max{d,2})^{a_R(n+m+1)^2}`.
4. **One corrected-corner theorem with optional closure**
   (`thm:count:cells`), reused by the approximation corollary, the
   growth-conditioned algorithm, all closure searches, and (by co-authors) the
   integer and recourse searches.
5. **Balanced meshes** unify isotropic and anisotropic constants
   (`cor:count:levels`).
6. **Gaussian-like sampler constants tightened and repaired.** Attempts
   `ceil(4K^2)`, failure mass `exp(-K)`; total Kolmogorov error `14e<2^{-b}`
   (source: `22e`). The source did not clamp the first Taylor value `y_0` to
   `[0,1]`, which the squaring error bound `|a^2-b^2|<=2|a-b|` requires; the
   manuscript clamps it.
7. **Growth-conditioned algorithm on equal-subdivision meshes.** The source
   clipped an isotropic lattice. Using the nested equal subdivisions of
   `def:count:mesh` lets `thm:count:cells` be reused; the packing count is
   `2^k(2 sqrt(k kappa)+2)^k` retained cells, which still gives `Z^{k/2}` for
   `k<=2` (Sol's verified exponent).
8. **MIQP gap constant.** Requiring `h_J<=1` gives
   `C_gap = k alpha/4 + theta_gap`, independent of the auxiliary width, so the
   Gaussian support loop satisfies `J(t)<=J(0)+t` instead of `J(0)+2t`.
9. **Unified expected-work proof** (`app:qp:main`) for the aligned, uniform
   ambient, and Gaussian-like laws, covering QP and MIQP at once; separable and
   anisotropic theorems are derived by listing replaced inputs (`app:qp:sep`).
10. **New explanatory lower bound** in `rem:qp:moments`: on
    `X=[-w0/2,w0/2]×Y` with a linear coordinate, `P{Z>t} >= nu w0/(sigma t)`,
    so `E min{B, Z^{k/2}}` is of order `(nu w0/sigma) B^{1-2/k}` for `k>=3`.
    This shows that integrating the inverse-growth power fails beyond two
    negative directions even with the sharp tail; it is a limitation of the
    method, not an algorithmic lower bound. Short proof given in place.
11. **Label isolation** stated with general interval concentration, so one
    lemma covers uniform grids and Gaussian-like laws.
12. **Aligned theorem without norm or frame promise** on `T`; `Theta` is
    computed with `tau_T = max|T_il|`.

No central argument failed. No defect requiring a stop was found.

## 3. Contracts stated in the theorems

- Base input `I` counts sigma and supplied factors; all sampling parameters
  (`M`, or `b` and the support radius) are computed from base data before the
  draw, with polynomial bit length.
- Supplied factorizations are checked exactly (PSD and frame tests). Exact
  convex QP (Kozlov–Tarasov–Khachiyan) and exact convex MIQP (Del Pia,
  Thm. 3, FPT in `n_z`) are cited primitives; MIQP witnesses are polished to
  polynomial height.
- Output: rational minimizer and value (QP/MIQP/separable); root
  representations of the canonical lexicographic minimizer (`thm:count:fallback`).
- Correctness on every draw; one draw; exceptional probability `<=1/B`;
  fallback cost `B poly`; expectation over all draws including ties.
- Numerical parameters stated: `nu diam(P)/sigma`, `nu S/sigma`,
  `alpha(u_i-l_i)/sigma`, `beta diam(X)/sigma`; uniform ambient bound
  contains a power of `n` growing with `k` (not FPT).
- Gaussian proxy used only in proofs; `G_{b,sigma}` is a finite rational law;
  no theorem covers arbitrary approximations of a Gaussian.

## 4. Pending integrations and requests

1. **Output format mismatch (model author).** `def:model:outputs`(d)
   ("Algebraic output") requires one primitive element `theta` with rational
   maps. `thm:count:fallback` returns a *coordinate-root tuple*: each
   coordinate of the lexicographically least minimizer, and the value, in its
   own root representation, all referring to the same canonical point. The
   assignment brief says this tuple is acceptable. Request: the model author
   adds a "root-tuple output" item (or relaxes (d)), and the sparse author's
   phrase "algebraic output of `thm:count:fallback`" (`05-sparse.tex`) is
   aligned with it. The recourse author already describes it correctly.
2. **Cross-author labels I depend on** (all exist now): `def:model:grid`,
   `eq:model:interval`, `def:model:perturbation`, `prop:model:regret`
   (model); `lem:sp:bezout` (sparse); `thm:lim:ambient`, `app:lim:ambient`
   (boundaries). `prop:qp:ambient-barrier` is stated as the `alpha=1` case of
   `thm:lim:ambient`, including its finite-law threshold `M>=32`; the two
   statements must stay consistent.
3. **Labels other authors use from my files** (verified present):
   `thm:count:local`, `thm:count:cells`, `cor:count:levels`,
   `def:count:mesh`, `def:count:growth`, `def:count:semialg`,
   `lem:count:rounding`, `lem:count:finite-tails`, `lem:count:rare-fallback`,
   `thm:count:growth-tail`, `thm:count:fallback`, `ex:count:atom`,
   `sec:count:laws`, `sec:qp:aux`, `prop:qp:ambient-barrier`, and the six main
   `thm:qp:*` theorems.
4. **Constants.** The absolute constant `a_R` (Renegar format bound) and the
   fallback base factor `B=2^{(I+1)^{C_d}}` rely on unextracted absolute
   constants of Renegar's theorem. The algorithms are well defined with one
   admissible value; an implementation would need explicit values. Suggest a
   sentence in the limitations section.
5. **Bibliography.** Four standard references are not in the KB and need
   verified entries from the Luna lead: `evans2015-measure-theory-and-fine`
   (Rademacher, area formula), `federer1969-geometric-measure-theory` (area
   formula), `rockafellar1970-convex-analysis` (a.e. differentiability of
   convex functions), `fulton1998-intersection-theory` (refined Bézout,
   Example 8.4.6; also used by the sparse author). Please confirm the exact
   locators or substitute equivalent sources.
6. **Notation.** I use `^{\mathsf T}`, `U_{\sigma,M}`, `\mathcal G_{b,\sigma}`,
   `delta_K` for Kolmogorov distance, `E_j` for the mesh correction,
   `\underline U_j` for the certified lower bound, `c_{\rm fr}`, `c_{\rm bal}`,
   `\Theta` (piece Hessian bound), `\Psi=(TT^T)^{-1}T`, `\Pi_T`, and
   `D x<=e` for constraints (the letter `M` is the grid size). No macro
   additions are required.
7. **Related work.** I attribute critical regions (Bemporad et al. 2002,
   Tøndel et al. 2003, Patrinos–Sarimveis 2011), the parametric reduction
   (Ding 1996), rational Jacobi rotations (Del Pia 2026), discrete isolation
   (Beier–Vöcking 2004, Röglin–Vöcking 2007), and qualitative genericity
   (Lee–Pham 2016; Alexandrov via Azagra et al. 2023). The introduction should
   carry the fuller comparison (Kelner–Nikolova 2007; Del Pia 2023, 2026
   approximation; Luo et al. spectral branch and bound if verified). No
   novelty or priority is claimed in my files.

## 5. Citation keys used (key → source)

| Key | Source | In KB |
| --- | --- | --- |
| `renegar1992-on-the-computational-complexity-and` | Renegar, Part III: Quantifier elimination, J. Symb. Comput. 13 (1992), Thm. 1.1 | yes |
| `kozlov1980-the-polynomial-solvability-of-convex` | Kozlov–Tarasov–Khachiyan, polynomial solvability of convex QP (1980) | yes |
| `pia2025-convex-quadratic-sets-and-the` | Del Pia, convex quadratic sets and MICQP, SIOPT 2025, Thm. 3 | yes |
| `pia2026-rational-jacobi-rotations-and-the` | Del Pia, rational Jacobi rotations, arXiv 2026 | yes |
| `grotschel1988-geometric-algorithms-and-combinatorial-optimization` | Grötschel–Lovász–Schrijver (LP, continued fractions) | yes |
| `basu2006-algorithms-in-real-algebraic-geometry` | Basu–Pollack–Roy (univariate root isolation, sign determination) | yes |
| `mehlhorn2015-from-approximate-factorization-to-root` | Mehlhorn–Sagraloff–Wang, root isolation | yes |
| `beier2006-typical-properties-of-winners-and` | Beier–Vöcking, STOC 2004 (winner-gap density) | yes |
| `roglin2007-smoothed-analysis-of-integer-programming` | Röglin–Vöcking, Math. Program. 2007 | yes |
| `lee2016-stability-and-genericity-for-semi` | Lee–Pham, JOTA 2016 | yes |
| `azagra2023-a-geometric-approach-to-second` | Azagra–Cappello–Hajłasz (Alexandrov's theorem) | yes |
| `ding1996-a-parametric-solution-for-local` | Ding, Waterloo thesis 1996 | yes |
| `bemporad2002-the-explicit-linear-quadratic-regulator` | Bemporad–Morari–Dua–Pistikopoulos, Automatica 2002 | yes |
| `tndel2003-an-algorithm-for-multi-parametric` | Tøndel–Johansen–Bemporad, Automatica 2003 | yes |
| `patrinos2011-convex-parametric-piecewise-quadratic-optimization` | Patrinos–Sarimveis, Automatica 2011 | yes |
| `evans2015-measure-theory-and-fine` | Evans–Gariepy, Measure Theory and Fine Properties of Functions | **no** |
| `federer1969-geometric-measure-theory` | Federer, Geometric Measure Theory | **no** |
| `rockafellar1970-convex-analysis` | Rockafellar, Convex Analysis | **no** |
| `fulton1998-intersection-theory` | Fulton, Intersection Theory, Example 8.4.6 | **no** |

## 6. Targeted checks actually run

All local and targeted; no project-wide build, no CI inspection.

1. Scratch compile of only my four files with the paper preamble and
   `macros.tex` (`/tmp/sg-check/harness.tex`, two `pdflatex` passes):
   exit 0, no LaTeX errors, 37 pages. Unresolved references are only the
   seven co-author labels listed in §4.2, each verified present by `grep` in
   the co-authors' files. One 0.7pt overfull box remains (Renegar theorem
   header). Citation warnings are expected (no `references.bib` yet).
2. `grep`-based check that every `count:`/`qp:` label referenced by other
   authors' files exists in my files: all present.
3. Proof diagnostics `/tmp/sg-diag/diag1.py` (sympy/numpy/scipy, exact
   fractions where possible), all passed: Jacobi rotation numerator and
   bracket sign (symbolic); fiber integral `n(n-1)∫r^{n-2}min(q,1-r)=1-(1-q)^n`
   for n in {2,3,5,9,16} (symbolic); weighted lattice-sum inequality on 3000
   random parameter sets (max ratio 0.999); constant envelope `V=-1/8` and
   the two pieces of `ex:qp:atom` (exact rationals); slice values and `P` of
   `ex:qp:corner-labels`; sampler error-budget arithmetic; normalization and
   intrinsic-constant inequalities.
4. Proof diagnostics `/tmp/sg-diag/diag2.py`, all passed: every-witness
   inequality on 300 random nonsmooth envelopes with ties (all attaining
   witnesses); label increment bound on 300 random instances; symbolic
   gradient identity `grad q_S = alpha(a-T x_S)` for a random KKT piece;
   finite-grid label isolation by exact enumeration (40 fixtures, three
   tolerances, including ties); capped-moment inequalities.

5. Formatting hygiene on my five files (inline `python3` with `pathlib`):
   no trailing whitespace, final newlines present, balanced `$`, braces,
   display delimiters, and environment pairs (one `\[` flag was the row
   spacing `\\[3pt]`, confirmed balanced).

These diagnostics check identities and inequalities of the written proofs.
They do not implement the algorithms, sample the theorems' laws, or measure
running times. The existing research checkers were not rerun.

## 7. Scope statements kept explicit

- All results optimize the sampled objective; no recovery of the unperturbed
  optimizer (`rem:qp:regret` points to `prop:model:regret`).
- The uniform ambient theorem is fixed-`k` polynomial, not fixed-parameter;
  the barrier concerns counting surrogates, not closure.
- Separable theorems use the supplied concave factor's rank and curvature,
  rational breakpoints, and product domains.
- Aligned noise is low-dimensional and correlated in original coordinates;
  aligned MIQP is not claimed.
- The two-direction theorem is a distinct numerical refinement, not
  superseded and not extended beyond `k=2`.
