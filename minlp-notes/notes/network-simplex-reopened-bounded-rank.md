# Reopened bounded-rank direction: proof, implementation, and small sharpness example

Date: 2026-09-07. Work log and retained scope decisions; the completed proof is
in [the result file](../results/network-simplex-bounded-rank-hull.md). The
[independent review](review-network-simplex-reopened-bounded-rank.md) passed for
both the general theorem and the sharp K4 extension.

## What the continuation resolved

The earlier common-fan outline can be completed constructively. Fundamental-cycle
matrices are TU, which gives a finite list of possible state-polytope edge
directions with a stronger property than coordinate boundedness: every arc
coordinate of every primitive direction is zero or ±1. Common arrangement rays
then give exact Minkowski-sum support tests, including degenerate summands.
Local feasibility uses positive TU circuits; support evaluation uses precomputed
nonnegative dual bases. Thus all online conditions are minima of affine forms,
with parameter-only work per observed state.

The key additional step is a change-of-basis coefficient argument. A support ray
is a primitive cofactor vector of independent edge directions. Any unimodular
basis of signed arc normals transforms those directions to ternary vectors.
Therefore the transformed support ray, which is exactly the dual multiplier
vector, has the same determinant bound. This avoids the otherwise unnecessary
factor of cycle rank in the product-coefficient bound.

The result gives an exact complete hull with integer flow/product coefficients
bounded only by maximum block cycle rank. At rank three the bound is two.
A seven-observation K4 coordinate section proves two is necessary. This is
stronger than finding a multiplier two in an arbitrary redundant cut: every
finite original-coordinate description needs the product ratio two, because a
two-dimensional coordinate section has a genuine boundary segment with that
normal. The construction fixes the aggregate flows, so adding flow equations
cannot remove the ratio.

## Practical implications and limits

K4's actual library is small: seven edge directions, 18 support rays, 128
invertible bases, and 120 distinct sparse support duals across all rays.
A rank-four wheel has 13 directions, 62 rays, 720 bases, and 1,034 sparse support
duals. Its largest enumerated primitive ray coordinate is two and its largest
dual multiplier is three, below the general Hadamard bound five. These are
library facts for the stated matrices, not lower bounds for necessary hull
coefficients; redundant rays/bases can inflate a library's maximum.

A reusable low-rank separator now appears realistic, but a sparse compressed
extended formulation is an essential comparison. Suppressing degree-two paths,
splitting blocks, and merging unobserved labels already avoid a full m-by-E
state expansion. The bounded-rank result adds explicit original-coordinate
branches and a coefficient theorem; it does not establish computational speed
without measurement.

The worst-case library grows as 2^{O(r^2)}. No claim should suggest that universal
precompilation at moderate rank will be competitive. Use actual graph-specific
libraries. The existing parallel-path max-flow method remains preferable on its
own class even at unbounded rank.

## Literature distinctions

The normal-fan mechanism is classical, already explicit in Gritzmann–Sturmfels
(1993), Lemma 2.1.5, Proposition 2.1.8, and Algorithm 2.3.6; see the repository's
[full text](../literature/papers/gritzmann1993-minkowski-addition-of-polytopes-computational/fulltext.md).
Onn–Rothblum, [Convex Combinatorial Optimization](https://arxiv.org/abs/math/0309083),
and Onn–Rozenblit,
[Convex Integer Optimization by Constantly Many Linear Counterparts](https://arxiv.org/abs/1208.5639),
provide related edge-direction/zonotope machinery. A new generic fan theorem is
not claimed. Network flow edge directions are also classical.

The exact network–simplex extended hull already exists in Khademnia–Davarnia.
The candidate novelty is the complete sparse, block-rank-parameterized
original-space coefficient and separation theorem, together with its sharp
rank-three threshold. A targeted open search found no matching theorem, but
priority is provisional and must account for the paper's weight-two example.

## Checks performed by the developing agent

The [script](../code/network-simplex-bounded-rank-verify.py) builds libraries
using exact determinant/cofactor arithmetic, verifies inverses and all multiplier
bounds, evaluates candidate formulas using Fraction, and compares 160 cases
against raw-state LPs. It also checks 218 support values against exact primal
vertex enumeration. The cycle, theta, K4, and wheel cases include zero weights,
repeated arc observations, local inconsistent observations, and aggregate-only
infeasibility. An 81-point grid checks the sharp K4 section against raw-state LPs;
accepted points are also checked using the explicit rational decomposition.
These computations complement the proof and do not replace independent review.

## Further directions that should not hold up a paper

- An optimized K4 library separator and a benchmark against the compressed EF
  would strengthen practical claims. This is implementation work, not a missing
  hypothesis of the theorem.
- Exact best coefficient bounds at rank four and beyond remain open here.
  Hadamard gives a clean parameter-only bound; the wheel's multiplier three is
  not yet a necessary product coefficient ratio.
- Direct linear-arithmetic convex decomposition at all fixed ranks is not proved
  by this continuation. Sparse extended feasibility supplies a polynomial
  construction; the result deliberately does not claim the stronger bound.
- The series–parallel graph boundary is logically distinct. K4 is outside that
  class; the K4 obstruction alone says nothing about it.
