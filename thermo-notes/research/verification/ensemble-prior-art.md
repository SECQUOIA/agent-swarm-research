# Closest prior-art check for finite-bath distribution thresholds

Date: 2026-09-06. Follow-up to [the ensemble scouting note](../scouting-ensembles.md).

## Decision

**The exact \(C_B\gg N^{3/2}\) total-variation threshold was not found in the three openly retrieved early papers. Novelty is still provisional, not established.** The two 1988 Gaussian-ensemble papers discuss a different asymptotic question: how mean energy density and mean inverse temperature behave at fixed system-to-bath size ratio. They do not state a probability-distance criterion for reproducing a two-phase canonical histogram, optimize temperature for that criterion, or derive the associated 3/2 threshold.

The mathematical ingredients are nevertheless old and close to the result: finite-bath quadratic weighting, the exact fluctuation relation, two-Gaussian coexistence approximations, and the different scaling of interfacial versus Gaussian valley costs. The proposed theorem should be presented as a sharp distribution-level refinement of this framework. It should not be advertised as a new finite-reservoir ensemble or a newly discovered finite-bath effect at first-order transitions.

The 1990 review remains an explicit full-text gap. Its abstract says that it reviews the two-Gaussian and finite-bath approaches. It could contain a scaling observation absent from the 1988 articles. No openly accessible copy was found in this bounded search.

## Retrieval and evidence

All successful downloads were ordinary unauthenticated HTTP GET requests to the publisher's public APS harvest endpoint. They returned HTTP 200 and `application/pdf`. No login, CAPTCHA, or access restriction was bypassed. The web rendering tool could not open these endpoints; Python's standard HTTP client could retrieve them directly.

| Paper | Retrieved primary PDF | Length | Read scope |
|---|---|---:|---|
| Challa, Landau and Binder, *Finite-size effects at temperature-driven first-order transitions*, PRB **34**, 1841 (1986) | [APS PDF](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevB.34.1841/fulltext) | 12 pages | Theory and limitations, printed pp.1841–1845; searched remaining text for bath/scaling terminology |
| Challa and Hetherington, *Gaussian Ensemble as an Interpolating Ensemble*, PRL **60**, 77 (1988) | [APS PDF](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevLett.60.77/fulltext) | 4 pages | Entire article |
| Challa and Hetherington, *Gaussian ensemble: An alternate Monte Carlo scheme*, PRA **38**, 6324 (1988) | [APS PDF](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRevA.38.6324/fulltext) | 14 pages | Theory, finite-size analysis, conclusions and appendices; inspected simulation discussion and searched full text |
| Challa, Landau and Binder, *Monte Carlo studies of finite-size effects at first-order transitions*, Phase Transitions **24–26**, 343–369 (1990) | [Publisher abstract](https://doi.org/10.1080/01411599008210236) | Full text unavailable | Abstract only |

Temporary copies and extracted text are under `/tmp/ensemble-prior-art/`. These are not durable literature packages. They can be retrieved again from the links above; the repository literature packages were not modified. Printed page numbers below refer directly to these PDFs, not to fabricated repository citation locators.

For the 1990 paper, an ordinary request to the publisher PDF URL returned HTTP 403. OpenAlex reported only a non-OA publisher location and no `best_oa_location`; Semantic Scholar reported `openAccessPdf.status=CLOSED` and an empty URL. Searches for the exact title, DOI, author combinations and PDF copies returned citations and the publisher abstract, but no accessible primary full text. These checks establish the retrieval limitation, not the article's contents.

## What the early papers actually establish

### Two-phase Gaussian reference: 1986 PRB

Printed p.1842 gives a single-phase energy-density Gaussian whose variance is proportional to \(L^{-d}\). Printed p.1843, equation (1), explicitly combines high- and low-temperature Gaussians with different phase heat capacities and temperature-dependent free-energy weights. Converting their energy-per-spin coordinate to total energy gives exactly the structural input used in the scouting result: phase-center separation of order \(N=L^d\), and within-phase widths of order \(N^{1/2}\).

Printed p.1844 directly warns that the Gaussian construction has the wrong suppression in the intermediate region. It compares

\[
 P_{\min}/P_{\max}\propto e^{-\mathrm{const}\,L^d}
\]

for the homogeneous Gaussian/Landau approximation against

\[
 P_{\min}/P_{\max}\propto e^{-\mathrm{const}\,L^{d-1}}
\]

for actual two-phase configurations controlled by an interface. This page was checked visually against the original PDF. It supports the scouting note's caveat that an exact double-Gaussian theorem cannot, by itself, justify molecular interfacial-barrier predictions.

The 1986 paper studies a canonical reference, not a finite-bath convergence threshold. Nothing in the inspected theory gives a reservoir-size exponent.

### Gaussian reservoir and fluctuation correction: 1988 PRL and PRA

PRL printed p.78 specifies a bath entropy quadratic in its energy, with coefficient \(a\) proportional to inverse bath size. Its equation (3) gives the generalized heat-capacity relation. PRA printed pp.6326–6327 gives the corresponding partition sum and explicitly writes, in their units,

\[
 \beta^2G_2=\frac{CC'}{C+C'},\qquad C'=\frac{\beta^2}{2a}.
\]

Therefore the single-phase variance ratio \(C'/(C+C')\), used in the scouting note to explain the failure of an unscaled L2 criterion, is already explicit prior art. The probability-metric interpretation is an application of that established relation.

PRA printed p.6329, section II C, derives a third-order correction to the mean energy. In their notation,

\[
 z=\frac12\frac{\widetilde C^2}{(\widetilde\beta^2+2a\widetilde C)^2}
 \left.\frac{\partial^2\beta}{\partial E^2}\right|_{E=\widetilde E},
\]

with \(\widetilde C=O(N)\) and \(\partial_E^2\beta=O(N^{-2})\). They then take \(N\to\infty\) at fixed

\[
 \lambda=N/N'\propto aN
\]

and discuss convergence of mean energy per particle and mean inverse temperature. This formula and the fixed-ratio statement were checked visually in the PDF. PRL printed p.78 states the same fixed-ratio argument in compressed form.

This is a local mean-property expansion, not a bound on the complete probability distribution. In particular, the assumption \(\widetilde C=O(N)\) is not the order of the full canonical heat capacity at two-phase coexistence. One should not turn their argument into an assertion of total-variation equivalence at fixed \(N/N'\), then claim the scouting theorem refutes it. The questions and assumptions are different.

PRL printed p.79, figure 2, directly shows a finite reservoir changing a first-order energy histogram between one and two peaks. PRA printed pp.6331–6333 studies finite-size data at fixed \(aN\) and discusses the flattening of caloric loops. The loss or recovery of bimodality with reservoir size is therefore established empirically and analytically at the qualitative level.

PRA printed p.6336, appendix A, prints an algorithmic choice \(a=(\Delta E)^2/N\), where \(\Delta E\) denotes a typical allowed energy change in one spin flip. This statement was checked visually in the original PDF; its energy units are the model units used by the paper. That quantity is **not the thermodynamic latent-energy gap**. Confusing the two would create a false apparent prior derivation of a macroscopic bath-size threshold.

## Claims to retain and claims to reject

| Proposed claim | Status after this check |
|---|---|
| Finite baths add a negative quadratic energy bias | Established by the early Gaussian-ensemble literature |
| Finite baths can suppress first-order canonical bimodality | Established; PRL 1988 figure 2 is a direct example |
| Two canonical phases have separation \(O(N)\) and widths \(O(\sqrt N)\) | Established Gaussian coexistence description |
| The Gaussian valley has the wrong interfacial scaling | Explicitly established in PRB 1986 p.1844 |
| Temperature-optimized TV convergence of the exact two-Gaussian reference iff \(C_B\gg N^{3/2}\) | Not located in these retrieved papers; narrow candidate refinement |
| Optimized-error limit \(\min\{2\Phi(a/2)-1,1/2\}\) and a phase-abandoning best fit | Not located; mathematically verified locally, but significance remains to be demonstrated |
| Fixed mean-centered bath with unequal phase weights requires \(C_B\gg N^2\) | Not located as a convergence theorem; elementary consequence of established reweighting |

No retrieved paper establishes that the exact threshold is already known. Conversely, the fact that a few papers lack it does not establish priority, especially with the 1990 review unavailable and decades of later generalized-ensemble work not exhaustively checked.

## Recommended next substantive direction

The most useful next step is **a controlled short-range coexistence theorem or benchmark that includes the interfacial valley**, not more exact Gaussian-mixture algebra. The 1986 paper makes this missing ingredient unusually clear.

A candidate theorem would combine local phase normality with an explicit bound on all intermediate canonical probabilities and a smooth, positive-heat-capacity physical bath. It should separately identify:

- the curvature error across a phase window, governed by latent-energy separation times within-phase width divided by bath heat capacity;
- the amplification of intermediate states, governed by latent-energy separation squared divided by bath heat capacity;
- the canonical interfacial free-energy cost that competes with that amplification.

For ordinary first-order coexistence in three dimensions, the scouting calculations suggest different capacities for relative barrier accuracy, complete-histogram accuracy, and absolute barrier accuracy. Establishing those distinctions in a real short-range model would go materially beyond the current exact-model note and would be more relevant to finite molecular simulations and nucleation. This remains a research proposal; the Gaussian model does not prove it.

A separate promising avenue is finite-size droplet condensation, where the energy gap and barrier can have different powers of system size from bulk first-order coexistence. Any claimed new exponents there must first be checked against the finite-size evaporation/condensation and microcanonical nucleation literature.
