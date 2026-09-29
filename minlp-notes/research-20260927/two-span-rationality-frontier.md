# Rational feasible points at Hessian span two

Date: 2026-09-28. Status: complete proof, independently reviewed. This is
a supporting boundary result. Publication priority is not established.

Every nonempty system of rational native PSD quadratic inequalities whose
Hessians span a space of dimension at most two has a rational feasible
point. Arbitrarily many rational affine inequalities and equalities are
allowed. Together with the
[three-span irrational singleton](convex-qcqp-rationality-boundary.md),
this gives a sharp threshold for the unconditional existence of rational
feasible points in this representation.

There is also a rational witness of polynomial binary length. Its size
bound uses classical algebraic sampling only to bound a strictly feasible
point and its margin.

The main rationality argument is elementary. After reducing to two convex
quadratics,
the only difficult case is tangency. The minimum of a positive weighted
sum is a rational function of the weight. Its real poles and residue signs
force its positive tangency root to be rational. Care is needed to cancel
the denominator before counting repeated roots.

## 1. Statement and scope

Write

\[
 F=\{x\in P:q_i(x)\le0\ (1\le i\le m)\},\qquad
 q_i(x)=\tfrac12x^TQ_ix+a_i^Tx+c_i,
\]

where \(P\) is a rational polyhedron, all coefficients are rational, and
\(Q_i\succeq0\). Define

\[
                 h=\dim\operatorname{span}_{\mathbb R}\{Q_i\}.
\]

**Theorem 1.** If \(h\le2\) and \(F\ne\varnothing\), then
\(F\cap\mathbb Q^n\ne\varnothing\). In fact the rational points of
\(F\) are dense in \(F\), and its affine hull is a rational affine
space.

No boundedness, strict feasibility, positive definiteness, or bound on the
number of affine rows is assumed. The condition concerns the Hessians of
the native defining polynomials. It does not apply merely because a set
is convex, or to squared SOC inequalities whose Hessians are indefinite.

The proof first establishes the result for two quadratic inequalities
with a rational polyhedron. Section 4 then gives the Hessian-span
reduction. The qualitative theorem does not depend on the repository's
quantitative algebraic-height bounds.

## 2. A rational positive tangency multiplier

The normalization in this section is
\(q_i(x)=\tfrac12x^TA_ix+b_i^Tx+c_i\).

**Lemma 2.** Let \(q_1,q_2\) be rational convex quadratics. Suppose
there exist \(p\in\mathbb R^d\) and \(t_0>0\) such that

\[
 q_1(p)=q_2(p)=0,\qquad
                  q_1+t_0q_2\ge0\quad\hbox{on }\mathbb R^d.       \tag{1}
\]

Then some rational \(t>0\) satisfies the same global nonnegativity
condition. The zero set of \(q_1+tq_2\) contains \(p\).
One can choose \(t\) with bit length polynomial in the rational input
length.

**Proof.** Put \(W=\ker A_1\cap\ker A_2\). Stationarity of the
aggregate at \(p\) gives

\[
                     (b_1+t_0b_2)^Tw=0\quad(w\in W).             \tag{2}
\]

The space \(W\) has a rational basis. If either linear form
\(b_i^T\vert_W\) is nonzero, (2) determines \(t_0\) as a ratio of
rational numbers. This proves the claim in that case.

Otherwise both linear forms vanish on \(W\). The quadratics are constant
along \(W\). Restrict to a rational complement and discard \(W\);
then \(A_1+A_2\succ0\). Dimension zero is immediate: both quadratics
are zero constants, and \(t=1\) works. In positive dimension define

\[
 \begin{aligned}
 H(t)&=A_1+tA_2,\\
 f(t)&=c_1+tc_2-	frac12(b_1+tb_2)^TH(t)^{-1}(b_1+tb_2).
                                                               \tag{3}
 \end{aligned}
\]

For every \(t>0\), \(H(t)\succ0\) and \(f(t)=\min_x(q_1+tq_2)\).
The unique quotient minimizer at \(t_0\) is the quotient of \(p\).
Differentiating (3), or differentiating along that minimizer, gives

\[
                         f(t_0)=f'(t_0)=0.                       \tag{4}
\]

The rational function \(f\) belongs to \(\mathbb Q(t)\). If it is
identically zero, choose \(t=1\). Then the aggregate is globally
nonnegative and vanishes at \(p\), since both individual values there
are zero.

Suppose now \(f\not\equiv0\). Simultaneous diagonalization by a real
congruence, using \(A_1+A_2\succ0\), transforms their diagonal entries
to \(1-d_j,d_j\), with \(0\le d_j\le1\). Polynomial division of
each term in (3) gives

\[
 f(t)=a+bt-ct^2-
             \sum_{j=1}^{r}\frac{\rho_j}{t-\sigma_j},\qquad
 c\ge0,\quad \rho_j>0,\quad
                \sigma_1<\cdots<\sigma_r\le0.                  \tag{5}
\]

The entries with \(d_j=0\) supply the nonpositive quadratic polynomial
part; those with \(d_j>0\) supply a linear part and a nonpositive
residue at \(\sigma=-(1-d_j)/d_j\). Equal poles have been combined,
and zero residues have been removed. Thus (5) lists precisely the poles
of the reduced rational function. The real diagonalization is used only
to prove the signs; no rationality of its coordinates is asserted.

Let \(N(t)\) be the numerator of \(f\) in reduced form. Its coefficients
are rational, up to multiplication by a nonzero scalar. Its degree is at
most \(r+1\) when \(c=0\), and exactly \(r+2\) when \(c>0\).
At each consecutive pair of poles,

\[
 \lim_{t\downarrow\sigma_j}f(t)=-\infty,
 \qquad
 \lim_{t\uparrow\sigma_{j+1}}f(t)=+\infty.
\]

Consequently each of the \(r-1\) intervals between poles contains
a real zero of odd multiplicity. All these zeros are nonpositive and
distinct from \(t_0\).

If \(c=0\) and \(r\ge1\), these \(r-1\) zeros and the positive
double zero (4) already account for at least \(r+1\) roots with
multiplicity. They exhaust the degree bound. Each intervening zero is
simple, \(t_0\) has multiplicity exactly two, and it is the only
repeated root of \(N\) over \(\mathbb C\).

If \(c>0\) and \(r\ge1\), there is one further zero in
\(( -\infty,\sigma_1)\), since \(f(t)\to-\infty\) as
\(t\to-\infty\) and \(f(t)\to+\infty\) as
\(t\uparrow\sigma_1\). This gives \(r\) distinct nonpositive
zeros before the positive double root; again all \(r+2\) degrees
are exhausted. If \(r=0\), the conclusion follows directly from the
quadratic polynomial (5); the case \(c=0\) would contradict
\(f\not\equiv0\) and (4).

Therefore \(\gcd(N,N')\) has degree one. Since \(N\in\mathbb Q[t]\),
its sole repeated root \(t_0\) is rational. Choose \(t=t_0\).

For the bit bound, all rational bases above have polynomial encoding
length. Before reduction, a numerator for (3) is

\[
 2(c_1+tc_2)\det H(t)
       -(b_1+tb_2)^T\operatorname{adj}(H(t))(b_1+tb_2).           \tag{6}
\]

It has degree at most \(d+1\) and coefficient bit length polynomial
in the input length. Once rationality of \(t_0\) is known, the rational
root theorem applied to (6) bounds its numerator and denominator by
polynomially many bits. In the identically-zero case take \(t=1\).
The earlier common-kernel ratio also has polynomial bit length.
\(\square\)

**Cancellation is essential.** The numerator (6), or the homogeneous
characteristic determinant, can have other repeated roots at nonpositive
parameters. These can cancel against \(\det H\). The uniqueness claim
in the proof concerns the *reduced* numerator only. In particular, one
must not infer that the gcd of the raw determinant and its derivative is
linear.

## 3. Two convex quadratics and arbitrary affine rows

**Proposition 3.** For a rational polyhedron \(P\) and two rational
convex quadratics \(q_1,q_2\), every nonempty set

\[
                 F=P\cap\{q_1\le0,q_2\le0\}                    \tag{7}
\]

contains a rational point.

**Proof.** Let \(P_0\) be the smallest face of \(P\) containing
\(F\). There is \(p\in F\cap\operatorname{relint}P_0\).
For example, for each affine inequality not identically tight on \(F\),
choose a feasible point where it is strict, and average these finitely
many points. Let \(L=\operatorname{aff}P_0\), a rational affine space.

If some \(y\in L\) has \(q_1(y)<0\) and \(q_2(y)<0\), a short
segment from \(p\) toward \(y\) lies in \(P_0\) and makes both
quadratics strictly negative. Rational points are dense in \(L\), so
a nearby rational point is in \(F\).

Otherwise there is no simultaneous strict point on \(L\). Convex
separation gives nonnegative weights \(\lambda_1,\lambda_2\), not
both zero, such that

\[
                    \lambda_1q_1+\lambda_2q_2\ge0
                         \quad\hbox{on }L.                     \tag{8}
\]

For completeness, separate the convex open upper image
\(\{(u_1,u_2):q_i(x)<u_i\text{ for some }x\in L\}\)
from the negative orthant. Monotonicity makes the separating normal
nonnegative. The common feasible point \(p\) makes the separation
constant zero, giving (8).

Use a rational affine chart of \(L\). If exactly one weight is
positive, its quadratic has global minimum zero on this chart. Its zero
set is the rational affine solution space of its gradient equations.
Restrict to that space. Only one quadratic inequality remains, besides
rational affine rows; the classical rational feasible-point theorem for
one quadratic inequality applies. This is Vavasis's theorem, also covered
by the mixed-integer extension of Del Pia, Dey, and Molinaro. An elementary
qualitative proof is available by repeating the same strict-point/zero-set
argument for that one remaining convex quadratic.

If both weights are positive, each \(q_i(p)=0\), and Lemma 2 supplies
a rational \(t>0\) for which \(g=q_1+tq_2\ge0\) on the chart.
Its zero set \(M\) is a nonempty rational affine space containing
\(p\), defined by the rational linear equations \(\nabla g=0\).
Because \(A_1,A_2\succeq0\),

\[
                    \ker(A_1+tA_2)=\ker A_1\cap\ker A_2.
\]

Both \(q_i\) restrict to affine functions on \(M\). Their coefficients
in a rational chart of \(M\) are rational. Thus (7) restricted to
\(M\) is a nonempty rational polyhedron and contains a rational point.
\(\square\)

## 4. From Hessian span to two quadratic inequalities

Assume \(h=2\); dimensions zero and one are easier. The finitely
generated cone

\[
                       K=\operatorname{cone}\{Q_1,\ldots,Q_m\}
\]

is a two-dimensional pointed cone. Pointedness follows because a matrix
and its negative cannot both be nonzero PSD. Its two extreme rays are
generated by two of the input matrices, say \(B_1,B_2\). Hence

\[
              Q_i=\alpha_i B_1+\beta_i B_2,
              \qquad \alpha_i,\beta_i\in\mathbb Q_+.           \tag{9}
\]

Rationality follows by solving two independent rational matrix-entry
equations. Choose \(b_j(x)=\tfrac12x^TB_jx\) and write
\(q_i=\alpha_i b_1+\beta_i b_2+\ell_i\), where \(\ell_i\) is
rational affine. Then \(F\) is the projection onto \(x\) of

\[
 \begin{aligned}
 x&\in P,\\
 b_1(x)&\le u_1,\qquad b_2(x)\le u_2,\\
 \alpha_i u_1+\beta_i u_2+\ell_i(x)&\le0\quad(1\le i\le m).
                                                               \tag{10}
 \end{aligned}
\]

The equivalence uses nonnegativity in (9). In one direction take
\(u_j=b_j(x)\); in the other substitute \(b_j(x)\le u_j\).
System (10) has just two native convex quadratic inequalities and
otherwise rational affine rows. Proposition 3 gives a rational feasible
\((x,u)\), proving the existence assertion of Theorem 1.

To prove density, intersect \(F\) with an arbitrarily small closed
rational box containing a given feasible point in its interior. This
preserves \(h\) and nonemptiness, so the intersection has a rational
point. Finally choose sufficiently close rational feasible points to
any affine basis of \(\operatorname{aff}F\). Affine independence is
open, so these rational points still form an affine basis. This proves
that the affine hull is rational. \(\square\)

## 5. Polynomial-size rational witnesses

The preceding proof is qualitative except for the multiplier bound in
Lemma 2. The following strengthens its output using an established
algebraic sampling theorem.

**Theorem 4.** If the rational native PSD system in Theorem 1 is nonempty,
it has a rational feasible point of total binary length bounded by a
universal polynomial in the input length \(N\). The number of variables
and rows need not be fixed.

**Proof.** The lift (10), its coefficients, and a rational chart of any
face of its affine polyhedron have polynomial binary length. We therefore
track the cases in Proposition 3 for two quadratics on such a chart.

In the strictly feasible case there is a point \(u\) satisfying both
quadratic inequalities strictly and satisfying every affine inequality
that is not identically tight on the selected affine face strictly.
Write those affine inequalities as \(a_j(u)\le0\). Introduce two
additional variables \(s,y\) and the closed system

\[
 \begin{aligned}
 q_1(u)+s&\le0,&q_2(u)+s&\le0,\\
 a_j(u)+s&\le0\quad\hbox{for every remaining affine row},\\
 s&\ge0,&1-sy&\le0.                                      \tag{11}
 \end{aligned}
\]

It is nonempty: choose \(s>0\) below all the finitely many strict
slacks and then set \(y=1/s\). Its quadratic Hessian span has dimension
at most three: the two original Hessian directions and the single new
\(sy\) block. This auxiliary system need not be convex.

The small-point consequence of Grigoriev--Pasechnik's Theorem 1.2,
recalled below, gives a feasible point of (11) whose coordinates have
absolute value at most

\[
                             R=2^{N^{O(1)}}.
\]

Since \(s\ge0\) and \(sy\ge1\), both \(s,y\) are positive and
\(s\ge1/y\ge1/R\). Thus \(u\) has magnitude at most \(R\)
and satisfies every required inequality with slack at least \(1/R\).
On the box of radius \(R+1\), the two quadratic polynomials and all
affine rows have a common Lipschitz bound \(1\le L\le2^{N^{O(1)}}\) in
the infinity norm. Rounding every coordinate of \(u\) to a dyadic
number with error at most \(\min\{1,1/(2RL)\}\) preserves all
inequalities. The rounded vector, and its image under the rational
affine chart, have polynomial binary length.

If only one exposing multiplier in (8) is positive, the zero set of its
quadratic has a polynomial-size rational affine chart, by rational
Gaussian elimination. Restriction leaves a single quadratic inequality
and affine rows, with polynomial-size rational data. Vavasis's classical
one-quadratic small-witness theorem gives a polynomial-size rational
feasible point.

If both multipliers are positive, Lemma 2 gives a rational positive
weight of polynomial bit length. The gradient equations defining its
zero set therefore have polynomial-size rational coefficients and admit
a rational chart of polynomial size. Both remaining quadratic
restrictions are affine, so a polynomial-size rational LP witness
finishes the proof.

There is no unbounded sequence of affine restrictions in this argument:
after selecting the initial affine face, one curved restriction leaves
either a rational polyhedron or one quadratic inequality handled by
Vavasis's theorem. Polynomial determinant bounds therefore compose only
a fixed number of times. \(\square\)

**Sampling dependency.** For clarity, the small-point fact used above
is a corollary of prior work, not a new height theorem. A rational
quadratic system of fixed Hessian span \(r\), allowing indefinite
Hessians and arbitrary affine rows, lifts to \(r\) quadratic
equalities inside a rational polyhedron. Choose a face of minimum
dimension meeting that quadratic variety. A connected component of the
variety in the face's affine hull which meets the face lies entirely in
its relative interior: its intersection with the face is both open and
closed in that component, since no proper face meets the variety.

Grigoriev--Pasechnik's Theorem 1.2, applied to the restricted quadratic
map and the outer polynomial \(\sum_{i=1}^rY_i^2\), samples every
component with univariate representation degree and coefficient bit
length \(N^{O(r+1)}\). Rational charts have polynomial-size
coefficients. Standard univariate denominator and root bounds then give
coordinate magnitude at most \(2^{N^{O(r+1)}}\). This applies to
(11) with \(r\le3\). The complete face argument and representation
conversion are recorded in
[the fixed-span feasibility note, Section 3.1](nonconvex-hessian-span-frontier.md)
and its [prior-work audit](nonconvex-hessian-span-prior-audit.md).

## 6. Consequences and limits

The threshold is sharp: the three rank-one native PSD quadratics in
[the companion note](convex-qcqp-rationality-boundary.md) have Hessian
span three and common feasible set
\(\{(\sqrt[3]{2},\sqrt[3]{4})\}\). Thus three is the smallest
possible Hessian span for a nonempty rational native PSD system with no
rational point. The distinction survives replacement by three positive
definite ellipsoids in that note.

For mixed-integer systems whose *continuous* Hessian span is at most two,
every nonempty integer fiber has a rational continuous feasible point:
fix the integer coordinates and apply Theorem 1. This alone gives no
bound on the size of a feasible integer assignment. With bounded integer
variables, the fiber conclusion is uniform at the level of existence.

A rational convex quadratic objective over a native PSD feasible system
of Hessian span at most one has a rational optimizer whenever its attained
optimal value \(\theta\) is rational. Append
\(q_0(x)-\theta\le0\); the optimizer set has native Hessian span at
most two, so Theorem 1 applies. More generally this holds whenever the
span of the objective and constraint Hessians together has dimension at
most two. An irrational optimal value cannot in general have a rational
optimizer for a rational polynomial objective.

The theorem does not make every feasible point rational, does not assert
that general quadratic equalities have rational solutions, and does not
extend to arbitrary rational SOCP representations. Two SOC inequalities
can force \(t=\sqrt2\); one of their squared native Hessians is negative.

Theorem 4 supplies short certificates checked using rational arithmetic
alone. It also separates the representation issue from the generic
algebraic feasible-point certificates needed at larger spans. Its proof
uses classical quadratic-map sampling in the strict-slack case; the
elementary rationality proof in Sections 2–4 is independent of that tool.

For exact solvers this boundary identifies a class in which a feasible
algebraic output can be replaced by a rational point. The subsequent
[constructive refinement](two-span-rational-output.md) now provides a
polynomial-time rational-output algorithm, using the main fixed-span
decision and value procedures. Its independent review is complete. This
is an exact-output refinement; practical rounding tolerances and a solver
implementation remain separate work.

## 7. Prior work and novelty qualification

The following primary sources were examined on 2026-09-28.

- Bienstock, Del Pia, and Hildebrand, *Complexity, exactness, and
  rationality in polynomial optimization*, Mathematical Programming
  197 (2023), 661–692,
  [DOI](https://doi.org/10.1007/s10107-022-01818-3),
  [open preprint](https://optimization-online.org/wp-content/uploads/2020/11/8105.pdf).
  The local published full text and the open introduction were inspected.
  The paper distinguishes rational witnesses for one quadratic inequality
  from the difficulty of more general systems, and discusses exact
  feasibility for two quadratics without arbitrary affine rows. Its
  stated rationality results and examples do not supply Theorem 1.
- Vavasis, *Quadratic programming is in NP*, Information Processing
  Letters 36 (1990), 73–77,
  [DOI](https://doi.org/10.1016/0020-0190(90)90100-C), and Del Pia,
  Dey, and Molinaro, *Mixed-integer quadratic programming is in NP*,
  Mathematical Programming 162 (2017), 225–240,
  [DOI](https://doi.org/10.1007/s10107-016-1036-0).
  These supply the previously known one-quadratic small rational witness
  result. The original Vavasis article was not separately retrieved;
  its theorem is stated in the inspected primary papers.
- Jia, Choi, Mourrain, and Wang, *An algebraic approach to continuous
  collision detection for ellipsoids*, Computer Aided Geometric Design
  28 (2011), 164–176,
  [open full text](https://i.cs.hku.hk/~ykchoi/quadrics/CAGD_algebraic_ellipsoids.pdf).
  Sections 2–3 were inspected. Theorem 3.10 analyzes external tangency of
  two three-dimensional ellipsoids through a positive double root of a
  homogeneous characteristic polynomial. It explicitly permits another
  negative double root, reinforcing the cancellation warning above.
  The inspected statements do not give the arbitrary-dimensional
  rational-witness result with affine rows.
- Grigoriev and Pasechnik, *Polynomial-time computing over quadratic
  maps I: sampling in real algebraic sets*, Computational Complexity
  14 (2005), 20–52,
  [open full text](https://arxiv.org/pdf/cs/0403008v3).
  Theorem 1.2 and its representation definition were inspected directly
  in the local primary text. It provides the degree and coefficient
  bounds for sampling a polynomial composed with a fixed-dimensional
  quadratic map. The minimum-face argument above handles the arbitrary
  affine rows. This establishes the quantitative dependency in Theorem 4;
  it does not by itself force sampled points to be rational.

Searches included “two convex quadratic inequalities rational points,”
“two quadratic inequalities rational feasible,” “rational tangent
ellipsoids point,” and rational optimal values in convex trust-region
problems. The rational function in (3) is the classical quadratic
Lagrangian/Schur-complement function; this mechanism is not claimed as
new. The potentially additional statement is the rational tangency
consequence, its extension to arbitrary affine rows, and the resulting
sharp native-Hessian-span threshold. No equivalence to an older theorem
was located in this limited audit. That does not establish novelty.

## 8. Verification

The independent review is recorded in
[two-span-rationality-review.md](two-span-rationality-review.md).
The critical checks are the reduced-numerator root count, the common
kernel case, the identically-zero rational function, and the passage
through arbitrary affine faces. Numerical experiments cannot establish
the absence of irrational tangencies, so the theorem rests on the proof
above. The reviewer ran

```sh
python research-20260927/check_two_span_rationality_review.py
```

Result: passed. The exact symbolic checks cover a raw determinant with an
extra negative double root, a negative quadratic polynomial part, an
identically zero scalar minimum, and a common-kernel multiplier ratio.
They verify these representative identities, not the general theorem.
No project-wide or CI checks were run. No Lean formalization is claimed.
