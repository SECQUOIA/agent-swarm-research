# Implicit polynomial-vector overlays: focused source assessment

Date: 2026-09-05. Bounded primary-source assessment by
`joint_flow_novelty`, coordinated with `quadratic_weighted_precision` and
`binary_formulation_review`. Both complete candidate notes were read;
independent mathematical audits are separate.

The candidates construct rational MILPs for the whole graph of a densely
encoded polynomial vector of one scalar input, with rational componentwise
absolute tolerances. The bounds are

```
p_out <= p_conv + 11 + ceil(log2 m)           (convex components),
p_out <= p_conv + 12 + ceil(log2 sum_j D_j)   (arbitrary components).
```

Here `p_conv` minimizes unrestricted integer dimension over arbitrary convex
lifts of the same graph tube, without a continuous-size restriction. In the
second expression the sum concerns nonlinear outputs; all-affine vectors
need no integer variables. Construction time and full rational encoding
length are polynomial in the dense input and tolerance encoding.

No matching combined guarantee was found in the sources checked. However,
there is an exact finite vector-overlay predecessor, and selection from
implicitly accessed sorted lists has direct algorithmic precedents. Those
facts substantially narrow the standalone novelty of the overlay. The
defensible contribution is the uniform compact construction and its
whole-formulation integer-count comparison, built on the scalar theorems.

## Direct prior for merging several output partitions

Bochuan Lyu, Illya V. Hicks, and Joey Huchette,
*Building Formulations for Piecewise Linear Relaxations of Nonlinear
Functions*, [primary preprint](https://arxiv.org/pdf/2304.14542), Section 3,
Proposition 1 and Equation (4), PDF pp.7–8, explicitly takes the union of
breakpoints of several univariate PWL functions with the same input. It
uses one SOS2 weight vector for all outputs. The following paragraph states
that a logarithmic SOS2 encoding uses `ceil(log2 d)` binary variables,
instead of the sum of the separate logarithmic counts, where `d` is the
number of merged intervals. Appendix B gives a merged incremental
formulation. Section 3 and the relevant definitions were read in full.

Comparison: neither common refinement, sharing one interval selection, nor
the resulting logarithm-of-a-sum count should be presented as new. Their
Equation (4) lists the merged breakpoints and has one continuous weight for
each. The present candidate avoids listing a potentially exponential number
of knots, supplies certified errors for the original polynomial graph, and
compares the count with all convex integer lifts. Those additional guarantees
were not found in this predecessor. Its later stronger relaxation results
also underline that merely using few binaries does not establish ideality.

## Implicit order statistics are established

Haim Kaplan, Laszlo Kozma, Or Zamir, and Uri Zwick,
*Selection from heaps, row-sorted matrices and X+Y using soft heaps*,
[primary preprint](https://arxiv.org/pdf/1802.07041), Section 4.3,
Theorem 4.3, PDF pp.13–14, gives selection from sorted rows of lengths
`n_i` in `O(m+sum_i log n_i)` operations. Section 4.2, PDF pp.12–13,
explicitly represents shifted and strided matrices implicitly by indices;
selection is represented by counts of the selected prefix in each row.
The introduction credits Frederickson and Johnson for earlier sorted-list
selection results. These sections were read. Frederickson–Johnson's 1982
[publisher abstract](https://www.sciencedirect.com/science/article/pii/0022000082900484)
also confirms sublinear selection and ranking for sorted-column matrices;
its original full proof was not read in this audit.

Comparison: random-access order statistics without listing every entry are
not new. The candidate uses a simpler rational-grid method: binary-search
each array for a rank, then binary-search the common numerator universe.
That method is sufficient because both index lengths and the common
denominator have polynomial bit length. Retaining duplicate knots removes
the need for distinct-value enumeration. These are useful implementation
details, not a new selection complexity theorem.

The canonical approximate-quantile evaluator needs a further property that
generic approximate inverses do not automatically have: its result must be
ordered in the target. The candidate proves this from a common deterministic
binary search tree, fixed node accuracy, and ordered branches. This is a
short algorithm-specific observation; this search did not find an exact
reference, but absence of a reference does not justify promoting it as a
major numerical result. Exact ordering here is of rational returned knots,
not exact comparison of curvature integrals.

## Inherited approximation and compiler contributions

The [scalar hybrid assessment](compiled-convex-polynomial-hybrid-novelty.md)
already compares LinA's greedy corridor segmentation, continuous-function
fitting, optimal scalar interpolation, and PSE error-band formulations. Its
distinction between explicit per-segment work and polynomial-bit indexed
construction carries over directly. The vector theorem should cite those
antecedents through its scalar dependency rather than claim a new general
segmentation method.

The [compiler assessment](compiled-rational-knot-formulations-novelty.md)
documents Avis–Bremner–Tiwary–Watanabe's continuous Boolean gate extensions,
Sparktope's algorithm compilation, Adams–Henry's logarithmic discrete
function/product encodings, and Filos-Ratsikas and coauthors' succinct
circuit-specified interpolation. That earlier primary-source reading was
reused here; these full papers were not reread in this focused search.
No novelty is claimed for keeping the computed Boolean wires continuous
once the input index is integral, or for decoding several output values.

The analytic dependencies remain essential: polynomial-time certified
integration, polynomial root processing, fixed rational accuracy, and dense
endpoint evaluation must all remain uniform in the instance. The merge
does not repair a missing guarantee in any scalar oracle. For the general
polynomial extension, recording convex/concave/bracket metadata and choosing
the appropriate directed graph band is a useful checked adaptation of the
same construction, not a separate general-purpose oracle.

## Scope and recommended positioning

The [convex-vector construction](compiled-convex-vector-knot-overlay.md)
and [general polynomial extension](compiled-polynomial-vector-overlay-precision.md)
support a compact graph-formulation theorem. They do not compute `p_conv`,
the optimal partition, or a minimum-size MILP. They do not establish a
polynomial-time solver for the resulting MINLP, a strong LP relaxation,
sparse binary-degree complexity, or general coupled error bodies.

The logarithmic output penalty is an upper bound, not a proved necessary
gap relative to `p_conv`. The scalar degree obstruction supports logarithmic
degree dependence for the arbitrary-polynomial extension, but does not
prove necessity of every term in the vector bound. Distinguish these
constructive rational results from the earlier finite real-coefficient
vector comparison, which permits unrestricted representation size.

A suitable claim is: “Combining known shared-breakpoint formulations,
implicit sorted selection, and circuit encodings with certified scalar
approximation yields a polynomial-size rational formulation for dense
polynomial-vector graphs. Its integer dimension is within the stated
logarithmic overhead of the minimum over all convex integer lifts. No
matching combined guarantee was located in the primary sources checked.”

Fresh searches covered simultaneous PWL outputs, implicit sorted selection,
succinct graph approximation, and minimum integer dimension. A 2026 primary
[preprint on binary relations in PWL approximations](https://optimization-online.org/wp-content/uploads/2026/02/MPIP_oo_manuscript.pdf)
was screened through its abstract and introduction: it develops cutting
planes between interval-selection groups, a different contribution. This
bounded review does not establish exhaustive priority or replace the two
independent mathematical audits.
