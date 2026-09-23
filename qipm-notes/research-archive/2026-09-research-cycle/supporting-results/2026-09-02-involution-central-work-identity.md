# Coordinate-free central work under an involutive symmetry

Date: 2026-09-02

## Result

Let \(R\) be an orthogonal involution, let a differentiable convex barrier
\(F\) be \(R\)-invariant, and let the linear objective be \(R\)-invariant.
At a central KKT point, the multiplier work against the antisymmetric part
of the equality data is exactly

\[
 \boxed{
 y^TAx_-=
 \frac{\mu}{4}
 \langle x-Rx,\nabla F(x)-\nabla F(Rx)\rangle\ge0,
 \qquad x_-:=\frac{I-R}{2}x.}
\tag{1}
\]

The most robust definition of the “antisymmetric right-hand side” is
\[
                         r_-:=Ax_-,
\tag{2}
\]
not a selected subset of coordinates of \(b=Ax\).  This definition permits
arbitrary coupling and arbitrary invertible mixing of equality rows.  If the
rows are already split into \(A_+R=A_+\) and \(A_-R=-A_-\), then
\(r_-=(0,b_-)\), and (1) becomes the proposed formula
\[
 b_-^Ty_-=
 \frac{\mu}{4}
 \langle x-Rx,\nabla F(x)-\nabla F(Rx)\rangle.
\tag{3}
\]

At an \(R\)-fixed Newton start, the exact linear analogue is
\[
 \boxed{
 (A\Delta x_-)^T\Delta y
 =\Delta x_-^TG_0\Delta x_-\ge0,
 \qquad
 \Delta x_-=\frac{I-R}{2}\Delta x,}
\tag{4}
\]
provided the Newton Hessian \(G_0\succ0\) is \(R\)-invariant and the
stationarity right-hand side is \(R\)-symmetric.  In a pure row split, (4)
is \(r_-^T\Delta y_-=\Delta x_-^TG_0\Delta x_-\).

These are virtual-work identities.  They do not imply a
representation-independent lower bound on a multiplier norm: only the
source--multiplier pairing is invariant under general row mixing.

## 1. Exact central theorem

Work in a finite-dimensional Euclidean space.  Assume:

1. \(R^T=R\) and \(R^2=I\);
2. the open convex domain \(\Omega\) satisfies \(R\Omega=\Omega\);
3. \(F:\Omega\to\mathbb R\) is differentiable, convex, and
   \(F(Rx)=F(x)\);
4. \(R^Tc=c\); and
5. \(x\in\Omega\) and \(y\) satisfy the stationarity convention
   \[
                 A^Ty=c+\mu\nabla F(x),\qquad \mu>0.
   \tag{5}
   \]

The convention in (5) corresponds to the Lagrangian
\(c^Tx+\mu F(x)-y^T(Ax-b)\).  Reversing the sign of the equality term
reverses every multiplier-work sign below.

### Theorem 1 (involution central work)

Under assumptions 1--5, equations (1)--(2) hold.  No rank assumption on
\(A\) and no uniqueness assumption on \(y\) are required.

### Proof

The invariant objective has no antisymmetric work:
\[
 \langle x_-,c\rangle
 =\frac12\langle x-Rx,c\rangle
 =\frac12\langle x,c-R^Tc\rangle=0.
\tag{6}
\]
Pair (5) with \(x_-\):
\[
 y^TAx_-=\mu\langle x_-,\nabla F(x)\rangle.
\tag{7}
\]
Orthogonal invariance gives
\(\nabla F(Rx)=R\nabla F(x)\).  Since
\(R(x-Rx)=-(x-Rx)\),
\[
\begin{aligned}
 \langle x-Rx,\nabla F(Rx)\rangle
 &=\langle x-Rx,R\nabla F(x)\rangle\\
 &=\langle R(x-Rx),\nabla F(x)\rangle\\
 &=-\langle x-Rx,\nabla F(x)\rangle.
\end{aligned}
\tag{8}
\]
Equations (7)--(8) prove the equality in (1).  Convex-gradient
monotonicity gives
\[
 \langle x-Rx,\nabla F(x)-\nabla F(Rx)\rangle\ge0,
\tag{9}
\]
which proves the inequality.

If \(\widetilde y\) is another multiplier satisfying (5), then
\(A^T(\widetilde y-y)=0\), and therefore
\[
 (A x_-)^T(\widetilde y-y)=0.
\tag{10}
\]
Thus the work is independent of multiplier nonuniqueness. \(\square\)

There is an exact Bregman-divergence form that needs only the differentiable
assumptions of Theorem 1.  With

\[
 D_F(u,v)=F(u)-F(v)-\langle\nabla F(v),u-v\rangle,
\]

invariance and (8) give

\[
 D_F(Rx,x)=D_F(x,Rx)
 =\langle\nabla F(x),x-Rx\rangle.
\]

Hence

\[
 \boxed{
 y^TAx_-=\frac\mu2D_F(Rx,x)
        =\frac\mu2D_F(x,Rx).}
\tag{10a}
\]

Thus (1) is half of either directed Bregman divergence, multiplied by
\(\mu\), rather than merely a consequence of an inequality.  Strict
convexity of \(F\) on the chord from \(x\) to \(Rx\) makes the work strictly
positive whenever \(x\ne Rx\).

Exact primal feasibility is not needed for (1).  It is needed only to
identify \(Ax_-\) with a fixed right-hand-side component.  Suppose
\[
 A=\begin{pmatrix}A_+\\A_-\end{pmatrix},\qquad
 A_+R=A_+,\qquad A_-R=-A_-,
\tag{11}
\]
and \(Ax=(b_+,b_-)\).  Then \(A_+x_-=0\) and
\(A_-x_-=A_-x=b_-\), proving (3).  Extra rows with mixed symmetric and
antisymmetric coefficients do not invalidate (1); they only invalidate the
shortcut of identifying the work vector by selecting a row subset.

## 2. Exact integrated-Hessian form

Assume additionally that \(F\in C^2(\Omega)\).  The whole chord from \(Rx\)
to \(x\) lies in \(\Omega\).  Put
\[
 d=x-Rx,\qquad
 \overline H_x=\int_0^1
 \nabla^2F(Rx+t d)\,dt.
\tag{12}
\]
The fundamental theorem of calculus gives
\[
 \nabla F(x)-\nabla F(Rx)=\overline H_xd.
\]
Therefore (1) has the exact forms
\[
 \boxed{
 y^TAx_-=\frac{\mu}{4}d^T\overline H_xd
         =\mu x_-^T\overline H_xx_-.}
\tag{13}
\]
Moreover \(R\overline H_xR=\overline H_x\), because \(R\) reverses the
chord parameter and
\(\nabla^2F(Rz)=R\nabla^2F(z)R\).

If the Hessian restricted to the antisymmetric subspace along the chord
obeys
\[
 m_-I\preceq
 \nabla^2F(Rx+td)|_{\ker(I+R)}
 \preceq M_-I
 \qquad(0\le t\le1),
\tag{14}
\]
then the sharp immediate bounds are
\[
 \boxed{
 \mu m_-\|x_-\|_2^2
 \le y^TAx_-
 \le\mu M_-\|x_-\|_2^2.}
\tag{15}
\]
The work is strictly positive for \(x\ne Rx\) whenever the integrated
Hessian is positive definite on the chord direction.  Convexity alone does
not give strictness.

For a standard self-concordant barrier, let
\(x_+=(x+Rx)/2\) and
\(\delta=\|x_-\|_{x_+}<1\).  Standard Hessian comparison along the chord
can be integrated instead of replaced by its worst value.  This gives the
sharper local constants
\[
 \boxed{
 \mu\left(1-\delta+\frac{\delta^2}{3}\right)\delta^2
 \le y^TAx_-
 \le\frac{\mu}{1-\delta}\delta^2.}
\tag{16}
\]

Indeed, write a chord point as \(x_++u x_-\), where \(-1\le u\le1\).
Hessian comparison bounds the directional energy by
\((1-|u|\delta)^2\delta^2\) and
\((1-|u|\delta)^{-2}\delta^2\).  Their chord averages are
\((1-\delta+\delta^2/3)\delta^2\) and
\(\delta^2/(1-\delta)\).  The familiar coarser bounds with factors
\((1-\delta)^2\) and \((1-\delta)^{-2}\) follow immediately.  Equation
(13), rather than either comparison, is exact.

### 2.1 Paired-variable logarithmic barrier

Take \(E=\mathbb R^n\times\mathbb R^n\), let \(R(u,v)=(v,u)\), and use
\[
 F(u,v)=-\sum_{j=1}^n(\log u_j+\log v_j),\qquad u,v>0.
\]
Put \(d=u-v\) and \(q=u+v\).  Then
\(x_-=(d/2,-d/2)\).  An antisymmetric row block with coefficients
\((C,-C)\) imposes \(Cd=b_-\).  In the row-split representation, (1) becomes
\[
 \boxed{
 b_-^Ty_-
 =\frac\mu2\sum_{j=1}^n\frac{d_j^2}{u_jv_j}
 =\sum_{j=1}^n\frac{2\mu d_j^2}{q_j^2-d_j^2}.}
\tag{16a}
\]
This exactly recovers the graph-free paired-LP work identity, including the
factor \(1/4\) in (1), and is strictly positive exactly when \(d\ne0\).
If \(0<\ell\le u_j,v_j\le U\), then
\[
 \frac{\mu}{2U^2}\|d\|_2^2
 \le b_-^Ty_-
 \le\frac{\mu}{2\ell^2}\|d\|_2^2.
\tag{16b}
\]
For mixed rows, replace \(b_-^Ty_-\) by the canonical pairing
\((Ax_-)^Ty\); the scalar value is unchanged.

### 2.2 Log-det SDP barrier under a matrix involution

Let \(E=\mathbb S^r\) with the Frobenius inner product.  Fix a symmetric
orthogonal matrix \(Q\), so \(Q^2=I\), and let
\[
 \mathcal R(X)=QXQ,\qquad F(X)=-\log\det X
\]
on \(\mathbb S_{++}^r\).  Then
\(X_-=(X-QXQ)/2\), and the central dual matrix is
\(S=-\mu\nabla F(X)=\mu X^{-1}\).  Suppose the cost is
\(Q\)-symmetric.  In a row split whose antisymmetric measurement block
satisfies \(\mathcal C(X_-)=b_-\), equation (1) gives
\[
 \begin{aligned}
 b_-^Ty_-
 &=\frac\mu4\operatorname{tr}
   [(X-QXQ)(QX^{-1}Q-X^{-1})]\\
 &=\boxed{\frac\mu2
   [\operatorname{tr}(QXQX^{-1})-r]}.
 \end{aligned}
\tag{16c}
\]
The two cross traces in the first line agree by cyclicity.  If \(Y=QXQ\),
then \(X^{-1/2}YX^{-1/2}\succ0\) has determinant one.  Its trace is at least
\(r\), with equality exactly when \(Y=X\), proving strict positivity off the
fixed-point subspace.

The integrated-Hessian form is the exact noncommutative identity
\[
 \boxed{
 b_-^Ty_-
 =\mu\int_0^1
 \|Z_t^{-1/2}X_-Z_t^{-1/2}\|_F^2\,dt,
 \quad Z_t=QXQ+t(X-QXQ).}
\tag{16d}
\]
If \(\ell I\preceq X\preceq UI\), the same spectral bounds hold for every
\(Z_t\), so
\[
 \frac\mu{U^2}\|X_-\|_F^2
 \le b_-^Ty_-
 \le\frac\mu{\ell^2}\|X_-\|_F^2.
\tag{16e}
\]
The trace pairing in the first line of (16c) is the sum of the two directed
Stein losses between \(X\) and \(QXQ\).  Thus (16c) is the exact log-det SDP
analogue of (16a), not only a spectral comparison.  Under arbitrary mixed
measurement rows, its left side is again the canonical work
\((AX_-)^Ty\).

## 3. Newton linearization at a fixed start

Let \(x^0=Rx^0\).  Let \(G_0\succ0\) satisfy
\[
                         R G_0=G_0R.
\tag{17}
\]
For a barrier Newton step one has
\(G_0=\mu\nabla^2F(x^0)\), and (17) follows by differentiating
\(F(Rx)=F(x)\) at the fixed point.

Suppose the projected Newton equations have the sign convention
\[
 A\Delta x=r_p,\qquad
 G_0\Delta x-A^T\Delta y=h_+,
 \qquad Rh_+=h_+.
\tag{18}
\]
Symmetric and antisymmetric eigenspaces are orthogonal, \(G_0\) preserves
them, and \(P_-h_+=0\).  Pair the second equation with
\(\Delta x_-=P_-\Delta x\).  This gives exactly (4):
\[
 \Delta y^TA\Delta x_-
 =\Delta x_-^TG_0\Delta x_-.
\tag{19}
\]
If the rows have the split (11), then
\[
 A\Delta x_-=(0,A_-\Delta x_-).
\]
Because \(A_-x^0=0\), a Newton correction targeting
\(A_-(x^0+\Delta x)=b_-\) has
\(A_-\Delta x_-=b_-\).  Hence
\[
                  b_-^T\Delta y_-
 =\Delta x_-^TG_0\Delta x_->0
\tag{20}
\]
unless the antisymmetric correction vanishes.

For the logarithmic barrier at a pair-symmetric,
complementarity-centered start, (20) specializes to
\[
 r_a^T\Delta y_a
 =\Delta d^T
 \operatorname{Diag}\!\left(\frac{s_v^0}{2x_v^0}\right)
 \Delta d,
\tag{21}
\]
including the factor \(1/2\) in the paired coordinates.

If (18) has an antisymmetric stationarity forcing \(h_-\), the identity
acquires the term
\[
 \Delta y^TA\Delta x_-
 =\Delta x_-^TG_0\Delta x_-
   -\langle\Delta x_-,h_-\rangle
\tag{22}
\]
for the displayed sign convention.  It need not be nonnegative.  Likewise,
if \(x^0\) is not fixed or \(G_0\) does not preserve the two eigenspaces,
cross terms with \(\Delta x_+\) appear.

## 4. Row mixing and access caveats

Let \(U\) be any invertible, possibly nonorthogonal, equality-row change of
basis:
\[
                         A'=UA,\qquad y'=U^{-T}y.
\tag{23}
\]
The tracked work vector and its pairing transform as
\[
 r_-'=A'x_-=Ur_-,
 \qquad
 (r_-')^Ty'=r_-^Ty.
\tag{24}
\]
Thus arbitrary row mixing, including mixing symmetric and antisymmetric
rows, preserves the work if \(r_-\) is carried through the transformation.
It generally does not preserve a visible row subset called “the
antisymmetric rows.”  In the split representation (11), the vector that
must be tracked after mixing is
\[
                         U(0,b_-),
\tag{25}
\]
not the corresponding coordinates of the total transformed RHS
\(U(b_+,b_-)\).

Hölder gives only the product bounds
\[
 \|r_-'\|_2\|y'\|_2\ge r_-^Ty,\qquad
 \|r_-'\|_1\|y'\|_\infty\ge r_-^Ty.
\tag{26}
\]
An ill-conditioned row change can make multiplier coordinates small while
making the tracked source or the coefficient/block-encoding normalization
large.  No multiplier-norm theorem is invariant without charging that
representation change.

## 5. Failure modes and extensions

- **Multiplier sign.**  With the Lagrangian
  \(c^Tx+\mu F(x)+y^T(Ax-b)\), stationarity is
  \(A^Ty=-(c+\mu\nabla F(x))\), and the left side of (1) is the negative of
  the displayed nonnegative work.
- **Antisymmetric objective or forcing.**  If \(R^Tc\ne c\), then
  \[
  y^TAx_-=\langle x_-,c\rangle+
  \frac{\mu}{4}\langle d,\nabla F(x)-\nabla F(Rx)\rangle.
  \]
  The first term can have either sign.  Equation (22) is the Newton
  analogue.
- **Constraint coupling.**  Mixed rows do not harm the coordinate-free
  identity (1), but \(Ax_-\) may no longer be determined from the numerical
  RHS \(b=Ax\) alone.  Treating an arbitrary selected row block as \(b_-\)
  can therefore give a false statement.
- **Nonunique multipliers.**  They do not harm the work pairing, by (10),
  although their coordinate norms can vary after redundant rows are added.
- **Lack of strict convexity.**  Convexity proves nonnegativity, not strict
  positivity.  A barrier with a flat chord direction gives zero work even
  when \(x\ne Rx\).
- **Nonorthogonal involutions.**  The scalar identity actually extends to
  every invertible linear involution.  Invariance then gives
  \(\nabla F(Rx)=R^{-T}\nabla F(x)\), and
  \(R(x-Rx)=-(x-Rx)\) still proves the factor \(1/4\).
  Orthogonality is needed for the Euclidean orthogonal-projection language
  and the simplest norm decompositions, not for the scalar identity.
  For a nonorthogonal involution, use the primal projector
  \((I-R)/2\) and its transpose on covectors, or choose an
  \(R\)-invariant inner product.  General non-involutive group actions do
  not satisfy the two-point formula without an appropriate representation
  projection and group averaging.

## 6. Finite and compact orthogonal symmetry groups

The involution theorem is the two-element case of a clean compact-group
identity.  Let a finite or compact group \(\mathcal G\) act orthogonally on
the variable space, and let
\[
 P_0=\int_{\mathcal G}g\,d\nu(g)
\tag{G1}
\]
be its Reynolds projector, with normalized counting measure in the finite
case and normalized Haar measure in the compact case.  Then \(P_0\) is the
orthogonal projector onto the fixed subspace
\[
 \operatorname{Fix}(\mathcal G)=\{v:gv=v\text{ for every }g\in\mathcal G\}.
\]
Put
\[
 x_0=P_0x,\qquad x_\perp=(I-P_0)x.
\tag{G2}
\]

Assume that the open convex domain \(\Omega\) is
\(\mathcal G\)-invariant.  Then \(x_0\in\Omega\).  Indeed, the orbit
\(\{gx:g\in\mathcal G\}\) is compact and contained in \(\Omega\), and its
closed convex hull is a compact subset of \(\Omega\); in finite dimension
this also follows directly from Carathéodory's theorem.  The Haar average
\(x_0\) lies in that convex hull.  Hence the full segment
\[
                       x_0+t x_\perp,\qquad 0\le t\le1,
\tag{G3}
\]
lies in \(\Omega\).  This domain check is essential; without convexity,
the Reynolds average or the segment can leave the barrier domain.

Assume \(F(gx)=F(x)\), \(gc=c\) for every \(g\), and use the stationarity
convention
\[
                         A^Ty=c+\mu\nabla F(x).
\tag{G4}
\]
Define the coordinate-free nontrivial-representation source
\[
                         r_\perp=Ax_\perp.
\tag{G5}
\]

### Theorem 2 (compact-group central work)

If \(F\) is differentiable and convex, then
\[
 \boxed{
 r_\perp^Ty
 =\mu\langle x_\perp,\nabla F(x)\rangle
 =\mu\langle x_\perp,\nabla F(x)-\nabla F(x_0)\rangle
 \ge0.}
\tag{G6}
\]
If \(F\in C^2(\Omega)\), then exactly
\[
 \boxed{
 r_\perp^Ty
 =\mu\int_0^1
 \left\langle x_\perp,
 \nabla^2F(x_0+t x_\perp)x_\perp\right\rangle\,dt.}
\tag{G7}
\]

#### Proof

The invariant objective vector \(c\) lies in
\(\operatorname{Fix}(\mathcal G)\), so
\(\langle x_\perp,c\rangle=0\).  Pairing (G4) with \(x_\perp\) gives the
first equality in (G6).  Since \(x_0\) is fixed, gradient equivariance gives
\[
 g\nabla F(x_0)=\nabla F(gx_0)=\nabla F(x_0)
\]
for every \(g\).  Thus \(\nabla F(x_0)\) is fixed and orthogonal to
\(x_\perp\), proving the second equality.  Convex-gradient monotonicity
between \(x_0\) and \(x\) proves nonnegativity.  The fundamental theorem of
calculus along (G3) proves (G7). \(\square\)

If the integrated Hessian on the nontrivial representation space has
eigenvalues in \([m_\perp,M_\perp]\), then
\[
 \mu m_\perp\|x_\perp\|^2
 \le r_\perp^Ty
 \le\mu M_\perp\|x_\perp\|^2.
\tag{G8}
\]
For a self-concordant barrier, if
\(\delta=\|x_\perp\|_{x_0}<1\), the same chord comparison as in (16)
gives
\[
 \mu\left(1-\delta+\frac{\delta^2}{3}\right)\delta^2
 \le r_\perp^Ty
 \le\frac{\mu}{1-\delta}\delta^2.
\tag{G9}
\]

For \(\mathcal G=\{I,R\}\), one has
\(P_0=(I+R)/2\) and \(x_\perp=(x-Rx)/2\).  Equation (G6), together with
gradient equivariance, is exactly (1).

### Newton analogue

Let \(x^0\) be fixed by \(\mathcal G\), and let \(G_0\succ0\) commute with
the group action.  This holds for
\(G_0=\mu\nabla^2F(x^0)\).  Suppose
\[
 A\Delta x=r_p,\qquad
 G_0\Delta x-A^T\Delta y=h_0,
\tag{G10}
\]
where \(h_0\) is group-fixed.  Put
\(\Delta x_\perp=(I-P_0)\Delta x\).  The fixed and nontrivial
representation spaces are orthogonal, and \(G_0\) preserves them.  Pairing
the stationarity equation with \(\Delta x_\perp\) gives
\[
 \boxed{
 (A\Delta x_\perp)^T\Delta y
 =\Delta x_\perp^TG_0\Delta x_\perp\ge0.}
\tag{G11}
\]
An unresolved nontrivial-component forcing adds
\(-\langle\Delta x_\perp,h_\perp\rangle\), so positivity then need not hold.
Also, the numerical primal residual \(r_p=A\Delta x\) determines
\(A\Delta x_\perp\) only when the constraint representation separates the
fixed and nontrivial variable subspaces.

### Examples

1. **Permutation representations.**  If \(\mathcal G\) permutes coordinates,
   \(P_0x\) replaces the coordinates on every group orbit \(O\) by their
   orbit average \(\bar x_O\).  For the logarithmic barrier on the positive
   orthant,
   \[
   r_\perp^Ty
   =\mu\sum_O\left(\bar x_O\sum_{i\in O}\frac1{x_i}-|O|\right)\ge0,
   \tag{G12}
   \]
   with nonnegativity also following from arithmetic--harmonic mean.
   The objective must be constant on each orbit.

2. **Simplex symmetry.**  For the full permutation group on
   \(\{x>0:\mathbf1^Tx=1\}\),
   \(P_0x=\mathbf1/n\), and (G12) becomes
   \[
   r_\perp^Ty
   =\mu\left(\frac1n\sum_{i=1}^n\frac1{x_i}-n\right)\ge0.
   \tag{G13}
   \]
   Formally one may work in the positive orthant with
   \(\mathbf1^Tx=1\) as an equality; that symmetric row contributes zero
   to \(r_\perp\).  Alternatively, interpret openness and Hessians relative
   to the simplex affine hull.

3. **Rotation representations.**  Let \(SO(k)\) act on a block \(z\) and
   trivially on the remaining variables.  Then \(P_0z=0\).  For the unit-ball
   barrier \(F(z)=-\log(1-\|z\|^2)\),
   \[
   r_\perp^Ty
   =\frac{2\mu\|z\|^2}{1-\|z\|^2}.
   \tag{G14}
   \]
   A group-invariant linear objective has no component in this rotation
   block.

### Row mixing and scope

The compact-group identity retains the same row-basis invariance as (24).
For \(A'=UA\) and \(y'=U^{-T}y\),
\[
 r_\perp'=A'x_\perp=Ur_\perp,\qquad
 (r_\perp')^Ty'=r_\perp^Ty.
\tag{G15}
\]
Thus mixed constraint rows and nonunique multipliers are harmless for the
pairing.  They can make \(r_\perp\) impossible to recover from the total
numerical right-hand side \(b=Ax\) without knowing the representation
decomposition.

For a fixed constant-dimensional group action, or a block-diagonal family
of constant-size local actions, \(P_0\) is a fixed public local map.  The
theorem therefore subsumes signed pairs, constant-size permutation encodings,
and constant-dimensional rotation encodings without changing their raw
input access model.  For a large or implicitly specified group, applying
the Reynolds projector may itself be dense or computationally expensive;
the identity is algebraic and does not grant that operation for free.

Finally, arbitrary orthogonal edge holonomy is not a global symmetry action
of this kind.  Edge-dependent transports around inconsistent cycles need not
arise from one representation of one group acting simultaneously on the
whole variable space, and there may be no single public Reynolds projector
whose complement tracks their local sources.  Such systems require the
signed/gain incidence and holonomy analysis separately; (G6) gives no
cut-local conservation theorem for them.

## Literature and novelty calibration

The theorem, constants, sign convention, Newton analogue, multiplier
nonuniqueness, and row-mixing invariance have been checked symbolically.  The
following components are established mathematics, not novelty claims.

- The divergence introduced by Bregman,
  [*The relaxation method of finding the common point of convex sets and its
  application to the solution of problems in convex
  programming*](https://doi.org/10.1016/0041-5553(67)90040-7),
  satisfies
  \[
  D_F(u,v)+D_F(v,u)
  =\langle u-v,\nabla F(u)-\nabla F(v)\rangle.
  \]
  This is the standard symmetrized Bregman divergence; see also
  Nielsen--Nock,
  [*On the Centroids of Symmetrized Bregman
  Divergences*](https://arxiv.org/abs/0711.3242).
  Thus (1) and (10a) are a symmetry-specialized Bregman identity, not a new
  convex-analysis divergence.  More generally, (G6) is exactly
  \[
  r_\perp^Ty
  =\mu\{D_F(x,x_0)+D_F(x_0,x)\},
  \]
  because \(x_0=P_0x\) and
  \(\langle x-x_0,\nabla F(x_0)\rangle=0\).
- Gradient equivariance, invariant fixed subspaces, Reynolds averaging, and
  decomposition into representation blocks are standard symmetry-reduction
  tools.  Palais'
  [*Principle of symmetric
  criticality*](https://doi.org/10.1007/BF01941322)
  is a classical variational reference.  For convex and semidefinite
  optimization, see Vallentin,
  [*Symmetry in semidefinite programs*](https://arxiv.org/abs/0706.4233).
  For symmetry and irreducible decomposition of self-scaled barriers, see
  Hauser--Güler,
  [*Self-scaled barrier functions on symmetric cones and their
  classification*](https://arxiv.org/abs/math/0103196).
- For \(F(X)=-\log\det X\), the directed Bregman divergence is the LogDet
  divergence or Stein loss.  Its two-direction sum in (16c) is the standard
  symmetrized LogDet/Jeffreys form
  \(\operatorname{tr}(XY^{-1}+YX^{-1}-2I)\); see Cichocki--Cruces--Amari,
  [*Log-Determinant Divergences
  Revisited*](https://doi.org/10.3390/e17052988).
  It should not be confused with the distinct Jensen--Bregman LogDet
  or S-divergence.
- The integrated-Hessian forms, the Hessian comparison in (16), and the
  Newton identity are respectively the fundamental theorem of calculus,
  standard self-concordant local-norm comparison, and KKT virtual-work
  algebra.  Row-basis covariance is the elementary invariance of a
  primal--dual pairing under \(r\mapsto Ur\), \(y\mapsto U^{-T}y\).

The contribution claimed here should therefore be narrow: one
row-mixing-invariant formulation that identifies exactly which
nontrivial-representation source must be charged, together with its use as
an obstruction template for sparse QIPM gadgets.  A targeted open-literature
search through 2 September 2026 found no source making that QIPM
gadget-design use.  This is evidence, not proof of priority; the general
identity itself should not be presented as new.
