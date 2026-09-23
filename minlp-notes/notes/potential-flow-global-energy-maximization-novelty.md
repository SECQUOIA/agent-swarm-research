# Global resistance-polytope energy maximization: source assessment

Date: 2026-09-05. Bounded primary-source assessment by `joint_flow_novelty`.
The full [candidate](potential-flow-global-energy-maximization.md), including
its rational global certificate and cactus capacity-filter corollary, was
read. The independent mathematical and certificate-code audits are separate.

The result is best positioned as an explicit positive companion to the
correlated-resistance minimum-energy hardness theorem. Its central
tractability mechanism follows directly from established variational
duality and resistance-energy concavity. Two rotated cones per edge are
an instance of known power-cone representations. No exact matching
statement with the entire graph, correlation, rational-scenario, and
certificate scope was located, but this does not justify calling the
underlying convexity or conic method new.

The precise construction maximizes physical quadratic dissipation over
an arbitrary bounded positive rational resistance polytope, on any connected
graph with fixed balanced nominations. It gives additive polynomial-bit
optimization and a rational original resistance scenario. The general-graph
theorem does not impose additional physical capacity or potential filters.

## Energy duality and the max/min distinction

The [minimum-energy source addendum](potential-flow-global-correlation-energy-novelty.md)
documents the checked primary variational formulation in Groß, Pfetsch,
Schewe, Schmidt and Skutella,
[Section 3, Equation (7)](https://optimization-online.org/wp-content/uploads/2017/08/6185.pdf).
For fixed nominations, physical flows minimize the sum of integrated
constitutive laws over the affine conservation space. It also documents
Ghosh–Boyd–Saberi's direct attribution of linear resistance concavity to
Shannon–Hagelbarger. Those source readings are reused here.

Comparison: the minimum primitive energy is an infimum of affine functions
of resistance, hence concave in resistance. Its maximization over a polytope
is therefore a convex optimization problem at the value-function level.
For the quadratic law, conjugating the cubic primitive gives the explicit
perspective `|d|^(3/2)/sqrt(beta)`. Maximizing the dual jointly over potential
and resistance is a direct use of duality; no interchange of a minimum and
maximum is needed for that displayed formulation. Homogeneity supplies
the factor of three between primitive energy and dissipation.

The positive maximum result and the hard minimum result consequently fit
the classical distinction between concave maximization and concave
minimization. A broad claim that correlated resistance uncertainty is always
hard would be incorrect. So would transferring this conclusion to arbitrary
weighted potentials or flow objectives, which need not have the same
energy representation.

## The two-cone representation has direct prior

Lobo, Vandenberghe, Boyd and Lebret, *Applications of second-order cone
programming*, [primary author copy](https://web.stanford.edu/~boyd/papers/pdf/socp.pdf),
Section 2.3, printed pp.199–201/PDF pp.7–9, converts nonnegative hyperbolic
constraints into second-order cones and builds geometric-mean formulations
from them. These constructions and examples were read directly. The paper
credits Nesterov and Nemirovsky for the geometric-mean construction.

Jie Wang, *Weighted Geometric Mean, Minimum Mediated Set, and Optimal
Simple Second-Order Cone Representation*,
[primary manuscript](https://arxiv.org/pdf/2206.05924), introduction,
PDF pp.1–3, treats rational weighted means and power cones. Remark 19 and
Corollary 21, PDF p.11, give an optimal simple representation size of
`ceil(log2 p)` for a bivariate mean with coprime weights `q/p,(p-q)/p`.
These sections and the adjacent construction were read. The qualification
“simple” is material: this is a specified subclass of SOC representations,
not a blanket lower bound for every possible conic lift.

Comparison: the candidate's scalar inequality is
`z <= beta^(1/3) t^(2/3)`, with nonnegative coordinates. It has denominator
three, so the established bivariate construction uses two quadratic cones.
The candidate's explicit equations are a valid specialization, not a new
power-cone representation or a new minimum-cone-count result. Writing them
out is useful for implementation and zero-case verification.

## Earlier robust circuit design uses different uncertain data

Diah Chaerani, *Modelling Robust Design Problems via Conic Optimization*,
2006 doctoral thesis,
[primary institutional copy](https://repository.tudelft.nl/file/File_0bc723d5-0864-494b-8bc7-5a6caa55afe0),
Chapter 6, Sections 6.5.1–6.5.3, printed pp.64–69, derives a variational
potential expression for linear-circuit dissipation and semidefinite
formulations. The robust model in Equation (6.30) varies external currents
over an ellipsoid; Equation (6.32) minimizes worst-case dissipation through
conductance allocation under a normalization constraint. These model
sections and the associated variational and robust equivalence proofs
were read directly.

The related 2012 Roos–Bai–Chaerani
[publisher abstract](https://squjs.squ.edu.om/squjs/vol17/iss1/2/)
describes linear and semidefinite resistor-network design models. Its
download failed during this audit; the 2006 thesis was read as a separate
primary source, not represented as a retrieved copy of that article.

Comparison: variational conic optimization of robust resistive networks is
established. The thesis's adversarial parameter is the current vector and
its design parameter is conductance. The candidate fixes nominations and
optimizes over a polytope in resistance coordinates for a quadratic law.
The sources do not support treating these two parameterizations or
uncertainty models as interchangeable.

The recent [Klimm–Pfetsch–Skutella–Strubberg preprint](https://arxiv.org/pdf/2604.26882),
already checked in the energy-minimum addendum, is also relevant: its
Corollary 4 gives convex continuous conductance-cost design without fixed
installation costs. That conclusion concerns a different objective and
parameter space. It supplies context for tractable nonlinear network
design, not a contradiction or an exact match to this resistance maximum.

## Rational scenario recovery and the global certificate

Dadush's *Integer Programming, Lattice Algorithms, and Deterministic Volume
Estimation*, [primary thesis](https://homepages.cwi.nl/~dadush/papers/dadush-thesis.pdf),
Theorem 2.5.9, printed p.48/PDF p.61, states polynomial-time convex
optimization on a centered body with a weak membership oracle and a
Lipschitz objective, returning a rational feasible point and an additive
value guarantee. The definitions and theorem were reread directly. The
thesis credits the classical weak-membership/optimization equivalence.

Comparison: the candidate's useful implementation obligations are the
explicitly bounded optimal potentials and cone variables, handling the
affine hull of a possibly lower-dimensional resistance polytope, and a
rational interior point with polynomial-bit radii. These permit use of the
established theorem. Rational scenario recovery then follows by projection
of a feasible conic point and its valid physical dual lower bound. This
is a precise output guarantee, not a new general conic complexity result.

The certificate combines two classical weak-duality bounds. A conserved
trial flow supplies a resistance-linear upper bound on physical primitive
energy. Nonnegative LP dual multipliers certify its maximum over the
complete resistance polytope. Potentials and rational conjugate upper
bounds provide a lower bound for the chosen scenario. Their difference
certifies global design quality. The certificate's original-instance
encoding and exact rational checker are useful reproducibility artifacts;
the Fenchel and LP weak-duality mechanisms are established.

An exact conic formulation does not imply polynomial-time exact scalar
comparison or rational optimal physical flows. The additive result and its
rational resistance output should remain distinct from exact algebraic
or square-root-sum evaluation. A successful rational certificate likewise
certifies its stated gap; a floating-point solver status alone does not.

## Scope and qualified positioning

The cactus capacity-filter addendum is a direct composition: the earlier
cycle-capacity halfspaces produce a rational resistance polytope, then the
energy conic program applies. The source attribution to Aßmann and coauthors
for those halfspaces should remain visible. Capacity filtering on arbitrary
graphs is not covered by that corollary.

For unit source/sink nominations the objective is the prescribed potential
difference. With squared-pressure potentials it is a squared-pressure
difference, not automatically an ordinary pressure drop or compressor power.
General fixed nominations give the energy pairing `b^T pi`.

A suitable description is: “Classical passive-flow energy duality gives an
explicit SOCP for worst-case dissipation under globally correlated positive
resistance uncertainty. The construction provides polynomial-bit rational
scenarios and exact rational certificates, complementing the minimum-energy
hardness boundary.” The combined scope was not found verbatim in the primary
sources checked, but its main tractability mechanism is a direct consequence
of established theory and should be presented accordingly.
