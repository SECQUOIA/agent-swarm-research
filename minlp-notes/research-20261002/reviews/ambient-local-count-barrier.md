# Ambient dimension in actual convex-QP local counts

Date: 2026-10-02. This note gives an explicit obstruction to removing
ambient dimension from the grid-count argument in
[the ambient-noise closure theorem](../new-direction/smoothed-ambient-cell-closure.md).
It uses actual convex recourse QPs, polynomially many linear constraints,
and a genuinely nonconvex feasible objective with one negative eigenvalue.
It is a lower bound on local and near-optimal grid-node counts, not a
lower bound on the work of an algorithm that closes quadratic pieces.

The rank-one family has ambient dimension \(n=m^2\), fixed noise scale,
and fixed projected feasible width. With fixed negative curvature it has
\(\Omega(m)\) expected local-comparison nodes and
\(\Omega(\sqrt m)\) expected globally near-optimal nodes at suitable
deterministic levels. Independent products give the corresponding
\((n/k)^{k/2}\) and \((n/k)^{k/4}\) powers in dimension \(n\).

## 1. Rational data with one negative eigenvalue

Let \(m\ge256\) be even and \(n=m^2\). Choose a rational unit vector
\(u\in\mathbb Q^n\) with \(n/2\) entries \(+1/m\) and \(n/2\)
entries \(-1/m\). The last two entries are both positive. Write
\(B_+\) and \(B_-\) for the positive and negative index sets among
the first \(n-2\) coordinates. Thus

\[
 |B_+|=n/2-2,\qquad |B_-|=n/2.
\]

Put

\[
 q=e_{n-1}-e_n,\quad c=3/4,\quad Y=4,\quad
 \epsilon=m^{-3},\quad T=u^T,
\]

and take either \(\alpha=1\) or \(\alpha=m\). Define

\[
 P=\alpha\bigl[uu^T+c(uq^T+qu^T)+qq^T\bigr],\qquad
 A=P-\alpha uu^T.
                                                        \tag{1}
\]

In the orthonormal basis \((u,q/\sqrt2)\), the nonzero blocks are

\[
 P=\alpha\begin{pmatrix}1&c\sqrt2\\c\sqrt2&2\end{pmatrix},
 \qquad
 A=\alpha\begin{pmatrix}0&c\sqrt2\\c\sqrt2&2\end{pmatrix}.
                                                        \tag{2}
\]

The first block is positive definite because its determinant is
\(2(1-c^2)>0\). Consequently \(P\succeq0\) and
\(\ker P\subseteq\ker T\). Also \(TT^T=1\). The matrix \(A\)
has exactly one negative eigenvalue, with magnitude

\[
 \nu=\alpha\left(\sqrt{17/8}-1\right).
                                                        \tag{3}
\]

Thus \(\alpha/\nu\) is an absolute constant and
\(\alpha<4\nu\). This construction does not obtain its count from
a convex objective with a redundant negative factor or from an
unbounded ratio between the supplied correction and the negative curvature.
The supplied factor is rational and perfectly conditioned; no assertion
is needed that a particular spectral-normalization implementation returns
this same factor.

The signs in \(u\) only simplify the polytope description below.
Reflecting every negative coordinate preserves the independent cube-noise
law and changes the factor to the all-ones row \((1/m,\ldots,1/m)\).
The transformed polytope still has \(O(n)\) rational constraints.

The polytope \(X\) is given by

\[
 \begin{split}
 x_i&\ge0 &&(1\le i\le n-2),\\
 \sum_{i=1}^{n-2}x_i&=mY,\\
 x_{n-1}+x_n&=0,\\
 |x_{n-1}-x_n|&\le\epsilon.
 \end{split}                                             \tag{4}
\]

Equalities may be written as pairs of inequalities. There are \(O(n)\)
constraints, and all data have polynomial rational encoding length.
Set

\[
 y=Tx,\qquad z=q^Tx.
\]

The last two coordinates are \((z/2,-z/2)\). The feasible image in
\((y,z)\) is exactly \([-Y,Y]\times[-\epsilon,\epsilon]\), so
the projected feasible width is \(2Y=8\), independently of \(m\).
With zero base linear and constant terms, the objective is

\[
 F(x)=\tfrac12x^TAx=\alpha(cyz+z^2/2).
                                                        \tag{5}
\]

Its Hessian in feasible coordinates \((y,z)\) has determinant
\(-\alpha^2c^2<0\). Since the feasible rectangle has nonempty
interior in these coordinates, the objective is nonconvex on \(X\).
The narrow \(z\)-interval is a stated feature of the family.

## 2. Exact recourse formula and a common event

Let the original noise coordinates be independently uniform on
\([-1,1]\). Define

\[
 d=u^T\gamma,\qquad r=\gamma-ud,
\]

and use the auxiliary objective

\[
 W_r(a)=\min_{x\in X}\{F(x)+r^Tx+\alpha(a-Tx)^2/2\},
 \qquad V_\gamma(a)=W_r(a)+da.
                                                        \tag{6}
\]

At fixed \(y\), the two active groups have total masses
\(m(Y+y)/2\) and \(m(Y-y)/2\). Minimizing a linear objective
over each simplex gives

\[
 \min r^Tx=L_r+C_ry+t z,
\]

where

\[
 \begin{split}
 L_r&=\frac{mY}{2}\left(\min_{B_+}r_i+\min_{B_-}r_i\right),\\
 C_r&=\frac m2\left(\min_{B_+}r_i-\min_{B_-}r_i\right),\\
 t&=(\gamma_{n-1}-\gamma_n)/2\in[-1,1].
 \end{split}                                             \tag{7}
\]

The first formula means minimization over the active coordinates with
\((y,z)\) fixed. In particular the residual difference in the last
two coordinates equals the original noise difference.

Put

\[
 S=\frac m2\left(\min_{B_+}\gamma_i-
                       \min_{B_-}\gamma_i\right).
\]

The signs of \(u\) imply the exact cancellation

\[
 C_r=S-d.                                                \tag{8}
\]

Whenever the inner optimum has \(|y|<Y\), stationarity in \(y\)
gives

\[
 y=a-C_r/\alpha-cz,\qquad
 V_\gamma'(a)=S+\alpha c z.                             \tag{9}
\]

The recourse objective is strictly convex in \((y,z)\), so these
formulas are unambiguous even if several simplex coordinates tie.

Consider the event

\[
 E=\left\{
 \min_{B_+}\gamma_i\le-1+4/n,\quad
 \min_{B_-}\gamma_i\le-1+4/n,\quad |d|\le2
 \right\}.
                                                        \tag{10}
\]

The first two events are independent. Since
\(|B_+|\ge15n/32\), their intersection has probability at least
\((1-e^{-15/16})(1-e^{-1})\). Also
\(\operatorname{Var}(d)=1/3\), so Chebyshev's inequality gives
\(\Pr\{|d|>2\}\le1/12\). No independence from \(d\) is assumed.
It follows that

\[
\Pr(E)\ge(1-e^{-15/16})(1-e^{-1})-1/12>1/4.
                                                        \tag{11}
\]

The same lower bound \(\Pr(E)>1/4\) holds for independent uniform
noise on an equally spaced endpoint grid with \(N_0\ge64n\) points.
Each lower tail in (10) then has probability at least
\(2/n-1/N_0\ge19/(10n)\), and
\(\operatorname{Var}(d)=(N_0+1)/(3(N_0-1))<0.336\). Consequently

\[
 \Pr(E)\ge(1-e^{-57/64})(1-e^{-19/20})-0.084>1/4.
\]

This is a finite-law statement as well as a continuous one. It does not
require noise precision to depend on the chosen grid level.

On this event,

\[
 |S|\le2/m,\quad |C_r|\le2+2/m,\quad
 \alpha c\epsilon\le3/(4m^2).
                                                        \tag{12}
\]

For every \(|a|\le3/2\) and every feasible \(z\), the unconstrained
stationary value \(a-C_r/\alpha-cz\) is strictly between \(-Y\)
and \(Y\). Thus (9) applies throughout this interval, and

\[
 |V_\gamma'(a)|<3/m.                                   \tag{13}
\]

## 3. Actual local events on a deterministic full-domain grid

The full auxiliary domain prescribed by the ambient theorem is

\[
 A_{\rm aux}=[-Y-m/\alpha,Y+m/\alpha],\qquad
 w=2Y+2m/\alpha,
                                                        \tag{14}
\]

because \(\sum_i|u_i|=m\). Use its deterministic nested dyadic
grids, with step \(h=w2^{-j}\). Choose a level for which

\[
 \frac{16}{\alpha m}\le h\le\frac{32}{\alpha m}.
                                                        \tag{15}
\]

Such a level exists, and \(h\le1/2\). Every grid node
\(v\in[-1,1]\) and its two neighbors lie in \([-3/2,3/2]\).
By (13), on the same event \(E\) all these nodes satisfy

\[
 V_\gamma(v)\le V_\gamma(v\pm h)+\alpha h^2/4.
                                                        \tag{16}
\]

This is precisely the local event from the ambient theorem, since
\(B=\alpha h^2/8\) in rank one. There are at least
\(2/h-1\ge\alpha m/32\) such nodes. Consequently

\[
 \mathbb E\#\{v:E_v\}\ge\alpha m/128.
                                                        \tag{17}
\]

For \(\alpha=1\), the noise scale, negative curvature, and projected
feasible width are fixed, yet this expectation is \(\Omega(\sqrt n)\).
The auxiliary width in (14) grows with \(m\).

For \(\alpha=m\), the auxiliary width is the fixed value \(10\).
The expectation is then \(\Omega(m^2)=\Omega(n)\), whereas a
putative bound \(O(1+\alpha w)\) without the volume lemma's
\(\sqrt n\) factor would be only \(O(m)\). This second version
isolates the extra \(\sqrt n\) in the local-event estimate; its
negative curvature grows with \(m\).

## 4. Globally near-optimal nodes

The same phenomenon is not confined to local comparisons. Completing
the square in (6) yields, up to a constant independent of \(a,y,z\),

\[
 V_\gamma(a)=\min_{|y|\le Y,\ |z|\le\epsilon}
 \left[G(y,z)+\frac\alpha2(a-y+d/\alpha)^2\right],
\]

where

\[
 G(y,z)=\alpha(cyz+z^2/2)+S y+t z.                      \tag{18}
\]

Minimizing also over \(a\) removes the square. On \(E\), for
each \(|a|\le1\) the trial point \((y,z)=(a+d/\alpha,0)\) is
feasible and has \(G(y,0)\le6/m\). Every feasible point satisfies

\[
 G(y,z)\ge-8/m-3/m^2-1/m^3.
\]

Therefore

\[
 V_\gamma(a)-\min V_\gamma<15/m\qquad(|a|\le1).
                                                        \tag{19}
\]

Choose a deterministic dyadic level with

\[
 \frac8{\sqrt{\alpha m}}\le h\le
 \frac{16}{\sqrt{\alpha m}}.
                                                        \tag{20}
\]

Its tolerance \(2B=\alpha h^2/4\) is at least \(16/m\).
On \(E\), every node in \([-1,1]\) is thus globally
\(2B\)-near-optimal, even relative to the continuous auxiliary minimum.
There are at least \(\sqrt{\alpha m}/16\) such nodes. Hence

\[
 \mathbb E\#\{\text{globally }2B\text{-near-optimal nodes}\}
 \ge\sqrt{\alpha m}/64.
                                                        \tag{21}
\]

This is \(\Omega(n^{1/4})\) with fixed curvature \(\alpha=1\),
and \(\Omega(\sqrt n)\) with fixed auxiliary width \(\alpha=m\).

## 5. Products and the limit of the conclusion

Take \(k\) independent copies with the same \(m,\alpha\). The total
ambient dimension is \(N=km^2\), the Hessian has exactly \(k\)
negative eigenvalues, and the disjoint factor rows satisfy \(TT^T=I_k\).
The constraints remain polynomial in \(N\). Each projected coordinate
has width \(8\), and all copies use the same deterministic grid step.

The intersection of the block events has probability greater than
\(4^{-k}\). Cartesian products of the central nodes satisfy the
multidimensional local event: its tolerance
\(2B=\alpha k h^2/4\) is at least the scalar tolerance used in (16).
Thus at the level (15),

\[
 \mathbb E\#\{v:E_v\}\ge(\alpha m/128)^k.              \tag{22}
\]

At the level (20), each block gap is below \(15/m\), so the summed
gap is below \(15k/m<2B\). Therefore

\[
 \mathbb E\#\{\text{globally }2B\text{-near-optimal nodes}\}
 \ge(\sqrt{\alpha m}/64)^k.                             \tag{23}
\]

With \(\alpha=1\), these are respectively
\(128^{-k}(N/k)^{k/2}\) and \(64^{-k}(N/k)^{k/4}\), with all
per-coordinate projected widths and curvature-to-noise ratios fixed.
These counts preclude a dimension-free bound for the corresponding
full-grid counts in only those intrinsic parameters.

They do not prove that the exact-closure solver visits all these nodes.
In this construction, the noise chooses one minimal coordinate in each
simplex group; subsequent recourse depends only on \((y,z)\). Its
few quadratic pieces can be easy to extract and close. Neither (22)
nor (23) is an algorithmic lower bound, a bit-complexity lower bound,
or a hardness result. The result identifies an obstruction to replacing
the ambient theorem's counting argument by a dimension-free version of
the same local or near-optimal grid count.

## 6. Verification scope

The construction is algebraic; equations (2), (7)--(9), and (18) are
exact identities. The probability estimate uses independent block minima
and a separate union bound for \(d\), not conditional independence of
the factor noise. Two separate analytic readers checked the rank-one
construction; one also checked the product and near-optimality arguments.

The targeted command

```sh
python research-20261002/new-direction/check_ambient_local_qp_barrier.py
```

passed 12 rational ambient-noise fixtures satisfying \(E\), 144 exact
derivative identities, 286 local comparisons, and 84 global-gap checks.
It covered both choices of \(\alpha\) and all three cases where the
thin coordinate is at its lower bound, interior, or upper bound. The
checker solves the reduced convex rectangle QP by enumerating its
interior stationary point and boundary minima. It computes the original
nonconvex minimum separately, using its affine dependence on \(y\).
These finite fixtures check the formulas and inequalities; they do not
establish the probability bound or measure the full closure algorithm.

Scoped whitespace and local Markdown-link checks passed. No project-wide
check or CI inspection was performed.
