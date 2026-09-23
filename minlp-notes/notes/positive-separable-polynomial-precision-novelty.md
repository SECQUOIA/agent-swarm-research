# Source audit: positive separable polynomial integer precision

Date: 2026-09-05. Focused, bounded novelty audit of
[the candidate](positive-separable-polynomial-integer-precision.md).
Mathematical review is separate.

No matching primary statement was found for the candidate's finite
integer-dimension characterization, uniform in nonnegative coefficients,
separate output tolerances, and output count, with additive error
`O(r+sum_i log D_i)`. Its rational construction within
`2 sum_i log2 D_i+4r+1` of the optimum over arbitrary convex integer
lifts is the strongest proposed contribution. Fixed degree gives
`O(r)` overhead. The model-size claim is polynomial for **dense**
polynomial input, not for arbitrary binary-encoded sparse exponents.

The following prior work substantially overlaps with the upper-bound
methods. A claim to introduce polynomial MILP approximation, radix
disaggregation, or reused variable encodings would be too broad.

## Polynomial disaggregation is established prior art

**Teles, Castro, and Matos (2013), Univariate parameterization for global
optimization of mixed-integer polynomial problems**, EJOR 229(3),
613–625, is the closest additional source beyond the quadratic audit.
Its primary publisher text describes radix expansions, binary digit
variables, continuous residuals, power transformations, and MILP
approximations for general nonnegative-domain polynomial programs.
The residual envelopes can be refined arbitrarily; Section 6 establishes
limiting convergence. It also develops a smaller formulation than its
earlier multiparametric disaggregation approach.
[Primary publisher record and accessible section excerpts](https://www.sciencedirect.com/science/article/abs/pii/S0377221713002750),
[DOI](https://doi.org/10.1016/j.ejor.2013.03.042).
The abstract, introduction, and exposed section excerpts were inspected;
the complete paywalled article was not obtained. No exact finite
minimum-integer comparison is asserted in the inspected statements.

**Teles, Castro, and Matos (2013), Multi-parametric disaggregation
technique for global optimization of polynomial programming problems**,
JGO 55(2), 227–251, is the earlier polynomial construction. The authors'
institutional record describes a power-based, termwise disaggregation
into discrete and continuous variables, producing MILP approximations
at an arbitrarily chosen precision. It also mentions rational-exponent
signomial transformations. Thus even the general connection between
power transformations and MILP polynomial approximation is prior art.
[Primary institutional record](https://repositorio.lneg.pt/entities/publication/9668a01e-94fa-4147-8941-8ba8da14370a).
The record and abstract, rather than the complete proof, were checked.

**Kolodziej, Castro, and Grossmann (2013)** derive bilinear
multiparametric disaggregation using generalized disjunctive programming
and exact linearization, with rigorous lower bounds and algorithms.
Their Section 2 explicitly starts from one discretized factor in each
bilinear product. This is direct prior methodology for the candidate's
binary-times-bounded-continuous products and prefix recurrences.
[Author-hosted primary manuscript](https://egon.cheme.cmu.edu/Papers/JGlobalOptMDTKolodziejCastroGrossmann.pdf),
Sections 1–3, *Global optimization of bilinear programs with a
multiparametric disaggregation technique*.

The candidate's explicit `O(D_i L_i)` recurrence and first-order Taylor
band are useful ways to make its rational upper bound and size
transparent. They should be treated as an application of established
linearization and approximation tools unless a separate detailed
comparison establishes priority for that exact recurrence. The present
audit does not establish such standalone priority.

## Other nearby formulation and approximation results

**Beach, Hildebrand, and Huchette** give logarithmic-size square
approximations and discuss extending sparse triangular constructions to
cubic functions. Their cubic experiments concern a particular triangular
basis; they are not an impossibility theorem for polynomial MILPs with
other continuous lifts. Prefix-power recurrences therefore do not
contradict that observation.
[Primary preprint](https://arxiv.org/abs/2011.08823), quadratic
construction and appendix; see the detailed
[diagonal audit](diagonal-psd-quadratic-precision-novelty.md).

**Lyu, Hicks, and Huchette (2023), Proposition 3.1**, explicitly reuse
one SOS2 representation across several piecewise linear functions of
the same input. Their later sections represent lower and upper bounds
together. Output sharing and simultaneous graph bounds are therefore
established methods.
[Primary paper](https://arxiv.org/html/2304.14542), Sections 3 and 5.

**Grimstad and Knudsen (2020)** construct mathematical programming
formulations of piecewise polynomials using monomial, Bernstein, and
spline bases, including disjunctive MINLP formulations. That is a
representation problem for specified piecewise polynomial functions,
not a uniform approximation law minimizing integer dimension over all
convex lifts.
[Primary article](https://link.springer.com/article/10.1007/s10898-020-00881-4),
Sections 4–5.

**Bienstock and Muñoz** give compact LP approximations for polynomial
optimization with bounded constraint-intersection treewidth. Theorem 4
of the inspected preprint has size
`O((2*pi/epsilon)^(omega+1) n log(pi/epsilon))` and bounds feasibility
and objective tolerances. This is a strong prior polynomial
approximation-formulation theorem, but it does not say that every
projected point lies near the original graph, or compare integer count
with an optimal convex integer lift. An LP optimization relaxation and
a graph outer approximation with uniform vertical error have different
requirements.
[Primary preprint](https://arxiv.org/pdf/1501.00288), version 15,
Theorem 4 and its tolerance definitions.

## Lower-bound contribution and necessary qualifications

The scalar inequality in the candidate is an elementary consequence of
convexity of a power function followed by a Lipschitz estimate. It need
not be presented as a new inequality. Jensen-gap refinements and
power-mean estimates have a substantial existing literature; the
candidate provides its own short proof and does not need a claim of
priority for this scalar step.

The potentially new step is using that inequality to send every exact
graph parity support through the coordinate homeomorphism
`t_i=x_i^(D_i/2)`. The transformed supports still cover a cube, while
their pairwise differences satisfy simultaneous positive diagonal
quadratic bounds. Their volumes are measured in the transformed cube,
so volume preservation is neither claimed nor needed. Combining this
with the trace-allocation covariance argument yields the finite lower
bound. The construction stays in the original rational coordinates;
it does not introduce irrational inverse-power grid points.

Credit the foundational parity/midpoint mechanism to **Lubin, Zadik,
and Vielma**, *Mixed-Integer Convex Representability*.
[Primary preprint](https://arxiv.org/abs/1706.05135), midpoint lemma.
Classical covariance-volume and Hadamard inequalities and the scalar
logarithmic allocation algorithm are also not new. The novelty rests
on the resulting quantitative comparison class and its uniform
dependence on coefficients, errors, active dimension, and degree.

The theorem is narrower than all convex separable polynomials:
nonnegative nonlinear monomial coefficients on a nonnegative box are
explicit assumptions. It does not cover signed cancellation,
nonseparable interactions, arbitrary coordinate changes, or compact
circuit representations of enormous degree. Nor is a near-minimal
integer formulation automatically a polynomial-time optimization
algorithm for problems using that formulation.

## Assessment and search limits

Recommended wording after independent proof acceptance:

> Positive separable polynomial graphs admit a finite allocation law
> for minimum integer dimension, accurate within
> `O(r+sum_i log D_i)`, and a compact rational MILP construction with
> the same additive guarantee against arbitrary convex integer lifts.

Follow this statement with the dense-input and nonnegative-coefficient
conditions. Attribute the upper construction to the established
radix-disaggregation, binary product, sharing, and Taylor tools above.

Searches combined polynomial/separable polynomial, binary expansion,
univariate parameterization, multiparametric disaggregation, logarithmic
MILP size, minimum integer dimension, Jensen gaps, and power
transformations. No matching whole-formulation theorem was found.
Full-text access was incomplete for the closest 2013 polynomial
disaggregation papers, which limits the strength of any claim that an
individual upper-bound identity has not appeared before. It does not
justify overlooking those papers in the result's attribution.
