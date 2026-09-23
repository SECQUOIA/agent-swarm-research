# Stage 1 author handoff

Author: `/root/paper_stage1_author`. Date: 2026-09-07.
Status: authored and locally checked; **not accepted**. Files are ready to freeze for five independent reviews. No later stage was authored and no subagent was delegated writing or proof work.

## Changed source files

- `sections/01-model-transfer.tex`: complete model, scalar/physical admissibility, stationary-variance derivation, Schur identity, logarithmic remainder, measurable information policies, optimized-moment transfer, and the observation-uniform cosine lower bound.
- `main.tex`: includes the new section and bibliography.
- `preamble.tex`: adds `mathrsfs` for the transverse generator.
- `references.bib`: verified Fukushima–Oshima–Takeda second-edition citation.
- `notation.md`: records the scalar versus physical policy classes and the distinct L² and energy-completion meanings of the source representative.

The current PDF is eight pages including the preparation-status paragraph and bibliography. The final assembly may move technical form arguments to an appendix, but the section is presently self-contained.

## Exact mathematical scope

**M1.** The forward bulk–surface equations conserve exchange flux and give equilibrium weights `dy/Z` and `K ds/Z`, with zero axial wall drift and mean speed `V=∫u/Z`. Only transverse motion is reversible. The pattern is quenched. Initial particle distribution is stationary. Axial molecular diffusion is an independent-driver contribution, with the isotropic surface term `KM/Z` identified separately.

**M2.** Every nonnegative L¹ mobility has an extended scalar smooth-test response. Actual transverse dynamics are assigned only to coefficients whose derivative preform is closable in wall L², using its minimal closure. Positive floors guarantee closability even without an upper bound. The coupled form is closed, regular, and Markovian on the disjoint union of the closed bulk and the adsorbed wall; the standard regular-form correspondence supplies the stationary process. Its finite-time covariance and spectral measure derive the physical long-time variance coefficient. The smooth variational representation then follows, so it is not used as a definition chosen to force the result.

Every physical coefficient has `Dflow≥χJ`, including infinite response. Positive-background coefficients have the usual L² inverse and Schur identity. The identity is also proved for *every physical finite-J coefficient*, using completion in the scalar reaction-plus-derivative energy norm. There is no presumption of an L² corrector in the latter case: the map `h↦sqrt(k)h` extends continuously to that completion, which makes `w=kh` meaningful as an L² image. Surface forcing from a bulk trace is energy-bounded, the surface square completes there, and its nonnegative residual controls the bulk supremum. This also shows that finite J gives finite Dflow for such coefficients, at fixed bulk data.

**M3.** With a positive floor `m`, bounded nonnegative rate, and uniform positive rate integral, the remainder is at most `C[1+log_+(1/m)]`. The proof gives the anchored Poincaré estimate, inverse existence, contraction/positivity argument, mass identity, the crude `||kh||∞≤C/m` bound, an explicit Fourier split for the H^(-1/2) norm, trace duality, and the final quadratic bulk supremum. Constants do not depend on any upper bound or derivative of D. The one-dimensional connected wall and fixed positive bulk diffusivity are explicit assumptions.

**M4.** Scalar policies are Borel maps into nonnegative L¹ fields with the exact budget for every observation. Physical policies lie in the closable subclass. Countable smooth cores make both response functions jointly Borel, so no selection theorem or unproved expectation–infimum interchange is used. An arbitrary scalar policy is mixed with a uniform positive field using a fraction θ of the same budget. This preserves all information and gives `J(Dθ)≤J(D)/(1−θ)`. The logarithmic remainder then proves finite-budget inequalities separately for q≥1 and 0<q<1. Choosing θ=M proves the asymptotic comparison under the stated logarithmic growth criterion, without regular variation or optimizer existence. A direct root bump proves `Fq≥cq M^(−q/5)` for the canonical cosine ensemble and every observation law; hence the quantitative comparison is uniform over observations, including laws depending on M.

All small-budget powers and logarithms are in fixed dimensionless units. The manuscript records `[M_phys]=L³/T`, `[J_phys]=LT`, and `J_phys=(ell_ref/k_ref)J'`. Thus applying dimensionless scalar constants to physical dispersion requires `χ_phys ell_ref/k_ref`, not merely `χ_phys`.

## Gaps in previous records resolved here

1. The phrase “natural closed form” for an arbitrary nonnegative L¹ weight did not establish closability and is insufficient in general. The manuscript separates the always-defined scalar relaxation from actual closable diffusion coefficients and proves that same-budget positive-floor mixtures recover scalar values asymptotically.
2. A finite energy response need not have an L² corrector. The finite-J Schur identity now uses a specified energy completion when needed.
3. The stationary coefficient previously appeared mainly through a variational formula. Here it follows from the physical Markov model and finite-time stationary variance. Degenerate coefficients are allowed an infinite coefficient; a spectral gap and stationary ergodicity are asserted only with a positive floor.
4. Joint response/policy measurability is proved using countable smooth cores. No formula `E inf = inf E` is assumed for exact observation.
5. Scalar and physical admissible classes are explicitly different. The lower bound uses class inclusion, and the upper bound uses the floor mixture to connect them.
6. The dimensional multiplier needed to transfer canonical scalar constants is made explicit.

## Citation verification

The one external theorem family needed at this stage is the standard Dirichlet-form construction. The manuscript cites Fukushima, Oshima, and Takeda, *Dirichlet Forms and Symmetric Markov Processes*, second revised and extended edition, De Gruyter Studies in Mathematics 19, DOI `10.1515/9783110218091`, conventionally dated 2011. The publisher lists a December 2010 release; the publisher's book preview has copyright 2011, so the standard 2011 bibliography is retained.

- [Publisher book page](https://www.degruyterbrill.com/document/doi/10.1515/9783110218091/html).
- [Publisher preview](https://api.pageplace.de/preview/DT0400.9783110218091_A15362972/preview-9783110218091_A15362972.pdf).
- [Li and Ying, primary open discussion of Hamza's criterion](https://arxiv.org/pdf/1701.02411), Section 3.4, identifies the relevant FOT Theorem 3.1.6.
- [Primary open Dirichlet-form application](https://arxiv.org/pdf/1308.0234), page 2, explicitly identifies FOT Theorems 4.2.3 and 7.2.1 as the associated Hunt-process construction. The manuscript cites Theorem 7.2.1 directly.

No novelty claim is made for the model, spectral identity, Schur algebra, form comparison, Fourier estimate, or policy-mixture method.

## Verification completed by the author

- Re-derived the adsorption boundary sign by conservation and the backward boundary condition by integration by parts.
- Checked the equilibrium normalization, forcing mean, constant-shift gauge, factors K and Z, and signs of all Schur terms independently against the defining energy.
- Checked the finite-response energy-space proof separately from the positive-floor inverse proof; no infinite energies are subtracted.
- Checked the Fourier convention, Parseval factor P, missing zero mode, harmonic low-mode sum, and high-mode bound.
- Checked q<1 using subadditivity, not Minkowski or convexity, and checked that the O(M) mixture error is smaller than both stated quantitative errors.
- Checked the cosine bump estimate against every budget-M design, including spikes and degenerate/nonclosable scalar competitors; the event `|c|≤1/2` has probability 1/4.
- Ran `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` from `paper-uncertain-mobility/`: successful PDF build and bibliography resolution.
- Checked `main.log` for warnings, overfull boxes, and underfull boxes: none.
- Ran `git diff --check`: no whitespace errors.
- Rendered and visually inspected PDF page 5, containing the detailed Schur proof and the remainder theorem: readable equations, margins, and page flow.

No numerical scientific result is introduced in this stage; numerical simulations would not settle the functional-analytic points that require independent review.

## Review priorities

Reviewers should scrutinize the weighted-form/physical-class distinction, the general finite-J energy completion, the coupled regular-form construction, the stationary spectral limit including zero modes, joint measurability of full physical responses, and the exact same-budget comparison. The author has no known unresolved mathematical gap in M1–M4. This is an author assessment, not an acceptance decision.
