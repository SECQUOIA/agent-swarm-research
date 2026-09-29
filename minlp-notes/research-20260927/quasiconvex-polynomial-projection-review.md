# Review of quasiconvex polynomial projection through a linear lift

Date: 2026-09-28. Scope: the structural projection lemma and its strict
phase-I oracle. The proposed lemma is correct. The stronger affine-direction
statement in Section 4 is proved here but should receive another independent
review before it is used to enlarge a main theorem. This review does not
verify the complete integer algorithm or establish novelty.

Throughout, quasiconvexity means that every weak sublevel set is convex.
All functions are defined on their entire indicated real vector spaces.

## 1. Rows that use the linear variables are convex

Let

\[
                  g(y,v)=Cv+p(y),\qquad C\ne0.
\]

If even the single set \(\{(y,v):g(y,v)\le0\}\) is convex, then \(p\)
is convex. Choose \(h\) with \(Ch=1\). For any \(y_1,y_2\), the points
\((y_j,-p(y_j)h)\) lie in that set. Convexity, at a weight
\(\theta\in[0,1]\), gives

\[
 p(\theta y_1+(1-\theta)y_2)
       \le\theta p(y_1)+(1-\theta)p(y_2).
\]

The converse holds because then \(g\) is convex. Polynomiality and
differentiability are unnecessary for this statement. Thus, in the proposed
model, each row with \(C_i\ne0\) is convex, while a row with \(C_i=0\)
can be genuinely quasiconvex.

The global scope matters. If only the zero sublevel restricted to a supplied
box is convex, the conclusion need not follow: \(g(y,v)=v-y^2\) has a
convex, full zero sublevel on \([-1,1]\times[-3,-2]\), but \(-y^2\) is
not convex.

## 2. Which Farkas rows preserve quasiconvexity

Let

\[
 \Lambda=\{\lambda\ge0:C^T\lambda=0,\mathbf1^T\lambda=1\}.
\]

Each unit vector \(e_i\) with \(C_i=0\) is a vertex. If a feasible
\(\lambda\) has \(0<\lambda_i<1\) for such an index, then

\[
 \lambda=\lambda_i e_i+(1-\lambda_i)\mu,\qquad
 \mu=\frac{\lambda-\lambda_i e_i}{1-\lambda_i}\in\Lambda.
\]

This is a nontrivial convex decomposition. Consequently every vertex is
either one of those unit vectors or is supported entirely on nonzero rows
of \(C\). A vertex polynomial \(\lambda^Tp(y)\) is therefore either a
native quasiconvex polynomial or a nonnegative sum of convex polynomials.
Both cases are globally quasiconvex.

Farkas' lemma now gives the exact weak projection as the intersection of
the corresponding weak polynomial inequalities. In particular this
projection is closed and convex for polynomial data. An empty \(\Lambda\)
gives no projected inequalities and the whole \(y\)-space.

**An arbitrary dual multiplier is not sufficient.** Take

\[
 C=(0,1,-1)^T,\qquad p(y)=(y^3,y^2,0)^T.
\]

Every native row is globally quasiconvex. The feasible multiplier
\(\lambda=(1/2,1/4,1/4)\) produces
\(F(y)=y^3/2+y^2/4\), which is not quasiconvex:
\(F(-1/2)=F(0)=0\), whereas \(F(-1/4)=1/128>0\).
This multiplier can be dual-optimal at \(y=0\). Thus a solver returning
an unspecified optimal dual point does not by itself provide the required
polynomial family.

An equivalent, simpler decomposition is to test every zero-\(C\) row
directly and project only the nonzero-\(C\) rows. Every multiplier of the
remaining system produces a convex polynomial. Selecting a basic dual
optimum remains a convenient way to obtain a uniform coefficient bound.
For rational \(C\), a vertex has at most
\(\operatorname{rank}C+1\) positive entries, and rational minor bounds
give polynomial encoding length in the explicitly supplied matrix size.

## 3. Strict projection and phase I

For any fixed finite vector \(b=b(y)\), consider

\[
 \rho(y)=\inf_{v,s}\{s:Cv+b(y)\le s\mathbf1\}.
\]

This LP is feasible. If \(\Lambda\ne\varnothing\), it has a finite
attained optimum, with

\[
             \rho(y)=\max_{\lambda\in\Lambda}\lambda^Tb(y).
\]

Hence \(\exists v:Cv+b(y)<0\) holds exactly when every vertex polynomial
is strictly negative. If \(\Lambda\) is empty, phase I is unbounded
below and the strict system is feasible for every \(y\); the same vertex
criterion holds vacuously. Opposite finite box rows on \(v\) ensure a
nonempty \(\Lambda\) whenever there is at least one \(v\)-coordinate,
so the boxed construction always uses the finite-optimum case. When there
are no \(v\)-coordinates, the oracle simply tests the native rows. With
no rows at all, membership is unconditional.

Subtracting a fixed relaxation \(\varepsilon\), applying an affine change
of variables to \(y\), and adding affine box rows preserve the structural
conclusion in Sections 1 and 2. Thus the proposed strict relaxed oracle is
valid at all rational queries, including noninteger queries.

Two restrictions must remain explicit:

- The phase-I variable \(s\) is only an LP device at fixed \(y\). A native
  nonconvex quasiconvex row \(p(y)\) does **not** make \(p(y)-s\)
  jointly quasiconvex. The proof must not apply the structural lemma to
  the augmented variables \((y,v,s)\).
- A violated quasiconvex row with zero gradient need not prove emptiness.
  For \(F(y)=y^3\), \(F(0)=F'(0)=0\) but \(F(y)<0\) holds for every
  \(y<0\). The convex-only zero-gradient shortcut must be replaced by
  the general quasiconvex shallow-cut procedure.

These restrictions also explain why an arbitrary quasiconvex objective
cannot simply be given a jointly convex epigraph. Fixed objective thresholds
are valid quasiconvex rows; varying thresholds need a separate value theorem.

## 4. A stronger affine-direction statement

**Lemma.** If a globally quasiconvex polynomial \(q(y,t)\) has degree at
most one in \(t\), then its coefficient on \(t\) is constant in \(y\).

Write \(q(y,t)=a(y)t+b(y)\), and restrict \(y\) to any affine line.
It suffices to prove the result for univariate polynomials \(a(s),b(s)\).
If \(a\) is not identically zero, choose an open interval \(I\) where
its sign is fixed and nonzero. For each real level \(\alpha\), put

\[
                     h_\alpha(s)=\frac{\alpha-b(s)}{a(s)}.
\]

When \(a>0\) on \(I\), the sublevel set intersected with
\(I\times\mathbb R\) is the hypograph of \(h_\alpha\), so
\(h_\alpha''\le0\). When \(a<0\), it is the epigraph and
\(h_\alpha''\ge0\). In either case the inequality holds for every real
\(\alpha\), forcing \((1/a)''=0\) on \(I\). Thus
\(1/a(s)=As+B\) there. The polynomial identity
\(a(s)(As+B)=1\) holds on all of \(\mathbb R\), and its degree forces
\(A=0\) and \(a\) constant. If \(a\) is identically zero it is already
constant. Since the restriction to every affine line is constant, \(a(y)\)
is constant. This proves the lemma.

It follows coordinatewise that a globally quasiconvex polynomial affine
in a vector \(v\) automatically has the form \(Cv+p(y)\) with constant
\(C\). If \(C\ne0\), Section 1 then shows that the entire polynomial
is convex.

There is also a consequence for intrinsic directions. If a fixed continuous
direction \(a\) lies in the polynomial kernel of every continuous Hessian
block \(\nabla^2_{xx}g_i(z,x)\), then along a linear change of coordinates
placing \(a\) last, each \(g_i\) is affine in that coordinate. The lemma
makes its coefficient constant in all other variables, including \(z\).
Thus the full Hessian also annihilates \((0,a)\). For globally quasiconvex
polynomials, the kernels from full Hessians and continuous Hessian blocks
therefore agree, by this argument rather than by a positive-semidefinite
Hessian argument.

The hypothesis of all sublevels is essential for this strengthening.
The polynomial \((1+s^2)t\) has the convex zero sublevel \(t\le0\), but
a variable coefficient on \(t\). Its level-one sublevel is not convex:
\((0,1)\) and \((2,1/5)\) belong to it, but their midpoint has value
\(6/5\).

## 5. Sources, checks, and remaining scope

The proof above is elementary and does not require a new theorem of linear
programming. The local primary text of
[Hildebrand--Köppe](https://arxiv.org/pdf/1006.4661), Section 5.2,
Lemma 5.2, Lemma 5.4, and Theorem 6.3, was inspected. It treats global
quasiconvex polynomials and gives the relevant directional and shallow-cut
machinery. Its stated explicit-input integer theorem does not itself
assert the present implicit projection interface.

Two web searches, on 2026-09-28, used combinations of “quasiconvex
polynomial,” “affine variable,” “constant coefficient,” “Hessian kernel,”
and “affine directions.” They did not identify an exact prior statement of
Section 4. This limited search does not establish novelty. Results about
quasiconvexity in the calculus of variations use a different definition and
were not treated as evidence for or against these claims.

Targeted command run: `python -`, with inline assertions using
`fractions.Fraction` and `sympy`. It passed exact rational checks of the two
counterexamples above and the identity
\((1/a)''=(2(a')^2-aa'')/a^3\), together with delimiter, trailing-whitespace,
and final-newline checks of this file. These calculations confirm those
identities and examples only. The structural proof, strict LP alternative, algorithmic
coefficient bounds, and any complete MINLP complexity theorem still rely on
their stated mathematical arguments. No project-wide checks or CI
inspection were performed.
