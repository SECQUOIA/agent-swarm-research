# Primary sources for constrained exact arithmetic extensions

Date: 2026-10-03. This source record supports
[the constrained Newton theorem](structural-newton.md). It records
specific dependencies rather than a complete priority search.

| Source | Relevant content | Use and limitation |
| --- | --- | --- |
| Jason D. Lee, Yuekai Sun and Michael A. Saunders, *Proximal Newton-Type Methods for Minimizing Composite Functions*, SIAM Journal on Optimization 24(3) (2014), 1420--1443, [author PDF](https://stanford.edu/group/SOL/multiscale/papers/14siopt-proxNewton.pdf), Theorem 3.4 | Quadratic convergence with constant `L_H/(2mu)` for exact proximal Newton steps | Taking the nonsmooth term to be the indicator of the feasible polyhedron yields the estimate used here. The proof needs no strict-complementarity condition. The numerical convergence theorem does not itself establish the arithmetic-circuit exact-comparison complexity. |
| Jong-Shi Pang and Shaoning Han, *Some Strongly Polynomially Solvable Convex Quadratic Programs with Bounded Variables*, [author manuscript](https://optimization-online.org/wp-content/uploads/2021/12/arxiv.pdf), revised September 2022 | Algorithm I and Proposition 2.1, printed pages 2--3; comparison-matrix vector construction, printed page 5 | The displayed exact box-QP algorithm uses rational linear algebra and comparisons. Our proof verifies the required vector for each circuit Hessian. The source does not claim the quartic exact-sign consequence. |
| Lucas Slot, David Steurer and Manuel Wiedmer, *Hesse's Redemption: Efficient Convex Polynomial Programming*, [version 1](https://arxiv.org/html/2511.03440v1), Corollary 1.2 | Polynomial-time feasible additive-objective approximation for globally convex polynomial optimization over rational polyhedra | Supplies a polynomial-bit initial feasible point. Strong convexity converts its objective error to distance. The later exact circuit refinement is a separate argument. |
| Saugata Basu, *Algorithms in Real Algebraic Geometry: A Survey*, [author PDF](https://www.math.purdue.edu/~sbasu/raag_survey2011.pdf), Theorem 2.16 | One-block quantifier elimination with degree and coefficient-size bounds | Used only to bound a nonzero observable at the unique constrained optimizer away from zero. Quantifier elimination is not executed by the proposed algorithm. |
| Frieda Granot and Jadranka Skorin-Kapov, *Towards a Strongly Polynomial Algorithm for Strictly Convex Quadratic Programs: An Extension of Tardos' Algorithm*, Mathematical Programming 46 (1990), 225--236, [DOI](https://doi.org/10.1007/BF01585740) | Arithmetic complexity independent of the right-hand side and linear cost; dependence on constraint and Hessian encodings remains | This theorem alone does not solve Taylor QPs whose Hessian entries have short circuits but potentially enormous expanded encodings. The [author's 1987 thesis record](https://open.library.ubc.ca/soa/cIRcle/collections/ubctheses/831/items/1.0097502) explicitly states this scope. |

The Pang--Han PDF was read directly, including the pivot formulas and
the statement that degeneracy is permitted. The other theorem interfaces
are also documented in the repository's reviewed
[unconstrained upper-bound proof](../../research-20260927/strong-convex-quartic-posslp-upper.md).

The Granot--Skorin-Kapov publisher download attempted during this work
returned HTML rather than a readable PDF. The scope stated above is
supported by the primary thesis abstract, rather than an assertion that
the complete 1990 proof was re-audited. No claim about which of its
internal bounds can be improved is made.
