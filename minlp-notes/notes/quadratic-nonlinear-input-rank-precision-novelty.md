# Source and novelty audit: nonlinear input rank

Date: 2026-09-05. Independent bounded audit of
[the nonlinear-input-rank draft](quadratic-nonlinear-input-rank-precision.md).
Mathematical proof reviews are recorded separately.

No matching prior whole-formulation theorem was found with additive
`O(r log(r+1))` integer-count overhead, where `r` is the rank of the vertically
stacked symmetric Hessians. The underlying common-kernel quotient, projected
cube, and ellipsoid normalization are established tools. The contribution to
emphasize is their use to improve the dimension term in the repository's
near-minimal rational MILP guarantee.

## Exact rational zonotope separation is standard LP

The proposed domain oracle is valid in the classical polynomial bit model.
For `Z=U[-1/2,1/2]^n` and a rational query `z`, membership is the explicit
rational linear feasibility problem

```
Ut=z,       -1/2<=t_i<=1/2.
```

For a direct separator certificate, use a second explicit LP:

```
v_i >= (U^T a)_i,       v_i >= -(U^T a)_i,
a^T z - (1/2) sum_i v_i >= 1.
```

If feasible, its solution gives the valid inequality
`a^T y <= (1/2)sum_i v_i` for every `y in Z`, violated by `z`. Conversely,
strict separation of a point outside the compact convex zonotope, together
with the support identity `h_Z(a)=(1/2)||U^T a||_1`, gives such a solution
after rescaling. Thus exactly one of the two systems is feasible. This
explicit alternative was supplied to the author and incorporated into the
draft during the audit.

Polynomial-time exact rational LP, including polynomial-size feasible
solutions, is a classical import. Khachiyan's *Polynomial algorithms in linear
programming* (1980) explicitly concerns exact algorithms with complexity
polynomial in the binary encoding length; the original archive supplies the
paper and its abstract.
[Original journal archive](https://www.mathnet.ru/eng/zvmmf5239).
The abstract was checked for this scope; no new reconstruction of the original
LP proof is claimed here. A modern primary treatment of exact feasible points
and Farkas certificates is Dadush–Végh–Zambelli, Theorem 1.3(i), with its rational
polyhedron discussion in Section 1.1.2. That stronger oracle machinery is not
needed for the two explicit LPs above.
[On finding exact solutions of linear programs in the oracle model (2026)](https://arxiv.org/html/2606.11820).

The matrix `U` and both LPs have polynomial rational encoding. A feasible basic
solution after the usual conversion to standard form has polynomial encoding
by determinant bounds. Thus the returned separator meets the polynomial-size
strong-oracle assumption of Dadush–Peikert–Vempala, Definition B.2 and Theorem
B.5. The latter rounding import was checked in the
[general-norm audit](quadratic-general-norm-precision-novelty.md).

## Ridge and active-subspace antecedents

The factorization `f(x)=a(x)+g(Ux)` is a vector-valued ridge representation
after removing an affine map. For rational quadratic functions its exact
construction from the common Hessian kernel is elementary linear algebra.
It should not be introduced as a new dimension-reduction principle.

Constantine and Gleich explicitly compute the gradient second-moment matrix
for a quadratic model on a uniform centered cube as `C=A^2/3`, in Section 5.1,
equations (74)–(75). This links its active directions to those of its Hessian.
[Computing active subspaces with Monte Carlo](https://arxiv.org/html/1408.0545).

Zahm, Constantine, Prieur, and Marzouk treat vector-valued ridge approximation
and the effect of output norms. Their equation (11) constructs the input
matrix by integrating `Jacobian(f)^T R_V Jacobian(f)`. Their analysis controls
mean-square approximation via subspace Poincaré inequalities, chiefly under
Gaussian input measures.
[Gradient-based dimension reduction of multivariate vector-valued functions](https://arxiv.org/html/1801.07922).
In the present quadratic setting, the exact common kernel can be read directly
from coefficients. The new target is uniform graph containment and error over
the whole cube, measured through minimum integer dimension, rather than a
mean-square surrogate approximation.

## Low-rank optimization and zonotope antecedents

Ferrez, Fukuda, and Liebling reduce fixed-rank PSD binary quadratic maximization
to zonotope vertex enumeration. Their 2005 algorithm has polynomial complexity
for fixed rank.
[Solving the fixed rank convex quadratic maximization in binary variables by a parallel zonotope construction algorithm](https://www.cs.mcgill.ca/~fukuda/download/paper/qpzono040429.pdf).

Hladík, Černý, and Rada extend this approach to arbitrary fixed-rank quadratic
objectives with linear terms on boxes. Section 2.2 explicitly reduces dimension
through a rank factorization and a projected-box zonotope; the algorithm then
enumerates faces. Thus the projected-cube bridge is a particularly close known
antecedent, not a new geometric construction.
[A new polynomially solvable class of quadratic optimization problems with box constraints](https://arxiv.org/pdf/1911.10877).

Dadush, Léonard, Rohwedder, and Verschae study the form `g(Wx)+c^T x` over
box-constrained integer inputs, with few nonlinear aggregate coordinates and
bounded integer coefficients in `W`. Their algorithms depend on aggregate
dimension and coefficient magnitudes, and include a related MILP extension.
[Optimizing Low Dimensional Functions over the Integers, IPCO 2023](https://arxiv.org/abs/2303.02474).
This already recognizes that many variables may enter an objective only
linearly. It solves a given discrete optimization problem, rather than
constructing a nearly integer-minimal approximation of a continuous graph.

The recent Soltanalian–Mousavi preprint also organizes fixed-rank PSD quadratic
optimization around projected feasible sets and linear exposure directions,
with explicit credit to prior zonotope methods. Its inspected statement and
discussion do not give an integer-precision formulation guarantee.
[The Rank-Collapse Principle for Quadratic Optimization, August 2026](https://arxiv.org/html/2608.07828).

## The remaining distinction and limits

The candidate exactly preserves the formulation optimum under affine input
quotient and output subtraction. After rational normalization, the reduced
zonotope occupies at least `2^(-O(r log(r+1)))` volume inside an `r`-cube.
The repository's contact-volume bound therefore compares the construction on
that containing cube to the optimum on the actual projected domain, losing
only `O(r log(r+1))` integers. The domain still has an exact rational linear
lift using the original cube variables. This combination is the meaningful
new consequence identified by the bounded search.

Keep the following limits explicit:

- `r` is exact common nonlinear input rank. It is not the number of Hessians,
  the maximum scalar Hessian rank, or the noncommutative rank of their span.
- The rank bound improves the additive overhead. It does not eliminate the
  necessary dependence of the optimum integer count on tolerance and scale.
- The construction is polynomial in the full encoded input, not necessarily
  polynomial in `r` alone. Original continuous variables may remain in its lift.
- The theorem constructs an approximation; it does not claim an efficient
  algorithm for optimizing every resulting MILP.
- This audit supports the projected-cube domain. It does not justify replacing
  an arbitrary curved feasible region by an exact linear lift.

The source search also discovered Del Pia's July 2026 rational Jacobi theorem,
which is directly relevant to the earlier numerical construction appendix.
That discovery and the exact theorem are recorded in the
[updated weighted-algorithm audit](quadratic-weighted-precision-algorithm-novelty.md).
It changes numerical-method attribution, not the current assessment of the
integer-count objective.
