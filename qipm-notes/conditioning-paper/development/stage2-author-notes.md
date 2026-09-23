# Stage 2 author report

Author: `stage2_geometry_author`.
Status: authored and reviewed by five independent reviewers, with no major
issues. All accepted minor findings were corrected by `stage1_fixer`; see
`stage2-corrections.md` for the correction record.

## Delivered scope

The stage adds `macros.tex` and three self-contained source sections:

- `sections/02-setup.tex`: fixed affine metric, barrier definition, sublevels and difference body, Dikin containment and semiboundedness, exact path existence, unique gap parameterization and classical two-sided gap–μ comparison.
- `sections/03-geometry.tex`: direct approximate containment for every residual below one; difference-body sandwich; equal-gap cross-barrier Loewner and eigenvalue comparisons; aspect-ratio characterization; both spectral edges and the matching diameter law for every fixed barrier; uniform bounded-parameter/residual families and a common attained exact-gap interval; optional canonical slack constants; pointwise compact-sublevel localization.
- `sections/04-widths.tex`: full radial minimax spectral profiles independent of the center, plus the original directed-exit profiles with their stronger pointwise constant and correct equatorial sign convention.

`main.tex` now includes these sections and the existing bibliography. The abstract remains explicitly a stage scaffold: the final introduction, abstract, examples, solver consequences, and numerical results are assigned to later stages. Original manuscript and unrelated folders were not modified.

## Main mathematical decisions and checks

All Hessians are the unscaled relative Hessian of F in the fixed Euclidean/product Frobenius metric. The gradient and residual are relative to the tangent space. Exact centrality is ∇F+c_V/μ=0, with μ>0.

1. **Containment is proved directly.** The barrier gradient inequality implies φ″≥φ′²/ν. Integrating the reciprocal of a positive φ′ proves semiboundedness, including a boundary endpoint by approaching it through the interior. The self-concordance inequality implies |(1/√φ″)′|≤1. Its upper-Hessian direction proves Dikin containment by contradiction with boundary divergence; its lower-Hessian direction gives φ′(t)≥t/(1+t)−ρ.
2. **The residual constant is verified algebraically.** For R equal to the local distance to a sublevel point, choose t₀=(√ν+ρ)/(1−ρ). If R≤t₀ the result is immediate; otherwise semiboundedness at t₀ gives R≤t₀+√ν(1+t₀)=(ν+2√ν+ρ)/(1−ρ). No boundary derivative is taken and no exact center is required for this pointwise result.
3. **Difference-body and Loewner directions are checked.** The objective-decreasing sign of each closed Dikin vector lies in L(g), so E_F⊆K_g. The opposite containment is K_g⊆2C_F E_F. Thus E_F⊆2C_G E_G gives H_G≼4C_G²H_F; interchange gives the reverse inequality with C_F. The condition-number factor is 16C_F²C_G².
4. **All-barrier upper bound closes the original rate gap.** A fixed ball z+rB⊆P yields (2rg/Δ)B⊆K_g by homothety about an optimum. Therefore λ_max≤(CΔ/(rg))². Combined with λ_min≥ℓ⁻², this gives the matching upper condition rate for every barrier, not only the canonical barrier.
5. **The classical gap–μ lower bound is proved without an implicit-barrier citation dependency.** Dikin objective support gives ||c_V||*≤g. Differentiate centrality to get g′=||c_V||*²/μ²≤g²/μ², integrate (1/g)′≥−1/μ² to μ=∞, and obtain μa_F/(μ+a_F)≤g≤νμ. This is Peña (2002), Proposition 3.2, expressed with a_F equal to the analytic-center gap. It implies g=Θ(μ) for every fixed barrier on compact P, without strict complementarity.
6. **Uniform exact-gap range is explicit.** At the analytic center, asymmetric containment and Dikin support give Δ−a_F≤C_ν a_F. Thus a_F≥Δ/(1+C_ν), so fixed-P barriers with ν≤ν̄ share every gap below Δ/(1+C_ν̄). Varying barriers require bounded parameters; approximate points additionally require residual bounded away from one.
7. **Widths and eigenvalue ordering are checked.** Eigenvalues increase with j; the two Courant–Fischer formulas give the stated reciprocal minimax inequalities. Difference-body radial width is not its support function. Their minima agree because both equal the centered inradius; the minimum support function of K_g is the minimum full width of L(g). At j=1 both radial profiles equal D(g), and both directed profiles equal ℓ(x). At j=d both radial profiles equal r_g. The original manuscript stated only one inequality for the first directed width; equality follows from the already-proved reverse inequality.
8. **Canonical constants are retained without an unnecessary bounded-slack hypothesis.** If desired, a strict primal point z and its smallest positive coordinate/eigenvalue σ bound all central dual slacks on μ≤μ̄ by [g(z)+ν_can μ̄]/σ. This follows from weak duality and canonical complementarity; dual nondegeneracy and strict complementarity are unnecessary. The optional resulting bound can improve the general geometric constant.
9. **Localization is pointwise.** If P is unbounded but has a compact positive objective sublevel, a relative interior ball exists inside that sublevel by interpolation from an optimum to a strict point. Replace Δ by the selected level and apply the same proofs. No global unbounded-path existence or analytic-center statement is claimed.

## Relation to repository material

The new setup and minimum-rigidity/chord results rebuild original Sections 2–3. The all-barrier diameter theorem strengthens the old canonical-achievability statement and its one-way barrier comparison. The direct residual theorem replaces the old ρ≤1/6 center-distance transfer with observed-gap estimates for all ρ<1; later solver sections can use it directly. Both original directed widths and the stronger center-independent radial profiles are included. The original conditioning dictionary, exact examples, degeneracy limits, clustered spectra, and right-hand-side developments remain assigned to Stages 3–4, so no obsolete open problem is carried into this stage.

## Literature actually inspected during authoring

- Local Renegar (2001), `literature/papers/renegar2001-a-mathematical-view-of-interior/fulltext.md`, Theorems 2.3.3–2.3.4 and the central-path discussion on extracted pp.44–45. The older asymmetric constant there is 4ν+1. We reproduce the semiboundedness argument and credit it as standard.
- Xiong–Freund, July 15, 2024 primary PDF, https://optimization-online.org/wp-content/uploads/2024/06/arXiv_0715.pdf, Section 5.1, Fact 5.2, Remark 5.1, and the rescaling discussion. Their ellipsoid bounds for primal–dual diameter and conic radius are a direct antecedent, prominently acknowledged at the start of the geometric section.
- Peña (2002), author-uploaded full-text HTML, https://www.researchgate.net/publication/220588878_Two_properties_of_condition_numbers_for_convex_programs_via_implicitly_defined_barrier_functions, Section 3.1 and Proposition 3.2 (including proof), and Proposition 3.7/Corollary 3.8. The identical gap conversion is expressly attributed. The matrix in the latter results is AH⁻¹Aᵀ, not the tangent primal Hessian. No novelty is claimed for gap parameterization or generic inverse-square upper bounds.
- The Nesterov (2018), Theorem 5.3.8 locator is expressly identified as the citation used by Xiong–Freund; the sharper constant is proved here, so an uninspected book theorem is not a proof dependency.
- The Stage 1 source-access limits for Peña (2001) and Renegar (1996) remain in force. Renegar (1996) is cited only for its verified classical matrix-conditioning scope, without an unchecked theorem claim.

The text says precisely which further comparisons it develops but makes no exclusive priority assertion or claim of exhaustive exclusion of prior art. The final introduction should retain the Stage 1 caveats when formulating any qualified novelty sentence.

## Verification and outstanding work

`make -C conditioning-paper` succeeds and produces a 10-page stage draft, including references. The final compiler log has no undefined references/citations, overfull/underfull boxes, or warnings. A separate author sanity check in the existing qipm environment checked 180 exact/approximate points for two weighted log barriers on the same rectangle: the two-sided gap–μ bounds and both difference-body inclusions all passed. This check is not presented as numerical evidence in the paper and introduces no dependency or retained research claim.

No unresolved mathematical question remains within the authored stage scope to the author's knowledge. The five independent reviews identified three minor improvements, now corrected. Later-stage examples, solver results, final positioning, and numerical evidence are intentionally not represented as completed here.

## Notation and width bounds after review

Use x_F(μ) for the barrier-parameter path and μ_F(g) for the inverse gap
map. The distinct gap functions are x̂_F(g), Ĥ_F(g), and κ̂_F(g), explicitly
defined in equation `eq:gap-path-notation`. Pointwise H_F(x) and κ_F(x)
retain their original meanings. Future sections should follow this convention.

The final minimax intervals are (w_j^+)⁻² ≤ λ_j ≤ 4C²(w_j^-)⁻² and
(v_j^+)⁻² ≤ λ_j ≤ C²(v_j^-)⁻². The lower pointwise Rayleigh estimate
is applied in inf_dimS=j sup_h∈S; the upper estimate is applied in
sup_codimU=j−1 inf_h∈U. This tightens the originally submitted intervals
without changing definitions, ordering, endpoint values, or hypotheses.
