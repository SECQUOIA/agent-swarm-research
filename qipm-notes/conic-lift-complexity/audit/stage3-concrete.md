# Stage 3 concrete-formulation author report

Completed `sections/07-concrete-barriers.tex`. No changes to shared main, macros, or bibliography.

## Source disposition and verification

- `norm-tree-reduced-barrier-parameter`: all positive mathematical developments included: arbitrary-arity root incidence law; exact capped optimizer and residual indicator; exact product additivity; intrinsic polyhedral-section lower bound L; linked-cone logarithmically homogeneous lower bound L+1; exact comparison with grouped barriers. The unresolved arbitrary-barrier optimum for general trees is explicitly not asserted.
- The root-incidence calculation already appears in `central-path-cost/sections/appendix-formulations.tex`. It is reproduced with a complete proof for standalone use, not treated as a development absent from that manuscript. The cap optimizer and intrinsic section are useful additional synthesis here.
- Replaced the note's floating-point failure of the logarithmic-axis correction by a new exact rational counterexample: at (3,0,1,0,0), in direction (0,0,1,1,0), the second and third derivatives are 53/16 and -441/32, so their squared self-concordance excess is 11401/256 > 0. Exact fractions independently checked in the qipm Python environment.
- Exhaustively enumerated feasible recursive tree costs for every N=2,...,13 and cap d=3,...,8; all match the derived cap optimizer. This supports the independent combinatorial proof, rather than replacing it.
- `coupled-barrier-grouped-ball-slice`: included the exact H parameter for arbitrary coupled barriers, the hidden affine H-box, an explicit paraboloid self-concordance calculation, projected-product parameter k, cap comparison, fixed-tail realization in all simple Jordan families, perspective-p lower bound only, and duplicated-block counterexample showing that simultaneous active blocks cannot establish arbitrary-barrier bounds.
- `one-block-psd-packing-coupled-barrier`: included exact b parameter for every coupled barrier with no restriction b<=p. Strengthened the exposition to a complete bounded-fiber projection proof under explicit closed-convex hypotheses. Generalized the packing statement to real, complex, and quaternionic matrices with heterogeneous nonzero real column subspaces, using the same real-trace derivatives and projected box argument.
- The parameter projection proof establishes local uniform boundedness from closed convexity and absence of a vertical recession ray. This is stronger justification than simply asserting that barrier divergence survives partial minimization. Interior fibers of an arbitrary open domain are not silently substituted for bounded closed fibers.
- Products of balls themselves have intrinsic parameter equal to their number, by the explicit barrier and a box section. This is distinct from both ambient rank and the tree's prescribed-barrier parameter.

## Primary literature inspected

1. Nesterov and Nemirovskii, *Interior-Point Polynomial Algorithms in Convex Programming*, SIAM 1994, DOI 10.1137/1.9781611970791. Local user-supplied original PDF checked directly using `pdftotext`: Proposition 2.3.6 requires exactly k active facets with independent normals at a boundary point, and concludes parameter at least k. The stated special cases include cubes and simplices. All polyhedral sections used here have exactly the required number of active facets. No local source artifact copied.
2. Peter Robert Chares, *Cones and Interior-Point Algorithms for Structured Convex Optimization Involving Powers and Exponentials*, PhD thesis, UCL, 2009. Primary open PDF inspected at https://perso.uclouvain.be/francois.glineur/files/theses/Chares-PhD-thesis-2007.pdf . Assumption 4 is printed p.156; Theorem 5.2.1 is printed p.158; proof and Schur-complement calculations continue through p.162. The URL contains 2007, but the supervisor's primary webpage https://perso.uclouvain.be/francois.glineur/ identifies Chares's PhD dates as 2005--2009 and links this thesis. Use 2009, not the URL's date fragment.
3. Norm-tree models use the already verified Ben-Tal--Nemirovski 2001 citation from Stage 1. No new priority claim is based on a modeling construction.

Targeted online searches for norm-tree barrier parameters, grouped-ball self-concordant barriers, and column-packing semidefinite barrier parameters did not locate a prior statement of these exact affine-slice applications. Such a negative search is not a proof of priority. This section makes no absolute priority claim and attributes all general barrier calculus to prior work.

## Required bibliography entries

```bibtex
@book{NN1994,
 author={Nesterov, Yurii and Nemirovskii, Arkadii},
 title={Interior-Point Polynomial Algorithms in Convex Programming},
 publisher={SIAM}, address={Philadelphia}, year={1994},
 doi={10.1137/1.9781611970791}}
@phdthesis{Chares2009,
 author={Chares, Peter Robert},
 title={Cones and Interior-Point Algorithms for Structured Convex Optimization Involving Powers and Exponentials},
 school={Universit{\'e} catholique de Louvain}, year={2009},
 url={https://perso.uclouvain.be/francois.glineur/files/theses/Chares-PhD-thesis-2007.pdf}}
```

The section references `lem:compact-base-parameter` from Section 6 for the linked-cone lower bound. All other cross references point to already integrated Stage 1 material. Parent reports successful integrated 35-page compilation, pending these two bibliography entries.
