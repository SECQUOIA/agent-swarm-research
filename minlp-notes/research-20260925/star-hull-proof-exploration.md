# A five-variable star counterexample to SDP–RLT exactness

Research date: 2026-09-25. Status: exact counterexample and self-contained
nonnegativity proof; independent adversarial review found no defect in the
certificate, scalar reduction, or affine transformation. The general star-exactness
conjecture investigated here is false. No novelty claim is made for the
counterexample or the general transfer argument below.

## Question and answer

For a box-constrained quadratic with a star interaction graph, does the full
first-order semidefinite moment relaxation, including every pairwise McCormick
inequality, always attain the true minimum? Equivalently, does its projection
onto the first moments, square moments, and center–leaf products equal the
convex hull of those moments?

The answer is no with five variables: one center and four leaves. The example
below even becomes submodular after complementing two leaves, and every
diagonal quadratic coefficient is positive. Its true minimum is zero, while a
strictly feasible rational SDP–RLT point has value

\[
-\frac{9337}{250000}.
\]

The construction comes from Stephen Drury's copositive matrix supported on the
book graph \(T_6\). Deleting a hub of the book graph leaves a star. Treating
that deleted coordinate as the homogenizing constant connects the two
problems. The explicit box proof below does not require the reader to assume
copositivity from an external source.

## Exact box polynomial

Write the variables as \((t,a,b,c,d)\in[0,4]^5\), and define

\[
\begin{aligned}
q(t,a,b,c,d)={}&625+625(t^2+a^2+b^2+c^2+d^2)-1200t\\
&+(1054-1200t)a+(-1200+1054t)b\\
&+(-350+1250t)c+(1250-350t)d.
\end{aligned}
\]

Only center–leaf products occur. This is \(z^TAz\), where
\(z=(1,t,a,b,c,d)^T\) and

\[
A=\begin{pmatrix}
625&-600&527&-600&-175&625\\
-600&625&-600&527&625&-175\\
527&-600&625&0&0&0\\
-600&527&0&625&0&0\\
-175&625&0&0&625&0\\
625&-175&0&0&0&625
\end{pmatrix}.
\]

This is exactly 625 times Drury's matrix (2.1), at
\(\cos\theta=24/25\), \(\sin\theta=7/25\). In particular
\(0<\theta<\pi/6\). It is also the integer example on the author's supporting
webpage, not a rounding of the numerical example elsewhere on that page.

### Self-contained proof that the minimum is zero

Fix \(t\in[0,4]\). Each leaf has positive quadratic coefficient 625. Its
minimizer is its unconstrained minimizer clipped to \([0,4]\):

\[
\begin{aligned}
a(t)&=\max\{0,(600t-527)/625\},\\
b(t)&=\max\{0,(600-527t)/625\},\\
c(t)&=\max\{0,7/25-t\},\\
d(t)&=\max\{0,7t/25-1\}.
\end{aligned}
\]

Every displayed value is at most 4 for \(t\in[0,4]\), so no upper clipping is
needed. Substitution gives the following reduced objective \(F(t)\).

| Interval for \(t\) | \(F(t)\) |
|---|---|
| \([0,7/25]\) | \(-289t(961t-350)/625\) |
| \([7/25,527/600]\) | \(49(48t-25)^2/625\) |
| \([527/600,600/527]\) | \(-20592(3t-4)(4t-3)/625\) |
| \([600/527,25/7]\) | \(49(25t-48)^2/625\) |
| \([25/7,4]\) | \(289(350t-961)/625\) |

The first piece is nonnegative because \(961(7/25)<350\). The second and fourth
pieces are squares. On the third interval, \(3t-4<0<4t-3\). The last piece is
positive because \(350(25/7)>961\). Thus \(q\geq0\) throughout the box.

Equality holds, for example, at

\[
(t,a,b,c,d)=(48/25,1,0,0,0).
\]

Hence the true minimum is exactly zero. The other center values at which the
reduced objective vanishes are \(t=0\) and \(t=25/48\).

## A strictly feasible rational relaxation point

Let \(Y=R/10^6\), with rows and columns indexed by
\((1,t,a,b,c,d)\), where

\[
R=\begin{pmatrix}
1000000&799266&291861&478567&69800&786\\
799266&1202068&562307&124777&4&3138\\
291861&562307&293721&4&4&2857\\
478567&124777&4&354219&67082&4\\
69800&4&4&67082&19549&678\\
786&3138&2857&4&678&99
\end{pmatrix}.
\]

Put \(m_i=Y_{0i}\), \(X_{ij}=Y_{ij}\) for \(i,j\geq1\). The relaxation is

\[
Y=\begin{pmatrix}1&m^T\\m&X\end{pmatrix}\succeq0,
\qquad
0\leq X_{ij}\leq\min\{4m_i,4m_j\},
\qquad
X_{ij}\geq4m_i+4m_j-16.
\]

The six leading principal minors of \(R\) are, in order,

\[
\begin{gathered}
1000000,\quad563241861244,\quad9195082165937060,\\
46807432377976756,\quad85462696063069044,\quad
288188945338719248.
\end{gathered}
\]

They are all positive, so Sylvester's criterion gives \(Y\succ0\). Every
McCormick slack is strictly positive. On the integer scale used for \(R\),
the smallest slack among nonnegativity, upper bounds, and lower bounds is 4.
Direct exact multiplication gives

\[
\langle A,Y\rangle=-\frac{9337}{250000}<0.
\]

Consequently the star moment projection is strictly larger than the true
convex hull. This does not depend on numerical eigenvalue tolerances or the
accuracy of an SDP optimum.

### Unit cube and submodular form

Set

\[
t=4u_0,\quad a=4u_1,\quad b=4(1-u_2),\quad
c=4(1-u_3),\quad d=4u_4.
\]

The resulting polynomial on \([0,1]^5\) is

\[
\begin{aligned}
p(u)={}&14425+10000\sum_{i=0}^{4}u_i^2
+32064u_0+4216u_1-15200u_2-18600u_3+5000u_4\\
&-19200u_0u_1-16864u_0u_2-20000u_0u_3-5600u_0u_4.
\end{aligned}
\]

Its off-diagonal coefficients are all negative. Its exact minimum is zero,
attained at \((12/25,1/4,1,1,0)\). The affine transformation of \(Y\) is a
strictly feasible unit-cube SDP–RLT point with the same negative objective.
The verification script checks this transformation and all unit-cube
McCormick inequalities exactly.

The quadratic matrix has exactly one negative eigenvalue. Before the affine
change, its leaf block is \(625I_4\), and the center Schur complement is
\(-668354/625\). Congruence under the invertible affine change of variable
preserves the inertia of the quadratic part. Thus the example also rules out
exactness based only on having one negative eigenvalue.

## General transfer from copositivity

The following elementary argument explains why the construction works.
Suppose a symmetric matrix \(A\), indexed by \(0,1,\ldots,n\), is copositive
but is not a sum of a positive semidefinite matrix and an entrywise nonnegative
matrix. Cone separation supplies a doubly nonnegative matrix \(W\) satisfying
\(\langle A,W\rangle<0\). Here “doubly nonnegative” means positive semidefinite
and entrywise nonnegative.

For sufficiently small \(\varepsilon>0\), replacing \(W\) by
\(W+\varepsilon(I+ee^T)\) preserves its negative pairing with \(A\) and makes
it positive definite and entrywise positive. Normalize by its \((0,0)\)
entry, and write the result as
\(Y=\left(\begin{smallmatrix}1&m^T\\m&X\end{smallmatrix}\right)\).
Every \(m_i>0\). For sufficiently large finite \(U\), all inequalities

\[
X_{ij}\leq U m_i,\qquad X_{ij}\leq U m_j,\qquad
X_{ij}\geq U(m_i+m_j)-U^2
\]

hold strictly: the upper right-hand sides grow linearly, and the last
right-hand side tends to \(-\infty\). Thus \(Y\) is feasible for full
SDP–RLT on \([0,U]^n\), but
\((1,x)^TA(1,x)\geq0\) there by copositivity and
\(\langle A,Y\rangle<0\).

Deleting vertex 0 from the graph of \(A\) gives the quadratic interaction
graph of this box problem; the deleted edges become linear terms. The only
cone fact used here is standard duality between the copositive/completely
positive cones and between the SPN/doubly nonnegative cones. To justify the
separation step directly, the SPN cone is closed: in any convergent sequence
\(P_k+N_k\), nonnegative diagonal entries bound both diagonal sequences;
positive semidefiniteness then bounds every entry of \(P_k\), and hence
\(N_k\). A convergent subsequence gives a limiting SPN decomposition.

This argument transfers a known matrix obstruction using standard cone
duality. It is not claimed as a new certificate framework or a new
characterization of exact interaction graphs, and the converse has not been
established here. The general SDP–RLT primal–dual optimality framework is
already explicit in Qiu and Yıldırım's Lemma 19 and Proposition 20, discussed
below.

## Literature comparison and limits

- Qiu and Yıldırım, [*On exact and inexact RLT and SDP-RLT relaxations of
  quadratic programs with box constraints*, Journal of Global Optimization
  90 (2024), 293–322](https://link.springer.com/article/10.1007/s10898-024-01407-y),
  give complete algebraic exactness criteria. Their Lemma 19 characterizes
  SDP–RLT optimality by primal–dual certificates; Proposition 20 characterizes
  exactness by the existence of such a certificate at a rank-one moment
  pair. These are established general results, not contributions of this
  note. Their criterion implies that a homogeneous copositive quadratic on
  the unit cube has an exact SDP–RLT relaxation if and only if its coefficient
  matrix is SPN: specialize the optimality conditions to the true minimizer
  at the origin. Thus using non-SPN copositive matrices to obtain box gaps is
  already part of this framework. The particular book-to-star construction
  has not been located in their paper. The additional content retained here
  is its explicit sparse specialization and rational witness, whose priority
  remains unchecked.
- Burer, Natarajan, and Willemsen, [*On the Semidefinite Representability of
  Continuous Quadratic Submodular Minimization With Applications to Pricing
  and Moment Problems*, arXiv:2504.03996v3](https://arxiv.org/html/2504.03996v3),
  prove exactness for submodular objectives in at most three variables and
  give a four-variable counterexample. A star can be made submodular by
  independently complementing its leaves, so their theorem settles stars
  with at most two leaves. It does not establish general star exactness.
- Shaked-Monderer's [corrigendum, arXiv:1712.05115](https://arxiv.org/abs/1712.05115)
  withdraws the earlier proof that every book graph \(T_n\) is SPN and proves
  the case \(T_5\). Relying on the uncorrected claim would give an invalid
  route toward star exactness.
- Drury, [*The Triangle Graph T6 is not SPN*, Electronic Journal of Linear
  Algebra 36 (2020), 90–93](https://emis.de/ft/34748), gives the exact
  copositive, non-SPN family used here. The [author's supporting
  page](https://www.math.mcgill.ca/drury/research/spn/index.html) records its
  integer specialization used above. The matrix and its non-SPN obstruction
  are prior work.
- Shaked-Monderer's [2025 survey on CP and SPN
  graphs](https://cot.mathres.org/issues/COT20253.pdf) confirms that Drury's
  obstruction supersedes the earlier open book-graph conjecture.

The precise contribution of this note is the explicit box transfer, a
rational full-McCormick witness, and a self-contained five-variable star
polynomial certificate. An adequate search for an equivalent box example
has not yet been completed. In particular, this note does not claim that
five is the smallest dimension of a star counterexample; the four-variable
star case remains unresolved in this investigation.

The practical implication is limited but useful: a solver cannot assume
that first-order SDP–RLT convexifies every star interaction exactly, even
when all diagonal terms are convex and all mixed terms are submodular.
Stars still admit direct scalar elimination for objective minimization;
failure of this particular relaxation does not imply computational hardness.

## Verification record

Run the targeted exact check with

```text
python research-20260925/check_star_counterexample.py
```

It uses rational arithmetic to check positive definiteness, all McCormick
inequalities, the negative objective, the unit-cube affine transformation,
and the exact minimum of every reduced quadratic piece. It does not check
novelty or any unproved structural generalization.

An independent reviewer reconstructed the calculation from the literal
matrices using a separate SymPy script,
`research-20260925/check_star_independent_review.py`. That check verified all
63 nonempty principal minors, every RLT slack, the negative pairing, the
independently derived leaf formulas and reduced polynomials, and the
unit-cube polynomial. Manual review also checked the signs on each interval
and the absence of upper clipping. The independent check and the author
check both passed. This is evidence for the stated exact certificates, not
a novelty assessment or a formalized proof.

Before finding the obstruction, 20,000 constructed four-variable star
objectives and 500 fixed-moment four-variable star problems gave no
convincing numerical gap. Those searches motivated investigation but did
not prove exactness. The fixed-moment comparison used a scalar exact-form
support oracle inside floating-point LP column generation; it was not a
formal certificate. Temporary discovery scripts are not part of the
claimed proof. No project-wide checks or CI inspection were performed.
