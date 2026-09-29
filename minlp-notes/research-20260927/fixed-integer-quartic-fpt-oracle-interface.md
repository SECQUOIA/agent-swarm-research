# Rational rounding and scalar MILP interfaces for a possible FPT bound

Date: 2026-09-28. Status: primary-source audit and detailed deductions.
The scalar-MILP source statement and reduction were independently checked
by a separate agent. The rounding and width-height deduction still needs
fresh independent review. No claim of novelty is made for these tools.
This note does not establish an FPT version of
[the mixed-integer quartic theorem](fixed-integer-strong-quartic-posslp.md).

A subsequent [integer-query source audit](integer-query-convex-oracle-prior.md)
identified a more direct FPT feasibility interface. The construction
below remains a useful explicit alternative, but is not presently the
preferred route to the complete quartic extension.

The fixed-dimension proof currently enumerates polytope vertices to
compute minimum lattice width. That can introduce a factor \(m^{O(k)}\)
for \(m\) rows and \(k\) integer variables. An approximate width
direction suffices for its dimension-dependent branching bound. The
classical rounding and LLL methods below compute such a direction without
enumerating all vertices. Their output coefficient heights are linear in
the input height, up to factors depending only on dimension. This last
property is useful when the direction enters an affine lattice recursion.

Throughout, the height of a rational number means the maximum binary
length of its reduced numerator and positive denominator. Let
\(P=\{x\in\mathbb R^d:Ax\le b\}\) be a nonempty, bounded,
full-dimensional rational polytope with \(m\) rows and individual
coefficient heights at most \(H\ge1\). Write

\[
 w(P,v)=\max_{x\in P}v^{\mathsf T}x-
             \min_{x\in P}v^{\mathsf T}x,\qquad
 w(P)=\min_{0\ne v\in\mathbb Z^d}w(P,v).
\]

## 1. The precise primary rounding result

[H. W. Lenstra, *Integer Programming with a Fixed Number of
Variables*](https://pub.math.leidenuniv.nl/~lenstrahw/PUBLICATIONS/1983i/art.pdf),
Section 2, printed pp. 541--544, constructs an initial full-dimensional
simplex using linear optimization, then replaces a simplex vertex by a
polytope vertex whenever the volume increases by more than a factor
\(3/2\). At termination every barycentric coordinate on \(P\) has
absolute value at most \(3/2\). Remark (a), p. 544, permits a fixed
rational simplex instead of a regular simplex. Remark (b) explicitly
states that this rounding algorithm is polynomial even when dimension
varies. This is a statement about its rounding subroutine; the paper's
overall running-time discussion on p. 538 gives a polynomial degree
depending on dimension and should not itself be quoted as the desired
FPT bound.

Here are the needed rational form and height bounds, derived directly
from that construction. They are not a separately stated theorem in the
source.

Choose a vertex \(p_0\). If the selected vertices span a proper affine
subspace, optimize linear functionals spanning its orthogonal complement
in both signs. Full dimensionality supplies a new vertex outside that
subspace. After at most \(d\) stages this gives vertices
\(p_0,\ldots,p_d\) spanning a simplex. All chosen LP optima can be
required to be vertices.

For this simplex let \(\lambda_0(x),\ldots,\lambda_d(x)\) be its
affine barycentric coordinate functions. Optimize each \(\lambda_i\)
and \(-\lambda_i\) over \(P\). If some vertex \(p\) has
\(|\lambda_i(p)|>3/2\), replace \(p_i\) by \(p\). The determinant
formula for simplex volume multiplies volume by \(|\lambda_i(p)|\),
so this process terminates with

\[
                 |\lambda_i(x)|\le3/2
           \quad(x\in P,\ 0\le i\le d).                 \tag{1}
\]

Set

\[
 S=[p_1-p_0\ \cdots\ p_d-p_0],\quad
 c=\frac1{d+1}{\bf1},\quad
 r=\frac1{d(d+1)},\quad
 a=p_0+Sc,\quad D=rS.
\]

The standard simplex contains \(c+rB_2^d\): each coordinate remains
nonnegative, while its coordinate sum is at most
\(d/(d+1)+\sqrt d\,r\le1\). In the coordinates
\(u=S^{-1}(x-p_0)\), (1) gives \(|u_i|\le3/2\), hence
\(\|u-c\|_2\le2\sqrt d\le2d\). Consequently

\[
 a+DB_2^d\ \subseteq\ P\ \subseteq\
 a+\beta_d DB_2^d,
 \qquad \beta_d=2d^2(d+1).                              \tag{2}
\]

Both \(a\) and the nonsingular matrix \(D\) are rational. The loose
factor \(\beta_d\) is sufficient here and avoids rational square-root
issues entirely.

### Height and running time

Clear denominators separately in each original row. The resulting
integer coefficient heights are \(O(dH)\). Every vertex is determined
by \(d\) independent tight rows. Cramer's rule and Hadamard's
inequality therefore bound each vertex-coordinate height by

\[
                         O(d^2(H+\log(d+1))).            \tag{3}
\]

This bound is independent of the number of rows. In particular, it
applies to every vertex selected by the iterative algorithm. Rational
matrix inversion shows that all current barycentric functions have
height \(a_1(d)(H+1)\) for a fixed polynomial \(a_1\). Formula (3)
also bounds the height of the final \(a,D\) by
\(a_2(d)(H+1)\).

The initial nonzero simplex determinant is at least
\(2^{-a_3(d)(H+1)}\). All vertices lie in a box of radius
\(2^{a_4(d)(H+1)}\), so the volume of \(P\) is at most
\(2^{a_5(d)(H+1)}\). Every replacement multiplies simplex volume by
more than \(3/2\). Thus there are at most
\(a_6(d)(H+1)\) replacements, each using \(2(d+1)\) rational LPs
with controlled coefficient heights. Rational linear programming has
polynomial bit complexity with an absolute exponent. Hence the entire
construction takes \(a_7(d)[m(H+1)]^C\) time for an absolute constant
\(C\), without a factor \(m^{d}\). It produces the stronger
linear-in-height output bound above.

## 2. LLL turns the rounding into an approximate width direction

Use the rational lattice \(D^{\mathsf T}\mathbb Z^d\). Choose a
positive integer \(Q\) clearing all denominators of \(D\), and apply
LLL to the integer basis matrix \(A=QD^{\mathsf T}\). If \(b_1\)
is its first reduced basis vector, compute

\[
                            v=A^{-1}b_1.
\]

Then \(v\in\mathbb Z^d\setminus\{0\}\).
[Lenstra--Lenstra--Lovász, *Factoring Polynomials with Rational
Coefficients*](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Lovasz/LovaszLenstraLenstrafactor.pdf),
Proposition 1.11, gives
\(\|b_1\|_2\le2^{(d-1)/2}\lambda_1(A\mathbb Z^d)\).
Proposition 1.26 states \(O(d^4\log B)\) arithmetic operations on
integers of length \(O(d\log B)\), when the input squared basis
norms are at most \(B\ge2\). These statements were read from the
scanned primary text: reprint pp. 30 and 34, PDF pages 4 and 8.

The ellipsoid width is \(2\|D^{\mathsf T}v\|_2\). Combining the
LLL guarantee with (2) gives

\[
 \begin{split}
 w(P,v)
 &\le2\beta_d\|D^{\mathsf T}v\|_2\\
 &\le\beta_d2^{(d-1)/2}
           \min_{0\ne u\in\mathbb Z^d}2\|D^{\mathsf T}u\|_2\\
 &\le\beta_d2^{(d-1)/2}w(P)
 \le\Gamma_d w(P),\qquad
 \Gamma_d:=2^{d+1}d^2(d+1).                             \tag{4}
 \end{split}
\]

This is an approximation to minimum width, not necessarily a minimum
direction. If a separate flatness argument establishes
\(w(P)\le\Phi_d\), the integer levels of \(v^{\mathsf T}x\)
intersecting \(P\) number at most
\(\lfloor\Gamma_d\Phi_d\rfloor+1\). Their endpoints are computed
by rational LP.

The denominator-clearing integer \(Q\) has height at most \(d^2\)
times the maximum entry height of \(D\). Therefore
\(\log B\le a_8(d)(H+1)\), and Proposition 1.26 bounds the
coordinates of \(b_1\) by the same linear-in-height form. Cramer's
rule applied to \(A^{-1}b_1\) then bounds each coordinate height of
\(v\) by

\[
                             a_9(d)(H+1).               \tag{5}
\]

One may divide \(v\) by the gcd of its entries to obtain a primitive
direction; this can only decrease its width and coordinate sizes.
Thus the required width interface has deterministic time
\(a(d)[m(H+1)]^C\), with a universal exponent, and linear height
growth (5). Computing the rational lattice coefficient vector through
\(A^{-1}b_1\) avoids needing a separate complexity statement about
the unimodular transformation recorded by an LLL implementation.

## 3. A primary FPT integer-optimization theorem

[Hildebrand--Köppe, *A new Lenstra-type Algorithm for Quasiconvex
Polynomial Integer Minimization*](https://arxiv.org/pdf/1006.4661v3),
Theorem 1.1, manuscript p. 2, gives, in its general case, time
\(s\ell^{O(1)}d^{O(n)}2^{2n\log_2n+O(n)}\) and output size
\(\ell d^{O(n)}\). The input is a sparse list of quasiconvex integer
polynomials, degree bounded by \(d\ge2\), coefficient length bounded
by \(\ell\). Its algorithm is deterministic; Section 3.4 and
Theorem 3.7 provide deterministic lattice subroutines.

For linear integer optimization set the degree bound to two. Clear
rational rows separately. An integer weak row \(q(x)\le0\) is
equivalent to the strict row \(q(x)-1<0\). This yields deterministic
time \(a(n)s(\ell+1)^C\) with an absolute exponent \(C\), and a
returned optimal point of height \(a(n)(\ell+1)\), whenever an
optimum exists. For the proposed application, all nonempty optimization
calls have finite attained optima; a distinction between unboundedness
and infeasibility is not being imported from a statement that merely
reports absence of a minimum.

The theorem's primary statement and its specialization were checked
independently by a second agent. This is a convenient precise FPT source
and avoids attributing a stronger overall running-time statement to
Lenstra's 1983 article than the article itself states.

## 4. Only one continuous scalar is needed in the MILP subroutine

The central-point MILP in the current quartic proof has integer
\(x\in\mathbb Z^d\) and one continuous scalar \(t\). The following
elementary reduction suffices; a theorem allowing arbitrarily many
continuous MILP variables is unnecessary for that proof.

Consider rows

\[
                    a_j^{\mathsf T}x+b_jt\le c_j
                         \quad(1\le j\le m).             \tag{6}
\]

Assume maximization of \(t\) has a finite attained optimum. For a
fixed feasible integer \(x\), its largest feasible scalar is the
smallest upper endpoint among rows with \(b_i>0\). In particular,
at a global optimum some such row is tight. Enumerate these rows and
substitute

\[
                         t=\frac{c_i-a_i^{\mathsf T}x}{b_i}
\tag{7}
\]

into every row and the objective. Each case becomes pure linear integer
optimization in \(d\) variables with at most \(m\) constraints.
Every feasible candidate is feasible for (6), and an optimum of (6)
occurs in at least one case. For minimization of \(t\), use the rows
with \(b_i<0\) instead. Rows with \(b_i=0\) remain ordinary integer
linear constraints.

If the original rational coefficients have height at most \(H\), the
substitution followed by rowwise denominator clearing gives height
\(O(d(H+1))\). It does not require a common denominator over all
\(m\) rows. Applying Section 3 to every case gives total time

\[
                         a(d)m^2(H+1)^C,                 \tag{8}
\]

and an optimal \((x,t)\) whose coordinate heights are at most
\(a(d)(H+1)\). The exponent \(C\) is absolute. This endpoint
reduction and its assumptions were independently reconstructed by the
second agent. It also applies to a width-epigraph MILP, though Section 2
now provides the preferable width computation without enumerating its
vertices.

## 5. What is still needed for the quartic FPT claim

These interfaces remove two specific obstacles: the \(m^{O(k)}\)
vertex enumeration, and an unspecified fixed-dimensional MILP exponent.
They do not by themselves justify the FPT conclusion for the complete
nonlinear algorithm.

In particular, the new cutting normals must have height bounded
linearly in a suitable measure of the current node's coefficient heights
and coordinate-radius logarithm. A merely polynomial height bound,
iterated \(k\) times, can produce an input-size exponent depending on
\(k\). Rounding approximate gradients to a controlled dyadic grid is
a plausible way to enforce the stronger bound, while preserving the
integer-cut margin. It must be proved with the chosen constants.

The integer affine parametrizations must also have height
\(a(k)(H+1)\), and the representation of the transformed quartic must
avoid multiplying its height by the variable continuous dimension at
every recursion level. Tracking one denominator for the original
quartic and using only integral affine substitutions may address this.
The nonlinear oracle costs and the size of every PosSLP query must be
bounded in terms of the resulting encoding, with an absolute polynomial
exponent. These are obligations of a separate full proof and review.

## 6. Verification record

Read Lenstra's complete Section 2 and Remarks (a)--(b) from the primary
PDF, including its use of vertices rather than arbitrary approximate LP
points. The LLL PDF is image-only: rendered and inspected PDF pages
3--4 and 7--9, particularly Propositions 1.11 and 1.26. Read
Hildebrand--Köppe's theorem from the existing local primary text; a
second agent independently verified its precise bounds and deterministic
subroutines. Source files and rendered pages used for the LLL inspection
were stored temporarily under `/tmp/minlp-fixed-k-fpt-sources/`.

Targeted checks: exact arithmetic for the rational standard-simplex
inradius inequality and dimension-only factors for \(1\le d\le32\);
Markdown local links, final newline, and trailing whitespace;
`git diff --check --
research-20260927/fixed-integer-quartic-fpt-oracle-interface.md`.
These checks passed. They do not verify the source algorithms or the
complete FPT reduction. No project-wide checks or CI inspection occurred.
