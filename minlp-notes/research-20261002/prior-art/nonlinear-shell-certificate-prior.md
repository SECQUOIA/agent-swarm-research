# Prior-art audit: sparse shell certificates for polynomial mixed boxes

Date: 2026-10-02. This is a focused comparison of the proposed-point
certificate in [`nonlinear-shell-certificate.md`](../new-direction/nonlinear-shell-certificate.md).
The main proof has passed full review after fixes; the exact arithmetic
checker is still pending. The comparisons below describe the current
statement. No priority claim is made.

The candidate concerns an explicit rational polynomial objective of fixed
degree on a bounded mixed product box, a supplied rational feasible point,
and a supplied tree decomposition containing every factor scope. It verifies
a coordinatewise upper-curvature bound on the full continuous box hull. If
the point has positive global quadratic growth `g` and the verified bound is
`L`, the claimed search and independently checkable certificate cost is
`f_d(p, max{1,L/g}) poly(I)`, with an absolute input exponent for each fixed
degree bound. Growth is not supplied: acceptance is sound without it, while
termination is claimed under it. The proposed mechanism is a sequence of
physical-distance shells, mean-preserving coordinate rounding with a
variance correction, and a local Taylor quadratic on the innermost slice
where lattice variables are fixed.

## Closest established methods

**Sparse moment/SOS hierarchies.** Lasserre’s sparse hierarchy assumes that
the objective and constraints split over local variable sets satisfying the
running-intersection property. Theorem 3.6 proves convergence to the global
minimum; Corollary 3.9 gives a sparse Putinar-style representation for strict
positivity. A moment block on a local set of `p` variables at order `r` has
dimension `binom(p+r,p)`: for fixed `p` this is polynomial in `r`, while
increasing local-set size raises the block size sharply. Value convergence
does not provide a uniform finite order or conditioning bound for the
candidate’s explicit grid tables in terms of `L/g`; Theorem 3.7’s finite
extraction instead requires flat-rank conditions. See [Lasserre (2006),
Theorems 3.6–3.7 and Corollary 3.9](https://doi.org/10.1137/05064504X),
especially pp. 6–12 and 15–16. The local package is
[`lasserre2006…/paper.md`](../../literature/papers/lasserre2006-convergent-sdprelaxations-in-polynomial-optimization/paper.md).

Nie gives an exact finite-convergence theorem for the dense Lasserre
hierarchy: under archimedeanness and CQC, strict complementarity, and second
order sufficiency at every global minimizer, some finite order attains the
optimum (Theorem 1.1). His genericity theorem identifies a Zariski-open regime
for those regularity conditions when archimedeanness also holds. The paper
does not give a uniform relaxation-order or bit-complexity bound, and the
result concerns continuous semialgebraic optimization rather than a mixed
box tree DP. This is a stronger exactness precedent than mere asymptotic SOS
convergence, but it does not imply the candidate’s stated fixed-parameter
certificate size. See [Nie (2013), Theorems 1.1–1.2](https://doi.org/10.1007/s10107-013-0680-x),
pp. 2–3 and 10–16; [open arXiv version](https://arxiv.org/abs/1206.0319).

Baldi and Mourrain provide effective Putinar degree bounds and a polynomial
convergence rate for the SOS hierarchy. Their bound depends on the target’s
strict-positivity margin and a Łojasiewicz exponent; a constraint qualification
can set the exponent to one, though the associated constant is not explicit.
The candidate instead has a nonnegative objective gap vanishing at the
proposed point and uses a local core argument. The Putinar bound is a useful
quantitative positivity baseline, but does not itself yield a sparse mixed-box
certificate with cost controlled by `L/g`. See [Baldi and Mourrain
(2023), Theorems 1.7, 2.11 and 4.3](https://doi.org/10.1007/s10107-022-01877-6),
pp. 1–4, 7–12 and 19–20; [arXiv version](https://arxiv.org/abs/2111.11258).

**Finite grids and width-based approximation.** Lasserre’s grid theorem gives
an exact finite-degree moment/SOS representation for polynomials nonnegative
on a finite Cartesian grid, with degree determined by the grid cardinalities
(Theorem 3.2). This is direct precedent for exact optimization after
discretization, but it covers the selected finite grid only; it does not
bound the continuum between grid labels or provide the shell correction.
See [Lasserre (2002), Theorem 3.2](https://doi.org/10.1090/S0002-9947-01-02898-7),
pp. 5–10.

Bienstock and Muñoz give LP approximations for bounded mixed-integer
polynomial optimization using constraint-intersection treewidth. Their
general size bound is `O((2π/ε)^(ω+1) n log(π/ε))`, with scaled feasibility
and objective errors; their binary subproblem has an exact small formulation.
This is a close structural approximation baseline, but its tolerance cost is
polynomial in `1/ε` and depends on scaling. It does not provide the candidate’s
growth-conditioned direct proof of a supplied point’s exact optimality.
See [Bienstock and Muñoz (2018), Theorems 4 and 7 and Corollary 8](https://doi.org/10.1137/15M1054079),
pp. 1–5 and 10–17; [arXiv version](https://arxiv.org/abs/1501.00288).

**Polynomial branch-and-bound and Bernstein certificates.** Buchheim and
D’Ambrosio construct monomial-wise optimal separable underestimators for
box-constrained mixed-integer polynomial optimization and use them inside
PolyOpt branch-and-bound. Their work is a direct mixed-polynomial solver
precedent, but the underestimators do not give a width- and `L/g`-controlled
certificate-size theorem. See [Buchheim and D’Ambrosio (2017),
Theorems 3–6 and §5](https://doi.org/10.1007/s10898-016-0443-3), pp. 3–16.

Leroy’s open 2009 manuscript gives explicit Bernstein degree-elevation and
subdivision certificates for strict positivity on simplices (Theorems 5.1,
5.7 and Algorithm 5.9). The degree depends on the simplex dimension, positive
minimum, and initial Bernstein coefficient second differences. This does
not directly handle a gap polynomial that is zero at the candidate point;
localizing the zero or separating an inner region is a distinct step. The
manuscript also has no supplied tree-decomposition parameter. See [Leroy
(2009), HAL hal-00589945](https://hal.science/hal-00589945), printed pp. 28–30.
The exact PDF inspected for these locators is
`/tmp/leroy2009-bernstein.pdf`; it is a distinct work from Boudaoud, Caruso,
and Roy’s 2008 Bernstein paper.

Ahmadi, Dash, Hua, and Stellato develop disjunctive SOS certificates and
simplicial spatial branch-and-bound for polynomial minimization and
copositivity. Their sphere hierarchy has an `O(1/m)` lower-bound rate, and
the SBB algorithm terminates at every positive tolerance. Their completeness
results focus on positive definite forms or strictly copositive matrices;
the paper leaves nonnegative forms with zeros as an open issue. It therefore
provides a strong spatial-certificate baseline but no finite tree-size bound
conditioned on pointwise quadratic growth or sparse factor width. See
[Ahmadi et al. (2026), Theorems 7–8 and 11, Algorithm 1](https://arxiv.org/abs/2605.28674),
pp. 17–19 and 24–34.

Mai, Magron, Lasserre, and Toh give convergent Pólya LP and factor-width SOS
hierarchies for polynomial optimization on the nonnegative orthant. For any
fixed factor-width cap, the largest SDP block is bounded independently of
hierarchy order, with an explicit convergence rate under nonempty-interior
assumptions. This offers a useful sparse hierarchy comparison, but its
approximation order remains polynomial in inverse tolerance and it does not
give a mixed-lattice candidate certificate. See [Mai et al. (2026),
Theorem 4](https://doi.org/10.1007/s10589-026-00782-4), pp. 3–11; [arXiv
version](https://arxiv.org/abs/2209.06175).

## Comparison boundary

The closest existing ingredients are standard: sparse tree DP on a supplied
decomposition; exact optimization on a finite grid; semiconcavity/chord bounds;
Taylor bounds near a candidate; and SOS or spatial branch-and-bound global
certificates. The candidate’s specific combination appears to be the
physical mixed-distance shells, the diagonal-variance correction for an
arbitrary fixed-degree polynomial, and a Taylor-certified inner core. Its
claimed result is more focused than an optimizer: it verifies a supplied
rational candidate, with a complexity guarantee under positive quadratic
growth. Existing finite-convergence and Bernstein results are not equivalent
complexity theorems, and this comparison does not establish novelty.

For a safe final claim, retain the derivation’s explicit model restrictions:
fixed degree, explicit rational monomial lists, product-box feasibility,
upper curvature verified on the full continuous box hull, rational candidate,
and a supplied decomposition containing every factor scope. In particular,
do not generalize the bit bound to binary-encoded exponents or arbitrary
arithmetic circuits: the derivation itself gives examples where exact table
values have exponentially many bits. The claim is candidate verification,
not finding an unknown optimum, handling arbitrary coupled constraints, or
certifying zero-growth unique minima such as `x^4`.

The related pure-integer exact-discovery extension is still in development.
If it becomes part of the claimed theorem, extend this comparison to general
integer polynomial optimization and finite-grid exactness before making any
scope statement about that extension.

No missing primary source was identified in this focused pass; the cited
primary texts are already available in the local literature collection or,
for Leroy, at the open HAL manuscript URL above. No knowledge-base files were
edited.
