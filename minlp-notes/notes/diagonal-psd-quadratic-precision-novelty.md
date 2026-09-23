# Novelty audit: finite precision for nonnegative diagonal quadratics

Date: 2026-09-05. Bounded primary-source audit of
[the candidate](diagonal-psd-quadratic-linear-dimension-precision.md).
This note does not replace its independent mathematical reviews.

No matching published theorem was found characterizing the minimum
integer dimension of a simultaneous diagonal PSD quadratic graph,
at prescribed unequal errors, within an additive `O(r)` term uniform
in the data and number of outputs. The potentially new contribution
is that characterization against **all convex lifted formulations**,
including unbounded general integer coordinates, together with a
polynomial-bit rational MILP construction within `5r+1` of that optimum.
Here `r` counts active original box coordinates, not the rank after an
arbitrary rotation.

The allocation problem, coordinate interpolation, shared encodings,
logarithmic binary counts, midpoint obstruction, and standard covariance
inequalities are established tools. The result should be presented as a
sharper finite formulation theorem obtained by connecting those tools.

## Closest construction results

**Beach, Hildebrand, and Huchette, compact quadratic formulations.**
Their univariate construction uses `L` binaries and `O(L)` rows and
continuous variables to obtain error `O(4^-L)` for a square. The paper
combines square approximations with diagonal perturbations and explicitly
extends the approach to quadratic constraints. It also compares with
existing logarithmic formulations and proves optimality of uniform
breakpoints for the area of a specified univariate piecewise McCormick
relaxation. These are direct antecedents of the candidate's upper-bound
gadget, not a finite lower bound on arbitrary lifted formulations of
simultaneous outputs.
[Primary preprint](https://arxiv.org/abs/2011.08823), Sections 2–3 and
Proposition 5; supplied published full text in
`literature/papers/beach2022-compact-mixed-integer-programming-formulations/`.

**Huchette–Vielma and Lyu–Hicks–Huchette.** Logarithmic formulations of
piecewise linear functions and relaxations are well developed. In
particular, Lyu et al. formulate upper and lower approximations together
and discuss several functions sharing the same input. Thus neither
sharing coordinate encodings across outputs nor representing both sides
of a graph tube is new. Their comparison is between formulations of
specified piecewise linear disjunctions; the candidate permits every
valid convex integer lift at the prescribed error, including choices
of approximation geometry different from that disjunction.
[Huchette–Vielma primary preprint](https://optimization-online.org/wp-content/uploads/2017/07/6148.pdf);
[Lyu–Hicks–Huchette (2023)](https://arxiv.org/html/2304.14542), Sections
2–3 and 5. Their introduction also states logarithmic lower bounds for
specified disjunctive structures; that prior statement should not be
confused with a lower bound uniform over all graph approximations.

**Padberg (2000)** is an earlier explicit source on mixed zero-one
representations of piecewise linear approximations of separable
functions. Its working-paper abstract describes comparisons of LP
relaxations and a third formulation. Only the primary working-paper
record and abstract were checked in this audit, so no claim about a
missing theorem deep in that paper is based on full-text inspection.
[Author working-paper record, written 1998](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1290963).

## The trace allocation is classical optimization

The benchmark maximizes `sum_i log p_i` under positive linear resource
constraints and coordinate caps. This belongs to classical logarithmic
utility allocation, often called proportional fairness. Kelly,
Maulloo, and Tan formulate weighted logarithmic rate allocation under
linear resource capacities and develop primal and dual algorithms.
[Primary 1998 paper](https://web.stanford.edu/class/cs244/papers/ShadowPricesFairnessStability.pdf),
Section 2. General nonnegative coefficients and explicit caps make the
candidate a routine convex allocation problem; they are not a new class
of optimization algorithms.

Hessian-based anisotropic interpolation and determinant or volume
optimization are also established. Cao (2007) selects ellipsoidal
metrics through determinant optimization, while Chen–Sun–Xu (2007)
study nearly optimal anisotropic interpolation meshes. Multiple-output
metric intersection appears in Frey–Alauzet's CFD work. Exact sources
and checked scopes are recorded in the
[earlier algorithm audit](quadratic-weighted-precision-algorithm-novelty.md).
These results compare approximation meshes and interpolation error,
not integer dimension over arbitrary convex lifts.

The distinctive bridge in the candidate is positivity: each parity
support yields simultaneous **trace** constraints on the diagonal
covariances. Hadamard's inequality then connects its volume to the
same product allocation that governs the shared coordinate grid. This
removes the `r log r` loss of the more general covariance benchmark.
The resulting additive `O(r)` estimate is materially stronger than a
fixed-dimension asymptotic law with an unspecified data-dependent
constant. It is also stronger than an optimality statement restricted
to Cartesian grids or fixed piecewise linear approximations.

The foundational integer parity/midpoint mechanism must remain credited
to Lubin, Zadik, and Vielma's mixed-integer convex representability work.
[Primary preprint](https://arxiv.org/abs/1706.05135), midpoint lemma;
the repository has already audited its exact use. The new assertion is
quantitative and error-dependent, not a new representability framework.

## Nearby positive separable polynomial extension

No uniform whole-formulation integer-dimension characterization for
positive separable polynomials was found in the targeted searches.
This was a secondary search, not a complete audit of the extension.
Two nearby sources require careful distinction:

- Beach et al.'s appendix investigates sparse triangular approximations
  to cubic functions. For the particular basis and experiments described
  there, cubic approximation has much slower observed decay than the
  quadratic construction. This is neither a general impossibility
  theorem for compact polynomial MILPs nor an integer-dimension lower
  bound. A construction using binary arithmetic or another lifted
  representation does not contradict the observation.
- Grimstad and Knudsen (2020) study piecewise polynomial representations
  using monomial, Bernstein, and spline bases and derive disjunctive
  MINLP formulations and bound-tightening methods. The inspected
  statements concern representing given piecewise polynomials; they
  do not supply a near-minimum-integer MILP graph approximation at a
  uniform tolerance.
  [Primary article](https://link.springer.com/article/10.1007/s10898-020-00881-4),
  Sections 4–5.

The distinction between original box axes and a rotated simultaneous
eigenbasis is essential. Commuting PSD Hessians alone do not make a
Cartesian allocation proof apply to the transformed domain. For
polynomials, any degree dependence, coefficient-sign conditions, and
domain restrictions must likewise remain explicit.

## Recommended claim and search limits

After proof acceptance, describe the result as a finite, data-uniform
`O(r)` characterization and rational construction for nonnegative
diagonal quadratic systems on their original box. Avoid claims to
introduce logarithmic square approximations, optimal resource
allocation, output sharing, or the leading `r/2` small-error exponent
in isolation.

Searches combined separable/diagonal quadratic, polynomial,
interpolation, logarithmic formulation, minimum integer dimension,
convex covers, and resource allocation. Primary formulation papers,
the available local literature, and the specific sources above were
checked. No direct match was found, but this remains a bounded novelty
assessment rather than certification of priority.
