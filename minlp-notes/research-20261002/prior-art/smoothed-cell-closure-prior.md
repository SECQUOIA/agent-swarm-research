# Prior-art audit: exact optimization by closing smoothed cells

Date: 2026-10-02. This focused audit compares the reviewed
[exact cell-closure theorem](../new-direction/smoothed-exact-cell-closure.md)
with multiparametric quadratic programming and parametric global optimization.
It records close precedents and scope limits; it is not a completeness or
publication-priority claim.

## Candidate result

The candidate solves a rational quadratic objective on a bounded rational
polytope after adding one fixed, finite rational-grid linear perturbation in
the negative-curvature factor coordinates. It writes the objective as convex
quadratic recourse plus a low-dimensional parameter function. A convex-QP
KKT basis queried at a cell corner supplies an affine optimizer and a
quadratic value formula on a polyhedral critical region. If one such region
contains a whole cell, the algorithm solves that cell's quadratic exactly
and closes it. Otherwise a retained cell forces the sampled perturbation
near one of finitely many fixed hyperplanes associated with critical-region
boundaries or singular gradient images. A sufficiently fine noise grid is
chosen from the unperturbed input before sampling; an exact enumeration
fallback on the same draw handles every exceptional case.

The theorem gives an exact rational optimizer and value for every draw, with
expected bit work bounded by
`C^k (1 + H_grid) (I + 1)^C`, where `k` is the negative-space dimension and
`H_grid` captures the factor-coordinate range relative to the noise scale.
It allows arbitrary negative inertia and makes no quadratic-growth promise.
The perturbation is aligned with the supplied negative-space factor, so its
original-coordinate coefficients are correlated and supported on a
low-dimensional subspace. The theorem does not cover independent noise in
all original coordinates.

## Strongest conceptual precedent: parametric global optimization

Baoyan Ding's Waterloo thesis, *A Parametric Solution for Local and Global
Optimization* (1996), is the closest formulation-level predecessor found.
For certain nonconvex quadratic programs, it fixes a low-dimensional
parameter in a convex parametric QP, obtains a piecewise-quadratic value
function, and then globally minimizes that value function; optimizers of
the original problem are recovered from the minimizing parameter's fiber.
The thesis's Theorem 2.2.5 states the global-minimum/fiber correspondence
(PDF p. 29; printed thesis p. 20). Its scalar negative-eigenvalue
construction uses parametric QP interval pieces and searches the parameter
range; the one-negative-eigenvalue case and Theorem 2.3.1 are on PDF
pp. 30–34 (printed pp. 21–25). Its arbitrary-negative-rank construction
proceeds by recursive lower-dimensional decomposition.
Thus the auxiliary parametric convex-QP representation, piecewise-quadratic
global objective, and lifting of a global value-function minimizer are
classical ingredients. Ding does not state the candidate's finite rational
noise law, random retained-cell bound, exact same-draw fallback, or expected
bit-complexity guarantee. The thesis was inspected from the official
[Waterloo repository record](https://uwspace.uwaterloo.ca/items/0ee267e7-ed4c-4eab-adff-a202444a746a)
and [author manuscript PDF](https://dspacemainprd01.lib.uwaterloo.ca/server/api/core/bitstreams/2c9e7b72-4454-4349-9741-b33beb9689ad/content).
The complete local source package is now read by the literature-ingest agent;
its `KB_CHECK` passed.

## Critical-region machinery

For a convex parametric QP, fixing a linearly independent active constraint
set and applying KKT conditions gives affine primal and multiplier maps.
Primal feasibility and multiplier nonnegativity define a polyhedral
critical region, and substitution gives a quadratic value formula there.
Bemporad, Morari, Dua, and Pistikopoulos prove the piecewise-affine optimizer
and piecewise-quadratic value structure for explicit constrained LQR under
positive-definite Hessian assumptions; they recursively partition the
parameter domain to enumerate regions. Tøndel, Johansen, and Bemporad give
an adjacent-region active-set exploration algorithm, including tests for
degeneracy and lower-dimensional active sets. Their region counts and
algorithms are worst-case/output-sensitive, not smoothed expected bounds.
These sources establish the KKT-region and region-exploration machinery used
by the candidate; they do not give its closure test as an expected exact
global-QP algorithm.
[[bemporad2002-the-explicit-linear-quadratic-regulator]] p.7-12
[[tndel2003-an-algorithm-for-multi-parametric]] p.2-7

Patrinos and Sarimveis study convex parametric piecewise-quadratic
optimization, including multivalued solution mappings and algorithms for
discovering adjacent critical regions. The 22-page author report states
that graph traversal enumerates the closures of all full-dimensional
critical regions, and describes the method's output sensitivity
qualitatively in terms of input and output size (number of regions). It
allows multivalued solution maps and does not assume constraint
qualifications for its adjacency procedure. It does not give a worst-case
region-count bound, a polynomial bit-complexity theorem, or a smoothed
global-optimization result. This is strong prior art for the deterministic
critical-region machinery and its nonunique convex recourse case; it does
not cover the candidate's random-cell expected bound or indefinite global
QP. The full author manuscript and exact theorem locators have now been
read by the literature-ingest agent. [[patrinos2011-convex-parametric-piecewise-quadratic-optimization]]
p.7-9, p.14-17

Bemporad and Filippi instead recursively subdivide parameter space into
simplices to approximate convex parametric programs. Their method has a
prescribed value-function error and work polynomial in the number of output
simplices when the convex-program oracle is polynomial; the number of
simplices can still be large. It is an approximation and output-sensitive
comparison, not exact closure of a cell on one critical-region quadratic or
a smoothed expected cell count.
[[bemporad2006-an-algorithm-for-approximate-multiparametric]] p.3-13

## Randomized region exploration

Katz and Pistikopoulos use offline hit-and-run samples in the feasible
parameter polytope to select critical-region representatives for partial
explicit MPC; online they use a nearest representative to hot-start the
active-set solver. This is the closest randomized critical-region
exploration source identified in this focused search. Its full text reports
computational experiments, not a formal finite-sample region-coverage bound,
an expected active-region count, or an exact global solver for a nonconvex
QP under random objective coefficients. The source has now been read in the
local package. DOI
[10.1016/j.compchemeng.2020.107057](https://doi.org/10.1016/j.compchemeng.2020.107057);
[author-accepted manuscript](https://par.nsf.gov/servlets/purl/10195683).

The broader smoothed-optimization comparators are also different in model.
Kelner and Nikolova bound expected projected-shadow vertices under random
rotations of a low-rank quasi-concave objective; Beier and Vöcking analyze
independent random objective coefficients over finite discrete feasible
sets. Neither result supplies a continuous parametric-QP cell-closure
bound under the candidate's fixed factor-aligned finite noise law.
[[kelner2007-on-the-hardness-and-smoothed]] p.3-4
[[beier2006-typical-properties-of-winners-and]] p.3-4, p.9-10

## Assessment and search boundary

The strongest prior overlap is not merely standard explicit-MPC geometry:
Ding already reduces classes of indefinite QPs to global optimization of a
piecewise-quadratic parametric convex-QP value function. That substantially
narrows any novelty claim about the reduction or the use of a piecewise
quadratic envelope. Explicit-MPC work further establishes critical-region
representations and active-set traversal, while approximate multiparametric
programming and partial explicit MPC provide output-sensitive or empirical
region-exploration precedents.

In the sources examined so far, I found no theorem combining (i) arbitrary
negative inertia, (ii) a fixed finite rational perturbation law aligned to
the negative factor, (iii) exact rational global output on every draw using
a same-draw fallback, and (iv) expected bit work controlled by the
conditioned range/noise ratio. The candidate-specific mechanism is the
expected analysis of unresolved cells through a fixed finite family of
critical-region/gradient-image hyperplanes, together with the preselected
finite noise grid and exact fallback. This is a scoped search result only;
it does not establish novelty or exclude an equivalent algorithm under
another formulation.

## Sources and access status

- Ding, Baoyan, *A Parametric Solution for Local and Global Optimization*,
  University of Waterloo thesis (cover year 1996; repository record dated
  1997), especially Theorems 2.2.4–2.2.5, PDF pp. 28–29, and the
  one-negative-eigenvalue construction, PDF pp. 30–34. The local full text
  and original PDF were read and checked by the sole literature-ingest agent.
- Bemporad, Morari, Dua, and Pistikopoulos (2002), “The Explicit Linear
  Quadratic Regulator for Constrained Systems,” *Automatica* 38(1):3–20,
  [DOI 10.1016/S0005-1098(01)00174-1](https://doi.org/10.1016/S0005-1098(01)00174-1).
  Local full text and notes read.
- Tøndel, Johansen, and Bemporad (2003), “An Algorithm for Multi-parametric
  Quadratic Programming and Explicit MPC Solutions,” *Automatica*
  39(3):489–497, [DOI 10.1016/S0005-1098(02)00250-9](https://doi.org/10.1016/S0005-1098(02)00250-9).
  Local full text and notes read; important conditions checked against the
  original PDF because extracted text is degraded.
- Bemporad and Filippi (2006), “An Algorithm for Approximate Multiparametric
  Convex Programming,” *Computational Optimization and Applications*
  35:87–108, [DOI 10.1007/s10589-006-6447-z](https://doi.org/10.1007/s10589-006-6447-z).
  Local full text and notes read.
- Patrinos and Sarimveis (2011), “Convex Parametric Piecewise Quadratic
  Optimization: Theory and Algorithms,” *Automatica* 47(8):1770–1777,
  [DOI 10.1016/j.automatica.2011.04.003](https://doi.org/10.1016/j.automatica.2011.04.003).
  The 22-page primary author report is read. Proposition 5 and Theorem 1
  give the convex PWQ value/solution-map structure and critical-region
  characterization (PDF pp. 7–9); Theorem 6 and Algorithms 1–2 give
  adjacency and graph traversal (PDF pp. 14–17). The paper's output
  sensitivity statement is qualitative, not a bit-complexity or region
  count bound.
- Katz and Pistikopoulos (2020), “A Partial Multiparametric Optimization
  Strategy to Improve the Computational Performance of Model Predictive
  Control,” *Computers & Chemical Engineering* 142, 107057,
  [DOI 10.1016/j.compchemeng.2020.107057](https://doi.org/10.1016/j.compchemeng.2020.107057).
  The local package and official NSF author manuscript were read by the
  literature-ingest agent; the result is an empirical two-phase sampling and
  hot-start strategy without a formal smoothed-complexity theorem.
- The reviewed [candidate theorem](../new-direction/smoothed-exact-cell-closure.md)
  and its [independent review](../reviews/smoothed-exact-cell-closure-review.md).

No literature knowledge-base files were edited for this audit. No project-wide
checks or CI inspection were run.
