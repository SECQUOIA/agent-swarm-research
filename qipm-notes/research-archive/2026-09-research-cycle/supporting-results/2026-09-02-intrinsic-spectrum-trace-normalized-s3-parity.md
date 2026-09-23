# Intrinsic-spectrum sparse SDP parity with a condition-one public Newton step

Date: 2026-09-02

## Main result

There is a linear-size family of trace-normalized product SDPs with the
following properties.

* The input consists of \(N\) signs on a path.  In isometric-svec form, every
  copy row has two nonzeros, the one normalization row has three nonzeros,
  and every column has at most two nonzeros.  One input sign changes only two
  coefficient values.
* Eliminating the path leaves the full qutrit density spectrahedron
  \(\{Z\succeq0:\operatorname{tr}Z=1\}\).  Its conic hull is
  \(\mathbb S_+^3\), so it has no finite second-order-cone lift.
* Parity changes the spectrum of the eliminated cost and changes the optimal
  value by exactly \(1/10\).  Estimating the optimal value to additive error
  \(1/25\), or relative error \(1/100\), therefore requires
  \(\Omega(N)\) raw coefficient queries.
* At the completely public feasible point \(X_i=I_3/3\), with product-barrier
  parameter \(\mu=1/P\), the complete equality-reduced Newton Hessian is a
  scalar identity.  The off-diagonal sparsity graph of the symmetric scalar
  KKT matrix is a forest and hence has treewidth one.  Equivalently, in the
  physical root coordinate the reduced Hessian is exactly \(9I\).  The complete
  unreduced KKT right-hand side is public.  A fixed
  observable has expectation \(2h/3\) on every normalized physical-block
  primal direction, where \(h\) is parity.  It has the same expectation on
  the normalized global primal-direction state.  The undamped Newton step
  remains positive definite; its decrement is \(1/\sqrt{150}\), and the
  universal next-decrement bound is below \(1/126\).  A public observable
  has magnitude greater than \(7/10\) on the normalized complete
  primal-plus-multiplier KKT state.  These state lower bounds also hold for
  calls to an exact, canonical normalization-three sparse KKT block encoding.
* The direction decoder remains parity-hard for every reduced Newton solve
  with relative residual at most \(1/10\).  A separate ambient theorem covers
  arbitrary PSD approximate optimizers with equality residual
  \(O(P^{-1/2})\); an explicit wrong-parity mixture shows this residual order
  is necessary under the stated objective and trace-normalized-state contract.
* Applying the tangent projector to the normalized public gradient has exact
  signal probability \(24/41\).  Synthesizing even a normalization-one
  projector block encoding to error \(1/32\) costs \(\Omega(P)\) raw queries
  including setup, although one supplied projector call reveals parity.

Thus the optimal-value lower bound is not a hidden-output-gauge artifact and
is not caused by poor reduced conditioning, a nonpublic Newton residual, or a
vanishing step.  The Newton state statement is a fixed-coordinate output lower
bound and retains the coordinate caveat stated in Section 6.  The optimal-value
statement is stronger than a central-state output lower bound: the two
optimization problems have different scalar optima.

> **Theorem (intrinsic value and condition-one Newton hardness).**  For every
> \(N\ge1\), the SDP (10) has \(P=33N\) constant-size PSD blocks, scalar row
> sparsity at most three, scalar column sparsity at most two, and strictly
> feasible primal and dual points.  Its optimal value is \(29/10\) when the
> input parity is positive and \(14/5\) when it is negative.  Hence
> additive-\(1/25\) or relative-\(1/100\) optimal-value estimation takes
> \(\Omega(P)\) raw coherent
> coefficient queries.  At the public start (19), the complete reduced
> primal log-barrier Hessian has condition number one, the unreduced Newton
> right-hand sides are public, its scalar symmetric KKT sparsity graph has
> treewidth one, and the full feasible primal direction is
> (23).  Preparing its normalized root or global amplitude state to trace
> distance \(1/100\) also takes \(\Omega(P)\) raw queries or calls to the
> canonical block encoding in Section 4.6.  The same two access lower bounds
> hold for the normalized complete primal-plus-multiplier KKT state.
> Synthesizing the tangent-projector oracle of Section 4.7 also takes
> \(\Omega(P)\) raw queries.  The feasible
> spectrahedron has no lift over any finite product of second-order cones.

## 1. Path construction and exact elimination

Let

\[
 K=16N,\qquad P=2K+N=33N,\qquad
 h=\prod_{j=1}^N\sigma_j,
 \qquad \sigma_j\in\{-1,+1\}.                \tag{1}
\]

There are \(P\) blocks \(X_0,\ldots,X_{P-1}\in\mathbb S_+^3\).  Consecutive
blocks satisfy

\[
 X_i=G_iX_{i-1}G_i^T.                         \tag{2}
\]

The first \(K-1\) edges are identity edges.  The next \(N\) edges, including
the edge into the first hidden block, have

\[
 G_i=D_{\sigma_j}:=\operatorname{Diag}(\sigma_j,1,1)
\]

in input order.  The final \(K\) edges are identity edges.  Hence the blocks
split into \(K\) pre-input blocks, \(N\) hidden-chain blocks, and \(K\)
post-input blocks.  The edge count is
\((K-1)+N+K=2K+N-1=P-1\).  Add the public normalization row

\[
                         \operatorname{tr}X_0=1. \tag{3}
\]

Write \(R_0=I_3\) and \(R_i=G_i\cdots G_1\).  Equations (2)--(3) are
equivalent to

\[
 X_i=R_iZR_i^T,\qquad Z\succeq0,\qquad
 \operatorname{tr}Z=1.                       \tag{4}
\]

The pre-input blocks have \(R_i=I\), the hidden blocks contain the prefix
signs, and every post-input block has \(R_i=D_h\).

Use Frobenius-isometric coordinates

\[
 \operatorname{svec}(X)=
 (X_{11},\sqrt2X_{12},\sqrt2X_{13},X_{22},
  \sqrt2X_{23},X_{33}).                       \tag{5}
\]

Then congruence by \(D_\sigma\) is the diagonal map

\[
 \operatorname{Diag}(1,\sigma,\sigma,1,1,1). \tag{6}
\]

Every scalar copy row therefore has two nonzeros of magnitude one.  The
trace row has three nonzeros.  A scalar column occurs in at most two rows:
an interior copy coordinate occurs in its two adjacent edge rows, while a
root diagonal coordinate occurs in the first edge row and (3).  Only the
\(12\) and \(13\) rows on signed edge \(j\) depend on \(\sigma_j\).  The
constraint matrix has full row rank \(6(P-1)+1\), leaving a five-dimensional
trace-zero tangent space.  Indeed, within each of the six svec coordinates, ordering
the copy rows along the path exposes a new block variable in every successive row, so
the \(6(P-1)\) copy rows are independent.  Their common kernel consists exactly of
the six-dimensional family (4) before normalization.  The trace row is nonzero on
that kernel (take \(Z=I_3\)), so it is independent of all copy rows.

## 2. A signed anisotropy triangle and intrinsic spectral parity

Let

\[
 H_{ab}=e_ae_b^T+e_be_a^T,\qquad
 u=\frac1{10},\qquad q=\frac KP=\frac{16}{33},\qquad
 \gamma=\frac uq=\frac{33}{160}.             \tag{7}
\]

Every local cost has the public baseline \(3I+uH_{23}\).  Add
\(\gamma H_{12}\) on each of the first \(K\) pre-input blocks and add
\(\gamma H_{13}\) on each of the final \(K\) post-input blocks.  Thus

\[
C_i=\begin{cases}
 3I+uH_{23}+\gamma H_{12},&0\le i<K,\\
 3I+uH_{23},&K\le i<K+N,\\
 3I+uH_{23}+\gamma H_{13},&K+N\le i<P.
 \end{cases}                                  \tag{8}
\]

All local costs are positive definite.  For a pre- or post-input block, the
anisotropic perturbation has eigenvalues
\(0,\pm\sqrt{u^2+\gamma^2}\), and

\[
 \sqrt{u^2+\gamma^2}<\frac14.                 \tag{9}
\]

The hidden-block costs have eigenvalues \(3-u,3,3+u\).  Hence every local
cost has spectrum in \((11/4,13/4)\).

Consider the averaged SDP

\[
 \begin{aligned}
 \text{minimize}\quad &\frac1P\sum_{i=0}^{P-1}\langle C_i,X_i\rangle,\\
 \text{subject to}\quad &(2),(3),\quad X_i\succeq0.
 \end{aligned}                                \tag{10}
\]

The baseline \(H_{23}\) is invariant under every \(R_i\).  The pre-input
\(H_{12}\) anchor is in the root frame, while the post-input
\(H_{13}\) anchor acquires the final sign \(h\).  Since \(q\gamma=u\),
pullback through (4) gives

\[
 \frac1P\sum_iR_i^TC_iR_i
 =3I+u(H_{12}+H_{23}+hH_{13})=:\overline C_h.  \tag{11}
\]

Thus (10) reduces exactly to

\[
 \min\{\langle\overline C_h,Z\rangle:
             Z\succeq0,\ \operatorname{tr}Z=1\}. \tag{12}
\]

Let

\[
 A_h=H_{12}+H_{23}+hH_{13}.                  \tag{13}
\]

For \(h=+1\), \(A_h\) is the adjacency matrix of the all-positive triangle
and has eigenvalues \(2,-1,-1\).  For \(h=-1\), its signed cycle product is
negative and its eigenvalues are \(1,1,-2\).  Consequently

\[
 \operatorname{spec}(\overline C_+)=\{16/5,29/10,29/10\},
 \qquad
 \operatorname{spec}(\overline C_-)=\{31/10,31/10,14/5\}.    \tag{14}
\]

No orthogonal congruence, even followed by a positive scalar rescaling, can
identify the two costs: orthogonal congruence preserves the spectrum, and
the common trace nine forces any scalar to equal one.  More strongly, the
scalar optimum of (12) is

\[
                         v_+=\frac{29}{10},\qquad
                         v_-=\frac{14}{5}.     \tag{15}
\]

Thus

\[
                         \boxed{|v_+-v_-|=\frac1{10}.}         \tag{16}
\]

Parity changes an invariant optimization output, not merely the coordinates
of a requested optimizer.  On the trace-one affine space, adding a multiple
of \(I\) only shifts every objective value, so one may also compare costs up
to \(C\mapsto \alpha Q^TCQ+\beta I\) with \(\alpha>0\).  Even under this
broader optimizer-preserving equivalence the two costs cannot be identified:
\(\overline C_+\) has a unique largest eigenvalue and a repeated smallest
eigenvalue, whereas \(\overline C_-\) has the opposite multiplicity pattern.

For the associated standalone unnormalized cone problems, parity also changes
the spectra of the cone central matrices and of the six-dimensional,
path-eliminated log-det Hessians.  For example, the determinant of the
symmetric-space operator
\(Y\mapsto\overline C_hY\overline C_h\) is
\((\det\overline C_h)^4\), and
\((16/5)(29/10)^2\ne(14/5)(31/10)^2\).

The primal is strictly feasible at \(X_i=I/3\).  The dual is strictly
feasible because every local objective coefficient \(C_i/P\) is positive
definite: zero equality multipliers and slacks \(C_i/P\) give a strict
certificate.  Consequently primal and dual optima are attained and have
equal value.

The optimal eigenspaces and strict complementarity can also be made explicit.
Put
\[
 r_+=\frac1{\sqrt3}(1,1,1)^T,\qquad
 r_-=\frac1{\sqrt3}(1,-1,1)^T.
\]
For positive parity, the minimum eigenspace is \(r_+^\perp\); for negative
parity, it is \(\operatorname{span}\{r_-\}\).  Thus reduced primal optima may
be chosen as
\[
 Z_+^*=\frac12(I-r_+r_+^T),\qquad
 Z_-^*=r_-r_-^T.
\tag{16a}
\]
The corresponding reduced dual slacks are
\[
 \overline S_+^*=\overline C_+-\frac{29}{10}I
                 =\frac3{10}r_+r_+^T,\qquad
 \overline S_-^*=\overline C_--\frac{14}{5}I
                 =\frac3{10}(I-r_-r_-^T).
\tag{16b}
\]
They satisfy \(Z_h^*\overline S_h^*=0\) and
\[
 \operatorname{rank}Z_h^*+\operatorname{rank}\overline S_h^*=3
\]
for both parities.  Hence the reduced problem has a strictly complementary
optimal pair, even though the positive-parity primal optimum is not unique.

This pair lifts to a strictly complementary optimum of the displayed product
SDP.  Set
\[
 X_i^*=R_iZ_h^*R_i^T,\qquad
 S_i^*=\frac1P R_i\overline S_h^*R_i^T.
\tag{16c}
\]
The tuple \((C_i/P-S_i^*)_i\) is orthogonal to every feasible tangent
\((R_iYR_i^T)_i\) with \(\operatorname{tr}Y=0\), because
\[
 \sum_i\langle C_i/P-S_i^*,R_iYR_i^T\rangle
 =\langle \overline C_h-\overline S_h^*,Y\rangle
 =v_h\operatorname{tr}Y=0.
\]
It therefore lies in the range of the equality adjoint, so suitable equality
multipliers exist.  Each block obeys \(X_i^*S_i^*=0\) and has complementary
ranks summing to three.

## 3. Linear raw-query lower bound for optimal value

Use coherent fixed-position row or column access to the nonzero values in
the scalar constraint matrix.  Its supports, right-hand sides, and all costs
are public.  A requested coefficient is either public or is one of the two
copies of one sign \(\sigma_j\), so either kind of sparse-access query is
simulated coherently with at most one standard query to input bit \(j\).

Suppose an algorithm estimates the optimum of (10) to additive error at most
\(1/25\), with success probability at least \(2/3\).  Since twice this error
is less than the gap in (16), comparison with the public threshold \(57/20\)
computes parity with the same success probability.  The same threshold works
under the multiplicative contract
\[
 |\widehat v-v_h|\le\frac1{100}v_h.             \tag{16d}
\]
indeed, \((99/100)(29/10)>57/20\), whereas
\((101/100)(14/5)<57/20\).  Thus either additive-\(1/25\) or
relative-\(1/100\) approximation computes parity.  Bounded-error quantum
parity needs \(\Omega(N)\) queries.  As \(P=33N\), this proves

\[
 \boxed{Q_{\rm add,1/25}=\Omega(N)=\Omega(P),\qquad
        Q_{\rm rel,1/100}=\Omega(N)=\Omega(P).} \tag{17}
\]

The upper bound is also \(O(N)\): read all signs, compute \(h\), and use
(15).  Thus the raw-query complexity is \(\Theta(P)\).

The approximation thresholds can be stated sharply for this two-value
family.  Under a worst-case additive-error contract, every
\(\epsilon<1/20\) leaves the two allowed output intervals disjoint and is
parity-hard, whereas for \(\epsilon\ge1/20\) the input-independent answer
\(57/20\) is valid for both parities and uses no query.  Under a relative
contract \(|\widehat v-v_h|\le r v_h\), the corresponding threshold is

\[
 r_*={v_+-v_-\over v_++v_-}={1\over57}.                 \tag{17a}
\]

For \(r<1/57\), the relative-error intervals are disjoint and thresholding
computes parity.  At \(r=1/57\) they first meet at the public value

\[
 v_+(1-r_*)=v_-(1+r_*)={812\over285},                   \tag{17b}
\]

so that value is a zero-query answer for every \(r\ge1/57\).  This sharp
phase transition is elementary and specific to the promise that the optimum
is one of the two known scalars in (15); it is not a general optimization
lower bound.

## 4. Condition-one Newton direction from a public point

Use the product log-det barrier

\[
 \Phi_\mu(X)=\frac1P\sum_i\langle C_i,X_i\rangle
              -\mu\sum_i\log\det X_i         \tag{18}
\]

and take the public feasible start and public barrier parameter

\[
                  X_i^0=I_3/3,\qquad \mu=1/P. \tag{19}
\]

At (19), in isometric-svec coordinates,

\[
 g_i=\frac1P(C_i-3I),\qquad
 \nabla^2\Phi_\mu(X^0)=\frac9P I.             \tag{20}
\]

Both the copy-constraint residual and the trace residual are zero, and the
stationarity right-hand side \(-g_i=(3I-C_i)/P\) is public.  The input signs
occur only in the sparse equality matrix.  Its norm is explicit and input
independent:
\[
 \|g\|_2^2
 =\frac{2Pu^2+4K\gamma^2}{P^2}
 =\frac{41}{400P}.                              \tag{20b}
\]

Writing \(\widetilde A_\sigma\) for all copy rows together with the trace
row, the primal barrier Newton equations can be written, under one multiplier
sign convention, as

\[
 \widetilde A_\sigma\Delta X=0,\qquad
 \frac9P\Delta X-\widetilde A_\sigma^*\Delta y=-g.           \tag{20a}
\]

Thus both vector right-hand sides in the unreduced KKT system are public;
only the sparse operator on the left contains input signs.

The off-diagonal sparsity graph of the symmetric scalar KKT matrix in (20a)
is a forest.  Ignore the diagonal entries of the scalar Hessian, which only
give graph loops.  For each of the six svec coordinates, the \(P\) primal
coordinate vertices and its \(P-1\) copy-multiplier vertices alternate to form
one subdivided path.  The trace multiplier is adjacent only to the root primal
vertices of the three diagonal-coordinate paths.  It joins those three
previously disjoint paths through one new vertex and therefore creates one
tree, while the three off-diagonal-coordinate paths remain separate trees.
Thus the graph has four connected components and treewidth one.  This is only
a sparsity statement: the long paths can still make the full saddle matrix
poorly conditioned.

For a trace-zero root tangent \(Y\), define the isometry

\[
 \mathcal W_\sigma(Y)=P^{-1/2}
       (R_0YR_0^T,\ldots,R_{P-1}YR_{P-1}^T).  \tag{21}
\]

The complete reduced Hessian in any Frobenius-orthonormal basis of the
five-dimensional trace-zero tangent is

\[
 \boxed{\mathcal W_\sigma^*\nabla^2\Phi_\mu(X^0)
                   \mathcal W_\sigma=\frac9P I_5.}            \tag{22}
\]

Thus its condition number is exactly one.  If the copies are first
eliminated and the physical root matrix \(Z\) is used as coordinate, the
same quadratic form is \(9I_5\); the factor \(P\) difference is only the
normalization between \(Y\) and the global orthonormal coordinate.

Since \(\overline C_h-3I=uA_h\) is already trace zero, projection of the
eliminated gradient onto the trace-zero tangent gives \(uA_h\).  The physical root
Newton direction is therefore

\[
                         \boxed{\Delta Z_h=-\frac u9A_h.}      \tag{23}
\]

The Newton decrement is also uniformly small:

\[
 \lambda^2=\langle uA_h,(9I)^{-1}uA_h\rangle
 =\frac{2u^2}{3}=\frac1{150},
 \qquad \lambda=\frac1{\sqrt{150}}<0.082.     \tag{24}
\]

Every physical direction is \(\Delta X_i=R_i\Delta Z_hR_i^T\).  The
undamped step is strongly feasible.  For \(h=+1\), its root eigenvalues are

\[
                         \frac{14}{45},\ \frac{31}{90},\ \frac{31}{90},
\]

and for \(h=-1\) they are

\[
                         \frac{29}{90},\ \frac{29}{90},\ \frac{16}{45}.
\tag{25}
\]

Hence \(Z^0+\Delta Z_h\succeq(14/45)I\).  Orthogonal congruence proves
\(X_i^0+\Delta X_i\succ0\) for every block.  Equation (23) is trace zero,
so the normalization row remains exact.

More intrinsically, the restriction of (18) to the feasible affine space is
a standard self-concordant function.  Since \(\lambda=1/\sqrt{150}<1\),
the Dikin-ellipsoid theorem guarantees the full Newton step remains in its
domain, and the universal next-decrement estimate is
\[
 \lambda(X^0+\Delta X)
 \le\left(\frac{\lambda(X^0)}{1-\lambda(X^0)}\right)^2
 =\frac1{(\sqrt{150}-1)^2}<\frac1{126}.          \tag{25a}
\]
This does not assert membership in a paper-specific primal--dual
neighborhood, but it is a representation-independent full-step guarantee.

### 4.1 Exact direction-state parity decoder

Let \(|12\rangle,|13\rangle,|23\rangle\) denote the three normalized
off-diagonal isometric-svec basis states.  Up to a global sign, the normalized
root direction is

\[
 |\delta z_h\rangle
 =\frac{|12\rangle+|23\rangle+h|13\rangle}{\sqrt3}.           \tag{26}
\]

The normalization is independent of the input:
\[
 \|\Delta Z_h\|_F^2=\frac{2u^2}{27},
 \qquad
 \sum_{i=0}^{P-1}\|\Delta X_i\|_F^2=\frac{2Pu^2}{27}.
\tag{26a}
\]
Thus neither target has a zero norm or an input-dependent normalization
factor.

The fixed Hermitian contraction

\[
 T=|12\rangle\langle13|+|13\rangle\langle12|                \tag{27}
\]

has

\[
                         \boxed{\langle\delta z_h|T|\delta z_h\rangle
                         =\frac{2h}{3}.}                      \tag{28}
\]

This identity persists on every physical block.  If
\(\tau_i\) is the prefix product at block \(i\), its normalized direction is,
up to a global sign,

\[
 |\delta x_i\rangle
 =\frac{\tau_i|12\rangle+|23\rangle+\tau_i h|13\rangle}{\sqrt3},           \tag{29}
\]

and its expectation of the same \(T\) is again \(2h/3\).  Every block also
has the same Frobenius norm.  Therefore the fixed public contraction
\[
                         T_{\rm glob}=\bigoplus_{i=0}^{P-1}T
\tag{29a}
\]
has expectation exactly \(2h/3\) on the normalized global primal-direction
state.  It is independent of every input sign and has operator norm one.

The two-outcome measurement uses \((I\pm T)/2\) for the root state and
\((I\pm T_{\rm glob})/2\) for the global state.  Either recovers parity with
success probability \(5/6\).  Trace-distance error \(1/100\) leaves success
at least \(5/6-1/100\).  The same coefficient-oracle reduction as in
Section 3 proves

\[
 \boxed{\Omega(N)=\Omega(P)}                                  \tag{30}
\]

raw queries for preparing either the normalized root or global primal
Newton-direction state.  Section 4.3 gives the corresponding normalized
complete primal-plus-multiplier KKT-state theorem.

Here trace distance means
\(D_{\rm tr}(\rho,\omega)=\tfrac12\|\rho-\omega\|_1\).  The probability of
any fixed POVM event changes by at most \(D_{\rm tr}\), so this statement
allows an arbitrary unconditional mixed output within the stated distance of
the target pure state.  A heralded or postselected contract must charge its
success probability and amplification cost.

### 4.2 Sharp reduced-residual decoder

The direction-state lower bound does not require an exact reduced solve.  Let
\(Y\ne0\) be trace zero and suppose

\[
 {\|9Y+uA_h\|_F\over\|uA_h\|_F}\le\eta.                \tag{30a}
\]

Since \(9\Delta Z_h+uA_h=0\) and \(\|A_h\|_F=\sqrt6\), this is exactly

\[
 \|Y-\Delta Z_h\|_F\le\eta\|\Delta Z_h\|_F.            \tag{30b}
\]

For \(0\le\eta<1\), let \(|y\rangle=\operatorname{svec}(Y)/\|Y\|_F\).
The projective angle \(\theta\) from the exact ray (26) then obeys
\(\sin\theta\le\eta\).  This follows by measuring the distance from the
unit exact vector to the line containing
\(Y/\|\Delta Z_h\|_F\), which is at most \(\eta\) by (30b).  Global sign is
therefore irrelevant.

For completeness, the sharp worst-case expectation of the fixed decoder
\(hT\) over this projective ball can be calculated exactly for
\(0\le\eta\le1/3\).  Put

\[
 |q_h\rangle={|12\rangle+h|13\rangle\over\sqrt2},qquad
 |r\rangle=|23\rangle.
\]

The exact state is
\(\sqrt{2/3}|q_h\rangle+|r\rangle/\sqrt3\).  In the orthonormal basis formed
by this vector,
\(|t_h\rangle=|q_h\rangle/\sqrt3-\sqrt{2/3}|r\rangle\), and the \(-1\)
eigenvector of \(hT\), direct minimization on the spherical cap gives

\[
 \boxed{
 h\langle y|T|y\rangle\ge
 m(\eta):={2\over3}-{\eta^2\over3}
 -{2\sqrt2\over3}\eta\sqrt{1-\eta^2},
 \qquad 0\le\eta\le{1\over3}.}                         \tag{30c}
\]

Here is the short minimization.  Write a unit vector at sine-angle
\(s\le\eta\) as
\(\sqrt{1-s^2}|\delta z_h\rangle+s(x|t_h\rangle+
\sqrt{1-x^2}|n_h\rangle)\), where \(|n_h\rangle\) is the \(-1\)
eigenvector; components in the remaining zero eigenspace cannot improve the
minimum.  Its expectation is

\[
 {2\over3}(1-s^2)-s^2
 +{2\sqrt2\over3}s\sqrt{1-s^2}\,x+{4\over3}s^2x^2.
\]

For \(s\le1/3\), the unconstrained quadratic minimizer lies below \(-1\),
so \(x=-1\).  The resulting expression is decreasing on this interval and
is exactly \(m(s)\), proving (30c).  Sharpness under (30b) follows by taking
the minimizing unit ray at \(s=\eta\) and scaling it by
\(\sqrt{1-\eta^2}\|\Delta Z_h\|_F\); this is its closest point to the exact
direction and has relative error exactly \(\eta\).

At \(\eta=1/10\),

\[
 m(1/10)={199\over300}-{\sqrt{198}\over150}>{17\over30}. \tag{30d}
\]

The fixed POVM \((I\pm T)/2\) therefore succeeds with probability greater
than \(47/60\).  If the prepared quantum state is within trace distance
\(\delta\) of \(|y\rangle\langle y|\), success remains greater than
\(47/60-\delta\); in particular \(\delta=1/100\) leaves constant bias.
Consequently the \(\Omega(P)\) raw-query theorem holds for every adversarial
approximate reduced direction satisfying (30a) with \(\eta\le1/10\).

The same conclusion holds for the exact feasible lift
\(\widetilde{\Delta X}_i=R_iYR_i^T\).  Conjugation multiplies the two
coordinates swapped by \(T\) by the same prefix sign, so the normalized
global expectation of \(T_{\rm glob}\) equals the root expectation exactly.
The approximate unit step is also physical:

\[
 \lambda_{\min}(I/3+Y)
 \ge {1\over3}-{1\over45}-{\sqrt6\over90}\eta
 >{3\over10}\qquad(\eta\le1/10).                       \tag{30e}
\]

Thus every lifted block remains positive definite.  None of these statements
follows from a constant relative residual in the unreduced KKT equations:
the path copy operator has small singular values, and conversion to reduced
tangent error requires a separate stability bound.

### 4.3 Complete primal-plus-multiplier KKT-state hardness

The baseline \(3I\) removes all diagonal coordinates from the KKT
right-hand side at \(X^0=I/3\).  This makes a constant-bias theorem possible
for the normalized complete solution of (20a), including every equality
multiplier.

Let \(\tau_i\) be the prefix sign at node \(i\), and set
\[
 \alpha=\frac KP=\frac{16}{33},\qquad
 \beta=\frac9P,\qquad
 c=\frac{\sqrt2\gamma}{P},\qquad d=\frac{\sqrt2u}{9}.
\]
On the three off-diagonal primal coordinate chains the exact solution is
\[
 d_{12,i}=-d\tau_i,\qquad
 d_{13,i}=-dh\tau_i,\qquad
 d_{23,i}=-d.                                      \tag{K1}
\]
All diagonal primal directions vanish.  Define the public edge tent
\[
 v_e=\begin{cases}
 c(1-\alpha)e,&1\le e\le K,\\
 c\alpha(P-e),&K<e<P.
 \end{cases}                                      \tag{K2}
\]
In the multiplier sign convention of (20a), the only nonzero equality
multipliers are
\[
 y_{12,e}=-\tau_ev_e,\qquad
 y_{13,e}=h\tau_ev_{P-e}.                         \tag{K3}
\]
The \(23\)-copy multipliers, all diagonal-copy multipliers, and the trace-row
multiplier are zero.

To verify (K3), let \(B_\sigma\) be the signed path incidence on either the
\(12\) or \(13\) chain.  With
\(T_\tau=\operatorname{diag}(\tau_0,\ldots,\tau_{P-1})\),
\(S_\tau=\operatorname{diag}(\tau_1,\ldots,\tau_{P-1})\), and ordinary path
incidence \(B\), one has \(B_\sigma=S_\tau BT_\tau\).  Gauging
\(\beta d-B_\sigma^Ty=-g\) gives the public zero-sum load
\(c({\bf1}_{\rm pre}-\alpha{\bf1})=-B^Tv\) in the \(12\) chain.
The \(13\) load is \(h\) times its node reversal, yielding (K3).
The \(23\) gradient lies entirely in the constant feasible tangent, so its
copy multiplier is zero.

Normalize the complete vector \((\Delta x,\Delta y)\) in the block-major
primal and edge-major multiplier ordering of (20a).  Let \(T_{\rm KKT}\)
swap the \(12\) and \(13\) coordinates within every primal block and within
the copy multipliers on every edge, and act as zero on all other
coordinates.  This is a fixed public norm-one observable.  Writing
\[
 D=\sum_i d_{12,i}^2=\frac{11N}{1350},\quad
 V=\sum_e v_e^2=\frac{289N}{4950}+\frac{17}{158400N},\quad
 C=\sum_e v_ev_{P-e}=\frac{577N}{9900}+\frac1{9900N},       \tag{K4}
\]
equations (K1)--(K3) give
\[
 \langle T_{\rm KKT}\rangle
 =\frac{2h(D-C)}{3D+2V}.                                  \tag{K5}
\]
Its sign is \(-h\), and its magnitude obeys the uniform rational bound
\[
 \left|\langle T_{\rm KKT}\rangle\right|
 \ge\frac{1489}{2097}>\frac7{10}.                          \tag{K6}
\]
Indeed, the leading-\(N\) ratio in (K5) is \(1489/2097\);
the ratio of the positive \(1/N\) corrections in its numerator and
denominator is \(16/17>1489/2097\), so every finite \(N\) only increases
the magnitude.

Because the sign in (K5) is \(-h\), use the fixed POVM
\((I\mp T_{\rm KKT})/2\), equivalently reverse the two outcome labels.  It
recovers parity with success probability greater than \(17/20\).  Trace error
\(1/100\) leaves success greater than \(21/25\).  Consequently:

> **Complete-KKT-state lower bound.**  Preparing the normalized complete
> equality-constrained KKT solution \((\Delta x,\Delta y)\) of (20a), in its
> displayed sign convention and ordering, to trace distance \(1/100\)
> requires \(\Omega(N)=\Omega(P)\) raw coherent coefficient queries.

The multiplier calculation is not a bounded-condition claim for the
unreduced saddle matrix.  It only shows that normalization by the complete
solution norm does not erase the parity signal.
Unlike the root and global primal-direction observables, this complete-state
decoder is tied to the canonical unit-scaled copy rows and multiplier sign
convention in (20a).  Rescaling or mixing equality rows changes multiplier
coordinates and can change the normalized complete state.  Such an
input-dependent row gauge must be constructed from, and charged to, the raw
coefficient oracle; it is not part of the displayed output contract.

### 4.4 Approximate-feasibility and objective-state theorem

There is a weaker but fully ambient robustness statement at the natural
inverse-square-root residual scale.  Consider arbitrary blocks \(X_i\succeq0\)
and let the residual consist of the trace row and all copy rows in their exact
isometric-svec scaling:

\[
 e_0=\operatorname{tr}X_0-1,qquad
 E_i=X_i-G_iX_{i-1}G_i^T,qquad
 e_0^2+\sum_{i=1}^{P-1}\|E_i\|_F^2\le\epsilon^2.        \tag{30f}
\]

Suppose also that the primal objective

\[
 f(X)={1\over P}\sum_i\langle C_i,X_i\rangle
 \le v_h+\delta_{\rm obj}.                              \tag{30g}
\]

Gauge the blocks to the root frame:
\(Z_i=R_i^TX_iR_i\) and \(D_i=Z_i-Z_{i-1}=R_i^TE_iR_i\).
For \(\bar t=P^{-1}\sum_i\operatorname{tr}X_i\), Cauchy--Schwarz gives the
exact useful bounds

\[
 |\bar t-1|
 \le\left(1+3\sum_{\ell=1}^{P-1}{\ell^2\over P^2}\right)^{1/2}\epsilon
 <\sqrt P\,\epsilon.                                    \tag{30h}
\]

Writing \(\widehat C_i=R_i^TC_iR_i\) and
\(W_j=P^{-1}\sum_{i=j}^{P-1}\widehat C_i\), one also has

\[
 f(X)=\langle\overline C_h,Z_0\rangle
       +\sum_{j=1}^{P-1}\langle W_j,D_j\rangle,qquad
 \left|\sum_j\langle W_j,D_j\rangle\right|
 <{13\over4}\sqrt P\,\epsilon.                         \tag{30i}
\]

Indeed, \(\|C_i\|_{\rm op}<13/4\) implies
\(\|W_j\|_F\le(13\sqrt3/4)(P-j)/P\), and summing the
squared suffix weights proves (30i).  Since \(Z_0\succeq0\),
\(\operatorname{tr}Z_0\ge1-\epsilon\), and
\(\lambda_{\min}(\overline C_h)=v_h\),

\[
 f(X)\ge v_h(1-\epsilon)-{13\over4}\sqrt P\,\epsilon. \tag{30j}
\]

Normalize the block diagonal matrix by trace,
\(\rho(X)=(\bigoplus_iX_i)/\sum_i\operatorname{tr}X_i\), and define the
public contraction

\[
 M={1\over2/5}\left(\bigoplus_i C_i-{57\over20}I\right). \tag{30k}
\]

Its norm is at most one because every local cost has spectrum in
\((11/4,13/4)\).  If

\[
 \epsilon\le{1\over400\sqrt P},qquad
 \delta_{\rm obj}\le{1\over100},                        \tag{30l}
\]

then (30h)--(30j), \(P\ge33\), and \(\sqrt{33}>5\) imply

\[
 \begin{array}{ll}
 h=+1:&\operatorname{tr}((\bigoplus_iC_i)\rho(X))>23/8,\\
 h=-1:&\operatorname{tr}((\bigoplus_iC_i)\rho(X))<113/40.
 \end{array}                                             \tag{30m}
\]

For the positive case, use (30j),
\(\bar t<1+1/400\), and \(\epsilon<1/2000\).  For the negative case, use
(30g) and \(\bar t>1-1/400\).  Thus

\[
                         \boxed{h\operatorname{tr}(M\rho(X))>{1\over16}.} \tag{30n}
\]

The fixed POVM \((I\pm M)/2\) reads parity with advantage greater than
\(1/32\).  Preparing any state within trace distance \(1/100\) of the trace
normalization of an arbitrary PSD point satisfying (30f)--(30l) therefore
still leaves a fixed positive advantage; a constant number of repetitions
amplifies it to bounded error.  The preparation therefore costs
\(\Omega(P)\) raw coefficient queries.

The \(P^{-1/2}\) feasibility scale is asymptotically sharp for this type of
statement.  Fix a positive-parity base input.  For every hidden bit \(j\),
flip only that bit and lift the negative-parity optimizer
\(Z_-^*=r_-r_-^T\) along the neighboring path.  The average of these \(N\)
exact neighboring optimizers is blockwise PSD, has trace one in every block,
and has objective \(v_-=14/5\), despite the base optimum \(v_+=29/10\).
Under the base constraints, only the \(N\) hidden transitions have nonzero
residual.  After conjugation back by the corresponding base-prefix matrix,
each equals

\[
 {D_-Z_-^*D_- -Z_-^*\over N},qquad D_-=\operatorname{Diag}(-1,1,1),
\]

whose Frobenius norm is \(4/(3N)\).  Hence the full residual is

\[
                         {4\over3\sqrt N}=\Theta(P^{-1/2}). \tag{30o}
\]

This wrong-value PSD point also makes the cost observable in (30k) report
negative parity.  Thus (30l) is sharp in residual order, not in its numerical
constant.  No constant-residual approximate-feasibility theorem is possible
under these promises.

### 4.5 Matching upper bounds and the intrinsic-versus-loading split

The value and root-state lower bounds are exactly tight, including their
leading query constant.  From (15),

\[
                         v_h=\frac{57}{20}+\frac h{20}.
\tag{U1}
\]

The standard exact quantum parity algorithm computes \(h\) with
\(\lceil N/2\rceil\) sign queries.  Equation (U1) then gives the exact optimal
value with no further query.  Concretely, apply Deutsch's one-query parity
circuit to each pair \((\sigma_{2r-1},\sigma_{2r})\), measure its exact pair
parity, and accumulate those outcomes in one classical bit; if \(N\) is odd,
query the last sign once.  This is QRAM-free, uses
\(O(N\log N)\) elementary routing gates, \(O(\log N)\) quantum workspace, and
constant classical workspace.  Conversely, any additive-\(1/25\), bounded-error
value algorithm computes parity by thresholding, as in Section 3.  Since
bounded-error parity also needs \(\lceil N/2\rceil\) queries, the precise raw
query complexity is in fact the complete two-regime characterization

\[
 Q_{\rm add,\epsilon}=
 \begin{cases}
  \lceil N/2\rceil,&0\le\epsilon<1/20,\\
  0,&\epsilon\ge1/20,
 \end{cases}
 \qquad
 Q_{\rm rel,r}=
 \begin{cases}
  \lceil N/2\rceil,&0\le r<1/57,\\
  0,&r\ge1/57.
 \end{cases}
\tag{U2}
\]

The zero-query branches use the public midpoint described after (17), and
the query-optimal parity algorithm supplies the exact answer on the other
branches.  In particular, both contracts displayed in (17) cost exactly
\(\lceil N/2\rceil\) queries.

The same exact parity computation followed by a public controlled phase
prepares the root state (26) with \(\lceil N/2\rceil\) queries.  The retained
parity/work registers cause no mixing of the requested state: on each fixed
input the exact parity output is the deterministic basis state \(|h\rangle\),
so the root-direction register is a product factor.  Thus the root-state
query complexity is also exactly \(\lceil N/2\rceil\) under the usual output
contract that permits unobserved workspace.  If every work register must be
returned clean, a simpler \(N\)-query construction starts from

\[
 \frac{|12\rangle+|23\rangle+|13\rangle}{\sqrt3}
\]

and, for each \(j\), uses one sign-bit phase-kickback query routed to the
\(|13\rangle\) component and to a public dummy \(+1\) coefficient on the
other two components.  The accumulated relative phase is exactly \(h\), and
all query-routing workspace is uncomputed after each call.

The global direction contains prefix information in addition to the final
parity, but it still has a direct linear-query, QRAM-free preparation.  Let

\[
 L(i)=\min\{N,\max\{0,i-K+1\}\},
 \qquad
 \tau_i=\prod_{j=1}^{L(i)}\sigma_j.
\tag{U3}
\]

Equations (23) and (29) give, up to a global sign,

\[
 |\delta x_h^{\rm glob}\rangle
 =\frac1{\sqrt{3P}}\sum_{i=0}^{P-1}|i\rangle
   \left(\tau_i|12\rangle+|23\rangle+\tau_i h|13\rangle\right).
\tag{U4}
\]

Start from the public uniform state obtained from (U4) by replacing all three
coefficients by \(+1\).  Hidden edge \(j\) has node threshold
\(t_j=K+j-1\).  For each \(j=1,\ldots,N\), coherently route one phase query
according to the public predicate

\[
 c_j(i,\ell)=
 \begin{cases}
  [i\ge t_j],&\ell=12,\\
  0,&\ell=23,\\
  [i<t_j],&\ell=13.
 \end{cases}
\tag{U5}
\]

If \(c_j=1\), query a fixed public coefficient position carrying
\(\sigma_j\); otherwise query a public dummy \(+1\) position.  Phase kickback
therefore contributes \(\sigma_j\) exactly where (U5) is one.  The accumulated
phases are respectively

\[
 \prod_{j:t_j\le i}\sigma_j=\tau_i,qquad
 1,qquad
 \prod_{j:t_j>i}\sigma_j=\tau_i h,
\]

which proves (U4).  The circuit makes exactly \(N\) raw coefficient queries,
uses \(O(N\log P)\) elementary reversible gates and \(O(\log P)\) work
qubits, and requires neither a prefix table nor QRAM.  It is exact in the
arbitrary-rotation model.  In a discrete gate set, synthesizing the two public
uniform superpositions to error \(\epsilon\) adds only
\(\operatorname{polylog}(P/\epsilon)\) gates; every input-dependent phase
remains exact.

Consequently the global-state raw-query complexity lies between
\(\lceil N/2\rceil\) and \(N\), while the value and root-state tasks equal
\(\lceil N/2\rceil\).  This gives a sharper algorithmic interpretation of the
construction.  Its intrinsic optimization output depends only on the single
aggregated bit \(h\), after which the reduced value and root Newton direction
take constant work.  Returning the direction in all original product-cone
coordinates additionally loads the path gauge \((\tau_i)_i\), but that loading
still costs only linear work and logarithmic workspace.  A deterministic
classical algorithm needs all \(N\) signs in the worst case for either value,
so this promise family permits only the familiar factor-two exact quantum
parity improvement, not an asymptotic speedup.

### 4.6 Canonical KKT block-encoding-call lower bound

Put \(d=6P\), \(m=6(P-1)+1=6P-5\), and set
\(y'=-\Delta y\) in (20a).  The Newton system is

\[
 M_\sigma\binom{\Delta x}{y'}=\binom{-g}{0},
 \qquad
 M_\sigma=
 \begin{pmatrix}(9/P)I_d&\widetilde A_\sigma^T\\
                 \widetilde A_\sigma&0_m\end{pmatrix}
 \in\mathbb R^{(12P-5)\times(12P-5)}.
\tag{KB1}
\]

Every copy row of \(\widetilde A_\sigma\) has absolute row sum two, the
trace row has sum three, and every column has sum at most two.  Since
\(P\ge33\),

\[
 \max_r\|(M_\sigma)_{r,*}\|_1
 =\max_c\|(M_\sigma)_{*,c}\|_1=3.
\tag{KB2}
\]

The equality is attained by the trace-multiplier row; a primal row has sum
at most \(2+9/P<3\).  The support and magnitudes are public.  A hidden sign
changes two predecessor coefficients, in the \(12\) and \(13\) copy rows,
and therefore four symmetric KKT positions.

For every potential nonzero \((r,c)\), introduce a distinct public label
\(\lvert e_{rc}\rangle\) and mutually orthogonal failure labels
\(\lvert L_r\rangle,\lvert R_c\rangle\).  Define

\[
\begin{aligned}
 \lvert\chi_r\rangle
 &=\sum_{c:(r,c)\in\operatorname{supp}M}
   \sqrt{\frac{|M_{rc}|}{3}}\lvert e_{rc}\rangle
   +\sqrt{1-\frac{\|(M_\sigma)_{r,*}\|_1}{3}}\lvert L_r\rangle,\\
 \lvert\phi_c^\sigma\rangle
 &=\sum_{r:(r,c)\in\operatorname{supp}M}
   \operatorname{sgn}(M_{rc}^\sigma)
   \sqrt{\frac{|M_{rc}|}{3}}\lvert e_{rc}\rangle
   +\sqrt{1-\frac{\|(M_\sigma)_{*,c}\|_1}{3}}\lvert R_c\rangle.
\end{aligned}
\tag{KB3}
\]

Each family is orthonormal because its labels are disjoint, and

\[
                   \langle\chi_r|\phi_c^\sigma\rangle
                   ={(M_\sigma)_{rc}\over3}.
\tag{KB4}
\]

Choose public unitary completions

\[
 L\lvert0,r\rangle=\lvert\chi_r\rangle,
 \qquad R_0\lvert0,c\rangle=\lvert\phi_c^0\rangle,
\tag{KB5}
\]

where the superscript zero sets hidden signs to \(+1\) but retains all
public signs.  Concretely, use the direct sum over disjoint row or column
sectors of the real Householder reflection taking a public seed to the state
in (KB3), with the identity on a fixed complement.  Padded invalid addresses
use a public bijection, so the junk action is input-independent.

On an entry label, reversibly recognize the four symmetric positions
controlled by a hidden edge and compute its bit index \(j\).  Let
\(S_\sigma\) multiply those labels by \(\sigma_j\), acting identically
elsewhere.  A public dummy index \(\sigma_0=1\) makes ordinary, adjoint, and
externally controlled uses cost one coherent phase-sign query.  Then

\[
 R_\sigma=S_\sigma R_0,
 \qquad U_M=L^\dagger R_\sigma
\tag{KB6}
\]

is an exact normalization-three block encoding:

\[
                  \langle0,r|U_M|0,c\rangle
                  ={(M_\sigma)_{rc}\over3},
                  \qquad \alpha_M=3.
\tag{KB7}
\]

The RHS \((-g,0)\), its state preparation, layouts, the two observables in
Section 4.1, and \(T_{\rm KKT}\) in Section 4.3 are public.  The multiplier
coordinate in (KB1) is \(y'=-\Delta y\), but this fixed sign flip on the
entire multiplier sector leaves every within-sector swap in
\(T_{\rm KKT}\) unchanged.  Substitution of the one-query implementation
into the raw parity reductions proves:

> **Canonical KKT-access theorem.**  Preparing the normalized root-primal
> state, global-primal state, or complete primal-plus-multiplier KKT state of
> Sections 4.1 and 4.3 to trace distance \(1/100\), from the canonical
> encoding (KB6), requires
> \[
>                         q_{\rm BE}\ge \lceil N/2\rceil=\Omega(P)
> \tag{KB8}
> \]
> block-encoding, adjoint, or controlled calls.

The theorem is deliberately relative to the displayed completion.  An
arbitrary input-dependent completion supplied at unit cost could store
prefix products or parity in its junk blocks.  Any queries or preprocessing
used to construct another completion must be charged.  Constant
normalization also does not assert that the unreduced saddle matrix is
condition one; (22) concerns the equality-reduced primal Hessian.

### 4.7 Nullspace-projector synthesis lower bound

Let \(\Pi_\sigma\) be the Euclidean orthogonal projector in the
\(6P\)-dimensional svec space onto
\(\ker\widetilde A_\sigma\).  Projecting (20a) gives

\[
                         \Pi_\sigma g=-{9\over P}\Delta x.
\tag{NP1}
\]

Using (23), \(\|A_h\|_F^2=6\), and Frobenius invariance under the block
congruences gives

\[
 \|\Delta x\|_2^2=P{u^2\over81}\|A_h\|_F^2={P\over1350},
 \qquad
 \|\Pi_\sigma g\|_2^2={3\over50P}.
\tag{NP2}
\]

Because the public baseline is \(3I\), the gradient (20) contains only the
three off-diagonal anisotropies.  Their svec coordinates are orthogonal, so

\[
 \|g\|_2^2
 ={1\over P}\left(2u^2+4q\gamma^2\right)
 ={41\over400P}.
\tag{NP3}
\]

Thus the public state \(\lvert\widehat g\rangle=g/\|g\|_2\) has exact
projector signal probability

\[
 \|\Pi_\sigma\lvert\widehat g\rangle\|_2^2={24\over41}.
\tag{NP4}
\]

Conditional on this signal, the state is the normalized global direction,
up to global sign.  The direct-sum swap \(T_{\rm glob}\) therefore has
conditional expectation \(2h/3\), and its unconditioned signal-sector
expectation satisfies

\[
                         h\,\langle T_{\rm glob}\rangle={16\over41}.
\tag{NP5}
\]

No postselection is needed.  Suppose a raw-query circuit implements a
normalization-one block encoding with principal block \(B_\sigma\) obeying

\[
                         \|B_\sigma-\Pi_\sigma\|\le\varepsilon.
\tag{NP6}
\]

Apply it once to \(\lvert\widehat g\rangle\), and measure
\(T_{\rm glob}\) on the output signal sector and zero on the junk sector.
For \(v_h=\Pi_\sigma\lvert\widehat g\rangle\) and
\(e_h=(B_\sigma-\Pi_\sigma)\lvert\widehat g\rangle\), one has
\(\|v_h\|=\sqrt{24/41}\), \(\|e_h\|\le\varepsilon\), and

\[
\begin{aligned}
 h\,\langle T_{\rm glob}\rangle
 &\ge {16\over41}-2\sqrt{24\over41}\,\varepsilon-\varepsilon^2\\
 &\ge {16\over41}-{1\over16}\sqrt{24\over41}-{1\over1024}
 >0.341,
 \qquad \varepsilon\le{1\over32}.
\end{aligned}
\tag{NP7}
\]

Assigning a fair random answer on the zero eigenspace gives success greater
than \(1/2+0.341/2>2/3\) after one call.

> **Nullspace-projector synthesis theorem.**  Any uniform raw-coefficient
> query circuit which, for every input, synthesizes a normalization-one
> block encoding (NP6) of \(\Pi_\sigma\) with error at most \(1/32\) uses
> at least \(\lceil N/2\rceil=\Omega(P)\) raw queries, counting setup and the
> first usable call.

Indeed, compose the synthesized unitary with the one-call decoder and apply
the degree-\(N\) parity bound.  Equivalently,
\(q_{\rm setup}+q_{\rm call}\ge\lceil N/2\rceil\).  After linear setup,
later marginal calls may be cheap.  Any completion actually built by the counted circuit is
allowed because only its principal block is measured.  If an arbitrary
projector oracle, parity, or prefix-gauge data are supplied for free, that
stronger access model has already performed the hard aggregation; one
projector call then suffices, so this is not a block-encoding-call lower
bound.

#### Matching exact QRAM-free projector synthesis

The synthesis lower bound is tight up to an absolute factor.  Let
\(\tau_i\) be the prefix sign at node \(i\), and define

\[
 \chi_\ell=
 \begin{cases}
  1,&\ell\in\{12,13\},\\
  0,&\ell\in\{11,22,23,33\}.
 \end{cases}
 \qquad
 F_\sigma\lvert i,\ell\rangle
 =\tau_i^{\chi_\ell}\lvert i,\ell\rangle.
\tag{PU1}
\]

For each hidden edge \(j\), compute the public predicate
\([i\ge K+j-1]\wedge\chi_\ell\), route a phase query to \(j\) when it is
true and to a public dummy \(+1\) address otherwise, and uncompute.  Repeating
over the \(N\) edges implements \(F_\sigma\) with exactly \(N\) raw
coefficient queries and no prefix table.

Let \(U_0\lvert0\rangle=P^{-1/2}\sum_i\lvert i\rangle\) be a public
unitary completion and set

\[
 U_{W,\sigma}=F_\sigma(U_0\otimes I_6).
\tag{PU2}
\]

Then

\[
 U_{W,\sigma}\lvert0,\ell\rangle
 ={1\over\sqrt P}\sum_i\tau_i^{\chi_\ell}\lvert i,\ell\rangle
\tag{PU3}
\]

is the full six-coordinate isometry for the copy equalities.  The trace row
removes the public normalized coordinate

\[
 \lvert t\rangle={\lvert11\rangle+\lvert22\rangle+\lvert33\rangle\over\sqrt3},
 \qquad Q_0=I_6-\lvert t\rangle\langle t\rvert.
\tag{PU4}
\]

Consequently the exact tangent projector is

\[
 \Pi_\sigma=U_{W,\sigma}
 (\lvert0\rangle\langle0\rvert\otimes Q_0)
 U_{W,\sigma}^\dagger.
\tag{PU5}
\]

To block encode the middle public projector in (PU5), add one signal qubit.
A fixed coordinate rotation sends \(\lvert t\rangle\) to a designated basis
state; flip the signal qubit unless the node register is zero and the
coordinate lies in the other five basis states, then undo the rotation.
The signal-zero block of this public flag unitary is exactly
\(\lvert0\rangle\langle0\rvert\otimes Q_0\).  Conjugating it by
\(U_{W,\sigma}\) and \(U_{W,\sigma}^\dagger\) therefore gives an exact
normalization-one block encoding of \(\Pi_\sigma\).

One call uses exactly \(2N\) raw queries, \(O(N\log P)\) public reversible
gates, and \(O(\log P)\) workspace.  Thus it matches the
\(\lceil N/2\rceil\) lower bound within a factor four.  Alternatively, an
\(N\)-query setup may cache the prefix signs and reduce later marginal query
cost, exactly as permitted by the setup-versus-first-call statement.  The
construction is exact with arbitrary public rotations; a discrete gate set
adds only public polylogarithmic synthesis overhead for \(U_0\) and the
trace-coordinate rotation.

## 5. Non-SOCP geometry

Projection of the feasible set of (10) onto \(X_0\) is exactly

\[
 \mathcal D_3=\{Z\succeq0:\operatorname{tr}Z=1\},             \tag{31}
\]

and (4) is its linear inverse.  If \(\mathcal D_3\) had a lift over a finite
product of second-order cones, homogenizing that lift would give such a lift
for

\[
 \operatorname{cone}(\mathcal D_3)=\mathbb S_+^3.             \tag{32}
\]

Concretely, replace every affine lift equation \(Ay=b\) by
\(Ay=tb\), impose \(t\ge0\), keep the lifting variable in its product cone,
and project \((y,t)\) to the matrix component.  For \(t>0\), division by \(t\)
shows that the projection is exactly \(t\mathcal D_3\).  At \(t=0\), let \(y\)
be any feasible homogeneous direction and let \(y_0\) lift one point of
\(\mathcal D_3\).  Convex conicity gives \(y_0+sy\) in the original affine lift
for every \(s\ge0\).  Compactness of \(\mathcal D_3\) therefore forces the matrix
projection of \(y\) to be zero.  Hence no extra nonzero matrices enter at \(t=0\),
and the homogenized projection is exactly (32).  Fawzi's theorem that
\(\mathbb S_+^3\) has no finite SOC lift
therefore rules out a finite SOC lift of (31), and hence of the path-feasible
set.

## 6. Conditioning and coordinate caveats

For reference, the standalone unnormalized cone problem with cost
\(\overline C_h\) has central reduced Hessian

\[
 H_h[Y]=\frac1\mu\overline C_hY\overline C_h.                 \tag{33}
\]

Equation (14) gives

\[
 \kappa_2(\overline C_+)=\frac{32}{29},\qquad
 \kappa_2(\overline C_-)=\frac{31}{28},
 \qquad \kappa_2(H_h)<\frac54.              \tag{34}
\]

### 6.1 The unscaled saddle matrix has condition \(\Theta(P)\)

The condition-one reduced Hessian must not be confused with the ordinary
spectral condition number of the unscaled symmetric KKT matrix (KB1).  Let
\(A=\widetilde A_\sigma\), \(\beta=9/P\), and
\[
                         M=\begin{pmatrix}\beta I&A^T\\A&0\end{pmatrix}.
\tag{34a}
\]
Then, uniformly over every sign input,
\[
                              \boxed{\kappa_2(M)=\Theta(P).}
\tag{34b}
\]

Here is a direct proof.  Orthogonal diagonal switching removes all signs from
the six path-copy operators without changing singular values.  On each of the
three off-diagonal svec coordinates, \(A\) is the ordinary
\((P-1)\)-by-\(P\) path difference matrix \(B\), whose nonzero singular values
are
\[
                         2\sin\frac{k\pi}{2P},\qquad 1\le k<P.
\tag{34c}
\]
In particular its least positive singular value lies between \(2/P\) and
\(\pi/P\).

For completeness, the trace row does not create a smaller scale on the three
diagonal paths.  Let \(x=(x^{(1)},x^{(2)},x^{(3)})\) be orthogonal to the
kernel of that diagonal subsystem.  If
\(m_k=P^{-1}{\bf1}^Tx^{(k)}\), orthogonality to all constant triples with
coefficient vector \(a\) satisfying \(a_1+a_2+a_3=0\) implies
\(m_1=m_2=m_3=:m\).  Write
\(x^{(k)}=m{\bf1}+z^{(k)}\), where each \(z^{(k)}\) has mean zero, and put
\[
 E^2=\sum_k\|Bz^{(k)}\|_2^2,qquad
 t=\sum_k x^{(k)}_0.
\]
The path Poincare inequality from (34c) gives
\(\sum_k\|z^{(k)}\|_2^2\le(P^2/4)E^2\).  Also
\[
 |z^{(k)}_0|
 =\left|P^{-1}\sum_{j=0}^{P-1}(z^{(k)}_0-z^{(k)}_j)\right|
 \le\sqrt P\,\|Bz^{(k)}\|_2.
\]
Since \(3m=t-\sum_kz^{(k)}_0\), these bounds imply
\[
 \|x\|_2^2
 =3Pm^2+\sum_k\|z^{(k)}\|_2^2
 \le\frac94P^2(t^2+E^2).
\tag{34d}
\]
But \(t^2+E^2\) is exactly the squared norm of the diagonal subsystem applied
to \(x\).  Combining this with the off-diagonal paths yields
\[
 \frac{2}{3P}\le s_{\min}^+(A)\le\frac\pi P,qquad
 \sqrt3\le s_{\max}(A)\le\sqrt6.             \tag{34e}
\]
The last upper bound also follows directly from maximum absolute row sum three
and maximum absolute column sum two.

Finally take an SVD of \(A\).  The five-dimensional kernel of \(A\) gives the
exact eigenvalue \(\beta=9/P\) of \(M\).  Every positive singular value \(s\)
of \(A\) gives the two eigenvalues
\[
                 \lambda_\pm(s)=\frac{\beta\pm\sqrt{\beta^2+4s^2}}2.
\tag{34f}
\]
Equations (34e)--(34f) show that the largest absolute eigenvalue is bounded
above and below by positive constants.  Moreover, the smallest absolute
eigenvalue is at most \(9/P\), while every eigenvalue has magnitude at least
\[
 {1\over P}\min\left\{9,{2\over3},
                 {\sqrt{745}-27\over6}\right\}>0.
\]
This proves (34b).  Thus the family simultaneously has a condition-one
equality-reduced primal Hessian and a linearly ill-conditioned unscaled saddle
matrix; neither statement contradicts the other.

The exact condition-one result (22), however, is for the trace-normalized
problem at the public start.  It is not a condition-one claim for the full
saddle KKT matrix or for every symmetrized primal--dual SDP Newton system.
Supplying the input-dependent elimination map \(\mathcal W_\sigma\), or the
already aggregated reduced gradient, gives away the hard path product.

The unequal spectra rule out every orthogonal hidden gauge.  An arbitrary
input-dependent nonorthogonal congruence can still canonicalize one positive
definite cost, but it changes the trace constraint and must itself be
constructed from the raw signed coefficients.  The query theorem charges
that construction.  In any case, the optimal-value gap (16) is invariant
under an exact reparameterization that preserves the objective, so the
optimal-value lower bound is not an output-coordinate artifact.

This intrinsic conclusion concerns the optimization problem and its scalar
value, not the coordinate-free identity of the normalized Newton direction.
Indeed, with \(D=\operatorname{Diag}(1,-1,1)\),
\[
                         D A_-D=-A_+.
\]
Consequently the two root direction matrices in (23) are related by an
orthogonal congruence and an irrelevant global sign when viewed as amplitude
states.  The state lower bound remains valid because it requests the direction
in the fixed public root coordinate, where the public measurement (27) decodes
parity.  It should not be advertised as hardness after an input-dependent
output gauge is supplied for free.  The global direction additionally carries
the prefix gauges described in Section 4.5.

For the displayed anisotropic Newton system, (K2)--(K3) in fact bound every
equality-multiplier coordinate by an absolute constant, and Section 4.3 gives
a complete primal-plus-multiplier state theorem.  This does not bound the
condition number of the unreduced saddle matrix, nor does it claim a
representation-invariant theorem for arbitrary row scalings or a complete
primal--dual SDP direction including a separate slack sector.  All primal
starting coordinates, local costs, barrier Hessian entries, residuals, and
primal Newton directions used in the theorem are also bounded by absolute
constants.

The exact value theorem by itself does not imply robustness to infeasibility.
Section 4.4 supplies the separate statement at residual
\(O(P^{-1/2})\), and its neighboring-instance mixture shows that this order
cannot be replaced by a constant under the same objective/state contract.
This sensitivity is consistent with the small singular values of the path
equality operator.

## 7. Novelty calibration

### 7.1 Classical ingredients and the SOC-lift boundary

The path elimination, signed-cycle spectrum, log-det Newton equation, and
spectral optimization over density matrices are classical ingredients.  In
particular, diagonal switching and cycle products are standard invariants of
signed or unit-gain adjacency matrices; see M. Kadyan and B. Bhattacharjya,
[*Switching equivalence of Hermitian adjacency matrices of mixed
graphs*](https://arxiv.org/abs/2103.13632).  Accumulating local group labels
into a global gauge or holonomy is also standard in synchronization; see
T. Gao, J. Brodzki, and S. Mukherjee,
[*The Geometry of Synchronization Problems and Learning Group
Actions*](https://arxiv.org/abs/1610.09051).  Orthogonal synchronization is
itself commonly relaxed as an SDP, for example by S. Ling,
[*Solving Orthogonal Group Synchronization via Convex and Low-Rank
Optimization*](https://arxiv.org/abs/2006.00902).  None of these sources uses
the signed product to prove an IPM or raw coefficient-query lower bound.

The parity lower bound is the polynomial-method result of R. Beals et al.,
[*Quantum lower bounds by polynomials*](https://arxiv.org/abs/quant-ph/9802049).
The trace-one density spectrahedron is a standard trace slice of a symmetric
cone.  H. Fawzi proves that the **cone** \(\mathbb S_+^3\) has no finite SOC
representation in
[*On representing the positive semidefinite cone using the second-order
cone*](https://arxiv.org/abs/1610.04901).  Fawzi does not need to be read as
separately proving the precise trace-one statement (31): that statement is
the direct compact-homogenization corollary proved in Section 5.  Thus neither
the non-SOC geometry nor the homogenization reduction should be claimed as a
separate principal novelty.

### 7.2 Optimal-value lower bounds

Optimal-value query hardness, even with a linear exponent, is already known.
Theorem 30 and Corollary 31 of J. van Apeldoorn, A. Gily\'en, S. Gribling, and
R. de Wolf,
[*Quantum SDP-Solvers: Better upper and lower
bounds*](https://arxiv.org/abs/1705.01843), encode a Boolean decision in two
possible integer optima of an LP and hence an SDP.  Their balanced instances
give stronger dense-instance exponents, but their width parameters are not
constant and their theorem does not impose bounded row and column incidence,
a trace-one \(S_+^3\) slice, or IPM Newton geometry.  The earlier
Brand\~ao--Svore bound,
[*Quantum Speed-ups for Semidefinite
Programming*](https://arxiv.org/abs/1609.05537), is another general
approximate-SDP comparator rather than this sparse construction.

More sharply, Theorem 8.4 of S. Apers and S. Gribling,
[*Quantum speedups for linear programming via interior point
methods*](https://arxiv.org/abs/2311.03215v3), gives
\(\Omega(\sqrt{nd}\,r)\) coefficient queries for constant-additive LP
optimal-value estimation when the constraint matrix has row sparsity \(r\).
For constant \(r\) and balanced dimensions this is already linear.  It is
therefore the closest collision with (17) at the level of exponent, sparsity,
and value output.  Its hard family is an LP construction based on a composed
majority--OR--majority function; it does not establish bounded **column**
degree, a signed-holonomy SDP over \(S_+^3\), intrinsic cost-spectrum parity,
or the public-start direction statement of Section 4.  Consequently (17)
should be described as a particularly structured matching linear lower bound,
not as the first sparse SDP optimal-value lower bound.

### 7.3 Newton-state and QLS boundaries

Quantum nullspace and primal--dual SDP-IPM direction systems are developed by
B. Augustino, G. Nannicini, T. Terlaky, and L. F. Zuluaga,
[*Quantum Interior Point Methods for Semidefinite
Optimization*](https://arxiv.org/abs/2112.06025).  This is the closest
algorithmic comparison to (21)--(23), but it is an upper-bound framework and
does not prove raw-query hardness of constructing its nullspace
representation.

Generic quantum-linear-system lower bounds do not subsume (30).  D. Orsucci
and V. Dunjko,
[*On solving classes of positive-definite quantum linear systems with
quadratically improved runtime in the condition
number*](https://arxiv.org/abs/2101.11868), and H. Mori et al.,
[*Sparsity-dependent Complexity Lower Bound of Quantum Linear System
Solvers*](https://arxiv.org/abs/2601.16697v2), concern a supplied square-system
oracle and its designated inverse-solution state.  Here condition number one
holds only after applying the input-dependent nullspace map
\(\mathcal W_\sigma\).  If a conventional QLS interface supplied the reduced
RHS state, it would already have supplied the parity-dependent aggregate.
The access distinction is explicit in G. H. Low and Y. Su,
[*Quantum linear system algorithm with optimal queries to initial state
preparation*](https://arxiv.org/abs/2410.18178), which treats the
matrix-block-encoding oracle and RHS-state-preparation oracle separately.
Thus (30) is not a condition-one QLSP lower bound under the standard supplied
RHS model, and it should not be compared to \(\Omega(\kappa)\) QLS bounds as if
the oracle contracts agreed.

Sections 4.6--4.7 make the access boundary explicit.  The first lower bound
uses calls to one fully specified constant-normalization KKT encoding; it does
not cover arbitrary input-dependent junk supplied for free.  The second is a
raw-query lower bound for *synthesizing* the nullspace projector.  It permits
any completion built by the counted circuit, but becomes a one-call parity
decoder when that projector oracle is supplied.  Neither statement is a
generic QLS condition-number lower bound.

### 7.4 Defensible novelty claim

A targeted primary-source search through September 2, 2026 found no previous
construction with this particular conjunction: bounded row and column path
incidence; a public signed-anisotropy triangle producing parity-dependent cost
spectrum and a constant optimal-value gap; a trace-normalized free
\(\mathbb S_+^3\) geometry; and a public-RHS, condition-one, full-step
Newton-direction state lower bound whose fixed decoder works on every
physical block and on the canonically normalized complete KKT solution.
The same family also supplies a relative-value contract and a sharp-order
ambient approximate-feasibility/near-optimal-state theorem.  The candidate
novelty is that explicit conjunction and the
shared instance witnessing both intrinsic value hardness and
reduction-access hardness, including the canonical KKT-call theorem and the
normalization-one projector-synthesis theorem.  It is not signed-cycle switching, SOC-lift
impossibility, parity, sparse optimal-value hardness, the linear exponent, or
nullspace elimination separately.  Bibliographic search is evidence against
an obvious collision, not proof of priority.
