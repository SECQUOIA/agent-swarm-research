# Priority and significance review of the five-parameter quadratic family

Date: 2026-09-25. Reviewer: `finish_family_priority`, independently of the
construction. Scope: the family and its order-five SDP lift already developed
in [the family note](three-positive-family-sdp.md), and their relation to the
specific prior results listed below. This review completes that comparison;
it does not establish publication priority through an exhaustive search.

**Verdict.** The defensible contribution is an explicit family of exposed
nonnegative quadratic rays, including a rational counterexample to a recent
disjoint-support relaxation, together with exact enforcement of a larger valid
parameter domain using one order-five PSD block and six nonnegative auxiliary
entries. The separating point also satisfies the inspected extended-triangle
SOC system. These are concrete additions relative to those relaxations. They
are not a new tractability result for three-variable BoxQP: a classical exact
SDP lift of its entire quadratic moment hull already implies every family cut.

## What the comparisons establish

For reference, the family is

\[
q_{h,d,k}=(h-d_1x-d_2y+d_3z)^2
 +2d_3kz(1-x-y)+k\bigl(2(d_1+d_2-h)+k\bigr)xy.
\]

Validity holds for arbitrary real `h` and nonnegative `d_1,d_2,d_3,k`.
The five-contact exposed-ray result requires the strict assumptions in
[the counterexample note](three-positive-disjoint-counterexample.md).
Positive simultaneous scaling of all five parameters scales the polynomial
by its square, so this parameterization includes the usual ray-scaling
redundancy. It should not be described as five independent dimensions of rays.

| Inspected source | Relevant established result | Consequence for the present claim |
|---|---|---|
| Anstreicher–Burer, Theorem 7 | Exact DNN representation of quadratic moment hulls over triangulated polytopes in dimension at most three | The exact three-cube lift already enforces this entire family. |
| Burer–Letchford, Sections 6.3–6.4 | Recursive validity test for indefinite quadratic inequalities, and a three-variable counterexample to PSD+RLT+TRI | Neither boundary reduction nor generic three-variable incompleteness of PSD+RLT+TRI is new here. |
| Lambert, Proposition 9 | General Triangle inequalities become ordinary triangle inequalities on the unit box | That named generalization does not subsume the displayed family cut. |
| Anstreicher–Puges, Section 4 | SOC strengthenings implying ETRI1, ETRI2 and ETRI3 | The rational witness proves that the present family supplies a cut absent from this stronger system. |
| Khajavirad, Section 3 | Disjoint-support moment matrices and a three-positive-loop exactness question | The checked 27-block feasible witness gives a negative answer for the inspected version. |

### The strongest exact comparator

[Anstreicher and Burer, *Computable representations for convex hulls of
low-dimensional quadratic forms*, Theorem 7](https://optimization-online.org/wp-content/uploads/2007/02/1586.pdf)
give exactness for a triangulated polytope in dimension at most three. Their
displayed cube triangulation uses six tetrahedra, hence six DNN matrices of
order four; they also mention a five-tetrahedron triangulation. The familiar
identity `CP_4=DNN_4` is the essential low-dimensional cone fact. Consequently,
the present family is already implied by their formulation. Its potential
value lies in selective enforcement of a particular useful subset of cuts.
One order-five block for one orientation is a meaningful formulation size,
but imposing up to 24 symmetry orientations can use more PSD blocks than
the exact classical formulation. There is no established total-size or
runtime advantage.

### Earlier indefinite inequalities and the named triangle generalization

[Burer and Letchford, *On nonconvex quadratic programming with box
constraints*](https://doi.org/10.1137/080729529), Section 6.3, Proposition 10,
reduce validity of an indefinite inequality to validity on box facets.
Their Section 6.4 gives explicit rational data separating the three-variable
hull from PSD+RLT+TRI. I inspected the local full paper
[PDF](extreme-prior-sources/burer-letchford-2009.pdf) and
[extracted text](extreme-prior-sources/burer-letchford-2009.txt).
The paper does not present the displayed five-contact family in the inspected
classification and example sections. This is a report about those sections,
not proof that equivalent formulas occur nowhere else.

There is also a simple distinction from that paper's explicit example. Written
as a nonnegative quadratic, its square coefficients have signs `(+ ,0,−)`.
The strict five-contact family here has three positive square coefficients.
Permutation, coordinate complementation, and positive multiplication preserve
the number and signs of nonzero square coefficients. Thus the two displayed
examples are not identical under these box symmetries. More general valid-cut
constructions or alternative parameterizations remain possible prior art.

[Lambert, *Valid inequalities and global solution algorithm for Quadratically
Constrained Quadratic Programs*, arXiv:2005.02667](https://arxiv.org/pdf/2005.02667),
Section 2, equations (8)–(19) and Proposition 9, was checked directly.
Her General Triangle inequalities use arbitrary variable bounds and reduce
to Padberg's ordinary triangle inequalities when the bounds are zero and one.
The present rational witness satisfies those ordinary inequalities as part
of a stronger system. Hence this particular named generalization does not
explain away the family counterexample. No assertion is made about every
inequality called a generalized triangle inequality in other literatures.

### The two recent systems that are strictly strengthened

[Anstreicher and Puges, *Extended Triangle Inequalities for Nonconvex
Box-Constrained Quadratic Programming*, arXiv:2501.09150v1](https://arxiv.org/html/2501.09150v1),
equations (14)–(16) and Lemmas 4–5, give the relevant SOC system. The source
uses one trilinear variable in addition to first and second moments. The
existing exact checker covers its multilinear inequalities, all switched
and permuted SOC instances, and the PSD and diagonal bounds. The same point
has family-cut value `−1/40`. This proves strict strengthening after
intersection with the family LMI. It does not prove that the family LMI alone
dominates the SOC system. The inspected arXiv HTML labels itself v1 submitted
15 January 2025 while displaying manuscript date 24 August 2026; the precise
URL and formulas, rather than an inferred chronology, identify this comparison.

[Khajavirad, *Tight semidefinite programming relaxations for sparse
box-constrained quadratic programs*, arXiv:2601.18545v2](https://arxiv.org/html/2601.18545v2),
Section 3, equation (17), is the other comparator. With three positive-loop
vertices and no other vertices it gives exactly the 27 disjoint matrices
in the checker. The independent
[counterexample review](three-positive-counterexample-review.md) matches
these matrices and the stated exactness question. This source-specific
negative answer is stronger than merely giving another PSD+RLT+TRI gap.
It does not invalidate the separate classical exact lift.

## What remains unestablished

The sources examined do not provide an identified equivalent formula for the
strict five-contact subclass or its compact family lift. This limited finding
supports describing them as candidate original results, with priority
unestablished. The algebraic proof of validity uses familiar nonnegative
polynomial ingredients. The order-four copositive decomposition and the Schur
complement are classical. Neither ingredient should be presented as new.

The exposed-ray statement gives a substantive structural property: under its
strict assumptions, a family member cannot be decomposed as a sum of
nonproportional nonnegative quadratics. It does not by itself show that the
corresponding moment inequality defines a facet. Nor does it establish that
these are all missing exposed rays, that all symmetry copies give the exact
hull, or that a useful class of larger sparse problems becomes exact.

The proposed capability is a concrete optional strengthening on a selected
variable triple, using existing quadratic moment coordinates and a small
auxiliary matrix. Solver improvements are plausible, but remain unmeasured.
Comparison with the exact triangulation formulation is necessary before a
practical advantage can be claimed. No such experiment is required to regard
the explicit gap, family validity, exposed-ray property, and exact family
enforcement as mathematical results.

## Search and verification record

The local Burer–Letchford paper and the four linked primary manuscripts were
inspected. Targeted searches included `box-constrained generalized triangle
inequalities`, `quadratic five zeros cube extreme rays`, `quadratic programming
triangle inequalities parameterized`, and the exact title of Lambert's paper.
These found the named general-triangle comparison above but did not identify
an equivalent five-contact parameterization. This is not an exhaustive
citation or priority search.

I read the two existing mathematical notes, the independent family-LMI review,
the independent disjoint-counterexample review, and the existing scripts
`verify_three_positive_family_review.py` and
`checks/three_positive_gap_certificate.py`. This source-priority review adds
no mathematical construction and changed no checker. I did not rerun checks
already reported by the independent mathematical reviewers. No project-wide
verification, CI inspection, or Lean work was performed in this review.
