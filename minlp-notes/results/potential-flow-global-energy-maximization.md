# Maximum dissipation over a resistance polytope is a convex conic problem

Date: 2026-09-05. Status: verified supporting result after two independent full mathematical audits, an independent certificate-code audit, and a completed bounded primary-source assessment. Its convexity and conic mechanisms are classical; the precise rational-scenario and certificate guarantees complement the correlated-resistance minimum-energy hardness result.

## Theorem

Let G be any finite connected graph with rational balanced fixed nominations b and quadratic laws pi_u-pi_v=beta_e x_e|x_e|. Let beta belong to a nonempty bounded rational polytope P with explicit positive bounds beta_L<=beta_e<=beta_U. There is no cactus or cycle-rank restriction.

Maximizing total physical dissipation

    D(beta)=sum_e beta_e |x_e(beta)|^3=b^T pi(beta)

over P has an exact second-order cone formulation. For every rational epsilon>0, a rational admissible resistance scenario with dissipation at least max_P D-epsilon is computable in polynomial time in input length and requested accuracy bits.

For unit source/sink nominations, D(beta) equals the source-to-sink potential difference. Thus its maximum is additively tractable under arbitrary global polytope correlations, whereas its minimum is strongly hard already on a cactus in the [reviewed energy-design construction](potential-flow-global-correlation-energy-design-hardness.md). No other physical capacity or potential restrictions filter scenarios in this positive theorem.

## 1. Energy duality makes joint resistance maximization convex

For fixed beta, define the minimum primitive energy

    V(beta)=min_{Ax=b} sum_e beta_e |x_e|^3/3.

Strict convexity and coercivity give a unique minimizer. The Lagrangian dual, with one potential fixed to zero, is

    V(beta)=max_pi [b^T pi-(2/3)sum_e sqrt(|(A^T pi)_e|^3/beta_e)].

The scalar conjugate follows by maximizing dx-beta|x|^3/3: its optimizing magnitude is sqrt(|d|/beta), and its value is (2/3)|d|^(3/2)/sqrt(beta). Strong duality holds on the nonempty affine conservation space. At the physical state the homogeneous identity gives D(beta)=3V(beta).

The conjugate term is a convex perspective in (d,beta). Therefore maximizing the displayed dual expression jointly over beta in P and pi is convex optimization, and its value equals max_P V because both optimizations are maximizations.

## 2. Explicit second-order cones

For each edge introduce z_e,u_e,t_e>=0 and impose

    z_e >= (A^T pi)_e,   z_e >= -(A^T pi)_e,
    z_e^2 <= t_e u_e,
    u_e^2 <= beta_e z_e.

The last two inequalities are rotated second-order cones. They are equivalent, after eliminating u, to z_e^3<=beta_e t_e^2. If z>0 multiply the inequalities and divide by z; conversely choose u=z^2/t when t>0. The z=0 case uses u=0. Thus projecting these constraints gives

    t_e>=sqrt(|(A^T pi)_e|^3/beta_e).

The exact conic maximization is

    maximize b^T pi-(2/3)sum_e t_e
    subject to beta in P and all the preceding constraints.

Multiplying its optimum by three gives maximum physical dissipation. The formulation uses two rotated cones per edge and polynomially many rational linear constraints. It is valid on arbitrary connected graphs.

## 3. Compact bounds and a polynomial-bit interior point

Let m be the number of edges and B=sum_v |b_v|. Handle B=0 and edgeless graphs directly. Every passive physical flow has magnitude at most B. With one reference potential zero, an optimal dual potential can be chosen with

    |pi_v|<=m beta_U B^2.

At this physical dual point, the cone variables can be chosen as

    z_e=beta_e |x_e|^2,
    u_e=beta_e |x_e|,
    t_e=beta_e |x_e|^3.

They attain the exact dual value. Hence polynomial-bit rational upper bounds of these magnitudes contain a global optimizer.

To ensure a strict conic interior point, put r=min(1,beta_L)/2 and use pi=0, z_e=1, u_e=r, t_e=2/r at any relative-interior beta0 of P. Then z_e>|(A^T pi)_e|, t_e u_e=2>z_e^2, and beta_e z_e>=beta_L>r^2. Enlarge the preceding upper bounds to exceed these interior coordinates by at least one, and use the potential bound m beta_U B^2+1. Every bound has polynomial rational encoding length.

Compute the affine hull of P and express beta in rational coordinates on that hull. A rational relative-interior point with polynomial-bit positive facet slacks is available by rational LP: identify constraints tight throughout P and average feasible points witnessing positive slack for all remaining constraints. Rational LP basic-solution bounds give polynomial-bit lower bounds on each resulting nonzero slack. If P is a singleton there are no beta coordinates to retain.

After this affine change, the bounded conic feasible region has a rational interior point and an explicitly bounded positive inner radius with polynomial encoding length. Indeed, all its strict linear and quadratic inequalities have polynomial-bit slacks at the displayed point; their gradients are bounded on a polynomial-bit neighborhood. Taking a sufficiently small rational radius preserves those inequalities. An outer radius follows from the coordinate bounds and the rational affine transformation. The region is convex because the two quadratic inequalities are used with nonnegative cone coordinates.

## 4. Rational optimization and original-scenario recovery

Membership in the compact conic region is decided exactly on rational points by rational linear and quadratic comparisons. This supplies a weak membership oracle. The linear objective is globally Lipschitz with an explicit rational bound. The bounded convex-optimization theorem in [Dadush's thesis](https://homepages.cwi.nl/~dadush/papers/dadush-thesis.pdf), Theorem 2.5.9, therefore computes a rational feasible conic point within epsilon/3 of the maximum in polynomial bit time. The affine coordinate transformation recovers rational beta in the original P exactly.

At every feasible conic point, its objective is a lower bound on V(beta). Thus if the returned point has objective at least max_P V-epsilon/3, its original resistance scenario satisfies

    D(beta)=3V(beta)>=max_P D-epsilon.

No physical-flow rounding or exact radical-sum evaluation is needed for this guarantee. The feasible rational conic point itself is a dual lower certificate for its returned scenario. The formulation does not promise a rational physical flow or an exact optimal resistance vector in every instance.

An exact conic formulation is not an exact polynomial-time scalar threshold algorithm. With fixed resistances and unit source/sink nominations on a cactus, D is the terminal potential difference, so exact threshold comparison already inherits the [square-root-sum barrier](../results/potential-flow-cactus-square-root-sum.md). The computational guarantee here is additive bit precision and original rational scenario recovery.

## Exact capacity filters on a cactus

When the graph is a cactus, the [reviewed global-correlation arc theorem](../results/potential-flow-global-correlation-arc-validation.md) converts all rational physical arc capacities into affine inequalities in the resistances. Intersect them with P to form the rational polytope P_cap, rejecting it if empty. Applying the present conic algorithm to P_cap maximizes dissipation to additive precision while returning a rational resistance scenario satisfying those capacities exactly.

This is a direct composition of the two reviewed constructions. The general-graph theorem does not otherwise claim that physical capacity filters are affine or that its unconstrained conic formulation enforces them.

The term dissipation denotes the mathematical quantity `sum_e beta_e |x_e|^3=b^T pi`. If a gas model uses squared pressure as its potential, the potential difference is a squared-pressure difference; this identity does not identify the quantity with literal compressor power.

## Attribution and verification

The [bounded primary-source assessment](../notes/potential-flow-global-energy-maximization-novelty.md) is complete. The energy variational formulation, concavity in resistance, Fenchel duality, power perspectives, two-cone representation, and weak-membership convex optimization are established. Thus the broad tractability mechanism is a direct consequence of classical theory. The source search did not locate the full combination of arbitrary graph, global resistance polytope, polynomial-bit rational scenario output, and exact original-instance certificate, but absence from this bounded search does not establish priority. The result is retained as an explicit supporting positive companion to the minimum-energy hardness boundary.

Both [the first mathematical audit](../notes/review-potential-flow-global-energy-maximization.md) and [the second mathematical audit](../notes/review-potential-flow-global-energy-maximization-second.md) passed, including the exact cactus capacity-filter composition and the global certificate. They checked cone boundary cases, physical bounds, lower-dimensional polytopes, and the exact feasible-output hypothesis in Dadush's theorem. The certificate implementation also passed a separate code audit, detailed below.

## Exact rational certificate for global design quality

The formulation also gives a certificate independent of a numerical solver. Write the complete bounded positive resistance polytope as P={beta:R beta<=c}, and let A continue to denote the graph incidence matrix. Let y be any rational conserved flow, Ay=b.

Choose rational multipliers lambda>=0 satisfying

    R^T lambda=w,   w_e=|y_e|^3/3.

Then U=c^T lambda is an upper bound on max_P V: for every beta, its physical energy is at most the trial energy beta^T w, and LP weak duality bounds beta^T w by U.

For a rational feasible chosen profile beta0, choose rational normalized potentials pi and rational t_e>=0 with

    beta0_e t_e^2>=|(A^T pi)_e|^3.

They give the rational lower bound L=b^T pi-(2/3)sum_e t_e<=V(beta0). Upward rational square-root enclosures can construct these t values. Therefore

    max_P D-D(beta0)<=3(U-L).

All certificate checks are exact rational equalities and inequalities: flow conservation, original polytope feasibility, LP dual feasibility, and conjugate upper bounds. This certificate verifies global design quality, not merely closeness to the physical state of one fixed profile. It does not require computing that profile's irrational physical flow.

As an exact zero-gap example, take a triangle with two path edges and one direct edge, unit through-nominations, and P={beta in [1,4]^3:sum beta=6}. The conserved trial flow is y=(1/2,1/2,1/2). Its energy coefficients are all 1/24, so the sum constraint gives U=1/4. The chosen profile beta0=(3/2,3/2,3), potentials (3/4,3/8,0), and t=(3/16,3/16,3/8) give L=1/4. Thus the rational certificate proves the maximum dissipation is 3/4 and that this original resistance scenario attains it exactly.

## Reproducible conic designs and certificate checker

[`energy_design_certificate.py`](../code/potential_flow_mpd/energy_design_certificate.py) is a standard-library rational checker for the complete original quadratic design instance: graph, nominations, positive resistance box, additional global polytope inequalities, chosen profile, and all certificate vectors. It uses unconditional validation, including under optimized Python. The [saved triangle certificate](../code/potential_flow_mpd/energy_design_certificate_example.json) proves maximum dissipation exactly 3/4 with zero scenario loss. This JSON specifies the quadratic optimization problem over its encoded parameter polytope. It does not contain separate physical operating bounds; any derivation of that polytope from such bounds remains a separate check.

[`global_energy_socp_checks.py`](../code/potential_flow_mpd/global_energy_socp_checks.py) solved six cycle and complete-graph design instances, including noncactus graphs, with a global resistance-budget equality. It rounded the original resistance profile and trial flow to rational feasible vectors, supplied exact LP-dual upper bounds for the budget polytope, and verified every global certificate independently of the solver's status. All six solver statuses were `optimal`. The largest certified additive dissipation loss was below `2.74e-5`; this is the achieved rigorous guarantee, not the solver's tighter numerical termination tolerance. The script is a numerical certificate producer, not a general implementation of the polynomial-bit convex-body theorem.

The separate [certificate code audit](../notes/review-potential-flow-global-energy-certificate.md) passed. Its [independent standard-library checker](../code/potential_flow_mpd/check_energy_design_certificate_review.py) accepted 99 exact known certificates and 99 potential gauge shifts, rejected 151 malformed direct inputs, and rejected 294 corrupt CLI files under normal and optimized Python. It independently checked the full encoded uncertainty problem and every upper/lower-bound condition. No code correction was required.

## Reproduction commands

Run from the repository root:

```sh
python code/potential_flow_mpd/global_energy_maximization_second_review.py
python code/potential_flow_mpd/energy_design_certificate.py --verify code/potential_flow_mpd/energy_design_certificate_example.json
python code/potential_flow_mpd/check_energy_design_certificate_review.py
```

The first and third commands use only the standard library. The third also runs the certificate CLI under normal and optimized Python. The numerical producer uses the scientific environment and its installed conic solver; its rigorous output guarantee is the exact certificate gap reported above.
