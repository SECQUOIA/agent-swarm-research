# Front matter, model, boundaries, and Appendix G: author report r1

Correction dated 2026-10-06: the characterization of B10 below as "new as a
manuscript statement" is withdrawn. The deterministic filter and its
retention, incumbent and witness guarantees come from the decomposition-aware
companion's conditional-recourse filter. Part (c) adds the expected
near-optimal bag-grid count under the finite noise law. No efficient oracle
for general outside-value problems is supplied. The historical account below
is retained; the companion-overlap addendum and revised manuscript supersede
its novelty wording.

Date: 2026-10-05. Author: Opus front-matter and boundaries author. This is an
evidence file, not submission text. It covers only the files this author owns:

- `sections/00-abstract.tex`, `sections/01-introduction.tex`,
  `sections/02-model.tex`, `sections/09-boundaries.tex`,
  `sections/10-discussion.tex`, `appendices/G-boundaries.tex`.

No other author's file was edited. No experiment was rerun, no literature
search was made (only BibTeX key lookups in `literature/references.bib`), and
no commit was made.

## 1. Status

All six files are complete drafts with full proofs for every result claimed in
them. The abstract and the introduction's results table were reconciled with
the theorem statements present on disk at 22:50 (Sections 3--8 and Appendices
A, C, E). They must be rechecked after the other authors' final revisions, in
particular:

- the integer lattice theorem `thm:int:lowrank`, whose unary class is being
  extended (the introduction and table now say "separable convex polynomial
  terms", not quartics);
- `thm:qp:two` (Gaussian accuracy b), the table's per-result sampling bits, and
  the per-draw output sizes of `thm:int:native` and `thm:int:flow-boundary`;
- Luna's literature audit, which had not appeared; the prior-work subsection
  `sec:intro:prior` uses only claims listed in Section 6 below and must be
  re-verified against that audit.

## 2. Labels defined, and labels other authors already cite

Defined here: `sec:model`, `sec:model:input`, `sec:model:noise`,
`sec:model:algorithms`, `sec:model:outputs`, `sec:model:parameters`,
`sec:model:original`, `sec:model:atom`, `eq:model:sampled`,
`eq:model:interval`, `def:model:grid`, `def:model:perturbation`,
`def:model:algorithm` (items `it:model:every`, `it:model:once`,
`it:model:expect`), `def:model:outputs` (items `it:model:rational`,
`it:model:implicit`, `it:model:charted`, `it:model:algebraic`,
`it:model:component`), `prop:model:regret`, `ex:model:tie`; `sec:intro*`,
`tab:intro:results`; `sec:lim`, `sec:lim:width`, `sec:lim:ambient`,
`sec:lim:constraints`, `sec:lim:points`, `sec:lim:rank`, `tab:lim:summary`,
`eq:lim:retain`, `eq:lim:completion`, `eq:lim:aux`, `thm:lim:width`,
`prop:lim:local`, `prop:lim:conditional`, `thm:lim:ambient`,
`thm:lim:constraints`, `ex:lim:coupled`, `prop:lim:threshold`, `rem:lim:dk`,
`prop:lim:value`, `thm:lim:posslp`, `prop:lim:flow`; `sec:disc*`; `app:lim`,
`app:lim:ambient`, `app:lim:posslp`, `app:lim:flow`, `lem:lim:signs`,
`lem:lim:amplifier`, `lem:lim:tree`, `lem:lim:trace`, `lem:lim:pairs`,
`lem:lim:gates`, and equation labels `eq:lim:amb-*`, `eq:lim:gate-bounds`.

Cited by other authors (all still defined; do not rename): `def:model:grid`,
`def:model:outputs`, `def:model:perturbation`, `eq:model:interval`,
`ex:model:tie`, `it:model:algebraic`, `it:model:component`,
`it:model:implicit`, `prop:model:regret`, `sec:model:algorithms`,
`sec:model:input`, `sec:model:parameters`, `ex:lim:coupled`, `prop:lim:flow`,
`prop:lim:local`, `prop:lim:threshold`, `thm:lim:constraints`,
`thm:lim:width`.

Removed after the root's integration review: `prop:lim:rotating` and
`prop:lim:rank` (duplicates of `ex:rec:fiber` and `prop:rec:rank`, which
Section 7 proves in Appendix E). No other file referenced them.

## 3. Source-to-label coverage

| Source development (inventory id) | Manuscript location | Proof |
| --- | --- | --- |
| Global-error cell barrier (X1), `global-error-cell-barrier.md` | `thm:lim:width` | Main text, full |
| Bag-local star (X2), `local-error-recourse-interface.md` §1 | `ex:rec:star` (Sect. 7, γ=0 values) and `prop:lim:local` (every draw with σ ≤ 1/1000, level-0 nonclosure) | Main text |
| Conditional-recourse interface (B10), same note §§2–3 | `prop:lim:conditional` | Main text, full |
| Positive-definite star, same note §5 | Mentioned in Sect. 7 text (`app:rec:examples`) | Not mine |
| Ambient count-surrogate barrier (X3), `ambient-local-count-barrier.md` §§2–6 | `thm:lim:ambient`; Sect. 4 states it as `prop:qp:ambient-barrier` | `app:lim:ambient`, full |
| Fiber sharpness (X3 §1) | `prop:qp:fiber-sharp` (Sect. 4) | Not mine |
| Affine feasibility barrier (X4), `constrained-smoothing-barrier.md` §§1–2 | `thm:lim:constraints` | Main text, full |
| Diagonal TU count (X4 §3) | `ex:lim:coupled`; complements `ex:rec:feasibility` (corner bound) | Main text |
| Width-two hardness compatibility (X8), `sparse-smoothed-hardness-sanity.md` | `prop:lim:threshold`, `rem:lim:dk` | Main text |
| Rotating fiber (X7), `core-only-noise-rotating-fiber.md` | `ex:rec:fiber` (Sect. 7), cross-referenced in `sec:lim:points` | Not mine |
| Regularization precision, `regularization-point-precision-obstruction.md` | `prop:lim:value` (a)–(d), with independent noisy core | Main text, full |
| Square Root Sum at treewidth two (X15; decision 11), `convex-active-set-radical-comparison.md`, `convex-point-radical-comparison.md` | `thm:lim:posslp`(a),(c) | `app:lim:posslp`: `lem:lim:tree`, `lem:lim:trace`, `lem:lim:signs`, `lem:lim:amplifier` |
| PosSLP reduction (X15), `posslp-convex-point-extraction.md` | `thm:lim:posslp`(b),(c) | `app:lim:posslp`: `lem:lim:pairs`, `lem:lim:gates` and the shared lemmas |
| Single-flow boundary obstruction (X6), `core-only-flow-boundary-obstruction.md` | `prop:lim:flow` (cited by Sect. 8) | `app:lim:flow`, full |
| Rank separation (C4), `polynomial-recourse-rank-separation.md` | `prop:rec:rank` (Sect. 7), discussed in `sec:lim:rank` | Not mine |
| Original-objective consequence (F18) | `prop:model:regret` and calibration paragraph | Main text, full |
| Finite-law atom needing fallback (contract) | `ex:model:tie` (new elementary example; complements `ex:count:atom`) | Main text, full |

Not covered here, by assignment: X5 (graph parameterization obstructions, Sect.
6), X9 (`rem:qp:moments`), X10 (`ex:count:atom`), X11–X14, and X16 (the
deterministic flow-core error bound; it belongs in Section 8, or follows from
`prop:rec:search`(b), and is not stated by any author at present).

## 4. Original versus classical, and overlap

Classical and cited: smoothed analysis; isolation-type anticoncentration;
qualitative genericity of tilts; tree-decomposition DP; exact convex QP; GLS;
exact convex MIQP in fixed integer dimension; separable convex TU optimization;
block-sensitive quantifier elimination and other real-algebraic tools; the
PosSLP/Square Root Sum relation; the trace argument (classical algebraic number
theory, proved inline). The introduction says explicitly that the finite-law
model, isolation-type anticoncentration, one-root algebraic representations,
and connected-set counting are not claimed as new.

Contributions named in `sec:intro:prior`: route-specific certificates and
expected bounds (critical-region closure; patch closure after global-error bag
search; excluded-region, competing-label, and optimal-face certificates), the
strong-noise composition, and the boundary results. No priority claim.

Overlap with unpublished companions, stated by bibliography key:

- `companion-exact-arithmetic` ("Exact Arithmetic in Polynomial Optimization:
  Values, Optimizers, and Certificates"): value and selected-core oracles under
  core noise for convex residual problems; finite-law replacement and section
  arguments in that setting; the Square Root Sum and PosSLP point reductions
  (its `thm:points-quartic-lower`) and the regularization proposition (its
  `prop:points-regularization`). Here they are reproduced with proofs in
  `thm:lim:posslp`(a),(b) and `prop:lim:value`; part (c) of `thm:lim:posslp` is
  the core-only consequence. The constants of my sign-test and amplifier lemmas
  (ε=κ/4, η=μ₀/12) differ from the companion's (ε=1/32, η=1/192); the stated
  structural bounds (treewidth two, bounded coefficients, diagonal ≤ 20) are
  re-derived for my constants.
- `companion-decomposition-aware` ("Decomposition-aware global optimization:
  certified coordinate grids, conditional recourse, and structural limits"):
  deterministic curvature-corrected grids, min-marginal filtering, a star
  example related to `ex:rec:star`; no random perturbation.
- `companion-sparse-indicator` ("Sparse indicator quadratics: exact complexity
  and smoothed separator messages"): smoothed separator messages under a
  different perturbation model.

The overlap statements rely on the inventory's reading of those manuscripts and
on my direct reading of the exact-arithmetic points section and Appendix C;
Luna should confirm the attribution wording.

## 5. Mathematical findings and repairs

1. `thm:lim:ambient` generalizes and sharpens the source. Both counts are proved
   for α ∈ {1, m}. The finite-law version holds for every power of two M ≥ 32,
   not only M ≥ 64m²: the atom count gives P{γ_i ≤ −1+4/n} ≥ (2/n)(1−1/M) ≥
   19/(10n) once M ≥ 20, and Var γ_i ≤ 3/8 once M ≥ 17. Notation follows
   Section 4 (ζ, ξ, E_h). The theorem is presented as the proof of Section 4's
   `prop:qp:ambient-barrier`; the root should keep only one statement or make
   Section 4's a pointer.
2. `prop:lim:local` is now an every-draw statement (σ ≤ 1/1000): every optimizer
   has v > 1/2 and z₁ < 1/2, and the deletion margin 19/32 − 33σ stays
   positive. Following Sol's early review, level-0 nonclosure is proved (all
   derivatives take both signs; the Hessian form at (1, ¼𝟙) is −2) and J ≥ 1 is
   taken from the sparse schedule.
3. `prop:lim:threshold` now assumes δ ≥ 0 (Sol finding 1, counterexample
   δ=−2), and its conclusion is narrowed to "these guarantees do not by
   themselves provide a polynomial-time algorithm" (Sol finding 2).
   `rem:lim:dk` gives the Del Pia–Khajavirad no-family with gap 2^(−2r−4) and a
   witness coordinate equal to one, as the contract requires; it depends on
   their construction and needs Luna's confirmation (Section 6).
4. `prop:lim:conditional` (B10) is new as a manuscript statement: with
   certified conditional values of error a·pLh²/8, the bag-local allowance
   e = pLh²/8 is sound, U_j ≤ f*+(1+a)e, witnesses are within 2(1+a)e, and the
   count is Π[4 + (1 + (1+a)p/2)Lw_i/(2σ)], with no factor n. It is stated as a
   sufficient interface, not an algorithm.
5. `thm:lim:posslp` now has three parts: (a) Square Root Sum, treewidth two,
   bounded coefficients, unit box, ∂ᵢᵢ ≤ 20 (decision 11); (b) PosSLP, no
   structural bounds claimed; (c) core-only consequences. Shared lemmas:
   sign test with modulus 3κ/4 and amplifier with modulus μ₀/2. The commentary
   now says the residual problem has no positive uniform modulus on its box
   (the y-curvature vanishes where both activation coordinates are zero), as
   Sol noted.
6. `prop:lim:value` uses x_n* ≤ 14·28^(−2^n) ≤ 4^(−2^n), so the gap is at most
   2^(−2^(n+2)) and the Tikhonov parameter needs λ ≤ 2^(−2^(n+2)).
7. `ex:model:tie` is new: on [0,1]², F₀ = 2x₁x₂ − x₁ − x₂, σ ≤ 1/4, the event
   γ₁=γ₂ has probability exactly 1/M and the optimal set is exactly
   {(1,0),(0,1)}; it forces β ≥ 1/M in any finite-law growth tail and rules out
   every strongly convex patch certificate on that event.
8. Model corrections from the root's early review: fallback scope (lattice and
   strong-noise theorems need none); regret endpoints are rational only after
   evaluation, with exactly feasible algebraic lifts on implicit graphs;
   Gaussian-like calibration by the support radius (b+20)σ with an explicit
   choice σ = 2^(−t); "models coincide in special cases" wording; promises for
   correctness versus for complexity; charted output format; noise scale σ;
   certificate length in I and verification work in the work bound; sparse
   (variable, exponent) monomial encoding, which the width example's
   I = O((n+p²) log n) needs.
9. Discussion no longer lists a universal finite law as open for the
   polynomial-bit routes, pending `author-reports/universal-law-budget-sol.md`.
   Once that report is final, a sentence on uniform resolutions can be added to
   `sec:disc:limits`.

## 6. Bibliographic requests (for the Luna lead, via the root)

Keys now used in my files, with the claim each supports:

- `pardalos1991-quadratic-programming-with-one` (not in the shared bib; please
  add): QP with one negative eigenvalue over a polytope is NP-hard.
- `pia2026-treewidth-and-the-complexity-of`: (i) strong NP-hardness of box QP
  at treewidth two with bounded integral coefficients (theorem number); (ii)
  the objective is a nonnegative sum of squared residuals with threshold zero;
  (iii) the no-instance family of `rem:lim:dk` (items A, A+2, target A+1,
  A = 2^r) has a feasible point with final square 2^(−2r−4), all other terms
  zero, and an indicator coordinate equal to one.
- `spielman2004-smoothed-analysis-of-algorithms-why`: smoothed analysis.
- `beier2006-typical-properties-of-winners-and`,
  `roglin2007-smoothed-analysis-of-integer-programming`: polynomial smoothed
  complexity closely tied to pseudo-polynomial solvability.
- `lee2017-generic-properties-for-semialgebraic-programs`: under a constraint
  qualification, generic tilts give a unique minimizer with quadratic growth.
- `bertele1972-nonserial-dynamic-programming` (used by other authors; not in
  the shared bib).
- `kozlov1980-the-polynomial-solvability-of-convex`: exact polynomial-time
  convex QP.
- `grotschel1988-geometric-algorithms-and-combinatorial-optimization`.
- `pia2025-convex-quadratic-sets-and-the`: exact convex MIQP in fixed integer
  dimension (literature request 1).
- `hochbaum1990-convex-separable-optimization-is-not`: separable convex
  optimization over TU systems.
- `renegar1992-on-the-computational-complexity-and`,
  `basu2006-algorithms-in-real-algebraic-geometry`, and `BasuLerario2023`
  (alias used by another author; the shared bib has
  `basu2021-hausdorff-approximations-and-volume-of`; please resolve).
- `kelner2007-on-the-hardness-and-smoothed`: expected polynomial time for
  low-rank quasi-concave minimization over polytopes under a random rotation of
  the low-rank subspace, via projected-vertex counts.
- `vavasis1992-approximation-algorithms-for-indefinite-quadratic`:
  approximation with work polynomial in the inverse accuracy for a fixed
  number of negative eigenvalues.
- `bienstock2018-lp-formulations-for-polynomial-optimization`: LP
  approximations of bounded-treewidth polynomial optimization, polynomial for
  fixed width.
- `allender2009-on-the-complexity-of-numerical`: Square Root Sum is
  polynomial-time decidable with a PosSLP oracle; both lie in the counting
  hierarchy.
- New unpublished entries: `companion-exact-arithmetic`,
  `companion-decomposition-aware`, `companion-sparse-indicator` (titles in
  Section 4; author fields to be handled by the root).

## 7. Integration notes for the root

- Two notations for the grid law: `def:model:grid` defines U_{σ,M} (used by
  Sections 5, 7, 8), while `def:count:laws` defines 𝒰_{σ,M} (Sections 3, 4).
  One definition and one symbol should remain.
- `rem:qp:regret` (Section 4) partly repeats `prop:model:regret`; it could cite
  it.
- The introduction's table caption defines Q_ex and Q_ap again; Section 7 owns
  `eq:rec:Q`.
- X16 is not stated anywhere yet.

## 8. Checks actually run

All were targeted to my files. None is a CI result or a project-wide check.

1. Scratch LaTeX harness in `/tmp/sgfront-check` (outside the repository):
   `main.tex` built from the preamble lines of `main.tex`, my six files, and
   auto-generated stub targets for every external label they cite;
   `pdflatex -interaction=nonstopmode` three times. Final result: no LaTeX
   errors, 0 undefined references, 0 overfull boxes, no font warnings; the only
   warnings are undefined citations (no `references.bib` yet). Earlier runs
   found two overfull boxes in Appendix G and two in the results table, an
   italic small-caps font substitution, and both large tables drifting to the
   end; all were fixed (table placement `[tbp]`).
2. Inline Python cross-reference check (`python3 -`): every `\ref`/`\cref` in
   my files resolves to a label defined in the current manuscript tree; there
   are no duplicate labels among all present section and appendix files; every
   label of mine cited by other authors is defined.
3. Inline Python proof diagnostics (`python3 -I -`, exact `Fraction` arithmetic
   unless stated): tie example (zero not an atom for M = 4, 8, 16; tie
   probability exactly 1/M; on a 41×41 rational grid the shifted objective is
   nonnegative with zeros exactly at (1,0) and (0,1)); star example (corner
   values 23/32, 27/32, 31/16, 31/16; for 200 random rational noise vectors
   with |γ_i| ≤ 1/1000 the local rule deletes and the global rule retains the
   cell; Hessian form −2); width barrier (vertex optimality and the 3p/40
   completion bound on random rational points for (n,p) ∈ {(4,2),(5,3),(6,3),
   (6,4)}; the inequalities 29p/400+1/200 ≤ 3p/40 and h_J² < 3p/(10n) for
   2 ≤ p ≤ n < 200); ambient-barrier constants (e^(57/64) > 12/5,
   e^(19/20) > 5/2 in floating point, 41/160 > 1/4, the flatness and gap
   inequalities for m ∈ {256, 258, 512, 1024} and α ∈ {1, m}, the atom
   probability ≥ 19/(10n) for M ∈ {32, 64, 1024}); chain bound x_n* ≤ 4^(−2^n)
   for n = 1..5 (floating-point fixed-point iteration); tree Hessian ≥ 1/8
   (floating-point eigenvalues, random leaves, n ∈ {1,2,3,5,8}); flow event
   probability exactly 1/4 per coordinate for M = 4..256. A first gate-Hessian
   check by floating-point finite differences failed through cancellation with
   weights near 64^N; it was replaced by an exact check: for 24 random
   straight-line programs (s = 3..6) at rational points of the box, the exact
   Hessian satisfies D⁻¹HD⁻¹ ⪰ (559/504)I and H ⪰ I by exact rational
   elimination (with a 10⁻⁹ diagonal slack), and the gate bounds
   (|p_i| ≤ 1/4, ‖∇p_i‖₁ ≤ 1, triangularity) hold. The amplifier identity and
   the chain quartic identity were checked exactly at 500 random rational
   points each. All passed.

These diagnostics corroborate the symbolic proofs on finite cases; they do not
replace them and are not computational experiments.

## 9. Later revisions in this round

Made after the contract additions of 23:07 and the universal-law report:

1. `prop:model:uniform` (new, Section 2, with proof): every theorem with
   polynomial sampling precision keeps its contract when its law is replaced
   by one resolution depending only on the input length, M(I) = 2^{P(I)} for
   grid laws (lattice cap reset to log₂M), or b(I) = A(I) + D(I)t(I),
   t(I) = ⌈4 log₂(A+D+21)⌉, for Gaussian-like laws with the auxiliary box and
   cap recomputed. Qualifications kept: fixed format constants and oracle
   implementation; domains with polynomial-length widths (counterexample
   1 ≤ x₀ ≤ 2, x_i = x_{i−1}², width 2^{2^N}−1); nonlinear boundary flow/TU
   only with a supplied K and F(K) in all bounds; strong-noise q_i recomputed
   for the chosen M (not monotone), sufficient regime preserved. Source:
   `author-reports/universal-law-budget-sol.md`; stated as an elementary
   consequence, not a priority claim. The proof cites `lem:count:transfer`,
   `thm:count:fallback`, `lem:count:finite-tails`, `app:qp:main` (support and
   precision loop), `thm:int:lowrank`, `thm:int:flow-boundary`, `thm:int:tu`.
2. The discussion's limitation now cites `prop:model:uniform`; the open
   question on universal laws was replaced by the narrower question about the
   parameter-dependent precision of nonlinear core-only flow results.
3. Original-objective calibration (Section 2, introduction, discussion) now
   states the bound after substituting σ (example: Theorem `thm:sp:main`
   becomes C₀^p[4+(1+n/2)Lw_max Σw_i/ε]^p poly_d(I)), and says "polynomial in
   1/ε with the other numerical parameters fixed; polynomial in I and 1/ε only
   when those parameters are polynomially bounded". Gaussian calibration uses
   the support radius (b+20)σ with σ = 2^{−t}; aligned calibration uses the
   projected widths ω_X(T_{i·}).
4. The results table now has a sampled-bits column and per-draw output sizes
   for `thm:int:native` (c_d^k poly_d(I)) and `thm:int:flow-boundary`
   (f_d(k) poly_d(I)); its caption was shortened to fit one page.

Checks after these revisions: the scratch harness rebuild (three pdflatex
passes) has no errors, no overfull boxes, no oversized floats, and 0
undefined references; the cross-reference script again found no unresolved
references from my files and no duplicate labels in the tree.
