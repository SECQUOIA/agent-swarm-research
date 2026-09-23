# Stage 4 correction record

Correction agent: `stage1_fixer`, distinct from the Stage 4 author.
The coordinator accepted three distinct minor findings after the five
independent reviews. No major finding required another review round.

## Corrections

1. **R1/R3/R5: approximate centers.** The paragraph after
   `thm:lp-all-spectra` now extends precisely the ordered eigenvalue scales
   and the general O(g) projector estimate to bounded-residual points at
   their observed gaps. It does not extend the canonical O(g²) estimate.
2. **R5: restricted solve.** Before `eq:conditional-window-residual`, the
   text explicitly requires both membership of the computed solution in
   `range(I-Pi)` and the strong-right-hand-side residual bound. Since this
   is an invariant spectral subspace, the residual component in it is
   orthogonal to `Pi r`, which justifies the full squared residual bound.
3. **Coordinator: prior nonconvergent paths.** The final paragraph of
   `08-lp-spectra.tex` now credits Bolte–Pauwels and distinguishes their
   Legendre-function construction from the present finite-parameter
   self-concordant barrier. The contribution is stated as the proved
   global certificate and sharp spectral/solution-error calculations;
   no first-nonconvergence claim is made. Added `boltepauwels2022`.

## Sources checked

Read the [primary institutional manuscript](https://www.tse-fr.eu/sites/default/files/TSE/documents/doc/wp/2020/wp_tse_1080.pdf),
Section 5.8, equation (42) and Corollary 11, printed page 43. Its path
minimizes a linear objective plus r times a Legendre function as r tends
to zero. The function is finite and continuous on the closed square;
the path has two distinct accumulation points. Also checked the
Legendre definition in Section 3.3, printed page 19: its boundary
requirement concerns gradient divergence, which differs from function
divergence in our definition `def:barrier`. These locators refer to the inspected
manuscript, not uninspected journal pagination.

Verified journal metadata at the [publisher's article page](https://link.springer.com/article/10.1007/s10107-021-01707-1):
Jérôme Bolte and Edouard Pauwels, *Curiosities and counterexamples in
smooth convex optimization*, Mathematical Programming 195, 553–603
(2022), DOI 10.1007/s10107-021-01707-1. The online publication date is
2021; the bibliography uses the journal issue year 2022.

## Validation

The corrected manuscript was rebuilt with `make -C conditioning-paper`.
The resulting 29-page PDF builds cleanly: the final log has no unresolved
references/citations or layout warnings. No original-paper,
literature-corpus, or `central-path-cost/`
files were changed.
