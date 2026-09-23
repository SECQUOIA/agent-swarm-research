# Root source and scope audit for the frontier stages

The repository developed further while stages 1--3 were being written.
The following complete topic sources supersede the weaker initial frontier
construction for the next mathematical stages:

- `results/infinite-quadratic-aggregation-hhc.md`: three constraints in
  four variables; indispensable continuum of strict good rays; finite
  impossibility for the closed hull and for arbitrary strict original-space
  quadratics; explicit hull and finite SDP lift.
- `notes/research-20260922-gram-hyperplane.md`: the full Gram map with one
  scalar square has HHC exactly when the repetition count is at least the
  Gram dimension. Its exact image formula excludes the scalar square case
  k=r=1, although HHC still holds in that case.
- `notes/research-20260922-aggregation-accuracy.md`: dimension-independent
  two-sided Hausdorff rate, rational coefficient mesh, and exact aggregation
  for a prescribed nonzero linear objective.
- `results/four-aggregation-strict-pdlc.md`: transfer of the published
  regular closed four-bound to arbitrary proper strict PDLC hulls, sharpness
  using the credited BDS example, and oriented SOC closure.

These are inputs to independent authoring and five-reviewer stages, not
accepted manuscript results merely because other repository reviews exist.
The general Gram/infinite stage comes first, accuracy second, and PDLC third.

## Primary sources independently opened by the root, 2026-09-22

[Uhlmann, On Partial Fidelities](https://www.physik.uni-leipzig.de/~uhlmann/PDF/Uh00d.pdf):
printed pp. 408--410 explicitly state separate concavity of transition
probability, allow unnormalized positive operators, and give the product of
traces formula as equation (14) at k=0. The matrix variational identity and
concavity are established prior work. The real Gram-fiber interval and the
sharp HHC formulation still need their own complete proofs and comparison.

[Wang and Kilinc-Karzan, arXiv v2](https://arxiv.org/html/2403.04752v2),
Section 4.1: quadratic matrix programs with at least as many repeated
columns as constraints have SDP convex-hull exactness under Assumption 1.
For the present three-constraint system this supplies relevant prior theory
at repetition count at least three. Distinguish a feasible-set hull from
the source's objective epigraph by specifying a zero objective if invoking
the result. Do not claim a novel SDP convexification principle.

[Ramachandran, Shu and Wang](https://ir.cwi.nl/pub/35175/35175.pdf), Lemma 1:
the classical singular-value extremum over SO(n) includes a determinant
correction. The source attributes this lemma to Farrell and coauthors.
Our trace-range proof must handle both real orthogonal components explicitly;
the disconnectedness of O(k) cannot be ignored. Its broader rotation-image
results merit comparison before any sharp Gram-map novelty claim.

The root read all four repository mathematical developments above and found
their main arguments plausible. The prescribed fresh reviews remain required.
No source search establishes priority by failing to find an earlier theorem.

## Two proof refinements for the author to assess independently

The Gram-fiber interval proof need not cite connectedness of the orthogonal
components. In diagonal singular-value coordinates, continuously rotate
disjoint pairs of coordinate axes from angle zero to pi. For even k this
moves the trace from M to -M. For odd k>=3 leave the least singular-value
axis fixed: the endpoint trace is 2*s_min-M<=0. This supplies [0,M];
negating the factors supplies [-M,0]. Singular values equal to zero cause
no difficulty. This is a possible shorter fully explicit argument.

The quartic-boundary obstruction appears to extend to a finite conjunction
of nonstrict arbitrary quadratics describing the closed hull. On the plane
u=x*e1, v=y*e2 discard restricted polynomials identically zero. At every
boundary-arc point the remaining values are nonpositive, and at least one
is zero, since otherwise a plane neighborhood would be included in the
closed hull. No finite family of nonzero quadratics can cover the
irreducible quartic arc by its zero sets. The open proof should discard
identically zero restrictions only if the strict representation permits
them; in that case they are impossible because the planar hull is nonempty.
The author and reviewers should validate this strengthening before inclusion.

## Additional root primary-text inspection

The root retrieved Beck's published 2009 JOTA article from the link on
[the author's publication page](https://sites.google.com/site/amirbeck314/publications):
[author PDF](https://www.tau.ac.il/~becka/22.pdf). Local review copies are
`/tmp/quadratic-paper-literature/beck2009.pdf` and `.txt`. The title page
gives DOI 10.1007/s10957-009-9539-y and online publication 5 March 2009.
The root read the introduction and Theorems 2.2, 3.1, 3.3, and 3.4 with
their proofs. The real global-image theorems use at most r general QM
functions, or r+1 with positive definiteness and a dimension qualification.
The homogenization uses an r-square matrix variable. These results are
important prior image-convexity theory. The inspected statements do not
give the scalar-square Gram map's exact image on every linear hyperplane
at the sharp full-Gram threshold. No assertion of exhaustive equivalence
or priority follows from that observation.

The root also freshly extracted the local original Dey--Munoz--Serrano
PDF and read Proposition 2.8 and its proof on printed pp. 681--682.
It treats closed inequalities in two variables and all valid aggregations,
without the later homogeneous inertia restriction. Its displayed family
has leading diagonal (a-1,-a), hence two negative directions for 0<a<1.
The y=0 restriction of its three homogeneous forms has a nonconvex image:
the images at (x,t)=(1,0),(0,1) have a midpoint that would require
x^2=t^2=1/2 and xt=0. Thus that example lacks HHC. Both the broad infinite
phenomenon and the use of varying active aggregates predate this manuscript.
The contribution must be stated with the HHC/good-aggregation qualifications.
