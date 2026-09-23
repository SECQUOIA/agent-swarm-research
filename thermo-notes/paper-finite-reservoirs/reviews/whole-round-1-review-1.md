# Whole-paper review, round 1, reviewer 1

Verdict: no major issue found. The principal probability and analysis claims are supported by the stated hypotheses and proofs. I recommend accepting the mathematical content subject to root adjudication and the other independent reviews. The two optional editorial clarifications below do not require a new mathematical review cycle.

I reviewed the manuscript independently, without reading current or previous reviewer reports or author-stage verdicts. I did not edit the manuscript, figures, data, or numerical source, and did not delegate. This report concerns the 47-page `main.pdf` generated on September 7, 2026, and its source files as read during this review.

## Findings

### Major findings

None found. In particular, I found no false claim, missing substantive hypothesis, or consequential proof gap in the weak-support necessity, positive-tail sufficiency, or optimization over arbitrary physical total energies.

### Minor editorial findings

1. **Repeat nonnegative curvature in the multivariate Gaussian model.** Location: `sections/gaussian-geometry.tex:121–129`, equation `eq:multivariate-gaussian-model`. The scalar model explicitly states `\kappa_N\ge0`; the new vector model uses the same parameter without restating that assumption. The ensuing proof uses transformed covariance at most `NI_d`. The intended restriction is clear from the preceding scalar model and reservoir context, so I do not classify this as a substantive missing hypothesis in the manuscript as a whole. Adding `\kappa_N\ge0` alongside `t\in\mathbb R^d` would make the independently readable vector theorem unambiguous.

2. **Avoid a potentially misleading use of “smooth” near the minimum truncation.** Location: `appendices/short-range-proof.tex:113–115`. “This positive smooth cap” can correctly refer to the exponential cap itself, but a reader could take it to describe the truncated activity `min(K_i, exp(-\tau m))`, which need not be smooth. Later paragraphs correctly recognize this and avoid twice differentiating the minimum. “This positive exponential cap” would remove the ambiguity without changing the argument.

## Scope and analytic checks

I read `main.tex`, every input section and appendix, all theorem/proposition/lemma statements and their proofs, the abstract and conclusions, `refs.bib`, `README.md`, and `COVERAGE.md`. I read all four Python files, inspected both rendered figure PNGs, checked their connection to the formulas and archived data, and inspected PDF metadata and the existing build log. The existing log contains no reported warning, undefined-reference, or overfull/underfull-box messages. I did not rerun the expensive `N=12000` enumeration.

### Exact physical law and weak-support theorem

The surface-density convention, canonical capacity offset `c+1`, boundedness of the unnormalized likelihood, admissibility criterion, and exact equality of energy and microscopic TV are consistent. The centered weight is bounded by one on the entire energy line, including below any nominal phase interval and above the cutoff. This bound is essential to the advertised sufficiency without a moment assumption, and the proof uses it correctly.

I checked the chord identities and the bound on `f_theta` directly. In `sections/thresholds.tex:93–123`, TV convergence supplies three feasible good energies even for discrete or singular energy laws. Portmanteau gives positive probabilities of separated open intervals; no positive mass at an individual selected energy is needed. The arbitrary cutoff cannot remove these selected energies, since their normalized likelihood is near one. The endpoint identity gives `c q ~ beta D`, and the chord inequality then forces first `q -> 0`, then `c q^2 -> 0`. This proves `c >> b^2` without assuming a residual bath energy scale in advance. The exactly two-atom exception follows from exact endpoint equality and is correctly distinguished from a two-atom scaling limit.

For two-scale necessity, the degenerating chord factor is retained: `theta(1-theta) ~ s/Delta`, giving a lower bound proportional to `min(Delta s/c,s)`. The divergence of `s` is explicitly assumed and supplies the required conclusion. The argument still works when only the upper phase is nondegenerate. It does not silently assume both variances positive or a vanishing exceptional mass for necessity.

### Positive tails and the continuous-density alternative

The secant derivative and amplification bounds follow from exact endpoint residual energies and concavity. The phase exponential moment supplies uniform integrability of the likelihood by the tangent bound; the separate amplified exceptional-mass condition is used on a positive measure, not a signed remainder. The more general sufficient scale involving the exceptional rate is correctly presented as sufficient rather than necessary.

I checked the density-envelope proof at the limiting exponent `alpha=1/2`. When `kappa N^(3/2) -> 0`, both ratios of the interior bath gain to the two allowed costs vanish, including at equality. Exterior tails cannot be amplified. The local masses sum to one and therefore establish tightness of the two phase windows. The extraction of positive midpoint conditional phase laws for necessity is valid. The boundary discussion correctly requires `alpha>1/2` for all fixed finite tilts by this route.

### Physical boundary and global calibration optimum

I independently checked the signs and constants in the endpoint slopes, the `d sqrt(N)` energy correction, the integrated Gaussian phase factors, compensation coefficient, and CDF formula. The strict inequality `eta>b` provides an actual `L^p` bound for some `p>1`; weak convergence alone is not used to infer tilted moments or TV. The exceptional condition removes the exceptional contribution after any bounded correction because the maximum log weight changes by only `O(1)`.

The global lower-bound argument in `sections/boundary-and-smooth.tex:220–251` is sound. Any calibration with limiting error below both phase weights has positive overlap with both target phases. Tightness, small-likelihood overlap control, and the normalization bound on large likelihoods produce two feasible points with bounded positive normalized likelihood. Solving their exact likelihood ratio confines the composite energy to `O(sqrt(N))` of secant calibration. This handles arbitrary cutoff and escaping-energy sequences rather than assuming the finite-correction window. The alternative centered calibrations attain the two phase-discard costs using weights bounded by one. Degenerate Gaussian phase laws are consistently permitted, including pure-spin mean-field disordered energy.

The scalar CDF optimizer is convex; when both variances are positive its derivative is strictly increasing and crosses zero. The equal-variance optimum remains at the original phase weights even when they are unequal. Phase-discard candidates must still be compared separately, as the theorem does.

### Microscopic results and short-range source inputs

For mean field, I checked the complete stationary-point classification, the two Hessian determinants, phase prefactors including the threefold ordered multiplicity, and the delta-method energy variance. The disordered spin energy has zero variance on scale `sqrt(N)`, while the ordered phase supplies the necessary nondegeneracy. The global occupation bound and Gamma transform justify all fixed exponential parameters for sufficiently large `N`. The Beta exponent `A+c` and second shape `c+1` agree with direct kinetic integration.

I checked the substantive short-range input locations against the local primary texts `sources/bkms1991.txt` and `sources/bct2012.txt`: BKMS Theorem 1, BCT contour diameter/interior bounds, matching-label partition sums and activity ratios, Appendix A's parameter window and truncation, cutoff inactivity, finite-volume estimates, magnetization criterion, and the interface-network sum. The manuscript distinguishes physical spin and random-cluster partition normalizations and the original versus later exterior conventions.

The one-sided Laplace-transform derivation of the conditional CLT is valid: exponential tilting gives a moment-generating function on a neighborhood of zero, compact untilting gives vague convergence, and the independently known phase mass prevents escape of mass. The lower variance bound passes through stable thermodynamic branches and does not mistake total coexistence variance for phase variance.

For positive contour moments, the log derivatives of finite positive interior sums have polynomial contour-size bounds. The exponential cluster majorant absorbs these factors. First obtaining Lipschitz truncated free energies and then removing every cutoff on the `1/L` window avoids an unjustified second derivative of the minimum. The conditional binomial noise argument transfers bond moments to the physical spin energy without falsely identifying bond count and exchanged energy. The surface exponent suffices for `c >> N^(3/2)` in every fixed dimension at least two. For the physical boundary, the all-parameter moment extension in dimensions above two and the restricted range in dimension two follow from the different window and surface scales stated in the paper.

### Shared baths, Gaussian geometry, and capillarity

The shared-bath selection theorems rely on globally bounded weights and therefore need only phase tightness. Joint and marginal TV limits follow from explicit conditioning on opposite assignments or a fixed phase count. The mutual-information arguments separately control `r log r` on a common compact interval; they do not invoke entropy continuity from microscopic TV. The balancing temperature shift has the correct sign and keeps the canonical target explicit. The linear-capacity Gaussian precision update, marginal variances, TV formulas, and information correction are consistent, with weak covariance-law convergence correctly distinguished from convergence of unbounded moments.

For multivariate Gaussian geometry I checked square completion, affine invariants, matching of all components, and the spherical versus nonspherical conditions. The optimal phase-loss proof handles both fields that do not vanish and fields whose induced sphere centers escape. The finite linear-system/Farkas step correctly upgrades asymptotic feasibility to exact feasibility. The anisotropic formulas use the effective metric, and their stated degeneracies are consistent.

The physical interior expansion has the correct cubic sign and order. The compact-support capillarity LDP follows from a uniform bounded tilt. The square-torus inequality gives the claimed threshold and all three equality minimizers. Tie weights, macroscopic concentration, and full TV are correctly distinguished. The histogram `L^2` and TV formulas and the exact `c log cosh(beta Delta/(2c))` midpoint gain check out; the barrier statement remains explicitly at prescribed energies and makes no dynamical claim.

## Numerical and presentation checks

I ran the existing verification functions without invoking their data-writing entry point:

- Explicit enumeration of all labeled spins for `N=1,...,8` passed. Maximum reported energy-mass error was approximately `3.33e-16`.
- At `N=12`, kinetic shape 6 gave direct-quadrature TV `0.0865823732895036` versus CDF TV `0.08658237328030982`; shape 12 gave `0.10307722681537486` versus `0.10307722681538645`. Likelihood and normalization checks passed.
- `check_stage4.py` passed its three weighted-normal quadrature/optimizer cases, physical compensation check, and square-model checks.
- I recomputed all four `N=300` regimes in memory. Their full-TV values agreed with the archived values to approximately `1.11e-16`.
- Re-evaluation of the plotted secant limits gave `0.15739182188178924` and `0.0379859806585022`, matching the text and derived data.
- The archived data contain 18 points. Their SHA-256 matches the README value `93fed9507ceaf9126feb93e79ae5bbb295be185a56f9a84dabe0608e55aab2c1`.

Both figure renderings are legible and their captions accurately separate finite microscopic computations from limiting formulas. The README discloses the unchanged large-size archive, floating-point character of the checks, and absence of short-range simulation. The coverage document preserves the important qualifications on positive tails, two-dimensional boundary coefficients, exact Gaussian assumptions, and capillarity modeling.

## Literature and limits of this review

I read the bibliography and relation-to-work discussion, and checked the local primary-source passages most relevant to the short-range proof and to the comparisons with Riera–Gogolin–Eisert, Griffin–Matty–Swendsen, Ramírez-Hernández–Larralde–Leyvraz, and Cohen–Rittenberg–Sadhu. Those comparisons are appropriately qualified. I did not perform a new exhaustive historical-priority search or independently reconstruct every cited paper. The manuscript does not rely on such a priority claim.

The numerical checks are ordinary floating-point checks, not interval certificates. This review provides an independent assessment of the complete manuscript, not a guarantee that all possible errors have been excluded. No mandatory mathematical revision is identified.
