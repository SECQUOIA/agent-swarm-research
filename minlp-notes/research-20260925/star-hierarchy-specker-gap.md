# Arbitrary-order local moment gaps for strictly convex quadratic stars

Date: 2026-09-25.

Status: explicit proof and targeted numerical checks. The quantum compatibility
construction is established prior work. The transfer to a strict gap in the
original quadratic indicator epigraph is developed here; its novelty has not
been established. An independent adversarial review verified the main argument; the
checks and limitations are recorded below.

## Result and scope

For every integer \(k\ge1\), there is a positive definite quadratic star with
\(k+1\) leaves for which imposing joint scalar second-moment compatibility on
every group of at most \(k\) leaves gives a strict gap after projection to the
original epigraph variables. Thus no fixed order of this particular hierarchy
is uniformly exact on positive definite stars.

This statement concerns the hierarchy that shares the center moment matrix
and the single-leaf moment matrices between groups. It does not concern a
stronger hierarchy that also identifies selected joint moments on group
intersections. It does not rule out other polynomial-size formulations or
efficient optimization algorithms for stars.

The starting model and the leaf-elimination identity are documented in
[tree-indicator-moment-gluing.md](tree-indicator-moment-gluing.md). This note
gives an explicit family, rather than relying on an abstract separation
argument.

## The precise relaxation

The center indicator is fixed to one. At fixed original means \(x_0=0\),
\(y_i\in\mathbb R\), and leaf activity means \(0<z_i<1\), write

\[
 M=\begin{pmatrix}1&0\\0&v\end{pmatrix},\qquad
 M_i=\begin{pmatrix}z_i&s_i\\s_i&r_i\end{pmatrix}.
\]

For an index set \(J\), compatibility means that there are matrices
\(G^J_S\succeq0\), \(S\subseteq J\), satisfying

\[
 \sum_{S\subseteq J}G^J_S=M,\qquad
 \sum_{S\ni i}G^J_S=M_i\quad(i\in J).                 \tag{1}
\]

These equations describe the closure of the jointly realizable scalar
moment cone. The subsetwise \(k\)-leaf compatibility relaxation imposes (1) for every \(J\) of size at
most \(k\), sharing \(M,M_i\), and minimizes

\[
 F(v,s,r)=a v+\sum_i\left[
   \frac{(y_i+b_i s_i)^2}{z_i}-b_i^2r_i\right].        \tag{2}
\]

The original quadratic has center diagonal \(a\), leaf diagonal entries one,
and center-leaf entries \(b_i\). For every true joint law, conditional
square completion proves that its expected quadratic cost is at least (2).
Every finite convex combination therefore satisfies each lower bound on (2)
proved using full joint compatibility.

## Explicit construction

Put \(N=k+1\ge2\), and define

\[
 \alpha=\frac{\pi}{2N},\qquad
 \theta_j=\frac\pi2+\frac\pi{4N}+\frac{j\pi}{N}
 \quad(j=0,\ldots,N-1),\qquad R=\csc\alpha.
\]

Choose any

\[
 \frac{R}{N}<\eta<
 \frac1{(N-2)\sin\alpha+\sin(2\alpha)}.              \tag{3}
\]

The interval is nonempty because
\(\sin(2\alpha)<2\sin\alpha\). The strict upper inequality is convenient but
can be replaced by a weak one. In particular \(0<\eta<1\), so all activity
means below lie strictly between zero and one.

Define the candidate moment point by

\[
 v^*=1,\quad z_j=\frac{1+\eta\cos\theta_j}{2},\quad
 s_j^*=\frac{\eta\sin\theta_j}{2},\quad
 r_j^*=\frac{1-\eta\cos\theta_j}{2}.                  \tag{4}
\]

Set

\[
 w_j=-\cos\theta_j>0,\quad
 W=\sum_j w_j=R\cos\frac\pi{4N}<R,\quad
 a=\frac{R+W}{2},\quad b_j=\sqrt{w_j},               \tag{5}
\]

and choose the original leaf means as

\[
 y_j=-b_j s_j^*-\frac{z_j\sin\theta_j}{b_j}.         \tag{6}
\]

The quadratic matrix is positive definite, since its Schur complement is

\[
 a-\sum_jb_j^2=\frac{R-W}{2}>0.                     \tag{7}
\]

**Theorem.** For (3)--(6), the subsetwise \((N-1)\)-leaf compatibility relaxation has value at most
\(F(v^*,s^*,r^*)\), whereas the true closed convex hull at
\(x=(0,y)\), \(z=(1,z_0,\ldots,z_{N-1})\) has lower boundary at least

\[
 F(v^*,s^*,r^*)+N\eta-R.
                                                               \tag{8}
\]

The gap in (8) is strictly positive by (3). The bound need not be the exact
closed-hull value.

## Why every proper subfamily is compatible

Use the real symmetric matrices

\[
 \sigma_x=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
 \sigma_z=\begin{pmatrix}1&0\\0&-1\end{pmatrix}.
\]

The matrices in (4) are unbiased real qubit effects

\[
 M_j^*=\frac12\left[I+\eta(\sin\theta_j\,\sigma_x+
                                     \cos\theta_j\,\sigma_z)\right].
                                                               \tag{9}
\]

The following elementary planar criterion gives a self-contained compatibility
proof. For \(u_i\in\mathbb R^2\), effects
\(A_i=(I+u_{i,x}\sigma_x+u_{i,z}\sigma_z)/2\) are jointly compatible if and only
if the perimeter of \(P=\operatorname{conv}\{\pm u_i\}\) is at most four.
For a segment, perimeter means twice its length.

For necessity, write a joint parent indexed by sign patterns as
\(G_\varepsilon=(q_\varepsilon I+g_\varepsilon\cdot\sigma)/2\).
Positivity and normalization give
\(\|g_\varepsilon\|\le q_\varepsilon\),
\(\sum q_\varepsilon=2\), and
\(u_i=\tfrac12\sum_\varepsilon\varepsilon_i g_\varepsilon\).
Consequently \(P\) is contained in the planar zonotope

\[
 Z=\sum_\varepsilon[-g_\varepsilon/2,g_\varepsilon/2].
\]

Its perimeter is \(2\sum_\varepsilon\|g_\varepsilon\|\le4\).
Perimeter is monotone under inclusion of planar convex bodies, proving the
necessary inequality. If the original parent is complex, taking entrywise
real parts first preserves positive semidefiniteness and the real marginals.

For sufficiency, every centrally symmetric planar polygon has a zonotope
decomposition \(P=\sum_j[-h_j,h_j]\), with
\(\sum_j\|h_j\|=\operatorname{perim}(P)/4\le1\). One may obtain the generators
as half of one edge from each opposite pair of edges. Use parent effects

\[
 H_{j,\pm}=\frac12(\|h_j\|I\pm h_j\cdot\sigma)
\]

and the residual effect \((1-\sum_j\|h_j\|)I\). Write each point
\(u_i=\sum_j t_{ij}h_j\), where \(-1\le t_{ij}\le1\).
On outcome \((j,+)\), output \(+1\) for measurement \(i\) with probability
\((1+t_{ij})/2\); on \((j,-)\), use probability \((1-t_{ij})/2\); on the residual
outcome use probability \(1/2\). These probabilities produce exactly \(A_i\).
Taking the product of these binary conditional probabilities gives a common
joint distribution on all outcomes, hence matrices satisfying (1).

For (9), the full polygon is a regular \(2N\)-gon of radius \(\eta\). Removing
one effect removes two opposite vertices. The remaining polygon has perimeter

\[
 4\eta\big[(N-2)\sin\alpha+\sin(2\alpha)\big]<4.     \tag{10}
\]

For \(N=2\), this polygon is a segment and the same formula holds. Thus every
\((N-1)\)-subfamily is compatible, and every smaller subfamily is compatible
by marginalization. This proves feasibility of the candidate point in the
relaxation.

There is also actual finite local moment feasibility. The strict inequality
in (10) leaves positive scalar slack in the parent construction. Distribute
this slack among the opposite generator pairs to make each nonzero parent
effect positive definite. Their top-left entries are then positive, and each
is the moment matrix of a finite measure on the real line with at most two
atoms. Thus the local examples need no zero-mass, positive-second-moment
limiting atoms.

The regular family and its compatibility interval are already the
\(N\)-Specker construction in Andrejic and Kunjwal, Corollary 8, for \(N\ge3\);
the two-effect case is elementary. The planar argument above is included to
make the moment application independently checkable.

## A witness that remains valid when the total moment matrix varies

Let

\[
 B_j=\sin\theta_j\,\sigma_x+\cos\theta_j\,\sigma_z.
\]

For every sign pattern \(\varepsilon\in\{-1,1\}^N\),

\[
 \lambda_{\max}\left(\sum_j\varepsilon_jB_j\right)
 =\left\|\sum_j\varepsilon_j(\sin\theta_j,\cos\theta_j)\right\|
 \le R.                                                        \tag{11}
\]

To prove (11), maximize the scalar product with a unit vector. The maximizing
signs choose the points lying in a semicircle from the regular \(2N\)-gon.
They are \(N\) consecutive vertices, allowing a limiting choice when a scalar
product is zero. Their vector sum has length

\[
 \left|\sum_{j=0}^{N-1}e^{ij\pi/N}\right|
 =\frac{\sin(\pi/2)}{\sin(\pi/(2N))}=R.
\]

Suppose arbitrary matrices \(M,M_j\) satisfy full compatibility. They need
not be unbiased or normalized to \(M=I\). For their parent matrices
\(G_\varepsilon\succeq0\), (11) gives

\[
 \sum_j\operatorname{tr}\big[B_j(2M_j-M)\big]
 =\sum_\varepsilon\operatorname{tr}
       \left[\left(\sum_j\varepsilon_jB_j\right)G_\varepsilon\right]
 \le R\operatorname{tr}M.                                     \tag{12}
\]

With \(M=\operatorname{diag}(1,v)\), expanding and dividing by two gives

\[
 \sum_j[2\sin\theta_j\,s_j+\cos\theta_j(z_j-r_j)]
 -\frac{1-v}{2}\sum_j\cos\theta_j
 \le\frac{R(1+v)}2.
\]

Equivalently,

\[
 L(v,s,r):=a v+\sum_j[-2\sin\theta_j\,s_j-w_jr_j]
 \ge C:=\sum_j\cos\theta_jz_j-
                    \frac{R+\sum_j\cos\theta_j}{2}.            \tag{13}
\]

At the candidate point (4), direct substitution gives

\[
 C-L(v^*,s^*,r^*)=N\eta-R>0.                                   \tag{14}
\]

The freedom to vary \(v\) is important: a separation inequality valid only
on the normalized slice \(M=I\) would not by itself prove an original
epigraph gap. Inequality (12) supplies the required homogeneous extension.

## Transfer to the original epigraph

The choice (6) ensures that the derivative of (2) with respect to \(s_j\),
at the candidate point, equals \(-2\sin\theta_j\). More explicitly,

\[
 F(v,s,r)-F(v^*,s^*,r^*)
 =L(v,s,r)-L(v^*,s^*,r^*)
  +\sum_j\frac{w_j}{z_j}(s_j-s_j^*)^2.                          \tag{15}
\]

Equations (13)--(15) give (8) for all exactly compatible moment tuples.
The same conclusion holds for every finite convex combination of original
feasible points because conditional square completion bounds its expected
cost below by (2).

The following affine inequality proves closed-hull validity directly. Put
\(p_i=\sin\theta_i\), \(P_0=\sum_i p_i\), and
\(\gamma=(R-W)/2\). Every original feasible point satisfies

\[
 t+P_0x_0+\sum_i\frac{2p_i}{b_i}y_i+\sum_i\frac{z_i}{w_i}
 \ge-\gamma.                                                   \tag{16}
\]

Indeed, let \(S\) be its active leaf support and define
\(h=\sum_i(2\,1_{\{i\in S\}}-1)(p_i,-w_i)\). Starting with the quadratic
cost and the left side of (16), moved to the nonnegative side, square
completion gives

\[
 x^TQx+P_0x_0+\sum_i\frac{2p_i}{b_i}y_i
       +\sum_i\frac{z_i}{w_i}+\gamma
 =
 \sum_{i\in S}\left(y_i+b_ix_0+\frac{p_i}{b_i}\right)^2
 +\frac{(R+h_z)x_0^2-2h_xx_0+R-h_z}{2}.                        \tag{17}
\]

The quadratic on the right is nonnegative because \(\|h\|\le R\) by (11).
Here \(w_i+p_i^2/w_i=1/w_i\) was used. Hence (16) is valid, including when the
center indicator is allowed to be zero, and its continuity makes it valid
on the closed convex hull. At the candidate epigraph point with
\(t=F(v^*,s^*,r^*)\), its left side plus \(\gamma\) is exactly
\(R-N\eta\). This proves the stated strict projected gap without any
moment-limit assumption.

## Literature comparison and novelty limits

- Andrejic and Kunjwal, *Joint measurability structures realizable with qubit
  measurements: incompatibility via marginal surgery*, Physical Review
  Research 2, 043147 (2020), [arXiv:2003.00785](https://arxiv.org/abs/2003.00785),
  Corollaries 7--8: the arbitrary-order real planar compatibility obstruction
  and the interval used in (3) are established results. They do not establish
  the original quadratic indicator epigraph gap (8).
- Zhang, Zhang, and Chitambar, *Cost of Simulating Entanglement in Steering
  Scenario*, [arXiv:2302.09060v3](https://arxiv.org/html/2302.09060v3), Section 4,
  Proposition 4, and Appendix A: parent-measurement compatible regions,
  symmetrization, planar zonotopes, and the perimeter-four calculation are
  already used there. The planar lemma above should therefore be treated as
  a direct geometric corollary of existing ideas, without an independent
  novelty claim.
- Grinko and Uola, *Compatibility of Binary Qubit Measurements*, Physical
  Review Letters 135, 200201 (2025),
  [arXiv:2407.07711](https://arxiv.org/abs/2407.07711): a general characterization
  of finite unbiased binary qubit families is available. Their counterexample
  to a proposed condition involving an angle-ordered polygonal walk does not
  contradict the lemma: that walk can include points interior to the actual
  symmetric convex hull.
- Carmeli, Heinosaari, and Toigo, *Quantum Incompatibility Witnesses*,
  Physical Review Letters 122, 130402 (2019),
  [arXiv:1812.02985v2](https://arxiv.org/html/1812.02985v2), Theorems 1--2:
  arbitrary linear incompatibility witnesses can already be represented by
  quantum state-discrimination advantages. Accordingly, witness separation
  and the general idea of converting incompatibility into an optimization
  advantage are prior work. Their decision problem and objective differ from
  (2); the specific issue here is realization by a strictly positive
  definite quadratic star with fixed original means and activity marginals.

The searches examined quantum compatibility, Specker scenarios, planar
compatibility conditions, convex hulls, zonotopes, and perimeter conditions.
No complete search for equivalent optimization-hierarchy results was
performed. An unsuccessful search would not prove originality. The potential
contribution here is the explicit, strictly convex star construction and its
projected gap, not the incompatibility pattern itself.

## Verification and limitations

One inline `python` command using NumPy, CVXPY, and Clarabel was run for
\(N=2,3,4,5\), taking \(\eta\) to be the midpoint of (3). The same check was then
preserved and run with the command

    python research-20260925/check_star_specker_gap.py

It enumerated all sign
patterns to check (11), checked positive Schur complements, evaluated (10),
and minimized (2) over the full joint PSD decomposition. The results were:

| \(N\) | Candidate objective | Numerical full-cone optimum | Proved gap lower bound |
|---:|---:|---:|---:|
| 2 | 1.04803097 | 1.36249579 | 0.29289322 |
| 3 | 2.14163259 | 2.24084981 | 0.09807621 |
| 4 | 3.26672659 | 3.31862834 | 0.05169564 |
| 5 | 4.45780569 | 4.49017392 | 0.03230942 |

An independent adversarial reviewer checked the planar lemma, the homogeneous
witness for arbitrary biased marginals and variable center variance, the exact
square remainder, and positive definiteness. A separate exhaustive sign check
for \(N=2,\ldots,10\) agreed with (11). This review is evidence, not a
formal verification or a novelty assessment.

These floating-point calculations check formulas and detect some possible
errors; they do not certify the theorem or the numerical full-cone optima.
The proof is given above. No project-wide tests or CI inspection were run.

The regular-family quadratic becomes poorly conditioned as \(N\) grows
because \((R-W)/2\) tends to zero. The subsequent
[short-arc construction](star-uniform-condition-subset-gaps.md) removes this
limitation: its quadratic matrices have a condition number bounded by a
constant independent of the number of leaves. Both constructions concern the
same subsetwise compatibility relaxation. Neither establishes a
dimension-independent relative gap. It also remains necessary to compare
the hierarchy and the transfer theorem carefully with existing optimization
formulations before making a publication claim.
