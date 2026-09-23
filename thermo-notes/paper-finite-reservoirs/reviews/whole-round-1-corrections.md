# Whole-paper round 1 — corrections

All five accepted merged issues are addressed. The corrected manuscript is ready for the required second whole-paper round. The workflow and previous reports were not edited.

## 1. Explicit nonnegative curvature in the necessity proposition

`sections/boundary-and-smooth.tex`, Proposition `prop:smooth-necessity`, now explicitly assumes `kappa_N >= 0`. This closes the literal counterexample allowed by the previous wording: with `h_N=0`, `Q_N=P_N`, and `kappa_N=-1`, the curvature lower bound held but its claimed conclusion failed. With the stated nonnegative scale, the existing chord bound traps the nonnegative quantity proportional to `kappa_N N^(3/2)` below a quantity tending to zero. The proof and all physical applications therefore remain valid. This is the formal statement change that triggers the repeat five-reader review.

## 2. Nonnegative vector-Gaussian curvature

`sections/gaussian-geometry.tex`, equation `eq:multivariate-gaussian-model`, now repeats `kappa_N >= 0` beside the independent vector model definition. Its integrability, transformed covariance, and later scale statements no longer rely on implicitly inheriting that sign from the scalar model. No formula changed.

## 3. Exponential-cap wording

`appendices/short-range-proof.tex` now says “positive exponential cap.” This identifies the smooth exponential branch without suggesting that the minimum-truncated activity is smooth. The proof still uses only absolute continuity before removing the cutoffs and takes second derivatives afterward.

## 4. Canonical coexistence heat capacity

The introduction now contains equation `eq:canonical-coexistence-capacity`:

`C_S,can/(k_B N^2) = beta_N^2 Var(E_N)/N^2 -> beta^2 w_- w_+ ell^2`.

The paragraph is explicitly restricted to the verified microscopic models. Its proof uses bounded spin energy per particle and convergence to the two-atom law, which imply convergence of both first and second moments. The variance of a two-atom law with gap `ell` is `w_- w_+ ell^2`. Independent kinetic variables add only `aN/beta_N^2` to the variance. The ordinary canonical heat-capacity identity follows by differentiating the finite canonical partition function at the specified temperature with Hamiltonian fixed.

The explanation states that the proved phase moments bound within-phase variances by order `N`, allowing degeneracy. It makes only the leading `N^2` statement and introduces no unjustified `O(N)` remainder based on limiting phase weights or nominal centers. It then explains why secant calibration permits `N^(3/2) << c_N << N^2`: its correction of relative phase bias makes full-law accuracy possible with a bath smaller than the complete subsystem's canonical coexistence heat capacity.

## 5. Narrow primary capillarity attribution

The capillarity subsection now credits established fluctuation/droplet competition and toroidal Potts droplet/strip configurations as motivation. It explicitly states that neither cited work supplies this paper's assumed full density envelope or derives its square-torus rate for the microscopic systems. The variational model and every hypothesis remain unchanged.

Verified primary sources and bibliography additions:

- **Biskup, Chayes, Kotecký (2002):** [arXiv record](https://arxiv.org/abs/math-ph/0207012) and [primary PDF](https://arxiv.org/pdf/math-ph/0207012). Page 2, equations (1)–(2), sets out Gaussian background cost and droplet surface cost. The abstract distinguishes its two-dimensional rigorous setting from heuristic generalizations. Metadata verified: *Europhysics Letters* **60**(1), 21–27; DOI `10.1209/epl/i2002-00312-y`.
- **Kim, Keyes, Straub (2011):** [author-hosted primary PDF](https://people.bu.edu/straub/pdffiles/pubs/JCP.135.061103.2011.pdf). The setup on page 3 specifies toroidal Potts geometry; page 4's Figure 3 discussion identifies droplets, strips, and their transition markers. Metadata verified on page 1: Jaegil Kim, Thomas Keyes, John E. Straub; *The Journal of Chemical Physics* **135**(6), 061103; DOI `10.1063/1.3626150`.

The primary PDFs and extracted texts are retained as `sources/biskup-chayes-kotecky-2002.{pdf,txt}` and `sources/kim-keyes-straub-2011.{pdf,txt}`. Europe PMC did not supply a usable response; the openly accessible author PDF supplied the needed primary evidence without bypassing any access control.

## Validation

Rechecked the sign-dependent chord inference, the elementary two-atom variance limit, and the independent kinetic variance addition analytically. Checked source passages directly before inserting citations. The manuscript now has 25 cited entries, no missing citation keys, no duplicate labels, and no missing reference labels. `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` succeeds and produces a 48-page PDF. The final log contains no warnings or overfull/underfull box diagnostics. The existing numerical formulas were untouched; no unrelated calculation or research direction was added.
