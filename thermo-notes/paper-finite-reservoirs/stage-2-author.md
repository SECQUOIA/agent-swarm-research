# Stage 2 author record

Stage scope: microscopic realizations and exact finite-system formulas. `sections/microscopic.tex` is included from `main.tex`; `refs.bib` supplies the primary references used by this stage. No Stage 1 mathematical statement was changed.

## Principal developments beyond transcription

### 1. The pure-spin mean-field model already has the sharp threshold

The legacy notes required fixed positive kinetic shape in their microscopic theorem, because the disordered spin energy has only order-one fluctuations. This restriction is unnecessary for the stronger Stage 1 two-scale theorem: a nondegenerate weak fluctuation limit in only one phase suffices. The ordered mean-field spin phase has strictly positive square-root-N variance.

The new paper proves the mean-field reservoir theorem for every fixed `a>=0`, including no momenta. A complete scalar stationary-point classification and explicit Hessians prove the four minima. Multinomial Laplace sums give the weights and conditional fluctuations. A global occupation probability bound, including the simplex boundary, gives uniform square-root-N exponential moments on positive Voronoi phase cells. Combining the three ordered cells gives an exact positive two-component decomposition with zero exceptional mass. The already proved abstract necessity and sufficiency then yield the sharp `c_N >> N^(3/2)` iff theorem.

For `a>0`, the stage also proves the local continuous energy limits and a global Gaussian-type bound on the coexistence interval. These stronger facts are retained for the later boundary-scale results. The kinetic variables are useful for smoothing and exact Gamma/Beta formulas; they are not essential for the bath exponent.

### 2. The isolated short-range sufficiency gap is closed in the draft

The new proof establishes uniform physical-spin-energy exponential moments under the actual positive contour phase events, for every fixed `d>=2` and sufficiently large fixed `q`. It does not assume that a signed partition remainder is a probability remainder, equate bond count to spin energy, or promote the minimum-truncated free energies to C2 functions.

The chain is:

1. Use the positive contour phase partition of Borgs–Chayes–Tetali (BCT), including its exponentially small tunneling mass.
2. The exact contour activities are ratios of positive interior random-cluster sums. Their logarithmic first derivatives are bounded by `C m^2`, and their ordinary second derivatives by `C m^4 K`, where `m` is contour size. The geometric input is `|Int gamma| <= m diam(gamma)/2 <= m^2/4`, valid in all the fixed dimensions under consideration.
3. BCT's truncated activities are minima of the exact activities and a smooth exponential cap. They are absolutely continuous, with almost-everywhere derivative bounded by `C m^2 K'`. The cluster expansion has an exponential size margin: its absolute terms, multiplied by `exp(rho total_size)`, have total at most `C N`. This absorbs every required polynomial derivative factor.
4. The truncated finite-volume free energies are therefore uniformly Lipschitz. Their limits are Lipschitz, so the metastability gap `a_i(beta)` is `O(|beta-beta_c|)`.
5. BCT Lemma A.1(i) removes a contour's cutoff whenever `a_i diam(gamma) <= c beta`. Every torus contour has diameter at most `L`. Hence *all* finite-torus cutoffs are inactive throughout `|beta-beta_c| <= eta/L` for fixed small `eta`.
6. Differentiate the original smooth positive activities on this interval. The same exponential cluster majorant gives `|d² log Z_phase / d beta²| <= C N`. This bypasses any second derivative of the minimum cutoff.
7. BCT's finite-volume pressure estimate and its stable-branch identity identify the first derivative at coexistence to `-N u_i + O(sqrt N)`, using a stable-side finite difference of size `eta/(2 sqrt N)`. This displacement is inside the cutoff-free interval because `d>=2`. The weaker displacement `eta/L` would not give a sufficiently accurate center for `d>2`, so it is not used.
8. Changing to the exact bond fugacity `lambda=log(exp(beta)-1)` yields bounded conditional exponential moments of `(B+pNu_i)/sqrt N` in each bond phase.
9. Under Edwards–Sokal, conditional on the spins, `B` is Binomial(`M,p`), where `M=-U` is the monochromatic bond count. Its noise `D=B-pM` has a uniform square-root-N exponential moment. Conditioning this nonnegative moment on a phase costs only the inverse phase probability; both phase probabilities stay positive. Cauchy–Schwarz transfers the bond moment to the actual spin energy via `U-Nu_i=-(B+pNu_i-D)/p`.
10. The positive-mixture sufficient theorem now applies. Tunneling mass is `O(exp(-b L^(d-1)))`, whereas reservoir amplification is `exp(o(sqrt N))`; `d-1>=d/2` closes the estimate for every fixed `d>=2`.

The separate necessity proof was rechecked from the original real-temperature partition expansion. One-sided Laplace transforms and known phase masses give actual midpoint-conditioned weak energy CLTs. A uniform conditional-spin variance bound passes through strong convexity to each stable thermodynamic pressure branch, proving nonzero phase variances without momenta. This completes the short-range iff theorem, subject to the user-prescribed independent review of the new closure argument.

## Exact finite-system verification

The paper derives the occupation probabilities, the `A+c` power after integrating kinetic and reservoir energies, the conditional Beta(`A,c+1`) law, and the shifted Gamma/Beta CDF sums. Strict concavity of the exact energy likelihood reduces continuous total variation to the probability difference on one interval. Shape-zero Gamma/Beta laws are not used: `a=0` is handled by a deterministic kinetic energy.

Ran the existing independent checker `python research/verification/check_potts_finite_bath.py`. Explicit enumeration of all labelled spins for N=1 through 8 agrees with occupation aggregation to machine precision. At N=12, independent density quadrature agrees with the CDF formulas within about `9.2e-12` in one case and `1.2e-14` in the other. These checks verify the exact formulas, not the asymptotic contour theorem.

## Primary source audit

Local PDFs and extracted text are retained in `sources/`.

- `bkms1991.pdf` and `.txt`: Borgs, Kotecký, Miracle-Solé, *Finite-Size Scaling for Potts Models*, Journal of Statistical Physics 62 (1991), 529–551, DOI `10.1007/BF01017971`. Original author manuscript: <https://www.microsoft.com/en-us/research/wp-content/uploads/2016/11/Finite-Size-Scaling-for-Potts-Models.pdf>. Printed p.6 equation (6) fixes the monochromatic-bond Hamiltonian. Printed pp.10–11 Theorem 1 gives six derivatives, stable branches, latent heat, and the real-temperature periodic partition expansion. The source's `f_i` is dimensional free energy; the paper uses `psi_i=beta f_i`.
- `bct2012.pdf` and `.txt`: Borgs, Chayes, Tetali, *Tight Bounds for Mixing of the Swendsen–Wang Algorithm at the Potts Transition Point*, Probability Theory and Related Fields 152 (2012), 509–557. Open primary preprint <https://arxiv.org/abs/1011.3058>. Publication metadata were checked against coauthor Tetali's publication list <https://tetali.math.gatech.edu/pubs_2012.html>. Printed pp.21–22 define diameter and prove Lemma 5.7. Sections 6.1–6.2 give the positive phase split and activity formulas. Printed p.39 explicitly extends Appendix A assumptions to both sides of the transition. Printed p.40 equations (A.3)–(A.8) give the minimum truncation, exponential cluster bounds, and absolute finite-volume pressure error. Printed p.41 Lemma A.1(i) gives exact equality of truncated and original activities under the diameter criterion. The manuscript uses these precise inputs, not an assumed analytic extension.
- `bchpt2022.pdf` and `.txt`: Borgs, Chayes, Helmuth, Perkins, Tetali, *Efficient Sampling and Counting Algorithms for the Potts Model on Z^d at All Temperatures*, <https://arxiv.org/abs/1909.09298v3>, version dated 8 August 2022. Section 2 Lemma 2.1 and equations (19)–(20) explicitly give the anchored exponential absolute-cluster bound and its global tail. Sections 3.3–3.4 equations (44)–(46) identify genuine positive phase events and the ordered multiplicity. Section 3.7 supplies the bounded-degree contour embedding; Section 3.8 identifies positive interior random-cluster partition sums. Lemma 4.1 supplies tunneling suppression, and Appendix B.1 gives the disordered-side versions of the contour estimates. The paper derives its own exact random-cluster/spin normalization from the Hamiltonian, rather than relying on an additive-energy convention in a secondary formula.
- `grw2008.pdf` and `.txt`: Gandolfo, Ruiz, Wouts, *Limit Theorems and Coexistence Probabilities for the Curie-Weiss Potts Model with an External Field*, SPA 120 (2010), **84–104**, DOI `10.1016/j.spa.2009.10.011`, <https://arxiv.org/abs/0811.2735>. Bibliographic metadata checked at the primary arXiv record; the stage independently derives the special q=3 quantities it uses.
- `cet2005.pdf` and `.txt`: Costeniuc, Ellis, Touchette, *Complete Analysis of Phase Transitions and Ensemble Equivalence for the Curie-Weiss-Potts Model*, JMP 46 (2005), 063301, DOI `10.1063/1.1904507`, <https://arxiv.org/abs/cond-mat/0410744>. Cited for established mean-field phase and ensemble analysis, not priority of the present full-law bath-size theorem.

## Scope and remaining review

The claimed microscopic results now include plain mean-field spins and plain nearest-neighbor spins in every fixed dimension at least two, with optional kinetic smoothing. The short-range theorem assumes the sufficiently large q required by the cited contour machinery; it is not stated for every first-order Potts transition or arbitrary molecular fluids. It proves no pointwise short-range energy density bound, Gaussian interphase valley, dynamics, or nucleation rate.

The first two stages compile to 19 pages with `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`. The final compilation has no unresolved citations or references and no box warnings. The new contour differentiation and observable-transfer proof requires the planned five independent reviewers before Stage 2 can be closed.
