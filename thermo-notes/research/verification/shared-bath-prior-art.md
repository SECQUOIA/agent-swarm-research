# Prior-art audit: canonical marginals under a shared finite bath

Date: 2026-09-07, updated after final scope review. Bounded independent primary-literature audit. The separate [mathematical review](shared-bath-review.md) verifies the total-variation and full mutual-information statements.

## Assessment

The broad effects are established: conservation laws induce correlations; canonical-looking marginals do not imply a canonical product state; and two identical systems exchanging energy can occupy opposite phases and switch their assignments. The last point has an especially close explicit precedent in Ramírez-Hernández, Larralde and Leyvraz (2008).

I did not find the proposed **constant-capacity bath scaling theorem for full microscopic total variation** in the inspected sources. The distinctive candidate is a regime where an external bath restores each macroscopic subsystem's complete canonical marginal while retaining opposite-phase correlations and an order-one error in their joint distribution. The resulting contrast between single-copy and joint bath requirements is more specific than earlier ensemble-equivalence statements. This is provisional novelty evidence, not an exhaustive priority determination.

## Candidate being assessed

Two identical, otherwise independent systems each contain \(N\) degrees of freedom and have two canonical energy peaks separated by order \(N\), with order-\(\sqrt N\) fluctuations within each phase. Their common reservoir has physical power-law density of states and constant heat capacity \(c\). The combined system has three distinct total-energy peaks.

Under the hypotheses of the repository's physical-reservoir theorems, the candidate conclusions are:

- Optimal joint canonical approximation requires \(c/N^2\to\infty\), whereas an isolated two-phase copy has the weaker optimal requirement \(c/N^{3/2}\to\infty\).
- With total energy centered on the mixed-phase sum and \(N\ll c\ll N^2\), the joint law approaches the canonical product conditioned on opposite phases.
- If the reference canonical phase weights are balanced, each full subsystem marginal approaches its canonical law in TV, but joint TV tends to \(1/2\).
- The phase-label mutual information tends to \(\log2\). Full microscopic mutual-information convergence requires additional entropy control beyond TV convergence.

For a short-range Potts example, balanced aggregate ordered/disordered weights may require a finite-size temperature sequence. A theorem at that sequence must not be restated as a theorem at a fixed coexistence inverse temperature. Nor should the result be described as a generic property of two spatial subregions of a directly interacting system: the independent-copy construction matters.

## Closest phase-selection precedent

A. Ramírez-Hernández, H. Larralde and F. Leyvraz, *Violation of the Zeroth Law of Thermodynamics in Systems with Negative Specific Heat*, Physical Review Letters **100**, 120601 (2008), DOI 10.1103/PhysRevLett.100.120601. [Open primary preprint](https://arxiv.org/abs/0802.1748).

The authors weakly couple two identical systems with negative specific heat. Their total entropy has two exchanged maxima, with different subsystem energies and magnetizations. Figure 3 explicitly shows switching between a magnetized first subsystem and unmagnetized second subsystem, and the reversed assignment. Thus opposite-phase locking and random assignment between identical copies are prior results.

They do not add the present external constant-capacity reservoir or prove microscopic TV convergence. Their conclusion explicitly distinguishes the resulting states from canonical equilibrium. The new candidate's intermediate bath is essential: it allows ordinary within-phase fluctuations while still suppressing same-phase pairs.

The full primary preprint and relevant derivation were read. Its cited predecessor, H. A. Posch and W. Thirring, *Thermodynamic instability of a confined gas*, Physical Review E **74**, 051103 (2006), DOI 10.1103/PhysRevE.74.051103, studies energy redistribution and phase separation in a confined mechanical model. [Primary article](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.74.051103).

## Ensemble-dependent correlations are classical

J. L. Lebowitz, J. K. Percus and L. Verlet, *Ensemble Dependence of Fluctuations with Application to Machine Computations*, Physical Review **153**, 250–254 (1967), DOI 10.1103/PhysRev.153.250. [Primary publisher PDF](https://harvest.aps.org/v2/journals/articles/10.1103/PhysRev.153.250/fulltext).

This derives ensemble-dependent fluctuation and correlation corrections. It is foundational prior art for the failure of fluctuation-level equivalence despite matching intensive averages. Its introduction expressly sets aside extensions at thermodynamic singularities. It therefore does not directly supply the candidate's two-scale coexistence proof.

O. Cohen, V. Rittenberg and T. Sadhu, *Shared information in classical mean-field models*, Journal of Physics A **48**, 055002 (2015), DOI 10.1088/1751-8113/48/5/055002. [Open primary preprint](https://arxiv.org/abs/1409.5520).

This analyzes bipartite information in canonical and microcanonical ensembles. The fixed-energy constraint adds correlations and changes logarithmic information scaling. Section 4.3 accounts for degenerate phases, including first-order transitions, and shows their contribution enters at order one. The bipartition is inside a system whose mean-field interactions cross the partition; it is not two independent copies sharing a separate bath. No bath-capacity threshold or full-marginal TV result was identified.

## Thermal marginals can conceal substantial correlations

M. Perarnau-Llobet et al., *Extractable Work from Correlations*, Physical Review X **5**, 041011 (2015), DOI 10.1103/PhysRevX.5.041011. [Open primary preprint](https://arxiv.org/abs/1407.7765).

This explicitly studies locally thermal quantum systems whose global correlations carry a work resource, including classical and separable correlations. Thus “locally thermal but globally nonthermal” is an established distinction. The present candidate should concern how a specified equilibrium finite reservoir produces that distinction near coexistence, with explicit microscopic error scales.

K. Ptaszyński and M. Esposito, *Ensemble dependence of information-theoretic contributions to the entropy production*, Physical Review E **107**, L052102 (2023), DOI 10.1103/PhysRevE.107.L052102. [Open primary preprint](https://arxiv.org/abs/2301.13061).

The paper shows that different reservoir ensembles can give the same reduced dynamics and thermodynamics while producing different information-theoretic decompositions of entropy production. Its primary manuscript was retrieved and inspected. It provides a close conceptual warning about inferring global correlations from reduced behavior, but it does not establish the candidate's equilibrium phase-locking window.

## Finite reservoirs at phase transitions and latent-heat buffering

L. D. Mosgaard, A. D. Jackson and T. Heimburg, *Fluctuations of systems in finite heat reservoirs with applications to phase transitions in lipid membranes* (2013). The original preprint title is *The heat capacity of lipid membranes in finite reservoirs and the relation to the frequency dependence*. [Open primary preprint](https://arxiv.org/abs/1305.4105).

Their finite-reservoir treatment uses the logarithmic entropy change of a constant-capacity bath, and studies membrane melting fluctuations. The reservoir and membrane fluctuations are correlated; a shared reservoir changes fluctuation strength. This is direct prior art for the physical bath model and finite-reservoir phase-transition effects. The inspected primary text does not show two-copy opposite-phase locking with canonical full marginals.

L. G. Moretto, K. A. Bugaev, J. B. Elliott and L. Phair, *The Hagedorn thermostat* (2005). [Open primary preprint](https://arxiv.org/abs/nucl-th/0504010).

An exponential density of states acts as a thermostat and is associated with first-order coexistence. This is prior context for the idea that phase coexistence supplies thermal buffering. The candidate's mechanism is narrower: a companion subsystem supplies a discrete compensating latent-heat change, while the ordinary external bath accommodates local fluctuations. Calling phase coexistence itself a newly discovered thermostat mechanism would be inaccurate.

## Information convergence needs its own proof

TV convergence alone does not control relative entropy or mutual information on growing microscopic spaces. It immediately gives the finite-alphabet phase-label result, but does not suffice for the full microscopic result.

The root agent supplied a separate entropy-control argument for the physical bath. Its unnormalized reweighting has exponent \(h\le0\), so \(e^h|h|\le1/e\). Pointwise phase-pair limits and domination control the joint relative entropy; bounded marginal density ratios and continuity of \(x\log x\) on a bounded interval control marginal relative entropies. The relative-entropy chain rule then yields the claimed full mutual-information limit. The separate [mathematical review](shared-bath-review.md) has now verified this argument. The mutual-information conclusion therefore rests on entropy control in addition to TV convergence.

## Final microscopic scope and wording review

The [consolidated manuscript](../reservoir-coexistence-manuscript.md) now supplies a plain short-range microscopic realization: two independent nearest-neighbor Potts models on periodic two-dimensional squares, with a fixed sufficiently large number of colors. The published phase-partition theorem and the separately reviewed conditional fluctuation argument have distinct roles. Three macroscopic support points alone give the joint \(c_N\gg N^2\) equivalence theorem. The opposite-phase selection window \(N\ll c_N\ll N^2\) additionally uses tight within-phase fluctuations on scale \(\sqrt N\).

At the fixed coexistence inverse temperature \(\beta_c\), the canonical phase weights generally are not balanced: the ordered colors contribute their degeneracy. Canonicality of both limiting marginals requires the explicitly stated common finite-size reference temperature
\[
\beta_N=\beta_c-\frac{\log q}{N\ell}+o(N^{-1}),
\]
where \(\ell=e_+-e_->0\). The bath uses that same \(\beta_N\), and the reference canonical laws are fixed by this prescription. At unbalanced weights the selected subsystem phase weights still tend to one half, so marginal canonicality is not claimed.

For a single plain short-range copy, \(c_N\gg N^{3/2}\) is currently proved necessary only. The mean-field Potts model with a kinetic sector has a matching sufficiency result using additional tail control. The two-copy theorem does not supply the missing isolated short-range sufficiency. Extensions to a fixed number of copies use familiar phase-count combinatorics; they should not be presented as results uniform in a growing number of copies.

No critical novelty wording change is needed in the final manuscript. It explicitly credits the 2008 opposite-phase example and earlier locally thermal but correlated states. The candidate contribution is the physical-bath window, the optimized strong-distance classification, and their verified microscopic realization. Historical priority and publication readiness remain provisional. This final wording review did not conduct a new open-ended search.

## Recommended positioning

Lead with a quantitative failure of using separate canonicality tests to certify joint canonicality near coexistence. State the two-copy independence assumption, bath density of states, energy-centering prescription, phase-weight balancing, and strong metric. Credit the 2008 opposite-phase example explicitly.

The best candidate is the simultaneous statement
\[
N\ll c\ll N^2,\quad
\|Q_A-P_A\|_{\rm TV}+\|Q_B-P_B\|_{\rm TV}\to0,\quad
\|Q_{AB}-P_A\otimes P_B\|_{\rm TV}\to\tfrac12,
\]
with a verified microscopic model and proof. The isolated-copy versus joint thresholds sharpen its practical meaning. No exact earlier version was found in this bounded search, but broader novelty claims are unsupported.

Retrieved primary PDFs and text are stored in research/sources under prefixes ramirez-etal-2008-zeroth, posch-thirring-2006-negativeheat, cohen-etal-2014-shared, lebowitz-etal-1967-fluctuations, and ptaszynski-esposito-2023-ensemble.
