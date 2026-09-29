# Exact rational sparse box certificates with quantitative slack

Date: 2026-09-28. Consequence of the reviewed
[sparse kernel theorem](sparse-kernel-rounding.md), with independent checks
of the algebra and algorithmic assumptions. The generic rational SOS and
ellipsoid arguments are established methods. No separate priority claim is
made for this consequence.

## Result and purpose

The sparse kernel theorem gives real Gram certificates at an explicit order.
For rational data, a further rational objective slack gives an exact rational
certificate whose encoding length, and theoretical construction time, are
polynomial in the expanded finite SDP size and the bit length of the data.
The extra dependence on the slack is logarithmic. Thus the convergence
theorem can supply certificates checked entirely by rational arithmetic.

This does not make the hierarchy polynomial in the original input size:
the matrix dimensions depend on the order and bag width. The constructive
claim uses a rational ellipsoid feasibility algorithm with proved inner and
outer bounds; it is not a claim about the output or running time of an
arbitrary floating point SDP solver.

## 1. Statement and encoding

Use the bags, running-intersection hypothesis, rational bag polynomials
`f_b`, and order `r >= max(w,deg f_b)` of the sparse kernel theorem. Put

\[
 E_r=\frac{3A(f;B)}{2(\lfloor r/w\rfloor+1)^2+1},\qquad
 p=f-\gamma.
\]

The Chebyshev coefficient budget `A(f;B)` is rational when the input
monomial coefficients are rational. Let `gamma` and `tau>0` be rational.
Assume the quantitative positivity promise

\[
 f^*-\gamma\ge E_r+\tau.                                      \tag{1}
\]

For a bag `b` and `I subseteq B_b`, write

\[
 g_{b,I}=\prod_{i\in I}(1-x_i^2),\qquad
 v_{b,I}=(x^\alpha:|\alpha|\le r-|I|),\qquad
 s_{b,I}=\binom{|B_b|+r-|I|}{|B_b|}.
\]

Empty bags may be removed or their constants assigned to another bag. Put

\[
 D=\sum_{b,I}s_{b,I},\quad
 V=\sum_{b,I}\frac{s_{b,I}(s_{b,I}+1)}2,\quad
 S=\max_{b,I}s_{b,I}.
\]

Let `M` be the number of distinct global monomials supported by some bag
and having total degree at most `2r`. The expanded coefficient map is

\[
 \mathcal A(Q)=\sum_{b,I}g_{b,I}\,v_{b,I}^{T}Q_{b,I}v_{b,I}.
                                                               \tag{2}
\]

Each output coefficient is represented in the monomial basis, collecting
equal global monomials from different bags. The independent variables are
the `V` upper triangular Gram entries. The map is rational, with integer
entries of magnitude at most two. Expanding a single column has at most
`2^w` nonzero coefficients. These dimensions include all local preordering
products; a reduced term-sparsity Gram basis is not covered automatically.

**Theorem.** Under (1), there are rational symmetric matrices satisfying

\[
 \mathcal A(Q)=p,\qquad Q_{b,I}\succeq\frac{\tau}{2D}I.
                                                               \tag{3}
\]

Their total binary encoding length is polynomial in the expanded finite
dimensions `V,M`, the rational input length, and `log^+(1/tau)`. They can be
constructed in deterministic polynomial time in those quantities under
promise (1). Here `log^+(z)=max(0,log_2 z)`. The input includes the bags,
monomial coefficients, `r`, `gamma`, and `tau`; the guarantee is polynomial
in the expanded finite dimensions, not in `log r` alone.

It suffices more generally that `p-tau` have a real certificate of form (2)
with positive semidefinite Grams. The tree and kernel theorem are used only
to establish that sufficient condition from (1).

## 2. A diagonal positive definite Gram certificate for one

For one local diagonal term `h=x^(2alpha) g_I`, where
`|alpha|+|I| <= r`, write the coordinates of the bag as `1,...,k` and list
`I={i_1,...,i_s}` in increasing order. There is an elementary identity

\[
\begin{split}
1-x^{2\alpha}g_I
={}&\sum_{i=1}^k\sum_{j=0}^{\alpha_i-1}
 \left(x_1^{\alpha_1}\cdots x_{i-1}^{\alpha_{i-1}}x_i^j\right)^2
 (1-x_i^2)\\
 &+\sum_{q=1}^s(x^\alpha x_{i_q})^2
             \prod_{\ell<q}(1-x_{i_\ell}^2).
                                                               \tag{4}
\end{split}
\]

The first line is `1-x^(2alpha)` and the second is
`x^(2alpha)(1-g_I)`. Each term is a monomial square times a squarefree
generator product. Its total degree is at most `2(|alpha|+|I|)<=2r`.
In particular, this proof does not require converting repeated generators
into squares.

Apply `1=h+(1-h)` to every allowed diagonal position of every block in
every bag, sum the `D` identities, and divide by `D`. The result is a tuple
of diagonal rational matrices `H` satisfying

\[
 \mathcal A(H)=1,\qquad H_{b,I}\succeq D^{-1}I,
 \qquad\sum_{b,I}\operatorname{tr}H_{b,I}\le r+1.        \tag{5}
\]

Every position receives its own positive baseline contribution. Each
source identity has `1+|alpha|+|I|<=r+1` monomial-square terms, which proves
the trace bound. The diagonal numerators before division by `D` are
nonnegative integers at most `D(r+1)`, a sufficient polynomial-bit bound.
All of (5) can be constructed with `O(Dr)` term additions once the bases
are enumerated.

The core theorem and finite SDP dual attainment give
`f-rho_r=mathcal A(G)` with `G>=0`, and `rho_r>=f*-E_r`.
Consequently `p-tau` has a positive semidefinite certificate under (1).
Adding `tau H` gives a real feasible tuple `Q*` with

\[
 Q^*_{b,I}\succeq\eta I,\qquad \eta=\tau/D.              \tag{6}
\]

The strictly feasible tuple need not be supplied to the construction
algorithm. Only its existence and the explicit margin are used below.

## 3. A polynomial-bit outer bound from rational moments

Let `ell` denote expectation under product uniform measure on `[-1,1]^n`.
For every local block define

\[
 W_{b,I}=\ell(g_{b,I}v_{b,I}v_{b,I}^{T}).                \tag{7}
\]

These are rational positive definite matrices: for a nonzero polynomial
`q`, the integral of `g_I q^2` is strictly positive because the weight is
positive in the open box. Their entries are products of univariate
integrals. For even `a` those factors are

\[
 \ell(x^a)=\frac1{a+1},\qquad
 \ell(x^a(1-x^2))=\frac2{(a+1)(a+3)};                  \tag{8}
\]

for odd `a` they are zero. Here all needed `a` satisfy `a<=2r`.
The integer

\[
 q_0=((2r+3)!)^{2w}
\]

clears every denominator in every `W`. Each diagonal entry is at most one.
If `W` has size `s`, its positive determinant is at least `q_0^(-s)` and
its trace is at most `s`. The product of its other `s-1` eigenvalues is at
most `s^(s-1)`, hence

\[
 W_{b,I}\succeq\lambda_0 I,\qquad
 \lambda_0=q_0^{-S}S^{-(S-1)}.                         \tag{9}
\]

Take the last factor to be one when `S=1`. The encoding length of
`lambda_0` is `O(Swr log(r+2)+S log(S+1))`, which is polynomial in the
finite dimensions. No useful numerical condition number is asserted.

Write `C=||p||_1` for the sum of absolute monomial coefficients. Every
positive semidefinite tuple with `mathcal A(Q)=p` satisfies

\[
 \lambda_0\sum_{b,I}\operatorname{tr}Q_{b,I}
 \le\sum_{b,I}\operatorname{tr}(W_{b,I}Q_{b,I})
 =\ell(p)\le C.
                                                               \tag{10}
\]

The equality uses the same global product measure for every bag, so
overlaps cause no issue. Thus the aggregate Frobenius norm is at most
`C/lambda_0`. Set `R=1+C/lambda_0`; `R` is a computable rational outer
bound with polynomial encoding length. In particular, the real tuple
`Q*` in (6) has all entries of magnitude less than `R`.

## 4. Exact coefficient correction and short rational witnesses

The map `mathcal A` has an explicit rational right inverse on its output
space. Given an output monomial `x^beta`, choose one containing bag and
split `beta=alpha+delta` with `|alpha|,|delta|<=r`. This is possible because
`|beta|<=2r`. In that bag's empty-generator block, use one diagonal entry
of value one if `alpha=delta`, or the two symmetric entries of value
`1/2` otherwise. Denote the resulting tuple by `Z_beta`; then

\[
 \mathcal A(Z_\beta)=x^\beta,\qquad \|Z_\beta\|_F\le1.
\]

Distinct output monomials use distinct matrix positions, since a position
has a unique exponent sum. Extending linearly gives `Z` with

\[
 \mathcal A Z=\operatorname{id},\qquad
 \|Z(c)\|_F\le\|c\|_1.                                \tag{11}
\]

Round each upper triangular entry of `Q*` to a multiple of `h=2^(-B)`,
with absolute error at most `h`. Call the resulting rational tuple `Q0`.
Symmetric off-diagonal entries are rounded together. Then

\[
 \|Q0-Q^*\|_F\le2Vh,\qquad
 \|\mathcal A(Q0-Q^*)\|_1\le2^{w+1}Vh.
\]

The second inequality counts at most `2^w` generator-expansion monomials
per Gram coordinate, each with coefficient of magnitude at most two.
Set

\[
 Q=Q0+Z(p-\mathcal A(Q0)).                              \tag{12}
\]

This enforces every coefficient equality exactly. By (11),

\[
 \|Q-Q^*\|_F\le 2^{w+2}Vh.
\]

Choose `B>=0` so that

\[
 2^{-B}\le\frac{\eta}{2^{w+3}V}.                       \tag{13}
\]

Then each block remains at least `eta/2` positive definite. Entries of
`Q0` have encoding length `O(B+log(R+1))`; exact correction uses only
polynomially many rational operations on those entries and the input.
Their denominators divide twice the least common multiple of `2^B` and
the input coefficient denominators, which has polynomial bit length.
This proves the short-witness assertion independently of an SDP solver.

Rounding an unknown real witness is an existence proof, not yet an
algorithm. The next section supplies a separate construction.

## 5. Polynomial-time construction under the slack promise

Choose the pivot position used by each `Z_beta` in Section 4. Each pivot
column of `mathcal A` has one nonzero entry, equal to one or two, in its
own row. There are `M` such distinct positions. Let `y` contain the
remaining `k=V-M` Gram coordinates. If `U(y)` inserts these free
coordinates and puts zero in every pivot position, define

\[
 Q(y)=Z(p)+U(y)-Z(\mathcal A(U(y))).                    \tag{14}
\]

Every tuple in the affine space `mathcal A(Q)=p` appears exactly once.
In particular, `Q(y*)=Q*`, where `y*` consists of the corresponding free
entries of `Q*` and `|y*_j|<R`.

Each free-coordinate column of the linear part in (14) has aggregate
Frobenius norm at most `2+2^(w+1)<=2^(w+2)`. Therefore

\[
 \|Q(y+z)-Q(y)\|_F\le\beta\|z\|_2,
 \qquad \beta=2^{w+2}V.                                \tag{15}
\]

For `k>0`, search the convex body

\[
 K=\{y\in[-R-1,R+1]^k:
                  Q_{b,I}(y)\succeq(\eta/2)I\ \forall b,I\}.
\]

It contains the Euclidean ball centered at `y*` of radius

\[
 a=\min\{1,\eta/(2\beta)\},                            \tag{16}
\]

and lies in a ball centered at zero of radius `k(R+1)`. Both radii are
known rationals with polynomial encoding length. The center `y*` need
not be known. If `k=0`, the unique tuple `Z(p)` is rational and satisfies
the promised margin, so direct evaluation handles the case.

There is an exact rational polynomial-time strong separation oracle for
`K`. Check the box inequalities, then test each rational symmetric matrix
`Q_{b,I}(y)-(eta/2)I` for positive semidefiniteness using rational symmetric
elimination. If one fails, elimination supplies a rational vector `v`
with negative quadratic value. The inequality

\[
 v^T(Q_{b,I}(z)-(\eta/2)I)v\ge0
\]

is a rational separating linear inequality in `z`. One can obtain such
a vector by successive positive diagonal pivots and Schur complements;
a negative diagonal gives a witness immediately, and a remaining matrix
with zero diagonal and a nonzero off-diagonal entry has a witness of the
form `e_i+e_j` or `e_i-e_j`. Back substitution preserves polynomial bit
length by the usual determinant bounds for rational elimination.

For `k=1`, rational interval bisection supplies the same conclusion. For
`k>=2`, the rational ellipsoid algorithm with this strong separation oracle
and the stated enclosing radius finds a point in `K` in polynomial time in
`k`, the oracle input length, and `log(k(R+1)/a)`. This is the standard
strong-feasibility volume argument: a sequence of separating cuts cannot
shrink an enclosing ellipsoid below the volume of the promised radius-`a`
ball while preserving `K`. Rational implementation includes the standard
rounding of ellipsoid updates, which keeps query encoding lengths
polynomial in the data and the radius bounds; each oracle call is
polynomial in its query length. Exact-real iteration counts alone would
not establish a bit-complexity result. Applying (14) to the resulting
rational point proves (3) constructively.

The algorithm does not have to verify the promise involving `f*`. Under
that promise it succeeds; outside it, failure within the prescribed
iteration bound does not prove that a certificate is impossible. A
returned certificate can always be checked independently without (1).

Rational Gram matrices are the stated output. Exact rational `LDL^T`
factorization gives positive rational weighted polynomial squares.
Producing those factors is optional: the polynomial identity and PSD
tests already give a complete rational checker. If unweighted rational
squares are wanted, each positive rational weight `a/b` can be expanded
as `ab/b^2` and the binary expansion of `ab` converted into at most twice
its bit length many integer squares. This also gives polynomial total
encoding length, without asserting four squares per weight or requiring
an integer factorization algorithm.

## 6. Ordinary sparse quadratic-module corollary

The same rational conclusion holds for the ordinary sparse box quadratic
module. This extension uses a real membership promise and does not depend
on any particular convergence theorem or its constants.

Fix `r>=1`, rational `p`, and rational `tau>0`. Suppose

\[
 p-\tau=\sum_b\left\{
    v_{b,0}^{T}G_{b,0}v_{b,0}
    +\sum_{i\in B_b}(1-x_i^2)v_{b,i}^{T}G_{b,i}v_{b,i}
                     \right\},\qquad G_{b,i}\succeq0,             \tag{17}
\]

where `v_(b,0)` contains all bag monomials of degree at most `r`, and
`v_(b,i)` contains all bag monomials of degree at most `r-1`. Let
`D_Q` be the sum of these matrix sizes and `V_Q` the number of their
independent upper triangular entries. Then there are rational matrices
of the same sizes representing `p` exactly and satisfying

\[
 Q_{b,i}\succeq\frac{\tau}{2D_Q}I.                              \tag{18}
\]

Their encoding length and deterministic construction time are polynomial
in the expanded module dimensions, rational data length, and
`log^+(1/tau)`. Under the direct membership promise (17), the bags need not
satisfy a running-intersection property.

To prove this, restrict the source diagonal terms in Section 2 to
`I=emptyset` and `I={i}`. Formula (4) stays within these blocks: its first
telescope uses only singleton generators, and its second telescope has
one empty-generator term when `I` is a singleton. Thus averaging over
the `D_Q` allowed positions supplies an ordinary-module representation of
one with every Gram block at least `I/D_Q`. All later arguments use only
this interior direction, the blockwise rational uniform moments, and the
empty-generator blocks for coefficient correction. Those ingredients
remain present. A Gram coordinate now expands into at most two monomials,
so the coefficient bounds can only improve.

For `p=f-gamma`, any proved bound `f*−rho_r<=E` with real dual attainment
implies (17) whenever `f*−gamma>=E+tau`. In particular,
[sparse-putinar-kernel.md, Section 6](sparse-putinar-kernel.md#6-sparse-polynomial-certificate-consequence)
supplies a real certificate using its stated finite-order bound
`E_(s,N)` and its own order assumptions. The rational conclusion here is
conditional on that real membership; it imports no unreviewed improvement
of the rate or constants. The extension is another specialization of
established strict-feasibility rational SOS methods, not a separate
novelty claim.

## 7. What is established and what remains

The theorem proves that quantitative sparse box lower bounds admit short
exact certificates, and gives a theoretical rational construction. The
slack `tau` places the certificate inside every full local Gram cone;
strict positivity of `p` alone at a prescribed order is not used as a
substitute for this stronger fact. Exact equality at the kernel error
threshold (`tau=0`) is outside the rational-size result.

A practical pipeline could use a numerical SDP, reserve objective slack,
round its Gram output, and apply (12). This becomes a proved checker when
the resulting rational matrices pass exact PSD tests. The theorem does
not guarantee that a particular solver returns a tuple with the needed
margin or accuracy, and the explicit moment bound (9) is intentionally
conservative. Measuring conditioning, selecting bases, and implementing
a useful recovery pipeline remain practical work.

The results cover the full local box preordering and, under (17), the
ordinary local box quadratic module. Additional constraints and reduced
Gram bases need their own interior certificates and bounds. Overlapping
bags pose no additional
rationality obstruction here because the output is one global polynomial
identity and the trace estimate uses one global product measure.

## 8. Prior work and verification

- [Peyrl and Parrilo (2008), *Computing sum of squares decompositions with
  rational coefficients*](https://www.mit.edu/~parrilo/pubs/files/PeyrlParrilo-ComputingSumOfSquaresDecompositionsWithRationalCoefficients.pdf)
  prove rational recovery from sufficiently accurate approximate Gram
  matrices under strict feasibility, with quantitative rounding and
  projection conditions. Section 4 specializes that established strategy;
  it is not a new general rational SOS method.
- [Davis and Papp (2024), *Rational dual certificates for weighted
  sums-of-squares polynomials with boundable bit size*](https://arxiv.org/abs/2305.19039)
  provide general bit-size bounds and rational algorithms for weighted SOS
  certificates, using dual certificates that recover rational Grams.
  Theorem 2.9 bounds integer dual certificates using an interior direction,
  distance to the cone boundary, and an evaluation-matrix condition number;
  Section 5 explicitly discusses correlative sparsity. The present note
  uses ordinary Grams and elementary explicit box bounds; no superiority
  to their general method is claimed.
- [Magron and Safey El Din, *On Exact Reznick, Hilbert-Artin and Putinar's
  Representations*](https://arxiv.org/abs/1811.10062)
  analyze perturbation and compensation methods for exact rational
  representations. Their general bounds address cases where a
  quantitative strict Gram margin is not supplied as it is here. Earlier
  versions of their complexity claims were corrected; comparison should
  use this revised report.
- [de Klerk and Vallentin (2016), *On the Turing model complexity of
  interior point methods for semidefinite programming*](https://arxiv.org/abs/1507.03549)
  make the arithmetic-model distinction explicit. Their stated theorem
  assumes a known rational feasible starting point, so it cannot directly
  be used to construct the first rational point here. Section 5 instead
  gives a strong-feasibility ellipsoid reduction with explicit radii.
- The underlying ellipsoid framework is due to Grötschel, Lovász and
  Schrijver; see their book *Geometric Algorithms and Combinatorial
  Optimization*, Chapter 3, the primary survey
  [*Geometric Methods in Combinatorial Optimization*](https://ir.cwi.nl/pub/10155/10155D.pdf),
  Section 1 and the first phase in the proof of Theorem 2.13,
  and the authors' account in
  [*The Mathematics of László Lovász*](https://www.zib.de/userpage/groetschel/pubnew/groetschel-nesetril.pdf).
  The essential assumption used here is a known positive lower bound on
  the radius of a ball contained somewhere in the feasible body, together
  with strong separation and a known enclosing radius.

These sources establish that the broad exact-rational conclusion is prior
methodology. The useful addition to the sparse kernel theorem is a complete
quantitative route from its objective error bound to an exact certificate,
with all finite-SDP conditioning assumptions discharged for this box cone.
No unsuccessful literature search is treated as evidence of novelty.

The exact targeted command
`python research-20260928/solver/check_rational_sparse_certificates.py`
passed 335 individual telescoping identities, 13 rational moment-matrix
lower-bound checks, all 25 monomial right-inverse checks for two overlapping
width-two bags, and an exact rational rounding/correction example with
`D=26,V=68`, including its claimed positive definite margin.
It also passed 272 telescoping identities using only the ordinary
quadratic-module blocks, checking closure of the restricted construction.
It also checks the corrected denominator bound when an input denominator
has more factors of two than the rounding grid. The whole-proof reviewer
identified that factor-of-two omission in an earlier draft; it was corrected
and independently checked by exact arithmetic before this test was added.

Two independent subagents checked the constant identity and the general
polynomial-time feasibility reduction. A separate whole-proof review is
recorded in [rational-certificates-review.md](rational-certificates-review.md).
The computational checks concern finite examples only. They do not verify
the full symbolic theorem, implement an ellipsoid method, establish a
practical solver runtime, or replace adversarial proof review. No Lean
formalization, project-wide verification, or CI inspection was used.
