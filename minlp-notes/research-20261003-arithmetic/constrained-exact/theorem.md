# Exact constrained quartic optimization with few nonlinear directions

Date: 2026-10-03. Status: proof developed in this note; independent review
is recorded in `verification.md`. Publication priority is unestablished.

The general deterministic \(\mathrm P^{\mathrm{PosSLP}}\) classification
for strongly convex quartics over arbitrary rational polyhedra remains open
in this research program. This note establishes a different positive
result: exact comparison is fixed-parameter tractable in the dimension of
the part of the objective of degree at least three. There is no restriction
on constraint rank, and no exact-comparison oracle is used.

## 1. An intrinsic parameter and the theorem

Write an explicit rational quartic as
\[
 f(x)=q(x)+r(x),\qquad \deg q\le2,
\]
where \(r\) consists of its monomials of degrees three and four. Define
\[
 K=\{v\in\mathbb R^n:D_vr\equiv0\},\qquad k=n-\dim K.
 \tag{1}
\]
We call \(k\) the **nonlinear dimension**. It measures nonlinear directions,
not the rank of the quadratic Hessian and not the number of nonlinear
monomials. Translation changes lower-degree terms but does not change the
subspace in (1): invariance of the third and higher derivatives gives the
same subspace after translation.

The essential-variable rank construction is established algebraic structure;
see [Carlini, Proposition 1](https://arxiv.org/pdf/math/0507531) for the
homogeneous case. Here it is applied degreewise to the cubic and quartic
pieces. The definition is effective over the rationals. Form a matrix whose row
indexed by a monomial \(x^\beta\) of degree two or three is the coefficient
vector of that monomial in \(\nabla r\). Then \(K\) is its nullspace and
\(k\) its rational rank. There are polynomially many entries for fixed
degree. A rational row basis \(U\in\mathbb Q^{k\times n}\) and rational
right inverse \(V\) have polynomial encoding length. The identity
\[
 r(x)=g(Ux),\qquad g(t)=r(Vt),                         \tag{2}
\]
follows because \(x-VUx\in K\) and \(r\) is constant on every line in a
direction in \(K\). Fixed-degree substitution constructs \(g\) in
polynomial time. Thus (1) needs no supplied decomposition.

**Theorem 1.** Let \(P=\{x:Ax\le b\}\) be an explicit rational polyhedron,
and let an explicit rational polynomial \(f\) of degree at most four have
a supplied rational \(\mu>0\) satisfying
\[
                    \nabla^2 f(x)\succeq\mu I\quad(x\in\mathbb R^n).
 \tag{3}
\]
Let \(h\) be any explicit rational polynomial of degree at most four, and
let \(L\ge2\) be total input encoding length. There are a computable
function \(F\) and an absolute constant \(C\) such that a deterministic
ordinary bit algorithm, in time \(F(k)L^C\), either reports \(P\) empty or
decides the sign of \(h(p)\), where \(p\) is the unique minimizer of
\(f\) on \(P\). Here \(k\) is (1).

Consequently all exact value, coordinate, and equality comparisons are
ordinary fixed-parameter tractable in \(k\). The theorem also computes
the full active set and an exact description of \(p\) as an affine image
of the unique stationary point of a rational strongly convex quartic in
at most \(k\) variables. The description is implicit; its coordinates
need not be rational.

The number of inequalities, their rank, and the ambient dimension are
unrestricted. Empty interiors, redundant inequalities, zero normals,
unbounded polyhedra, and zero optimal multipliers are allowed. Condition
(3) is a promise. A supplied rational positive semidefinite Gram for the
biform \(v^{\mathsf T}(\nabla^2 f(x)-\mu I)v\) gives a checkable
certificate subclass: check its coefficient identity and rational positive
semidefiniteness. This does not assert that every strongly convex quartic
has such a Gram. Unlike requiring a full positive definite Hessian Gram,
this format permits the low nonlinear dimensions central to the theorem.

The parameter function is not optimized. A singly exponential
quantifier-elimination bound gives a computable bound of the form
\(F(k)=(k+2)^{O(k)}\), after enlarging absolute constants; the FPT statement
does not require this sharper form.

## 2. The active face removes all but k algebraic variables

First assume \(P\ne\varnothing\). Coercivity from (3) gives a unique
minimizer \(p\). Let \(S\) be the full set of tight constraints at \(p\),
and let
\[
 E=\{x:A_Sx=b_S\}.
\]
Polyhedral optimality gives \(-\nabla f(p)\) in the cone of the active
normals. Therefore \(p\) is stationary on \(E\), and by (3) is the
unique unconstrained minimizer of \(f|_E\). This uses no constraint
qualification. The unknown set \(S\) is used only to prove a bound; the
algorithm below does not guess or enumerate it.

Choose a rational free-coordinate chart \(x=\bar x+Zy\) for \(E\).
The chart uses an independent subset of at most \(n\) input rows, so
all entries have uniformly polynomial bit length in \(L\), independent
of which subset is chosen. Put \(d=\dim E\) and
\(s=\operatorname{rank}(UZ)\le k\). Choose rational matrices \(T,W\)
such that \([T\ W]\) is invertible, \(W\) spans \(\ker(UZ)\), and
\(T\) has \(s\) columns. Then
\[
 x=\bar x+ZTt+ZWw,\qquad t\in\mathbb R^s,
 \quad w\in\mathbb R^{d-s}.                           \tag{4}
\]
The term \(g(Ux)\) is independent of \(w\). Write
\[
 f(\bar x+ZTt+ZWw)
 =\tfrac12w^{\mathsf T}Hw+w^{\mathsf T}(Jt+a)+\psi(t).
 \tag{5}
\]
All coefficients are rational of polynomial encoding length, and
\(\psi\) has degree at most four. Strong convexity gives
\[
 H\succeq\mu (ZW)^{\mathsf T}(ZW)\succ0
\]
when \(w\) is nonempty. Thus for each \(t\) the unique minimizing
\(w\) is
\[
 w(t)=-H^{-1}(Jt+a).                                   \tag{6}
\]
This makes \(x(t)=u+Dt\) a rational affine map with polynomial-bit
coefficients. Its linear part has full column rank: \(UZT\) has rank
\(s\), while \(UZW=0\). Define
\[
 \phi(t)=f(u+Dt),\qquad \eta(t)=h(u+Dt).               \tag{7}
\]
They are explicit degree-four polynomials with polynomial-bit
coefficients. Moreover \(\phi\) is globally strongly convex because
\(\nabla^2\phi\succeq\mu D^{\mathsf T}D\succ0\). If \(t_*\) is its
unique stationary point, then
\[
                     p=u+Dt_*,\qquad h(p)=\eta(t_*).
 \tag{8}
\]
The cases \(d=0\), \(s=0\), and \(d=s\) omit their empty blocks. In
particular \(s=0\) makes \(p\) a polynomial-bit rational point.

For completeness, all asserted coefficient bounds have absolute
polynomial exponents. There are a fixed number of rational nullspace,
row-basis, inverse, and fixed-degree substitution operations, each on
matrices of order at most \(L\) with polynomial-bit entries. Determinant
bounds control elimination bit growth. Expanding a degree-four affine
substitution adds at most a fourth-power number of terms. These bounds
hold for every independent input-row subset. Fix polynomial majorants for
these operations once; their composition supplies an effective polynomial
\(T(L)\) bounding every integer coefficient bit length after clearing
denominators in (7) and its gradient. No enumeration is needed to compute
this majorant.

## 3. A separation bound depending on nonlinear dimension

Let \(\alpha=h(p)\). The one-free-variable formula
\[
 \exists t\in\mathbb R^s:\quad
        \nabla\phi(t)=0\ \land\ z=\eta(t)             \tag{9}
\]
defines exactly \(\{\alpha\}\). It uses \(s+1\le k+1\) polynomials
of degree at most four and integer coefficient bit lengths at most
\(T(L)\). The one-block bound in
[Basu, Theorem 2.16](https://www.math.purdue.edu/~sbasu/raag_survey2011.pdf)
produces a quantifier-free description with degrees and coefficient bit
lengths bounded by \(G(k)T(L)\), for an effective parameter-only function
\(G\). The dependence on the original coefficient bit bound is linear
in that theorem; no power of \(L\) depending on \(k\) is introduced.
For \(s=0\), rational evaluation gives the same conclusion directly.

Some nonzero integer polynomial in this description vanishes at
\(\alpha\): otherwise all its nonconstant sign tests would be locally
constant at \(\alpha\), contradicting the singleton set. After removing
any power of \(z\), its nonzero constant term has magnitude at least one.
If its degree is \(D_0\), its largest coefficient magnitude is \(H_0\),
and \(0<|\alpha|<1\), then
\[
                  1\le D_0H_0|\alpha|.
\]
Enlarging \(G\) and \(T\) gives the uniform effective separation
\[
 \alpha\ne0\quad\Longrightarrow\quad
 |\alpha|\ge 2^{-N},\qquad N=G(k)T(L).                \tag{10}
\]
The same \(N\) works for every possible active face. Quantifier elimination
and active-set search are not executed. Unlike the general-dimensional
bound, the number \(N\) of required printed precision bits is FPT in
\(k\), with an absolute polynomial input-length exponent.

## 4. The deterministic algorithm

Use ordinary rational LP to test feasibility and obtain a polynomial-bit
feasible point \(x_0\) when nonempty. Strong convexity at zero gives
\[
 f(x)\ge f(0)+\nabla f(0)^{\mathsf T}x+\tfrac\mu2\|x\|^2.
\]
Set
\[
 A_0=\|\nabla f(0)\|_1+|f(x_0)-f(0)|+1,
 \qquad R=2+2A_0/\mu.
\]
Then \(f(x)>f(x_0)\) for \(\|x\|\ge R\), so \(\|p\|<R\).
The encoding length of \(R\) is polynomial in \(L\). On the radius
\(R+1\) ball compute a rational bound \(B\ge1\) for \(\|\nabla h\|\),
by differentiating its explicit monomials. Its bit length is polynomial.

Put \(\gamma=2^{-N}\),
\[
 \delta=\min\{1,\gamma/(8B)\},\qquad
 \varepsilon=\min\{1,\mu\delta^2/2\}.                          \tag{11}
\]
Use the polynomial-bit approximation algorithm of
[Slot, Steurer, and Wiedmer, Corollary 1.2](https://arxiv.org/html/2511.03440v1)
to obtain an actual rational feasible point \(\widehat x\in P\) with
\(f(\widehat x)\le f(p)+\varepsilon\). The source applies to globally
convex objectives over arbitrary rational polyhedra. Its runtime is
polynomial in input length and \(\log(1/\varepsilon)\).

Constrained first-order optimality and (3) yield
\[
 f(\widehat x)-f(p)\ge\tfrac\mu2\|\widehat x-p\|^2.
\]
Hence \(\|\widehat x-p\|\le\delta\), so
\[
             |h(\widehat x)-h(p)|\le\gamma/8.         \tag{12}
\]
All computation is now ordinary rational arithmetic. If
\(|h(\widehat x)|<\gamma/2\), return zero. Otherwise return the sign of
\(h(\widehat x)\). Bounds (10) and (12) prove correctness, including
exact zeros. All intermediate printed data have length \(F(k)L^C\), and
the approximation algorithm and exact evaluation have the same form of
runtime after enlarging \(F,C\). This proves Theorem 1's sign claim.

Apply that claim to every slack \(b_i-a_i^{\mathsf T}x\) to recover the
full active set. Each call has comparable explicit length; multiplying by
the number of rows preserves FPT. Now execute the constructions (4)--(8)
on that known set. This returns the claimed exact implicit description
and completes the theorem.

## 5. Mixed-integer consequence

**Corollary 2.** Suppose \(f(z,y)\) satisfies (3), has nonlinear dimension
\(k\), and \(z\in\mathbb Z^t\) is subject with \(y\) to arbitrary
rational linear inequalities. Exact optimum comparisons and selection of
an optimal integer block are deterministic ordinary FPT in \(k+t\).
There is no PosSLP oracle and no constraint-rank parameter.

Apply the
[mixed-linear candidate-list theorem](../../research-20260927/mixed-linear-strong-quartic-candidate-list.md)
to obtain all potentially optimal integer blocks in \(a(t)L^{C_0}\) time.
Every optimal block is in the list, and the list's fiber inputs have that
same parameter-polynomial encoding bound. In a fixed fiber \(z=\bar z\),
its terms of degree at least three in \(y\) still depend only on
\(U_y y\), so its nonlinear dimension is at most \(k\). Apply Theorem 1
to each fiber. For comparing two fiber minima, use their product
polyhedron, separable sum objective, and difference observable; the
nonlinear dimension is at most \(2k\). Repeated exact comparisons choose
a best block and can retain all ties. Absolute exponents compose to give
\(F_1(k+t)L^{C_1}\). The selected continuous optimizer has the implicit
representation in Theorem 1. This corollary uses the existing candidate-list
result; it does not claim a new integer-search method.

## 6. Scope and comparison with the existing program

A family such as
\[
 f(x)=\tfrac12x^{\mathsf T}Qx+c^{\mathsf T}x+
                      (a^{\mathsf T}x)^4,\qquad Q\succeq I,
\]
has nonlinear dimension one and can have dense \(Q\), arbitrarily many
coupled linear constraints, and constraint rank \(n\). Theorem 1 gives
ordinary polynomial-time exact comparison on this family. It is not a
consequence of bounding constraint rank, and it does not enumerate the
possibly many faces of its polyhedron.

Conversely, unconstrained quartics can have nonlinear dimension \(n\).
For them this theorem is only an exponential-parameter bound; the existing
PosSLP theorem is stronger in its oracle runtime. The parameters measure
different difficulties. Strong convexity is material to both eliminating
the quadratic directions and converting value accuracy into point accuracy.
No theorem here covers merely feasible-domain convexity or promises that
\(k\) is small for all strongly convex quartics.

The proof combines elementary essential-variable extraction, quadratic
elimination, an established real-algebraic separation bound, and an
established approximation theorem. Those ingredients are not claimed as
new. A focused literature search on 2026-10-03 did not locate this exact
parameter-and-output statement, but the search was limited; priority
requires a wider comparison with fixed-rank polynomial optimization and
parametric quadratic programming.

See [structural-newton.md](structural-newton.md) for a complementary
PosSLP extension with unrestricted nonlinear dimension and structured box
Newton subproblems. Neither theorem resolves arbitrary constrained
quartics in deterministic polynomial PosSLP time.
