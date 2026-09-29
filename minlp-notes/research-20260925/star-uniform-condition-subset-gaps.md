# Every proper leaf subset can miss a quadratic-star hull under uniform conditioning

Date: 2026-09-25.

Status: explicit proofs, targeted numerical and exact rational checks, and independent adversarial review of the short-arc and rational constructions. The planar joint-measurement geometry is established prior work. The transfer to uniformly conditioned indicator-quadratic stars is developed here; its publication novelty has not been established.

## Main result and scope

For every integer \(N\ge2\), there is a positive definite quadratic matrix \(Q_N\) on a star with \(N\) leaves such that

\[
 \frac1{24}I\prec Q_N\prec3I,
 \qquad\kappa_2(Q_N)<72,
                                                               \tag{1}
\]

but a natural relaxation of its binary-indicator epigraph has a strict gap even when it imposes exact scalar second-moment compatibility on **every proper subset of leaves**. The candidate moments for each proper subset have an actual finite scalar-law realization; the gap does not rely on zero-mass limiting atoms.

The relaxation shares the center moment matrix and every single-leaf moment matrix between subsets. It does **not** identify higher-order pattern moments on intersections of different subsets. Thus the theorem rules out exactness at any fixed order of this subsetwise compatibility construction. It does not rule out stronger hierarchies that enforce those additional consistency equations, arbitrary compact conic formulations, or polynomial-time optimization over stars.

An exact rational-data variant below has polynomial encoding length and spectral bounds `1/39` and `12`. The lower bound on the strict gap is explicit but shrinks with \(N\). No dimension-independent additive or relative gap is claimed. The star has treewidth one and diameter two, but its center degree grows with \(N\).

## The model and the specified relaxation

The original epigraph is

\[
 E_Q=\{(x,z,t):t\ge x^TQx,\quad x_i(1-z_i)=0,\quad
                        z_i\in\{0,1\}\}.
\]

The center indicator is fixed to one. Its prescribed mean is zero. For a convex combination of feasible points, write the center as \(X\), the leaf variables as \(Y_i\), and the leaf indicators as \(Z_i\). Fix their means \(\mathbb EY_i=y_i\), \(\mathbb EZ_i=z_i\in(0,1)\), and introduce

\[
 M=\begin{pmatrix}1&0\\0&v\end{pmatrix},\qquad
 M_i=\begin{pmatrix}z_i&s_i\\s_i&r_i\end{pmatrix},
 \quad
 v=\mathbb EX^2,\ s_i=\mathbb EXZ_i,\ r_i=\mathbb EX^2Z_i.
\]

A subset \(J\) is compatible if there are real symmetric PSD matrices \(G^J_S\), \(S\subseteq J\), with

\[
 \sum_{S\subseteq J}G^J_S=M,\qquad
 \sum_{S:\,i\in S}G^J_S=M_i\quad(i\in J).           \tag{2}
\]

The subsetwise relaxation imposes (2) separately for every proper \(J\), with the same \(M,M_i\), and minimizes

\[
 F(v,s,r)=av+\sum_i\left[
              \frac{(y_i+b_i s_i)^2}{z_i}-b_i^2r_i\right].     \tag{3}
\]

Here the star matrix has center diagonal \(a\), leaf diagonal entries one, and center–leaf entries \(b_i\). Conditional square completion gives (3) as the minimum leaf cost for any fixed common center/indicator law. Consequently every actual convex combination has cost at least (3) at fully compatible moments. The derivation and the full joint cone are given in [the moment-gluing note](tree-indicator-moment-gluing.md).

## A short circular arc and its perimeter witness

Set

\[
 \delta=\frac\pi6,\qquad h=\frac{\delta}{N-1},\qquad
 t_i=-\frac\delta2+ih,\qquad
 p_i=(\cos t_i,\sin t_i),\quad i=0,\ldots,N-1.
\]

Let

\[
 P=\operatorname{conv}\{\pm p_0,\ldots,\pm p_{N-1}\},
 \qquad P_i=\operatorname{conv}\{\pm p_j:j\ne i\}.
\]

Write \(p=\operatorname{perim}(P)\) and
\(p_-=\max_i\operatorname{perim}(P_i)\). For a segment, perimeter means twice its length. Every point listed is a strict vertex of the full polygon, so removing any opposite pair strictly decreases perimeter. Also every remaining set contains a unit segment. Therefore

\[
 4\le p_-<p,
 \qquad
 p=4\left[(N-1)\sin\frac h2+\cos\frac\delta2\right].        \tag{4}
\]

Choose the explicit value

\[
 \eta=\frac12\left(\frac4p+\frac4{p_-}\right).
                                                               \tag{5}
\]

Then \(0<\eta<1\), \(\eta p>4\), and \(\eta p_-<4\).

Let \(u_i\) be the unit edge tangent from \(p_i\) to \(p_{i+1}\) for \(i<N-1\). Let \(u_{N-1}\) be the unit tangent from \(p_{N-1}\) to \(-p_0\), and put \(u_{-1}=-u_{N-1}\). Define

\[
 g_i=u_{i-1}-u_i.
\]

Their angles are strictly increasing. The endpoint angles are

\[
 -\frac\pi4-\frac\delta4+\frac h4,
 \qquad
 \frac\pi4+\frac\delta4-\frac h4,
\]

and every internal \(g_i\) equals \(2\sin(h/2)p_i\). In particular, all gradient angles lie strictly between \(-7\pi/24\) and \(7\pi/24\). Direct telescoping gives

\[
 \sum_i g_i=(2,0),\qquad
 \sum_i g_i\cdot p_i=\frac p2.                    \tag{6}
\]

The first identity uses \(u_{N-1}=(-1,0)\). The second sums the lengths of the half-polygon's edges.

For every sign pattern,

\[
 \left\|\sum_i\varepsilon_i g_i\right\|\le2,
 \qquad\varepsilon\in\{-1,1\}^N.                 \tag{7}
\]

To see this, form the zonotope \(Z=\sum_i[-g_i,g_i]\). For generators whose directions are strictly ordered in an interval shorter than \(\pi\), its boundary vertices are obtained by starting at \(\sum_i g_i\), flipping the generators in angular order, and using the opposite half of the path. A prefix flip gives

\[
 \sum_i g_i-2\sum_{i=0}^j g_i=2u_j.
\]

Every such vertex, including the initial and final vertices, has norm two. Hence the whole zonotope lies in the radius-two Euclidean disk. All signed sums belong to it, proving (7).

## Rotation and the uniformly conditioned star

Let \(T\) be rotation by \(-\pi/3\), and write

\[
 q_i=Tp_i,\qquad Tg_i=(c_i,-w_i).
\]

After rotation the gradient angles lie in \((-5\pi/8,-\pi/24)\), inside the open lower half-plane. Thus every \(w_i>0\). Equation (6) gives

\[
 \sum_i(c_i,-w_i)=(1,-\sqrt3),\qquad
 W:=\sum_iw_i=\sqrt3.
\]

Define

\[
 a=\frac{2+\sqrt3}{2},\qquad b_i=\sqrt{w_i},\qquad
 Q_N=\begin{pmatrix}a&b^T\\b&I_N\end{pmatrix}.      \tag{8}
\]

The Schur complement is

\[
 \gamma=a-\|b\|^2=\frac{2-\sqrt3}{2}>0.
\]

There are \(N-1\) eigenvalues equal to one. The other two are the eigenvalues of

\[
 \begin{pmatrix}a&\sqrt{\sqrt3}\\\sqrt{\sqrt3}&1\end{pmatrix},
\]

whose trace is \(a+1<3\) and determinant is \(\gamma\). Hence
\(\lambda_{\max}<3\) and

\[
 \lambda_{\min}=\frac\gamma{\lambda_{\max}}
 >\frac{2-\sqrt3}{6}>\frac1{24}.
\]

The last inequality is equivalent to \(\sqrt3<7/4\). This proves (1) uniformly in \(N\).

## Candidate moments and actual local laws

Use the real matrices

\[
 \sigma_x=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
 \sigma_z=\begin{pmatrix}1&0\\0&-1\end{pmatrix}.
\]

Define

\[
 M^*=I_2,\qquad M_i^*=\frac12[I_2+\eta(q_{i,x}\sigma_x+q_{i,z}\sigma_z)].
\]

Equivalently,

\[
 v^*=1,\quad z_i=\frac{1+\eta q_{i,z}}2,\quad
 s_i^*=\frac{\eta q_{i,x}}2,\quad
 r_i^*=\frac{1-\eta q_{i,z}}2.                      \tag{9}
\]

These have \(0<z_i<1\). The planar compatibility criterion says that unbiased real-qubit effects with vectors \(a_i\in\mathbb R^2\) have a common PSD parent precisely when
\(\operatorname{perim}(\operatorname{conv}\{\pm a_i\})\le4\).
A self-contained proof using planar zonotopes appears in [the regular-family note](star-hierarchy-specker-gap.md#why-every-proper-subfamily-is-compatible). It applies to arbitrary planar vectors, not only equal angular spacing.

For every proper subfamily of (9), its vector polygon has perimeter at most \(\eta p_-<4\). Thus every proper subfamily satisfies (2), while the full family is incompatible since its perimeter is \(\eta p>4\).

The strict inequality ensures actual finite scalar realizations. For a proper \(J\), choose \(\eta'>\eta\) sufficiently close that its effects remain compatible, and let \(G'_S\) be a PSD parent for those effects. Then

\[
 G_S=\frac\eta{\eta'}G'_S+
       \left(1-\frac\eta{\eta'}\right)2^{-|J|}I_2
                                                               \tag{10}
\]

is a parent for the effects at \(\eta\), and every \(G_S\) is positive definite. Each is a scalar moment matrix of a finite nonnegative measure with at most two atoms. Combining the pattern measures gives an actual finite law of \(X\) and the indicators in \(J\). Different subsets are allowed to use different such laws, as the specified relaxation requires.

## The strict gap in the original epigraph

Set the prescribed leaf means to

\[
 y_i=-b_i s_i^*-\frac{z_i c_i}{b_i}.                \tag{11}
\]

**Theorem.** For the matrix (8), means (9), (11), and center mean zero with center indicator one, the subsetwise relaxation imposing every proper subset has value at most \(F(v^*,s^*,r^*)\). The lower boundary of the true closed convex hull is at least

\[
 F(v^*,s^*,r^*)+\Delta_N,
 \qquad
 \Delta_N=\frac{\eta p}{2}-2>0.                    \tag{12}
\]

The assertion is about the original \((x,z,t)\) epigraph coordinates, not only the auxiliary moment cone.

To prove it, put \(B_i=c_i\sigma_x-w_i\sigma_z\). By rotation invariance, (7) gives
\(\lambda_{\max}(\sum_i\varepsilon_iB_i)\le2\). Every full PSD parent therefore satisfies

\[
 \sum_i\operatorname{tr}[B_i(2M_i-M)]\le2\operatorname{tr}M.
                                                               \tag{13}
\]

Indeed, expand through the joint pattern matrices; each summand is bounded by twice that pattern matrix's trace. For \(M=\operatorname{diag}(1,v)\), (13) rearranges to

\[
 L(v,s,r):=av-2\sum_i c_i s_i-\sum_iw_i r_i
 \ge C:=-\sum_iw_i z_i-\frac{2-W}{2}.              \tag{14}
\]

At the candidate, (6) implies

\[
 C-L(v^*,s^*,r^*)
 =\eta\sum_i (Tg_i)\cdot q_i-2
 =\frac{\eta p}{2}-2=\Delta_N.
\]

The prescribed means (11) give the exact square identity

\[
 F(v,s,r)-F(v^*,s^*,r^*)
 =L(v,s,r)-L(v^*,s^*,r^*)
   +\sum_i\frac{w_i}{z_i}(s_i-s_i^*)^2.            \tag{15}
\]

Equations (14)--(15) prove the lower bound in (12) for every fully compatible tuple. Equation (10) proves candidate feasibility for the subsetwise relaxation. Conditional square completion then transfers the full-compatible lower bound to every actual convex combination in the original epigraph.

### An explicit inequality in the original variables

There is a more direct certificate that also settles closure. For any original feasible point, denote its center variable by \(X\), leaf variables by \(Y_i\), and leaf indicators by \(Z_i\). The affine inequality

\[
 t+X+\sum_i\frac{2c_i}{b_i}Y_i
       +\sum_i\left(w_i+\frac{c_i^2}{w_i}\right)Z_i
 \ge-\gamma                                             \tag{16}
\]

is valid globally, even if the center indicator is allowed to vary. At the candidate epigraph point \((t,X,Y,Z)=(F(v^*,s^*,r^*),0,y,z)\), its violation is exactly \(\Delta_N\).

To check validity, let \(S=\{i:Z_i=1\}\), and put

\[
 (h_x,h_z)=\sum_i(2Z_i-1)(c_i,-w_i).
\]

Equation (7) gives \(h_x^2+h_z^2\le4\). Subtracting
\(\sum_{i\in S}(Y_i+b_iX+c_i/b_i)^2\) from the left side of (16) plus \(\gamma\), with \(t\) replaced by \(x^TQ_Nx\), leaves

\[
 \frac12\big[(2+h_z)X^2-2h_xX+(2-h_z)\big]\ge0.      \tag{17}
\]

The inequality follows because the corresponding two-by-two matrix has nonnegative diagonal entries and determinant \(4-h_x^2-h_z^2\ge0\). For inactive leaves, \(Y_i=0\), as required by the indicator constraints. Every square is nonnegative, and increasing \(t\) preserves the bound. This proves (16) for the original set, hence for its closed convex hull by affine continuity. Direct substitution of (9), (11) into (16) gives left side plus \(\gamma\) equal to \(2-\eta p/2=-\Delta_N\), proving (12) directly in the original variables.

The cut is a concrete separation certificate. Its derivation was independently proposed and algebraically checked by the short-arc reviewer; it avoids relying on a closure argument for a lifted moment projection.

## Rational data with a uniform spectral bound

The phenomenon does not require irrational optimization data. For every
`N >= 2`, the following variant gives rational `Q`, original means, and
indicator means, with

\[
 \frac1{39}I\prec Q\prec12I,\qquad\kappa_2(Q)<468.
                                                               \tag{18}
\]

The total encoding length of its nonzero data is `O(N^2 log N)`. Every
proper subset remains finitely realizable, whereas the original epigraph
point violates an explicit affine valid inequality. An
[independent rational-construction review](star-rational-uniform-review.md)
checks the details below.

Identify planar vectors with complex numbers, and set

\[
 \tau_i=\frac{2i-(N-1)}{64(N-1)},\qquad
 q_i=\frac{(1+\mathrm{i}\tau_i)^2}{1+\tau_i^2},\qquad
 p_i=q_i^2,\qquad i=0,\ldots,N-1.
                                                               \tag{19}
\]

Both coordinates of `q_i` and `p_i` are rational and their norms are one.
The angles of `p_i` are `4 arctan(tau_i)`, strictly increasing and symmetric
about zero. They lie between `-1/16` and `1/16` radians. The interior unit
edge tangent from `p_i` to `p_(i+1)` is `i q_i q_(i+1)`, hence rational.
The incoming and outgoing long-edge tangents are `1` and `-1`. Define
`g_i` by the same consecutive-tangent differences as above.

For any subfamily, its closing unit tangent is the complex product of its
first and last `q` values, with the appropriate sign. Therefore every
subfamily perimeter is rational: each edge length is the dot product of
its rational edge vector with its rational unit tangent. This includes
singletons, whose symmetric hull has perimeter four. Let `p` be the full
perimeter, `p_-` the largest one-deletion perimeter, and choose the rational
midpoint (5).

Rotate the vectors `p_i,g_i` by the rational matrix

\[
 T=\begin{pmatrix}5/13&12/13\\-12/13&5/13\end{pmatrix}.
\]

The pre-rotation gradient angles are strictly between `-pi/3` and `pi/3`.
The rotation angle is strictly between `-pi/2` and `-pi/3`, so all rotated
gradients have negative second coordinate. Write

\[
 Tp_i=(u_i,v_i),\qquad Tg_i=(c_i,-w_i).
\]

Then `w_i>0`, and the telescoping tangent identity gives

\[
 \sum_i c_i=10/13,\qquad W:=\sum_iw_i=24/13.
\]

The signed-sum norm bound remains two. Put `a=25/13`, so the desired Schur
complement is `a-W=1/13`.

Choose a positive rational power of two `b_i` with
`w_i <= b_i^2 < 4 w_i`, and set

\[
 d_i=b_i^2/w_i\in[1,4).
\]

Such a power can be found by exact comparison with powers of four. Use
center diagonal `a`, leaf diagonals `d_i`, and edge coefficients `b_i`.
Then `b_i^2/d_i=w_i`, so the Schur complement is exactly `1/13`.
After scaling each leaf coordinate by `sqrt(d_i)`, the normalized arrow
matrix has center diagonal `25/13`, unit leaf diagonals, and squared edge
norm `24/13`. Its two nontrivial eigenvalues have sum `38/13<3` and product
`1/13`; hence they lie strictly between `1/39` and `3`. Congruence by a
diagonal matrix with entries between one and two proves (18).

Define the rational candidate moments and original leaf means by

\[
 z_i=\frac{1+\eta v_i}{2},\quad
 s_i^*=\frac{\eta u_i}{2},\quad
 r_i^*=\frac{1-\eta v_i}{2},\quad
 y_i=-\frac{w_i}{b_i}s_i^*-\frac{z_i c_i}{b_i},\quad v^*=1.
                                                               \tag{20}
\]

The leaf-eliminated objective now has the general diagonal form

\[
 F(v,s,r)=av+\sum_i\left[
 \frac{d_i}{z_i}\left(y_i+\frac{b_i}{d_i}s_i\right)^2-w_i r_i
 \right].                                                       \tag{21}
\]

Its derivative with respect to `s_i` at the candidate is `-2c_i`, and its
quadratic remainder is `w_i(s_i-s_i^*)^2/z_i`. The perimeter and homogeneous
witness arguments therefore apply without change. The original epigraph
hull exceeds the feasible subsetwise relaxation value by at least

\[
 \Delta_N=\eta p/2-2=\frac{p-p_-}{p_-}>0.
                                                               \tag{22}
\]

A fully rational affine certificate, valid for every original feasible
point including either center-indicator value, is

\[
 t+\frac{10}{13}X+
 \sum_i\frac{2d_i c_i}{b_i}Y_i+
 \sum_i\left(w_i+\frac{c_i^2}{w_i}\right)Z_i
 \ge-\frac1{13}.                                               \tag{23}
\]

Indeed, subtracting the active-leaf squares
`d_i(Y_i+(b_i/d_i)X+c_i/b_i)^2` from its left side plus `1/13` leaves
exactly the PSD scalar residual (17). At (20) and `t=F(v*,s*,r*)`,
inequality (23) is violated by `Delta_N`. Thus the gap is certified directly
in the original variables.

The strict perimeter margin gives actual finite local laws by the same
noise-mixture argument used earlier. No rationality of those atom locations
is needed; the optimization data and separating inequality are rational.

For the encoding bound, each local rational coordinate in (19), each
chord tangent, and each `g_i,w_i` has `O(log N)` bits. A perimeter sums at
most `2N` such rational edge lengths, giving `O(N log N)` bits by a product
denominator bound. The midpoint `eta` has the same order of bit length.
Since every positive `w_i` has `O(log N)` bits, the dyadic exponent used for
`b_i` has magnitude `O(log N)`; `b_i,d_i` have `O(log N)` bits. Formula (20)
gives `O(N log N)` bits per mean. There are `O(N)` nonzero coefficients and
means, establishing the stated total bound. All operations are exact
rational arithmetic and comparisons of polynomial bit length.

The displayed margin is at least inverse polynomial. Consecutive short-arc
angle gaps satisfy

\[
 4\big(\arctan\tau_{i+1}-\arctan\tau_i\big)
 \ge\frac1{9(N-1)}.
\]

At a removed vertex, let `A,B` be the two adjacent central-angle gaps.
Both are at least this bound, and `A+B<=pi`. Deleting its opposite pair
reduces perimeter by

\[
 16\sin(A/4)\sin(B/4)\sin((A+B)/4)
 \ge\frac{A B(A+B)}{32}
 \ge\frac1{11664(N-1)^3}.
\]

Here `sin u >= u/2` on `[0,pi/4]` suffices. The full perimeter is at most
`4+2(1/8)=17/4<5`, because chord lengths do not exceed arc lengths.
Consequently

\[
 \Delta_N\ge\frac1{58320(N-1)^3}.                               \tag{24}
\]

This is a lower bound on the certified gap. It is not an upper bound on the
actual hull gap or a claim that the displayed relaxation point is optimal.

The targeted command
`python research-20260925/verify_star_rational_uniform.py` checked `N=2,...,9`
with exact `Fraction` arithmetic. It passed 1,020 exhaustive sign-pattern
PSD checks, rational perimeter and threshold identities, the dyadic scaling
conditions, and the rational witness gaps. These finite checks support the
all-dimensional proof; they do not replace it or establish novelty.

## What the result adds and what it leaves open

The obstruction combines a one-dimensional continuous separator, a positive definite tree quadratic, and fixed spectral bounds. Sparsity and uniform conditioning therefore do not suffice to make this subsetwise moment construction ideal at any fixed leaf order. Any formulation based on these local descriptions needs extra global compatibility information, a stronger notion of consistency, or an approximation argument.

This is not a complexity obstruction for star optimization. It also does not contradict exact path formulations, fixed-leaf tree formulations, or bounds on approximation error. The certified gap shrinks as the number of leaves grows, and the center's degree is unbounded. No finite convergence lower bound is proved for hierarchies with overlap consistency, and no lower bound is proved for unrestricted conic extension complexity.

[The general transfer theorem](tree-indicator-moment-gluing.md#transferring-any-local-moment-incompatibility-to-a-star-epigraph) explains why incompatibility can be exposed by a positive definite star objective. The present short-arc witness adds explicit matrices with dimension-independent conditioning; this is stronger than the initial [regular Specker family](star-hierarchy-specker-gap.md).

## Literature examined and novelty limits

The following prior results are essential comparisons, not evidence that a failed search establishes novelty.

- Andrejic and Kunjwal, *Joint measurability structures realizable with qubit measurements: Incompatibility via marginal surgery*, Physical Review Research 2, 043147 (2020), [arXiv:2003.00785](https://arxiv.org/abs/2003.00785), Corollary 8. They establish an arbitrary-order qubit incompatibility construction used in the initial regular family. Arbitrary-order incompatibility itself is established prior work.
- Bluhm and Nechita, *Joint measurability of quantum effects and the matrix diamond*, Journal of Mathematical Physics 59, 112202 (2018), [arXiv:1807.01508](https://arxiv.org/abs/1807.01508). The equivalence between binary joint measurability and a common PSD parent is established theory.
- Carmeli, Heinosaari, and Toigo, *Quantum incompatibility witnesses*, Physical Review Letters 122, 130402 (2019), [arXiv:1812.02985](https://arxiv.org/abs/1812.02985), Theorems 1–2. Their witness-to-state-discrimination connection is a stronger prior comparator than treating incompatibility as a new generic source of optimization gaps. The claim investigated here is restricted to convex quadratic indicator epigraphs on uniformly conditioned stars.
- Choi, Fattahi, Han, Gómez, and Lozano, *Convexification of mixed-integer quadratic optimization via decision diagrams*, [arXiv:2608.22815](https://arxiv.org/abs/2608.22815), Section 7.2. Their exact tree SOCP has size \(O(n^{k+1})\) with \(k\) rooted leaves. The polynomial bound treats \(k\) as fixed. The present result concerns a different local moment construction and does not challenge their ideal formulation.

The scalar moment interpretation, the square-completion transfer, and the uniform-conditioning construction require comparison against the strongest indicator-quadratic convexification literature before any publication novelty claim. This note records a correct candidate contribution with qualified priority.

## Verification record

The proof was developed through independent algebraic derivations by the authoring and parent research agents. The [independent short-arc review](star-short-arc-uniform-review.md) checks the geometry, signed-sum witness, conditioning, finite local realizations, and original-variable projection. The [rational-construction review](star-rational-uniform-review.md) separately checks the rational refinement and encoding argument.

A targeted inline Python/NumPy command checked \(N=2,\ldots,9\). It enumerated every sign pattern to verify the norm bound numerically, checked all one-leaf deletion perimeters and strict threshold inequalities, and computed the star eigenvalues. All checks passed. The two nontrivial eigenvalues were approximately \(0.047534154\) and \(2.818491250\), independent of \(N\); all other eigenvalues were one. The certified gaps were positive, including approximately \(0.00182351\) for \(N=3\) and \(0.0000285396\) for \(N=9\). These floating-point checks challenge the formulas but do not prove them, certify novelty, or replace the displayed exact arguments.

The supporting agent also independently checked an alternative short arc of width \(\pi/8\), including numerical full-moment-cone optimizations for \(N=2,3,4\); those tests support the same construction but are not checks of the exact \(\delta=\pi/6\) instances in this note. No project-wide verification or CI inspection was performed.
