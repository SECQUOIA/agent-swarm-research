# Sparse block-SDP parity-state lower bound

Date: 2026-09-02

## Result

There is a linear-size product-cone SDP with \(P=17N+1\) real
\(2\times2\) PSD blocks and one scalar nonnegative cap such that:

- every constraint touches at most two cone blocks, every block participates
  in at most four constraints, and each input-dependent coefficient depends on
  one hidden bit;
- the primal optimum is unique, the primal and dual are strictly feasible, and
  the central primal blocks, dual multipliers, and dual slacks are bounded;
- at the common central parameter \(\mu_*=1/P\), the full reduced log-det
  Hessian has condition number at most \(17/15\);
- one copy of the normalized primal density matrix recovers parity with
  constant bias; hence preparing it to trace distance \(1/100\) requires
  \(\Omega(N)=\Omega(P)\) raw sparse-coefficient queries.

The construction is a genuine nonpolyhedral product-PSD slice, but the hard
central matrices commute and the parity mechanism is inherited from the paired
LP gadget. It is therefore an SDP-native extension, not a new intrinsically
noncommutative query lower bound. Exact condition one is available only after a
restriction that collapses the reduced slice to paired LP intervals. That
pinned-trace specialization nevertheless has a unique strictly complementary
optimum and gives the stronger uniform statement that, for every central
parameter (0<\nu\le 1/P), preparing the amplitude encoding of the complete
primal-dual central triple requires \(\Omega(P)\) raw coefficient queries.

## 1. Trace-normalized coordinates and construction

Use the real Pauli matrices

\[
 I=\begin{pmatrix}1&0\\0&1\end{pmatrix},\qquad
 X=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
 Z=\begin{pmatrix}1&0\\0&-1\end{pmatrix},
\]

and the trace inner product \(\langle U,V\rangle=\operatorname{tr}(UV)\).
Put

\[
 Q=I/2,\qquad J=X/2,
\]

so that every \(Y\in\mathbb S^2\) has the unique representation

\[
 Y=qI+dX+rZ,qquad
 q=\langle Q,Y\rangle,\quad d=\langle J,Y\rangle.         \tag{1}
\]

The factors \(1/2\) are essential: \(\langle J,Y\rangle=Y_{12}\), not
\(2Y_{12}\). In the standard isometric convention

\[
 \operatorname{svec}\!\begin{pmatrix}a&b\\b&c\end{pmatrix}
 =(a,\sqrt2b,c),                                          \tag{2}
\]

the vectors of \(Q,J\) both have Euclidean norm \(1/\sqrt2\).

Let hidden signs be \(\sigma_1,\ldots,\sigma_N\in\{\pm1\}\), put
\(K=16N\), \(P=N+K+1\), and define

\[
 a_i=\begin{cases}\sigma_i,&1\le i\le N,\\1,&N<i<P,\end{cases}
 \qquad
 \tau_0=1,\quad \tau_i=\prod_{j=1}^ia_j.                \tag{3}
\]

The primal variables are \(Y_0,\ldots,Y_{P-1}\succeq0\) and \(t\ge0\).
Write \(q_i=\langle Q,Y_i\rangle\), \(d_i=\langle J,Y_i\rangle\).
Impose

\[
 \begin{aligned}
 d_0&=1,&d_i-a_id_{i-1}&=0 &&(1\le i<P),\\
 &&q_i-q_{i-1}&=0 &&(1\le i<P),\\
 &&q_0+t&=8.&
 \end{aligned}                                            \tag{4}
\]

For

\[
 \mu_*={1\over P},\qquad
 c={4\over15P}-{1\over8P^2}>0,                           \tag{5}
\]

use the public symmetric cost

\[
             \min\ \sum_{i=0}^{P-1}\langle cI,Y_i\rangle. \tag{6}
\]

Exact feasibility fixes \(d_i=\tau_i\) and a common \(q_i=q\), while

\[
 Y_i=qI+\tau_iX+r_iZ,\qquad t=8-q.                       \tag{7}
\]

PSD feasibility is equivalent to

\[
 1\le q\le8,qquad r_i^2\le q^2-1.                      \tag{8}
\]

Thus the feasible set is compact. It is strictly feasible, for example at
\(q=4,r_i=0,t=4\). Since (6) equals \(2cPq\), its unique optimum is

\[
 q=1,qquad r_i=0,qquad t=7,qquad Y_i=I+\tau_iX.       \tag{9}
\]

The \(P\) pinned signed-difference rows in (4) are independent. The
\(P-1\) trace-propagation rows and the cap row are independent on the
\(q,t\) coordinates and are independent of the difference rows. Hence all
\(2P\) equality rows are independent. The cone dimension is \(3P+1\), so the
feasible tangent space has dimension \(P+1\).

Every row in (4) touches at most two blocks. A matrix block occurs in at most
two difference rows and two trace/cap rows. Each coefficient matrix has two
nonzero scalar entries and Frobenius norm \(1/\sqrt2\); all scalar coefficient
magnitudes and the cap RHS are bounded by eight. These are block-sparsity and
block-incidence bounds. In svec coordinates, every scalar coordinate also has
constant row and column incidence.

## 2. Exact central point and bounded dual certificate

For arbitrary \(\mu>0\), the log-det central objective on (7) is

\[
 2cPq-\mu\sum_{i=0}^{P-1}\log(q^2-1-r_i^2)-\mu\log(8-q).
                                                                    \tag{10}
\]

It is strictly convex on the feasible interior. Symmetry gives \(r_i=0\),
and the common \(q=q(\mu)\in(1,8)\) is the unique solution of

\[
 c={\mu q\over q^2-1}-{\mu\over2P(8-q)}.                \tag{11}
\]

At \(\mu=\mu_*\), (5) makes \(q=4\), so the exact common center is

\[
       Y_i^*=4I+\tau_iX,qquad t^*=4.                    \tag{12}
\]

All primal entries and eigenvalues are bounded absolute constants: the block
eigenvalues are three and five.

We next give the dual variables with all trace factors explicit. Use the
standard convention

\[
 S=C-\mathcal A^*y,\qquad s_t=c_t-\mathcal A_t^*y,
 \qquad S_iY_i=\mu I,quad s_tt=\mu.                     \tag{13}
\]

Let \(B_a\) be the lower-bidiagonal matrix for the first row family in (4),
so \(B_a d=e_0\). At (12),

\[
 S_i^*=\mu_*(Y_i^*)^{-1}
 ={1\over P}\left({4\over15}I-{\tau_i\over15}X\right),
 \qquad s_t^*={1\over4P}.                                \tag{14}
\]

For the difference-row multipliers \(y^d\), require

\[
 B_a^Ty^d={2\over15P}\tau.                              \tag{15}
\]

Because \(a_{i+1}\tau_{i+1}=\tau_i\), backward substitution gives

\[
             y_i^d={2(P-i)\over15P}\tau_i,qquad
             |y_i^d|\le{2\over15}.                      \tag{16}
\]

For the cap multiplier take \(y^{\rm cap}=-1/(4P)\). Give trace-propagation
row \(i\) the multiplier

\[
             y_i^q=-{P-i\over4P^2},qquad 1\le i<P.     \tag{17}
\]

The cap and propagation rows then contribute the coefficient
\(-1/(4P^2)\) times \(Q\) at every block. Since a scalar coefficient
\(zQ\) contributes \((z/2)I\), equations (5), (15), and (17) give exactly
(14) under (13). The scalar equation gives
\(s_t^*=-y^{\rm cap}=1/(4P)\). Thus the dual multipliers and slack entries are
bounded; in fact the slacks are \(O(1/P)\).

As a check on all factors, the primal central objective and dual objective are

\[
 \langle C,Y^*\rangle={32\over15}-{4\over P},
 \qquad
 b^Ty^*={2\over15}-{5\over P}.                           \tag{18}
\]

Their difference is \(2+1/P=(2P+1)\mu_*\), exactly the central gap for
\(P\) rank-two blocks and one rank-one scalar cone.

Strict dual feasibility also holds globally: choose a small negative cap
multiplier and zero difference/propagation multipliers. Then the scalar slack
and every matrix slack are positive definite. At the optimum, the blocks in
(9) have rank one and admit complementary rank-one slacks, while \(t=7>0\)
has zero optimum slack.

## 3. Full reduced log-det Hessian

At a central point \(Y_i=qI+\tau_iX\), the barrier Hessian is

\[
 H_\mu[U,V]
 =\mu\sum_i\operatorname{tr}(Y_i^{-1}U_iY_i^{-1}V_i)
   +\mu\,u_tv_t/t^2.                                     \tag{19}
\]

The signed-difference constraints kill every \(X\)-direction. The tangent
space has the following Frobenius-orthonormal basis:

\[
 W_i={1\over\sqrt2}Z\quad\hbox{in block }i
 \quad(0\le i<P),
 \qquad
 W_q={1\over\sqrt{2P+1}}(I,\ldots,I,-1).                \tag{20}
\]

The last coordinate in \(W_q\) is the scalar \(t\). Direct multiplication,
using \(ZXZ=-X\), gives

\[
 H_\mu[W_i,W_i]={\mu\over q^2-1},
 \qquad H_\mu[W_i,W_j]=0\ (i\ne j),
 \qquad H_\mu[W_i,W_q]=0,                               \tag{21}
\]

and

\[
 H_\mu[W_q,W_q]
 ={\mu\over2P+1}\left[
 {2P(q^2+1)\over(q^2-1)^2}+{1\over t^2}
 \right].                                                \tag{22}
\]

At (12), \(q=t=4\). Hence

\[
 \lambda_r={\mu_*\over15},
 \qquad
 \lambda_q={\mu_*\over2P+1}\left({34P\over225}+{1\over16}\right),
                                                                    \tag{23}
\]

and

\[
 1< {\lambda_q\over\lambda_r}
 ={34P/15+15/16\over2P+1}
 \le {17\over15}.                                       \tag{24}
\]

Thus the complete, unpreconditioned reduced log-det Hessian has condition
number at most \(17/15\) at \(\mu_*=1/P\). Its basis and eigenvalues are
input-independent.

The Hessian is not an exact scalar identity. Without the cap scalar, the two
eigenvalues are

\[
 {\mu\over q^2-1},qquad
 {\mu(q^2+1)\over(q^2-1)^2},                             \tag{25}
\]

whose difference is \(2\mu/(q^2-1)^2>0\). The cap changes only the public
radial eigenvalue and does not remove this structural split.

## 4. Density-matrix decoder and query lower bound

View the complete primal cone point as the density operator

\[
 \rho_\sigma={Y_0^*\oplus\cdots\oplus Y_{P-1}^*\oplus[t^*]
                  \over
                  \sum_i\operatorname{tr}Y_i^*+t^*}
 ={\bigoplus_i(4I+\tau_iX)\oplus[4]\over8P+4}.          \tag{26}
\]

This is trace normalization, not Frobenius-amplitude encoding. Let \(S\) be
the \(K=16N\) public copy nodes strictly after node \(N\), and define the
fixed Hermitian contraction

\[
 O=\bigoplus_{i=0}^{P-1}O_i\oplus[0],qquad
 O_i=\begin{cases}X,&i\in S,\\0,&i\notin S.\end{cases}  \tag{27}
\]

Since \(\operatorname{tr}(XY_i^*)=2\tau_N\) on \(S\),

\[
 \tau_N\operatorname{tr}(O\rho_\sigma)
 ={2K\over8P+4}={K\over4P+2}>{1\over5}\qquad(N\ge2).   \tag{28}
\]

The binary POVM \(E_\pm=(I\pm O)/2\) therefore returns parity with advantage
greater than \(1/10\). Trace distance \(1/100\) decreases this advantage by at
most \(1/100\), leaving a fixed positive constant.

Use coherent fixed-position sparse access to the constraint matrices, RHS,
and cost. The support pattern is public. A difference transition contains the
only input-dependent value, \(-a_iJ\). A row, block, svec-position, or value
query is simulated with at most one query to \(\sigma_i\); a block column has
at most one input-dependent outgoing transition. No global batch or
input-dependent state oracle is supplied.

Consequently, any quantum algorithm whose unconditional output \(\widetilde
\rho\) satisfies

\[
                 D_{\rm tr}(\widetilde\rho,\rho_\sigma)\le1/100             \tag{29}
\]

uses \(\Omega(N)=\Omega(P)\) raw sparse-coefficient queries. Compose the
algorithm with (27), repeat a constant number of times, and apply the quantum
parity lower bound. Arbitrary preprocessing, preconditioning, interior-point
iterations, and recovery are covered when every input-dependent primitive is
expanded into raw coefficient queries.

## 5. Is the construction genuinely semidefinite?

Yes at the level of the feasible cone slice, but only partially at the level
of the hardness mechanism. Eliminating (4) gives

\[
 \{(q,r_0,\ldots,r_{P-1}):
   1\le q\le8, r_i^2\le q^2-1\ \forall i\}.              \tag{30}
\]

This set has curved boundary and is not a polyhedron or a linear image of an
orthant slice. The free matrices
\(qI+\tau_iX+r_iZ\) do not lie in one simultaneously diagonalizable
subalgebra as \(r_i\) varies. Thus (4) is a genuine product of rank-two
symmetric cones, equivalently a coupled SOCP/\(2\times2\)-PSD formulation,
not merely diagonal nonnegativity written in matrix notation.

However, the hard centers have \(r_i=0\) and all lie in the commuting algebra
\(\operatorname{span}\{I,X\}\). The decoder (27) reads that commuting
orientation. The \(\Omega(P)\) reduction therefore does not establish a
specifically noncommutative source of quantum hardness.

There are two tempting ways to force exact condition one, and both lose the
genuine cone geometry:

1. Constraining every \(r_i=0\) leaves only the common \(q\)-ray. A public
   Hadamard rotation diagonalizes every block as
   \(\operatorname{diag}(q+\tau_i,q-\tau_i)\), exactly a paired LP embedding.
2. Pinning \(q=q_0\) removes the radial mode and leaves the \(r_i\)-Hessian
   scalar. But PSD feasibility becomes the product of intervals
   \(-\sqrt{q_0^2-1}\le r_i\le\sqrt{q_0^2-1}\), and

   \[
    \det Y_i=(\sqrt{q_0^2-1}+r_i)
              (\sqrt{q_0^2-1}-r_i),                     \tag{31}
   \]

   so the reduced log-det barrier is again the paired logarithmic LP barrier.

Equation (24), rather than exact scalarity, is the strongest claim supported by
this genuine shared-trace construction. The family is potentially useful as an
SDP/product-cone output-interface lower bound with nearly scalar geometry. It
should not be advertised as the first noncommutative parity lower bound or as
a hardness theorem for a supplied block encoding of \(\rho_\sigma\).

## 6. Exact condition-one pinned-trace specialization

There is a stronger condition-one variant with a unique optimum and bounded
data. As anticipated in item 2 above, its reduced feasible set is a product of
intervals, so it must be classified as an SDP representation of a paired LP
rather than genuinely semidefinite hardness.

Let

\[
                         F={X\over\sqrt2}.                \tag{32}
\]

For each block write

\[
       Y_i=2I+\tau_iX+r_iZ
       =\begin{pmatrix}2+r_i&\tau_i\\\tau_i&2-r_i\end{pmatrix}.             \tag{33}
\]

Use the \(P\) normalized difference constraints

\[
 \langle F,Y_0\rangle=\sqrt2,qquad
 \langle F,Y_i\rangle-a_i\langle F,Y_{i-1}\rangle=0,     \tag{34}
\]

and propagate the trace with

\[
 \langle I,Y_0\rangle=4,qquad
 \langle I,Y_i-Y_{i-1}\rangle=0.                         \tag{35}
\]

Here (34)--(35) contain \(2P\) independent rows. In svec coordinates,
\(F\) is the unit off-diagonal coordinate, a trace-difference row has four
nonzeros, and every scalar column occurs in at most two rows. The public RHS
has exactly two nonzero entries, so

\[
                         \|b\|_2=\sqrt{2+16}=\sqrt{18}.   \tag{36}
\]

Fix \(\mu_0=1/P\) and use the parity-invariant diagonal cost

\[
                  C_i=\mu_0I-\frac{\mu_0}{2}Z.           \tag{37}
\]

Conjugation by \(Z\) flips the hidden off-diagonal orientation and fixes this
cost. On the feasible slice, PSD is equivalent to

\[
                         -\sqrt3\le r_i\le\sqrt3,         \tag{38}
\]

and the nonconstant objective is \(-\mu_0\sum_i r_i\). Hence the unique
optimum has \(r_i=\sqrt3\) for every block.

At central parameter \(\nu>0\), every block has the same

\[
 r=r(\nu)=-{\nu\over\mu_0}
          +\sqrt{\left({\nu\over\mu_0}\right)^2+3},      \tag{39}
\]

because stationarity of
\(-\mu_0r-\nu\log(3-r^2)\) is

\[
                         \mu_0={2\nu r\over3-r^2}.        \tag{40}
\]

In particular, \(r(\mu_0)=1\), and

\[
 Y_i^0=\begin{pmatrix}3&\tau_i\\\tau_i&1\end{pmatrix},
 \qquad
 S_i^0=\mu_0(Y_i^0)^{-1}
 ={\mu_0\over2}\begin{pmatrix}1&-\tau_i\\-\tau_i&3\end{pmatrix}.         \tag{41}
\]

Both matrices have bounded entries; the primal eigenvalues are
\(2\pm\sqrt2\). At this center the trace-row multipliers vanish. If
\(B_a\) is the lower-bidiagonal matrix in (34), the difference multipliers
satisfy

\[
 B_a^Ty^d={\mu_0\over\sqrt2}\tau,qquad
 y_i^d={\mu_0(P-i)\over\sqrt2}\tau_i,                    \tag{42}
\]

and are bounded by \(1/\sqrt2\). The factor \(1/\sqrt2\) follows because a
coefficient \(zF\) contributes off-diagonal entry \(z/\sqrt2\).

The primal objective at (41) is three, while the dual objective is
\(\sqrt2y_0^d=1\). Their gap is two, exactly \(2P\mu_0\). This checks the
trace-pairing normalization.

At the optimum, the limiting complementary slack is

\[
 S_i^{\rm opt}={\mu_0\over2\sqrt3}
 \begin{pmatrix}2-\sqrt3&-\tau_i\\-\tau_i&2+\sqrt3\end{pmatrix}.            \tag{43}
\]

It has rank one and annihilates the rank-one optimum block. The required
difference coefficient is \(\mu_0\tau_i/\sqrt6\), and the common diagonal
coefficient in \(C_i-S_i^{\rm opt}\) is
\(\mu_0(1-1/\sqrt3)\). Backward substitution in the two propagation chains
therefore gives multipliers bounded respectively by \(1/\sqrt6\) and
\(1-1/\sqrt3\). Thus the unique optimum is strictly complementary, and all
relevant primal, dual, and slack coordinates are bounded. Strict primal and
dual feasibility are immediate from \(r_i=0\) and from \(y=0,S=C\succ0\).

### Scalar reduced Hessian

The Frobenius-orthonormal tangent basis is

\[
                    W_i={1\over\sqrt2}Z
                    \quad\hbox{in block }i.              \tag{44}
\]

For the log-det Hessian,

\[
 H_\nu[W_i,W_i]
 =\nu\,{3+r^2\over(3-r^2)^2},qquad
 H_\nu[W_i,W_j]=0\quad(i\ne j).                          \tag{45}
\]

It is therefore an exact scalar identity for every \(\nu>0\). At
\(\nu=\mu_0,r=1\), its common eigenvalue is exactly \(\mu_0\). This is the
unpreconditioned Frobenius geometry.

### Density-matrix and full-central-triple output

Trace normalization of the primal center gives

\[
                         \rho_\sigma^0={\bigoplus_iY_i^0\over4P}.           \tag{46}
\]

With \(O_i=X\) on the \(K\) output-copy blocks and zero elsewhere,

\[
        \tau_N\operatorname{tr}(O\rho_\sigma^0)
        ={2K\over4P}={K\over2P}>{2\over5}.                \tag{47}
\]

Thus one copy recovers parity with constant bias, and trace error \(1/100\)
preserves it. The raw sparse-query simulation from Section 4 applies, now with
the normalized coefficient \(F\); preparing (46) requires
\(\Omega(N)=\Omega(P)\) queries.

There is also a lower bound for the normalized amplitude encoding of the full
primal-dual central triple. For \(0<\nu\le\mu_0\), equation (39) gives
\(1\le r<\sqrt3\). From (40), the exact propagation multipliers are

\[
 \begin{aligned}
 y_i^q&=\mu_0(P-i)(1-1/r),\\
 y_i^d&={\mu_0(P-i)\over\sqrt2r}\tau_i,
 \end{aligned}                                            \tag{48}
\]

where \(y^q\) denotes the trace-row multipliers. The central slack is

\[
 S_i={\mu_0\over2r}
 \begin{pmatrix}2-r&-\tau_i\\-\tau_i&2+r\end{pmatrix}.   \tag{49}
\]

Let

\[
 |\Psi_\nu\rangle={
  (\operatorname{svec}Y,y^q,y^d,\operatorname{svec}S)
  \over
  \|(\operatorname{svec}Y,y^q,y^d,\operatorname{svec}S)\|_2}.        \tag{50}
\]

The three parts obey

\[
 \begin{aligned}
 \|\operatorname{svec}Y\|_2^2
   &=P(10+2r^2)<16P,\\
 \|(y^q,y^d)\|_2^2
   &=\left[(1-1/r)^2+{1\over2r^2}\right]
     {1\over P^2}\sum_{\ell=1}^P\ell^2
     \le {P\over2},\\
 \|\operatorname{svec}S\|_2^2
   &=P\,{\mu_0^2(5+r^2)\over2r^2}
     \le {3\over P}.
 \end{aligned}                                            \tag{51}
\]

For the middle inequality, the bracket is at most \(1/2\) on
\(1\le r\le\sqrt3\), and \(\sum_{\ell=1}^P\ell^2\le P^3\). Since this family
has \(P=17N+1\ge18\), the total squared norm in (50) is less than \(17P\).

In one primal svec block define

\[
 e_+=(1,0,1)/\sqrt2,qquad e_b=(0,1,0),qquad
 M=|e_+\rangle\langle e_b|+|e_b\rangle\langle e_+|.      \tag{52}
\]

This is a Hermitian contraction. Since
\(\operatorname{svec}Y_i=(2+r,\sqrt2\tau_i,2-r)\), its quadratic score is

\[
             (\operatorname{svec}Y_i)^TM
              (\operatorname{svec}Y_i)=8\tau_i.          \tag{53}
\]

Apply \(M\) on the primal coordinates of every output-copy block and zero on
all other coordinates of (50). Equations (51)--(53) give

\[
 \tau_N\langle\Psi_\nu|M_{\rm out}|\Psi_\nu\rangle
 >{8K\over17P}>{2\over5}.                                \tag{54}
\]

Thus preparing the complete central-triple amplitude state to trace distance
\(1/100\) also requires \(\Omega(P)\) raw queries uniformly on the central
tail \(0<\nu\le\mu_0\).

Finally, this exact-scalar family is LP reducible. Equation (38) is equivalent
to nonnegativity of \(z_i^\pm=\sqrt3\pm r_i\), and

\[
                       \det Y_i=z_i^+z_i^-.              \tag{55}
\]

The log-det barrier and linear cost are exactly those of a paired interval LP.
The density-matrix and full-triple output lower bounds are valid product-SDP
statements, but their mechanism is not genuinely nonpolyhedral or
noncommutative. The shared-trace construction in Sections 1--5 is the genuine
PSD variant; its price is the small spectral split (24).

Status: **construction and constants proved. The genuine shared-trace variant
has nearly scalar geometry; the pinned-trace variant has exact scalar geometry,
a unique strictly complementary optimum, and both density-matrix and complete
central-triple output lower bounds, but is paired-LP reducible. The parity and
commuting-center mechanism are inherited.**
