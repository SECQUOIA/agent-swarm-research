# Exact feasibility parameterized by the common Hessian range

Date: 2026-09-28. Status: proof draft; primary radius and integer-witness
statements inspected. The main projection and reciprocal arguments have
received an initial independent root check. A fresh complete adversarial
review is in progress. The [prior-art audit](common-range-fpt-prior.md)
found important nearby results but did not establish priority.

The dimension of the common Hessian range gives a possible true
fixed-parameter bound for exact convex quadratic and second-order cone
feasibility. This parameter differs from the dimension of the matrix span.
The argument uses the coefficient-sensitive projection and radius tools
already assembled in [the penalty note](penalty-frontier.md), without that
note's Slater assumption. It adds an exact feasibility algorithm by combining
those tools with compact rational polyhedral outer approximations.

## 1. Models and statements

All data are rational and explicitly encoded, with total binary length
\(N\ge2\). Equalities and affine inequalities are unrestricted in number.
We consider either of these convex models:

1. Quadratic inequalities \(q_i(w)\le0\) with positive-semidefinite full
   Hessians.
2. Second-order cone inequalities
   \[
   \|A_iw+b_i\|_2\le c_i^Tw+d_i.
   \]
   Define the squared polynomial
   \[
   q_i(w)=\|A_iw+b_i\|_2^2-(c_i^Tw+d_i)^2.
   \]
   Its Hessian can be indefinite. The quadratic description retains
   both \(q_i\le0\) and \(c_i^Tw+d_i\ge0\).

In the continuous case, let

\[
K=\bigcap_i\ker\nabla^2q_i,\qquad r=\operatorname{codim}K.
\]

Equivalently, \(r\) is the dimension of the sum of the ranges of the
symmetric Hessians. For PSD Hessians, \(r=\operatorname{rank}(\sum_i
\nabla^2q_i)\). For indefinite Hessians one must compute the common kernel,
not the rank of their sum.

**Claim A (continuous exact feasibility).** There is an algorithm deciding
exact feasibility in \(2^{O(r)}N^C\) bit operations, for an absolute
constant \(C\). No input box, Slater condition, rational feasible point,
or closedness assumption on a separately supplied projection is required.
The present proof is a decision algorithm; exact continuous algebraic
witness recovery is not included in this claim.

For mixed-integer problems write \(w=(z,x)\), with \(z\in\mathbb Z^k\).
When a finite rational box for \(z\) is supplied, define

\[
r_x=\operatorname{codim}\bigcap_i\ker\nabla^2_{xx}q_i.
\]

**Claim B (bounded integer projection).** There is a rational MILP of
encoding length and construction time \(2^{O(r_x)}N^C\) whose feasible
original integer assignments are exactly those of the original model.
It uses only the original integer variables; all auxiliary variables are
continuous. No continuous box need be supplied. Thus exact feasibility is
fixed-parameter tractable in \((k,r_x)\).

For integer variables without supplied bounds, put

\[
K_*=\{v\in\mathbb R^n:
       (\nabla^2q_i)(0,v)=0\text{ for every }i\},\qquad
\rho=\operatorname{codim}K_* .                         \tag{1}
\]

This definition uses the full Hessians acting on continuous directions;
it excludes a direction whenever it participates in an integer-continuous
bilinear term. It is computable by rational linear algebra.

**Claim C (unbounded mixed-integer feasibility).** Exact feasibility is
fixed-parameter tractable in \((k,\rho)\), with no variable bounds supplied.
For jointly convex quadratic inequalities, \(\rho=r_x\), so this gives
fixed-parameter tractability in the number of integer variables and the
common range dimension of the continuous Hessians. For general SOCP,
the full common Hessian range dimension bounds \(\rho\), and is an
alternative sufficient parameter.

These are feasibility statements. They do not yet assert an FPT algorithm
for exact optimal values, nonattainment classification, or algebraic
optimizer output. An objective threshold can be appended when its added
Hessian leaves the relevant parameter controlled.

The representation matters: affine invertible continuous coordinate
changes preserve these kernel dimensions, but arbitrary reformulations
can change them. Individual Hessian rank is insufficient. The repeated
squaring chain has rank-one rows and unbounded common range.

## 2. Coefficient-sensitive projection

Consider any rational quadratic system in continuous variables whose
common Hessian range dimension is \(r\); convexity is unnecessary in this
section. A rational basis of the common kernel and a rational complement
give an invertible change of coordinates

\[
x=T_1u+T_0v,\qquad u\in\mathbb R^r.
\]

The matrices and inverse have coefficient bit lengths \(N^{O(1)}\).
Every row has the form

\[
C_iv+p_i(u)\le0,                                    \tag{2}
\]

where \(C\) is rational and constant and \(p_i\) is quadratic.
Affine rows and both signs of an equality have this form.

By Farkas' lemma, projection onto \(u\) is described by
\(\lambda^Tp(u)\le0\) for the extreme rays of
\(\{\lambda\ge0:C^T\lambda=0\}\). Such a ray has support at most
\(\operatorname{rank}C+1\). A normalized generator is obtained from
minors, hence has \(N^{O(1)}\) coefficient bits. There are at most \(2^M\)
supports, where \(M=N^{O(1)}\) is the row count. Clearing denominators
separately in each projected row yields:

\[
\deg P_j\le2,\qquad
\operatorname{bit}P_j\le N^{O(1)},\qquad
\log(S+1)\le N^{O(1)}.                              \tag{3}
\]

Here \(S\) is the number of projected rows. The exponential family is
used only to establish bounds and is never generated by the algorithm.
Farkas' lemma proves equality of the projection and the displayed basic
closed description. We do not infer closedness from a general theorem
about convex projections.

The same argument retains an extra scalar \(t\), as long as the row
coefficients of \(v\) remain constant and every \(p_i(u,t)\) has degree
at most two. In particular it applies to residual epigraphs.

All these estimates can be kept polynomial in the matrix dimensions and
linear in the original maximum coefficient bit length, apart from
additive determinant and row-count terms. Therefore, after appending
numbers of bit length \(B\), the right side of the coefficient bound is
\((B+1)N^{O(1)}\), not \(B^{O(r)}N^{O(1)}\).

## 3. Two radius facts, with different quantifiers

[Basu--Roy, *Bounding the radii of balls meeting every connected component
of semi-algebraic sets*](https://www.math.purdue.edu/~sbasu/jsc_final-06-05-10.pdf),
final author manuscript, Theorems 3 and 4, gives explicit radii for
integer polynomials of degree at most two in \(d\) variables, coefficient
bit length \(\tau\), and row count \(S\). In both cases

\[
\log_2(2+R)\le
  (\tau+\log_2(S+1)+1)\,2^{O(d)}.                   \tag{4}
\]

Theorem 3 gives a ball **containing every bounded connected component**.
Theorem 4 gives a ball **meeting every connected component**, including
unbounded components. Both statements cover conjunctions of weak
inequalities and equations. The primary definitions and formulas on
pages 3--5 were inspected directly.

The distinction is essential below: the first theorem bounds the maximum
of a reciprocal coordinate on a compact set; the second only supplies
some small feasible point.

### 3.1 A small feasible point without an input box

If the projection in (3) is nonempty, its meeting radius yields some
\(u\) with

\[
\log_2(2+\|u\|_\infty)\le 2^{O(r)}N^{O(1)}.          \tag{5}
\]

If \(r=0\), the projected space consists of the empty tuple, and this
step is omitted. The fiber argument below directly supplies a small
original point; no zero-dimensional version of the radius theorem is
needed.

For this \(u\), the fiber (2) is a nonempty polyhedron with rational
matrix and real right-hand side. It has a point \(v\) satisfying

\[
\|v\|_\infty
\le 2^{N^{O(1)}}(1+\max_i|p_i(u)|).                \tag{6}
\]

For completeness, project the origin onto that fiber. Its projection
lies in the span of the active row normals by the polyhedral normal-cone
formula. Select a linearly independent basis of those normals. The
projection is the minimum-norm solution of their active equations, so
the formula using the inverse of their Gram matrix gives (6) by rational
minor bounds. If no row is active, the projection is zero. This works
with lineality and does not require a vertex or rational right-hand side.

Since the \(p_i\) are quadratic, (5)--(6) and the coordinate change give
a feasible original point in a box whose radius \(R_0\) has

\[
\operatorname{bit}R_0\le 2^{O(r)}N^{O(1)}.          \tag{7}
\]

The bound is effectively computable from the explicit radius formulas
and determinant estimates. It is not necessary to find the projected
point in order to print this box.

### 3.2 A positive residual gap in a supplied box

Let \(B\) be a nonempty finite rational box. Include all desired
quadratic and affine residuals in a list \(g_i\), and set

\[
\alpha=\min_{x\in B}\max(0,g_1(x),\ldots,g_M(x)).
\]

Choose a rational \(U\ge1\) bounding this maximum on \(B\), by direct
coefficient and coordinate bounds. The compact epigraph truncation

\[
\{(x,t):x\in B,\ 0\le t\le U,\ g_i(x)\le t\ \forall i\}
\]

is nonempty. Project the common-kernel variables. Its image \(E\) in
\((u,t)\) is compact, has the description (3), and has minimum
\(t=\alpha\).

If the original boxed system is infeasible, then \(\alpha>0\).
Consequently

\[
H=\{(u,t,y):(u,t)\in E,\ y\ge0,\ ty=1\}              \tag{8}
\]

is a nonempty compact basic closed set in \(r+2\) variables. Every
polynomial still has degree at most two, and
\(\max_H y=1/\alpha\). The **containing** radius, Theorem 3, therefore
gives

\[
\alpha\ge 2^{-2^{O(r)}N^{O(1)}}.                    \tag{9}
\]

When the supplied box itself has coefficient bit length \(B_0\), keep
the coefficient dependence explicit: the exponent in (9) is at most
\((B_0+1)N^{O(1)}2^{O(r)}\). Applying it after (7) still gives
\(2^{O(r)}N^{O(1)}\), with absolute input-size exponents.

The meeting-radius theorem would not prove (9): a small point with
large \(t\) says nothing about the minimum \(t\). Compactness of the
whole reciprocal set and the containing theorem are the needed facts.

As a separate check when \(r\ge1\),
[Jeronimo--Perrucci--Tsigaridas, Theorem 1](https://arxiv.org/abs/1112.0544)
also bounds a nonzero minimum on a compact connected component by a
quantity whose logarithm is
\((\tau+\log(S+1)+1)2^{O(r)}\) when the degree is two and the dimension
is \(r+1\). Apply it to a component of \(E\) containing a minimizer.
Its stated bound uses
\(\widetilde H=\max(H,2(r+1)+2S)\), so an exponential
number of implicit rows contributes only polynomially to its logarithm.

## 4. From the gap to an exact algorithm

The established constructions used in
[the convex quadratic projection note](mixed-integer-span-frontier.md)
and [the SOCP note](socp-hessian-span-frontier.md) have the following
property. On rational boxes, for rational \(\varepsilon>0\), they
construct a rational polyhedral outer lift in time polynomial in the
input encoding and \(\log(1/\varepsilon)\). Every original feasible point
lifts to it. Its projected points satisfy each original quadratic
residual at most \(\varepsilon\), while the affine rows and the SOCP
right-hand-side signs can be retained exactly.

For PSD quadratic rows this follows from compact rational lifted
approximations to the square. For SOCP it uses compact rational
polyhedral approximations of Lorentz cones, with the absolute residual
on the supplied box explicitly controlled. Squared indefinite rows
alone do not have this polyhedral approximation property.

First impose the box (7). Then choose
\(\varepsilon<\Delta\), where \(\Delta\) is a uniform lower bound from
(9). The resulting LP is feasible if and only if the original system
is feasible: a feasible LP point gives maximum original residual less
than \(\Delta\), which rules out a positive minimum residual.

The lift size, its coefficient bit lengths, its construction cost, and
the polynomial-time LP decision all have the bound
\(2^{O(r)}N^C\). Exponentiating a radius bound prints a number with
the stated bit length; its magnitude is not the running-time measure.
This proves Claim A, conditional only on the established outer-lift
construction cited above.

## 5. Integer variables

### 5.1 Supplied integer box

For each integer assignment in the input box, substitution leaves a
continuous quadratic system with common range \(r_x\) and uniformly
polynomial coefficient bit lengths. The matrix multiplying kernel
variables may depend on that assignment; all determinant and Farkas
estimates remain uniform because the assignment itself has polynomial
bit length. Neither enumeration of assignments nor a common symbolic
Farkas cone is needed.

Apply (7) uniformly to every nonempty fiber. Then apply (9) uniformly
to every fiber in that continuous box. A single rational outer lift
with error below the uniform gap preserves exactly the feasible integer
assignments. Its encoding length is \(2^{O(r_x)}N^C\), and no new integer
variables are introduced. For a precise true-FPT algorithmic import, use
[Del Pia, Proposition 4](https://arxiv.org/abs/2311.00099): mixed-integer
feasibility for a polyhedron with one convex quadratic inequality is FPT
in the number of integer coordinates, with arbitrary continuous dimension.
Taking that quadratic inequality to be redundant gives the required
MILP algorithm and hence \(f(k,r_x)N^C\) time. Merely citing a
polynomial-time theorem for each fixed \(k\) would not establish this
absolute input exponent. This proves Claim B.

### 5.2 No integer box

Use \(K_*\) from (1), choose a rational complement, and write
\(x=T_1u+T_0v\) with \(u\in\mathbb R^\rho\). The definition of \(K_*\)
eliminates both quadratic \(v\) terms and all bilinear \(zv\) and \(uv\)
terms. Every row therefore has the form

\[
C_iv+p_i(z,u)\le0
\]

with constant rational \(C\) and quadratic \(p_i\). Farkas gives a
possibly exponential family of degree-two rows \(P_j(z,u)\le0\),
each of coefficient bit length \(N^{O(1)}\). The integer projection is

\[
Y=\{z\in\mathbb R^k:\exists u\in\mathbb R^\rho\
                         P_j(z,u)\le0\ \forall j\}.             \tag{10}
\]

The set \(Y\) is convex because it is a linear projection of the
original convex set. Individual projected squared-SOC polynomials need
not be convex.

[Khachiyan--Porkolab, Theorem 1.1](https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Khachiyan/00230207.pdf)
gives an integer-witness coordinate bit bound
\(L D^{O(k^4)\prod_iO(n_i)}\) for a convex semialgebraic set described
by such a quantified formula. The number of predicates does not enter
this bound. Their reduction of feasibility to optimization appends an
integer coordinate fixed to zero. Applying it to (10), with \(D=2\),
\(L=N^{O(1)}\), and one quantified block of size \(\rho\), gives

\[
\operatorname{bit}z^*
\le N^C\,2^{O((k+1)^4(\rho+1))}                    \tag{11}
\]

for some feasible integer assignment whenever one exists. If \(\rho=0\),
use the quantifier-free case or add one unused quantified variable.
The formula is used only for this bound; it is not constructed.

Print the integer box (11), then apply Claim B. Its enlarged coefficient
bit lengths are \(f(k,\rho)N^C\), so polynomial dependence on those bits
preserves a fixed-parameter running time. This proves Claim C.

For a PSD full Hessian \(H_i\), the condition
\(Q_{ixx}v=0\) implies
\((0,v)^TH_i(0,v)=0\), hence \(H_i(0,v)=0\).
Therefore \(\rho=r_x\) for jointly convex quadratic inequalities.
For general indefinite squared-SOC Hessians this implication can fail:
the larger kernel condition in (1) is required for the proof.

For example, the rational SOC row
\(\|(2,z-x)\|_2\le z+x\) has squared residual \(4-4zx\).
Its continuous Hessian block is zero, while the full Hessian does not
annihilate a nonzero continuous direction. Thus \(r_x=0\) and \(\rho=1\).
Eliminating \(x\) using only its continuous Hessian would leave a
coefficient \(-4z\) depending on the integer parameter. The real
projection onto \(z\) is \((0,\infty)\), which also shows why the
constant-matrix closed-projection argument cannot be used in that case.
This limits the proof; it does not disprove a stronger parameter theorem.

## 6. Assessment and open work

Since \(h\le r(r+1)/2\), a fixed range also gives a fixed matrix span.
However the earlier bound \(N^{O(h+1)}\) only gives an XP bound in \(r\);
it does not imply the absolute input exponent obtained here. Conversely,
one full-rank Hessian has span one and arbitrarily large common range.
Thus bounded common range is a narrower structural class than bounded
matrix span. The improvement is a stronger running-time guarantee on that
class; the earlier span result still covers additional inputs.

The algebraic ingredients are established. The common-kernel projection
and logarithmic row-count argument already occur in the local penalty
note. The candidate contribution is their combination into exact
continuous and mixed-integer feasibility algorithms with a true
fixed-parameter bit bound. Whether this combination or an equivalent
formulation appears in the literature remains under review.

The proof does not use a Slater condition. It also does not give a useful
numerical error tolerance: conservative radius and separation constants
may be enormous. Possible practical uses include exact certification
layers and decomposition when a large model depends nonlinearly on a
small collection of aggregate features. Such benefits remain untested.

The next obligations are independent review of the full proof, a precise
prior comparison with algorithms using few nonlinear variables or
implicit convex constraints, and a separate investigation of exact
algebraic output and optimization. No FPT output claim should be inferred
from an FPT feasibility decision alone.

Targeted verification used an inline Python command to check this note and
the corrected nonconvex prior audit. Two documents and five local Markdown
links passed final-newline, trailing-whitespace, control-character, and
balanced math-delimiter checks. No project-wide tests or CI inspection
were performed. These document checks do not establish the theorem.
