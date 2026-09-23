# Stage 5 primary-source and novelty audit

Date: 2026-09-22. This stage concerns finite good-aggregation approximation
of the specific HHC example and exactness for one prescribed objective.
It does not make a new general approximation or duality claim.

## Sources actually inspected

- Local Bronshteyn–Ivanov, *The approximation of convex sets by polyhedra*,
  Siberian Mathematical Journal 16(5), 852–853 (1975),
  DOI [10.1007/BF00967115](https://doi.org/10.1007/BF00967115).
  Read `literature/papers/bronshteyn1975-the-approximation-of-convex-sets/paper.md`
  and its two-page primary full-text extraction, including the theorem,
  proof, and final lower-bound remark. The local original is a user-supplied
  translated PDF. The theorem concerns convex subsets of the unit ball
  in dimension greater than one and approximation by the convex hull of
  finitely many points. Its classical dimension-dependent exponent supplies
  context, not the present good-quadratic-cut theorem. No local managed
  literature files were changed.

- Sunil Arya, Guilherme D. da Fonseca, and David M. Mount,
  [*Optimal Area-Sensitive Bounds for Polytope Approximation*, arXiv:2306.15648v2](https://arxiv.org/html/2306.15648v2),
  dated December 16, 2025. Read the introduction, Section 1.1, and
  Theorems 1–2. Their original results concern linear-halfspace/convex-function
  approximation; their introduction compares the classical facet/vertex
  bounds of Dudley and Bronshteyn–Ivanov. The arXiv version is explicit
  because it is the source actually inspected. No numbered theorem from
  it is used as a premise of the manuscript's approximation proof.

- Günter Rote, [*The convergence rate of the Sandwich algorithm for
  approximating convex functions*](https://page.mi.fu-berlin.de/rote/Papers/abstract/The%2Bconvergence%2Brate%2Bof%2Bthe%2BSandwich%2Balgorithm%2Bfor%2Bapproximating%2Bconvex%2Bfunctions.html),
  Computing 48 (1992), 337–361, DOI
  [10.1007/BF02238642](https://doi.org/10.1007/BF02238642).
  The coordinator identified this closer antecedent, and the author
  independently read the author-hosted abstract and linked 22-page
  [primary report PDF](https://page.mi.fu-berlin.de/rote/Papers/pdf/The%2Bconvergence%2Brate%2Bof%2Bthe%2BSandwich%2Balgorithm%2Bfor%2Bapproximating%2Bconvex%2Bfunctions.pdf).
  Its title page identifies Report 118, version 2b, and says a slightly
  shortened version appeared in the journal. Inspected the introduction,
  Theorems 1–2, Corollary 2, and the start of Section 5. Finite endpoint
  slopes give the relevant uniform O(N^-2) vertical approximation bound
  for a univariate convex function; Section 5 treats planar Hausdorff
  approximation. The manuscript cites the journal record without assigning
  the report's theorem numbers to the journal. The main comparison is
  precise: a classical one-dimensional approximation rate with tangent/chord
  approximants, versus this prescribed family of quadratic sublevel sets.

- Stephen Boyd and Lieven Vandenberghe,
  [*Convex Optimization*](https://www.seas.ucla.edu/~vandenbe/cvxbook/bv_cvxbook.pdf),
  Cambridge University Press (2004). The accessible primary PDF is the
  seventh printing with corrections (2009), as its copyright page states.
  Read Section 5.9.1, printed pages 264–265, especially the generalized
  Slater condition, dual cone multiplier signs, strong duality, and dual
  attainment; also Section 5.9.2's complementary slackness discussion.
  The manuscript's one-objective proposition is a self-contained
  specialization of this classical conic convex duality argument.
  Attempts to access the Stanford PDF directly failed; the coauthor's UCLA
  copy succeeded. No claim relies on the failed access.

Additional online search for quadratic aggregation, finite approximation,
and Hausdorff accuracy returned the existing BDS/DMS and bilinear
aggregation lines already audited in stage 4. No priority conclusion is
drawn from the absence of a closer search hit.

## Novelty assessment

The paper does not claim the exponent two, tangent/chord approximation,
general convex-body approximation, Hausdorff/support-function duality,
or objective-specific exactness as new principles. Its additional result
is the two-sided good-cut guarantee for this exact HHC construction:
arbitrary interior good multipliers are included in the lower bound,
constants are independent of replication dimension, and explicit integer
multiplier meshes give the same rate. A rate for arbitrary original-space
quadratics is not asserted. No runtime, cut-selection iteration, numerical
conditioning, or solver performance statement follows.

## New proof development and comparison with concurrent formal work

The earlier accuracy note proves the lower constant
`sqrt(2)*(log 2)^2/1600` using logarithmic interval coverage. The author
independently checked that argument. During this stage, the coordinator
identified the new finite-grid proof in the concurrent
`sections/94-formal-aggregation-accuracy.tex`. The author independently
rederived it: with eta=1/(400 N^2), summing the two exclusion inequalities
and applying AM–GM shows that one cut cannot exclude two parameters of
the grid tau_j=1+j/N. The numerical coefficient is exactly
`16*((1+10*eta)^2-1)=4/(5 N^2)+1/(100 N^4)<1/N^2`.

Combining this finite pigeonhole proof with the sharper manuscript
Lipschitz constant `5 sqrt(2)` gives the stronger lower bound
`sqrt(2)/(2000 N^2)`. The concurrent formal fragment uses Lipschitz
constant 10 and reports `1/(2000 N^2)`. Formal certification of that
package is not asserted in this stage; its later semantic integration and
actual verification remain stage 7 work. In particular, this stage's
stronger constant must not be silently described as already formalized.
The weaker logarithmic proof is preserved in the source provenance and
superseded in the manuscript rather than duplicated there.
