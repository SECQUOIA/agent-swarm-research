# Two anchored branches make the free SDP optimizer parity-dependent

Date: 2026-09-02

## Main result

There is a linear-size sparse product-SDP family whose feasible set is
linearly isomorphic to the genuinely non-SOCP cone \(\mathbb S_+^3\), whose
free root optimizer and spectrum depend on parity, and whose reduced
log-det Hessian has constant condition number on the whole central path.
Preparing the trace-normalized primal central matrix to constant trace
distance requires a linear number of raw coefficient queries.

The construction improves on a fixed-affine-loading obstruction.  After
eliminating its copy constraints, the optimization problem itself is

\[
 \min_{Z\succeq0}\ \langle C_h,Z\rangle,
 \qquad
 C_h=B+c_hE,
 \qquad h=\prod_{i=1}^N\sigma_i,
\tag{1}
\]

where

\[
 B=\operatorname{Diag}(1,2,1),\qquad
 E=e_1e_2^T+e_2e_1^T,
\tag{2}
\]
\[
 c_+=\frac54q,\qquad c_-=-\frac34q,\qquad
 q=\frac{16N}{33N+1}.
\tag{3}
\]

The two effective costs have different spectra because
\(|c_+|\ne|c_-|\).  Their central roots
\(Z_h(t)=tC_h^{-1}\) therefore cannot be related by the signed orthogonal
gauge or by any orthogonal similarity.  They also do not commute.

For all \(N\ge1\):

- the scalar equality matrix has row and column sparsity two, and one input
  bit controls only two fixed-position coefficient values;
- the primal and dual are strictly feasible and the unique primal optimum
  is zero;
- throughout \(0<t\le1\), all primal central entries and canonical tree-flow
  multipliers are \(O(1)\), while all dual-slack entries are \(O(1/P)\);
- the complete reduced Hessian satisfies
  \[
  \kappa_2(H_{\rm red})=\kappa_2(C_h)^2<\frac{49}{4};
  \]
- one fixed density observable recovers \(h\) with signed expectation larger
  than \(1/15\); hence constant-trace-distance central-density preparation
  requires \(\Omega(N)=\Omega(P)\) raw coefficient queries.

Here \(P=33N+1\) is the number of \(3\times3\) PSD blocks.  The construction
is still an output theorem, not a lower bound for returning the ordinary
optimal value, which is zero on every input.  Its parity-bearing centers lie
in a \(2\oplus1\) matrix subalgebra even though the free feasible cone is all
of \(\mathbb S_+^3\); this limitation is recorded explicitly below.

## 1. Sparse congruence tree

Let \(\sigma_1,\ldots,\sigma_N\in\{\pm1\}\), and put

\[
 K=16N,\qquad P=1+N+2K=33N+1,\qquad
 \mu_0=\frac1P,\qquad q=\frac KP.
\tag{4}
\]

The block graph has:

- a root \(r\);
- a signed chain \(p_1,\ldots,p_N\) starting at \(r\);
- an identity output chain \(o_1,\ldots,o_K\) starting at \(r\); and
- an identity cost-amplifier chain \(a_1,\ldots,a_K\) starting at \(p_N\).

Thus every graph vertex has degree at most two.  Put

\[
 D_\sigma=\operatorname{Diag}(\sigma,1,1).
\tag{5}
\]

For every edge from a parent block \(X_u\) to a child block \(X_v\), impose

\[
 X_v=
 \begin{cases}
  D_{\sigma_i}X_uD_{\sigma_i},&v=p_i,\\
  X_u,&v=o_j\text{ or }v=a_j.
 \end{cases}
\tag{6}
\]

Equation (6) means six scalar equalities, one for each isometric-svec
coordinate.  Congruence by \(D_\sigma\) leaves the \(11,22,33,23\)
coordinates unchanged and multiplies the \(12,13\) coordinates by
\(\sigma\).  Hence each scalar row has exactly two nonzeros of magnitude
one.  A scalar block coordinate occurs in at most two rows because the block
graph has maximum degree two.  The support is public.  At signed edge \(i\),
only the two values in the \(12\) and \(13\) copy rows depend on
\(\sigma_i\), so a raw coefficient query uses at most one query to that bit.

Let

\[
 \tau_i=\prod_{j=1}^i\sigma_j,\qquad h=\tau_N.
\]

Eliminating (6) gives

\[
 X_r=Z,\qquad
 X_{p_i}=D_{\tau_i}ZD_{\tau_i},\qquad
 X_{o_j}=Z,\qquad
 X_{a_j}=D_hZD_h.
\tag{7}
\]

Therefore the feasible cone is linearly isomorphic to
\(\mathbb S_+^3\).  It is strictly feasible, for example by taking \(Z=I\).
The equality operator has rank \(6(P-1)\), leaving the full six-dimensional
root tangent space.

## 2. Two public cost anchors and exact elimination

Every block receives the baseline cost \(\mu_0B\).  In addition:

\[
 C_{o_j}=\mu_0\left(B+\frac14E\right),
 \qquad
 C_{a_j}=\mu_0(B+E),
\tag{8}
\]

while the root and signed-chain blocks have cost \(\mu_0B\).  All these
local costs are positive definite:

\[
 \det B_{1:2,1:2}=2,\quad
 \det(B+E/4)_{1:2,1:2}=\frac{31}{16},\quad
 \det(B+E)_{1:2,1:2}=1.
\tag{9}
\]

Thus \(y=0\) is a strictly dual-feasible certificate.

Orthogonal congruence preserves trace inner products.  Pulling all costs
back to the root in (7) gives

\[
 \begin{aligned}
 C_{\rm eff}(h)
 &=P\mu_0B
   +K\mu_0\frac14E
   +K\mu_0D_hED_h\\
 &=B+q\left(\frac14+h\right)E
 =B+c_hE.
 \end{aligned}
\tag{10}
\]

This proves (1)--(3).  Since \(q<16/33\),

\[
 |c_h|\le c_+<\frac{20}{33}<\frac23.
\tag{11}
\]

The eigenvalues of the leading \(2\times2\) block of \(C_h\) are

\[
 \lambda_\pm(c_h)
 =\frac{3\pm\sqrt{1+4c_h^2}}2.
\tag{12}
\]

Together with the third eigenvalue one, (11) gives

\[
 \frac23<\lambda_{\min}(C_h)
 \le1\le\lambda_{\max}(C_h)<\frac73,
 \qquad
 \kappa_2(C_h)<\frac72.
\tag{13}
\]

In particular \(C_h\succ0\).  The unique primal optimum is \(Z=0\), hence
every original block is zero and the optimum value is zero.

### Why two anchors are necessary

With only the signed endpoint cost, the effective matrices would be
\(B_0+qhE\) for a diagonal \(B_0\).  They obey

\[
 B_0-qE=D_{-1}(B_0+qE)D_{-1},
\]

so their centers are merely signed-gauge copies with identical spectra.
The root-copy anchor contributes the fixed \(qE/4\).  Consequently

\[
 |c_+|=\frac54q\ne\frac34q=|c_-|,
\tag{14}
\]

and

\[
 \det C_+=2-c_+^2\ne2-c_-^2=\det C_-.
\tag{15}
\]

Thus the free optimization and its central spectrum genuinely depend on
parity after the public elimination (7).  Moreover

\[
 [C_+,C_-]=(c_--c_+)[B,E]\ne0.
\tag{16}
\]

Since two invertible matrices commute if and only if their inverses commute,
\(C_+^{-1}\) and \(C_-^{-1}\) also do not commute.

## 3. Exact central path and bounded KKT data

After elimination, the primal log-det barrier objective at parameter
\(\mu>0\) is

\[
 \langle C_h,Z\rangle-P\mu\log\det Z.
\tag{17}
\]

Put \(t=\mu/\mu_0=P\mu\).  Its unique center is

\[
 \boxed{
 Z_h(t)=tC_h^{-1}
 =t\left[
 \frac1{2-c_h^2}
 \begin{pmatrix}
  2&-c_h&0\\
  -c_h&1&0\\
  0&0&0
 \end{pmatrix}
 +e_3e_3^T
 \right].}
\tag{18}
\]

All original primal centers follow from (7).  Each central dual slack is

\[
 \boxed{
 S_v(t)=\mu X_v(t)^{-1}
 =\mu_0Q_vC_hQ_v,}
\tag{19}
\]

where \(Q_v\) is \(I,D_{\tau_i}\), or \(D_h\) according to (7).
The slacks and the equality multipliers below are independent of \(t\).
Every block satisfies \(X_vS_v=\mu I_3\), and the central gap is
\(3P\mu=3t\).

For \(0<t\le1\), (13) gives

\[
 \|X_v(t)\|_{\rm op}<\frac32,\qquad
 \max_{a,b}|(S_v)_{ab}|\le\frac2P.
\tag{20}
\]

It remains to check that stationarity can be satisfied without large hidden
multipliers.  Orient every tree edge away from the root and write its matrix
constraint as

\[
                         X_v-Q_eX_uQ_e=0.
\tag{21}
\]

Let

\[
                         G_v=C_v-S_v.
\tag{22}
\]

For an edge \(e=(u,v)\), define the multiplier in the child frame by the
subtree sum

\[
 Y_e=\sum_{w\in{\rm subtree}(v)}
       Q_{v\to w}G_wQ_{v\to w},
\tag{23}
\]

where \(Q_{v\to w}\) is the product of edge congruences along the unique
path.  At a nonroot vertex, (23) gives

\[
 Y_{\rm in}-\sum_{e\ {\rm out}}Q_eY_eQ_e=G_v.
\tag{24}
\]

At the root, the same equation follows from

\[
 \sum_vQ_vG_vQ_v
 =C_{\rm eff}(h)-P\mu_0C_h=0.
\tag{25}
\]

Thus (23) is an exact dual multiplier certificate under the convention
\(S=C-\mathcal A^*y\).

All multipliers are uniformly bounded.  Indeed,

\[
 \|C_v\|_F\le\mu_0\|B+E\|_F=\sqrt8\,\mu_0,
 \qquad
 \|S_v\|_F=\mu_0\|C_h\|_F<\sqrt7\,\mu_0.
\]

Congruence by every \(Q_{v\to w}\) is orthogonal, so (23) yields

\[
                         \boxed{\|Y_e\|_F<6}
\tag{26}
\]

for every edge.  Consequently every scalar svec multiplier has magnitude
less than six, and the complete multiplier vector has norm \(O(\sqrt P)\).
Together, (20) and (26) prove bounded full KKT coordinates on the late tail.

## 4. Complete reduced Hessian

For \(H\in\mathbb S^3\), the corresponding feasible tangent is

\[
 \mathcal L_h(H)=(Q_vHQ_v)_{v\in V}.
\tag{27}
\]

Because every \(Q_v\) is orthogonal,

\[
 \|\mathcal L_h(H)\|_F^2=P\|H\|_F^2.
\tag{28}
\]

Let \(H_1,\ldots,H_6\) be any Frobenius-orthonormal basis of
\(\mathbb S^3\).  Then
\(W_j=P^{-1/2}\mathcal L_h(H_j)\) is an orthonormal basis of the complete
feasible tangent space.  The reduced barrier Hessian in this basis is

\[
 \boxed{
 (H_{\rm red})_{ij}
 =\frac{\mu_0^2}{\mu}
   \operatorname{tr}(C_hH_iC_hH_j).}
\tag{29}
\]

The congruence operator \(H\mapsto C_hHC_h\) on \(\mathbb S^3\) has
eigenvalues \(\lambda_i(C_h)\lambda_j(C_h)\), \(i\le j\).  Therefore

\[
 \boxed{
 \kappa_2(H_{\rm red})
 =\kappa_2(C_h)^2<\frac{49}{4}.}
\tag{30}
\]

This bound holds for every \(\mu>0\).  The eigenvalue scale changes as
\(\mu_0^2/\mu\), but its condition number does not.

## 5. Density-state query lower bound

The central blocks in (7) are all orthogonal congruences of \(Z_h(t)\), so
they have a common trace.  Define

\[
 \rho_\sigma(t)=
 \frac{\bigoplus_{v\in V}X_v(t)}
      {P\operatorname{tr}Z_h(t)}.
\tag{31}
\]

On each of the \(K\) root-copy output blocks, use the fixed local observable
\(-E\), and use zero on all other blocks.  Their direct sum \(O\) is a
Hermitian contraction because \(\|E\|_{\rm op}=1\).  From (18),

\[
 \operatorname{tr}Z_h(t)
 =t\,\frac{5-c_h^2}{2-c_h^2},
\qquad
 -\operatorname{tr}(EZ_h(t))
 =t\,\frac{2c_h}{2-c_h^2}.
\tag{32}
\]

Hence

\[
 \boxed{
 h\operatorname{tr}(O\rho_\sigma(t))
 =q\,\frac{2h c_h}{5-c_h^2}.}
\tag{33}
\]

The smaller case is \(h=-1\), where \(h c_h=3q/4\).  Since
\(q\ge8/17\),

\[
 h\operatorname{tr}(O\rho_\sigma(t))
 \ge
 \frac{3q^2/2}{5-9q^2/16}
 \ge\frac{96}{1409}
 >\frac1{15}.
\tag{34}
\]

The bound is independent of \(t\).  The binary POVM
\((I\pm O)/2\) therefore recovers parity with advantage greater than
\(1/30\).  If a prepared state is within trace distance \(1/100\) of
\(\rho_\sigma(t)\), the advantage remains greater than
\(1/30-1/100>0\).

Use coherent fixed-position sparse access to the equality coefficients and
public costs.  Every coefficient query is simulated with at most one query
to one \(\sigma_i\); only two values on signed edge \(i\) depend on that bit.
Composing a central-density preparation algorithm with the fixed POVM
therefore computes parity.  The quantum parity lower bound implies

\[
 \boxed{\Omega(N)=\Omega(P)}
\tag{35}
\]

raw coefficient queries for constant-trace-distance preparation at every
fixed public central parameter \(t>0\).  This is linear in the density
matrix dimension \(3P\), the scalar conic dimension \(6P\), and the number
of scalar equalities \(6(P-1)\).

The claim is for unconditional output.  Postselection must include its
success probability and amplification cost.  Supplying a purification or
block encoding of the target state is a stronger input model and is outside
the lower bound.

## 6. Non-SOCP geometry and precise limitations

Projection of the feasible cone onto its root block is exactly
\(\mathbb S_+^3\), and (7) is its linear inverse.  Thus the feasible cone is
linearly isomorphic to \(\mathbb S_+^3\).  Fawzi proved that
\(\mathbb S_+^3\) has no lift over any finite product of second-order cones;
see
[*On representing the positive semidefinite cone using the second-order
cone*](https://arxiv.org/abs/1610.04901) and the
[journal version](https://doi.org/10.1007/s10107-018-1233-0).
Consequently this feasible cone is genuinely non-SOCP-representable.

The construction closes the main loophole in the earlier fixed-loading
family: parity remains in the eliminated cost \(C_h\), changes the spectrum
of the free root center, and is copied to a public output branch.  An
algorithm cannot prepare the requested root-copy density blocks merely by
solving one public Schur-complement problem and applying the old signed
affine embedding.

Several limitations remain.

1. **The ordinary optimum is trivial.**  It is zero for every input, and the
   optimal value is zero.  The lower bound concerns a specified central
   state, not approximate optimization value.
2. **The parity-bearing center uses a lower-rank subalgebra.**  Although the
   free feasible cone is all of \(\mathbb S_+^3\), \(C_h\) and \(Z_h(t)\)
   lie in the reducible algebra
   \(\mathbb S^2\oplus\mathbb R\).  The family proves that a genuinely
   non-SOCP free cone and its optimizer depend on the input; it does not
   prove that parity requires irreducible \(3\times3\) matrix interactions.
3. **The raw equality representation matters.**  If an oracle directly
   supplies \(h\), \(C_h\), \(Z_h\), or the target state, the parity reduction
   no longer applies.  The theorem charges the local signed-copy
   coefficients from which \(h\) must be computed.
4. **Only reduced conditioning is controlled.**  The path-like equality
   operator has small singular values.  Equation (30) concerns the complete
   equality-eliminated barrier Hessian, not the unreduced KKT matrix.
5. **No coordinate-change-invariant lower bound is claimed.**  The unequal
   spectra rule out the original orthogonal sign gauge, but arbitrary
   input-dependent preprocessing is covered only when its raw coefficient
   queries are charged.

## 7. Novelty calibration

The component facts are established.  Schur/congruence elimination and the
log-det central path are standard.  Fawzi's theorem supplies the exact
non-SOCP boundary.  Quantum parity has linear bounded-error query
complexity.  Sparse product-cone SDP and quantum-IPM output models are
discussed in, for example, Augustino, Nannicini, Terlaky, and Zuluaga,
[*Quantum Interior Point Methods for Semidefinite
Optimization*](https://doi.org/10.22331/q-2023-09-11-1110).

A targeted search found no primary source combining:

- a maximum-degree-two signed congruence representation;
- two public cost anchors that make the eliminated free SDP center's
  spectrum depend on parity;
- a genuinely non-SOCP \(\mathbb S_+^3\) feasible cone;
- bounded full KKT coordinates and constant complete reduced-Hessian
  condition number; and
- a linear raw-query lower bound for central-density preparation.

The defensible candidate novelty is this conjunction and the two-anchor
mechanism.  It should not be advertised as a lower bound for ordinary SDP
optimization, for the unreduced KKT solve, or for all equivalent output
representations.

## Status

The elimination, effective costs, spectrum, central path, tree-flow dual
certificate, reduced-Hessian condition bound, density bias, sparsity counts,
and raw-query reduction have been derived exactly.  The two-anchor
construction is sound and materially stronger than the fixed-affine-loading
family, subject to the limitations in Section 6.
