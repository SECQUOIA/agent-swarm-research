# Whole-paper review, round 2, reviewer 1

Verdict: **no major or minor issue found in the corrected manuscript**. All five accepted corrections are implemented and consistent with the rest of the paper. I recommend acceptance of the current mathematical content, subject to the coordinator's adjudication of the independent reviews. I identify no further correction or additional numerical experiment that is necessary.

## Independence and scope

The review target is the current 48-page `main.pdf`, generated September 7, 2026, at 03:20:57 EDT, and its current LaTeX inputs. I read `whole-round-1-adjudication.md` and `whole-round-1-corrections.md` as instructed, but no other reviewer's report. My previous independent review informed the checks of unchanged material; the current complete manuscript was reread rather than treating the earlier verdict as proof.

I reread `main.tex`, all eleven section files, the full short-range appendix, every theorem and proof, `refs.bib`, `README.md`, and `COVERAGE.md`. I reassessed the numerical section and figure formulas against the numerical source and successful independent computations documented in my own round-1 report. No numerical algorithm or numerical theorem formula changed, so I did not repeat the occupation enumeration or direct quadratures. I made no manuscript, data, or code edits and did not delegate.

## Verification of the accepted corrections

### 1. Nonnegative curvature in smooth necessity: resolved

Location: `sections/boundary-and-smooth.tex:19–46`, Proposition `prop:smooth-necessity`.

The proposition now explicitly assumes a nonnegative sequence `\kappa_N\ge0`. I agree with the coordinator that the previous literal statement admitted the stated counterexample: `h_N=0` and `\kappa_N=-1` satisfy a lower-curvature bound but do not imply the claimed vanishing product. This was a material formal omission, even though the physical interpretation suggested the intended sign.

With the corrected hypothesis, the proof is sufficient. The chosen three good energies have distances of orders `sqrt(N)` and `N`; all lie inside the feasible interval and between the phase centers. Their log-likelihood chord defect is `o(1)`, while strong concavity bounds it below by a nonnegative constant multiple of `\kappa_N N^(3/2)`. The desired conclusion follows. The proof does not require the centers themselves to be good energies, a global curvature bound outside their interval, or a density local limit. Both phase variances are explicitly positive. The correction preserves the physical interpretation and the subsequent calibrated converse.

### 2. Vector Gaussian sign: resolved

Location: `sections/gaussian-geometry.tex:121–129`, equation `eq:multivariate-gaussian-model`.

The independently defined vector model now states `\kappa_N\ge0`. This makes integrability, the upper covariance bound, and the subsequent component-matching argument self-contained. Square completion and all weight invariants remain unchanged and correct. The anisotropic extension already explicitly requires a positive-semidefinite matrix.

### 3. Truncation wording: resolved

Location: `appendices/short-range-proof.tex:107–127` and the proof of `lem:sr-restricted-derivatives`.

“Positive exponential cap” correctly describes the cap without claiming the minimum-truncated activity is smooth. The proof continues to use absolute continuity and first derivatives almost everywhere before cutoff removal, and smooth second derivatives afterward. The change is consistent with the BCT truncation and does not conceal an altered mathematical input.

### 4. Canonical coexistence heat capacity: correct and appropriately scoped

Location: `sections/introduction.tex`, equation `eq:canonical-coexistence-capacity` and its surrounding paragraph; PDF page 4.

For a fixed Hamiltonian, the finite canonical identity is `C_can/k_B = beta_N^2 Var(E_N)`. For the verified microscopic examples, the bounded spin energy per particle has a two-atom weak limit. Boundedness yields convergence of its first and second moments, so `Var(U_N)/N^2 -> w_- w_+ ell^2`. An independent kinetic sector contributes `aN/beta_N^2`, which vanishes after division by `N^2`. Thus the new displayed limit is correct, including pure spins and the stated balancing temperature shifts when their limiting weights are used.

The positive phase exponential moments give second moments about their nominal centers of order `N`, hence within-phase variances at most order `N`; degeneracy causes no problem. This is consistent with the ordered mean-field variance, degenerate disordered pure-spin variance, and short-range contour-phase moments. The leading full-law variance is instead the phase-separation contribution.

The paragraph is expressly limited to these microscopic examples. It does not wrongly derive moment convergence from an arbitrary weak-support limit, infer heat-capacity convergence from TV, or assert an `O(N)` remainder using limiting weights. The comparison with `N^(3/2) << c_N << N^2` follows directly from the two-phase reservoir theorem. It clarifies why the complete canonical coexistence heat capacity and the optimized reservoir requirement need not have the same order.

### 5. Added capillarity attribution: supported and narrow

Location: `sections/capillarity-diagnostics.tex:45–52`, and the first two entries in `refs.bib`.

I checked the retained primary texts directly. Biskup–Chayes–Kotecký, *On the Formation/Dissolution of Equilibrium Droplets*, describes Gaussian background cost and droplet surface cost in equations (1)–(2) on page 2 and explains their competition. Its abstract distinguishes its rigorous two-dimensional Ising setting from heuristic generalizations. The manuscript credits the mechanism without importing a Potts theorem from that source.

Kim–Keyes–Straub, *Communication: Iteration-free, weighted histogram analysis method in terms of intensive variables*, specifies the toroidal two-dimensional Potts model and discusses droplet and strip configurations and their transition markers near Figure 3. Its first page confirms the author names, journal volume 135, article 061103, year 2011, and DOI `10.1063/1.3626150`. The manuscript's limited claim that these configurations are exhibited is supported.

The explicit following sentence correctly prevents either citation from being treated as a derivation of the assumed full density envelope or the square-torus rate function. The capillarity LDP hypotheses, variational proof, and nonidentifiability of tie weights are unchanged.

## Complete-paper reassessment

The reread found no new issue in the unchanged proof chain:

- The exact physical likelihood is bounded, its cutoff is handled explicitly, and energy TV equals microscopic TV. Centered calibration supplies the global bound needed for weak-support sufficiency without tail assumptions.
- Weak-support necessity still uses good energies and an exact chord identity, so arbitrary physical cutoffs and tuning sequences are covered. The two-scale version retains the small chord factor `s_N/Delta_N` and requires divergence of `s_N`; it allows nondegeneracy in only one phase.
- Positive-tail sufficiency supplies uniform integrability by a tangent bound and treats amplified exceptional mass separately. The density-envelope alternative controls the inward tail even at `alpha=1/2` when the tilt vanishes.
- Mean-field minima, Hessians, phase multiplicities, energy variances, Gamma/Beta formulas, and optional momenta agree with the reservoir hypotheses. The short-range proof keeps midpoint weak-limit phases distinct from positive contour moment phases, identifies stable branches with the correct normalization, and transfers bond moments to the exchanged spin energy through binomial noise.
- The boundary theorem has the required strict moment window and exceptional-mass suppression. The global optimum still uses positive overlap to confine every calibration beating both phase-discard costs to the finite `sqrt(N)` correction window. It does not assume that conclusion or exclude escaping calibrations without proof.
- Shared-bath TV and information statements use bounded microscopic likelihoods. The KL argument is separate from TV convergence, and the linear-capacity covariance result remains a weak Gaussian-law statement with positive variance assumptions.
- Gaussian geometry includes arbitrary fields and escaping sphere centers. The finite linear-system feasibility step in the optimal phase-loss proof remains valid. The anisotropic extension makes only its stated algebraic claims.
- The compact capillarity tilt, square-torus minimizers, histogram norm distinction, and exact midpoint barrier gain remain correct within their stated models. No microscopic morphology or dynamical-rate assertion is introduced by the added citations.

The abstract, theorem-summary table, conclusions, README, and coverage audit retain the material limitations: sufficiently large fixed `q`, separate moment and exceptional-mass assumptions, the restricted two-dimensional boundary range, and the distinction between finite microscopic calculations and exact illustrative models.

## Validation and remaining limits

I checked the current source labels and citation keys: no duplicate labels, no missing reference labels, and no missing citation entries; there are 25 cited bibliography entries. The current PDF has 48 pages. Its existing build log has no warning, undefined-reference, or overfull/underfull diagnostics. I rendered and visually inspected the two pages containing the new explanatory passages, pages 4 and 43; the equation and citations are legible and integrated cleanly.

The archived numerical-data SHA-256 still matches the README value `93fed9507ceaf9126feb93e79ae5bbb295be185a56f9a84dabe0608e55aab2c1`. The numerical evidence from my independent round-1 computations remains applicable because the formulas and implementation were not changed. I did not repeat expensive calculations merely for the review cycle.

This is an independent review of mathematical validity, source support, and presentation, not an exhaustive historical-priority search or an interval-certified numerical audit. Within that scope, I find no remaining revision to request.
