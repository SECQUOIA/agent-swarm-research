# Prior-art audit: expected exact sparse box QP under random linear noise

Date: 2026-10-02. This focused audit compares the candidate
[sparse bag-cell theorem](../new-direction/sparse-bag-cell-smoothed-qp.md)
with smoothed cell counts, continuous tree-decomposition algorithms, and
global box-QP results. It is not a completeness or publication-priority
claim. The root has read the candidate proof; independent reviews and
targeted exact-DP checks remain in progress.

## Candidate claim and exact scope

The candidate considers a rational quadratic on a product of continuous
intervals, a supplied tree decomposition with largest bag size `p`, and
independent uniform linear perturbations drawn from one fixed finite rational
grid chosen from the base input before sampling. For every draw, the
algorithm returns an exact rational optimizer and value. Its expected bit
work is

```text
C_0^p [4 + (1+n/2)Ls/(2sigma)]^p (I+1)^C,
```

where `L` bounds the diagonal entries of the full Hessian from above, `s`
is the largest interval width, and `I` is the base input length. The bound
gives expected polynomial work for each fixed `p` when `n Ls/sigma` is
polynomially bounded. Its displayed dependence is XP in bag size: it does
not establish an `f(p) poly(I)` bound. It permits arbitrary negative
inertia, needs no occurrence bound, and has no supplied uniqueness or
quadratic-growth promise. The theorem concerns its particular fine finite
noise law, not arbitrary coarse atoms.

The proof uses randomness in two separate ways. First, independent
in-bag noise bounds the expected number of locally near-optimal bag grid
tuples, uniformly over refinement levels. Second, the finite-grid global
growth tail and an active-gradient anti-concentration bound make the
original-bound/PSD closure test succeed with high probability. The
algorithm does not receive or test the growth or margin constants; exact
active-face enumeration on the same draw handles the exceptional event.
Thus “no growth assumption” means no growth promise is part of the input,
not that the proof avoids growth estimates.

## Closest probabilistic predecessor: semiconcave grid counts

The project's [semiconcave-cell analysis](smoothed-semiconcave-cells-prior.md)
already proves a mesh-uniform expected count for near-optimal grid points
under independent linear noise. Its local comparison confines each noisy
coordinate coefficient to an interval of length controlled by coordinate
curvature and mesh width; multiplying the coordinate probabilities and
summing over the tensor grid gives an expected count independent of mesh
depth. It requires no convexity, uniqueness, or quadratic growth. This is
the closest prior mathematical ingredient for the candidate's expected
bag-tuple count.

The earlier theorem works directly on one full continuous box with an
arithmetic oracle. It does not give an exact rational output under a fixed
finite law, an expected bit bound for a sparse tree-decomposition DP, or
the candidate's same-draw exact fallback. Its tensor count is over the
whole box dimension; applying it to a bag would give a bound depending
exponentially on `p`, but it does not by itself establish that sparse
whitelists and bag min-marginals preserve a globally valid lower bound.
The candidate's new algorithmic question is how to charge sparse retained
bag cells and table work while retaining every original optimizer and
triggering an exact convex-face closure with high probability.

Röglin and Rösner's expected Pareto-count theorem is another close
counting result. It handles independent linear profits over an adversarial
finite non-integer point set under a `(k, delta)` coordinate-separation
property. Its count concerns exact Pareto optima, and the bound worsens with
inverse minimum separation; for finer and finer grids that parameter can
grow. It therefore does not give a mesh-uniform count for the candidate's
near-optimal continuous bag tuples or an algorithm to enumerate retained
cells. [[roglin2017-the-smoothed-number-of-pareto]] p.4-7, p.12-13

Beier–Vöcking and Röglin–Vöcking establish the broader pattern of
independent objective perturbations, isolation bounds, and adaptive
precision for finite discrete optimization. Their feasible sets are
integer-valued and their complexity guarantees reduce to discrete winner
gaps or pseudopolynomial solvability. A continuous box has no positive
second-best feasible-value gap, so those results do not provide the
candidate's distance-normalized growth estimate, near-optimal bag-cell
count, or exact rational solver for continuous variables.
[[beier2006-typical-properties-of-winners-and]] p.3-4, p.9-10
[[roglin2007-smoothed-analysis-of-integer-programming]] p.3-8, p.21-28

## Exact and approximate sparse continuous-QP precedents

Del Pia and Khajavirad provide the strongest direct deterministic
box-QP/treewidth comparison. Their dynamic program solves rational
continuous box QP exactly in strongly polynomial `O(n^2)` arithmetic
operations when the interaction graph is a forest. They also prove strong
NP-hardness at interaction-treewidth two for unrestricted box QP, even
with small integral coefficients. The forest result needs neither random
noise nor a growth promise; the width-two hardness makes the candidate's
noise scale and smoothed guarantee substantive restrictions. Neither
result gives an expected exact algorithm for bounded width greater than
one. [[pia2026-treewidth-and-the-complexity-of]] p.3-4, p.20

Faenza, Muñoz, and Pokutta give treewidth-based LP approximations for
sparse polynomial optimization, including QCQP. Their formulation size
has an inverse-accuracy dependence of order `(degree/epsilon)^(tw+1)`;
their lower-bound results also caution against broad treewidth-only
approximation claims. This is an approximate convex-formulation result,
not an expected exact solver under random linear coefficients, and its
accuracy dependence differs from the candidate's expected retained-table
count. [[faenza2022-new-limits-of-treewidth-based]] p.6-15

Continuous graphical-model algorithms establish several nearby forms of
dynamic programming and adaptive discretization:

- Hoang et al.'s EC-DPOP exactly eliminates continuous variables for
  linear or quadratic utility functions on tree-structured graphs.
  Their approximate algorithms handle broader smooth factors with error
  bounds depending on the discretization. The result is a close tree-DP
  baseline, but it does not provide the candidate's fixed-width arbitrary
  box-QP theorem under independent noise or exact closure for arbitrary
  treewidth. [[hoang2020-new-algorithms-for-continuous-distributed]] p.1,
  p.6-7
- Dvijotham et al. use interval messages and lower-bound propagation for
  tree-network OPF. Their theorem allows constraint violation and has an
  `epsilon^-5` bound on local bound-propagation calls under OPF-specific
  assumptions. It is not exact feasible QP optimization and does not give
  a noise-based expected table count. In the arXiv v1 PDF the guarantee is
  Theorem 2, §4.3, PDF pp.16–17; the experimental HTML calls the same
  statement Theorem 4.1. [[dvijotham2017-graphical-models-for-optimal-power]]
  p.6, p.17
- Troullinos et al. put adaptive quadtree approximations inside Max-Sum
  messages for continuous graphical models. Their refinement is heuristic
  and their paper lists theoretical guarantees as future work; it does not
  give a global certificate or expected complexity theorem.
  [[troullinos2022-max-sum-with-quadtrees-for]] p.3, p.8
- Bhathena et al. give an exact DP for convex quadratic optimization with
  binary support indicators under bounded treewidth, polynomial volume
  growth, and a margin assumption. Bienstock and Chen give a
  treewidth-dependent approximation scheme for convex QPs with
  indicator-controlled blocks, with an epsilon-feasibility/superoptimal
  guarantee. These show that exact or approximate treewidth DP can exploit
  conditioning margins in structured convex models, but they do not cover
  arbitrary-inertia continuous box QP or the finite-noise sparse-cell
  count. [[bhathena2026-solving-convex-quadratic-optimization-with]]
  p.14, p.18, p.25
  [[bienstock2024-solving-convex-qps-with-structured]] p.1-3

Standard finite-state min-sum on a supplied tree decomposition is the
algorithmic baseline: if every variable has `q` grid values, dense tables
take time exponential in bag size, typically `q^(p)`, per bag. The
candidate avoids generating all grid rows. It keeps only corners of
surviving bag cells, computes exact bag-row min-marginals, and uses
independent coefficient noise to bound the expected number of relevant
rows independently of the number of mesh levels. It then uses box KKT
signs to pin original-bound coordinates and an exact convex QP solve on
the resulting face. Those sparse-list, exact-closure, and expected
bit-work pieces are not supplied by finite-state DP alone.

Ding's thesis is a close global-QP formulation precedent: it represents
certain structured indefinite QPs by a parametric convex QP and globally
minimizes the induced piecewise-quadratic value function. Theorem 2.2.5
gives an exact global-minimizer/fiber correspondence without isolatedness
(PDF p.29; printed p.20); its one-negative-eigenvalue scalar-envelope
construction is on PDF pp.30–34. This establishes that parametric convex
recourse and piecewise-quadratic global value minimization are classical.
It does not use sparse treewidth tables, random objective coefficients,
or an expected retained-cell bound. [[ding1996-a-parametric-solution-for-local]]
PDF pp.28-34

## Gaussian ambient-noise extension

A separate finite-bit Gaussian-like theorem is now drafted in
[smoothed-gaussian-cell-closure.md](../new-direction/smoothed-gaussian-cell-closure.md).
For a bounded rational polytope QP, supplied rational convexifier, and
negative inertia `k`, it samples independent original-coordinate
coefficients from one base-input-chosen finite rational law approximating
isotropic Gaussian noise. It returns an exact rational optimizer of the
perturbed QP on every draw, using a same-draw exact fallback on exceptional
events. The expected bit-work bound has form
`f(k, nu diam(X)/sigma) poly(I)` with an absolute input-length exponent;
there is no growth or uniqueness promise. This is not a Turing-model
algorithm for literal real Gaussian input and gives no guarantee about the
unperturbed QP. The root and a separate adversarial reader found no
substantive gap in the weighted count, finite sampler, or budget loop; the
written review is still pending.

The new analysis decomposes the continuous Gaussian proxy into independent
residual and negative-space components, then uses a Gaussian-weighted
lattice sum over only the projected feasible set. This removes the
`n^(O(k))` factor present in the finite uniform-grid ambient theorem. The
finite rational sampler approximates this proxy closely enough for the
finite-level event count and exact fallback probability, with its law and
support selected from the base input before the draw.

The closest established smoothed global-optimization result remains
Kelner and Nikolova's expected-polynomial algorithm for fixed-rank
quasi-concave minimization under a random rotation of the objective
subspace over an integral polytope. It is a substantial low-dimensional
smoothed-optimization antecedent, but it does not perturb only the linear
cost vector of a fixed indefinite QP and does not give the candidate's
Gaussian component decomposition or exact rational-output guarantee.
[[kelner2007-on-the-hardness-and-smoothed]] p.2-4

Burer and Ye show high-probability exactness of Shor SDP relaxations for
a class of randomly generated QCQPs. Their randomness affects the
quadratic objective and constraint data, and the theorem is about
relaxation exactness, not expected runtime for a fixed QP under a Gaussian
linear-cost perturbation. [[burer2018-exact-semidefinite-formulations-for-a]]
p.1

Lee, Tam, and Yen study how the global solution map and optimal value of
the nonconvex trust-region subproblem respond to changes in the linear
term. This is a direct sensitivity/stability neighbor, but the publisher
abstract gives no Gaussian law, expected complexity, or bit-model exact
algorithm. The sole literature-ingest agent is checking whether a lawful
full text is available. [SIAM J. Optim. 22(3):936–952 (2012),
DOI 10.1137/070710317](https://epubs.siam.org/doi/10.1137/070710317).

Classical smoothed LP work proves expected polynomial exact optimization
under Gaussian perturbations of linear-program data, and hence is a
general randomized-exactness precedent. Its problems remain linear and
convex, and its perturbation models generally randomize constraint data
as well as costs. It does not handle indefinite quadratic curvature or
treewidth-based sparse bag tables. No source in the focused searches
combined an ambient Gaussian linear-cost perturbation of a fixed
indefinite box QP with the candidate's fixed-parameter expected exact
algorithm.

## Assessment and search boundary

The prior art already contains the component methods: exact forest box-QP
DP; exact continuous tree-DP for some utility classes; interval and
quadtree discretization in continuous graphical models; treewidth-based
convex-QP approximation; semiconcave grid counts under independent linear
noise; finite-set smoothed isolation; and global optimization through
parametric piecewise-quadratic value functions. The candidate should not
claim any of these mechanisms individually as new.

The focused comparisons did not identify a source that combines a
bounded-treewidth continuous box QP with arbitrary negative inertia,
independent fixed finite rational-grid objective noise, expected
near-optimal bag-row counts, an exact every-draw rational output, and a
same-draw exact fallback. This is only a scoped search result. The
candidate's complexity is polynomial at each fixed bag size under its
stated numerical ratio, but the current bound is XP in that size, not FPT.
The finite-rational law is part of the theorem and must be stated whenever
the exact bit-complexity claim is cited.

For the Gaussian extension, distinguish the continuous proxy from the
finite rational law. The finite-bit expected-exact theorem is now present
in the draft, but its independent written review is pending. Do not state
an exact-solver guarantee for literal real Gaussian input, or a guarantee
for the unperturbed objective.

## Sources and review status

- The candidate sparse theorem and its expected-cell and closure
  arguments are recorded in
  [sparse-bag-cell-smoothed-qp.md](../new-direction/sparse-bag-cell-smoothed-qp.md).
  The root has read the proof; independent reviews and targeted exact-DP
  checks are in progress.
- The local smoothed semiconcave-cell, Pareto-count, treewidth QP, OPF,
  continuous DCOP, and convex-indicator QP packages cited above are read.
- Ding's full local source package is read and checked by the literature
  agent; the exact theorem locators above use physical PDF pagination.
- The Lee–Tam–Yen publisher abstract was examined; its full text is not
  yet verified locally.
- The rational Gaussian-like extension is recorded in
  [smoothed-gaussian-cell-closure.md](../new-direction/smoothed-gaussian-cell-closure.md).
  Its proof draft and finite sampler are complete; the written independent
  review is pending.
- No knowledge-base files were edited for this audit. No project-wide
  checks or CI inspection were run.
