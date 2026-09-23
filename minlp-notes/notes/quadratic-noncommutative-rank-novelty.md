# Novelty audit: noncommutative rank and quadratic graph precision

Date: 2026-09-05. Independent literature audit of
`results/quadratic-system-noncommutative-rank-complexity.md` and its
precursor `results/quadratic-system-covariance-lower-bounds.md`.
This note assesses attribution and overlap; it does not replace the
independent mathematical reviews.

## Assessment

No matching statement was found in the primary open literature searched:
for every fixed real quadratic vector map on a full-dimensional bounded
box, the least integer dimension of any convex lifted graph relaxation
with componentwise vertical error at most epsilon has leading coefficient
one half of the noncommutative rank of the Hessian space, and a compact
binary linear formulation attains that coefficient.

This looks materially stronger than the scalar Hessian-rank and bilinear
support-graph laws already developed locally. It identifies an invariant
of the full quadratic system, allows cancellations between monomials,
and covers arbitrary convex lifts and unbounded integer ranges. This is
an assessment of the candidate's scope, conditional on its mathematical
reviews. A negative literature search does not establish priority.

The new claim should be the **whole-formulation precision law**. Neither
noncommutative rank, operator capacity, shrunk subspaces, the integer
parity argument, nor the classical alternating-matrix example is new.
The matching upper bound uses established binary product constructions;
the proposed contribution there is selecting coordinates and precision
exponents from the Hessian space.

## Closest algebraic sources

**Fortin and Reutenauer (2004).**
*Commutative/Noncommutative Rank of Linear Matrices and Subspaces of
Matrices of Low Rank*, Séminaire Lotharingien de Combinatoire 52, B52f,
[publisher PDF](https://www.mat.univie.ac.at/~slc/wpapers/s52reut.pdf).
This is the direct source for the relationship between free-field rank
and compression by an all-zero rectangular block. The corresponding
shrunk-subspace optimization is established algebra. The paper also
compares commutative and noncommutative rank. It does not formulate a
real quadratic graph approximation problem or an integer-dimension
precision bound.

**Garg, Gurvits, Oliveira, and Wigderson (2020).**
*Operator Scaling: Theory and Applications*, Foundations of Computational
Mathematics 20, 223–290,
[author-hosted published PDF](https://www.math.ias.edu/~avi/PUBLICATIONS/GargGOW20.pdf).
Theorem 1.17 records the free-field rank/compression characterization;
Theorem 1.4 and Section 2 supply full noncommutative rank, rank
nondecrease, and positive-capacity equivalences. Theorem 1.18 gives
polynomial-time noncommutative rank computation for integer input.
Section 1.7 already displays

```
n cap(T)^(1/n) = inf tr[T(X)Y],
                det X >= 1, det Y >= 1, X,Y positive definite.
```

Thus the capacity-to-trace inequality in the candidate lower bound is
standard, even in a stronger two-matrix form. Its use with a graph-contact
covariance, followed by volume and integer-parity bounds, is the proposed
new connection. The paper also explicitly discusses the classical
three-by-three alternating pencil and its commutative/noncommutative
rank gap. Attribute capacity itself and its rank equivalence to Gurvits,
as GGOW do.

**Franks, Soma, and Goemans (2022 preprint).**
*Shrunk subspaces via operator Sinkhorn iteration*,
[arXiv:2207.08311](https://arxiv.org/abs/2207.08311).
This paper gives algorithms for finding a smallest shrunk subspace and
applications to fractional linear matroid matching and the rank-two
Brascamp–Lieb polytope. It is relevant if the candidate later claims an
efficient procedure to obtain its precision allocation. It supplies
neither a quadratic graph error law nor a mixed-integer formulation
lower bound. Existing algorithms must be distinguished from the present
existence statement with arbitrary real formulation coefficients.

**Volčič (2021).**
*Hilbert's 17th problem in free skew fields*, Forum of Mathematics,
Sigma,
[open publisher article](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/hilberts-17th-problem-in-free-skew-fields/1DC74DC3E0E011210C826FF4DCA24DE1).
The candidate uses Section 2.1 for the free-field involution, not for
approximation complexity. Hermitian principal-pivot elimination should
be presented as an algebraic lemma with its supplied proof, without
claiming a new result about Hermitian matrices.

## Operator capacity and Brascamp–Lieb are already connected

**Garg, Gurvits, Oliveira, and Wigderson (2018)**,
*Algorithmic and optimization aspects of Brascamp–Lieb inequalities,
via operator scaling*, Geometric and Functional Analysis 28, 100–145,
is explicitly cited in the 2020 primary paper as the earlier connection
between Brascamp–Lieb constants and operator capacity. The candidate
must not claim the general capacity/Brascamp–Lieb bridge as new.

**Bez, Gauvan, and Tsuji (2026 version).**
*Operator capacity, the Brascamp–Lieb inequality and geometric
programming*,
[arXiv:2508.02118v2](https://arxiv.org/html/2508.02118v2), revised
13 April 2026. The first version had the narrower title *Regularity of
the Capacity in Operator Scaling*, which still appears in search results.
The current paper relates capacity and Brascamp–Lieb constants to
geometric programming with a compact-group minimization, proves bounds
for near-minimizers and local Hölder regularity, and discusses quiver
capacity. Its statements allow arbitrary coefficients in relevant
regularity results. There is no quadratic graph approximation or
mixed-integer precision theorem in the full text inspected. This is a
useful recent source for future uniform constants or perturbation
questions, rather than a competing statement of the present result.

## Closest approximation and formulation sources

**Lubin, Vielma, and Zadik (2022).**
*Mixed-integer convex representability*, Mathematics of Operations
Research 47,
[open manuscript](https://arxiv.org/abs/1706.05135), with the full text
also in `literature/papers/lubin2022-mixed-integer-convex-representability/`.
Lemma 4.1 is the integer-parity midpoint obstruction. It already applies
to arbitrary integer ranges. Counting binary assignments alone would
miss this scope; the candidate correctly uses parity. Their exact
representability statements do not give the proposed epsilon-dependent
noncommutative-rank coefficient.

**Pottmann, Krasauskas, Hamann, Joy, and Seibold (2000).**
*On Piecewise Linear Approximation of Quadratic Functions*, Journal for
Geometry and Graphics 4, 31–53,
[publisher PDF](https://www.heldermann-verlag.de/jgg/jgg01_05/jgg0403.pdf).
Scalar quadratic approximation, including indefinite forms, midpoint
error geometry, and dimension reduction, is old. These objects differ
from a simultaneous quadratic graph represented by an arbitrary convex
lift with integer coordinates. The scalar law's local investigation
contains the more detailed comparison.

**Beach and collaborators, discretization Parts I and II.**
The earlier local graph novelty audit records these sources in detail;
Part II is [arXiv:2302.01164](https://arxiv.org/abs/2302.01164).
Shared binary encodings, exact products of binaries and bounded
continuous variables, residual McCormick envelopes, and square
relaxations are established construction ingredients. Existing
partition-volume results and encoding counts should not be confused
with a universal lower bound on the whole quadratic system after all
possible coordinate changes and convex lifts.

**Choi, Fattahi, Gómez, Han, and Lozano (2026).**
*Convexification of Mixed-Integer Quadratic Optimization via Decision
Diagrams*, posted 24 August 2026,
[arXiv:2608.22815v1](https://arxiv.org/html/2608.22815v1).
The recent paper treats convex quadratic epigraphs with indicator
variables. Its low-rank conditions concern the size of decision diagrams
and convex-hull descriptions; its approximation results concern diagram
size and optimization gaps. This differs from containing an entire
quadratic vector graph while limiting every admitted output's error.
No noncommutative-rank result appears in the full text inspected.

An additional search of anisotropic mesh literature found established
maximal-ellipsoid and derivative-tensor constructions, including
Weiming Cao's *An Interpolation Error Estimate on Anisotropic Meshes in
R^n and Optimal Metrics for Mesh Refinement*,
[SIAM primary abstract](https://epubs.siam.org/doi/10.1137/060667992).
Those geometric ideas are relevant background. The inspected abstract
does not claim the integer-dimension invariant; a broader historical
survey of simultaneous vector interpolation remains worthwhile.

## Precise claim boundaries

1. Define the invariant as rank of the symmetric Hessian pencil over the
   complex free skew field. Ordinary optimization variables remain real
   and commuting. Other papers use “rank of noncommutative quadratic
   forms” for different algebras; that terminology is not interchangeable.
2. State full-dimensional box, full graph containment, and uniform
   componentwise vertical error. Quadratic images, zero sets, epigraphs,
   and objective-value approximation are different problems.
3. State fixed-system asymptotics with data-dependent additive constants.
   A compact formulation with real coefficients does not by itself give
   polynomial-time rational preprocessing or a uniform bit bound.
4. The cross product uses a classical alternating matrix space. The new
   candidate consequence is coefficient three for its simultaneous
   six-variable graph despite the scalarized rank bound giving two.
5. Keep a self-contained proof of real shrunk-space selection and the
   symmetry-based precision allocation. Independent left/right matrix
   changes from rank theory do not automatically constitute permissible
   quadratic coordinate changes.

## Search record and remaining uncertainty

Searches combined noncommutative rank, operator capacity, shrunk subspace,
quadratic maps/forms/systems, approximation, convex covers, integer
dimension, Brascamp–Lieb, entropy, and anisotropic mesh metrics. Literal
queries for noncommutative rank with mixed-integer formulations or
covering numbers returned no direct matching research statement.
Primary full texts checked include Fortin–Reutenauer, GGOW2020,
Bez–Gauvan–Tsuji2026, and Choi et al.2026. Earlier source audits cover
Lubin's midpoint lemma and Beach's formulations. Downloaded scratch
texts are under `/tmp/minlp-ncrank-novelty/`; this note retains the
durable conclusions and source links.

The result is a credible candidate for a new connection between
noncommutative algebra and mixed-integer approximation complexity.
Publication priority remains unestablished, especially against older
vector-valued approximation geometry and unpublished work.
