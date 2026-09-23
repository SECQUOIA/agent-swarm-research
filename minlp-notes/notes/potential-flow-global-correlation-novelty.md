# Global resistance correlations on cacti: focused source assessment

Date: 2026-09-05. Primary-source assessment by `joint_flow_novelty`.
The complete [arc-validation draft](potential-flow-global-correlation-arc-validation.md)
and [total-arc-flow hardness draft](potential-flow-global-correlation-total-flow-hardness.md)
were read. Independent mathematical audits are separate.

The positive quadratic-law capacity reduction has a direct literature
antecedent and should be credited as a straightforward cactus extension.
No matching restricted hardness theorem was found for maximizing the sum
of every positive arc flow on a degree-three cactus, with unit end-to-end
nominations, quadratic passive laws, bounded resistances, and one explicitly
encoded global resistance polytope. This remains a qualified search finding.
The Max-Cut mechanism and broad circuit-tolerance hardness are established.

## Exact capacity intervals: direct prior, not a new linearization

Aßmann, Liers, Stingl, and Vera,
*Deciding Robust (In-)Feasibility Using Set Containment: An Application to
Uncertain Gas Networks*, [primary preprint](https://arxiv.org/pdf/1808.10241),
Section 4.3.2, Proposition 4.9 and Lemma 4.10, PDF pp.20–21, derive a
single-cycle equation and prove that a prescribed cycle-flow interval is
equivalent to two inequalities in the pressure-loss coefficients. The text
after the lemma explicitly identifies these as linear restrictions in the
coefficients. Proposition 4.11 explicitly notes that intersection with a
polyhedral uncertainty set remains polyhedral. Those statements and the
complete Lemma 4.10 proof were reread. Section 4.1.4 also confirms fixed
nominations and uncertain positive loss factors.

Our comparison: the local halfspace description does not require independent
resistance intervals. On a cactus, fixed nominations give one independent
physical circulation equation per block; shared parameters can occur in
every equation. Conjoining the known interval restrictions with a global
rational polytope therefore gives the candidate's one-LP existential
capacity test. Robust validation by optimizing each resulting affine
inequality is also a direct consequence. This is useful, but should not
be presented as a newly discovered quadratic-law feasibility principle.

For parameter-affine continuous piecewise-polynomial laws, evaluating a
cycle balance at a rational capacity endpoint still gives an affine
parameter expression. Extending the same argument is elementary under
the stated monotonicity promises and fixed rational breakpoints. Exact
individual-arc extrema and rational optimizing profiles additionally use
the [monotone-root arithmetic lemma](monotone-polynomial-root-polytope-novelty.md).
That lemma's source assessment recommends a supporting arithmetic
refinement, not a new general quasilinear optimization paradigm.

## Nonlinear circuit tolerance analysis already has extensive precedents

Lubomir V. Kolev and Valeri M. Mladenov,
*Worst-Case Tolerance Analysis of Non-Linear Circuits Using an Interval
Method*, X International Symposium on Theoretical Electrical Engineering,
Magdeburg, September 1999, printed pp.621–623,
[open proceedings scan](https://arnold-neumaier.at/glopt/gicolag/kolev/P4.pdf),
studies nonlinear resistive circuits with interval uncertain coefficients
and proposes iterative outer solution enclosures. Sections 2–3 formulate
the uncertain nonlinear system and its successive linear interval
enclosures; a transistor/diode example follows. The three article pages
were read visually from the scan. Browser screenshots timed out, but
ordinary download of the same open URL succeeded; text extraction was
empty, so no claim relies on OCR.

Comparison: this is prior for nonlinear circuit uncertainty and certified
enclosure methods. The inspected article does not give a correlated-cactus
complexity classification or the present all-arc objective reduction.

Kolev's *Worst-case tolerance analysis of linear DC and AC electric
circuits*, IEEE TCAS I 49(12), 1693–1701,
[author-posted primary abstract](https://www.researchgate.net/publication/3324037_Worst-case_tolerance_analysis_of_linear_DC_and_AC_electric_circuits),
DOI `10.1109/TCSI.2002.805700`, allows system coefficients that are nonlinear
functions of shared independent interval parameters. It describes inner
and outer bounds and exactness under monotonicity conditions. Only the
abstract was read in this audit. This prevents treating dependencies among
circuit coefficients as a new uncertainty model; it does not establish
the candidate's restricted hardness theorem.

Yamamura, Ishiguro, and Taki,
*Characteristic Analysis and Tolerance Analysis of Nonlinear Resistive
Circuits Using Integer Programming*, IEICE E99.A(3), 710–719 (2016),
[primary publisher abstract](https://www.jstage.jst.go.jp/article/transfun/E99.A/3/E99.A_710/_article),
formulates characteristic and operating-region analysis as MIP problems.
Only the abstract was read; the article is marked restricted access.
Using MIP does not itself prove an NP-hardness result.

The earlier [discrete-resistance audit](potential-flow-discrete-resistance-hardness-novelty.md)
records Huang–Bryant's 1993 NP-completeness of extremal steady-state
voltages in general linear switch-level MOS networks. Its
[institutional primary abstract](https://research.ibm.com/publications/intractability-in-linear-switch-level-simulation)
was reopened. That broad hardness predecessor uses a different physical
model and unrestricted topology. The unread Hasler–Wang 1993 nonlinear
tolerance paper remains a residual priority gap; its title alone settles
neither duplication nor novelty.

## What the hardness construction contributes, if verified

The combinatorial reduction is a standard convex-maximization realization
of unweighted Max-Cut. As one openly accessible primary reference,
Del Pia, Dey, and Molinaro,
[*Mixed-integer Quadratic Programming is in NP*](https://arxiv.org/pdf/1407.4798),
Section 1.1, Corollary 2, PDF p.2, explicitly recalls the binary quadratic
cut encoding. The candidate replaces that familiar cut reward by an even
convex pair of physical triangle responses. The general fact that a convex
function on a cube has a maximizing vertex supplies binary attainment.
Neither operation introduces a new combinatorial hardness mechanism.

The specific physical restriction is more informative: each comparison
uses two triangles with path resistances `2+(theta_i-theta_j)` and
`2-(theta_i-theta_j)`. The actual edge-resistance polytope includes extra
bridge coordinates representing the cube parameters, so it is given
explicitly by bounded-coefficient linear constraints rather than by an
unexamined projected representation. At cube vertices, the all-arc sum
is a fixed baseline plus a fixed positive constant times cut size.

Retain all the scope distinctions. The number of cycles grows; this is
not a fixed-global-cycle-rank lower bound. Unit source/sink nominations
fix the transported amount. The variable objective sums flow over all
arcs, counting a unit again when it traverses another edge; it is not
maximizing end-to-end delivered throughput. On this construction every
arc flow is positive, so the signed sum also equals the sum of magnitudes.

The positive feasibility theorem is consistent with the hardness result.
Individual capacity constraints become linear in parameters, but a sum of
several cycle-root responses generally does not. Moreover, correlations
between cycles remove the independent affine-box flow region used in the
earlier cactus linear-objective algorithm. Graph sparsity alone does not
control the complexity of the global parameter dependencies.

The draft's strong hardness and fixed absolute-error claim use bounded
physical data and a constant cut reward, not numerical amplification of
a weak Subset Sum gap. Its NP/coNP membership argument applies to the
explicit paired-triangle family, where vertex values lie in the fixed
field `Q(sqrt(2),sqrt(3))`. Do not extend membership to arbitrary sums of
algebraic cycle responses. No constant relative-error or normalized-objective
approximation barrier is established.

## Assessment

Recommend positioning this as a structural boundary between linear
parameter-space capacity validation and coupled physical-flow optimization.
Credit Aßmann and coauthors directly for the interval-to-halfspace lemma,
the classical Max-Cut reduction principle, and circuit-tolerance
predecessors. No equivalent bounded-data cactus theorem was located in
the primary material inspected, but the result should remain qualified
until its mathematical audits and broader priority investigation are complete.

Fresh searches covered correlated resistor tolerances, shared uncertain
circuit parameters, polyhedral friction uncertainty, continuous resistance
design, total-flow objectives, and restricted-topology hardness. Generic
load-correlation, stochastic power-flow, and discrete network-design papers
were not treated as equivalent merely because they mention correlations
or NP-hardness. This note is a bounded source assessment, not a proof audit
or exhaustive novelty certification.
