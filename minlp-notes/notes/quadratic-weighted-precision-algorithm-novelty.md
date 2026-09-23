# Novelty and source audit: computing near-optimal quadratic integer precision

Date: 2026-09-05. Independent audit of
`notes/quadratic-weighted-covariance-algorithm.md` and the reviewed finite
benchmark in `results/quadratic-weighted-covariance-precision.md`.
The algorithm is still undergoing mathematical and finite-precision
review. This note assesses sources and prior scope.

## Assessment

No primary open statement was found guaranteeing a polynomial-bit
algorithm that constructs a rational MILP relaxation of an arbitrary
rational quadratic vector graph, with prescribed unequal output
tolerances, using at most the optimum unrestricted convex-lift integer
dimension plus `O(n log(n+1))` binaries.

The strongest candidate contribution is this **finite guarantee against
all convex lifted formulations**, including unrestricted general integer
coordinates. The matrix optimization is useful because the reviewed
covariance theorem relates its optimum to that comparison class.

Hessian-based anisotropic meshes, maximum-volume ellipsoid selection,
combining several output metrics, positive definite matrix optimization,
geodesic subgradient convergence, and approximate diagonalization are
established topics. Even simultaneous metrics with separate tolerances
appear in older CFD mesh work. Avoid claiming these broad ideas as new.
The particular penalty, radius and conditioning bounds, and rational
construction may be useful implementation lemmas; their role is to
make the new formulation guarantee constructive.

## Anisotropic interpolation and ellipsoid selection

**Weiming Cao (2007).** *An Interpolation Error Estimate on Anisotropic
Meshes in R^n and Optimal Metrics for Mesh Refinement*, SIAM Journal on
Numerical Analysis 45(6), 2368–2391,
[researcher-hosted published PDF](https://www.ljll.fr/~frey/papers/meshing/Cao%20W.%2C%20An%20interpolation%20error%20estimate%20on%20anisotropic%20meshes%20and%20optimal%20metrics%20for%20mesh%20refinement.pdf).
The full PDF was downloaded and Sections 3.1–3.2 inspected.

Equation (25), printed pages 2379–2380, optimizes a positive definite
matrix describing derivative anisotropy. In the `L^p` error case its
objective reduces to determinant minimization. Equation (26) requires
the associated quadratic form to dominate a directional derivative
polynomial. Cao explicitly interprets this as finding a largest
ellipsoid inside that polynomial's absolute-value level set. Section
3.2 gives a successive dimension-reduction procedure described as a
suboptimal approximation because solving the original minimization can
be expensive. The inspected statements provide no polynomial-bit
guarantee for the present simultaneous Frobenius constraints and no
comparison against arbitrary mixed-integer convex lifts.

**Long Chen, Pengtao Sun, and Jinchao Xu (2007).** *Optimal Anisotropic
Meshes for Minimizing Interpolation Errors in L^p-Norm*, Mathematics of
Computation 76(257), 179–204,
[author-hosted paper](https://www.math.uci.edu/~chenlong/Papers/Chen.L%3BSun.P%3BXu.J2006.pdf).
The PDF filename reflects the prepublication year. Their interpolation
bounds and modified-Hessian metric give sufficient conditions for
nearly optimal simplicial meshes, with moving-mesh functionals and
numerical examples. This is direct prior art for translating local
Hessian geometry into anisotropic approximation. Its comparison class
is interpolation meshes and errors, not integer dimension over all
convex formulations.

**Frey and Alauzet: multiple outputs are also established.**
Their author-hosted *Anisotropic mesh adaptation in 3D: Application to
CFD simulations*,
[open manuscript](https://pages.saclay.inria.fr/frederic.alauzet/proceedings/Frey_Anisotropic%20mesh%20adaptation%20in%203D%20Application%20to%20CFD%20simulations.pdf),
contains a section on metric intersection. It explicitly requires the
interpolation error of each variable to meet its own tolerance and
describes the maximum-volume ellipsoid in the intersection of two
metric ellipsoids. Their related journal paper is *Anisotropic mesh
adaptation for CFD computations*, Computer Methods in Applied Mechanics
and Engineering 194 (2005), 5068–5082,
[primary publication](https://doi.org/10.1016/j.cma.2004.11.025).
Consequently, “one anisotropic metric for several output accuracies” is
not by itself a novelty claim. The candidate retains the signed Hessian
system and compares the resulting rational formulation with every convex
integer lift, which is a different theorem.

**Yano and Darmofal (2012).** *An optimization-based framework for
anisotropic simplex mesh adaptation*, Journal of Computational Physics
231, 7626–7649,
[primary abstract](https://doi.org/10.1016/j.jcp.2012.06.040),
already optimizes a Riemannian metric field using local error models,
an affine-invariant tensor framework, and gradient descent. The abstract
does not assert the present rational bit complexity or finite integer
dimension guarantee. A general claim to introduce gradient-based
optimization of mesh metrics would overlap with this work.

## Geodesic optimization imports

**Hongyi Zhang and Suvrit Sra (2016).** *First-order Methods for
Geodesically Convex Optimization*, COLT, PMLR 49, 1617–1638,
[official proceedings PDF](https://proceedings.mlr.press/v49/zhang16b.pdf).
The full paper was downloaded. Corollary 8, printed manuscript page 8,
is the projected one-step distance inequality used in the draft.
Theorem 9 gives the projected subgradient convergence bound with the
curvature factor `zeta(kappa,D)`. The proof controls a sum of objective
gaps, so using the best objective among iterates is consistent with
the inequality even though the theorem presents a geodesic average.

This is an iteration-complexity theorem with exponential-map,
subgradient, and projection operations. It does not supply rational
implementations of those operations or certify bit complexity of the
candidate. Its applicability requires the stated geodesic convexity,
Lipschitz, diameter, and curvature hypotheses; the candidate provides
its own bounds and rounding recurrence for those purposes.

**Allen-Zhu, Garg, Li, Oliveira, and Wigderson (2018).**
*Operator Scaling via Geodesically Convex Optimization, Invariant Theory
and Polynomial Identity Testing*,
[author-hosted STOC paper](https://www.math.ias.edu/~avi/PUBLICATIONS/Allen-ZhuGaLiOlWi2018_stoc.pdf),
[full preprint](https://arxiv.org/abs/1804.01076).
They already give a second-order method on positive definite matrices
and polynomial-time operator scaling with logarithmic dependence on
accuracy. Their analysis includes bounds on near-minimizer condition
numbers. The candidate therefore cannot claim the first polynomial-bit
use of geodesic positive definite optimization. Its objective, repair
map, and formulation target differ from operator capacity. In particular,
it needs only a constant additive log-determinant gap; logarithmic
dependence on the graph tolerances comes through input size and its
radius bound.

The known caveat that geodesic convexity alone does not imply a useful
polynomial diameter bound is documented by Franks and Reichenbach,
*Barriers for Recent Methods in Geodesic Optimization*, CCC 2021,
[primary proceedings](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2021.13).
Their difficult examples concern other scaling problems. They do not
contradict the explicit ball bound proposed here, but underscore why
that bound must be proved rather than inferred from geodesic convexity.

## Spectral approximation: source issue and proposed resolution

The first algorithm draft imported polynomial-time approximate spectral
decomposition without an exact reference. This deserves care: a theorem
about eigenvalues alone is insufficient for its coordinate construction.

Aleksandros Sobczyk, *Deterministic complexity analysis of Hermitian
eigenproblems*,
[arXiv:2410.21550v2](https://arxiv.org/html/2410.21550v2), revised April
2025, explicitly distinguishes eigenvalues, eigenspaces, and full
diagonalization, as well as Real-RAM and finite-precision complexity.
Its introduction also identifies incomplete eigenvector complexity
arguments in commonly cited earlier work. Its fast full-diagonalization
theorem in the Real-RAM part must not silently be treated as the
finite-bit eigenvalue theorem. This does not suggest that polynomial
diagonalization is impossible; it means the exact result being imported
must match the claim.

The author agreed to supply an explicit rounded maximum-pivot Jacobi
routine instead. The classical exact contraction is documented, with
proof, in Robert Gower's author-hosted *Optimization and Numerical
Analysis: Solving Linear Systems* (2020), slides 44–46,
[lecture PDF](https://gowerrobert.github.io/pdf/teaching/MDI210/NA_slides.pdf):

```
off(B)=off(A)-2 a_pq^2,
off(B)<=[1-2/(n(n-1))] off(A)
```

when `off` denotes the squared off-diagonal Frobenius norm and the
pivot has maximum magnitude. This is classical numerical linear
algebra, not new diagonalization theory. The candidate needs to add
and independently verify polynomial-bit approximate rotations and
accumulated residual/orthogonality bounds.

A useful simplification is to ask for small reconstruction residual and
near-orthogonality, not closeness to a distinguished exact eigenbasis.
Repeated or clustered eigenvalues then pose no artificial uniqueness
requirement. For the final grid, the required output is a rational
factorization whose reconstructed covariance lies between fixed scalar
multiples of the feasible covariance. Matrix functions and the Rayleigh
oracle need their own quantitative residual-to-error estimates.

## Publication framing and limits

Subject to verification, a defensible leading claim is:

> Rational quadratic systems with unequal rational accuracies admit a
> polynomial-time rational MILP construction whose binary count is
> within `O(n log(n+1))` of the least integer dimension of any convex
> lifted graph relaxation.

State that the additive term depends only on input dimension, while
runtime is polynomial in the total binary encoding. This does not mean
that the resulting MINLP or MILP can be optimized in polynomial time,
nor that the best integer count is computed exactly.

Searches covered the named interpolation sources, multiple-output metric
intersection, maximum-volume ellipsoids for quadratic forms, geodesic
positive definite optimization, operator scaling, and finite-precision
eigenproblems. No matching finite whole-formulation guarantee was found.
This remains limited negative evidence, not proof of priority. The
algorithm's mathematical status should follow its independent reviews;
this audit does not promote it by itself. Downloaded scratch sources
are under `/tmp/minlp-weighted-novelty/`.
## Later source discovery: rational Jacobi rotations

During the nonlinear-input-rank audit on 2026-09-05, a directly relevant
recent source was found: Alberto Del Pia, *Rational Jacobi Rotations and the
Complexity of Approximating Mixed Integer Quadratic Programming*,
arXiv:2607.29386, submitted 31 July 2026.
[Primary paper](https://arxiv.org/html/2607.29386).

Theorem 2 in Section 2.3.3 computes, for rational symmetric `A` and rational
`delta in (0,1]`, an exactly orthogonal rational matrix `L` with
`off(L^T A L)<=delta` in Turing time polynomial in their binary encodings.
Here `off` is the Frobenius norm of the off-diagonal part. Consequently,
`D=diag(L^T A L)` gives `||A-L D L^T||_F<=delta`. This is an established
alternative satisfying the construction's numerical import. The checked proof
uses rational Jacobi rotations and common-denominator bounds.

The paper's main theorem approximates a given MIQP objective with fixed integer
count and fixed negative inertia. It does not optimize integer count for a
graph approximation. The numerical diagonalization result must nevertheless
be credited; the repository's self-contained rounded Jacobi appendix should
not be presented as a new algorithmic result. Its prior verification remains
useful, and no replacement is required to preserve the present construction.
