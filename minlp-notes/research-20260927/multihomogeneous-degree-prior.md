# Prior audit: the multihomogeneous degree refinement

Date: 2026-09-27. This audit concerns a proposed refinement of
[explicit-span-separation.md](explicit-span-separation.md). It independently
checks the literature and the algebraic step; it does not independently verify
the full convex optimization reduction.

The count `2^s binom(d,s)` for a quadratic KKT system with `d` primal variables
and `s` active constraints is classical. The presence of other positive
dimensional components does not prevent this count from bounding the isolated
regular roots. A contribution here must concern the Hessian span reduction and
the controlled optimizer limit, not a new Bézout theorem or a new generic QCQP
degree formula.

## Sources examined and their precise scope

1. Nie and Ranestad, *Algebraic Degree of Polynomial Optimization*,
   [arXiv:0802.1233](https://arxiv.org/abs/0802.1233), Theorem 2.2,
   Corollary 2.5, and Section 3.2, equation (3.1). The local text
   [nie-ranestad-2009.txt](sources-hessian-span-prior/nie-ranestad-2009.txt)
   was read directly. Its header identifies the 2008 arXiv v1; the filename
   reflects the later publication year. Theorem 2.2 gives the generic
   polynomial optimization degree. Its nongeneric upper-bound assertion
   explicitly requires the entire complex KKT system to be zero dimensional.
   Corollary 2.5 retains that qualification for inequalities with a fixed active
   set. For quadratics the formula becomes `2^s binom(d,s)`, and the paper proves
   generic sharpness. This stated theorem alone does not cover an isolated
   regular root alongside other positive dimensional KKT components.

2. Dedieu, Malajovich, and Shub, *On the Curvature of the Central Path of Linear
   Programming Theory*,
   [open manuscript](https://arxiv.org/pdf/math/0312083), Section 5,
   Theorem 5.1; published in *Foundations of Computational Mathematics* 5
   (2005), 145–171,
   [DOI](https://doi.org/10.1007/s10208-003-0116-8). The complete Section 5
   was read. It states the multihomogeneous bound for the number of isolated
   zeros in a product of projective spaces, without assuming that all zeros
   are isolated. It separately gives equality when all zeros are nonsingular.
   The section attributes the theorem to Morgan and Sommese, *A homotopy for
   solving general polynomial systems that respects m-homogeneous structures*,
   *Applied Mathematics and Computation* 24 (1987), 101–113,
   [DOI](https://doi.org/10.1016/0096-3003(87)90063-4).
   The latter paper's publisher abstract and bibliographic data were checked;
   its full text was not obtained in this audit.

3. Safey El Din and Trébuchet, *Strong bi-homogeneous Bézout theorem and its use
   in effective real algebraic geometry*,
   [arXiv:cs/0610051](https://arxiv.org/pdf/cs/0610051), Theorems 1 and 2
   and the introductory discussion of Lagrange systems. This is a stronger
   treatment of nonequidimensional systems, controlling the sum of degrees
   of admissible isolated primary components in all dimensions. Theorem 1
   includes restrictions on the number of generators with zero degree in
   either variable block. The ordinary isolated-point bound in item 2 is
   sufficient here, so no stronger theorem is needed.

The search also identified Morgan and Sommese's *Coefficient-parameter
polynomial continuation* (1989),
[DOI](https://doi.org/10.1016/0096-3003(89)90099-4), and the accessible
[Morgan chapter on polynomial continuation](https://donaldlab.cs.duke.edu/Books/SymbolicNumericalComputation/021-044.pdf).
These establish the relevant prior context for continuation. Their results
are not being used as an unchecked substitute for the specialization argument
below.

## Application of the classical count

Before eliminating the primal variables, a fixed-support quadratic KKT system
has `s` equations of bidegree at most `(2,0)` and `d` stationarity equations of
bidegree at most `(1,1)` in the blocks `(u,lambda)`. Homogenize to those degrees
in `P^d x P^s`; padding degrees only adds behavior at infinity. The associated
multihomogeneous number is

\[
[U^dL^s](2U)^s(U+L)^d=2^s\binom ds.
\]

An affine root where the square KKT Jacobian is nonsingular is isolated also
in the affine chart of this projective system. Consequently the classical
bound applies even when the full projective or affine zero set contains
other positive dimensional components.

For a strongly convex objective, let `M` be the positive definite Hessian of
the Lagrangian and let the rows of `A` be the selected active gradients.
If these gradients are independent, the KKT Jacobian

\[
\begin{pmatrix}M&A^T\\A&0\end{pmatrix}
\]

is nonsingular: its Schur complement is `-A M^{-1} A^T`, which is negative
definite. This checks the relevant regularity condition locally. It does not
assert that the entire complex KKT variety is zero dimensional.

If only `s <= min(h,d)` is known, the safe uniform degree bound is

\[
B(d,h)=\max_{0\le s\le\min(h,d)}2^s\binom ds.
\]

The expression is not always increasing in `s`: for `d=3`, the values at
`s=2,3` are `12,8`. Using `2^h binom(d,h)` without another restriction would
therefore be unjustified. For fixed `h`, `B(d,h)=O(d^h)`.

## What parameter specialization still requires

The following is an algebraic proof route, not a claim that the cited QCQP
theorem already proves the desired optimizer result.

Let `p` denote the coefficient parameters, with all coefficients in `Q[p]`,
and let `F(p,y)=0` be a square KKT system. On the locus where `det D_y F` is
nonzero, the implicit function theorem makes the projection to parameter
space locally open. Thus every irreducible component meeting this locus
dominates parameter space and has zero dimensional generic fiber. Over
`Q(p)`, the reduced algebra of these regular roots is finite, with dimension
at most the multihomogeneous count. Multiplication by a coordinate, or by a
rational linear combination of primal coordinates, has a characteristic
polynomial of at most that degree. Clearing denominators gives a nonzero
polynomial `P(p,Y)` with rational coefficients.

This identity initially holds on a Zariski open subset of parameter space.
It extends to every regular root at an exceptional parameter by applying the
implicit function theorem near that root and using continuity of the
polynomial identity. This extension needs to be stated: merely discarding
exceptional parameters does not justify a limit lying in their locus.

For ordered parameters `(epsilon,delta)`, write

\[
P(\epsilon,\delta,Y)=\sum_{j\ge r}\delta^j P_j(\epsilon,Y),
\qquad P_r\ne0.
\]

At each fixed nonzero `epsilon`, divide the identity by `delta^r` and take a
finite inner limit as `delta` tends to zero. The limiting value satisfies
`P_r(epsilon,Y)=0`. Then take the lowest nonzero coefficient in `epsilon`
and pass to the finite outer limit. This produces a nonzero rational
annihilator of degree no larger than the original count. Neither bounded
multipliers nor a quantitative rule `delta(epsilon)` is required. The
argument does require a single fixed KKT support and a single polynomial
family along the chosen ordered sequences.

Applying this argument to every rational linear combination of the limiting
primal coordinates, followed by the primitive element theorem, bounds the
degree of their joint number field by the same number. Separately bounded
coordinate degrees would not alone imply this joint-field bound.

This argument supplies no coefficient-height estimate by itself. The
separate explicit elimination and height proof must remain in place for
precision bounds or polynomial bit complexity. A sequence of algebraic
numbers of bounded degree can converge to a transcendental number when no
common parameter-polynomial relation controls the sequence.

## Novelty assessment and verification record

The multihomogeneous count, its applicability to isolated roots of
nonequidimensional systems, and algebraic continuation are established
ingredients. The candidate advance is obtaining a support controlled by the
span of the native constraint Hessians and proving that a canonical optimizer
is an ordered limit of regular roots on such a support. No claim of a new
generic degree formula is justified. Whether that complete structural result
appears under another formulation remains a broader literature question;
this audit is not a proof of novelty.

Checks performed: direct reading of the specified local Nie–Ranestad text;
primary-source web searches; `pdftotext -layout` and targeted Section 5
inspection of the Dedieu–Malajovich–Shub manuscript; independent calculation
of the bidegree coefficient and the KKT Schur complement. No project-wide
checks, CI inspection, or numerical experiment was needed for this audit.
