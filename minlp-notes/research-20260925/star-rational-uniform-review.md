# Independent review: rational uniformly conditioned star examples

Date: 2026-09-25.

Status: the rational refinement and polynomial encoding claim pass this
review. This is a mathematical and arithmetic review, not a novelty review
or a formal verification. The main construction is documented in
[star-uniform-condition-subset-gaps.md](star-uniform-condition-subset-gaps.md).

## Rational polygon construction

Fix an integer \(N\ge2\), and use increasing indices \(i=1,\ldots,N\). Set

\[
t_i=\frac{2i-N-1}{64(N-1)},\qquad
q_i=\frac{1-t_i^2+2\mathrm i t_i}{1+t_i^2},\qquad p_i=q_i^2.
\]

Identify complex numbers with real planar vectors. Every \(q_i\) and
\(p_i\) is a rational unit vector. Writing
\(\theta_i=4\arctan t_i\), we have
\(-1/16<\theta_1<\cdots<\theta_N<1/16\). The symmetric polygon has vertices
\(p_1,\ldots,p_N,-p_1,\ldots,-p_N\) in this cyclic order.

The symmetry \(q_1q_N=1\) is essential for the following endpoint directions:

\[
e_0=1,\qquad e_i=\mathrm i q_iq_{i+1}\ (1\le i<N),\qquad e_N=-1,
\qquad g_i=e_{i-1}-e_i.
\]

These are rational vectors, and the \(e_i\) are the unit directions of
successive polygon edges along one half of the boundary. Summation by parts
gives

\[
\sum_i g_i=2,
\qquad
\sum_i g_i\cdot p_i=P/2,
\]

where \(P\) is the perimeter. The first identity is telescoping; the second
is the sum of the chord lengths along half the boundary.

Every vertex is strictly exposed, so deleting a pair \(\pm p_i\) strictly
reduces perimeter. Use the convention that the perimeter of a segment is
twice its length. This gives perimeter four after deletion when \(N=2\).

Perimeters of every subfamily are rational. For \(i<j\), the two relevant
length identities are

\[
\|p_j-p_i\|=2\det(q_i,q_j),\qquad
\|p_i+p_j\|=2q_i\cdot q_j.
\]

Both right sides are positive on the chosen arc. The corresponding unit
directions are \(\mathrm i q_iq_j\) and \(q_iq_j\). For any nonempty
ordered subfamily \(J=\{j_1<\cdots<j_m\}\),

\[
P_J=2\left[2q_{j_1}\cdot q_{j_m}
             +\sum_{r=1}^{m-1}2\det(q_{j_r},q_{j_{r+1}})\right].
\]

This also gives \(P_J=4\) when \(m=1\). A deleted endpoint changes the
closing direction to \(q_{j_1}q_{j_m}\); it is generally incorrect to keep
that direction equal to one for the deleted polygon.

Let \(P_-\) be the largest of the \(N\) single-deletion perimeters and set

\[
\eta=\tfrac12(4/P+4/P_-).
\]

Then \(4\le P_-<P\), so \(4/P<\eta<4/P_-\le1\). All proper subfamilies
have perimeter strictly below four after scaling by \(\eta\), and the full
family has perimeter strictly above four. The quantity \(\eta\) is rational.

## Rotation, positive weights, and uniform conditioning

Apply the rational rotation

\[
R=\frac1{13}\begin{pmatrix}5&12\\-12&5\end{pmatrix}
\]

to all \(p_i,g_i\), and keep the same symbols for the rotated vectors.
Define \(w_i=-g_{i,y}\). Each \(w_i\) is positive. Indeed, before rotation,
the interior \(g_i\) have arguments between \(-1/16\) and \(1/16\), while
the two endpoint arguments lie within \(1/32\) of \(-\pi/4\) and
\(\pi/4\). All lie strictly between \(-\pi/3\) and \(\pi/3\). The rotation
angle is \(-\arctan(12/5)\), and \(\pi/3<\arctan(12/5)<\pi/2\); consequently
all rotated vectors lie strictly in the lower half-plane. Also,

\[
\sum_iw_i=24/13.
\]

Choose a dyadic rational \(b_i>0\) with
\(w_i\le b_i^2<4w_i\), and set \(d_i=b_i^2/w_i\). The star matrix has
center diagonal \(a=25/13\), leaf diagonals \(d_i\in[1,4)\), and
center-leaf entries \(b_i\). Its Schur complement is

\[
a-\sum_i b_i^2/d_i=1/13.
\]

For a uniform spectral bound, write
\(Q=SAS\), with \(S=\operatorname{diag}(1,\sqrt{d_1},\ldots,\sqrt{d_N})\).
The matrix \(A\) has leaf diagonals one and edges \(\sqrt{w_i}\). Its
nontrivial two-dimensional block has trace \(38/13\) and determinant
\(1/13\), so

\[
\lambda_{\max}(A)<38/13<3,
\qquad
\lambda_{\min}(A)>1/38>1/39.
\]

The other eigenvalues equal one. Since \(I\preceq S^2\prec4I\),

\[
\tfrac1{39}I\prec Q\prec12I,
\qquad \kappa_2(Q)<468.
\]

Square roots appear only in this spectral proof; they are absent from the
input data \(a,b_i,d_i\).

## Rational moment point and objective transfer

Set

\[
M=I,\qquad
M_i=\tfrac12[I+\eta(p_{i,x}\sigma_x+p_{i,y}\sigma_z)]
   =\begin{pmatrix}z_i&s_i^*\\s_i^*&r_i^*\end{pmatrix}.
\]

All entries are rational, and \(0<z_i<1\). The correct leaf-eliminated
objective when the leaf diagonal is \(d_i\), rather than one, is

\[
F(v,s,r)=a v+\sum_i\left[
  \frac{d_i}{z_i}\left(y_i+\frac{b_i}{d_i}s_i\right)^2-w_ir_i
\right].
\]

Choose the rational original means

\[
y_i=-\frac{w_i}{b_i}s_i^*-\frac{z_i g_{i,x}}{b_i}.
\]

Then the exact tangent identity is

\[
F(v,s,r)-F(1,s^*,r^*)
=a(v-1)+\sum_i[-2g_{i,x}(s_i-s_i^*)-w_i(r_i-r_i^*)]
 +\sum_i\frac{w_i}{z_i}(s_i-s_i^*)^2.
\]

Thus varying \(d_i\) does not change the required linear witness or its
nonnegative square remainder.

For completeness, the signed-sum bound used by that witness is
\(\max_{\varepsilon_i\in\{-1,1\}}\|\sum_i\varepsilon_i g_i\|=2\).
Before rotation, the zonotope generated by the \(g_i\) has vertices
\(\pm2e_j\); all lie on the circle of radius two. This proves the bound
for all sign patterns, and the all-positive choice attains it. Rotation
preserves the bound. It gives the homogeneous inequality for arbitrary
compatible \(M,M_i\), including variable \(v\), rather than only the
normalized slice \(M=I\). Its violation at the candidate, in the objective
normalization above, is the rational positive number

\[
\eta P/2-2=(P-P_-)/P_->0.
\]

This review verifies the arithmetic and objective transfer. The parent note's
moment realization and closed-hull limiting argument must still be included
to make an assertion about the original closed epigraph, rather than just
incompatible matrices.

## An inverse-polynomial gap certificate

The gap above is not merely positive. It satisfies the explicit bound

\[
\frac{P-P_-}{P_-}>\frac1{58320(N-1)^3}.
\]

Indeed, consecutive short-arc angle gaps satisfy

\[
\theta_{i+1}-\theta_i
\ge \frac{512}{4097(N-1)}>\frac1{9(N-1)}=:\delta,
\]

by the derivative of \(4\arctan t\) on \([-1/64,1/64]\). At any vertex,
let \(a,b\) be the adjacent angular gaps in the symmetric polygon. Both
are at least \(\delta\), and \(a+b\le\pi\). For endpoints of the short arc,
one gap is \(\pi-(\theta_N-\theta_1)\); the other is at most
\(\theta_N-\theta_1\), proving the last assertion there. For interior
vertices it follows from the short arc itself.

Deleting that vertex and its antipode loses perimeter

\[
\begin{aligned}
\Delta P
 &=4[\sin(a/2)+\sin(b/2)-\sin((a+b)/2)]\\
 &=16\sin(a/4)\sin(b/4)\sin((a+b)/4)\\
 &\ge\delta^3/16.
\end{aligned}
\]

The last step uses \(\sin u\ge u/2\) on \([0,\pi/2]\). The formula also
applies when \(N=2\): the two surviving edges are the two copies of the
limiting segment. Finally,

\[
P\le2[2+(\theta_N-\theta_1)]<17/4<5,
\]

since the short chords have total length at most their total angle, and
the closing chord has length at most two. Applying these bounds to the
smallest single-deletion loss proves the displayed gap certificate. The
parent researcher independently rechecked this trigonometric identity and
the constant \(58320\). This estimate is not claimed to be sharp and does
not establish a gap bounded below by a positive constant as \(N\) grows.

## Encoding length and exact construction

Let \(L=64(N-1)\), \(k_i=2i-N-1\), and \(D_i=L^2+k_i^2\). Then

\[
q_i=\frac{L^2-k_i^2+2\mathrm iLk_i}{D_i},\qquad
D_i\le4097(N-1)^2.
\]

Every component of \(q_i,p_i,e_i,g_i,w_i\) therefore has \(O(\log N)\)
bits. More explicitly, an interior \(w_i\) has a denominator dividing
\(13D_{i-1}D_iD_{i+1}\); endpoint formulas require only two such factors.
Writing \(D=4097(N-1)^2\), positivity gives the useful crude bounds

\[
\frac1{13D^3}\le w_i\le2.
\]

No analytic lower bound on the small edge lengths is needed for this
encoding argument. Starting with \(b_i=1\), halve it while
\(b_i^2\ge4w_i\), then double it while \(b_i^2<w_i\). Exact rational
comparisons terminate with the required inequalities after \(O(\log N)\)
steps. Both \(b_i\) and \(d_i\) have \(O(\log N)\) bits.

Each perimeter has a common denominator dividing
\(C=\prod_{i=1}^N D_i\). To see this, use the determinant and inner-product
length formulas above, whose terms with distinct indices have denominators
dividing \(D_iD_j\); singleton perimeters equal four. Since perimeters
are bounded by \(2\pi\), their numerators and denominators have
\(O(N\log N)\) bits. Exact comparisons identify \(P_-\) in polynomial
time. Both \(\eta\) and every final mean or moment entry have
\(O(N\log N)\) bits.

Consequently the \(O(N)\) nonzero star data and witness coordinates have
total encoding length \(O(N^2\log N)\). A polynomial number of additions,
multiplications, divisions, and rational comparisons constructs them, and
all intermediate operands have polynomial length. This establishes a
polynomial-time rational construction, not just existence of rational
approximations to a real example.

## Targeted verification and limitations

An independent inline `python` command using only `fractions.Fraction` and
`itertools.combinations` checked all 501 nonempty subfamilies for
\(N=2,\ldots,8\). It verified exactly that the claimed rational chord
lengths are positive and their squares equal the Euclidean squared lengths,
that singleton perimeters equal four, and that every one-vertex extension
strictly increases perimeter. All checks passed.

A separate reviewer checked the denominator argument and dyadic selection,
and ran exact instances for \(N=2,3,4,10,30,100,300\). That review found no
rationality or encoding issue. The primary construction also has its own
targeted checker, [verify_star_rational_uniform.py](verify_star_rational_uniform.py).
Finite computation checks formulas; the all-\(N\) claims depend on the
proofs above. No project-wide tests or CI inspection were run.

The rational refinement removes two possible qualifications: irrational
input coefficients and condition numbers diverging with dimension. It does
not establish a constant additive or relative relaxation gap, any
complexity lower bound for other formulations, or independent novelty of
the quantum compatibility construction. No literature search was undertaken
as part of this arithmetic review.
