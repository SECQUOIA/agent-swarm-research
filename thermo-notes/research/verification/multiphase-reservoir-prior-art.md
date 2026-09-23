# Prior-art audit: finite reservoirs and multiphase probability preservation

Date: 2026-09-06. Independent literature scout: `capacity_prior_art`.

The candidate's plausible contribution is a **sharp finite-size distinction between preserving two phase peaks and preserving three or more peaks after optimizing the intensive field**, stated in total variation. Gaussian finite reservoirs, their use near phase transitions, and supporting-paraboloid geometry are established. The empty-ellipsoid description is a useful application of that geometry, but should not be presented as a new general geometric principle.

No exact prior theorem giving the proposed two-versus-three-peak thresholds, the intervening phase-selection regime, or its optimal total-variation error was located in this targeted search. This is a search outcome, not proof of novelty. The current Gaussian example also needs extension beyond its specially chosen equal variances before broad physical claims are warranted.

## Candidate and the distinction that matters

The candidate starts from a probability mixture with means $Ne_i$, variances $N$, and fixed positive weights. It reweights the distribution by

\[
\exp(t_NE-\kappa_NE^2/2),\qquad \kappa_N\geq0,
\]

and optimizes $t_N$. Its proposed thresholds are \(\kappa_NN^{3/2}\to0\) for complete two-peak probability-law preservation, versus \(\kappa_NN^2\to0\) for three or more distinct scalar phase energies. In the intervening regime, local peaks retain their shapes while their weights change. These are stronger statements than convergence of free energy per particle, agreement of an equilibrium macrostate set, or closeness in a metric that vanishes merely because probability spreads over more energy levels.

For a conventional bath of size $B_N$, an entropy expansion gives \(\kappa_N=O(B_N^{-1})\). The corresponding prospective distinction is therefore $B_N\gg N^{3/2}$ versus $B_N\gg N^2$. These exponents require the stated distributional accuracy, admissible field retuning, and regular bath assumptions; they are not unconditional thermodynamic definitions of a sufficiently large reservoir.

## Thewes and Sollich: close motivation, different physical mechanism

F. C. Thewes and P. Sollich, *Ensemble inequivalence in the design of mixtures with super-Gibbs phase coexistence*, Physical Review E **112**, 024131 (2025), published 25 August 2025. [Publisher](https://journals.aps.org/pre/abstract/10.1103/z6v8-pmm9), [open manuscript](https://arxiv.org/abs/2501.07734).

Section II, equations (1)–(4), explicitly represents grandcanonical phases as composition-distribution peaks, uses Gaussian peak widths proportional to $V^{-1/2}$, and retains curvature prefactors in equal-weight conditions. Section III then distinguishes this probability mixture of pure phases from simultaneous spatial phase separation. In the canonical problem, a fixed parent composition imposes a lever rule. All compatible phase splits have equal bulk free energy, so interfaces select the actual split. Designed interfacial tensions can restore super-Gibbs coexistence. The paper gives a graph formulation and a two-component/four-phase example.

Our comparison: finite-bath reweighting of homogeneous-phase probabilities is not their canonical interfacial optimization problem. Even a theorem showing that a bath suppresses some pure-phase probabilities would not by itself establish that those phases cannot occur as spatial domains. Conversely, their recovery of four spatial phases does not refute a pure-phase probability obstruction. This distinction should appear near any claim linking the candidate to super-Gibbs coexistence.

## Gaussian reservoirs have a long history

M. S. S. Challa and J. H. Hetherington, *Gaussian ensemble as an interpolating ensemble*, Physical Review Letters **60**, 77–80 (1988), [DOI](https://doi.org/10.1103/PhysRevLett.60.77); and *Gaussian ensemble: An alternate Monte Carlo scheme*, Physical Review A **38**, 6324–6337 (1988), [DOI](https://doi.org/10.1103/PhysRevA.38.6324).

The longer paper constructs a bath with quadratic entropy, giving the Gaussian reweighting with curvature proportional to inverse bath size. It investigates finite-system and finite-bath effects at phase transitions and the suppression or recovery of double-peaked distributions. Its finite-size discussion includes fixed system-to-bath ratio. Both papers were retrieved through APS's openly reachable full-text endpoint and inspected. I did not find the candidate's optimized TV theorem, its $N^{3/2}$ threshold, or a three-phase retuning obstruction there. They already establish the ensemble and the qualitative importance of bath size near coexistence.

The history extends earlier: their related work and Costeniuc et al.'s bibliography identify J. H. Hetherington, *Solid \(^3\)He magnetism in the classical approximation*, Journal of Low Temperature Physics **66**, 145–154 (1987), as an early introduction. That paper was not directly read in this audit.

## Supporting-paraboloid geometry is established in several dimensions

M. Costeniuc, R. S. Ellis, H. Touchette, B. Turkington, *The Generalized Canonical Ensemble and Its Universal Equivalence with the Microcanonical Ensemble*, Journal of Statistical Physics **119**, 1283–1329 (2005), [DOI](https://doi.org/10.1007/s10955-005-4407-0), [open manuscript](https://arxiv.org/abs/cond-mat/0408681).

Theorem 3.4 and Corollary 3.5 characterize generalized-canonical equilibrium macrostates through supporting hyperplanes of $s-g$, including multiple conserved quantities. Proposition 5.1, manuscript page 18, states that a supporting paraboloid of $f$ is equivalent to a supporting hyperplane of $f-\gamma\|\cdot\|^2$. Theorem 5.3 treats multidimensional Gaussian ensembles. These are equilibrium-macrostate and thermodynamic-limit results; the paper fixes the function $g$, rather than deriving the proposed shrinking-curvature TV crossover.

Their companion, *Generalized canonical ensembles and ensemble equivalence*, Physical Review E **73**, 026105 (2006), [DOI](https://doi.org/10.1103/PhysRevE.73.026105), [open manuscript](https://arxiv.org/abs/cond-mat/0505218), gives a more physical presentation and explicitly connects the Gaussian ensemble to a finite reservoir.

Our inference from this prior geometry: for phase density points $x_i$ and positive definite bath metric $K$, the leading scores

\[
b\cdot x_i-\tfrac12x_i^TKx_i
=-\tfrac12\|x_i-K^{-1}b\|_K^2
+\tfrac12 b^TK^{-1}b
\]

are maximized at the nearest phase points in that metric. Thus a common winning set lies on an empty ellipsoid. Preserving equal leading scores at *all* points asks that $x_i^TKx_i$ be affine on the point set, equivalently that all points lie on one metric sphere. This algebra is a finite-point application of established supporting-paraboloid theory. A thermodynamic interpretation may be useful, but the algebra alone has modest novelty potential.

The Delaunay part is also classical computational geometry: H. Edelsbrunner and R. Seidel, *Voronoi diagrams and arrangements*, Discrete & Computational Geometry **1**, 25–44 (1986), [author-hosted paper](https://pub.ista.ac.at/~edels/Papers/1986-11-VoronoiArrangements.pdf). Section 3 relates Delaunay faces to convex hulls of paraboloid lifts and also treats power diagrams. Replacing Euclidean distance by a positive definite metric is a linear coordinate change. Degenerate cospherical sets require Delaunay subdivisions/contact sets rather than an arbitrarily chosen triangulation.

## Finite-bath probability comparisons already exist, but the metric differs

W. Griffin, M. Matty, R. H. Swendsen, *Finite thermal reservoirs and the canonical distribution*, Physica A **484**, 1–10 (2017), [DOI](https://doi.org/10.1016/j.physa.2017.04.143), [open manuscript](https://arxiv.org/abs/1608.05455).

Equation (23) uses the unweighted energy-level Euclidean distance

\[
\delta=\bigg[\sum_E(P_{\rm bath}(E)-P_{\rm can}(E))^2\bigg]^{1/2}.
\]

Section VI studies a twelve-state Potts model at a first-order transition. The comparison temperature is optimized. Figure 3 shows that a small bath removes the canonical double peak and larger baths restore it. Table VIII tests inverse-bath-size scaling; the authors explicitly report that the system-size scaling found away from transitions does not hold there. Away from transitions their equation (26) gives \(\delta=\widetilde\delta(N_S/N_E)N_S^{3/4}/N_E\). No sharp two-versus-three-phase theorem is supplied.

Our caution: small \(\delta\) does not imply small TV when the number of occupied energy levels grows. For example, two lattice distributions approximating distinct normal densities on a width-\(\sqrt N\) window can have \(\ell^2\) distance $O(N^{-1/4})$ and a nonzero limiting TV distance. Therefore the candidate's stronger metric can distinguish asymptotic laws that this earlier metric identifies as close. This observation is elementary and should not be mistaken for a new criticism of thermodynamics as a whole.

## Gaussian particle reservoirs and probability-family closures

B. Sadigh, P. Erhart, A. Stukowski, A. Caro, E. Martinez, L. Zepeda-Ruiz, *Scalable parallel Monte Carlo algorithm for atomistic simulations of precipitation in alloys*, Physical Review B **85**, 184203 (2012), [open paper](https://materialsmodeling.org/assets/publications/SadErhStu12.pdf), [DOI](https://doi.org/10.1103/PhysRevB.85.184203).

The variance-constrained semigrandcanonical ensemble already introduces a composition weight of the form \(\exp[-\beta N c(\phi+\kappa Nc)]\). Section II.C connects it explicitly to finite reservoirs and multiphase sampling. Thus extension from energy to particle-number or composition reservoirs is not itself novel. The paper's purpose is efficient simulation and stabilization of constrained mean compositions, not preservation of a preassigned collection of pure-phase weights.

I. Csiszár and F. Matúš, *Closures of exponential families*, Annals of Probability **33**, 582–600 (2005), [DOI](https://doi.org/10.1214/009117904000000766), [open manuscript](https://arxiv.org/abs/math/0503653), characterizes variation-distance closures through faces of convex supports. This supplies broad mathematical prior for face-supported limiting phase probabilities. Applying it to the lifted statistics \((x_i,x_i^TKx_i)\) is natural; the prescribed diverging quadratic parameter still needs its own asymptotic argument. The general phenomenon of exponential weights concentrating on exposed faces should be treated as standard.

## Recommended claim boundary and next checks

- Keep the candidate as a finite-size probability theorem, initially under explicit Gaussian-mixture hypotheses. Do not advertise a new Gaussian ensemble, a new Delaunay construction, or a replacement for the Gibbs phase rule.
- The strongest unresolved novelty candidate is the optimized TV threshold separation and its quantitative intermediate-regime error. An extension to regular unequal-covariance peaks, with controlled bath Taylor remainders, would be more persuasive than the equal-variance example alone.
- Distinguish matching all original positive phase weights from arranging merely that several phases have nonzero limiting weights. Fixed positive weights can change without disappearing when \(\kappa_NN^2\) tends to a finite constant.
- State the permitted controls: tuning one energy-conjugate field, multiple chemical fields, temperature, or interaction parameters gives different interpolation spaces. Super-Gibbs systems were designed using additional interaction parameters; allowing those parameters to retune can remove an obstruction that chemical fields alone cannot remove.
- For a conventional $C^3$ bath entropy, a typical cubic log-weight remainder over energy changes (O$N$) is $O(N^3/B_N^2)$. Its uniform control matters when translating the exactly quadratic model to an actual reservoir; tails need separate control.

Searches included exact title matches; Gaussian ensembles with finite reservoirs, phase weights, total variation, three peaks, and coexistence; super-Gibbs with reservoirs; and Delaunay, cospherical, or supporting-paraboloid phase geometry. No direct finite-reservoir/super-Gibbs/Delaunay paper was found. Several older Gaussian-ensemble predecessors and later citations remain unchecked; therefore novelty remains provisional.

## Preserved sources

PDFs and searchable text are in `research/sources/`, with stems `thewes-sollich-2025-super-gibbs`, `challa-hetherington-1988-gaussian`, `challa-hetherington-1988-interpolating`, `costeniuc-etal-2005-universal`, `costeniuc-etal-2006-generalized`, `griffin-matty-swendsen-2017-finite-reservoirs`, `sadigh-etal-2012-vcsgc`, `csiszar-matus-2005-closures`, and `edelsbrunner-seidel-1986-voronoi`. Original texts should be consulted for exact hypotheses and notation.
