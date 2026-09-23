# Common Lagrangian optimizers need not yield a common feasibility optimizer

Date: 2026-09-05. Status: independently reviewed mathematical note;
[review](../notes/review-geoffrion-property-p.md). Novelty remains qualified.

This note gives a counterexample to the implication between the two precise
common-optimizer conditions in Geoffrion's Property (P′). The example has a
closed convex second-order-cone representable continuous domain, one binary
variable, objective and coupling functions affine in the continuous variables
for each binary choice, bounded objective values,
attained individual feasibility maxima, and strict feasibility of the
fixed-binary subproblems.

**Scope matters:** this does not refute Geoffrion's informal computational
Property (P), nor establish that his 1972 conjecture is false in every intended
interpretation. In this example the feasibility value functions have trivial
explicit formulas, so the informal second part of (P) holds. The result isolates
the failure of the exact common-optimizer interpretation without compactness.
Its impact is a precise limitation and clarification, not a new decomposition
algorithm. Novelty remains qualified; see the [investigation note](../notes/geoffrion-property-p-investigation.md).

## 1. Exact statements

Use Geoffrion's maximization convention. Let (X) be the continuous-variable
domain, (Y) the complicating-variable domain, (f:X\times Y\to\mathbb R),
and (G:X\times Y\to\mathbb R^m). The first part of (P′) is

\[
\tag{A}
\forall u\in\mathbb R^m_+\quad\exists x_u\in X\quad
f(x_u,y)+u^\top G(x_u,y)=\sup_{x\in X}[f(x,y)+u^\top G(x,y)]
\quad\forall y\in Y.
\]

The second part is

\[
\tag{B}
\forall\lambda\in\Delta_m\quad\exists x_\lambda\in X\quad
\lambda^\top G(x_\lambda,y)=\sup_{x\in X}\lambda^\top G(x,y)
\quad\forall y\in Y,
\]

where \(\Delta_m=\{\lambda\ge0:\sum_i\lambda_i=1\}\).
Geoffrion gives these as equations (22-1)–(22-2), then discusses the
first-part-implies-second-part conjecture and proves it under compactness and
continuity. The source distinguishes (P′) from the less formal (P).
[Geoffrion (1972), §4.2, printed pp. 256–257](https://www.anderson.ucla.edu/faculty_pages/art.geoffrion/home/docs/GBD.pdf).

## 2. A conic counterexample with individually attained maxima

**Theorem 1.** Condition (A) does not imply (B), even with all the regularity
properties listed in the opening paragraph.

**Construction.** Let \(Y=\{0,1\}\), \(m=1\), and

\[
X=\{(r,a,b,t):\ 0\le a,b\le1,\ r,t\ge0,
\ r^2\le a,\ r^2\le b,\ (a+b)t\ge1\}.
\]

Set

\[
f(x,y)=r,\qquad
G(x,y)=\tfrac12-(1-y)a-yb.
\]

**Proof.** The two epigraph constraints \(r^2\le a,b\) and the rotated-cone
constraint \((a+b)t\ge1\), with nonnegative factors, define closed convex
sets. Thus \(X\) is closed, convex, and second-order-cone representable. It
is unbounded in \(t\). For example, the last constraint can be written
\(\|(2,a+b-t)\|_2\le a+b+t\). Both \(f\) and \(G(\cdot,y)\) are affine
for fixed \(y\), and \(0\le f\le1\) on \(X\).

For \(u\ge0\), define

\[
q_u=\begin{cases}1,&0\le u\le\tfrac12,\\
1/(2u),&u>\tfrac12,
\end{cases}
\qquad
x_u=(q_u,q_u^2,q_u^2,1/(2q_u^2)).
\]

The point \(x_u\) belongs to \(X\). For either value of \(y\), every
\(x\in X\) satisfies

\[
f(x,y)+uG(x,y)\le \tfrac u2+r-ur^2,
\qquad 0\le r\le1.
\]

The right side is maximized at \(r=q_u\), and \(x_u\) achieves equality
for both \(y\). This proves (A). In particular the common value function is

\[
L^*(y;u)=\begin{cases}1-u/2,&0\le u\le1/2,\\
u/2+1/(4u),&u>1/2.
\end{cases}
\]

The feasibility supremum is \(1/2\) for each \(y\). It is attained at
\((0,0,1,1)\) for \(y=0\) and \((0,1,0,1)\) for \(y=1\). A common
maximizer would require \(a=b=0\), contradicting \((a+b)t\ge1\).
Since \(\Delta_1=\{1\}\), (B) fails.

The same point \((r,a,b,t)=(1/4,1/4,1/4,3)\) lies in the interior of
\(X\) and satisfies \(G(x,y)>0\) for both binary assignments. Thus the
failure is not caused by failure of Slater's condition for either subproblem.
Each subproblem \(\max\{f(x,y):x\in X,G(x,y)\ge0\}\) attains value
\(1/\sqrt2\): choose \(a=b=1/2\), \(r=1/\sqrt2\), \(t=1\).
The upper bound follows from \(r^2\le a\le1/2\) or its counterpart in
\(b\). \(\square\)

This is a convex MINLP in the usual fixed-integer sense. The dependence
\((1-y)a+yb\) is bilinear in the joint variables; no joint convexity claim
is made. The example uses standard conic modeling primitives relevant to
process models, but is a structural example rather than a calibrated process
case study.

## 3. What survives without compactness

The following elementary positive result explains why the example does not
contradict the limiting argument in Geoffrion's discussion. We do not claim
that the general convergence mechanism is new.

**Proposition 2 (pointwise simultaneous approximation).** Assume (A), fix
\(\lambda\in\Delta_m\), and write

\[
g_y(x)=\lambda^\top G(x,y),\quad
s_y=\sup_Xg_y<\infty,\quad M_y=\sup_Xf(\cdot,y)<\infty.
\]

Then any choice of the common maximizers \(x_{t\lambda}\) satisfies
\(g_y(x_{t\lambda})\to s_y\) as \(t\to\infty\), for every fixed
\(y\). If \(z_y\in X\) attains \(s_y\), then

\[
\tag{1}
0\le s_y-g_y(x_{t\lambda})
\le \frac{M_y-f(z_y,y)}t.
\]

In particular, convergence is uniform on finite \(Y\); it is uniform on
arbitrary \(Y\) if the constants on the right are uniformly bounded.
The assumption \(M_y<\infty\) is automatic from (A) at \(u=0\) when
\(f\) is real-valued.

**Proof.** Optimality against any \(z\in X\) gives

\[
g_y(x_{t\lambda})\ge g_y(z)
 +[f(z,y)-f(x_{t\lambda},y)]/t
\ge g_y(z)-[M_y-f(z,y)]/t.
\]

For \(z=z_y\), this is (1). Without attainment, choose for each fixed
\(\delta>0\) a point \(z\) with \(g_y(z)>s_y-\delta\), take the
limit inferior in \(t\), then let \(\delta\downarrow0\). \(\square\)

For the counterexample, the exact common feasibility error is
\(1/(4u^2)\) for \(u>1/2\), while \(t\), the fourth coordinate of
\(x_u\), equals \(2u^2\). Thus the error vanishes as the optimizer escapes
to infinity. In fact every common maximizer for \(u>0\) must have
\(a=b=q_u^2\): equality must hold in the bound used in Theorem 1 for
both binary assignments, and the maximizing \(r\) is unique. Therefore
every common maximizing selection has fourth coordinate at least \(2u^2\)
when \(u>1/2\). Escape is unavoidable, rather than a feature of the
particular displayed selection.

**Corollary 3 (closed joint upper image).** Suppose \(Y\) is finite and
the assumptions of Proposition 2 hold. If

\[
D_\lambda=\{z\in\mathbb R^Y:\exists x\in X,
\ z_y\le\lambda^\top G(x,y)\ \text{for all }y\in Y\}
\]

is closed, there is a common feasibility maximizer for this \(\lambda\).
Consequently (A) implies (B) when the image is closed and every feasibility
supremum is finite for every \(\lambda\in\Delta_m\).

**Proof.** Proposition 2 puts \((s_y)_{y\in Y}\) in
\(\overline{D_\lambda}\). Closedness puts it in \(D_\lambda\). The
witnessing \(x\) attains each coordinate supremum. \(\square\)

In particular, the implication holds when \(X\) is a polyhedron,
\(Y\) is finite, and \(G(\cdot,y)\) is affine, provided the feasibility
suprema are finite: \(D_\lambda\) is then the projection of a
polyhedron and hence closed. Compactness of \(X\) is unnecessary.

For the counterexample,

\[
D_1=(-\infty,1/2]^2\setminus\{(1/2,1/2)\}.
\]

Indeed its corner would require \(a=b=0\); every other point below the
corner is dominated by some \((1/2-a,1/2-b)\) with \(0\le a,b\le1\)
and \(a+b>0\). Thus even though each coordinate supremum is attained,
the joint upper image loses exactly the corner needed by (B).

**Corollary 4 (one compact anchor level set).** Let \(Y\) be arbitrary.
Suppose the assumptions of Proposition 2 hold for every \(y\), \(X\) is
closed in a finite-dimensional Euclidean space, and every \(g_y\) is upper
semicontinuous. If, for some \(y_0\) and \(\eta>0\),

\[
\{x\in X:g_{y_0}(x)\ge s_{y_0}-\eta\}
\]

is compact, there is a common feasibility maximizer for \(\lambda\).

**Proof.** The sequence \(x_{n\lambda}\) eventually belongs to the
compact set. A convergent subsequence has limit \(\bar x\in X\).
For every fixed \(y\), upper semicontinuity and Proposition 2 give
\(g_y(\bar x)\ge\limsup g_y(x_{n_k\lambda})=s_y\). This single
subsequence works for every \(y\); no diagonal extraction is needed.
\(\square\)

This is a standard compactness substitute and is consistent with
Geoffrion's explicit observation that boundedness can be weakened through
bounded upper level sets (§4.1–4.2). It is included to state the precise
boundary of the counterexample, not as a separate novelty claim.

## 4. An attainment consequence for convex polynomial models

**Proposition 5 (aggregate attainment).** Under the assumptions of
Proposition 2 with finite \(Y\), if \(\sum_{y\in Y}g_y(x)\) attains
its supremum over \(X\), there is a common feasibility maximizer for
\(\lambda\).

**Proof.** Proposition 2 gives
\(\sup_X\sum_y g_y=\sum_y s_y\). At an aggregate maximizer,
every term is at most \(s_y\), so equality of the sum forces equality
term by term. \(\square\)

One consequence is a noncompact polynomial case of the (P′) implication.
Suppose \(Y\) is finite, \(X\ne\varnothing\) is defined by finitely many
convex polynomial inequalities on \(\mathbb R^n\), every component of
\(G(\cdot,y)\) is a concave polynomial on \(\mathbb R^n\), and every
feasibility supremum is finite. Then (A) implies (B). For each \(\lambda\),
the convex polynomial \(-\sum_y\lambda^\top G(x,y)\) is bounded below
on \(X\) and attains its minimum by the convex polynomial extension of
the Frank–Wolfe existence theorem. Proposition 5 applies.
[Belousov and Klatte (2002), *A Frank–Wolfe Type Theorem for Convex Polynomial Programs*](https://link.springer.com/article/10.1023/A:1014813701864).

This is a direct consequence of a known attainment theorem, not an independent
novelty claim. A broader version uses convex sets without flat asymptotes and
the attainment theorem of
[Martínez-Legaz, Noll, and Sosa (2018), Theorem 1](https://arxiv.org/html/1805.03451).
The counterexample does not contradict the polynomial consequence:
\(1-(a+b)t\le0\) describes a convex set when its factors are nonnegative,
but its defining polynomial is not convex. Convexity of a constraint's feasible
set is weaker than convexity of its polynomial function.

## 5. Verification and limitations

- The proof above is exact and does not depend on a numerical solver.
- [Exact arithmetic checks](../code/geoffrion_property_p/check.py) verify
  the chosen points, scalar maximization identity, individual maxima,
  strictly feasible point, and escape/error relation at representative
  rational multipliers.
- [Independent review](../notes/review-geoffrion-property-p.md) verified
  Theorem 1, Proposition 2, Corollaries 3–4, Proposition 5, and the
  convex-polynomial consequence. The result must not be described as a
  verified resolution of the informal 1972 conjecture.
