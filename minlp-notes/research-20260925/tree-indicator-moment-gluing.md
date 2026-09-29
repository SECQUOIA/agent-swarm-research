# A strict gap from gluing second moments on a quadratic star

Date: 2026-09-25.

Status: exact derivations and targeted symbolic checks, with independent adversarial reviews of the [two-leaf gap](tree-indicator-moment-gap-review.md), [pairwise gap](tree-indicator-pair-gap-review.md), and [general transfer theorem](tree-indicator-projection-transfer-review.md). This is a limitation of specified moment relaxations, not a lower bound on the size of every formulation. No novelty claim is established.

## Problem and motivation

Consider the convex quadratic indicator epigraph

\[
 E_Q=\{(x,z,t):t\ge x^TQx,\quad x_i(1-z_i)=0,\quad
 z_i\in\{0,1\}\}.
\]

A star matrix has the form

\[
 Q=\begin{pmatrix}a&b^T\\b&D\end{pmatrix},\qquad
 D=\operatorname{diag}(d_i),\quad d_i>0,\quad
 \gamma=a-\sum_i b_i^2/d_i>0.
\]

We fix the center indicator to one. The center variable is an unrestricted real scalar, denoted by \(X\) in a probabilistic convex-combination interpretation. Each leaf has a binary activity indicator \(Z_i\) and a real value \(Y_i\), with \(Y_i=0\) when \(Z_i=0\).

The sparsity graph suggests combining the exact hulls of center–leaf pieces through the center's first two moments. The example below proves that common first and second moments do not suffice. The failure survives projection to the original epigraph variables: it is not merely a discrepancy in auxiliary moment variables. The example has two leaves, so its graph is also a three-vertex path; known compact path formulations remain exact and are not contradicted.

## Conditional leaf minimization

Write

\[
 \mathbb EX=x_0,\quad \mathbb EX^2=v,\quad
 \mathbb EZ_i=z_i,\quad \mathbb EXZ_i=s_i,\quad
 \mathbb EX^2Z_i=r_i,\quad \mathbb EY_i=y_i.
\]

For \(z_i>0\), completing the square and applying conditional Jensen gives

\[
 \inf_{Y_i:\,Y_i(1-Z_i)=0,\ \mathbb EY_i=y_i}
 \mathbb E[d_iY_i^2+2b_iXY_i]
 =\frac{d_i(y_i+(b_i/d_i)s_i)^2}{z_i}
   -\frac{b_i^2}{d_i}r_i.                         \tag{1}
\]

Equality holds for

\[
 Y_i=Z_i\left(\frac{y_i+(b_i/d_i)s_i}{z_i}
                    -\frac{b_i}{d_i}X\right).
\]

Thus, for a common law of the center and leaf indicators, the optimum expected quadratic cost is

\[
 av+\sum_i\left[
 \frac{d_i(y_i+(b_i/d_i)s_i)^2}{z_i}
 -\frac{b_i^2}{d_i}r_i\right].                    \tag{2}
\]

Define the moment matrices

\[
 M=\begin{pmatrix}1&x_0\\x_0&v\end{pmatrix},\qquad
 M_i=\begin{pmatrix}z_i&s_i\\s_i&r_i\end{pmatrix}.
\]

Every common law satisfies

\[
 0\preceq M_i\preceq M.                           \tag{3}
\]

The **individual moment relaxation** minimizes (2) subject to (3). Each inequality in (3) is a necessary second-moment condition for one leaf and its complement. These conditions do not assert that all leaf submeasures come from one common center law.

## Exact projected gap

Take

\[
 Q=\begin{pmatrix}3&1&1\\1&1&0\\1&0&1\end{pmatrix},
 \qquad x=(0,1,0),\qquad z=(1,1/2,1/2).
                                                               \tag{4}
\]

Here \(D=I\) and the Schur complement is \(3-1-1=1\), so \(Q\succ0\).

**Proposition.** At (4), the individual moment relaxation has value \(3/2\), while the lower boundary of \(\operatorname{cl\,conv}(E_Q)\) is

\[
 1+\frac1{\sqrt3}>\frac32.                         \tag{5}
\]

### Value of the relaxation

The local constraints are

\[
 r_i\ge2s_i^2,\qquad v-r_i\ge2s_i^2,
\]

and the objective is

\[
 3v+2(1+s_1)^2-r_1+2s_2^2-r_2.
\]

Using \(r_i\le v-2s_i^2\), this is at least

\[
 v+2+4s_1+4s_1^2+4s_2^2.
\]

The same constraints imply \(v\ge4s_1^2\). Consequently the objective is at least

\[
 2+4s_1+8s_1^2+4s_2^2
 =\frac32+8(s_1+1/4)^2+4s_2^2\ge\frac32.
\]

Equality is attained by

\[
 v=1/4,\quad s_1=-1/4,\quad r_1=1/8,\quad
 s_2=0,\quad r_2=1/4.
\]

At that point,

\[
 M=\begin{pmatrix}1&0\\0&1/4\end{pmatrix},\quad
 M_1=\begin{pmatrix}1/2&-1/4\\-1/4&1/8\end{pmatrix},\quad
 M_2=\begin{pmatrix}1/2&0\\0&1/4\end{pmatrix}.
\]

The matrices \(M_1\) and \(M-M_1\) both have rank one. A law realizing them must have \(X=-1/2\) on \(Z_1=1\) and \(X=1/2\) on \(Z_1=0\), each with probability one half. On the other hand, \(M-M_2\) has mass one half and zero second moment. A law realizing it must have \(X=0\) on \(Z_2=0\), an event of probability one half. These requirements are incompatible.

This incompatibility also rules out a limiting joint PSD-matrix decomposition: positive semidefinite summands of a rank-one matrix have ranges contained in its range. Every joint summand would have to respect both the two distinct rank-one ranges from leaf 1 and the incompatible zero-center range from the inactive part of leaf 2.

### Exact hull value

All convex combinations with leaf marginals one half have pattern probabilities

\[
 p_{00}=p_{11}=p,\qquad p_{10}=p_{01}=1/2-p,
 \qquad 0\le p\le1/2.                              \tag{6}
\]

For a pattern \(S\subseteq\{1,2\}\), let \(Q_{\{0\}\cup S}^{-1}\) be embedded in the full three-dimensional space by zeros outside its indices. With probabilities (6), let \(W(p)\) be the weighted sum of these embedded inverses. Standard quadratic minimization within each pattern gives the minimum expected cost at prescribed mean \(x\) as \(x^TW(p)^{-1}x\). For completeness, the optimum pattern means are

\[
 u_S=Q_{\{0\}\cup S}^{-1}h,
 \qquad h=W(p)^{-1}x,
\]

with restriction and embedding understood. They satisfy
\(\sum_Sp_Su_S=W(p)h=x\), and their expected quadratic cost is \(h^TW(p)h\). The matching lower bound follows by completing the square on each pattern.

Direct inversion yields

\[
 W(p)=\begin{pmatrix}
 p/3+1/2&-p/2-1/4&-p/2-1/4\\
 -p/2-1/4&p/2+3/4&p\\
 -p/2-1/4&p&p/2+3/4
 \end{pmatrix},
\]

and at the prescribed \(x\),

\[
 F(p)=x^TW(p)^{-1}x
 =\frac{4p^2-12p-15}{3(2p-3)(2p+1)}.
\]

The matrix \(W(p)\) is positive definite throughout \([0,1/2]\). At \(p=0\), the two single-leaf patterns jointly cover all coordinates; at \(p>0\), the full-support pattern has positive weight. Each nonzero vector therefore has a strictly positive quadratic form under the weighted inverse matrix.

Furthermore,

\[
 F'(p)=\frac{8(4p^2+12p-3)}
                  {3(2p-3)^2(2p+1)^2}.
\]

The numerator is strictly increasing on this interval and has its unique zero at \(p_* =\sqrt3-3/2\). This is the minimizer, and substitution gives
\(F(p_*)=1+\sqrt3/3\). Both endpoint values are \(5/3\). The pattern construction above attains this minimum by an actual finite convex combination, proving (5), including the asserted closed-hull value.

## What a common moment law requires

There is an exact cone description of joint compatibility, but it uses one matrix for every indicator pattern. Introduce symmetric matrices \(G_S\succeq0\), indexed by \(S\subseteq[n]\), and require

\[
 \sum_SG_S=M,\qquad \sum_{S:\,i\in S}G_S=M_i.       \tag{7}
\]

A common law gives (7) by setting

\[
 G_S=\mathbb E\left[
 \begin{pmatrix}1\\X\end{pmatrix}
 \begin{pmatrix}1&X\end{pmatrix}
 1_{\{i:Z_i=1\}=S}\right].
\]

Conversely, every PSD \(2\times2\) matrix whose top-left entry is positive is the moment matrix of a nonnegative scalar measure with at most two atoms. A matrix with zero top-left entry is necessarily \(\operatorname{diag}(0,r)\), \(r\ge0\), and is a limit of such moment matrices (mass \(\varepsilon\), atoms of magnitude \(\sqrt{r/\varepsilon}\)). Thus (7) describes the closure of the cone of jointly realizable moments. This closure qualification matters for general moment statements, even though all moments used to attain the true hull value in (5) are finitely realized.

When \(M\succ0\), congruence by \(M^{-1/2}\) normalizes (7) to PSD effects summing to the identity, with prescribed binary marginals. This is the mathematical condition called joint measurability of binary real qubit effects. It supplies useful existing language for the compatibility problem; it does not by itself supply a compact formulation. The completed [literature and significance assessment](tree-indicator-novelty-assessment.md) compares this established theory with the optimization transfer. The independent constraints (3) retain only one marginal at a time.

### Full compatibility gives the exact hull height

For completeness, fix a center mean \(x_0\in\mathbb R\), leaf means
\(y\in\mathbb R^n\), and leaf masses \(z\in(0,1)^n\). The minimum of
(2) over all moments admitting (7) equals the lower boundary of both the
ordinary and closed convex hulls of \(E_Q\) at these original means and
the center indicator fixed to one. The minimum is attained by an actual
finite common scalar law. This is an exact characterization with one
PSD block per indicator pattern, not a compact formulation claim.

Here is the argument, also checked in the
[independent transfer review](tree-indicator-projection-transfer-review.md).
Write \(w_i=b_i^2/d_i\), so \(\gamma=a-\sum_iw_i>0\).
Feasibility with finite cost follows by taking the center constantly equal
to \(x_0\), independent indicators with means \(z_i\), and active leaf
values \(y_i/z_i\).
Every compatible tuple satisfies \(0\le r_i\le v\); the objective in
(2) is consequently at least \(\gamma v\). A nonempty objective sublevel
set has bounded \(v,r,s\). The full compatibility set is closed: along
a convergent sequence, every joint block satisfies \(0\preceq G_S\preceq M\),
so all finitely many blocks have a convergent common subsequence. The
objective is continuous because all \(z_i>0\). A minimum therefore exists.

If a block in a minimizing parent has zero top-left entry, it is
\(G_S=\operatorname{diag}(0,\rho)\) for some \(\rho\ge0\).
Deleting it preserves the center mean, total mass, and all selected
first moments and masses. It decreases (2) by

\[
 \left(a-\sum_{i\in S}w_i\right)\rho\ge\gamma\rho.
\]

Optimality forces \(\rho=0\). Each remaining nonzero block thus has
positive mass and admits a scalar measure with at most two atoms.
Combining these measures by indicator pattern gives a finite common law.
The leaf values in the equality formula following (1) attain (2) exactly.
This proves attainment in the ordinary convex hull.

Every convex combination of original feasible points induces such a
compatible tuple and has expected cost at least (2). For a convergent
sequence of such combinations with bounded epigraph coordinate,
positive definiteness bounds all center second moments; the joint blocks
then have a convergent subsequence as above. At the target interior
masses, (2) is continuous also in the original means and masses.
The same lower bound passes to the closed hull. This addresses varying
means in the approximating sequence, not just limits within one fixed
slice.

## Scope, prior work, and remaining questions

The example establishes a strict gap for one specific relaxation. It neither precludes a compact SOCP/SDP lift for arbitrary stars nor proves a new complexity lower bound. Even this example is a path, and exact polynomial-size path formulations are already known.

Choi, Fattahi, Han, Gómez, and Lozano, *Convexification of mixed-integer quadratic optimization via decision diagrams*, arXiv:2608.22815, Section 7.2, give an exact SOCP lift of size \(O(n^{k+1})\) for a rooted quadratic-support tree with \(k\) leaves. Their result is polynomial for fixed \(k\); it gives no uniform polynomial bound as the number of star leaves grows. Their introduction also cites the polynomial-time optimization algorithm of Bhathena, Fattahi, Gómez, and Küçükyavuz for arbitrary trees. These results mean that a failure of (3) is a formulation-design obstacle, not evidence of hardness of star optimization.

Local source examined: `literature/papers/choi2026-convexification-of-mixed-integer-quadratic/fulltext.md`, especially Section 7.2 and its discussion of the fixed-leaf parameter. Existing common-factor least-law notes were also examined. Those notes constrain selected first moments and a common convex moment; (2) additionally contains negatively weighted selected second moments, so that earlier least-law construction does not apply directly.

Whether joint compatibility restricted to the objective directions in (2)
has a smaller formulation than the full moment cone remains open here.
The second question raised by these examples is now resolved in the
[quantitative construction](star-subset-accuracy-lower.md): checking every
subset of at most \(k\) leaves can leave a rational, uniformly conditioned
original-epigraph gap of order at least \(k^{-2}\). Its subsets share only
the center and single-leaf matrices, with no higher-order overlap moments.

## Targeted verification

Two inline `python` commands using SymPy were run. They computed the four embedded principal inverses, formed \(W(p)\), derived the displayed rational function and derivative, solved its stationary equation, and simplified the value at \(p_*\) to \(1+\sqrt3/3\). These are exact symbolic checks of the algebra. The displayed square-completion argument independently proves the relaxation value. The checks do not establish novelty and do not replace independent proof review. No project-wide tests or CI inspection were performed.

## Pairwise compatibility also leaves an original-epigraph gap

The following extension was developed with the parent research agent and checked independently here. It shows that adding exact compatibility for every pair of leaf indicators still does not solve the common-law problem.

Use three leaves with

\[
 a=4,\quad b_i=d_i=1,\quad
 x=(0,-1,1,0),\quad z=(1,1/4,1/4,1/4).             \tag{8}
\]

The star matrix is positive definite because its Schur complement is \(4-3=1\). The exact closed-hull epigraph value at (8) is

\[
 \frac{96}{17}.
                                                               \tag{9}
\]

A feasible point of the pairwise compatibility relaxation has objective

\[
 \frac{359}{64}<\frac{96}{17},\qquad
 \frac{96}{17}-\frac{359}{64}=\frac{41}{1088}.       \tag{10}
\]

This does not assert that \(359/64\) is the relaxation optimum; a feasible relaxation value suffices to establish a strict gap.

### Rational compatibility witnesses

Take

\[
 M=\operatorname{diag}(1,27/32),\quad
 M_1=\begin{pmatrix}1/4&5/16\\5/16&27/64\end{pmatrix},
 \quad
 M_2=\begin{pmatrix}1/4&-5/16\\-5/16&27/64\end{pmatrix},
 \quad
 M_3=\operatorname{diag}(1/4,45/64).
\]

Two effects \(M_i,M_j\) have a joint PSD decomposition precisely when some symmetric \(G_{ij}\) makes all four matrices

\[
 G_{ij},\quad M_i-G_{ij},\quad M_j-G_{ij},\quad
 M-M_i-M_j+G_{ij}
\]

positive semidefinite. For pair \(1,2\), use \(G_{12}=0\). The matrices \(M_1,M_2\) have determinant \(1/128\), and the last matrix is \(\operatorname{diag}(1/2,0)\).

For pair \(1,3\), use

\[
 G_{13}=\frac1{128}\begin{pmatrix}18&26\\26&39\end{pmatrix}.
\]

In the displayed order, the four matrices have determinants

\[
 \frac{13}{8192},\quad\frac7{8192},\quad
 \frac{19}{8192},\quad\frac{25}{8192}.
\]

Their diagonal entries are positive, so all four are positive definite. For pair \(2,3\), change the sign of the off-diagonal entries of \(G_{13}\); the same determinant check applies by congruence with \(\operatorname{diag}(1,-1)\). Thus all pairs are jointly compatible and use the same first and second center moments.

Substituting these moments into (2) gives

\[
 4\frac{27}{32}
 +4\left[\left(-1+\frac5{16}\right)^2
          +\left(1-\frac5{16}\right)^2\right]
 -2\frac{27}{64}-\frac{45}{64}=\frac{359}{64}.
\]

### Exact hull lower bound and attainment

Let \(W\) be the mean embedded principal inverse over any distribution of leaf supports with the prescribed marginals. Its cost at the fixed mean is \(x^TW^{-1}x\). The inverse expression is well-defined here: each coordinate is active with positive probability, so \(W\succ0\).

Average this distribution with its image under exchanging leaves 1 and 2. The mean-support constraint is preserved. This exchange sends \(x\) to \(-x\); therefore the cost is unchanged before averaging, and convexity of \(x^TW^{-1}x\) in \(W\) shows that averaging cannot increase it. We may consequently restrict attention to support distributions invariant under that exchange.

Then \(x\) is an eigenvector of \(W\), with eigenvalue

\[
 d=W_{11}-W_{12}.
\]

For a binary support vector \(q\in\{0,1\}^3\), put \(k=q_1+q_2+q_3\). The contribution to this eigenvalue after symmetrization is

\[
 \eta(q)=\frac{q_1+q_2}{2}
       +\frac{(q_1-q_2)^2}{2(4-k)}.
\]

For every one of the eight support patterns,

\[
 \eta(q)\le\frac23(q_1+q_2)+\frac1{12}q_3.         \tag{11}
\]

One can verify (11) directly: it is an equality on the empty support and on \(\{1\},\{2\},\{1,3\},\{2,3\}\); its slack on \(\{3\},\{1,2\},\{1,2,3\}\) is respectively \(1/12,1/3,5/12\). Taking expectations yields

\[
 d\le\frac23\frac12+\frac1{12}\frac14=\frac{17}{48}.
\]

Since \(\|x\|^2=2\), every symmetric distribution has cost
\(2/d\ge96/17\). This lower bound is attained by assigning mass \(1/8\) to each of \(\{1\},\{2\},\{1,3\},\{2,3\}\) and mass \(1/2\) to the empty support. The required leaf marginals are all \(1/4\), and every positive-mass pattern is tight in (11). The patternwise quadratic minimizers then supply a finite convex combination attaining (9).

An additional inline SymPy command independently checked every rational determinant above, the objective and gap in (10), and all eight cases of (11). The exact hull proof uses symmetry and a valid supportwise inequality, rather than numerical optimization.

## Transferring any local moment incompatibility to a star epigraph

The preceding examples are instances of a general transfer argument. This section was derived in the current research session and passed an [independent adversarial review](tree-indicator-projection-transfer-review.md). The theorem concerns a specified hierarchy of moment formulations. It does not establish extension-complexity lower bounds for arbitrary formulations.

Fix a real center mean \(m\) and masses \(z_i\in(0,1)\). Let \(\mathcal J(m,z)\) be the set of tuples \((v,s,r)\) for which the matrices

\[
 M=\begin{pmatrix}1&m\\m&v\end{pmatrix},\qquad
 M_i=\begin{pmatrix}z_i&s_i\\s_i&r_i\end{pmatrix}
\]

admit the full joint decomposition (7). For an integer \(1\le k\le n\), let \(\mathcal J_k(m,z)\) require a joint decomposition only for each subfamily of at most \(k\) leaves, with the same \(M,M_i\) in every subfamily. The joint decompositions for different subfamilies need not agree on higher-order pattern moments over their intersections. We call this the subsetwise \(k\)-leaf compatibility relaxation; the theorem below makes no claim about hierarchies that impose those additional consistency constraints. Thus \(\mathcal J_1\) is (3), and \(\mathcal J_2\) adds the pairwise conditions above.

**Transfer theorem.** Suppose

\[
 (v^*,s^*,r^*)\in\mathcal J_k(m,z)\setminus\mathcal J(m,z).
                                                               \tag{12}
\]

After possibly complementing some leaf marginals, there exist a positive definite star matrix \(Q\), with every edge coefficient nonzero, and prescribed leaf means \(y\), such that minimizing (2) over \(\mathcal J_k\) gives a value strictly below the exact closed-hull epigraph value at \(x=(m,y)\), center indicator one, and those leaf marginals.

### Separation and the sign of second-moment coefficients

The set \(\mathcal J(m,z)\) is closed and convex. For closedness, consider a convergent sequence of tuples and choose a joint decomposition for each. Every summand satisfies \(0\preceq G_S\preceq M\). Since the total matrices have bounded entries, all summands have bounded entries. Passing to a subsequence for the finitely many patterns gives a joint decomposition of the limit.

Strong separation of (12) therefore gives real coefficients and a scalar \(\ell\) with

\[
 L(v,s,r)=av+\sum_i(u_i s_i+c_i r_i)\ge\ell
 \quad\hbox{on }\mathcal J(m,z),\qquad
 L(v^*,s^*,r^*)<\ell.                              \tag{13}
\]

For any support \(S\), adding \(\tau\operatorname{diag}(0,1)\), \(\tau\ge0\), to its joint matrix is a recession direction of \(\mathcal J(m,z)\). It increases \(v\) by \(\tau\), and \(r_i\) by \(\tau\) for \(i\in S\). Since (13) is bounded below along that direction,

\[
 a+\sum_{i\in S}c_i\ge0\qquad\text{for every }S.   \tag{14}
\]

If \(c_i>0\), replace leaf \(i\) by its complement:

\[
 z_i'=1-z_i,\quad s_i'=m-s_i,\quad r_i'=v-r_i.
\]

Both full and \(k\)-local compatibility are preserved by this operation. The coefficient of \(r_i'\) becomes \(-c_i\), the coefficient of \(s_i'\) becomes \(-u_i\), and the coefficient of \(v\) increases by \(c_i\); a constant is absorbed into \(\ell\). Dropping primes after this transformation, (13) has the form

\[
 L=av+\sum_i(u_i s_i-w_i r_i),\qquad
 w_i\ge0,\quad a\ge\sum_iw_i.                     \tag{15}
\]

The last inequality follows from (14), or by taking the full-support recession direction after complementation.

To make these inequalities strict where needed, replace \(L\) by

\[
 L_\varepsilon=L+
 \varepsilon\left[(n+1)v-\sum_i r_i\right],
 \qquad\varepsilon>0.
\]

Every full or locally compatible tuple satisfies \(0\le r_i\le v\), so the added expression is nonnegative. Thus the lower bound \(L_\varepsilon\ge\ell\) remains valid on the full set. At the prescribed fake point it is finite, so sufficiently small \(\varepsilon\) preserves strict violation. The new coefficients satisfy

\[
 w_i>0,\qquad a>\sum_iw_i.
\]

We again drop the perturbation notation.

### Building the quadratic objective

Choose

\[
 d_i=b_i=w_i,\qquad
 y_i=\frac{z_i u_i}{2w_i}-s_i^*.
\]

Then \(d_i>0\), \(b_i\ne0\), and the star Schur complement is
\(a-\sum_i b_i^2/d_i=a-\sum_iw_i>0\). The resulting matrix is positive definite. Formula (2) becomes

\[
 F(v,s,r)=av+\sum_i\frac{w_i(y_i+s_i)^2}{z_i}
                   -\sum_iw_i r_i.
\]

The choice of \(y_i\) gives the exact identity

\[
 F(v,s,r)=L(v,s,r)+C+
                  \sum_i\frac{w_i}{z_i}(s_i-s_i^*)^2,          \tag{16}
\]

where \(C=\sum_i[z_i u_i^2/(4w_i)-u_i s_i^*]\) is independent of \((v,s,r)\). Consequently,

\[
 F(v^*,s^*,r^*)=L(v^*,s^*,r^*)+C<\ell+C,
 \qquad F(v,s,r)\ge\ell+C\quad\text{on }\mathcal J(m,z).
\]

The fake point is feasible for the \(k\)-local relaxation, while every actual convex combination of indicator-feasible quadratic points induces fully compatible center moments and has cost at least \(F\). This proves a strict gap for the convex hull.

The same lower bound holds for its closure. Indeed, along a convergent sequence of convex combinations with bounded epigraph coordinate, positive definiteness of \(Q\) bounds the expected squared norm and hence the center second moments. The selected first and second moments are then bounded by the PSD inequalities. Pass to a subsequence of all finitely many joint matrices \(G_S\), each bounded by its total matrix \(M\). Their limits give a full joint decomposition with exactly the limiting center mean and leaf masses, even though the approximating combinations can have different means and masses. Since the prescribed masses stay strictly positive, formula (2) is continuous at the limit. Its lower bound therefore passes to the closed hull.

### Implication and limit of the theorem

Any established family of binary real-qubit effects whose every \(k\)-subfamily is compatible, but whose full family is not, supplies a strict gap in the original variables of some positive definite star quadratic epigraph. The transfer does not depend on the incompatibility being visible through a preselected quadratic objective: it constructs an objective that exposes it.

The connection to arbitrary-order quantum incompatibility is documented in
[the first explicit family](star-hierarchy-specker-gap.md), with the
strongest completed normalization and accuracy bounds in
[the quantitative construction](star-subset-accuracy-lower.md).
Joint-measurement incompatibility is existing theory. The contribution
under investigation is its transfer to positive definite indicator-quadratic
epigraphs and the resulting limitation of this specified hierarchy.
