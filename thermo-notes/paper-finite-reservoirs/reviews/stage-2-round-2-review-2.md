# Stage 2, round 2: independent review 2

Verdict: **no major or minor issues identified in the revised stage**. The two source-convention concerns from my previous review are resolved. The short-range sufficiency argument now consistently uses BCT2012 objects, and the added arguments support the necessary derivative and pressure identifications.

I reviewed the revised `sections/microscopic.tex`, its Stage 1 dependencies, and the relevant original passages in the local primary sources. I did not read other round-2 reports, edit the manuscript, or delegate work. The checks below are analytic and source-based; I did not rerun numerical calculations.

## Corrected source dependencies

**One contour convention.** The manuscript now explicitly adopts BCT2012 Definitions 4.1–4.4 and 5.4, equations (6.1)–(6.5), and the matching-label/polymer constructions (6.13)–(6.22). The description of the compatible-interface rule agrees with original Definition 4.4. Its distinction from BCHPT2022 Definition 5 is accurate. The modified BCHPT phase events are no longer treated as identical to the BCT events or used as an implicit replacement in the proof.

**General interior sums.** The new equation for a matching-label summand agrees with BCT2012 (6.13)–(6.14): the vertex counts partition the interior, contour size enters through `−kappa M`, and the color-component factor is independent of temperature. Removing the ordered multiplicity contributes only a constant factor. The argument no longer relies on the restricted applicability of BCHPT2022 Section 3.8.

The bound on total internal size is valid for the stated geometry. A unit bond can have only a bounded number of intersections with the half-unit-cube boundaries and mutually compatible contours. A bond meeting the interior either touches an interior vertex or crosses its bounding contour; bounded lattice degree therefore gives `O(|Int gamma| + m_gamma)` relevant bonds. This also covers a wrapping interior. Positive-sum differentiation then gives first and second logarithmic derivatives of orders `V_gamma` and `V_gamma + V_gamma^2`. BCT Lemma 5.7 implies `V_gamma = O(m_gamma^2)`, yielding the displayed activity bounds, including the ordinary second derivative bound after adding the squared logarithmic derivative.

## Both-side pressure and phase identification

I checked the new stable-pressure argument against BCT2012 Appendix A and the original interface-network calculation, rather than assuming that a main-text ordered-side statement automatically extends.

1. BCT equation (1.5) places coexistence at `(log q)/d + O(q^(-1/d))`. Appendix A condition (A.1) therefore holds on a fixed neighborhood on both sides for sufficiently large fixed `q`. The appendix explicitly extends Lemma 6.3(i),(ii) beyond the ordered side.

2. BCT Lemma A.3 states `a_o=0` implies positive spontaneous magnetization, while `a_o>0` implies zero magnetization. Since `a_o` is nonnegative, these statements give the asserted equivalence. Below coexistence magnetization is zero, so `a_o>0` and `a_d=0`; above coexistence it is positive, so `a_o=0`. Continuity gives equality of the two truncated free energies at coexistence. This does not require proving a strict disordered metastability gap above coexistence.

3. On the full torus, Lemma A.1(ii) bounds each restricted partition function above by `exp[-N f_min + N epsilon_L]`: its remaining maximizing factors are at most one and the exterior boundary is absent. Equation (A.9) supplies the lower bound for a minimizing phase. Both inputs are valid throughout the fixed neighborhood.

4. The interface-network bound really does extend to this neighborhood. BCT (6.26) uses the upper bound with the minimum free energy, not the assertion that the ordered phase minimizes. The interface sum in (6.27) requires sufficiently large `kappa`, contour counting, and `q <= exp(2d kappa+d)`. At coexistence, `2d kappa+d-log q = d+o(1)` as `q` increases; shrinking the fixed neighborhood preserves this inequality on both sides. Since each network has at least two interfaces and each interface has size at least `L^(d-1)`, the geometric series gives `exp[-N f_min - b L^(d-1)]` after absorbing `N epsilon_L`. Thus the added both-side assertion is supported without transferring a different contour convention.

5. The positive decomposition now identifies the physical limiting random-cluster free energy as `f_min`. The exact normalization `Z_RC = exp(-d beta N) Z_spin` gives `f_i^tr = psi_i + d beta` on the appropriate stable side. Only equality of stable thermodynamic branches is used; no identity of metastable extensions is assumed.

## Rechecked theorem chain

- The original minimum cap has the stated exponent `beta/8-beta/20+1`; it is smooth on the fixed interval. BCT (A.5)–(A.6), with sufficiently large fixed `q`, leave a positive exponential size margin in the absolute cluster sum. The added polynomial derivative factors are absorbed by this margin.

- First differentiation of the absolutely continuous minimum activities can be justified by integrating their almost-everywhere derivatives against the cluster majorant. The resulting uniform Lipschitz bound passes to the limiting truncated free energies. Since the metastability gaps vanish at coexistence, all BCT torus contours satisfy the inactivity condition throughout a fixed `eta/L` window.

- On that window the original activities are smooth, so second differentiation does not touch a nonsmooth cutoff. The absolute second-derivative bound for the log restricted partition function is `O(N)`.

- The stable-side displacement `eta/(2 sqrt N)` is contained in that window for every fixed `d>=2`. The stable pressure estimate and finite difference give the required center error `O(sqrt N)`. The pressure error divided by the displacement is still exponentially small compared with this scale.

- The fugacity paragraph now explicitly differentiates the logarithm of the restricted partition function. Changing from `beta` to `lambda=log(exp(beta)-1)` converts these derivatives to the conditional bond mean and variance with the correct factors of `p`. The moment window and center accuracy are sufficient for the uniform standardized bond exponential moment.

- The centered binomial noise bound is applied before conditioning on the positive bond phase event. Dividing its nonnegative expectation by a phase probability bounded away from zero is valid even though conditioning changes the binomial law. The subsequent Cauchy–Schwarz step transfers the moment to the actual spin energy; it does not equate bond count with monochromatic-bond count.

- The tunneling probability has exponent `-b L^(d-1)`. For `c_N >> N^(3/2)` the maximal logarithmic reservoir gain is `o(sqrt N)`, which is dominated in every fixed `d>=2`. The positive-mixture sufficiency theorem applies on the Edwards–Sokal space, and projecting its exact energy-only reweighting yields the physical spin law.

- The necessity proof still uses only the BKMS1991 real-temperature expansion, positive midpoint events, and the conditional-spin variance bound passed through the stable pressure. The one-sided Laplace argument, untilting, and recovery of total mass justify weak conditional Gaussian limits without an unsupported local-density assumption. Both limiting variances are strictly positive.

## Other stage material

I rechecked the mean-field phase calculation, its global positive-phase moment bound, the pure-spin `a=0` extension, kinetic smoothing for `a>0`, and the finite occupation/Gamma/Beta formulas. Their hypotheses and normalizations remain consistent with Stage 1. No additional correction is needed. The revised stage contains enough explanation to distinguish its new contour differentiation and observable-transfer arguments from the cited equilibrium phase inputs.

This verdict concerns the scientific and mathematical content of the assigned stage. It is not a claim of established literature priority or a review of later manuscript sections.
